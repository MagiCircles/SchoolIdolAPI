"""
Django settings for sukutomo_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#yt2*mvya*ulaxd+6jtr#%ouyco*2%3ngb=u-_$44j^86g0$$3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'bootstrapform',
    'bootstrap_form_horizontal',
    'rest_framework',
    'storages',
    'magi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'magi.middleware.languageFromPreferences.LanguageFromPreferenceMiddleWare',
    'magi.middleware.httpredirect.HttpRedirectMiddleware',
)

ROOT_URLCONF = 'sukutomo_project.urls'

WSGI_APPLICATION = 'sukutomo_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

SITE = 'sukutomo'

AUTHENTICATION_BACKENDS = ('magi.backends.AuthenticationBackend',)

DEBUG_PORT = 8000

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('de', _('German')),
    ('it', _('Italian')),
    ('ru', _('Russian')),
)

LANGUAGE_CODE = 'en'

LOCALE_PATHS = [
  os.path.join(BASE_DIR, 'magi/locale'),
]

STATIC_UPLOADED_FILES_PREFIX = None

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

LOGIN_REDIRECT_URL = '/'
LOG_EMAIL = 'emails-log@schoolido.lu'
PASSWORD_EMAIL = 'password@schoolido.lu'
AWS_SES_RETURN_PATH = 'contact@schoolido.lu'

FAVORITE_CHARACTERS = []

MAX_WIDTH = 1200
MAX_HEIGHT = 1200
MIN_WIDTH = 300
MIN_HEIGHT = 300

try:
    from generated_settings import *
except ImportError, e:
    pass
try:
    from local_settings import *
except ImportError, e:
    pass

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append(SITE)

LOCALE_PATHS = list(LOCALE_PATHS)
LOCALE_PATHS.append(os.path.join(BASE_DIR, SITE, 'locale'))

if STATIC_UPLOADED_FILES_PREFIX is None:
    STATIC_UPLOADED_FILES_PREFIX = SITE + '/static/uploaded/' if DEBUG else 'u/'
