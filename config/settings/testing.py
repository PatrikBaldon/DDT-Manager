"""
Testing settings for DDT Application.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password hashers for faster testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable migrations for faster testing
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Test-specific settings
DDT_APP.update({
    'COMPANY_NAME': 'Test Company',
    'DEBUG_MODE': True,
    'ENABLE_DEBUG_TOOLBAR': False,
})

# Logging for testing
LOGGING['handlers']['console']['level'] = 'WARNING'
LOGGING['loggers']['ddt_app']['level'] = 'WARNING'
LOGGING['loggers']['django']['level'] = 'WARNING'
