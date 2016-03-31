from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models

def update_account_center_cache(opt={}):
    print '# Update account center'
    accounts = models.Account.objects.filter(center__isnull=False).select_related('center', 'center__card')
    for account in accounts:
        account.center_card_transparent_image = account.center.card.transparent_idolized_image if account.center.idolized or account.center.card.is_special else account.center.card.transparent_image
        account.center_card_round_image = account.center.card.round_card_idolized_image if account.center.idolized or account.center.card.is_special else account.center.card.round_card_image
        account.center_card_attribute = account.center.card.attribute
        account.center_alt_text = unicode(account.center.card)
        account.center_card_id = account.center.card.id
        print 'Account #{} center {}'.format(account, account.center)
        account.save()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_account_center_cache({})

