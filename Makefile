.PHONY: backup db-backup restore db-restore emulate-ci-cd

backup db-backup:
	@./scripts/backup-databank.sh

restore db-restore:
	@./scripts/restore-databank.sh

emulate-ci-cd:
	@./scripts/emulate-ci-cd.sh

down-v:
	docker compose down --volumes

up-b:
	docker compose up --build