from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q
from api import models

def update_event_ranking_cache(opt={}):
    print '# Update event ranking cache'
    participations = models.EventParticipation.objects.filter(account_owner_status__isnull=True).select_related('account', 'account__owner', 'account__owner__preferences')
    for participation in participations:
        participation.account_language = participation.account.language
        participation.account_link = '/user/' + participation.account.owner.username + '/#' + str(participation.account.id)
        participation.account_picture = participation.account.owner.preferences.avatar(size=100)
        participation.account_name = unicode(participation.account)
        participation.account_owner = participation.account.owner.username
        participation.account_owner_status = participation.account.owner.preferences.status
        print participation
        participation.save()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_event_ranking_cache({})

