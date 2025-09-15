# 🪟 Installazione DDT Application su Windows

## 📋 Prerequisiti

- **Sistema Operativo**: Windows 10/11 (consigliato) o Windows 8.1
- **Privilegi**: Amministratore per l'installazione
- **Spazio**: 500MB liberi su disco
- **Connessione**: Internet per il download iniziale

## 🚀 Installazione Rapida

### Passo 1: Download
1. **Vai su**: [GitHub Releases](https://github.com/PatrikBaldon/DDT-Application/releases)
2. **Scarica**: `DDT-Application-v1.0.1-Complete.zip`
3. **Salva** il file in una cartella temporanea (es. `C:\Temp\`)

### Passo 2: Estrazione
1. **Clicca destro** sul file ZIP scaricato
2. **Seleziona**: "Estrai tutto..."
3. **Scegli** una cartella di destinazione (es. `C:\Temp\DDT-Install\`)
4. **Clicca**: "Estrai"

### Passo 3: Installazione
1. **Apri** la cartella estratta
2. **Clicca destro** su `DDT-Application-v1.0.1-Installer.bat`
3. **Seleziona**: "Esegui come amministratore"
4. **Conferma** quando richiesto dal controllo account utente
5. **Segui** la procedura guidata

### Passo 4: Verifica Installazione
1. **Cerca** "DDT Application" nel menu Start
2. **Clicca** sull'icona per avviare l'applicazione
3. **Verifica** che si apra il browser su `http://127.0.0.1:8000`

## 🔧 Installazione Manuale (Avanzata)

### Prerequisiti Aggiuntivi
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/download/win)

### Passo 1: Clonare Repository
```cmd
git clone https://github.com/PatrikBaldon/DDT-Application.git
cd DDT-Application
```

### Passo 2: Creare Ambiente Virtuale
```cmd
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Installare Dipendenze
```cmd
pip install -r requirements.txt
```

### Passo 4: Configurare Database
```cmd
python manage.py migrate
python manage.py collectstatic --noinput
```

### Passo 5: Creare Superuser
```cmd
python manage.py createsuperuser
```

### Passo 6: Avviare Applicazione
```cmd
python manage.py runserver
```

## 🎯 Utilizzo dell'Applicazione

### Avvio
- **Desktop**: Doppio clic su "DDT Application"
- **Start Menu**: Start → "DDT Application"
- **Manuale**: Esegui `start_ddt.bat` dalla directory di installazione

### Prima Configurazione
1. **Apri** l'applicazione
2. **Crea** un account amministratore
3. **Configura** i dati dell'azienda
4. **Aggiungi** mittenti, destinatari e vettori
5. **Inizia** a creare DDT

### Gestione DDT
1. **Clicca** su "Nuovo DDT"
2. **Compila** i dati richiesti
3. **Salva** il documento
4. **Stampa** o esporta in PDF

## 🔄 Aggiornamenti

### Controllo Aggiornamenti
```cmd
# Dalla directory di installazione
cd "C:\Program Files\DDT Application\scripts"
check_version.bat
```

### Aggiornamento Automatico
```cmd
# Dalla directory di installazione
cd "C:\Program Files\DDT Application\scripts"
update_ddt.bat
```

### Rollback (Ripristino)
```cmd
# Dalla directory di installazione
cd "C:\Program Files\DDT Application\scripts"
rollback_ddt.bat
```

## 🛠️ Risoluzione Problemi

### Problema: "Applicazione non trovata"
**Soluzione**:
1. Verifica che l'installazione sia completata
2. Controlla che la directory `C:\Program Files\DDT Application` esista
3. Reinstalla l'applicazione

### Problema: "Errore database"
**Soluzione**:
1. Esegui `start_ddt.bat` dalla directory di installazione
2. Il script eseguirà automaticamente le migrazioni
3. Se il problema persiste, reinstalla l'applicazione

### Problema: "Porta già in uso"
**Soluzione**:
1. Chiudi altre istanze dell'applicazione
2. Riavvia il computer
3. Cambia porta modificando `start_ddt.bat`

### Problema: "Privilegi insufficienti"
**Soluzione**:
1. Esegui l'installer come amministratore
2. Verifica i permessi della directory di installazione
3. Contatta l'amministratore di sistema

## 📁 Struttura Installazione

```
C:\Program Files\DDT Application\
├── app\                    # Applicazione Django
│   ├── ddt_app\           # Modelli e viste
│   ├── ddt_project\       # Configurazione Django
│   ├── templates\         # Template HTML
│   ├── static\            # File statici
│   └── manage.py          # Script Django
├── scripts\               # Script di gestione
│   ├── start_ddt.bat      # Avvio applicazione
│   ├── update_ddt.bat     # Aggiornamento
│   ├── check_version.bat  # Controllo versione
│   └── rollback_ddt.bat   # Ripristino
├── backup\                # Backup automatici
├── logs\                  # File di log
├── version.txt            # Versione installata
├── README.md              # Documentazione
└── LICENSE                # Licenza
```

## 🔒 Sicurezza

### Backup Automatico
- L'applicazione crea backup automatici prima degli aggiornamenti
- I backup sono salvati in `C:\Program Files\DDT Application\backup\`
- Mantieni sempre una copia di backup recente

### Aggiornamenti Sicuri
- Gli aggiornamenti sono scaricati da GitHub
- Verifica sempre la fonte degli aggiornamenti
- Testa gli aggiornamenti in ambiente di sviluppo

### Dati Sensibili
- I dati sono salvati in database SQLite locale
- Non vengono inviati dati a server esterni
- Mantieni sempre backup dei dati importanti

## 📞 Supporto

### Log di Errore
- **Django**: `C:\Program Files\DDT Application\logs\django.log`
- **Applicazione**: `C:\Program Files\DDT Application\logs\ddt.log`
- **Errori**: `C:\Program Files\DDT Application\logs\error.log`

### Contatti
- **GitHub Issues**: [Segnala problemi](https://github.com/PatrikBaldon/DDT-Application/issues)
- **Email**: supporto@ddt-app.com
- **Documentazione**: [Wiki GitHub](https://github.com/PatrikBaldon/DDT-Application/wiki)

## 🎉 Congratulazioni!

Hai installato con successo DDT Application! 

L'applicazione è ora pronta per gestire i tuoi Documenti di Trasporto in modo professionale ed efficiente.

**Buon lavoro con la tua applicazione DDT!** 🌱
