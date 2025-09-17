"""
Basic tests for DDT Application.
"""
import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BasicTestCase(TestCase):
    """Basic test cases."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_home_page_loads(self):
        """Test that home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_page_loads(self):
        """Test that admin page loads."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_can_login(self):
        """Test that user can login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_logout(self):
        """Test that user can logout."""
        self.client.login(username='testuser', password='testpass123')
        self.client.logout()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to login


@pytest.mark.django_db
def test_user_creation():
    """Test user creation."""
    user = User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )
    assert user.username == 'testuser2'
    assert user.email == 'test2@example.com'
    assert user.check_password('testpass123')
