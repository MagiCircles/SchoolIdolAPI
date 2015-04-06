from django import template
register = template.Library()

def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False

def isnone(value):
    return value is None

register.filter('mod', mod)
register.filter('isnone', isnone)
