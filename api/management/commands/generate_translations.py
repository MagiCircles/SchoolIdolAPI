from django.core.management.base import BaseCommand, CommandError
from api import models
from contest import models as contest_models
from api.management.commands.importbasics import *
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        idols = models.Idol.objects.all()
        cards = models.Card.objects.all()
        songs = models.Song.objects.all()
        events = models.Event.objects.all()
        contests = contest_models.Contest.objects.all()

        things = []
        print '## Years'
        things += [idol['year'] for idol in idols.filter(year__isnull=False).values('year').distinct()]
        print '## Food'
        things += [idol['favorite_food'] for idol in idols.filter(favorite_food__isnull=False).values('favorite_food').distinct()]
        things += [idol['least_favorite_food'] for idol in idols.filter(least_favorite_food__isnull=False).values('least_favorite_food').distinct()]
        print '## Idol Descriptions'
        things += [idol['summary'] for idol in idols.filter(summary__isnull=False).values('summary').distinct()]
        print '## Hobbies'
        things += [idol['hobbies'] for idol in idols.filter(hobbies__isnull=False).values('hobbies').distinct()]
        print '## Translated Collections'
        things += [card['translated_collection'] for card in cards.filter(translated_collection__isnull=False).exclude(translated_collection='').values('translated_collection').distinct()]
        print '## Translated song names'
        things += [song['translated_name'] for song in songs.filter(translated_name__isnull=False).values('translated_name').distinct()]
        print '## Event notes'
        things += [event['note'] for event in events.filter(note__isnull=False).values('note').distinct()]
        print '## Event names'
        things += [event['english_name'] for event in events.exclude(english_name__icontains='Score Match').exclude(english_name__icontains='Medley Festival').exclude(english_name__contains='Challenge Festival').values('english_name').distinct()]
        print '## Contest names'
        things += [contest['name'] for contest in contests.values('name').distinct()]

        print 'Save translated terms in file to generate terms'
        s = ''
        for thing in things:
            if thing:
                s += u'{% blocktrans %}' + thing + u'{% endblocktrans %}\n'
        f = open('database_translations.html', 'w')
        print >> f, s
        f.close()

