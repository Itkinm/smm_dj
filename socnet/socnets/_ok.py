import requests
import feedparser
from datetime import datetime, timedelta

post_link = 'https://ok.ru/group/{}/topic/{}'
account_info_link = 'http://feed.exileed.com/ok/feed/{}'

def get_account_info(username):
    URL = account_info_link.format(username)
    response = requests.get(URL)
    account_info = feedparser.parse(response.text)
    return account_info

def get_account_feed(username, count=1):
    return get_account_info(username)


def save_page(account_info):
    full_name = account_info['feed']['title']

    return full_name, None


def get_post(account_feed, offset = 0):
    post = account_feed['entries'][offset]
    return post


def get_latest_post_id(latest_post):
    post_id = latest_post['id']
    return post_id, datetime.utcnow() + timedelta(hours=3), ''

def get_followers_count(account_info):
    return None