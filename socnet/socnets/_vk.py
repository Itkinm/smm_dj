import requests
import json
import random
from datetime import datetime, date

from django.conf import settings

service_keys = getattr(settings, 'VK_SERVICE_KEYS') 
service_key = random.choice(service_keys)

logger = getattr(settings, 'LOGGER') 


def get_account_info(username):
    account_info_link = 'https://api.vk.com/method/groups.getById'
    payload = {'group_ids': username, 
               'fields': 'members_count',
               'v': '5.65',
               'access_token': service_key}
    response = requests.get(account_info_link, params=payload)
    account_info = json.loads(response.text)
    return account_info


def get_account_feed(vk_group_id, count=1):
    feed_link = 'https://api.vk.com/method/wall.get'
    payload = {'owner_id': '-'+vk_group_id, 
               'count': count+1, 
               'v': '5.65', 
               'access_token': service_key}
    response = requests.get(feed_link, params=payload)
    account_feed = json.loads(response.text)

    return account_feed


def stat_req(posts_list):
    stat_link = 'https://api.vk.com/method/wall.getById'
    payload = {'posts': posts_list, 
               'extended': 1, 
               'fields' : 'members_count',
               'v': '5.65', 
               'access_token': service_key}

    response = requests.get(stat_link, params=payload)
    stats_feed = json.loads(response.text)  
    return stats_feed


def get_stats(posts):
    for i in range(len(list(posts))//100+1):
        posts_list = ''
        posts_list += ','.join(
            '-{}_{}'.format(x.page.feed_id, x.post_id) 
                for x in posts[i*100:(i+1)*100])
        stats_feed = stat_req(posts_list)

        for item in stats_feed['response']['items']:
            try: 
                post = posts.get(
                    post_id = str(item['id']), 
                    page__feed_id = str(-item['owner_id']))
                post.likes = item['likes']['count']
                post.reposts = item['reposts']['count'] 
                post.views = item.get('views',{'count':None})['count']  
                post.comments = item['comments']['count']  
                post.save()
            except Exception as e:
                logger.error(' '.join(('get_stats_vk', item, str(e)))) 
    
    
def get_post(account_feed, offset=0):
    items = account_feed['response']['items']
    try:
        if items[0]['date'] < items[offset+1]['date']:
            post = items[offset+1]
        else:
            post = items[offset]        
    except:
        post = items[offset]

    return post


def save_page(account_info):
    item = account_info['response'][0]
    full_name = item['name']
    vk_group_id = item['id']
    return full_name, vk_group_id


def get_followers_count(account_info):
    followers_count = account_info['response'][0]['members_count']
    return followers_count
    

def get_latest_post_id(latest_post):
    post_id = latest_post['id']
    time = datetime.fromtimestamp(int(latest_post['date']))
    title = latest_post.get('text','repost').split('.')[0]
    return post_id, time, title



