"""
Django settings for Cœur du Congo - Musée Virtuel de Lukafu
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env (optionnel)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================================
# SECURITY
# ============================================================================

SECRET_KEY = 'django-insecure--wj(_je(15aly21!i7=!mgx3c46$a$eooj27(v(=_lpy3vm+!='

DEBUG = False

ALLOWED_HOSTS = ['*']


# ============================================================================
# APPLICATION DEFINITION
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'village',
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

ROOT_URLCONF = 'DjangoProject.urls'

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
                'village.context_processors.get_visit_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoProject.wsgi.application'


# ============================================================================
# DATABASE - PostgreSQL Neon
# ============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_5iZHVGn3WpbX',
        'HOST': 'ep-calm-night-aymoym1u-pooler.c-5.us-east-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}


# ============================================================================
# AUTHENTICATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Rate limiting for admin login
AUTHENTICATION_BACKENDS = [
    'village.auth_backend.RateLimitedAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# ============================================================================
# HTMX
# ============================================================================

HTMX_BOOTSTRAP_CSS = False


# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Lubumbashi'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================================
# CLOUDINARY - Stockage d'images (gratuit 25Go)
# ============================================================================

CLOUDINARY_STORAGE = {
    'cloud_name': 'gq2tclzy',
    'api_key': '684697115451568',
    'api_secret': 'L3so-93fHmnpRxtcUiZIdJZOryE',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# ============================================================================
# DEFAULT AUTO FIELD
# ============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
