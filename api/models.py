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
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=10)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    is_promo = models.BooleanField(default=False, help_text="Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.")
    promo_item = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(default=datetime.date(2013, 4, 16), null=True, blank=True)
    event = models.ForeignKey(Event, related_name='card', blank=True, null=True)
    is_special = models.BooleanField(default=False, help_text="Special cards cannot be added in a team but they can be used in training.")
    hp = models.PositiveIntegerField()
    minimum_statistics_smile = models.PositiveIntegerField()
    minimum_statistics_pure = models.PositiveIntegerField()
    minimum_statistics_cool = models.PositiveIntegerField()
    non_idolized_maximum_statistics_smile = models.PositiveIntegerField()
    non_idolized_maximum_statistics_pure = models.PositiveIntegerField()
    non_idolized_maximum_statistics_cool = models.PositiveIntegerField()
    idolized_maximum_statistics_smile = models.PositiveIntegerField()
    idolized_maximum_statistics_pure = models.PositiveIntegerField()
    idolized_maximum_statistics_cool = models.PositiveIntegerField()
    skill = models.TextField(null=True)
    skill_details = models.TextField(null=True)
    center_skill = models.TextField(null=True)
    card_url = models.CharField(max_length=200, blank=True)
    card_idolized_url = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return '#' + str(self.id) + ' ' + self.name + ' ' + self.rarity

admin.site.register(Card)
