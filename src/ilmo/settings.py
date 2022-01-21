"""
Django settings for ILMO project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
import configparser
from django.utils.translation import gettext_lazy as _

"""CONFIG PARSER """
config = configparser.RawConfigParser()
if 'ILMO_CONFIG_FILE' in os.environ:
    config.read_file(open(os.environ.get('ILMO_CONFIG_FILE'), encoding='utf-8'))
else:
    config.read(['/etc/ilmo/ilmo.cfg', os.path.expanduser('~/.ilmo.cfg'), 'ilmo.cfg'],
                encoding='utf-8')
CONFIG_FILE = config

""" DJANGO """
SECRET_KEY = config.get('django', 'secret')
DEBUG = config.get('django', 'debug')

""" DATABASE """
DB_BACKEND = config.get("database", "backend", fallback="sqlite3")
DB_NAME = config.get("database", "name", fallback="ilmo.sqlite3")
DB_USER = config.get("database", "user", fallback='')
DB_PASSWORD = config.get("database", "password", fallback='')
DB_HOST = config.get("database", "host", fallback="localhost")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

""" SECURITY.TXT """
SEC_CONTACT = config.get("security", "Contact", fallback="julian-samuel@gebuehr.net")
SEC_EXPIRES = config.get("security", "Expires", fallback="2022-11-28T07:00:00.000Z")
SEC_ENCRYPTION = config.get("security", "Encryption", fallback="https://hyteck.de/julian-samuel@gebuehr.net.pub.asc")
SEC_LANG = config.get("security", "Preferred-Languages", fallback="en, de")
SEC_SCOPE = config.get("security", "Scope",
                       fallback="The provided contact is the main developer of the application and NOT necessarily the "
                                "instance")
SEC_POLICY = config.get("security", "Policy",
                        fallback="Do NOT include user data or detailed reports (especially public or unencrypted) "
                                 "without being asked to do so.")

""" LOCATIONS """
STATIC_ROOT = config.get("locations", "static", fallback=".django-static/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'library.apps.LibraryConfig',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fontawesomefree',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'ilmo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ilmo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
import os

# Use the following live settings to build on Travis CI
if os.getenv('BUILD_ON_TRAVIS', None):
    SECRET_KEY = "SecretKeyForUseOnTravis"
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }
elif (DB_BACKEND == "sqlite3"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_NAME,
        }
    }
elif (DB_BACKEND == "postgresql"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
        }
    }
else:
    print("Database backend unknown. Choose sqlite3 or postgresql")

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en-us', _('English')),
    ('de', _('German')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
