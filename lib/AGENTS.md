# LIBRARY GUIDE

## OVERVIEW

`lib/` is the root utility layer: Supabase clients, server auth, env parsing, SEO helpers, upload flows, URL/slug helpers, AI integrations, constants, and non-mutating data helpers.

## WHERE TO LOOK

- Supabase clients: `lib/supabase/{client,server,admin,middleware}.ts`
- server auth helpers: `lib/server/auth.ts`
- env parsing: `lib/env-config.ts`
- SEO/site URL: `lib/seo/site-url.ts`
- URL + slug logic: `lib/project-url.ts`, `lib/slug.ts`
- uploads/images: `lib/uploadthing*.ts`, `lib/image-utils.ts`, `lib/favicon-utils.ts`
- server mutations: `lib/actions/*`

## CONVENTIONS

- Keep shared helpers here; move mutations into `lib/actions/*`.
- Reuse the existing client/server/admin Supabase split instead of creating ad hoc clients.
- Prefer `getUser()`-based server validation patterns already documented in `lib/server/auth.ts` and `hooks/useAuth.ts`.
- Read env values through `env-config.ts`; keep URL and slug normalization centralized.

## ANTI-PATTERNS

- Do not duplicate Supabase setup, env parsing, site URL logic, slug generation, or project URL normalization.
- Do not spread the `as any` session shim pattern from `lib/server/auth.ts`; prefer direct typed helpers when touching auth code.
- Do not add app-specific JSX here unless the file is already intentionally view-adjacent.
