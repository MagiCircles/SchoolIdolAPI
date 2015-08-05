import urllib2, urllib
import json
import os

def is_positive_integer(string):
    try:
        integer = int(string)
        if integer < 0:
            return False
    except ValueError:
        return False
    return True

def chibiimage(idol, small=True):
    prefix = 'small_' if small else ''
    if idol is not None:
        filename = '/static/idols/chibi/' + prefix + idol.replace(' ', '_').replace('\'', '-') + '.png'
        if os.path.isfile('web/' + filename):
            return filename
    return '/static/idols/chibi/' + prefix + 'Alpaca.png'
