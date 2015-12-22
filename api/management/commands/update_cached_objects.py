from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models
from collections import OrderedDict
import sys
import urllib2, json
import time

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        print '## Total number of cards owners'
        cards = models.Card.objects.all()
        for card in cards:
            ownedcards = models.OwnedCard.objects.filter(card=card)
            card.total_owners = ownedcards.filter(Q(stored='Deck') | Q(stored='Album')).values('owner_account').distinct().count()
            card.total_wishlist = ownedcards.filter(stored='Favorite').values('owner_account').distinct().count()
            card.save()
            print 'Card # {}: {} owners, {} wishlist'.format(card.id, card.total_owners, card.total_wishlist)
