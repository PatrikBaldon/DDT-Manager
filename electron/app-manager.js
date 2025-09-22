const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Logger = require('./logger');
const SettingsManager = require('./settings');
const BackupManager = require('./backup');
const ErrorHandler = require('./error-handler');
const PerformanceMonitor = require('./performance-monitor');
const NotificationManager = require('./notifications');
const Updater = require('./updater');
const DependencyManager = require('./dependency-manager');
const RobustDependencyManager = require('./robust-dependency-manager');

class AppManager {
    constructor() {
        this.logger = new Logger();
        this.settings = new SettingsManager();
        this.backup = new BackupManager(this.logger);
        this.errorHandler = new ErrorHandler(this.logger);
        this.performance = new PerformanceMonitor(this.logger);
        this.notifications = new NotificationManager();
        this.updater = null;
        this.dependencyManager = new DependencyManager();
        this.robustDependencyManager = new RobustDependencyManager();
        
        this.mainWindow = null;
        this.isQuitting = false;
        this.ipcHandlersSetup = false;
        
        this.setupAppEvents();
        this.setupIpcHandlers();
    }
    
    setupAppEvents() {
        // Eventi dell'applicazione
        app.whenReady().then(() => {
            this.onAppReady();
        });
        
        app.on('window-all-closed', () => {
            this.onWindowAllClosed();
        });
        
        app.on('activate', () => {
            this.onActivate();
        });
        
        app.on('before-quit', () => {
            this.onBeforeQuit();
        });
        
        app.on('will-quit', () => {
            this.onWillQuit();
        });
    }
    
    setupIpcHandlers() {
        // Evita di registrare i gestori più volte
        if (this.ipcHandlersSetup) {
            return;
        }
        
        // Rimuovi tutti i gestori esistenti per evitare duplicati
        try {
            ipcMain.removeAllListeners();
        } catch (error) {
            console.log('Nessun listener da rimuovere');
        }
        
        // Gestione finestra
        this.registerIpcHandler('window-minimize', () => {
            if (this.mainWindow) {
                this.mainWindow.minimize();
            }
        });
        
        this.registerIpcHandler('window-maximize', () => {
            if (this.mainWindow) {
                if (this.mainWindow.isMaximized()) {
                    this.mainWindow.unmaximize();
                } else {
                    this.mainWindow.maximize();
                }
            }
        });
        
        this.registerIpcHandler('window-close', () => {
            if (this.mainWindow) {
                this.mainWindow.close();
            }
        });
        
        // Gestione impostazioni
        this.registerIpcHandler('settings-get', (event, key) => {
            return this.settings.get(key);
        });
        
        this.registerIpcHandler('settings-set', (event, key, value) => {
            this.settings.set(key, value);
            this.logger.settingsChanged(key, value);
            return true;
        });
        
        // Gestione backup
        this.registerIpcHandler('backup-create', () => {
            return this.backup.createBackup();
        });
        
        this.registerIpcHandler('backup-list', () => {
            return this.backup.listBackups();
        });
        
        this.registerIpcHandler('backup-restore', (event, backupFile) => {
            return this.backup.restoreBackup(backupFile);
        });
        
        // Gestione performance
        this.registerIpcHandler('performance-get-metrics', () => {
            return this.performance.getMetrics();
        });
        
        this.registerIpcHandler('performance-get-report', () => {
            return this.performance.getPerformanceReport();
        });
        
        // Gestione aggiornamenti
        this.registerIpcHandler('updater-check', () => {
            if (this.updater) {
                this.updater.checkForUpdates();
            }
            return true;
        });
        
        this.registerIpcHandler('updater-download', () => {
            if (this.updater) {
                this.updater.downloadUpdateManually();
            }
            return true;
        });
        
        this.registerIpcHandler('updater-install', () => {
            if (this.updater) {
                this.updater.installUpdateManually();
            }
            return true;
        });
        
        // Gestione notifiche
        this.registerIpcHandler('notifications-show', (event, type, message) => {
            switch (type) {
                case 'info':
                    this.notifications.showInfo(message);
                    break;
                case 'warning':
                    this.notifications.showWarning(message);
                    break;
                case 'error':
                    this.notifications.showError(message);
                    break;
            }
        });
        
        // Marca i gestori come configurati
        this.ipcHandlersSetup = true;
    }
    
    registerIpcHandler(channel, handler) {
        try {
            // Rimuovi handler esistente se presente
            ipcMain.removeHandler(channel);
            // Registra il nuovo handler
            ipcMain.handle(channel, handler);
        } catch (error) {
            console.log(`Errore registrazione handler ${channel}:`, error.message);
        }
    }
    
    async onAppReady() {
        try {
            this.logger.appStart();
            
            // Crea la finestra principale PRIMA di configurare l'ambiente
            await this.createMainWindow();
            
            // Configura automaticamente l'ambiente in background (non bloccante)
            this.setupEnvironment().then(success => {
                if (success) {
                    this.notifications.show('Ambiente configurato', 'Python, Node.js e dipendenze installati automaticamente');
                    // Avvia Django dopo la configurazione
                    this.initializeDependencies();
                }
            }).catch(error => {
                console.error('Errore configurazione ambiente in background:', error);
                this.notifications.show('Errore configurazione', 'Controlla che Python e Node.js siano installati');
                // Prova comunque ad avviare con dipendenze esistenti
                this.initializeDependencies();
            });
            
            // Inizializza l'updater se in produzione
            if (process.env.NODE_ENV === 'production') {
                this.updater = new Updater(this.mainWindow);
            }
            
            // Avvia il monitoraggio delle performance
            this.performance.startMonitoring();
            
            // Mostra notifica di benvenuto
            this.notifications.showWelcome();
            
            this.logger.info('Applicazione inizializzata con successo');
            
        } catch (error) {
            this.errorHandler.handleError('app-initialization', error);
            app.quit();
        }
    }
    
    /**
     * Configura automaticamente l'ambiente di sviluppo
     */
    async setupEnvironment() {
        try {
            console.log('🔧 Configurazione automatica ambiente...');
            
            // Usa il sistema robusto per configurare tutto
            const success = await this.robustDependencyManager.setupEnvironment();
            
            if (success) {
                console.log('✅ Ambiente configurato automaticamente');
                return true;
            } else {
                console.warn('⚠️ Configurazione ambiente fallita, continuo comunque...');
                return false;
            }
            
        } catch (error) {
            console.error('❌ Errore configurazione ambiente:', error);
            return false;
        }
    }
    
    async createMainWindow() {
        const windowState = this.settings.getWindowState();
        
        this.mainWindow = new BrowserWindow({
            width: windowState.width,
            height: windowState.height,
            x: windowState.x,
            y: windowState.y,
            minWidth: 800,
            minHeight: 600,
            show: true,
            titleBarStyle: 'default',
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                preload: path.join(__dirname, 'preload.js')
            }
        });
        
        // Carica l'applicazione Django
        try {
            await this.loadDjangoApp();
        } catch (error) {
            console.error('Errore nel caricamento di Django:', error);
            // Mostra la finestra anche se Django non si carica
            this.mainWindow.show();
            this.mainWindow.focus();
        }
        
        // Gestisci eventi della finestra
        this.mainWindow.on('ready-to-show', () => {
            this.mainWindow.show();
            this.mainWindow.focus();
            this.performance.recordStartupComplete();
        });
        
        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
        });
        
        this.mainWindow.on('resize', () => {
            this.saveWindowState();
        });
        
        this.mainWindow.on('move', () => {
            this.saveWindowState();
        });
        
        this.mainWindow.on('maximize', () => {
            this.saveWindowState();
        });
        
        this.mainWindow.on('unmaximize', () => {
            this.saveWindowState();
        });
        
        this.logger.windowCreated(this.mainWindow.id);
    }
    
    async loadDjangoApp() {
        try {
            // Verifica se Django è già in esecuzione
            const isDjangoRunning = await this.checkDjangoServer();
            
            if (!isDjangoRunning) {
                // Avvia il server Django
                await this.startDjangoServer();
            }
            
            // Attendi che Django sia pronto
            await this.waitForDjangoServer();
            
            // Carica l'applicazione
            const djangoUrl = 'http://localhost:8000';
            await this.mainWindow.loadURL(djangoUrl);
            
            this.logger.djangoStarted();
            
        } catch (error) {
            this.errorHandler.handleDjangoError(error);
            
            // Mostra pagina di errore invece di chiudere l'app
            await this.mainWindow.loadURL('data:text/html,<html><body><h1>Errore Django</h1><p>Impossibile connettersi al server Django. Controlla i log per maggiori dettagli.</p><p>Errore: ' + error.message + '</p></body></html>');
        }
    }
    
    async checkDjangoServer() {
        return new Promise((resolve) => {
            const http = require('http');
            const req = http.get('http://localhost:8000', (res) => {
                resolve(true);
            });
            req.on('error', () => {
                resolve(false);
            });
            req.setTimeout(1000, () => {
                req.destroy();
                resolve(false);
            });
        });
    }
    
    async waitForDjangoServer() {
        return new Promise((resolve, reject) => {
            const maxAttempts = 30; // 30 secondi
            let attempts = 0;
            
            const checkServer = () => {
                attempts++;
                this.checkDjangoServer().then(isRunning => {
                    if (isRunning) {
                        resolve();
                    } else if (attempts >= maxAttempts) {
                        reject(new Error('Timeout: Django server non risponde'));
                    } else {
                        setTimeout(checkServer, 1000);
                    }
                });
            };
            
            checkServer();
        });
    }
    
            async startDjangoServer() {
                return new Promise(async (resolve, reject) => {
                    try {
                        // Inizializza le dipendenze
                        const deps = await this.dependencyManager.initialize();
                        
                        if (!deps.allOk) {
                            throw new Error(`Dipendenze mancanti: Python=${deps.python}, Django=${deps.djangoOk}, Node=${deps.node}, npm=${deps.npmOk}`);
                        }
                        
                        const { spawn } = require('child_process');
                        const fs = require('fs');
                        const os = require('os');
                        
                        // Crea directory per Django nell'home directory
                        const djangoDir = path.join(os.homedir(), '.ddt-manager', 'django');
                        if (!fs.existsSync(djangoDir)) {
                            fs.mkdirSync(djangoDir, { recursive: true });
                        }
                        
                        // Copia i file Django necessari
                        await this.copyDjangoFiles(djangoDir);
                        
                        const managePyPath = path.join(djangoDir, 'manage.py');
                        
                        // Usa il Python dell'ambiente virtuale se disponibile
                        const pythonPath = this.robustDependencyManager.getVenvPythonPath() || deps.python;
                        
                        console.log('Avvio Django con Python:', pythonPath);
                        console.log('Percorso manage.py:', managePyPath);
                        console.log('Directory di lavoro:', djangoDir);
                        
                        // Aggiungi il percorso Django al PYTHONPATH
                        const env = { ...process.env };
                        env.PYTHONPATH = djangoDir;
                        env.DJANGO_SETTINGS_MODULE = 'config.settings.development';
                        
                        const djangoProcess = spawn(pythonPath, [managePyPath, 'runserver', '--noreload'], {
                            cwd: djangoDir,
                            stdio: 'pipe',
                            detached: true, // Processo separato
                            env: env
                        });
                
                djangoProcess.stdout.on('data', (data) => {
                    const output = data.toString();
                    console.log('Django:', output);
                    
                    if (output.includes('Starting development server') || output.includes('Quit the server with')) {
                        resolve();
                    }
                });
                
                djangoProcess.stderr.on('data', (data) => {
                    console.error('Django Error:', data.toString());
                });
                
                djangoProcess.on('error', (error) => {
                    console.error('Errore avvio Django:', error);
                    reject(error);
                });
                
                // Timeout per l'avvio
                setTimeout(() => {
                    resolve();
                }, 5000);
                
            } catch (error) {
                console.error('Errore inizializzazione dipendenze:', error);
                reject(error);
            }
        });
    }
    
    async copyDjangoFiles(djangoDir) {
        const fs = require('fs');
        const path = require('path');
        
        // Lista dei file e cartelle da copiare
        const filesToCopy = [
            'manage.py',
            'requirements.txt',
            'db.sqlite3',
            'ddt_app',
            'ddt_project', 
            'config',
            'templates',
            'static'
        ];
        
        for (const item of filesToCopy) {
            const sourcePath = path.join(__dirname, '..', item);
            const destPath = path.join(djangoDir, item);
            
            try {
                if (fs.existsSync(sourcePath)) {
                    if (fs.statSync(sourcePath).isDirectory()) {
                        // Copia directory ricorsivamente
                        await this.copyDirectory(sourcePath, destPath);
                    } else {
                        // Copia file
                        fs.copyFileSync(sourcePath, destPath);
                    }
                    console.log(`Copiato: ${item}`);
                }
            } catch (error) {
                console.log(`Errore copia ${item}:`, error.message);
            }
        }
    }
    
    async copyDirectory(source, dest) {
        const fs = require('fs');
        const path = require('path');
        
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest, { recursive: true });
        }
        
        const items = fs.readdirSync(source);
        for (const item of items) {
            const sourcePath = path.join(source, item);
            const destPath = path.join(dest, item);
            
            if (fs.statSync(sourcePath).isDirectory()) {
                await this.copyDirectory(sourcePath, destPath);
            } else {
                fs.copyFileSync(sourcePath, destPath);
            }
        }
    }
    
    saveWindowState() {
        if (this.mainWindow && !this.mainWindow.isDestroyed()) {
            try {
                const bounds = this.mainWindow.getBounds();
                const isMaximized = this.mainWindow.isMaximized();
                
                this.settings.setWindowState({
                    width: bounds.width,
                    height: bounds.height,
                    x: bounds.x,
                    y: bounds.y,
                    maximized: isMaximized
                });
            } catch (error) {
                console.log('Window already destroyed, skipping state save');
            }
        }
    }
    
    onWindowAllClosed() {
        if (process.platform !== 'darwin') {
            app.quit();
        }
    }
    
    onActivate() {
        if (this.mainWindow === null) {
            this.createMainWindow();
        }
    }
    
    onBeforeQuit() {
        this.isQuitting = true;
        this.performance.stopMonitoring();
        this.logger.appExit();
    }
    
    onWillQuit() {
        // Salva le impostazioni finali
        this.saveWindowState();
        
        // Crea un backup finale se abilitato
        const backupSettings = this.settings.getBackupSettings();
        if (backupSettings.enabled) {
            this.backup.createBackup();
        }
    }
    
    // Metodi pubblici per la gestione dell'applicazione
    
    showMainWindow() {
        if (this.mainWindow) {
            this.mainWindow.show();
            this.mainWindow.focus();
        }
    }
    
    hideMainWindow() {
        if (this.mainWindow) {
            this.mainWindow.hide();
        }
    }
    
    toggleMainWindow() {
        if (this.mainWindow) {
            if (this.mainWindow.isVisible()) {
                this.hideMainWindow();
            } else {
                this.showMainWindow();
            }
        }
    }
    
    restartApp() {
        app.relaunch();
        app.exit();
    }
    
    quitApp() {
        this.isQuitting = true;
        app.quit();
    }
    
    // Metodi per la gestione degli errori
    
    handleError(error, context = {}) {
        this.errorHandler.handleError('app-error', error, context);
    }
    
    // Metodi per la gestione delle performance
    
    getPerformanceMetrics() {
        return this.performance.getMetrics();
    }
    
    getPerformanceReport() {
        return this.performance.getPerformanceReport();
    }
    
    // Metodi per la gestione delle impostazioni
    
    getSettings() {
        return this.settings.store.store;
    }
    
    updateSettings(settings) {
        Object.keys(settings).forEach(key => {
            this.settings.set(key, settings[key]);
        });
    }
    
    // Metodi per la gestione dei backup
    
    createBackup() {
        return this.backup.createBackup();
    }
    
    listBackups() {
        return this.backup.listBackups();
    }
    
    restoreBackup(backupFile) {
        return this.backup.restoreBackup(backupFile);
    }
}

module.exports = AppManager;
