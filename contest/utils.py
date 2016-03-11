from django.db.models import Sum
import contest.models as contest_models
import api.models as api_models
from django.utils import timezone
from django.conf import settings
import random
import hashlib
import datetime
import uuid

def gen_fingerprint(request):
    return request.META['REMOTE_ADDR']

def past_contests_queryset():
    now = datetime.datetime.now()
    return contest_models.Contest.objects.filter(end__lte=now).order_by('-end')

def get_current_contest():
    now = datetime.datetime.now()
    return contest_models.Contest.objects.filter(end__gte=now, begin__lte=now).first()

def is_current_contest(contest):
    if contest.id == settings.GLOBAL_CONTEST_ID:
        return True
    now = timezone.now()
    return contest.begin <= now and contest.end >= now

def get_cards(contest):
    cards = contest.queryset()
    left = random.choice(cards)
    right = random.choice(cards)
    while (right.pk == left.pk):
        right = random.choice(cards)
    vote_left, _ = contest_models.Vote.objects.get_or_create(card=left, idolized=left.vote_idolized, contest=contest)
    vote_right, _ = contest_models.Vote.objects.get_or_create(card=right, idolized=right.vote_idolized, contest=contest)
    return vote_left, vote_right

def get_votesession(request, contest):
    """
    A player shouldn't be able to skip more than settings.CONTEST_MAX_SESSIONS votes.
    If there is more than settings.CONTEST_MAX_SESSIONS votesessions for this browser,
    we return True + a random one from the previous votesessions
    Else, we return False + a new one.
    """
    fingerprint = gen_fingerprint(request)
    sessions = contest_models.Session.objects.filter(fingerprint=fingerprint, contest=contest).all()
    if sessions.count() >= settings.CONTEST_MAX_SESSIONS:
        return (True, sessions.order_by('?').first())
    else:
        left, right= get_cards(contest)
        session = contest_models.Session(left=left, right=right,
                                         fingerprint=fingerprint,
                                         token=str(uuid.uuid4()),
                                         contest=contest,
                                         date=datetime.datetime.now())
        session.save()
        return (False, session)

def validate_vote(choice, session, contest):
    if choice == 'left':
        vote = session.left
    elif choice == 'right':
        vote = session.right
    vote.counter += 1
    vote.save()
    session.delete()
    return

def best_girls_query(contest):
    '''
    Return a list of the winners sorted by name
    '''
    queryset = contest_models.Vote.objects.filter(contest=contest).values('card__name').annotate(count=Sum('counter')).order_by('-count').select_related('card')
    characters = [(girl['card__name'], girl['count']) for girl in queryset.all()[:10]]
    return characters

def best_cards_query(contest):
    queryset = contest_models.Vote.objects.filter(contest=contest).order_by('-counter').select_related('card')
    cards = [(vote.idolized, vote.card, vote.counter) for vote in queryset.all()[:10]]
    return cards

def best_single_card_query(contest):
    vote = contest_models.Vote.objects.filter(contest=contest).order_by('-counter').first()
    return vote.card, vote.idolized

def best_single_girl_query(contest):
    girl = contest_models.Vote.objects.filter(contest=contest).values('card__name').annotate(count=Sum('counter')).order_by('-count').first()
    return girl['card__name']

def best_single_cards(contest):
    cards = dict()
    cards['best_girl'], cards['best_card'] = None, None
    if contest.best_girl:
        cards['best_girl'] = best_single_girl_query(contest)
    if contest.best_card:
        cards['best_card'] = best_single_card_query(contest)
    return cards
