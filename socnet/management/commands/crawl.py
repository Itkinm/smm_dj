from django.core.management.base import BaseCommand, CommandError
from socnet.models import Platform, Tguser, Page, Post
#from socnet.resources import PostResource

import telegram
import logging
from datetime import datetime, date, timedelta
import requests
import json
from django.conf import settings

import gspread
from oauth2client.service_account import ServiceAccountCredentials


from plotly.offline import iplot, init_notebook_mode
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio

import os


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Smm DJ-09f246eb8043.json', scope)

gc = gspread.authorize(credentials)



token = getattr(settings, 'TOKEN') 
bot = telegram.Bot(token)

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'log.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


apikey = getattr(settings, 'YOUTUBE_APIKEY') 


def stat_req(video_ids):
    stat_link = 'https://www.googleapis.com/youtube/v3/videos'
    payload = {'key': apikey, 
               'part': 'contentDetails,statistics,snippet',
               'id': video_ids,}    
    response = requests.get(stat_link, params=payload)
    stats = json.loads(response.text)   
    return stats           
    
"""
def get_stats(posts):
    for i in range(len(list(posts))//50+1):
        video_ids = ','.join(x.post_id for x in posts[i*50:(i+1)*50])
        stats = stat_req(video_ids)
        for item in stats['items']:
            post = posts.get(post_id = item['id'])
            post.likes = int(item['statistics']['likeCount'])
            post.views = int(item['statistics']['viewCount'])
            post.comments = int(item['statistics']['commentCount'])
            post.title = item['snippet']['title']
            post.description = item['snippet']['description']
            post.save()
"""

def handle_post(platform, page, l_p):
    try: 
        latest_post_id, time = get_latest_post_id[platform.name](l_p)
    except Exception as e:
        raise Exception('get_latest_post_id', e) 
    else:
        try:       
            post, created = Post.objects.get_or_create(
                post_id = latest_post_id,
                page = page,)   
            #post.title = l_p['title']
            #post.description = l_p['description']
            post.posted_on = time
            post.save()    
                       
        except Exception as e:
            raise Exception('create_post', e)    


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.db.models.functions import TruncDate
        from django.db.models import Count, Sum
        init_notebook_mode(connected=True)
        platform_posts = Post.objects.filter(page__platform = Platform.SI)
        span = date.today()-timedelta(days=45)
        recent_posts = platform_posts.filter(posted_on__gte = span)
        dates = recent_posts.annotate(date=TruncDate('posted_on'))
        counts= dates.values('date').annotate(count=Count('post_id')) 
        views = dates.values('date').annotate(views=Sum('views'))
        #print (list(counts))
        
        max_views = recent_posts.order_by('-views').values('title','views')
        #data = [go.Bar(
        #    x=[i['date'] for i in list(counts)],
        #    y=[i['count'] for i in list(counts)]
        #)]
        print (max_views)
        data = [go.Bar(
            x=[i['title'] for i in list(max_views)[10]],
            y=[i['views'] for i in list(max_views)[10]]
        )]

        fig = go.Figure(data=data)
        pio.write_image(fig, 'bar.png')
        bar = open('bar.png', 'rb')
        bot.send_photo(95856961, bar) 
        os.remove('bar.png')

"""        
        platform = Platform.objects.get(name = Platform.SI)
        posts = Post.objects.filter(
                page__in = platform.page_set.all(),
                posted_on__gte=date.today()-timedelta(days=30)
                )
        get_stats[platform.name](posts)
"""
"""
        dj = gc.open("smm_dj").sheet1
        posts = Post.objects.filter(posted_on__gte=date(2018, 6, 1))
        count = posts.count()

        cell_list = dj.range('A2:H{}'.format(count+1))
        
        print (count)
        for i in range(count):
            cells = cell_list[i*8:(i+1)*8]
            cells[0].value = posts[i].page.shtab.name
            cells[1].value = posts[i].page.platform.name
            cells[2].value = posts[i].url
            cells[3].value = str(posts[i].posted_on.date())
            cells[4].value = posts[i].views
            cells[5].value = posts[i].likes
            cells[6].value = posts[i].reposts
            cells[7].value = posts[i].comments

        dj.update_cells(cell_list)     
"""        
"""
        for platform in Platform.objects.filter(hook = True):
            for page in platform.page_set.all():
                try:
                    account_feed = get_account_feed[page.platform.name](page.feed_id, 50)
                except:
                    print (page)     
                else: 
                    for i in range(50):
                        try:
                            some_post = get_post[page.platform.name](account_feed, i)
                            handle_post(page.platform, page, some_post)
                        except Exception:
                            pass
"""                                       
"""        
        dj = gc.open("smm_dj").get_worksheet(1)
        #platform = Platform.objects.get(name = Platform.YT)
        posts = Post.objects.filter(page__platform = Platform.SI)
        count = posts.count()
        # Select a range
        cell_list = dj.range('A2:E{}'.format(count+1))
        
        #for page in Page.objects
"""        
"""
        print (count)
        for i in range(count):
            cells = cell_list[i*5:(i+1)*5]
            cells[0].value = posts[i].page.shtab.name
            cells[1].value = posts[i].page.platform.name
            cells[2].value = posts[i].url
            cells[3].value = str(posts[i].posted_on.date())
            #cells[4].value = posts[i].views
            #print (cells)        

        # Update in batch
        dj.update_cells(cell_list)
"""        
"""        
        platform = Platform.objects.get(name = Platform.SI)

        for page in Page.objects.filter(platform=platform):
            account_feed = get_account_feed[Platform.SI](page.feed_id, 50) 
            print (page)
            for some_post in account_feed['entries']:
                #print (some_post)
                handle_post(platform, page, some_post)
        #posts = Post.objects.filter(
        #        page__in = platform.page_set.all(),
        #        posted_on__gte=date(2018, 6, 4)
        #        )   
        #get_stats(posts) 

"""
"""        
        dj = gc.open("smm_dj").sheet1
        #platform = Platform.objects.get(name = Platform.YT)
        posts = Post.objects.filter(posted_on__gte=date(2018, 6, 4))
        count = posts.count()
        # Select a range
        cell_list = dj.range('A2:E{}'.format(count+1))
        
        
        print (count)
        for i in range(count):
            cells = cell_list[i*5:(i+1)*5]
            cells[0].value = posts[i].page.shtab.name
            cells[1].value = posts[i].page.platform.name
            cells[2].value = posts[i].url
            cells[3].value = str(posts[i].posted_on.date())
            cells[4].value = posts[i].views
            #print (cells)        

        # Update in batch
        dj.update_cells(cell_list)
"""


        #platform = Platform.objects.get(name = Platform.YT)
        #post_resource = PostResource()
        #queryset = Post.objects.filter(page__platform=platform, posted_on__gte=date(2018, 6, 4))
        #dataset = post_resource.export(queryset)
        #print(dataset.csv)
        #for page in Page.objects.filter(platform=platform):
        #    account_feed = get_account_feed[Platform.YT](page.feed_id, 50) 
            #print (account_feed)
        #    for some_post in account_feed['items']:
                #print (some_post)
        #        handle_post(platform, page, some_post)
        #posts = Post.objects.filter(
        #        page__in = platform.page_set.all(),
        #        posted_on__gte=date(2018, 6, 4)
        #        )   
        #get_stats(posts)        

