#!/usr/bin/env python
import sqlite3
import time
import traceback

__author__ = 'liao'

# api from https://github.com/Davidigest/pyYouku
# youku upload management page http://i.youku.com/u/videos

from keyfile import CLIENT_ID, ACCESS_TOKEN
from config import *

# my fork of youku
# https://github.com/hanguokai/youku
import sys
sys.path.append('/home/liao/git-repos/youku/youku/')
import imp
YoukuUpload = imp.load_source('YoukuUpload', '/home/liao/git-repos/youku/youku/youku_upload.py')


def uploader():
    my_name = "uploader"
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print my_name.rjust(10, '+'), 'Checking Database for new file to push'
    sql = 'SELECT TITLE, CATEGORIES, FILEPATH, YOUTUBE_URL FROM LINKS WHERE UPLOADED==0 AND DOWNLOADED==1 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    sql_result = c.fetchone()

    if sql_result:
        title, categories, filepath, youtubeURL = sql_result
        if ' & ' in categories:
            categories = categories.replace(' & ', ',')
            print categories
        file_info = {
          'title': title,
          'tags': categories,
          'copyright_type': 'reproduced',
          'description': 'Automatically uploaded by @liaozd, original URL: {0}'.format(youtubeURL),
        }
        youku = YoukuUpload.YoukuUpload(CLIENT_ID, ACCESS_TOKEN, filepath)
        print my_name.rjust(10, "+"), 'uploading "{0}" to YOUKU ..........'.format(filepath)
        print youku.upload(file_info)
        print my_name.rjust(10, "+"), 'uploading {0} finished!!!!'.format(filepath)
        sql = 'UPDATE LINKS SET UPLOADED=1 WHERE YOUTUBE_URL="{0}";'.format(youtubeURL)
        c.execute(sql)
        db.commit()
    db.close()


def pusher(sleeptime=190):
    my_name = 'pusher'
    while True:
        print my_name.rjust(10, '+'), 'start at {0}'.format(time.strftime("%Y-%m-%d %A %X %Z", time.localtime()))
        uploader()
        print my_name.rjust(10, '+'), 'takes a snap for {0}s'.format(sleeptime)
        time.sleep(sleeptime)

if __name__ == '__main__':
    pusher()