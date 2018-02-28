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
    'rest_framework',
    'api',
    'storages',
    'web',
    'oauth2_provider',
    'django.contrib.auth',
    'django_prometheus',
    'django_bouncy',
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

OAUTH2_PROVIDER = {
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https', 'sukutomo'],
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

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'web.views.minimumContext',
)

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
    ('de', _('German')),
    ('ru', _('Russian')),
    ('it', _('Italian')),
    ('sv', _('Swedish')),
    ('fr', _('French')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Brazilian Portuguese')),
    ('zh-cn', _('Simplified Chinese')),
    ('zh-tw', _('Traditional Chinese')),
    ('id', _('Indonesian')),
    ('tr', _('Turkish')),
    ('ro', _('Romanian')),
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

STATIC_FILES_URL = '/' if DEBUG else '//i.schoolido.lu/'
STATIC_FILES_URL = '//i.schoolido.lu/'
STATIC_FILES_SHARING_URL = 'http://i.schoolido.lu/'

IMAGES_HOSTING_PATH = '/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# If empty, importcards will not use TinyPNG
TINYPNG_API_KEY = ''

AWS_PASSWORD_EMAIL = 'password@schoolido.lu'
LOG_EMAIL = 'emails-log@schoolido.lu'

DISQUS_STAFF = 'sukutomostaff'

DISQUS_API_KEY = 'set me in local settings'

RANDOM_ORDERING_DATABASE = 'RANDOM'

HIGH_TRAFFIC = False

IMGUR_REGEXP = '^https?:\/\/(\w+\.)?imgur.com\/(?P<imgur>[\w\d]+)(\.[a-zA-Z]{3})?$'

CUSTOM_ACTIVITY_MAX_LENGTH = 8000

BACKGROUNDS = sorted(['b_liveback_001', 'b_liveback_002', 'b_liveback_003', 'b_liveback_004', 'b_liveback_005', 'b_liveback_006', 'b_liveback_007', 'b_liveback_008', 'b_liveback_009', 'b_liveback_010', 'b_liveback_011', 'b_liveback_e01', 'b_liveback_e02', 'b_liveback_r01', 'b_liveback_r02', 'b_st_000', 'b_st_001', 'b_st_002', 'b_st_003', 'b_st_004', 'b_st_005', 'b_st_006', 'b_st_007', 'b_st_008', 'b_st_009', 'b_st_010', 'b_st_011', 'b_st_012', 'b_st_013', 'b_st_014', 'b_st_015', 'b_st_016', 'b_st_017', 'b_st_018', 'b_st_019', 'b_st_020', 'b_st_021', 'b_st_022', 'b_st_023', 'b_st_024', 'b_st_025', 'b_st_026', 'b_st_027', 'b_st_028', 'b_st_029', 'b_st_030', 'b_st_031', 'b_st_032', 'b_st_033', 'b_st_034', 'b_st_035', 'b_st_036', 'b_st_037', 'b_st_038', 'b_st_039', 'b_st_040', 'b_st_041', 'b_st_042', 'b_st_043', 'b_st_044', 'b_st_045', 'b_st_046', 'b_st_047', 'b_st_048', 'b_st_049', 'b_st_050', 'b_st_051', 'b_st_052', 'b_st_053', 'b_st_054', 'b_st_055', 'b_st_056', 'b_st_057', 'b_st_058', 'b_st_059', 'b_st_060', 'b_st_061', 'b_st_062', 'b_st_063', 'b_st_064', 'b_st_065', 'b_st_066', 'b_st_067', 'b_st_068', 'b_st_069', 'b_st_070', 'b_st_071', 'b_st_072', 'b_st_073', 'b_st_074', 'b_st_075', 'b_st_076', 'b_st_077', 'b_st_078', 'b_st_079', 'b_st_080', 'b_st_081', 'b_st_082', 'b_st_083', 'b_st_084', 'b_st_085', 'b_st_086', 'b_st_087', 'b_st_088', 'b_st_089', 'b_st_090', 'b_st_091', 'b_st_092', 'b_st_093', 'b_st_094', 'b_st_095', 'b_st_096', 'b_st_097', 'b_st_098', 'b_st_099', 'b_st_100', 'b_st_109', 'b_st_110', 'b_st_118', 'b_st_119', 'b_st_120', 'b_st_121', 'b_st_122', 'b_st_123', 'b_st_124', 'b_st_125', 'b_st_126', 'b_st_127', 'b_st_128', 'b_st_129', 'b_st_130', 'b_st_131', 'b_st_132', 'b_st_133', 'b_st_134', 'b_st_135', 'b_st_136', 'b_st_137', 'b_st_138', 'b_st_139', 'b_st_140', 'b_st_141', 'b_st_142', 'b_st_143', 'b_st_144', 'b_st_146', 'b_st_147', 'b_st_148', 'b_st_149', 'b_st_150', 'b_st_151', 'b_st_152', 'b_st_153', 'b_st_154', 'b_st_155', 'b_st_156', 'b_st_157', 'b_st_158', 'b_st_159', 'b_st_160', 'b_st_161', 'b_st_162', 'b_st_163', 'b_st_164', 'b_st_165', 'b_st_166', 'b_st_167', 'b_st_168', 'b_st_169', 'b_st_170', 'b_st_171', 'b_st_172', 'b_st_173', 'b_st_174', 'b_st_175', 'b_st_176', 'b_st_177', 'b_st_178', 'b_st_179', 'b_st_180', 'b_st_181', 'b_st_182', 'b_st_183', 'b_st_184', 'b_st_185', 'b_st_186', 'b_st_187', 'b_st_188', 'b_st_189', 'b_st_190', 'b_st_191', 'b_st_192', 'b_st_195', 'b_st_196', 'b_st_197', 'b_st_198', 'bg_1', 'bg_165', 'bg_166', 'bg_167', 'bg_187_8', 'bg_22', 'bg_23', 'bg_2_1', 'bg_38', 'bg_58', 'bg_62_2', 'bg_63', 'bg_64', 'bg_65', 'bg_66', 'bg_73', 'bg_87', 'bg_87_1', 'bg_87_2', 'bg_87_3', 'bg_87_4', 'bg_87_5', 'bg_87_6', 'bg_87_7', 'bg_87_8', 'bg_87_9', 'bg_96', 'bg_96_101', 'bg_96_102', 'bg_96_103', 'bg_96_104', 'bg_96_105', 'bg_96_106', 'bg_96_107', 'bg_96_108', 'bg_96_109', 'cp_001', 'fs_001', 'fs_002', 'fs_003', 'fs_004', 'fs_005', 'ms_001', 'ms_002', 'ms_003', 'ms_004', 'ms_005', 'ms_006', 'ms_007', 'ms_008', 'ms_009', 'b_st_199', 'b_st_200', 'bg_62_1' ])
TOTAL_BACKGROUNDS = 84 # Used for old pages that use the old backgrounds with white shading

CONTEST_MAX_SESSIONS = 9

CARDS_LIMIT = 81

AWS_SES_RETURN_PATH = 'test@schoolido.lu'

LOGIN_URL = '/login/'

GLOBAL_CONTEST_ID = 33

LOVECA_PRICE = 0.568

# Generated settings:
CARDS_INFO = {'idols': []}

IMAGES_HOSTING_PATH = 'http://i.schoolido.lu/'

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
