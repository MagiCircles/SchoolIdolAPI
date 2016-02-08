from django.db import models
import api.models as api_models
from urlparse import parse_qs
from django.db.models import Q
from django.conf import settings
from django.contrib import admin

class Contest(models.Model):
    begin = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    name = models.CharField(max_length=300)
    best_girl = models.BooleanField(default=False)
    best_card = models.BooleanField(default=False)
    query = models.CharField(max_length=4092, null=True)

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

    def queryset(self):
        params = self.query
        if self.pk == settings.GLOBAL_CONTEST_ID:
            return api_models.Card.objects.all()
        if params.startswith('?'):
            params_parsed = parse_qs(params[1:])
            params = {self.alter_key(key): self.alter_value(key, value[0]) for key, value in params_parsed.iteritems()}
            queryset = api_models.Card.objects.filter(**params).all()
            return queryset
        else:
            cards = [int(num) for num in params.split(',')]
            condition = Q()
            for card in cards:
                condition = condition | Q(id=card)
            return api_models.Card.objects.filter(condition)

admin.site.register(Contest)

class Vote(models.Model):
	contest = models.ForeignKey(Contest, related_name='votes')
	card = models.ForeignKey(api_models.Card, related_name='votes')
	idolized = models.BooleanField(default=False)
	counter = models.PositiveIntegerField(default=0)

class Session(models.Model):
	right = models.ForeignKey(Vote, related_name='right')
	left = models.ForeignKey(Vote, related_name='left')
	fingerprint = models.CharField(max_length=300)
	contest = models.ForeignKey(Contest, related_name='sessions')
	token = models.CharField(max_length=36)
	date = models.DateTimeField()
