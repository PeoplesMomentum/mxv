"""
Django settings for mxv project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
from django.contrib import messages
from datetime import date
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MXV_SECRET_KEY', '&0+9q8c$q46+bslj=g#!i9@u#j@3#p=#k12je47wj%fj24q%=*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('MXV_DEBUG', 'True') == 'True' else False

# Application definition

INSTALLED_APPS = [
    # apps
    'mxv.apps.MxvConfig',
    'members.apps.MembersConfig',
    'review.apps.ReviewConfig',
    'voting_intentions.apps.VotingIntentionsConfig',    
    'consultations.apps.ConsultationsConfig',
    'tasks.apps.TasksConfig',
    # admin, Django and third party
    'nested_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'solo.apps.SoloAppConfig',
    'tinymce',
    'anymail',
    'widget_tweaks',
    'django_rq',
    'polymorphic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mxv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/mxv/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mxv.context_processors.default',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'mxv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('MXV_DATABASE_HOST', ''),
        'PORT': os.environ.get('MXV_DATABASE_PORT', ''),
        'NAME': os.environ.get('MXV_DATABASE_NAME', 'mxv'),
        'USER': os.environ.get('MXV_DATABASE_USER', 'mxv'),
        'PASSWORD': os.environ.get('MXV_DATABASE_PASSWORD', 'mxv')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# extend the base user model
AUTH_USER_MODEL = 'members.Member'

# get the secret used by the join page to create inactive members
CREATE_INACTIVE_MEMBER_SECRET = os.environ.get('MXV_CREATE_INACTIVE_MEMBER_SECRET', 'mxv')

# set up HTML editor
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'width' : 600,
    'height' : 300,
    'convert_urls' : False,
    'relative_urls' : False,
}

# Mailgun
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('MXV_MAILGUN_API_KEY', "mxv"),
    'MAILGUN_SENDER_DOMAIN': os.environ.get('MXV_MAILGUN_SENDER_DOMAIN', "mxv")
}
DEFAULT_FROM_EMAIL = "Team Momentum <mymomentum@peoplesmomentum.com>"

# join page
JOIN_URL = "https://join.peoplesmomentum.com"

# site name
SITE_NAME_SHORT = "My Momentum"
SITE_NAME_LONG = "My Momentum"

# send members to the index page after they login
LOGIN_URL = '/members/login'
LOGIN_REDIRECT_URL = '/'

# date/time formats
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i:s'

# close the session when the browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# whether to allow requests to the error URL (for testing error handling)
ALLOW_ERROR_URL = True if os.environ.get('MXV_ALLOW_ERROR_URL', 'False') == 'True' else False

# change error into danger for bootstrap
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# whether to show track voting-specific changes to just staff or anyone
TRACK3_VOTING_VISIBLE_TO_NON_STAFF = True if os.environ.get('MXV_TRACK3_VOTING_VISIBLE_TO_NON_STAFF', 'False') == 'True' else False

# when the site was launched to the members
LAUNCH_DATE = date(2018, 2, 2)

# token for accessing NationBuilder
NATIONBUILDER_API_TOKEN = os.environ.get('MXV_NATIONBUILDER_API_TOKEN', '')

# default redirect page URL
DEFAULT_REDIRECT_PAGE_URL = 'https://peoplesmomentum.com'

# whether to show consultations to just staff or anyone
CONSULTATIONS_VISIBLE_TO_NON_STAFF = True if os.environ.get('MXV_CONSULTATIONS_VISIBLE_TO_NON_STAFF', 'False') == 'True' else False

# task queueing
RQ_SHOW_ADMIN_LINK = True
RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
    }
}

# configure sentry
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()]
)
