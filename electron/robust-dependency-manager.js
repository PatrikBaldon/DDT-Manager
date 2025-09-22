const { exec, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

/**
 * Sistema robusto di gestione dipendenze cross-platform
 * Gestisce automaticamente Python, Node.js e ambiente virtuale
 */
class RobustDependencyManager {
    constructor() {
        this.platform = process.platform;
        this.arch = process.arch;
        this.isWindows = this.platform === 'win32';
        this.isMacOS = this.platform === 'darwin';
        this.isLinux = this.platform === 'linux';
        
        this.appDir = process.resourcesPath || process.cwd();
        this.venvDir = path.join(this.appDir, 'venv');
        this.pythonPath = null;
        this.nodePath = null;
        this.venvPythonPath = null;
        
        // Percorsi per ambiente virtuale per OS
        this.venvPaths = {
            win32: {
                python: path.join(this.venvDir, 'Scripts', 'python.exe'),
                pip: path.join(this.venvDir, 'Scripts', 'pip.exe'),
                activate: path.join(this.venvDir, 'Scripts', 'activate.bat')
            },
            darwin: {
                python: path.join(this.venvDir, 'bin', 'python3'),
                pip: path.join(this.venvDir, 'bin', 'pip3'),
                activate: path.join(this.venvDir, 'bin', 'activate')
            },
            linux: {
                python: path.join(this.venvDir, 'bin', 'python3'),
                pip: path.join(this.venvDir, 'bin', 'pip3'),
                activate: path.join(this.venvDir, 'bin', 'activate')
            }
        };
    }

    /**
     * Metodo principale: verifica e installa tutto automaticamente
     */
    async setupEnvironment() {
        console.log('🔧 Configurazione ambiente automatica...');
        
        try {
            // 1. Verifica/Installa Python
            await this.ensurePython();
            
            // 2. Verifica/Installa Node.js
            await this.ensureNodeJS();
            
            // 3. Crea/Verifica ambiente virtuale
            await this.ensureVirtualEnvironment();
            
            // 4. Installa dipendenze Python
            await this.installPythonDependencies();
            
            // 5. Verifica configurazione finale
            await this.verifySetup();
            
            console.log('✅ Ambiente configurato con successo!');
            return true;
            
        } catch (error) {
            console.error('❌ Errore configurazione ambiente:', error);
            return false;
        }
    }

    /**
     * Verifica e installa Python se necessario
     */
    async ensurePython() {
        console.log('🐍 Verifica Python...');
        
        // Prima prova a trovare Python esistente
        const systemPython = await this.findSystemPython();
        if (systemPython) {
            console.log('✅ Python trovato nel sistema:', systemPython);
            this.pythonPath = systemPython;
            return;
        }
        
        // Se non trovato, installa automaticamente
        console.log('📦 Python non trovato, installazione automatica...');
        await this.installPython();
    }

    /**
     * Cerca Python nel sistema
     */
    async findSystemPython() {
        const candidates = this.getPythonCandidates();
        
        for (const candidate of candidates) {
            try {
                const result = await this.executeCommand(`"${candidate}" --version`);
                if (result.success && result.stdout.includes('Python')) {
                    return candidate;
                }
            } catch (error) {
                // Continua con il prossimo candidato
            }
        }
        
        return null;
    }

    /**
     * Ottiene i candidati Python per il sistema operativo corrente
     */
    getPythonCandidates() {
        if (this.isWindows) {
            return [
                'python',
                'python3',
                'py',
                'C:\\Python311\\python.exe',
                'C:\\Python310\\python.exe',
                'C:\\Python39\\python.exe',
                `C:\\Users\\${process.env.USERNAME}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe`,
                `C:\\Users\\${process.env.USERNAME}\\AppData\\Local\\Programs\\Python\\Python310\\python.exe`
            ];
        } else if (this.isMacOS) {
            return [
                'python3',
                'python',
                '/opt/homebrew/bin/python3',
                '/usr/local/bin/python3',
                '/usr/bin/python3',
                '/opt/anaconda3/bin/python3'
            ];
        } else { // Linux
            return [
                'python3',
                'python',
                '/usr/bin/python3',
                '/usr/local/bin/python3'
            ];
        }
    }

    /**
     * Installa Python automaticamente
     */
    async installPython() {
        if (this.isWindows) {
            await this.installPythonWindows();
        } else if (this.isMacOS) {
            await this.installPythonMacOS();
        } else { // Linux
            await this.installPythonLinux();
        }
    }

    /**
     * Installa Python su Windows
     */
    async installPythonWindows() {
        console.log('📥 Download e installazione Python per Windows...');
        
        // Usa winget se disponibile (Windows 10/11)
        try {
            await this.executeCommand('winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements');
            this.pythonPath = 'python';
            console.log('✅ Python installato con winget');
            return;
        } catch (error) {
            console.log('⚠️ winget non disponibile, tentativo con chocolatey...');
        }
        
        // Fallback: chocolatey
        try {
            await this.executeCommand('choco install python311 -y');
            this.pythonPath = 'python';
            console.log('✅ Python installato con chocolatey');
            return;
        } catch (error) {
            console.log('⚠️ chocolatey non disponibile, installazione manuale richiesta');
            throw new Error('Installazione automatica Python fallita. Installa manualmente Python 3.11+ da https://python.org');
        }
    }

    /**
     * Installa Python su macOS
     */
    async installPythonMacOS() {
        console.log('📥 Installazione Python per macOS...');
        
        // Prova con Homebrew
        try {
            await this.executeCommand('brew install python@3.11');
            this.pythonPath = '/opt/homebrew/bin/python3';
            console.log('✅ Python installato con Homebrew');
            return;
        } catch (error) {
            console.log('⚠️ Homebrew non disponibile, installazione manuale richiesta');
            throw new Error('Installazione automatica Python fallita. Installa manualmente Python 3.11+ o Homebrew');
        }
    }

    /**
     * Installa Python su Linux
     */
    async installPythonLinux() {
        console.log('📥 Installazione Python per Linux...');
        
        // Rileva la distribuzione
        const distro = await this.detectLinuxDistro();
        
        if (distro === 'ubuntu' || distro === 'debian') {
            await this.executeCommand('sudo apt update && sudo apt install -y python3 python3-pip python3-venv');
        } else if (distro === 'fedora' || distro === 'rhel') {
            await this.executeCommand('sudo dnf install -y python3 python3-pip');
        } else if (distro === 'arch') {
            await this.executeCommand('sudo pacman -S --noconfirm python python-pip');
        } else {
            throw new Error(`Distribuzione Linux non supportata: ${distro}`);
        }
        
        this.pythonPath = 'python3';
        console.log('✅ Python installato per Linux');
    }

    /**
     * Verifica e installa Node.js se necessario
     */
    async ensureNodeJS() {
        console.log('🟢 Verifica Node.js...');
        
        const systemNode = await this.findSystemNode();
        if (systemNode) {
            console.log('✅ Node.js trovato nel sistema:', systemNode);
            this.nodePath = systemNode;
            return;
        }
        
        console.log('📦 Node.js non trovato, installazione automatica...');
        await this.installNodeJS();
    }

    /**
     * Cerca Node.js nel sistema
     */
    async findSystemNode() {
        try {
            const result = await this.executeCommand('node --version');
            if (result.success) {
                return 'node';
            }
        } catch (error) {
            // Continua con installazione
        }
        
        return null;
    }

    /**
     * Installa Node.js automaticamente
     */
    async installNodeJS() {
        if (this.isWindows) {
            await this.installNodeJSWindows();
        } else if (this.isMacOS) {
            await this.installNodeJSMacOS();
        } else { // Linux
            await this.installNodeJSLinux();
        }
    }

    /**
     * Installa Node.js su Windows
     */
    async installNodeJSWindows() {
        try {
            await this.executeCommand('winget install OpenJS.NodeJS --accept-package-agreements --accept-source-agreements');
            this.nodePath = 'node';
            console.log('✅ Node.js installato con winget');
        } catch (error) {
            throw new Error('Installazione automatica Node.js fallita. Installa manualmente Node.js 18+ da https://nodejs.org');
        }
    }

    /**
     * Installa Node.js su macOS
     */
    async installNodeJSMacOS() {
        try {
            await this.executeCommand('brew install node@18');
            this.nodePath = '/opt/homebrew/bin/node';
            console.log('✅ Node.js installato con Homebrew');
        } catch (error) {
            throw new Error('Installazione automatica Node.js fallita. Installa manualmente Node.js 18+');
        }
    }

    /**
     * Installa Node.js su Linux
     */
    async installNodeJSLinux() {
        try {
            await this.executeCommand('curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -');
            await this.executeCommand('sudo apt-get install -y nodejs');
            this.nodePath = 'node';
            console.log('✅ Node.js installato per Linux');
        } catch (error) {
            throw new Error('Installazione automatica Node.js fallita');
        }
    }

    /**
     * Crea e verifica ambiente virtuale
     */
    async ensureVirtualEnvironment() {
        console.log('🌍 Configurazione ambiente virtuale...');
        
        // Verifica se l'ambiente virtuale esiste già
        if (fs.existsSync(this.venvDir)) {
            console.log('✅ Ambiente virtuale esistente trovato');
            this.venvPythonPath = this.venvPaths[this.platform].python;
            return;
        }
        
        // Crea nuovo ambiente virtuale
        console.log('📦 Creazione nuovo ambiente virtuale...');
        await this.createVirtualEnvironment();
        this.venvPythonPath = this.venvPaths[this.platform].python;
    }

    /**
     * Crea ambiente virtuale
     */
    async createVirtualEnvironment() {
        const command = `"${this.pythonPath}" -m venv "${this.venvDir}"`;
        await this.executeCommand(command);
        console.log('✅ Ambiente virtuale creato');
    }

    /**
     * Installa dipendenze Python nell'ambiente virtuale
     */
    async installPythonDependencies() {
        console.log('📦 Installazione dipendenze Python...');
        
        const pipPath = this.venvPaths[this.platform].pip;
        const requirementsPath = path.join(this.appDir, 'requirements.txt');
        
        if (!fs.existsSync(requirementsPath)) {
            console.log('⚠️ requirements.txt non trovato');
            return;
        }
        
        const command = `"${pipPath}" install -r "${requirementsPath}"`;
        await this.executeCommand(command);
        console.log('✅ Dipendenze Python installate');
    }

    /**
     * Verifica la configurazione finale
     */
    async verifySetup() {
        console.log('🔍 Verifica configurazione finale...');
        
        // Verifica Python nell'ambiente virtuale
        const pythonVersion = await this.executeCommand(`"${this.venvPythonPath}" --version`);
        console.log('Python venv:', pythonVersion.stdout);
        
        // Verifica Django
        const djangoVersion = await this.executeCommand(`"${this.venvPythonPath}" -c "import django; print(django.get_version())"`);
        console.log('Django:', djangoVersion.stdout);
        
        // Verifica Node.js
        const nodeVersion = await this.executeCommand(`"${this.nodePath}" --version`);
        console.log('Node.js:', nodeVersion.stdout);
        
        console.log('✅ Configurazione verificata con successo');
    }

    /**
     * Ottiene il percorso Python dell'ambiente virtuale
     */
    getVenvPythonPath() {
        return this.venvPythonPath;
    }

    /**
     * Ottiene il percorso Node.js
     */
    getNodePath() {
        return this.nodePath;
    }

    /**
     * Esegue un comando e restituisce il risultato
     */
    executeCommand(command) {
        return new Promise((resolve) => {
            exec(command, (error, stdout, stderr) => {
                resolve({
                    success: !error,
                    stdout: stdout.trim(),
                    stderr: stderr.trim(),
                    error: error
                });
            });
        });
    }

    /**
     * Rileva la distribuzione Linux
     */
    async detectLinuxDistro() {
        try {
            const result = await this.executeCommand('cat /etc/os-release');
            if (result.stdout.includes('ubuntu')) return 'ubuntu';
            if (result.stdout.includes('debian')) return 'debian';
            if (result.stdout.includes('fedora')) return 'fedora';
            if (result.stdout.includes('arch')) return 'arch';
            return 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
}

module.exports = RobustDependencyManager;
