"""
Production settings for DDT Application.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hour
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': get_env_variable('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = int(get_env_variable('EMAIL_PORT', '587'))
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL', 'noreply@ddt-app.com')

# Logging
LOGGING['handlers']['file']['filename'] = '/var/log/ddt/ddt.log'
LOGGING['handlers']['file']['level'] = 'WARNING'
LOGGING['loggers']['ddt_app']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'WARNING'

# Add file rotation
LOGGING['handlers']['file']['class'] = 'logging.handlers.RotatingFileHandler'
LOGGING['handlers']['file']['maxBytes'] = 1024 * 1024 * 5  # 5MB
LOGGING['handlers']['file']['backupCount'] = 5


# Production-specific settings
DDT_APP.update({
    'COMPANY_NAME': get_env_variable('COMPANY_NAME', 'Azienda Agricola BB&F'),
    'COMPANY_ADDRESS': get_env_variable('COMPANY_ADDRESS', 'Via Roma, 123 - 00100 Roma'),
    'COMPANY_PHONE': get_env_variable('COMPANY_PHONE', '+39 06 1234567'),
    'COMPANY_EMAIL': get_env_variable('COMPANY_EMAIL', 'info@azienda.com'),
    'COMPANY_TAX_CODE': get_env_variable('COMPANY_TAX_CODE', '12345678901'),
    'COMPANY_VAT_NUMBER': get_env_variable('COMPANY_VAT_NUMBER', 'IT12345678901'),
    'DEBUG_MODE': False,
    'ENABLE_DEBUG_TOOLBAR': False,
})

# Monitoring
if get_env_variable('ENABLE_MONITORING', 'False').lower() == 'true':
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
        
        sentry_sdk.init(
            dsn=get_env_variable('SENTRY_DSN'),
            integrations=[
                DjangoIntegration(),
                CeleryIntegration(),
            ],
            traces_sample_rate=0.1,
            send_default_pii=True,
        )
    except ImportError:
        pass
