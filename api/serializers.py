# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse as django_reverse
import urllib
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
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            base_url = settings.IMAGES_HOSTING_PATH
            return u'%s%s' % (base_url, obj.image) if obj.image else ''
        return None

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
        fields=('japanese_name', 'english_name', 'image', 'beginning', 'end', 'japan_current', 'world_current', 'cards', 'japanese_t1_points', 'japanese_t1_rank', 'japanese_t2_points', 'japanese_t2_rank', 'note')

class IdolSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    wiki_url = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()

    def get_birthday(self, obj):
        if obj.birthday:
            return obj.birthday.strftime('%m-%d')
        return None

    def get_website_url(self, obj):
        return 'http://schoolido.lu/cards/?name=' + urllib.quote(obj.name)

    def get_wiki_url(self, obj):
        return 'http://decaf.kouhi.me/lovelive/index.php?title=' + urllib.quote(obj.name)

    def get_cv(self, obj):
        if not obj.cv:
            return None
        return {
            'name': obj.cv,
            'nickname': obj.cv_nickname,
            'url': obj.cv_url,
            'twitter': obj.cv_twitter,
            'instagram': obj.cv_instagram,
        }

    class Meta:
        model = models.Idol
        fields = ('name', 'japanese_name', 'main', 'age', 'birthday', 'astrological_sign', 'blood', 'height', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'attribute', 'year', 'cv', 'summary', 'website_url', 'wiki_url', 'official_url')

class CardSerializer(serializers.ModelSerializer):
    japan_only = serializers.SerializerMethodField()
    event = EventSerializer()
    idol = IdolSerializer()
    name = serializers.SerializerMethodField() # left for backward compatibility
    japanese_name = serializers.SerializerMethodField() # left for backward compatibility
    card_image = serializers.SerializerMethodField()
    card_idolized_image = serializers.SerializerMethodField()
    round_card_image = serializers.SerializerMethodField()
    owned_cards = serializers.SerializerMethodField()
    japanese_attribute = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()

    def _image_file_to_url(self, path, card, circle=False, idolized=False):
        base_url = settings.IMAGES_HOSTING_PATH
        if (not path and 'imagedefault' in self.context['request'].GET and self.context['request'].GET['imagedefault'] and self.context['request'].GET['imagedefault'].title() != 'False' and
            (idolized or circle or (not card.is_special and not card.is_promo))):
            if circle:
                return base_url + '/static/circle-' + card.attribute + '.png'
            return base_url + '/static/default-' + card.attribute + '.png'
        return '%s%s' % (base_url, path) if path else ''

    def get_name(self, obj):
        return obj.idol.name

    def get_japanese_name(self, obj):
        return obj.idol.japanese_name

    def get_japanese_attribute(self, obj):
        return obj.japanese_attribute()

    def get_japan_only(self, obj):
        return obj.is_japan_only()

    def get_card_image(self, obj):
        return self._image_file_to_url(str(obj.card_image), obj)
    def get_card_idolized_image(self, obj):
        return self._image_file_to_url(str(obj.card_idolized_image), obj, idolized=True)
    def get_round_card_image(self, obj):
        return self._image_file_to_url(str(obj.round_card_image), obj, circle=True)

    def get_website_url(self, obj):
        return 'http://schoolido.lu/cards/' + str(obj.id) + '/'

    def get_owned_cards(self, obj):
        if (not self.context['request'] or not self.context['request']
            or not self.context['request'].query_params
            or 'account' not in self.context['request'].query_params):
            return None
        account = int(self.context['request'].query_params['account'])
        return OwnedCardWithoutCardSerializer(obj.get_owned_cards_for_account(account), many=True, context=self.context).data

    class Meta:
        model = models.Card
        fields = ('id', 'name', 'japanese_name', 'idol', 'japanese_collection', 'rarity', 'attribute', 'japanese_attribute', 'is_promo', 'promo_item', 'release_date', 'japan_only', 'event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'japanese_center_skill', 'japanese_center_skill_details', 'card_image', 'card_idolized_image', 'round_card_image', 'video_story', 'japanese_video_story', 'website_url', 'owned_cards')

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

class OwnedCardWithoutCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OwnedCard
        fields = ('idolized', 'stored', 'expiration', 'max_level', 'max_bond')

class OwnedCardSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = models.OwnedCard
        fields = ('owner_account', 'card', 'idolized', 'max_level', 'max_bond', 'stored', 'expiration')
