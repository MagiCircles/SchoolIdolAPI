import datetime
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils.formats import dateformat, date_format
from giveaway_cheater import get_next_birthday, get_other_giveaways
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

        today = datetime.date.today()
        in_300_days = today + relativedelta(days=300)

        idol = models.Idol.objects.filter(name__icontains=idol_name)[0]
        next_birthday = get_next_birthday(idol.birthday)
        if next_birthday >= in_300_days:
            next_birthday = next_birthday.replace(next_birthday.year - 1)

        hashtag = u'{}BirthdayGiveaway{}'.format(idol.short_name, next_birthday.year)
        still_running_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)

        end_of_giveaway = next_birthday + relativedelta(days=16)

        countdown_url = 'https://www.timeanddate.com/countdown/birthday?iso={}T00&p0=%3A&msg=End+of+School+Idol+Tomodachi+{}+Birthday+Giveaway&font=sanserif&csz=1'.format(
            dateformat.format(end_of_giveaway, "Ymd"),
            idol.short_name,
        )

        print '![{} Birthday Giveaway]({})'.format(idol.name, banner_url)
        if banner_author:
            print '###### Banner by [{}](https://schoolido.lu/user/{}/)'.format(banner_author, banner_author)
        print ''
        print '# **Support our giveaways!**'
        print ''
        print 'These giveaways are made possible thanks to the support of our warm-hearted donators. If you wish to support School Idol Tomodachi for both our future giveaways and to cover the cost of our expensive servers in which our site run, please consider [donating on Patreon](http://patreon.com/db0company).'
        print ''
        print '[![Support us on Patreon](https://i.imgur.com/YYwkEhP.png)](http://patreon.com/db0company)'
        print ''
        print '***'
        print ''
        print '## Let\'s celebrate {}\'s birthday together!'.format(idol.short_name)
        print ''
        print '# -> [Countdown before the end of the giveaway]({})'.format(countdown_url)
        print '# -> [See all entries](http://schoolido.lu/#search={})'.format(hashtag)
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
        print '# **How to enter?**'
        print ''
        print '1. [Create an activity on School Idol Tomodachi](https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/How-to-post-an-activity%3F)'
        print '1. Do something to celebrate {}\'s birthday: it can be a photo, cosplay, your figures, a song cover, a drawing, a poem, a story or anything else! It can be very short or very long. The only rule is that it has to be about {}!'.format(idol.short_name, idol.short_name)
        print '1. If you post artworks, only post official artworks, artworks you own, or fan artworks that are approved by the artist and credited.'
        print '1. Write "{}" somewhere in your activity, without spaces (this is how we\'ll know you\'re entering the giveaway!)'.format(hashtag)
        print '1. To confirm that your entry is in, [check this link](http://schoolido.lu/#search={}) (you may need to wait a few days to get it approved by either our staff teams or by the community by getting enough likes)'.format(hashtag)
        print ''
        print '# **How to win?**'
        print ''
        print '1. The judges are going to be all of you, the members of the site!'
        print '    - You have until the end of the [countdown]({}) to get as many "likes" as you can on your activity.'.format(countdown_url)
        print '1. At the end of the [countdown]({}), the top 3 activities with the most likes will be the winners!'.format(countdown_url)
        print '    - #1 and #2 winners get a physical prize. #3 winner gets a digital prize.'
        print '1. Our staff and contributors will also hand pick 1 extra winner who gets a physical prize, regardless of likes. They will pay attention to:'
        print '    - Creativity & Originality'
        print '    - Effort'
        print '    - Passion'
        print '1. We will send you a private message on School Idol Tomodachi to ask for your address to send you the prize.'
        print ''
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
        print '    - Yes! The staff team picks a winner based on effort, creativity, originality and passion so do your best, you can do it~'
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
        print '    - Read the [Giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ)'

        print ''
        print '***'
        print ''
        if still_running_giveaways:
            print ''
            print u'{} {} currently running! Take your chance and enter!'.format(
                'is' if len(still_running_giveaways) == 1 else 'are',
                u' and '.join([
                    u'[{idol_name}\'s Birthday giveaway](https://schoolido.lu/activities/{id}/)'.format(
                        idol_name=idol.name, id=giveaway.id,
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
