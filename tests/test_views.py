"""
Test views for DDT Application.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ddt_app.models import (
    Mittente, Destinatario, Vettore, CausaleTrasporto, DDT, Articolo
)


class DDTViewsTest(TestCase):
    """Test DDT views."""
    
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
        
        self.causale = CausaleTrasporto.objects.create(
            codice="VEN",
            descrizione="Vendita"
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
        
        self.ddt = DDT.objects.create(
            numero="2024-0001",
            data_documento="2024-01-01",
            mittente=self.mittente,
            destinatario=self.destinatario,
            causale_trasporto=self.causale,
            luogo_destinazione="Roma",
            trasporto_mezzo="vettore",
            data_ritiro="2024-01-01",
            vettore=self.vettore
        )
    
    def test_home_view(self):
        """Test home view."""
        response = self.client.get(reverse('ddt_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DDT Application')
    
    def test_ddt_list_view(self):
        """Test DDT list view."""
        response = self.client.get(reverse('ddt_app:ddt_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
    
    def test_ddt_detail_view(self):
        """Test DDT detail view."""
        response = self.client.get(reverse('ddt_app:ddt_detail', args=[self.ddt.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
    
    def test_ddt_create_view_get(self):
        """Test DDT create view GET."""
        response = self.client.get(reverse('ddt_app:ddt_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_ddt_create_view_post(self):
        """Test DDT create view POST."""
        data = {
            'numero': '2024-0002',
            'data_documento': '2024-01-02',
            'mittente': self.mittente.pk,
            'destinatario': self.destinatario.pk,
            'causale_trasporto': self.causale.pk,
            'luogo_destinazione': 'Milano',
            'trasporto_mezzo': 'vettore',
            'data_ritiro': '2024-01-02',
            'vettore': self.vettore.pk,
        }
        response = self.client.post(reverse('ddt_app:ddt_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(DDT.objects.filter(numero='2024-0002').exists())
    
    def test_ddt_edit_view_get(self):
        """Test DDT edit view GET."""
        response = self.client.get(reverse('ddt_app:ddt_edit', args=[self.ddt.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
    
    def test_ddt_delete_view_get(self):
        """Test DDT delete view GET."""
        response = self.client.get(reverse('ddt_app:ddt_delete', args=[self.ddt.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conferma eliminazione')
    
    def test_ddt_delete_view_post(self):
        """Test DDT delete view POST."""
        response = self.client.post(reverse('ddt_app:ddt_delete', args=[self.ddt.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(DDT.objects.filter(pk=self.ddt.pk).exists())


class DDTAPITest(TestCase):
    """Test DDT API endpoints."""
    
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
        
        self.articolo = Articolo.objects.create(
            nome="Test Articolo",
            categoria="Test",
            um="pz",
            prezzo_unitario=10.00
        )
    
    def test_get_next_ddt_number(self):
        """Test get next DDT number API."""
        response = self.client.get(reverse('ddt_app:next_ddt_number'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('numero', data)
    
    def test_get_articoli(self):
        """Test get articoli API."""
        response = self.client.get(reverse('ddt_app:articoli'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('articoli', data)
        self.assertEqual(len(data['articoli']), 1)
        self.assertEqual(data['articoli'][0]['nome'], 'Test Articolo')


@pytest.mark.django_db
def test_home_view_anonymous():
    """Test home view for anonymous user."""
    client = Client()
    response = client.get(reverse('ddt_app:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_ddt_list_view_anonymous():
    """Test DDT list view for anonymous user."""
    client = Client()
    response = client.get(reverse('ddt_app:ddt_list'))
    assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
def test_api_endpoints():
    """Test API endpoints."""
    client = Client()
    
    # Test API root
    response = client.get('/api/')
    assert response.status_code == 200
    
    # Test API auth
    response = client.get('/api/auth/')
    assert response.status_code == 200
