"""
Django settings for tables_matchmaker project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h!0f=d4sbhifl+xl@dt$)v7my+7lzq_j$i0a(vg#s+$xfo4g#i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_api',
    'corsheaders',
    'channels',
    'matchmaker',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tables_matchmaker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'tables_matchmaker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# # HEROKU CONSULER CREDENTIALS
CLIENT_ID = '7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R'
CLIENT_SECRET = 'MSbi0l3apzI5DHtFNEBdntkmzccAb7vO2ZANej2irDEiaTUfEvAb1VBUrfYUaghf5TKNypl5zU69a2EcyVUGil10Utq8qtkjFJyH47KsjnJDSEFQo971ZgWPEbRzjBd1'

# CLIENT_ID = 'DwL0GjZmLAn4PL74KcFBLDnHeRdsF15nIb5HR95d'
# CLIENT_SECRET = 'DbHThFGcJhy0rKUT8mTKamfCBqBpdTtBoxK8rZkCoTBx2fAT0QHDHh8SFZIU5OvwB4pxaztq1RqWIY64Z1e39RYtasFa0Ytm1VZficG3GJe3rikOftjEiVVm5yH08alX'

CORS_ORIGIN_ALLOW_ALL = True
URL_AUTHORIZE = f'http://localhost:8000/o/authorize?response_type=code&client_id={CLIENT_ID}&state=random_state_string'
# URL_CALLBACK = f'http://localhost:8003/in_game'
URL_AUTH_GRANT = f'http://localhost:8000/'
URL_TOKEN = f'http://localhost:8000/o/token/'
URL_REPUTATION = f'http://localhost:8000/api/reputation'
URL_USER_AGENT = f'http://localhost:8003'
URL_TM = f'http://localhost:8002'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = "TMSESSIONS"

GAMES = {'chess': 2, 'monopoly': 3, 'poker': 4, 'uno': 5}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASGI_APPLICATION = 'tables_matchmaker.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
