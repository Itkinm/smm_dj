import requests
import json
from datetime import datetime, date
from django.conf import settings

post_link = 'https://www.youtube.com/watch?v={post_id}'

logger = getattr(settings, 'LOGGER') 
apikey = getattr(settings, 'YOUTUBE_APIKEY') 

def get_account_info(username):
    account_info_link = 'https://www.googleapis.com/youtube/v3/channels'

    payload = {'key': apikey, 
               'part': 'contentDetails,snippet,statistics',
               'id': username}
    response = requests.get(account_info_link, params=payload)
    account_info = json.loads(response.text)    
    return account_info


def get_account_feed(playlist_id, count=1):
    account_feed_link = 'https://www.googleapis.com/youtube/v3/playlistItems'
    payload = {'key': apikey, 
               'part': 'contentDetails,snippet',
               'playlistId': playlist_id,
               'maxResults': count+1}

    response = requests.get(account_feed_link, params=payload)
    account_feed = json.loads(response.text)   

    return account_feed


def stat_req(video_ids):
    stat_link = 'https://www.googleapis.com/youtube/v3/videos'
    payload = {'key': apikey, 
               'part': 'contentDetails,statistics',
               'id': video_ids,}    
    response = requests.get(stat_link, params=payload)
    stats = json.loads(response.text)   
    return stats           
    

def get_stats(posts):
    for i in range(len(list(posts))//50+1):
        video_ids = ','.join(x.post_id for x in posts[i*50:(i+1)*50])
        stats = stat_req(video_ids)
        for item in stats['items']:
            try: 
                post = posts.get(post_id = item['id'])
                post.likes = int(item['statistics']['likeCount'])
                post.views = int(item['statistics']['viewCount'])
                post.comments = int(item['statistics']['commentCount'])
                post.save()
            except Exception as e:
                logger.error(' '.join(('get_stats_youtube', item, str(e)))) 
    

def get_time(item):
    return item['contentDetails']['videoPublishedAt']


def get_post(account_feed, offset=0):
    items = account_feed['items']
    if get_time(items[0]) < get_time(items[offset+1]):
        post = items[offset+1]
    else:
        post = items[offset]
    return post


def save_page(account_info):
    try:
        item = account_info['items'][0]
        full_name = item['snippet']['title']
        contentDetails = item['contentDetails']
        playlist_id = contentDetails['relatedPlaylists']['uploads']
    except:
        full_name = None
        playlist_id = None
    return full_name, playlist_id


def get_followers_count(account_info):
    item = account_info['items'][0]
    followers_count = int(item['statistics']['subscriberCount'])
    return followers_count


def get_latest_post_id(latest_post):
    post_id = latest_post['contentDetails']['videoId']
    time = latest_post['contentDetails']['videoPublishedAt']
    title = latest_post['snippet']['title']
    
    return post_id, time, title
"""
URL = config.feed_link['youtube'].format('UUgxTPTFbIbCWfTR9I2-5SeQ', 1)
response = requests.get(URL)
account_feed = json.loads(response.text)
print(get_post(account_feed))
"""
