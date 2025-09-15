# 🚀 Installazione DDT Application su Windows - OFFLINE

Questa guida ti accompagnerà nell'installazione dell'applicazione DDT su Windows in modo completamente offline, come un'applicazione nativa.

## 📋 Prerequisiti

### 1. Sistema operativo
- Windows 10 o superiore (64-bit)
- Almeno 200 MB di spazio libero su disco
- **Nessuna connessione internet richiesta**
- **Nessuna installazione di Python richiesta**

### 2. Installazione completamente offline
- L'installer include Python portabile
- Tutte le dipendenze sono precompilate
- Database preconfigurato con dati di esempio
- Funziona come un'applicazione desktop tradizionale

## 🚀 Installazione Rapida

### Metodo 1: Installer Windows (Consigliato)

1. **Esegui l'installer**:
   - Fai doppio clic su `DDT_Application_Offline_Setup.exe`
   - Segui la procedura guidata di installazione
   - L'installer include tutto il necessario (Python, dipendenze, database)

2. **L'applicazione è pronta**:
   - Shortcut creato sul desktop
   - Entry nel menu Start
   - Associazioni file .ddt configurate
   - Servizio Windows opzionale

3. **Avvia l'applicazione**:
   - Doppio clic su "DDT Application" sul desktop
   - Oppure dal menu Start
   - Apri il browser e vai su: http://127.0.0.1:8000

### Metodo 2: Installazione Manuale

Se preferisci installare manualmente:

1. **Estrai i file** nella cartella desiderata (es. `C:\DDT\`)

2. **Esegui l'installazione**:
   - Fai doppio clic su `installer\scripts\install_ddt.bat`
   - Segui le istruzioni a schermo
   - L'installazione richiederà alcuni minuti

3. **Avvia l'applicazione**:
   - Fai doppio clic su `installer\scripts\start_ddt.bat`
   - Apri il browser e vai su: http://127.0.0.1:8000

## 📁 Struttura del Progetto

L'applicazione è organizzata in modo professionale:

```
DDT/
├── installer/                    # Installer completo offline
│   ├── DDT_Offline_Setup.exe    # Installer Windows principale
│   ├── scripts/                 # Script di installazione
│   │   ├── install_ddt.bat      # Installazione automatica
│   │   ├── start_ddt.bat        # Avvio applicazione
│   │   ├── uninstall_ddt.bat    # Disinstallazione
│   │   ├── ddt_service.bat      # Servizio Windows
│   │   └── open_ddt.bat         # Apertura file .ddt
│   ├── python/                  # Python portabile (offline)
│   ├── dependencies/            # Dipendenze Python precompilate
│   ├── app/                     # Applicazione DDT
│   │   ├── ddt_project/         # Configurazione Django
│   │   ├── ddt_app/             # Applicazione principale
│   │   ├── templates/           # Template HTML
│   │   ├── static/              # File CSS/JS
│   │   ├── data/                # Database e dati
│   │   └── setup_sample_data.py # Dati di esempio
│   ├── config/                  # File di configurazione
│   └── docs/                    # Documentazione
└── README.md                    # Documentazione principale
```

## 🎯 Utilizzo Quotidiano

### Avvio dell'Applicazione
- **Metodo rapido**: Doppio clic su "DDT Application" sul desktop
- **Menu Start**: Cerca "DDT Application" nel menu Start
- **File .ddt**: Doppio clic su un file .ddt per aprirlo direttamente

### Accesso all'Applicazione
- Apri il browser
- Vai su: http://127.0.0.1:8000
- L'applicazione sarà disponibile finché il server è attivo

### Fermare l'Applicazione
- Nel Prompt dei Comandi, premi `Ctrl+C`
- Chiudi la finestra del Prompt dei Comandi
- Oppure ferma il servizio Windows (se installato)

## 🔧 Manutenzione

### Aggiornamento
Per aggiornare l'applicazione:
1. Scarica la nuova versione
2. Esegui il nuovo installer
3. L'installer aggiornerà automaticamente l'installazione esistente

### Reset Database
Se hai problemi con il database:
1. Vai in Pannello di controllo > Programmi
2. Disinstalla e reinstalla l'applicazione
3. **ATTENZIONE**: Questo cancellerà tutti i dati!

### Backup
- I dati sono salvati in: `%PROGRAMFILES%\DDT Application\app\data\`
- Fai backup della cartella `data` per salvare i tuoi DDT
- Il database è in: `db.sqlite3`

## 🐛 Risoluzione Problemi

### Errore: "Applicazione non trovata"
- Reinstalla l'applicazione con l'installer
- Verifica che l'installazione sia completata correttamente

### Errore: "Database non trovato"
- L'installer crea automaticamente il database
- Se manca, reinstalla l'applicazione

### L'applicazione non si avvia
1. Controlla che l'installazione sia completata
2. Verifica che il database esista: `%PROGRAMFILES%\DDT Application\app\data\db.sqlite3`
3. Controlla i log in `%PROGRAMFILES%\DDT Application\logs\ddt.log`
4. Riavvia il computer e riprova

### L'applicazione si avvia ma non risponde
1. Chiudi tutte le finestre del browser
2. Riavvia l'applicazione
3. Prova con un browser diverso
4. Controlla che la porta 8000 non sia occupata

## 📊 Vantaggi dell'Installazione Offline

### ✅ Installazione Semplice
- Un solo file installer
- Nessuna configurazione richiesta
- Funziona su qualsiasi PC Windows

### ✅ Completamente Offline
- Nessuna connessione internet necessaria
- Python portabile incluso
- Dipendenze precompilate

### ✅ Applicazione Nativa
- Shortcut sul desktop
- Entry nel menu Start
- Associazioni file .ddt
- Servizio Windows opzionale

### ✅ Manutenzione Facile
- Disinstallazione completa
- Aggiornamenti semplici
- Backup automatico dei dati

## 🔒 Sicurezza

- L'applicazione è configurata per funzionare solo in locale (127.0.0.1)
- Non è esposta su internet
- I dati sono salvati nel file `db.sqlite3` locale
- Configurazione ottimizzata per uso offline

## 📞 Supporto

Se riscontri problemi:

1. **Controlla i log**: `%PROGRAMFILES%\DDT Application\logs\ddt.log`
2. **Verifica l'installazione**: Pannello di controllo > Programmi
3. **Riprova l'installazione**: Esegui di nuovo l'installer
4. **Reset completo**: Disinstalla e reinstalla l'applicazione

## 🎉 Installazione Completata!

Una volta completata l'installazione, avrai accesso a:

- ✅ Creazione e gestione DDT
- ✅ Gestione mittenti e destinatari
- ✅ Gestione vettori e targhe
- ✅ Generazione PDF automatica
- ✅ Interfaccia web moderna e intuitiva

**Buon lavoro con la tua applicazione DDT!** 🚀
