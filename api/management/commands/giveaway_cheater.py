import sys, datetime, operator
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.utils.formats import date_format
from django.utils import timezone
from api import models

def birthdays_within(days_after, days_before=0, field_name='birthday'):
    now = timezone.now()
    after = now - datetime.timedelta(days=days_before)
    before = now + datetime.timedelta(days=days_after)

    monthdays = [(now.month, now.day)]
    while after <= before:
        monthdays.append((after.month, after.day))
        after += datetime.timedelta(days=1)

    # Tranform each into queryset keyword args.
    monthdays = (dict(zip((
        u'{}__month'.format(field_name),
        u'{}__day'.format(field_name),
    ), t)) for t in monthdays)

    # Compose the djano.db.models.Q objects together for a single query.
    return reduce(operator.or_, (Q(**d) for d in monthdays))

def get_next_birthday(birthday):
    today = datetime.date.today()

    is_feb29 = False
    if birthday.month == 2 and birthday.day == 29:
        is_feb29 = True
        birthday = birthday.replace(
            month=user.preferences.birthdate.month + 1,
            day=1,
        )

    birthday = birthday.replace(year=today.year)
    if birthday < today:
        birthday = birthday.replace(year=today.year + 1)

    if is_feb29:
        try: birthday = birthday.replace(month=2, day=29)
        except ValueError: pass

    return birthday

def print_top(hashtag, winners, id, print_message_between=False):
    activities = models.Activity.objects.filter(id__gt=id, message_data__icontains=hashtag).annotate(total_likes=Count('likes')).select_related('account', 'account__owner').order_by('-total_likes')
    top = 0
    prev = -1
    has_printed = False
    to_print_at_the_end_for_form = []
    for activity in activities:
        if activity.total_likes != prev:
            top += 1
            prev = activity.total_likes
        if top > winners:
            if print_message_between and not has_printed:
                print '***'
                print ''
                print '**Don\'t see your name?** Don\'t worry, our staff team will go through all the activities and pick 1 more winner based on creativity, originality, effort and passion.'
                print ''
                print '***'
                print ''
                print 'Participants:'
                print ''
                has_printed = True
            if print_message_between:
                to_print_at_the_end_for_form.append(activity)
                sys.stdout.write(u'[{}](http://schoolido.lu/activities/{}/), '.format(activity.account.owner.username, activity.id))
            else:
                print u'{} - http://schoolido.lu/activities/{}/'.format(activity.account.owner.username, activity.id)
            continue
        print '### #{} [{}](http://schoolido.lu/user/{}/)'.format(
            top,
            activity.account.owner.username,
            activity.account.owner.username,
        )
        print ''
        print '    {} likes'.format(activity.total_likes + 1)
        print ''
        print '[See original activity](http://schoolido.lu/activities/{}/)'.format(
            activity.id
        )
        try:
            print ''
            print u'![{})'.format(activity.message_data.split('![')[1].split(')')[0])
            print ''
        except IndexError:
            pass
        print ''

    if print_message_between:
        sys.stdout.flush()



        print ''
        print ''
        print '***'
        print ''
        print '[See giveaway details](https://schoolido.lu/activities/{}/)'.format(id)
        print ''

        print '--------- END OF POST TO COPY'
        print ''
        print ''


        for activity in to_print_at_the_end_for_form:
            print u'{} - http://schoolido.lu/activities/{}/'.format(activity.account.owner.username, activity.id)


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if len(args) < 3:
            print 'Specify giveaway hashtag, number of winners and id of giveaway details'
            return
        hashtag = args[0]
        winners = int(args[1])
        id = int(args[2])
        current_giveaway = models.Activity.objects.get(id=id)

        birthday_idols = models.Idol.objects.filter(
            main=True,
        ).filter(birthdays_within(days_after=15, days_before=30))

        today = datetime.date.today()
        in_31_days = today + relativedelta(days=31)
        ended_recently = []
        still_running_giveaways = []
        coming_soon_giveaways = []

        for idol in birthday_idols:
            giveaway_tag = u'{}BirthdayGiveaway2018'.format(idol.short_name)
            if giveaway_tag == hashtag:
                # Current giveaway idol
                continue
            giveaway_posts = models.Activity.objects.filter(message_data__icontains=giveaway_tag, account_id__in=[1]).order_by('id')
            try:
                giveaway_details = giveaway_posts.filter(message_data__icontains='How to enter?')[0]
            except IndexError:
                giveaway_details = None
            try:
                giveaway_ended_post = giveaway_posts.filter(message_data__icontains='See giveaway details')[0]
                ended_recently.append((idol, giveaway_ended_post))
            except IndexError:
                giveaway_ended_post = None

            if giveaway_details and not giveaway_ended_post:
                still_running_giveaways.append((idol, giveaway_details))

            if not giveaway_details:
                coming_soon_giveaways.append(idol)

            next_birthday = get_next_birthday(idol.birthday)
            if next_birthday >= in_31_days and not giveaway_details:
                print '!! Warning:', idol.name, 'giveaway should have been organized already!'

        print_top(hashtag, winners, id)
        activities = models.Activity.objects.filter(id__gt=id, message_data__icontains=hashtag).annotate(total_likes=Count('likes'))
        for activity in activities:
            print '## Activity http://schoolido.lu/activities/{}/'.format(activity.id)
            print '  Total likes: {}'.format(activity.total_likes)
            print '  Cheat likes: ',
            sys.stdout.flush()
            total_cheat = 0
            for user in activity.likes.all().select_related('preferences'):
                total_accounts = user.accounts_set.all().count()
                if (False and (total_accounts == 0
                     or (total_accounts == 1 and user.accounts_set.all()[0].ownedcards.count() <= 1))
                    and not user.preferences.description
                    and not models.Activity.objects.filter(account__owner=user, message_type=models.ACTIVITY_TYPE_CUSTOM).count()
                    and not user.links.all().count()
                ):
                    print user.username, ', ',
                    sys.stdout.flush()
                    activity.likes.remove(user)
                    total_cheat += 1
            if total_cheat:
                activity.save()
            print ''
            print '  Total cheat likes: {}'.format(total_cheat)
            print '  Total remaining likes: {}'.format(activity.total_likes - total_cheat)

        print ''
        print '--------- START OF POST TO COPY'
        print ''

        print current_giveaway.message_data.split('\n# **Support our giveaways!**')[0]
        print '# Congratulations to our winners!'
        print ''
        print 'They will receive a prize of their choice among the {current_idol}-themed goodies we offer. You can see the list of prizes with pictures in [the original giveaway post](https://schoolido.lu/activities/{current_giveaway_id}/).'.format(
            current_idol=hashtag.split('BirthdayGiveaway')[0],
            current_giveaway_id=id,
        )
        print ''
        print 'Thanks to everyone who participated and helped make this contest a success!'
        if still_running_giveaways:
            print ''
            print 'Stay tuned for the winners of',
            for idol, giveaway in still_running_giveaways:
                print u'{} that will be announced soon!'.format(u' and '.join([
                    u'[{idol_name}\'s Birthday giveaway](https://schoolido.lu/activities/{id}/)'.format(
                        idol.name, giveaway.id,
                    )
                    for idol, giveaway in still_running_giveaways
                ]))
            print ''

        if coming_soon_giveaways:
            print ''
            print 'The birthday{} of {} {} coming soon, so look forward to that as well!'.format(
                '' if len(coming_soon_giveaways) == 1 else 's',
                ' and '.join([
                    u'{} ({})'.format(
                        idol.name,
                        date_format(idol.birthday, format='MONTH_DAY_FORMAT', use_l10n=True),
                    )
                    for idol in coming_soon_giveaways
                ]),
                'is' if len(coming_soon_giveaways) == 1 else 'are'
            )

        print ''
        print '***'
        print ''
        print '## Winners'
        print ''

        print_top(hashtag, winners, id, print_message_between=True)
