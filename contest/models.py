from django.db import models
import api.models as api_models
from urlparse import parse_qs
from django.db.models import Q
from django.conf import settings
from random import shuffle
from copy import copy

class Contest(models.Model):
    begin = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    name = models.CharField(max_length=300)
    best_girl = models.BooleanField(default=False)
    best_card = models.BooleanField(default=False)
    query = models.CharField(max_length=4092, null=True)
    suggested_by = models.ForeignKey(api_models.User, related_name='suggested_contests', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='contest/', null=True, blank=True)
    image_by = models.ForeignKey(api_models.User, related_name='designed_contest_banners', on_delete=models.SET_NULL, null=True, blank=True)
    result_image = models.ImageField(upload_to='contest_results/', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def alter_key(self, key):
        if key == 'is_event':
            return 'event__isnull'
        return key

    def alter_value(self, key, value):
        if value == 'False':
            return False
        elif value == 'True':
            return True
        return value

    def _queryset_idolized_and_normal(self, queryset):
        cards = []
        for card in queryset:
            card.vote_idolized = False
            cards.append(copy(card))
            card.vote_idolized = True
            cards.append(card)
        return cards

    def queryset(self):
        params = self.query
        if self.pk == settings.GLOBAL_CONTEST_ID:
            return self._queryset_idolized_and_normal(api_models.Card.objects.all())
        if params.startswith('?'):
            params_parsed = parse_qs(params[1:])
            params = {self.alter_key(key): self.alter_value(key, value[0]) for key, value in params_parsed.iteritems()}
            queryset = api_models.Card.objects.filter(**params).all().order_by('id')
            return self._queryset_idolized_and_normal(queryset)
        else:
            cards_ids = params.replace('i', '').replace('n', '').split(',')
            cards_objects = api_models.Card.objects.filter(pk__in=cards_ids).order_by('id')
            cards_list = params.split(',')
            cards = []
            for card_info in cards_list:
                card_id = int(card_info.replace('n', '').replace('i', ''))
                for card in cards_objects:
                    if card.id == card_id:
                        if 'n' in card_info:
                            card.vote_idolized = False
                            cards.append(copy(card))
                        elif 'i' in card_info:
                            card.vote_idolized = True
                            cards.append(copy(card))
                        else:
                            card.vote_idolized = False
                            cards.append(copy(card))
                            card.vote_idolized = True
                            cards.append(card)
            return cards

    def voted_cards(self):
        votes = self.votes.all().order_by('card__id', 'idolized').select_related('card')
        cards = []
        for vote in votes:
            vote.card.vote_idolized = vote.idolized
            cards.append(vote.card)
        return cards

class Vote(models.Model):
	contest = models.ForeignKey(Contest, related_name='votes')
	card = models.ForeignKey(api_models.Card, related_name='votes')
	idolized = models.BooleanField(default=False)
	counter = models.PositiveIntegerField(default=0)
        negative_counter = models.PositiveIntegerField(default=0)

class Session(models.Model):
	right = models.ForeignKey(Vote, related_name='right')
	left = models.ForeignKey(Vote, related_name='left')
	fingerprint = models.CharField(max_length=300)
	contest = models.ForeignKey(Contest, related_name='sessions')
	token = models.CharField(max_length=36)
	date = models.DateTimeField()
