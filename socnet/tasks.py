from __future__ import absolute_import, unicode_literals
from celery import task
from datetime import date, timedelta, datetime

from socnet.models import *        
from socnet.gspread_utils import upload_to_gspread

from constance import config


@task()
def crawler(platform_name):
    pages = Page.objects.filter(
                platform__name=platform_name,
                shtab__is_open=True)
    for page in pages:
        page.check_for_fresh_post()


def update_stats():
    for platform in Platform.objects.filter(stat=True):        
        platform.get_stats()
        platform.get_followers_counts()
        #platform.make_charts()

    config.LAST_STAT_UPDATE = datetime.utcnow() + timedelta(hours=3)  


def upload_stats():
    span = date.today()-timedelta(days=config.STATS_SHOW_DEFAULT_SPAN)    
    posts = Post.objects.filter(posted_on__gte=span)
    upload_to_gspread(posts)


def send_zhduns():
    for platform in Platform.objects.filter(zhdun=True):
        platform.send_zhduns() 


@task()
def stat_collector():
      
    send_zhduns()
    update_stats()   
    upload_stats()

                  
@task()
def zhdun_task():
    send_zhduns()


@task()
def upload_to_gspread_task():
    upload_stats()


@task()
def one_platform_stat_task(platform_name):
    platform = Platform.objects.get(name = platform_name)
    platform.get_stats()


@task()
def chart_task():
    for platform in Platform.objects.filter(stat=True):       
        platform.make_charts()
        

@task()
def pages_collector():
    pass

