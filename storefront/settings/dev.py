from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9k^4k_%t=m6zl8+(8w@j9ic3vch#)&5i7&%j@ah_0vnyw0+2r9'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'storefront',
        'USER': 'postgres',
        'PASSWORD': 'postgresql',
        'HOST': 'localhost',
        'PORT': '',
    }
}

if DEBUG:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]