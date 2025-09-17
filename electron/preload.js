const { contextBridge, ipcRenderer } = require('electron');

// Espone le API sicure al processo di rendering
contextBridge.exposeInMainWorld('electronAPI', {
  // Informazioni sull'applicazione
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // Store per le impostazioni
  getStoreValue: (key) => ipcRenderer.invoke('get-store-value', key),
  setStoreValue: (key, value) => ipcRenderer.setStoreValue('set-store-value', key, value),
  
  // Navigazione
  navigateTo: (path) => ipcRenderer.invoke('navigate-to', path),
  
  // Eventi
  onNavigateTo: (callback) => {
    ipcRenderer.on('navigate-to', callback);
  },
  
  // Rimuovi listener
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel);
  }
});

// Aggiungi funzionalità per la navigazione programmatica
window.addEventListener('DOMContentLoaded', () => {
  // Intercetta i link interni per la navigazione fluida
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href^="/"]');
    if (link) {
      event.preventDefault();
      const href = link.getAttribute('href');
      window.location.href = href;
    }
  });
  
  // Gestisci la navigazione tramite menu Electron
  window.electronAPI.onNavigateTo((event, path) => {
    window.location.href = path;
  });
});

// Aggiungi stili per l'integrazione con Electron
const style = document.createElement('style');
style.textContent = `
  /* Stili specifici per Electron */
  body {
    -webkit-app-region: no-drag;
    user-select: text;
  }
  
  /* Migliora l'aspetto per l'applicazione desktop */
  .navbar {
    -webkit-app-region: drag;
  }
  
  .navbar .nav-link,
  .navbar .dropdown-toggle,
  .navbar .btn {
    -webkit-app-region: no-drag;
  }
  
  /* Rimuovi effetti di hover non necessari su desktop */
  @media (hover: hover) {
    .btn:hover {
      transform: none;
    }
  }
  
  /* Migliora la leggibilità su schermi ad alta risoluzione */
  body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
`;
document.head.appendChild(style);
