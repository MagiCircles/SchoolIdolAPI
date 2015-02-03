from django import template
register = template.Library()

def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False

register.filter('mod', mod)
