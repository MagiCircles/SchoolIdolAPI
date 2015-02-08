from django import template
register = template.Library()

def padzeros(value, length):
    if value is None:
        return None
    return ("%0" + str(length) + "d") % value

register.filter('padzeros', padzeros)
