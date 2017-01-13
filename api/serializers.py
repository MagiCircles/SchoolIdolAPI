# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from api import models
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils import translation
from django.core.urlresolvers import reverse as django_reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from web.utils import shrinkImageFromData
from django.db import IntegrityError
from web.utils import chibiimage, singlecardurl, activity_cacheaccount, get_imgur_code
from api.raw import STARTERS
from api.management.commands.update_cards_rankings import update_cards_rankings
from api.management.commands.update_cards_join_cache import update_cards_join_cache
import urllib
import datetime
import markdown_deux
import pytz
import re
import os

class DateTimeJapanField(serializers.DateTimeField):
    def to_representation(self, value):
        value = value.astimezone(pytz.timezone('Asia/Tokyo'))
        return super(DateTimeJapanField, self).to_representation(value)

class LocalizedField(serializers.CharField):
    def to_representation(self, value):
        return _(value) if value else None

class UserPreferencesSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    html_description = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.avatar(200)

    def get_html_description(self, obj):
        return markdown_deux.markdown(obj.description)

    class Meta:
        model = models.UserPreferences
        fields = ('color', 'description', 'html_description', 'best_girl', 'location', 'latitude', 'longitude', 'private', 'status', 'avatar', 'birthdate', 'default_tab')

class UserLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.url()

    class Meta:
        model = models.UserLink
        fields = ('type', 'value', 'relevance', 'icon', 'url')

class UserNotExpandableSerializer(serializers.ModelSerializer):
    website_url = serializers.SerializerMethodField()

    def get_website_url(self, obj):
        return 'http://schoolido.lu/user/' + urllib.quote(obj.username) + '/'

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'website_url')

class UserWithPreferencesSerializer(UserNotExpandableSerializer):
    preferences = serializers.SerializerMethodField()

    def get_preferences(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('user-') or self.context['request'].resolver_match.url_name.startswith('account-'):
            if 'expand_preferences' in self.context['request'].query_params:
                serializer = UserPreferencesSerializer(obj.preferences, context=self.context)
                return serializer.data
            return note_to_expand('preferences')
        return None

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'website_url', 'preferences')

class UserSerializer(UserWithPreferencesSerializer):
    accounts = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

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

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class EventSerializer(serializers.ModelSerializer):
    translated_name = serializers.SerializerMethodField()
    beginning = DateTimeJapanField()
    end = DateTimeJapanField()
    japan_current = serializers.SerializerMethodField()
    world_current = serializers.SerializerMethodField()
    japan_status = serializers.SerializerMethodField()
    english_status = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    english_image = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    note = LocalizedField()

    def get_translated_name(self, obj):
        if self.context['request'].LANGUAGE_CODE != 'en':
            return _(obj.english_name) if obj.english_name else None
        return None

    def get_image(self, obj):
        return _get_image(obj.image)

    def get_english_image(self, obj):
        return _get_image(obj.english_image)

    def get_japan_current(self, obj):
        return obj.is_japan_current()

    def get_world_current(self, obj):
        return obj.is_world_current()

    def get_japan_status(self, obj):
        if obj.is_japan_current():
            return 'ongoing'
        elif obj.did_happen_japan():
            return 'finished'
        elif obj.soon_happen_japan():
            return 'announced'
        return 'unknown'

    def get_english_status(self, obj):
        if obj.is_world_current():
            return 'ongoing'
        elif obj.did_happen_world():
            return 'finished'
        elif obj.soon_happen_world():
            return 'announced'
        return 'unknown'

    def get_website_url(self, obj):
        return 'http://schoolido.lu/events/' + urllib.quote(obj.japanese_name.encode('utf8')) + '/'

    class Meta:
        model = models.Event
        lookup_field = 'japanese_name'
        fields = ('japanese_name', 'romaji_name', 'english_name', 'translated_name', 'image', 'english_image', 'beginning', 'end', 'english_beginning', 'english_end', 'japan_current', 'world_current', 'english_status', 'japan_status', 'japanese_t1_points', 'japanese_t1_rank', 'japanese_t2_points', 'japanese_t2_rank', 'english_t1_points', 'english_t1_rank', 'english_t2_points', 'english_t2_rank', 'note', 'website_url')

class IdolSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()
    favorite_food = LocalizedField()
    least_favorite_food = LocalizedField()
    summary = LocalizedField()
    year = LocalizedField()
    hobbies = LocalizedField()
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
        fields = ('name', 'japanese_name', 'main', 'age', 'school', 'birthday', 'astrological_sign', 'blood', 'height', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'attribute', 'year', 'main_unit', 'sub_unit', 'cv', 'summary', 'website_url', 'wiki_url', 'wikia_url', 'official_url', 'chibi', 'chibi_small')

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
    other_event = serializers.SerializerMethodField()
    idol = serializers.SerializerMethodField()
    card_image = ImageField(required=False)
    card_idolized_image = ImageField(required=False)
    english_card_image = ImageField(required=False)
    english_card_idolized_image = ImageField(required=False)
    round_card_image = ImageField(required=False)
    round_card_idolized_image = ImageField(required=False)
    english_round_card_image = ImageField(required=False)
    english_round_card_idolized_image = ImageField(required=False)
    translated_collection = LocalizedField(required=False)
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
    ur_pair = serializers.SerializerMethodField()
    skill_up_cards = serializers.SerializerMethodField()

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
            'translated_name': _(obj.event_english_name) if obj.event_english_name and self.context['request'].LANGUAGE_CODE != 'en' else None,
            'image': _get_image(obj.event_image),
            'note': note_to_expand('event') if self.context['request'].resolver_match.url_name.startswith('card-') else None,
        }

    def get_other_event(self, obj):
        if not obj.other_event_id:
            return None
        if self.context['request'].resolver_match.url_name.startswith('card-'):
            if 'expand_event' in self.context['request'].query_params:
                serializer = EventSerializer(obj.other_event, context=self.context)
                return serializer.data
        return {
            'japanese_name': obj.other_event_japanese_name,
            'english_name': obj.other_event_english_name,
            'translated_name': _(obj.other_event_english_name) if obj.other_event_english_name and self.context['request'].LANGUAGE_CODE != 'en' else None,
            'image': _get_image(obj.other_event_image),
            'note': note_to_expand('event') if self.context['request'].resolver_match.url_name.startswith('card-') else None,
        }

    def get_idol(self, obj):
        expandable = (self.context['request'].resolver_match.url_name.startswith('card-')
                      and 'in_ur_pair_{}'.format(obj.ur_pair_id) not in self.context)
        if expandable and 'expand_idol' in self.context['request'].query_params:
            serializer = IdolSerializer(obj.idol, context=self.context)
            return serializer.data
        return {
            'name': obj.name,
            'japanese_name': obj.japanese_name,
            'school': obj.idol_school,
            'year': _(obj.idol_year) if obj.idol_year else None,
            'main_unit': obj.idol_main_unit,
            'sub_unit': obj.idol_sub_unit,
            'note': note_to_expand('idol') if expandable else None,
            'chibi': chibiimage(obj.name, small=False),
            'chibi_small': chibiimage(obj.name, small=True),
        }

    def get_japanese_attribute(self, obj):
        return obj.japanese_attribute()

    def get_center_skill_details(self, obj):
        if obj.center_skill:
            sentence, data = obj.get_center_skill_details()
            if sentence and data:
                return _(sentence).format(*data)
        return None

    def get_japanese_center_skill(self, obj):
        if not obj.center_skill:
            return None
        old_lang = translation.get_language()
        translation.activate("ja")
        sentence = string_concat(_(obj.center_skill.split(' ')[0]), ' ', _(obj.center_skill.split(' ')[1]))
        sentence = unicode(sentence)
        translation.activate(old_lang)
        return sentence

    def get_japanese_center_skill_details(self, obj):
        if not obj.center_skill:
            return None
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
        elif obj.rarity == 'SSR': return 70
        elif obj.rarity == 'UR': return 80

    def get_idolized_max_level(self, obj):
        if obj.is_special: return 0
        if obj.rarity == 'N': return 40
        elif obj.rarity == 'R': return 60
        elif obj.rarity == 'SR': return 80
        elif obj.rarity == 'SSR': return 90
        elif obj.rarity == 'UR': return 100

    def get_ur_pair(self, obj):
        if not obj.ur_pair_id or 'in_ur_pair_{}'.format(obj.ur_pair_id) in self.context:
            return None
        expandable = (self.context['request'].resolver_match.url_name.startswith('card-')
                      and 'in_ur_pair_{}'.format(obj.ur_pair_id) not in self.context)
        if expandable and 'expand_ur_pair' in self.context['request'].query_params:
            self.context['in_ur_pair_{}'.format(obj.id)] = True
            serializer = CardSerializer(obj.ur_pair, context=self.context)
            card = serializer.data
        else:
            card = {
                'id': obj.ur_pair_id,
                'name': obj.ur_pair_name,
                'round_card_image': _get_image(obj.ur_pair_round_card_image),
                'attribute': obj.ur_pair_attribute,
                'note': note_to_expand('ur_pair'),
            }
        return {
            'card': card,
            'reverse_display': obj.ur_pair_reverse,
            'reverse_display_idolized': obj.ur_pair_idolized_reverse,
        }

    def get_skill_up_cards(self, obj):
        return [{
            'id': card[0],
            'round_card_image': _get_image('cards/' + str(card[0]) + 'Round' + card[1] + '.png'),
        } for card in obj.skill_up_cards]

    def _tinypng_images(self, validated_data):
        idolName = self.context['request'].data.get('idol', None)
        if not idolName:
            idolName = self.instance.idol.name
        idolId = validated_data['id'] if 'id' in validated_data else self.instance.id
        for (field, value) in validated_data.items():
            if value and (isinstance(value, InMemoryUploadedFile) or isinstance(value, TemporaryUploadedFile)):
                filename = value.name
                value = shrinkImageFromData(value.read(), filename)
                validated_data[field] = value
                if field in models.cardsImagesToName:
                    value.name = models.cardsImagesToName[field]({
                        'id': idolId,
                        'firstname': idolName.split(' ')[-1] if idolName else 'Unknown',
                    })
        return validated_data

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
            try:
                idol = models.Idol.objects.get(name=idol)
            except ObjectDoesNotExist:
                idol = models.Idol.objects.create(name=idol)
            card.idol = idol
            card.name = idol.name
            changed = True
        if changed:
            card.save()
        update_cards_join_cache(cards=[card])
        update_cards_rankings({})
        return card

    def validate(self, data):
        if self.context['request'].method == 'POST' and ('idol' not in self.context['request'].data or not self.context['request'].data['idol']):
            raise serializers.ValidationError({
                'idol': ['This field is required.'],
            })
        for (field, value) in data.items():
            if value and (isinstance(value, InMemoryUploadedFile) or isinstance(value, TemporaryUploadedFile)):
                _, extension = os.path.splitext(value.name)
                if extension.lower() != '.png':
                    raise serializers.ValidationError({
                        field: ['Only png images are accepted.'],
                    })
        return data

    def create(self, validated_data):
        validated_data = self._tinypng_images(validated_data)
        card = super(CardSerializer, self).create(validated_data)
        return self._save_fk(card)

    def update(self, instance, validated_data):
        validated_data = self._tinypng_images(validated_data)
        card = super(CardSerializer, self).update(instance, validated_data)
        return self._save_fk(card)

    class Meta:
        model = models.Card
        fields = ('id', 'game_id', 'idol', 'japanese_collection', 'translated_collection', 'rarity', 'attribute', 'japanese_attribute', 'is_promo', 'promo_item', 'promo_link', 'release_date', 'japan_only', 'event', 'other_event', 'is_special', 'hp', 'minimum_statistics_smile', 'minimum_statistics_pure', 'minimum_statistics_cool', 'non_idolized_maximum_statistics_smile', 'non_idolized_maximum_statistics_pure', 'non_idolized_maximum_statistics_cool', 'idolized_maximum_statistics_smile', 'idolized_maximum_statistics_pure', 'idolized_maximum_statistics_cool', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'center_skill_details', 'japanese_center_skill', 'japanese_center_skill_details', 'card_image', 'card_idolized_image', 'english_card_image', 'english_card_idolized_image', 'round_card_image', 'round_card_idolized_image', 'english_round_card_image', 'english_round_card_idolized_image', 'video_story', 'japanese_video_story', 'website_url', 'non_idolized_max_level', 'idolized_max_level', 'transparent_image', 'transparent_idolized_image', 'clean_ur', 'clean_ur_idolized', 'skill_up_cards', 'ur_pair', 'total_owners', 'total_wishlist', 'ranking_attribute', 'ranking_rarity', 'ranking_special')

class SongSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    itunes_id = serializers.SerializerMethodField()
    translated_name = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()

    def get_event(self, obj):
        if not obj.event_id:
            return None
        if self.context['request'].resolver_match.url_name.startswith('song-'):
            if 'expand_event' in self.context['request'].query_params:
                serializer = EventSerializer(obj.event, context=self.context)
                return serializer.data
            return note_to_expand("event")
        return None

    def get_image(self, obj):
        return _get_image(obj.image)

    def get_itunes_id(self, obj):
        if obj.itunes_id:
            return obj.itunes_id
        return None

    def get_translated_name(self, obj):
        if not obj.translated_name and not obj.romaji_name and self.context['request'].LANGUAGE_CODE != 'en':
            return _(obj.name)
        return _(obj.translated_name) if obj.translated_name else None

    def get_website_url(self, obj):
        return 'http://schoolido.lu/songs/' + urllib.quote(obj.name.encode('utf8')) + '/'

    class Meta:
        model = models.Song
        fields = ('id', 'name', 'romaji_name', 'translated_name', 'attribute', 'main_unit', 'BPM', 'time', 'event', 'rank', 'daily_rotation', 'daily_rotation_position', 'image', 'easy_difficulty', 'easy_notes', 'normal_difficulty', 'normal_notes', 'hard_difficulty', 'hard_notes', 'expert_difficulty', 'expert_random_difficulty', 'expert_notes', 'master_difficulty', 'master_notes', 'available', 'itunes_id', 'website_url')
        lookup_field = 'name'

class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    center = serializers.SerializerMethodField()
    starter = serializers.SerializerMethodField()
    friend_id = serializers.SerializerMethodField()
    creation = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

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
                serializer = UserWithPreferencesSerializer(obj.owner, context=self.context)
                return serializer.data
        return obj.owner_username

    def get_friend_id(self, obj):
        if obj.show_friend_id or self.context['request'].user.id == obj.owner_id:
            return obj.friend_id
        return None

    def get_creation(self, obj):
        if obj.show_creation or self.context['request'].user.id == obj.owner_id:
            return obj.creation
        return None

    def get_items(self, obj):
        if obj.show_items or self.context['request'].user.id == obj.owner_id:
            return {
                'loveca': obj.loveca,
                'friend_points': obj.friend_points,
                'g': obj.g,
                'tickets': obj.tickets,
                'vouchers': obj.vouchers,
                'bought_loveca': obj.bought_loveca,
                'money_spent': obj.money_spent,
            }
        return None

    class Meta:
        model = models.Account
        fields = ('id', 'owner', 'nickname', 'friend_id', 'language', 'center', 'starter', 'rank', 'ranking', 'os', 'device', 'play_with', 'accept_friend_requests', 'verified', 'website_url', 'creation', 'ranking', 'default_tab', 'items', 'fake')

class EditableAccountSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializer = AccountSerializer(instance, context=self.context)
        return serializer.data

    def validate(self, data):
        errors = {}
        if hasattr(self, 'instance'):
            if self.instance.verified:
                for read_only_field in ['friend_id', 'language']:
                    if read_only_field in data:
                        errors[read_only_field] = 'You can\'t edit this field because your account is verified.'
            if 'center' in data and data['center'].owner_account_id != self.instance.id:
                errors['center'] = 'This owned card is not yours.'
            if 'rank' in data and data['rank'] >= 200 and not self.instance.verified:
                errors['rank'] = 'Only verified accounts can have a rank above 200.'
            if 'starter' in data and data['starter'].id not in STARTERS:
                errors['starter'] = 'Invalid starter id. Valid ids are: {}'.format(','.join([str(id) for id in STARTERS]))
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        extra_kwargs = {}
        if 'center' in self.validated_data:
            center = self.validated_data['center']
            card = center.card
            extra_kwargs['center_card_transparent_image'] = card.transparent_idolized_image if center.idolized or card.is_special else card.transparent_image
            if self.instance.language == 'JP':
                extra_kwargs['center_card_round_image'] = card.round_card_idolized_image if center.idolized or card.is_special else card.round_card_image
            else:
                extra_kwargs['center_card_round_image'] = card.english_round_card_idolized_image if center.idolized or card.is_special else card.english_round_card_image
            extra_kwargs['center_card_attribute'] = card.attribute
            extra_kwargs['center_alt_text'] = unicode(card)
            extra_kwargs['center_card_id'] = card.id
        kwargs.update(extra_kwargs)
        return super(EditableAccountSerializer, self).save(**kwargs)

    class Meta:
        model = models.Account
        fields = ('nickname', 'friend_id', 'accept_friend_requests', 'device', 'play_with', 'language', 'os', 'center', 'rank', 'starter', 'loveca', 'friend_points', 'g', 'tickets', 'vouchers', 'bought_loveca')

class OwnedCardSerializer(serializers.ModelSerializer):
    owner_account = serializers.SerializerMethodField()
    card = serializers.SerializerMethodField()

    def get_card(self, obj):
        if (self.context['request'].resolver_match.url_name.startswith('ownedcard-')
            or self.context['request'].resolver_match.url_name.startswith('team-')):
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

    def validate(self, data):
        errors = {}
        request = self.context['request']
        if request.method == 'POST':
            try:
                data['card'] = models.Card.objects.get(pk=request.POST['card'])
            except (ObjectDoesNotExist, KeyError):
                if 'card' not in request.POST:
                    errors['card'] = 'This field is required'
                else:
                    errors['card'] = 'Invalid id'
            try:
                data['owner_account'] = models.Account.objects.get(pk=request.POST['owner_account'], owner=request.user)
            except (ObjectDoesNotExist, KeyError):
                if 'owner_account' not in request.POST:
                    errors['owner_account'] = 'This field is required'
                else:
                    errors['owner_account'] = 'This account does\'t exist or isn\'t yours'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        extra_kwargs = {}
        if not self.instance:
            card = self.validated_data['card']
        else:
            card = self.instance.card
        if card.is_promo:
            extra_kwargs['idolized'] = True
        if card.is_special:
            extra_kwargs['idolized'] = False
        if ((self.instance and self.instance.idolized == False and 'idolized' not in self.validated_data and 'idolized' not in extra_kwargs)
            or ('idolized' in self.validated_data and self.validated_data['idolized'] == False)
            or ('idolized' in extra_kwargs and extra_kwargs['idolized'] == False)):
            extra_kwargs['max_bond'] = False
            extra_kwargs['max_level'] = False
        if ((self.instance and self.instance.stored == 'Album' and 'stored' not in self.validated_data and 'stored' not in extra_kwargs)
            or ('stored' in self.validated_data and self.validated_data['stored'] == 'Album')
            or ('stored' in extra_kwargs and extra_kwargs['stored'] == 'Album')):
            extra_kwargs['skill'] = 1
        kwargs.update(extra_kwargs)
        return super(OwnedCardSerializer, self).save(**kwargs)

    class Meta:
        model = models.OwnedCard
        fields = ('id', 'owner_account', 'card', 'stored', 'idolized', 'max_level', 'max_bond', 'expiration', 'skill')

class ActivitySerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    last_update = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    html_message = serializers.SerializerMethodField()
    message_type = serializers.SerializerMethodField()
    figure = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.account_picture

    def get_account(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('activity-'):
            if 'expand_account' in self.context['request'].query_params:
                serializer = AccountSerializer(obj.account, context=self.context)
                return serializer.data
        return {
            'id': obj.account_id,
            'website_url': obj.account_link if 'http' in obj.account_link else 'http://schoolido.lu' + obj.account_link,
            'text': obj.account_name,
            'note': note_to_expand('account'),
        }

    def get_last_update(self, obj):
        return obj.creation

    def get_message(self, obj):
        return obj.localized_message_activity

    def get_html_message(self, obj):
        return markdown_deux.markdown(obj.localized_message_activity)

    def get_message_type(self, obj):
        return obj.message

    def get_figure(self, obj):
        picture = obj.right_picture
        link = obj.right_picture_link
        link_type = None
        link_data = None
        if not picture:
            if obj.message == 'Rank Up':
                picture = 'http://i.schoolido.lu/static/activity/rankup.png'
            elif obj.message == 'Verified':
                picture = 'http://i.schoolido.lu/static/activity/verified{}.png'.format(obj.number)
            elif obj.message == 'Trivia':
                picture = 'http://i.schoolido.lu/static/activity/trivia.png'
                link = 'http://schoolido.lu/trivia/'
        if picture == "" or picture is None:
            return None
        if '/' not in picture: # imgur
            return {
                'picture': 'http://i.imgur.com/{}t.png'.format(picture),
                'link': 'http://i.imgur.com/{}.png'.format(picture),
                'link_type': 'imgur',
                'link_data': picture,
            }
        if link and 'http' not in link:
            link = 'http://schoolido.lu' + obj.right_picture_link
        if link and '/cards/' in link:
            link_type = 'cards'
            m = re.search('\/cards\/(\d+)\/', link)
            if m:
                link_data = int(m.group(1))
        if link and '/events/' in link:
            link_type = 'events'
            m = re.search('\/events\/([^/]+)\/', link)
            if m:
                link_data = m.group(1)
        return {
            'picture': picture,
            'link': link,
            'link_type': link_type,
            'link_data': link_data,
        }

    def get_liked_by(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('activity-'):
            if 'expand_liked_by' in self.context['request'].query_params:
                # When an activity is created, the get_queryset is not called and liked_by is not populated but we can assume that it's an empty list
                if self.context['request'].method == 'POST':
                    return []
                serializer = UserNotExpandableSerializer(obj.liked_by, many=True, context=self.context)
                return serializer.data
            return note_to_expand('liked_by', multiple=True)
        return None

    def get_total_likes(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('activity-'):
            if 'expand_total_likes' in self.context['request'].query_params:
                # When an activity is created, the get_queryset is not called and total_likes is not populated but we can assume that it's 0
                if self.context['request'].method == 'POST':
                    return 0
                if 'expand_liked_by' in self.context['request'].query_params:
                    return len(obj.liked_by)
                else:
                    return obj.total_likes
            return 'To get the full total number of likes, use the parameter "expand_total_likes"'
        return None

    def get_liked(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('activity-'):
            if 'expand_liked' in self.context['request'].query_params:
                # When an activity is created, the get_queryset is not called and get_liked is not populated but owners can't like their own so it's always going to be False in that case
                if self.context['request'].method == 'POST':
                    return False
                if hasattr(obj, 'liked'):
                    return bool(obj.liked)
                if 'expand_liked_by' in self.context['request'].query_params:
                    for user in obj.liked_by:
                        if user.id == self.context['request'].user.id:
                            return True
                    return False
            return 'To know if the authenticated user liked this activity or not, use the parameter \"expand_liked\"'
        return None

    def get_website_url(self, obj):
        return 'http://schoolido.lu/activities/{}/'.format(obj.id)

    def validate(self, data):
        errors = {}
        new_data = {}
        request = self.context['request']
        if request.method == 'POST':
            new_data.update({
                'message': 'Custom',
                'message_type': models.ACTIVITY_TYPE_CUSTOM,
            })
            for required_field in ['account', 'message']:
                if required_field not in request.POST or not request.POST[required_field]:
                    errors[required_field] = ['This field is required']
            if 'account' in request.POST and 'account' not in errors:
                try:
                    new_data['account'] = models.Account.objects.get(pk=request.POST['account'], owner=request.user)
                except ObjectDoesNotExist:
                    errors['account'] = ['This account doesn\'t exist or isn\'t yours']
        if 'message' in request.data and 'message' not in errors:
            if self.instance and self.instance.message_type != models.ACTIVITY_TYPE_CUSTOM:
                errors['message'] = ['Editing the message of an activity that is not "Custom" is prohibited.']
            else:
                if len(request.data['message']) > settings.CUSTOM_ACTIVITY_MAX_LENGTH:
                    errors['message'] = ['Exceeds maximum length of {} characters (you have {})'.format(settings.CUSTOM_ACTIVITY_MAX_LENGTH, len(request.data['message']))]
                else:
                    new_data['message_data'] = request.data['message']
        if 'imgur_image' in request.data and request.data['imgur_image']:
            if not re.search(settings.IMGUR_REGEXP, request.data['imgur_image']):
                errors['imgur_image'] = ['Invalid imgur image URL. Format is: {}'.format(settings.IMGUR_REGEXP)]
            else:
                new_data['right_picture'] = get_imgur_code(request.data['imgur_image'])
        if errors:
            raise serializers.ValidationError(errors)
        if 'account' in new_data:
            new_data.update(activity_cacheaccount(new_data['account'], account_owner=request.user))
        return new_data

    class Meta:
        model = models.Activity
        fields = ('id', 'avatar', 'account', 'last_update', 'message', 'html_message', 'message_type', 'figure', 'liked_by', 'total_likes', 'liked', 'website_url')

class EventParticipationSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    def get_account(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('eventparticipation-'):
            if 'expand_account' in self.context['request'].query_params:
                serializer = AccountSerializer(obj.account, context=self.context)
                data = dict(serializer.data)
                data.update({
                    'owner_avatar': obj.account_picture,
                    'owner_status': obj.account_owner_status,
                })
                return data
        return {
            'id': obj.account_id,
            'text': obj.account_name,
            'language': obj.account_language,
            'website_url': 'http://schoolido.lu' + obj.account_link,
            'owner_avatar': obj.account_picture,
            'owner': obj.account_owner,
            'owner_status': obj.account_owner_status,
            'note': note_to_expand('account'),
        }

    def get_event(self, obj):
        if self.context['request'].resolver_match.url_name.startswith('eventparticipation-'):
            if 'expand_event' in self.context['request'].query_params:
                serializer = EventSerializer(obj.event, context=self.context)
                return serializer.data
            return note_to_expand("event")
        return None

    def validate(self, data):
        errors = {}
        request = self.context['request']
        if request.method == 'POST':
            try:
                data['event'] = models.Event.objects.get(japanese_name=request.POST['event'])
            except (ObjectDoesNotExist, KeyError):
                if 'event' not in request.POST:
                    errors['event'] = 'This field is required'
                else:
                    errors['event'] = 'Invalid event name'
            try:
                data['account'] = models.Account.objects.get(pk=request.POST['account'], owner=request.user)
            except (ObjectDoesNotExist, KeyError):
                if 'account' not in request.POST:
                    errors['account'] = 'This field is required'
                else:
                    errors['account'] = 'This account does\'t exist or isn\'t yours'
            if not errors:
                if ((data['account'].language == 'JP' and not data['event'].did_happen_japan())
                    or (data['account'].language != 'JP' and not data['event'].did_happen_world())):
                    errors['event'] = 'This event is not finished yet'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        request = self.context['request']
        if not self.instance:
            account = self.validated_data['account']
        else:
            account = self.instance.account
        if not self.instance:
            event = self.validated_data['event']
        else:
            event = self.instance.event

        if 'Score Match' in event.japanese_name or 'Medley Festival' in event.japanese_name or 'Challenge Festival' in event.japanese_name:
            kwargs['song_ranking'] = None
        if 'ranking' in self.validated_data and self.validated_data['ranking'] == 0: kwargs['ranking'] = None
        if 'points' in self.validated_data and self.validated_data['points'] == 0: kwargs['points'] = None
        if 'song_ranking' in self.validated_data and self.validated_data['song_ranking'] == 0: kwargs['song_ranking'] = None
        kwargs.update({
            'account_language': account.language,
            'account_link': '/user/' + request.user.username + '/#' + str(account.id),
            'account_picture': request.user.preferences.avatar(size=100),
            'account_name': unicode(account),
            'account_owner': request.user.username,
            'account_owner_status': request.user.preferences.status,
        })
        result = super(EventParticipationSerializer, self).save(**kwargs)
        return result

    class Meta:
        model = models.EventParticipation
        fields = ('id', 'event', 'account', 'ranking', 'song_ranking', 'points')

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        members = [None] * 9
        for member in obj.all_members:
            if member:
                members[member.position] = member.ownedcard
        serializer = OwnedCardSerializer(members, context=self.context, many=True)
        return [member if member['id'] is not None else None for member in serializer.data]

    def validate(self, data):
        errors = {}
        request = self.context['request']
        if request.method != 'POST' and 'owner_account' in data:
            del(data['owner_account'])
        if 'owner_account' in data and data['owner_account'].owner_id != request.user.id:
            errors['owner_account'] = 'This account isn\'t yours'
        if request.method == 'POST' or request.method == 'PATCH' or request.method == 'PUT':
            # Get the members to update
            members_to_update = []
            for position in range(1, 9):
                memberposition = 'member{}'.format(position)
                ownedcard = self.initial_data.get(memberposition, None)
                if ownedcard is not None:
                    if ownedcard == 'null':
                        members_to_update.append((position, memberposition, None))
                    else:
                        try:
                            members_to_update.append((position, memberposition, int(ownedcard)))
                        except ValueError:
                            errors[memberposition] = 'A valid integer is required.'
            # Check if members appear twice in parameters
            for member_to_update in members_to_update:
                similar_members = [m[1] for m in members_to_update if m[2] is not None and m[2] == member_to_update[2]]
                if len(similar_members) > 1:
                    for similar_member in similar_members:
                        errors[similar_member] = 'You can\'t have the same owned card twice in the same team.'
            # get the owned card objects
            self.members_to_update = []
            if not errors:
                ownedcards = models.OwnedCard.objects.filter(pk__in=[m[2] for m in members_to_update if m[2]], owner_account=(data['owner_account'] if request.method == 'POST' else self.instance.owner_account))
                for (position, memberposition, ownedcard) in members_to_update:
                    if ownedcard:
                        try:
                            self.members_to_update.append((position - 1, memberposition, (o for o in ownedcards if o.id == ownedcard).next()))
                        except StopIteration:
                            errors[memberposition] = 'This owned card does\'t exist or isn\'t yours'
                    else:
                        self.members_to_update.append((position - 1, memberposition, None))
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def save(self, **kwargs):
        request = self.context['request']
        result = super(TeamSerializer, self).save(**kwargs)
        if not hasattr(self.instance, 'all_members'):
            self.instance.all_members = []
        for (position, memberposition, ownedcard) in self.members_to_update:
            if ownedcard is None:
                models.Member.objects.filter(team=self.instance, position=position).delete()
                new_member = None
            else:
                existing_member = models.Member.objects.filter(team=self.instance, position=position)
                try:
                    updated = existing_member.update(ownedcard=ownedcard)
                    if updated:
                        new_member = existing_member[0]
                    else:
                        new_member = models.Member.objects.create(team=self.instance, ownedcard=ownedcard, position=position)
                        self.instance.all_members.append(new_member)
                        self.instance.all_members.sort(key=lambda m: m.position)
                except IntegrityError:
                    raise serializers.ValidationError({
                        memberposition: 'You can\'t have the same owned card twice in the same team.',
                    })
            self.instance.all_members = [member if member.position != position else new_member for member in self.instance.all_members]
        self.data['members'] = self.get_members(self.instance)
        return result

    class Meta:
        model = models.Team
        fields = ('id', 'name', 'owner_account', 'members')
