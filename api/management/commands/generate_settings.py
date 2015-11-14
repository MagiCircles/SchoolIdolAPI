from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from api import models
import sys
import urllib2, json

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
        if 'current' in data and data['current']:
            current_contest_url = '/contest/contest'
            current_contest_image = '/static/currentcontest.png'

        print 'Save generated settings'
        s = '\
TOTAL_DONATORS = ' + total_donators + '\n\
CURRENT_CONTEST_URL = \'' + current_contest_url + '\'\n\
CURRENT_CONTEST_IMAGE = \'' + current_contest_image + '\'\n\
'
        f = open('schoolidolapi/generated_settings.py', 'w')
        print >> f, s
        f.close()
