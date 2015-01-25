from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
import api.views as api_views
#import web.views as web_views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'cards', api_views.CardViewSet)
router.register(r'events', api_views.EventViewSet)
router.register(r'accounts', api_views.AccountViewSet, base_name='account')
router.register(r'ownedcards', api_views.OwnedCardViewSet, base_name='ownedcard')
router.register(r'cardids', api_views.CardIdViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
