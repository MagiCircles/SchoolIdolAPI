import urllib2, urllib
import json
import os
import string
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def send_email(subject, template_name, to=[], context={}, from_email=settings.AWS_SES_RETURN_PATH):
    context = Context(context)
    plaintext = get_template('emails/' + template_name + '.txt').render(context)
    htmly = get_template('emails/' + template_name + '.html').render(context)
    email = EmailMultiAlternatives(subject, plaintext, from_email, to)
    email.attach_alternative(htmly, "text/html")
    email.send()

class HttpRedirectException(Exception):
    pass

def is_positive_integer(string):
    try:
        integer = int(string)
        if integer < 0:
            return False
    except ValueError:
        return False
    return True

def concat_args(*args):
    return u'\"' + u'","'.join([unicode(value).replace('"','\"') for value in args]) + u'\"'

def chibiimage(idol, small=True):
    prefix = 'small_' if small else ''
    if idol is not None:
        filename = '/static/idols/chibi/' + prefix + idol.replace(' ', '_').replace('\'', '-') + '.png'
        if os.path.isfile('web/' + filename):
            return filename
    return '/static/idols/chibi/' + prefix + 'Alpaca.png'

def randomString(length, choice=(string.ascii_letters + string.digits)):
    return ''.join(random.SystemRandom().choice(choice) for _ in range(length))
