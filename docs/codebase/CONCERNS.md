# Codebase Concerns

## Core Sections (Required)

### 1) Top Risks (Prioritized)

| Severity | Concern | Evidence | Impact | Suggested action |
|----------|---------|----------|--------|------------------|
| medium | Database credentials are supplied through `.env` | `.env.example`, `docker-compose.yml` | Deployment fails if required values are missing | Keep `.env` out of version control and use a secret manager in production |
| medium | No automated tests or CI | package manifests, scan output | Regressions are not detected | Add API/database tests and CI checks |

### 2) Technical Debt

| Debt item | Why it exists | Where | Risk if ignored | Suggested fix |
|-----------|---------------|-------|----------------|---------------|
| Inline route/data-access design | Current implementation is concentrated in one file | `to-do-list/backend/src/index.ts` | Harder testing and extension | Separate routes, services, and persistence access |
| Hardcoded server port | Source still declares `const PORT = 3000` | `to-do-list/backend/src/index.ts` | Deployment flexibility is limited | Read the `PORT` environment variable with a default |
| Frontend has no automated UI tests | Frontend behavior is currently untested | `to-do-list/frontend/src/`, `docs/codebase/TESTING.md` | UI/API regressions may go unnoticed | Add component and browser tests |

### 3) Security Concerns

| Risk | OWASP category (if applicable) | Evidence | Current mitigation | Gap |
|------|--------------------------------|----------|--------------------|-----|
| CORS origins are explicitly configured | A05 Security Misconfiguration | `to-do-list/backend/src/app.ts`, `.env.example` | Production refuses to start without `CORS_ALLOWED_ORIGINS` | Set only the deployed frontend origin(s) |
| Minimal input validation | A03 Injection / data validation | `to-do-list/backend/src/index.ts` | Checks only truthiness of `title` | Validate type and length of `title` |
| No authentication/authorization | N/A for current single-user scope | `to-do-list/backend/src/index.ts`, `README.md` | App is intended as a personal local tool | Revisit if multi-user access is added |

### 4) Performance and Scaling Concerns

| Concern | Evidence | Current symptom | Scaling risk | Suggested improvement |
|---------|----------|-----------------|-------------|-----------------------|
| Unbounded task listing | `to-do-list/backend/src/index.ts` | GET returns every task | Response/database cost grows with task count | Add pagination and limits |
| No timeout/retry/health behavior | `to-do-list/backend/src/index.ts`, scan output | Integration failures are handled inconsistently | Slow/failing database can tie up requests | Add operational timeouts and explicit failure handling |

### 5) Fragile/High-Churn Areas

| Area | Why fragile | Churn signal | Safe change strategy |
|------|-------------|--------------|----------------------|
| `to-do-list/backend/src/index.ts` | Contains bootstrap, middleware, all routes, persistence, and startup | Git history unavailable; churn is [TODO] | Add tests before extracting route/service modules |

### 6) Resolved Scope Decisions

- The current application is a single-user personal app deployed locally; authentication and per-user task ownership are intentionally out of scope for now.

### 7) Evidence

- `to-do-list/backend/src/index.ts`
- `to-do-list/backend/src/prisma/schema.prisma`
- `to-do-list/frontend/package.json`
- `README.md`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
