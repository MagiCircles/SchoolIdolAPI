from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
import datetime

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        if self.context['request'].method == 'POST' or self.context['request'].user == obj:
            return obj.email
        return None

    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        if 'password' not in self.context['request'].data:
            raise serializers.ValidationError(detail={'password': ['This field is required.']})
        user = super(UserSerializer, self).create(data)
        user.set_password(self.context['request'].data)
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    japan_current = serializers.SerializerMethodField()
    world_current = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    def get_japan_current(self, obj):
        return obj.is_japan_current()

    def get_world_current(self, obj):
        return obj.is_world_current()

    def get_cards(self, obj):
        cards = models.Card.objects.filter(event=obj)
        cards = [card.pk for card in cards]
        return cards

    class Meta:
        model = models.Event
        fields = ('japanese_name', 'english_name', 'beginning', 'end', 'japan_current', 'world_current', 'cards')

class CardSerializer(serializers.HyperlinkedModelSerializer):
    japan_only = serializers.SerializerMethodField()
    event = EventSerializer()
    is_event = serializers.SerializerMethodField()

    def get_japan_only(self, obj):
        return (obj.is_promo
                or obj.release_date + relativedelta(years=1) > datetime.date.today())

    def get_is_event(self, obj):
        return obj.event != None

    class Meta:
        model = models.Card
        fields = ('id', 'name', 'rarity', 'attribute', 'is_promo', 'promo_item', 'release_date', 'japan_only', 'is_event', 'event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'skill_details', 'center_skill', 'card_url', 'card_idolized_url')
