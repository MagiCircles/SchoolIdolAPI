import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils.formats import dateformat, date_format
from giveaway_winners import (
    get_birthday,
    get_other_giveaways,
    get_days,
    get_with_staff_picks,
    get_countdown_url,
    print_still_running_and_coming_soon,
    print_support_us,
)
from api import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if len(args) < 7:
            print 'Specify idol name, template banner url, template small banner url, banner url, banner author (cay say "NONE"), pixel idols image (can say "NONE"), prizes banner url (can say "NONE")'
            return
        idol_name = args[0]
        template_banner_url = args[1]
        template_small_banner_url = args[2]
        banner_url = args[3] if args[3] != 'NONE' else None
        banner_author = args[4] if args[4] != 'NONE' else None
        pixel_idols = args[5] if args[5] != 'NONE' else None
        prizes_banner_url = args[6] if args[6] != 'NONE' else None

        idol = models.Idol.objects.filter(name__contains=' {}'.format(idol_name))[0]
        birthday = get_birthday(idol)
        # hashtag = u'{}BirthdayGiveaway{}'.format(idol.short_name, birthday.year)
        hashtag = u'{}FanElection{}'.format(idol.short_name, birthday.year)
        _idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        days_to_enter, days_to_vote = get_days(idol)
        with_staff_picks = get_with_staff_picks(idol)

        end_date, countdown_url = get_countdown_url(
            birthday, days_to_enter,
            title='End of {} {} Fan Election'.format(birthday.year, idol.short_name),
        )

        vote_end_date, countdown_vote_url = get_countdown_url(
            birthday, days_to_enter + days_to_vote,
            title='{} {} Fan Election - Votes closing in'.format(birthday.year, idol.short_name),
        )

        print '![{} {} Fan Election]({})'.format(birthday.year, idol.name, template_banner_url)
        print ''
        print '## **Do you think you are {}\'s number one fan?**'.format(idol.name)
        print ''
        print 'Show the community your true love and dedication to {} and you may get elected {}\'s #1 {} fan!'.format(
            idol.short_name,
            birthday.year,
            idol.short_name,
        )
        print ''
        print '***'
        print ''
        print '# **How to enter?**'
        print ''
        print '1. [Create an activity on School Idol Tomodachi](https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/How-to-post-an-activity%3F)'
        print '1. Do something to **show your love for {}** and celebrate her birthday! It can be a photo, cosplay, your figures, a song cover, a drawing, a poem, a story or anything else! It can be very short or very long. The only rule is that it has to be about {}!'.format(idol.short_name, idol.short_name)
        print '1. If you post artworks, only post official artworks, artworks you own, or fan artworks that are approved by the artist and credited.'
        print '1. Write "**{}**" somewhere in your activity, without spaces (this is how we\'ll know you\'re entering the election)'.format(hashtag)
        print '1. After submitting your entry, scroll back to where you posted it to open it.'
        print ''
        print '### Entering period: {} - {} - *[Countdown]({})*'.format(
            dateformat.format(birthday, 'F jS Y' if birthday.year != end_date.year else 'F jS'),
            dateformat.format(end_date, 'F jS Y' if birthday.month != end_date.month else 'jS Y'),
            countdown_url)
        print '### End of election: {} - *[Countdown]({})*'.format(dateformat.format(vote_end_date, 'F jS'), countdown_vote_url)
        print '### -> [See all entries](http://schoolido.lu/#search={})'.format(hashtag)
        print ''
        print '***'
        print ''
        if with_staff_picks:
            print '# **Categories**'
            print ''
            print '![Election categories](https://i.imgur.com/1NMG7sV.png)'
            print ''
            print '- **Number One Fan**'
            print '    - Elected by the members of our [judges panel](https://goo.gl/forms/42sCU6SXnKbqnag23). They will pay attention to:'
            print '        - Creativity & Originality'
            print '        - Effort'
            print '        - Passion'
            print '- **Crowd\'s Favorite**'
            print '    - Elected by the community. Make everyone fall in love with {} thanks to your entry and they\'ll leave a like! The most liked entry at the end of the election will be the winner of this category.'.format(idol.short_name)
            print ''
            print 'Both winners will be announced **[{} days after the end of the election entry period]({})**.'.format(
                days_to_vote,
                countdown_vote_url,
            )
            print ''
        else:
            print '# **How to win?**'
            print '![Election categories](https://i.imgur.com/7E4PZ8y.png)'
            print ''
            print 'The winner will be elected by the community. Make everyone fall in love with {} thanks to your entry and they\'ll leave a like! The most liked entry at the end of the election will be the winner.'.format(idol.short_name)
            print ''
            print 'Winner(s) will be announced **[{} days after the end of the election entry period]({})**.'.format(
                days_to_vote,
                countdown_vote_url,
            )
            print ''
        print 'Winners are eligible for digital or physical prizes based on their rank.'
        print ''
        print '***'
        print ''
        print '# **Prizes**'
        print ''
        if prizes_banner_url:
            print '![Prizes]({})'.format(prizes_banner_url)
            print ''
        print ''
        print '---------------------- COPY PRIZES -------------------------'
        print ''
        if pixel_idols:
            print '- 1 custom {} **square keychain** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            print '- 1 custom {} **round keychain** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            print '- 1 custom {} **badge** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            print ''
            print '![Example of keychain / badges](http://i.imgur.com/CJkU0q8.jpg)'
            if pixel_idols:
                print ''
                print '![Chibi pixel idols]({})'.format(pixel_idols)
            print ''
        print '- 1 custom {} drawing with outfit and text of your choice'.format(idol.short_name)
        print ''
        print '- Up to 3 custom {} graphic edits of your choice: wallpaper, avatar, Twitter header, ...'.format(idol.short_name)
        print ''
        print '![Digital prizes](https://i.imgur.com/FScvkTy.png)'
        print ''
        print '***'
        print ''
        print '# **More prizes?**'
        print ''
        print 'If you wish to help support this giveaway or other giveaways in the future and you have something to give away, we\'d be more than happy to add you to the list of prizes!:'
        print ''
        print '- Digital art or edit: [Join our Discord](https://discord.gg/mehDTsv) and in the channel #ask_permissions_to_join, say "Graphic designer" or "Artist"'
        print '- Physical hand-made gift or official merch: [Join our Discord](https://discord.gg/fmc6fef) and in the channel #chat_lovelive, mention @db0 (note: we cover shipping costs for you!)'
        print ''
        print '***'
        print ''
        print_support_us()
        print ''
        if banner_url:
            print '***'
            print ''
            print '![{} Birthday Giveaway]({})'.format(idol.name, banner_url)
            if banner_author:
                print '###### Banner by [{}](https://schoolido.lu/user/{}/)'.format(banner_author, banner_author)
            print ''
            print '***'
            print ''
        print '# **F.A.Q.**'
        print ''
        print '- **Is it international?**'
        print '    - Yes'
        print '- **Do I have to pay for shipping?**'
        print '    - No'
        print '- **I can\'t give you my address, can I join?**'
        print '    - Yes. If you win a physical prize, we will give you a digital prize instead.'
        if with_staff_picks:
            print '- **I\'m not popular, can I win?**'
            print '    - Yes! The staff team picks the winner based on effort, creativity, originality and passion so do your best, you can do it :)'
        print '- **Can I enter multiple times or combine multiple giveaway entries into one?**'
        print '    - Yes, but you\'ll only get one prize if you win.'
        print '- **Can I re-use something I didn\'t make specifically for this contest?**'
        print '    - Yes, but only if you didn\'t use it in a Circles contest before.'
        print '- **How can I include images, audio and videos in my entry?**'
        print '    - For images, [follow this guide](https://github.com/MagiCircles/Circles/wiki/Activity-images). For anything else, include an external link.'
        print '- **Do I have to post in English?**'
        print '    - No, any language is fine.'
        print '- **I posted and I can\'t see my activity on the homepage?**'
        print '    - After posting, scroll back to the form to post to get the direct link (or see errors if any). For your safety, only 18+ y/o users can see non-moderated activities on the homepage (in "new" tab). Wait for it to be approved by either our staff teams or by the community by getting enough likes.'
        print '- **How can  I thank you for your amazing work organizing these contests?**'
        print '    - We always appreciate sweet comments below, and if you want to push it a little further, we have a [Patreon](https://patreon.com/db0company/) open for donations <3'
        print '- **More questions?**'
        print '    - Read the [Giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ) and ask your questions in the comments.'

        print ''
        print '***'
        print '***'
        print '***'
        print ''
        if still_running_giveaways or voting_ongoing_giveaways or coming_soon_giveaways:
            print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=True)
            print ''
            print '***'
            print ''
        print ''
        print '###### {}'.format(hashtag)
        print '[]({}#small)'.format(template_small_banner_url)
        print ''
        print ''
        print '--------- END OF POST TO COPY'
        print ''
        banners = [
            {
                'url': 'https://schoolido.lu/activities/ID/',
                'image': template_small_banner_url,
                'name': u'{} Fan Election - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            },
        ]
        if prizes_banner_url:
            banners.append({
                'url': 'https://schoolido.lu/activities/ID/',
                'image': prizes_banner_url,
                'name': u'{} Fan Election - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            })
        if banner_url:
            banners.append({
                'url': 'https://schoolido.lu/activities/ID/',
                'image': banner_url,
                'name': u'{} Birthday Giveaway - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            })
        pprint(banners)
        print ''
        print ''

def get_small_image(current_giveaway):
    return current_giveaway.message_data.split('#small')[0].split('(')[-1]
