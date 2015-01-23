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
        fields = ('name', 'rarity', 'attribute', 'is_promo', 'is_special', 'hp', 'skill', 'center_skill', 'event', 'is_event')

class CardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cards to be viewed.
    """
    queryset = models.Card.objects.all()
    serializer_class = serializers.CardSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'skill', 'center_skill')
    filter_class = CardFilter
    ordering_fields = '__all__'
    ordering = ('id',)

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
