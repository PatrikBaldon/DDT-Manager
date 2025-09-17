@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    DDT ELECTRON APP - AVVIO
echo ========================================
echo.

REM Imposta variabili
set "APP_NAME=DDT Manager"
set "APP_DIR=%~dp0"

echo Avvio %APP_NAME% (Applicazione Electron)
echo.

REM Controlla se Node.js è installato
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Node.js non è installato
    echo.
    echo Per installare Node.js:
    echo 1. Vai su https://nodejs.org/
    echo 2. Scarica e installa Node.js LTS
    echo 3. Riavvia il computer
    echo 4. Esegui di nuovo questo script
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js trovato

REM Controlla se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Python non è installato
    echo.
    echo Per installare Python:
    echo 1. Vai su https://python.org/
    echo 2. Scarica e installa Python 3.8+
    echo 3. Riavvia il computer
    echo 4. Esegui di nuovo questo script
    echo.
    pause
    exit /b 1
)

echo ✅ Python trovato

REM Cambia directory
cd /d "%APP_DIR%.."

echo.
echo ========================================
echo    INSTALLAZIONE DIPENDENZE
echo ========================================

echo Installazione dipendenze Node.js...
call npm install
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Impossibile installare le dipendenze Node.js
    pause
    exit /b 1
)

echo Installazione dipendenze Python...
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Impossibile installare le dipendenze Python
    pause
    exit /b 1
)

echo ✅ Dipendenze installate

echo.
echo ========================================
echo    AVVIO APPLICAZIONE ELECTRON
echo ========================================

echo Avvio applicazione Electron...
call npm run electron-dev

echo.
echo ========================================
echo    APPLICAZIONE AVVIATA!
echo ========================================
echo.
echo 🎉 %APP_NAME% è stato avviato con successo!
echo.
echo 💻 Applicazione Electron: Si aprirà automaticamente
echo 🌐 Server Django: http://localhost:8000
echo 📊 Admin: http://localhost:8000/admin
echo.
echo ⚠️  Per fermare l'applicazione:
echo    - Chiudi la finestra dell'applicazione
echo    - Oppure premi Ctrl+C in questa finestra
echo.
echo Buon lavoro con la tua applicazione DDT! 🌱
echo.
pause
