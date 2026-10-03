#!/usr/bin/env bash

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_ID="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUTPUT_DIR="$ROOT_DIR/artifacts/ci-cd"
RUN_DIR="$OUTPUT_DIR/$RUN_ID"
EVENTS_FILE="$RUN_DIR/events.tsv"
IMAGE_IDS_FILE="$RUN_DIR/image-ids.txt"
REPORT_FILE="$OUTPUT_DIR/run-$RUN_ID.json"
LOG_FILE="$RUN_DIR/run.log"

mkdir -p "$RUN_DIR"
: > "$EVENTS_FILE"
: > "$IMAGE_IDS_FILE"

result="passed"

record_report() {
  CI_CD_RUN_ID="$RUN_ID" \
  CI_CD_STARTED_AT="$STARTED_AT" \
  CI_CD_RESULT="$result" \
    node "$ROOT_DIR/scripts/write-ci-cd-report.mjs" \
      "$EVENTS_FILE" "$IMAGE_IDS_FILE" "$REPORT_FILE"
}

finish() {
  record_report
  printf '\nJSON report: %s\n' "$REPORT_FILE"
}

trap finish EXIT

run_step() {
  local name="$1"
  shift
  local command="$*"
  local started ended status duration

  printf '\n==> %s: %s\n' "$name" "$command" | tee -a "$LOG_FILE"
  started="$(date +%s)"

  if "$@" 2>&1 | tee -a "$LOG_FILE"; then
    status="passed"
  else
    status="failed"
    result="failed"
  fi

  ended="$(date +%s)"
  duration=$((ended - started))
  printf '%s\t%s\t%s\t%s\n' "$name" "$command" "$status" "$duration" >> "$EVENTS_FILE"
  printf '<== %s (%s, %ss)\n' "$name" "$status" "$duration" | tee -a "$LOG_FILE"

  [[ "$status" == "passed" ]]
}

cd "$ROOT_DIR"

run_step "lint" npm run lint || exit 1
run_step "typecheck" npm run typecheck || exit 1
run_step "tests" npm test || exit 1
run_step "secret-scan" npm run gitleaks || exit 1

printf '\n==> deploy (emulated): Deploying on Coolify (emulated)\n' | tee -a "$LOG_FILE"
printf 'No external service was contacted.\n' | tee -a "$LOG_FILE"

run_step "docker-build" docker compose build || exit 1

compose_project="${COMPOSE_PROJECT_NAME:-$(basename "$ROOT_DIR")}"
for service in backend frontend database; do
  image="${compose_project}-${service}:latest"
  if docker image inspect "$image" >/dev/null 2>&1; then
    docker image inspect "$image" --format '{{.Id}}' >> "$IMAGE_IDS_FILE"
  fi
done
sort -u -o "$IMAGE_IDS_FILE" "$IMAGE_IDS_FILE"
printf '\nImages built:\n' | tee -a "$LOG_FILE"
cat "$IMAGE_IDS_FILE" | tee -a "$LOG_FILE"
