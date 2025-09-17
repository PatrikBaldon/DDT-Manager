#!/bin/bash

# ========================================
# DDT PWA - Aggiornamento da GitHub
# ========================================

set -e  # Exit on any error

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    DDT PWA - Update da GitHub${NC}"
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

# Backup del database
print_status "Backup database..."
if [ -f "db.sqlite3" ]; then
    backup_name="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    cp db.sqlite3 "backup/$backup_name" 2>/dev/null || mkdir -p backup && cp db.sqlite3 "backup/$backup_name"
    print_success "Backup creato: backup/$backup_name"
fi

# Controlla aggiornamenti disponibili
print_status "Controllo aggiornamenti disponibili..."
git fetch origin

# Mostra differenze
echo
print_info "Modifiche disponibili:"
git log HEAD..origin/main --oneline

# Chiedi conferma
echo
read -p "Vuoi procedere con l'aggiornamento? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Aggiornamento annullato."
    exit 0
fi

# Stash modifiche locali se presenti
if ! git diff --quiet; then
    print_status "Stash modifiche locali..."
    git stash push -m "Backup modifiche locali prima dell'aggiornamento"
fi

# Pull aggiornamenti
print_status "Download aggiornamenti..."
git pull origin main

# Installa/aggiorna dipendenze
print_status "Aggiornamento dipendenze..."
pip install -r requirements.txt --upgrade

# Esegui migrazioni
print_status "Esecuzione migrazioni..."
python manage.py migrate

# Test PWA
print_status "Test configurazione PWA..."
if [ -f "pwa/scripts/test_pwa.py" ]; then
    python pwa/scripts/test_pwa.py
fi

print_success "========================================${NC}"
print_success "   Aggiornamento completato!${NC}"
print_success "========================================${NC}"
echo
print_info "Per avviare il server:"
print_info "  python manage.py runserver"
echo


