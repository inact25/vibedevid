# ADMIN DASHBOARD GUIDE

## OVERVIEW

`app/(admin)/` is the protected admin dashboard subtree. It uses a role check in layout, tabbed board views, and admin-only mutations backed by Supabase admin access where needed.

## WHERE TO LOOK

- auth gate: `app/(admin)/layout.tsx`
- dashboard tabs and board composition: `app/(admin)/dashboard/page.tsx`
- board-specific UI: `app/(admin)/dashboard/boards/*`
- admin mutations: `lib/actions/admin/*`
- event moderation flow: `lib/actions/events.ts`

## CONVENTIONS

- Keep access control at the layout and server-action layer; this subtree already redirects non-admin users in `layout.tsx`.
- Treat each `boards/*` directory as an admin domain boundary: users, projects, blog, comments, events, analytics, overview.
- Reuse `components/admin-panel/*` and `components/ui/*` rather than pulling from unrelated packages.
- Use query-param driven filters/search/tab state where the subtree already does so.

## VERIFY

- check the layout gate still redirects unauthorized users
- manually exercise changed board filters/actions in `bun run dev`
- re-check cache refresh and moderation state after admin mutations

## ANTI-PATTERNS

- Do not apply these rules to `app/admin/page.tsx`; that file is outside this subtree.
- Do not expose admin data or actions without a role check.
- Do not bypass RLS with a public client when the change requires `createAdminClient()`.
- Do not reuse the main-site header/footer in this dashboard subtree.
