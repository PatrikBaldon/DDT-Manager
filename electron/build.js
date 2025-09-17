// Script per il build dell'applicazione Electron
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🔨 Build DDT Manager - Applicazione Electron');
console.log('=============================================');

// Funzione per eseguire comandi
function runCommand(command, description) {
  console.log(`\n📦 ${description}...`);
  try {
    execSync(command, { stdio: 'inherit', cwd: path.join(__dirname, '..') });
    console.log(`✅ ${description} completato`);
  } catch (error) {
    console.error(`❌ Errore durante ${description}:`, error.message);
    process.exit(1);
  }
}

// Funzione per verificare prerequisiti
function checkPrerequisites() {
  console.log('🔍 Verifica prerequisiti...');
  
  // Verifica Node.js
  try {
    const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
    console.log(`✅ Node.js: ${nodeVersion}`);
  } catch (error) {
    console.error('❌ Node.js non trovato');
    process.exit(1);
  }
  
  // Verifica npm
  try {
    const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
    console.log(`✅ npm: ${npmVersion}`);
  } catch (error) {
    console.error('❌ npm non trovato');
    process.exit(1);
  }
  
  // Verifica Python
  try {
    const pythonVersion = execSync('python3 --version', { encoding: 'utf8' }).trim();
    console.log(`✅ Python: ${pythonVersion}`);
  } catch (error) {
    console.error('❌ Python3 non trovato');
    process.exit(1);
  }
  
  // Verifica Django
  try {
    execSync('python3 -c "import django"', { stdio: 'pipe' });
    console.log('✅ Django: Installato');
  } catch (error) {
    console.error('❌ Django non trovato. Esegui: pip install -r requirements.txt');
    process.exit(1);
  }
}

// Funzione per pulire directory di build
function cleanBuild() {
  console.log('\n🧹 Pulizia directory di build...');
  const dirsToClean = ['dist', 'build', 'out'];
  
  dirsToClean.forEach(dir => {
    const dirPath = path.join(__dirname, '..', dir);
    if (fs.existsSync(dirPath)) {
      fs.rmSync(dirPath, { recursive: true, force: true });
      console.log(`✅ Rimosso: ${dir}`);
    }
  });
}

// Funzione per installare dipendenze
function installDependencies() {
  console.log('\n📦 Installazione dipendenze...');
  
  // Installa dipendenze Python
  runCommand('pip install -r requirements.txt', 'Installazione dipendenze Python');
  
  // Installa dipendenze Node.js
  runCommand('npm install', 'Installazione dipendenze Node.js');
}

// Funzione per preparare l'ambiente
function prepareEnvironment() {
  console.log('\n🔧 Preparazione ambiente...');
  
  // Crea directory necessarie
  const dirsToCreate = [
    'logs',
    'backup',
    'static/pdf',
    'templates/pdf'
  ];
  
  dirsToCreate.forEach(dir => {
    const dirPath = path.join(__dirname, '..', dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
      console.log(`✅ Creata directory: ${dir}`);
    }
  });
  
  // Esegui migrazioni Django
  runCommand('python3 manage.py migrate', 'Esecuzione migrazioni Django');
  
  // Raccogli file statici
  runCommand('python3 manage.py collectstatic --noinput', 'Raccolta file statici');
}

// Funzione per eseguire test
function runTests() {
  console.log('\n🧪 Esecuzione test...');
  runCommand('python3 manage.py test', 'Test Django');
}

// Funzione per costruire l'applicazione
function buildApplication() {
  console.log('\n🔨 Costruzione applicazione...');
  
  // Determina la piattaforma
  const platform = process.platform;
  let buildCommand = 'npm run build';
  
  if (platform === 'win32') {
    buildCommand = 'npm run build-win';
  } else if (platform === 'darwin') {
    buildCommand = 'npm run build-mac';
  } else {
    buildCommand = 'npm run build-linux';
  }
  
  runCommand(buildCommand, `Build per ${platform}`);
}

// Funzione principale
async function main() {
  try {
    checkPrerequisites();
    cleanBuild();
    installDependencies();
    prepareEnvironment();
    
    // Chiedi se eseguire i test
    const args = process.argv.slice(2);
    if (!args.includes('--skip-tests')) {
      runTests();
    }
    
    buildApplication();
    
    console.log('\n🎉 Build completato con successo!');
    console.log('📁 I file di distribuzione sono in: dist/');
    
  } catch (error) {
    console.error('\n❌ Errore durante il build:', error.message);
    process.exit(1);
  }
}

// Esegui il build
main();
