# DDT Manager - Applicazione Electron

Sistema di gestione Documenti di Trasporto per aziende agricole, sviluppato con Django e Electron.

## 🚀 Caratteristiche

- **Applicazione Desktop**: Interfaccia nativa per Windows, macOS e Linux
- **Gestione DDT Completa**: Creazione, modifica e visualizzazione documenti
- **Generazione PDF**: PDF professionali con layout ottimizzato
- **Backup Automatico**: Sistema di backup integrato per i dati
- **Aggiornamenti Automatici**: Controllo e installazione aggiornamenti
- **Monitoraggio Performance**: Tracciamento delle performance dell'applicazione
- **Gestione Errori**: Sistema avanzato di gestione e logging degli errori

## 📋 Prerequisiti

- **Python 3.8+**: Per il backend Django
- **Node.js 16+**: Per l'applicazione Electron
- **npm**: Gestore pacchetti Node.js

## 🛠️ Installazione

### Installazione Automatica

1. **Windows**:
   ```bash
   # Esegui l'installer NSIS
   DDT_Manager_Setup_1.1.0.exe
   ```

2. **macOS**:
   ```bash
   # Apri il file DMG
   open DDT_Manager-1.1.0.dmg
   # Trascina l'applicazione in Applications
   ```

3. **Linux**:
   ```bash
   # Rendi eseguibile l'AppImage
   chmod +x DDT_Manager-1.1.0.AppImage
   # Esegui l'applicazione
   ./DDT_Manager-1.1.0.AppImage
   ```

### Installazione Manuale

1. **Clona il repository**:
   ```bash
   git clone https://github.com/aziendaagricola/ddt-manager.git
   cd ddt-manager
   ```

2. **Installa dipendenze Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Installa dipendenze Node.js**:
   ```bash
   cd electron
   npm install
   ```

4. **Configura il database**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. **Avvia l'applicazione**:
   ```bash
   npm start
   ```

## 🔧 Configurazione

### Impostazioni Applicazione

L'applicazione salva le impostazioni in:
- **Windows**: `%APPDATA%/ddt-manager/`
- **macOS**: `~/Library/Application Support/ddt-manager/`
- **Linux**: `~/.config/ddt-manager/`

### Variabili d'Ambiente

- `NODE_ENV`: Ambiente di esecuzione (`development`, `production`)
- `DJANGO_HOST`: Host del server Django (default: `127.0.0.1`)
- `DJANGO_PORT`: Porta del server Django (default: `8000`)

## 📱 Utilizzo

### Avvio dell'Applicazione

1. **Windows**: Doppio click su "DDT Manager" sul desktop o nel menu Start
2. **macOS**: Apri "DDT Manager" da Applications
3. **Linux**: Doppio click sull'AppImage o esegui da terminale

### Funzionalità Principali

- **Gestione DDT**: Crea, modifica e visualizza documenti di trasporto
- **Gestione Entità**: Gestisci mittenti, destinatari e vettori
- **Generazione PDF**: Crea PDF professionali dei documenti
- **Backup**: Configura backup automatici dei dati
- **Aggiornamenti**: Controlla e installa aggiornamenti

## 🔧 Sviluppo

### Struttura del Progetto

```
electron/
├── launcher.js          # Punto di ingresso principale
├── app-manager.js       # Gestore principale dell'applicazione
├── main.js              # Processo principale Electron
├── preload.js           # Script di preload per il renderer
├── config.js            # Configurazione dell'applicazione
├── updater.js           # Sistema di aggiornamenti
├── settings.js          # Gestione impostazioni
├── backup.js            # Sistema di backup
├── logger.js            # Sistema di logging
├── error-handler.js     # Gestione errori
├── performance-monitor.js # Monitoraggio performance
├── notifications.js     # Sistema notifiche
└── installer.js         # Installer dell'applicazione
```

### Script Disponibili

- `npm start`: Avvia l'applicazione in modalità produzione
- `npm run dev`: Avvia l'applicazione in modalità sviluppo
- `npm run build`: Costruisce l'applicazione per la distribuzione
- `npm run install`: Installa l'applicazione nel sistema
- `npm run uninstall`: Disinstalla l'applicazione dal sistema

### Debug

Per abilitare il debug:

1. **Modalità Sviluppo**:
   ```bash
   NODE_ENV=development npm run dev
   ```

2. **Strumenti di Sviluppo**: Premi `F12` o `Ctrl+Shift+I` per aprire DevTools

3. **Log**: I log sono salvati in `logs/` nella directory dell'applicazione

## 🚀 Distribuzione

### Build per Windows

```bash
npm run build-win
```

### Build per macOS

```bash
npm run build-mac
```

### Build per Linux

```bash
npm run build-linux
```

### Build per Tutte le Piattaforme

```bash
npm run build
```

## 🔒 Sicurezza

- **Context Isolation**: Abilitato per sicurezza
- **Node Integration**: Disabilitato nel renderer
- **Remote Module**: Disabilitato
- **CSP**: Content Security Policy configurato

## 📊 Monitoraggio

### Performance

L'applicazione include un sistema di monitoraggio delle performance che traccia:
- Utilizzo memoria
- Utilizzo CPU
- Tempo di avvio
- Performance database
- Generazione PDF

### Logging

Sistema di logging avanzato con:
- Livelli di log configurabili
- Rotazione automatica dei file
- Esportazione log
- Statistiche errori

## 🐛 Risoluzione Problemi

### Problemi Comuni

1. **Applicazione non si avvia**:
   - Verifica che Python e Node.js siano installati
   - Controlla i log in `logs/`
   - Esegui `npm run install` per reinstallare

2. **Errori di database**:
   - Esegui `python manage.py migrate`
   - Verifica i permessi del file database

3. **Problemi di aggiornamento**:
   - Controlla la connessione internet
   - Verifica i log dell'updater

### Supporto

Per supporto tecnico:
- Controlla i log dell'applicazione
- Verifica la documentazione
- Apri una issue su GitHub

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. Fork del repository
2. Crea un branch per la feature
3. Commit delle modifiche
4. Push al branch
5. Apri una Pull Request

## 📞 Contatti

- **Azienda**: Azienda Agricola BB&F
- **Email**: info@aziendaagricola.com
- **GitHub**: https://github.com/aziendaagricola/ddt-manager
