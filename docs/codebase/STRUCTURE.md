# Codebase Structure

## Core Sections (Required)

### 1) Top-Level Map

| Path | Purpose | Evidence |
|------|---------|----------|
| `to-do-list/backend/` | Backend workspace and Prisma schema | `to-do-list/backend/package.json`, `to-do-list/backend/src/` |
| `to-do-list/backend/src/index.ts` | Express application and task API entry point | `to-do-list/backend/src/index.ts` |
| `to-do-list/backend/src/prisma/schema.prisma` | Prisma datasource and `Task` model | `to-do-list/backend/src/prisma/schema.prisma` |
| `to-do-list/frontend/` | React/Vite frontend workspace | `to-do-list/frontend/package.json`, `to-do-list/frontend/src/` |
| `dockerfiles/` | Backend, frontend, and PostgreSQL image definitions | `dockerfiles/backend.dockerfile`, `dockerfiles/frontend.dockerfile`, `dockerfiles/databank.dockerfile` |
| `docker-compose.yml` | Local PostgreSQL, backend, and frontend orchestration | `docker-compose.yml` |
| `docs/codebase/` | Generated repository knowledge documents | This document set |
| `package.json` | npm workspace root | `package.json` |

### 2) Entry Points

- Main runtime entry: `to-do-list/backend/src/index.ts`.
- Secondary entry points (worker/cli/jobs): None found.
- How entry is selected: `to-do-list/backend/package.json` exposes `dev: ts-node src/index.ts`, `build`, and `start`; `to-do-list/frontend/index.html` loads `to-do-list/frontend/src/main.tsx`; root scripts proxy backend commands.

### 3) Module Boundaries

| Boundary | What belongs here | What must not be here |
|----------|-------------------|------------------------|
| `to-do-list/backend/src/index.ts` | Express setup, middleware, route handlers, Prisma calls, server startup | [TODO] No enforced separate service/repository boundary exists |
| `to-do-list/backend/src/prisma/` | Prisma schema and database model definitions | HTTP route handling |
| `to-do-list/frontend/` | React UI and API client | Backend persistence and database access |

### 4) Naming and Organization Rules

- File naming pattern: lowercase names are used for `index.ts`, `schema.prisma`, and package manifests; broader rule is [TODO].
- Directory organization pattern: workspace-based (`backend/`, `frontend/`) with backend source under `src/` and Prisma schema under `src/prisma/`.
- Import aliasing or path conventions: relative/module package imports only; no path aliases were found.

### 5) Evidence

- `package.json`
- `to-do-list/backend/package.json`
- `to-do-list/backend/src/index.ts`
- `to-do-list/backend/src/prisma/schema.prisma`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
