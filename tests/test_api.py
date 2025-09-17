"""
Test API for DDT Application.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ddt_app.models import (
    Mittente, Destinatario, Vettore, TargaVettore, Articolo, DDT, CausaleTrasporto
)


class DDTAPITestCase(APITestCase):
    """Test DDT API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.mittente = Mittente.objects.create(
            nome="Test Mittente",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        
        self.destinatario = Destinatario.objects.create(
            nome="Test Destinatario",
            indirizzo="Via Test, 123",
            cap="00100",
            citta="Roma",
            provincia="RM",
            piva="98765432109",
            cf="BNCMRA80A01H501U",
            telefono="+39 06 7654321",
            email="dest@example.com"
        )
        
        self.vettore = Vettore.objects.create(
            nome="Test Vettore",
            indirizzo="Via Vettore, 456",
            cap="00100",
            citta="Roma",
            provincia="RM",
            piva="11111111111",
            cf="VTTMRA80A01H501U",
            telefono="+39 06 1111111",
            email="vettore@example.com",
            autista="Mario Rossi",
            patente="B123456789"
        )
        
        self.targa = TargaVettore.objects.create(
            vettore=self.vettore,
            targa="AB123CD",
            tipo_veicolo="Furgone",
            attiva=True
        )
        
        self.articolo = Articolo.objects.create(
            nome="Test Articolo",
            categoria="Test",
            um="pz",
            prezzo_unitario=10.00
        )
        
        self.causale = CausaleTrasporto.objects.create(
            codice="VEN",
            descrizione="Vendita"
        )
    
    def test_api_root(self):
        """Test API root endpoint."""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_auth(self):
        """Test API authentication endpoint."""
        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_next_ddt_number(self):
        """Test get next DDT number API."""
        response = self.client.get(reverse('ddt_app:next_ddt_number'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('numero', data)
        self.assertIsInstance(data['numero'], str)
    
    def test_get_articoli(self):
        """Test get articoli API."""
        response = self.client.get(reverse('ddt_app:articoli'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('articoli', data)
        self.assertEqual(len(data['articoli']), 1)
        self.assertEqual(data['articoli'][0]['nome'], 'Test Articolo')
        self.assertEqual(data['articoli'][0]['categoria'], 'Test')
        self.assertEqual(data['articoli'][0]['um'], 'pz')
        self.assertEqual(data['articoli'][0]['prezzo'], 10.0)
    
    def test_get_destinazioni_by_destinatario(self):
        """Test get destinazioni by destinatario API."""
        # Create destinazione
        from ddt_app.models import Destinazione
        destinazione = Destinazione.objects.create(
            destinatario=self.destinatario,
            nome="Test Destinazione",
            indirizzo="Via Destinazione, 789",
            codice_stalla="ST001"
        )
        
        response = self.client.get(reverse('ddt_app:destinazioni_by_destinatario', args=[self.destinatario.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('destinazioni', data)
        self.assertEqual(len(data['destinazioni']), 1)
        self.assertEqual(data['destinazioni'][0]['nome'], 'Test Destinazione')
    
    def test_get_targhe_by_vettore(self):
        """Test get targhe by vettore API."""
        response = self.client.get(reverse('ddt_app:targhe_by_vettore', args=[self.vettore.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('targhe', data)
        self.assertEqual(len(data['targhe']), 1)
        self.assertEqual(data['targhe'][0]['targa'], 'AB123CD')
    
    def test_get_destinazioni_by_destinatario_not_found(self):
        """Test get destinazioni by destinatario with non-existent destinatario."""
        response = self.client.get(reverse('ddt_app:destinazioni_by_destinatario', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_targhe_by_vettore_not_found(self):
        """Test get targhe by vettore with non-existent vettore."""
        response = self.client.get(reverse('ddt_app:targhe_by_vettore', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_api_without_authentication(self):
        """Test API endpoints without authentication."""
        self.client.force_authenticate(user=None)
        
        # These endpoints should still work without authentication
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # These endpoints require authentication
        response = self.client.get(reverse('ddt_app:next_ddt_number'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to login


class DDTAPIIntegrationTest(TestCase):
    """Test DDT API integration."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test data
        self.mittente = Mittente.objects.create(
            nome="Test Mittente",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        
        self.destinatario = Destinatario.objects.create(
            nome="Test Destinatario",
            indirizzo="Via Test, 123",
            cap="00100",
            citta="Roma",
            provincia="RM",
            piva="98765432109",
            cf="BNCMRA80A01H501U",
            telefono="+39 06 7654321",
            email="dest@example.com"
        )
        
        self.vettore = Vettore.objects.create(
            nome="Test Vettore",
            indirizzo="Via Vettore, 456",
            cap="00100",
            citta="Roma",
            provincia="RM",
            piva="11111111111",
            cf="VTTMRA80A01H501U",
            telefono="+39 06 1111111",
            email="vettore@example.com",
            autista="Mario Rossi",
            patente="B123456789"
        )
    
    def test_api_endpoints_integration(self):
        """Test API endpoints integration."""
        # Test API root
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        
        # Test API auth
        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)
        
        # Test get next DDT number
        response = self.client.get(reverse('ddt_app:next_ddt_number'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('numero', data)
        
        # Test get articoli
        response = self.client.get(reverse('ddt_app:articoli'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('articoli', data)
        
        # Test get destinazioni by destinatario
        response = self.client.get(reverse('ddt_app:destinazioni_by_destinatario', args=[self.destinatario.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('destinazioni', data)
        
        # Test get targhe by vettore
        response = self.client.get(reverse('ddt_app:targhe_by_vettore', args=[self.vettore.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('targhe', data)


@pytest.mark.django_db
def test_api_endpoints_anonymous():
    """Test API endpoints for anonymous user."""
    client = Client()
    
    # Test API root
    response = client.get('/api/')
    assert response.status_code == 200
    
    # Test API auth
    response = client.get('/api/auth/')
    assert response.status_code == 200
    
    # Test get next DDT number (should redirect to login)
    response = client.get(reverse('ddt_app:next_ddt_number'))
    assert response.status_code == 302
    
    # Test get articoli (should redirect to login)
    response = client.get(reverse('ddt_app:articoli'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_api_error_handling():
    """Test API error handling."""
    client = Client()
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    client.login(username='testuser', password='testpass123')
    
    # Test get destinazioni by non-existent destinatario
    response = client.get(reverse('ddt_app:destinazioni_by_destinatario', args=[999]))
    assert response.status_code == 404
    
    # Test get targhe by non-existent vettore
    response = client.get(reverse('ddt_app:targhe_by_vettore', args=[999]))
    assert response.status_code == 404