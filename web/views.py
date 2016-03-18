# -*- coding: utf-8 -*-
from __future__ import division
import math
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import password_reset_confirm as password_reset_confirm_view
from django.db.models import Count, Q, F
from django.db.models import Prefetch
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, string_concat
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.forms.util import ErrorList
from django.forms.models import model_to_dict
from api import models, raw
from web import forms, donations, transfer_code, raw as web_raw
from web.links import links as links_list
from web.templatetags.imageurl import ownedcardimageurl, eventimageurl
from utils import *
import urllib, hashlib
import datetime, time, pytz
import random
import re
import json
import collections
import operator

def contextAccounts(request, with_center=True):
    accounts = request.user.accounts_set.all().order_by('-rank')
    if with_center:
        accounts = accounts.select_related('center', 'center__card')
    return accounts

def globalContext(request):
    context ={
        'hide_back_button': False,
        'show_filter_button': False,
        'current_url': request.get_full_path() + ('?' if request.get_full_path()[-1] == '/' else '&'),
        'interfaceColor': 'default',
        'btnColor': 'Smile',
        'debug': settings.DEBUG,
        'hidenavbar': 'hidenavbar' in request.GET,
        'current_contests': settings.CURRENT_CONTESTS,
        'last_update': settings.GENERATED_DATE,
        'high_traffic': settings.HIGH_TRAFFIC,
    }
    if request.user.is_authenticated() and not request.user.is_anonymous():
        context['accounts'] = contextAccounts(request)
        if request.user.preferences.color:
            context['interfaceColor'] = request.user.preferences.color
            context['btnColor'] = request.user.preferences.color
    if 'notification' in request.GET:
        try:
            context['notification'] = web_raw.notifications[request.GET['notification']].copy()
            context['notification']['link'] = context['notification']['link'].format(*(request.GET['notification_link_variables'].split(',')))
        except KeyError: pass
    return context

def findAccount(id, accounts, forceGetAccount=False):
    try:
        id = int(id)
    except:
        return None
    for account in accounts:
        if account.id == id:
            return account
    if forceGetAccount:
        try: return models.Account.objects.get(id=id)
        except: return None
    return None

def findOwnedCard(id, ownedCards, forceGetOwnedCard=False):
    try:
        id = int(id)
    except:
        return None
    for ownedCard in ownedCards:
        if ownedCard.id == id:
            return ownedCard
    if forceGetOwnedCard:
        try: return models.OwnedCard.objects.get(id=id)
        except: return None
    return None

def hasJP(accounts):
    for account in accounts:
        if account.language == 'JP':
            return True
    return False

def onlyJP(context):
    if 'accounts' not in context:
        return False
    accounts = context['accounts']
    if not accounts:
        return False
    for account in accounts:
        if account.language != 'JP':
            return False
    return True

def getUserAvatar(user, size):
    return user.preferences.avatar(size)

def _pushActivity_cacheaccount(account, account_owner=None):
    if not account_owner:
        account_owner = account.owner
    return {
        'account_link': '/user/' + account_owner.username + '/#' + str(account.id),
        'account_picture': account_owner.preferences.avatar(size=100),
        'account_name': unicode(account),
    }

def pushActivity(message, number=None, ownedcard=None, eventparticipation=None, message_data=None, right_picture=None,
                 # Prefetch:
                 account=None, account_owner=None, card=None, event=None):
    """
    Will handle cache and duplicate depending on activity type (message).

    To avoid useless SQL queries, make sure your prefetch or specify the following:
    All:
    - account owner & preferences (or specify account owner with preferences)
    For ownedcard activities (added/idolized):
    - card (or specify card)
    - account (or specify account)
    Eventparticipation (for ranked in event):
    - account (or specify account)
    - event (or specify event)
    Rank up + Verified must specify:
    - account
    - number
    Trivia must specify:
    - number (= score)
    - message_data (= sentence)
    Custom must specify:
    - account
    - message_data
    - (optional) right_picture
    """
    if ownedcard is not None:
        if ownedcard.card.rarity == 'R' or ownedcard.card.rarity == 'N':
            return
    if eventparticipation is not None and not eventparticipation.ranking:
        return
    if message == 'Added a card' or message == 'Idolized a card' or message == 'Update card':
        if not account:
            account = ownedcard.owner_account
        if not card:
            card = ownedcard.card
        defaults = {
            'account': account,
            'eventparticipation': None,
            'message': message,
            'number': None,
            'message_data': concat_args(unicode(card), ownedcard.stored),
            'right_picture_link': '/cards/' + str(card.id) + '/',
            'right_picture': ownedcardimageurl({}, ownedcard),
        }
        defaults.update(_pushActivity_cacheaccount(account, account_owner))
        if message == 'Added a card':
            models.Activity.objects.create(ownedcard=ownedcard, **defaults)
        else:
            if message == 'Update card':
                del(defaults['message'])
            updated = models.Activity.objects.filter(ownedcard=ownedcard).update(**defaults)
            if not updated:
                models.Activity.objects.create(ownedcard=ownedcard, message='Added a card', **defaults)
    elif message == 'Rank Up' or message == 'Verified':
        defaults = {
            'account': account,
            'message': message,
            'message_data': concat_args(number) if message == 'Rank Up' else models.VERIFIED_DICT[number],
            'number': number,
        }
        defaults.update(_pushActivity_cacheaccount(account, account_owner))
        models.Activity.objects.update_or_create(account=account, message=message, number=number, defaults=defaults)
    elif message == 'Ranked in event':
        if not account:
            account = eventparticipation.account
        if not event:
            event = eventparticipation.event
        defaults = {
            'account': account,
            'ownedcard': None,
            'eventparticipation': eventparticipation,
            'message': message,
            'number': None,
            'message_data': concat_args(eventparticipation.ranking, unicode(event)),
            'right_picture': eventimageurl({}, event, english=(account.language != 'JP')),
            'right_picture_link': '/events/' + event.japanese_name + '/',
        }
        defaults.update(_pushActivity_cacheaccount(account, account_owner))
        models.Activity.objects.update_or_create(eventparticipation=eventparticipation, defaults=defaults)
    elif message == 'Trivia':
        defaults = {
            'account': account,
            'message': message,
            'number': number,
            'message_data': concat_args(number, message_data),
        }
        defaults.update(_pushActivity_cacheaccount(account, account_owner))
        activity = models.Activity.objects.create(**defaults)
        return activity
    elif message == 'Custom':
        defaults = {
            'account': account,
            'message': message,
            'message_data': message_data,
            'right_picture': right_picture,
        }
        defaults.update(_pushActivity_cacheaccount(account, account_owner))
        models.Activity.objects.create(**defaults)

def index(request):
    context = globalContext(request)

    # Get current events
    try:
        context['current_jp'] = models.Event.objects.order_by('-beginning')[0]
        context['current_jp'].is_current = context['current_jp'].is_japan_current()
        context['current_jp'].slide_position = len(contest['current_contests']) + 1
    except: pass
    try:
        context['current_en'] = models.Event.objects.filter(english_beginning__isnull=False).order_by('-english_beginning')[0]
        context['current_en'].is_current = context['current_en'].is_world_current()
        context['current_en'].slide_position = len(contest['current_contests'])
    except: pass
    context['trivia_slide_position'] = len(context['current_contests']) + 2
    context['total_donators'] = settings.TOTAL_DONATORS

    context['total_backgrounds'] = settings.TOTAL_BACKGROUNDS

    # Get random character
    context['character'] = None
    if not context['character'] and request.user.is_authenticated() and context['accounts'] and bool(random.getrandbits(1)):
        random_account = random.choice(context['accounts'])
        if random_account.center:
            context['character'] = random_account.center.card.transparent_idolized_image if random_account.center.idolized or random_account.center.card.is_special else random_account.center.card.transparent_image
    if not context['character']:
        card = models.Card.objects.filter(transparent_idolized_image__isnull=False).exclude(transparent_idolized_image='').order_by('?')
        if request.user.is_authenticated() and request.user.preferences.best_girl:
            card = card.filter(name=request.user.preferences.best_girl)
        else:
            card = card.filter(idol__main=True)
        if card:
            card = card[0]
            context['character'] = card.transparent_idolized_image
            if card.transparent_image and bool(random.getrandbits(1)):
                context['character'] = card.transparent_image

    return render(request, 'index.html', context)

def links(request):
    context = globalContext(request)
    context['links'] = links_list

    query = 'SELECT f.id, f.transparent_idolized_image, f.name FROM (SELECT card.id, card.transparent_idolized_image, idol.name FROM api_card AS card JOIN api_idol AS idol WHERE card.idol_id = idol.id AND idol.main = 1 AND card.transparent_idolized_image IS NOT NULL AND card.transparent_idolized_image != \'\' ORDER BY ' + (settings.RANDOM_ORDERING_DATABASE) + '()) AS f GROUP BY f.name'
    cards_objects = models.Card.objects.raw(query)
    cards = {}
    for card in cards_objects:
        cards[card.name] = card
    context['cards'] = cards
    return render(request, 'links.html', context)

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    accounts_with_transfer_code = 0
    if user is not None:
        accounts_with_transfer_code = user.accounts_set.exclude(transfer_code__isnull=True).exclude(transfer_code__exact='').count()

    response = password_reset_confirm_view(request, uidb64=uidb64, token=token, extra_context={'accounts_with_transfer_code': accounts_with_transfer_code})
    if isinstance(response, HttpResponseRedirect) and user is not None:
        accounts_with_transfer_code = user.accounts_set.all().update(transfer_code='')
    return response

def create(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            preferences = models.UserPreferences.objects.create(user=user)
            login(request, user)
            return redirect('/addaccount/')
    else:
        form = forms.CreateUserForm()
    context = globalContext(request)
    context['form'] = form
    context['current'] = 'create'
    return render(request, 'create.html', context)

def login_custom_view(request):
    response = login_view(request, template_name='login.html', extra_context={'interfaceColor': 'default'})
    if (isinstance(response, HttpResponseRedirect) and 'password' in request.POST
        and request.user.is_authenticated() and not request.user.is_anonymous()):
        accounts = request.user.accounts_set.all()
        for account in accounts:
            if account.transfer_code and not transfer_code.is_encrypted(account.transfer_code):
                account.transfer_code = transfer_code.encrypt(account.transfer_code, request.POST['password'])
                account.save()
    return response

def setaccountonlogin(request):
    context = globalContext(request)
    try:
        account = next(iter(context['accounts']))
    except StopIteration:
        return redirect('addaccount')
    return redirect('cards')

def cards(request, card=None, ajax=False):
    if len(request.GET.getlist('page')) > 1:
        raise PermissionDenied()

    page = 0
    context = globalContext(request)
    context['total_results'] = 0

    if len(request.GET) == 1 and 'name' in request.GET:
        return redirect('/idol/' + request.GET['name'] + '/')

    cardsinfo = settings.CARDS_INFO
    max_stats = cardsinfo['max_stats']

    # Set defaults
    request_get = {
        'ordering': 'id',
        'reverse_order': True,
    }

    if card is None:
        # Apply filters
        cards = models.Card.objects.filter()
        if 'search' in request.GET:
            request_get['search'] = request.GET['search']
            if request.GET['search']:
                cards = cards.filter(Q(name__icontains=request.GET['search'])
                                     | Q(idol__japanese_name__icontains=request.GET['search'])
                                     | Q(skill__icontains=request.GET['search'])
                                     | Q(japanese_skill__icontains=request.GET['search'])
                                     | Q(skill_details__icontains=request.GET['search'])
                                     | Q(japanese_skill_details__icontains=request.GET['search'])
                                     | Q(center_skill__icontains=request.GET['search'])
                                     | Q(japanese_collection__icontains=request.GET['search'])
                                     | Q(translated_collection__icontains=request.GET['search'])
                                     | Q(promo_item__icontains=request.GET['search'])
                                     | Q(event__english_name__icontains=request.GET['search'])
                                     | Q(event__japanese_name__icontains=request.GET['search'])
                )
        if 'name' in request.GET and request.GET['name']:
            cards = cards.filter(name__exact=request.GET['name'])
            request_get['name'] = request.GET['name']
        if 'collection' in request.GET and request.GET['collection']:
            cards = cards.filter(japanese_collection__exact=request.GET['collection'])
            request_get['collection'] = request.GET['collection']
        if 'translated_collection' in request.GET and request.GET['translated_collection']:
            cards = cards.filter(translated_collection__exact=request.GET['translated_collection'])
            request_get['translated_collection'] = request.GET['translated_collection']
        if 'sub_unit' in request.GET and request.GET['sub_unit']:
            cards = cards.filter(idol__sub_unit__exact=request.GET['sub_unit'])
            request_get['sub_unit'] = request.GET['sub_unit']
        if 'idol_year' in request.GET and request.GET['idol_year']:
            cards = cards.filter(idol__year__exact=request.GET['idol_year'])
            request_get['idol_year'] = request.GET['idol_year']
        if 'idol_school' in request.GET and request.GET['idol_school']:
            cards = cards.filter(idol__school__exact=request.GET['idol_school'])
            request_get['idol_school'] = request.GET['idol_school']
        if 'rarity' in request.GET and request.GET['rarity']:
            cards = cards.filter(rarity__exact=request.GET['rarity'])
            request_get['rarity'] = request.GET['rarity']
        if 'attribute' in request.GET and request.GET['attribute']:
            cards = cards.filter(attribute__exact=request.GET['attribute'])
            request_get['attribute'] = request.GET['attribute']
        if 'skill' in request.GET and request.GET['skill']:
            cards = cards.filter(skill__exact=request.GET['skill'])
            request_get['skill'] = request.GET['skill']

        if 'ids' in request.GET and request.GET['ids']:
            cards= cards.filter(pk__in=request.GET['ids'].split(','))

        if 'is_event' in request.GET and request.GET['is_event'] == 'on':
            cards = cards.filter(event__isnull=False)
            request_get['is_event'] = 'on'
        elif 'is_event' in request.GET and request.GET['is_event'] == 'off':
            cards = cards.filter(event__isnull=True)
            request_get['is_event'] = 'off'

        if 'is_special' in request.GET and request.GET['is_special'] == 'on':
            cards = cards.filter(is_special__exact=True)
            request_get['is_special'] = 'on'
        elif 'is_special' in request.GET and request.GET['is_special'] == 'off':
            cards = cards.filter(is_special__exact=False)
            request_get['is_special'] = 'off'
        if 'release_after' in request.GET and request.GET['release_after']:
            cards = cards.filter(release_date__gte=datetime.datetime.strptime(request.GET['release_after'] + '-01', "%Y-%m-%d"))
            request_get['release_after'] = request.GET['release_after']
        if 'release_before' in request.GET and request.GET['release_before']:
            cards = cards.filter(release_date__lte=datetime.datetime.strptime(request.GET['release_before'] + '-01', "%Y-%m-%d"))
            request_get['release_before'] = request.GET['release_before']

        if 'account' in request.GET and request.GET['account'] and request.user.is_authenticated() and not request.user.is_anonymous():
            account = findAccount(request.GET['account'], context['accounts'], forceGetAccount=request.user.is_staff)
            if account:
                request_get['account'] = account.id
                if 'max_level' in request.GET and request.GET['max_level'] == '1':
                    cards = cards.filter(id__in=models.OwnedCard.objects.filter(owner_account=account, max_level=True).values('card'))
                    request_get['max_level'] = '1'
                elif 'max_level' in request.GET and request.GET['max_level'] == '-1':
                    cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=account, max_level=True).values('card'))
                    request_get['max_level'] = '-1'
                if 'max_bond' in request.GET and request.GET['max_bond'] == '1':
                    cards = cards.filter(id__in=models.OwnedCard.objects.filter(owner_account=account, max_bond=True).values('card'))
                    request_get['max_bond'] = '1'
                elif 'max_bond' in request.GET and request.GET['max_bond'] == '-1':
                    cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=account, max_bond=True).values('card'))
                    request_get['max_bond'] = '-1'
                if 'idolized' in request.GET and request.GET['idolized'] == '1':
                    cards = cards.filter(id__in=models.OwnedCard.objects.filter(owner_account=account, idolized=True).values('card'))
                    request_get['idolized'] = '1'
                elif 'idolized' in request.GET and request.GET['idolized'] == '-1':
                    cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=account, idolized=True).values('card'))
                    request_get['idolized'] = '-1'

                if 'stored' in request.GET and request.GET['stored']:
                    if request.GET['stored'] == 'Album':
                        cards = cards.filter(ownedcards__owner_account=account).filter(Q(ownedcards__stored='Deck') | Q(ownedcards__stored='Album'))
                    else:
                        cards = cards.filter(ownedcards__owner_account=account, ownedcards__stored=request.GET['stored'])
                    cards = cards.distinct()
                    request_get['stored'] = request.GET['stored']

        if ('accounts' in context and not hasJP(context['accounts'])
            and 'search' not in request.GET or 'is_world' in request.GET and request.GET['is_world']):
            if 'is_world' in request.GET and request.GET['is_world'] == 'off':
                cards = cards.filter(japan_only=True)
            else:
                cards = cards.filter(japan_only=False)
                context['show_discover_banner'] = True
            request_get['is_world'] = True

        if ('accounts' in context and not hasJP(context['accounts'])
            and 'search' not in request.GET or 'is_promo' in request.GET and request.GET['is_promo']):
            if 'is_promo' not in request.GET or request.GET['is_promo'] == 'off':
                cards = cards.filter(is_promo=False)
                request_get['is_promo'] = 'off'
            else:
                cards = cards.filter(is_promo=True)
                request_get['is_promo'] = 'on'

        if 'ordering' in request.GET and request.GET['ordering']:
            request_get['ordering'] = request.GET['ordering']
            request_get['reverse_order'] = 'reverse_order' in request.GET and request.GET['reverse_order']
        prefix = '-' if request_get['reverse_order'] else ''
        cards = cards.order_by(prefix + request_get['ordering'], prefix +'id')

        context['total_results'] = cards.count()
        # Set limit
        page_size = 9
        if 'page' in request.GET and request.GET['page']:
            page = int(request.GET['page']) - 1
            if page < 0:
                page = 0
        cards = cards[(page * page_size):((page * page_size) + page_size)]
        context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    else:
        context['total_results'] = 1
        cards = models.Card.objects.filter(pk=int(card))
        context['single'] = cards[0]

    cards = cards.select_related('event', 'idol')
    if request.user.is_authenticated() and not request.user.is_anonymous():
        cards = cards.prefetch_related(Prefetch('ownedcards', queryset=models.OwnedCard.objects.filter(owner_account__owner=request.user).order_by('owner_account__language'), to_attr='owned_cards'))

    # Get statistics & other information to show in cards
    for card in cards:
        if card.video_story:
            card.embed_video = card.video_story.replace('/watch?v=', '/embed/')
        if card.japanese_video_story:
            card.embed_japanese_video = card.japanese_video_story.replace('/watch?v=', '/embed/')
        card.percent_stats = {
            'minimum': {
                'Smile': ((card.minimum_statistics_smile if card.minimum_statistics_smile else 0) / max_stats['Smile']) * 100,
                'Pure': ((card.minimum_statistics_pure if card.minimum_statistics_pure else 0) / max_stats['Pure']) * 100,
                'Cool': ((card.minimum_statistics_cool if card.minimum_statistics_cool else 0) / max_stats['Cool']) * 100,
            }, 'non_idolized_maximum': {
                'Smile': ((card.non_idolized_maximum_statistics_smile if card.non_idolized_maximum_statistics_smile else 0) / max_stats['Smile']) * 100,
                'Pure': ((card.non_idolized_maximum_statistics_pure if card.non_idolized_maximum_statistics_pure else 0) / max_stats['Pure']) * 100,
                'Cool': ((card.non_idolized_maximum_statistics_cool if card.non_idolized_maximum_statistics_cool else 0) / max_stats['Cool']) * 100,
            }, 'idolized_maximum': {
                'Smile': ((card.idolized_maximum_statistics_smile if card.idolized_maximum_statistics_smile else 0) / max_stats['Smile']) * 100,
                'Pure': ((card.idolized_maximum_statistics_pure if card.idolized_maximum_statistics_pure else 0) / max_stats['Pure']) * 100,
                'Cool': ((card.idolized_maximum_statistics_cool if card.idolized_maximum_statistics_cool else 0) / max_stats['Cool']) * 100,
            }
        }
        sentence, data = card.get_center_skill_details()
        if sentence and data:
            card.center_skill_details = _(sentence).format(*[_(d) for d in data])
        if card.center_skill:
            try:
                card.center_skill = string_concat(_(card.center_skill.split(' ')[0]), ' ', _(card.center_skill.split(' ')[1]))
            except: pass

    if not ajax:
       # Get filters info for the form
        context['filters'] = {
            'idols': forms.getGirls(with_total=True, with_japanese_name=request.LANGUAGE_CODE == 'ja'),
            'collections': cardsinfo['collections'],
            'translated_collections': cardsinfo['translated_collections'],
            'sub_units': cardsinfo['sub_units'] if 'sub_units' in cardsinfo else [],
            'skills': cardsinfo['skills'],
            'rarity_choices': models.RARITY_CHOICES,
            'attribute_choices': models.ATTRIBUTE_CHOICES,
            'idol_year_choices': cardsinfo['years'] if 'years' in cardsinfo else [],
            'idol_school_choices': cardsinfo['schools'] if 'schools' in cardsinfo else [],
            'stored_choices': models.STORED_CHOICES,
            'ordering_choices': (
                ('id', _('Card #ID')),
                ('release_date', _('Release date')),
                ('name', _('Idol')),
                ('idolized_maximum_statistics_smile', _('Smile\'s statistics')),
                ('idolized_maximum_statistics_pure', _('Pure\'s statistics')),
                ('idolized_maximum_statistics_cool', _('Cool\'s statistics')),
                ('total_owners', string_concat(_('Most popular'), ' (', _('Deck'), ')')),
                ('total_wishlist', string_concat(_('Most popular'), ' (', _('Wish List'), ')')),
                ('hp', _('HP'))
            )
        }

    context['total_cards'] = len(cards)
    if context['total_cards'] > 0:
        context['idol'] = cards[0].idol
    context['cards'] = enumerate(cards)
    context['max_stats'] = max_stats
    context['show_filter_button'] = False if 'single' in context and context['single'] else True
    context['request_get'] = request_get
    context['show_filter_bar'] = context['show_filter_button']
    context['show_total_results'] = 'search' in request_get
    if 'search' not in request_get and 'name' in request_get:
        context['show_filter_bar'] = False
    context['current'] = 'cards'
    if request.user.is_authenticated() and not request.user.is_anonymous():
        context['quickaddcard_form'] = forms.getOwnedCardForm(forms.QuickOwnedCardForm(), context['accounts'])
    context['page'] = page + 1
    context['ajax'] = ajax
    if ajax:
        return render(request, 'cardsPage.html', context)
    return render(request, 'cards.html', context)

idol_tabs = ['idol', 'pictures']

def idol(request, idol):
    context = globalContext(request)
    context['tab'] = 'idol'
    if 'tab' in request.GET and request.GET['tab'] in idol_tabs:
        context['tab'] = request.GET['tab']
    context['idol'] = get_object_or_404(models.Idol, name=idol)
    if context['tab'] == 'pictures':
        context['idol'].tag = idol.lower().replace(' ', '_')
    return render(request, 'idol.html', context)

def _addaccount_savecenter(account):
    if account.starter:
        center = models.OwnedCard.objects.create(card=account.starter, owner_account=account, stored='Deck')
        account.center = center
        account.save()

def addaccount(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            if account.rank >= 200:
                account.rank = 195
                account.save()
                _addaccount_savecenter(account)
                return redirect('/cards/?notification=ADDACCOUNTRANK200&notification_link_variables=' + str(account.pk))
            account.save()
            _addaccount_savecenter(account)
            return redirect('/cards/#tutorialaddcardModal')
    else:
        form = forms.AccountForm(initial={
            'nickname': request.user.username
        })
    context = globalContext(request)
    context['form'] = form
    context['current'] = 'addaccount'
    return render(request, 'addaccount.html', context)

def addteam(request, account):
    """
    SQL Queries
    - Context
    - Owned cards (JOIN + card)
    """
    context = globalContext(request)
    account = findAccount(account, context['accounts'])
    if not account:
        raise Http404
    account.deck = account.ownedcards.filter(stored='Deck').select_related('card').order_by('-card__rarity', '-idolized', '-card__attribute', '-card__id')
    if request.method == 'POST':
        form = forms.TeamForm(request.POST, account=account)
        if form.is_valid():
            team = models.Team.objects.create(name=form.cleaned_data['name'], owner_account=account)
            for i in range(9):
                if form.cleaned_data['card' + str(i)] is not None:
                    models.Member.objects.create(team=team, ownedcard=findOwnedCard(form.cleaned_data['card' + str(i)], account.deck), position=i)
            return redirect('/user/' + request.user.username + '/?show' + str(account.id) + '=teams#team' + str(team.id))
    else:
        form = forms.TeamForm(account=account)
    context['account'] = account
    context['form'] = form
    return render(request, 'addteam.html', context)

def editteam(request, team):
    """
    SQL Queries
    - Context
    - Owned cards (JOIN + card)
    """
    context = globalContext(request)
    team = get_object_or_404(models.Team.objects.filter(owner_account__owner=request.user).select_related('owner_account').prefetch_related(Prefetch('members', queryset=models.Member.objects.select_related('ownedcard', 'ownedcard__card').order_by('position'), to_attr='all_members')), pk=team)
    account = team.owner_account
    account.deck = account.ownedcards.filter(stored='Deck').select_related('card').order_by('-card__rarity', '-idolized', '-card__attribute', '-card__id')
    context['form_delete'] = forms.ConfirmDelete(initial={'thing_to_delete': team.id})
    if request.method == 'POST':
        if 'thing_to_delete' in request.POST:
            form = forms.TeamForm(instance=team, account=account)
            context['form_delete'] = forms.ConfirmDelete(request.POST)
            if context['form_delete'].is_valid():
                team.delete()
                return redirect('/user/' + request.user.username + '/?show' + str(account.id) + '=teams')
        else:
            old_name = team.name
            form = forms.TeamForm(request.POST, instance=team, account=account)
            if form.is_valid():
                if form.cleaned_data['name'] != old_name:
                    team.name = form.cleaned_data['name']
                    team.save()
                for i in range(9):
                    if form.cleaned_data['card' + str(i)] is not None:
                        models.Member.objects.update_or_create(team=team, position=i, defaults={
                            'ownedcard': findOwnedCard(form.cleaned_data['card' + str(i)], account.deck),
                        })
                return redirect('/user/' + request.user.username + '/?show' + str(account.id) + '=teams#team' + str(team.id))
    else:
        form = forms.TeamForm(instance=team, account=account)
    context['account'] = account
    context['form'] = form
    context['team'] = team
    return render(request, 'addteam.html', context)

def profile(request, username):
    """
    SQL Queries
    - Django session
    - Request user
    - (if me) Preferences
    - (if not me) User (JOIN + preferences)
    - Accounts (JOIN + center + center card + starter)
    - Deck stats (number of UR/SR in each account, raw SQL query)
    - Account queries (see ajaxaccounttab)
    - User links
    - (if not me) Is following?
    - Count followers
    - Count following
    """
    context = globalContext(request)
    if request.user.is_authenticated() and not request.user.is_anonymous() and request.user.username == username:
        user = request.user
    else:
        user = get_object_or_404(User.objects.select_related('preferences'), username=username)
    context['profile_user'] = user
    context['preferences'] = user.preferences
    if request.user.is_staff and (request.user.is_superuser or request.user.preferences.allowed_verifications):
        if request.user.is_superuser:
            context['form_preferences'] = forms.UserProfileStaffForm(instance=context['preferences'])
        if 'staff' in request.GET:
            context['show_staff'] = True
        if request.method == 'POST':
            if 'editPreferences' in request.POST and request.user.is_superuser:
                form_preferences = forms.UserProfileStaffForm(request.POST, instance=context['preferences'])
                if form_preferences.is_valid():
                    prefs = form_preferences.save()
                    return redirect('/user/' + context['profile_user'].username + '?staff')
            if 'addcard' in request.POST:
                form_addcard = forms.StaffAddCardForm(request.POST)
                if form_addcard.is_valid():
                    form_addcard.save()
                    return redirect('/user/' + context['profile_user'].username + '?staff#' + str(form_addcard.cleaned_data['owner_account']))
    if user == request.user:
        # force execute queryset
        [_ for account in context['accounts']]
        context['is_me'] = True
        context['user_accounts'] = context['accounts']
    else:
        context['is_me'] = False
        context['user_accounts'] = user.accounts_set.all().order_by('-rank')

    if request.user.is_staff and 'staff' in request.GET:
        deck_queryset = models.OwnedCard.objects.filter(Q(stored='Deck') | Q(stored='Album'))
    else:
        deck_queryset = models.OwnedCard.objects.filter(stored='Deck')
    context['user_accounts'] = context['user_accounts'].select_related('center', 'center__card', 'starter')

    if not context['preferences'].private or context['is_me']:
        # Get stats of cards
        accounts_ids = ','.join([str(account.id) for account in context['user_accounts']])
        if accounts_ids:
            cursor = connection.cursor()
            query = 'SELECT c.rarity, o.owner_account_id, COUNT(c.rarity) FROM api_ownedcard AS o JOIN api_card AS c WHERE o.card_id=c.id AND o.owner_account_id IN (' + accounts_ids + ') AND o.stored=\'Deck\' GROUP BY c.rarity, o.owner_account_id'
            cursor.execute(query)
            deck_stats = cursor.fetchall()
        for account in context['user_accounts']:
            # Set stats
            try: account.deck_total_sr = (s[2] for s in deck_stats if s[0] == 'SR' and s[1] == account.id).next()
            except StopIteration: account.deck_total_sr = 0
            try: account.deck_total_ur = (s[2] for s in deck_stats if s[0] == 'UR' and s[1] == account.id).next()
            except StopIteration: account.deck_total_ur = 0
            account.deck_total = sum([s[2] for s in deck_stats if s[1] == account.id])
            # Get opened tab
            if 'show' + str(account.id) in request.GET and request.GET['show' + str(account.id)] in models.ACCOUNT_TAB_DICT:
                account.opened_tab = request.GET['show' + str(account.id)]
            elif request.user.is_staff and 'staff' in request.GET:
                account.opened_tab = 'deck'
            else:
                account.opened_tab = account.default_tab
            # Get data of account depending on opened tab
            account.owner = user
            _context = _ajaxaccounttab_functions[account.opened_tab](account.opened_tab, request, account, more=False)
            if account.opened_tab == 'deck':
                account.total_cards = account.deck_total
            if 'account' in _context:
                account = _context['account']

            if context['is_me']:
                # Form to post custom activity
                if request.method == 'POST' and 'account_id' in request.POST and request.POST['account_id'] == str(account.id):
                    account.form_custom_activity = forms.CustomActivity(request.POST)
                    if account.form_custom_activity.is_valid():
                        imgur = None
                        if account.form_custom_activity.cleaned_data['right_picture']:
                            imgur = get_imgur_code(account.form_custom_activity.cleaned_data['right_picture'])
                        pushActivity('Custom', account=account,
                                     message_data=account.form_custom_activity.cleaned_data['message_data'],
                                     right_picture=imgur,
                                     # prefetch:
                                     account_owner=request.user)
                        context['posted_activity'] = True
                        account.form_custom_activity = forms.CustomActivity(initial={'account_id': account.id})
                else:
                    account.form_custom_activity = forms.CustomActivity(initial={'account_id': account.id})
            # Staff form to edit account
            if request.user.is_staff and (request.user.is_superuser or request.user.preferences.allowed_verifications):
                staffFormClass = forms.AccountAdminForm if request.user.is_superuser else forms.AccountStaffForm
                account.staff_form_addcard = forms.StaffAddCardForm(initial={'owner_account': account.id})
                account.staff_form = staffFormClass(instance=account)
                account.staff_form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=account, stored='Deck').order_by('card__id').select_related('card')
                if request.method == 'POST' and ('editAccount' + str(account.id)) in request.POST:
                    account.staff_form = staffFormClass(request.POST, instance=account)
                    if account.staff_form.is_valid():
                        account = account.staff_form.save(commit=False)
                        if request.user.is_superuser and 'owner_id' in account.staff_form.cleaned_data and account.staff_form.cleaned_data['owner_id']:
                            account_new_user = models.User.objects.get(pk=account.staff_form.cleaned_data['owner_id'])
                            account.owner = account_new_user
                        account.save()
                        return redirect('/user/' + context['profile_user'].username + '?staff#' + str(account.id))
    # Set links
    context['links'] = list(context['profile_user'].links.all().values())
    preferences = context['preferences']
    if preferences.birthdate:
        context['links'].insert(0, {
            'type': 'Birthdate',
            'value': string_concat(unicode(preferences.birthdate), ' (', str(preferences.age), ' ', _('years old'), ')'),
            'flaticon': 'event',
            'translate_type': True,
        })
    if preferences.location:
        context['links'].insert(0, {
            'type': 'Location',
            'value': preferences.location,
            'translate_type': True,
            'flaticon': 'world',
        })
    if preferences.best_girl:
        context['links'].insert(0, {
            'type': 'Best Girl',
            'value': preferences.best_girl,
            'translate_type': True,
            'div': '<div class="chibibestgirl" style="background-image: url(' + chibiimage(preferences.best_girl) + ')"></div>',
        })
    context['per_line'] = 6
    if (len(context['links']) % context['per_line']) < 4:
        context['per_line'] = 4

    context['accounts_tabs'] = models.ACCOUNT_TAB_ICONS
    context['current'] = 'profile'
    if not context['is_me']:
        context['following'] = isFollowing(user, request)
    context['total_following'] = context['preferences'].following.count()
    context['total_followers'] = user.followers.count()
    context['imgurClientID'] = settings.IMGUR_CLIENT_ID
    context['cards_limit'] = settings.CARDS_LIMIT
    if context['is_me']:
        context['deck_links'] = web_raw.deck_links
    return render(request, 'profile.html', context)

def _ajaxaccounttab_ownedcards(tab, request, account, more):
    """
    SQL Queries
    - Django session
    - Request user
    - Account (JOIN + owner + owner preferences)
    - Owned cards (JOIN + card)
    """
    context = {}
    context['is_me'] = False
    if 'staff' in request.GET:
        context['show_staff'] = True
    if account.owner == request.user:
        context['is_me'] = True
    if tab == 'deck' and context['is_me']:
        context['deck_links'] = web_raw.deck_links
    if account.owner.username != request.user.username and (account.owner.preferences.private or tab == 'presentbox'):
        raise PermissionDenied()
    ownedcards = account.ownedcards.filter(owner_account=account).select_related('card')
    account.total_cards = None
    if tab == 'album':
        account.album = ownedcards.filter(Q(stored='Album') | Q(stored='Deck')).order_by('card__id')
        if more:
            account.album = account.album.filter(card__id__gt=settings.CARDS_LIMIT)
        else:
            account.album = account.album.filter(card__id__lte=settings.CARDS_LIMIT)
        album = range(1, settings.CARDS_INFO['total_cards'] + 1) if account.language == 'JP' else settings.CARDS_INFO['en_cards'][:]
        account.total_cards = len(album) - settings.CARDS_LIMIT
        for owned_card in account.album:
            try: album[owned_card.card.id - 1] = owned_card
            except IndexError: pass
        if more:
            account.album = album[settings.CARDS_LIMIT:]
        else:
            account.album = album[:settings.CARDS_LIMIT]
    elif tab == 'deck':
        account.deck = ownedcards.filter(stored='Deck').order_by('-card__rarity', '-idolized', '-card__attribute', '-card__id')
        if more:
            account.deck = account.deck[settings.CARDS_LIMIT:]
        else:
            account.deck = account.deck[:settings.CARDS_LIMIT]
    elif tab == 'wishlist':
        account.wishlist = ownedcards.filter(stored='Favorite').order_by('-card__rarity', '-idolized', 'card__id')
        account.total_cards = account.wishlist.count()
        if more:
            account.wishlist = account.wishlist[settings.CARDS_LIMIT:]
        else:
            account.wishlist = account.wishlist[:settings.CARDS_LIMIT]
    elif tab == 'presentbox':
        account.presentbox = ownedcards.filter(stored='Box').order_by('card__id')
        account.total_cards = account.presentbox.count()
        if more:
            account.presentbox = account.presentbox[settings.CARDS_LIMIT:]
        else:
            account.presentbox = account.presentbox[:settings.CARDS_LIMIT]
    context['account'] = account
    context['cards_limit'] = settings.CARDS_LIMIT
    context['more'] = more
    return context

def _ajaxaccounttab_eventparticipations(tab, request, account, more):
    """
    SQL Queries
    - Django session
    - Request user
    - Account (JOIN + owner + owner preferences)
    - Event participations (JOIN + event)
    """
    context = {}
    account.eventparticipations = models.EventParticipation.objects.filter(account=account).order_by('-event__end').select_related('event')
    context['account'] = account
    return context

def _ajaxaccounttab_teams(tab, request, account, more):
    context = {}
    if account.owner == request.user:
        context['is_me'] = True
    teams = models.Team.objects.filter(owner_account=account).prefetch_related(Prefetch('members', queryset=models.Member.objects.select_related('ownedcard', 'ownedcard__card').order_by('position'), to_attr='all_members'))
    range_aligners = [0,1,2,3,4,3,2,1,0]
    for team in teams:
        team.owner_account = account
        members = [{'position': i, 'virtual': True, 'range_align': range(range_aligners[i])} for i in range(9)]
        for member in team.all_members:
            member.range_align = members[member.position]['range_align']
            members[member.position] = member
        team.all_members = members
    account.all_teams = teams
    context['account'] = account
    return context

_ajaxaccounttab_functions = {
    'deck': _ajaxaccounttab_ownedcards,
    'album': _ajaxaccounttab_ownedcards,
    'teams': _ajaxaccounttab_teams,
    'events': _ajaxaccounttab_eventparticipations,
    'wishlist': _ajaxaccounttab_ownedcards,
    'presentbox': _ajaxaccounttab_ownedcards,
}

def ajaxaccounttab(request, account, tab, more=False):
    account = get_object_or_404(models.Account.objects.select_related('owner', 'owner__preferences'), pk=account)
    try:
        context = _ajaxaccounttab_functions[tab](tab, request, account, more)
    except KeyError:
        raise Http404
    return render(request, 'include/account_tab_' + tab + '.html', context)

def ajaxaddcard(request):
    """
    SQL Queries
    - Django session
    - Request user
    - Account (JOIN + center + center card)
    - Card
    - Insert owned card
    - Preferences
    - (if SR/UR) Insert activity
    """
    if request.method != 'POST' or not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    account = get_object_or_404(models.Account.objects.select_related('center', 'center__card'), pk=request.POST['owner_account'], owner=request.user)
    card = get_object_or_404(models.Card, pk=request.POST['card'])
    ownedcard = models.OwnedCard(card=card,
                                 owner_account=account,
                                 stored='Deck',
                                 skill=1,
                                 idolized=card.is_promo)
    ownedcard.save()
    if not settings.HIGH_TRAFFIC:
        pushActivity(message="Added a card",
                     ownedcard=ownedcard,
                     # prefetch:
                     card=card,
                     account=account,
                     account_owner=request.user)
    context = {
        'owned': ownedcard,
        'owner_account': account,
        'withcenter': True,
    }
    return render(request, 'ownedCardOnBottomCard.html', context)

def ajaxeditcard(request, ownedcard):
    """
    SQL Queries
    - Get form:
    -- Django session
    -- Request user
    -- Owned card (JOIN + account + card)
    -- Accounts
    - Save edited card:
    -- Django session
    -- Request user
    -- Owned card (JOIN + account + card + account center + account center card)
    -- (if account changed) Account (JOIN + center + center card)
    -- Update owned card
    -- User preferences
    -- Activity
    -- Update or Create activity
    """
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = {
        'accounts': contextAccounts(request, with_center=False),
    }
    # Get existing owned card
    try:
        model_owned_card = models.OwnedCard.objects.select_related('card', 'owner_account')
        if request.method == 'POST':
            model_owned_card = model_owned_card.select_related('owner_account__center', 'owner_account__center__card')
        owned_card = model_owned_card.get(pk=int(ownedcard), owner_account__owner=request.user)
    except ObjectDoesNotExist:
        raise PermissionDenied()
    # Get form
    if request.method == 'GET':
        form = forms.getOwnedCardForm(forms.OwnedCardForm(instance=owned_card), context['accounts'], owned_card=owned_card)
    # Post edit owned card
    elif request.method == 'POST':
        was_idolized = owned_card.idolized
        if 'stored' not in request.POST:
            form = forms.EditQuickOwnedCardForm(request.POST, instance=owned_card)
        else:
            form = forms.EditOwnedCardForm(request.POST, instance=owned_card)
            if not owned_card.card.skill:
                form.fields.pop('skill')
        if form.is_valid():
            owned_card = form.save(commit=False)
            # Update account
            account_changed = False
            if 'owner_account' in request.POST and request.POST['owner_account'] and request.POST['owner_account'] != str(owned_card.owner_account.id):
                account = get_object_or_404(models.Account.objects.select_related('center', 'center__card'), pk=request.POST['owner_account'], owner=request.user)
                owned_card.owner_account = account
                account_changed = True
            # Set expiration date for present box storage
            if 'stored' in form.cleaned_data and form.cleaned_data['stored'] == 'Box' and 'expires_in' in request.POST:
                try: expires_in = int(request.POST['expires_in'])
                except (TypeError, ValueError): expires_in = 0
                if expires_in < 0: expires_in = 0
                if expires_in:
                    owned_card.expiration = datetime.date.today() + relativedelta(days=expires_in)
            # Save
            owned_card.save()
            # Update account on activity and generate activities on change
            if account_changed and owned_card.card.rarity != 'R' and owned_card.card.rarity != 'N':
                models.Activity.objects.filter(ownedcard=owned_card).update(account=account)
            # Push/update activity on card idolized
            if not was_idolized and owned_card.idolized:
                pushActivity("Idolized a card", ownedcard=owned_card,
                             # prefetch
                             account_owner=request.user)
            else:
                pushActivity("Update card", ownedcard=owned_card,
                             # prefetch
                             account_owner=request.user)
            context['owned'] = owned_card
            context['withcenter'] = True
            context['owner_account'] = owned_card.owner_account
            return render(request, 'ownedCardOnBottomCard.html', context)
    if 'stored' in form.fields:
        form.fields['stored'].required = False
    if 'skill' in form.fields:
        form.fields['skill'].required = False
    if owned_card.expiration:
         owned_card.expires_in = (owned_card.expiration - timezone.now()).days
    context['addcard_form'] = form
    context['edit'] = owned_card
    return render(request, 'addCardForm.html', context)

def ajaxdeletecard(request, ownedcard):
    context = globalContext(request)
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    try:
        if request.user.is_staff:
            owned_card = models.OwnedCard.objects.get(pk=int(ownedcard))
        else:
            owned_card = models.OwnedCard.objects.get(pk=int(ownedcard), owner_account__in=context['accounts'])
    except ObjectDoesNotExist:
        raise PermissionDenied()
    owned_card.delete()
    return HttpResponse('')

def ajaxdeletelink(request, link):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    try:
        link = models.UserLink.objects.get(owner=request.user, pk=int(link))
    except ObjectDoesNotExist:
        raise PermissionDenied()
    link.delete()
    return HttpResponse('deleted')

def ajaxcards(request):
    return cards(request, ajax=True)

def ajaxusers(request):
    return users(request, ajax=True)

def isFollowing(user, request):
    if request.user.is_authenticated():
        try:
            request.user.preferences.following.get(username=user.username)
            return True
        except: pass
    return False

def ajaxfollowers(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'followlist.html', { 'follow': [u.user for u in user.followers.all()],
                                            })

def ajaxfollowing(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'followlist.html', { 'follow': user.preferences.following.all(),
                                                })

def _localized_message_activity(activity):
    if activity.message == 'Custom':
        return activity.message_data
    message_string = models.activityMessageToString(activity.message)
    data = [_(models.STORED_DICT[d]) if d in models.STORED_DICT else _(d) for d in activity.split_message_data()]
    if len(data) == message_string.count('{}'):
        return _(message_string).format(*data)
    return 'Invalid message data'

def _activities(request, account=None, follower=None, user=None, avatar_size=3, card_size=None):
    """
    SQL Queries
    - Django session
    - Request user
    - (if different from request.user) Follower User
    - Preferences
    - Activities (JOIN + like counts)
    - Accounts
    """
    page = 0
    page_size = 5
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    activities = models.Activity.objects.all().order_by('-creation')
    if account is not None:
        activities = activities.filter(account=account)
    if user is not None:
        activities = activities.filter(account__owner__username=user)
    if follower is not None:
        if follower == request.user.username:
            follower = request.user
        else:
            follower = get_object_or_404(User.objects.select_related('preferences'), username=follower)
        accounts_followed = models.Account.objects.filter(owner__in=follower.preferences.following.all())
        ids = [account.id for account in accounts_followed]
        activities = activities.filter(account_id__in=ids)
    if not account and not follower and not user:
        activities = activities.filter(message='Custom')
    activities = activities[(page * page_size):((page * page_size) + page_size)]
    activities = activities.annotate(likers_count=Count('likes'))
    accounts = list(request.user.accounts_set.all()) if request.user.is_authenticated() else []
    for activity in activities:
        activity.localized_message = _localized_message_activity(activity)

    context = {
        'activities': activities,
        'accounts': accounts,
        'page': page + 1,
        'page_size': page_size,
        'avatar_size': avatar_size,
        'content_size': 12 - avatar_size,
        'current': 'activities',
        'card_size': request.GET['card_size'] if 'card_size' in request.GET and request.GET['card_size'] else card_size
    }
    return context

def ajaxactivities(request):
    if settings.HIGH_TRAFFIC:
        return render(request, 'cacheactivities.html')
    account = int(request.GET['account']) if 'account' in request.GET and request.GET['account'] and request.GET['account'].isdigit() else None
    user = request.GET['user'] if 'user' in request.GET and request.GET['user'] else None
    follower = request.GET['follower'] if 'follower' in request.GET and request.GET['follower'] else None
    avatar_size = int(request.GET['avatar_size']) if 'avatar_size' in request.GET and request.GET['avatar_size'] and request.GET['avatar_size'].isdigit() else 3
    return render(request, 'activities.html', _activities(request, account=account, follower=follower, avatar_size=avatar_size, user=user))

def activity(request, activity):
    context = globalContext(request)
    context['activity'] = get_object_or_404(models.Activity, pk=activity)
    context['activity'].likers = context['activity'].likes.all()
    context['activity'].likers_count = context['activity'].likers.count()
    context['avatar_size'] = 2
    context['content_size'] = 10
    context['card_size'] = 150
    context['imgurClientID'] = settings.IMGUR_CLIENT_ID
    context['is_mine'] = findAccount(context['activity'].account_id, context['accounts']) if 'accounts' in context else False
    context['single_activity'] = True
    if context['is_mine']:
        # Form to edit activity
        if context['activity'].message == 'Custom':
            formClass = forms.CustomActivity
            context['form_title'] = _('Edit')
        else:
            formClass = forms.EditActivityPicture
            context['form_title'] = _('Upload your own screenshot')
        form = formClass(instance=context['activity'])
        context['form_delete'] = forms.ConfirmDelete(initial={
            'thing_to_delete': context['activity'].id,
        })
        if request.method == 'POST':
            if 'thing_to_delete' in request.POST:
                context['form_delete'] = forms.ConfirmDelete(request.POST)
                if context['form_delete'].is_valid():
                    context['activity'].delete()
                    return redirect('/')
            else:
                form = formClass(request.POST, instance=context['activity'])
                if 'account_id' in form.fields:
                    del(form.fields['account_id'])
                if form.is_valid():
                    if 'message_data' in form.cleaned_data and form.cleaned_data['message_data']:
                        context['activity'].message_data = form.cleaned_data['message_data']
                    if form.cleaned_data['right_picture'] and get_imgur_code(form.cleaned_data['right_picture']) != context['activity'].right_picture:
                        imgur = get_imgur_code(form.cleaned_data['right_picture'])
                        context['activity'].right_picture = imgur
                    context['activity'].save()
        context['form'] = form
    context['activity'].localized_message = _localized_message_activity(context['activity'])
    return render(request, 'activity.html', context)

def _contextfeed(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    avatar_size = int(request.GET['avatar_size']) if 'avatar_size' in request.GET and request.GET['avatar_size'] and request.GET['avatar_size'].isdigit() else 2
    return _activities(request, follower=request.user.username, avatar_size=avatar_size)

def ajaxfeed(request):
    if settings.HIGH_TRAFFIC:
        return render(request, 'cacheactivities.html')
    return render(request, 'activities.html', _contextfeed(request))

def isLiking(request, activity_obj):
    if request.user.is_authenticated():
        for u in activity_obj.likes.all():
            if u.id == request.user.id:
                return True
    return False

@csrf_exempt
def ajaxlikeactivity(request, activity):
    context = globalContext(request)
    if not request.user.is_authenticated() or request.user.is_anonymous() or request.method != 'POST':
        raise PermissionDenied()
    activity_obj = get_object_or_404(models.Activity, id=activity)
    if activity_obj.account.owner.id != request.user.id:
        if 'like' in request.POST:
            if not isLiking(request, activity_obj):
                activity_obj.likes.add(request.user)
                activity_obj.save()
            return HttpResponse('liked')
        if 'unlike' in request.POST:
            if isLiking(request, activity_obj):
                activity_obj.likes.remove(request.user)
                activity_obj.save()
            return HttpResponse('unliked')
    raise PermissionDenied()

@csrf_exempt
def ajaxfollow(request, username):
    context = globalContext(request)
    if (not request.user.is_authenticated() or request.user.is_anonymous()
        or request.method != 'POST' or request.user.username == username):
        raise PermissionDenied()
    user = get_object_or_404(User, username=username)
    if 'follow' in request.POST and not isFollowing(user, request):
        request.user.preferences.following.add(user)
        request.user.preferences.save()
        return HttpResponse('followed')
    if 'unfollow' in request.POST and isFollowing(user, request):
        request.user.preferences.following.remove(user)
        request.user.preferences.save()
        return HttpResponse('unfollowed')
    raise PermissionDenied()

def ajaxeventranking(request, event, language):
    page = 0
    page_size = 10
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    event = get_object_or_404(models.Event, pk=event)
    participations = event.participations.filter(account__language=language).select_related('account', 'account__owner', 'account__owner__preferences').extra(select={'ranking_is_null': 'ranking IS NULL'}, order_by=['ranking_is_null', 'ranking'])[(page * page_size):((page * page_size) + page_size)]
    context = {
        'participations': participations,
        'event': event,
        'ajax': True,
        'loader': True,
        'page': page + 1,
    }
    return render(request, 'event_ranking.html', context)

def ajaxmodal(request, hash):
    context = {}
    if 'interfaceColor' in request.GET:
        context['interfaceColor'] = request.GET['interfaceColor']
    if hash == 'aboutllsif':
        return render(request, 'modalabout.html', context)
    elif hash == 'aboutsukutomo':
        return render(request, 'modalsukutomo.html', context)
    elif hash == 'developers':
        return render(request, 'modaldevelopers.html', context)
    elif hash == 'contact':
        return render(request, 'modalcontact.html', context)
    elif hash == 'thanks':
        return render(request, 'modalthanks.html', context)
    elif hash == 'tutorialaddcard':
        return render(request, 'modaltutorialaddcard.html', context)
    raise Http404

def edit(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    context['preferences'] = request.user.preferences
    context['show_verified_info'] = 'verification' in request.GET
    form = forms.UserForm(instance=request.user)
    form_preferences = forms.UserPreferencesForm(instance=context['preferences'], request=request)
    form_addlink = forms.AddLinkForm()
    form_changepassword = forms.ChangePasswordForm()
    if request.method == "POST":
        if 'editPreferences' in request.POST:
            form_preferences = forms.UserPreferencesForm(request.POST, instance=context['preferences'], request=request)
            old_location = context['preferences'].location
            if form_preferences.is_valid():
                prefs = form_preferences.save(commit=False)
                if old_location != prefs.location:
                    prefs.location_changed = True
                prefs.save()
                return redirect('/user/' + request.user.username)
        elif 'changePassword' in request.POST:
            form_changepassword = forms.ChangePasswordForm(request.POST)
            if form_changepassword.is_valid():
                new_password = form_changepassword.cleaned_data['new_password']
                username = request.user.username
                old_password = form_changepassword.cleaned_data['old_password']
                user = authenticate(username=username, password=old_password)
                if user is not None:
                    for account in context['accounts']:
                        if account.transfer_code and transfer_code.is_encrypted(account.transfer_code):
                            clear_transfer_code = transfer_code.decrypt(account.transfer_code, old_password)
                            encrypted_transfer_code = transfer_code.encrypt(clear_transfer_code, new_password)
                            account.transfer_code = encrypted_transfer_code
                            account.save()
                    user.set_password(new_password)
                    user.save()
                    authenticate(username=username, password=new_password)
                    login(request, user)
                    return redirect('/user/' + request.user.username)
                errors = form_changepassword._errors.setdefault("old_password", ErrorList())
                errors.append(_('Wrong password.'))
        elif 'addLink' in request.POST:
            form_addlink = forms.AddLinkForm(request.POST)
            if form_addlink.is_valid():
                link = form_addlink.save(commit=False)
                link.owner = request.user
                link.save()
                return redirect('/edit/#link' + str(link.id))
        else:
            form = forms.UserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/user/' + request.user.username)
    context['form'] = form
    context['attribute_choices'] = models.ATTRIBUTE_CHOICES
    context['form_addlink'] = form_addlink
    context['form_changepassword'] = form_changepassword
    context['form_preferences'] = form_preferences
    context['links'] = list(request.user.links.all().values())
    context['current'] = 'edit'
    return render(request, 'edit.html', context)

def report(request, account=None, eventparticipation=None):
    context = globalContext(request)
    if account:
        context['account'] = findAccount(int(account), context.get('accounts', []), forceGetAccount=True)
        if not context['account']: raise Http404
        context['eventparticipation'] = None
    else:
        context['eventparticipation'] = get_object_or_404(models.EventParticipation.objects.select_related('event', 'account', 'account__owner'), pk=eventparticipation)
        context['account'] = None
    context['report'] = None
    if request.user.is_authenticated():
        try: context['report'] = models.ModerationReport.objects.get(reported_by=request.user, fake_account=context['account'], fake_eventparticipation=context['eventparticipation'])
        except ObjectDoesNotExist: pass
    if request.method == 'POST':
        context['form'] = forms.ModerationReportForm(request.POST, request.FILES, instance=context['report'], request=request, account=context['account'], eventparticipation=context['eventparticipation'])
        if context['form'].is_valid():
            context['report'] = context['form'].save()
            context['reported'] = True
    else:
        context['form'] = forms.ModerationReportForm(instance=context['report'], request=request, account=context['account'], eventparticipation=context['eventparticipation'])
    if context['report']:
        context['report_images'] = context['report'].images.all()
    return render(request, 'report.html', context)

def editaccount(request, account):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    owned_account = findAccount(int(account), context['accounts'])
    if not owned_account:
        raise PermissionDenied()
    if owned_account.verified:
        formClass = forms.FullAccountNoFriendIDForm
    else:
        formClass = forms.FullAccountForm
    form = formClass(instance=owned_account)
    form_delete = forms.ConfirmDelete(initial={
        'thing_to_delete': owned_account.id,
    })
    form_get_transfer_code = forms.SimplePasswordForm()
    form_save_transfer_code = forms.TransferCodeForm()
    if not owned_account.transfer_code:
        del(form_save_transfer_code.fields['confirm'])
    try:
        context['verification'] = owned_account.verificationrequest.get()
    except: pass
    if 'verification' in context:
        form_verification = forms.VerificationRequestForm(instance=context['verification'], account=owned_account)
    else:
        form_verification = forms.VerificationRequestForm(account=owned_account)
    if request.method == "POST":
        if 'deleteAccount' in request.POST:
            form_delete = forms.ConfirmDelete(request.POST)
            if form_delete.is_valid():
                owned_account.delete()
                return redirect('/user/' + request.user.username)
        elif 'getTransferCode' in request.POST:
            form_get_transfer_code = forms.SimplePasswordForm(request.POST)
            if form_get_transfer_code.is_valid():
                if authenticate(username=request.user.username, password=form_get_transfer_code.cleaned_data['password']) is not None:
                    context['transfer_code'] = transfer_code.decrypt(owned_account.transfer_code, form_get_transfer_code.cleaned_data['password'])
                else:
                    errors = form_get_transfer_code._errors.setdefault("password", ErrorList())
                    errors.append(_('Wrong password.'))
        elif 'saveTransferCode' in request.POST:
            form_save_transfer_code = forms.TransferCodeForm(request.POST)
            if not owned_account.transfer_code:
                del(form_save_transfer_code.fields['confirm'])
            if form_save_transfer_code.is_valid():
                if authenticate(username=request.user.username, password=form_save_transfer_code.cleaned_data['password']) is not None:
                    encrypted_transfer_code = transfer_code.encrypt(form_save_transfer_code.cleaned_data['transfer_code'], form_save_transfer_code.cleaned_data['password'])
                    owned_account.transfer_code = encrypted_transfer_code
                    owned_account.save()
                    form_save_transfer_code = forms.TransferCodeForm()
                    context['saved_transfer_code'] = True
                else:
                    errors = form_save_transfer_code._errors.setdefault("password", ErrorList())
                    errors.append(_('Wrong password.'))
        elif 'deleteTransferCode' in request.POST:
            owned_account.transfer_code = ''
            owned_account.save()
            context['deleted_transfer_code'] = True
        elif 'deleteimage' in request.POST and 'verification' in context:
            imageObject = context['verification'].images.get(pk=request.POST['id'])
            imageObject.image.delete()
            imageObject.delete()
        elif 'cancelVerificationRequest' in request.POST and 'verification' in context:
            imagesObjects = context['verification'].images.all()
            for imageObject in imagesObjects:
                imageObject.image.delete()
            imagesObjects.delete()
            context['verification'].delete()
            del context['verification']
            form_verification = forms.VerificationRequestForm(account=owned_account)
        elif 'verificationRequest' in request.POST:
            if 'verification' in context:
                form_verification = forms.VerificationRequestForm(request.POST, request.FILES, instance=context['verification'], account=owned_account)
            else:
                form_verification = forms.VerificationRequestForm(request.POST, request.FILES, account=owned_account)
            if form_verification.is_valid():
                verification = form_verification.save(commit=False)
                verification.verification_date = None
                verification.verified_by = None
                verification.verification_comment = None
                verification.account = owned_account
                verification.creation = timezone.now()
                verification.status = 1
                verification.save()
                for image in form_verification.cleaned_data['upload_images']:
                    imageObject = models.UserImage.objects.create()
                    imageObject.image.save(randomString(64), image)
                    verification.images.add(imageObject)
                context['verification'] = verification
        else:
            old_rank = owned_account.rank
            form = formClass(request.POST, instance=owned_account)
            form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=owned_account, stored='Deck').order_by('rarity', '-idolized', 'attribute', 'card__id').select_related('card')
            if form.is_valid():
                account = form.save(commit=False)
                if account.rank >= 200 and account.verified <= 0:
                    account.rank = 195
                    account.save()
                    return redirect('/user/' + request.user.username + '/?notification=ADDACCOUNTRANK200&notification_link_variables=' + str(account.pk))
                else:
                    account.save()
                    if old_rank < account.rank:
                        pushActivity('Rank Up', number=account.rank, account=account,
                                     # prefetch:
                                     account_owner=request.user)
                    return redirect('/user/' + request.user.username)
    form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=owned_account, stored='Deck').order_by('card__id').select_related('card')
    context['form'] = form
    context['form_delete'] = form_delete
    context['form_get_transfer_code'] = form_get_transfer_code
    context['form_save_transfer_code'] = form_save_transfer_code
    context['form_verification'] = form_verification
    context['account'] = owned_account
    context['current'] = 'editaccount'
    context['edit'] = owned_account
    try:
        context['verification_images'] = context['verification'].images.all()
        if context['verification'].status == 1:
            context['verification_queue_position'] = models.VerificationRequest.objects.filter(status=1, account__rank__gte=context['account'].rank).count()
            if context['verification_queue_position'] == 0:
                context['verification_queue_position'] = 1
            context['verification_days'] = 1
            context['verification_days'] = int(math.ceil(context['verification_queue_position'] / 10))
            if context['verification_days'] == 0:
                context['verification_days'] = 1
    except: pass
    return render(request, 'addaccount.html', context)

def users(request, ajax=False):
    """
    SQL Queries
    - Context
    - Count accounts
    - Accounts
    - Users
    - Preferences
    - Center Owned Cards
    - Center Cards
    """
    if len(request.GET.getlist('page')) > 1:
        raise PermissionDenied()
    if ajax:
        context = {}
    else:
        context = globalContext(request)

    queryset = models.Account.objects.exclude(fake=True)
    page_size = 18
    default_ordering = 'rank'
    context['filter_form'] = forms.FilterUserForm(request.GET, request=request)

    if request.GET:
        if 'search' in request.GET:
            terms = request.GET['search'].split(' ')
            for term in terms:
                if term.isdigit():
                    queryset = queryset.filter(Q(rank__exact=term)
                                               | Q(friend_id__exact=term)
                                           )
                elif term != '':
                    queryset = queryset.filter(Q(owner__username__icontains=term)
                                               | Q(owner__preferences__description__icontains=term)
                                               | Q(owner__preferences__location__icontains=term)
                                               | Q(owner__email__iexact=term)
                                               | Q(owner__links__value__icontains=term)
                                               | Q(nickname__icontains=term)
                                           )
        if 'attribute' in request.GET and request.GET['attribute']:
            queryset = queryset.filter(owner__preferences__color=request.GET['attribute'])
        if 'best_girl' in request.GET and request.GET['best_girl']:
            queryset = queryset.filter(owner__preferences__best_girl=request.GET['best_girl'])
        # if 'location' in request.GET and request.GET['location']:
        #     queryset = queryset.filter()
        if 'private' in request.GET and request.GET['private']:
            if request.GET['private'] == '2':
                queryset = queryset.filter(owner__preferences__private=True)
            elif request.GET['private'] == '3':
                queryset = queryset.filter(owner__preferences__private=False)
        if 'status' in request.GET and request.GET['status']:
            if request.GET['status'] == 'only':
                queryset = queryset.filter(owner__preferences__status__isnull=False)
            else:
                queryset = queryset.filter(owner__preferences__status=request.GET['status'])
        if 'language' in request.GET and request.GET['language']:
            queryset = queryset.filter(language=request.GET['language'])
        if 'os' in request.GET and request.GET['os']:
            queryset = queryset.filter(os=request.GET['os'])
        if 'verified' in request.GET and request.GET['verified']:
            if request.GET['verified'] == '3':
                queryset = queryset.filter(Q(verified=1) | Q(verified=2) | Q(verified=3))
            else:
                queryset = queryset.filter(verified=request.GET['verified'])
        if 'center_attribute' in request.GET and request.GET['center_attribute']:
            queryset = queryset.filter(center__card__attribute=request.GET['center_attribute'])
        if 'center_rarity' in request.GET and request.GET['center_rarity']:
            queryset = queryset.filter(center__card__rarity=request.GET['center_rarity'])
        if 'with_friend_id' in request.GET and request.GET['with_friend_id']:
            if request.GET['with_friend_id'] == '2':
                queryset = queryset.filter(friend_id__isnull=False)
            elif request.GET['with_friend_id'] == '3':
                queryset = queryset.filter(friend_id__isnull=True)
        if 'accept_friend_requests' in request.GET and request.GET['accept_friend_requests']:
            if request.GET['accept_friend_requests'] == '2':
                queryset = queryset.filter(accept_friend_requests=True)
            elif request.GET['accept_friend_requests'] == '3':
                queryset = queryset.filter(accept_friend_requests=False)
        if 'play_with' in request.GET and request.GET['play_with']:
            queryset = queryset.filter(play_with=request.GET['play_with'])
        if (('owns' in request.GET and request.GET['owns'].isdigit())
            or ('wish' in request.GET and request.GET['wish'].isdigit())):
            wish = 'owns' not in request.GET
            context['wish'] = wish
            card_id = request.GET['wish' if wish else 'owns']
            try:
                context['owns_card'] = models.Card.objects.get(pk=card_id)
                context['owns_card_string'] = unicode(context['owns_card'])
            except: pass
            ownedcards = models.OwnedCard.objects.filter(card_id=card_id)
            if not wish:
                ownedcards = ownedcards.filter(Q(stored='Deck') | Q(stored='Album'))
            else:
                ownedcards = ownedcards.filter(stored='Favorite')
            if 'owns_idolized' in request.GET:
                ownedcards = ownedcards.filter(idolized=(request.GET['owns_idolized'] == 'on'))
                context['owns_card_idolized'] = request.GET['owns_idolized']
            queryset = queryset.filter(ownedcards__in=ownedcards)

    queryset = queryset.distinct()
    queryset = queryset.prefetch_related('owner', 'owner__preferences', 'center', 'center__card')

    page = 0
    reverse = ('reverse_order' in request.GET and request.GET['reverse_order']) or not request.GET or len(request.GET) == 1
    ordering = request.GET['ordering'] if 'ordering' in request.GET and request.GET['ordering'] else default_ordering
    prefix = '-' if reverse else ''
    queryset = queryset.order_by(prefix + ordering)

    context['total_results'] = queryset.count()

    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    queryset = queryset[(page * page_size):((page * page_size) + page_size)]

    context['ordering'] = ordering
    context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    context['page'] = page + 1
    context['page_size'] = page_size
    context['ajax'] = ajax
    context['show_no_result'] = not ajax
    context['show_search_results'] = bool('search' in request.GET)

    context['accounts_list'] = queryset
    context['users_language'] = request.GET['language'] if 'language' in request.GET else None

    cardsinfo = settings.CARDS_INFO
    context['idols'] = cardsinfo['idols']

    if len(request.GET) > 1 or (len(request.GET) == 1 and 'page' not in request.GET):
        context['filter_form'] = forms.FilterUserForm(request.GET, request=request)
    else:
        context['filter_form'] = forms.FilterUserForm(request=request)
    context['current'] = 'users'
    return render(request, 'usersPage.html' if ajax else 'users.html', context)

def events(request):
    context = globalContext(request)
    context['current'] = 'events'
    queryset = models.Event.objects.all()

    form_data = request.GET.copy()

    if 'search' in request.GET:
        terms = request.GET['search'].split(' ')
        for term in terms:
            if term != '':
                queryset = queryset.filter(Q(japanese_name__icontains=term)
                                           | Q(romaji_name__icontains=term)
                                           | Q(english_name__icontains=term)
                                           | Q(note__icontains=term)
                                           | Q(cards__name__icontains=term)
                                           | Q(cards__attribute__icontains=term)
                )
    if 'event_type' in request.GET and request.GET['event_type']:
        if request.GET['event_type'] == 'Token':
            queryset = queryset.exclude(japanese_name__icontains='Score Match').exclude(japanese_name__icontains='Medley Festival')
        else:
            queryset = queryset.filter(japanese_name__icontains=request.GET['event_type'])
    if 'idol' in request.GET and request.GET['idol']:
        queryset = queryset.filter(cards__name=request.GET['idol'])
    if 'idol_attribute' in request.GET and request.GET['idol_attribute']:
        queryset = queryset.filter(cards__attribute=request.GET['idol_attribute'])
    if 'idol_skill' in request.GET and request.GET['idol_skill']:
        queryset = queryset.filter(cards__skill=request.GET['idol_skill'])
    if request.user.is_authenticated() and 'participation' in request.GET and request.GET['participation']:
        if request.GET['participation'] == '2':
            queryset = queryset.filter(participations__account__owner=request.user)
        elif request.GET['participation'] == '3':
            queryset = queryset.exclude(participations__account__owner=request.user)

    if ('accounts' in context and not hasJP(context['accounts'])
        and 'search' not in request.GET or 'is_world' in request.GET and request.GET['is_world']):
        if 'is_world' in request.GET and request.GET['is_world'] == 'off':
            queryset = queryset.filter(english_beginning__isnull=True)
            form_data['is_world'] = False
            # Remove too old events when showing upcoming ones (very unlikely to happen in EN or else)
            if 'reverse_order' in request.GET:
                queryset = queryset.exclude(beginning__lte=timezone.now() - relativedelta(months=15))
                context['show_approximate_dates'] = True
        else:
            queryset = queryset.filter(english_beginning__isnull=False)
            context['show_discover_banner'] = True
            form_data['is_world'] = 'on'

    queryset = queryset.distinct()

    context['filter_form'] = forms.FilterEventForm(form_data, request=request)

    queryset = queryset.order_by(('' if 'reverse_order' in request.GET and request.GET['reverse_order'] else '-') + 'end')

    context['events'] = queryset
    context['show_english_banners'] = not onlyJP(context)
    return render(request, 'events.html', context)

def event(request, event):
    context = globalContext(request)
    event = get_object_or_404(models.Event, japanese_name=event)
    context['show_english_banners'] = not onlyJP(context)
    context['did_happen_world'] = event.did_happen_world()
    context['did_happen_japan'] = event.did_happen_japan()
    context['soon_happen_world'] = event.soon_happen_world()
    context['soon_happen_japan'] = event.soon_happen_japan()
    context['is_world_current'] = event.is_world_current()
    context['is_japan_current'] = event.is_japan_current()

    # get rankings
    event.all_cards = event.cards.all()
    if context['did_happen_japan']:
        event.japanese_participations = event.participations.filter(account__language='JP').select_related('account', 'account__owner', 'account__owner__preferences').extra(select={'ranking_is_null': 'ranking IS NULL'}, order_by=['ranking_is_null', 'ranking'])[:10]
        if context['did_happen_world']:
            event.english_participations = event.participations.filter(account__language='EN').select_related('account', 'account__owner', 'account__owner__preferences').extra(select={'ranking_is_null': 'ranking IS NULL'}, order_by=['ranking_is_null', 'ranking'])[:10]
            event.other_participations = event.participations.exclude(account__language='JP').exclude(account__language='EN').select_related('account', 'account__owner', 'account__owner__preferences').extra(select={'ranking_is_null': 'ranking IS NULL'}, order_by=['account__language', 'ranking_is_null', 'ranking'])

    context['event'] = event
    return render(request, 'event.html', context)

def _findparticipation(id, participations):
    for participation in participations:
        if str(participation.id) == id:
            return participation
    return None

def eventparticipations(request, event):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        return redirect('/create/')
    context = globalContext(request)
    event = get_object_or_404(models.Event, japanese_name=event)
    context['your_participations'] = event.participations.filter(account__owner=request.user).select_related('account')
    if 'Score Match' in event.japanese_name or 'Medley Festival' in event.japanese_name:
        context['with_song'] = False
    else:
        context['with_song'] = True
    # handle form post
    if request.method == 'POST':
        # edit
        if 'id' in request.POST:
            participation = _findparticipation(request.POST['id'], context['your_participations'])
            if participation:
                if 'deleteParticipation' in request.POST:
                    participation.delete()
                    context['your_participations'] = event.participations.filter(account__owner=request.user).select_related('account')
                else:
                    form = forms.EventParticipationNoAccountForm(request.POST, instance=participation)
                    if form.is_valid():
                        form.save()
                        pushActivity('Ranked in event',
                                     eventparticipation=participation,
                                     # Prefetch:
                                     account=findAccount(participation.account_id, context['accounts']),
                                     event=event,
                                     account_owner=request.user)
        # add
        else:
            form = forms.EventParticipationForm(request.POST)
            if form.is_valid():
                participation = form.save(commit=False)
                # check if the user owns the account
                if findAccount(participation.account_id, context['accounts']):
                    participation.event = event
                    participation.save()
                    pushActivity('Ranked in event',
                                 eventparticipation=participation,
                                 # Prefetch:
                                 account=findAccount(participation.account_id, context['accounts']),
                                 event=event,
                                 account_owner=request.user)

    # get forms to add or edit
    add_form_accounts_queryset = request.user.accounts_set.all()
    context['edit_forms'] = []
    if context['with_song']:
        formClass = forms.EventParticipationNoAccountForm
    else:
        formClass = forms.EventParticipationNoSongNoAccountForm
    for participation in context['your_participations']:
        context['edit_forms'].append((participation.id, participation.account, formClass(instance=participation)))
        add_form_accounts_queryset = add_form_accounts_queryset.exclude(id=participation.account.id)
    if not event.did_happen_world():
        add_form_accounts_queryset = add_form_accounts_queryset.filter(language='JP')
    if not event.did_happen_japan():
        add_form_accounts_queryset = add_form_accounts_queryset.exclude(language='JP')
    if event.did_happen_japan():
        if context['with_song']:
            formClass = forms.EventParticipationForm
        else:
            formClass = forms.EventParticipationNoSongForm
        context['add_form'] = forms.getEventParticipationForm(formClass(), add_form_accounts_queryset)
    context['event'] = event
    return render(request, 'event_participations.html', context)

def idols(request):
    context = globalContext(request)
    context['current'] = 'idols'
    idols = models.Idol.objects.all().order_by('main', 'main_unit', 'name')
    context['main_idols'] = sorted(filter(lambda x: x.main == True and x.main_unit != 'Aqours', idols), key=operator.attrgetter('year'))
    context['aqours_idols'] = sorted(filter(lambda x: x.main == True and x.main_unit == 'Aqours', idols), key=operator.attrgetter('year'))
    context['n_idols'] = filter(lambda x: x.main == False, idols)
    return render(request, 'idols.html', context)

def android(request):
    context = globalContext(request)
    context['android'] = raw.app_data['android']
    return render(request, 'android.html', context)

def mapview(request):
    context = globalContext(request)
    with open ("map.json", "r") as f:
        context['map'] = f.read().replace('\n', '')
    with open ("mapcount.json", "r") as f:
        context['mapcount'] = f.read().replace('\n', '')
    if request.user.is_authenticated() and request.user.preferences.latitude:
        context['you'] = request.user.preferences
    context['users_ages_values'] = settings.USERS_AGES.values()
    context['users_ages_keys'] = settings.USERS_AGES.keys()
    context['users_total_ages'] = settings.USERS_TOTAL_AGES
    context['current'] = 'map'
    return render(request, 'map.html', context)

def discussions(request):
    context = globalContext(request)
    context['discussions'] = web_raw.discussions
    context['community_links'] = (link for link in links_list if link['link'] == 'communities').next()
    context['card'] = models.Card.objects.filter(name=context['community_links']['idol'], transparent_idolized_image__isnull=False).order_by('?')[0]
    return render(request, 'discussions.html', context)

def discussion(request, discussion):
    context = globalContext(request)
    context['discussion'] = (d for d in web_raw.discussions if 'code' in d and d['code'] == discussion).next()
    return render(request, 'discussion.html', context)

def avatar_twitter(request, username):
    return redirect('http://avatars.io/twitter/' + username + '?size=large')
def avatar_facebook(request, username):
    return redirect('http://avatars.io/facebook/' + username + '?size=large')

def aboutview(request):
    context = globalContext(request)
    users = models.User.objects.filter(Q(is_staff=True) | Q(preferences__status__isnull=False)).exclude(is_staff=False, preferences__status='').order_by('-is_superuser', 'preferences__status', '-preferences__donation_link', '-preferences__donation_link_title').select_related('preferences')
    users = users.annotate(verifications_done=Count('verificationsdone'))

    context['staff'] = []
    context['donators_low'] = []
    context['donators_high'] = []
    for user in users:
        if user.is_staff:
            user.preferences.allowed_verifications = user.preferences.allowed_verifications.split(',') if user.preferences.allowed_verifications else []
            context['staff'].append(user)
        if user.preferences.status == 'THANKS' or user.preferences.status == 'SUPPORTER' or user.preferences.status == 'LOVER' or user.preferences.status == 'AMBASSADOR':
            context['donators_low'].append(user)
        elif user.preferences.status == 'PRODUCER' or user.preferences.status == 'DEVOTEE':
            context['donators_high'].append(user)
    context['total_donators'] = settings.TOTAL_DONATORS
    context['donations'] = donations.donations
    context['artists'] = []
    for idol in raw.raw_information:
        if 'chibi' in raw.raw_information[idol]:
            context['artists'] += raw.raw_information[idol]['chibi']
    for idol in raw.raw_information_n:
        if 'chibi' in raw.raw_information_n[idol]:
            context['artists'] += raw.raw_information_n[idol]['chibi']
    return render(request, 'about.html', context)

def staff_verifications(request):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff or not request.user.preferences.allowed_verifications:
        raise PermissionDenied()
    context = globalContext(request)
    context['verifications'] = models.VerificationRequest.objects
    if 'status' not in request.GET or not request.GET['status']:
        context['verifications'] = context['verifications'].filter(Q(status=1) | Q(status=2))
    else:
        context['verifications'] = context['verifications'].filter(status=request.GET['status'])
    if 'verified_by' in request.GET and request.GET['verified_by']:
        context['verifications'] = context['verifications'].filter(verified_by=request.GET['verified_by'])
    if 'OS' in request.GET and request.GET['OS']:
        context['verifications'] = context['verifications'].filter(account__os=request.GET['OS'])
    if 'language' in request.GET and request.GET['language']:
        context['verifications'] = context['verifications'].filter(account__language=request.GET['language'])
    if 'allow_during_events' in request.GET and request.GET['allow_during_events']:
        context['verifications'] = context['verifications'].filter(allow_during_events=True)
    if 'verification' in request.GET and int(request.GET['verification']) > 0:
        context['verifications'] = context['verifications'].filter(verification=request.GET['verification'])
    context['verifications'] = context['verifications'].filter(verification__in=request.user.preferences.allowed_verifications.split(','))
    if 'status' in request.GET and request.GET['status'] and (request.GET['status'] == '0' or request.GET['status'] == '3'):
        context['verifications'] = context['verifications'].order_by('-verification_date')
    else:
        context['verifications'] = context['verifications'].order_by('-status', '-account__rank', 'creation').select_related('account', 'account__owner')
    page = 0
    page_size = 10
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    context['total'] = context['verifications'].count()
    context['page'] = page + 1
    context['verifications'] = context['verifications'][(page * page_size):((page * page_size) + page_size)]
    context['form'] = forms.StaffFilterVerificationRequestForm(request.GET)
    context['disqus_shortname'] = settings.DISQUS_STAFF
    return render(request, 'staff_verifications.html', context)

def staff_verification(request, verification):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff:
        raise PermissionDenied()
    context = globalContext(request)
    context['verification'] = get_object_or_404(models.VerificationRequest.objects.select_related('account', 'account__owner', 'account__owner__preferences'), pk=verification)

    if str(context['verification'].verification) not in request.user.preferences.allowed_verifications.split(','):
        raise PermissionDenied()
    context['form'] = forms.StaffVerificationRequestForm(instance=context['verification'])
    if 'verificationRequest' in request.POST:
        form = forms.StaffVerificationRequestForm(request.POST, request.FILES, instance=context['verification'])
        if form.is_valid():
            sendverificationemail = lambda: send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + models.verifiedUntranslatedToString(context['verification'].verification) + u': ' + models.verificationUntranslatedStatusToString(context['verification'].status)),
               template_name='verified',
               to=[context['verification'].account.owner.email, 'contact@schoolido.lu'],
               context=context,
           )
            verification = form.save(commit=False)
            context['verification_images'] = verification.images.all()
            for image in form.cleaned_data['images']:
                imageObject = models.UserImage.objects.create()
                imageObject.image.save(randomString(64), image)
                verification.images.add(imageObject)
            if verification.status == 3:
                verification.verification_date = timezone.now()
                verification.verified_by = request.user
                verification.account.verified = verification.verification
                verification.account.fake = False
                verification.account.save()
                sendverificationemail()
                pushActivity('Verified', number=verification.verification, account=verification.account, account_owner=verification.account.owner)
            elif verification.status == 0:
                verification.verified_by = request.user
                verification.verification_date = timezone.now()
                sendverificationemail()
            verification.save()
            context['verification'] = verification
            return redirect('/staff/verifications/')
        context['form'] = forms.StaffVerificationRequestForm(instance=context['verification'])
    elif 'notification' in request.POST:
        context['notification_minutes'] = request.POST['notification_minutes']
        context['verification'].verification_date = timezone.now() + relativedelta(minutes=int(request.POST['notification_minutes']))
        context['verification'].status = 2
        context['verification'].verified_by = request.user
        send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + models.verifiedUntranslatedToString(context['verification'].verification) + u': ' + unicode(request.POST['notification_minutes']) + u' minutes notification before we verify your account'),
                   template_name='verification_notification',
                   to=[context['verification'].account.owner.email, 'contact@schoolido.lu'],
                   context=context,
                   )
        context['verification'].save()

    context['verification_images'] = context['verification'].images.all()
    context['show_profile'] = 'noprofile' not in request.GET
    return render(request, 'staff_verification.html', context)

def ajaxstaffverificationdeleteimage(request, verification, image):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff:
        raise PermissionDenied()
    verification = get_object_or_404(models.VerificationRequest, pk=verification)
    imageObject = verification.images.get(pk=image)
    imageObject.image.delete()
    imageObject.delete()
    return HttpResponse('deleted')

def ajaxverification(request, verification, status):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff:
        raise PermissionDenied()
    verification = get_object_or_404(models.VerificationRequest, pk=verification)
    verification.status = status
    if status == 1:
        verification.verified_by = None
        verification.verification_date = None
    else:
        verification.verified_by = request.user
    verification.save()
    return HttpResponse('status changed')

def staff_reports(request):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff:
        raise PermissionDenied()
    context = globalContext(request)
    context['reports'] = models.ModerationReport.objects
    if 'status' not in request.GET or not request.GET['status']:
        context['reports'] = context['reports'].filter(Q(status=1) | Q(status=2))
    else:
        context['reports'] = context['reports'].filter(status=request.GET['status'])
    if 'status' in request.GET and request.GET['status'] and (request.GET['status'] == '0' or request.GET['status'] == '3'):
        context['reports'] = context['reports'].order_by('-moderation_date')
    else:
        context['reports'] = context['reports'].order_by('-status', '-fake_account__rank', 'fake_eventparticipation__ranking', '-fake_eventparticipation__points', 'creation')
    context['reports'] = context['reports'].select_related('fake_account', 'fake_account__owner', 'fake_eventparticipation', 'fake_eventparticipation__event', 'fake_eventparticipation__account', 'fake_eventparticipation__account__owner', 'reported_by', 'moderated_by')
    page = 0
    page_size = 10
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    context['total'] = context['reports'].count()
    context['page'] = page + 1
    context['reports'] = context['reports'][(page * page_size):((page * page_size) + page_size)]
    context['reports'] = context['reports'].prefetch_related(Prefetch('images', to_attr='report_images'))
    context['disqus_shortname'] = settings.DISQUS_STAFF
    return render(request, 'staff_reports.html', context)

@csrf_exempt
def ajaxreport(request, report_id, status):
    if not request.user.is_authenticated() or request.user.is_anonymous() or not request.user.is_staff or request.method != 'POST':
        raise PermissionDenied()
    report = get_object_or_404(models.ModerationReport.objects.select_related('fake_account', 'fake_account__owner', 'fake_eventparticipation', 'fake_eventparticipation__event', 'fake_eventparticipation__account', 'fake_eventparticipation__account__owner'), pk=report_id)
    report.moderated_by = request.user
    report.moderation_date = timezone.now()
    report.moderation_comment = request.POST.get('comment', None)
    context = {'report': report}
    if status == 'accept':
        if report.fake_account:
            report.fake_account.fake = True
            report.fake_account.verified = 0
            report.fake_account.verificationrequest.all().update(status=0) # Verification requests rejected
            report.fake_account.save()
            if report.fake_account.owner.email:
                send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + u' Account marked as "fake": ' + unicode(report.fake_account)),
                           template_name='report_fake_account',
                           to=[report.fake_account.owner.email, 'contact@schoolido.lu'],
                           context=context,
                       )
            if report.reported_by and report.reported_by.email:
                send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + u' Thank you for reporting this fake account! ' + unicode(report.fake_account)),
                           template_name='report_fake_account_accepted',
                           to=[report.reported_by.email, 'contact@schoolido.lu'],
                           context=context,
                       )
        elif report.fake_eventparticipation:
            if report.fake_eventparticipation.account.owner.email:
                send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + u' Event participation deleted: ' + unicode(report.fake_eventparticipation.event)),
                           template_name='report_fake_eventparticipation',
                           to=[report.fake_eventparticipation.account.owner.email, 'contact@schoolido.lu'],
                           context=context,
                       )
            if report.reported_by and report.reported_by.email:
                send_email(subject=(u'School Idol Tomodachi' + u'✨ ' + u' Thank you for reporting this fake event participation! ' + unicode(report.fake_eventparticipation.event.japanese_name)),
                           template_name='report_fake_eventparticipation_accepted',
                           to=[report.reported_by.email, 'contact@schoolido.lu'],
                           context=context,
                       )
            report.fake_eventparticipation.delete()
        report.status = 3 # Accepted
    elif status == 'reject':
        report.status = 0 # Rejected
    report.save()
    return HttpResponse(status)
            
def songs(request, song=None, ajax=False):
    page = 0
    context = globalContext(request)

    if song is None:
        songs = models.Song.objects.filter()
        if 'search' in request.GET:
            if request.GET['search']:
                terms = request.GET['search'].split(' ')
                for term in terms:
                    songs = songs.filter(Q(name__icontains=term)
                                         | Q(romaji_name__icontains=term)
                                         | Q(translated_name__icontains=term)
                                         | Q(event__japanese_name__icontains=term)
                                         | Q(event__romaji_name__icontains=term)
                                         | Q(event__english_name__icontains=term)
                                     )
        if 'attribute' in request.GET and request.GET['attribute']:
            songs = songs.filter(attribute__exact=request.GET['attribute'])
        if 'is_daily_rotation' in request.GET and request.GET['is_daily_rotation']:
            if request.GET['is_daily_rotation'] == '2':
                songs = songs.filter(daily_rotation__isnull=False)
            elif request.GET['is_daily_rotation'] == '3':
                songs = songs.filter(daily_rotation__isnull=True)
        if 'is_event' in request.GET and request.GET['is_event']:
            if request.GET['is_event'] == '2':
                songs = songs.filter(event__isnull=False)
            elif request.GET['is_event'] == '3':
                songs = songs.filter(event__isnull=True)
        if 'available' in request.GET and request.GET['available']:
            if request.GET['available'] == '2':
                songs = songs.filter(available=True)
            elif request.GET['available'] == '3':
                songs = songs.filter(available=False)

        reverse = ('reverse_order' in request.GET and request.GET['reverse_order']) or not request.GET or len(request.GET) == 1
        ordering = request.GET['ordering'] if 'ordering' in request.GET and request.GET['ordering'] else 'id'
        prefix = '-' if reverse else ''
        if ordering == 'latest':
            songs = songs.order_by('-available', 'daily_rotation', 'daily_rotation_position', prefix + 'rank', 'name')
        else:
            songs = songs.order_by(prefix + ordering)
        songs = songs.select_related('event')

        context['total_results'] = songs.count()

        page_size = 12
        if 'page' in request.GET and request.GET['page']:
            page = int(request.GET['page']) - 1
            if page < 0:
                page = 0
        songs = songs.distinct()
        songs = songs.select_related('performer', 'parent')[(page * page_size):((page * page_size) + page_size)]
        context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
        context['page'] = page + 1
        context['page_size'] = page_size
    else:
        context['total_results'] = 1
        songs = [get_object_or_404(models.Song, name=song)]
        context['single'] = songs[0]

    context['show_filter_button'] = False if 'single' in context and context['single'] else True
    context['songs'] = songs
    if len(request.GET) > 1 or (len(request.GET) == 1 and 'page' not in request.GET):
        context['filter_form'] = forms.FilterSongForm(request.GET)
    else:
        context['filter_form'] = forms.FilterSongForm()
    context['current'] = 'songs'
    context['show_no_result'] = not ajax
    context['show_search_results'] = bool(request.GET)

    cardsinfo = settings.CARDS_INFO
    max_stats = cardsinfo['songs_max_stats']
    for song in songs:
        song.length = time.strftime('%M:%S', time.gmtime(song.time))
        song.percent_stats = collections.OrderedDict()
        song.percent_stats['easy'] = ((song.easy_notes if song.easy_notes else 0) / max_stats) * 100
        song.percent_stats['normal'] = ((song.normal_notes if song.normal_notes else 0) / max_stats) * 100
        song.percent_stats['hard'] = ((song.hard_notes if song.hard_notes else 0) / max_stats) * 100
        song.percent_stats['expert'] = ((song.expert_notes if song.expert_notes else 0) / max_stats) * 100
        song.percent_stats['expert_random'] = ((song.expert_notes if song.expert_notes else 0) / max_stats) * 100
    context['max_stats'] = max_stats

    context['ajax'] = ajax
    if ajax:
        return render(request, 'songsPage.html', context)
    return render(request, 'songs.html', context)

def ajaxsongs(request):
    return songs(request, ajax=True)

def trivia(request):
    context = globalContext(request)
    context['total_backgrounds'] = settings.TOTAL_BACKGROUNDS
    return render(request, 'trivia.html', context)

@csrf_exempt
def sharetrivia(request):
    if request.method == 'POST' and 'score' in request.POST:
        if not request.user.is_authenticated():
            return redirect('/create/')
        accounts = contextAccounts(request, with_center=True)
        try:
            activity = pushActivity('Trivia', account=accounts[0], account_owner=request.user, number=request.POST['score'], message_data=models.triviaScoreToSentence(int(request.POST['score'])))
            return redirect('/activities/' + str(activity.pk) + '/')
        except IndexError:
            return redirect('/addaccount/')
    raise PermissionDenied()
