#!/usr/bin/env node

/**
 * DDT Manager - Installer per Electron
 * 
 * Questo script gestisce l'installazione e la configurazione iniziale
 * dell'applicazione DDT Manager.
 */

const { app } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

class Installer {
    constructor() {
        this.appPath = app.getAppPath();
        this.userDataPath = app.getPath('userData');
        this.installDir = path.dirname(this.appPath);
        this.isInstalled = false;
    }
    
    async install() {
        try {
            console.log('🔧 Installazione DDT Manager...');
            
            // Verifica prerequisiti
            await this.checkPrerequisites();
            
            // Installa dipendenze Python
            await this.installPythonDependencies();
            
            // Installa dipendenze Node.js
            await this.installNodeDependencies();
            
            // Configura database
            await this.setupDatabase();
            
            // Crea directory necessarie
            await this.createDirectories();
            
            // Configura impostazioni iniziali
            await this.setupInitialSettings();
            
            // Crea shortcut
            await this.createShortcuts();
            
            this.isInstalled = true;
            console.log('✅ Installazione completata con successo!');
            
        } catch (error) {
            console.error('❌ Errore durante l\'installazione:', error);
            throw error;
        }
    }
    
    async checkPrerequisites() {
        console.log('🔍 Verifica prerequisiti...');
        
        // Verifica Python
        const pythonCheck = await this.checkPython();
        if (!pythonCheck.success) {
            throw new Error(`Python non trovato: ${pythonCheck.error}`);
        }
        
        // Verifica Node.js
        const nodeCheck = await this.checkNode();
        if (!nodeCheck.success) {
            throw new Error(`Node.js non trovato: ${nodeCheck.error}`);
        }
        
        console.log('✅ Prerequisiti verificati');
    }
    
    async checkPython() {
        return new Promise((resolve) => {
            const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
            const python = spawn(pythonCmd, ['--version'], { stdio: 'pipe' });
            
            python.on('close', (code) => {
                if (code === 0) {
                    resolve({ success: true });
                } else {
                    resolve({ success: false, error: 'Python non installato' });
                }
            });
            
            python.on('error', (error) => {
                resolve({ success: false, error: error.message });
            });
        });
    }
    
    async checkNode() {
        return new Promise((resolve) => {
            const node = spawn('node', ['--version'], { stdio: 'pipe' });
            
            node.on('close', (code) => {
                if (code === 0) {
                    resolve({ success: true });
                } else {
                    resolve({ success: false, error: 'Node.js non installato' });
                }
            });
            
            node.on('error', (error) => {
                resolve({ success: false, error: error.message });
            });
        });
    }
    
    async installPythonDependencies() {
        console.log('📦 Installazione dipendenze Python...');
        
        return new Promise((resolve, reject) => {
            const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
            const pip = spawn(pythonCmd, ['-m', 'pip', 'install', '-r', 'requirements.txt'], {
                cwd: this.installDir,
                stdio: 'inherit'
            });
            
            pip.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Dipendenze Python installate');
                    resolve();
                } else {
                    reject(new Error('Errore installazione dipendenze Python'));
                }
            });
            
            pip.on('error', (error) => {
                reject(error);
            });
        });
    }
    
    async installNodeDependencies() {
        console.log('📦 Installazione dipendenze Node.js...');
        
        return new Promise((resolve, reject) => {
            const npm = spawn('npm', ['install'], {
                cwd: this.installDir,
                stdio: 'inherit'
            });
            
            npm.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Dipendenze Node.js installate');
                    resolve();
                } else {
                    reject(new Error('Errore installazione dipendenze Node.js'));
                }
            });
            
            npm.on('error', (error) => {
                reject(error);
            });
        });
    }
    
    async setupDatabase() {
        console.log('🗄️ Configurazione database...');
        
        return new Promise((resolve, reject) => {
            const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
            const migrate = spawn(pythonCmd, ['manage.py', 'migrate'], {
                cwd: this.installDir,
                stdio: 'inherit'
            });
            
            migrate.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Database configurato');
                    resolve();
                } else {
                    reject(new Error('Errore configurazione database'));
                }
            });
            
            migrate.on('error', (error) => {
                reject(error);
            });
        });
    }
    
    async createDirectories() {
        console.log('📁 Creazione directory...');
        
        const directories = [
            path.join(this.userDataPath, 'logs'),
            path.join(this.userDataPath, 'backups'),
            path.join(this.userDataPath, 'temp'),
            path.join(this.installDir, 'static', 'pdf'),
            path.join(this.installDir, 'templates', 'pdf')
        ];
        
        for (const dir of directories) {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`✅ Creata directory: ${dir}`);
            }
        }
    }
    
    async setupInitialSettings() {
        console.log('⚙️ Configurazione impostazioni iniziali...');
        
        const settingsFile = path.join(this.userDataPath, 'settings.json');
        const defaultSettings = {
            general: {
                language: 'it',
                theme: 'light',
                autoStart: false,
                minimizeToTray: true,
                checkUpdates: true
            },
            application: {
                windowWidth: 1200,
                windowHeight: 800,
                windowX: null,
                windowY: null,
                maximized: false
            },
            database: {
                backupEnabled: true,
                backupInterval: 24,
                backupRetention: 30,
                backupPath: path.join(this.userDataPath, 'backups')
            },
            pdf: {
                defaultFormat: 'A4',
                defaultOrientation: 'portrait',
                includeLogo: true,
                logoPath: null,
                fontSize: 12,
                margin: 20
            }
        };
        
        if (!fs.existsSync(settingsFile)) {
            fs.writeFileSync(settingsFile, JSON.stringify(defaultSettings, null, 2));
            console.log('✅ Impostazioni iniziali create');
        }
    }
    
    async createShortcuts() {
        console.log('🔗 Creazione shortcut...');
        
        try {
            if (process.platform === 'win32') {
                await this.createWindowsShortcuts();
            } else if (process.platform === 'darwin') {
                await this.createMacShortcuts();
            } else {
                await this.createLinuxShortcuts();
            }
            
            console.log('✅ Shortcut creati');
        } catch (error) {
            console.warn('⚠️ Errore creazione shortcut:', error.message);
        }
    }
    
    async createWindowsShortcuts() {
        const desktopPath = path.join(require('os').homedir(), 'Desktop');
        const shortcutPath = path.join(desktopPath, 'DDT Manager.lnk');
        
        // Crea un file batch per avviare l'applicazione
        const batchPath = path.join(this.installDir, 'start_ddt.bat');
        const batchContent = `@echo off
echo Avvio DDT Manager...
cd /d "${this.installDir}"
npm run electron
pause`;
        
        fs.writeFileSync(batchPath, batchContent);
        console.log(`✅ Batch creato: ${batchPath}`);
    }
    
    async createMacShortcuts() {
        const applicationsPath = '/Applications';
        const appPath = path.join(applicationsPath, 'DDT Manager.app');
        
        // Crea un bundle app per macOS
        const bundlePath = path.join(appPath, 'Contents');
        const macosPath = path.join(bundlePath, 'MacOS');
        const resourcesPath = path.join(bundlePath, 'Resources');
        
        fs.mkdirSync(macosPath, { recursive: true });
        fs.mkdirSync(resourcesPath, { recursive: true });
        
        // Crea Info.plist
        const infoPlist = {
            CFBundleName: 'DDT Manager',
            CFBundleIdentifier: 'com.aziendaagricola.ddt',
            CFBundleVersion: '1.1.0',
            CFBundleExecutable: 'DDT Manager',
            CFBundleIconFile: 'icon.icns'
        };
        
        fs.writeFileSync(
            path.join(bundlePath, 'Info.plist'),
            this.createPlist(infoPlist)
        );
        
        // Crea script di avvio
        const launcherScript = `#!/bin/bash
cd "${this.installDir}"
npm run electron`;
        
        fs.writeFileSync(path.join(macosPath, 'DDT Manager'), launcherScript);
        fs.chmodSync(path.join(macosPath, 'DDT Manager'), '755');
        
        console.log(`✅ App bundle creato: ${appPath}`);
    }
    
    async createLinuxShortcuts() {
        const desktopPath = path.join(require('os').homedir(), 'Desktop');
        const shortcutPath = path.join(desktopPath, 'DDT Manager.desktop');
        
        const desktopFile = `[Desktop Entry]
Version=1.0
Type=Application
Name=DDT Manager
Comment=Sistema di gestione Documenti di Trasporto
Exec=${path.join(this.installDir, 'start_ddt.sh')}
Icon=${path.join(this.installDir, 'static', 'images', 'icons', 'icon-512x512.png')}
Terminal=false
Categories=Office;Business;
StartupWMClass=DDT Manager`;
        
        fs.writeFileSync(shortcutPath, desktopFile);
        fs.chmodSync(shortcutPath, '755');
        
        console.log(`✅ Desktop file creato: ${shortcutPath}`);
    }
    
    createPlist(obj) {
        let plist = '<?xml version="1.0" encoding="UTF-8"?>\n';
        plist += '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n';
        plist += '<plist version="1.0">\n<dict>\n';
        
        for (const [key, value] of Object.entries(obj)) {
            plist += `  <key>${key}</key>\n`;
            if (typeof value === 'string') {
                plist += `  <string>${value}</string>\n`;
            } else if (typeof value === 'number') {
                plist += `  <integer>${value}</integer>\n`;
            } else if (typeof value === 'boolean') {
                plist += `  <${value ? 'true' : 'false'}/>\n`;
            }
        }
        
        plist += '</dict>\n</plist>';
        return plist;
    }
    
    async uninstall() {
        try {
            console.log('🗑️ Disinstallazione DDT Manager...');
            
            // Rimuovi shortcut
            await this.removeShortcuts();
            
            // Rimuovi directory utente (opzionale)
            const removeUserData = process.argv.includes('--remove-user-data');
            if (removeUserData) {
                await this.removeUserData();
            }
            
            console.log('✅ Disinstallazione completata');
            
        } catch (error) {
            console.error('❌ Errore durante la disinstallazione:', error);
            throw error;
        }
    }
    
    async removeShortcuts() {
        try {
            if (process.platform === 'win32') {
                const desktopPath = path.join(require('os').homedir(), 'Desktop');
                const shortcutPath = path.join(desktopPath, 'DDT Manager.lnk');
                if (fs.existsSync(shortcutPath)) {
                    fs.unlinkSync(shortcutPath);
                }
            } else if (process.platform === 'darwin') {
                const appPath = '/Applications/DDT Manager.app';
                if (fs.existsSync(appPath)) {
                    fs.rmSync(appPath, { recursive: true, force: true });
                }
            } else {
                const desktopPath = path.join(require('os').homedir(), 'Desktop');
                const shortcutPath = path.join(desktopPath, 'DDT Manager.desktop');
                if (fs.existsSync(shortcutPath)) {
                    fs.unlinkSync(shortcutPath);
                }
            }
        } catch (error) {
            console.warn('⚠️ Errore rimozione shortcut:', error.message);
        }
    }
    
    async removeUserData() {
        try {
            if (fs.existsSync(this.userDataPath)) {
                fs.rmSync(this.userDataPath, { recursive: true, force: true });
                console.log('✅ Dati utente rimossi');
            }
        } catch (error) {
            console.warn('⚠️ Errore rimozione dati utente:', error.message);
        }
    }
}

// Esegui l'installazione se questo script viene eseguito direttamente
if (require.main === module) {
    const installer = new Installer();
    
    if (process.argv.includes('--uninstall')) {
        installer.uninstall();
    } else {
        installer.install();
    }
}

module.exports = Installer;
