import django_filters
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters, permissions
from api import permissions as api_permissions
from api import serializers, models

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
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    search_fields = ('username', 'preferences__description', 'preferences__location', 'links__value', 'accounts_set__nickname')
    filter_fields = ('email', 'preferences__private', 'preferences__status', 'preferences__color', 'preferences__best_girl', 'preferences__location')
    ordering_fields = '__all__'
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, UserFilterBackend)
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

    def filter_is_event(self, queryset, value):
        return queryset.filter(event__isnull=(False if value.title() == 'True' else True))

    class Meta:
        model = models.Card
        fields = ('name', 'japanese_collection', 'rarity', 'attribute', 'is_promo', 'is_special', 'japan_only', 'hp', 'skill', 'center_skill', 'is_event')

class CardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cards to be viewed.
    """
    queryset = models.Card.objects.all().select_related('event', 'idol')
    serializer_class = serializers.CardSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'idol__japanese_name', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'japanese_center_skill','japanese_center_skill_details','japanese_collection','promo_item','event__english_name','event__japanese_name')
    filter_class = CardFilter
    ordering_fields = '__all__'
    ordering = ('id',)

class IdolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows idols to be viewed.
    """
    queryset = models.Idol.objects.all()
    serializer_class = serializers.IdolSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'japanese_name', 'birthday', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'cv', 'cv_nickname', 'cv_twitter', 'cv_instagram', 'summary')
    filter_fields = ('name', 'main', 'age', 'astrological_sign', 'blood', 'attribute', 'year')
    ordering_fields = '__all__'
    ordering = ('-main', 'name')

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('japanese_name', 'english_name')
    ordering_fields = '__all__'
    ordering = ('beginning',)

class AccountFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'minimum_rank' in request.query_params:
            queryset = queryset.filter(rank__gte=request.query_params['minimum_rank'])
        if 'maximum_rank' in request.query_params:
            queryset = queryset.filter(rank__lte=request.query_params['maximum_rank'])
        return queryset

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = models.Account.objects.all().select_related('owner', 'center')
    serializer_class = serializers.AccountSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, AccountFilterBackend)
    search_fields = ('owner__username', 'nickname',)
    filter_fields = ('owner__username', 'nickname', 'language', 'center', 'rank', 'friend_id', 'language', 'os', 'center', 'rank')
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

class OwnedCardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows owned cards to be viewed or edited.
    """
    queryset = models.OwnedCard.objects.filter(owner_account__owner__preferences__private=False).select_related('owner_account', 'card')
    serializer_class = serializers.OwnedCardSerializer
    filter_backends = (filters.DjangoFilterBackend, OwnedCardFilterBackend)
    filter_fields = ('owner_account', 'card', 'idolized', 'stored', 'max_level', 'max_bond', 'skill', 'card__name', 'card__japanese_collection', 'card__rarity', 'card__attribute', 'card__is_promo', 'card__is_special', 'card__japan_only', 'card__hp', 'card__skill', 'card__center_skill')

class CardIdViewSet(CardViewSet):
    """
    API endpoint to get cards ids only.
    """
    paginate_by = None

    def list(self, request):
        r = super(CardIdViewSet, self).list(request)
        r.data = [card['id'] for card in r.data]
        return r
