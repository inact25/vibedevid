# SERVER ACTIONS GUIDE

## OVERVIEW

`lib/actions/` is the mutation layer for the root app. Files here already use `'use server'`, zod validation, Supabase access, ownership/role checks, Uploadthing cleanup, and path revalidation.

## WHERE TO LOOK

- project submit/edit/delete: `projects.ts`
- event submit/moderation: `events.ts`
- blog/comments/analytics/user flows: `blog.ts`, `comments.ts`, `analytics.ts`, `user.ts`
- admin mutations: `admin/*`
- legacy large action file: `../actions.ts`

## CONVENTIONS

- Start every action file with `'use server'`.
- Validate external input before writes; existing files use zod and explicit field-error maps.
- Use `createClient()` for user-scoped writes and `createAdminClient()` only when bypassing RLS is intentional.
- Revalidate affected routes/tags after successful mutations.
- Prefer adding new work to the split domain files here instead of extending the legacy `lib/actions.ts` monolith.
- Keep return shapes explicit: success flag, error message, and field errors when relevant.

## ANTI-PATTERNS

- Do not move mutations into client components or route components.
- Do not skip ownership or role checks for destructive/admin actions.
- Do not forget Uploadthing cleanup when replacing provisional or existing files.
- Do not trust raw `FormData` values without normalization.
