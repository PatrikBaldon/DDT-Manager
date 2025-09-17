#!/bin/bash

# ========================================
# DDT Electron App - Script di Sviluppo per Mac
# ========================================

set -e  # Exit on any error

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    DDT Electron App - Sviluppo Mac${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Funzione per stampare messaggi colorati
print_status() {
    echo -e "${YELLOW}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_info() {
    echo -e "${BLUE}$1${NC}"
}

# Verifica se siamo nella directory corretta
if [ ! -f "manage.py" ]; then
    print_error "Errore: Esegui questo script dalla directory root del progetto DDT"
    exit 1
fi

# Verifica se Node.js è installato
if ! command -v node &> /dev/null; then
    print_error "Node.js non trovato! Installa Node.js"
    print_info "Visita: https://nodejs.org/"
    exit 1
fi

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    print_error "Python3 non trovato! Installa Python3"
    print_info "Visita: https://python.org/"
    exit 1
fi

print_success "Node.js e Python3 trovati!"

# Installa dipendenze Python
print_status "Installazione dipendenze Python..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dipendenze Python installate!"
else
    print_error "Errore nell'installazione delle dipendenze Python!"
    exit 1
fi

# Installa dipendenze Node.js
print_status "Installazione dipendenze Node.js..."
npm install
if [ $? -eq 0 ]; then
    print_success "Dipendenze Node.js installate!"
else
    print_error "Errore nell'installazione delle dipendenze Node.js!"
    exit 1
fi

# Esegui migrazioni
print_status "Esecuzione migrazioni database..."
python manage.py migrate
if [ $? -eq 0 ]; then
    print_success "Migrazioni completate!"
else
    print_error "Errore nelle migrazioni!"
    exit 1
fi

# Crea superuser se non esiste
print_status "Configurazione utente amministratore..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ddt.local', 'admin123')
    print('Superuser creato: admin/admin123')
else:
    print('Superuser già esistente')
"

# Test Electron
print_status "Test configurazione Electron..."
if [ -f "electron/test.js" ]; then
    node electron/test.js
    if [ $? -eq 0 ]; then
        print_success "Test Electron superati!"
    else
        print_error "Test Electron falliti!"
    fi
fi

# Setup completato
print_success "========================================${NC}"
print_success "   Setup completato con successo!${NC}"
print_success "========================================${NC}"
echo
print_info "Per avviare l'applicazione Electron:"
print_info "  ./scripts/start-electron.sh"
print_info "  oppure"
print_info "  npm run electron-dev"
echo
print_info "Per avviare solo il server Django:"
print_info "  python3 manage.py runserver"
echo
print_info "Per sincronizzare con GitHub:"
print_info "  ./scripts/sync_to_github.sh"
echo

# Chiedi se avviare l'applicazione
read -p "Vuoi avviare l'applicazione Electron ora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Avvio applicazione Electron..."
    npm run electron-dev
fi


