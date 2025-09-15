#!/usr/bin/env python3
"""
Utility per la gestione dei DDT
"""

from .models import FormatoNumerazioneDDT, DDT
from datetime import datetime


def genera_numero_ddt(anno=None, mese=None):
    """
    Genera il prossimo numero DDT secondo il formato configurato
    
    Args:
        anno (int, optional): Anno per la numerazione. Default: anno corrente
        mese (int, optional): Mese per la numerazione. Default: mese corrente
    
    Returns:
        str: Prossimo numero DDT
    """
    # Ottieni il formato attivo
    formato_config = FormatoNumerazioneDDT.objects.filter(attivo=True).first()
    
    if not formato_config:
        # Se non c'è configurazione, usa il formato predefinito
        formato_config = FormatoNumerazioneDDT.objects.create(
            formato='aaaa-num',
            numero_iniziale=1,
            lunghezza_numero=4,
            attivo=True
        )
    
    return formato_config.genera_numero(anno, mese)


def get_formato_numerazione_attivo():
    """
    Ottiene la configurazione del formato di numerazione attivo
    
    Returns:
        FormatoNumerazioneDDT: Configurazione attiva o None
    """
    return FormatoNumerazioneDDT.objects.filter(attivo=True).first()


def valida_numero_ddt(numero):
    """
    Valida se un numero DDT è valido secondo il formato configurato
    
    Args:
        numero (str): Numero DDT da validare
    
    Returns:
        bool: True se valido, False altrimenti
    """
    formato_config = get_formato_numerazione_attivo()
    if not formato_config:
        return True  # Se non c'è configurazione, accetta tutto
    
    # Controlla se il numero esiste già
    if DDT.objects.filter(numero=numero).exists():
        return False
    
    # Qui potresti aggiungere altre validazioni specifiche per formato
    return True


def get_prossimo_numero_ddt():
    """
    Ottiene il prossimo numero DDT disponibile
    
    Returns:
        str: Prossimo numero DDT
    """
    return genera_numero_ddt()


def reset_numerazione_ddt(formato_config):
    """
    Resetta la numerazione DDT per un formato specifico
    
    Args:
        formato_config (FormatoNumerazioneDDT): Configurazione del formato
    
    Returns:
        bool: True se reset completato con successo
    """
    try:
        # Disattiva tutte le configurazioni
        FormatoNumerazioneDDT.objects.update(attivo=False)
        
        # Attiva solo quella specificata
        formato_config.attivo = True
        formato_config.save()
        
        return True
    except Exception as e:
        print(f"Errore nel reset della numerazione: {e}")
        return False
