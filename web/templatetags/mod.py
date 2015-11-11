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

def addstr(a, b):
    return unicode(a) + unicode(b)

def findModelId(array, id):
    return next(obj for obj in array if obj.id == id)

register.filter('mod', mod)
register.filter('isnone', isnone)
register.filter('torfc2822', torfc2822)
register.filter('addstr', addstr)
register.filter('findModelId', findModelId)
