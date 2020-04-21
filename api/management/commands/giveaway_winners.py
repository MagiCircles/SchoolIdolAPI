# -*- coding: utf-8 -*-
import sys, datetime, operator, urllib
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.utils.formats import dateformat, date_format
from django.utils import timezone
from django.utils.six.moves import input
from api import models
from web.views import PDP_IDOLS
from web.utils import chibiimage

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

def get_days(idol):
    if idol.name in PDP_IDOLS or not idol.main:
        return 6, 5
    if idol.main_unit == 'Aqours':
        return 6, 6
    # muse
    return 8, 5

def get_with_staff_picks(idol):
    return idol.name not in PDP_IDOLS and idol.main

def get_birthday(idol):
    today = datetime.date.today()
    in_300_days = today + relativedelta(days=300)
    next_birthday = get_next_birthday(idol.birthday)
    if next_birthday >= in_300_days:
        next_birthday = next_birthday.replace(next_birthday.year - 1)
    return next_birthday

def get_countdown_url(date, days, title):
    new_date = date + relativedelta(days=days)
    return (
        new_date,
        'https://www.timeanddate.com/countdown/birthday?iso={}T11&p0=%3A&msg={}&font=sanserif&csz=1'.format(
            dateformat.format(new_date, "Ymd"),
            title.replace(' ', '+')
        )
    )

def get_other_giveaways(hashtag):

    birthday_idols = models.Idol.objects.filter(
        Q(main=True) | Q(name__in=PDP_IDOLS),
    ).filter(birthdays_within(days_after=50, days_before=16))

    today = datetime.date.today()
    in_51_days = today + relativedelta(days=51)
    in_300_days = today + relativedelta(days=300)
    ended_recently = []
    still_running_giveaways = []
    voting_ongoing_giveaways = []
    coming_soon_giveaways = []
    current_idol = None

    for idol in birthday_idols:
        if idol.name == 'Emma Verde':
            idol.name = 'Verde Emma'
        if idol.name == 'Tsushima Yoshiko':
            idol.name = 'Tsushima Yohane'
        birthday = get_birthday(idol)

        giveaway_tags = [
                u'{}BirthdayGiveaway{}'.format(idol.short_name, birthday.year),
                u'{}FanAwards{}'.format(idol.short_name, birthday.year),
        ]
        if hashtag in giveaway_tags:
            # Current giveaway idol
            current_idol = idol
            continue

        filter_tag = Q()
        for giveaway_tag in giveaway_tags:
            filter_tag |= Q(message_data__contains=giveaway_tag)
        giveaway_posts = models.Activity.objects.filter(
            filter_tag,
            account_id=1,
        ).order_by('id')

        try:
            giveaway_details = giveaway_posts.filter(message_data__icontains='How to enter?')[0]
        except IndexError:
            giveaway_details = None

        try:
            giveaway_winners_post = giveaway_posts.filter(message_data__icontains='Congratulations to our winners!')[0]
            ended_recently.append((idol, giveaway_winners_post))
        except IndexError:
            giveaway_winners_post = None

        giveaway_ended_post = None
        try:
            giveaway_ended_post = giveaway_posts.filter(message_data__icontains='We\'re entering the last phase of')[0]
            if not giveaway_winners_post:
                giveaway_hashtag = None
                for tag in giveaway_tags:
                    if tag in giveaway_tags:
                        giveaway_hashtag = tag
                voting_ongoing_giveaways.append((idol, giveaway_ended_post, giveaway_details, tag))
        except IndexError:
            pass

        if giveaway_details and not giveaway_ended_post and not giveaway_winners_post:
            still_running_giveaways.append((idol, giveaway_details))

        if not giveaway_details:
            coming_soon_giveaways.append(idol)

        if birthday >= in_51_days and not giveaway_details:
            print '!! Warning:', idol.name, 'giveaway should have been organized already!'

    coming_soon_giveaways.sort(key=lambda i: i.birthday)
    return current_idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways

def get_image(current_giveaway):
    return current_giveaway.message_data.split(')')[0] + ')'

def get_small_image(current_giveaway):
    if not '#small' in current_giveaway.message_data:
        return None
    return current_giveaway.message_data.split('#small')[0].split('(')[-1]

def get_entry_image_url(activity):
    try:
        return u'![{})'.format(activity.message_data.split('![')[1].split(')')[0])
    except IndexError:
        return None

def print_support_us():
    print '# **![Support our giveaways!](https://i.imgur.com/2hI2BLn.png)**'
    print ''
    print '[![Support us on Patreon](https://i.imgur.com/VNqYEXt.png)](http://patreon.com/db0company)'
    print ''
    print 'These giveaways are made possible thanks to the support of our warm-hearted donators. If you wish to support School Idol Tomodachi for both our future giveaways and to cover the cost of our expensive servers in which our site run, please consider [donating on Patreon](http://patreon.com/db0company).'

def print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=False):
    if still_running_giveaways:
        print ''
        if with_icons:
            for idol, giveaway in still_running_giveaways:
                small_image = get_small_image(giveaway)
                if small_image:
                    print '![{idol_name} Fan Awards]({url})'.format(
                        idol_name=idol.name,
                        url=small_image,
                    )
                    print ''
        print u'{} {} currently running! Take your chance and enter!'.format(
            u' and '.join([
                u'[{idol_name} Fan Awards](https://schoolido.lu/activities/{id}/)'.format(
                    idol_name=idol.name, id=giveaway.id,
                )
                for idol, giveaway in still_running_giveaways
            ]),
            'is' if len(still_running_giveaways) == 1 else 'are',
        )
        print ''

    if voting_ongoing_giveaways:
        print ''
        if with_icons:
            for idol, giveaway, giveaway_details, hashtag in voting_ongoing_giveaways:
                small_image = get_small_image(giveaway_details)
                if small_image:
                    print '![{idol_name} Fan Awards]({url})'.format(
                        idol_name=idol.name,
                        url=small_image,
                    )
                    print ''
        print u'{} entry period{} just closed! Go check out all the entries and like your favorites!'.format(
            u' and '.join([
                u'[{idol_name} Fan Awards](https://schoolido.lu/activities/{id}/)'.format(
                    idol_name=idol.name, id=giveaway.id,
                )
                for idol, giveaway, giveaway_details, hashtag in voting_ongoing_giveaways
            ]),
            's' if len(voting_ongoing_giveaways) > 1 else ''
        )
        for idol, giveaway, giveaway_details, hashtag in voting_ongoing_giveaways:
            print ''
            print u'- [See {idol_name} Fan Awards entries](https://schoolido.lu/#search={hashtag}) *right click to open in new tab*'.format(
                    idol_name=idol.name, hashtag=hashtag,
                )
        print ''

    if coming_soon_giveaways:
        if with_icons:
            print ''
            for idol in coming_soon_giveaways:
                print '[![{name}]({icon_url})](https://schoolido.lu/idol/{url_name})'.format(
                    name=idol.name,
                    icon_url=chibiimage(idol.name, small=True, force_artist='klab', force_first=False, force_https=True),
                    url_name=urllib.quote(idol.name),
                )
        print ''
        print_idol = lambda idol: u'[{}](https://schoolido.lu/idol/{}/) ({})'.format(
            idol.name,
            urllib.quote(idol.name),
            date_format(idol.birthday, format='MONTH_DAY_FORMAT', use_l10n=True),
        )
        print 'The birthday{} of {} {} coming soon, so look forward to their Fan Awards as well!'.format(
            '' if len(coming_soon_giveaways) == 1 else 's',
            ' and '.join([
                u', '.join([
                    print_idol(idol)
                    for idol in coming_soon_giveaways[:-1]
                ]),
                print_idol(coming_soon_giveaways[-1]),
            ]),
            'is' if len(coming_soon_giveaways) == 1 else 'are'
        )

def delete_cheat_likes(hashtag, id_details, id_end):
    activities = models.Activity.objects.filter(
        message_data__icontains=hashtag,
        id__gt=id_details,
    ).exclude(
        message_data__icontains='Congratulations to our winners!',
    )
    if id_end:
        activities = activities.filter(
            id__lt=id_end,
        ).exclude(
            id=id_end,
        )
    activities = activities.annotate(total_likes=Count('likes'))
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

def print_top(winners, lucky=False):
    rank = 0
    prev = -1
    for activity in winners:
        if activity.total_likes != prev:
            rank += 1
            prev = activity.total_likes
        if rank == 1:
            if lucky:
                print '# ![#1 Lucky Winner - elected by the community](https://i.imgur.com/tpQXUQo.png)'
            else:
                print '# ![#1 Crowd\'s Favorite Winner - elected by the community](https://i.imgur.com/0jKB10n.png)'
        if rank == 2:
            print '# ![Runner up Crowd\'s Favorite Winner](https://i.imgur.com/jPZp57t.png)'
        print '### {}[{}](http://schoolido.lu/user/{}/)'.format(
            u'#{} '.format(rank) if rank not in [1,2] else '',
            activity.account.owner.username,
            activity.account.owner.username,
        )
        # print ''
        # print '    {} likes'.format(activity.total_likes + 1)
        print ''
        print '[See entry](http://schoolido.lu/activities/{}/)'.format(
            activity.id,
        )
        image = get_entry_image_url(activity)
        if image:
            print ''
            print u'[{}](http://schoolido.lu/activities/{}/)'.format(image, activity.id)
            print ''
        print ''

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if len(args) < 2:
            print 'Specify id of giveaway details, id of giveaway end post (or NONE), number of likes winners (default = 0)'
            return
        giveaway_details_id = int(args[0])

        if args[1] == 'NONE':
            giveaway_end_id = None
        else:
            giveaway_end_id = int(args[1])

        try:
            total_winners = int(args[2])
        except IndexError:
            total_winners = 0

        giveaway = models.Activity.objects.get(id=giveaway_details_id)
        if giveaway_end_id:
            end_giveaway = models.Activity.objects.get(id=giveaway_end_id)
        hashtag = giveaway.message_data.split('[See all participants](http://schoolido.lu/#search=')[1].split(')')[0]

        idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        if not idol:
            try:
                idol = models.Idol.objects.filter(name__contains=u' {}'.format(hashtag.split('Fan')[0]))[0]
            except:
                try:
                    idol = models.Idol.objects.filter(name=hashtag.split('Fan')[0])[0]
                except:
                    print 'Can\'t find idol'
                    return

        delete_cheat_likes(hashtag, giveaway_details_id, giveaway_end_id)

        queryset = models.Activity.objects.exclude(
            id=giveaway_details_id,
        ).exclude(
            message_data__icontains='Congratulations to our winners!',
        ).filter(
            message_data__icontains=hashtag,
            id__gt=giveaway_details_id,
        )
        if giveaway_end_id:
            queryset = queryset.filter(
                id__lt=giveaway_end_id,
            ).exclude(
                id=giveaway_end_id,
            )
        print queryset
        queryset = queryset.annotate(total_likes=Count('likes')).select_related('account', 'account__owner')

        winners = queryset.order_by('-total_likes')[:total_winners]
        print winners

        print ''
        print ''
        print 'Winning entries: {}'.format(','.join([str(w.id) for w in winners]))
        print ''
        # Prompt to ask for staff pick winner(s)

        if queryset.count() >= 30:

            staff_pick_winners = None
            try:
                staff_pick_winners = input('Enter list of staff pick winner ids: ')
            except KeyboardInterrupt:
                print ''
                print 'Operation cancelled.'
                sys.exit(1)
            staff_pick_winners = [int(id) for id in staff_pick_winners.split(',')]
            honorable_mentions = None
            try:
                honorable_mentions = input('Enter list of honorable mentions: ')
            except KeyboardInterrupt:
                print ''
                print 'Operation cancelled.'
                sys.exit(1)
            honorable_mentions = [int(id) for id in honorable_mentions.split(',')]
            
            has_staff_picks_winners = staff_pick_winners != [0]
            has_honorable_mentions = honorable_mentions != [0]

        else:
            staff_pick_winners = []
            honorable_mentions = []
            has_staff_picks_winners = False
            has_honorable_mentions = False
    
        remaining_entries = queryset.exclude(id__in=staff_pick_winners)

        if total_winners:
            likes_winners = remaining_entries.order_by('-total_likes')[:total_winners]
            remaining_entries = remaining_entries.exclude(id__in=[w.id for w in likes_winners])
        else:
            likes_winners = []
 
        random_winners = remaining_entries.order_by('?')[:1]
        remaining_entries = remaining_entries.exclude(id__in=[w.id for w in random_winners])

        remaining_entries = remaining_entries.exclude(id__in=honorable_mentions).order_by('?')

        print ''
        print '--------- START OF POST TO COPY'
        print ''

        print get_image(giveaway)
        print ''
        print '## The winner{} of {} {} Fan Awards {}...'.format('s' if total_winners or has_staff_picks_winners else '', hashtag[-4:], idol.name, 'are' if total_winners else 'is')
        print ''
        if has_staff_picks_winners:
            print '--------- COPY GRAND WINNERS HERE'
            print ''
            print '***'

        if total_winners:
            print_top(likes_winners)

        print_top(random_winners, lucky=True)

        print ''
        print '***'
        print ''
        print ''
        if has_honorable_mentions:
            print '--------- COPY HONORABLE MENTIONS HERE'
        print ''
        if remaining_entries and has_honorable_mentions:
            print ''
            for i, activity in enumerate(remaining_entries):
                if True: # change to True/False based on rds commented on all entries
                    print u'**[{username}](https://schoolido.lu/user/{username}/)** - [See activity](http://schoolido.lu/activities/{id}/)'.format(
                        username=activity.account.owner.username,
                        id=activity.id,
                    )
                    # print '    - rdsathene *(School Idol Tomodachi staff;Donator)*: ""'
                    print '    - ""'
                    print ''
                else:
                    print u'[{}](http://schoolido.lu/activities/{}/){}'.format(
                        activity.account.owner.username,
                        activity.id,
                        ', ' if i + 1 < len(remaining_entries) else '',
                    )
            print ''
        elif remaining_entries:
            print 'Other participants:'
            print ''
            for i, activity in enumerate(remaining_entries):
                print u'[{}](http://schoolido.lu/activities/{}/){}'.format(
                    activity.account.owner.username,
                    activity.id,
                    ', ' if i + 1 < len(remaining_entries) else '',
                )
            print ''
        print '***'
        print ''
        print '# **Congratulations to our winner{}!**'.format('s' if total_winners or has_staff_picks_winners else '')
        print ''
        print 'They will receive a prize of their choice among the {current_idol}-themed goodies we offer. You can see the list of prizes with pictures in [the original awards details post](https://schoolido.lu/activities/{current_giveaway_id}/).'.format(
            current_idol=idol.short_name if idol else 'Love Live',
            current_giveaway_id=giveaway_details_id,
        )
        print ''
        print 'Thanks to everyone who participated and helped make this contest a success! We loved your entries!'
        print ''
        print '***'
        print ''
        print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=True)
        print ''
        print '***'
        print ''
        print_support_us()
        print ''
        print '***'
        print ''
        print '# **![F.A.Q.](https://i.imgur.com/vghSFuS.png)**'
        print ''
        print '- **I won and I didn\'t hear from you?**'
        print '    - Check [your private messages](https://schoolido.lu/messages/). You may have to wait up to 24 hours after announcement.'
        print '- **I didn\'t win and I\'m sad ;_;**'
        print '    - Sorry :( Regardless, the staff and the community loved your entry so your efforts didn\'t go to waste at all <3 Please join our next giveaway to try again!'
        print '- **How can  I thank you for your amazing work organizing these contests?**'
        print '    - We always appreciate sweet comments below, and if you want to push it a little further, we have a [Patreon](https://patreon.com/db0company/) open for donations <3'
        print '- **More questions?**'
        print '    - Read the [Giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ) and ask your questions in the comments.'
        print ''
        print '***'
        print ''
        print '## What did you think about this contest?'
        print ''
        print 'We want to hear from you! Based on your opinion, we may or may not organize a similar contest next year.'
        print ''
        print u'→ [Take the survey!](https://goo.gl/forms/PVErf176nH0LX9go2)'
        print ''
        print u'Thank you ♥️'
        print ''
        print '***'
        print ''
        print 'We\'re looking for judges. [Join us!](https://goo.gl/forms/42sCU6SXnKbqnag23)'
        print ''
        print '***'
        print ''
        print '[See awards details and prizes](https://schoolido.lu/activities/{}/)'.format(giveaway_details_id)
        print ''
        print '###### {}'.format(hashtag)
        print ''
        print '--------- END OF POST TO COPY'
        print ''
        print ''
        print 'List of entries by like:'
        print ''
        for activity in queryset.order_by('-total_likes'):
            print u'{} likes - {}{} - http://schoolido.lu/activities/{}/'.format(
                activity.total_likes + 1,
                activity.account.owner.username,
                u' ({})'.format(activity.account.nickname) if activity.account.nickname != activity.account.owner.username else '',
                activity.id)
        print ''
        print ''
