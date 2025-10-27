from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# Database lokal (bisa SQLite atau PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# static dan media files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # untuk melihat email di terminal