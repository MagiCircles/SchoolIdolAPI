from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
import api.views as api_views
from django.views.generic.base import RedirectView

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'cards', api_views.CardViewSet)
router.register(r'idols', api_views.IdolViewSet)
router.register(r'cardids', api_views.CardIdViewSet)
router.register(r'events', api_views.EventViewSet)
router.register(r'songs', api_views.SongViewSet)

router.register(r'users', api_views.UserViewSet)
router.register(r'ownedcards', api_views.OwnedCardViewSet, base_name='ownedcard')
router.register(r'accounts', api_views.AccountViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include('web.urls')),
    url(r'^api[/]+$', RedirectView.as_view(url='https://github.com/SchoolIdolTomodachi/SchoolIdolAPI/wiki/LoveLive!-School-Idol-API', permanent=False), name='api'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/app/(?P<app>[\w.-]+)[/]+$', api_views.app),
    url(r'^admin/', include(admin.site.urls)),
]
