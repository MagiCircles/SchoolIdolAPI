from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models
import sys

def update_cards_join_cache(opt={}):
    print '# Update cache of join objects in cards'
    cards = models.Card.objects.all().select_related('event', 'idol', 'ur_pair', 'ur_pair__idol')
    for card in cards:
        print '#' + str(card.id) + ' ',
        sys.stdout.flush()
        card.name = card.idol.name
        card.japanese_name = card.idol.japanese_name
        card.idol_school = card.idol.school
        card.idol_year = card.idol.year
        card.idol_main_unit = card.idol.main_unit
        card.idol_sub_unit = card.idol.sub_unit
        if card.event:
            card.event_japanese_name = card.event.japanese_name
            card.event_english_name = card.event.english_name
            card.event_image = unicode(card.event.image)
        if card.ur_pair:
            card.ur_pair_name = card.ur_pair.idol.name
            card.ur_pair_round_card_image = unicode(card.ur_pair.round_card_image)
            card.ur_pair_attribute = card.ur_pair.attribute
        card.save()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_cards_join_cache({})

