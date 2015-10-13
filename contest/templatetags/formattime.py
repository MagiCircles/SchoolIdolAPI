from django import template
register = template.Library()

def formattime(date, fmt):
    return date.strftime(fmt)

def shortname(name):
    return name.split(' ')[-1]

def formatseconds(seconds):
    return int(seconds / 3600)

register.filter('formattime', formattime)
register.filter('formatseconds', formatseconds)
register.filter('shortname', shortname)
