import os
from django.urls import path
from django.contrib import admin

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0aiug(bez@idcedcq3g2)22=nzd6l61%ywny8ony9(*vv=lcpk'

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
    'oauth2_provider',
    'rest_framework',
    'corsheaders',
    # 'oauth', # Used for custom OAuth2 models
    'accounts',
    #'django.contrib.admindocs',
    'bootstrap4',
]

# Users to authenticate are players
AUTH_USER_MODEL = 'accounts.Player'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

OAUTH2_PROVIDER = {
    # 'OAUTH2_VALIDATOR_CLASS': 'oauth.validator.CustomValidator.CustomValidator', # custom OAuth2 validator class
    'SCOPES': {
        'read': 'Read Player\'s Reputation (No anonymity)',
        'read_2': 'Read Player\'s Reputation with anonymity level 2 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_3': 'Read Player\'s Reputation with anonymity level 3 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_4': 'Read Player\'s Reputation with anonymity level 4 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_5': 'Read Player\'s Reputation with anonymity level 5 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_6': 'Read Player\'s Reputation with anonymity level 6 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_7': 'Read Player\'s Reputation with anonymity level 7 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_8': 'Read Player\'s Reputation with anonymity level 8 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_9': 'Read Player\'s Reputation with anonymity level 9 (level 2 being most anonymous, level 10 being least anonymous)',
        'read_10': 'Read Player\'s Reputation with anonymity level 10 (level 2 being most anonymous, level 10 being least anonymous)',
        'write': 'Update Player\'s Reputation',
    },
}

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

ROOT_URLCONF = 'auth_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/auth_server/templates'],
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

WSGI_APPLICATION = 'auth_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CORS_ORIGIN_ALLOW_ALL = True
PKCE_REQUIRED = False
# OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth.AccessToken'
# OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = 'oauth.RefreshToken'
# OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth.Application'
# OAUTH2_PROVIDER_GRANT_MODEL = 'oauth.Grant'
# OAUTH2_PROVIDER_ID_TOKEN_MODEL = 'oauth.IDToken'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
