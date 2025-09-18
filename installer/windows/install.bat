@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    DDT Manager - Installazione Windows
echo ========================================
echo.

:: Controlla se l'utente ha privilegi di amministratore
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Privilegi di amministratore rilevati
) else (
    echo ⚠️  Attenzione: L'installazione potrebbe richiedere privilegi di amministratore
    echo    per installare le dipendenze di sistema
)

:: Verifica se Python è installato
echo.
echo 🔍 Verifica prerequisiti...
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Python trovato
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo    Versione: !PYTHON_VERSION!
) else (
    echo ❌ Python non trovato
    echo.
    echo 📥 Download e installazione di Python...
    echo    Verrà aperto il browser per scaricare Python
    start https://www.python.org/downloads/
    echo.
    echo ⏳ Attendere il completamento dell'installazione di Python, poi premere un tasto...
    pause >nul
    goto :check_python_again
)

:check_python_again
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python ancora non trovato. Installazione fallita.
    pause
    exit /b 1
)

:: Verifica se pip è installato
pip --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ pip trovato
) else (
    echo ❌ pip non trovato. Installazione di pip...
    python -m ensurepip --upgrade
)

:: Verifica se Node.js è installato
node --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Node.js trovato
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo    Versione: !NODE_VERSION!
) else (
    echo ❌ Node.js non trovato
    echo.
    echo 📥 Download e installazione di Node.js...
    echo    Verrà aperto il browser per scaricare Node.js
    start https://nodejs.org/
    echo.
    echo ⏳ Attendere il completamento dell'installazione di Node.js, poi premere un tasto...
    pause >nul
    goto :check_node_again
)

:check_node_again
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Node.js ancora non trovato. Installazione fallita.
    pause
    exit /b 1
)

:: Verifica se npm è installato
npm --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ npm trovato
) else (
    echo ❌ npm non trovato. Installazione di npm...
    node -e "console.log('npm dovrebbe essere incluso con Node.js')"
)

echo.
echo 📦 Installazione dipendenze Python...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ❌ Errore durante l'installazione delle dipendenze Python
    pause
    exit /b 1
)

echo.
echo 📦 Installazione dipendenze Node.js...
npm install
if %errorLevel% neq 0 (
    echo ❌ Errore durante l'installazione delle dipendenze Node.js
    pause
    exit /b 1
)

echo.
echo 🔧 Configurazione database...
python manage.py migrate
if %errorLevel% neq 0 (
    echo ❌ Errore durante la configurazione del database
    pause
    exit /b 1
)

echo.
echo 📁 Raccolta file statici...
python manage.py collectstatic --noinput
if %errorLevel% neq 0 (
    echo ❌ Errore durante la raccolta dei file statici
    pause
    exit /b 1
)

echo.
echo 🎉 Installazione completata con successo!
echo.
echo 🚀 Avvio dell'applicazione...
echo.

:: Crea uno script di avvio
echo @echo off > start_ddt.bat
echo echo Avvio DDT Manager... >> start_ddt.bat
echo npm run electron >> start_ddt.bat

:: Avvia l'applicazione
npm run electron

echo.
echo 👋 Grazie per aver utilizzato DDT Manager!
pause
