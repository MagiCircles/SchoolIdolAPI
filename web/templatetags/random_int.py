from django import template
import random

register = template.Library()

def random_int(minimum, maximum):
    return random.randint(minimum, maximum)

register.filter('random_int', random_int)
