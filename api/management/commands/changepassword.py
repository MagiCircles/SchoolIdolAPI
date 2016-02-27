from django.contrib.auth.management.commands import changepassword
from django.core.management.base import CommandError
from api import models
#import sys

class Command(changepassword.Command):

    def handle(self, *args, **options):

        try: username = args[0]
        except IndexError: raise CommandError('Missing argument username')

        accounts_with_transfer_code = models.Account.objects.filter(owner__username=username, transfer_code__isnull=False).exclude(transfer_code__exact='')

        if accounts_with_transfer_code:
            error_message = 'Password can\'t be changed because there are {} account(s) with a transfer code: {}. If you wish to change the password anyways, use the argument \'force\'.'.format(accounts_with_transfer_code.count(), ' '.join([account.transfer_code for account in accounts_with_transfer_code]))
            if 'force' not in args:
                raise CommandError(error_message)
            print error_message

        args = (username,)
        rtn = super(Command, self).handle(*args, **options)

        accounts_with_transfer_code.update(transfer_code='')
        return rtn
