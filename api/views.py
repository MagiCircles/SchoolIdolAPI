import django_filters
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import api_view
from rest_framework.filters import BaseFilterBackend
from api import permissions as api_permissions
from api import serializers, models, raw
from django.db.models import Count, Q, Prefetch

class CommaSeparatedValueFilter(django_filters.CharFilter):
    """Accept comma separated string as value and convert it to list.
    It's useful for __in lookups.
    """

    def filter(self, qs, value):
        if value:
            value = value.split(',')
        return super(CommaSeparatedValueFilter, self).filter(qs, value)

class RandomBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'ordering' in request.query_params and request.query_params['ordering'] == 'random':
            return queryset.order_by('?')
        return queryset

class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'following' in request.query_params:
            return queryset.filter(pk__in=(models.User.objects.get(username=request.query_params['following']).followers.all()))
        if 'followed_by' in request.query_params:
            return queryset.filter(pk__in=(models.User.objects.get(username=request.query_params['followed_by']).preferences.following.all()))
        return queryset.distinct()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get_queryset(self):
        queryset = models.User.objects.all()
        if 'expand_accounts' in self.request.query_params:
            queryset = queryset.prefetch_related(Prefetch('accounts_set', queryset=models.Account.objects.order_by('-rank'), to_attr='all_accounts'))
        if 'expand_links' in self.request.query_params:
            queryset = queryset.prefetch_related(Prefetch('links', to_attr='all_links'))
        if 'expand_preferences' in self.request.query_params:
            queryset = queryset.select_related('preferences')
        return queryset

    serializer_class = serializers.UserSerializer
    search_fields = ('username', 'preferences__description', 'preferences__location', 'links__value', 'accounts_set__nickname')
    filter_fields = ('email', 'preferences__private', 'preferences__status', 'preferences__color', 'preferences__best_girl', 'preferences__location')
    ordering_fields = '__all__'
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, UserFilterBackend, RandomBackend)
    permission_classes = (api_permissions.UserPermissions, )
    lookup_field = 'username'

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

class CardFilter(django_filters.FilterSet):
    is_event = django_filters.MethodFilter(action='filter_is_event')
    ids = django_filters.MethodFilter(action='filter_ids')
    for_trivia = django_filters.MethodFilter(action='filter_for_trivia')
    rarity = CommaSeparatedValueFilter(name='rarity', lookup_type='in')

    def filter_for_trivia(self, queryset, value):
        return queryset.filter(Q(idol__hobbies__isnull=False) | Q(idol__favorite_food__isnull=False) | Q(idol__least_favorite_food__isnull=False))


    def filter_is_event(self, queryset, value):
        return queryset.filter(event__isnull=(False if value.title() == 'True' else True))

    def filter_ids(self, queryset, value):
        return queryset.filter(id__in=value.split(','))

    class Meta:
        model = models.Card
        fields = ('name', 'japanese_collection', 'translated_collection', 'rarity', 'attribute', 'is_promo', 'is_special', 'japan_only', 'hp', 'skill', 'center_skill', 'is_event', 'ids')

class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed.
    """
    def get_queryset(self):
        queryset = models.Card.objects.all()
        if 'expand_idol' in self.request.query_params:
            queryset = queryset.select_related('idol')
        if 'expand_event' in self.request.query_params:
            queryset = queryset.select_related('event')
        return queryset

    serializer_class = serializers.CardSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('name', 'idol__japanese_name', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'japanese_collection', 'translated_collection', 'promo_item','event__english_name','event__japanese_name')
    filter_class = CardFilter
    permission_classes = (api_permissions.IsStaffOrReadOnly, )
    ordering_fields = '__all__'
    ordering = ('id',)

class SongFilter(django_filters.FilterSet):
    is_event = django_filters.MethodFilter(action='filter_is_event')
    is_daily_rotation = django_filters.MethodFilter(action='filter_is_daily_rotation')
    event = django_filters.MethodFilter(action='filter_event')

    def filter_is_event(self, queryset, value):
        return queryset.filter(event__isnull=(False if value.title() == 'True' else True))

    def filter_is_daily_rotation(self, queryset, value):
        return queryset.filter(daily_rotation__isnull=(False if value.title() == 'True' else True))

    def filter_event(self, queryset, value):
        return queryset.filter(event__japanese_name=value)

    class Meta:
        model = models.Song
        filter_fields = ('attribute', 'event', 'rank', 'daily_rotation', 'daily_rotation_position', 'available')

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('name', 'romaji_name', 'translated_name')
    filter_class = SongFilter
    ordering_fields = '__all__'
    ordering = ('-available', 'daily_rotation', 'daily_rotation_position', 'rank', 'name')
    lookup_field = 'name'

class IdolFilter(django_filters.FilterSet):
    for_trivia = django_filters.MethodFilter(action='filter_for_trivia')

    def filter_for_trivia(self, queryset, value):
        return queryset.filter(Q(hobbies__isnull=False) | Q(favorite_food__isnull=False) | Q(least_favorite_food__isnull=False))

    class Meta:
        model = models.Idol
        fields = ('name', 'main', 'age', 'astrological_sign', 'blood', 'attribute', 'year', 'cards__is_special', 'for_trivia')

class IdolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows idols to be viewed.
    """
    queryset = models.Idol.objects.all().distinct()
    serializer_class = serializers.IdolSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('name', 'japanese_name', 'birthday', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'cv', 'cv_nickname', 'cv_twitter', 'cv_instagram', 'summary')
    filter_class = IdolFilter
    ordering_fields = '__all__'
    ordering = ('-main', 'name')
    lookup_field = 'name'

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('japanese_name', 'english_name')
    filter_fields = ('cards__idol__name',)
    ordering_fields = '__all__'
    ordering = ('beginning',)
    lookup_field = 'japanese_name'

class AccountFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'minimum_rank' in request.query_params:
            queryset = queryset.filter(rank__gte=request.query_params['minimum_rank'])
        if 'maximum_rank' in request.query_params:
            queryset = queryset.filter(rank__lte=request.query_params['maximum_rank'])
        if 'is_verified' in request.query_params:
            if request.query_params['is_verified'].title() == 'True':
                queryset = queryset.filter(Q(verified=1) | Q(verified=2))
            elif request.query_params['is_verified'].title() == 'False':
                queryset = queryset.exclude(Q(verified=1) | Q(verified=2))
        return queryset

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    def get_queryset(self):
        queryset = models.Account.objects.all()
        if 'expand_owner' in self.request.query_params:
            queryset = queryset.select_related('owner')
        return queryset

    serializer_class = serializers.AccountSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, AccountFilterBackend, RandomBackend)
    search_fields = ('owner__username', 'nickname', 'device')
    filter_fields = ('owner__username', 'nickname', 'language', 'center', 'friend_id', 'language', 'os', 'center', 'rank', 'device', 'play_with', 'accept_friend_requests', 'verified')
    ordering_fields = '__all__'

class OwnedCardFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'minimum_skill' in request.query_params:
            queryset = queryset.filter(skill__gte=request.query_params['minimum_skill'])
        if 'maximum_skill' in request.query_params:
            queryset = queryset.filter(skill__lte=request.query_params['maximum_skill'])
        if 'card__is_event' in request.query_params:
            queryset = queryset.filter(card__event__isnull=(False if request.query_params['card__is_event'].title() == 'True' else True))
        return queryset

class OwnedCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owned cards to be viewed or edited.
    """
    def get_queryset(self):
        queryset = models.OwnedCard.objects.all()
        if self.request.user.is_authenticated():
            queryset = queryset.filter(Q(owner_account__owner__preferences__private=False) | Q(owner_account__owner__preferences__private=True, owner_account__pk__in=(self.request.user.accounts_set.all() if self.request.user.is_authenticated() else [])))
        # else: TODO: too slow, extra query
        #     queryset = queryset.filter(owner_account__owner__preferences__private=False)
        if 'expand_card' in self.request.query_params:
            queryset = queryset.select_related('card')
        if 'expand_owner' in self.request.query_params:
            queryset = queryset.select_related('owner_account')
        return queryset

    serializer_class = serializers.OwnedCardSerializer
    filter_backends = (filters.DjangoFilterBackend, OwnedCardFilterBackend, filters.OrderingFilter, RandomBackend)
    filter_fields = ('owner_account', 'card', 'idolized', 'stored', 'max_level', 'max_bond', 'skill', 'card__name', 'card__japanese_collection', 'card__rarity', 'card__attribute', 'card__is_promo', 'card__is_special', 'card__japan_only', 'card__hp', 'card__skill', 'card__center_skill')
    ordering_fields = ('owner_account', 'card', 'idolized', 'stored', 'max_level', 'max_bond', 'skill', 'card__name', 'card__japanese_collection', 'card__rarity', 'card__attribute', 'card__is_promo', 'card__is_special', 'card__japan_only', 'card__hp', 'card__skill', 'card__center_skill')
    permission_classes = (api_permissions.IsStaffOrSelf, )

class CardIdViewSet(CardViewSet):
    """
    API endpoint to get cards ids only.
    """
    queryset = models.Card.objects.all().values('id')
    serializer_class = serializers.CardIdSerializer
    paginate_by = None

    def list(self, request):
        r = super(CardIdViewSet, self).list(request)
        r.data = [card['id'] for card in r.data]
        return r

@api_view(['GET'])
def app(request, app):
    app = raw.app_data.get(app, None)
    if app is None:
        raise Http404
    return Response(app, status=status.HTTP_200_OK)
