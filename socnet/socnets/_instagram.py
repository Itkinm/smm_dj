from datetime import datetime, date
import requests
import json
from django.conf import settings

post_link = 'https://www.instagram.com/p/{}/'
account_link = 'https://www.instagram.com/{}/'

logger = getattr(settings, 'LOGGER') 



def get_entry_data(URL):
    response = requests.get(URL)
    page = response.text
    pos = page.find('window._sharedData')
    target = page.find('</script>', pos, len(page))
    dicta = json.loads(page[pos+21:target-1])
    entry_data = dicta['entry_data']
    return entry_data


def get_account_info(username):
    entry_data = get_entry_data(account_link.format(username))
    account_info = entry_data['ProfilePage'][0] 
    return account_info


def get_account_feed(username, count=1):   
    return (get_account_info(username))
    

def get_stats(posts):
    for post in posts:
        try:
            entry_data = get_entry_data(post_link.format(post.post_id))
            media = entry_data['PostPage'][0]['graphql']['shortcode_media']
            post.likes = media['edge_media_preview_like']['count']
            post.comments = media['edge_media_to_comment']['count']
            post.save()
        except Exception as e:
            logger.error(' '.join(('get_stats_insta', post.page.url, post.post_id, str(e)))) 
                             

# Extract the latest post from the feed
# There might be problems since it's not a documented instagram feature
def get_post(account_feed, offset = 0):
    post = account_feed['graphql']['user']['edge_owner_to_timeline_media']['edges'][offset]['node']
    return post


def save_page(account_info):
    full_name = account_info['graphql']['user']['full_name']
    return full_name, None


def get_followers_count(account_info):
    followers_count = account_info['graphql']['user']['edge_followed_by']['count']
    return followers_count


def get_latest_post_id(latest_post):
    post_id = latest_post['shortcode']
    stamp = latest_post['taken_at_timestamp']
    time = datetime.fromtimestamp(stamp)
    return post_id, time, ''
