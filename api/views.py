from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters
from api import serializers, models

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
                                
class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = models.Card.objects.all()
    serializer_class = serializers.CardSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('name', 'skill', 'center_skill')
    filter_fields = ('name', 'rarity', 'attribute', 'is_promo', 'is_special', 'hp', 'skill', 'center_skill')
