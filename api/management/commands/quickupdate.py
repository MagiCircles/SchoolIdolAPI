from django.core.management.base import BaseCommand, CommandError
from api import models
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

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
