# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.conf import settings
from web import views
from web import autocomplete_views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^links[/]+$', views.links, name='links'),

    url(r'^cards[/]+$', views.cards, name='cards'),
    url(r'^card[s]?/(?P<card>\d+)[/]$', views.cards, name='cards'),
    url(r'^cards[s]?/(?P<card>\d+)/[\w-]+[/]+$', views.cards, name='cards'),

    url(r'^songs[/]+$', views.songs, name='songs'),
    url(r'^song[s]?/(?P<song>[^/]+)[/]$', views.songs, name='songs'),

    url(r'^create[/]+$', views.create, name='create'),
    url(r'^edit[/]+$', views.edit, name='edit'),
    url(r'^login[/]+$', views.login_custom_view, name='login'),
    url(r'^setaccountonlogin[/]+$', views.setaccountonlogin, name='setaccountonlogin'),
    url(r'^logout[/]+$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^addaccount[/]+$', views.addaccount, name='addaccount'),
    url(r'^editaccount/(?P<account>\d+)[/]+$', views.editaccount, name='editaccount'),
    url(r'^reportaccount/(?P<account>\d+)[/]+$', views.report, name='reportaccount'),
    url(r'^reporteventparticipation/(?P<eventparticipation>\d+)[/]+$', views.report, name='reporteventparticipation'),
    url(r'^reportuser/(?P<user>[\w.@+-]+)[/]+$', views.report, name='reportuser'),
    url(r'^reportactivity/(?P<activity>\d+)[/]+$', views.report, name='reportactivity'),

    url(r'^addteam/(?P<account>\d+)[/]+$', views.addteam, name='addteam'),
    url(r'^editteam/(?P<team>\d+)[/]+$', views.editteam, name='editteam'),
    url(r'^user[s]?/(?P<username>[\w.@+-]+)[/]+$', views.profile, name='profile'),
    url(r'^user[s]?/(?P<username>[\w.@+-]+)/messages[/]+$', views.messages, name='messages'),
    url(r'^users[/]+$', views.users, name='users'),
    url(r'^events[/]+$', views.events, name='events'),
    url(r'^event[s]?/(?P<event>[^/]+)[/]+$', views.event, name='event'),
    url(r'^event[s]?/(?P<event>[^/]+)/participations[/]+$', views.eventparticipations, name='eventparticipations'),
    url(r'^idols[/]+$', views.idols, name='idols'),
    url(r'^idol[s]?/(?P<idol>[^/]+)[/]+$', views.idol, name='idol'),
    url(r'^collections[/]+$', views.collections, name='collections'),
    url(r'^collection[s]?/(?P<collection>[^/]+)[/]+$', views.collection, name='collection'),
    url(r'^discussions[/]+$', views.discussions, name='discussions'),
    url(r'^discussion[s]?/(?P<discussion>[\w_]+)[/]$', views.discussion, name='discussion'),
    url(r'^activities/(?P<activity>\d+)[/]+$', views.activity, name='activity'),
    url(r'^map[/]+$', views.mapview, name='map'),
    url(r'^trivia[/]+$', views.trivia, name='trivia'),
    url(r'^memory[/]+$', views.memory, name='memory'),
    url(r'^about[/]+$', views.aboutview, name='about'),
    url(r'^android[/]+$', views.android, name='android'),
    url(r'^cards/albumbuilder[/]+$', views.albumbuilder, name='albumbuilder'),
    url(r'^cards/initialsetup[/]+$', views.initialsetup, name='initialsetup'),
    url(r'^skillup[/]+$', views.skillup, name='skillup'),
    url(r'^staff/verifications[/]$', views.staff_verifications, name='staff_verifications'),
    url(r'^staff/verification/(?P<verification>\d+)[/]$', views.staff_verification, name='staff_verification'),
    url(r'^staff/reports[/]$', views.staff_reports, name='staff_reports'),
    url(r'^staff/moderation[/]$', views.staff_moderation, name='staff_moderation'),
    url(r'^staff/database[/]$', views.staff_database, name='staff_database'),
    url(r'^staff/database/(?P<script>[\w -_]+)[/]$', views.staff_database_script, name='staff_database_script'),
    url(r'^staff/editcard/(?P<id>\d+)[/]$', views.staff_editcard, name='staff_editcard'),
    url(r'^staff/editevent/(?P<id>\d+)[/]$', views.staff_editevent, name='staff_editevent'),
    url(r'^staff/editsong/(?P<id>\d+)[/]$', views.staff_editsong, name='staff_editsong'),
    url(r'^urpairs[/]+$', views.urpairs, name='urpairs'),
    url(r'^english_future[/]+$', views.english_future, name='english_future'),
    url(r'^.sicaltriofestival[/]+$', views.usicaltriofestival, name='usicaltriofestival'),

    url(r'^password_reset[/]+$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'password/password_reset_form.html',
        'html_email_template_name': 'password/password_reset_email_html.html',
        'from_email': settings.AWS_PASSWORD_EMAIL,
     }, name='password_reset'),
    url(r'^password_reset/done[/]+$', 'django.contrib.auth.views.password_reset_done', {
        'template_name': 'password/password_reset_done.html'
    }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, {
        'template_name': 'password/password_reset_confirm.html'
    }, name='password_reset_confirm'),
    url(r'^reset/done[/]+$', 'django.contrib.auth.views.password_reset_complete', {
        'template_name': 'password/password_reset_complete.html'
    }, name='password_reset_complete'),

    url(r'^ajax/modal/(?P<hash>\w+)[/]+$', views.ajaxmodal, name='ajaxmodal'),
    url(r'^ajax/addcard[/]+$', views.ajaxaddcard, name='ajaxaddcard'),
    url(r'^ajax/editcard/(?P<ownedcard>\d+)[/]+$', views.ajaxeditcard, name='ajaxeditcard'),
    url(r'^ajax/deletecard/(?P<ownedcard>\d+)[/]+$', views.ajaxdeletecard, name='ajaxdeletecard'),
    url(r'^ajax/albumbuilder/editcard/(?P<ownedcard_id>\d+)[/]+$', views.ajax_albumbuilder_editcard, name='ajax_albumbuilder_editcard'),
    url(r'^ajax/albumbuilder/addcard/(?P<card_id>\d+)[/]+$', views.ajax_albumbuilder_addcard, name='ajax_albumbuilder_addcard'),
    url(r'^ajax/deletelink/(?P<link>\d+)[/]+$', views.ajaxdeletelink, name='ajaxdeletelink'),
    url(r'^ajax/cards[/]+$', views.ajaxcards, name='ajaxcards'),
    url(r'^ajax/songs[/]+$', views.ajaxsongs, name='ajaxsongs'),
    url(r'^ajax/users[/]+$', views.ajaxusers, name='ajaxusers'),
    url(r'^ajax/notifications[/]+$', views.ajaxnotifications, name='ajaxnotifications'),
    url(r'^ajax/messages/(?P<username>[\w.@+-]+)[/]+$', views.messages, { 'ajax': True }, name='messages'),
    url(r'^ajax/accounttab/(?P<account>\d+)/(?P<tab>\w+)[/]+$', views.ajaxaccounttab, name='ajaxaccounttab'),
    url(r'^ajax/accounttab/(?P<account>\d+)/(?P<tab>\w+)/more[/]+$', views.ajaxaccounttab, { 'more': True }, name='ajaxaccounttab'),
    url(r'^ajax/follow/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollow, name='ajaxfollow'),
    url(r'^ajax/followers/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollowers, name='ajaxfollowers'),
    url(r'^ajax/following/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollowing, name='ajaxfollowing'),
    url(r'^ajax/activities[/]+$', views.ajaxactivities, name='ajaxactivities'),
    url(r'^ajax/likeactivity/(?P<activity>\d+)[/]+$', views.ajaxlikeactivity, name='ajaxlikeactivity'),
    url(r'^ajax/feed[/]+$', views.ajaxfeed, name='ajaxfeed'),
    url(r'^ajax/eventranking/(?P<event>\d+)/(?P<language>\w+)[/]+$', views.ajaxeventranking, name='ajaxeventranking'),
    url(r'^ajax/staff/verification/(?P<verification>\d+)/inprogress[/]+$', views.ajaxverification, {'status': 2}, name='ajaxverification'),
    url(r'^ajax/staff/verification/(?P<verification>\d+)/cancel[/]+$', views.ajaxverification, {'status': 1}, name='ajaxverification'),
    url(r'^ajax/staff/verification/(?P<verification>\d+)/deleteimage/(?P<image>\d+)[/]+$', views.ajaxstaffverificationdeleteimage, name='ajaxstaffverificationdeleteimage'),
    url(r'^ajax/staff/report/(?P<report_id>\d+)/accept/$', views.ajaxreport, {'status': 'accept'}, name='ajaxreport'),
    url(r'^ajax/staff/report/(?P<report_id>\d+)/reject/$', views.ajaxreport, {'status': 'reject'}, name='ajaxreport'),
    url(r'^ajax/trivia/share/', views.sharetrivia, name='sharetrivia'),
    url(r'^ajax/markhot/', views.markhot, name='markhot'),
    url(r'^ajax/removehot/', views.removehot, name='removehot'),
    url(r'^ajax/bump/', views.bump, name='bump'),
    url(r'^ajax/drown/', views.drown, name='drown'),

    url(r'^autocomplete/user/', autocomplete_views.UserAutocomplete.as_view(), name='autocomplete-user'),

    url(r'^avatar/twitter/(?P<username>[\w.@+-]+)[/]+$', views.avatar_twitter, name='avatar_twitter'),
    url(r'^avatar/facebook/(?P<username>[\w.@+-]+)[/]+$', views.avatar_facebook, name='avatar_facebook'),

    url(r'^i18n/', include('django.conf.urls.i18n')),
)
