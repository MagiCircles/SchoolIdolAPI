from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from api import models
from collections import OrderedDict
import sys
import urllib2, json
import time

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        print 'Get total donators'
        total_donators = str(models.UserPreferences.objects.filter(status__isnull=False).exclude(status__exact='').count())

        print 'Check the current contest'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        request = urllib2.Request('http://schoolido.lu/contest/json/current', headers=hdr)
        response = urllib2.urlopen(request)
        data = json.load(response)
        current_contest_url = '/contest/'
        current_contest_image = '/static/currentcontest_no.png'
        current_contest_name = None
        if 'current' in data and data['current']:
            current_contest_url = '/contest/contest'
            current_contest_image = '/static/currentcontest.png'
            current_contest_name = data['name'].replace('\'', '\\\'')

        print 'Get ages'
        ages = {}
        for i in range(10,30):
            ages[i] = 0
        prefs = models.UserPreferences.objects.filter(birthdate__isnull=False)
        total_ages = prefs.count()
        for p in prefs:
            age = p.age
            if age > 0 and age < 88:
                if age in ages:
                    ages[age] += 1
                else:
                    ages[age] = 1
        ages = OrderedDict(sorted(ages.items()))

        print 'Save generated settings'
        s = '\
from collections import OrderedDict\n\
import datetime\n\
TOTAL_DONATORS = ' + total_donators + '\n\
CURRENT_CONTEST_URL = \'' + current_contest_url + '\'\n\
CURRENT_CONTEST_IMAGE = \'' + current_contest_image + '\'\n\
CURRENT_CONTEST_NAME = ' + ('None' if not current_contest_name else '\'' + current_contest_name + '\'') + '\n\
USERS_AGES = ' + unicode(ages) + '\n\
USERS_TOTAL_AGES = ' + unicode(total_ages) + '\n\
GENERATED_DATE = datetime.datetime.fromtimestamp(' + str(time.time()) + ')\n\
'
        print s
        f = open('schoolidolapi/generated_settings.py', 'w')
        print >> f, s
        f.close()
