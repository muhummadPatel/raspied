"""
Django settings for raspied project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'students.apps.StudentsConfig',
    'pipeline',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'raspied.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,  'templates'),
        ],
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

WSGI_APPLICATION = 'raspied.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'raspied.storage.GzipManifestPipelineStorage'
PIPELINE = {
    # NOTE: have to use a no-op js compressor otherwise it throws errors from
    # jquery. May be able to actually compress the js with a different
    # compressor or a different version of jquery.
    'JS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'CSS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'STYLESHEETS': {
        'libs_css': {
            'source_filenames': (
              'raspied/bower_components/Materialize/dist/css/materialize.css',
            ),
            'output_filename': 'css/libs_css.min.css',
        },
        'custom_css': {
            'source_filenames': (
              'raspied/css/custom.css',
            ),
            'output_filename': 'css/custom_css.min.css',
        },
        'pickadate_css': {
            'source_filenames': (
                'raspied/bower_components/pickadate/lib/compressed/themes/default.css',
                'raspied/bower_components/pickadate/lib/compressed/themes/default.date.css',
                'raspied/bower_components/pickadate/lib/compressed/themes/default.time.css',
            ),
            'output_filename': 'css/pickadate_css.min.css',
        },
    },
    'JAVASCRIPT': {
        'libs_js': {
            'source_filenames': (
                'raspied/bower_components/jquery/dist/jquery.js',
                'raspied/bower_components/Materialize/dist/js/materialize.js',
                'raspied/bower_components/js-cookie/src/js.cookie.js',
            ),
            'output_filename': 'js/libs_js.min.js',
        },
        'init_js': {
            'source_filenames': (
                'raspied/js/init.js',
            ),
            'output_filename': 'js/init_js.min.js',
        },
        'jsmpg_js': {
            'source_filenames': (
                'students/js/jsmpg.js',
            ),
            'output_filename': 'js/jsmpg_js.min.js',
        },
        'ace_js': {
            'source_filenames': (
                'raspied/bower_components/ace-builds/src-noconflict/ace.js',
                'raspied/bower_components/ace-builds/src-noconflict/mode-python.js',
                'raspied/bower_components/ace-builds/src-noconflict/theme-monokai.js',
            ),
            'output_filename': 'js/ace_js.min.js',
        },
        'filesaver_js': {
            'source_filenames': (
                'raspied/bower_components/Blob/Blob.js',
                'raspied/bower_components/file-saver/FileSaver.min.js',
            ),
            'output_filename': 'js/filesaver_js.min.js',
        },
        'pickadate_js': {
            'source_filenames': (
                'raspied/bower_components/pickadate/lib/compressed/picker.js',
                'raspied/bower_components/pickadate/lib/compressed/picker.date.js',
                'raspied/bower_components/pickadate/lib/compressed/picker.time.js',
                'raspied/bower_components/pickadate/lib/compressed/legacy.js',
            ),
            'output_filename': 'js/pickadate_js.min.js',
        },
        'moment_js': {
            'source_filenames': (
                'raspied/bower_components/moment/min/moment.min.js',
            ),
            'output_filename': 'js/moment_js.min.js',
        },
    },
}

LOGIN_URL = '/students/accounts/login/'
LOGIN_REDIRECT_URL = '/students/home/'

STREAMING_SERVER_IP = '105.226.75.112'

# Duration of a bookable session in seconds
BOOKING_INTERVAL = 3600
USER_BOOKINGS_PER_MONTH = 5

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'raspied.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
