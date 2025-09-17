@echo off
setlocal enabledelayedexpansion

REM DDT Manager - Installer Batch per Windows
REM Script per installazione automatica con interfaccia utente

echo ========================================
echo    DDT Manager - Installer Windows
echo ========================================
echo.

REM Imposta variabili
set "APP_NAME=DDT Manager"
set "APP_VERSION=1.0.0"
set "INSTALL_DIR=%PROGRAMFILES%\DDT Manager"
set "SCRIPT_DIR=%~dp0"

echo Avvio installer %APP_NAME% v%APP_VERSION%
echo.

REM Verifica privilegi amministratore
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRORE: Questo installer richiede privilegi di amministratore
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

REM Verifica se già installato
if exist "%INSTALL_DIR%\DDT Manager.exe" (
    echo ⚠️  %APP_NAME% è già installato
    echo.
    set /p choice="Vuoi disinstallare la versione precedente? (s/n): "
    if /i "!choice!"=="s" (
        echo.
        echo Disinstallazione versione precedente...
        "%INSTALL_DIR%\Uninstall.exe" /S
        if !errorlevel! neq 0 (
            echo ❌ Errore durante la disinstallazione
            pause
            exit /b 1
        )
        echo ✅ Versione precedente disinstallata
        echo.
    ) else (
        echo Installazione annullata
        pause
        exit /b 0
    )
)

REM Verifica Python
echo 🐍 Verifica Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato
    echo.
    set /p choice="Vuoi installare Python automaticamente? (s/n): "
    if /i "!choice!"=="s" (
        echo.
        echo Installazione Python...
        powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%scripts\install-ddt.ps1" -SkipNode
        if !errorlevel! neq 0 (
            echo ❌ Errore durante l'installazione di Python
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Per installare Python manualmente:
        echo 1. Vai su https://python.org/
        echo 2. Scarica Python 3.8 o superiore
        echo 3. Installa con "Add to PATH" abilitato
        echo 4. Riavvia questo installer
        echo.
        pause
        exit /b 1
    )
) else (
    echo ✅ Python trovato
)

REM Verifica Node.js
echo 📦 Verifica Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js non trovato
    echo.
    set /p choice="Vuoi installare Node.js automaticamente? (s/n): "
    if /i "!choice!"=="s" (
        echo.
        echo Installazione Node.js...
        powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%scripts\install-ddt.ps1" -SkipPython
        if !errorlevel! neq 0 (
            echo ❌ Errore durante l'installazione di Node.js
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Per installare Node.js manualmente:
        echo 1. Vai su https://nodejs.org/
        echo 2. Scarica Node.js LTS
        echo 3. Installa con le impostazioni predefinite
        echo 4. Riavvia questo installer
        echo.
        pause
        exit /b 1
    )
) else (
    echo ✅ Node.js trovato
)

REM Verifica se l'installer NSIS esiste
if not exist "%SCRIPT_DIR%nsis\DDT_Manager_Setup.exe" (
    echo ❌ Installer NSIS non trovato
    echo.
    echo Per creare l'installer:
    echo 1. Installa NSIS (https://nsis.sourceforge.io/)
    echo 2. Esegui: makensis installer\nsis\ddt-installer.nsi
    echo 3. Riavvia questo script
    echo.
    pause
    exit /b 1
)

echo ✅ Installer NSIS trovato
echo.

REM Esegui installer NSIS
echo 🚀 Avvio installazione %APP_NAME%...
echo.
"%SCRIPT_DIR%nsis\DDT_Manager_Setup.exe"

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
    powershell -Command "& {$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%APP_NAME%.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'DDT Manager - Sistema di gestione Documenti di Trasporto'; $Shortcut.Save()}"
    echo ✅ Shortcut creato!
)

echo.
echo Premi un tasto per uscire...
pause >nul
