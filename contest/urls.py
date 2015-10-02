from django.conf.urls import include, patterns, url
from contest import views

urlpatterns = patterns('',
    url(r'^result/(?P<contestid>\w+)[/]+$', views.result_view),
    url(r'^results[/]+$', views.results_index_view),
    url(r'^(?P<contestid>\w+)[/]+$', views.contest_view),
    url(r'^$', views.global_contest_view),
)
