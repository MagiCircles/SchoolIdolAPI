import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from django.db.models import Q
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
    PDP_IDOLS,
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

        idol = models.Idol.objects.exclude(name__contains='Marika').filter(Q(name__contains=' {}'.format(idol_name)) | Q(name__exact=idol_name))[0]
        if idol.name == 'Emma Verde':
            idol.name = 'Verde Emma'
        if idol.name == 'Tsushima Yoshiko':
            idol.name = 'Tsushima Yohane'
        birthday = get_birthday(idol)
        # hashtag = u'{}BirthdayGiveaway{}'.format(idol.short_name, birthday.year)
        hashtag = u'{}FanAwards{}'.format(idol.short_name, birthday.year)
        _idol, still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways = get_other_giveaways(hashtag)
        days_to_enter, days_to_vote = get_days(idol)
        with_staff_picks = get_with_staff_picks(idol)
        is_main = idol.name not in PDP_IDOLS and idol.main

        end_date, countdown_url = get_countdown_url(
            birthday, days_to_enter,
            title='End of {} {} Fan Awards'.format(birthday.year, idol.short_name),
        )

        vote_end_date, countdown_vote_url = get_countdown_url(
            birthday, days_to_enter + days_to_vote,
            title='{} {} Fan Awards - Votes closing in'.format(birthday.year, idol.short_name),
        )

        print '![{} {} Fan Awards]({})'.format(birthday.year, idol.name, template_banner_url)
        print ''
        print '## **Welcome to {}\'s {} Fan Awards!**'.format(idol.name, birthday.year)
        print ''
        print ''
        print 'A celebration of each and everyone of {name}\'s fans, where everyone, community and staff included, is here to love and recognize all fans of our favorite idol: {name}!'.format(
            name=idol.short_name,
        )
        print ''
        print '***Going all out or casually entering?* We\'re looking forward to see your posts!**'
        print ''
        print '***'
        print ''
        print '# **How to join the celebrations?**'
        print ''
        print '1. [Create an activity on School Idol Tomodachi](https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/How-to-post-an-activity%3F)'
        print '1. Do something to **show your love for {}** and celebrate her birthday!'.format(idol.short_name)
        print '    - *It can be a photo, cosplay, your figures, a song cover, a drawing, a poem, a story or anything else! It can be very short or very long. The only rule is that it has to be about {}!*'.format(idol.short_name)
        print '1. Write "**{}**" somewhere in your activity, without spaces.'.format(hashtag)
        print '    - *This is how everyone knows you\'re joining the celebrations!*'
        print ''
        print '***'
        print ''
        print '### Tag posting period: {} - {} - *[Countdown]({})*'.format(
            dateformat.format(birthday, 'F jS Y' if birthday.year != end_date.year else 'F jS'),
            dateformat.format(end_date, 'F jS Y' if birthday.month != end_date.month else 'jS Y'),
            countdown_url)
        print ''
        print '### -> [See all participants](http://schoolido.lu/#search={})'.format(hashtag)
        print '*right click to open in new tab*'
        print ''
        print '***'
        print ''
        print '# **Bonus prize for a lucky winner!**'
        print ''
        print '![Lucky winner](https://i.imgur.com/tpQXUQo.png)'
        print 'As a little bonus and thank you from the staff, we will give away a prize to a lucky winner, selected randomly!'
        print ''
        print '- **If you want to be eligible for a prize:**'
        print '    - *You are only allowed to post **up to 3** full size pictures.*'
        print '        - *If you want to post more, use our [gallery generator](http://imgur.gallery.db0.company/).*'
        print '        - *If you append multiple images **vertically** in a single image, they\'ll still count as **multiple** images.*'
        print '        - *If you append multiple images **horizontally** in a single image, they\'ll count as **one image**, as they won\'t make the post longer.*'
        print '    - *If you post artworks, only post official artworks or artworks you own.*'
        print '        - *Fan artworks by other artists are not allowed.*'
        print '    - *You can post pictures of your **merch or SIF cards collection** if you\'d like, but they won\'t be taken into account in the judging phase to ensure fairness for those who can\'t afford them.*'
        print '- **Otherwise**:'
        print '    - *You\'re more than welcome to post using the tag to join in the celebration even when you don\'t want to get a prize. Just let us know by writing "**JustForFun**" anywhere in your entry.*'
        print ''
        print 'Winner will be announced **[after the end of the awards entry period]({})**.'.format(
            countdown_url,
        )
        print ''
        print '# **Prize**'
        print ''
        print '- 1 custom commissioned {} graphic edit of your choice: wallpaper, avatar, Twitter header, ...'.format(idol.short_name)
        print ''
        print '![Comissioned graphic edit](https://i.imgur.com/8GMA2Dt.png)'
        print ''
        print '***'
        print '***'
        print '***'
        print ''
        print '# **![Stretch goals](https://i.imgur.com/btOF5QS.png)**'
        print ''
        print 'Introducing **stretch goals**: starting now, we will add more winners and more prizes based on how many people enter our Fan Awards!'
        print ''
        print 'More participants? More fun!'
        print ''
        print '### **If we get 15 participants or more:**'
        print ''
        print 'We will add another winner, elected by the community!'
        print ''
        print '# ![#1 Crowd\'s Favorite Winner - elected by the community](https://i.imgur.com/0jKB10n.png)'
        print ''
        print 'Make everyone fall in love with {} thanks to your entry and they\'ll leave a like! The most liked entry at the end of the awards will get **a commissioned graphic edit of their choice**.'.format(idol.short_name)
        print ''
        print '*Crowd\'s Favorite winner is not eligible to be the Lucky winner.*'
        print ''
        print '### **If we get 30 participants or more:**'
        print ''
        print 'We will get a special judges panel to pick the Grand winner!'
        print ''
        print '![#1 Grand winner - elected by our judges panel](https://i.imgur.com/FP0cMmw.png)'
        print ''
        print 'Our [judges panel](https://goo.gl/forms/42sCU6SXnKbqnag23) will pay attention to:'
        print ''
        print '- Creativity & Originality'
        print '- Effort'
        print '- Passion'
        print ''
        print 'Learn more about [how judging works](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ#how-do-judges-pick-entries) or [how to become a judge](https://goo.gl/forms/42sCU6SXnKbqnag23).'
        print ''
        print '**All** winners will be announced **[{} days after the end of the awards entry period]({})**, to give the judges time to vote.'.format(
            days_to_vote,
            countdown_vote_url,
        )
        print ''
        print 'The Grand winner will get a prize of their choice between:'
        print ''
        print '- 1 {} physical prize (official merch)'.format('Love Live!' if not is_main else idol.short_name)
        print '- 1 custom comissioned art of {} with outfit and text of your choice'.format(idol.short_name)
        print '- 1 custom commissioned {} graphic edit of your choice: wallpaper, avatar, Twitter header, ...'.format(idol.short_name)
        print ''
        print '![Physical prize](https://i.imgur.com/CWEgyLu.png)'
        print '![Custom drawing](https://i.imgur.com/hUHFYHc.png)'
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
            print ''
        print ''
        print ''
        print '*Subject to availability*'
        print ''
        if prizes_banner_url:
            print '![Prizes]({})'.format(prizes_banner_url)
            print ''

        print ''
        print '*Grand winner is not eligible to be the Crowd\'s Favorite winner or the Lucky winner.*'
        print ''
        print '### **If we get 50 participants or more:**'
        print ''
        print '![#2 Grand winner - Runner up](https://i.imgur.com/T0JEn99.png)'
        print ''
        print 'We will add a runner-up Grand winner picked by our judges panel.'
        print ''
        print 'The runner-up Grand winner will get a prize of their choice between a physical of digital prize.'
        print ''
        print '*Runner-up Grand winner is not eligible to be the Crowd\'s Favorite winner or the Lucky winner.*'
        print ''
        print '### **If we get even more:**'
        print ''
        print 'We will add more stretch goals!'
        print ''
        print '***'
        print ''
        print '# **![Got some merch you don\'t need?](https://i.imgur.com/VG1KvNd.png)**'
        print ''
        print 'Our giveaways are organized by fans and for fans! We accept donations of hand-made gifts or official merch!'
        print ''
        print 'If you have something to donate and want to support our giveaways, [join our Discord](https://discord.gg/fmc6fef) and in the channel #ask_us_anything, mention @db0'
        print ''
        print 'We cover shipping costs for you!'
        print ''
        print '# **![Artist or graphic editor?](https://i.imgur.com/MLZvqbW.png)**'
        print ''
        print 'Join our team to help make prizes for winners!'
        print ''
        print '[Join our Discord](https://discord.gg/mehDTsv) and in the channel #ask_for_roles, say "Graphic designer" or "Artist"'
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
        print '# **![F.A.Q.](https://i.imgur.com/vghSFuS.png)**'
        print ''
        print '- **I\'m not popular, can I win?**'
        print '    - Yes! The Lucky winner is selected randomly, so you have the same chances as everyone. The Grand winner (if any) will be picked based on effort, creativity, originality and passion. So do your best, you can do it :)'
        print '- **Does it matter if I win or not?**'
        print '    - The awards are first of all a celebration of our love for {name}. The prizes are just here to recognize those who went all out, and do not invalidate you as a {name} fan <3'.format(name=idol.short_name)
        print '- **Is it international?**'
        print '    - Yes'
        print '- **Do I have to pay for shipping?**'
        print '    - No'
        print '- **I can\'t give you my address, can I join?**'
        print '    - Yes. If you win a physical prize, we will give you a digital prize instead.'
        print '- **Can I re-use something I didn\'t make specifically for this contest?**'
        print '    - Yes, but only if you didn\'t use it in a Circles contest before.'
        print '- **How can I include images, audio and videos in my entry?**'
        print '    - For images, [follow this guide](https://github.com/MagiCircles/Circles/wiki/Activity-images). For anything else, include an external link.'
        print '- **Do I have to post in English?**'
        print '    - No, any language is accepted.'
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
                'name': u'{} Fan Awards - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            },
        ]
        if prizes_banner_url:
            banners.append({
                'url': 'https://schoolido.lu/activities/ID/',
                'image': prizes_banner_url,
                'name': u'{} Fan Awards - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
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
