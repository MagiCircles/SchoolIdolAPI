import django_filters
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters, permissions
from api import permissions as api_permissions
from api import serializers, models

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (api_permissions.UserPermissions, )

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
        fields = ('name', 'japanese_collection', 'rarity', 'attribute', 'is_promo', 'is_special', 'hp', 'skill', 'center_skill', 'is_event')

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
    search_fields = ('name', 'japanese_name', 'birthday', 'measurements', 'favorite_food', 'least_favorite_food', 'hobbies', 'cv', 'summary')
    filter_fields = ('name', 'main', 'age', 'astrological_sign', 'blood', 'attribute', 'year')
    ordering_fields = '__all__'
    ordering = ('main', 'name')

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

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = models.Account.objects.all().select_related('owner', 'center')
    serializer_class = serializers.AccountSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('owner', 'nickname')
    filter_fields = ('owner', 'nickname', 'language', 'center', 'rank')

class OwnedCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owned cards to be viewed or edited.
    """
    queryset = models.OwnedCard.objects.all().select_related('owner_account', 'card')
    serializer_class = serializers.OwnedCardSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('owner_account', 'card', 'idolized', 'stored')

class CardIdViewSet(CardViewSet):
    """
    API endpoint to get cards ids only.
    """
    paginate_by = None

    def list(self, request):
        r = super(CardIdViewSet, self).list(request)
        r.data = [card['id'] for card in r.data]
        return r
