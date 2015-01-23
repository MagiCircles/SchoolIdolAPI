from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
import api.views as api_views
import web.views as web_views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'api/users', api_views.UserViewSet)
router.register(r'api/cards', api_views.CardViewSet)
router.register(r'api/events', api_views.EventViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
