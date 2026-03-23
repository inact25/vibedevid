# UI PRIMITIVES GUIDE

## OVERVIEW

`components/ui/` is the root shared UI layer. It contains Radix/shadcn-style primitives plus several large client widgets such as `submit-project-form.tsx`, `sidebar.tsx`, and `video-vibe-coding-manager.tsx`.

## WHERE TO LOOK

- core primitives: `button.tsx`, `input.tsx`, `card.tsx`, `select.tsx`, `tabs.tsx`, `sheet.tsx`
- notifications: `sonner.tsx`, `toaster.tsx`
- sidebar system: `sidebar.tsx`, `hooks/use-mobile.tsx`
- large domain widgets: `submit-project-form.tsx`, `video-vibe-coding-manager.tsx`, `profile-edit-dialog.tsx`

## CONVENTIONS

- Build on the existing Radix + CVA + Tailwind patterns already used in this folder.
- Reuse existing primitives before adding new wrappers.
- Client widgets should call `lib/actions/*` for mutations instead of embedding DB access.
- Keep image/upload flows aligned with existing progressive/upload helpers instead of inventing a second pattern.
- Sidebar state already uses a `sidebar_state` cookie and `SidebarProvider`; follow that path for sidebar work.

## ANTI-PATTERNS

- Do not import UI primitives from `admin-kit/` into the root app.
- Do not grow the existing large files indefinitely; extract sections/helpers instead.
- Do not put server secrets, Supabase admin clients, or direct service-role logic in client components.
