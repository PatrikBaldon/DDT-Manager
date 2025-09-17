# 🚀 DDT Manager v1.1.0 - Release Notes

## 📦 Download e Installazione

### Windows (Raccomandato)
[![Download Windows](https://img.shields.io/badge/Download-Windows-blue?style=for-the-badge&logo=windows)](https://github.com/PatrikBaldon/DDT-Application/releases/download/v1.1.0/DDT_Manager_Package.zip)

**Installazione in 3 passi:**
1. **Scarica** il file `DDT_Manager_Package.zip`
2. **Estrai** l'archivio in una cartella
3. **Esegui** `Avvio_Rapido.bat` come amministratore

## ✨ Novità in questa versione

### 🎯 **Migrazione Completa da PWA a Electron**
- **Applicazione desktop** moderna e professionale
- **Interfaccia nativa** ottimizzata per Windows
- **Prestazioni migliorate** rispetto alla versione web

### 🚀 **Sistema di Distribuzione Automatica**
- **Download automatico** dell'ultima versione da GitHub
- **Installazione automatica** con un click
- **Verifica e installazione** prerequisiti automatica
- **Configurazione automatica** dell'applicazione

### 🛠️ **Installer Professionale**
- **Installer NSIS** con interfaccia grafica moderna
- **Best practices globali** per installazione Windows
- **Disinstallazione pulita** tramite Pannello di Controllo
- **Shortcut automatici** su Desktop, Start Menu, Quick Launch

### 🔧 **Miglioramenti Tecnici**
- **Architettura Electron** con Django backend
- **Configurazioni multi-ambiente** (dev, prod, test)
- **GitHub Actions** per build e release automatica
- **Script PowerShell** per installazione automatica

## 📋 Prerequisiti

### Windows
- **Sistema Operativo**: Windows 10/11 (64-bit)
- **Python**: 3.8+ (installato automaticamente)
- **Node.js**: 16+ (installato automaticamente)
- **Privilegi**: Amministratore (richiesto per installazione)

## 🛠️ Opzioni di Installazione

### 1. Installazione Automatica (Raccomandato)
```bash
# Windows
1. Scarica DDT_Manager_Package.zip
2. Estrai l'archivio
3. Esegui Avvio_Rapido.bat come amministratore
4. Scegli "Download e Installazione Automatica"
```

**Vantaggi:**
- ✅ Installazione completamente automatica
- ✅ Verifica e installazione prerequisiti
- ✅ Configurazione automatica
- ✅ Creazione shortcut automatica

### 2. Installazione da PowerShell
```powershell
# Apri PowerShell come amministratore
# Esegui il comando:
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/PatrikBaldon/DDT-Application/main/installer/scripts/download-and-install.ps1" -OutFile "install-ddt.ps1"
.\install-ddt.ps1
```

## 🔧 Risoluzione Problemi

### ❌ "Privilegi amministratore richiesti"
**Soluzione:**
1. Clicca destro su `Avvio_Rapido.bat`
2. Seleziona "Esegui come amministratore"
3. Conferma quando richiesto

### ❌ "Python non trovato"
**Soluzione:**
- L'installer installerà Python automaticamente
- Oppure installa manualmente da [python.org](https://python.org/)

### ❌ "Node.js non trovato"
**Soluzione:**
- L'installer installerà Node.js automaticamente
- Oppure installa manualmente da [nodejs.org](https://nodejs.org/)

### ❌ "Errore durante il download"
**Soluzione:**
1. Verifica la connessione internet
2. Disabilita temporaneamente l'antivirus
3. Prova a scaricare manualmente da GitHub

## 🎯 Funzionalità

### ✨ Caratteristiche Principali
- **Gestione DDT** - Creazione e gestione documenti di trasporto
- **Interfaccia Moderna** - UI/UX ottimizzata per desktop
- **Offline** - Funziona senza connessione internet
- **Backup Automatico** - Salvataggio automatico dei dati
- **Esportazione PDF** - Generazione documenti PDF professionali

### 🔧 Funzionalità Tecniche
- **Installazione Automatica** - Setup completo in un click
- **Prerequisiti Automatici** - Installazione Python e Node.js
- **Configurazione Automatica** - Setup ottimale per il sistema
- **Disinstallazione Pulita** - Rimozione completa senza residui

## 📚 Documentazione

### Guida Completa
- [Guida Installazione](https://github.com/PatrikBaldon/DDT-Application/blob/main/installer/README_INSTALLER.md) - Guida dettagliata per sviluppatori
- [Guida Electron](https://github.com/PatrikBaldon/DDT-Application/blob/main/README_ELECTRON.md) - Documentazione applicazione Electron
- [README Principale](https://github.com/PatrikBaldon/DDT-Application/blob/main/README.md) - Panoramica del progetto

### Supporto
- **GitHub Issues**: [Segnala problemi](https://github.com/PatrikBaldon/DDT-Application/issues)
- **Email**: patrik.baldon@example.com
- **Documentazione**: [Wiki del progetto](https://github.com/PatrikBaldon/DDT-Application/wiki)

## 🔄 Aggiornamenti

### Verifica Aggiornamenti
L'applicazione verificherà automaticamente gli aggiornamenti all'avvio.

### Aggiornamento Manuale
1. Vai su [GitHub Releases](https://github.com/PatrikBaldon/DDT-Application/releases)
2. Scarica l'ultima versione
3. Segui la procedura di installazione

### Disinstallazione
```bash
# Windows
1. Vai in Pannello di Controllo > Programmi
2. Trova "DDT Manager"
3. Clicca "Disinstalla"

# Oppure esegui:
powershell -ExecutionPolicy Bypass -File uninstall-ddt.ps1
```

## 🤝 Contributi

### Come Contribuire
1. **Fork** del repository
2. **Crea** un branch per la tua feature
3. **Commit** le modifiche
4. **Push** al branch
5. **Apri** una Pull Request

### Segnalazione Bug
1. Vai su [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
2. Clicca "New Issue"
3. Compila il template
4. Invia la segnalazione

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi [LICENSE](https://github.com/PatrikBaldon/DDT-Application/blob/main/LICENSE) per dettagli.

---

**Sviluppato da Patrik Baldon per Azienda Agricola BB&F** 🌱

*Release Date: $(Get-Date -Format "dd/MM/yyyy")*
