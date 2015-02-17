# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
import urllib2
from bs4 import BeautifulSoup
from api import models
import re
import HTMLParser
import unicodedata
import sys
import datetime
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def removeHTML(str):
    return re.sub('<[^<]+?>', '', str)

def clean(string):
    if string is None:
        return None
    return removeHTML(str(string)).strip().translate(None, '\'\"|[]')

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

def extract_skill(td):
    if td.span is not None:
        name = td.span.extract()
        details = td.string
        if details is None:
            if td.br is None:
                details = None
            else:
                details = td.br.extract()
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

def downloadBestWikiaImage(url):
    url2 = url.split('/revision')[0]
    file1 = downloadFile(url)
    print 'File 1 Downloaded. ',; sys.stdout.flush()
    file2 = downloadFile(url2)
    print 'File 2 Downloaded. ',; sys.stdout.flush()
    if file1.width > file2.width:
        return file1
    return file2

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args

        if 'delete' in args:
             models.Card.objects.all().delete()
             models.Event.objects.all().delete()
             return

        h = HTMLParser.HTMLParser()

        types = {'Normals': 'N', 'Rares': 'R', 'Super Rares': 'SR', 'Ultra Rares': 'UR'}
        specials = {'None': 0, 'Promo Cards': 1, 'Special Cards': 2}

        print '### Import card ids & stats from decaf wiki'
        if local:
            f = open('decaf.html', 'r')
        else:
            f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=List_of_Cards&action=edit')

        currentType = types['Normals']
        special = specials['None']
        for line in f.readlines():
            line = h.unescape(line)
            data = str(line).split('||')
            if len(data) == 1:
                name = clean(data[0].translate(None, '='))
                if name in types.keys():
                    currentType = types[name]
                    special = specials['None']
                    note = ""
                    center = None
                if name in specials.keys():
                    special = specials[name]
                    note = ""
                    center = None
            elif len(data) > 2:
                id = int(clean(data[0]))
                print 'Importing card #', id, '...',; sys.stdout.flush()
                name = clean(data[1].split('|')[1])
                type = clean(data[2])

                hp = 0
                minStats = (0, 0, 0)
                intStats = (0, 0, 0)
                maxStats = (0, 0, 0)
                nextData = 7
                skill = None
                promo = None
                release_date = None
                event_en = ''
                event_jp = ''
                event = None

                if len(data) > 3:
                    if special != 2:
                        hp = int(clean(data[3]))
                    else:
                        note = clean(data[3].split('|')[-1])
                if len(data) > 6:
                    minStats = (int(clean(data[4])), int(clean(data[5])), int(clean(data[6])))
                if currentType != 'N' and special == 0 and len(data) > 14: # intermediate stats
                    intStats = (int(clean(data[8])), int(clean(data[9])), int(clean(data[10])))
                    maxStats = (int(clean(data[12])), int(clean(data[13])), int(clean(data[14])))
                    nextData = 15
                elif len(data) > 10:
                    maxStats = (int(clean(data[8])), int(clean(data[9])), int(clean(data[10])))
                    nextData = 11
                if len(data) > nextData:
                    skill = clean(data[nextData].split('|')[-1])
                if len(data) > nextData + 1:
                    center = clean(data[nextData + 1].split('|')[-1])

                soup = BeautifulSoup(data[1])
                soupsmall = soup.small
                if soupsmall is not None:
                    soupspan = soupsmall.span
                    if soupspan is not None:
                        if special == 1:
                            promo = soupspan.text.split('c/w ')[-1].replace('[[', '').replace('|', ' (').replace(']]', ') ')
                        else:
                            if 'Added on' in soupspan.text:
                                release_date_str = soupspan.text.split('Added on ')[1]
                                release_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(release_date_str, '%B %d, %Y')))
                            elif 'event prize' in soupspan.text:
                                event_name = soupspan.text.split(' event prize')[0].replace(']]', '').replace('[[', '')
                                event_jp = event_name.split('|')[0]
                                event_en = event_name.split('|')[-1]
                                event, created = models.Event.objects.get_or_create(japanese_name=event_jp, defaults={
                                    'english_name': event_en,
                                })

                defaults = {
                    'name': name,
                    'rarity': currentType,
                    'attribute': type,
                    'is_promo': special == 1,
                    'promo_item': promo,
                    'is_special': special == 2,
                    'hp': hp,
                    'minimum_statistics_smile': minStats[0],
                    'minimum_statistics_pure': minStats[1],
                    'minimum_statistics_cool': minStats[2],
                    'non_idolized_maximum_statistics_smile': intStats[0],
                    'non_idolized_maximum_statistics_pure': intStats[1],
                    'non_idolized_maximum_statistics_cool': intStats[2],
                    'idolized_maximum_statistics_smile': maxStats[0],
                    'idolized_maximum_statistics_pure': maxStats[1],
                    'idolized_maximum_statistics_cool': maxStats[2],
                    'skill': skill,
                    'skill_details': (note if note else None),
                    'center_skill': center,
                }
                if promo:
                    defaults['release_date'] = None
                if release_date is not None:
                    defaults['release_date'] = release_date
                if event is not None:
                    defaults['event'] = event
                card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                print 'Done'
        f.close()

        print '### Import events from decaf wiki'
        if local:
            f = open('events.html', 'r')
        else:
            f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=List_of_Events&action=edit')

        for line in f.readlines():
            line = h.unescape(line)
            data = str(line).split('||')
            if len(data) > 1:
                dates = data[0].replace('|', '').split(' - ')
                beginning = datetime.datetime.fromtimestamp(time.mktime(time.strptime(clean(dates[0]), '%Y/%m/%d')))
                end = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(beginning.year) + '/' + clean(dates[1]), '%Y/%m/%d')))
                name = clean(data[1].replace('[[', '').replace(']]', '').split('|')[-1]).replace('μs', 'μ\'s')
                t1_points = optInt(clean(data[3]))
                i = 4
                if 'rowspan' in data[i] or len(data) == 7 or len(data) == 8:
                    t1_new_rank = optInt(clean(data[i].split('|')[-1]))
                    if t1_new_rank: t1_rank = t1_new_rank
                    i = i + 1
                t2_points = optInt(data[i])
                i = i + 1
                if len(data) > i and ('rowspan' in data[i] or len(data) == 7 or len(data) == 8):
                    t2_new_rank = optInt(clean(data[i].split('|')[-1]))
                    if t2_new_rank: t2_rank = t2_new_rank
                    i = i + 1
                if len(data) > i:
                    note = optString(clean(data[i].split('|')[-1]))
                print 'Import event ', name, '...',; sys.stdout.flush()
                defaults = {
                    'beginning': beginning,
                    'end': end,
                    'japanese_t1_points': t1_points,
                    'japanese_t1_rank': (None if not t1_points else t1_rank),
                    'japanese_t2_points': t2_points,
                    'japanese_t2_rank': t2_rank,
                    'note': note,
                }
                event, created = models.Event.objects.update_or_create(japanese_name=name, defaults=defaults)
                models.Card.objects.filter(event=event).update(release_date=beginning)
                print 'Done'

        f.close()

        print '### Import card pictures and skills details from wikia'
        if local:
            f = open('wikia.html', 'r')
        else:
            f = urllib2.urlopen('http://love-live.wikia.com/wiki/Love_Live!_School_Idol_Festival_Card_List')
        soup = BeautifulSoup(f.read())

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 4:
                id = ""
                normal = ''
                idolized = ''
                skill = None
                id = tds[0].string
                if id is not None:
                    id = int(clean(str(id)))
                    print 'Import images & skill for #', id, '...',; sys.stdout.flush()
                normaltd = tds[1].a
                if normaltd is not None:
                    normal = wikiaImageURL(normaltd.get('href'))
                idolizedtd = tds[2].a
                if idolizedtd is not None:
                    idolized = wikiaImageURL(idolizedtd.get('href'))
                skilltd = tds[3].text
                if skilltd is not None:
                    skill_title = tds[3].b.extract()
                    skill = clean(tds[3].text)
                if id is not None:
                    defaults = {
                        'card_url': normal,
                        'card_idolized_url': idolized,
                    }
                    if skill:
                        defaults['skill_details'] = skill
                    card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                    if normal and (redownload or not card.card_image):
                        card.card_image.save(str(card.id) + '.jpg', downloadBestWikiaImage(normal))
                    if idolized and (redownload or not card.card_idolized_image):
                        card.card_idolized_image.save(str(card.id) + 'idolized.jpg', downloadBestWikiaImage(idolized))
                    print 'Done'
        f.close()

        print '### Import japanese information for R/SR/UR'
        if local:
            f = open('jpcards.html', 'r')
        else:
            f = urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/34.html')
        soup = BeautifulSoup("".join(line.strip() for line in f.read().split("\n")))

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 4:
                id = tds[0].string
                try:
                    id = int(id)
                except (ValueError, TypeError):
                    continue
                if id != None:
                    print 'Import for #', id, '...',; sys.stdout.flush()
                    picture = tds[1].img
                    if picture is not None:
                        picture = wikiaImageURL(picture.get('src'))
                    if tds[2].span is not None:
                        tmp = tds[2].span.extract()
                    if tds[2].br is not None:
                        tmp = tds[2].br.extract()
                    name = clean(tds[2].string)
                    if name is not None and '(' in name:
                        version = clean(name.split('(')[-1].split(')')[0])
                        name = clean(name.split('(')[0])
                    elif name is not None and '（' in name:
                        version = clean(name.split('（')[-1].split('）')[0])
                        name = clean(name.split('（')[0])
                    else:
                        version = ''
                    if len(tds) == 5: # special card
                        skill_name = None
                        skill_details = clean(tds[-1].string)
                        center_skill_name = None
                        center_skill_details = None
                    elif len(tds) == 18: # all info specified
                        skill_name, skill_details = extract_skill(tds[-2])
                        center_skill_name, center_skill_details = extract_skill(tds[-1])
                    elif len(tds) == 16: # take center skill from previous line
                        skill_name, skill_details = extract_skill(tds[-1])
                    # elif len(tds) == 15: # take skill + center skill from previous line
                    defaults = {
                        'japanese_name': name,
                    }
                    if picture is not None:
                        defaults['round_card_url'] = picture
                    if version is not None:
                        defaults['japanese_collection'] = version
                    if skill_name is not None:
                        defaults['japanese_skill'] = skill_name
                    if skill_details is not None:
                        defaults['japanese_skill_details'] = skill_details
                    if center_skill_name is not None:
                        defaults['japanese_center_skill'] = center_skill_name
                    if center_skill_details is not None:
                        defaults['japanese_center_skill_details'] = center_skill_details
                    card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                    if picture and (redownload or not card.round_card_image):
                        print 'Download image...',; sys.stdout.flush()
                        card.round_card_image.save(str(card.id) + 'round.jpg', downloadFile(picture))
                    print 'Done'

        f.close()

        print '### Import japanese information for N (round image + name)'
        if local:
            f = open('jpcardsN.html', 'r')
        else:
            f = urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/101.html')
        soup = BeautifulSoup("".join(line.strip() for line in f.read().split("\n")))

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 4:
                id = tds[0].string
                if id != None:
                    print 'Import for #', id, '...',; sys.stdout.flush()
                    picture = tds[1].img
                    if picture is not None:
                        picture = wikiaImageURL(picture.get('src'))
                    if tds[2].span is not None:
                        tmp = tds[2].span.extract()
                    if tds[2].br is not None:
                        tmp = tds[2].br.extract()
                    name = clean(tds[2].string)
                    defaults = {
                        'japanese_name': name,
                    }
                    if picture is not None:
                        defaults['round_card_url'] = picture
                    card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                    if picture and (redownload or not card.round_card_image):
                        print 'Download image...',; sys.stdout.flush()
                        card.round_card_image.save(str(card.id) + 'round.jpg', downloadFile(picture))
                    print 'Done'

        f.close()
