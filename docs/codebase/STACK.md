# Technology Stack

## Core Sections (Required)

### 1) Runtime Summary

| Area | Value | Evidence |
|------|-------|----------|
| Primary language | TypeScript for the backend; README states TypeScript and React as the intended stack | `README.md`, `to-do-list/backend/src/index.ts` |
| Runtime + version | Node.js runtime is implied by npm/TypeScript tooling; exact version is [TODO] | `package.json`, `backend/package.json` |
| Package manager | npm workspaces | `package.json`, `package-lock.json` |
| Module/build system | CommonJS package mode with `ts-node` development execution; no build configuration found | `package.json`, `backend/package.json` |

### 2) Production Frameworks and Dependencies

| Dependency | Version | Role in system | Evidence |
|------------|---------|----------------|----------|
| Express | `^5.2.1` | HTTP server and task routes | `to-do-list/backend/package.json`, `to-do-list/backend/src/index.ts` |
| CORS | `^2.8.6` | Cross-origin middleware | `to-do-list/backend/package.json`, `to-do-list/backend/src/index.ts` |
| `@prisma/client` | `^6.16.2` | Database client | `to-do-list/backend/package.json`, `to-do-list/backend/src/index.ts` |
| React | `^19.1.1` | Frontend UI runtime | `to-do-list/frontend/package.json`, `to-do-list/frontend/src/App.tsx` |
| React DOM | `^19.1.1` | Browser rendering | `to-do-list/frontend/package.json`, `to-do-list/frontend/src/main.tsx` |

### 3) Development Toolchain

| Tool | Purpose | Evidence |
|------|---------|----------|
| TypeScript | Backend language/tooling | `to-do-list/backend/package.json`, `to-do-list/backend/src/index.ts` |
| `ts-node` | Runs backend TypeScript directly in development | `to-do-list/backend/package.json` |
| Prisma CLI | Prisma client generation and database tooling | `to-do-list/backend/package.json`, `to-do-list/backend/src/prisma/schema.prisma` |
| Vite | `^7.1.7` | Frontend development server and production bundler | `to-do-list/frontend/package.json`, `to-do-list/frontend/vite.config.ts` |
| Linter/formatter/test runner | [TODO] No project configuration or real test command found | Scan output, package manifests |

### 4) Key Commands

```bash
npm install
npm run --workspace backend dev
npm run build --workspace frontend
npm run test --workspace backend
```

Build and lint commands are [TODO].

### 5) Environment and Config

- Config sources: `package.json`, `to-do-list/backend/package.json`, `to-do-list/backend/tsconfig.json`, `to-do-list/backend/src/prisma/schema.prisma`, `.env.example`, and `docker-compose.yml`.
- Required env vars: `DATABASE_URL` for Prisma; `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` configure the local database. `PORT` is supplied by Compose but the current source still uses `3000` directly.
- Deployment/runtime constraints: deployment target is local; Docker Compose provides PostgreSQL, backend, and an Nginx-served frontend on port `5173`.
- Database initialization: the backend image runs `prisma migrate deploy` before starting the API. Schema changes must be committed under `to-do-list/backend/src/prisma/migrations/`.

### 6) Evidence

- `package.json`
- `to-do-list/backend/package.json`
- `to-do-list/backend/src/index.ts`
- `to-do-list/backend/src/prisma/schema.prisma`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
