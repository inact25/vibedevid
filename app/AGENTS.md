# APP ROUTER GUIDE

## OVERVIEW

`app/` is the main Next.js 16 App Router tree: public routes, dynamic segments, route groups, API handlers, metadata, and auth callback entry points.

## WHERE TO LOOK

- public homepage and global metadata: `app/layout.tsx`, `app/page.tsx`
- route groups and dashboards: `app/(admin)/*`, `app/dashboard/*`
- API handlers: `app/api/**/route.ts`, `app/api/**/route.tsx`
- auth callback: `app/auth/callback/route.ts`
- localized metadata/text: `app/layout.tsx`, `messages/*.json`

## CONVENTIONS

- Default to Server Components; existing client-heavy route helpers use `*-client.tsx`.
- Use `generateMetadata()` or route-level `metadata` where SEO differs by route.
- Use `next-intl/server` helpers (`getLocale`, `getTranslations`) for layout/page metadata work.
- Keep route handlers under `app/api/**/route.*`; do not hide them in feature folders.
- Reuse `lib/seo/site-url.ts` and `getSiteUrl()` for canonical URLs and metadata base.

## SPECIAL CASES

- `app/(admin)` is the protected admin dashboard route group.
- `app/admin/page.tsx` is a separate public-facing admin page and is **not** covered by `app/(admin)` rules.
- Dynamic routes already exist for usernames, blog posts, events, and projects; follow their slug/param patterns instead of inventing new ones.

## VERIFY

- run `bunx tsc --noEmit`
- run `bun run dev` for route/layout changes
- manually hit changed routes and relevant API handlers

## ANTI-PATTERNS

- Do not hardcode locale-specific metadata strings when `next-intl` already owns them.
- Do not move route-specific server mutations into components; keep them in `lib/actions`.
- Do not assume `/admin` means `app/(admin)`.
