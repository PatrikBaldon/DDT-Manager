@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    DDT Application - INSTALLER
echo ========================================
echo.
echo Installazione di DDT Application v1.0.0
echo.

REM Controlla privilegi amministratore
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Questo installer deve essere eseguito come amministratore
    echo Clicca destro sull'installer e seleziona "Esegui come amministratore"
    pause
    exit /b 1
)

echo ✅ Privilegi amministratore verificati
echo.

REM Crea directory di installazione
if not exist "%PROGRAMFILES%\DDT Application" (
    mkdir "%PROGRAMFILES%\DDT Application"
    echo ✅ Directory di installazione creata
) else (
    echo ⚠️  Directory di installazione già esistente
)

echo.

REM Copia file applicazione
echo Copia file applicazione...
xcopy /E /I /Y "app" "%PROGRAMFILES%\DDT Application\app"
xcopy /E /I /Y "scripts" "%PROGRAMFILES%\DDT Application\scripts"
copy "README.md" "%PROGRAMFILES%\DDT Application\"
copy "LICENSE" "%PROGRAMFILES%\DDT Application\"
copy "requirements.txt" "%PROGRAMFILES%\DDT Application\"
echo ✅ File applicazione copiati
echo.

REM Crea collegamento desktop
echo Creazione collegamento desktop...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\DDT Application.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\DDT Application\scripts\start_ddt.bat'; $Shortcut.WorkingDirectory = '%PROGRAMFILES%\DDT Application'; $Shortcut.Description = 'DDT Application'; $Shortcut.Save()}"
echo ✅ Collegamento desktop creato
echo.

REM Crea collegamento Start Menu
echo Creazione collegamento Start Menu...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs"
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\DDT Application.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\DDT Application\scripts\start_ddt.bat'; $Shortcut.WorkingDirectory = '%PROGRAMFILES%\DDT Application'; $Shortcut.Description = 'DDT Application'; $Shortcut.Save()}"
echo ✅ Collegamento Start Menu creato
echo.

REM Crea file di versione
echo 1.0.0 > "%PROGRAMFILES%\DDT Application\version.txt"
echo ✅ File versione creato
echo.

REM Configura associazione file .ddt
echo Configurazione associazione file .ddt...
reg add "HKEY_CLASSES_ROOT\.ddt" /ve /d "DDTApplication" /f >nul
reg add "HKEY_CLASSES_ROOT\DDTApplication" /ve /d "DDT Application" /f >nul
reg add "HKEY_CLASSES_ROOT\DDTApplication\DefaultIcon" /ve /d "%PROGRAMFILES%\DDT Application\app\logo1.png" /f >nul
reg add "HKEY_CLASSES_ROOT\DDTApplication\shell\open\command" /ve /d "\"%PROGRAMFILES%\DDT Application\scripts\start_ddt.bat\" \"%1\"" /f >nul
echo ✅ Associazione file .ddt configurata
echo.

REM Copia script di avvio
echo Copia script di avvio...
if exist "scripts\start_ddt.bat" (
    copy "scripts\start_ddt.bat" "%PROGRAMFILES%\DDT Application\scripts\"
    echo ✅ Script di avvio copiato
) else (
    echo ⚠️  AVVISO: Script start_ddt.bat non trovato
)
echo.

REM Crea script di aggiornamento
echo Creazione script di aggiornamento...
(
echo @echo off
echo cd /d "%PROGRAMFILES%\DDT Application\scripts"
echo call update_ddt.bat
) > "%PROGRAMFILES%\DDT Application\scripts\update.bat"
echo ✅ Script di aggiornamento creato
echo.

echo ========================================
echo    INSTALLAZIONE COMPLETATA!
echo ========================================
echo.
echo 🎉 DDT Application è stato installato con successo!
echo.
echo 📍 Directory di installazione: %PROGRAMFILES%\DDT Application
echo 🖥️  Collegamento desktop: %USERPROFILE%\Desktop\DDT Application.lnk
echo 📱 Start Menu: %APPDATA%\Microsoft\Windows\Start Menu\Programs\DDT Application.lnk
echo.
echo 🚀 Per avviare l'applicazione:
echo   - Doppio clic su "DDT Application" dal desktop
echo   - Oppure dal menu Start
echo.
echo 🔄 Per aggiornare l'applicazione:
echo   - Esegui update_ddt.bat dalla directory di installazione
echo.
echo Buon lavoro con la tua applicazione DDT! 🌱
echo.
pause
