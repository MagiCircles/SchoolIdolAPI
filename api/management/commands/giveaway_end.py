from django.core.management.base import BaseCommand, CommandError
from giveaway_winners import (
    get_other_giveaways,
    get_days,
    get_image,
    get_birthday,
    get_countdown_url,
    print_still_running_and_coming_soon,
)
from api import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if len(args) < 1:
            print 'Specify giveaway details id'
            return
        id = int(args[0])
        giveaway = models.Activity.objects.get(id=id)
        hashtag = giveaway.message_data.split('[See all participants](http://schoolido.lu/#search=')[1].split(')')[0]

        idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        if not idol:
            try:
                idol_name = hashtag.split('Birthday')[0].split('FanAwards')[0]
                idol = models.Idol.objects.filter(name__contains=u' {}'.format(idol_name))[0]
            except:
                print 'Can\'t find idol'
                return

        days_to_enter, days_to_vote = get_days(idol)
        birthday = get_birthday(idol)
        end_date, countdown_url = get_countdown_url(
            birthday, days_to_enter + days_to_vote,
            '{} Birthday Giveaway winners announcement'.format(idol.short_name),
        )
        entries = models.Activity.objects.exclude(message_data__contains='JustForFun').filter(id__gt=id, message_data__icontains=hashtag).order_by('?')
        non_participating_entries = models.Activity.objects.filter(message_data__contains='JustForFun').filter(id__gt=id, message_data__icontains=hashtag).order_by('?')
        total_entries = entries.count()
        total_non_participating_entries = non_participating_entries.count()

        print ''
        print '--------- START OF POST TO COPY'
        print ''
        print get_image(giveaway)
        print ''
        print '# **Stretch goal reached!**'
        print ''
        print 'With a total of {} participating entries{}, we are proud to announce that there will be {} Grand winner{}, a Crowd\'s Favorite winner, and a Lucky winner!'.format(
            total_entries,
            '' if not total_non_participating_entries else ' *- and {} non-participating celebratory posts -*',
            '2' if total_entries >= 50 else 'a',
            's' if total_entries >= 50 else '',
        ) 
        print ''
        if total_entries >= 50:
            print '![All winners](https://i.imgur.com/HiaFNdW.png)'
        else:
            print '![All winners](https://i.imgur.com/tnKH2BK.png)'
        print ''
        print 'To give some time to our judges to pick the {}Grand winner{}, we will announce **all** the winners in {} days.'.format(
            '2 ' if total_entries >= 50 else '',
            's' if total_entries >= 50 else '',
            days_to_vote,
        ) 
        print ''
        print '### [Countdown before we announce the winners]({})'.format(countdown_url)
        print ''
        print '***'
        print ''
        print '- You can still post with the hashtag, but your post won\'t be eligible for prizes.'
        print '- Our judges panel is going through all the entries to select the ones who truly went above and beyond to celebrate {}\'s birthday.'.format(idol.short_name)
        print ''
        print '***'
        print ''
        print '# **[Check out all the entries here!](http://schoolido.lu/#search={})**'.format(hashtag)
        print '*right click to open in new tab*'
        print ''
        print 'We encourage you to join in the celebrations with everyone by supporting all the entries.'
        print ''
        print '**Hit the like button** or leave a comment to share the {} love!'.format(idol.short_name)
        print '![](https://i.imgur.com/Scvsqw6.png)'
        print ''
        print '***'
        print ''
        print 'Thanks everyone who entered! We love your entries!'
        print ''
        print 'The winners will be announced in {} days, so look forward to it!'.format(days_to_vote)
        print ''
        print '***'
        print ''
        print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=True)
        print ''
        print '***'
        print ''
        print '[See awards details and prizes](https://schoolido.lu/activities/{}/)'.format(id)
        print ''
        print '[Read our giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ)'
        print ''
        print '###### {}'.format(hashtag)
        print ''
        print '--------- END OF POST TO COPY'
        print ''
        print 'List of entries to copy/paste to staff picks form:'
        print ''
        for activity in entries:
            print u'{}{} - http://schoolido.lu/activities/{}/'.format(
                activity.account.owner.username,
                u' ({})'.format(activity.account.nickname) if activity.account.nickname != activity.account.owner.username else '',
                activity.id)
        print ''
        print ''
