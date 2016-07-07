from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from api import models
from web.utils import concat_args
from web.templatetags.imageurl import ownedcardimageurl, eventimageurl
from web.utils import singlecardurl
import sys
import datetime
import pytz
from django.db import transaction

@transaction.atomic
def update_centers():
        print 'Update centers'
        total = 0
        for account in models.Account.objects.filter(language='JP').select_related('center', 'center__card'):
                if account.center:
                        account.center_card_round_image = account.center.card.round_card_idolized_image if account.center.idolized or account.center.card.is_special else account.center.card.round_card_image
                        account.save()
                        total += 1
        print 'Done ({})'.format(total)

@transaction.atomic
def update_activities():
        print 'Update activities'
        total = 0
        for activity in models.Activity.objects.filter(creation__gte=datetime.datetime(2016, 07, 4, 0, 0, 0, 0, pytz.UTC), message_type__in=[0, 1]).select_related('ownedcard', 'ownedcard__card', 'account'):
                if '/' in activity.right_picture: # not imgur
                        activity.right_picture = ownedcardimageurl({}, activity.ownedcard, card=activity.ownedcard.card, english_version=(activity.account.language != 'JP'))
                        activity.save()
                        total += 1
        print 'Done ({})'.format(total)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        update_centers()
        update_activities()
