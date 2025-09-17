#!/bin/bash

# DDT Manager - Script per Creazione Release
# Script per automatizzare la creazione di release su GitHub

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Funzione per verificare se git è configurato
check_git_config() {
    if ! git config user.name > /dev/null 2>&1; then
        print_error "Git non è configurato. Configura nome e email:"
        echo "git config --global user.name 'Il Tuo Nome'"
        echo "git config --global user.email 'tua@email.com'"
        exit 1
    fi
}

# Funzione per verificare se ci sono modifiche non committate
check_uncommitted_changes() {
    if ! git diff-index --quiet HEAD --; then
        print_error "Ci sono modifiche non committate. Commit o stash le modifiche prima di creare una release."
        git status
        exit 1
    fi
}

# Funzione per verificare se il tag esiste già
check_tag_exists() {
    local version=$1
    if git tag -l | grep -q "^$version$"; then
        print_error "Il tag $version esiste già."
        exit 1
    fi
}

# Funzione per aggiornare le versioni
update_versions() {
    local version=$1
    local version_number=${version#v}  # Rimuovi 'v' dal prefisso
    
    print_status "Aggiornamento versioni..."
    
    # Aggiorna package.json
    if [ -f "package.json" ]; then
        sed -i.bak "s/\"version\": \".*\"/\"version\": \"$version_number\"/" package.json
        rm package.json.bak
        print_success "package.json aggiornato"
    fi
    
    # Aggiorna electron-builder.json
    if [ -f "electron-builder.json" ]; then
        sed -i.bak "s/\"version\": \".*\"/\"version\": \"$version_number\"/" electron-builder.json
        rm electron-builder.json.bak
        print_success "electron-builder.json aggiornato"
    fi
    
    # Aggiorna installer NSIS
    if [ -f "installer/nsis/ddt-installer.nsi" ]; then
        sed -i.bak "s/!define APP_VERSION \".*\"/!define APP_VERSION \"$version_number\"/" installer/nsis/ddt-installer.nsi
        rm installer/nsis/ddt-installer.nsi.bak
        print_success "installer NSIS aggiornato"
    fi
}

# Funzione per creare il changelog
create_changelog() {
    local version=$1
    local changelog_file="CHANGELOG.md"
    
    print_status "Creazione changelog..."
    
    if [ ! -f "$changelog_file" ]; then
        touch "$changelog_file"
    fi
    
    # Crea header per la nuova versione
    local temp_file=$(mktemp)
    echo "# Changelog" > "$temp_file"
    echo "" >> "$temp_file"
    echo "## [$version] - $(date +%Y-%m-%d)" >> "$temp_file"
    echo "" >> "$temp_file"
    echo "### Added" >> "$temp_file"
    echo "- Nuove funzionalità" >> "$temp_file"
    echo "" >> "$temp_file"
    echo "### Changed" >> "$temp_file"
    echo "- Miglioramenti esistenti" >> "$temp_file"
    echo "" >> "$temp_file"
    echo "### Fixed" >> "$temp_file"
    echo "- Bug fixes" >> "$temp_file"
    echo "" >> "$temp_file"
    echo "### Security" >> "$temp_file"
    echo "- Miglioramenti di sicurezza" >> "$temp_file"
    echo "" >> "$temp_file"
    
    # Aggiungi contenuto esistente
    if [ -s "$changelog_file" ]; then
        tail -n +2 "$changelog_file" >> "$temp_file"
    fi
    
    mv "$temp_file" "$changelog_file"
    print_success "Changelog creato"
}

# Funzione per creare il commit
create_commit() {
    local version=$1
    
    print_status "Creazione commit..."
    
    git add .
    git commit -m "Release $version

- Aggiornamento versioni
- Preparazione release
- Aggiornamento changelog"
    
    print_success "Commit creato"
}

# Funzione per creare il tag
create_tag() {
    local version=$1
    
    print_status "Creazione tag $version..."
    
    git tag -a "$version" -m "Release $version"
    
    print_success "Tag $version creato"
}

# Funzione per pushare su GitHub
push_to_github() {
    local version=$1
    
    print_status "Push su GitHub..."
    
    git push origin main
    git push origin "$version"
    
    print_success "Push completato"
}

# Funzione per creare la release su GitHub
create_github_release() {
    local version=$1
    
    print_status "Creazione release su GitHub..."
    
    # Verifica se gh CLI è installato
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) non installato. Installa da: https://cli.github.com/"
        print_info "Oppure crea la release manualmente su GitHub"
        return 1
    fi
    
    # Crea la release
    gh release create "$version" \
        --title "DDT Manager $version" \
        --notes-file CHANGELOG.md \
        --latest
    
    print_success "Release GitHub creata"
}

# Funzione per mostrare le istruzioni
show_instructions() {
    local version=$1
    
    print_success "========================================"
    print_success "   Release $version Creata!"
    print_success "========================================"
    echo
    print_info "Prossimi passi:"
    echo "1. GitHub Actions creerà automaticamente gli installer"
    echo "2. Gli utenti potranno scaricare da:"
    echo "   https://github.com/PatrikBaldon/DDT-Application/releases/tag/$version"
    echo
    print_info "Per testare l'installazione:"
    echo "1. Vai su GitHub Releases"
    echo "2. Scarica DDT_Manager_Package.zip"
    echo "3. Esegui Avvio_Rapido.bat"
    echo
    print_info "Per monitorare il build:"
    echo "https://github.com/PatrikBaldon/DDT-Application/actions"
}

# Funzione principale
main() {
    print_info "========================================"
    print_info "    DDT Manager - Creazione Release"
    print_info "========================================"
    echo
    
    # Verifica argomenti
    if [ $# -eq 0 ]; then
        print_error "Uso: $0 <versione>"
        echo "Esempio: $0 v1.0.0"
        exit 1
    fi
    
    local version=$1
    
    # Verifica formato versione
    if [[ ! $version =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_error "Formato versione non valido. Usa: v1.0.0"
        exit 1
    fi
    
    print_info "Creazione release: $version"
    echo
    
    # Verifiche preliminari
    check_git_config
    check_uncommitted_changes
    check_tag_exists "$version"
    
    # Aggiorna versioni
    update_versions "$version"
    
    # Crea changelog
    create_changelog "$version"
    
    # Crea commit
    create_commit "$version"
    
    # Crea tag
    create_tag "$version"
    
    # Push su GitHub
    push_to_github "$version"
    
    # Crea release su GitHub
    create_github_release "$version"
    
    # Mostra istruzioni
    show_instructions "$version"
}

# Esegui funzione principale
main "$@"
