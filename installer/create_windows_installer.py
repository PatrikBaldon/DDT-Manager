#!/usr/bin/env python3
"""
DDT Application - Create Windows Installer
Versione: 1.0.0

Script per creare un installer Windows semplice
"""

import os
import zipfile
from pathlib import Path

def create_windows_installer():
    """Crea un installer Windows semplice"""
    
    print("=" * 50)
    print("    DDT APPLICATION - WINDOWS INSTALLER")
    print("=" * 50)
    print()
    
    version = "1.0.0"
    app_name = "DDT Application"
    install_dir = r"%PROGRAMFILES%\DDT Application"
    desktop = r"%USERPROFILE%\Desktop"
    start_menu = r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
    
    print(f"Creazione installer Windows per {app_name} v{version}")
    print()
    
    # Crea directory di output
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    
    # Crea installer batch
    installer_content = f'''@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    {app_name} - INSTALLER
echo ========================================
echo.
echo Installazione di {app_name} v{version}
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
if not exist "{install_dir}" (
    mkdir "{install_dir}"
    echo ✅ Directory di installazione creata
) else (
    echo ⚠️  Directory di installazione già esistente
)

echo.

REM Copia file applicazione
echo Copia file applicazione...
xcopy /E /I /Y "app" "{install_dir}\\app"
xcopy /E /I /Y "scripts" "{install_dir}\\scripts"
copy "README.md" "{install_dir}\\"
copy "LICENSE" "{install_dir}\\"
copy "requirements.txt" "{install_dir}\\"
echo ✅ File applicazione copiati
echo.

REM Crea collegamento desktop
echo Creazione collegamento desktop...
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{desktop}\\{app_name}.lnk'); $Shortcut.TargetPath = '{install_dir}\\scripts\\start_ddt.bat'; $Shortcut.WorkingDirectory = '{install_dir}'; $Shortcut.Description = '{app_name}'; $Shortcut.Save()}}"
echo ✅ Collegamento desktop creato
echo.

REM Crea collegamento Start Menu
echo Creazione collegamento Start Menu...
if not exist "{start_menu}" mkdir "{start_menu}"
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{start_menu}\\{app_name}.lnk'); $Shortcut.TargetPath = '{install_dir}\\scripts\\start_ddt.bat'; $Shortcut.WorkingDirectory = '{install_dir}'; $Shortcut.Description = '{app_name}'; $Shortcut.Save()}}"
echo ✅ Collegamento Start Menu creato
echo.

REM Crea file di versione
echo {version} > "{install_dir}\\version.txt"
echo ✅ File versione creato
echo.

REM Configura associazione file .ddt
echo Configurazione associazione file .ddt...
reg add "HKEY_CLASSES_ROOT\\.ddt" /ve /d "DDTApplication" /f >nul
reg add "HKEY_CLASSES_ROOT\\DDTApplication" /ve /d "{app_name}" /f >nul
reg add "HKEY_CLASSES_ROOT\\DDTApplication\\DefaultIcon" /ve /d "{install_dir}\\app\\logo1.png" /f >nul
reg add "HKEY_CLASSES_ROOT\\DDTApplication\\shell\\open\\command" /ve /d "\\"{install_dir}\\scripts\\start_ddt.bat\\" \\"%1\\"" /f >nul
echo ✅ Associazione file .ddt configurata
echo.

REM Copia script di avvio
echo Copia script di avvio...
if exist "scripts\\start_ddt.bat" (
    copy "scripts\\start_ddt.bat" "{install_dir}\\scripts\\"
    echo ✅ Script di avvio copiato
) else (
    echo ⚠️  AVVISO: Script start_ddt.bat non trovato
)
echo.

REM Crea script di aggiornamento
echo Creazione script di aggiornamento...
(
echo @echo off
echo cd /d "{install_dir}\\scripts"
echo call update_ddt.bat
) > "{install_dir}\\scripts\\update.bat"
echo ✅ Script di aggiornamento creato
echo.

echo ========================================
echo    INSTALLAZIONE COMPLETATA!
echo ========================================
echo.
echo 🎉 {app_name} è stato installato con successo!
echo.
echo 📍 Directory di installazione: {install_dir}
echo 🖥️  Collegamento desktop: {desktop}\\{app_name}.lnk
echo 📱 Start Menu: {start_menu}\\{app_name}.lnk
echo.
echo 🚀 Per avviare l'applicazione:
echo   - Doppio clic su "{app_name}" dal desktop
echo   - Oppure dal menu Start
echo.
echo 🔄 Per aggiornare l'applicazione:
echo   - Esegui update_ddt.bat dalla directory di installazione
echo.
echo Buon lavoro con la tua applicazione DDT! 🌱
echo.
pause
'''
    
    # Salva installer batch
    installer_file = output_dir / f"DDT-Application-v{version}-Installer.bat"
    with open(installer_file, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print(f"✅ Installer batch creato: {installer_file}")
    
    # Crea pacchetto completo
    print()
    print("=" * 50)
    print("    CREAZIONE PACCHETTO COMPLETO")
    print("=" * 50)
    
    # Crea ZIP con installer e applicazione
    complete_zip = output_dir / f"DDT-Application-v{version}-Complete.zip"
    
    with zipfile.ZipFile(complete_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Aggiungi installer
        zipf.write(installer_file, installer_file.name)
        
        # Aggiungi script di avvio
        start_script = Path("installer/scripts/start_ddt.bat")
        if start_script.exists():
            zipf.write(start_script, "start_ddt.bat")
        
        # Aggiungi file applicazione
        app_dir = Path("installer/app")
        scripts_dir = Path("installer/scripts")
        
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = Path("app") / file_path.relative_to(app_dir)
                zipf.write(file_path, arc_path)
        
        for root, dirs, files in os.walk(scripts_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = Path("scripts") / file_path.relative_to(scripts_dir)
                zipf.write(file_path, arc_path)
        
        # Aggiungi file aggiuntivi
        zipf.write("README.md", "README.md")
        zipf.write("LICENSE", "LICENSE")
        zipf.write("requirements.txt", "requirements.txt")
    
    print(f"✅ Pacchetto completo creato: {complete_zip}")
    
    print()
    print("=" * 50)
    print("    BUILD COMPLETATO!")
    print("=" * 50)
    print()
    
    print("🎉 Installer Windows creato con successo!")
    print()
    
    print("File creati:")
    print(f"- {installer_file} (Installer batch)")
    print(f"- {complete_zip} (Pacchetto completo)")
    print()
    
    print("Per caricare su GitHub:")
    print("1. Vai su https://github.com/PatrikBaldon/DDT-Application/releases")
    print("2. Crea una nuova release")
    print(f"3. Carica i file dalla cartella {output_dir}/")
    print()
    
    print("Per installare su Windows:")
    print("1. Scarica il pacchetto completo")
    print("2. Estrai i file")
    print("3. Esegui DDT-Application-v1.0.0-Installer.bat come amministratore")

if __name__ == "__main__":
    create_windows_installer()
