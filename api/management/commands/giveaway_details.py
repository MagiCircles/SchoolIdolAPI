import datetime
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils.formats import dateformat, date_format
from giveaway_winners import (
    get_birthday,
    get_other_giveaways,
    get_days,
    get_countdown_url,
    print_still_running_and_coming_soon,
    print_support_us,
)
from api import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        if len(args) < 4:
            print 'Specify idol name, banner url, banner author (cay say "NONE"), pixel idols image (can say "NONE")'
            return
        idol_name = args[0]
        banner_url = args[1]
        banner_author = args[2] if args[2] != 'NONE' else None
        pixel_idols = args[3] if args[3] != 'NONE' else None

        idol = models.Idol.objects.filter(name__contains=' {}'.format(idol_name))[0]
        birthday = get_birthday(idol)
        hashtag = u'{}BirthdayGiveaway{}'.format(idol.short_name, birthday.year)
        _idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        days_to_enter, days_to_vote = get_days(idol)

        end_date, countdown_url = get_countdown_url(
            birthday, days_to_enter,
            title='End of {} Birthday Giveaway'.format(idol.short_name),
        )

        vote_end_date, countdown_vote_url = get_countdown_url(
            birthday, days_to_enter + days_to_vote,
            title='{} Birthday Giveaway - Votes closing in'.format(idol.short_name),
        )

        print '![{} Birthday Giveaway]({})'.format(idol.name, banner_url)
        if banner_author:
            print '###### Banner by [{}](https://schoolido.lu/user/{}/)'.format(banner_author, banner_author)
        print ''
        print_support_us()
        print ''
        print '***'
        print ''
        print '## Let\'s celebrate {}\'s birthday together!'.format(idol.short_name)
        print ''
        print '{} - {}'.format(
            dateformat.format(birthday, 'F jS Y' if birthday.year != end_date.year else 'F jS'),
            dateformat.format(end_date, 'F jS Y' if birthday.month != end_date.month else 'jS Y'),
        )
        print ''
        print '### -> [Countdown before the end of the giveaway]({})'.format(countdown_url)
        print '### -> [See all entries](http://schoolido.lu/#search={})'.format(hashtag)
        print ''
        print '# Enter our giveaway to win:'
        print ''
        if pixel_idols:
            print '- 1 custom {} keychain'.format(idol.name)
            print '    - The keychain is going to be hand made and will have a pixel illustration of {} made by [shinylyni](http://schoolido.lu/user/shinylyni/)~'.format(idol.short_name)
            print '    - [Example of keychain (from previous giveaway)](https://i.imgur.com/1EfFpeB.jpg)'
            print ''
            print '- 1 custom {} badge'.format(idol.name)
            print '    - The badge is going to be hand made and will have a pixel illustration of {} made by [shinylyni](http://schoolido.lu/user/shinylyni/)~'.format(idol.short_name)
            print '    - [Example of badges (from previous giveaway)](https://i.imgur.com/jHzqJQR.jpg)'
            print ''
            print '![]({})'.format(pixel_idols)
            print ''
            print '![](http://i.imgur.com/CJkU0q8.jpg)'
            print ''
        print '- 1 Custom {} drawing with outfit and text of your choice'.format(idol.name)
        print ''
        print '- 1 Custom {} wallpaper, avatar, Twitter header, or any other graphic edit of your choice'.format(idol.name)
        print ''
        print '- More prizes may be announced later!'
        print ''
        print 'If you wish to help support this giveaway or other giveaways in the future and you have something to give away, we\'d be more than happy to add you to the list of prizes!:'
        print ''
        print '- Digital art or edit: [Join our Discord](https://discord.gg/mehDTsv) and in the channel #ask_permissions_to_join, say "Graphic designer" or "Artist"'
        print '- Physical hand-made gift or official merch: [Join our Discord](https://discord.gg/fmc6fef) and in the channel #chat_lovelive, mention @db0 (note: we cover shipping costs for you!)'
        print ''
        print '***'
        print ''
        print '# **How to enter?**'
        print ''
        print '1. [Create an activity on School Idol Tomodachi](https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/How-to-post-an-activity%3F)'
        print '1. Do something to celebrate {}\'s birthday: it can be a photo, cosplay, your figures, a song cover, a drawing, a poem, a story or anything else! It can be very short or very long. The only rule is that it has to be about {}!'.format(idol.short_name, idol.short_name)
        print '1. If you post artworks, only post official artworks, artworks you own, or fan artworks that are approved by the artist and credited.'
        print '1. Write "{}" somewhere in your activity, without spaces (this is how we\'ll know you\'re entering the giveaway!)'.format(hashtag)
        print '1. After submitting your entry, scroll back to where you posted it to open it.'
        print ''
        print '***'
        print ''
        print '# **How to win?**'
        print ''
        print '- **Most popular**'
        print '    - The power is in the end of the community! Make everyone fall in love with {} thanks to your entry and they\'ll leave a like! The most liked entries at the end of the giveaway will be the winners!'.format(idol.short_name)
        print '- **Staff picks**'
        print '    - The members of our [judges panel](https://goo.gl/forms/42sCU6SXnKbqnag23) will pick a winner, regardless of likes. They will pay attention to:'
        print '        - Creativity & Originality'
        print '        - Effort'
        print '        - Passion'
        print ''
        print 'Likes will close and winners will be announced **[{} days after the end of the giveaway]({})**.'.format(
            days_to_vote,
            countdown_vote_url,
        )
        print ''
        print 'Winners are eligible for digital or physical prizes based on their rank.'
        print ''
        print '***'
        print ''
        print '# **FAQ**'
        print ''
        print '- **Is it international?**'
        print '    - Yes'
        print '- **Do I have to pay for shipping?**'
        print '    - No'
        print '- **I can\'t give you my address, can I join?**'
        print '    - Yes. If you win a physical prize, we will give you a digital prize instead.'
        print '- **I\'m not popular, can I win?**'
        print '    - Yes! The staff team picks a winner based on effort, creativity, originality and passion so do your best, you can do it :)'
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
        print '- **How can  I thank you for your amazing work organizing these giveaways?**'
        print '    - We always appreciate sweet comments below, and if you want to push it a little further, we have a [Patreon](https://patreon.com/db0company/) open for donations <3'
        print '- **More questions?**'
        print '    - Read the [Giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ) and ask your questions in the comments.'

        print ''
        print '***'
        print '***'
        print '***'
        print ''
        if still_running_giveaways or voting_ongoing_giveaways or coming_soon_giveaways:
            print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol)
            print ''
            print '***'
            print ''
        print '###### {}'.format(hashtag)
        print ''
        print ''
