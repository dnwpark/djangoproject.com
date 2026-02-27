from .common import *  # noqa

ALLOWED_HOSTS = [
    "www.djangoproject.localhost",
    "djangoproject.localhost",
    "docs.djangoproject.localhost",
    "dashboard.djangoproject.localhost",
    ".vercel.app",
] + SECRETS.get("allowed_hosts", [])

LOCALE_MIDDLEWARE_EXCLUDED_HOSTS = ["docs.djangoproject.localhost"]

DEBUG = True
THUMBNAIL_DEBUG = DEBUG

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "trololololol",
    },
    "docs-pages": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "docs-pages",
    },
}

CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_ROOT = DATA_DIR / "media_root"

SESSION_COOKIE_SECURE = False

STATIC_ROOT = DATA_DIR / "static_root"

# Docs settings
DOCS_BUILD_ROOT = DATA_DIR / "djangodocs"

# django-hosts settings

PARENT_HOST = "djangoproject.localhost:8000"

# django-push settings

PUSH_SSL_CALLBACK = False

# django-debug-toolbar initialization
try:
    import debug_toolbar  # NOQA
except ImportError:
    pass
else:
    INSTALLED_APPS.append("debug_toolbar")
    INTERNAL_IPS = ["127.0.0.1"]
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    MIDDLEWARE.insert(
        MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,
        "djangoproject.middleware.CORSMiddleware",
    )

# Vercel static files
if os.getenv("VERCEL"):
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
        "whitenoise.middleware.WhiteNoiseMiddleware",
    )
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Vercel / Neon database override
if os.getenv("DATABASE_URL"):
    import urllib.parse

    _db_url = urllib.parse.urlparse(os.getenv("DATABASE_URL"))
    DATABASES["default"].update({
        "NAME": _db_url.path.lstrip("/"),
        "USER": _db_url.username,
        "PASSWORD": _db_url.password,
        "HOST": _db_url.hostname,
        "PORT": str(_db_url.port or ""),
        "OPTIONS": {"sslmode": "require"},
    })

# django-recaptcha settings
SILENCED_SYSTEM_CHECKS = SILENCED_SYSTEM_CHECKS + [
    # Default test keys for development.
    "django_recaptcha.recaptcha_test_key_error"
]
