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
        print giveaway_details(idol_name, template_banner_url, template_small_banner_url, banner_url, banner_author, pixel_idols, prizes_banner_url)

def get_banners_from_previous_years(idol_short_name, year=''):
    try:
        giveaway_post = models.Activity.objects.filter(
            message_data__contains='{}FanAwards{}'.format(idol_short_name, year),
            account_id__in=[1, 111876],
        ).order_by('id')[0]
    except IndexError:
        print 'Cant find banners from previous years'
        return (None, None)
    try:
        return (
            giveaway_post.message_data.split(')')[0].split('(')[1],
            giveaway_post.message_data.split('[](')[-1].split('#small)')[0],
        )
    except IndexError:
        print 'Cant extract banners from giveaway post', giveaway_post.id
        return (None, None)

def giveaway_details(idol_name, template_banner_url=None, template_small_banner_url=None, banner_url=None, banner_author=None, pixel_idols=None, prizes_banner_url=None):

    post = ""
    if True:

        idol = models.Idol.objects.exclude(name__contains='Marika').filter(Q(name__contains=' {}'.format(idol_name)) | Q(name__exact=idol_name))[0]
        if idol.name == 'Emma Verde':
            idol.name = 'Verde Emma'
        if idol.name == 'Tsushima Yoshiko':
            idol.name = 'Tsushima Yohane'
        birthday = get_birthday(idol)
        # hashtag = u'{}BirthdayGiveaway{}'.format(idol.short_name, birthday.year)

        if not template_banner_url:
            template_banner_url, template_small_banner_url = get_banners_from_previous_years(idol.short_name, birthday.year - 1)
            if not template_banner_url:
                template_banner_url, template_small_banner_url = get_banners_from_previous_years(idol.short_name, birthday.year - 2)
                if not template_banner_url:
                    template_banner_url, template_small_banner_url = get_banners_from_previous_years(idol.short_name)


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

        post += '\n![{} {} Fan Awards]({})'.format(birthday.year, idol.name, template_banner_url)
        post += '\n'
        post += '\n## **Welcome to {}\'s {} Fan Awards!**'.format(idol.name, birthday.year)
        post += '\n'
        post += '\n'
        post += '\nA celebration of each and everyone of {name}\'s fans, where everyone, community and staff included, is here to love and recognize all fans of our favorite idol: {name}!'.format(
            name=idol.short_name,
        )
        post += '\n'
        post += '\n***Going all out or casually entering?* We\'re looking forward to see your posts!**'
        post += '\n'
        post += '\n***'
        post += '\n'
        post += '\n# **How to join the celebrations?**'
        post += '\n'
        post += '\n1. [Create an activity on School Idol Tomodachi](https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/How-to-post-an-activity%3F)'
        post += '\n1. Do something to **show your love for {}** and celebrate her birthday!'.format(idol.short_name)
        post += '\n    - *It can be a photo, cosplay, your figures, a song cover, a drawing, a poem, a story or anything else! It can be very short or very long. The only rule is that it has to be about {}!*'.format(idol.short_name)
        post += '\n1. Write "**{}**" somewhere in your activity, without spaces.'.format(hashtag)
        post += '\n    - *This is how everyone knows you\'re joining the celebrations!*'
        post += '\n'
        post += '\n***'
        post += '\n'
        post += '\n### Tag posting period: {} - {} - *[Countdown]({})*'.format(
            dateformat.format(birthday, 'F jS Y' if birthday.year != end_date.year else 'F jS'),
            dateformat.format(end_date, 'F jS Y' if birthday.month != end_date.month else 'jS Y'),
            countdown_url)
        post += '\n'
        post += '\n### -> [See all participants](http://schoolido.lu/#search={})'.format(hashtag)
        post += '\n*right click to open in new tab*'
        post += '\n'
        post += '\n***'
        post += '\n'
        post += '\n# **Bonus prize for a lucky winner!**'
        post += '\n'
        post += '\n![Lucky winner](https://i.imgur.com/tpQXUQo.png)'
        post += '\nAs a little bonus and thank you from the staff, we will give away a prize to a lucky winner, selected randomly!'
        post += '\n'
        post += '\n- **If you want to be eligible for a prize:**'
        post += '\n    - *You are only allowed to post **up to 3** full size pictures.*'
        post += '\n        - *If you want to post more, use our [gallery generator](http://imgur.gallery.db0.company/).*'
        post += '\n        - *If you append multiple images **vertically** in a single image, they\'ll still count as **multiple** images.*'
        post += '\n        - *If you append multiple images **horizontally** in a single image, they\'ll count as **one image**, as they won\'t make the post longer.*'
        post += '\n    - *If you post artworks, only post official artworks or artworks you own.*'
        post += '\n        - *Fan artworks by other artists are not allowed.*'
        post += '\n    - *You can post pictures of your **merch or SIF cards collection** if you\'d like, but they won\'t be taken into account in the judging phase to ensure fairness for those who can\'t afford them.*'
        post += '\n- **Otherwise**:'
        post += '\n    - *You\'re more than welcome to post using the tag to join in the celebration even when you don\'t want to get a prize. Just let us know by writing "**JustForFun**" anywhere in your entry.*'
        post += '\n'
        post += '\nWinner will be announced **[after the end of the awards entry period]({})**.'.format(
            countdown_url,
        )
        post += '\n'
        post += '\n# **Prize**'
        post += '\n'
        post += '\n- 1 custom commissioned {} graphic edit of your choice: wallpaper, avatar, Twitter header, ...'.format(idol.short_name)
        post += '\n'
        post += '\n![Comissioned graphic edit](https://i.imgur.com/8GMA2Dt.png)'
        post += '\n'
        post += '\n***'
        post += '\n***'
        post += '\n***'
        post += '\n'
        post += '\n# **![Stretch goals](https://i.imgur.com/btOF5QS.png)**'
        post += '\n'
        post += '\nIntroducing **stretch goals**: starting now, we will add more winners and more prizes based on how many people enter our Fan Awards!'
        post += '\n'
        post += '\nMore participants? More fun!'
        post += '\n'
        post += '\n### **If we get 15 participants or more:**'
        post += '\n'
        post += '\nWe will add another winner, elected by the community!'
        post += '\n'
        post += '\n# ![#1 Crowd\'s Favorite Winner - elected by the community](https://i.imgur.com/0jKB10n.png)'
        post += '\n'
        post += '\nMake everyone fall in love with {} thanks to your entry and they\'ll leave a like! The most liked entry at the end of the awards will get **a commissioned graphic edit of their choice**.'.format(idol.short_name)
        post += '\n'
        post += '\n*Crowd\'s Favorite winner is not eligible to be the Lucky winner.*'
        post += '\n'
        post += '\n### **If we get 30 participants or more:**'
        post += '\n'
        post += '\nWe will get a special judges panel to pick the Grand winner!'
        post += '\n'
        post += '\n![#1 Grand winner - elected by our judges panel](https://i.imgur.com/FP0cMmw.png)'
        post += '\n'
        post += '\nOur [judges panel](https://goo.gl/forms/42sCU6SXnKbqnag23) will pay attention to:'
        post += '\n'
        post += '\n- Creativity & Originality'
        post += '\n- Effort'
        post += '\n- Passion'
        post += '\n'
        post += '\nLearn more about [how judging works](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ#how-do-judges-pick-entries) or [how to become a judge](https://goo.gl/forms/42sCU6SXnKbqnag23).'
        post += '\n'
        post += '\n**All** winners will be announced **[{} days after the end of the awards entry period]({})**, to give the judges time to vote.'.format(
            days_to_vote,
            countdown_vote_url,
        )
        post += '\n'
        post += '\nThe Grand winner will get a prize of their choice between:'
        post += '\n'
        post += '\n- 1 {} physical prize (official merch)'.format('Love Live!' if not is_main else idol.short_name)
        post += '\n- 1 custom comissioned art of {} with outfit and text of your choice'.format(idol.short_name)
        post += '\n- 1 custom commissioned {} graphic edit of your choice: wallpaper, avatar, Twitter header, ...'.format(idol.short_name)
        post += '\n'
        post += '\n![Physical prize](https://i.imgur.com/CWEgyLu.png)'
        post += '\n![Custom drawing](https://i.imgur.com/hUHFYHc.png)'
        post += '\n'
        if pixel_idols:
            post += '\n- 1 custom {} **square keychain** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            post += '\n- 1 custom {} **round keychain** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            post += '\n- 1 custom {} **badge** by [shinylyni](http://schoolido.lu/user/shinylyni/)'.format(idol.short_name)
            post += '\n'
            post += '\n![Example of keychain / badges](http://i.imgur.com/CJkU0q8.jpg)'
            if pixel_idols:
                post += '\n'
                post += '\n![Chibi pixel idols]({})'.format(pixel_idols)
                post += '\n'
            post += '\n'
        post += '\n'
        post += '\n'
        post += '\n*Subject to availability*'
        post += '\n'
        if prizes_banner_url:
            post += '\n![Prizes]({})'.format(prizes_banner_url)
            post += '\n'

        post += '\n'
        post += '\n*Grand winner is not eligible to be the Crowd\'s Favorite winner or the Lucky winner.*'
        post += '\n'
        post += '\n### **If we get 50 participants or more:**'
        post += '\n'
        post += '\n![#2 Grand winner - Runner up](https://i.imgur.com/T0JEn99.png)'
        post += '\n'
        post += '\nWe will add a runner-up Grand winner picked by our judges panel.'
        post += '\n'
        post += '\nThe runner-up Grand winner will get a prize of their choice between a physical of digital prize.'
        post += '\n'
        post += '\n*Runner-up Grand winner is not eligible to be the Crowd\'s Favorite winner or the Lucky winner.*'
        post += '\n'
        post += '\n### **If we get even more:**'
        post += '\n'
        post += '\nWe will add more stretch goals!'
        post += '\n'
        post += '\n***'
        post += '\n'
        post += '\n# **![Got some merch you don\'t need?](https://i.imgur.com/VG1KvNd.png)**'
        post += '\n'
        post += '\nOur giveaways are organized by fans and for fans! We accept donations of hand-made gifts or official merch!'
        post += '\n'
        post += '\nIf you have something to donate and want to support our giveaways, [join our Discord](https://discord.gg/fmc6fef) and in the channel #ask_us_anything, mention @db0'
        post += '\n'
        post += '\nWe cover shipping costs for you!'
        post += '\n'
        post += '\n# **![Artist or graphic editor?](https://i.imgur.com/MLZvqbW.png)**'
        post += '\n'
        post += '\nJoin our team to help make prizes for winners!'
        post += '\n'
        post += '\n[Join our Discord](https://discord.gg/mehDTsv) and in the channel #ask_for_roles, say "Graphic designer" or "Artist"'
        post += '\n'
        post += '\n***'
        post += '\n'
        post += print_support_us()
        post += '\n'
        if banner_url:
            post += '\n***'
            post += '\n'
            post += '\n![{} Birthday Giveaway]({})'.format(idol.name, banner_url)
            if banner_author:
                post += '\n###### Banner by [{}](https://schoolido.lu/user/{}/)'.format(banner_author, banner_author)
            post += '\n'
            post += '\n***'
            post += '\n'
        post += '\n# **![F.A.Q.](https://i.imgur.com/vghSFuS.png)**'
        post += '\n'
        post += '\n- **I\'m not popular, can I win?**'
        post += '\n    - Yes! The Lucky winner is selected randomly, so you have the same chances as everyone. The Grand winner (if any) will be picked based on effort, creativity, originality and passion. So do your best, you can do it :)'
        post += '\n- **Does it matter if I win or not?**'
        post += '\n    - The awards are first of all a celebration of our love for {name}. The prizes are just here to recognize those who went all out, and do not invalidate you as a {name} fan <3'.format(name=idol.short_name)
        post += '\n- **Is it international?**'
        post += '\n    - Yes'
        post += '\n- **Do I have to pay for shipping?**'
        post += '\n    - No'
        post += '\n- **I can\'t give you my address, can I join?**'
        post += '\n    - Yes. If you win a physical prize, we will give you a digital prize instead.'
        post += '\n- **Can I re-use something I didn\'t make specifically for this contest?**'
        post += '\n    - Yes, but only if you didn\'t use it in a Circles contest before.'
        post += '\n- **How can I include images, audio and videos in my entry?**'
        post += '\n    - For images, [follow this guide](https://github.com/MagiCircles/Circles/wiki/Activity-images). For anything else, include an external link.'
        post += '\n- **Do I have to post in English?**'
        post += '\n    - No, any language is accepted.'
        post += '\n- **How can  I thank you for your amazing work organizing these contests?**'
        post += '\n    - We always appreciate sweet comments below, and if you want to push it a little further, we have a [Patreon](https://patreon.com/db0company/) open for donations <3'
        post += '\n- **More questions?**'
        post += '\n    - Read the [Giveaways FAQ](https://github.com/MagiCircles/Circles/wiki/Giveaways-FAQ) and ask your questions in the comments.'

        post += '\n'
        post += '\n***'
        post += '\n***'
        post += '\n***'
        post += '\n'
        if still_running_giveaways or voting_ongoing_giveaways or coming_soon_giveaways:
            post += print_still_running_and_coming_soon(still_running_giveaways, voting_ongoing_giveaways, coming_soon_giveaways, idol, with_icons=True)
            post += '\n'
            post += '\n***'
            post += '\n'
        post += '\n'
        post += '\n###### {}'.format(hashtag)
        post += '\n[]({}#small)'.format(template_small_banner_url)
        post += '\n'
        post += '\n'
        banners = [
            {
                'image': template_small_banner_url,
                'name': u'{} Fan Awards - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            },
        ]
        if prizes_banner_url:
            banners.append({
                'image': prizes_banner_url,
                'name': u'{} Fan Awards - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            })
        if banner_url:
            banners.append({
                'image': banner_url,
                'name': u'{} Birthday Giveaway - Why do you love {}? Tell us and win prizes! Keychains, badges, custom art and more!'.format(idol.name, idol.short_name),
            })
        pprint(banners)
        post += '\n'
        post += '\n'
    return post, banners

def get_small_image(current_giveaway):
    return current_giveaway.message_data.split('#small')[0].split('(')[-1]
