# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-23
**Commit:** 2d09393
**Branch:** main

## OVERVIEW

VibeDev ID is a Next.js 16 App Router app backed by Supabase, `next-intl`, Bun, Biome, Vitest, and Playwright. This repo also contains `admin-kit/`, a separate Next.js 15 package with its own pnpm + ESLint + Prettier workflow.

## INHERITANCE

- Read this file first.
- Then read the closest nested `AGENTS.md` for the subtree you are touching.
- Ignore `%TEMP%/nextjs-docs/AGENTS.md`; it is imported reference material, not repo-local policy.

## STRUCTURE

```text
./
├── app/              # Next.js 16 routes, layouts, API handlers
├── components/       # feature components + shared wrappers
├── lib/              # helpers, Supabase, auth, SEO, uploads
├── docs/             # operational and design documentation
├── scripts/          # SQL migrations + repo scripts
├── admin-kit/        # separate Next.js 15 package
```

## WHERE TO LOOK

| Task | Location | Notes |
| --- | --- | --- |
| auth/session | `lib/server/auth.ts`, `lib/supabase/*` | server/client/admin split |
| project submit/edit | `components/ui/submit-project-form.tsx`, `lib/actions/projects.ts` | Uploadthing + validation + cache refresh |
| admin moderation | `app/(admin)/*`, `lib/actions/admin/*`, `lib/actions/events.ts` | role-gated dashboard subtree |
| public `/admin` page | `app/admin/page.tsx` | separate from `app/(admin)` |
| docs index | `docs/README.md` | keep links current |
| DB history | `scripts/*.sql`, `docs/migrations/*`, `docs/database/*` | numbered migration flow |

## COMMANDS

```bash
bun run dev
bun run lint        # changed files only
bun run lint:all
bunx tsc --noEmit   # required; build ignores TS errors
bun run test
bun run test:e2e
bun run build
```

## CONVENTIONS

- Use Bun at the repo root.
- Use Biome at the repo root; do not introduce root-level ESLint/Prettier workflows.
- Prefer Server Components in `app/`; client-heavy files commonly use `*-client.tsx`.
- Put server mutations in `lib/actions/*` with `'use server'`.
- `components/ui/` is the shared UI layer; feature-specific components live in sibling folders.
- `next-intl` is wired through `i18n/request.ts`, `messages/*.json`, and `app/layout.tsx`.

## ANTI-PATTERNS

- Do not rely on `bun run build` for type safety; `next.config.mjs` sets `typescript.ignoreBuildErrors = true`.
- Do not mix root tooling assumptions with `admin-kit/`.
- Do not create or update files under `.next/`, `node_modules/`, `playwright-report/`, `%TEMP%/`, or `nul`.
- Do not assume every `/admin` route is protected by `app/(admin)`.
- Do not duplicate Supabase client setup, env parsing, slug logic, or URL normalization outside `lib/`.

## NOTES

- Root test config points at `tests/unit`, `tests/integration`, and `tests/e2e`; verify actual test files exist in the current checkout before claiming coverage.
- Keep `docs/README.md` aligned with the AGENTS hierarchy.
