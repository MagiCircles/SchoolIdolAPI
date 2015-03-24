from __future__ import division
import math
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.forms.models import model_to_dict
from api import models
from web import forms, links
import urllib, hashlib
import datetime
import random
import json

def globalContext(request):
    context ={
        'hide_back_button': False,
        'show_filter_button': False,
        'current_url': request.get_full_path() + ('?' if request.get_full_path()[-1] == '/' else '&'),
        'interfaceColor': 'default',
        'debug': settings.DEBUG,
    }
    if request.user.is_authenticated and not request.user.is_anonymous():
        context['accounts'] = request.user.accounts_set.all().select_related('center')
        session_preferences = request.session.get('preferences')
        if not session_preferences:
            preferences, created = request.user.preferences.get_or_create()
            request.session['preferences'] = model_to_dict(preferences)
            request.session['preferences']['following'] = [f.username for f in preferences.following.all()]
        context['session_preferences'] = request.session['preferences']
        context['interfaceColor'] = context['session_preferences']['color']
    active_account_id = request.session.get('active_account')
    if active_account_id:
        for account in context['accounts']:
            if account.pk == active_account_id:
                context['active_account'] = account
    if not 'active_account' in context and 'accounts' in context and context['accounts']:
        active_account = context['accounts'][0]
        request.session['active_account'] = active_account
        context['active_account'] = active_account
    return context

def getUserPreferencesAvatar(user, preferences, size):
    default = 'http://schoolido.lu/static/kotori.jpg'
    if preferences.twitter:
        default = 'http://avatars.io/twitter/' + preferences.twitter + '?size=large'
    elif preferences.facebook:
        default = 'http://avatars.io/facebook/' + preferences.facebook + '?size=large'
    return ("http://www.gravatar.com/avatar/"
            + hashlib.md5(user.email.lower()).hexdigest()
            + "?" + urllib.urlencode({'d': default, 's': str(size)}))

def getUserAvatar(user, size):
    preferences, created = user.preferences.get_or_create()
    return getUserPreferencesAvatar(user, preferences, size)

def pushActivity(account, message, rank=None, ownedcard=None, eventparticipation=None):
    models.Activity.objects.create(account=account, message=message, rank=rank, ownedcard=ownedcard, eventparticipation=eventparticipation)

def index(request):
    context = globalContext(request)
    context['hide_back_button'] = True

    # Get current events
    current_jp = models.Event.objects.order_by('-beginning')[0]
    current_en = models.Event.objects.filter(beginning__lte=(datetime.date.today() - relativedelta(years=1))).order_by('-beginning')[0]
    context['links'] = links.get_links(current_en, current_jp)
    context['links']
    for link in context['links']:
        link['card'] = models.Card.objects.filter(name=link['idol']).filter(Q(rarity='SR') | Q(rarity='UR')).order_by('?')[0]
        link['card'].idolized = bool(random.getrandbits(1)) if link['card'].card_url else 1
    context['links1'] = enumerate(context['links'])
    context['links2'] = enumerate(context['links'])
    context['links3'] = enumerate(context['links'])
    context['links'] = enumerate(context['links'])
    return render(request, 'index.html', context)

def create(request):
    if request.user.is_authenticated and not request.user.is_anonymous():
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/addaccount')
    else:
        form = forms.UserForm()
    context = globalContext(request)
    context['form'] = form
    context['current'] = 'create'
    return render(request, 'create.html', context)

def setaccountonlogin(request):
    context = globalContext(request)
    try:
        account = next(iter(context['accounts']))
    except StopIteration:
        return redirect('addaccount')
    request.session['active_account'] = account.pk
    return redirect('cards')

def switchaccount(request, account):
    context = globalContext(request)
    account_id = int(account)
    for account in context['accounts']:
        if account.pk == account_id:
            request.session['active_account'] = account.pk
            break
    return redirect('cards')

def cards(request, card=None, ajax=False):

    page = 0
    context = globalContext(request)
    context['total_results'] = 0

    f = open('cardsinfo.json', 'r')
    cardsinfo = json.load(f)
    f.close()
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
                cards = cards.filter(Q(name__contains=request.GET['search'])
                                     | Q(idol__japanese_name__contains=request.GET['search'])
                                     | Q(skill__contains=request.GET['search'])
                                     | Q(japanese_skill__contains=request.GET['search'])
                                     | Q(skill_details__contains=request.GET['search'])
                                     | Q(japanese_skill_details__contains=request.GET['search'])
                                     | Q(center_skill__contains=request.GET['search'])
                                     | Q(japanese_center_skill__contains=request.GET['search'])
                                     | Q(japanese_center_skill_details__contains=request.GET['search'])
                                     | Q(japanese_collection__contains=request.GET['search'])
                                     | Q(promo_item__contains=request.GET['search'])
                                     | Q(event__english_name__contains=request.GET['search'])
                                     | Q(event__japanese_name__contains=request.GET['search'])
                )
        if 'name' in request.GET and request.GET['name']:
            cards = cards.filter(name__exact=request.GET['name'])
            request_get['name'] = request.GET['name']
        if 'collection' in request.GET and request.GET['collection']:
            cards = cards.filter(japanese_collection__exact=request.GET['collection'])
            request_get['collection'] = request.GET['collection']
        if 'rarity' in request.GET and request.GET['rarity']:
            cards = cards.filter(rarity__exact=request.GET['rarity'])
            request_get['rarity'] = request.GET['rarity']
        if 'attribute' in request.GET and request.GET['attribute']:
            cards = cards.filter(attribute__exact=request.GET['attribute'])
            request_get['attribute'] = request.GET['attribute']
        if 'skill' in request.GET and request.GET['skill']:
            cards = cards.filter(skill__exact=request.GET['skill'])
            request_get['skill'] = request.GET['skill']
        if 'is_promo' in request.GET and request.GET['is_promo']:
            cards = cards.filter(is_promo__exact=True)
            request_get['is_promo'] = request.GET['is_promo']
        if 'is_special' in request.GET and request.GET['is_special']:
            cards = cards.filter(is_special__exact=True)
            request_get['is_special'] = request.GET['is_special']
        if 'is_event' in request.GET and request.GET['is_event']:
            cards = cards.filter(event__isnull=False)
            request_get['is_event'] = request.GET['is_event']
        if 'active_account' in context and 'max_level' in request.GET and request.GET['max_level'] == '1':
            cards = cards.filter(ownedcards__owner_account=context['active_account'],
                                 ownedcards__max_level=True)
            request_get['max_level'] = '1'
        elif 'active_account' in context and 'max_level' in request.GET and request.GET['max_level'] == '-1':
            cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=context['active_account'], max_level=True).values('card'))
            request_get['max_level'] = '-1'
        if 'active_account' in context and 'max_bond' in request.GET and request.GET['max_bond'] == '1':
            cards = cards.filter(ownedcards__owner_account=context['active_account'],
                                 ownedcards__max_bond=True)
            request_get['max_bond'] = '1'
        elif 'active_account' in context and 'max_bond' in request.GET and request.GET['max_bond'] == '-1':
            cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=context['active_account'], max_bond=True).values('card'))
            request_get['max_bond'] = '-1'
        if 'active_account' in context and 'idolized' in request.GET and request.GET['idolized'] == '1':
            cards = cards.filter(ownedcards__owner_account=context['active_account'],
                                 ownedcards__idolized=True).exclude(ownedcards__stored='Favorite')
            request_get['idolized'] = '1'
        elif 'active_account' in context and 'idolized' in request.GET and request.GET['idolized'] == '-1':
            cards = cards.exclude(id__in=models.OwnedCard.objects.filter(owner_account=context['active_account'], idolized=True).exclude(stored='Favorite').values('card'))
            request_get['idolized'] = '-1'

        if 'active_account' in context and 'stored' in request.GET and request.GET['stored']:
            if request.GET['stored'] == 'Album':
                cards = cards.filter(ownedcards__owner_account=context['active_account']).filter(Q(ownedcards__stored='Deck') | Q(ownedcards__stored='Album'))
            else:
                cards = cards.filter(ownedcards__owner_account=context['active_account'], ownedcards__stored=request.GET['stored'])
            cards = cards.distinct()
            request_get['stored'] = request.GET['stored']

        if ('active_account' in context and context['active_account'].language != 'JP'
            and 'search' not in request.GET or 'is_world' in request.GET and request.GET['is_world']):
            cards = cards.filter(Q(release_date__isnull=True) | Q(release_date__lte=(datetime.date.today() - relativedelta(years=1) + relativedelta(days=2)))).exclude(is_promo__exact=True, video_story__isnull=True).exclude(is_special__exact=True, id__gte=379)
            request_get['is_world'] = True

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
        cards = cards.select_related('event', 'idol')[(page * page_size):((page * page_size) + page_size)]
        context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    else:
        context['total_results'] = 1
        cards = [get_object_or_404(models.Card, id=int(card))]
        context['single'] = cards[0]

    # Get statistics & other information to show in cards
    for card in cards:
        card.japan_only = card.is_japan_only()
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
        if 'active_account' in context:
            card.owned_cards = card.get_owned_cards_for_account(context['active_account'])
        else:
            card.owned_cards = []

    if not ajax:
       # Get filters info for the form
        context['filters'] = {
            'idols': cardsinfo['idols'],
            'collections': cardsinfo['collections'],
            'skills': cardsinfo['skills'],
            'rarity_choices': models.RARITY_CHOICES,
            'attribute_choices': models.ATTRIBUTE_CHOICES,
            'stored_choices': models.STORED_CHOICES,
            'ordering_choices': (
                ('id', _('Card #ID')),
                ('release_date', _('Release date')),
                ('name', _('Idol')),
                ('idolized_maximum_statistics_smile', _('Smile\'s statistics')),
                ('idolized_maximum_statistics_pure', _('Pure\'s statistics')),
                ('idolized_maximum_statistics_cool', _('Cool\'s statistics')),
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
    context['show_filter_bar'] = True if request.GET else False
    if 'search' not in request_get and 'name' in request_get:
        context['show_filter_bar'] = False
    context['current'] = 'cards'
    context['addcard_form'] = forms.OwnedCardForm()
    context['page'] = page + 1
    context['ajax'] = ajax
    if ajax:
        return render(request, 'cardsPage.html', context)
    return render(request, 'cards.html', context)

def addaccount(request):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            # account = models.Account.objects.create(form.cleaned_data)
            request.session['active_account'] = account.pk
            return redirect('cards')
    else:
        form = forms.AccountForm(initial={
            'nickname': request.user.username
        })
    context = globalContext(request)
    context['form'] = form
    context['current'] = 'addaccount'
    return render(request, 'addaccount.html', context)

def profile(request, username):
    context = globalContext(request)
    user = get_object_or_404(User, username=username)
    context['profile_user'] = user
    context['preferences'], created = user.preferences.get_or_create()
    if user == request.user:
        context['is_me'] = True
        context['user_accounts'] = context['accounts']
    else:
        context['is_me'] = False
        context['user_accounts'] = user.accounts_set.all()
    if not context['preferences'].private or context['is_me']:
        for account in context['user_accounts']:
            account.deck = account.ownedcards.filter(stored='Deck').select_related('card').order_by('-card__rarity', '-idolized', '-max_level', '-max_bond', 'card__id')
            account.deck_total_sr = sum(card.card.rarity == 'SR' for card in account.deck)
            account.deck_total_ur = sum(card.card.rarity == 'UR' for card in account.deck)
    context['current'] = 'profile'
    context['avatar'] = getUserPreferencesAvatar(user, context['preferences'], 200)
    context['following'] = isFollowing(user, context)
    context['total_following'] = context['preferences'].following.count()
    context['total_followers'] = user.followers.count()
    return render(request, 'profile.html', context)

def ajaxownedcards(request, account, stored):
    if stored not in models.STORED_DICT:
        raise Http404
    account = get_object_or_404(models.Account, pk=account)
    if account.owner.username != request.user.username and (account.owner.preferences.get_or_create()[0].private or stored == 'Box'):
        raise PermissionDenied()
    ownedcards = account.ownedcards.filter()
    if stored == 'Album':
        ownedcards = ownedcards.filter(Q(stored='Album') | Q(stored='Deck')).order_by('card__id')
    else:
        ownedcards = ownedcards.filter(stored=stored)
        if stored == 'Box':
            ownedcards = ownedcards.order_by('card__id')
        elif stored == 'Favorite':
            ownedcards == ownedcards.order_by('-card__rarity', '-idolized', 'card__id')
    context = { 'cards': ownedcards, 'nolink': True, 'stored': stored }
    return render(request, 'ownedcards.html', context)

def ajaxaddcard(request):
    context = globalContext(request)
    if request.method != 'POST' or not context['active_account']:
        raise PermissionDenied()
    form = forms.OwnedCardForm(request.POST)
    if form.is_valid():
        ownedcard = form.save(commit=False)
        if form.cleaned_data['stored'] == 'Box' and 'expires_in' in request.POST:
            try: expires_in = int(request.POST['expires_in'])
            except (TypeError, ValueError): expires_in = 0
            if expires_in < 0: expires_in = 0
            if expires_in:
                ownedcard.expiration = datetime.date.today() + relativedelta(days=expires_in)
        ownedcard.owner_account = context['active_account']
        ownedcard.save()
        context['owned'] = ownedcard
        pushActivity(account=context['active_account'],
                     message="Added a card",
                     ownedcard=ownedcard)
        return render(request, 'ownedCardOnBottomCard.html', context)
    form = forms.OwnedCardForm(initial={
        'card': request.POST['card']
    })
    context['addcard_form'] = form
    return render(request, 'addCardForm.html', context)

def ajaxeditcard(request, ownedcard):
    context = globalContext(request)
    if 'active_account' not in context:
        raise PermissionDenied()
    try:
        owned_card = models.OwnedCard.objects.get(pk=int(ownedcard), owner_account=context['active_account'])
    except ObjectDoesNotExist:
        raise PermissionDenied()
    if request.method == 'GET':
        form = forms.OwnedCardForm(instance=owned_card)
    elif request.method == 'POST':
        (was_idolized, was_max_leveled, was_max_bonded) = (owned_card.idolized, owned_card.max_level, owned_card.max_bond)
        form = forms.OwnedCardForm(request.POST, instance=owned_card)
        if form.is_valid():
            ownedcard = form.save(commit=False)
            if form.cleaned_data['stored'] == 'Box' and 'expires_in' in request.POST:
                try: expires_in = int(request.POST['expires_in'])
                except (TypeError, ValueError): expires_in = 0
                if expires_in < 0: expires_in = 0
                if expires_in:
                    ownedcard.expiration = datetime.date.today() + relativedelta(days=expires_in)
            ownedcard.owner_account = owned_card.owner_account # owner & card change not allowed
            ownedcard.card = owned_card.card
            ownedcard.save()
            context['owned'] = ownedcard
            if not was_idolized and ownedcard.idolized:
                pushActivity(ownedcard.owner_account, "Idolized a card", ownedcard=ownedcard)
            if not was_max_leveled and ownedcard.max_level:
                pushActivity(ownedcard.owner_account, "Max Leveled a card", ownedcard=ownedcard)
            if not was_max_bonded and ownedcard.max_bond:
                pushActivity(ownedcard.owner_account, "Max Bonded a card", ownedcard=ownedcard)
            return render(request, 'ownedCardOnBottomCard.html', context)
    else:
        raise PermissionDenied()
    if owned_card.expiration:
         owned_card.expires_in = (owned_card.expiration - timezone.now()).days
    context['addcard_form'] = form
    context['edit'] = owned_card
    return render(request, 'addCardForm.html', context)

def ajaxdeletecard(request, ownedcard):
    context = globalContext(request)
    if 'active_account' not in context:
        raise PermissionDenied()
    try:
        owned_card = models.OwnedCard.objects.get(pk=int(ownedcard), owner_account=context['active_account'])
    except ObjectDoesNotExist:
        raise PermissionDenied()
    owned_card.delete()
    return HttpResponse('')

def ajaxcards(request):
    return cards(request, ajax=True)

def ajaxusers(request):
    return users(request, ajax=True)

def isFollowing(user, context): # must have globalContext
    if 'session_preferences' in context:
        for followed in context['session_preferences']['following']:
            if followed == user.username:
                return True
    return False

def _ajaxfollowcontext(follow):
    for user in follow:
        user.prefs, created = user.preferences.get_or_create()
        user.avatar = getUserPreferencesAvatar(user, user.prefs, 100)
    return { 'follow': follow }

def ajaxfollowers(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'followlist.html', _ajaxfollowcontext([p.user for p in user.followers.all()]))

def ajaxfollowing(request, username):
    preferences = get_object_or_404(models.UserPreferences, user__username=username)
    return render(request, 'followlist.html', _ajaxfollowcontext(preferences.following.all()))

def _activities(request, account=None, follower=None, avatar_size=3):
    page = 0
    page_size = 25
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    activities = models.Activity.objects.all().order_by('-creation')
    if account is not None:
        activities = activities.filter(account=account)
    if follower is not None:
        follower = get_object_or_404(User, username=follower)
        preferences, created = follower.preferences.get_or_create()
        accounts = models.Account.objects.filter(owner__in=preferences.following.all())
        activities = activities.filter(account__in=accounts)
    total = activities.count()
    activities = activities[(page * page_size):((page * page_size) + page_size)]
    for activity in activities:
        activity.account.owner.avatar = getUserAvatar(activity.account.owner, 100)
    context = {
        'activities': activities,
        'page': page + 1,
        'page_size': page_size,
        'avatar_size': avatar_size,
        'content_size': 12 - avatar_size,
        'total_results': total,
        'current': 'activities',
    }
    return context

def ajaxactivities(request):
    account = int(request.GET['account']) if 'account' in request.GET and request.GET['account'] and request.GET['account'].isdigit() else None
    follower = request.GET['follower'] if 'follower' in request.GET and request.GET['follower'] else None
    avatar_size = int(request.GET['avatar_size']) if 'avatar_size' in request.GET and request.GET['avatar_size'] and request.GET['avatar_size'].isdigit() else 3
    return render(request, 'activities.html', _activities(request, account=account, follower=follower, avatar_size=avatar_size))

def _contextfeed(request):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    return _activities(request, follower=request.user, avatar_size=2)

def ajaxfeed(request):
    return render(request, 'activities.html', _contextfeed(request))

def activities(request):
    context = globalContext(request)
    context.update(_contextfeed(request))
    return render(request, 'feed.html', context)

@csrf_exempt
def ajaxfollow(request, username):
    context = globalContext(request)
    if (not request.user.is_authenticated or request.user.is_anonymous()
        or request.method != 'POST' or request.user.username == username):
        raise PermissionDenied()
    user = get_object_or_404(User, username=username)
    if 'follow' in request.POST and not isFollowing(user, context):
        preferences, created = request.user.preferences.get_or_create()
        preferences.following.add(user)
        preferences.save()
        del request.session['preferences']
        return HttpResponse('followed')
    if 'unfollow' in request.POST and isFollowing(user, context):
        preferences, created = request.user.preferences.get_or_create()
        preferences.following.remove(user)
        preferences.save()
        del request.session['preferences']
        return HttpResponse('unfollowed')
    raise PermissionDenied()

def ajaxeventparticipations(request, account):
    eventparticipations = models.EventParticipation.objects.filter(account=account).order_by('-event__end')
    return render(request, 'ajaxevents.html', { 'eventparticipations': eventparticipations })

def ajaxmodal(request, hash):
    context = {}
    if 'interfaceColor' in request.GET:
        context['interfaceColor'] = request.GET['interfaceColor']
    if hash == 'about':
        return render(request, 'modalabout.html', context)
    elif hash == 'developers':
        return render(request, 'modaldevelopers.html', context)
    elif hash == 'contact':
        return render(request, 'modalcontact.html', context)
    elif hash == 'donate':
        return render(request, 'modaldonate.html', context)
    elif hash == 'thanks':
        return render(request, 'modalthanks.html', context)
    raise Http404

def edit(request):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    context['preferences'], created = models.UserPreferences.objects.get_or_create(user=request.user)
    form = forms.UserForm(instance=request.user)
    form_preferences = forms.UserPreferencesForm(instance=context['preferences'])
    if request.method == "POST":
        if 'editPreferences' in request.POST:
            form_preferences = forms.UserPreferencesForm(request.POST, instance=context['preferences'])
            old_location = context['preferences'].location
            if form_preferences.is_valid():
                prefs = form_preferences.save(commit=False)
                if old_location != prefs.location:
                    prefs.location_changed = True
                prefs.save()
                request.session['preferences'] = model_to_dict(form_preferences.instance)
                return redirect('/user/' + request.user.username)
        else:
            form = forms.UserForm(request.POST, instance=request.user)
            if form.is_valid():
                edited_user = form.save(commit=False)
                edited_user.set_password(form.cleaned_data['password'])
                edited_user.save()
                return redirect('/login/')
    context['form'] = form
    context['form_preferences'] = form_preferences
    context['current'] = 'edit'
    return render(request, 'edit.html', context)

def editaccount(request, account):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    account = int(account)
    for owned_account in context['accounts']:
        if account == owned_account.pk:
            if request.method == 'GET':
                form = forms.FullAccountForm(instance=owned_account)
            elif request.method == "POST":
                if 'deleteAccount' in request.POST:
                    owned_account.delete()
                    return redirect('/user/' + request.user.username)
                old_rank = owned_account.rank
                form = forms.FullAccountForm(request.POST, instance=owned_account)
                if form.is_valid():
                    account = form.save()
                    if old_rank < account.rank:
                        pushActivity(account, "Rank Up", rank=account.rank)
                    return redirect('/user/' + request.user.username)
            form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=owned_account, stored='Deck').order_by('card__id')
            context['form'] = form
            context['current'] = 'editaccount'
            context['edit'] = owned_account
            return render(request, 'addaccount.html', context)
    raise PermissionDenied()

def users(request, ajax=False):
    if ajax:
        context = {}
    else:
        context = globalContext(request)
    page = 0
    page_size = 18
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    users = User.objects.all()
    flag = False
    if request.GET:
        form = forms.UserSearchForm(request.GET)
        if form.is_valid():
            if 'term' in form.cleaned_data and form.cleaned_data['term']:
                terms = request.GET['term'].split(' ')
                for term in terms:
                    if term.isdigit():
                        users = users.filter(Q(accounts_set__rank__exact=term)
                                             | Q(accounts_set__friend_id__exact=term)
                                         )
                    else:
                        users = users.filter(Q(username__contains=term)
                                             | Q(preferences__description__contains=term)
                                             | Q(preferences__location__contains=term)
                                             | Q(preferences__twitter__contains=term)
                                             | Q(preferences__facebook__contains=term)
                                             | Q(email__exact=term)
                                             | Q(preferences__reddit__contains=term)
                                             | Q(preferences__line__contains=term)
                                             | Q(preferences__tumblr__contains=term)
                                             | Q(accounts_set__nickname__contains=term)
                                         )
            if 'ordering' in form.cleaned_data and form.cleaned_data['ordering']:
                flag = True
                users = users.order_by(form.cleaned_data['ordering'])
    else:
        form = forms.UserSearchForm()
    if not flag:
        users = users.order_by('-accounts_set__rank')
    context['form'] = form
    context['total_results'] = users.count()
    users = users[(page * page_size):((page * page_size) + page_size)]
    for user in users:
        preferences, created = user.preferences.get_or_create()
        user.prefs = preferences
        user.avatar = getUserPreferencesAvatar(user, user.prefs, 100)
        user.accounts = user.accounts_set.all().order_by('-rank')
    context['total_users'] = len(users)
    context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    context['users'] = users
    context['page'] = page + 1
    return render(request, 'usersPage.html' if ajax else 'users.html', context)

def events(request):
    context = globalContext(request)
    events = models.Event.objects.all().order_by('-end')
    context['events'] = events
    return render(request, 'events.html', context)

def _event_valid_form(form, context, event, old_ranking=None):
    if form.is_valid():
        participation = form.save(commit=False)
        participation.account = context['active_account']
        participation.event = event
        participation.save()
        if (participation.ranking is not None
            and old_ranking is None
            or old_ranking < participation.ranking):
            pushActivity(context['active_account'], 'Ranked in event', eventparticipation=participation)
        return redirect(context['current_url'])

def event(request, event):
    context = globalContext(request)
    event = get_object_or_404(models.Event, japanese_name=event)

    if 'Score Match' in event.japanese_name or 'Medley Festival' in event.japanese_name:
        formClass = forms.EventParticipationNoSongForm
    else:
        formClass = forms.EventParticipationForm
        context['with_song'] = True
    if request.user.is_authenticated and not request.user.is_anonymous() and 'active_account' in context:
        try:
            participation = event.participations.get(event=event, account=context['active_account'])
            old_ranking = participation.ranking
            context['form_type'] = 'edit'
            if request.method == 'POST':
                if 'deleteParticipation' in request.POST:
                    participation.delete()
                    return redirect('/event/' + unicode(event.japanese_name))
                form = formClass(request.POST, instance=participation)
                return _event_valid_form(form, context, event, old_ranking)
            else:
                form = formClass(instance=participation)
            context['form'] = form
        except models.EventParticipation.DoesNotExist:
            context['form_type'] = 'create'
            if request.method == 'POST':
                form = formClass(request.POST)
                return _event_valid_form(form, context, event)
            else:
                form = formClass()
            context['form'] = form
    else:
        context['form_type'] = 'none'

    event.all_cards = event.cards.all()
    event.all_participations = event.participations.all().order_by('account__language', 'ranking')
    context['event'] = event
    return render(request, 'event.html', context)

def idols(request):
    context = globalContext(request)
    context['main_idols'] = models.Idol.objects.filter(main=True).order_by('year', 'name')
    context['n_idols'] = models.Idol.objects.filter(main=False).order_by('name')
    for idol in context['n_idols']:
        idol.card = idol.cards.all().order_by('?')[0]
    return render(request, 'idols.html', context)

def twitter(request):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    context['twitter'] = models.UserPreferences.objects.filter(twitter__isnull=False).exclude(twitter__exact='').values_list('twitter', flat=True)
    return render(request, 'twitter.html', context)

def mapview(request):
    context = globalContext(request)
    context['map'] = models.UserPreferences.objects.filter(latitude__isnull=False).select_related('user')
    if request.user.is_authenticated and not request.user.is_anonymous():
        if context['session_preferences']['latitude']:
            context['you'] = context['session_preferences']
    return render(request, 'map.html', context)
