@echo off
echo Avvio DDT Manager...
echo.
echo Se questo e' il primo avvio, potrebbe richiedere alcuni minuti
echo per scaricare e installare le dipendenze necessarie.
echo.
echo Premi un tasto per continuare...
pause >nul

cd /d "%~dp0"
"DDT Manager.exe"

if %errorlevel% neq 0 (
    echo.
    echo ERRORE: Impossibile avviare DDT Manager
    echo.
    echo Possibili soluzioni:
    echo 1. Assicurati di avere Python 3.8+ installato
    echo 2. Assicurati di avere Node.js 16+ installato
    echo 3. Esegui questo file come amministratore
    echo 4. Controlla che Windows Defender non blocchi l'applicazione
    echo.
    pause
)
