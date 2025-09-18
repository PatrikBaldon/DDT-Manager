# DDT Manager v1.0.0 - File di Distribuzione

## 🎉 Prima Release Electron

Questa è la prima release dell'applicazione Electron per la gestione dei Documenti di Trasporto.

## 📦 File di Distribuzione

### Windows
- **File**: `DDT Manager Setup 1.0.0.exe` (81.2 MB)
- **Tipo**: Installer NSIS
- **Architettura**: x64 (compatibile con Windows 10/11 x64)
- **Alternativa**: `DDT_Manager_Portable_Windows.zip` - Versione portatile (senza installazione)

### macOS
- **File**: `DDT Manager-1.0.0-arm64.dmg` (97.7 MB)
- **Tipo**: Installer DMG
- **Architettura**: ARM64 (compatibile con Apple Silicon)

### Linux
- **File**: `DDT Manager-1.0.0-arm64.AppImage` (107.1 MB)
- **Tipo**: AppImage portabile
- **Architettura**: ARM64 (compatibile con Linux ARM64)

## 🚀 Installazione

### Windows

#### **Opzione 1: Installer (Raccomandato)**
1. Scarica `DDT Manager Setup 1.0.0.exe`
2. Esegui l'installer come amministratore
3. Segui le istruzioni per installare Python e Node.js se necessario
4. L'applicazione si avvierà automaticamente

#### **Opzione 2: Versione Portatile (Se l'installer non funziona)**
1. Scarica `DDT_Manager_Portable_Windows.zip`
2. Estrai l'archivio in una cartella
3. Installa Python 3.8+ e Node.js 16+ se non già presenti
4. Esegui `Start_DDT_Manager.bat` (doppio click)

### macOS
1. Scarica `DDT Manager-1.0.0-arm64.dmg`
2. Apri il file DMG
3. Trascina l'applicazione in Applications
4. Esegui l'applicazione da Applications

### Linux
1. Scarica `DDT Manager-1.0.0-arm64.AppImage`
2. Rendi eseguibile: `chmod +x DDT_Manager-1.0.0-arm64.AppImage`
3. Esegui: `./DDT_Manager-1.0.0-arm64.AppImage`

## ✨ Caratteristiche

- 🖥️ **Applicazione Desktop**: Interfaccia nativa per Windows, macOS e Linux
- 📄 **Gestione DDT Completa**: Creazione, modifica e visualizzazione documenti
- 📊 **Generazione PDF**: PDF professionali con layout ottimizzato
- 🔄 **Aggiornamenti Automatici**: Controllo e installazione aggiornamenti
- 💾 **Backup Automatico**: Sistema di backup integrato per i dati
- 📈 **Monitoraggio Performance**: Tracciamento delle performance dell'applicazione
- 🔔 **Notifiche Desktop**: Sistema di notifiche per l'utente
- ⚙️ **Gestione Impostazioni**: Configurazione persistente dell'applicazione

## 🔧 Prerequisiti

- Python 3.8+ (installato automaticamente dall'installer)
- Node.js 16+ (installato automaticamente dall'installer)
- 500MB di spazio su disco
- Connessione internet per aggiornamenti

## 🚀 Sviluppato da

**Patrik Baldon** per **Azienda Agricola BB&F**

## 📞 Supporto

Per supporto tecnico o segnalazione bug, visita:
- [GitHub Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
- Email: patrik.baldon@aziendaagricola.com

## 📋 Note Tecniche

- **File Locali**: Generati su macOS ARM64 (solo per test)
- **File Ufficiali**: Creati automaticamente da GitHub Actions per ogni piattaforma
- **Architetture Corrette**: 
  - Windows: x64 (compatibile con la maggior parte dei PC)
  - macOS: x64 + ARM64 (Intel e Apple Silicon)
  - Linux: x64 (compatibile con la maggior parte delle distribuzioni)
- **Sicurezza**: Tutti i file sono firmati e sicuri per l'installazione
- **Offline**: L'applicazione funziona offline dopo l'installazione