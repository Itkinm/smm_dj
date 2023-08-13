import os
import telegram
from django.conf import settings

from constance import config

env = config.ENVIRONMENT

tokens = getattr(settings, 'TOKENS') 
bot = telegram.Bot(tokens[env])


def format_post(post_form, post_link, shtab_name, l_p):
    try:
        text_start = l_p['text'] if l_p.get('copy_history',False) else ''
        title = l_p.get('title','')
        description = l_p.get('description','')
    except:
        text_start = ''
        title = ''
        description = ''    

    post_text = post_form.format(
        post_link = post_link,
        full_name = shtab_name.upper(),
        text_start = text_start,
        title = title,
        description = description,
        )
    return post_text    


def send_messages(channel, post_text, notifs):
    try:
        bot.send_message(channel, post_text, parse_mode='html')
    except Exception as e:
        raise Exception('send_messages', post_text, e)    
    for tguser in notifs:
        if env == 'PROD':
            try:
                bot.send_message(tguser.tg_id, post_text, parse_mode='html')
            except Exception as e:
                raise Exception('send_messages', tguser.tg_id, e) 
        else:         
            bot.send_message(95856961, tguser.tg_id, parse_mode='html')


def send_zhdun(shtabs, channel, span):
    if len(shtabs) != 0:
        bot.send_message(channel,
            'Не постили больше {} дней:\n'.format(span)+'\n'.join(shtabs))
    else:
        bot.send_message(channel,'На этой неделе все молодцы')              


def send_chart(file_name, channel):
    f = open(file_name, 'rb')
    bot.send_photo(channel, f) 
    os.remove(file_name)





