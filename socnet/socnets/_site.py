import requests
import json
import feedparser
from datetime import datetime, date
from django.conf import settings

from socnet.gspread_utils import gspread_auth


logger = getattr(settings, 'LOGGER') 


def get_account_info(username):
    account_info_link = 'https://shtab.navalny.com/hq/map.json' 
    response = requests.get(account_info_link)
    j = json.loads(response.text)

    for shtab in j:
        print(username, j[shtab][0]['hqs'][0]['page'].split('/')[-2])
        if username == j[shtab][0]['hqs'][0]['page'].split('/')[-2]:
            return j[shtab][0]
    return None         


def get_account_feed(username, count=1):
    feed_link = 'https://shtab.navalny.com/hq/{}/feed'.format(username)
    response = requests.get(feed_link)
    account_feed = feedparser.parse(response.text)

    return account_feed  


def get_post(account_feed, offset = 0):
    entries = account_feed['entries']
    try: 
        post = entries[offset]
        return post
    except:
        return None  


def get_stats(posts):
    gc = gspread_auth()
    dj = gc.open("smm_dj").worksheet('shtabs')
    cell_list = dj.range('A16:C1030')
    for i in range(1000):
        try:
            cells = cell_list[i*3:(i+1)*3]
            try:
                post = posts.get(post_id = cells[1].value.strip('/'),
                                 page__feed_id = cells[0].value.strip('/')) 
            except:
                pass
            else:
                post.views = cells[2].value       
                post.save()
        except Exception as e:
            logger.error(' '.join(('get_stats_site', str(e))))     
        

def get_followers_count(account_info):
    return 0


def save_page(account_info):
    full_name = account_info['city']
    return full_name, None    


def get_latest_post_id(latest_post):
    latest_post_url = latest_post['guid']
    link_ending = latest_post_url.split('/')[-2]
    if link_ending.isdigit():
        post_id = link_ending[:50]
    else:
        post_id = latest_post['title']
    time = datetime(*latest_post['published_parsed'][:6])   

    return post_id, time, latest_post['title']    
    