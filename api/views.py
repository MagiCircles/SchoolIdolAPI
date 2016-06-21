import django_filters
import json
import codecs
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404, JsonResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import api_view, detail_route
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
        if 'liked_activity' in request.query_params:
            return queryset.filter(pk__in=(models.Activity.objects.get(pk=request.query_params['liked_activity']).likes.all()))
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
        if 'expand_is_following' in self.request.query_params and self.request.user.is_authenticated():
            queryset = queryset.extra(select={'is_following': 'SELECT COUNT(*) FROM api_userpreferences_following WHERE userpreferences_id=(SELECT id FROM api_userpreferences WHERE user_id={}) AND user_id=auth_user.id'.format(self.request.user.id) })
        return queryset

    serializer_class = serializers.UserSerializer
    search_fields = ('username', 'preferences__description', 'preferences__location', 'links__value', 'accounts_set__nickname')
    filter_fields = ('email', 'preferences__private', 'preferences__status', 'preferences__color', 'preferences__best_girl', 'preferences__location')
    ordering_fields = '__all__'
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, UserFilterBackend, RandomBackend)
    permission_classes = (api_permissions.UserPermissions, )
    lookup_field = 'username'

    def me(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if 'expand_accounts' in request.GET:
                request.user.all_accounts = request.user.accounts_set.all()
            if 'expand_links' in request.GET:
                request.user.all_links = request.user.links.all()
            serializer = serializers.UserSerializer(request.user, context={'request':request})
            return Response(serializer.data)
        raise PermissionDenied()

    @detail_route(methods=['POST', 'DELETE'])
    def follow(self, request, username=None):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            request.user.preferences.following.add(user)
            request.user.preferences.save()
            return JsonResponse({'follow': 'followed'})
        if request.method == 'DELETE':
            request.user.preferences.following.remove(user)
            request.user.preferences.save()
            return JsonResponse({'follow': 'unfollowed'})

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
    event_english_name = django_filters.MethodFilter(action='filter_event_english')
    event_japanese_name = django_filters.MethodFilter(action='filter_event_japanese')

    def filter_for_trivia(self, queryset, value):
        return queryset.filter(Q(idol__hobbies__isnull=False) | Q(idol__favorite_food__isnull=False) | Q(idol__least_favorite_food__isnull=False))

    def filter_event_english(self, queryset, value):
        return queryset.filter(Q(event_english_name=value) | Q(other_event_english_name=value))

    def filter_event_japanese(self, queryset, value):
        return queryset.filter(Q(event_japanese_name=value) | Q(other_event_japanese_name=value))

    def filter_is_event(self, queryset, value):
        return queryset.filter(event__isnull=(False if value.title() == 'True' else True))

    def filter_ids(self, queryset, value):
        return queryset.filter(id__in=value.split(','))

    class Meta:
        model = models.Card
        fields = ('name', 'japanese_name', 'japanese_collection', 'translated_collection', 'rarity', 'attribute', 'is_promo', 'is_special', 'japan_only', 'hp', 'skill', 'center_skill', 'is_event', 'ids', 'idol_year', 'idol_main_unit', 'idol_sub_unit', 'idol_school', 'event_japanese_name', 'event_english_name', 'ur_pair_name')

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
        if 'expand_ur_pair' in self.request.query_params:
            queryset = queryset.select_related('ur_pair')
        return queryset

    serializer_class = serializers.CardSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('name', 'japanese_name', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'japanese_collection', 'translated_collection', 'promo_item','event_english_name','event_japanese_name')
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
        filter_fields = ('romaji_name', 'attribute', 'event', 'rank', 'daily_rotation', 'daily_rotation_position', 'available')

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
        fields = ('japanese_name', 'main', 'age', 'astrological_sign', 'blood', 'attribute', 'year', 'cards__is_special', 'for_trivia')

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

class EventFilter(django_filters.FilterSet):
    idol = django_filters.CharFilter('cards__name')
    main_unit = django_filters.CharFilter('cards__idol_main_unit')
    skill = django_filters.CharFilter('cards__skill')
    attribute = django_filters.CharFilter('cards__attribute')
    is_english = django_filters.MethodFilter(action='filter_is_english')

    def filter_is_english(self, queryset, value):
        return queryset.filter(english_beginning__isnull=(False if value.title() == 'True' else True))

    class Meta:
        model = models.Event
        fields = ('idol', 'is_english', 'main_unit', 'skill', 'attribute')

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter, RandomBackend)
    search_fields = ('japanese_name', 'english_name')
    filter_class = EventFilter
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
        if 'has_friend_id' in request.query_params:
            if request.query_params['has_friend_id'].title() == 'True':
                queryset = queryset.filter(friend_id__isnull=False).exclude(friend_id=0)
            else:
                queryset = queryset.filter(Q(friend_id__isnull=True) | Q(friend_id=0))
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
    filter_fields = ('owner__username', 'nickname', 'language', 'center__card_id', 'friend_id', 'os', 'rank', 'device', 'play_with', 'accept_friend_requests', 'verified', 'owner__preferences__best_girl', 'owner__preferences__private', 'owner__preferences__status', 'center_card_attribute', 'center__card__rarity', 'owner__preferences__color')
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

class OwnedCardFilterSet(django_filters.FilterSet):
    stored = django_filters.MethodFilter(action='filter_stored')
    owner_account = CommaSeparatedValueFilter(name='owner_account', lookup_type='in')
    card__rarity = CommaSeparatedValueFilter(name='card__rarity', lookup_type='in')

    def filter_stored(self, queryset, value):
        if value == 'Album':
            return queryset.filter(Q(stored='Album') | Q(stored='Deck'))
        return queryset.filter(stored=value)

    class Meta:
        model = models.OwnedCard
        fields = ('owner_account', 'card', 'idolized', 'stored', 'max_level', 'max_bond', 'skill', 'card__name', 'card__japanese_collection', 'card__rarity', 'card__attribute', 'card__is_promo', 'card__is_special', 'card__japan_only', 'card__hp', 'card__skill', 'card__center_skill')

class OwnedCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows owned cards to be viewed or edited.
    """
    def get_queryset(self):
        queryset = models.OwnedCard.objects.all()
        queryset = queryset.filter(Q(owner_account__owner__preferences__private=False) | Q(owner_account__owner__preferences__private=True, owner_account__pk__in=(self.request.user.accounts_set.all() if self.request.user.is_authenticated() else [])))
        if ('expand_card' in self.request.query_params
            or self.request.method == 'PATCH' or self.request.method == 'PUT'):
            queryset = queryset.select_related('card')
        if 'expand_owner' in self.request.query_params:
            queryset = queryset.select_related('owner_account')
        if api_permissions.shouldSelectOwner(self.request):
            queryset = queryset.select_related('owner_account', 'owner_account__owner')
        return queryset

    serializer_class = serializers.OwnedCardSerializer
    filter_backends = (filters.DjangoFilterBackend, OwnedCardFilterBackend, filters.OrderingFilter, RandomBackend)
    filter_class = OwnedCardFilterSet
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

class ActivityFilter(django_filters.FilterSet):
    message_type = django_filters.MethodFilter(action='filter_message_type')
    account = CommaSeparatedValueFilter(name='account', lookup_type='in')
    card = django_filters.NumberFilter('ownedcard__card')
    followed_by = django_filters.MethodFilter(action='filter_followed_by')

    def filter_message_type(self, queryset, value):
        return queryset.filter(message_type=models.messageStringToInt(value))

    def filter_followed_by(self, queryset, value):
        return queryset.filter(Q(account__owner__in=(models.UserPreferences.objects.get(user__username=value).following.all())) | Q(account_id=1, message_type=models.ACTIVITY_TYPE_CUSTOM))

    class Meta:
        model = models.Activity
        fields = ('message_type', 'account', 'card', 'followed_by')

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = models.Activity.objects.all()
        if 'expand_account' in self.request.query_params:
            queryset = queryset.select_related('account')
        if 'expand_liked_by' in self.request.query_params:
            queryset = queryset.prefetch_related(Prefetch('likes', to_attr='liked_by'))
            queryset = queryset.select_related('account', 'account__owner')
        ordering = self.request.query_params.get('ordering', '')
        if ('expand_total_likes' in self.request.query_params and 'expand_liked_by' not in self.request.query_params) or 'total_likes' in ordering:
            queryset = queryset.annotate(total_likes=Count('likes'))
        if ('expand_liked' in self.request.query_params and self.request.user.is_authenticated()
            and 'expand_liked_by' not in self.request.query_params):
            queryset = queryset.extra(select={'liked': 'SELECT COUNT(*) FROM api_activity_likes WHERE activity_id=api_activity.id AND user_id={}'.format(self.request.user.id) })
        return queryset

    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('message_data',)
    filter_class = ActivityFilter
    ordering_fields = ('creation', 'total_likes')
    ordering = ('-creation',)

    @detail_route(methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        activity = get_object_or_404(models.Activity, pk=pk)
        if request.method == 'POST':
            activity.likes.add(request.user)
            request.user.preferences.save()
            return JsonResponse({'like': 'liked'})
        if request.method == 'DELETE':
            activity.likes.remove(request.user)
            request.user.preferences.save()
            return JsonResponse({'like': 'unliked'})

class EventParticipationFilter(django_filters.FilterSet):
    account = CommaSeparatedValueFilter(name='account', lookup_type='in')
    with_ranking = django_filters.MethodFilter(action='filter_with_ranking')
    with_song_ranking = django_filters.MethodFilter(action='filter_with_song_ranking')
    with_points = django_filters.MethodFilter(action='filter_with_points')
    event = django_filters.CharFilter('event__japanese_name')
    language = django_filters.CharFilter('account__language')

    def filter_with_ranking(self, queryset, value):
        return queryset.filter(ranking__isnull=(False if value.title() == 'True' else True))

    def filter_with_song_ranking(self, queryset, value):
        return queryset.filter(song_ranking__isnull=(False if value.title() == 'True' else True))

    def filter_with_points(self, queryset, value):
        return queryset.filter(points__isnull=(False if value.title() == 'True' else True))

    class Meta:
        model = models.EventParticipation
        fields = ('account', 'event', 'language', 'with_ranking', 'with_song_ranking', 'with_points')

class EventParticipationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = models.EventParticipation.objects.all()
        # do not allow fake account participations
        if 'account' not in self.request.query_params:
            queryset = queryset.filter(account__fake=False)
        if 'expand_account' in self.request.query_params:
            queryset = queryset.select_related('account')
        if 'expand_event' in self.request.query_params:
            queryset = queryset.select_related('event')
        if api_permissions.shouldSelectOwner(self.request):
            queryset = queryset.select_related('account', 'account__owner')
        return queryset

    queryset = models.EventParticipation.objects.all()
    serializer_class = serializers.EventParticipationSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = EventParticipationFilter
    ordering_fields = '__all__'
    permission_classes = (api_permissions.IsStaffOrSelf, )

class TeamViewSet(viewsets.ModelViewSet):
    def get_members_queryset(self):
        members_queryset = models.Member.objects.select_related('ownedcard')
        if 'expand_card' in self.request.query_params:
            members_queryset = members_queryset.select_related('ownedcard__card')
        return members_queryset

    def get_queryset(self):
        queryset = models.Team.objects.all().prefetch_related(Prefetch('members', queryset=self.get_members_queryset(), to_attr='all_members'))
        if api_permissions.shouldSelectOwner(self.request):
            queryset = queryset.select_related('owner_account', 'owner_account__owner')
        return queryset

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('owner_account',)
    search_fields = ('name',)
    ordering_fields = ('name', 'id', 'owner_account')
    permission_classes = (api_permissions.IsStaffOrSelf, )

    def _serialize_member(self, request, member):
        serializer = serializers.OwnedCardSerializer(member.ownedcard, context={'request': request})
        return Response(serializer.data)

    def _member_permissions(self, request, team):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        team_owner = models.Team.objects.filter(pk=team).values('owner_account__owner')
        print team_owner
        if request.user.id != team_owner['owner_account__owner']:
            raise PermissionDenied()

    def get_member(self, request, team, position):
        member = get_object_or_404(self.get_members_queryset(), team_id=team, position=(int(position) + 1))
        return self._serialize_member(request, member)

    def edit_member(self, request, team, position):
        self._member_permissions(request, team)
        #ownedcard = get_object_or_404(models.OwnedCard.annotate(owner_id='owner_account__owner_id'), pk=request.POST.get('ownedcard'))
        #if ownedcard.
        # todo create on duplicate key update
        member = get_object_or_404(self.get_members_queryset(), team_id=team, position=(int(position) + 1))
        return self._serialize_member(request, member)

    def delete_member(self, request, team, position):
        self._member_permissions(request, team)
        models.Member.objects.filter(team_id=team, position=(int(position) + 1))
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def app(request, app):
    app = raw.app_data.get(app, None)
    if app is None:
        raise Http404
    return Response(app, status=status.HTTP_200_OK)

@api_view(['GET'])
def cacheddata(request):
    return Response({
        'current_contests': settings.CURRENT_CONTESTS,
        'current_event_jp': settings.CURRENT_EVENT_JP,
        'current_event_en': settings.CURRENT_EVENT_EN,
        'cards_info': settings.CARDS_INFO,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def map(request):
    with codecs.open("map.json", "r", encoding='utf-8') as f:
        return HttpResponse(u'[{}]'.format(f.read().replace('new google.maps.LatLng(', '[').replace(') }', ']}').replace('\'', '"').replace('\\', '\\\\').replace('\n', '')).replace(',]', ']'), content_type="application/json")
