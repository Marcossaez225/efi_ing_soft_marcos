# concesionario/settings.py

import os
from pathlib import Path

# Construcción de rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
def load_env_file():
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('#') or '=' not in line:
                    continue
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Cargar el archivo .env
load_env_file()

# Seguridad
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-secret-key-for-development-only')
DEBUG = True  # Cambiar a False en producción
ALLOWED_HOSTS = []  # Añadir dominios o direcciones IP permitidas en producción

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vehicles',
    'media',
    'users',
    'comments',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URL
ROOT_URLCONF = 'concesionario.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta de plantillas global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'concesionario.context_processors.dealership_info',
            ],
        },
    },
]

# Configuración de WSGI
WSGI_APPLICATION = 'concesionario.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to the profile login
LOGIN_REDIRECT_URL = 'profile'

# concesionario/settings.py
LOGOUT_REDIRECT_URL = 'home'  
