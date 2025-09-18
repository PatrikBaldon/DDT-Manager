const { app, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const cron = require('node-cron');

class BackupManager {
    constructor(logger) {
        this.logger = logger;
        this.backupDir = path.join(app.getPath('userData'), 'backups');
        this.dbPath = path.join(__dirname, '..', 'db.sqlite3');
        this.isBackupRunning = false;
        this.backupTask = null;
        
        // Crea la directory di backup se non esiste
        this.ensureBackupDir();
        
        // Configura i listener IPC
        this.setupIpcHandlers();
    }
    
    ensureBackupDir() {
        if (!fs.existsSync(this.backupDir)) {
            fs.mkdirSync(this.backupDir, { recursive: true });
        }
    }
    
    setupIpcHandlers() {
        // Crea backup manuale
        ipcMain.handle('backup-create', async () => {
            return await this.createBackup();
        });
        
        // Lista backup disponibili
        ipcMain.handle('backup-list', () => {
            return this.listBackups();
        });
        
        // Ripristina backup
        ipcMain.handle('backup-restore', async (event, backupFile) => {
            return await this.restoreBackup(backupFile);
        });
        
        // Elimina backup
        ipcMain.handle('backup-delete', async (event, backupFile) => {
            return await this.deleteBackup(backupFile);
        });
        
        // Configura backup automatico
        ipcMain.handle('backup-schedule', async (event, schedule) => {
            return await this.scheduleBackup(schedule);
        });
        
        // Ferma backup automatico
        ipcMain.handle('backup-stop-schedule', () => {
            return this.stopScheduledBackup();
        });
    }
    
    async createBackup() {
        if (this.isBackupRunning) {
            return { success: false, error: 'Backup già in corso' };
        }
        
        this.isBackupRunning = true;
        
        try {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupFile = path.join(this.backupDir, `ddt-backup-${timestamp}.sqlite3`);
            
            // Verifica che il database esista
            if (!fs.existsSync(this.dbPath)) {
                throw new Error('Database non trovato');
            }
            
            // Copia il database
            await fs.promises.copyFile(this.dbPath, backupFile);
            
            // Comprimi il backup se possibile
            const compressedFile = await this.compressBackup(backupFile);
            
            // Rimuovi il file non compresso se la compressione è riuscita
            if (compressedFile && compressedFile !== backupFile) {
                await fs.promises.unlink(backupFile);
            }
            
            this.logger.databaseBackup(compressedFile || backupFile);
            
            return {
                success: true,
                file: compressedFile || backupFile,
                size: fs.statSync(compressedFile || backupFile).size
            };
            
        } catch (error) {
            this.logger.databaseBackupError(error);
            return { success: false, error: error.message };
        } finally {
            this.isBackupRunning = false;
        }
    }
    
    async compressBackup(backupFile) {
        try {
            // Prova a usare gzip se disponibile
            const compressedFile = `${backupFile}.gz`;
            
            return new Promise((resolve, reject) => {
                const gzip = spawn('gzip', ['-c', backupFile]);
                const writeStream = fs.createWriteStream(compressedFile);
                
                gzip.stdout.pipe(writeStream);
                
                gzip.on('close', (code) => {
                    if (code === 0) {
                        resolve(compressedFile);
                    } else {
                        resolve(backupFile); // Fallback al file non compresso
                    }
                });
                
                gzip.on('error', () => {
                    resolve(backupFile); // Fallback al file non compresso
                });
            });
        } catch (error) {
            return backupFile; // Fallback al file non compresso
        }
    }
    
    listBackups() {
        try {
            const files = fs.readdirSync(this.backupDir);
            const backups = files
                .filter(file => file.startsWith('ddt-backup-') && file.endsWith('.sqlite3'))
                .map(file => {
                    const filePath = path.join(this.backupDir, file);
                    const stats = fs.statSync(filePath);
                    return {
                        name: file,
                        path: filePath,
                        size: stats.size,
                        created: stats.birthtime,
                        modified: stats.mtime
                    };
                })
                .sort((a, b) => b.created - a.created);
            
            return { success: true, backups };
        } catch (error) {
            this.logger.error('Errore lettura backup', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    async restoreBackup(backupFile) {
        try {
            // Verifica che il backup esista
            if (!fs.existsSync(backupFile)) {
                throw new Error('File di backup non trovato');
            }
            
            // Crea un backup del database corrente prima del ripristino
            const currentBackup = await this.createBackup();
            if (!currentBackup.success) {
                throw new Error('Impossibile creare backup del database corrente');
            }
            
            // Ferma il server Django se è in esecuzione
            // (Questo dovrebbe essere gestito dal processo principale)
            
            // Ripristina il database
            await fs.promises.copyFile(backupFile, this.dbPath);
            
            this.logger.info('Database ripristinato', { backupFile });
            
            return { success: true };
            
        } catch (error) {
            this.logger.error('Errore ripristino backup', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    async deleteBackup(backupFile) {
        try {
            if (!fs.existsSync(backupFile)) {
                throw new Error('File di backup non trovato');
            }
            
            await fs.promises.unlink(backupFile);
            
            this.logger.info('Backup eliminato', { backupFile });
            
            return { success: true };
            
        } catch (error) {
            this.logger.error('Errore eliminazione backup', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    async scheduleBackup(schedule) {
        try {
            // Ferma il task esistente se presente
            if (this.backupTask) {
                this.backupTask.stop();
            }
            
            // Crea un nuovo task cron
            this.backupTask = cron.schedule(schedule.cron, async () => {
                this.logger.info('Backup automatico avviato');
                const result = await this.createBackup();
                if (result.success) {
                    this.logger.info('Backup automatico completato', { file: result.file });
                } else {
                    this.logger.error('Backup automatico fallito', { error: result.error });
                }
            }, {
                scheduled: false
            });
            
            // Avvia il task
            this.backupTask.start();
            
            this.logger.info('Backup automatico programmato', { schedule: schedule.cron });
            
            return { success: true };
            
        } catch (error) {
            this.logger.error('Errore programmazione backup', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    stopScheduledBackup() {
        try {
            if (this.backupTask) {
                this.backupTask.stop();
                this.backupTask = null;
                this.logger.info('Backup automatico fermato');
            }
            
            return { success: true };
            
        } catch (error) {
            this.logger.error('Errore fermata backup automatico', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    // Metodo per pulire i backup vecchi
    async cleanOldBackups(retentionDays = 30) {
        try {
            const files = fs.readdirSync(this.backupDir);
            const cutoffDate = new Date();
            cutoffDate.setDate(cutoffDate.getDate() - retentionDays);
            
            let deletedCount = 0;
            
            for (const file of files) {
                if (file.startsWith('ddt-backup-') && file.endsWith('.sqlite3')) {
                    const filePath = path.join(this.backupDir, file);
                    const stats = fs.statSync(filePath);
                    
                    if (stats.birthtime < cutoffDate) {
                        await fs.promises.unlink(filePath);
                        deletedCount++;
                    }
                }
            }
            
            this.logger.info('Backup vecchi puliti', { deletedCount, retentionDays });
            
            return { success: true, deletedCount };
            
        } catch (error) {
            this.logger.error('Errore pulizia backup vecchi', { error: error.message });
            return { success: false, error: error.message };
        }
    }
    
    // Metodo per esportare i backup
    async exportBackups(exportPath) {
        try {
            const backups = this.listBackups();
            if (!backups.success) {
                throw new Error(backups.error);
            }
            
            const exportData = {
                timestamp: new Date().toISOString(),
                backupCount: backups.backups.length,
                backups: backups.backups.map(backup => ({
                    name: backup.name,
                    size: backup.size,
                    created: backup.created,
                    modified: backup.modified
                }))
            };
            
            await fs.promises.writeFile(exportPath, JSON.stringify(exportData, null, 2));
            
            this.logger.info('Backup esportati', { exportPath, count: backups.backups.length });
            
            return { success: true, count: backups.backups.length };
            
        } catch (error) {
            this.logger.error('Errore esportazione backup', { error: error.message });
            return { success: false, error: error.message };
        }
    }
}

module.exports = BackupManager;
