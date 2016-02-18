# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils import translation
from django.core.urlresolvers import reverse as django_reverse
from web.utils import chibiimage
import urllib
import datetime
import pytz

class DateTimeJapanField(serializers.DateTimeField):
    def to_representation(self, value):
        value = value.astimezone(pytz.timezone('Asia/Tokyo'))
        return super(DateTimeJapanField, self).to_representation(value)

class UserPreferencesSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.avatar(200)

    class Meta:
        model = models.UserPreferences
        fields = ('color', 'description', 'best_girl', 'location', 'latitude', 'longitude', 'private', 'status', 'avatar')

class UserSerializer(serializers.ModelSerializer):
    accounts = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    preferences = UserPreferencesSerializer()
    website_url = serializers.SerializerMethodField()

    def get_website_url(self, obj):
        return 'http://schoolido.lu/user/' + urllib.quote(obj.username) + '/'

    def get_accounts(self, obj):
        accounts = models.Account.objects.filter(owner=obj)
        serializer = AccountSerializer(accounts, many=True, context=self.context)
        return serializer.data

    def get_links(self, obj):
        return [{'type': link.type, 'url': link.url(), 'relevance': link.relevance} for link in obj.links.all()]

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'accounts', 'preferences', 'links', 'website_url')
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
    beginning = DateTimeJapanField()
    end = DateTimeJapanField()
    japan_current = serializers.SerializerMethodField()
    world_current = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()
    song = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    english_image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _get_image(obj.image)

    def get_english_image(self, obj):
        return _get_image(obj.english_image)

    def get_japan_current(self, obj):
        return obj.is_japan_current()

    def get_world_current(self, obj):
        return obj.is_world_current()

    def get_cards(self, obj):
        cards = models.Card.objects.filter(event=obj)
        cards = [card.pk for card in cards]
        return cards

    def get_song(self, obj):
        try: return obj.songs.all()[0].name
        except: return None

    class Meta:
        model = models.Event
        lookup_field = 'japanese_name'
        fields = ('japanese_name', 'romaji_name', 'english_name', 'image', 'english_image', 'beginning', 'end', 'english_beginning', 'english_end', 'japan_current', 'world_current', 'cards', 'song', 'japanese_t1_points', 'japanese_t1_rank', 'japanese_t2_points', 'japanese_t2_rank', 'english_t1_points', 'english_t1_rank', 'english_t2_points', 'english_t2_rank', 'note')

class IdolSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    wiki_url = serializers.SerializerMethodField()
    wikia_url = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()
    chibi = serializers.SerializerMethodField()
    chibi_small = serializers.SerializerMethodField()

    def get_birthday(self, obj):
        if obj.birthday:
            return obj.birthday.strftime('%m-%d')
        return None

    def get_website_url(self, obj):
        return 'http://schoolido.lu/idol/' + urllib.quote(obj.name) + '/'

    def get_wikia_url(self, obj):
        if obj.main:
            return 'http://love-live.wikia.com/wiki/' + urllib.quote(obj.name.replace(' ', '_'))
        return None

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

    def _chibi_image(self, name, small):
        image = chibiimage(name, small)
        if settings.IMAGES_HOSTING_PATH in image:
            return image
        return 'http://schoolido.lu' + image

    def get_chibi(self, obj):
        return self._chibi_image(obj.name, small=False)

    def get_chibi_small(self, obj):
        return self._chibi_image(obj.name, small=True)

    class Meta:
        model = models.Idol
        fields = ('name', 'japanese_name', 'main', 'age', 'birthday', 'astrological_sign', 'blood', 'height', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'attribute', 'year', 'sub_unit', 'cv', 'summary', 'website_url', 'wiki_url', 'wikia_url', 'official_url', 'chibi', 'chibi_small')

def _get_image(image):
    if image:
        base_url = settings.IMAGES_HOSTING_PATH
        return u'%s%s' % (base_url, image)
    return None

class CardIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id',)


class CardSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    idol = IdolSerializer()
    name = serializers.SerializerMethodField() # left for backward compatibility
    japanese_name = serializers.SerializerMethodField() # left for backward compatibility
    card_image = serializers.SerializerMethodField()
    card_idolized_image = serializers.SerializerMethodField()
    round_card_image = serializers.SerializerMethodField()
    round_card_idolized_image = serializers.SerializerMethodField()
    owned_cards = serializers.SerializerMethodField()
    japanese_attribute = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    non_idolized_max_level = serializers.SerializerMethodField()
    idolized_max_level = serializers.SerializerMethodField()
    transparent_image = serializers.SerializerMethodField()
    transparent_idolized_image = serializers.SerializerMethodField()
    transparent_ur_pair = serializers.SerializerMethodField()
    transparent_idolized_ur_pair = serializers.SerializerMethodField()
    center_skill_details = serializers.SerializerMethodField()
    japanese_center_skill = serializers.SerializerMethodField()
    japanese_center_skill_details = serializers.SerializerMethodField()

    def _image_file_to_url(self, path, card, circle=False, idolized=False):
        if (not path and 'imagedefault' in self.context['request'].GET and self.context['request'].GET['imagedefault'] and self.context['request'].GET['imagedefault'].title() != 'False' and
            (idolized or circle or (not card.is_special and not card.is_promo))):
            if circle:
                return _get_image('/static/circle-' + card.attribute + '.png')
            return _get_image('/static/default-' + card.attribute + '.png')
        return _get_image(path)

    def get_name(self, obj):
        if obj.idol:
            return obj.idol.name
        return None

    def get_japanese_name(self, obj):
        if obj.idol:
            return obj.idol.japanese_name
        return None

    def get_japanese_attribute(self, obj):
        return obj.japanese_attribute()

    def get_card_image(self, obj):
        return self._image_file_to_url(str(obj.card_image), obj)
    def get_card_idolized_image(self, obj):
        return self._image_file_to_url(str(obj.card_idolized_image), obj, idolized=True)
    def get_round_card_image(self, obj):
        return self._image_file_to_url(str(obj.round_card_image), obj, circle=True)
    def get_round_card_idolized_image(self, obj):
        return self._image_file_to_url(str(obj.round_card_idolized_image), obj, circle=True, idolized=True)
    def get_transparent_image(self, obj):
        return _get_image(obj.transparent_image)
    def get_transparent_idolized_image(self, obj):
        return _get_image(obj.transparent_idolized_image)
    def get_transparent_ur_pair(self, obj):
        return _get_image(obj.transparent_ur_pair)
    def get_transparent_idolized_ur_pair(self, obj):
        return _get_image(obj.transparent_idolized_ur_pair)

    def get_center_skill_details(self, obj):
        sentence, data = obj.get_center_skill_details()
        if sentence and data:
            old_lang = translation.get_language()
            translation.activate("en")
            sentence = _(sentence).format(*data)
            translation.activate(old_lang)
            return sentence
        return None

    def get_japanese_center_skill(self, obj):
        if not obj.center_skill:
            return None
        old_lang = translation.get_language()
        translation.activate("ja")
        sentence = string_concat(_(obj.center_skill.split(' ')[0]), ' ', _(obj.center_skill.split(' ')[1]))
        translation.activate(old_lang)
        return sentence

    def get_japanese_center_skill_details(self, obj):
        sentence, data = obj.get_center_skill_details()
        if sentence and data:
            old_lang = translation.get_language()
            translation.activate("ja")
            sentence = _(sentence).format(*[_(d) for d in data])
            translation.activate(old_lang)
            return sentence
        return None

    def get_website_url(self, obj):
        return 'http://schoolido.lu/cards/' + str(obj.id) + '/'

    def get_non_idolized_max_level(self, obj):
        if obj.is_promo or obj.is_special: return 0
        if obj.rarity == 'N': return 30
        elif obj.rarity == 'R': return 40
        elif obj.rarity == 'SR': return 60
        elif obj.rarity == 'UR': return 80

    def get_idolized_max_level(self, obj):
        if obj.is_special: return 0
        if obj.rarity == 'N': return 40
        elif obj.rarity == 'R': return 60
        elif obj.rarity == 'SR': return 80
        elif obj.rarity == 'UR': return 100

    def get_owned_cards(self, obj):
        if (not self.context['request']
            or not self.context['request'].query_params
            or 'account' not in self.context['request'].query_params):
            return None
        account = int(self.context['request'].query_params['account'])
        return OwnedCardWithoutCardSerializer(obj.get_owned_cards_for_account(account), many=True, context=self.context).data

    class Meta:
        model = models.Card
        fields = ('id', 'name', 'japanese_name', 'idol', 'japanese_collection', 'translated_collection', 'rarity', 'attribute', 'japanese_attribute', 'is_promo', 'promo_item', 'release_date', 'japan_only', 'event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'center_skill_details', 'japanese_center_skill', 'japanese_center_skill_details', 'card_image', 'card_idolized_image', 'round_card_image', 'round_card_idolized_image', 'video_story', 'japanese_video_story', 'website_url', 'non_idolized_max_level', 'idolized_max_level', 'owned_cards', 'transparent_image', 'transparent_idolized_image', 'transparent_ur_pair', 'transparent_idolized_ur_pair')

class SongSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _get_image(obj.image)

    class Meta:
        model = models.Song
        fields = ('name', 'romaji_name', 'translated_name', 'attribute', 'BPM', 'time', 'event', 'rank', 'daily_rotation', 'daily_rotation_position', 'image', 'easy_difficulty', 'easy_notes', 'normal_difficulty', 'normal_notes', 'hard_difficulty', 'hard_notes', 'expert_difficulty', 'expert_random_difficulty', 'expert_notes', 'available', 'itunes_id')
        lookup_field = 'name'

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OwnedCard
        fields = ('id', 'card', 'idolized', 'max_level', 'max_bond', 'skill')

class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    center = CenterSerializer()
    website_url = serializers.SerializerMethodField()

    def get_website_url(self, obj):
        return 'http://schoolido.lu/user/' + urllib.quote(obj.owner.username) + '/#' + str(obj.id)

    def get_owner(self, obj):
        return obj.owner.username

    def get_nickname(self, obj):
        if not obj.nickname:
            return obj.owner.username
        return obj.nickname

    def create(self, data):
        data['owner'] = self.context['request'].user
        return super(AccountSerializer, self).create(data)

    class Meta:
        model = models.Account
        fields = ('id', 'owner', 'nickname', 'friend_id', 'language', 'center', 'rank', 'os', 'device', 'play_with', 'accept_friend_requests', 'verified', 'website_url')

class OwnedCardWithoutCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OwnedCard
        fields = ('id', 'idolized', 'stored', 'expiration', 'max_level', 'max_bond', 'skill')

class OwnedCardSerializer(serializers.ModelSerializer):
    owner_account = serializers.SerializerMethodField()
    card = serializers.SerializerMethodField()

    def get_card(self, obj):
        if 'expand_card' in self.context['request'].query_params:
            serializer = CardSerializer(obj.card, context=self.context)
            return serializer.data
        return obj.card.id

    def get_owner_account(self, obj):
        if 'expand_owner' in self.context['request'].query_params:
            serializer = AccountSerializer(obj.owner_account, context=self.context)
            return serializer.data
        return obj.owner_account.id

    class Meta:
        model = models.OwnedCard
        fields = ('id', 'owner_account', 'card', 'stored', 'idolized', 'max_level', 'max_bond', 'expiration', 'skill')
