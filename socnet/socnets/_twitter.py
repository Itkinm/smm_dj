from django.conf import settings
import twitter
from datetime import datetime, date
 
consumer_key = getattr(settings, 'TWITTER_CONSUMER_KEY') 
consumer_secret = getattr(settings, 'TWITTER_CONSUMER_SECRET') 
access_token_key = getattr(settings, 'TWITTER_ACCESS_TOKEN_KEY') 
access_token_secret = getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET') 

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

logger = getattr(settings, 'LOGGER') 



def get_account_info(username):
    account_info = api.GetUser(screen_name = username)
    return account_info


def get_account_feed(username, count=1):
    account_feed = api.GetUserTimeline(screen_name = username, count = count+9)
    return (account_feed)


def get_stats(posts):
    post_ids = [x.post_id for x in posts]
    statuses = api.GetStatuses(post_ids, trim_user=True)
    for status in statuses:
        try:
            post = posts.get(post_id=status.id_str)
            
            post.reposts = status.retweet_count
            post.likes = status.favorite_count
            post.save()
        except Exception as e:
                logger.error(' '.join(('get_stats_twitter', status, str(e))))     


def get_post(account_feed, offset = 0):
    count = 0
    for status in account_feed:
        if status.retweeted_status == None:
            if count == offset:
                return status
            else: 
                count += 1    
    raise ValueError('last {} posts are retweets'.format(len(account_feed)))        


def save_page(account_info):
    full_name = account_info.name

    return full_name, None


def get_latest_post_id(latest_post):
    post_id = latest_post.id
    twitime = '%a %b %d %H:%M:%S +0000 %Y'
    time = datetime.strptime(latest_post.created_at, twitime)
    return post_id, time, ''

def get_followers_count(account_info):
    return account_info.followers_count
