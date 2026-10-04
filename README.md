# Goal

The goal for this task is to create a simpel to-do list using Typescript, Prisma and React. For backend: Prisma, Typescript, Express
frontend: Typescript and React

> **Callout:** See [`docs/misc/short_anwers.md`](docs/misc/short_anwers.md) for the short answers.

## Structure

Monorepo holding both back and frontend as workspaces.

## Pre-commit checks

- Lint and Typecheck
- Enforce standard commit message
- Check for any secret leaks

## Technical Information

**Docker**:

- image size:
  - `to-do-list-backend`: 1,159.88 MiB (15 layers)
  - `to-do-list-frontend`: 89.55 MiB (10 layers)
  - `to-do-list-database`: 412.68 MiB (9 layers)
- time to build: 38 seconds
- time to build with cache: 2 seconds
- platform: `linux/amd64`
- configured user: `root` (default)
- exposed ports: backend `3000/tcp`, frontend `80/tcp`, database `5432/tcp`

## GitHub quality gate

Pull requests targeting `main` run three independent required checks through
the self-hosted GitHub Actions runner:

- `Lint and typecheck` runs ESLint and TypeScript checks.
- `Tests` runs the backend test suite.
- `Secret scan` checks the repository history with Gitleaks.

Configure these three checks as required status checks in the `main` branch
protection rules. A pull request can merge only after all required checks pass.

The [CI/CD workflow](.github/workflows/ci-cd.yml) also builds the backend,
frontend, and database images and publishes immutable GitHub Container Registry
tags in the form `sha-<commit SHA>`. The `main` branch additionally receives a
`latest` tag. The commit tag is the rollback-safe image reference.

The [Coolify integration workflow](.github/workflows/coolify-integration.yml)
is a deployment template. Configure the `COOLIFY_WEBHOOK_URL` secret and,
when required by the selected webhook, `COOLIFY_TOKEN`. It deploys the exact
commit image tag after a successful `main` workflow and supports manually
selecting an older `sha-<commit SHA>` tag for rollback.

## Container build metrics

The separate `Container build` workflow builds the backend, frontend, and
database images. For each image it logs the build duration, image ID, digest
metadata, architecture, operating system, configured user, command,
exposed ports, layer count, and final size in bytes and MiB. Docker Buildx
uses a separate GitHub Actions cache scope for each image.

## Local CI/CD emulation

Run the local pipeline with:

```bash
make emulate-ci-cd
```

The command runs linting, typechecking, tests, secret scanning, and a local
Docker Compose build. The Coolify deployment is currently simulated only; no
external service is contacted. Each run writes a JSON report under
`artifacts/ci-cd/`.

## Database backups

With the database service running, create a compressed PostgreSQL backup with:

```bash
make backup
```

Backups are written to `backups/databank-<UTC timestamp>.dump` and are ignored
by Git. The alias `make db-backup` runs the same command. To use another output
directory, set `BACKUP_DIR`, for example `BACKUP_DIR=/mnt/backups make backup`.

To restore a backup into the running database, use PostgreSQL's custom-format
restore tool:

```bash
docker compose exec -T database pg_restore \
  --username="${POSTGRES_USER:-todo}" \
  --dbname="${POSTGRES_DB:-todo}" \
  --clean --if-exists < backups/databank-<UTC timestamp>.dump
```
