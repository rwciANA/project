"""
Django settings for veterinaria project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SEGURIDAD Y VARIABLES DE ENTORNO
# ==========================================

# Lee la clave secreta desde las variables de Vercel (o usa la de respaldo para local)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-55%am8vri(kh9+pmbl!7@zsmk=pf(pnn40si*0=xj$nf+3u2pa'
)

# Activa DEBUG en local si la variable no está definida en Vercel
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '*',  # Puedes cambiarlo a '.vercel.app' en producción por mayor seguridad
]


# ==========================================
# APLICACIONES E INSTALACIONES
# ==========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de terceros
    'corsheaders',
    
    # Tus apps
    'adopciones',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 👈 Posición correcta para CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'veterinaria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 👈 Corregido de 'veterinaria.wsgi.app' a 'veterinaria.wsgi.application'
WSGI_APPLICATION = 'veterinaria.wsgi.application'


# ==========================================
# BASE DE DATOS
# ==========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# VALIDACIÓN DE CONTRASEÑAS Y IDIOMA
# ==========================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es' # O 'en-us' según prefieras
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True


# ==========================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ==========================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# CORS Y AUTENTICACIÓN
# ==========================================

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

CORS_ALLOWED_ORIGINS = [
    "https://frontend.vercel.app",  # Cambia esto por la URL real de tu Vercel
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Si usas una variable de entorno para el frontend, puedes agregarla dinámicamente:
if FRONTEND_URL and FRONTEND_URL not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

CORS_ALLOW_CREDENTIALS = True

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/adopciones/'