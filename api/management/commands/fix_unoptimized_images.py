import sys
from django.core.management.base import BaseCommand, CommandError
from api import models
from web.utils import shrinkImageFromData

# Recommended to run update_cards_join_cache before running this

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        all_cards = models.Card.objects.all()
        for card in all_cards:
            for (field, f) in models.cardsImagesToName.items():
                if ((card.is_special and 'idolized' in field)
                    or (card.is_promo and 'idolized' not in field)):
                    continue
                name = f({
                    'id': card.id,
                    'firstname': card.name.split(' ')[-1] if card.name else 'Unknown',
                })
                if getattr(card, field) and unicode(getattr(card, field)) and unicode(getattr(card, field)).split('/')[-1].split('?')[0] != name:
                    data = getattr(card, field).read()
                    print u'#{id}      {old} => {new}...'.format(
                        id=card.id,
                        old=unicode(getattr(card, field)),
                        new=name
                    ),
                    sys.stdout.flush()
                    image = shrinkImageFromData(data, name)
                    image.name = name
                    setattr(card, field, image)
                    card.save()
                    print u'Done.'
