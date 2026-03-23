# COMPONENTS GUIDE

## OVERVIEW

`components/` holds shared feature components, app shells, providers, and loose reusable pieces. It is broader than `components/ui/`; feature folders like `blog/`, `event/`, `project/`, `profile/`, `sections/`, `layout/`, and `admin-panel/` live here too.

## WHERE TO LOOK

- shared providers/wrappers: `agentation-provider.tsx`, `theme-provider.tsx`, `search-provider.tsx`
- dashboard chrome: `admin-panel/*`, `layout/*`
- feature UI: `blog/*`, `event/*`, `project/*`, `profile/*`, `sections/*`
- primitive controls: `ui/*`

## CONVENTIONS

- Put reusable primitives in `components/ui/`; keep feature composition here.
- Let components call hooks and server actions, but keep database mutation logic in `lib/actions/*`.
- Prefer reusing existing provider, search, theme, dialog, and sidebar wiring before introducing parallel wrappers.
- Match existing folder ownership: landing-page sections stay in `sections/`, dashboard chrome stays in `admin-panel/` or `layout/`.

## ANTI-PATTERNS

- Do not import `admin-kit/src/components/*` into the root app.
- Do not add another button/input/modal primitive here when `components/ui/` already owns it.
- Do not move route ownership out of `app/` just to share JSX.
