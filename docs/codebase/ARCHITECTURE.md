# Architecture

## Core Sections (Required)

### 1) Architectural Style

- Primary style: small monolithic HTTP service with inline route/data-access logic.
- Why this classification: one entry file creates the Express app, registers routes, directly calls Prisma, and starts the server.
- Primary constraints: task persistence requires Prisma/PostgreSQL; all backend routes share one process; frontend integration is intended but not implemented.

### 2) System Flow

```text
HTTP request -> Express middleware -> inline task route -> Prisma Client -> PostgreSQL -> JSON response
```

1. `to-do-list/backend/src/index.ts` constructs `PrismaClient` and the Express app.
2. CORS and JSON parsing middleware run for requests.
3. `/tasks` route handlers validate or read request data.
4. Handlers call `prisma.task.findMany/create/update`.
5. Results or JSON errors are returned to the caller.

### 3) Layer/Module Responsibilities

| Layer or module | Owns | Must not own | Evidence |
|-----------------|------|--------------|----------|
| Express bootstrap/routes | Middleware, HTTP routing, request validation, response serialization | [TODO] No documented separation exists | `to-do-list/backend/src/index.ts` |
| Prisma client instance | ORM access to `Task` records | UI concerns | `to-do-list/backend/src/index.ts` |
| Prisma schema | PostgreSQL datasource and `Task` model | HTTP behavior | `to-do-list/backend/src/prisma/schema.prisma` |

### 4) Reused Patterns

| Pattern | Where found | Why it exists |
|---------|-------------|---------------|
| Process-local client instance | `const prisma = new PrismaClient()` | Shared database client for route handlers | `to-do-list/backend/src/index.ts` |
| Middleware pipeline | `app.use(cors())`, `app.use(express.json())` | Cross-origin access and JSON parsing | `to-do-list/backend/src/index.ts` |

### 5) Known Architectural Risks

- HTTP, validation, persistence, and startup are coupled in one file, increasing change and testing cost.
- There is no frontend source or checked-in API client, so the stated end-to-end flow is incomplete.
- The service remains a single inline route/data-access module; additional endpoints will increase coupling until routes and persistence are separated.
- `to-do-list/backend/src/app.ts` now exposes app construction separately from `to-do-list/backend/src/index.ts`, allowing HTTP tests to inject a database implementation.

### 6) Evidence

- `to-do-list/backend/src/index.ts`
- `to-do-list/backend/src/prisma/schema.prisma`
- `README.md`
- `to-do-list/frontend/package.json`
