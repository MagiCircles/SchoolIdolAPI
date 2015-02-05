# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib import admin
from dateutil.relativedelta import relativedelta
import datetime

ATTRIBUTE_CHOICES = (
    ('Smile', 'Smile'),
    ('Pure', 'Pure'),
    ('Cool', 'Cool'),
    ('All', 'All'),
)

RARITY_CHOICES = (
    ('N', 'Normal'),
    ('R', 'Rare'),
    ('SR', 'Super Rare'),
    ('UR', 'Ultra Rare'),
)

LANGUAGE_CHOICES = (
    ('JP', 'Japanese'),
    ('EN', 'English'),
    ('KR', 'Korean'),
    ('CH', 'Chinese'),
)

OS_CHOICES = (
    ('Android', 'Android'),
    ('iOs', 'iOs'),
)

STORED_CHOICES = (
    ('Deck', 'In deck'),
    ('Album', 'In album'),
    ('Box', 'In present box'),
    ('Favorite', 'Favorite Cards'),
)

class Event(models.Model):
    japanese_name = models.CharField(max_length=100, unique=True)
    english_name = models.CharField(max_length=100)
    beginning = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    def is_japan_current(self):
        return (self.beginning is not None
                and self.end is not None
                and datetime.date.today() > self.beginning
                and datetime.date.today() < self.end)

    def is_world_current(self):
        return (self.beginning is not None
                and self.end is not None
                and datetime.date.today() > (self.beginning + relativedelta(years=1))
                and datetime.date.today() < (self.end + relativedelta(years=1)))

    def __unicode__(self):
        return self.japanese_name

admin.site.register(Event)

class Card(models.Model):
    id = models.PositiveIntegerField(unique=True, help_text="Number of the card in the album", primary_key=3)
    name = models.CharField(max_length=100)
    japanese_name = models.CharField(max_length=100, blank=True, null=True)
    japanese_collection = models.CharField(max_length=100, blank=True, null=True)
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=10)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    is_promo = models.BooleanField(default=False, help_text="Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.")
    promo_item = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(default=datetime.date(2013, 4, 16), null=True, blank=True)
    event = models.ForeignKey(Event, related_name='card', blank=True, null=True)
    is_special = models.BooleanField(default=False, help_text="Special cards cannot be added in a team but they can be used in training.")
    hp = models.PositiveIntegerField(null=True)
    minimum_statistics_smile = models.PositiveIntegerField(null=True)
    minimum_statistics_pure = models.PositiveIntegerField(null=True)
    minimum_statistics_cool = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_smile = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_pure = models.PositiveIntegerField(null=True)
    non_idolized_maximum_statistics_cool = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_smile = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_pure = models.PositiveIntegerField(null=True)
    idolized_maximum_statistics_cool = models.PositiveIntegerField(null=True)
    skill = models.TextField(null=True)
    japanese_skill = models.TextField(null=True)
    skill_details = models.TextField(null=True)
    japanese_skill_details = models.TextField(null=True)
    center_skill = models.TextField(null=True)
    japanese_center_skill = models.TextField(null=True)
    japanese_center_skill_details = models.TextField(null=True)
    card_url = models.CharField(max_length=200, blank=True)
    card_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)
    card_idolized_url = models.CharField(max_length=200, blank=True)
    card_idolized_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)
    round_card_url = models.CharField(max_length=200, blank=True, null=True)
    round_card_image = models.ImageField(upload_to='web/static/cards/', null=True, blank=True)

    def japanese_attribute(self):
        if self.attribute == 'Smile':
            return 'スマイル'
        elif self.attribute == 'Pure':
            return 'ピュア'
        elif self.attribute == 'Cool':
            return 'クール'
        return ''

    def is_japan_only(self):
        return (self.is_promo
                or self.release_date + relativedelta(years=1) > datetime.date.today())

    def get_owned_cards_for_account(self, account):
        return OwnedCard.objects.filter(owner_account=account, card=self)

    def __unicode__(self):
        return '#' + str(self.id) + ' ' + self.name + ' ' + self.rarity

admin.site.register(Card)

class Account(models.Model):
    owner = models.ForeignKey(User, related_name='account')
    nickname = models.CharField(blank=True, max_length=20)
    friend_id = models.PositiveIntegerField(blank=True, null=True, help_text='You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.')
    transfer_code = models.CharField(blank=True, max_length=30, help_text='It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='JP', max_length=10, help_text='This is the version of the game you play.')
    os = models.CharField(choices=OS_CHOICES, default='iOs', max_length=10)
    center = models.ForeignKey('OwnedCard', null=True, blank=True, help_text='The character that talks to you on your home screen.')
    rank = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return (self.owner.username if self.nickname == '' else self.nickname) + ' ' + self.language

admin.site.register(Account)

class OwnedCard(models.Model):
    owner_account = models.ForeignKey(Account, related_name='ownedcard')
    card = models.ForeignKey(Card, related_name='ownedcard')
    stored = models.CharField(choices=STORED_CHOICES, default='Deck', max_length=30)
    expiration = models.DateTimeField(default=None, null=True, blank=True)
    idolized = models.BooleanField(default=False)
    max_level = models.BooleanField(default=False)
    max_bond = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.owner_account) + ' owns ' + str(self.card)

admin.site.register(OwnedCard)
