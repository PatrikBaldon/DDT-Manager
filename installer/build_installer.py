#!/usr/bin/env python3
"""
DDT Application - Build Installer Script
Versione: 1.0.0

Script per costruire l'installer Windows per DDT Application
"""

import os
import sys
import shutil
import zipfile
import subprocess
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Build DDT Application Installer')
    parser.add_argument('--version', default='1.0.0', help='Version number')
    parser.add_argument('--app-name', default='DDT Application', help='Application name')
    parser.add_argument('--create-exe', action='store_true', help='Create .exe installer')
    parser.add_argument('--output-dir', default='dist', help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("    DDT APPLICATION - BUILD INSTALLER")
    print("=" * 50)
    print()
    
    print(f"Costruzione installer per {args.app_name} v{args.version}")
    print()
    
    # Imposta variabili
    build_dir = Path("build")
    installer_dir = Path("installer")
    output_dir = Path(args.output_dir)
    zip_file = output_dir / f"DDT-Application-v{args.version}.zip"
    exe_file = output_dir / f"DDT-Application-v{args.version}.exe"
    
    # Crea directory di build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)
    
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    print("✅ Directory di build create")
    
    print()
    print("=" * 50)
    print("    PREPARAZIONE FILE APPLICAZIONE")
    print("=" * 50)
    
    print("Copia file applicazione...")
    
    # Copia file applicazione
    shutil.copytree(installer_dir / "app", build_dir / "app")
    shutil.copytree(installer_dir / "scripts", build_dir / "scripts")
    
    # Copia file aggiuntivi
    shutil.copy2("README.md", build_dir)
    shutil.copy2("LICENSE", build_dir)
    shutil.copy2("requirements.txt", build_dir)
    
    print("✅ File applicazione copiati")
    
    print()
    print("=" * 50)
    print("    CREAZIONE PACCHETTO ZIP")
    print("=" * 50)
    
    print("Creazione pacchetto ZIP...")
    try:
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(build_dir)
                    zipf.write(file_path, arc_path)
        
        print(f"✅ Pacchetto ZIP creato: {zip_file}")
    except Exception as e:
        print(f"❌ ERRORE: Creazione pacchetto ZIP fallita: {e}")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("    CREAZIONE INSTALLER NSIS")
    print("=" * 50)
    
    if args.create_exe:
        nsis_path = Path("C:/Program Files (x86)/NSIS/makensis.exe")
        if nsis_path.exists():
            print("Creazione installer NSIS...")
            try:
                cmd = [
                    str(nsis_path),
                    f"/DVERSION={args.version}",
                    f"/DAPP_NAME={args.app_name}",
                    "installer/DDT_Complete_Setup.nsi"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Installer NSIS creato con successo")
                else:
                    print(f"⚠️  AVVISO: Installer NSIS non creato (errore): {result.stderr}")
            except Exception as e:
                print(f"⚠️  AVVISO: Errore nella creazione installer NSIS: {e}")
        else:
            print("⚠️  AVVISO: NSIS non trovato, installer .exe non creato")
            print("Per creare l'installer .exe, installa NSIS da: https://nsis.sourceforge.io/")
    else:
        print("⚠️  AVVISO: Creazione installer .exe saltata (usa --create-exe per abilitare)")
    
    print()
    print("=" * 50)
    print("    CREAZIONE INSTALLER INNO SETUP")
    print("=" * 50)
    
    if args.create_exe:
        inno_setup_path = Path("C:/Program Files (x86)/Inno Setup 6/ISCC.exe")
        if inno_setup_path.exists():
            print("Creazione installer Inno Setup...")
            try:
                cmd = [
                    str(inno_setup_path),
                    f"/DVERSION={args.version}",
                    f"/DAPP_NAME={args.app_name}",
                    "installer/DDT_Complete_Setup.iss"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Installer Inno Setup creato con successo")
                else:
                    print(f"⚠️  AVVISO: Installer Inno Setup non creato (errore): {result.stderr}")
            except Exception as e:
                print(f"⚠️  AVVISO: Errore nella creazione installer Inno Setup: {e}")
        else:
            print("⚠️  AVVISO: Inno Setup non trovato, installer .exe non creato")
            print("Per creare l'installer .exe, installa Inno Setup da: https://jrsoftware.org/isinfo.php")
    else:
        print("⚠️  AVVISO: Creazione installer .exe saltata (usa --create-exe per abilitare)")
    
    print()
    print("=" * 50)
    print("    PULIZIA FILE TEMPORANEI")
    print("=" * 50)
    
    print("Pulizia file temporanei...")
    shutil.rmtree(build_dir)
    print("✅ Pulizia completata")
    
    print()
    print("=" * 50)
    print("    BUILD COMPLETATO!")
    print("=" * 50)
    print()
    
    print("🎉 Build dell'installer completato!")
    print()
    
    print("File creati:")
    print(f"- {zip_file}")
    if exe_file.exists():
        print(f"- {exe_file}")
    
    print()
    print("Per creare installer .exe:")
    print("1. Installa NSIS o Inno Setup")
    print("2. Esegui: python installer/build_installer.py --create-exe")
    
    print()
    print("Per caricare su GitHub:")
    print("1. Vai su https://github.com/PatrikBaldon/DDT-Application/releases")
    print("2. Crea una nuova release")
    print(f"3. Carica i file dalla cartella {output_dir}/")

if __name__ == "__main__":
    main()
