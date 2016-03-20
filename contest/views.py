from django.shortcuts import render, get_object_or_404, redirect
import contest.models as contest_models
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from django.conf import settings
from contest.utils import (get_votesession, validate_vote,
                           best_girls_query, best_cards_query,
                           best_single_cards, past_contests_queryset,
                           is_current_contest,
                           is_future_contest, future_contests_queryset)
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
    if settings.HIGH_TRAFFIC:
        return render(request, 'disabled.html', context)
    contest = get_object_or_404(contest_models.Contest.objects.select_related('suggested_by', 'image_by'), pk=contestid)
    if not is_current_contest(contest):
       return redirect('/contest/result/' + contestid + '/' + tourldash(contest.name) + '/')
    if (request.method == 'POST' and 'vote_side' in request.POST and request.POST['vote_side']
        and (request.POST['vote_side'] == 'right' or request.POST['vote_side'] == 'left')):
        votesession = contest_models.Session.objects.get(token=request.session['token'])
        if votesession:
            choice = request.POST['vote_side']
            validate_vote(choice, votesession, contest)
    reused_session, cards = get_votesession(request, contest)
    request.session['token'] = cards.token
    context.update({
        'reused_session': reused_session,
        'cards': cards,
        'contest': contest,
        'token': cards.token,
        'contest_max_sessions': settings.CONTEST_MAX_SESSIONS,
    })
    return render(request, 'contest.html', context)

def global_contest_view(request):
    return contest_view(request, settings.GLOBAL_CONTEST_ID)

def result_view(request, contestid):
    context = globalContext(request)
    if settings.HIGH_TRAFFIC:
        return render(request, 'disabled.html', context)
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
    if settings.HIGH_TRAFFIC:
        return render(request, 'disabled.html', context)
    context = globalContext(request)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    is_current = is_current_contest(contest)
    if is_current or is_future_contest(contest):
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
    if settings.HIGH_TRAFFIC:
        return render(request, 'disabled.html', context)
    queryset = past_contests_queryset().annotate(count=Sum('votes__counter')).select_related('suggested_by', 'image_by')
    now = datetime.datetime.now()
    total_votes = contest_models.Vote.objects.filter(contest__end__lte=now).values('contest_id').annotate(total_votes=Sum('counter')).order_by('-contest__end')
    contests = [(contest, best_single_cards(contest), total_votes['total_votes']) for contest, total_votes in zip(queryset, total_votes)]
    context.update({
        'contests': contests,
        'current': 'past_contests',
    })
    return render(request, 'contest_result_index.html', context)

def schedule_view(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        raise PermissionDenied()
    context = globalContext(request)
    contests = future_contests_queryset().select_related('suggested_by', 'image_by')
    previous = None
    for contest in contests:
        if previous:
            contest.delta = contest.begin - previous.end
        previous = contest
    context.update({
        'contests': contests,
    })
    return render(request, 'contest_schedule.html', context)
