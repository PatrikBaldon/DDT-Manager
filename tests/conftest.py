"""
Pytest configuration for DDT Application.
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def user():
    """Test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Test admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
