import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------
# Load environment variables
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "Example.env")  # Явно підключаємо твій файл .env

# -------------------------
# Security
# -------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    "subio.onrender.com",
    "localhost",
    "127.0.0.1"
]


# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN не заданий у Example.env")

# -------------------------
# Installed apps
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "users",
    "subscriptions",
    "dashboard",
    "notifications",
    'widget_tweaks',
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "subio.urls"

# -------------------------
# Templates
# -------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "subio.wsgi.application"

# -------------------------
# Database
# -------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# -------------------------
# Password validation
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------
# Static and media
# -------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -------------------------
# Email config
# -------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# -------------------------
# Celery config
# -------------------------
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# -------------------------
# Authentication URLs
# -------------------------
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/users/login/'

AUTH_USER_MODEL = "users.CustomUser"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ["subio", "localhost", "127.0.0.1"]
