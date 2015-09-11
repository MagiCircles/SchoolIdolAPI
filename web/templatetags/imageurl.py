from django import template
from django.conf import settings
from web.utils import chibiimage
from api.models import LINK_URLS
import os.path
import re

register = template.Library()

def imageurl(card, image):
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            #if settings.DEBUG:
             #   card_image = unicode(card_image).replace('web/', '')
            return '%s%s' % (settings.IMAGES_HOSTING_PATH, str(card_image))
        elif hasattr(card, image.replace('image', 'url')):
            url = getattr(card, image.replace('image', 'url'))
            if url:
                return url
    return '/static/default-' + card.attribute + '.png'

def eventimageurl(event):
    if event.image:
        if settings.DEBUG:
            event.image = unicode(event.image).replace('web/', '')
        return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(event.image))
    return ''

def standimage(idol, number):
    if idol is not None:
        m = re.search(r'[^0-9]+(?P<number>[0-9]+)[.]html$', idol.official_url)
        member_number = m.group('number')
        return 'http://www.lovelive-anime.jp/otonokizaka/img/member/member' + member_number + '_0'+ str(number) + '.png'
    return ''

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

register.filter('imageurl', imageurl)
register.filter('standimage', standimage)
register.filter('chibiimage', chibiimage)
register.filter('eventimageurl', eventimageurl)
register.filter('linkimage', linkimage)
register.filter('linkurl', linkurl)
