from django import template
from django.utils.translation import ugettext_lazy as _, string_concat
from web.views import findAccount
import random

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

positiveAdjectives = [
    _('lovely'),
    _('awesome'),
    _('incredible'),
    _('adorable'),
    _('generous'),
    _('idols-addicted'),
    _('friendly'),
    _('kind'),
    _('warmhearted'),
    _('nice'),
]

@register.simple_tag()
def randomPositiveAdjective():
    return random.choice(positiveAdjectives)

def activity_is_mine(activity, accounts):
    return findAccount(activity.account_id, accounts)

register.filter('mod', mod)
register.filter('isnone', isnone)
register.filter('torfc2822', torfc2822)
register.filter('addstr', addstr)
register.filter('findModelId', findModelId)
register.filter('activity_is_mine', activity_is_mine)
