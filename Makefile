.PHONY: backup db-backup emulate-ci-cd

backup db-backup:
	@./scripts/backup-databank.sh

emulate-ci-cd:
	@./scripts/emulate-ci-cd.sh
