"""
Development settings — SpatiaLite, DEBUG=True.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

SPATIALITE_LIBRARY_PATH = "/opt/homebrew/lib/mod_spatialite.dylib"
GDAL_LIBRARY_PATH = "/Applications/Postgres.app/Contents/Versions/16/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/Applications/Postgres.app/Contents/Versions/16/lib/libgeos_c.dylib"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
