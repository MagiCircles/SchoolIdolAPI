# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils import translation
from django.core.urlresolvers import reverse as django_reverse
from web.utils import chibiimage, singlecardurl
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

class UserLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.url()
    class Meta:
        model = models.UserLink
        fields = ('type', 'value', 'relevance', 'icon', 'url')

class UserSerializer(serializers.ModelSerializer):
    accounts = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    preferences = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    def get_website_url(self, obj):
        return 'http://schoolido.lu/user/' + urllib.quote(obj.username) + '/'

    def get_accounts(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('user-'):
            if 'expand_accounts' in self.context['request'].query_params:
                serializer = AccountSerializer(obj.all_accounts, many=True, context=self.context)
                return serializer.data
            return note_to_expand("accounts", multiple=True)
        return None

    def get_links(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('user-'):
            if 'expand_links' in self.context['request'].query_params:
                serializer = UserLinkSerializer(obj.all_links, many=True, context=self.context)
                return serializer.data
            return note_to_expand("links", multiple=True)
        return None

    def get_preferences(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('user-'):
            if 'expand_preferences' in self.context['request'].query_params:
                serializer = UserPreferencesSerializer(obj.preferences, context=self.context)
                return serializer.data
            return note_to_expand('preferences')
        return None

    def get_is_following(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('user-'):
            if 'expand_is_following' in self.context['request'].query_params and hasattr(obj, 'is_following'):
                return bool(obj.is_following)
            return 'To know if the authenticated user follows this user or not, use the parameter \"expand_is_following\"'
        return None

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'accounts', 'preferences', 'links', 'website_url', 'is_following')
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

    class Meta:
        model = models.Event
        lookup_field = 'japanese_name'
        fields = ('japanese_name', 'romaji_name', 'english_name', 'image', 'english_image', 'beginning', 'end', 'english_beginning', 'english_end', 'japan_current', 'world_current', 'japanese_t1_points', 'japanese_t1_rank', 'japanese_t2_points', 'japanese_t2_rank', 'english_t1_points', 'english_t1_rank', 'english_t2_points', 'english_t2_rank', 'note')

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

    def get_chibi(self, obj):
        return chibiimage(obj.name, small=False)

    def get_chibi_small(self, obj):
        return chibiimage(obj.name, small=True)

    class Meta:
        model = models.Idol
        fields = ('name', 'japanese_name', 'main', 'age', 'birthday', 'astrological_sign', 'blood', 'height', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'attribute', 'year', 'main_unit', 'sub_unit', 'cv', 'summary', 'website_url', 'wiki_url', 'wikia_url', 'official_url', 'chibi', 'chibi_small')

def _get_image(image):
    if image:
        base_url = settings.IMAGES_HOSTING_PATH
        return u'%s%s' % (base_url, image)
    return None

def note_to_expand(obj, multiple=False):
    return 'To get the full {} object{}, use the parameter "expand_{}"'.format(obj, 's' if multiple else '', obj)

class CardIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id',)

class ImageField(serializers.ImageField):
    def to_representation(self, value):
        if value:
            return u'%s%s' % (settings.IMAGES_HOSTING_PATH, value.name)
        return None

class CardSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    idol = serializers.SerializerMethodField()
    card_image = ImageField(required=False)
    card_idolized_image = ImageField(required=False)
    round_card_image = ImageField(required=False)
    round_card_idolized_image = ImageField(required=False)
    japanese_attribute = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    non_idolized_max_level = serializers.SerializerMethodField()
    idolized_max_level = serializers.SerializerMethodField()
    transparent_image = ImageField(required=False)
    transparent_idolized_image = ImageField(required=False)
    clean_ur = ImageField(required=False)
    clean_ur_idolized = ImageField(required=False)
    center_skill_details = serializers.SerializerMethodField()
    japanese_center_skill = serializers.SerializerMethodField()
    japanese_center_skill_details = serializers.SerializerMethodField()

    def get_event(self, obj):
        if not obj.event_id:
            return None
        if self.context['request'].resolver_match.url_name.startswith('card-'):
            if 'expand_event' in self.context['request'].query_params:
                serializer = EventSerializer(obj.event, context=self.context)
                return serializer.data
        return {
            'japanese_name': obj.event_japanese_name,
            'english_name': obj.event_english_name,
            'image': _get_image(obj.event_image),
            'note': note_to_expand('event') if self.context['request'].resolver_match.url_name.startswith('card-') else None,
        }

    def get_idol(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('card-'):
            if 'expand_idol' in self.context['request'].query_params:
                serializer = IdolSerializer(obj.idol, context=self.context)
                return serializer.data
        return {
            'name': obj.name,
            'japanese_name': obj.japanese_name,
            'school': obj.idol_school,
            'year': obj.idol_year,
            'main_unit': obj.idol_main_unit,
            'sub_unit': obj.idol_sub_unit,
            'note': note_to_expand('idol') if self.context['request'].resolver_match.url_name.startswith('card-') else None,
            'chibi': chibiimage(obj.name, small=False),
            'chibi_small': chibiimage(obj.name, small=True),
        }

    def get_japanese_attribute(self, obj):
        return obj.japanese_attribute()

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
        return 'http://schoolido.lu' + singlecardurl(obj)

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

    def _save_fk(self, card):
        changed = False
        event = self.context['request'].data.get('event', None)
        idol = self.context['request'].data.get('idol', None)
        if event:
            if event == 'None':
                card.event = None
            else:
                event = models.Event.objects.get(japanese_name=event)
                card.event = event
            changed = True
        if idol:
            idol = models.Idol.objects.get(name=idol)
            card.idol = idol
            #card.name = idol.name
            changed = True
        if changed:
            card.save()
        return card

    def create(self, validated_data):
        card = super(CardSerializer, self).create(validated_data)
        return self._save_fk(card)

    def update(self, instance, validated_data):
        card = super(CardSerializer, self).update(instance, validated_data)
        return self._save_fk(card)

    class Meta:
        model = models.Card
        fields = ('id', 'idol', 'japanese_collection', 'translated_collection', 'rarity', 'attribute', 'japanese_attribute', 'is_promo', 'promo_item', 'promo_link', 'release_date', 'japan_only', 'event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'center_skill_details', 'japanese_center_skill', 'japanese_center_skill_details', 'card_image', 'card_idolized_image', 'round_card_image', 'round_card_idolized_image', 'video_story', 'japanese_video_story', 'website_url', 'non_idolized_max_level', 'idolized_max_level', 'transparent_image', 'transparent_idolized_image', 'clean_ur', 'clean_ur_idolized')

class SongSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_event(self, obj):
        if not obj.event_id:
            return None
        if self.context['request'].resolver_match.url_name.startswith('song-'):
            if 'expand_event' in self.context['request'].query_params:
                serializer = EventSerializer(obj.event, context=self.context)
                return serializer.data
        return note_to_expand("event")

    def get_image(self, obj):
        return _get_image(obj.image)

    class Meta:
        model = models.Song
        fields = ('name', 'romaji_name', 'translated_name', 'attribute', 'BPM', 'time', 'event', 'rank', 'daily_rotation', 'daily_rotation_position', 'image', 'easy_difficulty', 'easy_notes', 'normal_difficulty', 'normal_notes', 'hard_difficulty', 'hard_notes', 'expert_difficulty', 'expert_random_difficulty', 'expert_notes', 'available', 'itunes_id')
        lookup_field = 'name'

class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    center = serializers.SerializerMethodField()
    starter = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()

    def get_website_url(self, obj):
        return obj.website_url

    def get_center(self, obj):
        if not obj.center_id:
            return None
        return {
            'id': obj.center_id,
            'card': obj.center_card_id,
            'round_image': _get_image(obj.center_card_round_image),
            'attribute': obj.center_card_attribute,
            'card_text': obj.center_alt_text,
        }

    def get_starter(self, obj):
        return {
            'id': obj.starter_id,
            'round_image': _get_image(obj.starter_card_round_image),
            'card_text': obj.starter_alt_text,
            'attribute': obj.starter_attribute,
        }

    def get_owner(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('account-'):
            if 'expand_owner' in self.context['request'].query_params:
                serializer = UserSerializer(obj.owner, context=self.context)
                return serializer.data
        return obj.owner_username

    def get_nickname(self, obj):
        return obj.nickname

    def create(self, data):
        data['owner'] = self.context['request'].user
        return super(AccountSerializer, self).create(data)

    class Meta:
        model = models.Account
        fields = ('id', 'owner', 'nickname', 'friend_id', 'language', 'center', 'starter', 'rank', 'os', 'device', 'play_with', 'accept_friend_requests', 'verified', 'website_url')

class OwnedCardWithoutCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OwnedCard
        fields = ('id', 'idolized', 'stored', 'expiration', 'max_level', 'max_bond', 'skill')

class OwnedCardSerializer(serializers.ModelSerializer):
    owner_account = serializers.SerializerMethodField()
    card = serializers.SerializerMethodField()

    def get_card(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('ownedcard-'):
            if 'expand_card' in self.context['request'].query_params:
                serializer = CardSerializer(obj.card, context=self.context)
                return serializer.data
        return obj.card_id

    def get_owner_account(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('ownedcard-'):
            if 'expand_owner' in self.context['request'].query_params:
                serializer = AccountSerializer(obj.owner_account, context=self.context)
                return serializer.data
        return obj.owner_account_id

    class Meta:
        model = models.OwnedCard
        fields = ('id', 'owner_account', 'card', 'stored', 'idolized', 'max_level', 'max_bond', 'expiration', 'skill')
