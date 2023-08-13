#import config
#import telebot

#bot = telebot.TeleBot(config.token)


def get_followers_count(account_info):
    chat_id = account_info.id
    ChatMembersCount = bot.get_chat_members_count(int(chat_id))
    return (ChatMembersCount)


def form_sub(chat):
    sub_info = {'full_name': chat.title,
                'last_posted_id': '',
                'daily_count': 0}
    return (sub_info)


def get_account_info(chat_id):
    chat = bot.get_chat(int(chat_id))
    return chat
