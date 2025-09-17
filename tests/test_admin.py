"""
Test admin for DDT Application.
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ddt_app.models import (
    Mittente, SedeMittente, Destinatario, Destinazione, Vettore, TargaVettore,
    Articolo, DDT, DDTRiga, CausaleTrasporto, FormatoNumerazioneDDT
)


class AdminTest(TestCase):
    """Test admin interface."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create test data
        self.mittente = Mittente.objects.create(
            nome="Test Mittente",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        
        self.sede_mittente = SedeMittente.objects.create(
            mittente=self.mittente,
            nome="Sede Principale",
            indirizzo="Via Roma, 123",
            cap="00100",
            citta="Roma",
            provincia="RM",
            sede_legale=True,
            attiva=True
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
        
        self.destinazione = Destinazione.objects.create(
            destinatario=self.destinatario,
            nome="Destinazione Principale",
            indirizzo="Via Destinazione, 456",
            codice_stalla="ST001"
        )
        
        self.vettore = Vettore.objects.create(
            nome="Test Vettore",
            indirizzo="Via Vettore, 789",
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
        
        self.targa_vettore = TargaVettore.objects.create(
            vettore=self.vettore,
            targa="AB123CD",
            tipo_veicolo="Furgone",
            attiva=True
        )
        
        self.articolo = Articolo.objects.create(
            nome="Test Articolo",
            categoria="Test",
            um="pz",
            prezzo_unitario=10.50
        )
        
        self.causale = CausaleTrasporto.objects.create(
            codice="VEN",
            descrizione="Vendita"
        )
        
        self.formato = FormatoNumerazioneDDT.objects.create(
            formato='aaaa-num',
            numero_iniziale=1,
            lunghezza_numero=4,
            attivo=True
        )
        
        self.ddt = DDT.objects.create(
            numero="2024-0001",
            data_documento="2024-01-15",
            mittente=self.mittente,
            sede_mittente=self.sede_mittente,
            destinatario=self.destinatario,
            destinazione=self.destinazione,
            causale_trasporto=self.causale,
            luogo_destinazione="Roma",
            trasporto_mezzo="vettore",
            data_ritiro="2024-01-15",
            vettore=self.vettore,
            targa_vettore=self.targa_vettore
        )
        
        self.ddt_riga = DDTRiga.objects.create(
            ddt=self.ddt,
            articolo=self.articolo,
            quantita=5.0,
            descrizione="Test descrizione",
            ordine=1
        )
    
    def test_admin_login(self):
        """Test admin login."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django administration')
    
    def test_mittente_admin(self):
        """Test Mittente admin."""
        response = self.client.get('/admin/ddt_app/mittente/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Mittente')
        
        # Test add
        response = self.client.get('/admin/ddt_app/mittente/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/mittente/{self.mittente.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Mittente')
    
    def test_sede_mittente_admin(self):
        """Test SedeMittente admin."""
        response = self.client.get('/admin/ddt_app/sedemittente/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sede Principale')
        
        # Test add
        response = self.client.get('/admin/ddt_app/sedemittente/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/sedemittente/{self.sede_mittente.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sede Principale')
    
    def test_destinatario_admin(self):
        """Test Destinatario admin."""
        response = self.client.get('/admin/ddt_app/destinatario/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Destinatario')
        
        # Test add
        response = self.client.get('/admin/ddt_app/destinatario/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/destinatario/{self.destinatario.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Destinatario')
    
    def test_destinazione_admin(self):
        """Test Destinazione admin."""
        response = self.client.get('/admin/ddt_app/destinazione/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Destinazione Principale')
        
        # Test add
        response = self.client.get('/admin/ddt_app/destinazione/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/destinazione/{self.destinazione.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Destinazione Principale')
    
    def test_vettore_admin(self):
        """Test Vettore admin."""
        response = self.client.get('/admin/ddt_app/vettore/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vettore')
        
        # Test add
        response = self.client.get('/admin/ddt_app/vettore/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/vettore/{self.vettore.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vettore')
    
    def test_targa_vettore_admin(self):
        """Test TargaVettore admin."""
        response = self.client.get('/admin/ddt_app/targavettore/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AB123CD')
        
        # Test add
        response = self.client.get('/admin/ddt_app/targavettore/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/targavettore/{self.targa_vettore.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AB123CD')
    
    def test_articolo_admin(self):
        """Test Articolo admin."""
        response = self.client.get('/admin/ddt_app/articolo/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Articolo')
        
        # Test add
        response = self.client.get('/admin/ddt_app/articolo/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/articolo/{self.articolo.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Articolo')
    
    def test_ddt_admin(self):
        """Test DDT admin."""
        response = self.client.get('/admin/ddt_app/ddt/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
        
        # Test add
        response = self.client.get('/admin/ddt_app/ddt/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/ddt/{self.ddt.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
    
    def test_ddt_riga_admin(self):
        """Test DDTRiga admin."""
        response = self.client.get('/admin/ddt_app/ddtriga/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Articolo')
        
        # Test add
        response = self.client.get('/admin/ddt_app/ddtriga/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/ddtriga/{self.ddt_riga.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Articolo')
    
    def test_causale_trasporto_admin(self):
        """Test CausaleTrasporto admin."""
        response = self.client.get('/admin/ddt_app/causaletrasporto/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VEN')
        
        # Test add
        response = self.client.get('/admin/ddt_app/causaletrasporto/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/causaletrasporto/{self.causale.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VEN')
    
    def test_formato_numerazione_ddt_admin(self):
        """Test FormatoNumerazioneDDT admin."""
        response = self.client.get('/admin/ddt_app/formatonumerazioneddt/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaaa-num')
        
        # Test add
        response = self.client.get('/admin/ddt_app/formatonumerazioneddt/add/')
        self.assertEqual(response.status_code, 200)
        
        # Test change
        response = self.client.get(f'/admin/ddt_app/formatonumerazioneddt/{self.formato.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aaaa-num')
    
    def test_admin_search(self):
        """Test admin search functionality."""
        # Search for mittente
        response = self.client.get('/admin/ddt_app/mittente/?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Mittente')
        
        # Search for destinatario
        response = self.client.get('/admin/ddt_app/destinatario/?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Destinatario')
        
        # Search for vettore
        response = self.client.get('/admin/ddt_app/vettore/?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vettore')
        
        # Search for articolo
        response = self.client.get('/admin/ddt_app/articolo/?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Articolo')
        
        # Search for DDT
        response = self.client.get('/admin/ddt_app/ddt/?q=2024')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2024-0001')
    
    def test_admin_filters(self):
        """Test admin filters."""
        # Filter mittenti by created_at
        response = self.client.get('/admin/ddt_app/mittente/?created_at__year=2024')
        self.assertEqual(response.status_code, 200)
        
        # Filter destinatari by provincia
        response = self.client.get('/admin/ddt_app/destinatario/?provincia=RM')
        self.assertEqual(response.status_code, 200)
        
        # Filter vettori by provincia
        response = self.client.get('/admin/ddt_app/vettore/?provincia=RM')
        self.assertEqual(response.status_code, 200)
        
        # Filter articoli by categoria
        response = self.client.get('/admin/ddt_app/articolo/?categoria=Test')
        self.assertEqual(response.status_code, 200)
        
        # Filter DDT by data_documento
        response = self.client.get('/admin/ddt_app/ddt/?data_documento__year=2024')
        self.assertEqual(response.status_code, 200)
        
        # Filter DDT by causale_trasporto
        response = self.client.get(f'/admin/ddt_app/ddt/?causale_trasporto={self.causale.pk}')
        self.assertEqual(response.status_code, 200)
        
        # Filter DDT by trasporto_mezzo
        response = self.client.get('/admin/ddt_app/ddt/?trasporto_mezzo=vettore')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_ordering(self):
        """Test admin ordering."""
        # Order mittenti by nome
        response = self.client.get('/admin/ddt_app/mittente/?o=1')
        self.assertEqual(response.status_code, 200)
        
        # Order destinatari by nome
        response = self.client.get('/admin/ddt_app/destinatario/?o=1')
        self.assertEqual(response.status_code, 200)
        
        # Order vettori by nome
        response = self.client.get('/admin/ddt_app/vettore/?o=1')
        self.assertEqual(response.status_code, 200)
        
        # Order articoli by nome
        response = self.client.get('/admin/ddt_app/articolo/?o=1')
        self.assertEqual(response.status_code, 200)
        
        # Order DDT by data_documento
        response = self.client.get('/admin/ddt_app/ddt/?o=1')
        self.assertEqual(response.status_code, 200)
        
        # Order DDT by numero
        response = self.client.get('/admin/ddt_app/ddt/?o=2')
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
def test_admin_anonymous_user():
    """Test admin for anonymous user."""
    client = Client()
    
    # Test admin login redirect
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/admin/login/' in response.url


@pytest.mark.django_db
def test_admin_regular_user():
    """Test admin for regular user."""
    client = Client()
    user = User.objects.create_user(
        username='regularuser',
        email='regular@example.com',
        password='regularpass123'
    )
    client.login(username='regularuser', password='regularpass123')
    
    # Test admin access denied
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/admin/login/' in response.url


@pytest.mark.django_db
def test_admin_superuser():
    """Test admin for superuser."""
    client = Client()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    client.login(username='admin', password='adminpass123')
    
    # Test admin access granted
    response = client.get('/admin/')
    assert response.status_code == 200
    assert 'Django administration' in response.content.decode()


@pytest.mark.django_db
def test_admin_model_creation():
    """Test admin model creation."""
    client = Client()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    client.login(username='admin', password='adminpass123')
    
    # Test creating mittente
    response = client.post('/admin/ddt_app/mittente/add/', {
        'nome': 'New Mittente',
        'piva': '12345678901',
        'cf': 'RSSMRA80A01H501U',
        'telefono': '+39 06 1234567',
        'email': 'new@example.com'
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check mittente was created
    assert Mittente.objects.filter(nome='New Mittente').exists()
    
    # Test creating destinatario
    response = client.post('/admin/ddt_app/destinatario/add/', {
        'nome': 'New Destinatario',
        'indirizzo': 'Via New, 123',
        'cap': '00100',
        'citta': 'Roma',
        'provincia': 'RM',
        'piva': '98765432109',
        'cf': 'BNCMRA80A01H501U',
        'telefono': '+39 06 7654321',
        'email': 'newdest@example.com'
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check destinatario was created
    assert Destinatario.objects.filter(nome='New Destinatario').exists()
    
    # Test creating vettore
    response = client.post('/admin/ddt_app/vettore/add/', {
        'nome': 'New Vettore',
        'indirizzo': 'Via Vettore, 456',
        'cap': '00100',
        'citta': 'Roma',
        'provincia': 'RM',
        'piva': '11111111111',
        'cf': 'VTTMRA80A01H501U',
        'telefono': '+39 06 1111111',
        'email': 'newvettore@example.com',
        'autista': 'Mario Rossi',
        'patente': 'B123456789'
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check vettore was created
    assert Vettore.objects.filter(nome='New Vettore').exists()
    
    # Test creating articolo
    response = client.post('/admin/ddt_app/articolo/add/', {
        'nome': 'New Articolo',
        'categoria': 'Test',
        'um': 'pz',
        'prezzo_unitario': '15.50'
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check articolo was created
    assert Articolo.objects.filter(nome='New Articolo').exists()
    
    # Test creating causale
    response = client.post('/admin/ddt_app/causaletrasporto/add/', {
        'codice': 'NEW',
        'descrizione': 'Nuova Causale',
        'attiva': True
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check causale was created
    assert CausaleTrasporto.objects.filter(codice='NEW').exists()
    
    # Test creating formato
    response = client.post('/admin/ddt_app/formatonumerazioneddt/add/', {
        'formato': 'num',
        'numero_iniziale': '1',
        'lunghezza_numero': '4',
        'attivo': True
    })
    assert response.status_code == 302  # Redirect after successful creation
    
    # Check formato was created
    assert FormatoNumerazioneDDT.objects.filter(formato='num').exists()
