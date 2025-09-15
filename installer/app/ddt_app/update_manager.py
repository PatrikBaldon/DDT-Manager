"""
Sistema di aggiornamenti per DDT Application
Gestisce controlli versione e aggiornamenti automatici
"""

import os
import json
import requests
import subprocess
import tempfile
import zipfile
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

class UpdateManager:
    """Gestore aggiornamenti per DDT Application"""
    
    def __init__(self):
        self.github_repo = "https://github.com/PatrikBaldon/DDT-Application"
        self.update_url = "https://api.github.com/repos/PatrikBaldon/DDT-Application/releases/latest"
        self.install_dir = getattr(settings, 'INSTALLATION_PATH', None)
        self.version_file = os.path.join(self.install_dir, 'version.txt') if self.install_dir else None
        
    def get_current_version(self):
        """Ottiene la versione attuale dell'applicazione"""
        if self.version_file and os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Errore lettura versione: {e}")
                return "1.0.0"
        return "1.0.0"
    
    def get_latest_version(self):
        """Ottiene la versione più recente da GitHub"""
        try:
            response = requests.get(self.update_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                'version': data.get('tag_name', ''),
                'download_url': data.get('assets', [{}])[0].get('browser_download_url', ''),
                'release_notes': data.get('body', ''),
                'published_at': data.get('published_at', ''),
                'prerelease': data.get('prerelease', False)
            }
        except Exception as e:
            logger.error(f"Errore controllo versione remota: {e}")
            return None
    
    def check_for_updates(self):
        """Controlla se ci sono aggiornamenti disponibili"""
        current_version = self.get_current_version()
        latest_info = self.get_latest_version()
        
        if not latest_info:
            return {
                'error': 'Impossibile controllare aggiornamenti',
                'current_version': current_version,
                'latest_version': None,
                'update_available': False
            }
        
        latest_version = latest_info['version']
        update_available = current_version != latest_version
        
        return {
            'current_version': current_version,
            'latest_version': latest_version,
            'update_available': update_available,
            'release_notes': latest_info['release_notes'],
            'published_at': latest_info['published_at'],
            'prerelease': latest_info['prerelease']
        }
    
    def download_update(self, download_url):
        """Scarica l'aggiornamento"""
        try:
            temp_dir = tempfile.mkdtemp(prefix='ddt_update_')
            zip_path = os.path.join(temp_dir, 'update.zip')
            
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            return zip_path, temp_dir
        except Exception as e:
            logger.error(f"Errore download aggiornamento: {e}")
            return None, None
    
    def extract_update(self, zip_path, temp_dir):
        """Estrae l'aggiornamento"""
        try:
            extract_dir = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            return extract_dir
        except Exception as e:
            logger.error(f"Errore estrazione aggiornamento: {e}")
            return None
    
    def backup_current_version(self):
        """Crea backup della versione attuale"""
        if not self.install_dir:
            return False
        
        try:
            backup_dir = os.path.join(self.install_dir, 'backup')
            if os.path.exists(backup_dir):
                import shutil
                shutil.rmtree(backup_dir)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup file critici
            data_dir = os.path.join(self.install_dir, 'app', 'data')
            if os.path.exists(data_dir):
                shutil.copytree(data_dir, os.path.join(backup_dir, 'data'))
            
            logs_dir = os.path.join(self.install_dir, 'logs')
            if os.path.exists(logs_dir):
                shutil.copytree(logs_dir, os.path.join(backup_dir, 'logs'))
            
            if self.version_file and os.path.exists(self.version_file):
                shutil.copy2(self.version_file, os.path.join(backup_dir, 'version.txt'))
            
            return True
        except Exception as e:
            logger.error(f"Errore backup: {e}")
            return False
    
    def apply_update(self, extract_dir):
        """Applica l'aggiornamento"""
        if not self.install_dir:
            return False
        
        try:
            # Ferma l'applicazione se in esecuzione
            try:
                subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                             capture_output=True, check=False)
                subprocess.run(['taskkill', '/f', '/im', 'start_ddt.bat'], 
                             capture_output=True, check=False)
            except:
                pass
            
            # Aggiorna file applicazione
            app_dir = os.path.join(extract_dir, 'app')
            if os.path.exists(app_dir):
                import shutil
                shutil.copytree(app_dir, os.path.join(self.install_dir, 'app'), 
                              dirs_exist_ok=True)
            
            scripts_dir = os.path.join(extract_dir, 'scripts')
            if os.path.exists(scripts_dir):
                shutil.copytree(scripts_dir, os.path.join(self.install_dir, 'scripts'), 
                              dirs_exist_ok=True)
            
            # Aggiorna Python se necessario
            python_dir = os.path.join(extract_dir, 'python')
            if os.path.exists(python_dir):
                shutil.copytree(python_dir, os.path.join(self.install_dir, 'python'), 
                              dirs_exist_ok=True)
            
            # Aggiorna dipendenze se necessario
            deps_dir = os.path.join(extract_dir, 'dependencies')
            if os.path.exists(deps_dir):
                site_packages = os.path.join(self.install_dir, 'python', 'Lib', 'site-packages')
                shutil.copytree(deps_dir, site_packages, dirs_exist_ok=True)
            
            return True
        except Exception as e:
            logger.error(f"Errore applicazione aggiornamento: {e}")
            return False
    
    def run_post_update_tasks(self):
        """Esegue le attività post-aggiornamento"""
        if not self.install_dir:
            return False
        
        try:
            python_path = os.path.join(self.install_dir, 'python', 'python.exe')
            app_path = os.path.join(self.install_dir, 'app')
            
            # Imposta variabili d'ambiente
            env = os.environ.copy()
            env['DJANGO_SETTINGS_MODULE'] = 'ddt_project.settings_offline'
            env['PYTHONPATH'] = app_path
            
            # Esegui migrazioni
            subprocess.run([python_path, 'manage.py', 'migrate'], 
                         cwd=app_path, env=env, check=False)
            
            # Raccoglie file statici
            subprocess.run([python_path, 'manage.py', 'collectstatic', '--noinput'], 
                         cwd=app_path, env=env, check=False)
            
            return True
        except Exception as e:
            logger.error(f"Errore attività post-aggiornamento: {e}")
            return False
    
    def update_version_file(self, version):
        """Aggiorna il file versione"""
        if self.version_file:
            try:
                with open(self.version_file, 'w', encoding='utf-8') as f:
                    f.write(version)
                return True
            except Exception as e:
                logger.error(f"Errore aggiornamento versione: {e}")
        return False
    
    def perform_update(self):
        """Esegue l'aggiornamento completo"""
        try:
            # Controlla aggiornamenti
            update_info = self.check_for_updates()
            if not update_info['update_available']:
                return {'success': False, 'message': 'Nessun aggiornamento disponibile'}
            
            # Scarica aggiornamento
            zip_path, temp_dir = self.download_update(update_info['download_url'])
            if not zip_path:
                return {'success': False, 'message': 'Errore download aggiornamento'}
            
            # Estrae aggiornamento
            extract_dir = self.extract_update(zip_path, temp_dir)
            if not extract_dir:
                return {'success': False, 'message': 'Errore estrazione aggiornamento'}
            
            # Crea backup
            if not self.backup_current_version():
                return {'success': False, 'message': 'Errore creazione backup'}
            
            # Applica aggiornamento
            if not self.apply_update(extract_dir):
                return {'success': False, 'message': 'Errore applicazione aggiornamento'}
            
            # Esegue attività post-aggiornamento
            if not self.run_post_update_tasks():
                return {'success': False, 'message': 'Errore attività post-aggiornamento'}
            
            # Aggiorna versione
            self.update_version_file(update_info['latest_version'])
            
            # Pulizia
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return {
                'success': True, 
                'message': 'Aggiornamento completato con successo',
                'old_version': update_info['current_version'],
                'new_version': update_info['latest_version']
            }
            
        except Exception as e:
            logger.error(f"Errore aggiornamento: {e}")
            return {'success': False, 'message': f'Errore aggiornamento: {str(e)}'}

# Viste per l'API di aggiornamento
@require_http_methods(["GET"])
def check_updates(request):
    """API per controllare aggiornamenti"""
    try:
        update_manager = UpdateManager()
        update_info = update_manager.check_for_updates()
        return JsonResponse(update_info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def perform_update(request):
    """API per eseguire aggiornamento"""
    try:
        update_manager = UpdateManager()
        result = update_manager.perform_update()
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_current_version(request):
    """API per ottenere versione attuale"""
    try:
        update_manager = UpdateManager()
        version = update_manager.get_current_version()
        return JsonResponse({'version': version})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)