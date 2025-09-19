# 📚 Documentazione Completa del Progetto DDT Manager

## 🎯 Panoramica del Progetto

**DDT Manager** è un'applicazione Electron per la gestione dei Documenti di Trasporto (DDT) sviluppata per Azienda Agricola BB&F. L'applicazione combina un backend Django con un frontend Electron per fornire un'interfaccia desktop nativa su Windows, macOS e Linux.

---

## 📁 Struttura del Progetto

### 🏗️ File Principali

#### **App_details.md**
- **Funzione**: Documentazione dettagliata dell'applicazione
- **Contenuto**: Descrizione delle funzionalità, tecnologie utilizzate, requisiti di sistema
- **Scopo**: Guida per sviluppatori e utenti finali

#### **manage.py**
- **Funzione**: Script principale di Django per la gestione del progetto
- **Contenuto**: Configurazione Django, comandi di amministrazione
- **Scopo**: Punto di ingresso per tutti i comandi Django (migrate, runserver, etc.)

#### **requirements.txt**
- **Funzione**: Lista delle dipendenze Python
- **Contenuto**: Tutti i pacchetti Python necessari per il progetto
- **Scopo**: Gestione delle dipendenze per l'installazione

#### **package.json**
- **Funzione**: Configurazione Node.js e dipendenze Electron
- **Contenuto**: Scripts, dipendenze, configurazione electron-builder
- **Scopo**: Gestione delle dipendenze Node.js e build dell'applicazione

#### **electron-builder.json**
- **Funzione**: Configurazione per la build e distribuzione Electron
- **Contenuto**: Impostazioni per Windows (NSIS), macOS (DMG), Linux (AppImage)
- **Scopo**: Personalizzazione del processo di packaging per ogni piattaforma

---

### 🐍 Backend Django

#### **ddt_project/** - Configurazione Django Principale

##### **ddt_project/settings.py**
- **Funzione**: Configurazione principale di Django
- **Contenuto**: Database, middleware, app installate, configurazioni di sicurezza
- **Scopo**: Punto centrale per tutte le impostazioni Django

##### **ddt_project/urls.py**
- **Funzione**: URL routing principale
- **Contenuto**: Pattern URL per l'intera applicazione
- **Scopo**: Definisce come le richieste vengono indirizzate alle view

##### **ddt_project/wsgi.py**
- **Funzione**: Configurazione WSGI per il deployment
- **Contenuto**: Configurazione per server web in produzione
- **Scopo**: Interfaccia tra Django e server web

#### **config/settings/** - Configurazioni per Ambiente

##### **config/settings/base.py**
- **Funzione**: Configurazioni base condivise
- **Contenuto**: Impostazioni comuni a tutti gli ambienti
- **Scopo**: Evita duplicazione di codice tra ambienti

##### **config/settings/development.py**
- **Funzione**: Configurazioni per sviluppo
- **Contenuto**: Debug=True, database SQLite, logging dettagliato
- **Scopo**: Ambiente ottimizzato per lo sviluppo

##### **config/settings/production.py**
- **Funzione**: Configurazioni per produzione
- **Contenuto**: Debug=False, database sicuro, logging ottimizzato
- **Scopo**: Ambiente ottimizzato per la produzione

##### **config/settings/testing.py**
- **Funzione**: Configurazioni per test
- **Contenuto**: Database in memoria, configurazioni per test
- **Scopo**: Ambiente isolato per l'esecuzione dei test

#### **ddt_app/** - Applicazione Django Principale

##### **ddt_app/models.py**
- **Funzione**: Definizione dei modelli di dati
- **Contenuto**: Modelli per DDT, Mittente, Destinatario, Vettore, etc.
- **Scopo**: Struttura del database e logica di business

##### **ddt_app/views.py**
- **Funzione**: Logica di business e gestione richieste
- **Contenuto**: View per CRUD operations, generazione PDF, API
- **Scopo**: Controllo del flusso dell'applicazione

##### **ddt_app/urls.py**
- **Funzione**: Routing specifico dell'app
- **Contenuto**: Pattern URL per le funzionalità DDT
- **Scopo**: Definisce gli endpoint dell'applicazione

##### **ddt_app/forms.py**
- **Funzione**: Form Django per input utente
- **Contenuto**: Form per creazione/modifica DDT e entità correlate
- **Scopo**: Validazione e gestione input utente

##### **ddt_app/admin.py**
- **Funzione**: Interfaccia amministrativa Django
- **Contenuto**: Configurazione admin per gestione dati
- **Scopo**: Interfaccia per amministratori

##### **ddt_app/utils.py**
- **Funzione**: Funzioni di utilità
- **Contenuto**: Helper functions, validazioni, formattazione
- **Scopo**: Codice riutilizzabile per l'applicazione

##### **ddt_app/pdf_generator_advanced.py**
- **Funzione**: Generazione PDF avanzata
- **Contenuto**: Logica per creare PDF professionali dei DDT
- **Scopo**: Produzione di documenti stampabili

##### **ddt_app/management/commands/**
- **Funzione**: Comandi Django personalizzati
- **Contenuto**: 
  - `load_initial_data.py`: Caricamento dati iniziali
  - `setup_default_numbering.py`: Configurazione numerazione DDT
- **Scopo**: Automatizzazione di task amministrativi

##### **ddt_app/migrations/**
- **Funzione**: Migrazioni database
- **Contenuto**: File di migrazione per evoluzione schema database
- **Scopo**: Gestione versioni del database

---

### ⚡ Frontend Electron

#### **electron/launcher.js**
- **Funzione**: Punto di ingresso principale dell'applicazione Electron
- **Contenuto**: Inizializzazione app, configurazione, avvio AppManager
- **Scopo**: Bootstrap dell'applicazione Electron

#### **electron/main.js**
- **Funzione**: Processo principale Electron (deprecato)
- **Contenuto**: Configurazione base Electron
- **Scopo**: Sostituito da launcher.js e app-manager.js

#### **electron/app-manager.js**
- **Funzione**: Gestore principale dell'applicazione Electron
- **Contenuto**: 
  - Gestione finestra principale
  - Avvio server Django
  - Gestione eventi applicazione
  - Setup IPC handlers
- **Scopo**: Cuore dell'applicazione Electron

#### **electron/dependency-manager.js**
- **Funzione**: Rilevamento automatico dipendenze
- **Contenuto**: 
  - Rilevamento Python (Anaconda, Homebrew, standard)
  - Rilevamento Node.js
  - Verifica Django e npm
- **Scopo**: Assicura che tutte le dipendenze siano disponibili

#### **electron/config.js**
- **Funzione**: Configurazione generale dell'app
- **Contenuto**: Impostazioni app, server Django, finestra, menu
- **Scopo**: Configurazione centralizzata

#### **electron/development.js**
- **Funzione**: Configurazione per ambiente sviluppo
- **Contenuto**: Impostazioni specifiche per sviluppo
- **Scopo**: Ottimizzazione per debugging

#### **electron/production.js**
- **Funzione**: Configurazione per ambiente produzione
- **Contenuto**: Impostazioni ottimizzate per produzione
- **Scopo**: Performance e sicurezza in produzione

#### **electron/preload.js**
- **Funzione**: Script di preload per sicurezza
- **Contenuto**: Esposizione sicura di API Node.js al renderer
- **Scopo**: Sicurezza e isolamento del processo renderer

#### **electron/updater.js**
- **Funzione**: Sistema di aggiornamenti automatici
- **Contenuto**: Controllo e installazione aggiornamenti
- **Scopo**: Mantenere l'app aggiornata automaticamente

#### **electron/updater-config.js**
- **Funzione**: Configurazione updater
- **Contenuto**: Impostazioni per il sistema di aggiornamenti
- **Scopo**: Personalizzazione del comportamento updater

#### **electron/logger.js**
- **Funzione**: Sistema di logging avanzato
- **Contenuto**: Logging strutturato, rotazione file, livelli
- **Scopo**: Debugging e monitoraggio applicazione

#### **electron/backup.js**
- **Funzione**: Sistema di backup automatico
- **Contenuto**: Backup database, compressione, scheduling
- **Scopo**: Protezione dati utente

#### **electron/error-handler.js**
- **Funzione**: Gestione centralizzata errori
- **Contenuto**: Cattura errori, logging, notifiche utente
- **Scopo**: Esperienza utente robusta

#### **electron/performance-monitor.js**
- **Funzione**: Monitoraggio performance
- **Contenuto**: Metriche CPU, memoria, tempi risposta
- **Scopo**: Ottimizzazione e debugging performance

#### **electron/notifications.js**
- **Funzione**: Sistema notifiche desktop
- **Contenuto**: Notifiche native per Windows, macOS, Linux
- **Scopo**: Feedback utente e notifiche importanti

#### **electron/settings.js**
- **Funzione**: Gestione impostazioni utente
- **Contenuto**: Persistenza configurazioni, preferenze utente
- **Scopo**: Personalizzazione esperienza utente

#### **electron/installer.js**
- **Funzione**: Gestione installazione
- **Contenuto**: Logica per installazione e disinstallazione
- **Scopo**: Gestione ciclo di vita applicazione

#### **electron/build.js**
- **Funzione**: Script di build personalizzato
- **Contenuto**: Build multi-piattaforma, controlli prerequisiti
- **Scopo**: Automatizzazione processo di build

#### **electron/test.js**
- **Funzione**: Test configurazione
- **Contenuto**: Verifica configurazione build
- **Scopo**: Validazione setup prima del build

#### **electron/README.md**
- **Funzione**: Documentazione specifica Electron
- **Contenuto**: Guida per sviluppatori Electron
- **Scopo**: Documentazione tecnica per Electron

---

### 🎨 Frontend Web (Templates e Static)

#### **templates/** - Template HTML Django

##### **templates/base.html**
- **Funzione**: Template base per tutti i template
- **Contenuto**: Layout comune, CSS, JavaScript
- **Scopo**: Consistenza UI e DRY principle

##### **templates/ddt_app/** - Template Specifici
- **ddt_form.html**: Form per creazione/modifica DDT
- **ddt_detail.html**: Visualizzazione dettagli DDT
- **ddt_list.html**: Lista DDT con filtri
- **mittente_form.html**: Form gestione mittenti
- **destinatario_form.html**: Form gestione destinatari
- **vettore_form.html**: Form gestione vettori
- **home.html**: Dashboard principale
- **Altri template**: Form e liste per entità correlate

#### **static/** - File Statici

##### **static/css/**
- **style.css**: Stili principali dell'applicazione
- **liquid_glass.css**: Effetti glassmorphism per UI moderna

##### **static/js/**
- **main.js**: JavaScript principale per interattività UI

##### **static/images/**
- **logo1.png**: Logo aziendale
- **icons/**: Icone per diverse risoluzioni (192x192, 384x384, 512x512)

---

### 🚀 Scripts e Automazione

#### **scripts/** - Script di Automazione

##### **scripts/setup.sh**
- **Funzione**: Setup iniziale progetto
- **Contenuto**: Installazione dipendenze, configurazione ambiente
- **Scopo**: Automatizzazione setup per nuovi sviluppatori

##### **scripts/dev_mac.sh**
- **Funzione**: Avvio ambiente sviluppo su macOS
- **Contenuto**: Avvio Django + Electron in modalità sviluppo
- **Scopo**: Sviluppo locale ottimizzato

##### **scripts/start-electron.sh**
- **Funzione**: Avvio applicazione Electron
- **Contenuto**: Script per avviare Electron
- **Scopo**: Avvio semplificato dell'app

##### **scripts/start.bat**
- **Funzione**: Avvio su Windows
- **Contenuto**: Script batch per Windows
- **Scopo**: Compatibilità Windows

##### **scripts/sync_to_github.sh**
- **Funzione**: Sincronizzazione con GitHub
- **Contenuto**: Push automatico, gestione branch
- **Scopo**: Automatizzazione workflow Git

##### **scripts/update_from_github.sh**
- **Funzione**: Aggiornamento da GitHub
- **Contenuto**: Pull automatico, gestione conflitti
- **Scopo**: Sincronizzazione team

##### **scripts/create-release.sh**
- **Funzione**: Creazione release
- **Contenuto**: Build, tag, push release
- **Scopo**: Automatizzazione release

---

### 📦 Installer e Distribuzione

#### **installer/** - Script di Installazione

##### **installer/windows/**
- **install.bat**: Installer Windows
- **start_ddt.bat**: Avvio applicazione Windows

##### **installer/macos/**
- **install.sh**: Installer macOS

##### **installer/linux/**
- **install.sh**: Installer Linux

##### **installer/nsis/**
- **ddt-installer.nsi**: Script NSIS per installer Windows
- **installer.nsh**: Include personalizzato NSIS

#### **release-files/** - File di Distribuzione
- **README.md**: Documentazione release
- **File binari**: Installer per diverse piattaforme
- **DDT_Manager_Portable_Windows/**: Versione portatile Windows

---

### 🧪 Test e Qualità

#### **tests/** - Suite di Test

##### **tests/test_models.py**
- **Funzione**: Test modelli Django
- **Contenuto**: Test creazione, validazione, relazioni modelli
- **Scopo**: Verifica logica di business

##### **tests/test_views.py**
- **Funzione**: Test view Django
- **Contenuto**: Test endpoint, risposte HTTP, logica view
- **Scopo**: Verifica funzionalità API

##### **tests/test_forms.py**
- **Funzione**: Test form Django
- **Contenuto**: Test validazione, rendering form
- **Scopo**: Verifica input utente

##### **tests/test_pdf.py**
- **Funzione**: Test generazione PDF
- **Contenuto**: Test creazione, contenuto, formattazione PDF
- **Scopo**: Verifica output documenti

##### **tests/test_utils.py**
- **Funzione**: Test funzioni di utilità
- **Contenuto**: Test helper functions, validazioni
- **Scopo**: Verifica codice riutilizzabile

##### **tests/conftest.py**
- **Funzione**: Configurazione pytest
- **Contenuto**: Fixtures, setup test
- **Scopo**: Configurazione comune per tutti i test

---

### 🔧 Configurazione e Deployment

#### **.github/workflows/build.yml**
- **Funzione**: CI/CD GitHub Actions
- **Contenuto**: Build automatico, test, release
- **Scopo**: Automatizzazione build e distribuzione

#### **Makefile**
- **Funzione**: Automazione task comuni
- **Contenuto**: Comandi per build, test, deploy
- **Scopo**: Semplificazione workflow sviluppo

#### **env.example**
- **Funzione**: Template variabili ambiente
- **Contenuto**: Esempio configurazione environment
- **Scopo**: Guida per configurazione ambiente

#### **LICENSE**
- **Funzione**: Licenza del progetto
- **Contenuto**: Termini di licenza MIT
- **Scopo**: Definizione diritti d'uso

---

### 📊 Database e Logs

#### **db.sqlite3**
- **Funzione**: Database SQLite
- **Contenuto**: Dati applicazione, configurazioni
- **Scopo**: Persistenza dati utente

#### **logs/ddt.log**
- **Funzione**: File di log applicazione
- **Contenuto**: Log eventi, errori, debug
- **Scopo**: Debugging e monitoraggio

---

### 🗂️ File di Build e Distribuzione

#### **dist/**
- **Funzione**: Directory output build
- **Contenuto**: File binari per tutte le piattaforme
- **Scopo**: Distribuzione finale

#### **staticfiles/**
- **Funzione**: File statici raccolti
- **Contenuto**: CSS, JS, immagini ottimizzati
- **Scopo**: Servire file statici in produzione

#### **node_modules/**
- **Funzione**: Dipendenze Node.js
- **Contenuto**: Pacchetti npm installati
- **Scopo**: Dipendenze runtime Node.js

---

## 🔄 Flusso di Esecuzione

### 1. **Avvio Applicazione**
```
launcher.js → app-manager.js → dependency-manager.js → Django server
```

### 2. **Gestione Dati**
```
Django models → views → templates → Electron renderer
```

### 3. **Generazione PDF**
```
Django views → pdf_generator_advanced.py → file PDF
```

### 4. **Aggiornamenti**
```
updater.js → GitHub releases → download → install
```

---

## 🛠️ Tecnologie Utilizzate

- **Backend**: Django 4.x, Python 3.11+
- **Frontend**: Electron 28.x, HTML5, CSS3, JavaScript
- **Database**: SQLite (sviluppo), PostgreSQL (produzione)
- **PDF**: ReportLab, WeasyPrint
- **Build**: electron-builder, GitHub Actions
- **OS**: Windows, macOS, Linux

---

## 📝 Note per Sviluppatori

1. **Sviluppo**: Usa `scripts/dev_mac.sh` per avvio rapido
2. **Test**: Esegui `python manage.py test` per test suite
3. **Build**: Usa `npm run build` per build multi-piattaforma
4. **Deploy**: Push tag per triggerare GitHub Actions
5. **Debug**: Controlla `logs/ddt.log` per troubleshooting

---

*Documentazione generata automaticamente per DDT Manager v1.0.0*
*Sviluppato da Patrik Baldon per Azienda Agricola BB&F*
