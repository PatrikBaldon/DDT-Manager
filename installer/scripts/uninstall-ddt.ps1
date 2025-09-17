# DDT Manager - Script di Disinstallazione
# PowerShell script per rimuovere completamente DDT Manager

param(
    [switch]$Silent,
    [switch]$KeepData
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

# Funzione per fermare i processi DDT Manager
function Stop-DDTProcesses {
    Write-ColorOutput "🛑 Arresto processi DDT Manager..." $InfoColor
    
    try {
        $processes = Get-Process | Where-Object { $_.ProcessName -like "*DDT*" -or $_.ProcessName -like "*ddt*" }
        if ($processes) {
            $processes | Stop-Process -Force
            Write-ColorOutput "✅ Processi arrestati!" $SuccessColor
        } else {
            Write-ColorOutput "ℹ️ Nessun processo DDT Manager in esecuzione" $InfoColor
        }
    }
    catch {
        Write-ColorOutput "⚠️ Errore durante l'arresto dei processi: $($_.Exception.Message)" $WarningColor
    }
}

# Funzione per rimuovere file e cartelle
function Remove-DDTFiles {
    param(
        [string]$Path,
        [string]$Description
    )
    
    if (Test-Path $Path) {
        try {
            Write-ColorOutput "🗑️ Rimozione $Description..." $InfoColor
            Remove-Item -Path $Path -Recurse -Force
            Write-ColorOutput "✅ $Description rimosso!" $SuccessColor
        }
        catch {
            Write-ColorOutput "⚠️ Errore durante la rimozione di $Description : $($_.Exception.Message)" $WarningColor
        }
    } else {
        Write-ColorOutput "ℹ️ $Description non trovato" $InfoColor
    }
}

# Funzione per rimuovere shortcut
function Remove-DDTShortcuts {
    Write-ColorOutput "🔗 Rimozione shortcut..." $InfoColor
    
    # Desktop shortcut
    $desktopShortcut = "$env:USERPROFILE\Desktop\DDT Manager.lnk"
    if (Test-Path $desktopShortcut) {
        Remove-Item $desktopShortcut -Force
        Write-ColorOutput "✅ Shortcut desktop rimosso!" $SuccessColor
    }
    
    # Start Menu shortcuts
    $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\DDT Manager"
    if (Test-Path $startMenuPath) {
        Remove-Item $startMenuPath -Recurse -Force
        Write-ColorOutput "✅ Shortcut Start Menu rimossi!" $SuccessColor
    }
    
    # Quick Launch shortcut
    $quickLaunchShortcut = "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\DDT Manager.lnk"
    if (Test-Path $quickLaunchShortcut) {
        Remove-Item $quickLaunchShortcut -Force
        Write-ColorOutput "✅ Shortcut Quick Launch rimosso!" $SuccessColor
    }
}

# Funzione per rimuovere chiavi di registro
function Remove-DDTRegistryKeys {
    Write-ColorOutput "🔧 Rimozione chiavi di registro..." $InfoColor
    
    try {
        # Rimuovi chiavi HKCU
        Remove-Item -Path "HKCU:\Software\DDT Manager" -Recurse -Force -ErrorAction SilentlyContinue
        
        # Rimuovi chiavi HKLM
        Remove-Item -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" -Recurse -Force -ErrorAction SilentlyContinue
        
        Write-ColorOutput "✅ Chiavi di registro rimosse!" $SuccessColor
    }
    catch {
        Write-ColorOutput "⚠️ Errore durante la rimozione delle chiavi di registro: $($_.Exception.Message)" $WarningColor
    }
}

# Funzione per rimuovere Python (opzionale)
function Remove-Python {
    Write-ColorOutput "🐍 Rimozione Python..." $InfoColor
    
    try {
        # Trova Python installato
        $pythonPath = Get-ItemProperty -Path "HKLM:\SOFTWARE\Python\PythonCore\*" -Name "InstallPath" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($pythonPath) {
            $pythonUninstaller = Join-Path $pythonPath.InstallPath "python.exe"
            if (Test-Path $pythonUninstaller) {
                Write-ColorOutput "⚠️ Python trovato. Rimuovi manualmente se necessario." $WarningColor
            }
        }
    }
    catch {
        Write-ColorOutput "ℹ️ Python non trovato o già rimosso" $InfoColor
    }
}

# Funzione per rimuovere Node.js (opzionale)
function Remove-Node {
    Write-ColorOutput "📦 Rimozione Node.js..." $InfoColor
    
    try {
        # Trova Node.js installato
        $nodePath = Get-ItemProperty -Path "HKLM:\SOFTWARE\Node.js" -Name "InstallPath" -ErrorAction SilentlyContinue
        if ($nodePath) {
            Write-ColorOutput "⚠️ Node.js trovato. Rimuovi manualmente se necessario." $WarningColor
        }
    }
    catch {
        Write-ColorOutput "ℹ️ Node.js non trovato o già rimosso" $InfoColor
    }
}

# Funzione per pulire file temporanei
function Clear-DDTTempFiles {
    Write-ColorOutput "🧹 Pulizia file temporanei..." $InfoColor
    
    $tempPaths = @(
        "$env:TEMP\DDT*",
        "$env:TEMP\ddt*",
        "$env:APPDATA\DDT*",
        "$env:LOCALAPPDATA\DDT*"
    )
    
    foreach ($path in $tempPaths) {
        if (Test-Path $path) {
            try {
                Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
                Write-ColorOutput "✅ File temporanei rimossi: $path" $SuccessColor
            }
            catch {
                Write-ColorOutput "⚠️ Errore durante la pulizia di $path : $($_.Exception.Message)" $WarningColor
            }
        }
    }
}

# Funzione principale
function Main {
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput "    DDT Manager - Disinstallazione" $InfoColor
    Write-ColorOutput "========================================" $InfoColor
    Write-ColorOutput ""
    
    # Verifica privilegi amministratore
    if (-not (Test-Administrator)) {
        Write-ColorOutput "❌ Questo script richiede privilegi di amministratore!" $ErrorColor
        Write-ColorOutput "Esegui PowerShell come amministratore e riprova." $WarningColor
        Read-Host "Premi Invio per uscire"
        exit 1
    }
    
    # Conferma disinstallazione
    if (-not $Silent) {
        $confirm = Read-Host "Sei sicuro di voler disinstallare DDT Manager? (s/n)"
        if ($confirm -ne "s" -and $confirm -ne "S" -and $confirm -ne "si" -and $confirm -ne "Si") {
            Write-ColorOutput "Disinstallazione annullata." $InfoColor
            exit 0
        }
    }
    
    # Arresta processi
    Stop-DDTProcesses
    
    # Rimuovi file principali
    $installPath = "$env:PROGRAMFILES\DDT Manager"
    Remove-DDTFiles -Path $installPath -Description "file di installazione"
    
    # Rimuovi dati utente (se non specificato di mantenerli)
    if (-not $KeepData) {
        $appDataPath = "$env:APPDATA\DDT Manager"
        Remove-DDTFiles -Path $appDataPath -Description "dati utente"
    } else {
        Write-ColorOutput "ℹ️ Dati utente mantenuti" $InfoColor
    }
    
    # Rimuovi shortcut
    Remove-DDTShortcuts
    
    # Rimuovi chiavi di registro
    Remove-DDTRegistryKeys
    
    # Pulizia file temporanei
    Clear-DDTTempFiles
    
    Write-ColorOutput ""
    Write-ColorOutput "🎉 Disinstallazione completata!" $SuccessColor
    Write-ColorOutput ""
    Write-ColorOutput "DDT Manager è stato rimosso dal sistema." $InfoColor
    Write-ColorOutput "Grazie per aver utilizzato DDT Manager!" $InfoColor
    
    if (-not $Silent) {
        Read-Host "Premi Invio per uscire"
    }
}

# Esegui funzione principale
Main
