from django import template
from django.conf import settings
from web.utils import chibiimage as _chibiimage
from api.models import LINK_IMAGES, LINK_URLS
from api.raw import raw_information
import os.path
import string
import re

register = template.Library()

def _imageurl(path, context={}):
    return u'{static_url}{path}'.format(
        static_url = context.get('static_url', settings.STATIC_FILES_URL),
        path=path,
    )

@register.simple_tag(takes_context=True)
def imageurl(context, card, image, english_version=False):
    """
    Return one image field (image=field name) in a card object.
    Returns a default image when the field doesn't exist or the card doesn't have this image stored.
    """
    if english_version:
        image = 'english_' + image
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            return _imageurl(unicode(card_image), context=context)
    return context['static_url'] + u'static/default-' + card.attribute + '.png'

@register.filter
def account_is_world(account):
    return account.language != 'JP'

@register.simple_tag(takes_context=True)
def cleanurl(context, card, idolized, small=True):
    """
    Returns the URL of the clean UR image
    """
    if idolized:
        if card.clean_ur_idolized:
            if small:
                return _imageurl(str(card.clean_ur_idolized).replace('/cards/ur_pairs/', '/cards/ur_pairs/small_'), context=context)
            else:
                return _imageurl(str(card.clean_ur_idolized), context=context)
        return _imageurl(str(card.card_idolized_image), context=context)
    else:
        if card.clean_ur:
            if small:
                return _imageurl(str(card.clean_ur).replace('/cards/ur_pairs/', '/cards/ur_pairs/small_'), context=context)
            else:
                return _imageurl(str(card.clean_ur), context=context)
        return _imageurl(str(card.card_image), context=context)

@register.simple_tag(takes_context=True)
def cardrawurl(context, card_id, idol_name, image_type, english_version=False):
    """
    Returns an image URL that _should_ exist but not guaranteed, depending on a few info on the card.
    """
    prefix = 'c/'
    if english_version:
        prefix = 'cards/'
    if image_type == 'round_card_image':
        return _imageurl(prefix + str(card_id) + 'Round' + idol_name + '.png', context=context)
    elif image_type == 'round_card_idolized_image':
        return _imageurl(prefix + str(card_id) + 'RoundIdolized' + idol_name + '.png', context=context)
    elif image_type == 'card_image':
        return _imageurl(prefix + str(card_id) + idol_name + '.png', context=context)
    elif image_type == 'card_image':
        return _imageurl(prefix + str(card_id) + 'idolized' + idol_name + '.png', context=context)
    return _imageurl('static/empty.png', context=context)

@register.simple_tag(takes_context=True)
def cardidolizedimageurl(context, card, idolized, english_version=False):
    """
    Returns an image URL for a card in the context of School Idol Contest
    """
    prefix = 'english_' if english_version else ''
    if card.is_special or card.is_promo:
        idolized = True
    if idolized:
        if getattr(card, prefix + 'round_card_idolized_image'):
            return _imageurl(getattr(card, prefix + 'round_card_idolized_image'), context=context)
        if getattr(card, prefix + 'card_idolized_image'):
            return _imageurl(getattr(card, prefix + 'card_idolized_image'), context=context)
        return _imageurl('static/default-' + card.attribute + '.png', context=context)
    if getattr(card, prefix + 'round_card_image'):
        return _imageurl(getattr(card, prefix + 'round_card_image'), context=context)
    if getattr(card, prefix + 'card_image'):
        return _imageurl(getattr(card, prefix + 'card_image'), context=context)
    return _imageurl('static/default-' + card.attribute + '.png', context=context)

@register.simple_tag(takes_context=True)
def ownedcardimageurl(context, ownedcard, card=None, english_version=False):
    if not ownedcard:
        return _imageurl('static/default-All.png', context=context)
    if not card:
        card = ownedcard.card
    idolized = True if card.is_special or card.is_promo else ownedcard.idolized
    return cardidolizedimageurl(context, card, idolized, english_version=english_version)

@register.simple_tag(takes_context=True)
def eventimageurlwithreplace(context, event, english=False):
    if english and event.english_image:
        return _imageurl(event.english_image, context=context).replace('\'', "\\'")
    if event.image:
        return _imageurl(event.image, context=context).replace('\'', "\\'")
    return _imageurl('static/default_event.png', context=context)

@register.simple_tag(takes_context=True)
def eventimageurl(context, event, english=False):
    if english and event.english_image:
        return _imageurl(event.english_image, context=context)
    if event.image:
        return _imageurl(event.image, context=context)
    return _imageurl('static/default_event.png', context=context)

@register.simple_tag(takes_context=True)
def songimageurl(context, song):
    if song.image:
        return _imageurl(song.image, context=context)
    return _imageurl('static/defaultsong.png', context=context)

def userimage(image):
    return _imageurl(image)

@register.simple_tag(takes_context=True)
def standimage(context, idol, number):
    if idol is not None:
        if idol.main_unit == 'Aqours':
            if number == 5:
                return raw_information[idol.name]['image'].replace('Transparent', 'idolizedTransparent')
            return raw_information[idol.name]['image']
        if idol.official_url:
            m = re.search(r'[^0-9]+(?P<number>[0-9]+)[.]html$', idol.official_url)
            member_number = m.group('number')
            return 'http://www.lovelive-anime.jp/otonokizaka/img/member/member' + member_number + '_0'+ str(number) + '.png'
    return ''

@register.simple_tag(takes_context=True)
def idolimage(context, name):
    filename = name.replace(' ', '_').replace('\'', '-')
    return filename

def linkimage(link):
    return LINK_IMAGES.get(link['type'], None)

def linkurl(link):
    return LINK_URLS[link['type']].format(link['value'])

@register.simple_tag(takes_context=True)
def chibiimage(context, idol, small=True, force_first=False, force_artist=False):
    return _chibiimage(idol, small, force_first=force_first, force_artist=force_artist)

@register.filter
def chibioriginal(link):
    return link.replace('/chibi/', '/chibi/original-')

@register.filter
def accountattribute(account):
    if account.fake:
        return 'default'
    if account.center_id:
        return account.center_card_attribute
    return 'All'

register.filter('userimage', userimage)
register.filter('linkimage', linkimage)
register.filter('linkurl', linkurl)
