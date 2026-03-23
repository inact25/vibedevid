# ADMIN-KIT SUBPROJECT GUIDE

## OVERVIEW

`admin-kit/` is a separate Next.js 15 package. It does **not** follow the root Bun + Biome workflow; it uses pnpm, ESLint, Prettier, Tailwind v4, and its own `src/`-scoped aliasing.

## COMMANDS

```bash
pnpm install
pnpm run dev
pnpm run build
pnpm run lint
pnpm run format
pnpm run format:fix
pnpm run lint:fix
```

## WHERE TO LOOK

- package/tooling: `package.json`, `eslint.config.mjs`, `.prettierrc`, `tsconfig.json`, `next.config.ts`
- route tree: `src/app/*`
- local UI layer: `src/components/ui/*`
- local dashboard chrome: `src/components/layout/*`

## CONVENTIONS

- Use pnpm in this subtree.
- Use ESLint + Prettier here; root Biome rules do not apply.
- Respect the local alias mapping `@/* -> ./src/*`.
- Keep `admin-kit` components isolated from root `components/` and `components/ui/`.
- This package ships with template/demo-style data and layouts; verify real integrations before connecting it to production systems.

## ANTI-PATTERNS

- Do not import root app components into this package.
- Do not assume root commands, root lockfile rules, or Bun-specific workflows apply here.
- Do not mix the root UI layer with `admin-kit/src/components/ui/*`.
