from django.shortcuts import render, get_object_or_404, redirect
import contest.models as contest_models
from django.db.models import Sum
from django.conf import settings
from contest.utils import (get_votesession, validate_vote,
                           best_girls_query, best_cards_query,
                           best_single_cards, past_contests_queryset,
                           get_current_contest, is_current_contest)
from web.views import globalContext as web_globalContext
from web.templatetags.mod import tourldash
import datetime

def globalContext(request):
    context = web_globalContext(request)
    context.update({
        'total_backgrounds': settings.TOTAL_BACKGROUNDS,
        'global_contest_id': settings.GLOBAL_CONTEST_ID,
    })
    return context

def contest_view(request, contestid):
    context = globalContext(request)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    if not is_current_contest(contest):
       return redirect('/contest/result/' + contestid + '/' + tourldash(contest.name) + '/')
    if request.method == 'POST':
        try:
            votesession = contest_models.Session.objects.get(token=request.session['token'])
            if votesession:
                choice = 'left' if request.POST.has_key('left') else 'right'
                validate_vote(choice, votesession, contest)
        except: pass
    cards = get_votesession(request, contest)
    request.session['token'] = cards.token
    context.update({
        'cards': cards,
        'contest': contest,
        'token': cards.token,
    })
    return render(request, 'contest.html', context)

def global_contest_view(request):
    return contest_view(request, settings.GLOBAL_CONTEST_ID)

def result_view(request, contestid):
    context = globalContext(request)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    list_girl, list_card = None, None
    if contest.best_girl:
        list_girl = best_girls_query(contest)
    if contest.best_card:
        list_card = best_cards_query(contest)
    context.update({
        'list_girl': list_girl,
        'list_card': list_card,
        'contest': contest,
        'is_current': is_current_contest(contest),
    })
    return render(request, 'contest_result.html', context)

def global_result_view(request):
    return result_view(request, settings.GLOBAL_CONTEST_ID)

def collection_view(request, contestid):
    try:
        if int(contestid) == settings.GLOBAL_CONTEST_ID:
            return redirect('/cards/')
    except ValueError: return redirect('/contest/results/')
    context = globalContext(request)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    is_current = is_current_contest(contest)
    if is_current:
        cards = contest.queryset()
    else:
        cards = contest.voted_cards()
    context.update({
        'contest': contest,
        'is_current': is_current,
        'cards': cards,
    })
    return render(request, 'contest_collection.html', context)

def results_index_view(request):
    context = globalContext(request)
    queryset = past_contests_queryset().annotate(count=Sum('votes__counter')).all()
    now = datetime.datetime.now()
    total_votes = contest_models.Vote.objects.filter(contest__end__lte=now).values('contest_id').annotate(total_votes=Sum('counter')).order_by('-contest__end')
    contests = [(contest, best_single_cards(contest), total_votes['total_votes']) for contest, total_votes in zip(queryset, total_votes)]
    context.update({
        'contests': contests,
        'title': 'Contests listing',
        'current': 'past_contests',
    })
    return render(request, 'contest_result_index.html', context)
