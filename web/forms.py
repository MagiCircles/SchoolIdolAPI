from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User, Group
from api import models

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
        fields = ('card', 'stored', 'expiration', 'idolized', 'max_level', 'max_bond')
