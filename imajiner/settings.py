import os
import dj_database_url
from uuid import uuid1
from django.utils.translation import gettext, gettext_lazy
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', str(uuid1()))

SITE_ID = 1

DEBUG = True
ON_HEROKU = bool(os.getenv('ON_HEROKU', False))
GITHUB_WORKFLOW = bool(os.getenv('GITHUB_WORKFLOW', False))

if ON_HEROKU:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    DEBUG = False


ALLOWED_HOSTS = [
    'localhost',
    '192.168.1.10',
    '192.168.43.182',
    'imajiner.space',
    'imajiner.herokuapp.com',
    'imajiner-b4f81b48dfc7.herokuapp.com'
]
PRIMARY_HOST = 'imajiner.space'


EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'server@imajiner.space'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = f'Imajiner Sunucu <{EMAIL_HOST_USER}>'
FROM_EMAILS = [
    'server@imajiner.space',
    'webserver@imajiner.space',
    'django@imajiner.space',
]

ADMINS = [
    ('Ömer Selçuk', 'omerselcuk@imajiner.space'),
]
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'FATAL',
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.postgres.fields',
    'notebook.apps.NotebookConfig',
    'tagmanager.apps.TagManagerConfig',
    'gatewall.apps.GatewallConfig',
    'identity.apps.IdentityConfig',
    'explore.apps.ExploreConfig',
    'console.apps.ConsoleConfig',
    'django_extensions',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'identity.middleware.ShadowMiddleware',
]

ROOT_URLCONF = 'imajiner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imajiner.wsgi.application'

DATABASE_URL = os.getenv('DATABASE_URL', None)

if GITHUB_WORKFLOW:
    DB = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'github_actions',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
elif DATABASE_URL:
    DB = dj_database_url.parse(DATABASE_URL)

else:
    raise Exception('DB not configured and no DATABASE_URL supplied.')

DATABASES = {
    'default': DB
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('tr', 'Türkçe'),
)

LANGUAGES_DICT = dict(LANGUAGES)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGIN_URL = "gatewall:auth"

sentry_sdk.init(
    dsn="https://6411c6f4c53c406abd0647667289228a@o908447.ingest.sentry.io/5844277",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
