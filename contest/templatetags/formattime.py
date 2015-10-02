from django import template
register = template.Library()

def formattime(date, fmt):
    return date.strftime(fmt) 

def shortname(name):
    return name.split(' ')[-1]

register.filter('formattime', formattime)
register.filter('shortname', shortname)
