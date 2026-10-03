# External Integrations

## Core Sections (Required)

### 1) Integration Inventory

| System | Type (API/DB/Queue/etc) | Purpose | Auth model | Criticality | Evidence |
|--------|---------------------------|---------|------------|-------------|----------|
| PostgreSQL | Database | Persists `Task` records through Prisma | Local Compose credentials/env vars | high | `to-do-list/backend/src/prisma/schema.prisma`, `docker-compose.yml` |
| Frontend clients | HTTP consumer | Intended consumer of task endpoints | None shown | medium | `README.md`, `to-do-list/backend/src/index.ts` |
| Nginx | Static web server | Serves the compiled frontend image | None | medium | `dockerfiles/frontend.dockerfile`, `dockerfiles/frontend.nginx.conf` |

### 2) Data Stores

| Store | Role | Access layer | Key risk | Evidence |
|-------|------|--------------|----------|----------|
| PostgreSQL | Task persistence | Prisma Client | Local credentials use development defaults unless overridden | `to-do-list/backend/src/prisma/schema.prisma`, `.env.example`, `docker-compose.yml` |

### 3) Secrets and Credentials Handling

- Credential sources: `.env.example` and Docker Compose environment variables for local development.
- Hardcoding checks: no credentials were found; the backend defaults to port `3000` but accepts `PORT`.
- Rotation or lifecycle notes: [TODO].

### 4) Reliability and Failure Behavior

- Retry/backoff behavior: none found.
- Timeout policy: none found.
- Circuit-breaker or fallback behavior: none found.
- Local container startup applies the Prisma schema with `prisma db push` before starting the backend.
- PATCH maps caught update failures to HTTP 404; GET/POST database failures have no explicit handler.

### 5) Observability for Integrations

- Logging around external calls: no database-call logging; startup uses `console.log`.
- Metrics/tracing coverage: none found.
- Missing visibility gaps: request correlation, database latency, error metrics, and health endpoint are [TODO].

### 6) Evidence

- `to-do-list/backend/src/index.ts`
- `to-do-list/backend/src/prisma/schema.prisma`
- `.env.example`
- `docker-compose.yml`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
