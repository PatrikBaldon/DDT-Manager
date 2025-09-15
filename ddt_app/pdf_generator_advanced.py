#!/usr/bin/env python3
"""
Generatore PDF avanzato per DDT con supporto per note centrali e numerazione automatica
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white, Color
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from .models import DDT, DDTRiga
import os


def create_ddt_pdf(ddt_id, output_path=None):
    """
    Crea un PDF DDT completo con tutti i dati
    
    Args:
        ddt_id (int): ID del DDT da generare
        output_path (str, optional): Percorso di output. Default: auto-generato
    
    Returns:
        str: Percorso del file PDF generato
    """
    try:
        ddt = DDT.objects.get(id=ddt_id)
    except DDT.DoesNotExist:
        raise ValueError(f"DDT con ID {ddt_id} non trovato")
    
    if not output_path:
        output_path = f"ddt_{ddt.numero.replace('/', '_')}.pdf"
    
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
    
    # Crea il PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # Disegna l'header
    _draw_header(c, ddt, page_width, page_height, margin_top, margin_left, usable_width)
    
    # Disegna le caselle principali
    _draw_main_boxes(c, ddt, page_width, page_height, margin_top, margin_left, usable_width)
    
    # Disegna la tabella prodotti
    _draw_products_table(c, ddt, page_width, page_height, margin_top, margin_left, usable_width)
    
    # Disegna il footer
    _draw_footer(c, ddt, page_width, page_height, margin_top, margin_left, usable_width)
    
    c.save()
    
    return output_path


def _draw_header(c, ddt, page_width, page_height, margin_top, margin_left, usable_width):
    """Disegna l'header del DDT"""
    # Striscia grigia scura
    stripe_height = 1.5 * cm
    stripe_x = margin_left
    stripe_y = page_height - margin_top - stripe_height
    stripe_width = usable_width
    
    # Colore grigio scuro quasi nero
    dark_grey = Color(0.2, 0.2, 0.2)
    
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


def _draw_main_boxes(c, ddt, page_width, page_height, margin_top, margin_left, usable_width):
    """Disegna le caselle principali del DDT"""
    stripe_height = 1.5 * cm
    stripe_y = page_height - margin_top - stripe_height
    
    # Casella mittente
    mittente_y = stripe_y - 1 * cm - 4.3 * cm
    mittente_x = margin_left
    mittente_width = (usable_width / 2) - 0.05 * cm
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
    
    # Inserisci il logo nell'angolo in alto a destra della casella MITTENTE
    _draw_logo(c, mittente_x, mittente_y, mittente_width, mittente_height)
    
    # Aggiungi dati mittente
    if ddt.sede_mittente:
        _draw_sede_mittente_data(c, ddt.sede_mittente, mittente_x + 5, mittente_y + 5, mittente_width - 10)
    elif ddt.mittente:
        _draw_entity_data(c, ddt.mittente, mittente_x + 5, mittente_y + 5, mittente_width - 10)
    
    # Casella causale di trasporto
    casella2_y = mittente_y - 0.1 * cm - 1.8 * cm
    casella2_x = margin_left
    casella2_width = mittente_width
    casella2_height = 1.8 * cm
    
    c.rect(casella2_x, casella2_y, casella2_width, casella2_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "CAUSALE DI TRASPORTO"
    c.setFont("Times-Bold", 10)
    label2_text = "CAUSALE DI TRASPORTO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 15
    c.drawString(label2_x, label2_y, label2_text)
    
    # Aggiungi causale
    if ddt.causale_trasporto:
        c.setFont("Times-Roman", 10)
        c.drawString(casella2_x + 5, casella2_y + 5, ddt.causale_trasporto)
    
    # Casella numero e data
    casella3_x = mittente_x + mittente_width + 0.1 * cm
    casella3_y = stripe_y - 1 * cm - 1.8 * cm
    casella3_width = (usable_width / 2) - 0.05 * cm
    casella3_height = 1.8 * cm
    
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "NUMERO E DATA DOCUMENTO"
    c.setFont("Times-Bold", 10)
    label3_text = "NUMERO E DATA DOCUMENTO"
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 15
    c.drawString(label3_x, label3_y, label3_text)
    
    # Aggiungi numero e data sulla stessa riga
    if ddt.numero:
        c.setFont("Times-Roman", 10)
        # Rimuovi il trattino dal numero DDT se presente
        numero_pulito = ddt.numero.lstrip('-')
        if ddt.data_documento:
            numero_data_text = f"DDT N° {numero_pulito} - Data: {ddt.data_documento.strftime('%d/%m/%Y')}"
        else:
            numero_data_text = f"DDT N° {numero_pulito}"
        c.drawString(casella3_x + 5, casella3_y + 8, numero_data_text)
    
    # Casella destinatario
    casella4_x = casella3_x
    casella4_y = casella3_y - 0.1 * cm - 4.3 * cm
    casella4_width = casella3_width
    casella4_height = 4.3 * cm
    
    c.rect(casella4_x, casella4_y, casella4_width, casella4_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "DESTINATARIO"
    c.setFont("Times-Bold", 10)
    label4_text = "DESTINATARIO"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 15
    c.drawString(label4_x, label4_y, label4_text)
    
    # Aggiungi dati destinatario
    if ddt.destinazione:
        _draw_destinazione_data(c, ddt.destinazione, casella4_x + 5, casella4_y + 5, casella4_width - 10)
    elif ddt.destinatario:
        _draw_entity_data(c, ddt.destinatario, casella4_x + 5, casella4_y + 5, casella4_width - 10)
    
    # Casella luogo di destinazione
    casella5_x = margin_left
    casella5_y = casella2_y - 0.1 * cm - 2.5 * cm
    casella5_width = usable_width
    casella5_height = 2.5 * cm
    
    c.rect(casella5_x, casella5_y, casella5_width, casella5_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "LUOGO DI DESTINAZIONE"
    c.setFont("Times-Bold", 10)
    label5_text = "LUOGO DI DESTINAZIONE"
    label5_x = casella5_x + 5
    label5_y = casella5_y + casella5_height - 15
    c.drawString(label5_x, label5_y, label5_text)
    
    # Aggiungi luogo di destinazione
    if ddt.luogo_destinazione:
        c.setFont("Times-Roman", 10)
        c.drawString(casella5_x + 5, casella5_y + 5, ddt.luogo_destinazione)


def _draw_products_table(c, ddt, page_width, page_height, margin_top, margin_left, usable_width):
    """Disegna la tabella prodotti con supporto per note centrali"""
    stripe_height = 1.5 * cm
    stripe_y = page_height - margin_top - stripe_height
    
    # Posizione tabella
    tabella_x = margin_left
    # Calcola la posizione dell'header della tabella
    header_y = stripe_y - 1 * cm - 4.3 * cm - 0.1 * cm - 1.8 * cm - 0.1 * cm - 2.5 * cm - 0.1 * cm - 1.2 * cm
    # Le righe iniziano sotto l'header
    tabella_y = header_y - 10 * 0.8 * cm
    tabella_width = usable_width
    header_height = 1.2 * cm
    riga_height = 0.8 * cm
    
    # Calcola larghezza delle colonne
    descrizione_width = tabella_width * 0.75
    unita_quantita_width = tabella_width * 0.125
    
    # Disegna l'header della tabella
    c.setFillColor(black)
    c.rect(tabella_x, header_y, tabella_width, header_height, fill=0, stroke=1)
    
    # Linee verticali per dividere l'header in 3 colonne
    c.line(tabella_x + descrizione_width, header_y, 
           tabella_x + descrizione_width, header_y + header_height)
    c.line(tabella_x + descrizione_width + unita_quantita_width, header_y, 
           tabella_x + descrizione_width + unita_quantita_width, header_y + header_height)
    
    # Aggiungi testo header della tabella
    c.setFont("Times-Bold", 10)
    
    # Colonna 1: DESCRIZIONE DEI BENI
    text1 = "DESCRIZIONE DEI BENI"
    text1_width = c.stringWidth(text1, "Times-Bold", 10)
    text1_x = tabella_x + (descrizione_width - text1_width) / 2
    text1_y = header_y + (header_height - 10) / 2
    c.drawString(text1_x, text1_y, text1)
    
    # Colonna 2: U.M.
    text2 = "U.M."
    text2_width = c.stringWidth(text2, "Times-Bold", 10)
    text2_x = tabella_x + descrizione_width + (unita_quantita_width - text2_width) / 2
    text2_y = header_y + (header_height - 10) / 2
    c.drawString(text2_x, text2_y, text2)
    
    # Colonna 3: QUANTITÀ
    text3 = "QUANTITÀ"
    text3_width = c.stringWidth(text3, "Times-Bold", 10)
    text3_x = tabella_x + descrizione_width + unita_quantita_width + (unita_quantita_width - text3_width) / 2
    text3_y = header_y + (header_height - 10) / 2
    c.drawString(text3_x, text3_y, text3)
    
    # Disegna le 10 righe della tabella
    for i in range(10):
        riga_y = tabella_y + (i * riga_height)
        c.rect(tabella_x, riga_y, tabella_width, riga_height, fill=0, stroke=1)
        
        # Linee verticali per dividere ogni riga in 3 colonne
        c.line(tabella_x + descrizione_width, riga_y, tabella_x + descrizione_width, riga_y + riga_height)
        c.line(tabella_x + descrizione_width + unita_quantita_width, riga_y, tabella_x + descrizione_width + unita_quantita_width, riga_y + riga_height)
    
    # Gestione note centrali o righe articoli
    if ddt.usa_note_centrali and ddt.note_centrali:
        # Disegna le note centrali
        _draw_central_notes(c, ddt.note_centrali, tabella_x, tabella_y, descrizione_width, riga_height)
    else:
        # Disegna le righe degli articoli
        _draw_article_rows(c, ddt, tabella_x, tabella_y, descrizione_width, unita_quantita_width, riga_height, header_y)


def _draw_central_notes(c, notes, tabella_x, tabella_y, descrizione_width, riga_height):
    """Disegna le note centrali nella tabella"""
    # Etichetta bianca con bordo nero spesso
    etichetta_width = 6 * cm
    etichetta_height = 4 * cm
    etichetta_x = tabella_x + (descrizione_width - etichetta_width) / 2
    etichetta_y = tabella_y + (2.7 * riga_height) - 0.3 * cm
    
    # Disegna l'etichetta bianca con bordo nero spesso
    c.setFillColor(white)
    c.setStrokeColor(black)
    c.setLineWidth(3)
    c.rect(etichetta_x, etichetta_y, etichetta_width, etichetta_height, fill=1, stroke=1)
    
    # Reset del colore e spessore
    c.setFillColor(black)
    c.setLineWidth(1)
    
    # Aggiungi il testo delle note
    c.setFont("Times-Roman", 12)
    
    # Dividi il testo in righe
    lines = notes.split('\n')
    y_offset = etichetta_y + etichetta_height - 15
    
    for line in lines[:6]:  # Massimo 6 righe
        if y_offset > etichetta_y + 10:
            c.drawString(etichetta_x + 10, y_offset, line[:50])  # Massimo 50 caratteri per riga
            y_offset -= 12


def _draw_article_rows(c, ddt, tabella_x, tabella_y, descrizione_width, unita_quantita_width, riga_height, header_y):
    """Disegna le righe degli articoli nella tabella"""
    c.setFont("Times-Roman", 10)
    
    for i, riga in enumerate(ddt.righe.all().order_by('ordine')[:10]):  # Massimo 10 righe, ordinate per ordine
        # Le righe sono posizionate sotto l'header della tabella, dall'alto verso il basso
        riga_y = header_y - ((i + 1) * riga_height)
        
        # Descrizione articolo
        descrizione = f"{riga.articolo.nome}"
        if riga.descrizione:
            descrizione += f" - {riga.descrizione}"
        
        # Tronca la descrizione se troppo lunga
        if len(descrizione) > 60:
            descrizione = descrizione[:57] + "..."
        
        c.drawString(tabella_x + 5, riga_y + 5, descrizione)
        
        # Unità di misura
        c.drawString(tabella_x + descrizione_width + 5, riga_y + 5, riga.articolo.um)
        
        # Quantità
        quantita_text = f"{riga.quantita}"
        c.drawString(tabella_x + descrizione_width + unita_quantita_width + 5, riga_y + 5, quantita_text)


def _draw_footer(c, ddt, page_width, page_height, margin_top, margin_left, usable_width):
    """Disegna il footer del DDT"""
    stripe_height = 1.5 * cm
    stripe_y = page_height - margin_top - stripe_height
    
    # Calcola posizione footer
    header_y = stripe_y - 1 * cm - 4.3 * cm - 0.1 * cm - 1.8 * cm - 0.1 * cm - 2.5 * cm - 0.1 * cm - 1.2 * cm
    tabella_y = header_y - 10 * 0.8 * cm
    footer_y = tabella_y - 0.1 * cm - 1.8 * cm
    
    # Prima casella - TRASPORTO A MEZZO
    casella1_x = margin_left
    casella1_y = footer_y
    casella1_width = (usable_width / 3) - 0.3 * cm
    casella1_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella1_x, casella1_y, casella1_width, casella1_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "TRASPORTO A MEZZO"
    c.setFont("Times-Bold", 10)
    label1_text = "TRASPORTO A MEZZO"
    label1_x = casella1_x + 5
    label1_y = casella1_y + casella1_height - 15
    c.drawString(label1_x, label1_y, label1_text)
    
    # Aggiungi mezzo di trasporto
    if ddt.trasporto_mezzo:
        c.setFont("Times-Roman", 10)
        c.drawString(casella1_x + 5, casella1_y + 5, ddt.trasporto_mezzo)
    
    # Seconda casella - DATA RITIRO
    casella2_x = casella1_x + casella1_width
    casella2_y = footer_y
    casella2_width = (usable_width / 3) - 0.3 * cm
    casella2_height = 1.8 * cm
    
    c.rect(casella2_x, casella2_y, casella2_width, casella2_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "DATA RITIRO"
    c.setFont("Times-Bold", 10)
    label2_text = "DATA RITIRO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 15
    c.drawString(label2_x, label2_y, label2_text)
    
    # Aggiungi data ritiro
    if ddt.data_ritiro:
        c.setFont("Times-Roman", 10)
        c.drawString(casella2_x + 5, casella2_y + 5, ddt.data_ritiro.strftime('%d/%m/%Y'))
    
    # Terza casella - VETTORE
    casella3_x = casella2_x + casella2_width
    casella3_y = footer_y - 2.2 * cm  # Più alta per contenere i dati del vettore
    casella3_width = usable_width - casella1_width - casella2_width
    casella3_height = 4 * cm
    
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    # Aggiungi etichetta dinamica per trasporto
    c.setFont("Times-Bold", 10)
    if ddt.trasporto_mezzo == 'vettore':
        label3_text = "VETTORE:"
    elif ddt.trasporto_mezzo == 'mittente':
        label3_text = "MITTENTE:"
    elif ddt.trasporto_mezzo == 'destinatario':
        label3_text = "DESTINATARIO:"
    else:
        label3_text = "TRASPORTO:"
    
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 15
    c.drawString(label3_x, label3_y, label3_text)
    
    # Aggiungi dati vettore/trasporto
    if ddt.trasporto_mezzo == 'vettore' and ddt.vettore:
        _draw_vettore_data(c, ddt.vettore, ddt.targa_vettore, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    elif ddt.trasporto_mezzo == 'mittente' and ddt.sede_mittente:
        _draw_sede_mittente_data(c, ddt.sede_mittente, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    elif ddt.trasporto_mezzo == 'destinatario' and ddt.destinazione:
        _draw_destinazione_data(c, ddt.destinazione, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    
    # Casella ANNOTAZIONI
    casella4_x = casella1_x
    casella4_y = casella3_y
    casella4_width = casella1_width + casella2_width
    casella4_height = casella3_height - 1.8 * cm
    
    c.rect(casella4_x, casella4_y, casella4_width, casella4_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "ANNOTAZIONI"
    c.setFont("Times-Bold", 10)
    label4_text = "ANNOTAZIONI"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 15
    c.drawString(label4_x, label4_y, label4_text)
    
    # Aggiungi annotazioni
    if ddt.annotazioni:
        c.setFont("Times-Roman", 10)
        lines = ddt.annotazioni.split('\n')
        y_offset = casella4_y + casella4_height - 25
        for line in lines[:8]:  # Massimo 8 righe
            if y_offset > casella4_y + 5:
                c.drawString(casella4_x + 5, y_offset, line[:60])  # Massimo 60 caratteri per riga
                y_offset -= 10
    
    # Caselle per le firme
    firme_y = casella4_y - 2 * cm
    firme_height = 2 * cm
    firme_width = usable_width / 3
    
    # Prima firma - FIRMA MITTENTE
    firma1_x = margin_left
    firma1_y = firme_y
    firma1_width = firme_width
    firma1_height = firme_height
    
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
    
    c.rect(firma3_x, firma3_y, firma3_width, firma3_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 10)
    firma3_text = "FIRMA DESTINATARIO"
    firma3_text_x = firma3_x + 5
    firma3_text_y = firma3_y + firma3_height - 15
    c.drawString(firma3_text_x, firma3_text_y, firma3_text)


def _draw_logo(c, x, y, width, height):
    """Disegna il logo nell'angolo in alto a destra"""
    try:
        # Carica il logo PNG
        img = ImageReader("logo1.png")
        
        # Dimensioni del logo
        logo_width = 2.5 * cm
        logo_height = 2.5 * cm
        
        # Posizione del logo nell'angolo in alto a destra
        logo_x = x + width - logo_width - 5
        logo_y = y + height - logo_height - 5
        
        # Disegna il logo
        c.drawImage(img, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
        
    except Exception as e:
        print(f"⚠️ Errore nel caricamento del logo: {e}")
        # Se c'è un errore, disegna un rettangolo placeholder
        logo_width = 2.5 * cm
        logo_height = 2.5 * cm
        logo_x = x + width - logo_width - 5
        logo_y = y + height - logo_height - 5
        c.setFillColor(Color(0.9, 0.9, 0.9))
        c.rect(logo_x, logo_y, logo_width, logo_height, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Times-Bold", 8)
        c.drawString(logo_x + 10, logo_y + logo_height/2, "LOGO")


def _draw_entity_data(c, entity, x, y, max_width):
    """Disegna i dati di un'entità (mittente, destinatario)"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4.3 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome
    if hasattr(entity, 'nome') and entity.nome:
        c.drawString(x, current_y, entity.nome)
        current_y -= line_height
    
    # Indirizzo
    if hasattr(entity, 'indirizzo') and entity.indirizzo:
        c.drawString(x, current_y, entity.indirizzo)
        current_y -= line_height
    
    # Città, CAP, Provincia
    if hasattr(entity, 'citta') and entity.citta:
        citta_text = f"{entity.citta}"
        if hasattr(entity, 'cap') and entity.cap:
            citta_text += f" ({entity.cap})"
        if hasattr(entity, 'provincia') and entity.provincia:
            citta_text += f" {entity.provincia}"
        c.drawString(x, current_y, citta_text)
        current_y -= line_height
    
    # P.IVA e CF
    if hasattr(entity, 'piva') and entity.piva:
        c.drawString(x, current_y, f"P.IVA: {entity.piva}")
        current_y -= line_height
    if hasattr(entity, 'cf') and entity.cf:
        c.drawString(x, current_y, f"CF: {entity.cf}")


def _draw_sede_mittente_data(c, sede, x, y, max_width):
    """Disegna i dati di una sede mittente con codice stalla"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4.3 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome azienda
    if sede.mittente and sede.mittente.nome:
        c.drawString(x, current_y, sede.mittente.nome)
        current_y -= line_height
    
    # Nome sede
    if sede.nome:
        c.drawString(x, current_y, sede.nome)
        current_y -= line_height
    
    # Indirizzo
    if sede.indirizzo:
        c.drawString(x, current_y, sede.indirizzo)
        current_y -= line_height
    
    # Città, CAP, Provincia
    citta_text = f"{sede.citta}"
    if sede.cap:
        citta_text += f" ({sede.cap})"
    if sede.provincia:
        citta_text += f" {sede.provincia}"
    c.drawString(x, current_y, citta_text)
    current_y -= line_height
    
    # Codice stalla
    if sede.codice_stalla:
        c.drawString(x, current_y, f"Codice Stalla: {sede.codice_stalla}")
        current_y -= line_height
    
    # P.IVA e CF
    if sede.mittente and sede.mittente.piva:
        c.drawString(x, current_y, f"P.IVA: {sede.mittente.piva}")
        current_y -= line_height
    if sede.mittente and sede.mittente.cf:
        c.drawString(x, current_y, f"CF: {sede.mittente.cf}")


def _draw_destinazione_data(c, destinazione, x, y, max_width):
    """Disegna i dati di una destinazione con codice stalla"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4.3 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome destinatario
    if destinazione.destinatario and destinazione.destinatario.nome:
        c.drawString(x, current_y, destinazione.destinatario.nome)
        current_y -= line_height
    
    # Nome destinazione
    if destinazione.nome:
        c.drawString(x, current_y, destinazione.nome)
        current_y -= line_height
    
    # Indirizzo
    if destinazione.indirizzo:
        c.drawString(x, current_y, destinazione.indirizzo)
        current_y -= line_height
    
    # Codice stalla
    if destinazione.codice_stalla:
        c.drawString(x, current_y, f"Codice Stalla: {destinazione.codice_stalla}")
        current_y -= line_height
    
    # P.IVA e CF del destinatario
    if destinazione.destinatario and destinazione.destinatario.piva:
        c.drawString(x, current_y, f"P.IVA: {destinazione.destinatario.piva}")
        current_y -= line_height
    if destinazione.destinatario and destinazione.destinatario.cf:
        c.drawString(x, current_y, f"CF: {destinazione.destinatario.cf}")


def _draw_vettore_data(c, vettore, targa_vettore, x, y, max_width):
    """Disegna i dati del vettore"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome azienda
    if vettore.nome:
        c.drawString(x, current_y, vettore.nome)
        current_y -= line_height
    
    # Autista
    if vettore.autista:
        c.drawString(x, current_y, f"Autista: {vettore.autista}")
        current_y -= line_height
    
    # Targa
    if targa_vettore and targa_vettore.targa:
        c.drawString(x, current_y, f"Targa: {targa_vettore.targa}")
        current_y -= line_height
    
    # Patente
    if vettore.patente:
        c.drawString(x, current_y, f"Patente: {vettore.patente}")
        current_y -= line_height
    
    # Licenza BDN
    if vettore.licenza_bdn:
        c.drawString(x, current_y, f"Licenza BDN: {vettore.licenza_bdn}")
        current_y -= line_height
    
    # Indirizzo
    if vettore.indirizzo:
        c.drawString(x, current_y, vettore.indirizzo)
        current_y -= line_height
    
    # Città, CAP, Provincia
    if vettore.citta:
        citta_text = f"{vettore.citta}"
        if vettore.cap:
            citta_text += f" ({vettore.cap})"
        if vettore.provincia:
            citta_text += f" {vettore.provincia}"
        c.drawString(x, current_y, citta_text)
