from django.core.management.base import BaseCommand, CommandError
from api import models
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        cards = models.Card.objects.all().order_by('id')
        release_date = None
        for card in cards:
            if card.release_date:
                release_date = card.release_date
            else:
                print 'Edit #{} release date {} {}'.format(card.id, release_date, card.is_promo or card.is_special)
                card.release_date = release_date
                card.save()

