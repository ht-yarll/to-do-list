#!/usr/bin/env bash

set -Eeuo pipefail

readonly service="${DATABASE_SERVICE:-database}"
readonly backup_dir="${BACKUP_DIR:-backups}"
readonly postgres_user="${POSTGRES_USER:-todo}"
readonly postgres_db="${POSTGRES_DB:-todo}"
readonly timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
readonly backup_file="${backup_dir}/databank-${timestamp}.dump"
readonly temporary_file="${backup_file}.tmp"

cleanup() {
  rm -f -- "$temporary_file"
}

trap cleanup EXIT

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker is required to create a database backup." >&2
  exit 1
fi

mkdir -p -- "$backup_dir"

echo "Creating PostgreSQL backup from service '${service}'..."
if ! docker compose exec -T "$service" \
  pg_dump \
    --username="$postgres_user" \
    --dbname="$postgres_db" \
    --format=custom >"$temporary_file"; then
  echo "Error: database backup failed." >&2
  exit 1
fi

if [[ ! -s "$temporary_file" ]]; then
  echo "Error: database backup was empty." >&2
  exit 1
fi

mv -- "$temporary_file" "$backup_file"
echo "Database backup created: ${backup_file}"
