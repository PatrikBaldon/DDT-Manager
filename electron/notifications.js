const { Notification, nativeImage } = require('electron');
const path = require('path');

class NotificationManager {
    constructor() {
        this.isSupported = Notification.isSupported();
        this.icon = this.createIcon();
    }
    
    createIcon() {
        try {
            const iconPath = path.join(__dirname, '..', 'static', 'images', 'icons', 'icon-192x192.png');
            return nativeImage.createFromPath(iconPath);
        } catch (error) {
            console.warn('Impossibile caricare l\'icona per le notifiche:', error);
            return null;
        }
    }
    
    showUpdateAvailable(version) {
        if (!this.isSupported) {
            console.log('Notifiche non supportate su questo sistema');
            return;
        }
        
        const notification = new Notification({
            title: 'DDT Manager - Aggiornamento Disponibile',
            body: `È disponibile la versione ${version}. Clicca per scaricare.`,
            icon: this.icon,
            sound: 'default',
            urgency: 'normal'
        });
        
        notification.on('click', () => {
            // Emetti un evento per gestire il click
            process.emit('update-notification-clicked');
        });
        
        notification.show();
    }
    
    showUpdateDownloaded(version) {
        if (!this.isSupported) {
            console.log('Notifiche non supportate su questo sistema');
            return;
        }
        
        const notification = new Notification({
            title: 'DDT Manager - Aggiornamento Scaricato',
            body: `L'aggiornamento alla versione ${version} è pronto per l'installazione.`,
            icon: this.icon,
            sound: 'default',
            urgency: 'normal'
        });
        
        notification.on('click', () => {
            // Emetti un evento per gestire il click
            process.emit('update-downloaded-notification-clicked');
        });
        
        notification.show();
    }
    
    showUpdateError(error) {
        if (!this.isSupported) {
            console.log('Notifiche non supportate su questo sistema');
            return;
        }
        
        const notification = new Notification({
            title: 'DDT Manager - Errore Aggiornamento',
            body: `Errore durante l'aggiornamento: ${error.message}`,
            icon: this.icon,
            sound: 'default',
            urgency: 'critical'
        });
        
        notification.show();
    }
    
    showInstallationComplete() {
        if (!this.isSupported) {
            console.log('Notifiche non supportate su questo sistema');
            return;
        }
        
        const notification = new Notification({
            title: 'DDT Manager - Installazione Completata',
            body: 'L\'applicazione è stata installata con successo!',
            icon: this.icon,
            sound: 'default',
            urgency: 'normal'
        });
        
        notification.show();
    }
    
    showWelcome() {
        if (!this.isSupported) {
            console.log('Notifiche non supportate su questo sistema');
            return;
        }
        
        const notification = new Notification({
            title: 'DDT Manager - Benvenuto!',
            body: 'Grazie per aver installato DDT Manager. Inizia a gestire i tuoi documenti di trasporto!',
            icon: this.icon,
            sound: 'default',
            urgency: 'normal'
        });
        
        notification.show();
    }
}

module.exports = NotificationManager;
