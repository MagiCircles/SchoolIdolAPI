from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models
from collections import OrderedDict
import sys
import urllib2, json
import time

def for_ranking(cards, attribute, ranking_type):
    previous_card_stat = 0
    i = 0
    for card in cards:
        stat = getattr(card, 'idolized_maximum_statistics_' + attribute.lower())
        if previous_card_stat != stat:
            i += 1
            previous_card_stat = stat
        print '   ', i, card, stat
        setattr(card, ranking_type, i)
        card.save()

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

        print '## Ranking positions'
        all_cards = models.Card.objects.filter(is_special=False, idolized_maximum_statistics_smile__gt=0)
        for attribute in models.ATTRIBUTE_ARRAY:
            if attribute != 'All':
                cards = all_cards.filter(attribute=attribute).order_by('-idolized_maximum_statistics_' + attribute.lower())
                print '# Ranking attribute ' + attribute
                for_ranking(cards, attribute, 'ranking_attribute')
                for rarity in models.RARITY_DICT.keys():
                    cards_rarity = cards.filter(rarity=rarity)
                    print '# Ranking attribute ' + attribute + ' rarity ' + rarity
                    for_ranking(cards_rarity, attribute, 'ranking_rarity')
                print '# Ranking event SR'
                event_cards_SR = cards.filter(event__isnull=False, rarity='N')
                for_ranking(event_cards_SR, attribute, 'ranking_special')
                print '# Ranking event N'
                event_cards_N = cards.filter(event__isnull=False, rarity='SR')
                for_ranking(event_cards_N, attribute, 'ranking_special')
                print '# Ranking promo'
                promo_cards = cards.filter(is_promo=True)
                for_ranking(promo_cards, attribute, 'ranking_special')
