# Decisions

- Keep scope on submit-project creation flow only; no moderation/status redesign.
- No schema changes by default; current project data quality does not justify expanding the DB upfront.
- Keep immediate-publish behavior.
- Use tests-after with Vitest for internal logic and Playwright for user flow.
# Decisions

- Kept `redirectTo` as a route-level constant for `/project/submit` so the auth flow and the form shell share the same return path without duplicating logic in the client.
- Used path-level revalidation for the smallest explicit cache invalidation after create: `revalidatePath('/project/list')` for the listing and `revalidatePath(`/project/${slug}`)` for the new detail page.
- Task 4: keep UploadThing deletion split into two layers — `lib/uploadthing.ts` owns raw `UTApi.deleteFiles(...)`, while authenticated server actions in `lib/actions/projects.ts` gate cleanup for explicit remove/replace helpers and submit-failure rollback.
- Task 4: keep cleanup scope narrow to deterministic provisional-file paths only (replace, explicit remove/cancel, submit failure after upload) so routine validation retries do not unexpectedly delete a still-useful uploaded screenshot.
- Task 5: keep GitHub import non-destructive by merging only into empty form fields; manual user edits always win over imported values.
- Task 5: expose `preview_image_url` alongside `image_url` in the import payload for contract clarity, while keeping the current form behavior compatible with either field.
