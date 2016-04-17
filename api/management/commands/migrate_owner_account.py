from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from api import models
from web.utils import concat_args
from web.templatetags.imageurl import ownedcardimageurl, eventimageurl
from web.utils import singlecardurl
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        print 'Save owner of account'
        for account in models.Account.objects.all().select_related('owner'):
            account.owner_username = account.owner.username
            account.save()
            print account.id,
        print 'Done'

