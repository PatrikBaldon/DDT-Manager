# 🌱 DDT Manager - Sistema di Gestione Documenti di Trasporto

Un'applicazione completa per la gestione dei Documenti di Trasporto (DDT) sviluppata con Django e Electron, progettata specificamente per aziende agricole.

## ✨ Caratteristiche Principali

### 📱 Applicazione Desktop (Electron)
- **🚀 App Nativa**: Installabile su Windows, macOS e Linux
- **⚡ Performance Ottimizzate**: Interfaccia desktop fluida e responsiva
- **🔄 Aggiornamenti Automatici**: Sistema di aggiornamento integrato
- **💾 Installazione Offline**: Funziona senza connessione internet
- **🎨 UI Moderna**: Interfaccia con design "Liquid Glass" e animazioni

### 📄 Gestione DDT Completa
- **Creazione e Modifica**: Form intuitivi per la gestione completa dei DDT
- **Numerazione Automatica**: Sistema configurabile di numerazione progressiva
- **Due Modalità di Compilazione**:
  - **Righe Articoli**: Tabella dettagliata con prodotti, quantità e prezzi
  - **Note Centrali**: Campo di testo per descrizioni generali
- **Generazione PDF**: PDF professionali con layout ottimizzato
- **Ricerca e Filtri**: Sistema di ricerca avanzato per numero, mittente, destinatario

### 🏢 Gestione Entità Aziendali

#### Mittenti (Aziende di Origine)
- **Dati Aziendali**: Nome, P.IVA, Codice Fiscale, contatti
- **Sedi Multiple**: Gestione di più sedi per azienda
- **Codici Stalla**: Supporto per codici identificativi specifici
- **Sede Legale**: Distinzione tra sede legale e operative

#### Destinatari (Clienti)
- **Anagrafica Completa**: Dati fiscali e di contatto
- **Destinazioni Multiple**: Gestione di più destinazioni per cliente
- **Codici Stalla**: Tracciamento specifico per destinazioni zootecniche

#### Vettori (Trasportatori)
- **Dati Aziendali**: Informazioni complete dell'azienda di trasporto
- **Autisti**: Gestione dati conducenti e patenti
- **Licenze Speciali**: Supporto per licenze BDN per trasporto animali vivi
- **Targhe Veicoli**: Gestione di più veicoli per vettore
- **Tipi Veicolo**: Classificazione dei mezzi di trasporto

### 📋 Gestione Configurazioni
- **Causali di Trasporto**: Codici e descrizioni per tipologie di trasporto
- **Formato Numerazione**: Configurazione personalizzabile della numerazione DDT
- **Articoli/Prodotti**: Catalogo prodotti con categorie e prezzi

## 📄 Documento di Trasporto (DDT)

### Struttura del DDT
- **Intestazione**:
  - Numero DDT (numerazione automatica)
  - Data documento e data ritiro
  - Dati mittente e sede di partenza
  - Dati destinatario e destinazione
  - Causale di trasporto

- **Informazioni Trasporto**:
  - Vettore e autista
  - Targa veicolo
  - Mezzo di trasporto (mittente/vettore/destinatario)
  - Luogo di destinazione dettagliato

- **Sezione Prodotti** (due modalità):
  - **Modalità Righe**: Tabella con articoli, quantità, unità di misura, prezzi
  - **Modalità Note**: Campo di testo per descrizioni generali

- **Note e Annotazioni**: Campi per informazioni aggiuntive

### Generazione PDF
- **Layout Professionale**: Design ottimizzato per stampa
- **Formato A4**: Standard per documenti aziendali
- **Calcoli Automatici**: Totali quantità e valori
- **Personalizzazione**: Logo aziendale e intestazioni personalizzate

## 🖥️ PAGINE E FUNZIONALITÀ

### 🏠 Homepage
- **Lista DDT**: Visualizzazione paginata di tutti i documenti
- **Ricerca Avanzata**: Filtri per numero, mittente, destinatario
- **Azioni Rapide**: Visualizza, modifica, PDF, elimina
- **Statistiche**: Contatori e informazioni riassuntive

### 📝 Gestione DDT
- **Creazione DDT**: Form guidato con validazione completa
- **Modifica DDT**: Editor completo per documenti esistenti
- **Visualizzazione**: Dettaglio completo con tutti i dati
- **Eliminazione**: Conferma di sicurezza per cancellazioni

### 🏢 Gestione Entità

#### Mittenti
- **Lista Mittenti**: Visualizzazione e ricerca aziende
- **Dettaglio Mittente**: Informazioni complete e sedi associate
- **Gestione Sedi**: Aggiunta, modifica, eliminazione sedi
- **Validazione Dati**: Controlli su P.IVA, CAP, province

#### Destinatari
- **Lista Destinatari**: Catalogo clienti con ricerca
- **Dettaglio Destinatario**: Anagrafica completa
- **Gestione Destinazioni**: Multiple destinazioni per cliente
- **Codici Stalla**: Tracciamento specifico per settore zootecnico

#### Vettori
- **Lista Vettori**: Gestione aziende di trasporto
- **Dettaglio Vettore**: Informazioni complete e veicoli
- **Gestione Targhe**: Aggiunta e gestione veicoli
- **Licenze Speciali**: Supporto per autorizzazioni specifiche

### ⚙️ Configurazioni
- **Causali di Trasporto**: Gestione codici e descrizioni
- **Formato Numerazione**: Configurazione sistema numerazione
- **Amministrazione**: Accesso al pannello Django Admin

## 🔧 Tecnologie Utilizzate

### Backend
- **Django 4.x**: Framework web robusto e scalabile
- **SQLite**: Database leggero e portabile
- **ReportLab**: Generazione PDF professionali
- **Bootstrap 5**: Framework CSS responsive

### Frontend
- **Electron**: Applicazione desktop cross-platform
- **Liquid Glass Design**: UI moderna con effetti glassmorphism
- **jQuery**: Interattività e AJAX
- **Font Awesome**: Icone vettoriali

### Caratteristiche Tecniche
- **PWA Ready**: Funzionalità Progressive Web App
- **Offline First**: Lavora senza connessione internet
- **Auto-update**: Sistema di aggiornamento automatico
- **Multi-platform**: Windows, macOS, Linux
- **Responsive**: Adattabile a diverse dimensioni schermo

## 🎯 Obiettivo

Semplificare e digitalizzare la gestione dei documenti di trasporto per aziende agricole, fornendo uno strumento completo, intuitivo e professionale che sostituisca la gestione cartacea tradizionale.