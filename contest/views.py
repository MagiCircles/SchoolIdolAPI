from django.shortcuts import render, get_object_or_404
import contest.models as contest_models
from django.db.models import Sum
from contest.utils import (get_votesession, validate_vote,
                           best_girls_query, best_cards_query,
                           best_single_cards, passed_contests_queryset,
                           get_current_contest)
import datetime

def contest_view(request, contestid):
    if contestid == 'contest':
        return global_contest_view(request)
    contestid = int(contestid)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    current_contest = get_current_contest()
    if request.method == 'POST':
        try:
            votesession = contest_models.Session.objects.get(token=request.session['token'])
            if votesession:
                choice = 'left' if request.POST.has_key('left') else 'right'
                validate_vote(choice, votesession, contest)
        except:
            pass
    cards = get_votesession(request, contest)
    is_current = None
    delta = datetime.datetime.combine(contest.end, datetime.datetime.min.time()) - datetime.datetime.now() if is_current else None
    request.session['token'] = cards.token
    return render(request, 'contest.html', {'cards': cards,
                                            'contest': contest,
                                            'current_contest': current_contest,
                                            'delta': delta,
                                            'is_current': True,
                                            'token': cards.token,
                                            })

def global_contest_view(request):
    return contest_view(request, '0')

def result_view(request, contestid):
    contestid = int(contestid)
    contest = get_object_or_404(contest_models.Contest, pk=contestid)
    list_girl, list_card = None, None
    if contest.best_girl:
        list_girl = enumerate(best_girls_query(contest))
    if contest.best_card:
        list_card = enumerate(best_cards_query(contest))
    return render(request, 'contest_result.html', {'cards': {},
                                                   'list_girl': list_girl,
                                                   'list_card': list_card,
                                                   'contest': contest,
                                                   'delta': {},
                                                   'is_current': True
                                                   })

def results_index_view(request):
    queryset = passed_contests_queryset().annotate(count=Sum('votes__counter')).all()
    contests = [(contest, best_single_cards(contest)) for contest in queryset]
    return render(request, 'contest_result_index.html', {'contests': contests,
                                                         'contest': contest,
                                                         'title': 'Contests listing'})
