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
from django.conf import settings
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
    
    # Aggiungi etichetta "MITTENTE" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label_text = "MITTENTE"
    label_x = mittente_x + 5
    label_y = mittente_y + mittente_height - 12
    c.drawString(label_x, label_y, label_text)
    
    # Inserisci il logo nell'angolo in alto a destra della casella MITTENTE
    _draw_logo(c, ddt, mittente_x, mittente_y, mittente_width, mittente_height)
    
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
    
    # Aggiungi etichetta "CAUSALE DI TRASPORTO" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label2_text = "CAUSALE DI TRASPORTO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 12
    c.drawString(label2_x, label2_y, label2_text)
    
    # Aggiungi causale
    if ddt.causale_trasporto:
        c.setFont("Times-Roman", 10)
        causale_text = f"{ddt.causale_trasporto.codice} - {ddt.causale_trasporto.descrizione}"
        c.drawString(casella2_x + 5, casella2_y + 5, causale_text)
    
    # Casella numero e data
    casella3_x = mittente_x + mittente_width + 0.1 * cm
    casella3_y = stripe_y - 1 * cm - 1.8 * cm
    casella3_width = (usable_width / 2) - 0.05 * cm
    casella3_height = 1.8 * cm
    
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "NUMERO E DATA DOCUMENTO" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label3_text = "NUMERO E DATA DOCUMENTO"
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 12
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
    
    # Aggiungi etichetta "DESTINATARIO" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label4_text = "DESTINATARIO"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 12
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
    
    # Aggiungi etichetta "LUOGO DI DESTINAZIONE" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label5_text = "LUOGO DI DESTINAZIONE"
    label5_x = casella5_x + 5
    label5_y = casella5_y + casella5_height - 12
    c.drawString(label5_x, label5_y, label5_text)
    
    # Aggiungi luogo di destinazione (gestisce più righe)
    if ddt.luogo_destinazione:
        c.setFont("Times-Roman", 10)
        
        # Dividi il testo in righe e rimuovi duplicati
        lines = ddt.luogo_destinazione.split('\n')
        unique_lines = []
        for line in lines:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.append(line)
        
        # Se non ci sono caratteri di nuova riga, prova a dividere per altri separatori
        if len(unique_lines) == 1 and ('Codice Stalla:' in unique_lines[0] or 'Via' in unique_lines[0]):
            # Prova a dividere per "Codice Stalla:" e "Via"
            text = unique_lines[0]
            parts = []
            
            # Dividi per "Codice Stalla:"
            if 'Codice Stalla:' in text:
                before_codice = text.split('Codice Stalla:')[0]
                after_codice = text.split('Codice Stalla:')[1]
                if before_codice.strip():
                    parts.append(before_codice.strip())
                if after_codice.strip():
                    # Dividi ulteriormente per "Via"
                    if 'Via' in after_codice:
                        codice_part = after_codice.split('Via')[0].strip()
                        via_part = 'Via' + after_codice.split('Via')[1]
                        if codice_part:
                            parts.append('Codice Stalla:' + codice_part)
                        if via_part.strip():
                            parts.append(via_part.strip())
                    else:
                        parts.append('Codice Stalla:' + after_codice.strip())
            else:
                # Dividi per "Via"
                if 'Via' in text:
                    before_via = text.split('Via')[0]
                    via_part = 'Via' + text.split('Via')[1]
                    if before_via.strip():
                        parts.append(before_via.strip())
                    if via_part.strip():
                        parts.append(via_part.strip())
                else:
                    parts.append(text)
            
            unique_lines = parts
        
        # Disegna ogni riga (stessa distanza del mittente, standardizzato)
        start_y = casella5_y + casella5_height - 40  # Stessa distanza del mittente
        current_y = start_y
        for line in unique_lines:
            # Standardizza il testo del luogo destinazione
            if 'Codice Stalla:' in line:
                # Gestisce il caso speciale del codice stalla
                parts = line.split('Codice Stalla:')
                if len(parts) == 2:
                    before = parts[0].strip().title()  # Prima parte con title case
                    after = parts[1].strip().upper()   # Codice stalla in maiuscolo
                    # Rimuovi spazio extra prima di "Codice Stalla:"
                    if before:
                        line = f"{before} Codice Stalla: {after}"
                    else:
                        line = f"Codice Stalla: {after}"
                else:
                    line = line.title()  # Fallback con title case
            else:
                line = line.title()  # Standardizza con title case
            c.drawString(casella5_x + 5, current_y, line)
            current_y -= 12  # Spaziatura tra le righe


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
    
    # Aggiungi testo header della tabella (titoli più piccoli)
    c.setFont("Times-Bold", 8)
    
    # Colonna 1: DESCRIZIONE DEI BENI
    text1 = "DESCRIZIONE DEI BENI"
    text1_width = c.stringWidth(text1, "Times-Bold", 8)
    text1_x = tabella_x + (descrizione_width - text1_width) / 2
    text1_y = header_y + (header_height - 8) / 2
    c.drawString(text1_x, text1_y, text1)
    
    # Colonna 2: U.M.
    text2 = "U.M."
    text2_width = c.stringWidth(text2, "Times-Bold", 8)
    text2_x = tabella_x + descrizione_width + (unita_quantita_width - text2_width) / 2
    text2_y = header_y + (header_height - 8) / 2
    c.drawString(text2_x, text2_y, text2)
    
    # Colonna 3: QUANTITÀ
    text3 = "QUANTITÀ"
    text3_width = c.stringWidth(text3, "Times-Bold", 8)
    text3_x = tabella_x + descrizione_width + unita_quantita_width + (unita_quantita_width - text3_width) / 2
    text3_y = header_y + (header_height - 8) / 2
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
            # Standardizza il testo delle note centrali
            line_standardized = line.title()  # Prima lettera maiuscola per ogni parola
            c.drawString(etichetta_x + 10, y_offset, line_standardized[:50])  # Massimo 50 caratteri per riga
            y_offset -= 12


def _draw_article_rows(c, ddt, tabella_x, tabella_y, descrizione_width, unita_quantita_width, riga_height, header_y):
    """Disegna le righe degli articoli nella tabella"""
    c.setFont("Times-Roman", 10)
    
    for i, riga in enumerate(ddt.righe.all().order_by('ordine')[:10]):  # Massimo 10 righe, ordinate per ordine
        # Le righe sono posizionate sotto l'header della tabella, dall'alto verso il basso
        riga_y = header_y - ((i + 1) * riga_height)
        
        # Descrizione articolo (standardizzata)
        descrizione = f"{riga.articolo.nome.title()}"  # Nome articolo standardizzato
        if riga.descrizione:
            descrizione += f" - {riga.descrizione.title()}"  # Descrizione standardizzata
        
        # Tronca la descrizione se troppo lunga
        if len(descrizione) > 60:
            descrizione = descrizione[:57] + "..."
        
        c.drawString(tabella_x + 5, riga_y + 5, descrizione)
        
        # Unità di misura (standardizzata)
        um_standardized = riga.articolo.um.upper()  # Unità di misura in maiuscolo
        c.drawString(tabella_x + descrizione_width + 5, riga_y + 5, um_standardized)
        
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
    
    # Prima casella - TRASPORTO A MEZZO (ridotta)
    casella1_x = margin_left
    casella1_y = footer_y
    casella1_width = (usable_width / 4) - 0.2 * cm  # Ridotta per dare spazio al vettore
    casella1_height = 1.8 * cm
    
    c.setFillColor(black)
    c.rect(casella1_x, casella1_y, casella1_width, casella1_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "TRASPORTO A MEZZO" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label1_text = "TRASPORTO A MEZZO"
    label1_x = casella1_x + 5
    label1_y = casella1_y + casella1_height - 12
    c.drawString(label1_x, label1_y, label1_text)
    
    # Aggiungi mezzo di trasporto (standardizzato)
    if ddt.trasporto_mezzo:
        c.setFont("Times-Roman", 10)
        # Standardizza il testo del mezzo di trasporto
        trasporto_text = ddt.trasporto_mezzo.title()  # Prima lettera maiuscola
        c.drawString(casella1_x + 5, casella1_y + 5, trasporto_text)
    
    # Seconda casella - DATA RITIRO (ridotta)
    casella2_x = casella1_x + casella1_width
    casella2_y = footer_y
    casella2_width = (usable_width / 4) - 0.2 * cm  # Ridotta per dare spazio al vettore
    casella2_height = 1.8 * cm
    
    c.rect(casella2_x, casella2_y, casella2_width, casella2_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "DATA RITIRO" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label2_text = "DATA RITIRO"
    label2_x = casella2_x + 5
    label2_y = casella2_y + casella2_height - 12
    c.drawString(label2_x, label2_y, label2_text)
    
    # Aggiungi data ritiro
    if ddt.data_ritiro:
        c.setFont("Times-Roman", 10)
        c.drawString(casella2_x + 5, casella2_y + 5, ddt.data_ritiro.strftime('%d/%m/%Y'))
    
    # Terza casella - VETTORE (aumentata)
    casella3_x = casella2_x + casella2_width
    casella3_y = footer_y - 2.2 * cm  # Più alta per contenere i dati del vettore
    casella3_width = usable_width - casella1_width - casella2_width  # Aumentata automaticamente
    casella3_height = 4 * cm
    
    c.rect(casella3_x, casella3_y, casella3_width, casella3_height, fill=0, stroke=1)
    
    # Aggiungi etichetta dinamica per trasporto (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    if ddt.trasporto_mezzo == 'vettore':
        label3_text = "VETTORE:"
    elif ddt.trasporto_mezzo == 'mittente':
        label3_text = "MITTENTE:"
    elif ddt.trasporto_mezzo == 'destinatario':
        label3_text = "DESTINATARIO:"
    else:
        label3_text = "TRASPORTO:"
    
    label3_x = casella3_x + 5
    label3_y = casella3_y + casella3_height - 12
    c.drawString(label3_x, label3_y, label3_text)
    
    # Aggiungi dati vettore/trasporto
    if ddt.trasporto_mezzo == 'vettore' and ddt.vettore:
        _draw_vettore_data(c, ddt.vettore, ddt.targa_vettore, ddt.targa_vettore_2, ddt.autista, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    elif ddt.trasporto_mezzo == 'mittente' and ddt.sede_mittente:
        _draw_sede_mittente_data(c, ddt.sede_mittente, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    elif ddt.trasporto_mezzo == 'destinatario' and ddt.destinazione:
        _draw_destinazione_data(c, ddt.destinazione, casella3_x + 5, casella3_y + 5, casella3_width - 10)
    
    # Casella ANNOTAZIONI (ridotta)
    casella4_x = casella1_x
    casella4_y = casella3_y
    casella4_width = casella1_width + casella2_width  # Ora più piccola (TRASPORTO + DATA RITIRO ridotta)
    casella4_height = casella3_height - 1.8 * cm
    
    c.rect(casella4_x, casella4_y, casella4_width, casella4_height, fill=0, stroke=1)
    
    # Aggiungi etichetta "ANNOTAZIONI" (titolo più piccolo)
    c.setFont("Times-Bold", 8)
    label4_text = "ANNOTAZIONI"
    label4_x = casella4_x + 5
    label4_y = casella4_y + casella4_height - 12
    c.drawString(label4_x, label4_y, label4_text)
    
    # Aggiungi annotazioni (standardizzato)
    if ddt.annotazioni:
        c.setFont("Times-Roman", 10)
        lines = ddt.annotazioni.split('\n')
        y_offset = casella4_y + casella4_height - 25
        for line in lines[:8]:  # Massimo 8 righe
            if y_offset > casella4_y + 5:
                # Standardizza il testo delle annotazioni
                line_standardized = line.title()  # Prima lettera maiuscola per ogni parola
                c.drawString(casella4_x + 5, y_offset, line_standardized[:60])  # Massimo 60 caratteri per riga
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
    
    c.setFont("Times-Bold", 8)
    firma1_text = "FIRMA MITTENTE"
    firma1_text_x = firma1_x + 5
    firma1_text_y = firma1_y + firma1_height - 12
    c.drawString(firma1_text_x, firma1_text_y, firma1_text)
    
    # Seconda firma - FIRMA VETTORE
    firma2_x = firma1_x + firma1_width
    firma2_y = firme_y
    firma2_width = firme_width
    firma2_height = firme_height
    
    c.rect(firma2_x, firma2_y, firma2_width, firma2_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 8)
    firma2_text = "FIRMA VETTORE"
    firma2_text_x = firma2_x + 5
    firma2_text_y = firma2_y + firma2_height - 12
    c.drawString(firma2_text_x, firma2_text_y, firma2_text)
    
    # Terza firma - FIRMA DESTINATARIO
    firma3_x = firma2_x + firma2_width
    firma3_y = firme_y
    firma3_width = firme_width
    firma3_height = firme_height
    
    c.rect(firma3_x, firma3_y, firma3_width, firma3_height, fill=0, stroke=1)
    
    c.setFont("Times-Bold", 8)
    firma3_text = "FIRMA DESTINATARIO"
    firma3_text_x = firma3_x + 5
    firma3_text_y = firma3_y + firma3_height - 12
    c.drawString(firma3_text_x, firma3_text_y, firma3_text)


def _draw_logo(c, ddt, x, y, width, height):
    """Disegna il logo nell'angolo in alto a destra"""
    logo_path = None
    
    # Cerca il logo personalizzato del mittente
    if ddt.sede_mittente and ddt.sede_mittente.mittente and ddt.sede_mittente.mittente.logo:
        logo_path = ddt.sede_mittente.mittente.logo.path
    elif ddt.mittente and ddt.mittente.logo:
        logo_path = ddt.mittente.logo.path
    
    # Se non c'è un logo personalizzato, usa quello di default
    if not logo_path:
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo1.png')
    
    try:
        # Carica il logo
        if os.path.exists(logo_path):
            img = ImageReader(logo_path)
        else:
            raise FileNotFoundError(f"Logo non trovato: {logo_path}")
        
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
    
    # Nome (standardizzato)
    if hasattr(entity, 'nome') and entity.nome:
        nome_text = entity.nome.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, nome_text)
        current_y -= line_height
    
    # Indirizzo (standardizzato)
    if hasattr(entity, 'indirizzo') and entity.indirizzo:
        indirizzo_text = entity.indirizzo.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, indirizzo_text)
        current_y -= line_height
    
    # Città, CAP, Provincia (standardizzato)
    if hasattr(entity, 'citta') and entity.citta:
        citta_text = entity.citta.title()  # Prima lettera maiuscola
        if hasattr(entity, 'cap') and entity.cap:
            citta_text += f" ({entity.cap})"
        if hasattr(entity, 'provincia') and entity.provincia:
            citta_text += f" {entity.provincia.upper()}"  # Provincia in maiuscolo
        c.drawString(x, current_y, citta_text)
        current_y -= line_height
    
    # P.IVA e CF (standardizzato)
    if hasattr(entity, 'piva') and entity.piva:
        c.drawString(x, current_y, f"P.IVA: {entity.piva.upper()}")  # P.IVA in maiuscolo
        current_y -= line_height
    if hasattr(entity, 'cf') and entity.cf:
        c.drawString(x, current_y, f"CF: {entity.cf.upper()}")  # CF in maiuscolo


def _draw_sede_mittente_data(c, sede, x, y, max_width):
    """Disegna i dati di una sede mittente con codice stalla"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4.3 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome società (standardizzato)
    if sede.mittente and sede.mittente.nome:
        nome_text = sede.mittente.nome.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, nome_text)
        current_y -= line_height
    
    # Indirizzo completo (standardizzato)
    if sede.indirizzo:
        indirizzo_text = sede.indirizzo.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, indirizzo_text)
        current_y -= line_height
    
    # Città, CAP, Provincia (standardizzato)
    citta_text = sede.citta.title()  # Prima lettera maiuscola
    if sede.cap:
        citta_text += f" ({sede.cap})"
    if sede.provincia:
        citta_text += f" {sede.provincia.upper()}"  # Provincia in maiuscolo
    c.drawString(x, current_y, citta_text)
    current_y -= line_height
    
    # P.IVA (standardizzato)
    if sede.mittente and sede.mittente.piva:
        c.drawString(x, current_y, f"P.IVA: {sede.mittente.piva.upper()}")  # P.IVA in maiuscolo
        current_y -= line_height
    
    # Codice stalla (standardizzato)
    if sede.codice_stalla:
        c.drawString(x, current_y, f"Codice Stalla: {sede.codice_stalla.upper()}")  # Codice stalla in maiuscolo
        current_y -= line_height


def _draw_destinazione_data(c, destinazione, x, y, max_width):
    """Disegna i dati di una destinazione con codice stalla"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4.3 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome destinatario (standardizzato)
    if destinazione.destinatario and destinazione.destinatario.nome:
        nome_text = destinazione.destinatario.nome.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, nome_text)
        current_y -= line_height
    
    # Indirizzo destinatario (standardizzato)
    if destinazione.destinatario and destinazione.destinatario.indirizzo:
        indirizzo_text = destinazione.destinatario.indirizzo.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, indirizzo_text)
        current_y -= line_height
    
    # CAP, Città, Provincia destinatario (standardizzato)
    if destinazione.destinatario:
        destinatario = destinazione.destinatario
        citta_text = ""
        if destinatario.citta:
            citta_text = destinatario.citta.title()  # Prima lettera maiuscola
        if destinatario.cap:
            citta_text += f" ({destinatario.cap})"
        if destinatario.provincia:
            citta_text += f" {destinatario.provincia.upper()}"  # Provincia in maiuscolo
        if citta_text:
            c.drawString(x, current_y, citta_text)
            current_y -= line_height
    
    # P.IVA destinatario (standardizzato)
    if destinazione.destinatario and destinazione.destinatario.piva:
        c.drawString(x, current_y, f"P.IVA: {destinazione.destinatario.piva.upper()}")  # P.IVA in maiuscolo
        current_y -= line_height
    
    # Codice stalla destinazione (standardizzato)
    if destinazione.codice_stalla:
        c.drawString(x, current_y, f"Codice Stalla: {destinazione.codice_stalla.upper()}")  # Codice stalla in maiuscolo
        current_y -= line_height


def _draw_vettore_data(c, vettore, targa_vettore, targa_vettore_2, autista, x, y, max_width):
    """Disegna i dati del vettore con autista e due targhe"""
    c.setFont("Times-Roman", 10)
    
    # Calcola l'altezza della casella e la posizione di partenza
    casella_height = 4 * cm
    line_height = 12  # Spaziatura tra le righe
    start_y = y + casella_height - 40  # Abbassato per evitare sovrapposizione con l'etichetta
    
    current_y = start_y
    
    # Nome azienda (standardizzato)
    if vettore.nome:
        nome_text = vettore.nome.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, nome_text)
        current_y -= line_height
    
    # Indirizzo (standardizzato)
    if vettore.indirizzo:
        indirizzo_text = vettore.indirizzo.title()  # Prima lettera maiuscola per ogni parola
        c.drawString(x, current_y, indirizzo_text)
        current_y -= line_height
    
    # Città, CAP, Provincia (standardizzato)
    if vettore.citta:
        citta_text = vettore.citta.title()  # Prima lettera maiuscola
        if vettore.cap:
            citta_text += f" ({vettore.cap})"
        if vettore.provincia:
            citta_text += f" {vettore.provincia.upper()}"  # Provincia in maiuscolo
        c.drawString(x, current_y, citta_text)
        current_y -= line_height
    
    # P.IVA (standardizzato)
    if vettore.piva:
        c.drawString(x, current_y, f"P.IVA: {vettore.piva.upper()}")  # P.IVA in maiuscolo
        current_y -= line_height
    
    # Licenza (standardizzato)
    if vettore.licenza_bdn:
        c.drawString(x, current_y, f"Licenza: {vettore.licenza_bdn.upper()}")  # Licenza in maiuscolo
        current_y -= line_height
    
    # Autista (standardizzato)
    if autista:
        nome_autista = f"{autista.nome.title()} {autista.cognome.title()}"  # Prima lettera maiuscola per nome e cognome
        c.drawString(x, current_y, f"Autista: {nome_autista}")
        current_y -= line_height
        if autista.patente:
            c.drawString(x, current_y, f"Patente: {autista.patente.upper()}")  # Patente in maiuscolo
            current_y -= line_height
    
    # Targhe sulla stessa riga (standardizzato)
    targhe_text = "Targhe: "
    targhe_list = []
    if targa_vettore and targa_vettore.targa:
        targhe_list.append(targa_vettore.targa.upper())  # Targa in maiuscolo
    if targa_vettore_2 and targa_vettore_2.targa:
        targhe_list.append(targa_vettore_2.targa.upper())  # Targa in maiuscolo
    
    if targhe_list:
        targhe_text += ", ".join(targhe_list)
        c.drawString(x, current_y, targhe_text)
        current_y -= line_height
