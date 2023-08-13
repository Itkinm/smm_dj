import os
from celery.schedules import crontab

import logging
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cd5pbnm=y1k$5%=2sazy+&xyu%&e)%hgp9qjm)e#$0324qt*a#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '51.15.141.90', 'smm.navalny-team.org']


# Application definition

INSTALLED_APPS = [
    'constance',
    'rangefilter',
    'import_export',
    #'bots.apps.BotsConfig',
    'socnet.apps.SocnetConfig',
    'django_celery_beat',
    'django_telegrambot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smm_dj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'socnet.context_processors.add_navbar',
            ],
        },
    },
]

WSGI_APPLICATION = 'smm_dj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow' 

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGER = logging.getLogger(__name__)

logging.basicConfig(filename = 'log.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


# Celery application definition
# http://docs.celeryproject.org/en/v4.0.2/userguide/configuration.html

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


CONSTANCE_CONFIG = {
    'STATS_UPDATE_DEFAULT_SPAN': (7, 'Posts from fow many days back to update stats for'),
    'STATS_SHOW_DEFAULT_SPAN': (60, 'Posts from fow many days back to show stats for'),
    'LAST_ZHDUN_RUN': (datetime(2018, 1, 1) ,'When was the last Zhdun check'), 
    'LAST_STAT_UPDATE': (datetime(2018, 1, 1) ,'When stats were last updated'),
    'LAST_STAT_UPLOAD': (datetime(2018, 1, 1) ,'When stats were last uploaded'),
    'ENVIRONMENT': ('DEV', 'DEV/PROD'),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ADMIN_GROUP_ID = -1001060656304

#twitter
TWITTER_CONSUMER_KEY='HYcLShTWgyqf1bDEqout8S5MY'
TWITTER_CONSUMER_SECRET='6Hq9lWhjeiNhi54BbpAaQg6sgnbnSPa7rhSWXttZfei2emPS8i'
TWITTER_ACCESS_TOKEN_KEY='186531848-K1WXDAieFzV6pCIAKB2QpDjeRYEt0qA2wjCVQh2h'
TWITTER_ACCESS_TOKEN_SECRET='xoSoZNSpenDraqV0I41MwQe3JHejXpO7gHwZK7GvfsVnc'

#fb
FACEBOOK_APP_ID = '368091016976861'
FACEBOOK_APP_SECRET = 'd5229f6e5139dc6d2ff440f9fe81b4b2'


#vk
VK_SERVICE_KEYS = ['5c301a565c301a565c301a563f5c6cac1055c305c301a560572bfafc2887120352ab324',
                   '7084e12f7084e12f7084e12ff070e512ee770847084e12f2a379da6bf3c9cfcd26e3177']


#youtube
YOUTUBE_APIKEY = 'AIzaSyBEFWMABr3xFlAVT8tUeTXmhYwrbtbKQXo'#'AIzaSyCWOl6xLVUduHJFxrnk6Bt3yPKkqgTyuWs'


DJANGO_TELEGRAMBOT = {

    'MODE' : 'POLLING', #(Optional [str]) # The default value is WEBHOOK,
                        # otherwise you may use 'POLLING'
                        # NB: if use polling you must provide to run
                        # a management command that starts a worker

    'WEBHOOK_SITE' : 'http://localhost:8000/',


    'BOTS' : [
        {
           'TOKEN': '419878279:AAGTTPqpXEXobv3TH8Rtq6dD0pk-Idnaqec',
        },
        {  
           'TOKEN': '394160317:AAHZGWz2U7_KwM4j-JYmkeCC2otVMxj4W-Y',
        },
    ],
}


TOKENS = {'PROD': DJANGO_TELEGRAMBOT['BOTS'][1]['TOKEN'],
          'DEV': DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']}                            




