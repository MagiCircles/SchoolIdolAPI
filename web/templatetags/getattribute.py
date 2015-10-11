import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        if callable(getattr(value, arg)):
            return getattr(value, arg)()
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    elif str(arg) in value:
        return value.get(arg)
    try: return value[arg]
    except: return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)

from api.models import japanese_attribute as jpa

def japanese_attribute(attribute):
    return jpa(attribute)

register.filter('japanese_attribute', japanese_attribute)

# Then, in template:
# {% load getattribute %}
# {{ object|getattribute:dynamic_string_var }}
