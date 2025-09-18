#!/usr/bin/env node

/**
 * DDT Manager - Launcher per Electron
 * 
 * Questo file serve come punto di ingresso principale per l'applicazione Electron.
 * Gestisce l'inizializzazione e la configurazione dell'applicazione.
 */

const { app } = require('electron');
const path = require('path');
const AppManager = require('./app-manager');

// Configurazione dell'applicazione
app.setName('DDT Manager');
app.setVersion('1.1.0');

// Configurazione per la sicurezza
app.allowRendererProcessReuse = true;

// Configurazione per il debug
if (process.env.NODE_ENV === 'development') {
    app.commandLine.appendSwitch('--enable-logging');
    app.commandLine.appendSwitch('--log-level=0');
}

// Configurazione per la produzione
if (process.env.NODE_ENV === 'production') {
    app.commandLine.appendSwitch('--disable-dev-shm-usage');
    app.commandLine.appendSwitch('--no-sandbox');
}

// Gestione degli errori globali
process.on('uncaughtException', (error) => {
    console.error('Errore non gestito:', error);
    app.quit();
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Promessa rifiutata non gestita:', reason);
    app.quit();
});

// Inizializza l'applicazione
let appManager;

app.whenReady().then(() => {
    try {
        appManager = new AppManager();
        console.log('DDT Manager avviato con successo');
    } catch (error) {
        console.error('Errore durante l\'inizializzazione:', error);
        app.quit();
    }
});

// Gestione della chiusura dell'applicazione
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (appManager) {
        appManager.onActivate();
    }
});

app.on('before-quit', () => {
    if (appManager) {
        appManager.onBeforeQuit();
    }
});

app.on('will-quit', () => {
    if (appManager) {
        appManager.onWillQuit();
    }
});

// Gestione dei segnali di sistema
process.on('SIGINT', () => {
    console.log('Ricevuto SIGINT, chiusura applicazione...');
    app.quit();
});

process.on('SIGTERM', () => {
    console.log('Ricevuto SIGTERM, chiusura applicazione...');
    app.quit();
});

// Gestione degli errori di Electron
app.on('render-process-gone', (event, webContents, details) => {
    console.error('Processo di rendering terminato:', details);
    if (appManager) {
        appManager.handleError(new Error(details.reason), { type: 'render-process-gone' });
    }
});

app.on('child-process-gone', (event, details) => {
    console.error('Processo figlio terminato:', details);
    if (appManager) {
        appManager.handleError(new Error(details.reason), { type: 'child-process-gone' });
    }
});

// Esporta l'AppManager per uso esterno
module.exports = AppManager;
