"""
Django settings for schoolidolapi project.

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
SECRET_KEY = 'v9d($6-ui(noij(0#&x4c0p9+%2k53#=sg6z-2g$14&u8i!1rj'
TRANSFER_CODE_SECRET_KEY = 'q+sem2i+4+2mfjsy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markdown_deux',
    'corsheaders',
    'bootstrap_form_horizontal',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'oauth2_provider',
    'rest_framework',
    'api',
    'storages',
    'web',
    'django.contrib.auth',
    'django_prometheus',
    'contest'
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'api.permissions.IsStaffOrSelf',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'api.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 10,
    'MAX_PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
}

MIDDLEWARE_CLASSES = (
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
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
    'schoolidolapi.middleware.httpredirect.HttpRedirectMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
)

ROOT_URLCONF = 'schoolidolapi.urls'

WSGI_APPLICATION = 'schoolidolapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('es', _('Spanish')),
    ('it', _('Italian')),
    ('de', _('German')),
    ('ru', _('Russian')),
    ('fr', _('French')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Brazilian Portuguese')),
    ('zh-cn', _('Simplified Chinese')),
    ('zh-tw', _('Traditional Chinese')),
    ('id', _('Indonesian')),
    ('tr', _('Turkish')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'web/locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

IMAGES_HOSTING_PATH = '/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# If empty, importcards will not use TinyPNG
TINYPNG_API_KEY = ''

AWS_PASSWORD_EMAIL = 'password@schoolido.lu'
DISQUS_STAFF = 'sukutomostaff'

RANDOM_ORDERING_DATABASE = 'RANDOM'

HIGH_TRAFFIC = False

IMGUR_REGEXP = '^https?:\/\/(\w+\.)?imgur.com\/(?P<imgur>[\w\d]+)(\.[a-zA-Z]{3})?$'

IMGUR_CLIENT_ID = '2e57c00bd3e1b6f'

TOTAL_BACKGROUNDS = 12

CONTEST_MAX_SESSIONS = 9

CARDS_LIMIT = 81

AWS_SES_RETURN_PATH = 'test@schoolido.lu'

GLOBAL_CONTEST_ID = 33

LOVECA_PRICE = 0.568

# Generated settings:
CARDS_INFO = {'idols': []}

try:
    from generated_settings import *
except ImportError, e:
    pass
try:
    from local_settings import *
except ImportError, e:
    pass

# In production, use these in the local_settings file

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_STORAGE_BUCKET_NAME = 'schoolido.lu-assets'
# IMAGES_HOSTING_PATH = 'http://datjr36easq2c.cloudfront.net/'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_REGION_NAME = 'us-east-1'
# AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws_com'
# AWS_SES_RETURN_PATH = 'password@schoolido.lu'
