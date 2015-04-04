from django import template
from api import models

register = template.Library()

def verifiedToString(value):
    return models.verifiedToString(value)

register.filter('verifiedToString', verifiedToString)
