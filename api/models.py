from django.contrib.auth.models import User, Group
from django.db import models

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

class Card(models.Model):
    id = models.PositiveIntegerField(unique=True, help_text="Number of the card in the album", primary_key=3)
    name = models.CharField(max_length=100)
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=10)
    attribute = models.CharField(choices=ATTRIBUTE_CHOICES, max_length=6)
    is_promo = models.BooleanField(default=False, help_text="Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.")
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
    skill = models.TextField()
    skill_details = models.TextField()
    center_skill = models.TextField()
    card_url = models.CharField(max_length=200, blank=True)
    card_idolized_url = models.CharField(max_length=200, blank=True)
