# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, string_concat
from api import raw as api_raw
from api import models

notifications = {
    'ADDACCOUNTRANK200': {
        'link': '/editaccount/{}/#verify',
        'link_text': _('Get verified'),
        'message': _('Only verified accounts can have a rank above 200.'),
        'left_html': '<i class=\'flaticon-star fontx3 verified2\'></i>',
    },
}

deck_links = [
    {
        'name': _('Search & Filter your cards'),
        'background': 'http://i.schoolido.lu/cards/transparent/72idolizedTransparent.png',
        'color': '#8f56cc',
        'link': 'ordering=game_rarity&reverse_order=on',
    },
    {
        'name': _('Your Perfect Lock cards'),
        'background': 'http://i.schoolido.lu/cards/transparent/73Transparent.png',
        'color': '#205cbf',
        'link': 'skill=Perfect Lock',
    },
    {
        'name': _('Your Healer cards'),
        'background': 'http://i.schoolido.lu/cards/transparent/57idolizedTransparent.png',
        'color': '#65dba2',
        'link': 'skill=Healer',
        'end_row': True,
    },
    {
        'name': _('Your top Smile cards'),
        'background': '/static/Smile.png',
        'color': '#e6006f',
        'link': 'ordering=idolized_maximum_statistics_smile&reverse_order=on',
        'background_size': 80,
        'background_position_x': -90,
    },
    {
        'name': _('Your top Pure cards'),
        'background': '/static/Pure.png',
        'color': '#20ab53',
        'link': 'ordering=idolized_maximum_statistics_pure&reverse_order=on',
        'background_size': 80,
        'background_position_x': -90,
    },
    {
        'name': _('Your top Cool cards'),
        'background': '/static/Cool.png',
        'color': '#0098eb',
        'link': 'ordering=idolized_maximum_statistics_cool&reverse_order=on',
        'background_size': 80,
        'background_position_x': -90,
        'end_row': True,
    },
    {
        'name': _('Cards you should max level'),
        'background': 'http://i.schoolido.lu/cards/transparent/108idolizedTransparent.png',
        'color': '#ffa500',
        'link': 'idolized=1&max_level=-1',
        'col_size': 6,
        'background_size': 110,
        'background_position_x': 340,
        'sm': True,
   },
    {
        'name': _('Cards you should max bond'),
        'background': 'http://i.schoolido.lu/cards/transparent/64Transparent.png',
        'color': '#72cfc3',
        'link': 'idolized=1&max_bond=-1',
        'col_size': 6,
        'background_size': 101,
        'background_position_x': 3500,
        'sm': True,
    },
]

discussions = [
    {
        'code': 'sukutomo',
        'name': _('School Idol Tomodachi'),
        'image': '/static/screenshots/home_blurred.png',
        'color': '#ffffff',
        'alt_color': '#ff53b9',
        'big': True,
        'hide_background': True,
    },
    {
        'code': 'FAQsukutomo',
        'name': string_concat(_('F.A.Q.'), ' ', _('School Idol Tomodachi')),
        'image': '/static/SchoolIdolTomodachi.svg',
        'color': '#ffffff',
        'alt_color': '#ff53b9',
    },
    {
        'code': 'FAQ',
        'name': string_concat(_('F.A.Q.'), ' ', _('LoveLive! School Idol Festival')),
        'image': 'http://www.school-fes.klabgames.net/img/img_main.png#/static/',
        'color': '#ff53b9',
    },
    {
        'code': 'FAQenglish',
        'name': string_concat(_('F.A.Q.'), ' ', _('LoveLive! School Idol Festival'), ' ', _(models.languageToString('EN'))),
        'image': '/static/usa.png',
        'color': '#0d87ff',
    },
    {
        'code': 'FAQjapanese',
        'name': string_concat(_('F.A.Q.'), ' ', _('LoveLive! School Idol Festival'), ' ', _(models.languageToString('JP'))),
        'image': '/static/japan.png',
        'color': '#f47b7f',
    },
    {
        'code': 'FAQother',
        'name': string_concat(_('F.A.Q.'), ' ', _('LoveLive! School Idol Festival'), ' ', _(models.languageToString('KR')), ', ', _(models.languageToString('CN')), ', ', _(models.languageToString('TW'))),
        'image': '/static/china.png',
        'color': '#7ed68a',
    },
    {
        'code': 'drawings',
        'name': string_concat(_('LoveLive!'), ' ', _('Drawings & fan-arts')),
        'image': 'http://i.schoolido.lu/cards/transparent/684Transparent.png',
        'color': '#56d1ff',
    },
    {
        'code': 'cosplay',
        'name': string_concat(_('LoveLive!'), ' ', _('Cosplay')),
        'image': 'http://i.schoolido.lu/cards/transparent/687idolizedTransparent.png',
        'color': '#9a59cb',
        'big': True,
    },
    {
        'code': 'comedy',
        'name': string_concat(_('LoveLive!'), ' ', _('MEMES & comedy')),
        'image': 'http://i.schoolido.lu/cards/transparent/686Transparent.png',
        'color': '#fff766',
        'alt_color': '#7ed68a',
    },
    {
        'code': 'soloyolo',
        'name': _('Your best SOLO YOLOs'),
        'image': '/static/soloyolo.png',
        'color': '#f4739d',
        'big': True,
    },
    {
        'code': '101',
        'name': _('Your best 10+1 pulls'),
        'image': '/static/10+1.png',
        'color': '#f4739d',
        'big': True,
    },
    {
        'code': 'scores',
        'name': _('Your best scores'),
        'image': '/static/score.png',
        'color': '#7ed68a',
        'big': True,
    },
    {
        'link': '/cards/',
        'name': string_concat(_('Discuss'), ' ', _('Cards')),
        'image': '/static/screenshots/cards_blurred.png',
        'color': '#989898',
        'big': True,
    },
    {
        'link': '/songs/',
        'name': string_concat(_('Discuss'), ' ', _('Songs')),
        'image': '/static/screenshots/songs_blurred.png',
        'color': '#989898',
        'big': True,
    },
    {
        'link': '/events/',
        'name': string_concat(_('Discuss'), ' ', _('Events')),
        'image': '/static/screenshots/events_blurred.png',
        'color': '#989898',
        'big': True,
    },
] + [{
    'name': idol,
    'image': api_raw.raw_information[idol]['image'],
    'color': api_raw.raw_information[idol]['color'],
    'link': '/idol/' + idol + '/',
        'big': True,
} for idol in api_raw.raw_information] + [
    {
        'code': 'usicforever',
        'not_translate_name': True,
        'name': 'μ\'sic forever',
        'image': 'http://i.schoolido.lu/cards/transparent/846idolizedTransparent.png',
        'color': '#4075c1',
        'full_size': True,
    },
]
