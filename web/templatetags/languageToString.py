from django import template
from api import models_languages as models

register = template.Library()

def languageToString(value):
    return models.languageToString(value)

register.filter('languageToString', languageToString)
