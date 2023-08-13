from django.core.management.base import BaseCommand, CommandError
from socnet.rss import *

from socnet.models import Tguser, Page, Platform, Post
import logging
from YaDiskClient.YaDiskClient import YaDisk
disk = YaDisk('botianya', 'tseeuzm')

from datetime import datetime, date

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'log.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

def form_subs_list():

    downloaded = False
    while downloaded == False:
        try:
            disk.download('subs/{}'.format('subs_list.txt'), 'subs_list.txt')
            downloaded = True
        except Exception as e:
            logging.warning('DOWNLOAD_SUBS: ' + str(e))
    logging.info('downloaded subscriptions list')

    with open('subs_list.txt') as current_file:
        subs_local = eval(current_file.read())
    return subs_local


ps = {'instagram': Platform.IN, 
      'vk': Platform.VK, 
      'twitter': Platform.TW, 
      'youtube': Platform.YT,
      'telegram': Platform.TG,
      'fb': Platform.FB,
      'ok': Platform.OK,}



class Command(BaseCommand):
    def handle(self, *args, **options):

        subs = form_subs_list()

        for platform in subs:
            for username in subs[platform]:
                try:
                    sub = subs[platform][username]
                    page_obj, created = Page.objects.get_or_create(
                    username = username,
                    full_name  = sub['full_name'],
                            #last_posted_id = sub['last_posted_id'],
                    platform = Platform.objects.get(pk=ps[platform]))
                    try:
                        page_obj.vk_group_id = sub['vk_group_id']
                    except:
                        pass
                    try:
                        page_obj.playlist_id = sub['playlist_id']
                    except:
                        pass

                    #post_obj , created = Post.objects.get_or_create(
                    #    post_id = sub['last_posted_id'],
                    #    page = page_obj,
                    #    )
                    #if created:
                    #    post_obj.posted_on = datetime.now()
                    #    post_obj(save)

                    for notif in sub['notifs']:
                        tg_obj, created = Tguser.objects.get_or_create(pk=notif)
                        page_obj.notifs.add(tg_obj)

                    if platform != 'telegram': 
                        full_name, page_obj.feed_id = save_page[ps[platform]](username)    
                    page_obj.save()
                
                except Exception as e:
                    print (e, username, platform)    

                    
