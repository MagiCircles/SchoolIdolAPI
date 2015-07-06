from django import template
from web.views import getUserAvatar

register = template.Library()

def _getUserAvatar(user, size=200):
    return getUserAvatar(user, size)

register.filter('gravatar', _getUserAvatar)
