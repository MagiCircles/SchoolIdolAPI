# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Count
from django.forms.models import model_to_dict
import urllib2, urllib
from bs4 import BeautifulSoup, Comment
from api import models
from api.raw import raw_information
from tinypng import shrink_file
from web.forms import getGirls
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

reload(sys)
sys.setdefaultencoding('utf-8')

h = HTMLParser.HTMLParser()
japantz = pytz.timezone('Asia/Tokyo')

types = {'Normals': 'N', 'Rares': 'R', 'Super Rares': 'SR', 'Ultra Rares': 'UR'}
specials = {'None': 0, 'Promo Cards': 1, 'Special Cards': 2}
attribute_colors = {'blue': 'Cool', 'red': 'Smile', 'green': 'Pure', 'purple': 'All'}
attribute_jphexcolors = {'#7EF': 'Cool', '#FCE': 'Smile', '#7FA': 'Pure', '#d8bff8': 'All'}

local = False
redownload = False
noimages = False

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

def removeHTML(str):
    return re.sub('<[^<]+?>', '', str)

def cleanwithquotes(string):
    return clean(string, '|[]')

def clean(string, removecharacters=None):
    if string is None:
        return None
    if removecharacters is None:
        removecharacters = '\'\"|[]'
    return removeHTML(str(string.replace('”', '"').replace('！', '!').replace('？', '?').replace('～', '~'))).strip().translate(None, removecharacters).replace(u'\xc2', '').replace(u'\xa0', '')

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
        name = td.span.extract()
        details = td.string
        if details is None:
            if td.br is not None:
                td.br.extract()
            details = td.string
    elif td.strong is not None:
        name = td.strong.extract()
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

def shrunkImage(picture, url):
    from django.conf import settings
    api_key = settings.TINYPNG_API_KEY
    if not api_key or not url.endswith('.png'):
        return picture
    img_shrunked = NamedTemporaryFile(delete=False)
    shrink_info = shrink_file(
            picture.name,
            api_key=api_key,
            out_filepath=img_shrunked.name
    )
    img_shrunked.flush()
    return ImageFile(img_shrunked)

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
    for idol in raw_information.keys():
        card = models.Card.objects.filter(name=idol).order_by('id')[0]
        raw_information[idol]['main'] = True
        idol, created = models.Idol.objects.update_or_create(name=idol, defaults=raw_information[idol])

    print "#### Update cardsinfo.json"
    j = json.dumps({
        'max_stats': {
            'Smile': models.Card.objects.order_by('-idolized_maximum_statistics_smile')[:1][0].idolized_maximum_statistics_smile,
            'Pure': models.Card.objects.order_by('-idolized_maximum_statistics_pure')[:1][0].idolized_maximum_statistics_pure,
            'Cool': models.Card.objects.order_by('-idolized_maximum_statistics_cool')[:1][0].idolized_maximum_statistics_cool,
        },
        'idols': ValuesQuerySetToDict(models.Card.objects.values('name').annotate(total=Count('name')).order_by('-total', 'name')),
        'sub_units': [card['sub_unit'] for card in models.Idol.objects.filter(sub_unit__isnull=False).values('sub_unit').distinct()],
        'years': [idol['year'] for idol in models.Idol.objects.filter(year__isnull=False).values('year').distinct()],
        'collections': ValuesQuerySetToDict(models.Card.objects.filter(japanese_collection__isnull=False).exclude(japanese_collection__exact='').values('japanese_collection').annotate(total=Count('name')).order_by('-total', 'japanese_collection')),
        'skills': ValuesQuerySetToDict(models.Card.objects.filter(skill__isnull=False).values('skill').annotate(total=Count('skill')).order_by('-total'))
    })
    f = open('cardsinfo.json', 'w')
    print >> f, j
    f.close()

import_raw_db = update_raw_db
