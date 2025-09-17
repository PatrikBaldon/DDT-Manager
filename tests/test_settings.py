"""
Test settings for DDT Application.
"""
import pytest
from django.test import TestCase, override_settings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SettingsTest(TestCase):
    """Test settings configuration."""
    
    def test_development_settings(self):
        """Test development settings."""
        from config.settings.development import *
        
        # Check basic settings
        self.assertTrue(DEBUG)
        self.assertIn('localhost', ALLOWED_HOSTS)
        self.assertIn('127.0.0.1', ALLOWED_HOSTS)
        self.assertIn('0.0.0.0', ALLOWED_HOSTS)
        
        # Check database settings
        self.assertEqual(DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(DATABASES['default']['NAME'], 'db.sqlite3')
        
        # Check installed apps
        self.assertIn('ddt_app', INSTALLED_APPS)
        self.assertIn('crispy_forms', INSTALLED_APPS)
        self.assertIn('crispy_bootstrap5', INSTALLED_APPS)
        self.assertIn('rest_framework', INSTALLED_APPS)
        self.assertIn('corsheaders', INSTALLED_APPS)
        
        # Check middleware
        self.assertIn('corsheaders.middleware.CorsMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.security.SecurityMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.common.CommonMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.auth.middleware.AuthenticationMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.messages.middleware.MessageMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.clickjacking.XFrameOptionsMiddleware', MIDDLEWARE)
        
        # Check templates
        self.assertEqual(TEMPLATES[0]['BACKEND'], 'django.template.backends.django.DjangoTemplates')
        self.assertIn('templates', TEMPLATES[0]['DIRS'][0])
        self.assertTrue(TEMPLATES[0]['APP_DIRS'])
        
        # Check static files
        self.assertEqual(STATIC_URL, '/static/')
        self.assertIn('static', STATICFILES_DIRS[0])
        
        # Check media files
        self.assertEqual(MEDIA_URL, '/media/')
        self.assertIn('media', MEDIA_ROOT)
        
        # Check internationalization
        self.assertEqual(LANGUAGE_CODE, 'it-it')
        self.assertEqual(TIME_ZONE, 'Europe/Rome')
        self.assertTrue(USE_I18N)
        self.assertTrue(USE_TZ)
        
        # Check crispy forms
        self.assertEqual(CRISPY_ALLOWED_TEMPLATE_PACKS, "bootstrap5")
        self.assertEqual(CRISPY_TEMPLATE_PACK, "bootstrap5")
        
        # Check CORS
        self.assertTrue(CORS_ALLOW_ALL_ORIGINS)
        
        # Check logging
        self.assertIn('ddt_app', LOGGING['loggers'])
        self.assertIn('django', LOGGING['loggers'])
    
    def test_production_settings(self):
        """Test production settings."""
        from config.settings.production import *
        
        # Check basic settings
        self.assertFalse(DEBUG)
        self.assertIn('localhost', ALLOWED_HOSTS)
        
        # Check database settings
        self.assertEqual(DATABASES['default']['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(DATABASES['default']['NAME'], 'ddt_db')
        self.assertEqual(DATABASES['default']['USER'], 'ddt_user')
        self.assertEqual(DATABASES['default']['PASSWORD'], 'ddt_password')
        self.assertEqual(DATABASES['default']['HOST'], 'localhost')
        self.assertEqual(DATABASES['default']['PORT'], '5432')
        
        # Check security settings
        self.assertTrue(SECURE_SSL_REDIRECT)
        self.assertEqual(SECURE_HSTS_SECONDS, 31536000)
        self.assertTrue(SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertTrue(SECURE_HSTS_PRELOAD)
        self.assertTrue(SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertTrue(SECURE_BROWSER_XSS_FILTER)
        self.assertEqual(X_FRAME_OPTIONS, 'DENY')
        
        # Check session security
        self.assertTrue(SESSION_COOKIE_SECURE)
        self.assertTrue(SESSION_COOKIE_HTTPONLY)
        self.assertEqual(SESSION_COOKIE_AGE, 3600)
        self.assertTrue(CSRF_COOKIE_SECURE)
        self.assertTrue(CSRF_COOKIE_HTTPONLY)
        
        # Check cache
        self.assertEqual(CACHES['default']['BACKEND'], 'django.core.cache.backends.redis.RedisCache')
        self.assertEqual(CACHES['default']['LOCATION'], 'redis://localhost:6379/1')
        
        # Check email settings
        self.assertEqual(EMAIL_BACKEND, 'django.core.mail.backends.smtp.EmailBackend')
        self.assertEqual(EMAIL_HOST, 'localhost')
        self.assertEqual(EMAIL_PORT, 587)
        self.assertTrue(EMAIL_USE_TLS)
        self.assertEqual(EMAIL_HOST_USER, '')
        self.assertEqual(EMAIL_HOST_PASSWORD, '')
        self.assertEqual(DEFAULT_FROM_EMAIL, 'noreply@ddt-app.com')
        
        # Check logging
        self.assertIn('ddt_app', LOGGING['loggers'])
        self.assertIn('django', LOGGING['loggers'])
        self.assertEqual(LOGGING['handlers']['file']['filename'], '/var/log/ddt/ddt.log')
        self.assertEqual(LOGGING['handlers']['file']['level'], 'WARNING')
        self.assertEqual(LOGGING['loggers']['ddt_app']['level'], 'INFO')
        self.assertEqual(LOGGING['loggers']['django']['level'], 'WARNING')
    
    def test_testing_settings(self):
        """Test testing settings."""
        from config.settings.testing import *
        
        # Check basic settings
        self.assertTrue(DEBUG)
        
        # Check database settings
        self.assertEqual(DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(DATABASES['default']['NAME'], ':memory:')
        
        # Check password hashers
        self.assertEqual(PASSWORD_HASHERS[0], 'django.contrib.auth.hashers.MD5PasswordHasher')
        
        # Check cache
        self.assertEqual(CACHES['default']['BACKEND'], 'django.core.cache.backends.locmem.LocMemCache')
        
        # Check email backend
        self.assertEqual(EMAIL_BACKEND, 'django.core.mail.backends.locmem.EmailBackend')
        
        # Check migrations
        self.assertIsInstance(MIGRATION_MODULES, dict)
        
        # Check logging
        self.assertEqual(LOGGING['handlers']['console']['level'], 'WARNING')
        self.assertEqual(LOGGING['loggers']['ddt_app']['level'], 'WARNING')
        self.assertEqual(LOGGING['loggers']['django']['level'], 'WARNING')
    
    def test_base_settings(self):
        """Test base settings."""
        from config.settings.base import *
        
        # Check basic settings
        self.assertIsNotNone(SECRET_KEY)
        self.assertIsInstance(ALLOWED_HOSTS, list)
        
        # Check installed apps
        self.assertIn('django.contrib.admin', INSTALLED_APPS)
        self.assertIn('django.contrib.auth', INSTALLED_APPS)
        self.assertIn('django.contrib.contenttypes', INSTALLED_APPS)
        self.assertIn('django.contrib.sessions', INSTALLED_APPS)
        self.assertIn('django.contrib.messages', INSTALLED_APPS)
        self.assertIn('django.contrib.staticfiles', INSTALLED_APPS)
        self.assertIn('crispy_forms', INSTALLED_APPS)
        self.assertIn('crispy_bootstrap5', INSTALLED_APPS)
        self.assertIn('rest_framework', INSTALLED_APPS)
        self.assertIn('corsheaders', INSTALLED_APPS)
        self.assertIn('ddt_app', INSTALLED_APPS)
        
        # Check middleware
        self.assertIn('corsheaders.middleware.CorsMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.security.SecurityMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.common.CommonMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.auth.middleware.AuthenticationMiddleware', MIDDLEWARE)
        self.assertIn('django.contrib.messages.middleware.MessageMiddleware', MIDDLEWARE)
        self.assertIn('django.middleware.clickjacking.XFrameOptionsMiddleware', MIDDLEWARE)
        
        # Check templates
        self.assertEqual(TEMPLATES[0]['BACKEND'], 'django.template.backends.django.DjangoTemplates')
        self.assertIn('templates', TEMPLATES[0]['DIRS'][0])
        self.assertTrue(TEMPLATES[0]['APP_DIRS'])
        
        # Check static files
        self.assertEqual(STATIC_URL, '/static/')
        self.assertIn('static', STATICFILES_DIRS[0])
        
        # Check media files
        self.assertEqual(MEDIA_URL, '/media/')
        self.assertIn('media', MEDIA_ROOT)
        
        # Check internationalization
        self.assertEqual(LANGUAGE_CODE, 'it-it')
        self.assertEqual(TIME_ZONE, 'Europe/Rome')
        self.assertTrue(USE_I18N)
        self.assertTrue(USE_TZ)
        
        # Check crispy forms
        self.assertEqual(CRISPY_ALLOWED_TEMPLATE_PACKS, "bootstrap5")
        self.assertEqual(CRISPY_TEMPLATE_PACK, "bootstrap5")
        
        # Check REST framework
        self.assertIn('rest_framework.authentication.SessionAuthentication', REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])
        self.assertIn('rest_framework.authentication.TokenAuthentication', REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'])
        self.assertIn('rest_framework.permissions.IsAuthenticated', REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'])
        self.assertEqual(REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'], 'rest_framework.pagination.PageNumberPagination')
        self.assertEqual(REST_FRAMEWORK['PAGE_SIZE'], 20)
        
        # Check CORS
        self.assertIn('http://localhost:3000', CORS_ALLOWED_ORIGINS)
        self.assertIn('http://127.0.0.1:3000', CORS_ALLOWED_ORIGINS)
        self.assertTrue(CORS_ALLOW_CREDENTIALS)
        
        # Check security
        self.assertTrue(SECURE_BROWSER_XSS_FILTER)
        self.assertTrue(SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(X_FRAME_OPTIONS, 'DENY')
        
        # Check session
        self.assertTrue(SESSION_COOKIE_HTTPONLY)
        self.assertTrue(CSRF_COOKIE_HTTPONLY)
        
        # Check logging
        self.assertIn('ddt_app', LOGGING['loggers'])
        self.assertIn('django', LOGGING['loggers'])
        
        # Check cache
        self.assertEqual(CACHES['default']['BACKEND'], 'django.core.cache.backends.redis.RedisCache')
        self.assertEqual(CACHES['default']['LOCATION'], 'redis://localhost:6379/1')
        
        # Check Celery
        self.assertEqual(CELERY_BROKER_URL, 'redis://localhost:6379/0')
        self.assertEqual(CELERY_RESULT_BACKEND, 'redis://localhost:6379/0')
        self.assertEqual(CELERY_ACCEPT_CONTENT, ['json'])
        self.assertEqual(CELERY_TASK_SERIALIZER, 'json')
        self.assertEqual(CELERY_RESULT_SERIALIZER, 'json')
        self.assertEqual(CELERY_TIMEZONE, TIME_ZONE)
        
        # Check email
        self.assertEqual(EMAIL_BACKEND, 'django.core.mail.backends.console.EmailBackend')
        self.assertEqual(EMAIL_HOST, 'localhost')
        self.assertEqual(EMAIL_PORT, 587)
        self.assertTrue(EMAIL_USE_TLS)
        self.assertEqual(EMAIL_HOST_USER, '')
        self.assertEqual(EMAIL_HOST_PASSWORD, '')
        
        # Check file upload
        self.assertEqual(FILE_UPLOAD_MAX_MEMORY_SIZE, 10 * 1024 * 1024)
        self.assertEqual(DATA_UPLOAD_MAX_MEMORY_SIZE, 10 * 1024 * 1024)
        self.assertEqual(FILE_UPLOAD_PERMISSIONS, 0o644)
        
        # Check PDF settings
        self.assertIn('pdfs', PDF_OUTPUT_DIR)
        self.assertIn('pdfs', PDF_TEMP_DIR)
        
        # Check DDT app settings
        self.assertIn('COMPANY_NAME', DDT_APP)
        self.assertIn('COMPANY_ADDRESS', DDT_APP)
        self.assertIn('COMPANY_PHONE', DDT_APP)
        self.assertIn('COMPANY_EMAIL', DDT_APP)
        self.assertIn('COMPANY_TAX_CODE', DDT_APP)
        self.assertIn('COMPANY_VAT_NUMBER', DDT_APP)


@pytest.mark.django_db
def test_settings_import():
    """Test settings import."""
    from config.settings import development
    from config.settings import production
    from config.settings import testing
    from config.settings import base
    
    # Check that settings can be imported
    assert hasattr(development, 'DEBUG')
    assert hasattr(production, 'DEBUG')
    assert hasattr(testing, 'DEBUG')
    assert hasattr(base, 'SECRET_KEY')
    
    # Check that settings have expected values
    assert development.DEBUG is True
    assert production.DEBUG is False
    assert testing.DEBUG is True
    assert base.SECRET_KEY is not None


@pytest.mark.django_db
def test_settings_environment_variables():
    """Test settings environment variables."""
    import os
    
    # Test with environment variables
    os.environ['DEBUG'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['DB_NAME'] = 'test_db'
    os.environ['DB_USER'] = 'test_user'
    os.environ['DB_PASSWORD'] = 'test_password'
    os.environ['DB_HOST'] = 'test_host'
    os.environ['DB_PORT'] = '5432'
    os.environ['REDIS_URL'] = 'redis://test:6379/1'
    os.environ['CELERY_BROKER_URL'] = 'redis://test:6379/0'
    os.environ['CELERY_RESULT_BACKEND'] = 'redis://test:6379/0'
    os.environ['EMAIL_HOST'] = 'test_email_host'
    os.environ['EMAIL_PORT'] = '587'
    os.environ['EMAIL_USE_TLS'] = 'True'
    os.environ['EMAIL_HOST_USER'] = 'test_email_user'
    os.environ['EMAIL_HOST_PASSWORD'] = 'test_email_password'
    os.environ['DEFAULT_FROM_EMAIL'] = 'test@example.com'
    os.environ['COMPANY_NAME'] = 'Test Company'
    os.environ['COMPANY_ADDRESS'] = 'Test Address'
    os.environ['COMPANY_PHONE'] = '+39 06 1234567'
    os.environ['COMPANY_EMAIL'] = 'test@company.com'
    os.environ['COMPANY_TAX_CODE'] = '12345678901'
    os.environ['COMPANY_VAT_NUMBER'] = 'IT12345678901'
    os.environ['CORS_ALLOWED_ORIGINS'] = 'http://test.com,https://test.com'
    os.environ['ENABLE_MONITORING'] = 'True'
    os.environ['SENTRY_DSN'] = 'https://test@sentry.io/test'
    os.environ['GRAFANA_PASSWORD'] = 'test_password'
    
    # Import settings
    from config.settings.development import *
    
    # Check that environment variables are used
    assert DEBUG is True
    assert SECRET_KEY == 'test-secret-key'
    assert DATABASES['default']['NAME'] == 'test_db'
    assert DATABASES['default']['USER'] == 'test_user'
    assert DATABASES['default']['PASSWORD'] == 'test_password'
    assert DATABASES['default']['HOST'] == 'test_host'
    assert DATABASES['default']['PORT'] == '5432'
    assert CACHES['default']['LOCATION'] == 'redis://test:6379/1'
    assert CELERY_BROKER_URL == 'redis://test:6379/0'
    assert CELERY_RESULT_BACKEND == 'redis://test:6379/0'
    assert EMAIL_HOST == 'test_email_host'
    assert EMAIL_PORT == 587
    assert EMAIL_USE_TLS is True
    assert EMAIL_HOST_USER == 'test_email_user'
    assert EMAIL_HOST_PASSWORD == 'test_email_password'
    assert DEFAULT_FROM_EMAIL == 'test@example.com'
    assert DDT_APP['COMPANY_NAME'] == 'Test Company'
    assert DDT_APP['COMPANY_ADDRESS'] == 'Test Address'
    assert DDT_APP['COMPANY_PHONE'] == '+39 06 1234567'
    assert DDT_APP['COMPANY_EMAIL'] == 'test@company.com'
    assert DDT_APP['COMPANY_TAX_CODE'] == '12345678901'
    assert DDT_APP['COMPANY_VAT_NUMBER'] == 'IT12345678901'
    assert 'http://test.com' in CORS_ALLOWED_ORIGINS
    assert 'https://test.com' in CORS_ALLOWED_ORIGINS
    assert ENABLE_MONITORING is True
    assert SENTRY_DSN == 'https://test@sentry.io/test'
    assert GRAFANA_PASSWORD == 'test_password'
    
    # Clean up
    for key in ['DEBUG', 'SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
                'REDIS_URL', 'CELERY_BROKER_URL', 'CELERY_RESULT_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT',
                'EMAIL_USE_TLS', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL',
                'COMPANY_NAME', 'COMPANY_ADDRESS', 'COMPANY_PHONE', 'COMPANY_EMAIL', 'COMPANY_TAX_CODE',
                'COMPANY_VAT_NUMBER', 'CORS_ALLOWED_ORIGINS', 'ENABLE_MONITORING', 'SENTRY_DSN', 'GRAFANA_PASSWORD']:
        if key in os.environ:
            del os.environ[key]
