# DDT Application - Build Installer PowerShell Script
# Versione: 1.0.0

param(
    [string]$Version = "1.0.0",
    [string]$AppName = "DDT Application",
    [switch]$CreateExe = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    DDT APPLICATION - BUILD INSTALLER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Costruzione installer per $AppName v$Version" -ForegroundColor Green
Write-Host ""

# Imposta variabili
$BuildDir = "build"
$InstallerDir = "installer"
$OutputDir = "dist"
$ZipFile = "$OutputDir\DDT-Application-v$Version.zip"
$ExeFile = "$OutputDir\DDT-Application-v$Version.exe"

# Crea directory di build
if (Test-Path $BuildDir) {
    Remove-Item -Path $BuildDir -Recurse -Force
}
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

if (Test-Path $OutputDir) {
    Remove-Item -Path $OutputDir -Recurse -Force
}
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

Write-Host "✅ Directory di build create" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    PREPARAZIONE FILE APPLICAZIONE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Copia file applicazione..."
Copy-Item -Path "$InstallerDir\app" -Destination "$BuildDir\app" -Recurse -Force
Copy-Item -Path "$InstallerDir\scripts" -Destination "$BuildDir\scripts" -Recurse -Force

# Copia file aggiuntivi
Copy-Item -Path "README.md" -Destination "$BuildDir\" -Force
Copy-Item -Path "LICENSE" -Destination "$BuildDir\" -Force
Copy-Item -Path "requirements.txt" -Destination "$BuildDir\" -Force

Write-Host "✅ File applicazione copiati" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    CREAZIONE PACCHETTO ZIP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Creazione pacchetto ZIP..."
try {
    Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipFile -Force
    Write-Host "✅ Pacchetto ZIP creato: $ZipFile" -ForegroundColor Green
} catch {
    Write-Host "❌ ERRORE: Creazione pacchetto ZIP fallita: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    CREAZIONE INSTALLER NSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($CreateExe) {
    $NSISPath = "C:\Program Files (x86)\NSIS\makensis.exe"
    if (Test-Path $NSISPath) {
        Write-Host "Creazione installer NSIS..."
        try {
            & $NSISPath /DVERSION=$Version /DAPP_NAME="$AppName" "installer\DDT_Complete_Setup.nsi"
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Installer NSIS creato con successo" -ForegroundColor Green
            } else {
                Write-Host "⚠️  AVVISO: Installer NSIS non creato (errore)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "⚠️  AVVISO: Errore nella creazione installer NSIS: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  AVVISO: NSIS non trovato, installer .exe non creato" -ForegroundColor Yellow
        Write-Host "Per creare l'installer .exe, installa NSIS da: https://nsis.sourceforge.io/" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  AVVISO: Creazione installer .exe saltata (usa -CreateExe per abilitare)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    CREAZIONE INSTALLER INNO SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($CreateExe) {
    $InnoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (Test-Path $InnoSetupPath) {
        Write-Host "Creazione installer Inno Setup..."
        try {
            & $InnoSetupPath /DVERSION=$Version /DAPP_NAME="$AppName" "installer\DDT_Complete_Setup.iss"
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Installer Inno Setup creato con successo" -ForegroundColor Green
            } else {
                Write-Host "⚠️  AVVISO: Installer Inno Setup non creato (errore)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "⚠️  AVVISO: Errore nella creazione installer Inno Setup: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  AVVISO: Inno Setup non trovato, installer .exe non creato" -ForegroundColor Yellow
        Write-Host "Per creare l'installer .exe, installa Inno Setup da: https://jrsoftware.org/isinfo.php" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  AVVISO: Creazione installer .exe saltata (usa -CreateExe per abilitare)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    PULIZIA FILE TEMPORANEI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Pulizia file temporanei..."
Remove-Item -Path $BuildDir -Recurse -Force
Write-Host "✅ Pulizia completata" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    BUILD COMPLETATO!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎉 Build dell'installer completato!" -ForegroundColor Green
Write-Host ""

Write-Host "File creati:" -ForegroundColor White
Write-Host "- $ZipFile" -ForegroundColor White
if (Test-Path $ExeFile) {
    Write-Host "- $ExeFile" -ForegroundColor White
}

Write-Host ""
Write-Host "Per creare installer .exe:" -ForegroundColor Yellow
Write-Host "1. Installa NSIS o Inno Setup" -ForegroundColor Yellow
Write-Host "2. Esegui: .\installer\build_installer.ps1 -CreateExe" -ForegroundColor Yellow

Write-Host ""
Write-Host "Per caricare su GitHub:" -ForegroundColor Yellow
Write-Host "1. Vai su https://github.com/PatrikBaldon/DDT-Application/releases" -ForegroundColor Yellow
Write-Host "2. Crea una nuova release" -ForegroundColor Yellow
Write-Host "3. Carica i file dalla cartella $OutputDir\" -ForegroundColor Yellow

Write-Host ""
Write-Host "Premi un tasto per continuare..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
