# DDT Manager - Sistema di Installazione Windows

## 🚀 Panoramica

Questo sistema fornisce un'installazione automatica e professionale per DDT Manager su Windows, senza richiedere interazione con il terminale da parte dell'utente finale.

## 📁 Struttura File

```
installer/
├── nsis/                    # Script NSIS per installer
│   ├── ddt-installer.nsi   # Script principale installer
│   └── installer.nsh       # Configurazioni personalizzate
├── scripts/                 # Script PowerShell
│   ├── install-ddt.ps1     # Installazione automatica
│   ├── uninstall-ddt.ps1   # Disinstallazione automatica
│   └── build-installer.ps1 # Build installer automatico
├── windows/                 # Script batch Windows
│   └── DDT_Manager_Installer.bat
└── dist/                    # File di output
    ├── DDT_Manager_Setup.exe
    └── DDT_Manager_Package/
```

## 🛠️ Prerequisiti per Sviluppatori

### 1. **NSIS (Nullsoft Scriptable Install System)**
```bash
# Download da: https://nsis.sourceforge.io/
# Installa con le impostazioni predefinite
```

### 2. **PowerShell 5.0+**
```bash
# Verifica versione
powershell -Command "$PSVersionTable.PSVersion"
```

### 3. **Node.js e npm**
```bash
# Verifica installazione
node --version
npm --version
```

## 🔧 Creazione Installer

### Metodo 1: Script Automatico (Raccomandato)
```bash
# Crea installer completo
make installer-package

# Oppure solo installer
make installer-build

# Pulisci file di build
make installer-clean
```

### Metodo 2: PowerShell Diretto
```powershell
# Build completo
.\installer\scripts\build-installer.ps1

# Build con pulizia
.\installer\scripts\build-installer.ps1 -Clean

# Solo installer (salta build Electron)
.\installer\scripts\build-installer.ps1 -SkipBuild
```

### Metodo 3: NSIS Manuale
```bash
# Installa NSIS
# Esegui makensis
makensis installer\nsis\ddt-installer.nsi
```

## 📦 Distribuzione

### Package Completo
Il sistema crea automaticamente un package di distribuzione in `installer/dist/DDT_Manager_Package/` contenente:

- **`DDT_Manager_Setup.exe`** - Installer principale
- **`Avvio_Rapido.bat`** - Script di avvio con menu
- **`install-ddt.ps1`** - Installazione automatica
- **`uninstall-ddt.ps1`** - Disinstallazione automatica
- **`DDT_Manager_Installer.bat`** - Installer batch
- **`README.txt`** - Documentazione utente
- **`LICENSE`** - Licenza

### Distribuzione agli Utenti
1. **Copia** la cartella `DDT_Manager_Package` su un supporto di distribuzione
2. **Condividi** con gli utenti finali
3. **Gli utenti** eseguono `Avvio_Rapido.bat` per installare

## 👥 Installazione per Utenti Finali

### Opzione 1: Installazione Automatica (Raccomandato)
1. Esegui `Avvio_Rapido.bat`
2. Scegli opzione 1 (Installazione Automatica)
3. L'installer gestirà tutto automaticamente

### Opzione 2: Installazione Manuale
1. Esegui `DDT_Manager_Setup.exe`
2. Segui la procedura guidata
3. L'installer verificherà e installerà i prerequisiti

### Opzione 3: PowerShell
1. Apri PowerShell come amministratore
2. Esegui `.\install-ddt.ps1`
3. L'installer gestirà tutto automaticamente

## 🔧 Funzionalità Installer

### ✅ Installazione Automatica
- **Verifica prerequisiti** (Python, Node.js)
- **Download e installazione** automatica dei prerequisiti
- **Installazione applicazione** con configurazione automatica
- **Creazione shortcut** (Desktop, Start Menu, Quick Launch)
- **Configurazione registro** per disinstallazione

### ✅ Disinstallazione Completa
- **Rimozione file** applicazione
- **Rimozione shortcut** e collegamenti
- **Pulizia registro** Windows
- **Rimozione dati utente** (opzionale)
- **Pulizia file temporanei**

### ✅ Verifica Prerequisiti
- **Python 3.8+** - Verifica e installazione automatica
- **Node.js 16+** - Verifica e installazione automatica
- **Privilegi amministratore** - Verifica automatica

### ✅ Configurazione Automatica
- **Directory installazione** - `C:\Program Files\DDT Manager`
- **Dati utente** - `%APPDATA%\DDT Manager`
- **File di configurazione** - Creazione automatica
- **Log** - Directory dedicata per log

## 🚨 Risoluzione Problemi

### Errore: "Privilegi amministratore richiesti"
```bash
# Soluzione: Esegui come amministratore
# Clicca destro su script > "Esegui come amministratore"
```

### Errore: "NSIS non trovato"
```bash
# Soluzione: Installa NSIS
# Download da: https://nsis.sourceforge.io/
```

### Errore: "Python non trovato"
```bash
# Soluzione: L'installer installerà Python automaticamente
# Oppure installa manualmente da: https://python.org/
```

### Errore: "Node.js non trovato"
```bash
# Soluzione: L'installer installerà Node.js automaticamente
# Oppure installa manualmente da: https://nodejs.org/
```

## 📋 Personalizzazione

### Modificare Configurazioni
1. **`installer/nsis/ddt-installer.nsi`** - Script principale installer
2. **`installer/nsis/installer.nsh`** - Configurazioni personalizzate
3. **`installer/scripts/install-ddt.ps1`** - Script installazione
4. **`installer/scripts/uninstall-ddt.ps1`** - Script disinstallazione

### Modificare Aspetto Installer
1. **Icone** - Modifica `static/images/icons/icon-512x512.ico`
2. **Banner** - Modifica `static/images/logo1.png`
3. **Colori** - Modifica script NSIS
4. **Testi** - Modifica stringhe in script NSIS

### Aggiungere Funzionalità
1. **Verifica prerequisiti** - Modifica `installer.nsh`
2. **Installazione componenti** - Modifica `ddt-installer.nsi`
3. **Configurazione post-installazione** - Modifica script PowerShell

## 🔄 Aggiornamenti

### Aggiornamento Installer
```bash
# Modifica versioni in:
# - installer/nsis/ddt-installer.nsi
# - installer/nsis/installer.nsh
# - package.json
# - electron-builder.json

# Ricrea installer
make installer-package
```

### Aggiornamento Applicazione
```bash
# L'installer gestisce automaticamente gli aggiornamenti
# Gli utenti possono disinstallare e reinstallare
```

## 📞 Supporto

Per problemi o domande:
- **GitHub Issues** - [DDT-Application Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
- **Email** - patrik.baldon@example.com
- **Documentazione** - [README_ELECTRON.md](../README_ELECTRON.md)

## 📄 Licenza

Questo sistema di installazione è rilasciato sotto licenza MIT. Vedi [LICENSE](../LICENSE) per dettagli.

---

**Sviluppato da Patrik Baldon per Azienda Agricola BB&F** 🌱
