from django import template
register = template.Library()

def imageurl(image):
    return str(image).replace('web', '')

register.filter('imageurl', imageurl)
