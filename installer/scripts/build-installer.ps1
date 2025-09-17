# DDT Manager - Script per Build Installer
# PowerShell script per creare installer Windows automaticamente

param(
    [switch]$Clean,
    [switch]$SkipBuild,
    [string]$OutputDir = "installer\dist"
)

# Colori per output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

# Funzione per stampare messaggi colorati
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Funzione per verificare se NSIS è installato
function Test-NSISInstalled {
    $nsisPath = Get-Command "makensis.exe" -ErrorAction SilentlyContinue
    if ($nsisPath) {
        return $true
    }
    
    # Cerca in percorsi comuni
    $commonPaths = @(
        "${env:PROGRAMFILES}\NSIS\makensis.exe",
        "${env:PROGRAMFILES(X86)}\NSIS\makensis.exe",
        "C:\Program Files\NSIS\makensis.exe",
        "C:\Program Files (x86)\NSIS\makensis.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            return $true
        }
    }
    
    return $false
}

# Funzione per installare NSIS
function Install-NSIS {
    Write-ColorOutput "📦 Installazione NSIS..." $InfoColor
    
    $nsisUrl = "https://sourceforge.net/projects/nsis/files/NSIS%203/3.08/nsis-3.08-setup.exe/download"
    $nsisInstaller = "$env:TEMP\nsis-installer.exe"
    
    try {
        # Download NSIS installer
        Write-ColorOutput "📥 Download NSIS installer..." $InfoColor
        Invoke-WebRequest -Uri $nsisUrl -OutFile $nsisInstaller -UseBasicParsing
        
        # Install NSIS silently
        Write-ColorOutput "⚙️ Installazione NSIS in corso..." $InfoColor
        Start-Process -FilePath $nsisInstaller -ArgumentList "/S" -Wait
        
        # Cleanup
        Remove-Item $nsisInstaller -Force
        
        # Verify installation
        if (Test-NSISInstalled) {
            Write-ColorOutput "✅ NSIS installato con successo!" $SuccessColor
            return $true
        } else {
            Write-ColorOutput "❌ Installazione NSIS fallita!" $ErrorColor
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Errore durante l'installazione di NSIS: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per pulire build precedenti
function Clear-BuildFiles {
    Write-ColorOutput "🧹 Pulizia file di build..." $InfoColor
    
    $pathsToClean = @(
        "dist",
        "build",
        "out",
        "installer\dist",
        "installer\nsis\DDT_Manager_Setup.exe"
    )
    
    foreach ($path in $pathsToClean) {
        if (Test-Path $path) {
            try {
                Remove-Item -Path $path -Recurse -Force
                Write-ColorOutput "✅ Rimosso: $path" $SuccessColor
            }
            catch {
                Write-ColorOutput "⚠️ Errore durante la rimozione di $path : $($_.Exception.Message)" $WarningColor
            }
        }
    }
}

# Funzione per build Electron
function Build-Electron {
    Write-ColorOutput "🔨 Build applicazione Electron..." $InfoColor
    
    try {
        # Verifica se package.json esiste
        if (-not (Test-Path "package.json")) {
            Write-ColorOutput "❌ package.json non trovato!" $ErrorColor
            return $false
        }
        
        # Installa dipendenze se necessario
        if (-not (Test-Path "node_modules")) {
            Write-ColorOutput "📦 Installazione dipendenze Node.js..." $InfoColor
            npm install
            if ($LASTEXITCODE -ne 0) {
                Write-ColorOutput "❌ Errore durante l'installazione delle dipendenze!" $ErrorColor
                return $false
            }
        }
        
        # Build Electron
        Write-ColorOutput "⚙️ Build Electron in corso..." $InfoColor
        npm run build
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "❌ Errore durante il build di Electron!" $ErrorColor
            return $false
        }
        
        Write-ColorOutput "✅ Build Electron completato!" $SuccessColor
        return $true
    }
    catch {
        Write-ColorOutput "❌ Errore durante il build di Electron: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per creare installer NSIS
function New-NSISInstaller {
    Write-ColorOutput "🔧 Creazione installer NSIS..." $InfoColor
    
    try {
        # Verifica se NSIS è installato
        if (-not (Test-NSISInstalled)) {
            Write-ColorOutput "❌ NSIS non trovato!" $ErrorColor
            Write-ColorOutput "Installazione NSIS in corso..." $InfoColor
            if (-not (Install-NSIS)) {
                return $false
            }
        }
        
        # Verifica se il file NSI esiste
        $nsiFile = "installer\nsis\ddt-installer.nsi"
        if (-not (Test-Path $nsiFile)) {
            Write-ColorOutput "❌ File NSI non trovato: $nsiFile" $ErrorColor
            return $false
        }
        
        # Crea directory di output
        $outputPath = "installer\dist"
        if (-not (Test-Path $outputPath)) {
            New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
        }
        
        # Esegui makensis
        Write-ColorOutput "⚙️ Esecuzione makensis..." $InfoColor
        $makensisPath = Get-Command "makensis.exe" -ErrorAction SilentlyContinue
        if (-not $makensisPath) {
            $makensisPath = "${env:PROGRAMFILES}\NSIS\makensis.exe"
        }
        
        & $makensisPath.Path /D"OUTPUT_DIR=$outputPath" $nsiFile
        
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "❌ Errore durante la creazione dell'installer!" $ErrorColor
            return $false
        }
        
        # Verifica se l'installer è stato creato
        $installerPath = "$outputPath\DDT_Manager_Setup.exe"
        if (Test-Path $installerPath) {
            Write-ColorOutput "✅ Installer creato: $installerPath" $SuccessColor
            return $true
        } else {
            Write-ColorOutput "❌ Installer non trovato dopo la creazione!" $ErrorColor
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Errore durante la creazione dell'installer: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per creare package di distribuzione
function New-DistributionPackage {
    Write-ColorOutput "📦 Creazione package di distribuzione..." $InfoColor
    
    try {
        $packageDir = "installer\dist\DDT_Manager_Package"
        if (Test-Path $packageDir) {
            Remove-Item -Path $packageDir -Recurse -Force
        }
        New-Item -ItemType Directory -Path $packageDir -Force | Out-Null
        
        # Copia installer
        Copy-Item "installer\dist\DDT_Manager_Setup.exe" "$packageDir\" -Force
        
        # Copia script di installazione
        Copy-Item "installer\scripts\install-ddt.ps1" "$packageDir\" -Force
        Copy-Item "installer\scripts\uninstall-ddt.ps1" "$packageDir\" -Force
        Copy-Item "installer\windows\DDT_Manager_Installer.bat" "$packageDir\" -Force
        
        # Copia documentazione
        Copy-Item "README.md" "$packageDir\README.txt" -Force
        Copy-Item "LICENSE" "$packageDir\" -Force
        
        # Crea script di avvio rapido
        $quickStartScript = @"
@echo off
echo DDT Manager - Avvio Rapido
echo ==========================
echo.
echo 1. Installazione Automatica (Raccomandato)
echo 2. Installazione Manuale
echo 3. Disinstallazione
echo.
set /p choice="Scegli un'opzione (1-3): "
if "%choice%"=="1" (
    call DDT_Manager_Installer.bat
) else if "%choice%"=="2" (
    DDT_Manager_Setup.exe
) else if "%choice%"=="3" (
    powershell -ExecutionPolicy Bypass -File uninstall-ddt.ps1
) else (
    echo Opzione non valida
    pause
)
"@
        $quickStartScript | Out-File -FilePath "$packageDir\Avvio_Rapido.bat" -Encoding ASCII
        
        Write-ColorOutput "✅ Package di distribuzione creato: $packageDir" $SuccessColor
        return $true
    }
    catch {
        Write-ColorOutput "❌ Errore durante la creazione del package: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione principale
function Main {
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput "    DDT Manager - Build Installer" $InfoColor
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput ""
    
    # Pulizia se richiesta
    if ($Clean) {
        Clear-BuildFiles
    }
    
    # Build Electron se non saltato
    if (-not $SkipBuild) {
        if (-not (Build-Electron)) {
            Write-ColorOutput "❌ Build fallito!" $ErrorColor
            exit 1
        }
    }
    
    # Crea installer NSIS
    if (-not (New-NSISInstaller)) {
        Write-ColorOutput "❌ Creazione installer fallita!" $ErrorColor
        exit 1
    }
    
    # Crea package di distribuzione
    if (-not (New-DistributionPackage)) {
        Write-ColorOutput "❌ Creazione package fallita!" $ErrorColor
        exit 1
    }
    
    Write-ColorOutput ""
    Write-ColorOutput "🎉 Build installer completato con successo!" $SuccessColor
    Write-ColorOutput ""
    Write-ColorOutput "File creati:" $InfoColor
    Write-ColorOutput "  - installer\dist\DDT_Manager_Setup.exe" $InfoColor
    Write-ColorOutput "  - installer\dist\DDT_Manager_Package\" $InfoColor
    Write-ColorOutput ""
    Write-ColorOutput "Per distribuire:" $InfoColor
    Write-ColorOutput "  1. Copia la cartella DDT_Manager_Package" $InfoColor
    Write-ColorOutput "  2. Condividi con gli utenti" $InfoColor
    Write-ColorOutput "  3. Gli utenti possono eseguire Avvio_Rapido.bat" $InfoColor
    Write-ColorOutput ""
}

# Esegui funzione principale
Main
