import facebook
from django.conf import settings
import datetime
import requests
import json 

post_link = 'https://facebook.com/{}'

logger = getattr(settings, 'LOGGER') 

def get_graph():
    url = 'https://graph.facebook.com/oauth/access_token'
    payload = {'client_id': settings.FACEBOOK_APP_ID, 
               'client_secret': settings.FACEBOOK_APP_SECRET,
               'grant_type': 'client_credentials'}

    r = requests.get(url, params = payload)
    j = json.loads(r.text)
    access_token = j['access_token']

    graph = facebook.GraphAPI(access_token=access_token, version='2.7')

    return graph

graph = get_graph()



def engs(post_id, resp):
    likes = graph.get_connections(id=post_id,
                                  connection_name='reactions',
                                  summary = True,
                                  limit=0)
    likes = likes['summary']['total_count']
    comments = len(resp[post_id].get('comments',{'data':[]})['data'])
    reposts = resp[post_id].get('shares',{'count':0})['count']
    return likes, reposts, comments


def get_stats(posts):
    for i in range(len(list(posts))//50+1):
        post_ids = {x.post_id for x in posts[i*50:(i+1)*50]}
        resp = graph.get_objects(ids=post_ids, fields="shares,comments")
        for post_id in resp:
            try:
                post = posts.get(post_id=post_id)
                post.likes, post.reposts, post.comments = engs(post_id, resp)
                post.save()
            except Exception as e:
                logger.error(' '.join(('get_stats_fb', post_id, str(e)))) 
    

def get_account_feed(username, count=1):
    account_feed = graph.get_object(id=username, fields='posts')
    return (account_feed)


def get_account_info(username):
    account_info = graph.get_object(id=username, fields='name, fan_count')
    return account_info


def get_post(account_feed, offset=0):
    post = account_feed['posts']['data'][offset]
    return post


def get_latest_post_id(latest_post):
    post_id = latest_post['id']
    time = latest_post['created_time'][:-5]
    return post_id, time, ''


def save_page(account_info):
    try:
        full_name = account_info['name']
        return full_name, ''
    except:
        return '', ''    


def get_followers_count(account_info):
    followers_count = account_info['fan_count']
    return followers_count



