#!/usr/bin/env python
"""
Script per configurare dati di esempio per l'applicazione DDT
Versione ottimizzata per installazione offline
"""

import os
import sys
import django

# Aggiungi il percorso del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ddt_project.settings_offline')
django.setup()

from ddt_app.models import (
    Mittente, SedeMittente, Destinatario, Destinazione, 
    Vettore, TargaVettore, CausaleTrasporto, FormatoNumerazioneDDT
)

def create_sample_data():
    """Crea dati di esempio per l'applicazione"""
    
    print("Creazione dati di esempio per installazione offline...")
    
    # 1. Mittente
    mittente, created = Mittente.objects.get_or_create(
        ragione_sociale="Azienda Agricola BB&F",
        defaults={
            'partita_iva': 'IT12345678901',
            'codice_fiscale': 'BBF12345678901',
            'indirizzo': 'Via delle Rose, 123',
            'cap': '00100',
            'citta': 'Roma',
            'provincia': 'RM',
            'telefono': '+39 06 1234567',
            'email': 'info@bbfagricola.it'
        }
    )
    if created:
        print(f"✅ Mittente creato: {mittente.ragione_sociale}")
    else:
        print(f"ℹ️  Mittente esistente: {mittente.ragione_sociale}")
    
    # 2. Sede Mittente
    sede_mittente, created = SedeMittente.objects.get_or_create(
        mittente=mittente,
        nome_sede="Sede Principale",
        defaults={
            'indirizzo': 'Via delle Rose, 123',
            'cap': '00100',
            'citta': 'Roma',
            'provincia': 'RM',
            'telefono': '+39 06 1234567',
            'email': 'sede@bbfagricola.it'
        }
    )
    if created:
        print(f"✅ Sede mittente creata: {sede_mittente.nome_sede}")
    else:
        print(f"ℹ️  Sede mittente esistente: {sede_mittente.nome_sede}")
    
    # 3. Destinatari
    destinatari_data = [
        {
            'ragione_sociale': 'Supermercato ABC',
            'partita_iva': 'IT98765432109',
            'codice_fiscale': 'ABC98765432109',
            'indirizzo': 'Via del Commercio, 456',
            'cap': '20100',
            'citta': 'Milano',
            'provincia': 'MI',
            'telefono': '+39 02 9876543',
            'email': 'ordini@supermercatoabc.it'
        },
        {
            'ragione_sociale': 'Ristorante La Bella Vista',
            'partita_iva': 'IT11223344556',
            'codice_fiscale': 'LBV11223344556',
            'indirizzo': 'Piazza del Gusto, 789',
            'cap': '50100',
            'citta': 'Firenze',
            'provincia': 'FI',
            'telefono': '+39 055 1122334',
            'email': 'info@labellavista.it'
        },
        {
            'ragione_sociale': 'Mercato Rionale Centrale',
            'partita_iva': 'IT55667788990',
            'codice_fiscale': 'MRC55667788990',
            'indirizzo': 'Piazza del Mercato, 1',
            'cap': '40100',
            'citta': 'Bologna',
            'provincia': 'BO',
            'telefono': '+39 051 5566778',
            'email': 'info@mercatocentrale.it'
        }
    ]
    
    for data in destinatari_data:
        destinatario, created = Destinatario.objects.get_or_create(
            ragione_sociale=data['ragione_sociale'],
            defaults=data
        )
        if created:
            print(f"✅ Destinatario creato: {destinatario.ragione_sociale}")
        else:
            print(f"ℹ️  Destinatario esistente: {destinatario.ragione_sociale}")
    
    # 4. Destinazioni
    destinazioni_data = [
        {
            'nome': 'Magazzino Centrale',
            'indirizzo': 'Via del Magazzino, 100',
            'cap': '20100',
            'citta': 'Milano',
            'provincia': 'MI',
            'telefono': '+39 02 1111111',
            'email': 'magazzino@supermercatoabc.it'
        },
        {
            'nome': 'Cucina Principale',
            'indirizzo': 'Piazza del Gusto, 789',
            'cap': '50100',
            'citta': 'Firenze',
            'provincia': 'FI',
            'telefono': '+39 055 2222222',
            'email': 'cucina@labellavista.it'
        },
        {
            'nome': 'Banco Vendita',
            'indirizzo': 'Piazza del Mercato, 1',
            'cap': '40100',
            'citta': 'Bologna',
            'provincia': 'BO',
            'telefono': '+39 051 3333333',
            'email': 'vendita@mercatocentrale.it'
        }
    ]
    
    for data in destinazioni_data:
        destinazione, created = Destinazione.objects.get_or_create(
            nome=data['nome'],
            defaults=data
        )
        if created:
            print(f"✅ Destinazione creata: {destinazione.nome}")
        else:
            print(f"ℹ️  Destinazione esistente: {destinazione.nome}")
    
    # 5. Vettori
    vettori_data = [
        {
            'ragione_sociale': 'Trasporti Veloci SRL',
            'partita_iva': 'IT99887766554',
            'codice_fiscale': 'TVR99887766554',
            'indirizzo': 'Via dei Trasporti, 200',
            'cap': '00100',
            'citta': 'Roma',
            'provincia': 'RM',
            'telefono': '+39 06 9988776',
            'email': 'info@trasportiveloci.it'
        },
        {
            'ragione_sociale': 'Logistica Express',
            'partita_iva': 'IT55443322110',
            'codice_fiscale': 'LEX55443322110',
            'indirizzo': 'Via della Logistica, 300',
            'cap': '20100',
            'citta': 'Milano',
            'provincia': 'MI',
            'telefono': '+39 02 5544332',
            'email': 'info@logisticaexpress.it'
        },
        {
            'ragione_sociale': 'Trasporti Locali',
            'partita_iva': 'IT11223344556',
            'codice_fiscale': 'TLR11223344556',
            'indirizzo': 'Via Locale, 400',
            'cap': '50100',
            'citta': 'Firenze',
            'provincia': 'FI',
            'telefono': '+39 055 1122334',
            'email': 'info@trasportilocali.it'
        }
    ]
    
    for data in vettori_data:
        vettore, created = Vettore.objects.get_or_create(
            ragione_sociale=data['ragione_sociale'],
            defaults=data
        )
        if created:
            print(f"✅ Vettore creato: {vettore.ragione_sociale}")
        else:
            print(f"ℹ️  Vettore esistente: {vettore.ragione_sociale}")
    
    # 6. Targhe Vettore
    targhe_data = [
        {'targa': 'AB123CD', 'vettore': vettori_data[0]['ragione_sociale']},
        {'targa': 'EF456GH', 'vettore': vettori_data[0]['ragione_sociale']},
        {'targa': 'IJ789KL', 'vettore': vettori_data[1]['ragione_sociale']},
        {'targa': 'MN012OP', 'vettore': vettori_data[1]['ragione_sociale']},
        {'targa': 'QR345ST', 'vettore': vettori_data[2]['ragione_sociale']},
        {'targa': 'UV678WX', 'vettore': vettori_data[2]['ragione_sociale']},
    ]
    
    for data in targhe_data:
        vettore = Vettore.objects.get(ragione_sociale=data['vettore'])
        targa, created = TargaVettore.objects.get_or_create(
            targa=data['targa'],
            vettore=vettore
        )
        if created:
            print(f"✅ Targa creata: {targa.targa}")
        else:
            print(f"ℹ️  Targa esistente: {targa.targa}")
    
    # 7. Causalie Trasporto
    causali_data = [
        {'codice': 'VEN', 'descrizione': 'Vendita'},
        {'codice': 'RES', 'descrizione': 'Reso'},
        {'codice': 'CAM', 'descrizione': 'Cambio merce'},
        {'codice': 'OMG', 'descrizione': 'Omaggio'},
        {'codice': 'RIP', 'descrizione': 'Riparazione'},
        {'codice': 'DEP', 'descrizione': 'Deposito'},
        {'codice': 'TRA', 'descrizione': 'Trasferimento'},
        {'codice': 'ALT', 'descrizione': 'Altro'},
    ]
    
    for data in causali_data:
        causale, created = CausaleTrasporto.objects.get_or_create(
            codice=data['codice'],
            defaults={'descrizione': data['descrizione']}
        )
        if created:
            print(f"✅ Causale creata: {causale.codice} - {causale.descrizione}")
        else:
            print(f"ℹ️  Causale esistente: {causale.codice} - {causale.descrizione}")
    
    # 8. Formato Numerazione DDT
    formato, created = FormatoNumerazioneDDT.objects.get_or_create(
        nome="Formato Standard",
        defaults={
            'prefisso': 'DDT',
            'suffisso': '',
            'numero_iniziale': 1,
            'lunghezza_numero': 6,
            'formato_completo': 'DDT-{numero:06d}',
            'attivo': True
        }
    )
    if created:
        print(f"✅ Formato numerazione creato: {formato.nome}")
    else:
        print(f"ℹ️  Formato numerazione esistente: {formato.nome}")
    
    print("\n" + "="*50)
    print("✅ DATI DI ESEMPIO CREATI CON SUCCESSO!")
    print("="*50)
    print("\nOra puoi:")
    print("1. Avviare l'applicazione con start_ddt.bat")
    print("2. Accedere all'admin Django per gestire i dati")
    print("3. Creare i tuoi primi DDT")
    print("\nBuon lavoro! 🚀")

if __name__ == '__main__':
    create_sample_data()
