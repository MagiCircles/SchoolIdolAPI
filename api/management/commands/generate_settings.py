from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from api import models
from contest.utils import get_current_contest
from collections import OrderedDict
from web.templatetags.mod import tourldash
from django.db.models import Count
from django.conf import settings
import sys
import urllib2, json
import time

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

def generate_settings():

        print 'Get total donators'
        total_donators = str(models.UserPreferences.objects.filter(status__isnull=False).exclude(status__exact='').count())

        print 'Check the current contest'
        current_contest = get_current_contest()
        if current_contest is None:
            current_contest_url = '/contest/'
            current_contest_image = '/static/currentcontest_no.png'
            current_contest_name = None
        else:
            current_contest_url = '/contest/' + str(current_contest.id) + '/' + tourldash(current_contest.name) + '/'
            current_contest_image = (u'%s%s' % (settings.IMAGES_HOSTING_PATH, current_contest.image)) if current_contest.image else '/static/currentcontest.png'
            current_contest_name = current_contest.name.replace('\'', '\\\'')

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

        print 'Get cardsinfo dictionary'
        cards_info = str({
            'max_stats': {
                'Smile': models.Card.objects.order_by('-idolized_maximum_statistics_smile')[:1][0].idolized_maximum_statistics_smile,
                'Pure': models.Card.objects.order_by('-idolized_maximum_statistics_pure')[:1][0].idolized_maximum_statistics_pure,
                'Cool': models.Card.objects.order_by('-idolized_maximum_statistics_cool')[:1][0].idolized_maximum_statistics_cool,
            },
            'songs_max_stats': models.Song.objects.order_by('-expert_notes')[0].expert_notes,
            'idols': ValuesQuerySetToDict(models.Card.objects.values('name', 'idol__japanese_name').annotate(total=Count('name')).order_by('-total', 'name')),
            'sub_units': [card['sub_unit'] for card in models.Idol.objects.filter(sub_unit__isnull=False).values('sub_unit').distinct()],
            'years': [idol['year'] for idol in models.Idol.objects.filter(year__isnull=False).values('year').distinct()],
            'schools': [idol['school'] for idol in models.Idol.objects.filter(school__isnull=False).values('school').distinct()],
            'collections': ValuesQuerySetToDict(models.Card.objects.filter(japanese_collection__isnull=False).exclude(japanese_collection__exact='').values('japanese_collection').annotate(total=Count('name')).order_by('-total', 'japanese_collection')),
            'translated_collections': ValuesQuerySetToDict(models.Card.objects.filter(translated_collection__isnull=False).exclude(translated_collection__exact='').values('translated_collection').annotate(total=Count('name')).order_by('-total', 'translated_collection')),
            'skills': ValuesQuerySetToDict(models.Card.objects.filter(skill__isnull=False).values('skill').annotate(total=Count('skill')).order_by('-total')),
            'total_cards': models.Card.objects.order_by('-id')[0].id,
            'en_cards': [int(c.id) for c in models.Card.objects.filter(japan_only=False)],
        })

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
CARDS_INFO = ' + cards_info + '\n\
'
        print s
        f = open('schoolidolapi/generated_settings.py', 'w')
        print >> f, s
        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
