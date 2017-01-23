import urllib2, urllib
import json
import os
import string
import random
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.files.temp import NamedTemporaryFile
from tinypng import shrink_file
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.http import urlquote
from tinypng.api import shrink_data
from django.conf import settings
from api.raw import all_chibis

from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

def dataToImageFile(data):
    image = NamedTemporaryFile(delete=False)
    image.write(data)
    image.flush()
    return ImageFile(image)

def shrinkImageFromData(data, filename='lol.png'):
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    api_key = settings.TINYPNG_API_KEY
    if not api_key or extension not in ['.png', '.jpg', '.jpeg']:
        return dataToImageFile(data)
    info, new_data = shrink_data(data, api_key)
    return dataToImageFile(new_data)

def shrunkImage(picture, filename):
    api_key = settings.TINYPNG_API_KEY
    if not api_key or not filename.endswith('.png'):
        return picture
    img_shrunked = NamedTemporaryFile(delete=False)
    shrink_info = shrink_file(
            picture.name,
            api_key=api_key,
            out_filepath=img_shrunked.name
    )
    img_shrunked.flush()
    return ImageFile(img_shrunked)

def send_email(subject, template_name, to=[], context={}, from_email=settings.AWS_SES_RETURN_PATH):
    if 'template_name' != 'notification':
        to.append(settings.LOG_EMAIL)
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

def chibiimage(idol, small=True, force_first=False, force_artist=None):
    prefix = 'small_' if small else ''
    image = None
    if idol is not None and idol in all_chibis:
        images = all_chibis[idol]
        if force_artist:
            images = [i for i in images if i[1] == force_artist]
            if not images:
                images = all_chibis[idol]
        try:
            if force_first:
                image = images[0][0]
            else:
                image = random.choice(images)[0]
        except IndexError:
            image = None
    if image:
        return (image if not small else image.replace('chibi/', 'chibi/small_'))
    return 'http://i.schoolido.lu/static/idols/chibi/' + prefix + idol.replace(' ', '_').replace('\'', '-') + '.png'

def randomString(length, choice=(string.ascii_letters + string.digits)):
    return ''.join(random.SystemRandom().choice(choice) for _ in range(length))

def get_imgur_code(url):
    return re.compile(settings.IMGUR_REGEXP).match(url).group('imgur')

def get_parameters_to_string(request):
    return '?' + '&'.join([p[0] + '=' + p[1] for p in request.GET.items()])

def tourldash(string):
    return ''.join(e if e.isalnum() else '-' for e in string)

def singlecardurl(card):
    return urlquote(u'/cards/{}/{}-{}{}{}{}-{}/'.format(
        card.id,
        card.rarity,
        tourldash(card.name),
        '-' + tourldash(card.translated_collection) if card.translated_collection else '',
        '-promo' if card.is_promo else '',
        '-event' if card.event_id else '',
        card.attribute))

def activity_cacheaccount(account, account_owner=None):
    if not account_owner:
        account_owner = account.owner
    return {
        'account_link': '/user/' + account_owner.username + '/#' + str(account.id),
        'account_picture': account_owner.preferences.avatar(size=100),
        'account_name': unicode(account),
    }
