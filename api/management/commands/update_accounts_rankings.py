from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models
from django.db import transaction

def for_ranking(accounts, ranking_type):
    previous_account_rank = 0
    i = 0
    for account in accounts:
        if previous_account_rank != account.rank:
            i += 1
            previous_account_rank = account.rank
        previous_ranking = getattr(account, ranking_type)
        if i != previous_ranking:
            print '   ', i, account, account.rank
            setattr(account, ranking_type, i)
            account.save()

@transaction.atomic
def update_accounts_rankings(opt):
    print '## Accounts Ranking positions'
    all_accounts = models.Account.objects.filter(verified__in=[1,2,3])
    for language in models.LANGUAGE_DICT.keys():
        accounts = all_accounts.filter(language=language).order_by('-rank')
        for_ranking(accounts, 'ranking')

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_accounts_rankings({})

