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
