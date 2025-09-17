const { app, BrowserWindow, Menu, shell, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const Store = require('electron-store');
const config = require('./config');

// Inizializza il store per le impostazioni
const store = new Store();

// Variabile per il processo Django
let djangoProcess = null;

// Configurazione della finestra principale
let mainWindow;

function createWindow() {
  // Crea la finestra del browser
  mainWindow = new BrowserWindow({
    ...config.window,
    icon: config.icons.app
  });

  // Carica l'applicazione Django
  const djangoUrl = config.django.url;
  
  mainWindow.loadURL(djangoUrl).then(() => {
    mainWindow.show();
    
    // Apri gli strumenti di sviluppo in modalità sviluppo
    if (config.menu.showDevTools) {
      mainWindow.webContents.openDevTools();
    }
  }).catch((error) => {
    console.error('Errore nel caricamento dell\'applicazione:', error);
    dialog.showErrorBox('Errore', 'Impossibile connettersi al server Django. Assicurati che il server sia in esecuzione.');
  });

  // Gestisci la chiusura della finestra
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Gestisci i link esterni
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Mostra la finestra quando è pronta
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });
}

// Avvia il server Django
function startDjangoServer() {
  return new Promise((resolve, reject) => {
    djangoProcess = spawn(config.django.pythonPath, [config.django.managePyPath, 'runserver', '--noreload'], {
      cwd: path.join(__dirname, '..'),
      stdio: 'pipe'
    });

    djangoProcess.stdout.on('data', (data) => {
      const output = data.toString();
      console.log('Django:', output);
      
      // Controlla se il server è pronto
      if (output.includes('Starting development server') || output.includes('Quit the server with')) {
        resolve();
      }
    });

    djangoProcess.stderr.on('data', (data) => {
      console.error('Django Error:', data.toString());
    });

    djangoProcess.on('error', (error) => {
      console.error('Errore nell\'avvio di Django:', error);
      reject(error);
    });

    // Timeout per l'avvio
    setTimeout(() => {
      resolve(); // Procedi anche se non abbiamo conferma esplicita
    }, 5000);
  });
}

// Ferma il server Django
function stopDjangoServer() {
  if (djangoProcess) {
    djangoProcess.kill();
    djangoProcess = null;
  }
}

// Crea il menu dell'applicazione
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Nuovo DDT',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('navigate-to', '/ddt/create/');
          }
        },
        { type: 'separator' },
        {
          label: 'Esci',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Gestione',
      submenu: [
        {
          label: 'Mittenti',
          click: () => {
            mainWindow.webContents.send('navigate-to', '/mittenti/');
          }
        },
        {
          label: 'Destinatari',
          click: () => {
            mainWindow.webContents.send('navigate-to', '/destinatari/');
          }
        },
        {
          label: 'Vettori',
          click: () => {
            mainWindow.webContents.send('navigate-to', '/vettori/');
          }
        },
        {
          label: 'Causali di Trasporto',
          click: () => {
            mainWindow.webContents.send('navigate-to', '/causali/');
          }
        }
      ]
    },
    {
      label: 'Visualizza',
      submenu: [
        {
          label: 'Ricarica',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            mainWindow.reload();
          }
        },
        {
          label: 'Strumenti di Sviluppo',
          accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Ctrl+Shift+I',
          click: () => {
            mainWindow.webContents.toggleDevTools();
          }
        },
        { type: 'separator' },
        {
          label: 'Zoom In',
          accelerator: 'CmdOrCtrl+Plus',
          click: () => {
            const currentZoom = mainWindow.webContents.getZoomFactor();
            mainWindow.webContents.setZoomFactor(currentZoom + 0.1);
          }
        },
        {
          label: 'Zoom Out',
          accelerator: 'CmdOrCtrl+-',
          click: () => {
            const currentZoom = mainWindow.webContents.getZoomFactor();
            mainWindow.webContents.setZoomFactor(Math.max(0.5, currentZoom - 0.1));
          }
        },
        {
          label: 'Zoom Reset',
          accelerator: 'CmdOrCtrl+0',
          click: () => {
            mainWindow.webContents.setZoomFactor(1);
          }
        }
      ]
    },
    {
      label: 'Aiuto',
      submenu: [
        {
          label: 'Informazioni',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'DDT Manager',
              message: 'DDT Manager v1.0.0',
              detail: 'Sistema di gestione Documenti di Trasporto per Azienda Agricola BB&F'
            });
          }
        }
      ]
    }
  ];

  // Menu specifico per macOS
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { label: 'Informazioni su ' + app.getName(), role: 'about' },
        { type: 'separator' },
        { label: 'Servizi', role: 'services' },
        { type: 'separator' },
        { label: 'Nascondi ' + app.getName(), accelerator: 'Command+H', role: 'hide' },
        { label: 'Nascondi Altri', accelerator: 'Command+Shift+H', role: 'hideothers' },
        { label: 'Mostra Tutti', role: 'unhide' },
        { type: 'separator' },
        { label: 'Esci', accelerator: 'Command+Q', click: () => app.quit() }
      ]
    });
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Eventi dell'applicazione
app.whenReady().then(async () => {
  try {
    // Avvia il server Django
    await startDjangoServer();
    
    // Crea la finestra principale
    createWindow();
    
    // Crea il menu
    createMenu();
    
    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
      }
    });
  } catch (error) {
    console.error('Errore nell\'inizializzazione:', error);
    dialog.showErrorBox('Errore', 'Impossibile avviare l\'applicazione. Controlla che Python e Django siano installati correttamente.');
    app.quit();
  }
});

app.on('window-all-closed', () => {
  // Ferma il server Django prima di chiudere
  stopDjangoServer();
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Ferma il server Django prima di chiudere
  stopDjangoServer();
});

// Gestisci i messaggi IPC
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-store-value', (event, key) => {
  return store.get(key);
});

ipcMain.handle('set-store-value', (event, key, value) => {
  store.set(key, value);
});

ipcMain.handle('navigate-to', (event, path) => {
  if (mainWindow) {
    mainWindow.loadURL(`http://localhost:8000${path}`);
  }
});

// Gestisci gli aggiornamenti automatici
if (process.env.NODE_ENV === 'production') {
  const { autoUpdater } = require('electron-updater');
  
  autoUpdater.checkForUpdatesAndNotify();
  
  autoUpdater.on('update-available', () => {
    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'Aggiornamento Disponibile',
      message: 'È disponibile un nuovo aggiornamento. L\'applicazione verrà riavviata per installarlo.',
      buttons: ['OK']
    });
  });
}
