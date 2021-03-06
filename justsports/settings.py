"""
Django settings for justsports project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm&l@8!vfcg_k5p=4ih=e)_ac-ub)pv9^wmypv80q(5=tnr(@dg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',
    'mysports',
    'users',
    'payment',
    'view_breadcrumbs',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'justsports.urls'

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

WSGI_APPLICATION = 'justsports.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
#https://www.tutorialspoint.com/python/python_sending_email.htm

# PAYTM_MERCHANT_ID = '<your_merchant_id>'
# PAYTM_SECRET_KEY = '<your_paytm_secret_key>'
# PAYTM_WEBSITE = 'WEBSTAGING'
# PAYTM_CHANNEL_ID = 'WEB'
# PAYTM_INDUSTRY_TYPE_ID = 'Retail'
# https://micropyramid.medium.com/django-payu-payment-gateway-integration-81b8d03b38ae#:~:text=To%20integrate%20with%20PayU%2C%20we,%E2%80%9D%20%E2%80%94%20a%20pluggable%20Django%20application.&text=Integration%20Process%3A,experience%20of%20overall%20transaction%20flow.

# PAYU INTEGRATION CREDENTIALS
PAYU_MERCHANT_KEY = 'oBkA8OgU'
# PAYU_MERCHANT_KEY = '6eLmQBOE'
PAYU_MERCHANT_SALT = "TrpZ52Rdwb"
# PAYU_MERCHANT_KEY = 'MPrfqIlx'

# PAYU_MERCHANT_SALT = 'pcCG30E51O'
# PAYU_MERCHANT_SALT= 'ucUCfDiJJy'
# Change the PAYU_MODE to 'LIVE' for production.
PAYU_MODE = "TEST"
PAYU_BASE_URL = "https://test.payu.in/_payment"
#PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
# https://djangostars.com/blog/configuring-django-settings-best-practices/
# https://www.codegrepper.com/code-examples/html/option+in+bootstrap+sample
