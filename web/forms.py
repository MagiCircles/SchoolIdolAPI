from django.shortcuts import get_object_or_404
from django import forms
from django.forms import Form, ModelForm, ModelChoiceField, ChoiceField
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BLANK_CHOICE_DASH
from multiupload.fields import MultiFileField
from api import models

class CreateUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class AddLinkForm(ModelForm):
    class Meta:
        model = models.UserLink
        fields = ('type', 'value', 'relevance')

class ChangePasswordForm(Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label=_('Old Password'))
    new_password = forms.CharField(widget=forms.PasswordInput(), label=_('New Password'))
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label=_('New Password Again'))

    def clean(self):
        if ('new_password' in self.cleaned_data and 'new_password2' in self.cleaned_data
            and self.cleaned_data['new_password'] == self.cleaned_data['new_password2']):
            return self.cleaned_data
        raise forms.ValidationError(_("The two password fields did not match."))

def getGirls():
    girls = models.Card.objects.values('idol__name').annotate(total=Count('idol__name')).order_by('-total', 'idol__name')
    return [('', '')] + [(girl['idol__name'], girl['idol__name']) for girl in girls]

class UserPreferencesForm(ModelForm):
    best_girl = ChoiceField(label=_('Best Girl'), choices=getGirls(), required=False)
    class Meta:
        model = models.UserPreferences
        fields = ('color', 'best_girl', 'location', 'private', 'description', 'private')

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
        fields = ('nickname', 'center', 'rank', 'friend_id', 'language', 'os', 'device', 'play_with', 'accept_friend_requests')

class FullAccountNoFriendIDForm(FullAccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'center', 'rank', 'os', 'device', 'play_with', 'accept_friend_requests')

class SimplePasswordForm(Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}), label=_('Password'))

class TransferCodeForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Password'))
    class Meta:
        model = models.Account
        fields = ('transfer_code',)

class _OwnedCardForm(ModelForm):
    def save(self, commit=True):
        instance = super(_OwnedCardForm, self).save(commit=False)
        if instance.card.is_promo or instance.card.is_special:
            instance.idolized = True
        if commit:
            instance.save()
        return instance

class QuickOwnedCardForm(_OwnedCardForm):
    card = forms.IntegerField()
    class Meta:
        model = models.OwnedCard
        fields = ('card', 'owner_account', 'idolized')

class EditQuickOwnedCardForm(_OwnedCardForm):
    card = forms.IntegerField()
    class Meta:
        model = models.OwnedCard
        fields = ('idolized',)

class StaffAddCardForm(ModelForm):
    card = forms.IntegerField()
    owner_account = forms.IntegerField()

    def save(self, commit=True):
        self.instance.card = get_object_or_404(models.Card, pk=self.cleaned_data['card'])
        self.instance.owner_account = get_object_or_404(models.Account, pk=self.cleaned_data['owner_account'])
        return super(StaffAddCardForm, self).save(commit)

    class Meta:
        model = models.OwnedCard
        fields = ('card', 'owner_account', 'stored', 'idolized', 'max_level', 'max_bond', 'skill')
        exclude = ('card', 'owner_account')

class OwnedCardForm(_OwnedCardForm):
    class Meta:
        model = models.OwnedCard
        fields = ('owner_account', 'stored', 'idolized', 'max_level', 'max_bond', 'skill')

class EditOwnedCardForm(_OwnedCardForm):
    class Meta:
        model = models.OwnedCard
        fields = ('stored', 'idolized', 'max_level', 'max_bond', 'skill')

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
        fields = ('status', 'donation_link', 'donation_link_title', 'description', 'location', 'location_changed')

class AccountStaffForm(ModelForm):
    owner_id = forms.IntegerField(required=False)
    center = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=True)
    class Meta:
        model = models.Account
        fields = ('owner_id', 'friend_id', 'verified', 'rank', 'os', 'device', 'center')

class MultiImageField(MultiFileField, forms.ImageField):
    pass

class VerificationRequestForm(ModelForm):
    images = MultiImageField(min_num=0, max_num=10, required=False, help_text=_('If your files are too large, send them one by one. First upload one image, then edit your request with the second one, and so on. If even one image doesn\'t work, please resize your images.'))

    def __init__(self, *args, **kwargs):
        account = None
        if 'account' in kwargs:
            account = kwargs.pop('account')
        super(VerificationRequestForm, self).__init__(*args, **kwargs)
        if account is not None:
            if account.language != 'JP' and account.language != 'EN':
                self.fields['verification'].choices = ((0, ''), (1, _('Silver Verified')))
            elif account.rank < 195:
                self.fields['verification'].choices = ((0, ''), (1, _('Silver Verified')), (2, _('Gold Verified')))

    class Meta:
        model = models.VerificationRequest
        fields = ('verification', 'comment', 'images', 'allow_during_events')

class StaffVerificationRequestForm(ModelForm):
    images = MultiImageField(min_num=0, max_num=10, required=False)
    status = forms.ChoiceField(choices=((3, 'Verified'), (0, 'Rejected')), widget=forms.RadioSelect)

    class Meta:
        model = models.VerificationRequest
        fields = ('status', 'verification_comment', 'images')

class StaffFilterVerificationRequestForm(ModelForm):
    OS = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(models.OS_CHOICES), required=False)
    language = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(models.LANGUAGE_CHOICES), required=False)

    def __init__(self, *args, **kwargs):
        super(StaffFilterVerificationRequestForm, self).__init__(*args, **kwargs)
        self.fields['verified_by'].queryset = User.objects.filter(is_staff=True)
        self.fields['verified_by'].required = False
        self.fields['status'].required = False
        self.fields['status'].choices = BLANK_CHOICE_DASH + self.fields['status'].choices
        self.fields['verification'].required = False
        self.fields['verification'].help_text = None
        self.fields['allow_during_events'].help_text = None
        self.fields['allow_during_events'].label = 'Allowed us to verify them during events'

    class Meta:
        model = models.VerificationRequest
        fields = ('status', 'verified_by', 'verification', 'OS', 'language', 'allow_during_events')

class FilterSongForm(ModelForm):
    search = forms.CharField(required=False, label=_('Search'))
    ordering = forms.ChoiceField(choices=[
        ('latest', _('Latest unlocked songs')),
        ('name', _('Song name')),
        ('BPM', _('Beats per minute')),
        ('time', _('Song length')),
        ('rank', _('Rank to unlock song')),
        ('hard_notes', _('Notes in Hard song')),
        ('expert_notes', _('Notes in Expert song')),
    ], initial='latest', required=False, label=_('Ordering'))
    reverse_order = forms.BooleanField(initial=True, required=False, label=_('Reverse order'))
    is_daily_rotation = forms.NullBooleanField(required=False, label=_('Daily rotation'))
    is_event = forms.NullBooleanField(required=False, label=_('Event'))
    available = forms.NullBooleanField(required=False, label=_('Available'))

    def __init__(self, *args, **kwargs):
        super(FilterSongForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    class Meta:
        model = models.Song
        fields = ('search', 'attribute', 'is_daily_rotation', 'is_event', 'available', 'ordering', 'reverse_order')

# class TeamForm(ModelForm):
#     card0 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card1 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card2 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card3 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card4 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card5 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card6 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card7 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     card8 = OwnedCardModelChoiceField(queryset=models.OwnedCard.objects.all(), required=False)
#     class Meta:
#         model = models.Team
#         fields = ('name', 'card0', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8')

# def getTeamForm(form, ownedcards):
#     for i in range(9):
#         print 'test'
#         setattr(form, 'card' + str(i), OwnedCardModelChoiceField(queryset=ownedcards, required=False))
#     return form

