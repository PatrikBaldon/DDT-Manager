@echo off
echo.
echo ========================================
echo    DDT Manager - Avvio Applicazione
echo ========================================
echo.

:: Verifica se l'applicazione è già in esecuzione
tasklist /FI "IMAGENAME eq DDT Manager.exe" 2>NUL | find /I "DDT Manager.exe" >NUL
if %errorLevel% == 0 (
    echo ⚠️  DDT Manager è già in esecuzione
    echo    Chiudere l'applicazione esistente e riprovare
    pause
    exit /b 1
)

:: Verifica se le dipendenze sono installate
if not exist "node_modules" (
    echo ❌ Dipendenze Node.js non trovate
    echo    Eseguire prima install.bat
    pause
    exit /b 1
)

if not exist "venv" (
    echo ❌ Ambiente virtuale Python non trovato
    echo    Eseguire prima install.bat
    pause
    exit /b 1
)

echo 🚀 Avvio DDT Manager...
echo.

:: Avvia l'applicazione
npm run electron

if %errorLevel% neq 0 (
    echo.
    echo ❌ Errore durante l'avvio dell'applicazione
    echo    Controllare i log per maggiori dettagli
    pause
)
