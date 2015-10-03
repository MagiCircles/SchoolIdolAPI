from django.db.models import Sum
import contest.models as contest_models
import api.models as api_models
import random
import hashlib
import datetime
import uuid

def gen_fingerprint(request):
    return request.META['REMOTE_ADDR']

def passed_contests_queryset():
    now = datetime.datetime.now()
    return contest_models.Contest.objects.filter(end__lte=now)

def get_current_contest():
    now = datetime.datetime.now()
    return contest_models.Contest.objects.filter(end__gte=now, begin__lte=now).first()

def get_cards(contest):
    queryset = contest.queryset()
    cards = [card for card in queryset]
    left = random.choice(cards)
    right = random.choice(cards)
    left_idolized = random.choice([True, False])
    right_idolized = random.choice([True, False])
    #FIXME handle idolized-only cards
    while (right.pk == left.pk) and (left_idolized == right_idolized):
        right_idolized = random.choice([True, False])
    vote_left, _ = contest_models.Vote.objects.get_or_create(card=left, idolized=left_idolized, contest=contest)
    vote_right, _ = contest_models.Vote.objects.get_or_create(card=right, idolized=right_idolized, contest=contest)
    return vote_left, vote_right

def get_votesession(request, contest):
    """
    A player shouldn't be able to skip more than 9 votes.
    If there is more than 9 votesessions for this browser,
    we return a random one from the previous votesessions
    Else, we return a new one.
    """
    fingerprint = gen_fingerprint(request)
    sessions = contest_models.Session.objects.filter(fingerprint=fingerprint).all()
    if sessions.count() >= 9:
        return sessions.order_by('?').first()
    else:
        left, right= get_cards(contest)
        session = contest_models.Session(left=left, right=right,
                                         fingerprint=fingerprint,
                                         token=str(uuid.uuid4()),
                                         contest=contest,
                                         date=datetime.datetime.now())
        session.save()
        return session

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
    queryset = contest_models.Vote.objects.filter(contest=contest).values('card__name').annotate(count=Sum('counter')).order_by('-count')
    characters = [(girl['card__name'], girl['count']) for girl in queryset.all()[:10]]
    return characters

def best_cards_query(contest):
    queryset = contest_models.Vote.objects.filter(contest=contest).order_by('-counter')
    cards = [(vote.idolized, vote.card, vote.counter) for vote in queryset.all()[:10]]
    return cards

def best_single_card_query(contest):
    vote = contest_models.Vote.objects.filter(contest=contest).order_by('-counter').first()
    return vote.card, vote.idolized

def best_single_girl_query(contest):
    girl = contest_models.Vote.objects.filter(contest=contest).values('card__name').annotate(count=Sum('counter')).order_by('-count').first()
    return girl['card__name'], girl['count']

def best_single_cards(contest):
    cards = dict()
    cards['best_girl'], cards['best_card'] = None, None
    if contest.best_girl:
        cards['best_girl'] = best_single_girl_query(contest)
    if contest.best_card:
        cards['best_card'] = best_single_card_query(contest)
    return cards
