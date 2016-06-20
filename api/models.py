# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib import admin
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _, string_concat
from api.models_languages import *
from django.core import validators
from django.utils import timezone
from django.conf import settings
from django_prometheus.models import ExportModelOperationsMixin
from api.raw import raw_information
from web.utils import randomString
import hashlib, urllib
import csv
import datetime
import os

ATTRIBUTE_CHOICES = (
    ('Smile', _('Smile')),
    ('Pure', _('Pure')),
    ('Cool', _('Cool')),
    ('All', _('All')),
)
ATTRIBUTE_ARRAY = dict(ATTRIBUTE_CHOICES).keys()

RARITY_CHOICES = (
    ('N', _('Normal')),
    ('R', _('Rare')),
    ('SR', _('Super Rare')),
    ('UR', _('Ultra Rare')),
)
RARITY_DICT = dict(RARITY_CHOICES)

OS_CHOICES = (
    ('Android', 'Android'),
    ('iOs', 'iOs'),
)

STORED_CHOICES = (
    ('Deck', string_concat(_('Deck'), ' (', _('You have it'), ')')),
    ('Album', string_concat(_('Album'), ' (', _('You don\'t have it anymore'), ')')),
    ('Box', _('Present Box')),
    ('Favorite', _('Wish List')),
)
STORED_DICT = dict(STORED_CHOICES)

STORED_DICT_FOR_ACTIVITIES = {
    'Deck': _('Deck'),
    'Album': _('Album'),
    'Box': _('Present Box'),
    'Favorite': _('Wish List'),
}

VERIFIED_CHOICES = (
    (0, ''),
    (1, _('Silver Verified')),
    (2, _('Gold Verified')),
    (3, _('Bronze Verified')),
)
VERIFIED_DICT = dict(VERIFIED_CHOICES)

VERIFIED_UNTRANSLATED_CHOICES = (
    (0, ''),
    (1, 'Silver Verified'),
    (2, 'Gold Verified'),
    (3, 'Bronze Verified'),
)
VERIFIED_UNTRANSLATED_DICT = dict(VERIFIED_UNTRANSLATED_CHOICES)

PLAYWITH_CHOICES = (
    ('Thumbs', _('Thumbs')),
    ('Fingers', _('All fingers')),
    ('Index', _('Index fingers')),
    ('Hand', _('One hand')),
    ('Other', _('Other')),
)
PLAYWITH_DICT = dict(PLAYWITH_CHOICES)

PLAYWITH_ICONS = (
    ('Thumbs', 'thumbs'),
    ('Fingers', 'fingers'),
    ('Index', 'index'),
    ('Hand', 'fingers'),
    ('Other', 'sausage'),
)
PLAYWITH_ICONS_DICT = dict(PLAYWITH_ICONS)

ACTIVITY_TYPE_CUSTOM = 6

ACTIVITY_MESSAGE_CHOICES_INT = (
    (0, 'Added a card'),
    (1, 'Idolized a card'),
    (2, 'Rank Up'),
    (3, 'Ranked in event'),
    (4, 'Verified'),
    (5, 'Trivia'),
    (ACTIVITY_TYPE_CUSTOM, 'Custom'),
)
ACTIVITY_MESSAGE_DICT_INT = dict(ACTIVITY_MESSAGE_CHOICES_INT)

def messageStringToInt(message):
    for k, v in ACTIVITY_MESSAGE_DICT_INT.items():
        if v == message:
            return k
    return 0

ACTIVITY_MESSAGE_CHOICES = (
    ('Added a card', _('Added {} in {}')),
    ('Idolized a card', _('Idolized {} in {}')),
    ('Rank Up', _('Rank Up {}')),
    ('Ranked in event', _('Ranked {} in event {}')),
    ('Verified', _('Just got verified: {}')),
    ('Trivia', _('{}/10 on School Idol Trivia! {}')),
    ('Custom', 'Custom'),
)
ACTIVITY_MESSAGE_DICT = dict(ACTIVITY_MESSAGE_CHOICES)

STATUS_CHOICES = (
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Idol Supporter')),
    ('LOVER', _('Idol Lover')),
    ('AMBASSADOR', _('Idol Ambassador')),
    ('PRODUCER', _('Idol Producer')),
    ('DEVOTEE', _('Ultimate Idol Devotee')),
)
STATUS_DICT = dict(STATUS_CHOICES)

STAFF_PERMISSIONS_CHOICES = (
    ('VERIFICATION_1', string_concat(_('Takes care of verifications:'), ' ', _('Silver Verified'))),
    ('VERIFICATION_2', string_concat(_('Takes care of verifications:'), ' ', _('Gold Verified'))),
    ('VERIFICATION_3', string_concat(_('Takes care of verifications:'), ' ', _('Bronze Verified'))),
    ('ACTIVE_MODERATOR', string_concat(_('Active'), ' ', _('Moderator'))),
    ('DECISIVE_MODERATOR', string_concat(_('Decisive'), ' ', _('Moderator'))),
    ('COMMUNITY_MANAGER', _('Community Manager')),
    ('DATABASE_MAINTAINER', _('Database Maintainer')),
    ('DEVELOPER', _('Developer')),
)
STAFF_PERMISSIONS_DICT = dict(STAFF_PERMISSIONS_CHOICES)

VERIFICATION_STATUS_CHOICES = (
    (0, _('Rejected')),
    (1, _('Pending')),
    (2, _('In Progress')),
    (3, _('Verified')),
)
VERIFICATION_STATUS_DICT = dict(VERIFICATION_STATUS_CHOICES)

VERIFICATION_STATUS_CHOICES = (
    (0, _('Rejected')),
    (1, _('Pending')),
    (2, _('In Progress')),
    (3, _('Verified')),
)
VERIFICATION_STATUS_DICT = dict(VERIFICATION_STATUS_CHOICES)

VERIFICATION_UNTRANSLATED_STATUS_CHOICES = (
    (0, 'Rejected'),
    (1, 'Pending'),
    (2, 'In Progress'),
    (3, 'Verified'),
)
VERIFICATION_UNTRANSLATED_STATUS_DICT = dict(VERIFICATION_UNTRANSLATED_STATUS_CHOICES)

MODERATION_REPORT_STATUS_CHOICES = (
    (0, 'Rejected'),
    (1, 'Pending'),
    (2, 'In Progress'),
    (3, 'Accepted'),
)
MODERATION_REPORT_STATUS_DICT = dict(MODERATION_REPORT_STATUS_CHOICES)

LINK_CHOICES = (
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
    ('reddit', 'Reddit'),
    ('line', 'LINE Messenger'),
    ('tumblr', 'Tumblr'),
    ('otonokizaka', 'Otonokizaka.org Forum'),
    ('twitch', 'Twitch'),
    ('steam', 'Steam'),
    ('osu', 'Osu!'),
    ('mal', 'MyAnimeList'),
    ('instagram', 'Instagram'),
    ('myfigurecollection', 'MyFigureCollection'),
    ('hummingbird', 'Hummingbird'),
    ('youtube', 'YouTube'),
    ('deviantart', 'DeviantArt'),
    ('pixiv', 'Pixiv'),
    ('github', 'GitHub'),
    ('animeplanet', 'Anime-Planet'),
)
LINK_DICT = dict(LINK_CHOICES)

LINK_URLS = {
    'Best Girl': '/idol/{}/',
    'Location': 'http://maps.google.com/?q={}',
    'Birthdate': '/map/',
    'twitter': 'http://twitter.com/{}',
    'facebook': 'https://www.facebook.com/{}',
    'reddit': 'http://www.reddit.com/user/{}',
    'line': 'http://line.me/#{}',
    'tumblr': 'http://{}.tumblr.com/',
    'otonokizaka': 'http://otonokizaka.org/index.php?user/{}/',
    'twitch': 'http://twitch.tv/{}',
    'steam': 'http://steamcommunity.com/id/{}',
    'osu': 'http://osu.ppy.sh/u/{}',
    'mal': 'http://myanimelist.net/profile/{}',
    'instagram': 'https://instagram.com/{}/',
    'myfigurecollection': 'http://myfigurecollection.net/profile/{}',
    'hummingbird': 'https://hummingbird.me/users/{}',
    'youtube': 'https://www.youtube.com/{}',
    'deviantart': 'http://{}.deviantart.com/gallery/',
    'pixiv': 'http://www.pixiv.net/member.php?id={}',
    'github': 'https://github.com/{}',
    'animeplanet': 'http://www.anime-planet.com/users/{}',
}

LINK_IMAGES = {
    'reddit': 'http://i.schoolido.lu/static/reddit.png',
    'twitter': 'http://i.schoolido.lu/static/twitter.png',
    'facebook': 'http://i.schoolido.lu/static/facebook.png',
    'instagram': 'http://i.schoolido.lu/static/instagram.png',
    'line': 'http://i.schoolido.lu/static/line.png',
    'twitch': 'http://i.schoolido.lu/static/twitch.png',
    'mal': 'http://i.schoolido.lu/static/mal.png',
    'steam': 'http://i.schoolido.lu/static/steam.png',
    'tumblr': 'http://i.schoolido.lu/static/tumblr.png',
}

LINK_RELEVANCE_CHOICES = (
    (0, _('Never')),
    (1, _('Sometimes')),
    (2, _('Often')),
    (3, _('Every single day')),
)
LINK_RELEVANCE_DICT = dict(LINK_RELEVANCE_CHOICES)

ACCOUNT_TAB_CHOICES = (
    ('deck', _('Deck')),
    ('album', _('Album')),
    ('teams', _('Teams')),
    ('events', _('Events')),
    ('wishlist', _('Wish List')),
    ('presentbox', _('Present Box')),
)
ACCOUNT_TAB_DICT = dict(ACCOUNT_TAB_CHOICES)

HOME_TAB_CHOICES = (
    ('following', _('Following')),
    ('all', _('All')),
)
ACCOUNT_TAB_DICT = dict(ACCOUNT_TAB_CHOICES)

ACCOUNT_TAB_ICONS = (
    ('deck', 'deck'),
    ('album', 'album'),
    ('teams', 'more'),
    ('events', 'event'),
    ('wishlist', 'star'),
    ('presentbox', 'present'),
)
ACCOUNT_TAB_ICONS_DICT = dict(ACCOUNT_TAB_ICONS)

CENTER_SKILL_SENTENCES = {
    'Power': _('{} increases slightly (+3%)'),
    'Heart': _('{} increases (+6%)'),
    'UR': _('{} increases drastically (+9%)'),
    'differentUR':  _('{} increases based on {}'),
}

CENTER_SKILL_UR = {
    'Princess': 'Smile',
    'Angel': 'Pure',
    'Empress': 'Cool',
}

CENTER_SKILL_TRANSLATE = _('Princess'), _('Angel'), _('Empress'), _('Power'), _('Heart')

TRIVIA_SCORE_SENTENCES = [
    _('Ouch!'),
    _('Oh no...'),
    _('Oh no...'),
    _('Oh no...'),
    _('Meh.'),
    _('Meh.'),
    _('Not bad!'),
    _('Not bad!'),
    _('Yay~'),
    _('Awesome!'),
    _('Woohoo!'),
]

def triviaScoreToSentence(score):
    return TRIVIA_SCORE_SENTENCES[score]

def verifiedToString(val):
    val = int(val)
    return VERIFIED_DICT[val]

def verifiedUntranslatedToString(val):
    val = int(val)
    return VERIFIED_UNTRANSLATED_DICT[val]

def verificationStatusToString(val):
    return VERIFICATION_STATUS_DICT[val]

def verificationUntranslatedStatusToString(val):
    return VERIFICATION_UNTRANSLATED_STATUS_DICT[val]

def staffPermissionToString(val):
    return STAFF_PERMISSIONS_DICT[val]

def reportStatusToString(val):
    return MODERATION_REPORT_STATUS_DICT[val]

def activityMessageToString(val):
    return ACTIVITY_MESSAGE_DICT[val]

def playWithToString(val):
    return PLAYWITH_DICT[val]

def playWithToIcon(val):
    return PLAYWITH_ICONS_DICT[val]

def storedChoiceToString(stored):
    for key, string in STORED_CHOICES:
        if stored == key:
            return string
    return None

def linkTypeToString(val):
    return LINK_DICT[val]

def accountTabToString(val):
    return ACCOUNT_TAB_DICT[val]

def accountTabToIcon(val):
    return ACCOUNT_TAB_ICONS_DICT[val.lower()]

def statusToString(val):
    return STATUS_DICT[val]

def statusToColor(status):
    if status == 'SUPPORTER': return '#4a86e8'
    elif status == 'LOVER': return '#ff53a6'
    elif status == 'AMBASSADOR': return '#a8a8a8'
    elif status == 'PRODUCER': return '#c98910'
    elif status == 'DEVOTEE': return '#c98910'
    return ''

def statusToColorString(status):
    if status == 'SUPPORTER': return _('blue')
    elif status == 'LOVER': return _('pink')
    elif status == 'AMBASSADOR': return _('shiny Silver')
    elif status == 'PRODUCER': return _('shiny Gold')
    elif status == 'DEVOTEE': return _('shiny Gold')
    return ''

def idolToColor(idol_name):
    if idol_name in raw_information:
        return raw_information[idol_name]['color']
    return '#ccc'

def rarityToString(val):
    return RARITY_DICT[val]

def japanese_attribute(attribute):
    if attribute == 'Smile':
        return u'スマイル'
    elif attribute == 'Pure':
        return u'ピュア'
    elif attribute == 'Cool':
        return u'クール'
    return u'❤'

def event_EN_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'events/EN/' + (instance.english_name if instance.english_name else instance.japanese_name) + randomString(16) + extension

class Event(ExportModelOperationsMixin('Event'), models.Model):
    japanese_name = models.CharField(max_length=100, unique=True)
    romaji_name = models.CharField(max_length=100, blank=True, null=True)
    english_name = models.CharField(max_length=100, blank=True, null=True)
    beginning = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    english_beginning = models.DateTimeField(blank=True, null=True)
    english_end = models.DateTimeField(blank=True, null=True)
    english_t1_points = models.PositiveIntegerField(null=True, blank=True)
    english_t1_rank = models.PositiveIntegerField(null=True, blank=True)
    english_t2_points = models.PositiveIntegerField(null=True, blank=True)
    english_t2_rank = models.PositiveIntegerField(null=True, blank=True)
    japanese_t1_points = models.PositiveIntegerField(null=True, blank=True)
    japanese_t1_rank = models.PositiveIntegerField(null=True, blank=True)
    japanese_t2_points = models.PositiveIntegerField(null=True, blank=True)
    japanese_t2_rank = models.PositiveIntegerField(null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    english_image = models.ImageField(upload_to=event_EN_upload_to, null=True, blank=True)

    def is_japan_current(self):
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > self.beginning
                and timezone.now() < self.end)

    def is_world_current(self):
        return (self.english_beginning is not None
                and self.english_end is not None
                and timezone.now() > self.english_beginning
                and timezone.now() < self.english_end)

    def did_happen_world(self):
        return (self.english_beginning is not None
                and self.english_end is not None
                and timezone.now() > self.english_end)

    def did_happen_japan(self):
         return (self.beginning is not None
                 and self.end is not None
                 and timezone.now() > self.end)

    def soon_happen_world(self):
        return (self.english_beginning is not None
                and self.english_end is not None
                and timezone.now() > (self.english_beginning - relativedelta(days=3))
                and timezone.now() < self.english_beginning)

    def soon_happen_japan(self):
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > (self.beginning - relativedelta(days=3))
                and timezone.now() < self.beginning)

    def __unicode__(self):
        return self.japanese_name

admin.site.register(Event)

class Idol(ExportModelOperationsMixin('Idol'), models.Model):
    name = models.CharField(max_length=100, unique=True)
    japanese_name = models.CharField(max_length=100, blank=True, null=True)
    main = models.BooleanField(default=False)
    main_unit = models.CharField(max_length=20, blank=True, null=True)
    sub_unit = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True, default=None)
    astrological_sign = models.CharField(max_length=20, blank=True, null=True)
    blood = models.CharField(max_length=3, blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    measurements = models.CharField(max_length=20, blank=True, null=True)
    favorite_food = models.CharField(max_length=100, blank=True, null=True)
    least_favorite_food = models.CharField(max_length=100, blank=True, null=True)
    hobbies = models.CharField(max_length=100, blank=True, null=True)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    year = models.CharField(max_length=10, blank=True, null=True)
    cv = models.CharField(max_length=100, blank=True, null=True)
    cv_url = models.CharField(max_length=200, blank=True, null=True)
    cv_nickname = models.CharField(max_length=20, blank=True, null=True)
    cv_twitter = models.CharField(max_length=200, blank=True, null=True)
    cv_instagram = models.CharField(max_length=200, blank=True, null=True)
    official_url = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def short_name(self):
        return self.name.split(' ')[-1]

admin.site.register(Idol)

class Card(ExportModelOperationsMixin('Card'), models.Model):
    id = models.PositiveIntegerField(unique=True, help_text="Number of the card in the album", primary_key=3)
    idol = models.ForeignKey(Idol, related_name='cards', blank=True, null=True, on_delete=models.SET_NULL)
    japanese_collection = models.CharField(max_length=100, blank=True, null=True)
    english_collection = models.CharField(max_length=100, blank=True, null=True)
    translated_collection = models.CharField(max_length=100, blank=True, null=True)
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=10)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    is_promo = models.BooleanField(default=False, help_text="Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.")
    promo_item = models.CharField(max_length=100, blank=True, null=True)
    promo_link = models.CharField(max_length=300, blank=True, null=True)
    release_date = models.DateField(default=datetime.date(2013, 4, 16), null=True, blank=True)
    event = models.ForeignKey(Event, related_name='cards', blank=True, null=True, on_delete=models.SET_NULL)
    other_event = models.ForeignKey(Event, related_name='other_cards', blank=True, null=True, on_delete=models.SET_NULL)
    is_special = models.BooleanField(default=False, help_text="Special cards cannot be added in a team but they can be used in training.")
    japan_only = models.BooleanField(default=True)
    seal_shop = models.BooleanField(default=False)
    hp = models.PositiveIntegerField(null=True, default=0, blank=True)
    minimum_statistics_smile = models.PositiveIntegerField(null=True)
    minimum_statistics_pure = models.PositiveIntegerField(null=True)
    minimum_statistics_cool = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_smile = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_pure = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_cool = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_smile = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_pure = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_cool = models.PositiveIntegerField(null=True)
    skill = models.TextField(null=True, blank=True)
    japanese_skill = models.TextField(null=True, blank=True)
    skill_details = models.TextField(null=True, blank=True)
    japanese_skill_details = models.TextField(null=True, blank=True)
    center_skill = models.TextField(null=True, blank=True)
    transparent_image = models.ImageField(upload_to='cards/transparent/', null=True, blank=True)
    transparent_idolized_image = models.ImageField(upload_to='cards/transparent/', null=True, blank=True)
    card_image = models.ImageField(upload_to='cards/', null=True, blank=True)
    card_idolized_image = models.ImageField(upload_to='cards/', null=True, blank=True)
    round_card_image = models.ImageField(upload_to='cards/', null=True, blank=True)
    round_card_idolized_image = models.ImageField(upload_to='cards/', null=True, blank=True)
    video_story = models.CharField(max_length=300, blank=True, null=True)
    japanese_video_story = models.CharField(max_length=300, blank=True, null=True)
    _skill_up_cards = models.CharField(max_length=300, blank=True, null=True)
    ur_pair = models.ForeignKey('self', related_name='other_ur_pair', on_delete=models.SET_NULL, null=True, blank=True)
    ur_pair_reverse = models.BooleanField(default=False)
    ur_pair_idolized_reverse = models.BooleanField(default=False)
    clean_ur = models.ImageField(upload_to='web/static/cards/ur_pairs/', null=True, blank=True)
    clean_ur_idolized = models.ImageField(upload_to='web/static/cards/ur_pairs/', null=True, blank=True)
    # cache
    total_owners = models.PositiveIntegerField(null=True, blank=True)
    total_wishlist = models.PositiveIntegerField(null=True, blank=True)
    ranking_attribute = models.PositiveIntegerField(null=True, blank=True)
    ranking_rarity = models.PositiveIntegerField(null=True, blank=True)
    ranking_special = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    japanese_name = models.CharField(max_length=100, blank=True, null=True)
    idol_school = models.CharField(max_length=100, blank=True, null=True)
    idol_year = models.CharField(max_length=10, blank=True, null=True)
    idol_main_unit = models.CharField(max_length=20, blank=True, null=True)
    idol_sub_unit = models.CharField(max_length=20, blank=True, null=True)
    event_japanese_name = models.CharField(max_length=100, blank=True, null=True)
    event_english_name = models.CharField(max_length=100, blank=True, null=True)
    event_image = models.CharField(max_length=200, null=True, blank=True)
    other_event_japanese_name = models.CharField(max_length=100, blank=True, null=True)
    other_event_english_name = models.CharField(max_length=100, blank=True, null=True)
    other_event_image = models.CharField(max_length=200, null=True, blank=True)
    ur_pair_name = models.CharField(max_length=100, blank=True)
    ur_pair_round_card_image = models.CharField(max_length=200, null=True, blank=True)
    ur_pair_attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6, blank=True, null=True)

    @property
    def short_name(self):
        return self.name.split(' ')[-1]

    def japanese_attribute(self):
        return japanese_attribute(self.attribute)

    def get_owned_cards_for_account(self, account):
        return OwnedCard.objects.filter(owner_account=account, card=self)

    def __unicode__(self):
        return u'#' + unicode(self.id) + u' ' + unicode(self.name) + u' ' + unicode(self.rarity)

    def get_center_skill_details(self):
        try:
            attribute, skill = self.center_skill.split(' ')
            if skill in CENTER_SKILL_UR:
                if CENTER_SKILL_UR[skill] != attribute:
                    return CENTER_SKILL_SENTENCES['differentUR'], [attribute, CENTER_SKILL_UR[skill]]
                return CENTER_SKILL_SENTENCES['UR'], [attribute]
            return CENTER_SKILL_SENTENCES[skill], [attribute]
        except (ValueError, AttributeError, KeyError):
            return None, None

    @property
    def ur_pair_japanese_attribute(self):
        return japanese_attribute(self.ur_pair_attribute)

    @property
    def skill_up_cards(self):
        if not self._skill_up_cards:
            return []
        return [(int(s.split('-')[0]), s.split('-')[-1]) for s in self._skill_up_cards.split(',')]

admin.site.register(Card)

class Account(ExportModelOperationsMixin('Account'), models.Model):
    owner = models.ForeignKey(User, related_name='accounts_set')
    nickname = models.CharField(_("Nickname"), blank=True, max_length=20)
    friend_id = models.PositiveIntegerField(_("Friend ID"), blank=True, null=True, help_text=_('You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.'))
    show_friend_id = models.BooleanField('', default=True, help_text=_('Should your friend ID be visible to other players?'))
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), blank=True, null=True)
    transfer_code = models.CharField(_("Transfer Code"), blank=True, max_length=100, help_text=_('It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.'))
    device = models.CharField(_('Device'), help_text=_('The modele of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True, blank=True)
    play_with = models.CharField(_('Play with'), blank=True, null=True, max_length=30, choices=PLAYWITH_CHOICES)
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, default='JP', max_length=10, help_text=_('This is the version of the game you play.'))
    os = models.CharField(_("Operating System"), choices=OS_CHOICES, default='iOs', max_length=10)
    center = models.ForeignKey('OwnedCard', verbose_name=_("Center"), null=True, blank=True, help_text=_('The character that talks to you on your home screen.'), on_delete=models.SET_NULL)
    rank = models.PositiveIntegerField(_("Rank"), blank=True, null=True)
    verified = models.PositiveIntegerField(_("Verified"), default=0, choices=VERIFIED_CHOICES)
    default_tab = models.CharField(_('Default tab'), max_length=30, choices=ACCOUNT_TAB_CHOICES, help_text=_('What people see first when they take a look at your account.'), default='deck')
    starter = models.ForeignKey(Card, verbose_name=_("Starter"), null=True, blank=True, help_text=_('The character that you selected when you started playing.'), on_delete=models.SET_NULL)
    creation = models.DateField(blank=True, null=True, verbose_name=_('Creation'), help_text=_('When you started playing with this account.'))
    show_creation = models.BooleanField('', default=True, help_text=_('Should this date be visible to other players?'))
    loveca = models.PositiveIntegerField(_('Love gems'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Love gems')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    friend_points = models.PositiveIntegerField(_('Friend Points'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Friend Points')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    g = models.PositiveIntegerField('G', help_text=string_concat(_('Number of {} you currently have in your account.').format('G'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    tickets = models.PositiveIntegerField('Scouting Tickets', help_text=string_concat(_('Number of {} you currently have in your account.').format('Scouting Tickets'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    vouchers = models.PositiveIntegerField('Vouchers (blue tickets)', help_text=string_concat(_('Number of {} you currently have in your account.').format('Vouchers (blue tickets)'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    bought_loveca = models.PositiveIntegerField(_('Total love gems bought'), help_text=_('You can calculate that number in "Other" then "Purchase History". Leave it empty to stay F2P.'), null=True, blank=True)
    show_items = models.BooleanField('', default=True, help_text=_('Should your items be visible to other players?'))
    fake = models.BooleanField(_('Fake'), default=False)
    # Cache
    owner_username = models.CharField(max_length=32, null=True, blank=True)
    center_card_transparent_image = models.CharField(max_length=200, null=True, blank=True)
    center_card_round_image = models.CharField(max_length=200, null=True, blank=True)
    center_card_attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6, blank=True, null=True)
    center_card_id = models.PositiveIntegerField(default=0)
    center_alt_text = models.CharField(max_length=100, null=True, blank=True)
    ranking = models.PositiveIntegerField(null=True, blank=True)

    @property
    def website_url(self):
        return 'http://schoolido.lu/user/{}/#{}'.format(self.owner_username, self.id)

    @property
    def money_spent(self):
        if not self.bought_loveca:
            return None
        return int(round(self.bought_loveca * settings.LOVECA_PRICE))

    @property
    def days_played(self):
        if not self.creation:
            return None
        today = datetime.date.today()
        return (today - self.creation).days

    def _get_starter_idol(self):
        a =  (e for e in raw_information.items() if e[1]['starter'] == self.starter_id).next()
        return a

    @property
    def starter_card_round_image(self):
        if not self.starter_id:
            return None
        return 'cards/' + str(self.starter_id) + 'Round' + self._get_starter_idol()[0].split(' ')[-1] + '.png'

    @property
    def starter_name(self):
        if not self.starter_id:
            return None
        return self._get_starter_idol()[0]

    @property
    def starter_attribute(self):
        if not self.starter_id:
            return None
        return 'Smile'

    @property
    def starter_alt_text(self):
        if not self.starter_id:
            return None
        return "#{} {} R".format(self.starter_id, self._get_starter_idol()[0])

    def __unicode__(self):
        return (unicode(self.owner.username) if self.nickname == '' else unicode(self.nickname)) + u' ' + unicode(self.language)

admin.site.register(Account)

class OwnedCard(ExportModelOperationsMixin('OwnedCard'), models.Model):
    owner_account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='ownedcards')
    card = models.ForeignKey(Card, related_name='ownedcards')
    stored = models.CharField(_("Stored"),  choices=STORED_CHOICES, default='Deck', max_length=30)
    expiration = models.DateTimeField(_("Expiration"), default=None, null=True, blank=True)
    idolized = models.BooleanField(_("Idolized"), default=False)
    max_level = models.BooleanField(_("Max Leveled"), default=False)
    max_bond = models.BooleanField(_("Max Bonded (Kizuna)"), default=False)
    skill = models.PositiveIntegerField(string_concat(_('Skill'), ' (', _('Level'), ')'), default=1, validators=[validators.MaxValueValidator(8), validators.MinValueValidator(1)])

    @property
    def owner(self):
        return self.owner_account.owner

    def __unicode__(self):
        return unicode(self.owner_account) + u' owns ' + unicode(self.card)

admin.site.register(OwnedCard)

class Team(models.Model):
    owner_account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='teams')
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

admin.site.register(Team)

class Member(models.Model):
    team = models.ForeignKey(Team, related_name='members')
    ownedcard = models.ForeignKey(OwnedCard)
    position = models.PositiveIntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(8)])

    class Meta:
        unique_together = (('team', 'position'), ('team', 'ownedcard'))

admin.site.register(Member)

class EventParticipation(ExportModelOperationsMixin('EventParticipation'), models.Model):
    event = models.ForeignKey(Event, related_name='participations')
    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='events')
    ranking = models.PositiveIntegerField(_('Ranking'), null=True, blank=True)
    song_ranking = models.PositiveIntegerField(_('Song Ranking'), null=True, blank=True)
    points = models.PositiveIntegerField(_('Points'), null=True, blank=True)
    # cache
    account_language = models.CharField(choices=LANGUAGE_CHOICES, default='JP', max_length=10)
    account_link = models.CharField(max_length=200, null=True, blank=True)
    account_picture = models.CharField(max_length=500, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    account_owner = models.CharField(max_length=100, null=True, blank=True)
    account_owner_status = models.CharField(choices=STATUS_CHOICES, max_length=12, null=True)

    @property
    def owner(self):
        return self.account.owner

    class Meta:
        unique_together = (('event', 'account'))

admin.site.register(EventParticipation)

class UserLink(ExportModelOperationsMixin('UserLink'), models.Model):
    alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z-_\. ]*$', 'Only alphanumeric and - _ characters are allowed.')
    owner = models.ForeignKey(User, related_name='links')
    type = models.CharField(_('Platform'), max_length=20, choices=LINK_CHOICES)
    value = models.CharField(_('Username/ID'), max_length=64, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    relevance = models.PositiveIntegerField(_('How often do you tweet/stream/post about Love Live?'), choices=LINK_RELEVANCE_CHOICES, null=True)

    def url(self):
        return LINK_URLS[self.type].format(self.value)

    @property
    def icon(self):
        return LINK_IMAGES[self.type]

admin.site.register(UserLink)

class UserPreferences(ExportModelOperationsMixin('UserPreferences'), models.Model):
    alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z-_\.]*$', 'Only alphanumeric and - _ characters are allowed.')
    user = models.OneToOneField(User, related_name='preferences')
    color = models.CharField(_('Attribute'), choices=ATTRIBUTE_CHOICES, max_length=6, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, help_text=_('Write whatever you want. You can add formatting and links using Markdown.'), blank=True)
    best_girl = models.CharField(_('Best Girl'), max_length=200, null=True, blank=True)
    location = models.CharField(_('Location'), max_length=200, null=True, blank=True, help_text=string_concat(_('The city you live in.'), ' ', _('It might take up to 24 hours to update your location on the map.')))
    location_changed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    twitter = models.CharField(max_length=15, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    reddit = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    line = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric]) # max length not checked
    tumblr = models.CharField(max_length=32, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    otonokizaka = models.CharField(verbose_name='Otonokizaka.org Forum', max_length=20, null=True, blank=True, help_text='Write your UID only, no URL.', validators=[alphanumeric])
    twitch = models.CharField(max_length=25, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    mal = models.CharField(verbose_name='MyAnimeList', max_length=16, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    private = models.BooleanField(_('Private Profile'), default=False, help_text=_('If your profile is private, people will only see your center.'))
    following = models.ManyToManyField(User, related_name='followers')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, null=True)
    donation_link = models.CharField(max_length=200, null=True, blank=True)
    donation_link_title = models.CharField(max_length=100, null=True, blank=True)
    _staff_permissions = models.CharField(max_length=200, null=True, blank=True)
    birthdate = models.DateField(_('Birthdate'), blank=True, null=True)
    default_tab = models.CharField(_('Default tab'), max_length=30, choices=HOME_TAB_CHOICES, help_text=_('The activities you see by default on the homepage.'), default='following')

    def avatar(self, size):
        default = 'https://i.schoolido.lu/static/kotori.jpg'
        if self.twitter:
            default = 'http://schoolido.lu/avatar/twitter/' + self.twitter
        return ("http://www.gravatar.com/avatar/"
                + hashlib.md5(self.user.email.lower()).hexdigest()
                + "?" + urllib.urlencode({'d': default, 's': str(size)}))

    @property
    def staff_permissions(self):
        if self._staff_permissions:
            return self._staff_permissions.split(',')
        return []

    def has_permission(self, permission):
        return permission in self.staff_permissions

    @property
    def has_verification_permissions(self):
        return 'VERIFICATION' in self._staff_permissions

    @property
    def allowed_verifications(self):
        return [int(permission.replace('VERIFICATION_', '')) for permission in self.staff_permissions if 'VERIFICATION' in permission]

    @property
    def age(self):
        if not self.birthdate:
            return None
        today = datetime.date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

admin.site.register(UserPreferences)

class Activity(ExportModelOperationsMixin('Activity'), models.Model):
    """
    Added card/Idolized (1 per ownedcard):
      right_picture: card icon
      right_picture_link: card
    Rank up (1 per account):
      number
    Ranked in event (1 per eventparticipation):
      right_picture: event banner
    Verified (1 per account):
      number
    """
    # Foreign keys
    account = models.ForeignKey(Account, related_name='activities', null=True, blank=True, db_index=True)
    ownedcard = models.ForeignKey(OwnedCard, null=True, blank=True)
    eventparticipation = models.ForeignKey(EventParticipation, null=True, blank=True)
    # Data
    creation = models.DateTimeField(auto_now=True, db_index=True)
    message_type = models.PositiveIntegerField(choices=ACTIVITY_MESSAGE_CHOICES_INT, db_index=True)
    message = models.CharField(max_length=300, choices=ACTIVITY_MESSAGE_CHOICES)
    number = models.PositiveIntegerField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_activities")
    # Cached data (can be generated from foreign keys)
    message_data = models.TextField(blank=True, null=True)
    account_link = models.CharField(max_length=200)
    account_picture = models.CharField(max_length=500)
    account_name = models.CharField(max_length=100)
    right_picture_link = models.CharField(max_length=200, blank=True, null=True)
    right_picture = models.CharField(max_length=100, blank=True, null=True)

    def utf_8_encoder(self, unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

    def unicode_csv_reader(self, unicode_csv_data, **kwargs):
        csv_reader = csv.reader(self.utf_8_encoder(unicode_csv_data), **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

    def split_message_data(self):
        if not self.message_data:
            return []
        reader = self.unicode_csv_reader([self.message_data])
        for reader in reader:
            return [r for r in reader]
        return []

    @property
    def localized_message_activity(self):
        activity = self
        if activity.message == 'Custom':
            return activity.message_data
        message_string = activityMessageToString(activity.message)
        data = [_(STORED_DICT_FOR_ACTIVITIES[d]) if d in STORED_DICT_FOR_ACTIVITIES else _(d) for d in activity.split_message_data()]
        if len(data) == message_string.count('{}'):
            return _(message_string).format(*data)
        return 'Invalid message data'

    def __unicode__(self):
        return u'%s %s' % (self.account, self.message)

admin.site.register(Activity)

class UserImage(ExportModelOperationsMixin('UserImage'), models.Model):
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

admin.site.register(UserImage)

class VerificationRequest(ExportModelOperationsMixin('VerificationRequest'), models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    verification_date = models.DateTimeField(null=True)
    account = models.ForeignKey(Account, related_name='verificationrequest', unique=True)
    verification = models.PositiveIntegerField(_('Verification'), default=1, choices=VERIFIED_CHOICES, help_text=_('What kind of verification would you like?'))
    status = models.PositiveIntegerField(default=0, choices=VERIFICATION_STATUS_CHOICES)
    comment = models.TextField(_('Comment'), null=True, help_text=_('If you have anything to say to the person who is going to verify your account, feel free to write it here!'), blank=True)
    verified_by = models.ForeignKey(User, related_name='verificationsdone', null=True)
    images = models.ManyToManyField(UserImage, related_name="request")
    verification_comment = models.TextField(_('Comment'), null=True, blank=True)
    allow_during_events = models.BooleanField(_('Allow us to verify your account during events'), default=False, help_text=_('Check this only if you don\'t care about the current event. You\'ll get verified faster.'))

admin.site.register(VerificationRequest)

class ModerationReport(models.Model):
    reported_by = models.ForeignKey(User, related_name='reports_sent', null=True, on_delete=models.SET_NULL)
    moderated_by = models.ForeignKey(User, related_name='moderation_done', null=True, on_delete=models.SET_NULL)
    creation = models.DateTimeField(auto_now_add=True)
    moderation_date = models.DateTimeField(null=True)
    fake_account = models.ForeignKey(Account, related_name='moderationreport', null=True)
    fake_eventparticipation = models.ForeignKey(EventParticipation, related_name='moderationreport', null=True, on_delete=models.SET_NULL)
    fake_user = models.ForeignKey(User, related_name='moderationreport', null=True)
    fake_activity = models.ForeignKey(Activity, related_name='moderationreport', null=True)
    status = models.PositiveIntegerField(default=1, choices=MODERATION_REPORT_STATUS_CHOICES)
    comment = models.TextField(_('Comment'), null=True, blank=True)
    images = models.ManyToManyField(UserImage, related_name="report")
    moderation_comment = models.TextField(_('Comment'), null=True, blank=True)

admin.site.register(ModerationReport)

class Song(ExportModelOperationsMixin('Song'), models.Model):
    name = models.CharField(max_length=100, unique=True)
    romaji_name = models.CharField(max_length=100, blank=True, null=True)
    translated_name = models.CharField(max_length=100, blank=True, null=True)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    BPM = models.PositiveIntegerField(null=True, blank=True)
    time = models.PositiveIntegerField(null=True, blank=True)
    event = models.OneToOneField(Event, related_name='song', null=True, blank=True, on_delete=models.SET_NULL)
    rank = models.PositiveIntegerField(null=True, blank=True)
    daily_rotation = models.CharField(max_length=2, null=True, blank=True)
    daily_rotation_position = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='songs/', null=True, blank=True)
    easy_difficulty = models.PositiveIntegerField(null=True, blank=True)
    easy_notes = models.PositiveIntegerField(null=True, blank=True)
    normal_difficulty = models.PositiveIntegerField(null=True, blank=True)
    normal_notes = models.PositiveIntegerField(null=True, blank=True)
    hard_difficulty = models.PositiveIntegerField(null=True, blank=True)
    hard_notes = models.PositiveIntegerField(null=True, blank=True)
    expert_difficulty = models.PositiveIntegerField(null=True, blank=True)
    expert_random_difficulty = models.PositiveIntegerField(null=True, blank=True)
    expert_notes = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    itunes_id = models.PositiveIntegerField(null=True, blank=True)

    @property
    def expert_random_notes(self):
        return self.expert_notes

    @property
    def japanese_attribute(self):
        return japanese_attribute(self.attribute)

    def __unicode__(self):
        return self.name

admin.site.register(Song)

# class TradeOrGiveawayAccount(models.Model):
#     account = models.ForeignKey(Account, related_name='trade_or_giveaway', unique=True)
#     verification_request = models.ForeignKey(VerificationRequest, related_name='trade_account')
#     type = models.PositiveIntegerField(choices=TRADE_OR_GIVEAWAY_TYPE)
#     status = models.PositiveIntegerField(choices=TRADE_OR_GIVEAWAY_STATUS)
#     external_link = models.CharField(max_length=300, null=True)
#     message = models.TextField(_('Message'), null=True, help_text=_('Write whatever you want. You can add formatting and links using Markdown.'), blank=True)
#     minimum_price = models.PositiveIntegerField(_('Minimum price'), validators=[validators.MaxValueValidator(5000)], null=True)
#     transfer_code = models.ImageField(upload_to='trades_and_giveaways/', null=True, blank=True)

#     def __unicode__(self):
#         return u'{} {}'.format(tradeOrGiveawayTypeToString(self.type), self.account)

# admin.site.register(TradeOrGiveawayAccount)

# class TradeOffer(models.Model):
#     trade_or_giveaway_account = models.ForeignKey(TradeOrGiveawayAccount, related_name='trade_offers')
#     account = models.ForeignKey(Account, related_name='trade_offer', unique=True)
#     accepted_date = models.DateTimeField(null=True)
#     verification_request = models.ForeignKey(VerificationRequest, related_name='trade_offer')
#     transfer_code = models.ImageField(upload_to='trades_and_giveaways/', null=True, blank=True)

usicaltriofestival_entries = [
    (7, u'ღ\'s ☪★♪', u'だってだって噫無情', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/zCvNz1K6Tvo?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (11, u'βN\'s', u'UNBALANCED LOVE', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/C_GWBT4hkAY?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (13, u'FURious Alpaca', u'after school NAVIGATORS', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/3X7I50_7LfQ?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (14, u'wAr-RICE', u'同じ星が見たい', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/-dbIC1ei0ZM?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (21, u'Crystal❖Lilies', u'錯覚CROSSROADS', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/XFf3FjQPq5c?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (22, u'Procrastinate → Tomorrow', u'UNBALANCED LOVE', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/cPJFupdJVEM?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (23, u'Petit ƸӜƷ Papillon', u'思い出以上になりたくて', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/3RkNI-pbpW8?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (38, u'✿Ƈнσcσℓαт Ƒση∂αηт✿', u'冬がくれた予感', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/xmqS66cNzrQ?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (40, u'NYAvigators', u'春情ロマンティック', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/MZNKw06GMGE?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (54, u'ミkμ', u'Mermaid festa vol.2 ~Passionate~', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/-gG8BSbVplM?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (56, u'lilaq✿', u'UNBALANCED life marginal (Mashup: UNBALANCED LOVE, Someday of my life, LOVE marginal)', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/8QBcFAEISpM?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (57, u'Sock It 2 Me', u'同じ星が見たい', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/7VzhIsvFzKQ?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (59, u'茶茶茶', u'あ・の・ね・が・ん・ば・れ!', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/geB0BmK75ao?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (61, u'AKB0033', u'孤独なHeaven', True, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/j2mO0oboM1c?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (62, u'Undefined Red', u'るてしキスキしてる', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/JSSBe6PrlBQ?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
    (67, u'Midnight✿Blossoms', u'Silent tonight', False, '<iframe style="width: 100%" height="172" src="http://www.youtube.com/embed/hWZ3KVgsaKY?rel=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'),
]

usicaltriofestival_entries_db = [(i[0], i[1]) for i in usicaltriofestival_entries]

class UsicalVote(models.Model):
    entry = models.PositiveIntegerField(default=0, choices=usicaltriofestival_entries_db)
    user = models.ForeignKey(User, related_name='usical_vote', unique=True)
