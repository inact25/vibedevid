# Submit Project Modernization Plan

## TL;DR
> **Summary**: Modernize `/project/submit` into a structured, resilient, multilingual submission flow that improves data quality without adding unnecessary friction or introducing a new moderation/status system.
> **Deliverables**:
> - Server-safe submit-project data flow with feature-scoped action module and schema validation
> - 4-step submit-project experience with GitHub import, upload cleanup, draft recovery, and mobile-safe UX
> - Consistent `next-intl` copy for English and Indonesian across the submit flow
> - Dedicated automated verification for auth redirect, validation, GitHub import, upload lifecycle, and successful project creation
> **Effort**: Large
> **Parallel**: YES - 3 waves
> **Critical Path**: 1 → 2 → 3 → 6 → 8 → 9 → 10 → 11/12

## Context
### Original Request
Improve the submit-project feature across feature scope, UX, and UI because the current flow feels outdated; inspect the implementation, provide suggestions, and create a work plan. Supabase MCP must be used to inspect the project database.

### Interview Summary
- Scope selected: end-to-end submit-project flow, not cosmetic-only changes.
- Database changes are allowed in principle, but only if clearly justified.
- Test strategy selected: tests-after.
- Planning default applied: keep scope on project creation flow only; do not redesign moderation/admin or broad project-domain architecture.

### Metis Review (gaps addressed)
- Locked scope to submit-project creation only to avoid turning this into a full project-domain redesign.
- Chose **no schema change by default** because current data quality is already decent (`71` projects, `5` missing tagline, `2` missing website URL, `3` missing image URL, average `2.70` tags/project).
- Explicitly included auth redirect continuity, upload cleanup, non-destructive GitHub import, and draft-recovery edge cases.
- Required a dedicated test matrix for auth, happy path, validation, import, upload failure, and recovery.

## Work Objectives
### Core Objective
Ship a modern submit-project flow that is easier to complete, harder to break, and more consistent with the repo’s current patterns while preserving the existing lean `projects` schema and immediate-publish behavior.

### Deliverables
- Refactored submit-project server logic into a project-scoped action module using schema-based validation.
- Server-fetched categories passed from the route layer instead of client-side category fetching inside the form.
- A 4-step submit flow:
  1. **Source** (manual or GitHub import)
  2. **Basics** (title, tagline, description, category)
  3. **Links & Media** (website, favicon override, tags, screenshot)
  4. **Review & Submit**
- Non-destructive GitHub import policy: import fills only empty fields, merges tags by union, never overwrites manually entered values.
- Upload lifecycle with explicit remove/replace/cancel cleanup using UploadThing file keys.
- Session-scoped draft recovery for accidental refresh/auth interruption using client storage only.
- Fully wired `projectSubmit` translations and validation/error copy for `en` and `id`.
- Dedicated automated tests for the submit flow.

### Definition of Done (verifiable conditions with commands)
- `bun tsc --noEmit` passes.
- `bun lint` passes.
- `bunx vitest run tests/unit/project-submit*.spec.ts` passes.
- `bunx playwright test tests/project-submit.spec.ts` passes.
- Anonymous visit to `/project/submit` redirects to auth with return-path preservation.
- Logged-in user can complete the 4-step flow manually and land on the new project detail page.
- GitHub import can prefill empty fields without overwriting manual values.
- Uploaded screenshot removal/cancel/submission-failure cleanup behavior is deterministic.
- All submit-page copy comes from `messages/en.json` and `messages/id.json` without hardcoded submit-flow strings.

### Must Have
- Keep slug generation auto-generated only; do not expose slug editing in the submit UI.
- Keep project creation as immediate publish; no approval/status workflow in this plan.
- Require final submit payload to contain:
  - `title` (required, sanitized)
  - `description` (required, minimum quality threshold)
  - `category` (required, must match active categories)
  - `image_url` (required by final submit, satisfied by UploadThing upload or imported preview)
  - `tags` (minimum 1, maximum 10)
  - optional `tagline`, `website_url`, `favicon_url`
- Pass `redirectTo=/project/submit` when bouncing anonymous users to auth.
- Preserve in-progress input in `sessionStorage` and clear it on successful submit or explicit discard.
- Use server-side `getUser()` for all mutation and cleanup paths.
- Use UploadThing file keys for cleanup operations; do not rely on URL-only cleanup.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- No new `projects` columns, status tables, moderation queues, or draft tables in this plan.
- No redesign of project detail pages, project list pages, dashboard management, or admin tooling.
- No broad migration of all legacy `lib/actions.ts` functions; only submit-project-related logic may be extracted.
- No destructive GitHub import overwrite flow.
- No client-side category fetching inside the submit form after the refactor.
- No CI overhaul beyond minimal submit-flow verification support if strictly needed.
- No design-system rewrite, no speculative AI-assist features, no analytics expansion.

## Verification Strategy
> ZERO HUMAN INTERVENTION — all verification is agent-executed.
- Test decision: tests-after using **Vitest** for pure schema/util logic and **Playwright** for user-visible flow.
- QA policy: Every task includes agent-executed happy-path and failure/edge scenarios.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. Shared dependencies are extracted into Wave 1.

Wave 1: route/data contract, project action extraction, schema validation, upload cleanup foundation

Wave 2: GitHub import hardening, multi-step shell, basics step, links/media/review integration

Wave 3: failure recovery polish, i18n completion, full-flow Playwright coverage, failure-mode Playwright coverage

### Dependency Matrix (full, all tasks)
| Task | Depends On | Enables |
|---|---|---|
| 1 | — | 6, 7, 8, 11 |
| 2 | — | 6, 8, 9, 11, 12 |
| 3 | 2 | 5, 6, 7, 8, 9, 11, 12 |
| 4 | — | 8, 9, 12 |
| 5 | 3 | 8, 12 |
| 6 | 1, 2, 3 | 7, 8, 9, 10, 11, 12 |
| 7 | 3, 6 | 9, 10, 11 |
| 8 | 4, 5, 6 | 9, 10, 11, 12 |
| 9 | 2, 4, 6, 7, 8 | 10, 11, 12 |
| 10 | 6, 7, 8, 9 | 11, 12 |
| 11 | 1, 3, 6, 7, 8, 9, 10 | F1-F4 |
| 12 | 4, 5, 8, 9, 10 | F1-F4 |

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 4 tasks → `quick`, `unspecified-high`
- Wave 2 → 4 tasks → `visual-engineering`, `unspecified-high`, `quick`
- Wave 3 → 4 tasks → `unspecified-high`, `writing`, `quick`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [x] 1. Move submit-page data loading and auth redirect ownership into the route layer

  **What to do**: Refactor `app/project/submit/page.tsx` so the page remains the auth gate, fetches active categories on the server, passes `categories` and `redirectTo` into the client form, and redirects anonymous users to `/user/auth?redirectTo=/project/submit` instead of dropping return intent. Keep page-level heading and surrounding layout in the route file.
  **Must NOT do**: Do not move auth checks into the client component. Do not add loading/error route files in this task. Do not redesign any non-submit route.

  **Recommended Agent Profile**:
  - Category: `quick` — Reason: one route file plus prop contract update.
  - Skills: `[]` — no extra skill required.
  - Omitted: `['visual-engineering']` — route data ownership is more architectural than visual.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [6, 7, 8, 11] | Blocked By: []

  **References**:
  - Pattern: `app/project/submit/page.tsx:6-37` — existing auth-gated route shell to preserve.
  - Pattern: `app/AGENTS.md` — route ownership, auth-required route rules.
  - API/Type: `lib/categories.ts:23-53` — current category fetch source to move to route-layer usage.
  - Test: `tests/AGENTS.md` — redirect and user-visible behavior testing guidance.

  **Acceptance Criteria**:
  - [ ] Visiting `/project/submit` anonymously redirects to auth with `redirectTo=/project/submit` preserved.
  - [ ] `SubmitProjectForm` no longer performs initial category fetch on mount.
  - [ ] Active categories are passed from route to client form as props.

  **QA Scenarios**:
  ```
  Scenario: Anonymous user is redirected with return path
    Tool: Playwright
    Steps: Visit /project/submit in a fresh browser context; inspect final URL.
    Expected: URL matches /user/auth and includes redirectTo=/project/submit.
    Evidence: .sisyphus/evidence/task-1-auth-redirect.png

  Scenario: Server-provided categories render without client bootstrap error
    Tool: Playwright
    Steps: Sign in; visit /project/submit; wait for category combobox to become interactive.
    Expected: Category select shows active options without a temporary "Loading categories..." fetch state tied to client mount.
    Evidence: .sisyphus/evidence/task-1-categories.png
  ```

  **Commit**: YES | Message: `refactor(project-submit): move route auth and category loading to page` | Files: [`app/project/submit/page.tsx`, `components/ui/submit-project-form.tsx`]

- [x] 2. Extract submit-project server logic into a feature-scoped action module

  **What to do**: Move submit-project-specific logic out of `lib/actions.ts` into a new feature-scoped module under `lib/actions/projects.ts` (or equivalent project-scoped file already aligned with repo patterns). Keep exported response shape consistent as `{ success: boolean, slug?: string, error?: string }`. Update imports so the form consumes the extracted action module. Add `revalidatePath('/project/list')` and `revalidatePath('/project/[slug]')`-equivalent invalidation strategy appropriate for created project pages.
  **Must NOT do**: Do not migrate unrelated actions from `lib/actions.ts`. Do not change behavior of edit, likes, comments, auth, or admin actions in this task.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: action extraction touches server-action boundaries and cache invalidation.
  - Skills: `[]` — repository guidance is sufficient.
  - Omitted: `['quick']` — extraction + revalidation is larger than a trivial move.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [6, 8, 9, 11, 12] | Blocked By: []

  **References**:
  - Pattern: `lib/actions/comments.ts:1-194` — feature-scoped server action module structure.
  - Pattern: `lib/AGENTS.md` — server action rules, response contract, revalidation expectations.
  - API/Type: `lib/actions.ts:765-884` — current `submitProject` behavior to preserve then improve.
  - Test: `tests/unit/blog-actions.spec.ts` — existing unit-test style baseline.

  **Acceptance Criteria**:
  - [ ] `submitProject` no longer lives in the legacy monolithic section of `lib/actions.ts`.
  - [ ] Client imports point to the new feature-scoped module.
  - [ ] Created project mutations trigger explicit cache invalidation.

  **QA Scenarios**:
  ```
  Scenario: Successful create still returns slug contract from new module
    Tool: Vitest
    Steps: Call the extracted action with valid mocked FormData and authenticated context helpers.
    Expected: Result matches { success: true, slug: <non-empty string> }.
    Evidence: .sisyphus/evidence/task-2-action-contract.txt

  Scenario: Failed insert returns structured error without throwing
    Tool: Vitest
    Steps: Mock Supabase insert failure and invoke submitProject.
    Expected: Result matches { success: false, error: <message> } and no uncaught exception escapes.
    Evidence: .sisyphus/evidence/task-2-action-error.txt
  ```

  **Commit**: YES | Message: `refactor(project-submit): extract submit action into project module` | Files: [`lib/actions.ts`, `lib/actions/projects.ts`, `components/ui/submit-project-form.tsx`]

- [x] 3. Add schema-based validation and normalized submit payload rules

  **What to do**: Introduce a `zod` schema for project submission input and a small normalizer used by both submit flow and future adjacent project form reuse. Validate title, tagline, description length, website URL format, category membership, tags array length/content, and image URL presence at final submit time. Return field-aware, user-safe errors. Normalize tags to trimmed lowercase unique values and reject empty/whitespace-only tags. Keep category validation tied to active database categories, not a hardcoded array.
  **Must NOT do**: Do not introduce new required database columns. Do not reuse ad hoc string parsing in multiple places after the schema exists.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: validation contract impacts server action, UI, and tests.
  - Skills: `[]` — native `zod` is already in repo.
  - Omitted: `['writing']` — this is executable validation logic, not documentation.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [5, 6, 7, 8, 9, 11, 12] | Blocked By: [2]

  **References**:
  - Pattern: `lib/AGENTS.md` — recommends Zod for server action validation.
  - API/Type: `package.json:83-97` — `zod` and `vitest` already available.
  - Source: `lib/actions.ts:769-803` — current inline validation to replace.
  - Source: `lib/categories.ts:87-93` — existing category validity helper pattern.

  **Acceptance Criteria**:
  - [ ] All submit payload validation runs through a shared schema/normalizer path.
  - [ ] Final submit requires a valid image URL, at least 1 tag, and a category present in active categories.
  - [ ] Validation errors are field-specific enough for the client UI to map them.

  **QA Scenarios**:
  ```
  Scenario: Valid payload is normalized consistently
    Tool: Vitest
    Steps: Pass FormData with mixed-case duplicate tags, padded strings, and a valid URL/image/category.
    Expected: Parsed output trims strings, lowercases/de-duplicates tags, and preserves safe values.
    Evidence: .sisyphus/evidence/task-3-validate-valid.txt

  Scenario: Invalid payload is rejected with actionable errors
    Tool: Vitest
    Steps: Submit empty title, invalid website URL, missing image URL, and invalid category.
    Expected: Schema returns explicit field failures for title, website_url, image_url, and category.
    Evidence: .sisyphus/evidence/task-3-validate-invalid.txt
  ```

  **Commit**: YES | Message: `feat(project-submit): add validated submission schema` | Files: [`lib/actions/projects.ts`, `lib/categories.ts`, `tests/unit/project-submit-schema.spec.ts`]

- [x] 4. Add UploadThing file-key tracking and server-side cleanup helpers

  **What to do**: Update `lib/uploadthing.ts` and the submit flow contract so upload completion returns both public URL and file key in a stable shape consumed by the form. Add server-side helper(s) using UploadThing deletion support to remove provisional files on cancel, replace, or submit failure. Store file key client-side only for the in-progress session; do not persist it to Supabase in this plan. Ensure cleanup helpers are only called from authenticated server paths.
  **Must NOT do**: Do not build a background orphan sweeper job in this plan. Do not add new DB columns for upload bookkeeping.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: file lifecycle changes span uploader contract and server cleanup.
  - Skills: `[]` — official UploadThing guidance already researched.
  - Omitted: `['visual-engineering']` — this task is behavioral/infrastructure.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [8, 9, 12] | Blocked By: []

  **References**:
  - Pattern: `lib/uploadthing.ts:26-84` — current uploader contract.
  - Pattern: `app/api/uploadthing/route.ts:1-17` — current App Router wiring.
  - External: `https://docs.uploadthing.com/api-reference/ut-api#delete-files` — authoritative deletion support.
  - External: `https://docs.uploadthing.com/getting-started/appdir` — App Router integration pattern.

  **Acceptance Criteria**:
  - [ ] Upload completion returns stable `url` + `key` data used by the submit form.
  - [ ] Replacing or removing an uploaded screenshot invokes deterministic cleanup for the previous provisional file.
  - [ ] Submit failure after successful upload triggers cleanup for the provisional file key.

  **QA Scenarios**:
  ```
  Scenario: Replace-image flow cleans up the previous provisional upload
    Tool: Vitest
    Steps: Mock two upload completions and trigger the replace/remove handler path with delete helper spies.
    Expected: Previous file key is deleted exactly once before the new file becomes active.
    Evidence: .sisyphus/evidence/task-4-replace-cleanup.txt

  Scenario: Submit failure triggers provisional file cleanup
    Tool: Vitest
    Steps: Mock successful upload metadata followed by Supabase insert failure during final submit.
    Expected: Cleanup helper runs with the active provisional file key and the action returns a structured error.
    Evidence: .sisyphus/evidence/task-4-submit-failure-cleanup.txt
  ```

  **Commit**: YES | Message: `feat(project-submit): add provisional upload cleanup handling` | Files: [`lib/uploadthing.ts`, `lib/actions/projects.ts`, `app/api/uploadthing/route.ts`, `tests/unit/project-submit-upload.spec.ts`]

- [x] 5. Harden the GitHub import API contract for safe prefill behavior

  **What to do**: Keep `app/api/github-import/route.ts` as the import source, but formalize its output contract for the new form: title, tagline, description, website URL, preview image URL, favicon URL, tags, and repo metadata. Add server-side output normalization and explicit fallback behavior when README parsing or external GitHub fields are missing. Enforce the UI rule that imported data only fills empty fields unless the user explicitly chooses to replace a single field at review time. Preserve manual edits after import.
  **Must NOT do**: Do not require GitHub import for submission. Do not add repo URL storage to the database in this plan.

  **Recommended Agent Profile**:
  - Category: `quick` — Reason: API contract hardening with bounded scope.
  - Skills: `[]` — existing route is already feature-contained.
  - Omitted: `['deep']` — no external redesign beyond safe normalization.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [8, 12] | Blocked By: [3]

  **References**:
  - Pattern: `app/api/github-import/route.ts:61-184` — current import route behavior.
  - Source: `components/ui/submit-project-form.tsx:194-247` — current client import behavior that overwrites values.
  - API/Type: `app/api/github-import/route.ts:3-59` — current route helpers and output fields.

  **Acceptance Criteria**:
  - [ ] Import response is normalized and stable even when optional GitHub fields are missing.
  - [ ] Imported data does not silently overwrite manually entered fields.
  - [ ] Import errors do not clear existing form state.

  **QA Scenarios**:
  ```
  Scenario: Import fills only empty fields and preserves manual edits
    Tool: Playwright
    Steps: Enter a manual title/tagline; trigger GitHub import with a valid repo; continue through the form.
    Expected: Existing manual title/tagline remain unchanged while empty fields are populated from import.
    Evidence: .sisyphus/evidence/task-5-import-preserve.png

  Scenario: Import failure keeps current draft intact
    Tool: Playwright
    Steps: Fill several fields; enter an invalid or 404 repo; trigger import.
    Expected: Error message appears and all previously typed values remain present.
    Evidence: .sisyphus/evidence/task-5-import-error.png
  ```

  **Commit**: YES | Message: `feat(project-submit): harden github import prefill behavior` | Files: [`app/api/github-import/route.ts`, `components/ui/submit-project-form.tsx`, `tests/project-submit.spec.ts`]

- [x] 6. Replace the monolithic form with a 4-step submit-project shell

  **What to do**: Rebuild `components/ui/submit-project-form.tsx` around a stepper/wizard shell with four named steps: Source, Basics, Links & Media, Review & Submit. Use a single controlled form state object, keep Back/Next navigation explicit, block progression when the current step has validation errors, and preserve values across steps. Provide a mobile-safe sticky footer for primary actions. Keep the overall page width constrained and avoid redesigning the surrounding page chrome.
  **Must NOT do**: Do not split each step into over-abstracted microcomponents unless reuse is obvious inside this flow. Do not introduce a third-party form framework migration.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` — Reason: this is the core UX/UI modernization task.
  - Skills: `[]` — repo component guidance is sufficient.
  - Omitted: `['quick']` — too much interactive restructuring.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [7, 8, 9, 10, 11, 12] | Blocked By: [1, 2, 3]

  **References**:
  - Pattern: `components/ui/submit-project-form.tsx:160-644` — current monolithic form to replace.
  - Pattern: `components/event/cover-image-uploader.tsx:51-248` — current polished upload section UX.
  - Pattern: `components/project/ProjectEditClient.tsx:135-401` — current project field ordering and editing expectations.
  - Pattern: `components/AGENTS.md` — `use client`, auth-aware prop passing, and i18n usage rules.

  **Acceptance Criteria**:
  - [ ] Submit-project UI is divided into exactly 4 steps with visible progress indication.
  - [ ] Next/Back navigation preserves entered values.
  - [ ] Users cannot advance past a step with blocking validation errors.
  - [ ] Mobile viewport keeps step actions accessible without hidden CTA issues.

  **QA Scenarios**:
  ```
  Scenario: Multi-step happy path preserves values through navigation
    Tool: Playwright
    Steps: Sign in; fill step 1 and 2; move forward to step 3; go back to step 2; return to step 3.
    Expected: All previously entered values remain intact and current step indicator updates correctly.
    Evidence: .sisyphus/evidence/task-6-stepper-happy.png

  Scenario: Step progression is blocked by validation
    Tool: Playwright
    Steps: Attempt to advance from Basics with empty required fields.
    Expected: Stay on the current step; field-level errors are visible; Next remains blocked until fixed.
    Evidence: .sisyphus/evidence/task-6-stepper-validation.png
  ```

  **Commit**: YES | Message: `feat(project-submit): add multi-step submit flow shell` | Files: [`components/ui/submit-project-form.tsx`]

- [x] 7. Implement Basics-step guidance and data-quality UX

  **What to do**: Modernize the Basics step to guide title, tagline, description, and category selection with field-specific helper text, live counters, clear required-state messaging, and category descriptions where available. Make description quality explicit: minimum meaningful length threshold, max length, and visible progress. Use server-provided categories and ensure invalid/stale category selections are rejected gracefully if categories change mid-session.
  **Must NOT do**: Do not add new database fields for product metadata. Do not turn description guidance into AI-generated text suggestions.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` — Reason: user guidance and clarity improvements are primarily UX/UI.
  - Skills: `[]` — no extra skills needed.
  - Omitted: `['deep']` — localized field guidance is not architecture-heavy.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [9, 10, 11] | Blocked By: [3, 6]

  **References**:
  - Source: `components/ui/submit-project-form.tsx:265-384` — current Basics-field structure.
  - Source: `components/project/ProjectEditClient.tsx:155-271` — adjacent project field patterns.
  - API/Type: `lib/categories.ts:3-12` — category metadata available for richer presentation.

  **Acceptance Criteria**:
  - [ ] Basics step shows title, tagline, description, and category in a guided, low-clutter layout.
  - [ ] Description counter reflects min/max guidance and error state clearly.
  - [ ] Stale or invalid category values cannot proceed to review/submit.

  **QA Scenarios**:
  ```
  Scenario: Basics step gives clear data-quality guidance
    Tool: Playwright
    Steps: Enter a too-short description, then extend it past the minimum and near the max.
    Expected: UI transitions from error to valid guidance; counter reflects current count accurately.
    Evidence: .sisyphus/evidence/task-7-description-guidance.png

  Scenario: Invalid category selection is rejected before review
    Tool: Vitest
    Steps: Submit a payload containing a category value not present in active categories.
    Expected: Validation fails with category-specific error and no DB insert occurs.
    Evidence: .sisyphus/evidence/task-7-invalid-category.txt
  ```

  **Commit**: YES | Message: `feat(project-submit): improve basics step guidance and validation` | Files: [`components/ui/submit-project-form.tsx`, `lib/actions/projects.ts`, `tests/unit/project-submit-schema.spec.ts`]

- [x] 8. Implement Links & Media step with explicit upload/import state management

  **What to do**: Build the Links & Media step around website URL, favicon override, tags, and screenshot management. Make screenshot required for final submit but not required before the user reaches review. Show preview, replace, remove, upload progress, and imported-preview state clearly. Keep favicon auto-derivation from website URL but allow manual override. Add a clear distinction between imported image preview and uploaded local screenshot, with uploaded local screenshot winning if both exist.
  **Must NOT do**: Do not accept more than one screenshot in this plan. Do not introduce gallery/carousel functionality.

  **Recommended Agent Profile**:
  - Category: `visual-engineering` — Reason: mixed behavioral and UX state management in an interactive media step.
  - Skills: `[]` — existing uploader patterns are enough.
  - Omitted: `['writing']` — copy is secondary here.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [9, 10, 11, 12] | Blocked By: [4, 5, 6]

  **References**:
  - Pattern: `components/event/cover-image-uploader.tsx:21-248` — upload vs URL mode and preview affordances.
  - Source: `components/ui/submit-project-form.tsx:386-639` — current website/favicon/tags/upload implementation.
  - Source: `lib/uploadthing.ts:26-53` — project uploader contract.
  - External: `https://docs.uploadthing.com/api-reference/ut-api#delete-files` — cleanup path for provisional uploads.

  **Acceptance Criteria**:
  - [ ] Links & Media step explicitly shows current media source and active screenshot state.
  - [ ] Replace/remove/cancel behaviors keep `image_url` and upload key state in sync.
  - [ ] Final review blocks submission if no valid screenshot is present.

  **QA Scenarios**:
  ```
  Scenario: Uploaded screenshot overrides imported preview during review
    Tool: Playwright
    Steps: Import a repo with preview image; upload a local screenshot afterward; continue to review.
    Expected: Review shows the uploaded screenshot as the active image and retains imported non-image fields.
    Evidence: .sisyphus/evidence/task-8-upload-overrides-import.png

  Scenario: Removing active screenshot blocks final submit
    Tool: Playwright
    Steps: Reach review with a valid screenshot, remove it from Links & Media, return to review, attempt submit.
    Expected: Submission is blocked and a screenshot-required message is shown.
    Evidence: .sisyphus/evidence/task-8-screenshot-required.png
  ```

  **Commit**: YES | Message: `feat(project-submit): improve links and media step behavior` | Files: [`components/ui/submit-project-form.tsx`, `lib/uploadthing.ts`, `lib/actions/projects.ts`, `tests/project-submit.spec.ts`]

- [ ] 9. Add review step, submit orchestration, and session-scoped draft recovery

  **What to do**: Add a final Review & Submit step that summarizes all values before submission, surfaces missing/invalid sections with direct jump-back actions, and orchestrates final submit through the validated action. Persist in-progress state to `sessionStorage` on step changes and meaningful field edits. Restore draft state on reload with a dismissible recovery notice. Clear draft state on successful submit and explicit discard. Handle expired auth gracefully by preserving draft and redirecting to auth.
  **Must NOT do**: Do not persist drafts to Supabase or create a draft table. Do not autosave on every keystroke with aggressive writes; debounce client storage updates.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: orchestration spans UX, auth failure handling, and storage lifecycle.
  - Skills: `[]` — built-in browser storage patterns suffice.
  - Omitted: `['quick']` — recovery/orchestration is more than a simple UI patch.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [10, 11, 12] | Blocked By: [2, 4, 6, 7, 8]

  **References**:
  - Source: `components/ui/submit-project-form.tsx:119-158` — current submit orchestration to replace.
  - Pattern: `app/project/submit/page.tsx:6-14` — route-level auth entry that must pair with recovery redirect.
  - Pattern: `tests/event-auth-submit.spec.ts:23-84` — auth continuity expectations in adjacent submit flow.

  **Acceptance Criteria**:
  - [ ] Review step summarizes all sections and supports direct correction navigation.
  - [ ] Session refresh restores in-progress draft state with explicit user notice.
  - [ ] Successful submit clears draft state and redirects to `/project/{slug}`.
  - [ ] Auth-expiry failure preserves draft state and returns the user to submit after re-auth.

  **QA Scenarios**:
  ```
  Scenario: Refresh restores draft state
    Tool: Playwright
    Steps: Fill multiple steps; reload the page; accept draft recovery prompt.
    Expected: Step state and entered values are restored into the wizard.
    Evidence: .sisyphus/evidence/task-9-draft-restore.png

  Scenario: Auth interruption preserves draft and recoverability
    Tool: Playwright
    Steps: Fill flow as an authenticated user; expire session or clear auth before final submit; attempt submit; sign in again.
    Expected: User is redirected to auth, then back to submit with prior draft recoverable.
    Evidence: .sisyphus/evidence/task-9-auth-recovery.png
  ```

  **Commit**: YES | Message: `feat(project-submit): add review step and draft recovery` | Files: [`components/ui/submit-project-form.tsx`, `app/project/submit/page.tsx`, `tests/project-submit.spec.ts`]

- [ ] 10. Align submit-project copy and i18n behavior across English and Indonesian

  **What to do**: Replace all remaining hardcoded submit-flow strings in `components/ui/submit-project-form.tsx` with `useTranslations('projectSubmit')` keys. Keep `messages/en.json` and `messages/id.json` structurally identical and update the copy to a consistent product tone: concise, supportive, and modern, with Indonesian copy using the repo’s informal-but-professional style. Add keys for step labels, validation messages, recovery notice, import conflict hints, upload cleanup messages, and review summaries.
  **Must NOT do**: Do not use custom translation wrapper hooks. Do not update unrelated sections outside the submit-project namespace.

  **Recommended Agent Profile**:
  - Category: `writing` — Reason: this task is primarily structured copy and i18n completeness.
  - Skills: `[]` — next-intl repo conventions are already documented.
  - Omitted: `['visual-engineering']` — this is content consistency, not layout architecture.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [11, 12] | Blocked By: [6, 7, 8, 9]

  **References**:
  - Pattern: `app/project/submit/page.tsx:17-29` — existing `useTranslations('projectSubmit')` namespace entry.
  - Source: `messages/en.json:205-252` — current namespace structure to extend.
  - Source: `messages/id.json:205-252` — Indonesian namespace structure to keep identical.
  - Guidance: `components/AGENTS.md` — direct `useTranslations`, update both locale files together.

  **Acceptance Criteria**:
  - [ ] Submit form contains no hardcoded UI strings specific to submit-project flow.
  - [ ] `messages/en.json` and `messages/id.json` expose identical `projectSubmit` key structure.
  - [ ] Recovery, validation, import, upload, and review messaging all resolve through i18n.

  **QA Scenarios**:
  ```
  Scenario: English locale renders full submit flow without missing keys
    Tool: Playwright
    Steps: Open the submit flow in English locale and navigate all steps.
    Expected: No raw translation keys, undefined strings, or fallback artifacts are visible.
    Evidence: .sisyphus/evidence/task-10-en-i18n.png

  Scenario: Indonesian locale renders matching submit flow structure
    Tool: Playwright
    Steps: Open the submit flow in Indonesian locale and navigate all steps.
    Expected: All step labels, helper text, and toasts render in Indonesian with no missing-key artifacts.
    Evidence: .sisyphus/evidence/task-10-id-i18n.png
  ```

  **Commit**: YES | Message: `docs(i18n): align submit project copy across locales` | Files: [`components/ui/submit-project-form.tsx`, `messages/en.json`, `messages/id.json`]

- [ ] 11. Add dedicated happy-path and auth/validation Playwright coverage for submit-project

  **What to do**: Create `tests/project-submit.spec.ts` as the canonical end-to-end suite for this flow. Cover anonymous redirect, authenticated manual submit, step validation blocking, successful redirect to slug-based project page, and draft restoration after refresh. Prefer accessible selectors and add `data-testid` only where roles/labels are insufficient. Reuse the repo’s auth helper style, but remove hardcoded assumptions that new project URLs are numeric IDs.
  **Must NOT do**: Do not keep project submit coverage buried only inside `tests/views-tracking.spec.ts`. Do not rely on brittle CSS selectors.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: this is a primary regression suite for a critical user flow.
  - Skills: `[]` — Playwright patterns already exist in repo.
  - Omitted: `['quick']` — multiple scenarios and selector hardening required.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [F1-F4] | Blocked By: [1, 3, 6, 7, 8, 9, 10]

  **References**:
  - Pattern: `tests/event-auth-submit.spec.ts:6-84` — adjacent authenticated submit-flow pattern.
  - Pattern: `tests/AGENTS.md` — user-visible behavior, accessible selectors, cleanup expectations.
  - Pattern: `playwright.config.ts:14-86` — current Playwright environment and base URL assumptions.
  - Source: `tests/views-tracking.spec.ts:204-235` — outdated project submit assumptions to remove from future reliance.

  **Acceptance Criteria**:
  - [ ] `tests/project-submit.spec.ts` exists and covers auth redirect, manual happy path, validation blocking, and draft recovery.
  - [ ] New-project redirect assertions target slug URLs, not numeric IDs.
  - [ ] Submit-flow tests use accessible selectors and stable test ids only where necessary.

  **QA Scenarios**:
  ```
  Scenario: Dedicated submit-project suite passes for happy path
    Tool: Playwright
    Steps: Run bunx playwright test tests/project-submit.spec.ts -g "creates project with valid manual input".
    Expected: Test passes, creates a project, and lands on /project/<slug> with expected persisted values.
    Evidence: .sisyphus/evidence/task-11-happy.txt

  Scenario: Dedicated submit-project suite passes for auth redirect and blocked progression
    Tool: Playwright
    Steps: Run bunx playwright test tests/project-submit.spec.ts -g "redirects anonymous users|blocks next step on missing required fields".
    Expected: Anonymous redirect and validation-blocking scenarios both pass.
    Evidence: .sisyphus/evidence/task-11-auth-validation.txt
  ```

  **Commit**: YES | Message: `test(project-submit): add dedicated submit flow coverage` | Files: [`tests/project-submit.spec.ts`, `components/ui/submit-project-form.tsx`]

- [ ] 12. Add failure-mode coverage for GitHub import and upload lifecycle

  **What to do**: Extend automated coverage to verify import failure resilience, non-destructive import merge behavior, screenshot remove/replace behavior, and submit-failure cleanup path. Use Playwright for visible behavior and Vitest for internal cleanup helper guarantees where browser-level verification is too indirect. Document any required test fixtures or env assumptions inline in the test files.
  **Must NOT do**: Do not leave upload cleanup behavior unverified. Do not rely exclusively on manual inspection for failure cases.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` — Reason: failure-mode regression coverage spans both E2E and unit layers.
  - Skills: `[]` — no extra skills needed.
  - Omitted: `['writing']` — test behavior matters more than docs text.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [F1-F4] | Blocked By: [2, 4, 5, 8, 9, 10]

  **References**:
  - Pattern: `app/api/github-import/route.ts:61-184` — import behaviors to simulate.
  - Pattern: `lib/uploadthing.ts:26-53` — upload metadata returned to the client.
  - Pattern: `components/ui/submit-project-form.tsx:516-582` — current upload lifecycle error handling to replace and verify.
  - External: `https://docs.uploadthing.com/api-reference/ut-api#delete-files` — cleanup behavior being implemented.

  **Acceptance Criteria**:
  - [ ] Failure-mode suite verifies that import errors preserve manual draft values.
  - [ ] Replace/remove image paths are tested.
  - [ ] Submit failure after upload is covered at least once with cleanup assertion.

  **QA Scenarios**:
  ```
  Scenario: GitHub import failure preserves current manual data
    Tool: Playwright
    Steps: Run bunx playwright test tests/project-submit.spec.ts -g "keeps manual data when github import fails".
    Expected: Failure toast/message appears and all manual fields remain unchanged.
    Evidence: .sisyphus/evidence/task-12-import-failure.txt

  Scenario: Provisional upload cleanup is verified after submit failure
    Tool: Vitest
    Steps: Run bunx vitest run tests/unit/project-submit-upload.spec.ts.
    Expected: Cleanup helper assertions pass for remove/replace/submit-failure paths.
    Evidence: .sisyphus/evidence/task-12-upload-cleanup.txt
  ```

  **Commit**: YES | Message: `test(project-submit): cover import and upload failure paths` | Files: [`tests/project-submit.spec.ts`, `tests/unit/project-submit-upload.spec.ts`, `tests/unit/project-submit-schema.spec.ts`]

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [ ] F1. Plan Compliance Audit — oracle
- [ ] F2. Code Quality Review — unspecified-high
- [ ] F3. Real Manual QA — unspecified-high (+ playwright if UI)
- [ ] F4. Scope Fidelity Check — deep

## Commit Strategy
- Commit 1: `refactor(project-submit): move submit flow onto feature module`
- Commit 2: `feat(project-submit): add validated multi-step submission flow`
- Commit 3: `feat(project-submit): harden import and upload recovery`
- Commit 4: `docs(i18n): align submit project copy across locales`
- Commit 5: `test(project-submit): cover auth validation import and upload flows`

## Success Criteria
- The submit flow feels materially more modern because users progress through focused steps instead of one long screen.
- Submission quality improves through schema validation and better guided fields without adding database complexity.
- The flow is resilient to auth interruption, refreshes, upload issues, and GitHub import failures.
- The implementation aligns with repo conventions for server actions, i18n, auth, and testing.
