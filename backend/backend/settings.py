import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Adding variables if environment don't have it
if 'SECRET_KEY' not in os.environ:
    from .dev_tools import create_environment_variable

    create_environment_variable()

SECRET_KEY = os.getenv('SECRET_KEY', 'test-key-django')

DEBUG = os.getenv('DEBUG', False) == 'True'

TEST_BASE = os.getenv('TEST_BASE', False) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'djoser',
    'colorfield',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig'
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


def get_db_settings():
    if TEST_BASE:
        return {
            'default':
                {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3'
                }
        }
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'postgres'),
            'USER': os.getenv('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
            'HOST': os.getenv('DB_HOST', '172.17.0.2'),
            'PORT': os.getenv('DB_PORT', 5432),
        }
    }


DATABASES = get_db_settings()

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    "HIDE_USERS": False,
    'LOGIN_FIELD': 'email',
    'SET_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user': 'api.users.serializers.CustomUserSerializer',
        'current_user': 'api.users.serializers.CustomUserSerializer',
        'user_create': 'api.users.serializers.CustomUserCreateSerializer',
        'set_password_retype': 'djoser.serializers.SetPasswordSerializer',
    },
    'PERMISSIONS': {
        "user": ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        "user_list": ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    }
}

TAGS_FOR_RECIPES = [
    {'name': 'Ужин', 'slug': 'dinner', 'color': '#0000ff'},
    {'name': 'Обед', 'slug': 'lunch', 'color': '#cd7f32'},
    {'name': 'Завтрак', 'slug': 'breakfast', 'color': '#61db5c'},
]

CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000'
).split(',')
