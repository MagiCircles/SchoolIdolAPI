from django import template
from api import models

register = template.Library()

def storedChoiceToString(value):
    return models.storedChoiceToString(value)

register.filter('storedChoiceToString', storedChoiceToString)
