from django import template
from api import models

register = template.Library()

def verifiedToString(value):
    return models.verifiedToString(value)

def playWithToString(value):
    return models.playWithToString(value)

register.filter('verifiedToString', verifiedToString)
register.filter('playWithToString', playWithToString)
