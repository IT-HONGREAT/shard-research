import datetime
from pathlib import Path

from gunicorn.http import wsgi

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


PROJECT_NAME = "DRF-light"


class Response(wsgi.Response):
    def __init__(self, req, sock, cfg):
        super(Response, self).__init__(req, sock, cfg)
        self.version = PROJECT_NAME


wsgi.Response = Response


SECRET_KEY = "pj%2ze09(g)i^joilp-f8gvs)6ou_m036u3ejs^ky&9nse5k92"

ALLOWED_HOSTS = []

LOCAL_APPS = [
    "app.common.apps.CommonConfig",
    "app.user.apps.UserConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "channels",
    "corsheaders",
    "django_filters",
    "django_hosts",
    "drf_spectacular",
    "storages",
    "ckeditor",
    "ckeditor_uploader",
    "safedelete",
    "django_seed",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS


MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.RequestLogMiddleware",
]


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
            ],
        },
    },
]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ko"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_NAME = PROJECT_NAME


# APPEND_SLASH
APPEND_SLASH = False

# AUTH_USER_MODEL
AUTH_USER_MODEL = "user.User"

# SOCIAL REGISTER
SOCIAL_REGISTER = True

# APPLICATION
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.routing.application"


# HOST
DEFAULT_HOST = "api"
ROOT_HOSTCONF = "config.hosts"
ROOT_URLCONF = "config.urls.api"


# MODEL ID
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATABASE ROUTER
DATABASE_ROUTERS = [
    "config.router.ShardDBRouter",
]


# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}


# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.authentication.Authentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "app.common.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "EXCEPTION_HANDLER": "config.exception_handler.custom_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "config.openapi.CustomAutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "NON_FIELD_ERRORS_KEY": "non_field",
}


# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": f"{SITE_NAME} API",
    "DESCRIPTION": f"""swagger description""",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/v[0-9]",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SORT_OPERATIONS": False,
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 0,
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "agate",
        "showExtensions": True,
        "filter": True,
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "APPEND_COMPONENTS": {"securitySchemes": {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}},
    "SECURITY": [
        {
            "Bearer": [],
        }
    ],
    "PREPROCESSING_HOOKS": [
        "config.spectacular_hooks.api_ordering",
    ],
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
}

# CKEDITOR
CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
    },
}


# CELERY
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "Asia/Seoul"
CELERYD_SOFT_TIME_LIMIT = 300
CELERYD_TIME_LIMIT = CELERYD_SOFT_TIME_LIMIT + 60
CELERY_TASK_IGNORE_RESULT = True
