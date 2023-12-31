"""
Django settings for storefront project.

Generated by 'django-admin startproject' using Django 3.2.22.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #third party
    'django_filters',
    "debug_toolbar",
    'rest_framework',
    'djoser',
    'corsheaders',
    'silk',
    #local apps
    'playground',
    'store',
    'tags',
    'likes',
    'core'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8001","http://localhost:8001"]

ROOT_URLCONF = 'storefront.urls'

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

WSGI_APPLICATION = 'storefront.wsgi.application'

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,"static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK ={
    'COERCE_DECIMAL_TO_STRING':False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
   "ACCESS_TOKEN_LIFETIME": timedelta(days=2)
}

AUTH_USER_MODEL ='core.User'

DJOSER ={
    'SERIALIZERS':{
        'user_create':'core.serializers.UserCreateSerializer',
        'current_user':'core.serializers.CurrentUserSerializer'
    }
}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT= 2525
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD =""
DEFAULT_FROM_EMAIL ="from@me.c"

ADMINS = [
			("Abdallah",'abdallah@test.com')
		]

CELERY_BROKER_URL ="redis://localhost:6379/1"

CELERY_BEAT_SHEDULE = {
   'notify_customers':{
       'task':'playground.tasks.notify_customers',
       'schedule':5,
       'args': ['hey']
   } 
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LOGGING = {
    'version':1,
    'disable_existing_loggers': False,
    'handlers':{
        'console':{
            'class':'logging.StreamHandler'
        },
        'file':{
            'class': 'logging.FileHandler',
            'filename':"general.log",
            'formatter':'verbose' # different formaters for differnt handlers
        }
    },
    'loggers':{ # we can specify custom logger for different apps
        '':{
            'handlers':['console','file'],
            'level': os.environ.get("DJANGO_LOG_LEVEL","INFO")
        }
    },
    'formatters':{
        'verbose':{
            'format':'{asctime} ({levelname}) - {name} - {message}',
            'style': '{' #'{' string.format(), '$' string.Template
        }
    }
}