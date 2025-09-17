// Configurazione per l'ambiente di test
const path = require('path');

// Override della configurazione per i test
const testingConfig = {
  // Configurazione dell'applicazione
  app: {
    name: 'DDT Manager (Test)',
    version: '1.0.0-test',
    description: 'Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F - Modalità Test'
  },

  // Configurazione del server Django
  django: {
    host: '127.0.0.1',
    port: 8001, // Porta diversa per i test
    url: 'http://127.0.0.1:8001',
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
    path: path.join(__dirname, '..', 'test_db.sqlite3'),
    backupDir: path.join(__dirname, '..', 'test_backup')
  },

  // Configurazione dei log
  logging: {
    level: 'debug',
    file: path.join(__dirname, '..', 'logs', 'electron-test.log')
  },

  // Configurazione PDF
  pdf: {
    outputDir: path.join(__dirname, '..', 'static', 'test_pdf'),
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
    isProduction: false,
    isTesting: true,
    platform: process.platform
  }
};

module.exports = testingConfig;