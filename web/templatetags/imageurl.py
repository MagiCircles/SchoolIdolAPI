from django import template
from django.conf import settings
from web.utils import chibiimage as _chibiimage
from api.models import LINK_URLS
import os.path
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def imageurl(context, card, image):
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            return '%s%s' % (settings.IMAGES_HOSTING_PATH, str(card_image))
        elif hasattr(card, image.replace('image', 'url')):
            url = getattr(card, image.replace('image', 'url'))
            if url:
                return url
    return '/static/default-' + card.attribute + '.png'

@register.simple_tag(takes_context=True)
def eventimageurl(context, event, english=False):
    if english and event.english_image:
        return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(event.english_image))
    if event.image:
        return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(event.image))
    return '/static/default_event.png'

@register.simple_tag(takes_context=True)
def songimageurl(context, song):
    if song.image:
        if settings.DEBUG:
            song.image = unicode(song.image).replace('web/', '')
        return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(song.image))
    return '/static/defaultsong.png'

def userimage(image):
    return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(image))

@register.simple_tag(takes_context=True)
def standimage(context, idol, number):
    if idol is not None:
        m = re.search(r'[^0-9]+(?P<number>[0-9]+)[.]html$', idol.official_url)
        member_number = m.group('number')
        return 'http://www.lovelive-anime.jp/otonokizaka/img/member/member' + member_number + '_0'+ str(number) + '.png'
    return ''

@register.simple_tag(takes_context=True)
def idolimage(name):
    filename = name.replace(' ', '_').replace('\'', '-')
    return filename

linkimages = {
    'reddit': '/static/reddit.png',
    'twitter': '/static/twitter.png',
    'facebook': '/static/facebook.png',
    'instagram': '/static/instagram.png',
    'line': '/static/line.png',
    'twitch': '/static/twitch.png',
    'mal': '/static/mal.png',
    'steam': '/static/steam.png',
    'tumblr': '/static/tumblr.png',
}

def linkimage(link):
    return linkimages.get(link['type'], None)

def linkurl(link):
    return LINK_URLS[link['type']].format(link['value'])

@register.simple_tag(takes_context=True)
def chibiimage(context, idol, small=True):
    return _chibiimage(idol, small)

register.filter('userimage', userimage)
register.filter('linkimage', linkimage)
register.filter('linkurl', linkurl)
