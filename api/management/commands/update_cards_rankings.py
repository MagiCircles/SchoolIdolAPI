from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models

def for_ranking(cards, attribute, ranking_type):
    previous_card_stat = 0
    i = 0
    for card in cards:
        stat = getattr(card, 'idolized_maximum_statistics_' + attribute.lower())
        if previous_card_stat != stat:
            i += 1
            previous_card_stat = stat
        previous_ranking = getattr(card, ranking_type)
        if i != previous_ranking:
            print '   ', i, card, stat
            setattr(card, ranking_type, i)
            card.save()

def update_cards_rankings(opt):
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

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_cards_rankings({})

