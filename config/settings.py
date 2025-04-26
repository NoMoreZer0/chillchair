# flake8: noqa
import hashlib
import os
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR.joinpath("app")
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# -----------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = env.str("SECRET_KEY")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LOCALE_NAME = "ru"

LOCALE_PATHS = [str(BASE_DIR / "locale")]

LIST_PER_PAGE = 20

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CONTAINER_ENVIRONMENT = env.str("CONTAINER_ENVIRONMENT", "local")
BUILD_VERSION = env.str("BUILD_VERSION", "0.1.0")

CSRF_TRUSTED_ORIGINS = [
    "https://api-marsopr.site",
    "https://www.chillchair.xyz"
]


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = "core.User"

# INTERNATIONALIZATION
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "ru"

gettext = lambda s: s  # noqa

TIME_ZONE = "Asia/Aqtobe"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = " "

NUMBER_GROUPING = 3

LANGUAGES = [
    ("ru", gettext("Russian")),
    ("kk", gettext("Kazakh")),
    ("en", gettext("English")),
]

# HOSTS
# -----------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# APPLICATIONS
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "grappelli",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_json_widget",
]

LOCAL_APPS = ["app.core.apps.CoreConfig"]

THIRD_PARTY_APPS = [
    "drf_spectacular",
    "waffle",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
SITE_URL = "http://localhost:39000"

if CONTAINER_ENVIRONMENT in ["dev"]:
    SITE_URL = "https://api-marsopr.site"

# SPECTACULAR_SETTINGS
# -----------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "TITLE": "ChillChair API",
    "DESCRIPTION": "СhillChair backend service ultimate",
    "SERVERS": [{"url": SITE_URL}],
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
    },
}

# MIDDLEWARES
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "waffle.middleware.WaffleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR.joinpath("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "django.templatetags.static",
                "waffle.templatetags.waffle_tags",
            ],
        },
    }
]
# STATIC
# -----------------------------------------------------------------------------
STATIC_ROOT = "/static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    APP_DIR.joinpath("static"),
]

MEDIA_ROOT = "/media"
MEDIA_URL = "/media/"

if CONTAINER_ENVIRONMENT in ["ci"]:
    MEDIA_ROOT = APP_DIR.joinpath("media")

# DATABASE
# -----------------------------------------------------------------------------
DATABASES = {"default": env.db(), "deploy": env.db(), "readonly": env.db()}

# REST FRAMEWORK
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# Cache settings
# -----------------------------------------------------------------------------
def release_cache_key(key, key_prefix, version):
    key = hashlib.blake2s(str(key).encode("utf-8")).hexdigest()
    return f"{key_prefix}:{version}:{BUILD_VERSION[:9]}:{key}"


CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": [
            env.str("CACHE_MAIN", ""),
        ],
        "KEY_PREFIX": "chillchair",
        "KEY_FUNCTION": release_cache_key,
    },
}

if CONTAINER_ENVIRONMENT in ["local", "ci"]:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

GRAPPELLI_ADMIN_TITLE = "ChillChair"

if CONTAINER_ENVIRONMENT in ["prod"]:
    ALLOWED_HOSTS = [
        "localhost",
        "localhost:8000",  # healthcheck
    ]  # add here deployment host and SITE_URL
    SITE_URL = "https://"
    DEBUG = False
