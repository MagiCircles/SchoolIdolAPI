from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from api import models
from web.utils import concat_args
from web.templatetags.imageurl import ownedcardimageurl, eventimageurl
import sys

def activity_cache_account(activity, account):
    activity.account_link = '/user/' + account.owner.username + '/#' + str(account.id)
    activity.account_picture = account.owner.preferences.avatar(size=100)
    activity.account_name = unicode(account)
    return activity

def get_ownedcardqueryset():
    return models.Activity.objects.filter(Q(message='Added a card') | Q(message='Idolized a card')).filter(right_picture__isnull=True).prefetch_related('ownedcard', 'ownedcard__card', 'ownedcard__owner_account', 'ownedcard__owner_account__owner', 'ownedcard__owner_account__owner__preferences')

def get_rankupqueryset():
    return models.Activity.objects.filter(message='Rank Up').filter(message_data__isnull=True).prefetch_related('account', 'account__owner', 'account__owner__preferences')

def get_rankeventqueryset():
    return models.Activity.objects.filter(message='Ranked in event').filter(message_data__isnull=True).prefetch_related('account', 'account__owner', 'account__owner__preferences', 'eventparticipation', 'eventparticipation__event')

def get_rankevent_withoutranking_queryset():
    return models.Activity.objects.filter(message='Ranked in event').filter(Q(eventparticipation__ranking__isnull=True) | Q(eventparticipation__ranking=0))

def get_duplicateownedcard_queryset():
    return models.Activity.objects.filter(ownedcard__isnull=False).order_by('ownedcard_id', 'id')

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        print 'Delete activities max bonded/max leveled...'
        while models.Activity.objects.filter(Q(message='Max Leveled a card') | Q(message='Max Bonded a card')).count():
            ids = list(models.Activity.objects.filter(Q(message='Max Leveled a card') | Q(message='Max Bonded a card')).values_list('pk', flat=True)[:100])
            total_this = models.Activity.objects.filter(pk__in=ids).delete()
        print 'Done.'

        print 'Delete activities rank in event without ranking...'
        while get_rankevent_withoutranking_queryset().count():
            ids = list(get_rankevent_withoutranking_queryset().values_list('pk', flat=True)[:100])
            total_this = get_rankevent_withoutranking_queryset().filter(pk__in=ids).delete()
        print 'Done.'

        print 'Cache for owned cards activities'
        while get_ownedcardqueryset().count():
            activities_ownedcards = get_ownedcardqueryset()[:500]
            for activity in activities_ownedcards:
                account = activity.ownedcard.owner_account
                # Fix account
                activity.account = account
                # Cache
                activity = activity_cache_account(activity, account)
                activity.message_data = concat_args(unicode(activity.ownedcard.card), activity.ownedcard.stored)
                activity.right_picture_link = '/cards/' + str(activity.ownedcard.card.id) + '/'
                activity.right_picture = ownedcardimageurl({}, activity.ownedcard)
                activity.save()
            print '.',
            sys.stdout.flush()
        print 'Done.'

        print 'Cache for rank up activities'
        while get_rankupqueryset().count():
            activities_rankup = get_rankupqueryset()[:500]
            for activity in activities_rankup:
                # Cache
                activity = activity_cache_account(activity, activity.account)
                activity.message_data = concat_args(activity.number)
                activity.save()
            print '.',
            sys.stdout.flush()
        print 'Done.'

        print 'Cache for Rank in event activities'
        while get_rankeventqueryset().count():
            activities_rankevent = get_rankeventqueryset()[:500]
            for activity in activities_rankevent:
                # Cache
                activity = activity_cache_account(activity, activity.account)
                activity.message_data = concat_args(activity.eventparticipation.ranking,
                                                    unicode(activity.eventparticipation.event))
                activity.right_picture = eventimageurl({}, activity.eventparticipation.event, english=(activity.account.language != 'JP'))
                activity.right_picture_link = '/events/' + activity.eventparticipation.event.japanese_name + '/'
                activity.save()
            print '.',
            sys.stdout.flush()
        print 'Done.'

        print 'Remove duplicate activities with ownedcards'
        lastSeenId = float('-Inf')
        i = 0
        total_deleted = 0
        while get_duplicateownedcard_queryset()[i:i+500].count():
            activities_ownedcards = get_duplicateownedcard_queryset()[i:i+500]
            for activity in activities_ownedcards:
                if activity.ownedcard_id == lastSeenId:
                    print 'delete', activity
                    activity.delete()
                    total_deleted += 1
                else:
                    lastSeenId = activity.ownedcard_id
                pass
            i += 500
            print '.',
            sys.stdout.flush()
        print 'Done.'
