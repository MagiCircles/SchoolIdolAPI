from django.conf.urls import include, patterns, url
from contest import views

urlpatterns = patterns('',
    url(r'^result/(?P<contestid>\w+)[/]+$', views.result_view),
    url(r'^result/(?P<contestid>\w+)/[\w-]+[/]+$', views.result_view),
    url(r'^best[/]+$', views.global_result_view),
    url(r'^result[/]+$', views.global_result_view),
    url(r'^results[/]+$', views.results_index_view),
    url(r'^(?P<contestid>\d+)[/]+$', views.contest_view),
    url(r'^(?P<contestid>\d+)/[\w-]+[/]+$', views.contest_view),
    url(r'^$', views.global_contest_view),
)
