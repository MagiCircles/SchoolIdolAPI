from django.core.management.base import BaseCommand, CommandError
import urllib2
from bs4 import BeautifulSoup
from api import models
import re
import HTMLParser
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def removeHTML(str):
    return re.sub('<[^<]+?>', '', str)

def clean(string):
    return removeHTML(str(string)).strip().translate(None, '\'\"|[]')

def wikiaImageURL(string):
    if string is None:
        return ""
    return clean(string)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        h = HTMLParser.HTMLParser()

        types = {'Normals': 'N', 'Rares': 'R', 'Super Rares': 'SR', 'Ultra Rares': 'UR'}
        specials = {'None': 0, 'Promo Cards': 1, 'Special Cards': 2}
        
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
                    center = ""
                if name in specials.keys():
                    special = specials[name]
                    note = ""
                    center = ""
            elif len(data) > 2:
                id = int(clean(data[0]))
                name = clean(data[1].split('|')[1])
                type = clean(data[2])
                hp = 0
                minStats = (0, 0, 0)
                intStats = (0, 0, 0)
                maxStats = (0, 0, 0)
                nextData = 7
                skill = ''
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

                models.Card.objects.update_or_create(id=id, defaults={
                    'name': name,
                    'rarity': currentType,
                    'attribute': type,
                    'is_promo': special == 1,
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
                    'center_skill': center,
                })
        
        from bs4 import BeautifulSoup
        # f = open('list.html', 'r')
        f = urllib2.urlopen('http://love-live.wikia.com/wiki/Love_Live!_School_Idol_Festival_Card_List')
        soup = BeautifulSoup(f.read())
        
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 4:
                id = ""
                normal = ""
                idolized = ""
                id = tds[0].string
                if id is not None:
                    id = int(clean(str(id)))
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
                    models.Card.objects.update_or_create(id=id, defaults={
                        'skill_details': skill,
                        'card_url': normal,
                        'card_idolized_url': idolized,
                    })
