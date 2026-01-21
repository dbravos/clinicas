"""
Django settings for ctrlinfo project.
"""

import os
from pathlib import Path
import dj_database_url  # Mover aquí para que esté disponible en todo el archivo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-desarrollo')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS corregido
#if DEBUG:
ALLOWED_HOSTS = ['*']  # Desarrollo
#else:
# ALLOWED_HOSTS = [
#        'localhost',
#        '127.0.0.1',
#        '.up.railway.app',
#        '.railway.app'
#        '.onrender.com'
#    ]



SESSION_COOKIE_AGE = 300

# La sesión se cierra al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Evita que JavaScript acceda a la cookie de sesión (Protege contra ataques XSS)
SESSION_COOKIE_HTTPONLY = True

# DATABASE CONFIGURATION - CORREGIDO
if os.environ.get('DATABASE_URL'):
    # PRODUCCIÓN (Railway) - PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    # DESARROLLO (Local) - PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'clinica'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'admin'),
            'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# STATIC FILES CONFIGURATION
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'mapp/static')]

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djmoney',
    'mapp',
    'django.contrib.humanize',

]

# MIDDLEWARE - AÑADE WHITENOISE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ¡AÑADIDO!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mapp.middleware.ClinicaMiddleware',  # ← AGREGA esta línea

]




ROOT_URLCONF = 'ctrlinfo.urls'

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
                'mapp.context_processors.clinica_actual',

            ],
        },
    },
]

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
WSGI_APPLICATION = 'ctrlinfo.wsgi.application'

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True  # ¡CORREGIDO: SEPARATOR no SEPERATOR!
USE_TZ = True

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Money settings
DEFAULT_CURRENCY = 'MXN'
CURRENCIES = ('MXN', 'USD')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'mapp': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Crear superusuario automáticamente en producción
#if not DEBUG:
#    try:
#        from scripts.createsuperuser import *
#        print("✅ Script de superusuario cargado")
#    except Exception as e:
#        print(f"⚠️  Error cargando script de superusuario: {e}")

 # Cargar datos automáticamente en producción (solo una vez)
#if not DEBUG:
#    try:
#        # Verificar si ya se cargaron los datos
#        from django.contrib.auth.models import User
#        if User.objects.count() < 2:  # Si no hay usuarios, cargar datos
#           from scripts.loaddata import cargar_datos
#           cargar_datos()
#        else:
#            print("✅ Los datos ya fueron cargados previamente")
#    except Exception as e:
#        print(f"⚠️  Error en carga de datos: {e}")