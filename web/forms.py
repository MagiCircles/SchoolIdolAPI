from django import forms
from django.forms import Form, ModelForm, ModelChoiceField, ChoiceField
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from api import models

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

def getGirls():
    girls = models.Card.objects.values('name').annotate(total=Count('name')).order_by('-total', 'name')
    return [('', '')] + [(girl['name'], girl['name']) for girl in girls]

class UserPreferencesForm(ModelForm):
    best_girl = ChoiceField(label=_('Best Girl'), choices=getGirls(), required=False)
    class Meta:
        model = models.UserPreferences
        fields = ('color', 'best_girl', 'location', 'private', 'accept_friend_requests', 'description', 'private', 'twitter', 'facebook', 'reddit', 'line', 'tumblr')

class AccountForm(ModelForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'language', 'os', 'friend_id', 'rank')

class OwnedCardModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return unicode(obj.card) + ' ' + ('idolized' if obj.idolized else '')

class FullAccountForm(ModelForm):
    center = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
    # Always override this queryset to set the current account only
    # form.fields['center'].queryset = models.OwnedCard.objects.filter(owner_account=owned_account, stored='Deck')
    class Meta:
        model = models.Account
        fields = ('nickname', 'center', 'rank', 'friend_id', 'transfer_code', 'language', 'os')

class OwnedCardForm(ModelForm):
    class Meta:
        model = models.OwnedCard
        fields = ('card', 'stored', 'idolized', 'max_level', 'max_bond')

class EventParticipationForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('ranking', 'song_ranking', 'points')

class EventParticipationNoSongForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('ranking', 'points')

class UserSearchForm(Form):
    term = forms.CharField(required=False, label=_('Search'))
    ordering = forms.ChoiceField(required=False, label='', widget=forms.RadioSelect, choices=[
        ('-accounts_set__rank', _('Ranking')),
        ('-date_joined', _('New players')),
        ('username', _('Name')),
    ], initial='-accounts_set__rank')
