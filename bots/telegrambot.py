from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from app.models import User, Tusa
from django.utils import timezone
from django.conf import settings


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'log.log',
                    format='%(asctime)s %(message)s',
                    level=logging.WARNING)


def main():
    logger.info("Loading handlers for telegram bot")
    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    # dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    #dp = DjangoTelegramBot.getDispatcher(token)     #get by bot token
    dp = DjangoTelegramBot.getDispatcher('botianya_com_bot')  #get by bot username
    #dp = DjangoTelegramBot.getDispatcher('tumblebot')

    #dp.add_handler(CommandHandler("help", help))
    
 
    # log all errors
    dp.add_error_handler(error)