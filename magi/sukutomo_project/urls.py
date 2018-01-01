from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sukutomo_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('magi.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
