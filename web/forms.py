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
    girls = models.Card.objects.values('idol__name').annotate(total=Count('idol__name')).order_by('-total', 'idol__name')
    return [('', '')] + [(girl['idol__name'], girl['idol__name']) for girl in girls]

class UserPreferencesForm(ModelForm):
    best_girl = ChoiceField(label=_('Best Girl'), choices=getGirls(), required=False)
    class Meta:
        model = models.UserPreferences
        fields = ('color', 'best_girl', 'location', 'private', 'description', 'private', 'twitter', 'facebook', 'reddit', 'line', 'tumblr', 'twitch', 'mal', 'otonokizaka')

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
        fields = ('nickname', 'center', 'rank', 'friend_id', 'transfer_code', 'language', 'os', 'device', 'play_with', 'accept_friend_requests')

class FullAccountNoFriendIDForm(FullAccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'center', 'rank', 'transfer_code', 'device', 'play_with', 'accept_friend_requests')

class OwnedCardForm(ModelForm):
    class Meta:
        model = models.OwnedCard
        fields = ('card', 'owner_account', 'stored', 'idolized', 'max_level', 'max_bond', 'skill')

def getOwnedCardForm(form, accounts, owned_card=None):
    form.fields['owner_account'].queryset = accounts
    form.fields['owner_account'].required = True
    form.fields['owner_account'].empty_label = None
    if owned_card is not None:
        if not owned_card.card.skill:
            form.fields.pop('skill')
    return form

class EventParticipationForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('account', 'ranking', 'points', 'song_ranking')

class EventParticipationNoSongForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('account', 'ranking', 'points')

class EventParticipationNoAccountForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('ranking', 'points', 'song_ranking')

class EventParticipationNoSongNoAccountForm(ModelForm):
    class Meta:
        model = models.EventParticipation
        fields = ('ranking', 'points')

def getEventParticipationForm(form, accounts):
    form.fields['account'].queryset = accounts
    form.fields['account'].required = True
    form.fields['account'].empty_label = None
    return form

class UserSearchForm(Form):
    term = forms.CharField(required=False, label=_('Search'))
    ordering = forms.ChoiceField(required=False, label='', widget=forms.RadioSelect, choices=[
        ('-accounts_set__rank', _('Ranking')),
        ('-accounts_set__verified', _('Verified')),
        ('-date_joined', _('New players')),
        ('username', _('Nickname')),
    ], initial='-accounts_set__rank')

class UserProfileStaffForm(ModelForm):
    class Meta:
        model = models.UserPreferences
        fields = ('status', 'donation_link', 'donation_link_title')
