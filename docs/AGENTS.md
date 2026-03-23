# DOCUMENTATION GUIDE

## OVERVIEW

`docs/` is the repo knowledge base for database work, deployment, migrations, testing, legal, architecture, reviews, and dated plans.

## WHERE TO LOOK

- index: `docs/README.md`
- database decisions: `docs/database/*`
- deployment/runbook: `docs/deployment/*`
- migration history + verification: `docs/migrations/*`
- testing notes: `docs/testing/*`
- dated implementation/design plans: `docs/plans/*`
- security references: `docs/security/*`

## CONVENTIONS

- Keep docs in the correct category; do not dump everything into `plans/`.
- Use kebab-case filenames; `docs/README.md` already documents that convention.
- When adding/removing docs or AGENTS files, update `docs/README.md` in the same change.
- Keep app-facing legal or operational docs aligned with the corresponding code paths and pages.
- Treat dated plan docs as historical context unless newer code or newer plans supersede them.

## ANTI-PATTERNS

- Do not treat `%TEMP%` or imported third-party docs as repo policy.
- Do not leave stale AGENTS links in `docs/README.md`.
- Do not record destructive DB or deployment guidance without rollback/verification notes nearby.
