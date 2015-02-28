from django import template
from django.conf import settings
register = template.Library()

def imageurl(card, image):
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            if settings.DEBUG:
                card_image = unicode(card_image).replace('web/', '')
            return '%s%s' % (settings.IMAGES_HOSTING_PATH, str(card_image))
        elif hasattr(card, image.replace('image', 'url')):
            url = getattr(card, image.replace('image', 'url'))
            if url:
                return url
    return '/static/default-' + card.attribute + '.png'

def eventimageurl(event):
    print event
    if event.image:
        if settings.DEBUG:
            event.image = unicode(event.image).replace('web/', '')
        return u'%s%s' % (settings.IMAGES_HOSTING_PATH, unicode(event.image))
    return ''

register.filter('imageurl', imageurl)
register.filter('eventimageurl', eventimageurl)
