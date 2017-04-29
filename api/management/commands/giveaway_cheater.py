import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db.models import Count
from api import models

def print_top(hashtag):
    activities = models.Activity.objects.filter(message_data__icontains=hashtag).annotate(total_likes=Count('likes')).select_related('account', 'account__owner').order_by('-total_likes')
    top = 0
    prev = -1
    for activity in activities:
        if activity.total_likes != prev:
            top += 1
            prev = activity.total_likes
        print '# #{} [{}](http://schoolido.lu/user/{}/)'.format(
            top,
            activity.account.owner.username,
            activity.account.owner.username,
        )
        print ''
        print '  {} likes'.format(activity.total_likes + 1)
        print ''
        print '  [See original activity](http://schoolido.lu/activities/{}/)'.format(
            activity.id
        )
        print ''
        print ''

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Specify giveaway hashtag'
            return
        hashtag = args[0]
        print_top(hashtag)
        activities = models.Activity.objects.filter(message_data__icontains=hashtag).annotate(total_likes=Count('likes'))
        for activity in activities:
            print '## Activity http://schoolido.lu/activities/{}/'.format(activity.id)
            print '  Total likes: {}'.format(activity.total_likes)
            print '  Cheat likes: ',
            sys.stdout.flush()
            total_cheat = 0
            for user in activity.likes.all().select_related('preferences'):
                if True or user.accounts_set.all().count() == 0 and not user.preferences.description:
                    print user.username, ', ',
                    sys.stdout.flush()
                    activity.likes.remove(user)
                    total_cheat += 1
            if total_cheat:
                activity.save()
            print '  Total cheat likes: {}'.format(total_cheat)
            print '  Total remaining likes: {}'.format(activity.total_likes - total_cheat)

        print_top(hashtag)
