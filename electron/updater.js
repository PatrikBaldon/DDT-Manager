const { autoUpdater } = require('electron-updater');
const { dialog, app } = require('electron');
const path = require('path');

class Updater {
    constructor(mainWindow) {
        this.mainWindow = mainWindow;
        this.isUpdateAvailable = false;
        this.isUpdateDownloaded = false;
        
        // Configura l'auto-updater
        autoUpdater.checkForUpdatesAndNotify();
        
        // Configura i listener per gli eventi di aggiornamento
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Controlla se ci sono aggiornamenti disponibili
        autoUpdater.on('checking-for-update', () => {
            console.log('Controllo aggiornamenti...');
        });
        
        // Aggiornamento disponibile
        autoUpdater.on('update-available', (info) => {
            console.log('Aggiornamento disponibile:', info);
            this.isUpdateAvailable = true;
            this.showUpdateAvailableDialog(info);
        });
        
        // Nessun aggiornamento disponibile
        autoUpdater.on('update-not-available', (info) => {
            console.log('Nessun aggiornamento disponibile:', info);
        });
        
        // Errore durante il controllo aggiornamenti
        autoUpdater.on('error', (err) => {
            console.error('Errore durante il controllo aggiornamenti:', err);
        });
        
        // Download dell'aggiornamento iniziato
        autoUpdater.on('download-progress', (progressObj) => {
            let log_message = "Velocità download: " + progressObj.bytesPerSecond;
            log_message = log_message + ' - Downloaded ' + progressObj.percent + '%';
            log_message = log_message + ' (' + progressObj.transferred + "/" + progressObj.total + ')';
            console.log(log_message);
            
            // Invia il progresso alla finestra principale
            if (this.mainWindow) {
                this.mainWindow.webContents.send('update-download-progress', progressObj);
            }
        });
        
        // Download dell'aggiornamento completato
        autoUpdater.on('update-downloaded', (info) => {
            console.log('Aggiornamento scaricato:', info);
            this.isUpdateDownloaded = true;
            this.showUpdateDownloadedDialog(info);
        });
    }
    
    showUpdateAvailableDialog(info) {
        const options = {
            type: 'info',
            title: 'Aggiornamento Disponibile',
            message: `È disponibile una nuova versione di DDT Manager (${info.version}).`,
            detail: 'Vuoi scaricare e installare l\'aggiornamento ora?',
            buttons: ['Scarica Ora', 'Più Tardi'],
            defaultId: 0,
            cancelId: 1
        };
        
        dialog.showMessageBox(this.mainWindow, options).then((result) => {
            if (result.response === 0) {
                // L'utente ha scelto di scaricare l'aggiornamento
                this.downloadUpdate();
            }
        });
    }
    
    showUpdateDownloadedDialog(info) {
        const options = {
            type: 'info',
            title: 'Aggiornamento Scaricato',
            message: 'L\'aggiornamento è stato scaricato con successo.',
            detail: 'L\'applicazione verrà riavviata per installare l\'aggiornamento.',
            buttons: ['Riavvia Ora', 'Più Tardi'],
            defaultId: 0,
            cancelId: 1
        };
        
        dialog.showMessageBox(this.mainWindow, options).then((result) => {
            if (result.response === 0) {
                // L'utente ha scelto di riavviare ora
                this.installUpdate();
            }
        });
    }
    
    downloadUpdate() {
        if (this.isUpdateAvailable) {
            console.log('Avvio download aggiornamento...');
            autoUpdater.downloadUpdate();
        }
    }
    
    installUpdate() {
        if (this.isUpdateDownloaded) {
            console.log('Installazione aggiornamento...');
            autoUpdater.quitAndInstall();
        }
    }
    
    // Metodo per controllare manualmente gli aggiornamenti
    checkForUpdates() {
        console.log('Controllo manuale aggiornamenti...');
        autoUpdater.checkForUpdates();
    }
    
    // Metodo per scaricare manualmente l'aggiornamento
    downloadUpdateManually() {
        if (this.isUpdateAvailable && !this.isUpdateDownloaded) {
            this.downloadUpdate();
        }
    }
    
    // Metodo per installare manualmente l'aggiornamento
    installUpdateManually() {
        if (this.isUpdateDownloaded) {
            this.installUpdate();
        }
    }
    
    // Metodo per ottenere lo stato dell'aggiornamento
    getUpdateStatus() {
        return {
            isUpdateAvailable: this.isUpdateAvailable,
            isUpdateDownloaded: this.isUpdateDownloaded
        };
    }
}

module.exports = Updater;
