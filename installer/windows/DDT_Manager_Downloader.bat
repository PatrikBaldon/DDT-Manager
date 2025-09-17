@echo off
setlocal enabledelayedexpansion

REM DDT Manager - Downloader e Installer Automatico
REM Script per scaricare e installare l'ultima versione da GitHub

echo ========================================
echo    DDT Manager - Downloader Automatico
echo ========================================
echo.

REM Imposta variabili
set "APP_NAME=DDT Manager"
set "GITHUB_REPO=PatrikBaldon/DDT-Application"
set "SCRIPT_DIR=%~dp0"

echo Avvio downloader %APP_NAME%
echo.

REM Verifica privilegi amministratore
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Questo script richiede privilegi di amministratore
    echo.
    echo Per installare %APP_NAME%:
    echo 1. Clicca destro su questo file
    echo 2. Seleziona "Esegui come amministratore"
    echo 3. Conferma quando richiesto
    echo.
    pause
    exit /b 1
)

echo ✅ Privilegi amministratore verificati
echo.

REM Verifica se PowerShell è disponibile
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRORE: PowerShell non disponibile
    echo.
    echo Per installare %APP_NAME%:
    echo 1. Installa PowerShell 5.0 o superiore
    echo 2. Riavvia questo script
    echo.
    pause
    exit /b 1
)

echo ✅ PowerShell disponibile
echo.

REM Verifica se già installato
if exist "%PROGRAMFILES%\DDT Manager\DDT Manager.exe" (
    echo ⚠️  %APP_NAME% è già installato
    echo.
    set /p choice="Vuoi aggiornare alla versione più recente? (s/n): "
    if /i "!choice!"=="s" (
        echo.
        echo Disinstallazione versione precedente...
        "%PROGRAMFILES%\DDT Manager\Uninstall.exe" /S
        if !errorlevel! neq 0 (
            echo ❌ Errore durante la disinstallazione
            pause
            exit /b 1
        )
        echo ✅ Versione precedente disinstallata
        echo.
    ) else (
        echo Aggiornamento annullato
        pause
        exit /b 0
    )
)

REM Esegui script PowerShell di download e installazione
echo 🚀 Avvio download e installazione %APP_NAME%...
echo.
echo Questo processo includerà:
echo   - Download dell'ultima versione da GitHub
echo   - Verifica e installazione di Python (se necessario)
echo   - Verifica e installazione di Node.js (se necessario)
echo   - Installazione di %APP_NAME%
echo   - Creazione shortcut sul desktop
echo.

powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%scripts\download-and-install.ps1"

if %errorlevel% neq 0 (
    echo ❌ Errore durante l'installazione
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installazione Completata!
echo ========================================
echo.
echo 🎉 %APP_NAME% è stato installato con successo!
echo.
echo Per avviare %APP_NAME%:
echo   - Clicca sull'icona sul desktop
echo   - Oppure vai in Start Menu ^> %APP_NAME%
echo.
echo Per disinstallare:
echo   - Vai in Pannello di Controllo ^> Programmi
echo   - Oppure esegui: Uninstall-DDTManager
echo.
echo Buon lavoro con la tua applicazione DDT! 🌱
echo.

REM Crea shortcut sul desktop se non esiste
if not exist "%USERPROFILE%\Desktop\%APP_NAME%.lnk" (
    echo 🔗 Creazione shortcut desktop...
    powershell -Command "& {$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\%APP_NAME%\%APP_NAME%.exe'; $Shortcut.WorkingDirectory = '%PROGRAMFILES%\%APP_NAME%'; $Shortcut.Description = 'DDT Manager - Sistema di gestione Documenti di Trasporto'; $Shortcut.Save()}"
    echo ✅ Shortcut creato!
)

echo.
echo Premi un tasto per uscire...
pause >nul
