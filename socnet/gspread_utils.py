from datetime import datetime, date, timedelta

import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from constance import config
from django.conf import settings

env = config.ENVIRONMENT

logger = getattr(settings, 'LOGGER') 

def clear_sheet(sheet):
    sheet.clear()
    cell_list = sheet.range('A1:I1')
    cell_list[0].value = "Штаб"
    cell_list[1].value = "Платформа"
    cell_list[2].value = "Ссылка"
    cell_list[3].value = "Время"
    cell_list[4].value = "Просмотры"
    cell_list[5].value = "Лайки"
    cell_list[6].value = "Репосты"
    cell_list[7].value = "Комменты"
    cell_list[8].value = "Название"
    sheet.update_cells(cell_list)    


def gspread_auth():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Smm DJ-09f246eb8043.json', scope)
    gc = gspread.authorize(credentials)
    return gc


def get_sheet():
    gc = gspread_auth()  
    if env == 'PROD':
        sheet = "Posts"  
    else:
        sheet = "DEV"             
             
    dj = gc.open("smm_dj").worksheet(sheet)
    return dj  


def fill_spread(sheet, posts):
    count = posts.count()
    cell_list = sheet.range('A2:I{}'.format(count+1))

    for i in range(count):
        cells = cell_list[i*9:(i+1)*9]
        cells[0].value = posts[i].page.shtab.name
        cells[1].value = posts[i].page.platform.name
        cells[2].value = posts[i].url
        cells[3].value = str(posts[i].posted_on.date())
        cells[4].value = posts[i].views
        cells[5].value = posts[i].likes
        cells[6].value = posts[i].reposts
        cells[7].value = posts[i].comments
        cells[8].value = str(posts[i].title)
        logger.info(posts[i].url + ' :written to gspread')

    return cell_list


def upload_to_gspread(posts):
    try:
        dj = get_sheet()
    except Exception as e:
        raise Exception('get_sheet',e)  

    clear_sheet(dj)
    
    try: 
        cell_list = fill_spread(dj, posts) 
    except Exception as e:
        raise Exception('fill_spread',e)  
    
    dj.update_cells(cell_list)    
    config.LAST_STAT_UPLOAD = datetime.utcnow() + timedelta(hours=3)  