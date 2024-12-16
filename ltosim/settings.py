"""
Django settings for ltosim project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import mimetypes
from os.path import join, dirname
from dotenv import load_dotenv
from ltosim.context_processors import MAX_LESSON1_LEVELS, MAX_LESSON2_LEVELS, MAX_LESSON3_LEVELS

mimetypes.add_type("text/css", ".css", True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MAX_LESSON1_LEVELS_ENV = os.getenv(MAX_LESSON1_LEVELS, "6")
MAX_LESSON2_LEVELS_ENV = os.getenv(MAX_LESSON2_LEVELS, "7")
MAX_LESSON3_LEVELS_ENV = os.getenv(MAX_LESSON3_LEVELS, "2")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(rby5ubl=%2=_8qhhro3nms+(9bsen1-v#kx#(s=hi!c)1oh(t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'ltosimulator.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['ltosimulator.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    # 'system.apps.MyOwnConfig',
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_bootstrap5',
    'bootstrap4',
    'system',
    'rest_framework',
    'django_tables2',
    'django_filters',
    'modeltranslation'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ltosim.urls'

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
                'ltosim.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ltosim.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if os.environ.get("DJANGO_ENV") == "LOCAL":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "ltosimulator$default",
            "USER": "root",
            "PASSWORD": "",
            "HOST": "127.0.0.1",
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "ltosimulator$default",
            "USER": "ltosimulator",
            "PASSWORD": "notCommonPassword1234",
            "HOST": "ltosimulator.mysql.pythonanywhere-services.com",
            "PORT": "3306",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'  # this is the name of the url

LOGOUT_REDIRECT_URL = '/'

# login details danielc / ofhNrp21f5bkj3xj

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('fil', 'Filipino'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

USE_I18N = True

TIME_ZONE = 'Asia/Manila'

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "system.CustomUser"

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

X_FRAME_OPTIONS = 'SAMEORIGIN'

PLAYFAB_SECRET_KEY = 'NEWWSYXID3P4CU5HZKCZHAN96KWAW8I83PJOOYK358F3Q97XHM'

CSRF_TRUSTED_ORIGINS = [
    "https://ltosimulator.pythonanywhere.com",  # Add the scheme here
]