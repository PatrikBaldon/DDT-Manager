"""
Test forms for DDT Application.
"""
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from ddt_app.forms import (
    DDTForm, DDTRigaForm, MittenteForm, SedeMittenteForm,
    DestinatarioForm, DestinazioneForm, VettoreForm, TargaVettoreForm,
    ArticoloForm, CausaleTrasportoForm, FormatoNumerazioneDDTForm
)
from ddt_app.models import (
    Mittente, SedeMittente, Destinatario, Destinazione, Vettore, TargaVettore,
    Articolo, DDT, DDTRiga, CausaleTrasporto, FormatoNumerazioneDDT
)


class DDTFormTest(TestCase):
    """Test DDTForm."""
    
    def setUp(self):
        """Set up test data."""
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
    
    def test_ddt_form_valid(self):
        """Test DDT form with valid data."""
        form_data = {
            'numero': '2024-0001',
            'data_documento': '2024-01-01',
            'mittente': self.mittente.pk,
            'destinatario': self.destinatario.pk,
            'causale_trasporto': self.causale.pk,
            'luogo_destinazione': 'Roma',
            'trasporto_mezzo': 'vettore',
            'data_ritiro': '2024-01-01',
            'vettore': self.vettore.pk,
        }
        form = DDTForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_ddt_form_invalid(self):
        """Test DDT form with invalid data."""
        form_data = {
            'numero': '',  # Required field
            'data_documento': '2024-01-01',
            'mittente': self.mittente.pk,
            'destinatario': self.destinatario.pk,
            'causale_trasporto': self.causale.pk,
            'luogo_destinazione': 'Roma',
            'trasporto_mezzo': 'vettore',
            'data_ritiro': '2024-01-01',
            'vettore': self.vettore.pk,
        }
        form = DDTForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('numero', form.errors)


class MittenteFormTest(TestCase):
    """Test MittenteForm."""
    
    def test_mittente_form_valid(self):
        """Test Mittente form with valid data."""
        form_data = {
            'nome': 'Test Azienda',
            'piva': '12345678901',
            'cf': 'RSSMRA80A01H501U',
            'telefono': '+39 06 1234567',
            'email': 'test@example.com',
            'pec': 'pec@example.com',
            'note': 'Test note'
        }
        form = MittenteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_mittente_form_invalid_piva(self):
        """Test Mittente form with invalid P.IVA."""
        form_data = {
            'nome': 'Test Azienda',
            'piva': '123',  # Invalid P.IVA
            'cf': 'RSSMRA80A01H501U',
            'telefono': '+39 06 1234567',
            'email': 'test@example.com'
        }
        form = MittenteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('piva', form.errors)


class DestinatarioFormTest(TestCase):
    """Test DestinatarioForm."""
    
    def test_destinatario_form_valid(self):
        """Test Destinatario form with valid data."""
        form_data = {
            'nome': 'Test Destinatario',
            'indirizzo': 'Via Test, 123',
            'cap': '00100',
            'citta': 'Roma',
            'provincia': 'RM',
            'piva': '98765432109',
            'cf': 'BNCMRA80A01H501U',
            'telefono': '+39 06 7654321',
            'email': 'dest@example.com'
        }
        form = DestinatarioForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_destinatario_form_invalid_cap(self):
        """Test Destinatario form with invalid CAP."""
        form_data = {
            'nome': 'Test Destinatario',
            'indirizzo': 'Via Test, 123',
            'cap': '123',  # Invalid CAP
            'citta': 'Roma',
            'provincia': 'RM',
            'piva': '98765432109',
            'cf': 'BNCMRA80A01H501U',
            'telefono': '+39 06 7654321',
            'email': 'dest@example.com'
        }
        form = DestinatarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cap', form.errors)


class VettoreFormTest(TestCase):
    """Test VettoreForm."""
    
    def test_vettore_form_valid(self):
        """Test Vettore form with valid data."""
        form_data = {
            'nome': 'Test Vettore',
            'indirizzo': 'Via Vettore, 456',
            'cap': '00100',
            'citta': 'Roma',
            'provincia': 'RM',
            'piva': '11111111111',
            'cf': 'VTTMRA80A01H501U',
            'telefono': '+39 06 1111111',
            'email': 'vettore@example.com',
            'autista': 'Mario Rossi',
            'patente': 'B123456789',
            'licenza_bdn': 'BDN123456',
            'note': 'Test note'
        }
        form = VettoreForm(data=form_data)
        self.assertTrue(form.is_valid())


class ArticoloFormTest(TestCase):
    """Test ArticoloForm."""
    
    def test_articolo_form_valid(self):
        """Test Articolo form with valid data."""
        form_data = {
            'nome': 'Test Articolo',
            'categoria': 'Test',
            'um': 'pz',
            'prezzo_unitario': '10.50',
            'note': 'Test note'
        }
        form = ArticoloForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_articolo_form_invalid_prezzo(self):
        """Test Articolo form with invalid prezzo."""
        form_data = {
            'nome': 'Test Articolo',
            'categoria': 'Test',
            'um': 'pz',
            'prezzo_unitario': '-10.50',  # Invalid negative price
            'note': 'Test note'
        }
        form = ArticoloForm(data=form_data)
        self.assertFalse(form.is_valid())


class CausaleTrasportoFormTest(TestCase):
    """Test CausaleTrasportoForm."""
    
    def test_causale_form_valid(self):
        """Test CausaleTrasporto form with valid data."""
        form_data = {
            'codice': 'VEN',
            'descrizione': 'Vendita',
            'attiva': True,
            'note': 'Test note'
        }
        form = CausaleTrasportoForm(data=form_data)
        self.assertTrue(form.is_valid())


class FormatoNumerazioneDDTFormTest(TestCase):
    """Test FormatoNumerazioneDDTForm."""
    
    def test_formato_form_valid(self):
        """Test FormatoNumerazioneDDT form with valid data."""
        form_data = {
            'formato': 'aaaa-num',
            'numero_iniziale': 1,
            'lunghezza_numero': 4,
            'attivo': True
        }
        form = FormatoNumerazioneDDTForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formato_form_custom_valid(self):
        """Test FormatoNumerazioneDDT form with custom format."""
        form_data = {
            'formato': 'custom',
            'formato_personalizzato': 'DDT-{anno}-{numero}',
            'numero_iniziale': 1,
            'lunghezza_numero': 3,
            'attivo': True
        }
        form = FormatoNumerazioneDDTForm(data=form_data)
        self.assertTrue(form.is_valid())


@pytest.mark.django_db
def test_ddt_form_save():
    """Test DDT form save."""
    mittente = Mittente.objects.create(
        nome="Test Mittente",
        piva="12345678901",
        cf="RSSMRA80A01H501U",
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    
    destinatario = Destinatario.objects.create(
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
    
    causale = CausaleTrasporto.objects.create(
        codice="VEN",
        descrizione="Vendita"
    )
    
    vettore = Vettore.objects.create(
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
    
    form_data = {
        'numero': '2024-0001',
        'data_documento': '2024-01-01',
        'mittente': mittente.pk,
        'destinatario': destinatario.pk,
        'causale_trasporto': causale.pk,
        'luogo_destinazione': 'Roma',
        'trasporto_mezzo': 'vettore',
        'data_ritiro': '2024-01-01',
        'vettore': vettore.pk,
    }
    
    form = DDTForm(data=form_data)
    assert form.is_valid()
    
    ddt = form.save()
    assert ddt.numero == '2024-0001'
    assert ddt.mittente == mittente
    assert ddt.destinatario == destinatario
