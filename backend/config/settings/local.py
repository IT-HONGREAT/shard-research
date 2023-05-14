import os

import boto3
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS += ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# local database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_db_1",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    },
    "shard_1": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_db_1",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    },
    "shard_2": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_db_2",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5433",
    },
}

SHARD_GROUP = {
    "default": {
        "NAME": "shard_1",
        "SHARDS": ["shard_1", "shard_2"],
    },
}


# MEDIA
MEDIA_ROOT = BASE_DIR / "_media"
MEDIA_URL = "/_media/"


# STATIC
STATIC_ROOT = BASE_DIR / "_static"
STATIC_URL = "/_static/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple_formatter": {
            "format": "{message}",
            "style": "{",
        },
    },
    "handlers": {
        "simple_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple_formatter",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["simple_console"],
            "level": "DEBUG",
        },
    },
}
