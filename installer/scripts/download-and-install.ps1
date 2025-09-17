# DDT Manager - Download e Installazione Automatica da GitHub
# Script PowerShell per scaricare e installare l'ultima versione

param(
    [switch]$Silent,
    [switch]$SkipDownload,
    [string]$Version = "latest",
    [string]$GitHubRepo = "PatrikBaldon/DDT-Application"
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

# Funzione per verificare se l'utente è amministratore
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Funzione per scaricare l'ultima versione da GitHub
function Get-LatestRelease {
    param(
        [string]$Repo,
        [string]$Version
    )
    
    try {
        if ($Version -eq "latest") {
            $url = "https://api.github.com/repos/$Repo/releases/latest"
        } else {
            $url = "https://api.github.com/repos/$Repo/releases/tags/$Version"
        }
        
        Write-ColorOutput "📡 Recupero informazioni versione da GitHub..." $InfoColor
        $response = Invoke-RestMethod -Uri $url -Headers @{
            "Accept" = "application/vnd.github.v3+json"
            "User-Agent" = "DDT-Manager-Installer"
        }
        
        return $response
    }
    catch {
        Write-ColorOutput "❌ Errore nel recupero delle informazioni: $($_.Exception.Message)" $ErrorColor
        return $null
    }
}

# Funzione per scaricare file da GitHub
function Download-ReleaseAsset {
    param(
        [object]$Release,
        [string]$AssetName,
        [string]$OutputPath
    )
    
    try {
        $asset = $Release.assets | Where-Object { $_.name -like "*$AssetName*" }
        if (-not $asset) {
            Write-ColorOutput "❌ Asset '$AssetName' non trovato nella release" $ErrorColor
            return $false
        }
        
        Write-ColorOutput "📥 Download $($asset.name)..." $InfoColor
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $OutputPath -UseBasicParsing
        
        if (Test-Path $OutputPath) {
            Write-ColorOutput "✅ Download completato: $OutputPath" $SuccessColor
            return $true
        } else {
            Write-ColorOutput "❌ Download fallito" $ErrorColor
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Errore durante il download: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per verificare Python
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+)") {
            $version = $matches[1]
            if ([version]$version -ge [version]"3.8") {
                return $true
            }
        }
    }
    catch {
        return $false
    }
    return $false
}

# Funzione per verificare Node.js
function Test-NodeInstalled {
    try {
        $nodeVersion = node --version 2>&1
        if ($nodeVersion -match "v(\d+\.\d+\.\d+)") {
            $version = $matches[1]
            if ([version]$version -ge [version]"16.0.0") {
                return $true
            }
        }
    }
    catch {
        return $false
    }
    return $false
}

# Funzione per installare Python
function Install-Python {
    Write-ColorOutput "🐍 Installazione Python..." $InfoColor
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    try {
        Write-ColorOutput "📥 Download Python installer..." $InfoColor
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        
        Write-ColorOutput "⚙️ Installazione Python in corso..." $InfoColor
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        Remove-Item $pythonInstaller -Force
        
        if (Test-PythonInstalled) {
            Write-ColorOutput "✅ Python installato con successo!" $SuccessColor
            return $true
        } else {
            Write-ColorOutput "❌ Installazione Python fallita!" $ErrorColor
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Errore durante l'installazione di Python: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per installare Node.js
function Install-Node {
    Write-ColorOutput "📦 Installazione Node.js..." $InfoColor
    
    $nodeUrl = "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi"
    $nodeInstaller = "$env:TEMP\node-installer.msi"
    
    try {
        Write-ColorOutput "📥 Download Node.js installer..." $InfoColor
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
        
        Write-ColorOutput "⚙️ Installazione Node.js in corso..." $InfoColor
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $nodeInstaller, "/quiet" -Wait
        
        Remove-Item $nodeInstaller -Force
        
        if (Test-NodeInstalled) {
            Write-ColorOutput "✅ Node.js installato con successo!" $SuccessColor
            return $true
        } else {
            Write-ColorOutput "❌ Installazione Node.js fallita!" $ErrorColor
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Errore durante l'installazione di Node.js: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per installare DDT Manager
function Install-DDTManager {
    param(
        [string]$InstallerPath
    )
    
    Write-ColorOutput "🚀 Installazione DDT Manager..." $InfoColor
    
    try {
        if (-not (Test-Path $InstallerPath)) {
            Write-ColorOutput "❌ Installer non trovato: $InstallerPath" $ErrorColor
            return $false
        }
        
        Write-ColorOutput "⚙️ Esecuzione installer DDT Manager..." $InfoColor
        if ($Silent) {
            Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait
        } else {
            Start-Process -FilePath $InstallerPath -Wait
        }
        
        Write-ColorOutput "✅ DDT Manager installato con successo!" $SuccessColor
        return $true
    }
    catch {
        Write-ColorOutput "❌ Errore durante l'installazione di DDT Manager: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

# Funzione per creare shortcut
function New-DDTShortcut {
    $shortcutPath = "$env:USERPROFILE\Desktop\DDT Manager.lnk"
    $targetPath = "$env:PROGRAMFILES\DDT Manager\DDT Manager.exe"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $targetPath
        $Shortcut.WorkingDirectory = "$env:PROGRAMFILES\DDT Manager"
        $Shortcut.Description = "DDT Manager - Sistema di gestione Documenti di Trasporto"
        $Shortcut.Save()
        
        Write-ColorOutput "✅ Shortcut creato sul desktop!" $SuccessColor
    }
    catch {
        Write-ColorOutput "⚠️ Impossibile creare shortcut: $($_.Exception.Message)" $WarningColor
    }
}

# Funzione principale
function Main {
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput "    DDT Manager - Download e Installazione" $InfoColor
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput ""
    
    # Verifica privilegi amministratore
    if (-not (Test-Administrator)) {
        Write-ColorOutput "❌ Questo script richiede privilegi di amministratore!" $ErrorColor
        Write-ColorOutput "Esegui PowerShell come amministratore e riprova." $WarningColor
        if (-not $Silent) {
            Read-Host "Premi Invio per uscire"
        }
        exit 1
    }
    
    # Verifica Python
    if (-not (Test-PythonInstalled)) {
        Write-ColorOutput "🐍 Python non trovato. Installazione in corso..." $WarningColor
        if (-not (Install-Python)) {
            Write-ColorOutput "❌ Installazione Python fallita!" $ErrorColor
            if (-not $Silent) {
                Read-Host "Premi Invio per uscire"
            }
            exit 1
        }
    } else {
        Write-ColorOutput "✅ Python già installato!" $SuccessColor
    }
    
    # Verifica Node.js
    if (-not (Test-NodeInstalled)) {
        Write-ColorOutput "📦 Node.js non trovato. Installazione in corso..." $WarningColor
        if (-not (Install-Node)) {
            Write-ColorOutput "❌ Installazione Node.js fallita!" $ErrorColor
            if (-not $Silent) {
                Read-Host "Premi Invio per uscire"
            }
            exit 1
        }
    } else {
        Write-ColorOutput "✅ Node.js già installato!" $SuccessColor
    }
    
    # Download e installazione DDT Manager
    if (-not $SkipDownload) {
        Write-ColorOutput "📡 Recupero ultima versione da GitHub..." $InfoColor
        $release = Get-LatestRelease -Repo $GitHubRepo -Version $Version
        
        if (-not $release) {
            Write-ColorOutput "❌ Impossibile recuperare le informazioni della versione!" $ErrorColor
            if (-not $Silent) {
                Read-Host "Premi Invio per uscire"
            }
            exit 1
        }
        
        Write-ColorOutput "📋 Versione trovata: $($release.tag_name)" $InfoColor
        Write-ColorOutput "📝 Note: $($release.body)" $InfoColor
        
        # Crea directory temporanea
        $tempDir = "$env:TEMP\DDT_Manager_Install"
        if (Test-Path $tempDir) {
            Remove-Item $tempDir -Recurse -Force
        }
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
        
        # Scarica installer
        $installerPath = "$tempDir\DDT_Manager_Setup.exe"
        if (-not (Download-ReleaseAsset -Release $release -AssetName "DDT_Manager_Setup.exe" -OutputPath $installerPath)) {
            Write-ColorOutput "❌ Download installer fallito!" $ErrorColor
            if (-not $Silent) {
                Read-Host "Premi Invio per uscire"
            }
            exit 1
        }
        
        # Installa DDT Manager
        if (Install-DDTManager -InstallerPath $installerPath) {
            # Crea shortcut
            New-DDTShortcut
            
            Write-ColorOutput ""
            Write-ColorOutput "🎉 Installazione completata con successo!" $SuccessColor
            Write-ColorOutput ""
            Write-ColorOutput "Per avviare DDT Manager:" $InfoColor
            Write-ColorOutput "  - Clicca sull'icona sul desktop" $InfoColor
            Write-ColorOutput "  - Oppure vai in Start Menu > DDT Manager" $InfoColor
            Write-ColorOutput ""
            Write-ColorOutput "Per disinstallare:" $InfoColor
            Write-ColorOutput "  - Vai in Pannello di Controllo > Programmi" $InfoColor
            Write-ColorOutput "  - Oppure esegui: Uninstall-DDTManager" $InfoColor
        } else {
            Write-ColorOutput "❌ Installazione DDT Manager fallita!" $ErrorColor
        }
        
        # Pulizia file temporanei
        Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    if (-not $Silent) {
        Read-Host "Premi Invio per uscire"
    }
}

# Esegui funzione principale
Main
