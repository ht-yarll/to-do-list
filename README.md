# Goal

The goal for this task is to create a simpel to-do list using Typescript, Prisma and React. For backend: Prisma, Typescript, Express
frontend: Typescript and React

## Structure

Monorepo holding both back and frontend as workspaces.

## Pre-commit checks

- Lint and Typecheck
- Enforce standard commit message
- Check for any secret leaks

## Technical Information

**Docker**:

- image-size:
- time to build:
- time to build with cache:

## GitHub quality gate

Pull requests targeting `main` run three independent required checks through
the self-hosted GitHub Actions runner:

- `Lint and typecheck` runs ESLint and TypeScript checks.
- `Tests` runs the backend test suite.
- `Secret scan` checks the repository history with Gitleaks.

Configure these three checks as required status checks in the `main` branch
protection rules. A pull request can merge only after all required checks pass.

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
