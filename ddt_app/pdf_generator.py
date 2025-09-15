"""
PDF Generator per i DDT basato sul modello esistente
"""
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white, Color
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from .models import DDT


def generate_ddt_pdf(ddt):
    """
    Genera un PDF per il DDT specificato basato sul modello esistente
    """
    # Crea la directory per i PDF se non esiste
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nome del file PDF
    pdf_filename = f"DDT_{ddt.numero.replace('/', '_')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    
    # Dimensioni A4
    page_width, page_height = A4
    
    # Margini richiesti
    margin_top = 1 * cm
    margin_bottom = 1.5 * cm
    margin_left = 1 * cm
    margin_right = 1 * cm
    
    # Area utilizzabile
    usable_width = page_width - margin_left - margin_right
    usable_height = page_height - margin_top - margin_bottom
    
    # Striscia grigia scura
    stripe_height = 1.5 * cm
    stripe_x = margin_left
    stripe_y = page_height - margin_top - stripe_height
    stripe_width = usable_width
    
    # Colore grigio scuro quasi nero
    dark_grey = Color(0.2, 0.2, 0.2)
    
    # Crea il PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # Disegna la striscia grigia scura
    c.setFillColor(dark_grey)
    c.rect(stripe_x, stripe_y, stripe_width, stripe_height, fill=1, stroke=0)
    
    # Posiziona il testo al centro della striscia
    text = "DOCUMENTO DI TRASPORTO"
    c.setFillColor(white)
    c.setFont("Times-Bold", 18)
    
    # Calcola la larghezza totale del testo con spaziatura
    char_spacing = 7
    total_width = 0
    for char in text:
        if char == ' ':
            total_width += c.stringWidth(char, "Times-Bold", 14)
        else:
            total_width += c.stringWidth(char, "Times-Bold", 14) + char_spacing
    
    # Calcola la posizione del testo per centrarlo
    text_x = stripe_x + (stripe_width - total_width) / 2
    text_y = stripe_y + (stripe_height - 14) / 2
    
    # Disegna il testo con spaziatura maggiore tra le lettere
    current_x = text_x
    for char in text:
        if char == ' ':
            char_width = c.stringWidth(char, "Times-Bold", 14)
            c.drawString(current_x, text_y, char)
            current_x += char_width
        else:
            char_width = c.stringWidth(char, "Times-Bold", 14)
            c.drawString(current_x, text_y, char)
            current_x += char_width + char_spacing
    
    # Casella mittente
    mittente_y = stripe_y - 1 * cm - 4.3 * cm
    mittente_x = margin_left
    mittente_width = (stripe_width / 2) - 0.05 * cm
    mittente_height = 4.3 * cm
    
    # Disegna la casella mittente
    c.setFillColor(black)
    c.rect(mittente_x, mittente_y, mittente_width, mittente_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "MITTENTE"
    c.setFont("Times-Bold", 10)
    label_text = "MITTENTE"
    label_x = mittente_x + 5
    label_y = mittente_y + mittente_height - 15
    c.drawString(label_x, label_y, label_text)
    
    # Inserisci i dati del mittente
    c.setFont("Times-Roman", 9)
    mittente_data = [
        ddt.mittente.nome,
        ddt.mittente.indirizzo,
        f"{ddt.mittente.cap} {ddt.mittente.citta} ({ddt.mittente.provincia})",
        f"P.IVA: {ddt.mittente.piva}",
        f"CF: {ddt.mittente.cf}",
        f"Tel: {ddt.mittente.telefono}",
        f"Email: {ddt.mittente.email}"
    ]
    
    y_offset = label_y - 20
    for line in mittente_data:
        if y_offset > mittente_y + 10:  # Evita di scrivere fuori dalla casella
            c.drawString(mittente_x + 5, y_offset, line[:50])  # Tronca se troppo lungo
            y_offset -= 12
    
    # Inserisci il logo se disponibile
    logo_path = os.path.join(settings.BASE_DIR, 'logo1.png')
    if os.path.exists(logo_path):
        try:
            img = ImageReader(logo_path)
            logo_width = 2.5 * cm
            logo_height = 2.5 * cm
            logo_x = mittente_x + mittente_width - logo_width - 5
            logo_y = mittente_y + mittente_height - logo_height - 5
            c.drawImage(img, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
        except Exception as e:
            print(f"Errore nel caricamento del logo: {e}")
    
    # Seconda casella - Causale di trasporto
    casella2_y = mittente_y - 0.1 * cm - 1.8 * cm
    casella2_x = margin_left
    casella2_width = mittente_width
    casella2_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella2_x, casella2_y, casella2_width, casella2_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label2_text = "CAUSALE DI TRASPORTO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 15
    c.drawString(label2_x, label2_y, label2_text)
    
    c.setFont("Times-Roman", 12)
    c.drawString(casella2_x + 5, casella2_y + 5, ddt.causale_trasporto)
    
    # Casella numero e data
    casella3_x = mittente_x + mittente_width + 0.1 * cm
    casella3_y = stripe_y - 1 * cm - 1.8 * cm
    casella3_width = (stripe_width / 2) - 0.05 * cm
    casella3_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label3_text = "NUMERO E DATA DOCUMENTO"
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 15
    c.drawString(label3_x, label3_y, label3_text)
    
    c.setFont("Times-Roman", 12)
    c.drawString(casella3_x + 5, casella3_y + 5, f"DDT n. {ddt.numero}")
    c.drawString(casella3_x + 5, casella3_y - 10, f"Data: {ddt.data_documento.strftime('%d/%m/%Y')}")
    
    # Casella destinatario
    casella4_x = casella3_x
    casella4_y = casella3_y - 0.1 * cm - 4.3 * cm
    casella4_width = casella3_width
    casella4_height = 4.3 * cm
    
    c.setFillColor(black)
    c.rect(casella4_x, casella4_y, casella4_width, casella4_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label4_text = "DESTINATARIO"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 15
    c.drawString(label4_x, label4_y, label4_text)
    
    # Inserisci i dati del destinatario
    c.setFont("Times-Roman", 9)
    destinatario_data = [
        ddt.destinatario.nome,
        ddt.destinatario.indirizzo,
        f"{ddt.destinatario.cap} {ddt.destinatario.citta} ({ddt.destinatario.provincia})",
        f"P.IVA: {ddt.destinatario.piva}",
        f"CF: {ddt.destinatario.cf}",
        f"Tel: {ddt.destinatario.telefono}",
        f"Email: {ddt.destinatario.email}"
    ]
    
    y_offset = label4_y - 20
    for line in destinatario_data:
        if y_offset > casella4_y + 10:
            c.drawString(casella4_x + 5, y_offset, line[:50])
            y_offset -= 12
    
    # Casella luogo di destinazione
    casella5_x = margin_left
    casella5_y = casella2_y - 0.1 * cm - 2.5 * cm
    casella5_width = stripe_width
    casella5_height = 2.5 * cm
    
    c.setFillColor(black)
    c.rect(casella5_x, casella5_y, casella5_width, casella5_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label5_text = "LUOGO DI DESTINAZIONE"
    label5_x = casella5_x + 5
    label5_y = casella5_y + casella5_height - 15
    c.drawString(label5_x, label5_y, label5_text)
    
    c.setFont("Times-Roman", 10)
    c.drawString(casella5_x + 5, casella5_y + 5, ddt.luogo_destinazione)
    
    # Tabella prodotti
    tabella_x = margin_left
    tabella_y = casella5_y - 0.1 * cm - (1.2 * cm + 10 * 0.8 * cm)
    tabella_width = stripe_width
    header_height = 1.2 * cm
    riga_height = 0.8 * cm
    
    # Calcola larghezza delle colonne
    descrizione_width = tabella_width * 0.75
    unita_quantita_width = tabella_width * 0.125
    
    # Disegna l'header della tabella
    c.setFillColor(black)
    c.rect(tabella_x, tabella_y + (10 * riga_height), tabella_width, header_height, fill=0, stroke=1)
    
    # Linee verticali per dividere l'header
    c.line(tabella_x + descrizione_width, tabella_y + (10 * riga_height), 
           tabella_x + descrizione_width, tabella_y + (10 * riga_height) + header_height)
    c.line(tabella_x + descrizione_width + unita_quantita_width, tabella_y + (10 * riga_height), 
           tabella_x + descrizione_width + unita_quantita_width, tabella_y + (10 * riga_height) + header_height)
    
    # Testo header della tabella
    c.setFont("Times-Bold", 10)
    
    # Colonna 1: DESCRIZIONE DEI BENI
    text1 = "DESCRIZIONE DEI BENI"
    text1_width = c.stringWidth(text1, "Times-Bold", 10)
    text1_x = tabella_x + (descrizione_width - text1_width) / 2
    text1_y = tabella_y + (10 * riga_height) + (header_height - 10) / 2
    c.drawString(text1_x, text1_y, text1)
    
    # Colonna 2: U.M.
    text2 = "U.M."
    text2_width = c.stringWidth(text2, "Times-Bold", 10)
    text2_x = tabella_x + descrizione_width + (unita_quantita_width - text2_width) / 2
    text2_y = tabella_y + (10 * riga_height) + (header_height - 10) / 2
    c.drawString(text2_x, text2_y, text2)
    
    # Colonna 3: QUANTITÀ
    text3 = "QUANTITÀ"
    text3_width = c.stringWidth(text3, "Times-Bold", 10)
    text3_x = tabella_x + descrizione_width + unita_quantita_width + (unita_quantita_width - text3_width) / 2
    text3_y = tabella_y + (10 * riga_height) + (header_height - 10) / 2
    c.drawString(text3_x, text3_y, text3)
    
    # Disegna le righe della tabella
    for i in range(10):
        riga_y = tabella_y + (i * riga_height)
        c.rect(tabella_x, riga_y, tabella_width, riga_height, fill=0, stroke=1)
        
        # Linee verticali per dividere ogni riga
        c.line(tabella_x + descrizione_width, riga_y, tabella_x + descrizione_width, riga_y + riga_height)
        c.line(tabella_x + descrizione_width + unita_quantita_width, riga_y, tabella_x + descrizione_width + unita_quantita_width, riga_y + riga_height)
        
        # Inserisci i dati delle righe del DDT
        if i < len(ddt.righe.all()):
            riga = ddt.righe.all()[i]
            c.setFont("Times-Roman", 8)
            
            # Descrizione
            descrizione = f"{riga.articolo.nome}"
            if riga.descrizione:
                descrizione += f" - {riga.descrizione}"
            c.drawString(tabella_x + 2, riga_y + 2, descrizione[:60])  # Tronca se troppo lungo
            
            # Unità di misura
            c.drawString(tabella_x + descrizione_width + 2, riga_y + 2, riga.articolo.um)
            
            # Quantità
            c.drawString(tabella_x + descrizione_width + unita_quantita_width + 2, riga_y + 2, str(riga.quantita))
    
    # Footer con caselle per trasporto, data ritiro e vettore
    casella1_y = tabella_y - 0.1 * cm - 1.8 * cm
    casella1_x = tabella_x
    casella1_width = (tabella_width / 3) - 0.3 * cm
    casella1_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella1_x, casella1_y, casella1_width, casella1_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label1_text = "TRASPORTO A MEZZO"
    label1_x = casella1_x + 5
    label1_y = casella1_y + casella1_height - 15
    c.drawString(label1_x, label1_y, label1_text)
    
    c.setFont("Times-Roman", 10)
    c.drawString(casella1_x + 5, casella1_y + 5, ddt.trasporto_mezzo)
    
    # Seconda casella del footer - DATA RITIRO
    casella2_y = casella1_y
    casella2_x = casella1_x + casella1_width
    casella2_width = (tabella_width / 3) - 0.3 * cm
    casella2_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella2_x, casella2_y, casella2_width, casella2_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label2_text = "DATA RITIRO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 15
    c.drawString(label2_x, label2_y, label2_text)
    
    c.setFont("Times-Roman", 10)
    c.drawString(casella2_x + 5, casella2_y + 5, ddt.data_ritiro.strftime('%d/%m/%Y'))
    
    # Terza casella del footer - VETTORE
    casella3_y = tabella_y - 0.1 * cm - 4 * cm
    casella3_x = casella2_x + casella2_width
    casella3_width = tabella_width - casella1_width - casella2_width
    casella3_height = 4 * cm
    
    c.setFillColor(black)
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label3_text = "VETTORE:"
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 15
    c.drawString(label3_x, label3_y, label3_text)
    
    # Inserisci i dati del vettore
    c.setFont("Times-Roman", 9)
    vettore_data = [
        ddt.vettore.nome,
        f"Autista: {ddt.vettore.autista}",
        f"Patente: {ddt.vettore.patente}",
        f"Targa: {ddt.vettore.targa}",
        f"Tel: {ddt.vettore.telefono}",
        f"Email: {ddt.vettore.email}"
    ]
    
    y_offset = label3_y - 20
    for line in vettore_data:
        if y_offset > casella3_y + 10:
            c.drawString(casella3_x + 5, y_offset, line[:40])
            y_offset -= 12
    
    # Quarta casella del footer - ANNOTAZIONI
    casella4_y = casella3_y
    casella4_x = casella1_x
    casella4_width = casella1_width + casella2_width
    casella4_height = casella3_height - 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella4_x, casella4_y, casella4_width, casella4_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    label4_text = "ANNOTAZIONI"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 15
    c.drawString(label4_x, label4_y, label4_text)
    
    c.setFont("Times-Roman", 9)
    if ddt.annotazioni:
        # Dividi le annotazioni in righe
        annotazioni_lines = ddt.annotazioni.split('\n')
        y_offset = label4_y - 20
        for line in annotazioni_lines:
            if y_offset > casella4_y + 10:
                c.drawString(casella4_x + 5, y_offset, line[:50])
                y_offset -= 12
    
    # Tre caselle per le firme
    firme_y = casella4_y - 2 * cm
    firme_height = 2 * cm
    firme_width = tabella_width / 3
    
    # Prima firma - FIRMA MITTENTE
    firma1_x = tabella_x
    firma1_y = firme_y
    firma1_width = firme_width
    firma1_height = firme_height
    
    c.setFillColor(black)
    c.rect(firma1_x, firma1_y, firma1_width, firma1_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    firma1_text = "FIRMA MITTENTE"
    firma1_text_x = firma1_x + 5
    firma1_text_y = firma1_y + firma1_height - 15
    c.drawString(firma1_text_x, firma1_text_y, firma1_text)
    
    # Seconda firma - FIRMA VETTORE
    firma2_x = firma1_x + firma1_width
    firma2_y = firme_y
    firma2_width = firme_width
    firma2_height = firme_height
    
    c.setFillColor(black)
    c.rect(firma2_x, firma2_y, firma2_width, firma2_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    firma2_text = "FIRMA VETTORE"
    firma2_text_x = firma2_x + 5
    firma2_text_y = firma2_y + firma2_height - 15
    c.drawString(firma2_text_x, firma2_text_y, firma2_text)
    
    # Terza firma - FIRMA DESTINATARIO
    firma3_x = firma2_x + firma2_width
    firma3_y = firme_y
    firma3_width = firme_width
    firma3_height = firme_height
    
    c.setFillColor(black)
    c.rect(firma3_x, firma3_y, firma3_width, firma3_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    firma3_text = "FIRMA DESTINATARIO"
    firma3_text_x = firma3_x + 5
    firma3_text_y = firma3_y + firma3_height - 15
    c.drawString(firma3_text_x, firma3_text_y, firma3_text)
    
    c.save()
    
    return pdf_path

