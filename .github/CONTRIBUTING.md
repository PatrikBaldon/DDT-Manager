# 🤝 Contribuire a DDT-Application

Grazie per il tuo interesse a contribuire a DDT-Application! Questo documento ti guiderà attraverso il processo di contribuzione per l'applicazione Electron di gestione Documenti di Trasporto.

## 🚀 Come Iniziare

### 1. Fork del Repository
1. Vai su [DDT-Application](https://github.com/PatrikBaldon/DDT-Application)
2. Clicca su "Fork" in alto a destra
3. Clona il tuo fork localmente:
   ```bash
   git clone https://github.com/TUO_USERNAME/DDT-Application.git
   cd DDT-Application
   ```

### 2. Setup Ambiente di Sviluppo
```bash
# Prerequisiti
# - Node.js 16.0+ (https://nodejs.org/)
# - Python 3.8+ (https://python.org/)
# - Electron 28.0+ (installato automaticamente)

# Crea ambiente virtuale Python
python -m venv venv

# Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installa dipendenze Python
pip install -r requirements.txt

# Installa dipendenze Node.js
npm install

# Esegui migrazioni
python manage.py migrate

# Raccogli file statici
python manage.py collectstatic --noinput

# Avvia applicazione Electron in modalità sviluppo
npm run electron-dev
```

## 🔧 Processo di Contribuzione

### 1. Crea un Branch
```bash
git checkout -b feature/nome-della-tua-feature
# oppure
git checkout -b bugfix/descrizione-bug
```

### 2. Sviluppa la Funzionalità
- Scrivi codice pulito e ben documentato
- Segui le convenzioni di naming del progetto
- Aggiungi test per le nuove funzionalità
- Aggiorna la documentazione se necessario

### 3. Test
```bash
# Esegui test Django
python manage.py test

# Test Electron (se disponibili)
npm test

# Controlla stile codice
flake8 .
eslint electron/
```

### 4. Commit
```bash
git add .
git commit -m "feat: aggiungi descrizione della funzionalità"
```

### 5. Push e Pull Request
```bash
git push origin feature/nome-della-tua-feature
```

Poi vai su GitHub e crea una Pull Request.

## 📋 Convenzioni

### Commit Messages
Usa il formato [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` per nuove funzionalità
- `fix:` per bug fixes
- `docs:` per documentazione
- `style:` per formattazione
- `refactor:` per refactoring
- `test:` per test
- `chore:` per task di manutenzione

### Codice
- Usa Python 3.8+
- Segui PEP 8 per Python
- Usa ESLint per JavaScript/Electron
- Aggiungi docstring alle funzioni
- Usa type hints quando possibile

### Electron
- Testa sempre l'applicazione su tutte le piattaforme
- Verifica la compatibilità con Windows, macOS e Linux
- Controlla che l'installer funzioni correttamente
- Testa gli aggiornamenti automatici

## 🐛 Segnalazione Bug

### Prima di Segnalare
1. Controlla se il bug è già stato segnalato
2. Verifica di usare l'ultima versione
3. Prova a riprodurre il bug su diverse piattaforme

### Come Segnalare
1. Vai su [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
2. Clicca "New Issue"
3. Seleziona "Bug Report"
4. Compila il template includendo:
   - Sistema operativo
   - Versione dell'applicazione
   - Passi per riprodurre il bug
   - Log di errore (se disponibili)

## 💡 Richieste di Funzionalità

### Prima di Richiedere
1. Controlla se la funzionalità è già stata richiesta
2. Verifica che sia in linea con gli obiettivi del progetto
3. Pensa a come implementarla per tutte le piattaforme

### Come Richiedere
1. Vai su [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
2. Clicca "New Issue"
3. Seleziona "Feature Request"
4. Compila il template

## 🧪 Test

### Test Unitari
```bash
# Test Django
python manage.py test

# Test Electron (se disponibili)
npm test
```

### Test Manuali
1. **Installazione**:
   - Testa l'installer su Windows (NSIS)
   - Testa l'installer su macOS (DMG)
   - Testa l'AppImage su Linux

2. **Funzionalità**:
   - Verifica creazione/modifica DDT
   - Testa generazione PDF
   - Controlla backup automatico
   - Verifica aggiornamenti automatici

3. **Piattaforme**:
   - Windows 10/11
   - macOS 10.15+
   - Linux (Ubuntu, Fedora, Arch)

## 📚 Documentazione

### Aggiornare Documentazione
- `README.md` per informazioni generali
- `electron/README.md` per funzionalità Electron
- `installer/` per guide di installazione
- `App_details.md` per dettagli dell'applicazione
- Aggiungi commenti nel codice

### Traduzioni
- Mantieni la documentazione in italiano
- Aggiungi traduzioni in inglese se necessario

## 🔄 Processo di Review

### Per i Maintainer
1. Controlla che il codice segua le convenzioni
2. Verifica che i test passino
3. Testa manualmente su diverse piattaforme
4. Controlla la documentazione
5. Verifica che l'installer funzioni
6. Approva o richiedi modifiche

### Per i Contributor
1. Rispondi prontamente ai feedback
2. Fai le modifiche richieste
3. Aggiorna la PR se necessario
4. Sii paziente con il processo di review

## 🎯 Aree di Contribuzione

### 🐛 Bug Fixes
- Correzioni di bug esistenti
- Miglioramenti di performance
- Fix di compatibilità tra piattaforme
- Correzioni installer

### ✨ Nuove Funzionalità
- Miglioramenti UI/UX
- Nuove funzionalità Electron
- Integrazioni esterne
- Miglioramenti PDF

### 📚 Documentazione
- Miglioramenti alla documentazione
- Guide di installazione
- Esempi di utilizzo
- Video tutorial

### 🧪 Test
- Aggiunta di test unitari
- Test di integrazione
- Test cross-platform
- Test installer

### 🔧 Build e Distribuzione
- Miglioramenti GitHub Actions
- Ottimizzazioni installer
- Code signing
- Aggiornamenti automatici

## 🏆 Riconoscimenti

I contributor saranno riconosciuti in:
- README.md
- CHANGELOG.md
- Release notes
- Sezione Contributors

## 📞 Supporto

### Domande
- GitHub Discussions per domande generali
- Issues per bug e feature requests
- Email: patrik.baldon@aziendaagricola.com

### Chat
- Discord: [Link Discord]
- Telegram: [Link Telegram]

## 🚀 Build e Distribuzione

### Build Locale
```bash
# Build per tutte le piattaforme
npm run build

# Build specifico
npm run build-win    # Windows
npm run build-mac    # macOS
npm run build-linux  # Linux
```

### Distribuzione
- I file di distribuzione vengono generati automaticamente via GitHub Actions
- Creare un tag di versione: `git tag v1.1.0 && git push origin v1.1.0`
- I file saranno allegati alla Release su GitHub

## 📄 Licenza

Contribuendo a questo progetto, accetti che il tuo codice sarà distribuito sotto la licenza MIT.

---

**Grazie per il tuo contributo a DDT-Application!** 🚀

*Sviluppato da Patrik Baldon per Azienda Agricola BB&F*