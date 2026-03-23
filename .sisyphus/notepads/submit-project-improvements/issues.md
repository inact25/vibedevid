# Issues

- `app/project/submit/page.tsx` was calling `getCategories()` from `lib/categories.ts`, but that helper used the browser Supabase client. The submit route now loads categories with the server client so the route fetch is actually server-safe.
- A later retry introduced an import-trace regression by making `lib/categories.ts` pull in `next/headers` through the server Supabase client. The final fix keeps `lib/categories.ts` client-safe and moves the submit-page category query directly into the route.
- Vitest in this repo does not currently resolve the `@/` alias by default, so the Task 2 unit test uses relative imports for the action and mocked modules to keep the targeted spec runnable without broad test-config work.
- Repo-level lint/typecheck commands still pick up unrelated generated/temp workspace content under `%TEMP%` and docs bundles, so task verification used direct file-scoped Biome + LSP checks instead of broad project-wide config work.
- Playwright browser binaries were initially missing locally; `bunx playwright install chromium` was required before the new submit/import spec could run.

### Task 6: 4-Step Form Stepper Caveats
- Playwright auth flow (`/user/auth` navigation using `TEST_EMAIL`) currently fails in our local automated run due to DB/seed mismatch (returns to login), but the test logic itself correctly navigates the stepper using `getByRole('button', { name: 'Next' })` and successfully tests value preservation between steps.
- Currently `category` doesn't display the full object data (only its `name` string value) until step 3, so its display name lookup assumes `categories` prop contains the value.

### Test Concurrency Issues with Auth
Running Playwright tests concurrently using a single local test user account (`signIn` helper) led to unpredictable redirect failures and timeouts (`http://localhost:3000/user/auth` not redirecting). Using `test.describe.serial` enforces sequential execution and prevents auth token race conditions in the local environment.

### Task 7: Basics-Step Guidance Caveats
- When enforcing text limits, HTML `<textarea>`/`<input>` handle `maxLength` natively, but driving dynamic warnings (amber/red text colors) and character counts required explicitly tracking the lengths via React state over relying solely on DOM validation.
- Handling stale categories mid-session requires explicitly checking the client state value against the live `categories` array prop during `validateCurrentStep` to guarantee the chosen value is still valid before allowing the user to proceed.
- The path alias `@/` was breaking Vitest for `lib/uploadthing.ts` because it relied on `lib/supabase/server`, requiring a relative path fallback to avoid deeper test tooling changes.

### Task 8: Upload/Import State Management Fix
- The initial UI implementation for removing a provisional uploaded image conditionally cleared the UI state based on the success of the backend cleanup API. If the cleanup failed (e.g. in development/test environments or due to network flakiness), the UI would become stuck with a stale `uploadedImageKey` state, preventing subsequent submissions or replacements. We fixed this by ensuring `setUploadedImageUrl('')` and `setUploadedImageKey('')` are called regardless of the cleanup function's return status.
- Added `data-testid="review-image-badge"` to reliably test the final active state badge during Playwright tests because `getByText('Imported')` hit multiple elements (e.g., the success toast and the replace text).
