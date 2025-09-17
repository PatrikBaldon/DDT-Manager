# DDT Manager - Script di Installazione Automatica
# PowerShell script per installazione completa su Windows

param(
    [switch]$Silent,
    [switch]$SkipPython,
    [switch]$SkipNode,
    [string]$InstallPath = "$env:PROGRAMFILES\DDT Manager"
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

# Funzione per verificare se Python è installato
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

# Funzione per verificare se Node.js è installato
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
        # Download Python installer
        Write-ColorOutput "📥 Download Python installer..." $InfoColor
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        
        # Install Python silently
        Write-ColorOutput "⚙️ Installazione Python in corso..." $InfoColor
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        # Cleanup
        Remove-Item $pythonInstaller -Force
        
        # Verify installation
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
        # Download Node.js installer
        Write-ColorOutput "📥 Download Node.js installer..." $InfoColor
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
        
        # Install Node.js silently
        Write-ColorOutput "⚙️ Installazione Node.js in corso..." $InfoColor
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $nodeInstaller, "/quiet" -Wait
        
        # Cleanup
        Remove-Item $nodeInstaller -Force
        
        # Verify installation
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
    Write-ColorOutput "🚀 Installazione DDT Manager..." $InfoColor
    
    try {
        # Verifica se l'installer esiste
        $installerPath = "DDT_Manager_Setup.exe"
        if (-not (Test-Path $installerPath)) {
            Write-ColorOutput "❌ Installer DDT Manager non trovato: $installerPath" $ErrorColor
            return $false
        }
        
        # Esegui installer
        Write-ColorOutput "⚙️ Esecuzione installer DDT Manager..." $InfoColor
        if ($Silent) {
            Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
        } else {
            Start-Process -FilePath $installerPath -Wait
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
    $targetPath = "$InstallPath\DDT Manager.exe"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $targetPath
        $Shortcut.WorkingDirectory = $InstallPath
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
    Write-ColorOutput "    DDT Manager - Installazione" $InfoColor
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput ""
    
    # Verifica privilegi amministratore
    if (-not (Test-Administrator)) {
        Write-ColorOutput "❌ Questo script richiede privilegi di amministratore!" $ErrorColor
        Write-ColorOutput "Esegui PowerShell come amministratore e riprova." $WarningColor
        Read-Host "Premi Invio per uscire"
        exit 1
    }
    
    # Verifica Python
    if (-not $SkipPython) {
        if (-not (Test-PythonInstalled)) {
            Write-ColorOutput "🐍 Python non trovato. Installazione in corso..." $WarningColor
            if (-not (Install-Python)) {
                Write-ColorOutput "❌ Installazione fallita!" $ErrorColor
                Read-Host "Premi Invio per uscire"
                exit 1
            }
        } else {
            Write-ColorOutput "✅ Python già installato!" $SuccessColor
        }
    }
    
    # Verifica Node.js
    if (-not $SkipNode) {
        if (-not (Test-NodeInstalled)) {
            Write-ColorOutput "📦 Node.js non trovato. Installazione in corso..." $WarningColor
            if (-not (Install-Node)) {
                Write-ColorOutput "❌ Installazione fallita!" $ErrorColor
                Read-Host "Premi Invio per uscire"
                exit 1
            }
        } else {
            Write-ColorOutput "✅ Node.js già installato!" $SuccessColor
        }
    }
    
    # Installa DDT Manager
    if (Install-DDTManager) {
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
        Write-ColorOutput "❌ Installazione fallita!" $ErrorColor
    }
    
    if (-not $Silent) {
        Read-Host "Premi Invio per uscire"
    }
}

# Esegui funzione principale
Main
