import re
from datetime import datetime, date, timedelta
import importlib

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings

from socnet.telegram_utils import format_post, send_messages 
from socnet.telegram_utils import send_zhdun, send_chart
#from socnet.plotly_utils import daily_pics

from constance import config

logger = getattr(settings, 'LOGGER') 


# Create your models here.  


class Tguser(models.Model):
    tg_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, 
                                on_delete=models.SET_NULL, 
                                null=True, 
                                default=None,
                                related_name='tguser',
                                blank = True)  
    def __str__(self):
        return str(self.tg_id)


class Platform(models.Model):
    IN = 'INSTAGRAM'
    VK = 'VK'
    TW = 'TWITTER'
    YT = 'YOUTUBE'
    TG = 'TELEGRAM'
    FB = 'FACEBOOK'
    OK = 'OK'
    SI = 'SITE'
    NAME_CHOICES = (
      ('INSTAGRAM', 'instagram'), 
      ('VK', 'vk'),
      ('TWITTER', 'twitter'),
      ('YOUTUBE', 'youtube'),
      ('TELEGRAM', 'telegram'),
      ('FACEBOOK', 'facebook'),
      ('OK', 'ok'),
      ('SITE', 'site'),
      )
    name = models.CharField(primary_key=True, 
                            max_length=10, 
                            choices = NAME_CHOICES, 
                            default = VK)
    account_link_start = models.CharField(max_length=50, 
                                          null=True, 
                                          default=None, 
                                          blank = True)
    post_link = models.CharField(max_length=50, 
                                 null=True, 
                                 default=None, 
                                 blank = True)
    post_form = models.TextField(max_length=100, 
                                 null=True, 
                                 default=None, 
                                 blank = True)
    channel = models.IntegerField(default=0)
    channel_link = models.URLField(max_length=100, 
                                    null=True, 
                                    default=None, 
                                    blank = True)
    datastudio_link = models.URLField(max_length=100, 
                                      null=True, 
                                      default=None, 
                                      blank = True)
    hook = models.BooleanField(default = True)
    stat = models.BooleanField(default = True)
    zhdun = models.BooleanField(default = False)
    zhdun_span = models.IntegerField(default=7)


    def get_platform_module(self):
        module_name = self.get_name_display().lower()
        module_path = 'socnet.socnets._{}'.format(module_name)
        module = importlib.import_module(module_path)
        return module


    def query_recent_posts(self, span=30):
        posts = Post.objects.filter(
            page__in = self.page_set.filter(shtab__is_open = True),
            posted_on__gte=date.today()-timedelta(days=span))
        return posts   


    def get_stats(self, span=config.STATS_UPDATE_DEFAULT_SPAN):
        module = self.get_platform_module()
        posts = self.query_recent_posts(span)
        try:
            module.get_stats(posts)
        except Exception as e:
            logger.error('get_stats: %s — %s', self.name, e)   


    def get_followers_counts(self):
        for page in self.page_set.filter(shtab__is_open = True):
            page.get_followers_count()                 


    def send_zhduns(self):
        shtabs = []
        for page in self.page_set.filter(shtab__is_open = True):
            try:
                span = self.zhdun_span
                if page.last_posted_on.date()<date.today()-timedelta(days=span):
                    shtabs.append(page.shtab.name)
            except Exception as e:
                logger.error(e)        
        send_zhdun(shtabs, self.channel, span)
        config.LAST_ZHDUN_RUN = datetime.utcnow() + timedelta(hours=3)


    def make_charts(self, span=14):
        posts = self.query_recent_posts(span) 
        #file_name = daily_pics(posts)
        send_chart(file_name, self.channel)

    def __str__(self):
        return str(self.name)



class Shtab(models.Model):
    name = models.CharField(max_length=30, null=True, default=None, blank = True)
    url = models.URLField(max_length=30, null=True, default=None, blank = True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)          



class Page(models.Model):
    username = models.CharField(max_length=100, default=None)
    platform = models.ForeignKey(Platform,on_delete=models.CASCADE,
                                 default=None, null=True)
    shtab = models.ForeignKey(Shtab, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=50, default=None,
                                 null=True, blank = True)
    feed_id = models.CharField(max_length=50, default=None, 
                               null=True, blank = True)
    notifs = models.ManyToManyField(Tguser, default=None, null=True, blank=True)


    def last_post(self):
        if self.post_set.all():
            return self.post_set.all().order_by('-posted_on').first()
        else:
            return None


    @property
    def last_post_id(self):
        try:    
            return self.last_post.post_id
        except:
            return None    


    @property
    def last_posted_on(self):
        try:    
            return self.last_post().posted_on
        except:
            return None 


    @property
    def followers_count(self):
        if self.pagestat_set.all():
            latest = self.pagestat_set.all().order_by('-date').first()
            return latest.followers_count
        else:
            return None              
                

    @property
    def url(self):
        try:
            return str(self.platform.account_link_start) + str(self.username)
        except:
            return 'link'    


    def get_account_info(self):
        module = self.platform.get_platform_module()
        try:
            return module.get_account_info(self.username)
        except Exception as e:
            logger.error('get_account_info: %s — %s', self.url, e)


    def get_account_feed(self, count):    
        module = self.platform.get_platform_module()
        try: 
            return module.get_account_feed(self.feed_id, count)
        except Exception as e:
            logger.error('get_account_feed: %s — %s', self.url, e)     


    def get_posts(self, offset=0):
        module = self.platform.get_platform_module() 
        account_feed = self.get_account_feed(offset+1)
        posts = []
        for i in range(offset+1):
            try:
                post = module.get_post(account_feed,i)
                posts.append(post)
            except Exception as e:
                logger.warning('get_posts: %s — %s', i, e)
        return posts 

           
    def get_latest_post_id(self):
        module = self.platform.get_platform_module()
        post = self.get_posts()[0]
        try:
            post_id, time, title = module.get_latest_post_id(post)
            return post, post_id, time, title
        except Exception as e:
            logger.error('latest_post_id: %s — %s', self.url, e)            


    def send_post(self, post, latest_post):
        post_text = format_post(self.platform.post_form, 
                                post.url, 
                                self.shtab.name, 
                                latest_post)
        send_messages(self.platform.channel, post_text, self.notifs.all())    


    def check_for_fresh_post(self):   
        try:
            latest_post, latest_post_id, time, title = self.get_latest_post_id()
            post, created = Post.objects.get_or_create(
                            post_id = latest_post_id,
                            page = self) 
            if created:
                post.posted_on = time
                post.title = title
                post.save()
                self.send_post(post, latest_post)
        except Exception as e:        
            logger.error('check_for_fresh_post: %s — %s', self.url, e)


    def get_followers_count(self):
        module = self.platform.get_platform_module()
        account_info = self.get_account_info()

        try:
            followers_count = int(module.get_followers_count(account_info))
        except Exception as e:
            logger.error('get_followers_count: %s — %s', self.url, e)   
        else:
            pagestat, created = Pagestat.objects.get_or_create(
                                date = date.today(),
                                page = self)
            pagestat.followers_count = followers_count
            pagestat.save()

            return followers_count


    __original_username = None

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        self.__original_username = self.username

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.username != self.__original_username:
            module = self.platform.get_platform_module()
            try:
                account_info = self.get_account_info()
                self.full_name, self.feed_id = module.save_page(account_info)
                if self.feed_id == None:
                    self.feed_id = self.username
            except Exception as e:
                self.username = str(e)[:100]
        super(Page, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_username = self.username        
    
    def __str__(self):
        try:
            return '{} {}'.format(self.shtab.name, self.platform.name)
        except:
            return str(self.full_name)              


class Post(models.Model):
    post_id = models.CharField(max_length=50, 
                               null=True, 
                               default=None, 
                               blank = True)
    posted_on = models.DateTimeField(null=True, 
                                     blank=True, 
                                     default=None)
    title = models.CharField(max_length=255, 
                             null=True, 
                             default=None, 
                             blank = True)
    #description = models.TextField(null=True, 
    #                               default=None, 
    #                               blank = True)
    page = models.ForeignKey(Page, 
                             on_delete=models.CASCADE, 
                             blank=True, 
                             null=True)
    views = models.IntegerField(null=True, 
                                default=None, 
                                blank = True)
    likes = models.IntegerField(null=True, 
                                default=None, 
                                blank = True)
    reposts = models.IntegerField(null=True, 
                                default=None, 
                                blank = True)
    comments = models.IntegerField(null=True, 
                                   default=None, 
                                   blank = True)


    @property
    def url(self):
        if re.match("^[A-Za-z0-9_-]*$", str(self.post_id)):
            post_part = str(self.post_id)
        else:
            post_part = ''    

        return self.page.platform.post_link.format(post_id=post_part,
                                                   feed_id=self.page.feed_id)

    def __str__(self):
        return str(self.post_id)


class Pagestat(models.Model):
    date = models.DateField(default=None)
    followers_count = models.IntegerField(null=True, blank=True, default=None)        
    page = models.ForeignKey(Page,on_delete=models.CASCADE,
                             default=None, null=True)


  
                        
