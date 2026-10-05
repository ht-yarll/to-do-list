#!/usr/bin/env bash

set -Eeuo pipefail

readonly service="${DATABASE_SERVICE:-database}"
readonly backup_file="${BACKUP_FILE:-}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker is required to restore a database backup." >&2
  exit 1
fi

if [[ -z "$backup_file" ]]; then
  echo "Usage: BACKUP_FILE=backups/databank-<UTC timestamp>.dump make db-restore" >&2
  exit 1
fi

if [[ ! -f "$backup_file" ]]; then
  echo "Error: backup file does not exist: $backup_file" >&2
  exit 1
fi

echo "Restoring PostgreSQL backup to service '${service}'..."
if ! docker compose exec -T "$service" \
  sh -c 'pg_restore --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --clean --if-exists' \
  <"$backup_file"; then
  echo "Error: database restore failed." >&2
  exit 1
fi

echo "Database restore completed from: ${backup_file}"
