from django import template
register = template.Library()

def imageurl(card, image):
    if hasattr(card, image):
        card_image = getattr(card, image)
        if card_image:
            return str(card_image).replace('web', '')
        elif hasattr(card, image.replace('image', 'url')):
            url = getattr(card, image.replace('image', 'url'))
            if url:
                return url
    return '/static/default-' + card.attribute + '.png'

register.filter('imageurl', imageurl)
