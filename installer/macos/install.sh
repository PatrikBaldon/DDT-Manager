#!/bin/bash

echo ""
echo "========================================"
echo "   DDT Manager - Installazione macOS"
echo "========================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verifica se Homebrew è installato
check_homebrew() {
    if command -v brew &> /dev/null; then
        print_status "Homebrew trovato"
        return 0
    else
        print_warning "Homebrew non trovato"
        echo ""
        print_info "Installazione di Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Aggiungi Homebrew al PATH se necessario
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        
        if command -v brew &> /dev/null; then
            print_status "Homebrew installato con successo"
            return 0
        else
            print_error "Installazione di Homebrew fallita"
            return 1
        fi
    fi
}

# Verifica e installa Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python trovato - Versione: $PYTHON_VERSION"
        return 0
    else
        print_warning "Python3 non trovato"
        print_info "Installazione di Python tramite Homebrew..."
        brew install python
        
        if command -v python3 &> /dev/null; then
            print_status "Python installato con successo"
            return 0
        else
            print_error "Installazione di Python fallita"
            return 1
        fi
    fi
}

# Verifica e installa Node.js
check_nodejs() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js trovato - Versione: $NODE_VERSION"
        return 0
    else
        print_warning "Node.js non trovato"
        print_info "Installazione di Node.js tramite Homebrew..."
        brew install node
        
        if command -v node &> /dev/null; then
            print_status "Node.js installato con successo"
            return 0
        else
            print_error "Installazione di Node.js fallita"
            return 1
        fi
    fi
}

# Verifica se pip è installato
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_status "pip3 trovato"
        return 0
    else
        print_warning "pip3 non trovato"
        print_info "Installazione di pip..."
        python3 -m ensurepip --upgrade
        
        if command -v pip3 &> /dev/null; then
            print_status "pip3 installato con successo"
            return 0
        else
            print_error "Installazione di pip fallita"
            return 1
        fi
    fi
}

# Crea ambiente virtuale Python
create_venv() {
    if [ ! -d "venv" ]; then
        print_info "Creazione ambiente virtuale Python..."
        python3 -m venv venv
        
        if [ -d "venv" ]; then
            print_status "Ambiente virtuale creato"
        else
            print_error "Creazione ambiente virtuale fallita"
            return 1
        fi
    else
        print_status "Ambiente virtuale già esistente"
    fi
    
    # Attiva l'ambiente virtuale
    source venv/bin/activate
    print_status "Ambiente virtuale attivato"
}

# Installa dipendenze Python
install_python_deps() {
    print_info "Installazione dipendenze Python..."
    pip3 install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_status "Dipendenze Python installate"
    else
        print_error "Installazione dipendenze Python fallita"
        return 1
    fi
}

# Installa dipendenze Node.js
install_node_deps() {
    print_info "Installazione dipendenze Node.js..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_status "Dipendenze Node.js installate"
    else
        print_error "Installazione dipendenze Node.js fallita"
        return 1
    fi
}

# Configura database Django
setup_django() {
    print_info "Configurazione database Django..."
    python3 manage.py migrate
    
    if [ $? -eq 0 ]; then
        print_status "Database configurato"
    else
        print_error "Configurazione database fallita"
        return 1
    fi
    
    print_info "Raccolta file statici..."
    python3 manage.py collectstatic --noinput
    
    if [ $? -eq 0 ]; then
        print_status "File statici raccolti"
    else
        print_error "Raccolta file statici fallita"
        return 1
    fi
}

# Crea script di avvio
create_launcher() {
    print_info "Creazione script di avvio..."
    
    cat > start_ddt.sh << 'EOF'
#!/bin/bash

echo ""
echo "========================================"
echo "   DDT Manager - Avvio Applicazione"
echo "========================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verifica se l'applicazione è già in esecuzione
if pgrep -f "DDT Manager" > /dev/null; then
    print_warning "DDT Manager è già in esecuzione"
    echo "   Chiudere l'applicazione esistente e riprovare"
    exit 1
fi

# Verifica dipendenze
if [ ! -d "node_modules" ]; then
    print_error "Dipendenze Node.js non trovate"
    echo "   Eseguire prima install.sh"
    exit 1
fi

if [ ! -d "venv" ]; then
    print_error "Ambiente virtuale Python non trovato"
    echo "   Eseguire prima install.sh"
    exit 1
fi

# Attiva ambiente virtuale
source venv/bin/activate

print_status "Avvio DDT Manager..."
echo ""

# Avvia l'applicazione
npm run electron

if [ $? -ne 0 ]; then
    echo ""
    print_error "Errore durante l'avvio dell'applicazione"
    echo "   Controllare i log per maggiori dettagli"
fi
EOF

    chmod +x start_ddt.sh
    print_status "Script di avvio creato"
}

# Crea alias per il desktop
create_desktop_alias() {
    print_info "Creazione alias per il desktop..."
    
    # Crea un alias nell'Applications folder
    cat > "/Applications/DDT Manager.command" << EOF
#!/bin/bash
cd "$(dirname "$0")/../Desktop/Azienda_Agricola_BB&F/DDT"
./start_ddt.sh
EOF
    
    chmod +x "/Applications/DDT Manager.command"
    print_status "Alias creato in Applications"
}

# Funzione principale
main() {
    echo "🔍 Verifica prerequisiti..."
    echo ""
    
    # Verifica e installa prerequisiti
    check_homebrew || exit 1
    check_python || exit 1
    check_pip || exit 1
    check_nodejs || exit 1
    
    echo ""
    echo "📦 Installazione dipendenze..."
    echo ""
    
    # Crea ambiente virtuale e installa dipendenze
    create_venv || exit 1
    install_python_deps || exit 1
    install_node_deps || exit 1
    
    echo ""
    echo "🔧 Configurazione applicazione..."
    echo ""
    
    # Configura Django
    setup_django || exit 1
    
    echo ""
    echo "🚀 Creazione script di avvio..."
    echo ""
    
    # Crea script di avvio
    create_launcher || exit 1
    create_desktop_alias || exit 1
    
    echo ""
    echo "🎉 Installazione completata con successo!"
    echo ""
    echo "💡 Per avviare l'applicazione:"
    echo "   - Doppio click su 'DDT Manager' in Applications"
    echo "   - Oppure esegui: ./start_ddt.sh"
    echo ""
    echo "🚀 Avvio dell'applicazione..."
    echo ""
    
    # Avvia l'applicazione
    ./start_ddt.sh
}

# Esegui installazione
main
