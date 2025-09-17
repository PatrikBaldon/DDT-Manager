# DDT Manager - Applicazione Electron

Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F - Versione Desktop

## 🚀 Caratteristiche

- **Interfaccia Desktop Nativa**: Applicazione Electron con interfaccia moderna e responsiva
- **Gestione Completa DDT**: Creazione, modifica, visualizzazione e stampa di Documenti di Trasporto
- **Database Integrato**: SQLite per la gestione dei dati
- **Stampa PDF**: Generazione automatica di PDF per i DDT
- **Multi-piattaforma**: Supporto per Windows, macOS e Linux

## 📋 Prerequisiti

### Sistema Operativo
- Windows 10/11 (x64)
- macOS 10.14+ (Intel/Apple Silicon)
- Linux (Ubuntu 18.04+, Debian 10+, etc.)

### Software Richiesto
- **Node.js** 16.0+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://python.org/))
- **Git** (opzionale, per clonare il repository)

## 🛠️ Installazione

### 1. Clona il Repository
```bash
git clone <repository-url>
cd DDT
```

### 2. Installa Dipendenze Python
```bash
pip install -r requirements.txt
```

### 3. Installa Dipendenze Node.js
```bash
npm install
```

### 4. Configura il Database
```bash
python manage.py migrate
python manage.py loaddata initial_data.json  # Se disponibile
```

## 🚀 Avvio dell'Applicazione

### Modalità Sviluppo
```bash
# Linux/macOS
./scripts/start-electron.sh

# Windows
scripts\start-electron.bat

# Oppure direttamente
npm run electron-dev
```

### Modalità Produzione
```bash
# Costruisci l'applicazione
npm run build

# Avvia l'applicazione costruita
npm run electron
```

## 📦 Build e Distribuzione

### Build per Tutte le Piattaforme
```bash
npm run build
```

### Build Specifica per Piattaforma
```bash
# Windows
npm run build-win

# macOS
npm run build-mac

# Linux
npm run build-linux
```

I file di distribuzione saranno creati nella directory `dist/`.

## 🎯 Funzionalità Principali

### Gestione DDT
- ✅ Creazione nuovi DDT
- ✅ Modifica DDT esistenti
- ✅ Visualizzazione dettagliata
- ✅ Eliminazione DDT
- ✅ Generazione PDF

### Gestione Anagrafiche
- ✅ Mittenti e Sedi
- ✅ Destinatari e Destinazioni
- ✅ Vettori e Targhe
- ✅ Causali di Trasporto

### Configurazione
- ✅ Formato numerazione DDT
- ✅ Impostazioni applicazione
- ✅ Backup e ripristino dati

## 🔧 Configurazione

### Impostazioni Applicazione
Le impostazioni sono salvate in:
- **Windows**: `%APPDATA%/ddt-electron-app/config.json`
- **macOS**: `~/Library/Application Support/ddt-electron-app/config.json`
- **Linux**: `~/.config/ddt-electron-app/config.json`

### Database
Il database SQLite è salvato nella directory dell'applicazione come `db.sqlite3`.

## 🐛 Risoluzione Problemi

### Errore "Django non trovato"
```bash
pip install -r requirements.txt
```

### Errore "Node.js non trovato"
Installa Node.js dalla [pagina ufficiale](https://nodejs.org/).

### Errore "Porta 8000 già in uso"
```bash
# Trova il processo che usa la porta 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Termina il processo
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### L'applicazione non si avvia
1. Controlla che tutte le dipendenze siano installate
2. Verifica che la porta 8000 sia libera
3. Controlla i log nella console per errori specifici

## 📁 Struttura Progetto

```
DDT/
├── electron/                 # Codice Electron
│   ├── main.js              # Processo principale
│   └── preload.js           # Script di preload
├── static/                  # File statici
├── templates/               # Template Django
├── ddt_app/                 # App Django principale
├── ddt_project/             # Configurazione Django
├── scripts/                 # Script di utilità
├── package.json             # Configurazione Node.js
└── electron-builder.json    # Configurazione build
```

## 🔄 Aggiornamenti

L'applicazione supporta aggiornamenti automatici in modalità produzione. Gli aggiornamenti vengono controllati automaticamente all'avvio.

## 📞 Supporto

Per problemi o domande:
- Controlla la sezione "Risoluzione Problemi"
- Verifica i log dell'applicazione
- Contatta il supporto tecnico

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

---

**DDT Manager** - Sviluppato per Azienda Agricola BB&F
