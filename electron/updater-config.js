// Configurazione per l'updater
const { app } = require('electron');
const path = require('path');

// Configurazione per l'updater in base all'ambiente
const updaterConfig = {
  // URL del repository GitHub per gli aggiornamenti
  github: {
    owner: 'aziendaagricola',
    repo: 'ddt-manager'
  },
  
  // Configurazione per l'auto-updater
  autoUpdater: {
    // Abilita il controllo automatico degli aggiornamenti
    checkForUpdatesAndNotify: true,
    
    // Intervallo di controllo aggiornamenti (in millisecondi)
    // 24 ore = 24 * 60 * 60 * 1000
    checkInterval: 24 * 60 * 60 * 1000,
    
    // Configurazione per il download
    download: {
      // Abilita il download automatico
      autoDownload: false,
      
      // Abilita l'installazione automatica all'uscita
      autoInstallOnAppQuit: true
    },
    
    // Configurazione per le notifiche
    notifications: {
      // Mostra notifiche per aggiornamenti disponibili
      showUpdateAvailable: true,
      
      // Mostra notifiche per download completato
      showUpdateDownloaded: true,
      
      // Mostra notifiche per errori
      showError: true
    }
  },
  
  // Configurazione per il server di aggiornamenti
  server: {
    // URL del server di aggiornamenti (se diverso da GitHub)
    url: null,
    
    // Token per l'autenticazione (se necessario)
    token: null
  },
  
  // Configurazione per i log
  logging: {
    // Abilita i log dell'updater
    enabled: true,
    
    // Livello di log (debug, info, warn, error)
    level: 'info',
    
    // File di log
    file: path.join(app.getPath('userData'), 'updater.log')
  }
};

// Configurazione specifica per l'ambiente di produzione
if (process.env.NODE_ENV === 'production') {
  updaterConfig.autoUpdater.checkForUpdatesAndNotify = true;
  updaterConfig.autoUpdater.download.autoDownload = false;
  updaterConfig.autoUpdater.download.autoInstallOnAppQuit = true;
  updaterConfig.logging.level = 'info';
} else {
  // Configurazione per l'ambiente di sviluppo
  updaterConfig.autoUpdater.checkForUpdatesAndNotify = false;
  updaterConfig.autoUpdater.download.autoDownload = false;
  updaterConfig.autoUpdater.download.autoInstallOnAppQuit = false;
  updaterConfig.logging.level = 'debug';
}

module.exports = updaterConfig;
