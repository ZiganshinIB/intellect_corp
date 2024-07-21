
import os
from pathlib import Path
from environs import Env
env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY', 'django-insecure-!%&5n&5#qj8m!m!p!tq^%5y5#d#k%k!i!z8!qz#z%8w!#z%8w')
DEBUG = env.bool('DEBUG', True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'account.apps.AccountConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'worker.apps.WorkerConfig',
    'tasker.apps.TaskerConfig',
    #'debug_toolbar',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'icorp.urls'

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

WSGI_APPLICATION = 'icorp.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = "Europe/Moscow"

PHONENUMBER_DEFAULT_REGION = 'RU'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'account:login'
LOGOUT_URL = 'logout'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', 'test@example.com')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', 'password')
EMAIL_PORT = env.int('EMAIL_PORT', 587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/')

# AD
AD_HOST = env.str("AD_HOST")
AD_ADMIN_NAME = env.str("AD_ADMIN_NAME")
AD_ADMIN_PASSWORD = env.str("AD_ADMIN_PASSWORD")
