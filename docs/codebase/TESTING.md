# Testing Patterns

## Core Sections (Required)

### 1) Test Stack and Commands

- Primary test framework: Vitest `^3.2.4`.
- Assertion/mocking tools: Vitest assertions/mocks and Supertest `^7.1.4` for HTTP integration tests.
- Commands:

```bash
npm run test --workspace backend
# coverage command: [TODO]
```

### 2) Test Layout

- Test file placement pattern: repository-level `tests/backend/`.
- Naming convention: `*.unit.test.ts` for unit tests and `*.integration.test.ts` for HTTP integration tests.
- Setup files and where they run: [TODO].

### 3) Test Scope Matrix

| Scope | Covered? | Typical target | Notes |
|-------|----------|----------------|-------|
| Unit | yes | task input validation | `tests/backend/validation.unit.test.ts` |
| Integration | partial | Express task API with injected database mock | `tests/backend/tasks.integration.test.ts`; does not require a live PostgreSQL instance |
| E2E | no evidence | frontend task flows | Frontend source is absent |

### 4) Mocking and Isolation Strategy

- Main mocking approach: Vitest function mocks for the injected task database; Supertest drives the Express app.
- Isolation guarantees: a fresh database mock is created before each test; the app is created per test request.
- Common failure mode in tests: a live database is not exercised by the current integration suite.

### 5) Coverage and Quality Signals

- Coverage tool + threshold: [TODO].
- Current reported coverage: 10 tests passing across unit and integration suites.
- Known gaps/flaky areas: no live PostgreSQL integration test or end-to-end frontend test exists.

### 6) Evidence

- `package.json`
- `to-do-list/backend/package.json`
- `tests/backend/validation.unit.test.ts`
- `tests/backend/tasks.integration.test.ts`
- Terminal scan output from `.agents/skills/acquire-codebase-knowledge/scripts/scan.py`
