from django import template
register = template.Library()

def times(value):
    if value:
        return range(value)
    return []

register.filter('times', times)
