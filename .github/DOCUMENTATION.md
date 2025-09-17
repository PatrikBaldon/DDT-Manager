# 📚 Documentazione DDT Electron App

## 🎯 Panoramica

DDT Electron App è un sistema completo per la gestione dei Documenti di Trasporto (DDT) progettato specificamente per aziende agricole italiane.

## 🏗️ Architettura

### Backend (Django)
- **Framework**: Django 4.2.7
- **Database**: SQLite3 (configurabile)
- **API**: REST API per aggiornamenti
- **PDF**: ReportLab per generazione documenti

### Frontend (Electron)
- **Framework**: Electron 28.0+
- **Template**: Django Templates
- **CSS**: Bootstrap 5 + Custom CSS
- **JavaScript**: Vanilla JS + jQuery
- **UI**: Desktop nativo

### Build e Distribuzione
- **Multi-piattaforma**: Windows, macOS, Linux
- **Build**: Electron Builder
- **Auto-aggiornamenti**: Electron Updater
- **Installer**: NSIS (Windows), DMG (macOS), AppImage (Linux)

## 📁 Struttura del Codice

```
DDT-Electron/
├── electron/                   # Configurazioni Electron
│   ├── main.js                 # Processo principale
│   ├── preload.js              # Script di preload
│   ├── config.js               # Configurazione multi-ambiente
│   └── build.js                # Script di build
├── ddt_app/                    # App Django principale
│   ├── models.py              # Modelli dati
│   ├── views.py               # Viste web
│   ├── forms.py               # Form Django
│   ├── pdf_generator.py       # Generazione PDF
│   └── update_manager.py      # Sistema aggiornamenti
├── ddt_project/               # Configurazione Django
│   ├── settings.py            # Impostazioni base
│   └── settings_offline.py    # Impostazioni offline
├── installer/                 # File di installazione
│   ├── scripts/               # Script di gestione
│   └── app/                   # App per installer
└── templates/                 # Template HTML
```

## 🔧 Configurazione

### Impostazioni Base
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Impostazioni Offline
```python
# settings_offline.py
DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## 🚀 Deployment

### Windows (Consigliato)
1. **Installer**: Esegui `DDT_Complete_Setup.exe`
2. **Manuale**: Segui `INSTALLAZIONE_WINDOWS.md`
3. **Portable**: Usa la versione portable

### Linux/Mac
1. **Clona**: `git clone https://github.com/PatrikBaldon/DDT-Application.git`
2. **Installa**: `pip install -r requirements.txt`
3. **Configura**: `python manage.py migrate`
4. **Avvia**: `python manage.py runserver`

## 🔄 Sistema di Aggiornamenti

### Controllo Automatico
- **GitHub API**: Controlla nuove release
- **Download**: Scarica automaticamente
- **Backup**: Crea backup prima di aggiornare
- **Rollback**: Ripristina versione precedente

### Script di Gestione
- **`update_ddt.bat`**: Aggiornamento principale
- **`check_version.bat`**: Controllo versione
- **`rollback_ddt.bat`**: Ripristino versione
- **`auto_update.bat`**: Aggiornamento automatico

## 📊 Modelli Dati

### DDT (Documento di Trasporto)
```python
class DDT(models.Model):
    numero_ddt = models.CharField(max_length=20)
    data_ddt = models.DateField()
    mittente = models.ForeignKey(Mittente, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    # ... altri campi
```

### Entità
- **Mittente**: Azienda che invia
- **Destinatario**: Azienda che riceve
- **Vettore**: Trasportatore
- **Destinazione**: Luogo di consegna

## 🎨 Interfaccia Utente

### Pagine Principali
- **Home**: Dashboard principale
- **DDT List**: Lista documenti
- **DDT Form**: Creazione/modifica DDT
- **Entità**: Gestione mittenti, destinatari, ecc.

### Componenti
- **Form**: Input validati
- **Tabelle**: Lista dati paginata
- **PDF**: Anteprima e stampa
- **Modali**: Conferme e dettagli

## 🔒 Sicurezza

### Autenticazione
- **Login**: Sistema di autenticazione Django
- **Sessioni**: Gestione sessioni sicure
- **CSRF**: Protezione CSRF attiva

### Validazione
- **Form**: Validazione lato client e server
- **File**: Controllo tipi file
- **Input**: Sanitizzazione input utente

## 📈 Performance

### Ottimizzazioni
- **Database**: Query ottimizzate
- **Statici**: File statici raccolti
- **Cache**: Cache per dati frequenti
- **Lazy Loading**: Caricamento lazy per liste

### Monitoraggio
- **Log**: Sistema di logging completo
- **Errori**: Gestione errori centralizzata
- **Metriche**: Monitoraggio performance

## 🧪 Testing

### Test Unitari
```bash
python manage.py test
```

### Test di Integrazione
- **API**: Test endpoint REST
- **UI**: Test interfaccia utente
- **PDF**: Test generazione documenti

### Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

## 📝 API

### Endpoint Aggiornamenti
- **GET** `/api/check-updates/`: Controlla aggiornamenti
- **POST** `/api/perform-update/`: Esegue aggiornamento
- **GET** `/api/current-version/`: Versione attuale

### Formato Risposta
```json
{
  "current_version": "1.0.0",
  "latest_version": "1.0.1",
  "update_available": true,
  "release_notes": "Bug fixes and improvements"
}
```

## 🔧 Manutenzione

### Backup
- **Database**: Backup automatico prima aggiornamenti
- **File**: Backup file critici
- **Configurazione**: Backup impostazioni

### Pulizia
- **Log**: Rotazione log automatica
- **Temp**: Pulizia file temporanei
- **Cache**: Pulizia cache periodica

### Monitoraggio
- **Errori**: Log errori centralizzati
- **Performance**: Monitoraggio risorse
- **Uso**: Statistiche utilizzo

## 🚨 Troubleshooting

### Problemi Comuni
1. **Errore migrazioni**: `python manage.py migrate --fake-initial`
2. **File statici**: `python manage.py collectstatic`
3. **Permessi**: Controlla permessi file
4. **Porta**: Verifica porta disponibile

### Log
- **Django**: `logs/django.log`
- **Applicazione**: `logs/ddt.log`
- **Errori**: `logs/error.log`

## 📞 Supporto

### Contatti
- **GitHub**: [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
- **Email**: supporto@ddt-app.com
- **Documentazione**: [Wiki](https://github.com/PatrikBaldon/DDT-Application/wiki)

### Contribuire
1. Fork del repository
2. Crea branch per feature
3. Sviluppa e testa
4. Crea Pull Request

---

**DDT Application** - Documentazione completa per sviluppatori e utenti 🌱
