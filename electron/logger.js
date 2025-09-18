const { app } = require('electron');
const path = require('path');
const fs = require('fs');
const { format } = require('date-fns');

class Logger {
    constructor() {
        this.logDir = path.join(app.getPath('userData'), 'logs');
        this.logFile = path.join(this.logDir, 'ddt-manager.log');
        this.maxFileSize = 10 * 1024 * 1024; // 10MB
        this.maxFiles = 5;
        this.level = 'info';
        
        // Crea la directory dei log se non esiste
        this.ensureLogDir();
        
        // Livelli di log
        this.levels = {
            error: 0,
            warn: 1,
            info: 2,
            debug: 3
        };
    }
    
    ensureLogDir() {
        if (!fs.existsSync(this.logDir)) {
            fs.mkdirSync(this.logDir, { recursive: true });
        }
    }
    
    setLevel(level) {
        this.level = level;
    }
    
    shouldLog(level) {
        return this.levels[level] <= this.levels[this.level];
    }
    
    formatMessage(level, message, meta = {}) {
        const timestamp = format(new Date(), 'yyyy-MM-dd HH:mm:ss.SSS');
        const metaStr = Object.keys(meta).length > 0 ? ` ${JSON.stringify(meta)}` : '';
        return `[${timestamp}] [${level.toUpperCase()}] ${message}${metaStr}`;
    }
    
    writeToFile(message) {
        try {
            // Controlla la dimensione del file
            if (fs.existsSync(this.logFile)) {
                const stats = fs.statSync(this.logFile);
                if (stats.size > this.maxFileSize) {
                    this.rotateLogs();
                }
            }
            
            // Scrive il messaggio nel file
            fs.appendFileSync(this.logFile, message + '\n');
        } catch (error) {
            console.error('Errore durante la scrittura del log:', error);
        }
    }
    
    rotateLogs() {
        try {
            // Sposta i file esistenti
            for (let i = this.maxFiles - 1; i > 0; i--) {
                const oldFile = `${this.logFile}.${i}`;
                const newFile = `${this.logFile}.${i + 1}`;
                
                if (fs.existsSync(oldFile)) {
                    if (i === this.maxFiles - 1) {
                        // Elimina il file più vecchio
                        fs.unlinkSync(oldFile);
                    } else {
                        fs.renameSync(oldFile, newFile);
                    }
                }
            }
            
            // Sposta il file corrente
            if (fs.existsSync(this.logFile)) {
                fs.renameSync(this.logFile, `${this.logFile}.1`);
            }
        } catch (error) {
            console.error('Errore durante la rotazione dei log:', error);
        }
    }
    
    log(level, message, meta = {}) {
        if (!this.shouldLog(level)) {
            return;
        }
        
        const formattedMessage = this.formatMessage(level, message, meta);
        
        // Stampa nella console
        switch (level) {
            case 'error':
                console.error(formattedMessage);
                break;
            case 'warn':
                console.warn(formattedMessage);
                break;
            case 'info':
                console.info(formattedMessage);
                break;
            case 'debug':
                console.debug(formattedMessage);
                break;
            default:
                console.log(formattedMessage);
        }
        
        // Scrive nel file
        this.writeToFile(formattedMessage);
    }
    
    error(message, meta = {}) {
        this.log('error', message, meta);
    }
    
    warn(message, meta = {}) {
        this.log('warn', message, meta);
    }
    
    info(message, meta = {}) {
        this.log('info', message, meta);
    }
    
    debug(message, meta = {}) {
        this.log('debug', message, meta);
    }
    
    // Metodi specifici per l'applicazione
    
    appStart() {
        this.info('Applicazione avviata', {
            version: app.getVersion(),
            platform: process.platform,
            arch: process.arch
        });
    }
    
    appExit() {
        this.info('Applicazione chiusa');
    }
    
    windowCreated(windowId) {
        this.info('Finestra creata', { windowId });
    }
    
    windowClosed(windowId) {
        this.info('Finestra chiusa', { windowId });
    }
    
    djangoStarted() {
        this.info('Server Django avviato');
    }
    
    djangoStopped() {
        this.info('Server Django fermato');
    }
    
    djangoError(error) {
        this.error('Errore server Django', { error: error.message, stack: error.stack });
    }
    
    updateAvailable(version) {
        this.info('Aggiornamento disponibile', { version });
    }
    
    updateDownloaded(version) {
        this.info('Aggiornamento scaricato', { version });
    }
    
    updateError(error) {
        this.error('Errore aggiornamento', { error: error.message });
    }
    
    settingsChanged(key, value) {
        this.debug('Impostazione modificata', { key, value });
    }
    
    databaseBackup(path) {
        this.info('Backup database creato', { path });
    }
    
    databaseBackupError(error) {
        this.error('Errore backup database', { error: error.message });
    }
    
    pdfGenerated(filename) {
        this.info('PDF generato', { filename });
    }
    
    pdfGenerationError(error) {
        this.error('Errore generazione PDF', { error: error.message });
    }
    
    // Metodo per ottenere i log recenti
    getRecentLogs(lines = 100) {
        try {
            if (!fs.existsSync(this.logFile)) {
                return [];
            }
            
            const content = fs.readFileSync(this.logFile, 'utf8');
            const logLines = content.split('\n').filter(line => line.trim());
            return logLines.slice(-lines);
        } catch (error) {
            this.error('Errore lettura log', { error: error.message });
            return [];
        }
    }
    
    // Metodo per pulire i log
    clearLogs() {
        try {
            if (fs.existsSync(this.logFile)) {
                fs.unlinkSync(this.logFile);
            }
            
            // Rimuovi anche i file di rotazione
            for (let i = 1; i <= this.maxFiles; i++) {
                const file = `${this.logFile}.${i}`;
                if (fs.existsSync(file)) {
                    fs.unlinkSync(file);
                }
            }
            
            this.info('Log puliti');
        } catch (error) {
            this.error('Errore pulizia log', { error: error.message });
        }
    }
    
    // Metodo per esportare i log
    exportLogs(filePath) {
        try {
            const logs = this.getRecentLogs();
            fs.writeFileSync(filePath, logs.join('\n'));
            this.info('Log esportati', { filePath });
            return { success: true };
        } catch (error) {
            this.error('Errore esportazione log', { error: error.message });
            return { success: false, error: error.message };
        }
    }
}

module.exports = Logger;
