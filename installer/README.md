# 📦 Installer DDT Application

Questa cartella contiene tutti i file necessari per l'installazione offline dell'applicazione DDT.

## 🗂️ Struttura

```
installer/
├── README.md                    # Questo file
├── python/                      # Python portabile (offline)
├── dependencies/                # Dipendenze Python precompilate
├── app/                         # Applicazione DDT
├── scripts/                     # Script di installazione
├── config/                      # File di configurazione
└── docs/                        # Documentazione
```

## 🚀 Installazione

1. **Esegui l'installer principale**:
   - `install_ddt.exe` - Installer Windows completo
   - `install_ddt.bat` - Script di installazione batch

2. **L'installer include**:
   - Python portabile (nessuna installazione richiesta)
   - Tutte le dipendenze Python precompilate
   - Database preconfigurato con dati di esempio
   - Configurazione ottimizzata per Windows

3. **Dopo l'installazione**:
   - L'applicazione sarà disponibile nel menu Start
   - Shortcut sul desktop
   - Funziona completamente offline

## 🔧 Configurazione

L'installer configura automaticamente:
- Ambiente Python portabile
- Database SQLite locale
- File di configurazione ottimizzati
- Shortcut e associazioni file
- Servizio Windows (opzionale)

## 📋 Requisiti

- Windows 10/11 (64-bit)
- 200 MB di spazio libero
- Nessuna connessione internet richiesta
- Nessuna installazione di Python richiesta
