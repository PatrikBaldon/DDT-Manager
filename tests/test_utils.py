"""
Test utils for DDT Application.
"""
import pytest
from django.test import TestCase
from ddt_app.utils import (
    generate_ddt_number, format_currency, format_date,
    validate_piva, validate_cf, validate_cap
)


class UtilsTest(TestCase):
    """Test utility functions."""
    
    def test_generate_ddt_number(self):
        """Test DDT number generation."""
        # Test with year
        numero = generate_ddt_number(2024, 1)
        self.assertEqual(numero, "2024-0001")
        
        # Test with different year
        numero = generate_ddt_number(2023, 1)
        self.assertEqual(numero, "2023-0001")
    
    def test_format_currency(self):
        """Test currency formatting."""
        # Test with float
        formatted = format_currency(10.50)
        self.assertEqual(formatted, "€ 10,50")
        
        # Test with integer
        formatted = format_currency(100)
        self.assertEqual(formatted, "€ 100,00")
        
        # Test with zero
        formatted = format_currency(0)
        self.assertEqual(formatted, "€ 0,00")
    
    def test_format_date(self):
        """Test date formatting."""
        from datetime import date
        
        # Test with date object
        test_date = date(2024, 1, 15)
        formatted = format_date(test_date)
        self.assertEqual(formatted, "15/01/2024")
        
        # Test with string
        formatted = format_date("2024-01-15")
        self.assertEqual(formatted, "15/01/2024")
    
    def test_validate_piva(self):
        """Test P.IVA validation."""
        # Valid P.IVA
        self.assertTrue(validate_piva("12345678901"))
        
        # Invalid P.IVA (too short)
        self.assertFalse(validate_piva("123"))
        
        # Invalid P.IVA (too long)
        self.assertFalse(validate_piva("123456789012"))
        
        # Invalid P.IVA (contains letters)
        self.assertFalse(validate_piva("1234567890a"))
        
        # Invalid P.IVA (empty)
        self.assertFalse(validate_piva(""))
    
    def test_validate_cf(self):
        """Test Codice Fiscale validation."""
        # Valid CF
        self.assertTrue(validate_cf("RSSMRA80A01H501U"))
        
        # Invalid CF (too short)
        self.assertFalse(validate_cf("RSSMRA80A01H501"))
        
        # Invalid CF (too long)
        self.assertFalse(validate_cf("RSSMRA80A01H501UU"))
        
        # Invalid CF (contains numbers in wrong places)
        self.assertFalse(validate_cf("RSSMRA80A01H5011"))
        
        # Invalid CF (empty)
        self.assertFalse(validate_cf(""))
    
    def test_validate_cap(self):
        """Test CAP validation."""
        # Valid CAP
        self.assertTrue(validate_cap("00100"))
        
        # Invalid CAP (too short)
        self.assertFalse(validate_cap("001"))
        
        # Invalid CAP (too long)
        self.assertFalse(validate_cap("001000"))
        
        # Invalid CAP (contains letters)
        self.assertFalse(validate_cap("0010a"))
        
        # Invalid CAP (empty)
        self.assertFalse(validate_cap(""))


@pytest.mark.django_db
def test_generate_ddt_number_integration():
    """Test DDT number generation integration."""
    from ddt_app.models import FormatoNumerazioneDDT
    
    # Create formato
    formato = FormatoNumerazioneDDT.objects.create(
        formato='aaaa-num',
        numero_iniziale=1,
        lunghezza_numero=4,
        attivo=True
    )
    
    # Test numero generation
    numero = formato.genera_numero(2024)
    assert numero == "2024-0001"
    
    # Test next numero
    numero = formato.genera_numero(2024)
    assert numero == "2024-0002"


@pytest.mark.django_db
def test_validate_piva_integration():
    """Test P.IVA validation integration."""
    from ddt_app.models import Mittente
    
    # Test with valid P.IVA
    mittente = Mittente(
        nome="Test Azienda",
        piva="12345678901",
        cf="RSSMRA80A01H501U",
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    
    # Should not raise validation error
    mittente.full_clean()
    
    # Test with invalid P.IVA
    mittente_invalid = Mittente(
        nome="Test Azienda",
        piva="123",  # Invalid P.IVA
        cf="RSSMRA80A01H501U",
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    
    # Should raise validation error
    with pytest.raises(Exception):  # ValidationError
        mittente_invalid.full_clean()


@pytest.mark.django_db
def test_validate_cf_integration():
    """Test Codice Fiscale validation integration."""
    from ddt_app.models import Mittente
    
    # Test with valid CF
    mittente = Mittente(
        nome="Test Azienda",
        piva="12345678901",
        cf="RSSMRA80A01H501U",
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    
    # Should not raise validation error
    mittente.full_clean()
    
    # Test with invalid CF
    mittente_invalid = Mittente(
        nome="Test Azienda",
        piva="12345678901",
        cf="RSSMRA80A01H501",  # Invalid CF
        telefono="+39 06 1234567",
        email="test@example.com"
    )
    
    # Should raise validation error
    with pytest.raises(Exception):  # ValidationError
        mittente_invalid.full_clean()


@pytest.mark.django_db
def test_validate_cap_integration():
    """Test CAP validation integration."""
    from ddt_app.models import Destinatario
    
    # Test with valid CAP
    destinatario = Destinatario(
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
    
    # Should not raise validation error
    destinatario.full_clean()
    
    # Test with invalid CAP
    destinatario_invalid = Destinatario(
        nome="Test Destinatario",
        indirizzo="Via Test, 123",
        cap="001",  # Invalid CAP
        citta="Roma",
        provincia="RM",
        piva="98765432109",
        cf="BNCMRA80A01H501U",
        telefono="+39 06 7654321",
        email="dest@example.com"
    )
    
    # Should raise validation error
    with pytest.raises(Exception):  # ValidationError
        destinatario_invalid.full_clean()