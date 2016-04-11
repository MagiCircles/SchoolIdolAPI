from django.core.management.base import BaseCommand, CommandError
from api import models
import urllib2, urllib
import json
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if 'songs' in args:
            page_url = u'http://schoolido.lu/api/songs/'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for song in data['results']:
                    models.Song.objects.filter(name=song['name']).update(image=song['image'].replace('http://i.schoolido.lu/', ''))
            return

        if 'clean_ur' in args:
            page_url = u'http://schoolido.lu/api/cards/?rarity=UR'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for card in data['results']:
                    models.Card.objects.filter(id=card['id']).update(clean_ur=card['clean_ur'].replace('http://i.schoolido.lu/', ''),
                                                                     clean_ur_idolized=card['clean_ur_idolized'].replace('http://i.schoolido.lu/', ''))
            return

        cards = models.Card.objects.all()
        for card in cards:
            card.card_idolized_image = 'cards/' + str(card.id) + 'idolized' + card.name.split(' ')[-1] + '.png'
            card.transparent_idolized_image = 'cards/transparent/' + str(card.id) + 'idolizedTransparent.png'
            card.round_card_idolized_image = 'cards/' + str(card.id) + 'RoundIdolized' + card.name.split(' ')[-1] + '.png'
            if not card.is_special and not card.is_promo:
                card.card_image = 'cards/' + str(card.id) + card.name.split(' ')[-1] + '.png'
                card.transparent_image = 'cards/transparent/' + str(card.id) + 'Transparent.png'
                card.round_card_image = 'cards/' + str(card.id) + 'Round' + card.name.split(' ')[-1] + '.png'
            else:
                card.card_image = None
                card.transparent_image = None
                card.round_card_image = None
            card.save()
