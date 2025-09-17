#!/bin/bash

# ========================================
# DDT PWA - Setup Git Repository
# ========================================

set -e  # Exit on any error

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    DDT PWA - Setup Git${NC}"
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

# Verifica se git è installato
if ! command -v git &> /dev/null; then
    print_error "Git non installato! Installa Git da https://git-scm.com/"
    exit 1
fi

# Inizializza repository se non esiste
if [ ! -d ".git" ]; then
    print_status "Inizializzazione repository Git..."
    git init
    print_success "Repository Git inizializzato!"
fi

# Configura Git se non configurato
if ! git config user.name &> /dev/null; then
    print_status "Configurazione Git..."
    read -p "Inserisci il tuo nome: " user_name
    read -p "Inserisci la tua email: " user_email
    git config user.name "$user_name"
    git config user.email "$user_email"
    print_success "Git configurato!"
fi

# Aggiungi remote origin se non esiste
if ! git remote get-url origin &> /dev/null; then
    print_status "Configurazione remote GitHub..."
    read -p "Inserisci l'URL del repository GitHub (es. https://github.com/username/DDT-Application.git): " github_url
    git remote add origin "$github_url"
    print_success "Remote GitHub configurato!"
fi

# Crea .gitignore se non esiste
if [ ! -f ".gitignore" ]; then
    print_status "Creazione .gitignore..."
    # Il file .gitignore è già stato creato
    print_success ".gitignore creato!"
fi

# Aggiungi tutti i file
print_status "Aggiunta file al repository..."
git add .

# Commit iniziale
print_status "Creazione commit iniziale..."
git commit -m "feat: setup iniziale DDT PWA con installer Windows"

# Push su GitHub
print_status "Push su GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    print_success "========================================${NC}"
    print_success "   Setup Git completato!${NC}"
    print_success "========================================${NC}"
    echo
    print_info "Repository configurato e sincronizzato con GitHub"
    print_info "Per sincronizzare modifiche future:"
    print_info "  ./scripts/sync_to_github.sh"
    echo
else
    print_error "Errore nel push su GitHub!"
    print_info "Verifica che il repository GitHub esista e che tu abbia i permessi"
    exit 1
fi


