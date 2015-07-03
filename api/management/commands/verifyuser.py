from django.core.management.base import BaseCommand, CommandError
from api.models import Account
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Specify account'
            return
        account_id = int(args[0])
        account = Account.objects.get(pk=account_id)
        print "Set verification level for the account " + account.nickname + " (user is " + account.owner.username + ")"

        while True:
            print 'Specify verification level (Gold = 2, Silver = 1, Bronze = 3): '
            line = sys.stdin.readline()
            try:
                choice = int(line)
            except ValueError:
                continue
            if choice != 1 and choice != 2 and choice != 3:
                continue
            else:
                account.verified = choice
                account.save()
                break
        return
