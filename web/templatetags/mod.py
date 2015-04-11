from django import template
register = template.Library()

def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False

def isnone(value):
    return value is None

def torfc2822(date):
    return date.strftime("%B %d, %Y %H:%M:%S %z")

register.filter('mod', mod)
register.filter('isnone', isnone)
register.filter('torfc2822', torfc2822)
