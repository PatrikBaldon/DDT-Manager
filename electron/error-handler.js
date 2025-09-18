const { app, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

class ErrorHandler {
    constructor(logger) {
        this.logger = logger;
        this.errorLogFile = path.join(app.getPath('userData'), 'logs', 'errors.log');
        this.setupGlobalHandlers();
    }
    
    setupGlobalHandlers() {
        // Gestisce errori non catturati
        process.on('uncaughtException', (error) => {
            this.handleError('uncaughtException', error);
        });
        
        // Gestisce promesse rifiutate
        process.on('unhandledRejection', (reason, promise) => {
            this.handleError('unhandledRejection', reason, { promise });
        });
        
        // Gestisce errori di Electron
        app.on('render-process-gone', (event, webContents, details) => {
            this.handleError('render-process-gone', new Error(details.reason), details);
        });
        
        app.on('child-process-gone', (event, details) => {
            this.handleError('child-process-gone', new Error(details.reason), details);
        });
    }
    
    handleError(type, error, context = {}) {
        const errorInfo = {
            type,
            message: error.message || error,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            context,
            platform: process.platform,
            arch: process.arch,
            version: app.getVersion(),
            electronVersion: process.versions.electron,
            nodeVersion: process.versions.node
        };
        
        // Logga l'errore
        this.logger.error(`Errore ${type}`, errorInfo);
        
        // Salva l'errore nel file di log specifico
        this.saveErrorToFile(errorInfo);
        
        // Mostra una notifica all'utente per errori critici
        if (this.isCriticalError(type, error)) {
            this.showErrorDialog(errorInfo);
        }
    }
    
    isCriticalError(type, error) {
        // Errori critici che richiedono l'attenzione dell'utente
        const criticalTypes = [
            'uncaughtException',
            'render-process-gone',
            'child-process-gone'
        ];
        
        const criticalMessages = [
            'ENOENT',
            'EACCES',
            'EMFILE',
            'ENOSPC',
            'database',
            'connection',
            'memory'
        ];
        
        return criticalTypes.includes(type) || 
               criticalMessages.some(msg => 
                   error.message && error.message.toLowerCase().includes(msg)
               );
    }
    
    showErrorDialog(errorInfo) {
        const options = {
            type: 'error',
            title: 'Errore Critico - DDT Manager',
            message: 'Si è verificato un errore critico nell\'applicazione.',
            detail: `Tipo: ${errorInfo.type}\nMessaggio: ${errorInfo.message}\n\nL'errore è stato registrato nei log.`,
            buttons: ['OK', 'Mostra Log', 'Riavvia Applicazione'],
            defaultId: 0,
            cancelId: 0
        };
        
        dialog.showMessageBox(null, options).then((result) => {
            switch (result.response) {
                case 1: // Mostra Log
                    this.showErrorLog();
                    break;
                case 2: // Riavvia Applicazione
                    app.relaunch();
                    app.exit();
                    break;
            }
        });
    }
    
    showErrorLog() {
        try {
            const logContent = this.getErrorLogContent();
            const options = {
                type: 'info',
                title: 'Log Errori - DDT Manager',
                message: 'Ultimi errori registrati:',
                detail: logContent,
                buttons: ['OK', 'Esporta Log'],
                defaultId: 0,
                cancelId: 0
            };
            
            dialog.showMessageBox(null, options).then((result) => {
                if (result.response === 1) { // Esporta Log
                    this.exportErrorLog();
                }
            });
        } catch (error) {
            this.logger.error('Errore visualizzazione log', { error: error.message });
        }
    }
    
    getErrorLogContent() {
        try {
            if (!fs.existsSync(this.errorLogFile)) {
                return 'Nessun errore registrato.';
            }
            
            const content = fs.readFileSync(this.errorLogFile, 'utf8');
            const lines = content.split('\n').filter(line => line.trim());
            const recentLines = lines.slice(-20); // Ultimi 20 errori
            
            return recentLines.join('\n');
        } catch (error) {
            return 'Errore durante la lettura del log.';
        }
    }
    
    exportErrorLog() {
        try {
            const exportPath = path.join(app.getPath('userData'), 'error-log-export.txt');
            const content = this.getErrorLogContent();
            
            fs.writeFileSync(exportPath, content);
            
            dialog.showMessageBox(null, {
                type: 'info',
                title: 'Log Esportato',
                message: 'Il log degli errori è stato esportato con successo.',
                detail: `Percorso: ${exportPath}`,
                buttons: ['OK']
            });
        } catch (error) {
            this.logger.error('Errore esportazione log', { error: error.message });
        }
    }
    
    saveErrorToFile(errorInfo) {
        try {
            const errorLine = JSON.stringify(errorInfo) + '\n';
            fs.appendFileSync(this.errorLogFile, errorLine);
        } catch (error) {
            // Se non possiamo salvare nel file, almeno logghiamo
            this.logger.error('Errore salvataggio log errori', { error: error.message });
        }
    }
    
    // Metodi per gestire errori specifici
    
    handleDjangoError(error) {
        this.handleError('django-error', error, { component: 'django' });
    }
    
    handleDatabaseError(error) {
        this.handleError('database-error', error, { component: 'database' });
    }
    
    handlePdfError(error) {
        this.handleError('pdf-error', error, { component: 'pdf' });
    }
    
    handleNetworkError(error) {
        this.handleError('network-error', error, { component: 'network' });
    }
    
    handleFileSystemError(error) {
        this.handleError('filesystem-error', error, { component: 'filesystem' });
    }
    
    // Metodo per pulire i log degli errori
    clearErrorLog() {
        try {
            if (fs.existsSync(this.errorLogFile)) {
                fs.unlinkSync(this.errorLogFile);
                this.logger.info('Log errori pulito');
            }
        } catch (error) {
            this.logger.error('Errore pulizia log errori', { error: error.message });
        }
    }
    
    // Metodo per ottenere statistiche degli errori
    getErrorStats() {
        try {
            if (!fs.existsSync(this.errorLogFile)) {
                return { total: 0, byType: {}, byComponent: {} };
            }
            
            const content = fs.readFileSync(this.errorLogFile, 'utf8');
            const lines = content.split('\n').filter(line => line.trim());
            
            const stats = {
                total: lines.length,
                byType: {},
                byComponent: {}
            };
            
            lines.forEach(line => {
                try {
                    const errorInfo = JSON.parse(line);
                    
                    // Conta per tipo
                    stats.byType[errorInfo.type] = (stats.byType[errorInfo.type] || 0) + 1;
                    
                    // Conta per componente
                    if (errorInfo.context && errorInfo.context.component) {
                        stats.byComponent[errorInfo.context.component] = 
                            (stats.byComponent[errorInfo.context.component] || 0) + 1;
                    }
                } catch (parseError) {
                    // Ignora righe non valide
                }
            });
            
            return stats;
        } catch (error) {
            this.logger.error('Errore calcolo statistiche errori', { error: error.message });
            return { total: 0, byType: {}, byComponent: {} };
        }
    }
}

module.exports = ErrorHandler;
