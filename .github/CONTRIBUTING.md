# 🤝 Contribuire a DDT Electron App

Grazie per il tuo interesse a contribuire a DDT Electron App! Questo documento ti guiderà attraverso il processo di contribuzione.

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

# Crea superuser
python manage.py createsuperuser

# Avvia applicazione Electron
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
# Esegui test
python manage.py test

# Test PWA
python pwa/scripts/test_pwa.py

# Controlla stile codice
flake8 .
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
- Usa Python 3.11+
- Segui PEP 8
- Aggiungi docstring alle funzioni
- Usa type hints quando possibile

### PWA
- Testa sempre le funzionalità offline
- Verifica la compatibilità con Chrome/Edge
- Controlla che il Service Worker funzioni correttamente

## 🐛 Segnalazione Bug

### Prima di Segnalare
1. Controlla se il bug è già stato segnalato
2. Verifica di usare l'ultima versione
3. Prova a riprodurre il bug

### Come Segnalare
1. Vai su [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
2. Clicca "New Issue"
3. Seleziona "Bug Report"
4. Compila il template

## 💡 Richieste di Funzionalità

### Prima di Richiedere
1. Controlla se la funzionalità è già stata richiesta
2. Verifica che sia in linea con gli obiettivi del progetto
3. Pensa a come implementarla

### Come Richiedere
1. Vai su [Issues](https://github.com/PatrikBaldon/DDT-Application/issues)
2. Clicca "New Issue"
3. Seleziona "Feature Request"
4. Compila il template

## 🧪 Test

### Test Unitari
```bash
python manage.py test
```

### Test PWA
```bash
python pwa/scripts/test_pwa.py
```

### Test Manuali
1. Testa l'installazione su Windows
2. Verifica funzionalità offline
3. Controlla sincronizzazione dati
4. Testa aggiornamenti automatici

## 📚 Documentazione

### Aggiornare Documentazione
- README.md per informazioni generali
- PWA_README.md per funzionalità PWA
- installer/README_Installazione.md per installazione Windows
- Aggiungi commenti nel codice

### Traduzioni
- Mantieni la documentazione in italiano
- Aggiungi traduzioni in inglese se necessario

## 🔄 Processo di Review

### Per i Maintainer
1. Controlla che il codice segua le convenzioni
2. Verifica che i test passino
3. Testa manualmente le funzionalità
4. Controlla la documentazione
5. Approva o richiedi modifiche

### Per i Contributor
1. Rispondi prontamente ai feedback
2. Fai le modifiche richieste
3. Aggiorna la PR se necessario
4. Sii paziente con il processo di review

## 🎯 Aree di Contribuzione

### 🐛 Bug Fixes
- Correzioni di bug esistenti
- Miglioramenti di performance
- Fix di compatibilità

### ✨ Nuove Funzionalità
- Miglioramenti UI/UX
- Nuove funzionalità PWA
- Integrazioni esterne

### 📚 Documentazione
- Miglioramenti alla documentazione
- Guide di installazione
- Esempi di utilizzo

### 🧪 Test
- Aggiunta di test unitari
- Test di integrazione
- Test PWA

## 🏆 Riconoscimenti

I contributor saranno riconosciuti in:
- README.md
- CHANGELOG.md
- Release notes

## 📞 Supporto

### Domande
- GitHub Discussions per domande generali
- Issues per bug e feature requests
- Email: supporto@ddt-app.com

### Chat
- Discord: [Link Discord]
- Telegram: [Link Telegram]

## 📄 Licenza

Contribuendo a questo progetto, accetti che il tuo codice sarà distribuito sotto la licenza MIT.

---

**Grazie per il tuo contributo a DDT PWA!** 🚀