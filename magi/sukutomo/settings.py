from django.conf import settings as django_settings
from sukutomo import models

SITE_NAME = 'Sample Website'
SITE_URL = 'http://sukutomo.com/'
SITE_IMAGE = 'sukutomo.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.sukutomo.com/'
GAME_NAME = 'Sample Game'
DISQUS_SHORTNAME = 'sukutomo'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'
