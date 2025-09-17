# ========================================
# DDT Electron App - Makefile per Sviluppo
# ========================================

.PHONY: help dev test sync update clean install electron electron-dev electron-build

# Colori per output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostra questo help
	@echo "$(BLUE)DDT Electron App - Comandi Disponibili$(NC)"
	@echo "============================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

dev: ## Avvia server di sviluppo
	@echo "$(YELLOW)Avvio server di sviluppo...$(NC)"
	@python manage.py runserver

test: ## Esegue tutti i test
	@echo "$(YELLOW)Esecuzione test...$(NC)"
	@python manage.py test

sync: ## Sincronizza con GitHub
	@echo "$(YELLOW)Sincronizzazione con GitHub...$(NC)"
	@./scripts/sync_to_github.sh

update: ## Aggiorna da GitHub
	@echo "$(YELLOW)Aggiornamento da GitHub...$(NC)"
	@./scripts/update_from_github.sh

clean: ## Pulisce file temporanei
	@echo "$(YELLOW)Pulizia file temporanei...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/

install: ## Setup completo del progetto
	@echo "$(YELLOW)Setup completo del progetto...$(NC)"
	@./scripts/dev_mac.sh

electron: ## Avvia applicazione Electron
	@echo "$(YELLOW)Avvio applicazione Electron...$(NC)"
	@npm run electron

electron-dev: ## Avvia applicazione Electron in modalità sviluppo
	@echo "$(YELLOW)Avvio applicazione Electron in modalità sviluppo...$(NC)"
	@npm run electron-dev

electron-build: ## Costruisce applicazione Electron
	@echo "$(YELLOW)Costruzione applicazione Electron...$(NC)"
	@npm run build

electron-install: ## Installa dipendenze Node.js
	@echo "$(YELLOW)Installazione dipendenze Node.js...$(NC)"
	@npm install

installer-build: ## Crea installer Windows
	@echo "$(YELLOW)Creazione installer Windows...$(NC)"
	@powershell -ExecutionPolicy Bypass -File installer/scripts/build-installer.ps1

installer-clean: ## Pulisce file di build installer
	@echo "$(YELLOW)Pulizia file installer...$(NC)"
	@powershell -ExecutionPolicy Bypass -File installer/scripts/build-installer.ps1 -Clean

installer-package: ## Crea package di distribuzione completo
	@echo "$(YELLOW)Creazione package di distribuzione...$(NC)"
	@powershell -ExecutionPolicy Bypass -File installer/scripts/build-installer.ps1 -Clean

download-install: ## Download e installazione automatica da GitHub
	@echo "$(YELLOW)Download e installazione automatica...$(NC)"
	@powershell -ExecutionPolicy Bypass -File installer/scripts/download-and-install.ps1

create-release: ## Crea release su GitHub (usa: make create-release VERSION=v1.0.0)
	@echo "$(YELLOW)Creazione release su GitHub...$(NC)"
	@./scripts/create-release.sh $(VERSION)

github-setup: ## Configura GitHub per distribuzione
	@echo "$(YELLOW)Configurazione GitHub per distribuzione...$(NC)"
	@echo "1. Vai su GitHub.com > Settings > Developer settings > Personal access tokens"
	@echo "2. Crea un token con permessi 'repo' e 'workflow'"
	@echo "3. Configura il token: gh auth login"
	@echo "4. Abilita GitHub Actions nel repository"
	@echo "5. Crea la prima release: make create-release VERSION=v1.0.0"

migrate: ## Esegue migrazioni database
	@echo "$(YELLOW)Esecuzione migrazioni...$(NC)"
	@python manage.py migrate

superuser: ## Crea superuser
	@echo "$(YELLOW)Creazione superuser...$(NC)"
	@python manage.py createsuperuser

collectstatic: ## Raccoglie file statici
	@echo "$(YELLOW)Raccolta file statici...$(NC)"
	@python manage.py collectstatic --noinput

shell: ## Apre shell Django
	@echo "$(YELLOW)Apertura shell Django...$(NC)"
	@python manage.py shell

dbshell: ## Apre shell database
	@echo "$(YELLOW)Apertura shell database...$(NC)"
	@python manage.py dbshell

runserver: ## Avvia server (alias per dev)
	@make dev

# Comandi per Windows (da eseguire su Windows)
windows-install: ## Installa su Windows (da eseguire su Windows)
	@echo "$(YELLOW)Per installare su Windows, esegui:$(NC)"
	@echo "DDT_PWA_Installer.bat"

windows-update: ## Aggiorna su Windows (da eseguire su Windows)
	@echo "$(YELLOW)Per aggiornare su Windows, esegui:$(NC)"
	@echo "DDT_PWA_Update.bat"

# Comandi di sviluppo avanzati
dev-full: clean install test ## Setup completo con test
	@echo "$(GREEN)Setup completo completato!$(NC)"

dev-quick: ## Setup rapido senza test
	@echo "$(YELLOW)Setup rapido...$(NC)"
	@pip install -r requirements.txt
	@python manage.py migrate
	@python manage.py runserver

# Comandi di produzione
prod-build: clean collectstatic electron-build ## Build per produzione
	@echo "$(GREEN)Build produzione completata!$(NC)"

prod-deploy: prod-build sync ## Deploy su GitHub
	@echo "$(GREEN)Deploy completato!$(NC)"

# Comandi di manutenzione
backup: ## Crea backup del database
	@echo "$(YELLOW)Creazione backup database...$(NC)"
	@mkdir -p backup
	@cp db.sqlite3 backup/db_backup_$(shell date +%Y%m%d_%H%M%S).sqlite3
	@echo "$(GREEN)Backup creato!$(NC)"

restore: ## Ripristina da backup (specificare BACKUP=filename)
	@echo "$(YELLOW)Ripristino da backup...$(NC)"
	@if [ -z "$(BACKUP)" ]; then echo "$(RED)Specifica BACKUP=filename$(NC)"; exit 1; fi
	@cp backup/$(BACKUP) db.sqlite3
	@echo "$(GREEN)Backup ripristinato!$(NC)"

# Comandi di debug
debug: ## Avvia server in modalità debug
	@echo "$(YELLOW)Avvio server in modalità debug...$(NC)"
	@python manage.py runserver --settings=config.settings.development

logs: ## Mostra log dell'applicazione
	@echo "$(YELLOW)Log dell'applicazione:$(NC)"
	@tail -f logs/ddt.log 2>/dev/null || echo "$(RED)File di log non trovato$(NC)"

# Comandi di utilità
status: ## Mostra stato del repository
	@echo "$(YELLOW)Stato repository:$(NC)"
	@git status

diff: ## Mostra differenze non committate
	@echo "$(YELLOW)Differenze non committate:$(NC)"
	@git diff

# Comandi di help esteso
help-dev: ## Mostra comandi di sviluppo
	@echo "$(BLUE)Comandi di Sviluppo:$(NC)"
	@echo "  make dev          - Avvia server di sviluppo"
	@echo "  make test         - Esegue tutti i test"
	@echo "  make sync         - Sincronizza con GitHub"
	@echo "  make update       - Aggiorna da GitHub"
	@echo "  make clean        - Pulisce file temporanei"
	@echo "  make install      - Setup completo del progetto"

help-electron: ## Mostra comandi Electron
	@echo "$(BLUE)Comandi Electron:$(NC)"
	@echo "  make electron         - Avvia applicazione Electron"
	@echo "  make electron-dev     - Avvia in modalità sviluppo"
	@echo "  make electron-build   - Costruisce applicazione"
	@echo "  make electron-install - Installa dipendenze Node.js"

help-prod: ## Mostra comandi di produzione
	@echo "$(BLUE)Comandi di Produzione:$(NC)"
	@echo "  make prod-build   - Build per produzione"
	@echo "  make prod-deploy  - Deploy su GitHub"
	@echo "  make backup       - Crea backup database"
	@echo "  make restore      - Ripristina da backup"