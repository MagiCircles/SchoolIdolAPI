from django import template
register = template.Library()

def times(value):
    return range(value)

register.filter('times', times)
