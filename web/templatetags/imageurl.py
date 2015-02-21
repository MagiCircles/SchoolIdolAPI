from django import template
register = template.Library()

HOSTING = 'http://schoolido.lu-assets.s3-website-ap-northeast-1.amazonaws.com/'

def imageurl(card, image):
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            return '%s%s' % (HOSTING, str(card_image))
        elif hasattr(card, image.replace('image', 'url')):
            url = getattr(card, image.replace('image', 'url'))
            if url:
                return url
    return '/static/default-' + card.attribute + '.png'

register.filter('imageurl', imageurl)
