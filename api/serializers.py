from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id', 'name', 'rarity', 'attribute', 'is_promo', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'skill_details', 'center_skill', 'card_url', 'card_idolized_url')
    
