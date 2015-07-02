from django.core.management.base import BaseCommand, CommandError
from api import models
from django.db.models import Count, Q

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if 'NR' in args:
            print 'Delete activities of N/R cards'
            activities = models.Activity.objects.filter(Q(ownedcard__card__rarity='R') | Q(ownedcard__card__rarity='N'))
            count = activities.count()
            activities.delete()
            print '  Deleted %d activities.' % (count)

        print 'Delete activities > 50 per user'
        accounts = models.Account.objects.all()
        for account in accounts:
            to_keep = models.Activity.objects.filter(account=account).order_by('-creation')[:50]
            to_delete = models.Activity.objects.filter(account=account).exclude(pk__in=to_keep.values('pk'))
            count = to_delete.count()
            if count > 0:
                to_delete.delete()
                print '  %s Deleted %d activities.' % (account, count)
