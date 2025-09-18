#!/bin/bash

echo ""
echo "========================================"
echo "   DDT Manager - Installazione Linux"
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

# Rileva la distribuzione Linux
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    elif [ -f /etc/redhat-release ]; then
        DISTRO="rhel"
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
    else
        DISTRO="unknown"
    fi
    
    print_info "Distribuzione rilevata: $DISTRO $VERSION"
}

# Installa dipendenze di sistema
install_system_deps() {
    print_info "Installazione dipendenze di sistema..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv nodejs npm curl wget build-essential
            ;;
        fedora|rhel|centos)
            sudo dnf install -y python3 python3-pip nodejs npm curl wget gcc gcc-c++ make
            ;;
        arch|manjaro)
            sudo pacman -S --noconfirm python python-pip nodejs npm curl wget base-devel
            ;;
        opensuse*)
            sudo zypper install -y python3 python3-pip nodejs npm curl wget gcc gcc-c++ make
            ;;
        *)
            print_warning "Distribuzione non supportata: $DISTRO"
            print_info "Assicurati di avere installato:"
            print_info "  - Python 3.8+"
            print_info "  - pip3"
            print_info "  - Node.js 16+"
            print_info "  - npm"
            print_info "  - build-essential (gcc, make, etc.)"
            ;;
    esac
}

# Verifica Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python trovato - Versione: $PYTHON_VERSION"
        return 0
    else
        print_error "Python3 non trovato"
        print_info "Installa Python3 con il gestore pacchetti della tua distribuzione"
        return 1
    fi
}

# Verifica Node.js
check_nodejs() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js trovato - Versione: $NODE_VERSION"
        return 0
    else
        print_error "Node.js non trovato"
        print_info "Installa Node.js con il gestore pacchetti della tua distribuzione"
        return 1
    fi
}

# Verifica pip
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_status "pip3 trovato"
        return 0
    else
        print_error "pip3 non trovato"
        print_info "Installa pip3 con il gestore pacchetti della tua distribuzione"
        return 1
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

# Crea desktop file per il menu applicazioni
create_desktop_file() {
    print_info "Creazione file desktop..."
    
    DESKTOP_FILE="$HOME/.local/share/applications/ddt-manager.desktop"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DDT Manager
Comment=Sistema di gestione Documenti di Trasporto
Exec=$PWD/start_ddt.sh
Icon=$PWD/static/images/icons/icon-512x512.png
Terminal=false
Categories=Office;Business;
StartupWMClass=DDT Manager
EOF

    chmod +x "$DESKTOP_FILE"
    print_status "File desktop creato: $DESKTOP_FILE"
}

# Crea shortcut sul desktop
create_desktop_shortcut() {
    print_info "Creazione shortcut sul desktop..."
    
    SHORTCUT_FILE="$HOME/Desktop/DDT Manager.desktop"
    
    cat > "$SHORTCUT_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DDT Manager
Comment=Sistema di gestione Documenti di Trasporto
Exec=$PWD/start_ddt.sh
Icon=$PWD/static/images/icons/icon-512x512.png
Terminal=false
Categories=Office;Business;
StartupWMClass=DDT Manager
EOF

    chmod +x "$SHORTCUT_FILE"
    print_status "Shortcut desktop creato: $SHORTCUT_FILE"
}

# Funzione principale
main() {
    echo "🔍 Rilevamento sistema..."
    detect_distro
    
    echo ""
    echo "📦 Installazione dipendenze di sistema..."
    install_system_deps
    
    echo ""
    echo "🔍 Verifica prerequisiti..."
    check_python || exit 1
    check_pip || exit 1
    check_nodejs || exit 1
    
    echo ""
    echo "📦 Installazione dipendenze applicazione..."
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
    
    # Crea script di avvio e shortcut
    create_launcher || exit 1
    create_desktop_file || exit 1
    create_desktop_shortcut || exit 1
    
    echo ""
    echo "🎉 Installazione completata con successo!"
    echo ""
    echo "💡 Per avviare l'applicazione:"
    echo "   - Doppio click su 'DDT Manager' sul desktop"
    echo "   - Oppure cerca 'DDT Manager' nel menu applicazioni"
    echo "   - Oppure esegui: ./start_ddt.sh"
    echo ""
    echo "🚀 Avvio dell'applicazione..."
    echo ""
    
    # Avvia l'applicazione
    ./start_ddt.sh
}

# Esegui installazione
main
