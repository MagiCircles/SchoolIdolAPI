from django.utils.translation import ugettext_lazy as _, string_concat

deck_links = [
    {
        'name': _('Search & Filter your cards'),
        'background': 'http://i.schoolido.lu/cards/transparent/72idolizedTransparent.png',
        'color': '#8f56cc',
        'link': '',
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
    },
    {
        'name': _('Cards you should max level'),
        'background': 'http://i.schoolido.lu/cards/transparent/108idolizedTransparent.png',
        'color': '#ffa500',
        'link': 'idolized=1&max_level=-1',
    },
    {
        'name': _('Your top Smile cards'),
        'background': '/static/Smile.png',
        'color': '#e6006f',
        'link': 'ordering=idolized_maximum_statistics_smile&reverse_order=on',
    },
    {
        'name': _('Your top Pure cards'),
        'background': '/static/Pure.png',
        'color': '#20ab53',
        'link': 'ordering=idolized_maximum_statistics_pure&reverse_order=on',
    },
    {
        'name': _('Your top Cool cards'),
        'background': '/static/Cool.png',
        'color': '#0098eb',
        'link': 'ordering=idolized_maximum_statistics_cool&reverse_order=on',
    },
    {
        'name': _('Cards you should max bond (kizuna)'),
        'background': 'http://i.schoolido.lu/cards/transparent/64Transparent.png',
        'color': '#72cfc3',
        'link': 'idolized=1&max_bond=-1',
    },

]
