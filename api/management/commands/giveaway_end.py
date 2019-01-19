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
        hashtag = giveaway.message_data.split('[See all entries](http://schoolido.lu/#search=')[1].split(')')[0]

        idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        if not idol:
            try:
                idol = models.Idol.objects.filter(name__contains=u' {}'.format(hashtag.split('Birthday')[0]))[0]
            except:
                print 'Can\'t find idol'
                return

        days_to_enter, days_to_vote = get_days(idol)
        birthday = get_birthday(idol)
        end_date, countdown_url = get_countdown_url(
            birthday, days_to_enter + days_to_vote,
            '{} Birthday Giveaway winners announcement'.format(idol.short_name),
        )
        entries = models.Activity.objects.filter(id__gt=id, message_data__icontains=hashtag).order_by('?')

        print ''
        print '--------- START OF POST TO COPY'
        print ''
        print get_image(giveaway)
        print ''
        print '{} #1 Fan Election just reached its last phase.'.format(idol.short_name)
        print ''
        print 'You are not allowed to enter anymore, however, you still have {} days to vote for your favorite entries and support whom you think is {}\'s #1 fan!'.format(days_to_vote, idol.short_name)
        print ''
        print '***'
        print ''
        print '# Vote for {}\'s #1 fan'.format(idol.short_name)
        print ''
        print '![](https://i.imgur.com/Scvsqw6.png)'
        print ''
        print '1. Make sure you have an account on [School Idol Tomodachi](http://schoolido.lu/) and you\'re logged in'
        print '2. **[See all the entries here!](http://schoolido.lu/#search={})** *right click to open in new tab*'.format(hashtag)
        print '3. Hit the "Like" button to support your favorite entries. You can like as many entries as you want!'
        print '4. To see the total number of likes an entry has, click "Write comment", which will take you to the entry only and you\'ll see the likes and comments there.'
        print ''
        print '***'
        print ''
        print 'Thanks everyone who entered! We love your entries!'
        print ''
        print 'The winners will be announced in {} days, so look forward to it!'.format(days_to_vote)
        print ''
        print '### [Countdown before we announce the winners]({})'.format(countdown_url)
        print ''
        print '***'
        print ''
        print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=True)
        print ''
        print '***'
        print ''
        print '[See election details and prizes](https://schoolido.lu/activities/{}/)'.format(id)
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
            print u'{} - http://schoolido.lu/activities/{}/'.format(activity.account.owner.username, activity.id)
        print ''
        print ''
