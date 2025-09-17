// Test per verificare la configurazione Electron
const config = require('./config');
const path = require('path');

console.log('🧪 Test Configurazione Electron');
console.log('================================');

// Test configurazione base
console.log('✅ Nome applicazione:', config.app.name);
console.log('✅ Versione:', config.app.version);
console.log('✅ Piattaforma:', config.environment.platform);

// Test configurazione Django
console.log('✅ URL Django:', config.django.url);
console.log('✅ Path Python:', config.django.pythonPath);
console.log('✅ Path manage.py:', config.django.managePyPath);

// Test configurazione finestra
console.log('✅ Dimensioni finestra:', `${config.window.width}x${config.window.height}`);
console.log('✅ Dimensioni minime:', `${config.window.minWidth}x${config.window.minHeight}`);

// Test configurazione icone
console.log('✅ Icona app:', config.icons.app);
console.log('✅ Icona tray:', config.icons.tray);

// Test configurazione database
console.log('✅ Path database:', config.database.path);
console.log('✅ Directory backup:', config.database.backupDir);

// Test configurazione PDF
console.log('✅ Directory PDF output:', config.pdf.outputDir);
console.log('✅ Directory PDF template:', config.pdf.templateDir);

// Test configurazione logging
console.log('✅ Livello log:', config.logging.level);
console.log('✅ File log:', config.logging.file);

// Test ambiente
console.log('✅ Modalità sviluppo:', config.environment.isDevelopment);
console.log('✅ Modalità produzione:', config.environment.isProduction);

// Verifica esistenza file
const fs = require('fs');

function checkFile(filePath, description) {
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${description}: TROVATO`);
  } else {
    console.log(`❌ ${description}: NON TROVATO (${filePath})`);
  }
}

console.log('\n🔍 Verifica File:');
checkFile(config.django.managePyPath, 'manage.py');
checkFile(config.icons.app, 'Icona applicazione');
checkFile(config.database.path, 'Database SQLite');
checkFile(config.pdf.outputDir, 'Directory PDF output');
checkFile(config.pdf.templateDir, 'Directory PDF template');

// Verifica directory
function checkDirectory(dirPath, description) {
  if (fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory()) {
    console.log(`✅ ${description}: TROVATA`);
  } else {
    console.log(`❌ ${description}: NON TROVATA (${dirPath})`);
  }
}

console.log('\n🔍 Verifica Directory:');
checkDirectory(path.dirname(config.database.path), 'Directory database');
checkDirectory(path.dirname(config.logging.file), 'Directory log');
checkDirectory(config.database.backupDir, 'Directory backup');

console.log('\n🎉 Test completato!');
console.log('Se tutti i test sono passati, l\'applicazione dovrebbe funzionare correttamente.');
