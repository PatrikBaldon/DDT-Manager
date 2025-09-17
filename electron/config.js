// Configurazione per l'applicazione Electron
const path = require('path');

// Carica la configurazione appropriata in base all'ambiente
let config;
if (process.env.NODE_ENV === 'production') {
  config = require('./production');
} else if (process.env.NODE_ENV === 'development') {
  config = require('./development');
} else if (process.env.NODE_ENV === 'testing') {
  config = require('./testing');
} else {
  // Configurazione di default
  config = {
  // Configurazione dell'applicazione
  app: {
    name: 'DDT Manager',
    version: '1.0.0',
    description: 'Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F'
  },

  // Configurazione del server Django
  django: {
    host: process.env.DJANGO_HOST || '127.0.0.1',
    port: process.env.DJANGO_PORT || 8000,
    url: `http://${process.env.DJANGO_HOST || '127.0.0.1'}:${process.env.DJANGO_PORT || 8000}`,
    pythonPath: process.platform === 'win32' ? 'python' : 'python3',
    managePyPath: path.join(__dirname, '..', 'manage.py')
  },

  // Configurazione della finestra
  window: {
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    show: false, // Non mostrare finché non è pronto
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
    showDevTools: process.env.NODE_ENV === 'development'
  },

  // Configurazione degli aggiornamenti
  updater: {
    enabled: process.env.NODE_ENV === 'production',
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
    level: process.env.LOG_LEVEL || 'info',
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
      isDevelopment: process.env.NODE_ENV === 'development',
      isProduction: process.env.NODE_ENV === 'production',
      platform: process.platform
    }
  };
}

module.exports = config;
