from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from api import models
from web.utils import concat_args
from web.templatetags.imageurl import ownedcardimageurl, eventimageurl
from web.utils import singlecardurl
import sys
from django.db import transaction

class Command(BaseCommand):
    can_import_settings = True

    @transaction.atomic
    def handle(self, *args, **options):

        print 'Save activity_type in activities'
        print 'To update: {}'.format(models.Activity.objects.filter(message_type=0).exclude(message='Added a card').count())
        for activity in models.Activity.objects.filter(message_type=0).exclude(message='Added a card'):
            activity.message_type = models.messageStringToInt(activity.message)
            activity.save()
        print 'Done'

