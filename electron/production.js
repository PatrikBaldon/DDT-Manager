// Configurazione per l'ambiente di produzione
const path = require('path');

// Override della configurazione per la produzione
const productionConfig = {
  // Configurazione dell'applicazione
  app: {
    name: 'DDT Manager',
    version: '1.0.0',
    description: 'Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F'
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
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
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
    showDevTools: false
  },

  // Configurazione degli aggiornamenti
  updater: {
    enabled: true,
    autoDownload: false,
    autoInstallOnAppQuit: true
  },

  // Configurazione del database
  database: {
    path: path.join(__dirname, '..', 'db.sqlite3'),
    backupDir: path.join(__dirname, '..', 'backup')
  },

  // Configurazione dei log
  logging: {
    level: 'info',
    file: path.join(__dirname, '..', 'logs', 'electron.log')
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
    isDevelopment: false,
    isProduction: true,
    platform: process.platform
  }
};

module.exports = productionConfig;
