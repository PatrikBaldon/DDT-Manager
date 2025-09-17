// Configurazione per l'ambiente di sviluppo
const path = require('path');

// Override della configurazione per lo sviluppo
const developmentConfig = {
  // Configurazione dell'applicazione
  app: {
    name: 'DDT Manager (Dev)',
    version: '1.0.0-dev',
    description: 'Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F - Modalità Sviluppo'
  },

  // Configurazione del server Django
  django: {
    host: '127.0.0.1',
    port: 8000,
    url: 'http://127.0.0.1:8000',
    pythonPath: process.platform === 'win32' ? 'python' : 'python3',
    managePyPath: path.join(__dirname, '..', 'manage.py')
  },

  // Configurazione della finestra
  window: {
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    show: false,
    titleBarStyle: 'default',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }
  },

  // Configurazione del menu
  menu: {
    showDevTools: true
  },

  // Configurazione degli aggiornamenti
  updater: {
    enabled: false,
    autoDownload: false,
    autoInstallOnAppQuit: false
  },

  // Configurazione del database
  database: {
    path: path.join(__dirname, '..', 'db.sqlite3'),
    backupDir: path.join(__dirname, '..', 'backup')
  },

  // Configurazione dei log
  logging: {
    level: 'debug',
    file: path.join(__dirname, '..', 'logs', 'electron-dev.log')
  },

  // Configurazione PDF
  pdf: {
    outputDir: path.join(__dirname, '..', 'static', 'pdf'),
    templateDir: path.join(__dirname, '..', 'templates', 'pdf')
  },

  // Configurazione delle icone
  icons: {
    app: path.join(__dirname, '..', 'static', 'images', 'icons', 'icon-512x512.png'),
    tray: path.join(__dirname, '..', 'static', 'images', 'icons', 'icon-192x192.png')
  },

  // Configurazione dell'ambiente
  environment: {
    isDevelopment: true,
    isProduction: false,
    platform: process.platform
  }
};

module.exports = developmentConfig;
