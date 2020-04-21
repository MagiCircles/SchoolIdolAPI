# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.forms.models import model_to_dict
from django.conf import settings
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
from api import models
from api.raw import raw_information, raw_information_n
from web.forms import getGirls
from web.utils import shrunkImage
from api.management.commands.generate_settings import generate_settings
import re
import HTMLParser
import unicodedata
import sys
import datetime
import pytz
import time
import csv
import json
import dateutil.parser
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

h = HTMLParser.HTMLParser()
japantz = pytz.timezone('Asia/Tokyo')

types = {'Normals': 'N', 'Rares': 'R', 'Super Rares': 'SR', 'Super Super Rares': 'SSR', 'Ultra Rares': 'UR'}
specials = {'None': 0, 'Promo Cards': 1, 'Special Cards': 2}
attribute_colors = {'blue': 'Cool', 'red': 'Smile', 'green': 'Pure', 'purple': 'All'}
attribute_jphexcolors = {'#7DF': 'Cool', '#FCC': 'Smile', '#7F7': 'Pure', '#d8bff8': 'All'}

local = False
redownload = False
noimages = False

def removeHTML(str):
    return re.sub('<[^<]+?>', '', str)

def cleanwithquotes(string):
    return clean(string, '|[]')

def clean(string, removecharacters=None):
    if string is None:
        return None
    if removecharacters is None:
        removecharacters = '\'\"|[]'
    return removeHTML(str(string.replace('”', '"').replace('？', '?').replace('～', '~'))).strip().translate(None, removecharacters).replace(u'\xc2', '').replace(u'\xa0', '')

def optInt(i):
    try:
        i = int(i)
    except (ValueError, TypeError):
        i = None
    return i
def optString(s):
    return None if not s else s

def wikiaImageURL(string):
    if string is None:
        return ""
    return clean(string)

def eventDateFromString(date, format='%Y/%m/%d %I%p', timezone=pytz.utc):
    return timezone.localize(datetime.datetime.fromtimestamp(time.mktime(time.strptime(clean(date), format))))

def remove_all_comments(soup):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup

def extract_skill(td):
    td = remove_all_comments(td)
    if td.span is not None:
        name = td.span.extract().text
        details = td.string
        if details is None:
            if td.br is not None:
                td.br.extract()
            details = td.string
    elif td.strong is not None:
        name = td.strong.extract().text
        details = td.string
    else:
        name = td.string
        details = None
    return clean(name), clean(details)

def downloadFile(url):
    img_temp = NamedTemporaryFile(delete=True)
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36' })
    img_temp.write(urllib2.urlopen(req).read())
    img_temp.flush()
    return ImageFile(img_temp)

def downloadShrunkedImage(url):
    downloaded = downloadFile(url)
    return shrunkImage(downloaded, url)

def downloadBestWikiaImage(url):
    url2 = url.split('/revision')[0]
    file1 = downloadFile(url)
    print 'File 1 Downloaded. ',; sys.stdout.flush()
    file2 = downloadFile(url2)
    print 'File 2 Downloaded. ',; sys.stdout.flush()
    if file1.width > file2.width:
        return shrunkImage(file1, url)
    return shrunkImage(file2, url2)

def update_raw_db():
    print "#### Update raw information"
    generate_settings()

def opt_parse(args, delete=False):
    opt = {
        'local': False,
        'redownload': False,
        'noimages': False,
        'delete': False,
    }
    if 'local' in args: opt['local'] = True
    if 'redownload' in args: opt['redownload'] = True
    if 'noimages' in args: opt['noimages'] = True
    if 'delete' in args: opt['delete'] = True
    return opt

import_raw_db = update_raw_db
