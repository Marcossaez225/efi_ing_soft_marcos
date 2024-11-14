# concesionario/settings.py

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Building paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
def load_env_file():
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('#') or '=' not in line:
                    continue
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Load the .env file
load_env_file()

# Security settings
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-secret-key-for-development-only')
DEBUG = True  
ALLOWED_HOSTS = ['*']  # Add allowed domains or IPs in production

# Core Django applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# External libraries and frameworks
EXTERNAL_APPS = [
    'rest_framework',  # Django REST framework for API
    'rest_framework.authtoken',
    'django_filters',  # Django filters for API filtering
    'drf_yasg',  # Swagger generator
]

# Custom applications
SELF_APPS = [
    "vehicles",
    "users",
    "api", 
]

# Combine all applications
INSTALLED_APPS = INSTALLED_APPS + EXTERNAL_APPS + SELF_APPS

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Added for internationalization
]

# URL configuration
ROOT_URLCONF = 'concesionario.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global template folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'concesionario.context_processors.dealership_info',
                'users.context_processors.user_status',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

# WSGI configuration
WSGI_APPLICATION = 'concesionario.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization settings
LANGUAGE_CODE = 'en'  # Default language

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Español')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to the profile login
LOGIN_REDIRECT_URL = 'profile'

# Logout redirection
LOGOUT_REDIRECT_URL = 'home'  

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
