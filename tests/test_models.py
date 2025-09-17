"""
Test models for DDT Application.
"""
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from ddt_app.models import (
    Mittente, SedeMittente, Destinatario, Destinazione, Vettore, TargaVettore,
    Articolo, DDT, DDTRiga, CausaleTrasporto, FormatoNumerazioneDDT
)


class MittenteModelTest(TestCase):
    """Test Mittente model."""
    
    def test_mittente_creation(self):
        """Test Mittente creation."""
        mittente = Mittente.objects.create(
            nome="Test Azienda",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        self.assertEqual(mittente.nome, "Test Azienda")
        self.assertEqual(mittente.piva, "12345678901")
        self.assertEqual(str(mittente), "Test Azienda")
    
    def test_mittente_piva_validation(self):
        """Test P.IVA validation."""
        with self.assertRaises(ValidationError):
            mittente = Mittente(
                nome="Test Azienda",
                piva="123",  # Invalid P.IVA
                cf="RSSMRA80A01H501U",
                telefono="+39 06 1234567",
                email="test@example.com"
            )
            mittente.full_clean()


class DDTModelTest(TestCase):
    """Test DDT model."""
    
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
    
    def test_ddt_creation(self):
        """Test DDT creation."""
        ddt = DDT.objects.create(
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
        self.assertEqual(ddt.numero, "2024-0001")
        self.assertEqual(str(ddt), "DDT 2024-0001 - Test Destinatario")
    
    def test_ddt_totale_quantita(self):
        """Test DDT totale quantita calculation."""
        ddt = DDT.objects.create(
            numero="2024-0002",
            data_documento="2024-01-01",
            mittente=self.mittente,
            destinatario=self.destinatario,
            causale_trasporto=self.causale,
            luogo_destinazione="Roma",
            trasporto_mezzo="vettore",
            data_ritiro="2024-01-01",
            vettore=self.vettore
        )
        
        # Create articolo
        articolo = Articolo.objects.create(
            nome="Test Articolo",
            categoria="Test",
            um="pz",
            prezzo_unitario=10.00
        )
        
        # Create righe
        DDTRiga.objects.create(
            ddt=ddt,
            articolo=articolo,
            quantita=5.0
        )
        DDTRiga.objects.create(
            ddt=ddt,
            articolo=articolo,
            quantita=3.0
        )
        
        self.assertEqual(ddt.totale_quantita, 8.0)
        self.assertEqual(ddt.totale_valore, 80.0)


class FormatoNumerazioneDDTTest(TestCase):
    """Test FormatoNumerazioneDDT model."""
    
    def test_genera_numero_aaaa_num(self):
        """Test numero generation with AAAA-NUM format."""
        formato = FormatoNumerazioneDDT.objects.create(
            formato='aaaa-num',
            numero_iniziale=1,
            lunghezza_numero=4
        )
        
        numero = formato.genera_numero(2024)
        self.assertEqual(numero, "2024-0001")
    
    def test_genera_numero_num(self):
        """Test numero generation with NUM format."""
        formato = FormatoNumerazioneDDT.objects.create(
            formato='num',
            numero_iniziale=1,
            lunghezza_numero=4
        )
        
        numero = formato.genera_numero()
        self.assertEqual(numero, "0001")
    
    def test_genera_numero_custom(self):
        """Test numero generation with custom format."""
        formato = FormatoNumerazioneDDT.objects.create(
            formato='custom',
            formato_personalizzato='DDT-{anno}-{numero}',
            numero_iniziale=1,
            lunghezza_numero=3
        )
        
        numero = formato.genera_numero(2024)
        self.assertEqual(numero, "DDT-2024-001")


@pytest.mark.django_db
def test_mittente_str():
    """Test Mittente __str__ method."""
    mittente = Mittente.objects.create(
        nome="Test Azienda",
        piva="12345678901",
        cf="RSSMRA80A01H501U",
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    assert str(mittente) == "Test Azienda"


@pytest.mark.django_db
def test_ddt_str():
    """Test DDT __str__ method."""
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
    
    ddt = DDT.objects.create(
        numero="2024-0001",
        data_documento="2024-01-01",
        mittente=mittente,
        destinatario=destinatario,
        causale_trasporto=causale,
        luogo_destinazione="Roma",
        trasporto_mezzo="vettore",
        data_ritiro="2024-01-01",
        vettore=vettore
    )
    
    assert str(ddt) == "DDT 2024-0001 - Test Destinatario"
