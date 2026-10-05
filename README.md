# To-do list

A small full-stack to-do application built with TypeScript, React, Express,
Prisma, and PostgreSQL.

> **Callout:** See [`docs/misc/short_anwers.md`](docs/misc/short_anwers.md) for the short answers.

## Contents

- [How to use the repository](#how-to-use-the-repository)
- [Project structure](#project-structure)
- [Development and quality checks](#development-and-quality-checks)
- [Technical information](#technical-information)
- [GitHub CI/CD](#github-cicd)
- [Database backups](#database-backups)
- [Current scope and next steps](#current-scope-and-next-steps)

## How to use the repository

### Prerequisites and environment

Docker must be installed before starting the containerized application. Docker
Desktop includes Docker Compose; on Linux, install Docker Engine and the
Compose plugin.

Create the local environment file from the example:

```bash
cp .env.example .env
```

Replace the placeholder database credentials and frontend origin in `.env`.
Compose requires these values from `.env`; it does not load `.env.example`.
Never commit real credentials.

### Run the complete application with Docker Compose

From the repository root, start the database, backend, and frontend services:

```bash
docker compose up --build
```

The services are available at:

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:3000>
- Backend health check: <http://localhost:3000/health>
- PostgreSQL: `localhost:5432`

The backend waits for a healthy database and applies committed Prisma
migrations before starting. Stop the foreground services with `Ctrl+C`, or
start them in the background with `docker compose up --build -d` and stop them
later with:

```bash
docker compose down
```

### Run the frontend with Vite

Use Vite when making changes to the React frontend. Keep the database and
backend running so the frontend can load and update tasks:

```bash
docker compose up -d database backend
npm run dev --workspace frontend
```

Vite serves the frontend at <http://localhost:5173> and automatically reloads
when files under `to-do-list/frontend/src` change. Stop the Vite server with
`Ctrl+C` when finished.

## Project structure

The repository is an npm-workspaces monorepo containing the backend and
frontend:

```text
.
├── .github/workflows/              # GitHub Actions quality and deployment workflows
├── dockerfiles/                    # Service Dockerfiles and Nginx configuration
├── docs/                           # Architecture, testing, stack, and project notes
├── scripts/                        # Backup, restore, CI/CD, and reporting scripts
├── tests/backend/                  # Backend unit and HTTP integration tests
├── to-do-list/
│   ├── backend/
│   │   └── src/
│   │       ├── models/             # Request models and validation
│   │       ├── prisma/             # Prisma schema and database migrations
│   │       ├── routes/             # Express task routes
│   │       ├── app.ts              # Express application construction
│   │       └── index.ts            # Prisma client setup and server startup
│   └── frontend/
│       ├── src/                    # React application and styles
│       ├── index.html              # Browser entry document
│       └── vite.config.ts          # Vite development and build configuration
├── .env.example                    # Example local environment variables
├── docker-compose.yml              # Local multi-service application definition
├── Makefile                        # Shortcuts for backups and CI/CD emulation
├── package.json                    # Root workspace scripts and tooling
└── README.md                       # Project documentation
```

The main areas are organized as follows:

- `.github/workflows/` contains the GitHub Actions workflows for quality checks
  and the Coolify deployment notification.
- `dockerfiles/` contains one image definition for each service, plus the Nginx
  configuration used to serve the built frontend.
- `docs/` contains documentation covering architecture, conventions,
  integrations, testing, and technical concerns.
- `scripts/` contains operational utilities for database backups and restores,
  local CI/CD emulation, and report generation.
- `tests/backend/` contains request-validation unit tests and Express API
  integration tests using an injected database mock.
- `to-do-list/backend/` is the backend workspace. `models` validates requests,
  `routes` exposes the task API, and `prisma` defines the PostgreSQL schema and
  committed migrations.
- `to-do-list/frontend/` is the React workspace. Its `src` directory contains
  the application components, API calls, theme behavior, and styles.
- `docker-compose.yml` connects the database, backend, and frontend services,
  including ports, dependencies, volumes, and health checks.
- `Makefile` provides shortcuts such as `make backup` and
  `make emulate-ci-cd`.

## Development and quality checks

The root workspace provides the common commands:

```bash
npm run lint
npm run typecheck
npm test
npm run format
```

The backend test suite contains request-validation unit tests and HTTP API
integration tests. The API tests inject a database mock, so they do not require
a live PostgreSQL instance.

Pre-commit and pre-push checks are configured with Lefthook and include:

- Linting, formatting, and TypeScript checks.
- Conventional commit-message validation.
- Secret scanning with Gitleaks.
- Branch-name validation and dependency auditing.

Time to complete quality checks is 30s

## Technical information

### Application stack

- Frontend: React `19.1.1` with Vite `7.1.7`.
- Backend: Node.js 22, TypeScript `5.9.3`, and Express `5.2.1`.
- Persistence: Prisma `6.19.3` with PostgreSQL `18-alpine`.
- Testing: Vitest `5.0.3` and Supertest `7.1.4`.
- Package management: npm workspaces with the root `package-lock.json`.

### Compose services and ports

| Service | Container image | Host port | Container port | Purpose |
| --- | --- | ---: | ---: | --- |
| `frontend` | `to-do-list-frontend` | `5173` | `8080` | Serves the built React app through Nginx |
| `backend` | `to-do-list-backend` | `3000` | `3000` | Express API and Prisma migrations |
| `database` | `to-do-list-database` | `5432` | `5432` | PostgreSQL task persistence |

The database uses the named `postgres_data` volume so data survives normal
container restarts. `docker compose down --volumes` removes that volume and
its data when a clean database reset is required.

### Latest Docker build metrics

The following values were collected after rebuilding with `docker compose build`.
Sizes and build duration depend on the local Docker cache and host machine.

| Image | Size | Layers | Platform | Runtime user | Command |
| --- | ---: | ---: | --- | --- | --- |
| `to-do-list-backend:latest` | 729.84 MiB / 765,294,313 bytes | 14 | `linux/amd64` | `node` | `npm run db:migrate && npm run start` |
| `to-do-list-frontend:latest` | 78.75 MiB / 82,577,498 bytes | 11 | `linux/amd64` | `101` | `nginx -g daemon off;` |
| `to-do-list-database:latest` | 412.68 MiB / 432,729,160 bytes | 9 | `linux/amd64` | `postgres` | `postgres` |

Additional image metadata:

- Backend exposes `3000/tcp`.
- Frontend exposes `8080/tcp`.
- Database exposes `5432/tcp`.
- The backend and database run as non-root users; the frontend uses the
  unprivileged Nginx image.

## GitHub CI/CD

### Quality gate

Pull requests and pushes targeting `main` or `master` run the quality gate in
[`.github/workflows/quality-gate.yml`](.github/workflows/quality-gate.yml):

- ESLint
- TypeScript checks
- Backend tests
- Secret scanning with Gitleaks

The quality gate does not publish Docker images. Configure its jobs as required
status checks in the protected `main` branch before allowing merges.

### Coolify integration

The [`coolify-integration.yml`](.github/workflows/coolify-integration.yml)
workflow runs after a pull request is merged into `main`. It verifies that the
quality gate passed, then calls the configured Coolify webhook.

Coolify should be configured with this repository, the `main` branch, and
`docker-compose.yml`. It builds the three services on the Coolify server.
Configure `COOLIFY_WEBHOOK_URL` and, when required by the webhook,
`COOLIFY_TOKEN`. Previous successful deployments can be used for rollback.

### Local CI/CD emulation

Run the local pipeline with:

```bash
make emulate-ci-cd
```

The command runs linting, typechecking, tests, secret scanning, and a local
Docker Compose build. The Coolify deployment is simulated only; no external
service is contacted. Each run writes a JSON report under
`artifacts/ci-cd/`.

## Database backups

With the database service running, create a compressed PostgreSQL backup:

```bash
make backup
```

Backups are written to `backups/databank-<UTC timestamp>.dump` and are ignored
by Git. `make db-backup` is an alias for `make backup`. To use another output
directory, set `BACKUP_DIR`, for example:

```bash
BACKUP_DIR=/mnt/backups make backup
```

Restore a backup into the running database with:

```bash
BACKUP_FILE=backups/databank-<UTC timestamp>.dump make db-restore
```

Restore uses PostgreSQL's `--clean --if-exists` options and replaces matching
objects in the running database. Restore validation should be performed after
creating important backups.

## Current scope and next steps

The current application is a single-user personal task board. Authentication
and per-user task ownership are intentionally out of scope.
