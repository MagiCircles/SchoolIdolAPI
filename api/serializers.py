from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
import datetime

class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    accounts = serializers.SerializerMethodField()

    def get_email(self, obj):
        if self.context['request'].method == 'POST' or self.context['request'].user == obj:
            return obj.email
        return None

    def get_accounts(self, obj):
        accounts = models.Account.objects.filter(owner=obj)
        serializer = AccountSerializer(accounts, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'email', 'accounts')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        if 'password' not in self.context['request'].data:
            raise serializers.ValidationError(detail={'password': ['This field is required.']})
        user = super(UserSerializer, self).create(data)
        user.set_password(self.context['request'].data['password'])
        user.save()
        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class EventSerializer(serializers.ModelSerializer):
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

class CardSerializer(serializers.ModelSerializer):
    japan_only = serializers.SerializerMethodField()
    event = EventSerializer()

    def get_japan_only(self, obj):
        return obj.is_japan_only()

    class Meta:
        model = models.Card
        fields = ('id', 'name', 'rarity', 'attribute', 'is_promo', 'promo_item', 'release_date', 'japan_only', 'event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'skill_details', 'center_skill', 'card_url', 'card_idolized_url')

class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    transfer_code = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.owner.username

    def get_transfer_code(self, obj):
        if self.context['request'].user == obj.owner:
            return obj.transfer_code
        return None

    def get_nickname(self, obj):
        if not obj.nickname:
            return obj.owner.username
        return obj.nickname

    def create(self, data):
        data['owner'] = self.context['request'].user
        return super(AccountSerializer, self).create(data)

    class Meta:
        model = models.Account
        fields = ('pk', 'owner', 'nickname', 'friend_id', 'transfer_code', 'language', 'os', 'center', 'rank')

class OwnedCardSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = models.OwnedCard
        fields = ('owner_account', 'card', 'idolized', 'stored', 'expiration')
