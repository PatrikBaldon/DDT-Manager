#!/bin/bash

# Script per avviare l'applicazione Electron in modalità sviluppo

echo "🚀 Avvio DDT Manager - Applicazione Electron"
echo "=============================================="

# Controlla se Node.js è installato
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non trovato. Installa Node.js prima di continuare."
    echo "   Visita: https://nodejs.org/"
    exit 1
fi

# Controlla se npm è installato
if ! command -v npm &> /dev/null; then
    echo "❌ npm non trovato. Installa npm prima di continuare."
    exit 1
fi

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installa Python3 prima di continuare."
    exit 1
fi

# Controlla se Django è installato
if ! python3 -c "import django" &> /dev/null; then
    echo "❌ Django non trovato. Installa le dipendenze Python:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Installa le dipendenze Node.js se necessario
if [ ! -d "node_modules" ]; then
    echo "📦 Installazione dipendenze Node.js..."
    npm install
fi

# Crea la directory dist se non esiste
mkdir -p dist

# Avvia l'applicazione in modalità sviluppo
echo "🔧 Avvio in modalità sviluppo..."
echo "   - Server Django: http://localhost:8000"
echo "   - Applicazione Electron: Si aprirà automaticamente"
echo ""
echo "💡 Suggerimenti:"
echo "   - Premi Ctrl+C per fermare l'applicazione"
echo "   - Premi F12 per aprire gli strumenti di sviluppo"
echo ""

# Avvia l'applicazione
npm run electron-dev
