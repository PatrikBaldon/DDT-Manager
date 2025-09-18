const { app, dialog, ipcMain } = require('electron');
const Store = require('electron-store');
const path = require('path');
const fs = require('fs');

class SettingsManager {
    constructor() {
        this.store = new Store({
            defaults: {
                // Impostazioni generali
                general: {
                    language: 'it',
                    theme: 'light',
                    autoStart: false,
                    minimizeToTray: true,
                    checkUpdates: true
                },
                
                // Impostazioni dell'applicazione
                application: {
                    windowWidth: 1200,
                    windowHeight: 800,
                    windowX: null,
                    windowY: null,
                    maximized: false
                },
                
                // Impostazioni del database
                database: {
                    backupEnabled: true,
                    backupInterval: 24, // ore
                    backupRetention: 30, // giorni
                    backupPath: path.join(app.getPath('userData'), 'backups')
                },
                
                // Impostazioni PDF
                pdf: {
                    defaultFormat: 'A4',
                    defaultOrientation: 'portrait',
                    includeLogo: true,
                    logoPath: null,
                    fontSize: 12,
                    margin: 20
                },
                
                // Impostazioni di rete
                network: {
                    timeout: 30000, // millisecondi
                    retryAttempts: 3,
                    proxyEnabled: false,
                    proxyHost: '',
                    proxyPort: 8080
                },
                
                // Impostazioni di sicurezza
                security: {
                    requirePassword: false,
                    password: null,
                    sessionTimeout: 0, // minuti, 0 = disabilitato
                    encryptData: false
                },
                
                // Impostazioni di logging
                logging: {
                    enabled: true,
                    level: 'info',
                    maxFileSize: 10, // MB
                    maxFiles: 5
                }
            }
        });
        
        this.setupIpcHandlers();
    }
    
    setupIpcHandlers() {
        // Ottieni tutte le impostazioni
        ipcMain.handle('settings-get-all', () => {
            return this.store.store;
        });
        
        // Ottieni una specifica impostazione
        ipcMain.handle('settings-get', (event, key) => {
            return this.store.get(key);
        });
        
        // Imposta una specifica impostazione
        ipcMain.handle('settings-set', (event, key, value) => {
            this.store.set(key, value);
            return true;
        });
        
        // Resetta tutte le impostazioni
        ipcMain.handle('settings-reset', () => {
            this.store.clear();
            return true;
        });
        
        // Esporta le impostazioni
        ipcMain.handle('settings-export', async (event, filePath) => {
            try {
                const settings = this.store.store;
                await fs.promises.writeFile(filePath, JSON.stringify(settings, null, 2));
                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });
        
        // Importa le impostazioni
        ipcMain.handle('settings-import', async (event, filePath) => {
            try {
                const data = await fs.promises.readFile(filePath, 'utf8');
                const settings = JSON.parse(data);
                this.store.store = settings;
                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });
        
        // Seleziona file per import/export
        ipcMain.handle('settings-select-file', async (event, operation) => {
            const result = await dialog.showSaveDialog({
                title: operation === 'export' ? 'Esporta Impostazioni' : 'Importa Impostazioni',
                defaultPath: `ddt-settings-${new Date().toISOString().split('T')[0]}.json`,
                filters: [
                    { name: 'JSON Files', extensions: ['json'] },
                    { name: 'All Files', extensions: ['*'] }
                ]
            });
            
            return result;
        });
    }
    
    // Metodi per gestire le impostazioni specifiche
    
    getLanguage() {
        return this.store.get('general.language');
    }
    
    setLanguage(language) {
        this.store.set('general.language', language);
    }
    
    getTheme() {
        return this.store.get('general.theme');
    }
    
    setTheme(theme) {
        this.store.set('general.theme', theme);
    }
    
    getAutoStart() {
        return this.store.get('general.autoStart');
    }
    
    setAutoStart(enabled) {
        this.store.set('general.autoStart', enabled);
    }
    
    getWindowState() {
        return {
            width: this.store.get('application.windowWidth'),
            height: this.store.get('application.windowHeight'),
            x: this.store.get('application.windowX'),
            y: this.store.get('application.windowY'),
            maximized: this.store.get('application.maximized')
        };
    }
    
    setWindowState(state) {
        this.store.set('application.windowWidth', state.width);
        this.store.set('application.windowHeight', state.height);
        this.store.set('application.windowX', state.x);
        this.store.set('application.windowY', state.y);
        this.store.set('application.maximized', state.maximized);
    }
    
    getBackupSettings() {
        return {
            enabled: this.store.get('database.backupEnabled'),
            interval: this.store.get('database.backupInterval'),
            retention: this.store.get('database.backupRetention'),
            path: this.store.get('database.backupPath')
        };
    }
    
    setBackupSettings(settings) {
        this.store.set('database.backupEnabled', settings.enabled);
        this.store.set('database.backupInterval', settings.interval);
        this.store.set('database.backupRetention', settings.retention);
        this.store.set('database.backupPath', settings.path);
    }
    
    getPdfSettings() {
        return {
            format: this.store.get('pdf.defaultFormat'),
            orientation: this.store.get('pdf.defaultOrientation'),
            includeLogo: this.store.get('pdf.includeLogo'),
            logoPath: this.store.get('pdf.logoPath'),
            fontSize: this.store.get('pdf.fontSize'),
            margin: this.store.get('pdf.margin')
        };
    }
    
    setPdfSettings(settings) {
        this.store.set('pdf.defaultFormat', settings.format);
        this.store.set('pdf.defaultOrientation', settings.orientation);
        this.store.set('pdf.includeLogo', settings.includeLogo);
        this.store.set('pdf.logoPath', settings.logoPath);
        this.store.set('pdf.fontSize', settings.fontSize);
        this.store.set('pdf.margin', settings.margin);
    }
    
    // Metodo per validare le impostazioni
    validateSettings(settings) {
        const errors = [];
        
        // Valida dimensioni finestra
        if (settings.application && settings.application.windowWidth) {
            if (settings.application.windowWidth < 800 || settings.application.windowWidth > 3840) {
                errors.push('Larghezza finestra deve essere tra 800 e 3840 pixel');
            }
        }
        
        if (settings.application && settings.application.windowHeight) {
            if (settings.application.windowHeight < 600 || settings.application.windowHeight > 2160) {
                errors.push('Altezza finestra deve essere tra 600 e 2160 pixel');
            }
        }
        
        // Valida intervallo backup
        if (settings.database && settings.database.backupInterval) {
            if (settings.database.backupInterval < 1 || settings.database.backupInterval > 168) {
                errors.push('Intervallo backup deve essere tra 1 e 168 ore');
            }
        }
        
        // Valida dimensione font
        if (settings.pdf && settings.pdf.fontSize) {
            if (settings.pdf.fontSize < 8 || settings.pdf.fontSize > 24) {
                errors.push('Dimensione font deve essere tra 8 e 24');
            }
        }
        
        return errors;
    }
    
    // Metodo per creare backup delle impostazioni
    async createBackup() {
        try {
            const backupDir = path.join(app.getPath('userData'), 'backups');
            if (!fs.existsSync(backupDir)) {
                fs.mkdirSync(backupDir, { recursive: true });
            }
            
            const backupFile = path.join(backupDir, `settings-backup-${new Date().toISOString().split('T')[0]}.json`);
            const settings = this.store.store;
            await fs.promises.writeFile(backupFile, JSON.stringify(settings, null, 2));
            
            return { success: true, file: backupFile };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

module.exports = SettingsManager;
