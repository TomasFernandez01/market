# === settings.py - Configuración Django Optimizada ===
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url # -> RENDER

# CLOUDINARY DEBE ESTAR ARRIBA DE TODO 
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage.storage import MediaCloudinaryStorage

# Cargar variables de entorno
load_dotenv()

# =============================================================================
# CONFIGURACIÓN CLOUDINARY
# =============================================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'PREFIX': 'masivo_tech/'  # ← Organización en carpetas
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-para-desarrollo')

# Solucionado 
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'masivotech.onrender.com,localhost,127.0.0.1').split(',')

# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================

INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Cloudinary
    'cloudinary',
    'cloudinary_storage',

    # Apps de terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'django_extensions',
    
    # Apps locales
    'marketplace',
    'users',
    'chat',
]

MIDDLEWARE = [
    # Middleware de CORS (primero)
    'corsheaders.middleware.CorsMiddleware',
    
    # Middleware de seguridad
    'django.middleware.security.SecurityMiddleware',
    
    # Whitenoise para archivos estáticos en producción -> RENDER
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Middleware de sesión
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Middleware común
    'django.middleware.common.CommonMiddleware',
    
    # Middleware CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Middleware de autenticación
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Middleware de mensajes
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Middleware de clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'masivo_tech.urls'

WSGI_APPLICATION = 'masivo_tech.wsgi.application'

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

# =============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# =============================================================================

# Solo el backend básico de Django
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'users.CustomUser'

# Configuración básica de login
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# =============================================================================
# CONFIGURACIÓN DE EMAIL (DESACTIVADO PARA RENDER)
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@masivotech.com"

# =============================================================================
# CONFIGURACIÓN DE INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA
# =============================================================================

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
# --> RENDER <--
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# CONFIGURACIÓN DE TEMPLATES
# =============================================================================

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
                'marketplace.context_processors.cart_context',
            ],
        },
    },
]

# =============================================================================
# CONFIGURACIÓN DE CRISPY FORMS
# =============================================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =============================================================================
# CONFIGURACIÓN DE CARRITO
# =============================================================================

CART_SESSION_ID = 'cart'

# =============================================================================
# CONFIGURACIÓN DE APIs EXTERNAS
# =============================================================================

# Google Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY')

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD ADICIONAL
# =============================================================================

# Validadores de contraseña
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

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# URL base para callbacks
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000") # <-- render

# Configuración del admin dashboard
ADMIN_DASHBOARD = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'