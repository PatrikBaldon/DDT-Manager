#!/bin/bash

# ========================================
# DDT PWA - Sincronizzazione con GitHub
# ========================================

set -e  # Exit on any error

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    DDT PWA - Sync GitHub${NC}"
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

# Verifica se git è configurato
if ! git config user.name &> /dev/null; then
    print_error "Git non configurato! Configura nome e email:"
    print_info "git config --global user.name 'Il Tuo Nome'"
    print_info "git config --global user.email 'tua@email.com'"
    exit 1
fi

# Verifica stato del repository
print_status "Controllo stato repository..."
git status --porcelain

# Chiedi conferma per il commit
echo
read -p "Vuoi procedere con il commit e push? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Operazione annullata."
    exit 0
fi

# Aggiungi tutti i file modificati
print_status "Aggiunta file modificati..."
git add .

# Commit con messaggio
print_status "Creazione commit..."
if [ -z "$1" ]; then
    # Se non è stato fornito un messaggio, chiedi all'utente
    read -p "Inserisci messaggio commit: " commit_message
else
    commit_message="$1"
fi

git commit -m "$commit_message"

# Push su GitHub
print_status "Push su GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    print_success "========================================${NC}"
    print_success "   Sincronizzazione completata!${NC}"
    print_success "========================================${NC}"
    echo
    print_info "Le modifiche sono ora disponibili su GitHub"
    print_info "Gli utenti Windows possono aggiornare l'app con:"
    print_info "  DDT_PWA_Update.bat"
    echo
else
    print_error "Errore nel push su GitHub!"
    exit 1
fi


