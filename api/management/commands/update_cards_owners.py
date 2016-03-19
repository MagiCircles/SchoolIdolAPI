from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models

def update_cards_owners(opt):
    print '## Total number of cards owners'
    cards = models.Card.objects.all()
    for card in cards:
        ownedcards = models.OwnedCard.objects.filter(card=card)
        previous_owners = card.total_owners
        if not previous_owners:
            previous_owners = 0
        card.total_owners = ownedcards.filter(Q(stored='Deck') | Q(stored='Album')).values('owner_account').distinct().count()
        previous_wishers = card.total_wishlist
        if not previous_wishers:
            previous_wishers = 0
        card.total_wishlist = ownedcards.filter(stored='Favorite').values('owner_account').distinct().count()
        if previous_owners != card.total_owners or previous_wishers != card.total_wishlist:
            card.save()
            print 'Card # {}: {} owners [{}{}], {} wishlist [{}{}]'.format(
                card.id,
                card.total_owners,
                '+' if card.total_owners - previous_owners > 0 else '',
                card.total_owners - previous_owners,
                card.total_wishlist,
                '+' if card.total_wishlist - previous_wishers > 0 else '',
                card.total_wishlist - previous_wishers
            )

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_cards_owners({})

