import datetime
from collections import OrderedDict
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, string_concat
from django.db import models
from magi.utils import PastOnlyValidator
from magi.item_model import MagiModel, CacheOwner, i_choices
from sukutomo.django_translated import t

class Account(CacheOwner):
    collection_name = 'account'

    # Foreign keys

    owner = models.ForeignKey(User, related_name='accounts')
    #center = models.ForeignKey('OwnedCard', verbose_name=_('Center'), null=True, help_text=_('The character that talks to you on your home screen.'), on_delete=models.SET_NULL)
    #starter = models.ForeignKey(Card, verbose_name=_('Starter'), null=True, help_text=_('The character that you selected when you started playing.'), on_delete=models.SET_NULL)

    # Details

    creation = models.DateTimeField(auto_now_add=True) # new
    nickname = models.CharField(_('Nickname'), max_length=20)
    rank = models.PositiveIntegerField(_('Rank'), null=True)

    VERSIONS = OrderedDict((
        ('JP', { 'translation': t['Japanese'], 'icon': 'JP' }),
        ('WW', { 'translation': _('Worldwide'), 'icon': 'world' }),
        ('KR', { 'translation': t['Korean'], 'icon': 'KR' }),
        ('CN', { 'translation': t['Chinese'], 'icon': 'CN' }),
        ('TW', { 'translation': t['Taiwanese'], 'icon': 'TW' }),
    ))
    VERSION_CHOICES = [(name, info['translation']) for name, info in VERSIONS.items()]

    i_version = models.PositiveIntegerField(_('Version'), choices=i_choices(VERSION_CHOICES), default=1)

    friend_id = models.PositiveIntegerField(_('Friend ID'), null=True, help_text=_('You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.'))
    show_friend_id = models.BooleanField(_('Should your friend ID be visible to other players?'), default=True)
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), null=True)
    device = models.CharField(_('Device'), help_text=_('The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True)
    # previously: creation
    start_date = models.DateField(blank=True, null=True, verbose_name=_('Start Date'), validators=[
        MinValueValidator(datetime.date(2013, 4, 16)),
        PastOnlyValidator,
    ])
    # previously: show_creation
    show_start_date = models.BooleanField('', default=True, help_text=_('Should this date be visible to other players?'))
    loveca = models.PositiveIntegerField(_('Love gems'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Love gems')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    friend_points = models.PositiveIntegerField(_('Friend Points'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Friend Points')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    g = models.PositiveIntegerField('G', help_text=string_concat(_('Number of {} you currently have in your account.').format('G'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    tickets = models.PositiveIntegerField('Scouting Tickets', help_text=string_concat(_('Number of {} you currently have in your account.').format('Scouting Tickets'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    vouchers = models.PositiveIntegerField('Vouchers (blue tickets)', help_text=string_concat(_('Number of {} you currently have in your account.').format('Vouchers (blue tickets)'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), default=0)
    bought_loveca = models.PositiveIntegerField(_('Total love gems bought'), help_text=_('You can calculate that number in "Other" then "Purchase History". Leave it empty to stay F2P.'), null=True)
    show_items = models.BooleanField('', default=True, help_text=_('Should your items be visible to other players?'))

    # Choices

    PLAY_WITH = OrderedDict([
        ('Thumbs', {
            'translation': _('Thumbs'),
            'icon': 'thumbs'
        }),
        ('Fingers', {
            'translation': _('All fingers'),
            'icon': 'fingers'
        }),
        ('Index', {
            'translation': _('Index fingers'),
            'icon': 'index'
        }),
        ('Hand', {
            'translation': _('One hand'),
            'icon': 'fingers'
        }),
        ('Other', {
            'translation': _('Other'),
            'icon': 'sausage'
        }),
    ])
    PLAY_WITH_CHOICES = [(name, info['translation']) for name, info in PLAY_WITH.items()]

    i_play_with = models.PositiveIntegerField(_('Play with'), choices=i_choices(PLAY_WITH_CHOICES), null=True)

    OS_CHOICES = (
        'Android',
        'iOs',
    )
    i_os = models.PositiveIntegerField(_('Operating System'), choices=i_choices(OS_CHOICES), null=True)

    # Special

    transfer_code = models.CharField(_('Transfer Code'), max_length=100, help_text=_('It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.'))
    fake = models.BooleanField(_('Fake'), default=False)

    #verified = models.PositiveIntegerField(_('Verified'), default=0, choices=VERIFIED_CHOICES)
    #default_tab = models.CharField(_('Default tab'), max_length=30, choices=ACCOUNT_TAB_CHOICES, help_text=_('What people see first when they take a look at your account.'), default='deck')

    # Cache: leaderboard position

    _cache_leaderboards_days = 1
    _cache_leaderboards_last_update = models.DateTimeField(null=True)
    _cache_leaderboard = models.PositiveIntegerField(null=True)
    _cache_leaderboard_version = models.PositiveIntegerField(null=True)

    def update_cache_leaderboards(self):
        self._cache_leaderboards_last_update = timezone.now()
        self._cache_leaderboard = getAccountLeaderboard(self)
        self._cache_leaderboard_version = getAccountLeaderboardForVersion(self)

    def force_cache_leaderboards(self):
        self.update_cache_leaderboards()
        self.save()

    @property
    def cached_leaderboard(self):
        if not self._cache_leaderboards_last_update or self._cache_leaderboards_last_update < timezone.now() - datetime.timedelta(days=self._cache_leaderboards_days):
            self.force_cache_leaderboards()
        return self._cache_leaderboard

    @property
    def cached_leaderboard_team(self):
        if not self._cache_leaderboards_last_update or self._cache_leaderboards_last_update < timezone.now() - datetime.timedelta(days=self._cache_leaderboards_days):
            self.force_cache_leaderboards()
        return self._cache_leaderboard_team

    def __unicode__(self):
        return u'{} {} '.format(self.nickname, self.version)

def getAccountLeaderboard(account):
    return Account.objects.filter(rank__gt=account.rank).values('rank').distinct().count() + 1

def getAccountLeaderboardForVersion(account):
    return Account.objects.filter(i_version=account.i_version, rank__gt=account.rank).values('rank').distinct().count() + 1
