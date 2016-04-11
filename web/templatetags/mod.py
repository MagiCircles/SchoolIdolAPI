from django import template
from django.utils.translation import ugettext_lazy as _, string_concat
from django.utils import timezone
from web.views import findAccount
from web.utils import singlecardurl
from django.forms.fields import NullBooleanField, BooleanField, DateTimeField
from dateutil.relativedelta import relativedelta
import random

register = template.Library()

def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False

def trans(value):
    return _(value)

def transconcat(value, svalue):
    return string_concat(_(value), _(svalue))

def transconcatspace(value, svalue):
    return string_concat(_(value), ' ', _(svalue))

@register.filter
def multiply(value1, value2):
    return value1 * value2

@register.filter
def tourldash(string):
    return ''.join(e if e.isalnum() else '-' for e in string)

@register.filter
def is_boolean(field):
    if isinstance(field.field, NullBooleanField):
        return False
    if isinstance(field.field, BooleanField):
        return True
    return False

@register.filter
def is_int(val):
    return isinstance(val, int)

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def has_permission(user, permission):
    return user.has_permission(permission)

@register.filter
def range(min, max):
    return range(min, max)

def isnone(value):
    return value is None

def plusmonths(date, months):
    return date + relativedelta(months=months)

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
register.filter('singlecardurl', singlecardurl)
register.filter('trans', trans)
register.filter('transconcat', transconcat)
register.filter('transconcatspace', transconcatspace)
register.filter('plusmonths', plusmonths)
register.filter('isnone', isnone)
register.filter('torfc2822', torfc2822)
register.filter('addstr', addstr)
register.filter('findModelId', findModelId)
register.filter('activity_is_mine', activity_is_mine)
