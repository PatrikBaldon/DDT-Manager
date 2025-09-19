const { exec } = require('child_process');
const path = require('path');

class DependencyManager {
    constructor() {
        this.pythonPath = null;
        this.nodePath = null;
    }

    /**
     * Trova Python disponibile nel sistema
     */
    async findPython() {
        if (this.pythonPath) {
            return this.pythonPath;
        }

        const candidates = [
            // Percorsi comuni su macOS
            'python3',
            'python',
            '/opt/anaconda3/bin/python3',
            '/opt/homebrew/bin/python3',
            '/usr/bin/python3',
            '/usr/local/bin/python3',
            '/opt/miniconda3/bin/python3',
            
            // Percorsi comuni su Windows
            'python',
            'python3',
            'C:\\Python39\\python.exe',
            'C:\\Python310\\python.exe',
            'C:\\Python311\\python.exe',
            'C:\\Python312\\python.exe',
            'C:\\Python313\\python.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python39\\python.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python310\\python.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python311\\python.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python312\\python.exe',
            
            // Percorsi comuni su Linux
            '/usr/bin/python3',
            '/usr/local/bin/python3',
            '/opt/python3/bin/python3',
            'python3',
            'python'
        ];

        return new Promise((resolve) => {
            let index = 0;
            
            const tryNext = () => {
                if (index >= candidates.length) {
                    console.warn('Python non trovato, usando fallback');
                    resolve('python3');
                    return;
                }
                
                const candidate = candidates[index++];
                const expandedCandidate = candidate.replace('%USERNAME%', process.env.USERNAME || '');
                
                exec(`"${expandedCandidate}" --version`, (error, stdout) => {
                    if (error) {
                        tryNext();
                    } else {
                        console.log('Python trovato:', expandedCandidate, stdout.trim());
                        this.pythonPath = expandedCandidate;
                        resolve(expandedCandidate);
                    }
                });
            };
            
            tryNext();
        });
    }

    /**
     * Trova Node.js disponibile nel sistema
     */
    async findNode() {
        if (this.nodePath) {
            return this.nodePath;
        }

        const candidates = [
            // Percorsi comuni su macOS
            'node',
            '/opt/homebrew/bin/node',
            '/usr/local/bin/node',
            '/opt/node/bin/node',
            
            // Percorsi comuni su Windows
            'node',
            'C:\\Program Files\\nodejs\\node.exe',
            'C:\\Program Files (x86)\\nodejs\\node.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Roaming\\npm\\node.exe',
            'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\nodejs\\node.exe',
            
            // Percorsi comuni su Linux
            '/usr/bin/node',
            '/usr/local/bin/node',
            '/opt/node/bin/node',
            'node'
        ];

        return new Promise((resolve) => {
            let index = 0;
            
            const tryNext = () => {
                if (index >= candidates.length) {
                    console.warn('Node.js non trovato, usando fallback');
                    resolve('node');
                    return;
                }
                
                const candidate = candidates[index++];
                const expandedCandidate = candidate.replace('%USERNAME%', process.env.USERNAME || '');
                
                exec(`"${expandedCandidate}" --version`, (error, stdout) => {
                    if (error) {
                        tryNext();
                    } else {
                        console.log('Node.js trovato:', expandedCandidate, stdout.trim());
                        this.nodePath = expandedCandidate;
                        resolve(expandedCandidate);
                    }
                });
            };
            
            tryNext();
        });
    }

    /**
     * Verifica se Python ha Django installato
     */
    async checkDjango(pythonPath) {
        return new Promise((resolve) => {
            exec(`"${pythonPath}" -c "import django; print(django.get_version())"`, (error, stdout) => {
                if (error) {
                    console.error('Django non trovato:', error.message);
                    resolve(false);
                } else {
                    console.log('Django versione:', stdout.trim());
                    resolve(true);
                }
            });
        });
    }

    /**
     * Verifica se Node.js ha npm installato
     */
    async checkNpm(nodePath) {
        return new Promise((resolve) => {
            exec(`"${nodePath}" -e "console.log(require('child_process').execSync('npm --version').toString().trim())"`, (error, stdout) => {
                if (error) {
                    console.error('npm non trovato:', error.message);
                    resolve(false);
                } else {
                    console.log('npm versione:', stdout.trim());
                    resolve(true);
                }
            });
        });
    }

    /**
     * Inizializza tutte le dipendenze
     */
    async initialize() {
        console.log('Inizializzazione dipendenze...');
        
        const python = await this.findPython();
        const node = await this.findNode();
        
        const djangoOk = await this.checkDjango(python);
        const npmOk = await this.checkNpm(node);
        
        return {
            python,
            node,
            djangoOk,
            npmOk,
            allOk: djangoOk && npmOk
        };
    }

    /**
     * Ottieni informazioni dettagliate sulle dipendenze
     */
    getInfo() {
        return {
            python: this.pythonPath,
            node: this.nodePath,
            platform: process.platform,
            arch: process.arch
        };
    }
}

module.exports = DependencyManager;
