# 🌱 DDT Application - Sistema di Gestione Documenti di Trasporto

Un'applicazione Django completa per la gestione dei Documenti di Trasporto (DDT) per aziende agricole.

## ✨ Caratteristiche Principali

- **📄 Gestione DDT**: Creazione, modifica e stampa di documenti di trasporto
- **👥 Gestione Entità**: Mittenti, destinatari, vettori e destinazioni
- **📊 Reportistica**: Generazione PDF professionali
- **🔄 Sistema di Aggiornamenti**: Aggiornamenti automatici via GitHub
- **💻 Installazione Offline**: Funziona senza connessione internet
- **🪟 Windows Native**: Installazione semplice su Windows

## 🚀 Installazione Rapida

### Per Windows (Consigliato)

1. **Scarica** l'installer: `DDT_Complete_Setup.exe`
2. **Esegui** l'installer come amministratore
3. **Segui** la procedura guidata
4. **Avvia** l'applicazione dal desktop

### Installazione Manuale

```bash
# Clona il repository
git clone https://github.com/PatrikBaldon/DDT-Application.git
cd DDT-Application

# Installa dipendenze
pip install -r requirements.txt

# Esegui migrazioni
python manage.py migrate

# Crea superuser
python manage.py createsuperuser

# Avvia l'applicazione
python manage.py runserver
```

## 📁 Struttura del Progetto

```
DDT-Application/
├── installer/                 # File di installazione Windows
│   ├── scripts/              # Script di gestione
│   │   ├── update_ddt.bat    # Aggiornamento applicazione
│   │   ├── check_version.bat # Controllo versione
│   │   └── rollback_ddt.bat  # Ripristino versione precedente
│   └── app/                  # Applicazione Django
├── ddt_app/                  # App Django principale
├── ddt_project/              # Configurazione Django
├── templates/                # Template HTML
├── static/                   # File statici (CSS, JS)
└── requirements.txt          # Dipendenze Python
```

## 🔧 Utilizzo

### Avvio dell'Applicazione

- **Windows**: Doppio clic su "DDT Application" dal desktop
- **Manuale**: `python manage.py runserver`

### Gestione DDT

1. **Accedi** all'applicazione web
2. **Crea** un nuovo DDT
3. **Compila** i dati richiesti
4. **Stampa** o **esporta** in PDF

### Aggiornamenti

```bash
# Controlla aggiornamenti
check_version.bat

# Aggiorna applicazione
update_ddt.bat

# Ripristina versione precedente
rollback_ddt.bat
```

## 🛠️ Sviluppo

### Setup Ambiente di Sviluppo

```bash
# Clona il repository
git clone https://github.com/PatrikBaldon/DDT-Application.git
cd DDT-Application

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui migrazioni
python manage.py migrate

# Crea superuser
python manage.py createsuperuser

# Avvia server di sviluppo
python manage.py runserver
```

### Struttura del Codice

- **`ddt_app/models.py`**: Modelli Django per DDT e entità
- **`ddt_app/views.py`**: Viste per la gestione DDT
- **`ddt_app/forms.py`**: Form per input dati
- **`ddt_app/pdf_generator.py`**: Generazione PDF
- **`installer/scripts/`**: Script di installazione e aggiornamento

## 📋 Requisiti di Sistema

- **OS**: Windows 10/11 (consigliato) o Linux/Mac
- **Python**: 3.8+ (se installazione manuale)
- **RAM**: 4GB minimo
- **Spazio**: 500MB per l'installazione

## 🔄 Sistema di Aggiornamenti

L'applicazione include un sistema di aggiornamenti automatici:

- **Controllo automatico** di nuove versioni su GitHub
- **Download e installazione** automatica degli aggiornamenti
- **Backup automatico** prima di ogni aggiornamento
- **Rollback** in caso di problemi

## 📝 Note di Rilascio

### v1.0.0
- Prima versione stabile
- Gestione completa DDT
- Sistema di aggiornamenti
- Installazione offline per Windows

## 🤝 Contribuire

1. **Fork** il repository
2. **Crea** un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 📞 Supporto

Per supporto e domande:
- **Issues**: [GitHub Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
- **Email**: supporto@ddt-app.com

## 🙏 Ringraziamenti

- Django Framework
- ReportLab per la generazione PDF
- Bootstrap per l'interfaccia utente
- Tutti i contributori del progetto

---

**DDT Application** - Gestione professionale dei Documenti di Trasporto per aziende agricole 🌱