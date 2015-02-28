from django import template
from web.views import getUserAvatar

register = template.Library()

def gravatar(value, size=200):
    return getUserAvatar(value, size)

register.filter('gravatar', gravatar)

