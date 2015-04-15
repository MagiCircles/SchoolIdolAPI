# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib import admin
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _, string_concat
from api.models_languages import LANGUAGE_CHOICES
from django.core import validators
from django.utils import timezone

import datetime

ATTRIBUTE_CHOICES = (
    ('Smile', _('Smile')),
    ('Pure', _('Pure')),
    ('Cool', _('Cool')),
    ('All', _('All')),
)

RARITY_CHOICES = (
    ('N', _('Normal')),
    ('R', _('Rare')),
    ('SR', _('Super Rare')),
    ('UR', _('Ultra Rare')),
)

OS_CHOICES = (
    ('Android', 'Android'),
    ('iOs', 'iOs'),
)

STORED_CHOICES = (
    ('Deck', _('Deck')),
    ('Album', _('Album')),
    ('Box', _('Present Box')),
    ('Favorite', _('Wish List')),
)
STORED_DICT = dict(STORED_CHOICES)

VERIFIED_CHOICES = (
    (0, ''),
    (1, _('Silver Verified')),
    (2, _('Gold Verified')),
)
VERIFIED_DICT = dict(VERIFIED_CHOICES)

PLAYWITH_CHOICES = (
    ('Thumbs', _('Thumbs')),
    ('Fingers', _('All fingers')),
    ('Hand', _('One hand')),
    ('Other', _('Other')),
)
PLAYWITH_DICT = dict(PLAYWITH_CHOICES)

def verifiedToString(val):
    return VERIFIED_DICT[val]

def playWithToString(val):
    return PLAYWITH_DICT[val]

def storedChoiceToString(stored):
    for key, string in STORED_CHOICES:
        if stored == key:
            return string
    return None

def japanese_attribute(attribute):
    if attribute == 'Smile':
        return u'スマイル'
    elif attribute == 'Pure':
        return u'ピュア'
    elif attribute == 'Cool':
        return u'クール'
    return u'❤'

class Event(models.Model):
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
    image = models.ImageField(upload_to='web/static/events/', null=True, blank=True)

    def is_japan_current(self):
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > self.beginning
                and timezone.now() < self.end)

    def is_world_current(self):
        if (self.english_beginning is not None
            and self.english_end is not None):
            return (timezone.now() > self.english_beginning
                    and timezone.now() < self.english_end)
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > (self.beginning + relativedelta(years=1))
                and timezone.now() < (self.end + relativedelta(years=1)))

    def did_happen_world(self):
        if (self.english_beginning is not None
            and self.english_end is not None):
            return (timezone.now() > self.english_beginning)
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > (self.beginning + relativedelta(years=1)))

    def __unicode__(self):
        return self.japanese_name

admin.site.register(Event)

class Idol(models.Model):
    name = models.CharField(max_length=100, unique=True)
    japanese_name = models.CharField(max_length=100, blank=True, null=True)
    main = models.BooleanField(default=False)
    age = models.PositiveIntegerField(blank=True, null=True)
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

admin.site.register(Idol)

class Card(models.Model):
    id = models.PositiveIntegerField(unique=True, help_text="Number of the card in the album", primary_key=3)
    name = models.CharField(max_length=100, blank=True) # duplicate with idol, used only in __unicode__ because otherwise it makes another query everytime
    idol = models.ForeignKey(Idol, related_name='cards', blank=True, null=True, on_delete=models.SET_NULL)
    japanese_collection = models.CharField(max_length=100, blank=True, null=True)
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=10)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    is_promo = models.BooleanField(default=False, help_text="Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.")
    promo_item = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(default=datetime.date(2013, 4, 16), null=True, blank=True)
    event = models.ForeignKey(Event, related_name='cards', blank=True, null=True, on_delete=models.SET_NULL)
    is_special = models.BooleanField(default=False, help_text="Special cards cannot be added in a team but they can be used in training.")
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
    japanese_center_skill = models.TextField(null=True, blank=True)
    japanese_center_skill_details = models.TextField(null=True, blank=True)
    card_url = models.CharField(max_length=200, blank=True)
    card_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)
    card_idolized_url = models.CharField(max_length=200, blank=True)
    card_idolized_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)
    round_card_url = models.CharField(max_length=200, blank=True, null=True)
    round_card_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)
    video_story = models.CharField(max_length=300, blank=True, null=True)
    japanese_video_story = models.CharField(max_length=300, blank=True, null=True)

    def japanese_attribute(self):
        return japanese_attribute(self.attribute)

    def is_japan_only(self):
        return ((self.release_date and self.release_date + relativedelta(years=1) - relativedelta(days=2) > datetime.date.today())
                or (self.is_promo and not self.video_story)
                or (self.is_special and self.id >= 379))

    def get_owned_cards_for_account(self, account):
        return OwnedCard.objects.filter(owner_account=account, card=self)

    def __unicode__(self):
        return '#' + str(self.id) + ' ' + self.name + ' ' + self.rarity

admin.site.register(Card)

class Account(models.Model):
    owner = models.ForeignKey(User, related_name='accounts_set')
    nickname = models.CharField(_("Nickname"), blank=True, max_length=20)
    friend_id = models.PositiveIntegerField(_("Friend ID"), blank=True, null=True, help_text=_('You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.'))
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), blank=True, null=True)
    transfer_code = models.CharField(_("Transfer Code"), blank=True, max_length=30, help_text=_('It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.'))
    device = models.CharField(_('Device'), help_text=_('The modele of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True, blank=True)
    play_with = models.CharField(_('Play with'), blank=True, null=True, max_length=30, choices=PLAYWITH_CHOICES)
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, default='JP', max_length=10, help_text=_('This is the version of the game you play.'))
    os = models.CharField(_("Operating System"), choices=OS_CHOICES, default='iOs', max_length=10)
    center = models.ForeignKey('OwnedCard', verbose_name=_("Center"), null=True, blank=True, help_text=_('The character that talks to you on your home screen.'), on_delete=models.SET_NULL)
    rank = models.PositiveIntegerField(_("Rank"), blank=True, null=True)
    verified = models.PositiveIntegerField(default=0, choices=VERIFIED_CHOICES)

    def __unicode__(self):
        return (self.owner.username if self.nickname == '' else self.nickname) + ' ' + self.language

admin.site.register(Account)

class OwnedCard(models.Model):
    owner_account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='ownedcards')
    card = models.ForeignKey(Card, related_name='ownedcards')
    stored = models.CharField(_("Stored"),  choices=STORED_CHOICES, default='Deck', max_length=30)
    expiration = models.DateTimeField(_("Expiration"), default=None, null=True, blank=True)
    idolized = models.BooleanField(_("Idolized"), default=False)
    max_level = models.BooleanField(_("Max Leveled"), default=False)
    max_bond = models.BooleanField(_("Max Bonded (Kizuna)"), default=False)
    skill = models.PositiveIntegerField(string_concat(_('Skill'), ' (', _('Level'), ')'), default=1, validators=[validators.MaxValueValidator(8), validators.MinValueValidator(1)])

    def __unicode__(self):
        return str(self.owner_account) + ' owns ' + str(self.card)

admin.site.register(OwnedCard)

class EventParticipation(models.Model):
    event = models.ForeignKey(Event, related_name='participations')
    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='events')
    ranking = models.PositiveIntegerField(_('Ranking'), null=True, blank=True)
    song_ranking = models.PositiveIntegerField(_('Song Ranking'), null=True, blank=True)
    points = models.PositiveIntegerField(_('Points'), null=True, blank=True)

    class Meta:
        unique_together = (('event', 'account'))

admin.site.register(EventParticipation)

class UserPreferences(models.Model):
    alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z-_\.]*$', 'Only alphanumeric and - _ characters are allowed.')
    user = models.ForeignKey(User, related_name='preferences')
    color = models.CharField(_('Attribute'), choices=ATTRIBUTE_CHOICES, max_length=6, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, help_text=_('Write whatever you want. You can add formatting and links using Markdown.'), blank=True)
    best_girl = models.CharField(_('Best Girl'), max_length=200, null=True, blank=True)
    location = models.CharField(_('Location'), max_length=200, null=True, blank=True, help_text=_('The city you live in.'))
    location_changed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    twitter = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    facebook = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    reddit = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    line = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    tumblr = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    otonokizaka = models.CharField(verbose_name='Otonokizaka.org Forum', max_length=20, null=True, blank=True, help_text='Write your UID only, no URL.', validators=[alphanumeric])
    twitch = models.CharField(max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    mal = models.CharField(verbose_name='MyAnimeList', max_length=20, null=True, blank=True, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    private = models.BooleanField(_('Private Profile'), default=False, help_text=_('If your profile is private, people will only see your center.'))
    following = models.ManyToManyField(User, symmetrical=False, related_name='followers')

admin.site.register(UserPreferences)

# Add card to deck/album/wish list
# Level up
# Idolized / Max leveled / Max bonded
class Activity(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name='activities', null=True, blank=True)
    message = models.CharField(max_length=300)
    rank = models.PositiveIntegerField(null=True, blank=True)
    ownedcard = models.ForeignKey(OwnedCard, null=True, blank=True)
    eventparticipation = models.ForeignKey(EventParticipation, null=True, blank=True)

admin.site.register(Activity)
