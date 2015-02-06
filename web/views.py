from __future__ import division
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from api import models
from web import forms, links

import datetime
import random

def globalContext(request):
    context ={
        'hide_back_button': False,
        'show_filter_button': False,
    }
    if request.user.is_authenticated and not request.user.is_anonymous():
        context['accounts'] = models.Account.objects.filter(owner=request.user)
    active_account_id = request.session.get('active_account')
    if active_account_id:
        for account in context['accounts']:
            if account.pk == active_account_id:
                context['active_account'] = account
    if not 'active_account' in context and 'accounts' in context and context['accounts']:
        context['active_account'] = context['accounts'][0]
    return context

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

    # Set defaults
    request_get = {
        'ordering': 'release_date',
        'reverse_order': True,
    }

    if card is None:
        # Apply filters
        cards = models.Card.objects.filter()
        if 'search' in request.GET and request.GET['search']:
            cards = cards.filter(Q(name__contains=request.GET['search'])
                                 | Q(japanese_name__contains=request.GET['search'])
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
            request_get['search'] = request.GET['search']
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
        if 'active_account' in context and 'stored' in request.GET and request.GET['stored']:
            if request.GET['stored'] == 'Album':
                cards = cards.filter(ownedcard__owner_account=context['active_account']).filter(Q(ownedcard__stored='Deck') | Q(ownedcard__stored='Album'))
            else:
                cards = cards.filter(ownedcard__owner_account=context['active_account'], ownedcard__stored=request.GET['stored'])
            request_get['stored'] = request.GET['stored']
        if 'active_account' in context and 'max_level' in request.GET and request.GET['max_level'] == '1':
            cards = cards.filter(ownedcard__owner_account=context['active_account'],
                                 ownedcard__max_level=True)
            request_get['max_level'] = '1'
        elif 'active_account' in context and 'max_level' in request.GET and request.GET['max_level'] == '-1':
            cards = cards.exclude(ownedcard__owner_account=context['active_account'], ownedcard__max_level=True)
            request_get['max_level'] = '-1'
        if 'active_account' in context and 'max_bond' in request.GET and request.GET['max_bond'] == '1':
            cards = cards.filter(ownedcard__owner_account=context['active_account'],
                                 ownedcard__max_bond=True)
            request_get['max_bond'] = 1
        elif 'active_account' in context and 'max_bond' in request.GET and request.GET['max_bond'] == '-1':
            cards = cards.exclude(ownedcard__owner_account=context['active_account'], ownedcard__max_bond=True)
            request_get['max_bond'] = '-1'
        if 'active_account' in context and 'idolized' in request.GET and request.GET['idolized'] == '1':
            cards = cards.filter(ownedcard__owner_account=context['active_account'],
                                 ownedcard__idolized=True)
            request_get['idolized'] = 1
        elif 'active_account' in context and 'idolized' in request.GET and request.GET['idolized'] == '-1':
            cards = cards.exclude(ownedcard__owner_account=context['active_account'], ownedcard__idolized=True)
            request_get['idolized'] = '-1'

        if ('active_account' in context and context['active_account'].language != 'JP'
            and 'search' not in request.GET or 'is_world' in request.GET and request.GET['is_world']):
            cards = cards.filter(is_promo__exact=False, release_date__lte=(datetime.date.today() - relativedelta(years=1)))
            request_get['is_world'] = True

        if 'ordering' in request.GET and request.GET['ordering']:
            request_get['ordering'] = request.GET['ordering']
            request_get['reverse_order'] = 'reverse_order' in request.GET and request.GET['reverse_order']
        cards = cards.order_by(('-' if request_get['reverse_order'] else '') + request_get['ordering'])

        # Set limit
        page_size = 9
        if 'page' in request.GET and request.GET['page']:
            page = int(request.GET['page']) - 1
            if page < 0:
                page = 0
        cards = cards[(page * page_size):((page * page_size) + page_size)]
    else:
        cards = [get_object_or_404(models.Card, id=int(card))]
        context['single'] = cards[0]

    # Get statistics & other information to show in cards
    max_stats = {
        'Smile': models.Card.objects.order_by('-idolized_maximum_statistics_smile')[:1][0].idolized_maximum_statistics_smile,
        'Pure': models.Card.objects.order_by('-idolized_maximum_statistics_pure')[:1][0].idolized_maximum_statistics_pure,
        'Cool': models.Card.objects.order_by('-idolized_maximum_statistics_cool')[:1][0].idolized_maximum_statistics_cool,
        }
    for card in cards:
        card.japan_only = card.is_japan_only()
        card.percent_stats = {
            'minimum': {
                'Smile': (card.minimum_statistics_smile / max_stats['Smile']) * 100,
                'Pure': (card.minimum_statistics_pure / max_stats['Pure']) * 100,
                'Cool': (card.minimum_statistics_cool / max_stats['Cool']) * 100,
            }, 'non_idolized_maximum': {
                'Smile': (card.non_idolized_maximum_statistics_smile / max_stats['Smile']) * 100,
                'Pure': (card.non_idolized_maximum_statistics_pure / max_stats['Pure']) * 100,
                'Cool': (card.non_idolized_maximum_statistics_cool / max_stats['Cool']) * 100,
            }, 'idolized_maximum': {
                'Smile': (card.idolized_maximum_statistics_smile / max_stats['Smile']) * 100,
                'Pure': (card.idolized_maximum_statistics_pure / max_stats['Pure']) * 100,
                'Cool': (card.idolized_maximum_statistics_cool / max_stats['Cool']) * 100,
            }
        }
        if 'active_account' in context:
            card.owned_cards = card.get_owned_cards_for_account(context['active_account'])
        else:
            card.owned_cards = []

    if not ajax:
       # Get filters info for the form
        context['filters'] = {
            'idols': models.Card.objects.values('name').annotate(total=Count('name')).order_by('-total', 'name'),
            'collections': models.Card.objects.filter(japanese_collection__isnull=False).exclude(japanese_collection__exact='').values('japanese_collection').annotate(total=Count('name')).order_by('-total', 'japanese_collection'),
            'skills': models.Card.objects.filter(skill__isnull=False).values('skill').annotate(total=Count('skill')).order_by('-total'),
            'rarity_choices': models.RARITY_CHOICES,
            'attribute_choices': models.ATTRIBUTE_CHOICES,
            'stored_choices': models.STORED_CHOICES,
            'ordering_choices': (
                ('release_date', 'Release date'),
                ('id', 'Card #ID'),
                ('name', 'Idol\'s names'),
                ('idolized_maximum_statistics_smile', 'Smile\'s statistics'),
                ('idolized_maximum_statistics_pure', 'Pure\'s statistics'),
                ('idolized_maximum_statistics_cool', 'Cool\'s statistics'),
                ('hp', 'HP')
            )
        }

    context['total_cards'] = len(cards)
    context['cards'] = enumerate(cards)
    context['max_stats'] = max_stats
    context['show_filter_button'] = False if 'single' in context and context['single'] else True
    context['request_get'] = request_get
    context['show_filter_bar'] = True if request.GET else False
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
    if user == request.user:
        context['is_me'] = True
        context['user_accounts'] = context['accounts']
    else:
        context['is_me'] = False
        context['user_accounts'] = models.Account.objects.filter(owner=user)
    for account in context['user_accounts']:
        account.deck = models.OwnedCard.objects.filter(owner_account=account, stored='Deck').order_by('-card__rarity', '-idolized', '-max_level', '-max_bond', 'card__id')
        account.deck_total_sr = sum(card.card.rarity == 'SR' for card in account.deck)
        account.deck_total_ur = sum(card.card.rarity == 'UR' for card in account.deck)
        account.album = models.OwnedCard.objects.filter(owner_account=account).filter((Q(stored='Album') | Q(stored='Deck'))).order_by('card__id')
        if context['is_me']:
            account.box = models.OwnedCard.objects.filter(owner_account=account, stored='Box').order_by('card__id')
        account.favorite = models.OwnedCard.objects.filter(owner_account=account, stored='Favorite').order_by('card__id')
    context['current'] = 'profile'
    return render(request, 'profile.html', context)

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

def edit(request):
    if not request.user.is_authenticated or request.user.is_anonymous():
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.UserForm(request.POST, instance=request.user)
        if form.is_valid():
            edited_user = form.save(commit=False)
            edited_user.set_password(form.cleaned_data['password'])
            edited_user.save()
            return redirect('/login/')
    else:
        form = forms.UserForm(instance=request.user)
    context = globalContext(request)
    context['form'] = form
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
                form = forms.FullAccountForm(request.POST, instance=owned_account)
                if form.is_valid():
                    account = form.save()
                    return redirect('/user/' + request.user.username)
            form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=owned_account, stored='Deck').order_by('card__id')
            context['form'] = form
            context['current'] = 'editaccount'
            context['edit'] = owned_account
            return render(request, 'addaccount.html', context)
    raise PermissionDenied()

def users(request):
    context = globalContext(request)
    page = 0
    page_size = 9
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    users = User.objects.all().order_by('-last_login')[(page * page_size):((page * page_size) + page_size)]
    for user in users:
        user.accounts = models.Account.objects.filter(owner=user)
    context['total_users'] = len(users)
    context['users'] = enumerate(users)
    return render(request, 'users.html', context)
