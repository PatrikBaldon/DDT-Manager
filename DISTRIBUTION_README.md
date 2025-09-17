# 🚀 DDT Manager - Sistema di Distribuzione

## 📋 Panoramica

Questo sistema fornisce una distribuzione completa e automatica di DDT Manager tramite GitHub, permettendo agli utenti di scaricare e installare l'applicazione con un semplice click.

## 🎯 Obiettivi

- **Zero interazione terminale** - L'utente non deve mai aprire PowerShell o CMD
- **Installazione automatica** - Tutto gestito automaticamente
- **Best practices globali** - Installazione secondo standard internazionali
- **Distribuzione GitHub** - Utilizzo di GitHub per hosting e distribuzione

## 🏗️ Architettura

### 1. **GitHub Releases**
- **Hosting file** - Installer e package di distribuzione
- **Versioning automatico** - Gestione versioni tramite tag Git
- **Download diretto** - Link diretti per download

### 2. **GitHub Actions**
- **Build automatico** - Compilazione per Windows, macOS, Linux
- **Release automatica** - Creazione release al push di tag
- **Deploy automatico** - Distribuzione file su GitHub Releases

### 3. **Installer Automatico**
- **Download da GitHub** - Recupero ultima versione automaticamente
- **Verifica prerequisiti** - Controllo Python e Node.js
- **Installazione automatica** - Setup completo senza interazione

## 📁 Struttura File

```
installer/
├── scripts/
│   ├── download-and-install.ps1    # Download e installazione automatica
│   ├── uninstall-ddt.ps1           # Disinstallazione automatica
│   └── build-installer.ps1         # Build installer automatico
├── windows/
│   ├── DDT_Manager_Downloader.bat  # Downloader batch
│   └── DDT_Manager_Installer.bat   # Installer batch
├── nsis/
│   ├── ddt-installer.nsi           # Script NSIS installer
│   └── installer.nsh               # Configurazioni personalizzate
├── DOWNLOAD_PAGE.md                # Pagina download user-friendly
└── README_INSTALLER.md             # Documentazione installer

.github/
└── workflows/
    ├── build-and-release.yml       # Build e release automatica
    └── deploy-download-page.yml     # Deploy pagina download

scripts/
└── create-release.sh               # Script creazione release
```

## 🚀 Flusso di Distribuzione

### 1. **Sviluppo**
```bash
# Sviluppa l'applicazione
make dev

# Testa l'applicazione
make test

# Crea installer locale
make installer-package
```

### 2. **Release**
```bash
# Crea release su GitHub
make create-release VERSION=v1.0.0

# Oppure manualmente
./scripts/create-release.sh v1.0.0
```

### 3. **Distribuzione Automatica**
1. **GitHub Actions** rileva il tag
2. **Build automatico** per tutte le piattaforme
3. **Creazione release** con file allegati
4. **Deploy pagina download** su GitHub Pages

### 4. **Download Utente**
1. **Utente** va su GitHub Releases
2. **Scarica** `DDT_Manager_Package.zip`
3. **Estrae** l'archivio
4. **Esegue** `Avvio_Rapido.bat`
5. **Installazione automatica** completa

## 🛠️ Configurazione Iniziale

### 1. **Setup GitHub**
```bash
# Configura GitHub CLI
gh auth login

# Abilita GitHub Actions
# Vai su GitHub.com > Settings > Actions > General
# Abilita "Allow all actions and reusable workflows"
```

### 2. **Configura Repository**
```bash
# Abilita GitHub Pages
# Vai su GitHub.com > Settings > Pages
# Source: GitHub Actions
```

### 3. **Prima Release**
```bash
# Crea prima release
make create-release VERSION=v1.0.0

# Verifica su GitHub
# https://github.com/PatrikBaldon/DDT-Application/releases
```

## 📦 Package di Distribuzione

### **DDT_Manager_Package.zip**
Contiene:
- **`Avvio_Rapido.bat`** - Menu di installazione
- **`DDT_Manager_Downloader.bat`** - Downloader automatico
- **`DDT_Manager_Setup.exe`** - Installer NSIS
- **`DDT_Manager_Portable.exe`** - Versione portable
- **`install-ddt.ps1`** - Script PowerShell
- **`uninstall-ddt.ps1`** - Script disinstallazione
- **`README.txt`** - Documentazione utente
- **`LICENSE`** - Licenza

### **Installazione Utente**
1. **Scarica** `DDT_Manager_Package.zip`
2. **Estrae** in una cartella
3. **Esegue** `Avvio_Rapido.bat` come amministratore
4. **Sceglie** "Download e Installazione Automatica"

## 🔧 Personalizzazione

### **Modificare Installer**
1. **`installer/nsis/ddt-installer.nsi`** - Script principale
2. **`installer/nsis/installer.nsh`** - Configurazioni
3. **`installer/scripts/download-and-install.ps1`** - Download automatico

### **Modificare Pagina Download**
1. **`installer/DOWNLOAD_PAGE.md`** - Contenuto pagina
2. **`.github/workflows/deploy-download-page.yml`** - Deploy automatico

### **Modificare Build**
1. **`.github/workflows/build-and-release.yml`** - Build automatico
2. **`electron-builder.json`** - Configurazione Electron

## 📊 Monitoraggio

### **GitHub Actions**
- **Build Status**: https://github.com/PatrikBaldon/DDT-Application/actions
- **Release Status**: https://github.com/PatrikBaldon/DDT-Application/releases

### **Download Statistics**
- **GitHub Releases**: Mostra statistiche download
- **GitHub Insights**: Analisi traffico repository

## 🚨 Risoluzione Problemi

### **Build Fallito**
```bash
# Verifica log GitHub Actions
# https://github.com/PatrikBaldon/DDT-Application/actions

# Testa build locale
make installer-package
```

### **Release Non Creata**
```bash
# Verifica tag Git
git tag -l

# Verifica GitHub CLI
gh auth status

# Crea release manualmente
gh release create v1.0.0 --title "DDT Manager v1.0.0"
```

### **Download Fallito**
```bash
# Verifica URL GitHub
# https://github.com/PatrikBaldon/DDT-Application/releases/latest

# Testa download manuale
curl -L -o test.zip "https://github.com/PatrikBaldon/DDT-Application/releases/latest/download/DDT_Manager_Package.zip"
```

## 🔄 Aggiornamenti

### **Nuova Versione**
```bash
# Crea nuova release
make create-release VERSION=v1.1.0

# GitHub Actions creerà automaticamente:
# - Build per tutte le piattaforme
# - Release con file allegati
# - Deploy pagina download
```

### **Hotfix**
```bash
# Crea hotfix
make create-release VERSION=v1.0.1

# Release immediata senza modifiche al build
```

## 📈 Metriche di Successo

### **Download**
- **Totale download** per release
- **Download per piattaforma** (Windows, macOS, Linux)
- **Download per versione** (stabile, beta, alpha)

### **Installazione**
- **Tasso di successo** installazione
- **Errori comuni** durante installazione
- **Tempo medio** installazione

### **Utilizzo**
- **Utenti attivi** per versione
- **Feedback** utenti
- **Bug reports** per versione

## 🎯 Best Practices

### **Versioning**
- **Semantic Versioning** (v1.0.0, v1.1.0, v2.0.0)
- **Tag Git** per ogni release
- **Changelog** dettagliato

### **Distribuzione**
- **File multipli** per diverse esigenze
- **Documentazione** completa
- **Supporto** utenti

### **Sicurezza**
- **Verifica hash** file
- **Firma digitale** installer
- **Scan antivirus** automatico

---

**Sviluppato da Patrik Baldon per Azienda Agricola BB&F** 🌱

*Sistema di distribuzione professionale per applicazioni Electron*
