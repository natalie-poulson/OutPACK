"""
Django settings for final_django project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MEDIA_DIR = os.path.join('final_app/profile_pictures')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('secret_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'django_extensions',
    'crispy_forms',
    "bootstrap4",
    'bootstrap_datepicker_plus',
    'leaflet',
    'djgeojson',
    # my apps
    'accounts',
    'final_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'final_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'final_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'final',
    }
}

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (41.850033, -87.6500523),
    'DEFAULT_ZOOM': 3,
    'MIN_ZOOM': 1,
    'MAX_ZOOM': 18,
    'TILES': [('Outdoors', 'https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=f5d4ab6c487e4dc1acaeee2b4b978238',{})]
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/






#The address to visit to find the media files
MEDIA_URL = '/media/'

# MEDIA_ROOT = MEDIA_DIR
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CRISPY_TEMPLATE_PACK = 'bootstrap4'


# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    
# The address to visit to find the static files 
STATIC_URL = '/static/'

# Tells Django where to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'assets'),
)


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static')),

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


django_heroku.settings(locals())

