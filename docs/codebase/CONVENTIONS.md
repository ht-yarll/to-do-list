# Coding Conventions

## Core Sections (Required)

### 1) Naming Rules

| Item | Rule | Example | Evidence |
|------|------|---------|----------|
| Files | Lowercase/simple names are present; complete rule is [TODO] | `index.ts`, `schema.prisma` | Repository tree |
| Functions/methods | Express callbacks are inline arrow functions; complete rule is [TODO] | `app.get('/tasks', async (...) => ...)` | `to-do-list/backend/src/app.ts` |
| Types/interfaces | Framework types use PascalCase imports | `Request`, `Response`, `PrismaClient` | `to-do-list/backend/src/app.ts` |
| Constants/env vars | Uppercase is used for the port environment variable | `PORT` | `to-do-list/backend/src/index.ts` |

### 2) Formatting and Linting

- Formatter: [TODO] No formatter configuration found.
- Linter: [TODO] No linter configuration found.
- Most relevant enforced rules: [TODO].
- Run commands: [TODO]; no lint/format scripts are defined.

### 3) Import and Module Conventions

- Import grouping/order: [TODO]; the only source file groups package imports without a documented rule.
- Alias vs relative import policy: package imports are used; no aliases were found.
- Public exports/barrel policy: [TODO]; no exports or barrel files are present.

### 4) Error and Logging Conventions

- Error strategy by layer: route handlers return JSON errors for missing titles and failed updates; database errors in GET/POST are not explicitly caught.
- Logging style and required context fields: one `console.log` startup message; required context is [TODO].
- Sensitive-data redaction rules: [TODO].

### 5) Testing Conventions

- Test file naming/location rule: [TODO]; no test files found.
- Mocking strategy norm: [TODO].
- Coverage expectation: [TODO].

### 6) Evidence

- `to-do-list/backend/src/index.ts`
- `backend/package.json`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
