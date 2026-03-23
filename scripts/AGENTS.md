# SCRIPTS AND MIGRATIONS GUIDE

## OVERVIEW

`scripts/` is mostly ordered SQL migrations plus a few repo scripts such as `lint-changed.mjs` and destructive maintenance helpers.

## WHERE TO LOOK

- schema bootstrap: `01_create_tables.sql`
- RLS/policy hardening: `08_*` through `20_*`
- blog/image cleanup migrations: `12_*` through `15_*`
- lint helper: `lint-changed.mjs`
- destructive helpers: `clear_database.js`, `production-reset.sql`

## CONVENTIONS

- Preserve numeric migration ordering; append new migrations instead of renumbering old ones.
- Keep SQL changes narrow and review the related docs in `docs/database/*` or `docs/migrations/*` before changing historical assumptions.
- Treat RLS, indexes, and foreign keys as first-class concerns; many scripts in this folder exist only to tighten those areas.
- Root linting for changed files runs through `node scripts/lint-changed.mjs`.

## ANTI-PATTERNS

- Do not casually run `production-reset.sql` or `clear_database.js`.
- Do not rename or reorder historical migrations after they have meaning in the sequence.
- Do not remove indexes just because they look unused; check the database docs first.
