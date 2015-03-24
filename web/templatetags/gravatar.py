from django import template
from web.views import getUserAvatar, getUserPreferencesAvatar

register = template.Library()

def gravatar(value, size=200):
    return getUserAvatar(value, size)

def gravatarpreferences(user, preferences):
    return getUserPreferencesAvatar(user, preferences, 200)

register.filter('gravatar', gravatar)
register.filter('gravatarpreferences', gravatarpreferences)

