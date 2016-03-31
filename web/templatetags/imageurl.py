from django import template
from django.conf import settings
from web.utils import chibiimage as _chibiimage
from web.templatetags.getattribute import getattribute
from api.models import LINK_URLS
from api.raw import raw_information
import os.path
import string
import re
import random

register = template.Library()

def _imageurl(path):
    return '%s%s' % (settings.IMAGES_HOSTING_PATH, path)

@register.simple_tag(takes_context=True)
def imageurl(context, card, image):
    # April fool stuff
    dummy = 'force_dummy' in context
    if not dummy:
        dummy = bool(random.getrandbits(1))
    idols = [u'Kousaka Honoka', u'Nishikino Maki', u'Ayase Eli', u'Minami Kotori', u'Hoshizora Rin', u'Koizumi Hanayo', u'Sonoda Umi', u'Toujou Nozomi', u'Yazawa Nico']
    if dummy and (card.rarity == 'SR' or card.rarity == 'R') and (image == 'card_image' or image == 'card_idolized_image') and card.name in idols:
        return '{}{}'.format(settings.IMAGES_HOSTING_PATH, 'cards/dummy/' + card.rarity + card.attribute + card.name.replace(' ', '_').replace('\'', '-') + ('Idolized' if image == 'card_idolized_image' else '') + '.png')
    # / April fool stuff
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            return _imageurl(unicode(card_image))
    return '/static/default-' + card.attribute + '.png'

@register.simple_tag(takes_context=True)
def cleanurl(context, card, idolized):
    if idolized:
        if card.clean_ur_idolized:
            return _imageurl(str(card.clean_ur_idolized).replace('/cards/ur_pairs/', '/cards/ur_pairs/small_'))
        return _imageurl(str(card.card_idolized_image))
    else:
        if card.clean_ur:
            return _imageurl(str(card.clean_ur).replace('/cards/ur_pairs/', '/cards/ur_pairs/small_'))
        return _imageurl(str(card.card_image))

@register.simple_tag()
def cardrawurl(card_id, idol_name, image_type):
    if image_type == 'round_card_image':
        return _imageurl('cards/' + str(card_id) + 'Round' + idol_name + '.png')
    elif image_type == 'round_card_idolized_image':
        return _imageurl('cards/' + str(card_id) + 'RoundIdolized' + idol_name + '.png')
    elif image_type == 'card_image':
        return _imageurl('cards/' + str(card_id) + idol_name + '.png')
    elif image_type == 'card_image':
        return _imageurl('cards/' + str(card_id) + 'idolized' + idol_name + '.png')
    return '/static/empty.png'

@register.simple_tag()
def cardidolizedimageurl(card, idolized):
    if card.is_special or card.is_promo:
        idolized = True
    if idolized:
        if card.round_card_idolized_image:
            return _imageurl(card.round_card_idolized_image)
        if card.card_idolized_image:
            return _imageurl(card.card_idolized_image)
        return '/static/default-' + card.attribute + '.png'
    if card.round_card_image:
        return _imageurl(card.round_card_image)
    if card.card_image:
        return _imageurl(card.card_image)
    return '/static/default-' + card.attribute + '.png'

@register.simple_tag(takes_context=True)
def ownedcardimageurl(context, ownedcard, card=None):
    if not ownedcard:
        return '/static/default-All.png'
    if not card:
        card = ownedcard.card
    idolized = True if card.is_special or card.is_promo else ownedcard.idolized
    return cardidolizedimageurl(card, idolized)

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
        if idol.main_unit == 'Aqours':
            if number == 5:
                return raw_information[idol.name]['image'].replace('Transparent', 'idolizedTransparent')
            return raw_information[idol.name]['image']
        m = re.search(r'[^0-9]+(?P<number>[0-9]+)[.]html$', idol.official_url)
        member_number = m.group('number')
        return 'http://www.lovelive-anime.jp/otonokizaka/img/member/member' + member_number + '_0'+ str(number) + '.png'
    return ''

@register.simple_tag(takes_context=True)
def idolimage(context, name):
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

@register.filter
def accountattribute(account):
    if account.fake:
        return 'default'
    if account.center:
        return account.center.card.attribute
    return 'All'

register.filter('userimage', userimage)
register.filter('linkimage', linkimage)
register.filter('linkurl', linkurl)
