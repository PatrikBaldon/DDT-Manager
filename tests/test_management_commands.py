"""
Test management commands for DDT Application.
"""
import pytest
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from io import StringIO
from ddt_app.models import (
    Mittente, Destinatario, Vettore, Articolo, CausaleTrasporto,
    FormatoNumerazioneDDT, DDT
)


class ManagementCommandsTest(TestCase):
    """Test management commands."""
    
    def test_load_initial_data_command(self):
        """Test load_initial_data command."""
        # Check initial state
        self.assertEqual(Mittente.objects.count(), 0)
        self.assertEqual(Destinatario.objects.count(), 0)
        self.assertEqual(Vettore.objects.count(), 0)
        self.assertEqual(Articolo.objects.count(), 0)
        self.assertEqual(CausaleTrasporto.objects.count(), 0)
        self.assertEqual(FormatoNumerazioneDDT.objects.count(), 0)
        
        # Run command
        out = StringIO()
        call_command('load_initial_data', stdout=out)
        
        # Check data was loaded
        self.assertGreater(Mittente.objects.count(), 0)
        self.assertGreater(Destinatario.objects.count(), 0)
        self.assertGreater(Vettore.objects.count(), 0)
        self.assertGreater(Articolo.objects.count(), 0)
        self.assertGreater(CausaleTrasporto.objects.count(), 0)
        self.assertGreater(FormatoNumerazioneDDT.objects.count(), 0)
        
        # Check output
        output = out.getvalue()
        self.assertIn('Dati iniziali caricati con successo', output)
    
    def test_setup_default_numbering_command(self):
        """Test setup_default_numbering command."""
        # Check initial state
        self.assertEqual(FormatoNumerazioneDDT.objects.count(), 0)
        
        # Run command
        out = StringIO()
        call_command('setup_default_numbering', stdout=out)
        
        # Check data was created
        self.assertEqual(FormatoNumerazioneDDT.objects.count(), 1)
        
        formato = FormatoNumerazioneDDT.objects.first()
        self.assertEqual(formato.formato, 'aaaa-num')
        self.assertEqual(formato.numero_iniziale, 1)
        self.assertEqual(formato.lunghezza_numero, 4)
        self.assertTrue(formato.attivo)
        
        # Check output
        output = out.getvalue()
        self.assertIn('Formato di numerazione configurato', output)
    
    def test_setup_default_numbering_command_with_existing(self):
        """Test setup_default_numbering command with existing formato."""
        # Create existing formato
        FormatoNumerazioneDDT.objects.create(
            formato='num',
            numero_iniziale=100,
            lunghezza_numero=3,
            attivo=True
        )
        
        # Check initial state
        self.assertEqual(FormatoNumerazioneDDT.objects.count(), 1)
        
        # Run command
        out = StringIO()
        call_command('setup_default_numbering', stdout=out)
        
        # Check no new formato was created
        self.assertEqual(FormatoNumerazioneDDT.objects.count(), 1)
        
        # Check output
        output = out.getvalue()
        self.assertIn('Formato di numerazione già esistente', output)
    
    def test_load_initial_data_command_with_existing_data(self):
        """Test load_initial_data command with existing data."""
        # Create some existing data
        Mittente.objects.create(
            nome="Existing Mittente",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        
        # Check initial state
        initial_count = Mittente.objects.count()
        
        # Run command
        out = StringIO()
        call_command('load_initial_data', stdout=out)
        
        # Check data was loaded (should not duplicate existing)
        self.assertGreaterEqual(Mittente.objects.count(), initial_count)
        
        # Check output
        output = out.getvalue()
        self.assertIn('Dati iniziali caricati con successo', output)


@pytest.mark.django_db
def test_load_initial_data_command_integration():
    """Test load_initial_data command integration."""
    # Run command
    out = StringIO()
    call_command('load_initial_data', stdout=out)
    
    # Check data was loaded
    assert Mittente.objects.count() > 0
    assert Destinatario.objects.count() > 0
    assert Vettore.objects.count() > 0
    assert Articolo.objects.count() > 0
    assert CausaleTrasporto.objects.count() > 0
    assert FormatoNumerazioneDDT.objects.count() > 0
    
    # Check specific data
    mittente = Mittente.objects.first()
    assert mittente.nome is not None
    assert mittente.piva is not None
    assert mittente.cf is not None
    assert mittente.telefono is not None
    assert mittente.email is not None
    
    destinatario = Destinatario.objects.first()
    assert destinatario.nome is not None
    assert destinatario.indirizzo is not None
    assert destinatario.cap is not None
    assert destinatario.citta is not None
    assert destinatario.provincia is not None
    assert destinatario.piva is not None
    assert destinatario.cf is not None
    assert destinatario.telefono is not None
    assert destinatario.email is not None
    
    vettore = Vettore.objects.first()
    assert vettore.nome is not None
    assert vettore.indirizzo is not None
    assert vettore.cap is not None
    assert vettore.citta is not None
    assert vettore.provincia is not None
    assert vettore.piva is not None
    assert vettore.cf is not None
    assert vettore.telefono is not None
    assert vettore.email is not None
    assert vettore.autista is not None
    assert vettore.patente is not None
    
    articolo = Articolo.objects.first()
    assert articolo.nome is not None
    assert articolo.categoria is not None
    assert articolo.um is not None
    assert articolo.prezzo_unitario is not None
    
    causale = CausaleTrasporto.objects.first()
    assert causale.codice is not None
    assert causale.descrizione is not None
    assert causale.attiva is not None
    
    formato = FormatoNumerazioneDDT.objects.first()
    assert formato.formato is not None
    assert formato.numero_iniziale is not None
    assert formato.lunghezza_numero is not None
    assert formato.attivo is not None


@pytest.mark.django_db
def test_setup_default_numbering_command_integration():
    """Test setup_default_numbering command integration."""
    # Run command
    out = StringIO()
    call_command('setup_default_numbering', stdout=out)
    
    # Check data was created
    assert FormatoNumerazioneDDT.objects.count() == 1
    
    formato = FormatoNumerazioneDDT.objects.first()
    assert formato.formato == 'aaaa-num'
    assert formato.numero_iniziale == 1
    assert formato.lunghezza_numero == 4
    assert formato.attivo is True
    
    # Test numero generation
    numero = formato.genera_numero(2024)
    assert numero == "2024-0001"
    
    # Test next numero
    numero = formato.genera_numero(2024)
    assert numero == "2024-0002"


@pytest.mark.django_db
def test_management_commands_error_handling():
    """Test management commands error handling."""
    # Test load_initial_data with invalid data
    with pytest.raises(CommandError):
        call_command('load_initial_data', '--invalid-option')
    
    # Test setup_default_numbering with invalid data
    with pytest.raises(CommandError):
        call_command('setup_default_numbering', '--invalid-option')
