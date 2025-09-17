"""
Test PDF generation for DDT Application.
"""
import pytest
from django.test import TestCase
from django.http import HttpResponse
from ddt_app.models import (
    Mittente, SedeMittente, Destinatario, Destinazione, Vettore, TargaVettore,
    Articolo, DDT, DDTRiga, CausaleTrasporto
)
from ddt_app.pdf_generator import generate_ddt_pdf


class PDFGenerationTest(TestCase):
    """Test PDF generation."""
    
    def setUp(self):
        """Set up test data."""
        # Create mittente
        self.mittente = Mittente.objects.create(
            nome="Test Mittente",
            piva="12345678901",
            cf="RSSMRA80A01H501U",
            telefono="+39 06 1234567",
            email="test@example.com"
        )
        
        # Create sede mittente
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
        
        # Create destinatario
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
        
        # Create destinazione
        self.destinazione = Destinazione.objects.create(
            destinatario=self.destinatario,
            nome="Destinazione Principale",
            indirizzo="Via Destinazione, 456",
            codice_stalla="ST001"
        )
        
        # Create vettore
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
        
        # Create targa vettore
        self.targa_vettore = TargaVettore.objects.create(
            vettore=self.vettore,
            targa="AB123CD",
            tipo_veicolo="Furgone",
            attiva=True
        )
        
        # Create causale
        self.causale = CausaleTrasporto.objects.create(
            codice="VEN",
            descrizione="Vendita"
        )
        
        # Create articolo
        self.articolo = Articolo.objects.create(
            nome="Test Articolo",
            categoria="Test",
            um="pz",
            prezzo_unitario=10.50
        )
        
        # Create DDT
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
            targa_vettore=self.targa_vettore,
            annotazioni="Test annotazioni"
        )
        
        # Create DDT riga
        self.ddt_riga = DDTRiga.objects.create(
            ddt=self.ddt,
            articolo=self.articolo,
            quantita=5.0,
            descrizione="Test descrizione",
            ordine=1
        )
    
    def test_generate_ddt_pdf(self):
        """Test DDT PDF generation."""
        response = generate_ddt_pdf(self.ddt)
        
        # Check response type
        self.assertIsInstance(response, HttpResponse)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check content disposition
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('DDT-2024-0001.pdf', response['Content-Disposition'])
        
        # Check content is not empty
        self.assertGreater(len(response.content), 0)
    
    def test_generate_ddt_pdf_with_righe(self):
        """Test DDT PDF generation with righe."""
        # Add more righe
        articolo2 = Articolo.objects.create(
            nome="Test Articolo 2",
            categoria="Test",
            um="kg",
            prezzo_unitario=15.75
        )
        
        DDTRiga.objects.create(
            ddt=self.ddt,
            articolo=articolo2,
            quantita=2.5,
            descrizione="Test descrizione 2",
            ordine=2
        )
        
        response = generate_ddt_pdf(self.ddt)
        
        # Check response type
        self.assertIsInstance(response, HttpResponse)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check content is not empty
        self.assertGreater(len(response.content), 0)
    
    def test_generate_ddt_pdf_with_note_centrali(self):
        """Test DDT PDF generation with note centrali."""
        # Update DDT with note centrali
        self.ddt.note_centrali = "Test note centrali"
        self.ddt.save()
        
        # Remove righe
        self.ddt_riga.delete()
        
        response = generate_ddt_pdf(self.ddt)
        
        # Check response type
        self.assertIsInstance(response, HttpResponse)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check content is not empty
        self.assertGreater(len(response.content), 0)
    
    def test_generate_ddt_pdf_without_sede_mittente(self):
        """Test DDT PDF generation without sede mittente."""
        # Update DDT without sede mittente
        self.ddt.sede_mittente = None
        self.ddt.save()
        
        response = generate_ddt_pdf(self.ddt)
        
        # Check response type
        self.assertIsInstance(response, HttpResponse)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check content is not empty
        self.assertGreater(len(response.content), 0)
    
    def test_generate_ddt_pdf_without_targa_vettore(self):
        """Test DDT PDF generation without targa vettore."""
        # Update DDT without targa vettore
        self.ddt.targa_vettore = None
        self.ddt.save()
        
        response = generate_ddt_pdf(self.ddt)
        
        # Check response type
        self.assertIsInstance(response, HttpResponse)
        
        # Check content type
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Check content is not empty
        self.assertGreater(len(response.content), 0)


@pytest.mark.django_db
def test_generate_ddt_pdf_integration():
    """Test DDT PDF generation integration."""
    # Create minimal DDT
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
        data_documento="2024-01-15",
        mittente=mittente,
        destinatario=destinatario,
        causale_trasporto=causale,
        luogo_destinazione="Roma",
        trasporto_mezzo="vettore",
        data_ritiro="2024-01-15",
        vettore=vettore
    )
    
    response = generate_ddt_pdf(ddt)
    
    assert isinstance(response, HttpResponse)
    assert response['Content-Type'] == 'application/pdf'
    assert len(response.content) > 0


@pytest.mark.django_db
def test_generate_ddt_pdf_error_handling():
    """Test DDT PDF generation error handling."""
    # Test with invalid DDT
    with pytest.raises(Exception):
        generate_ddt_pdf(None)
    
    # Test with non-existent DDT
    with pytest.raises(Exception):
        generate_ddt_pdf(999)
