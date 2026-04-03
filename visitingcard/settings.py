"""
settings.py — Main configuration file for the entire Django project.
Think of this as the "control panel" for your project.
"""

from pathlib import Path
from decouple import config  # reads values from your .env file

# ─── BASE DIRECTORY ────────────────────────────────────────────────────────────
# This is the root folder of your project on your computer.
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── SECURITY ──────────────────────────────────────────────────────────────────
# Secret key is used to keep sessions & cookies secure. Keep it private!
SECRET_KEY = config('SECRET_KEY', default='change-me-in-production')

# DEBUG=True shows detailed errors. Set to False in production.
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']  # In production, put your domain here


# ─── INSTALLED APPS ────────────────────────────────────────────────────────────
# List of all apps Django should load. We have two custom apps:
#   'accounts' → handles Register / Login
#   'cards'    → handles Visiting Card upload, OCR, list, export, send
INSTALLED_APPS = [
    'django.contrib.admin',       # Built-in admin panel at /admin/
    'django.contrib.auth',        # Built-in login/logout/register system
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our custom apps
    'accounts',
    'cards',
]


# ─── MIDDLEWARE ────────────────────────────────────────────────────────────────
# Middleware = code that runs on every request/response (security, sessions, etc.)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Protects forms from attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─── URL CONFIGURATION ─────────────────────────────────────────────────────────
# This file tells Django "which file has the main URL list"
ROOT_URLCONF = 'visitingcard.urls'


# ─── TEMPLATES ─────────────────────────────────────────────────────────────────
# Where Django looks for your HTML files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Our global templates folder
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

WSGI_APPLICATION = 'visitingcard.wsgi.application'


# ─── DATABASE ──────────────────────────────────────────────────────────────────
# SQLite is a simple file-based database — perfect for development.
# Later you can switch to PostgreSQL for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─── PASSWORD VALIDATION ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── LANGUAGE & TIME ───────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # Indian Standard Time
USE_I18N = True
USE_TZ = True


# ─── STATIC FILES (CSS, JS) ────────────────────────────────────────────────────
# Static files = your CSS, JavaScript files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']   # Where you put your CSS/JS files
STATIC_ROOT = BASE_DIR / 'staticfiles'     # Where collectstatic puts files


# ─── MEDIA FILES (Uploaded Images) ────────────────────────────────────────────
# Media files = files users upload (visiting card photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'            # Where uploaded files are saved


# ─── AUTH REDIRECTS ────────────────────────────────────────────────────────────
# After login, go to home. After logout, go to login page.
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/cards/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# ─── EMAIL SETTINGS ────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')


# ─── TWILIO (WhatsApp & SMS) ───────────────────────────────────────────────────
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
