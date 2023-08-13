from django.core.management.base import BaseCommand, CommandError
from socnet.rss import *

from socnet.models import Tguser, Page, Platform, Post, Shtab
import logging
import requests
import json
import feedparser
from datetime import datetime, date


logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'log.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


def feed_handler(r, shtab):
    entries = r['entries']

    try: 
        latest_post = entries[0]
    except:
        return False    

    latest_post_url = latest_post['guid']  

    if latest_post_url == r['feed']['link']:
        post_no_link_handler(latest_post, shtab)
    else:
        post_with_link_handler(latest_post, shtab)

def determine_platform(account_link_start, link):
    if link.startswith(account_link_start):
        text = self.link.split('?')[0]
        username = text[len(account_link_start):].split('/')[0]
        return username
    raise ValueError('Not a valid link')   


class Command(BaseCommand):
    def handle(self, *args, **options):
        for shtab in Shtab.objects.exclude(url = None):
            try: 
                req = requests.get(shtab.url)
                pos = 0
                for i in range(req.text.count('social-item--')):
                    pos = req.text.index('social-item--', pos, len(req.text))
                    target = req.text.find('"', pos, len(req.text))
                    platform_name = req.text[pos+13:target].upper()
                    platform = Platform.objects.get(name = platform_name)
                    if platform.hook == True:
                        pos_link = req.text.index('href="', target, len(req.text))
                        target_link = req.text.find('" ', pos_link, len(req.text))
                        link = req.text[pos_link+6:target_link]
                        #print (link)
                        #print (pos, target, pos_link, target_link)
                        username = link.split('?')[0].strip('/').split('/')[-1]
                        try: 
                            page = Page.objects.get(
                                shtab = shtab, 
                                platform = platform)
                                                            
                        except Exception as e:  
                            page = Page.objects.create(
                                shtab = shtab, 
                                platform = platform,
                                username = username)
                            page.full_name, page.feed_id = save_page[platform_name](username)
                            page.save()
                            
                            #pass
                    pos += 1
            except Exception as e: 
                print (e)    
"""
        Page.objects.filter(platform__name = 'SITE').delete()
        for shtab in j:
            username = j[shtab][0]['hqs'][0]['page'].split('/')[-2]
            #print (username, j[shtab][0]['city'], Platform.objects.get(name = Platform.SI)) 
            page, created = Page.objects.get_or_create(
                username = username,
                shtab = Shtab.objects.get(name = j[shtab][0]['city']),
                platform = Platform.objects.get(name = Platform.SI))
            page.full_name, page.feed_id = save_page[Platform.SI](username)
            page.save()
"""     
"""
        for shtab in Shtab.objects.all():
            if shtab.url != None:
                feed = requests.get(shtab.url+'feed')
                r = feedparser.parse(feed.text)              
                has_posts = feed_handler(r, shtab)
"""    
"""
        for page in Page.objects.all():
            for post in page.post_set.all():
                if post != page.post_set.filter(post_id=post.post_id).order_by('-posted_on').first():
                    print (post)
                    post.delete()
"""                    
"""        
        for platform in Platform.objects.filter(hook = True):
            for shtab in Shtab.objects.all():
                if shtab.page_set.filter(platform=platform).count()>1:
                    print (shtab.name, platform.name)
"""

"""
        for vk_page in Page.objects.filter(platform = Platform.VK):
            city = vk_page.full_name.split('|')[1][1:]
            shtab, created = Shtab.objects.get_or_create(name = city)
            vk_page.shtab = shtab
            vk_page.save()
            for platform in Platform.objects.exclude(name = Platform.VK):
                for page in platform.page_set.all():
                    try:
                        if city[:-1] in page.full_name:
                            page.shtab = shtab
                            page.save()
                    except: 
                        print (page, page.full_name)      

"""