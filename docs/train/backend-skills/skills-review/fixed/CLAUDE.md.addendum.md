# CLAUDE.md addendum — apply these two edits to the repo's CLAUDE.md

This file is not a replacement for CLAUDE.md — it contains two localized insertions.

---

## Edit 1 — after the last bullet of the "Entity Conventions" section
## (the bullet that starts "**`@Index(...)` must always be given an explicit name...")

INSERT the following new section:

```md
## Module-Local Types (`types/`)

Every module folder may contain a `types/` subdirectory holding `*.types.ts` files for
module-local interfaces, type aliases, and composed/computed return shapes (an entity joined
with a computed field, a list-item shape, a method return type that isn't just an entity or
DTO). The rule is **no inline `interface`/`type` declarations at the top of a `.service.ts`
or `.controller.ts`** — they live in `types/<feature>.types.ts` and are imported.

This is not "new modules only": existing services with inline types (e.g.
`orders.service.ts`, `products.service.ts`, `reviews.service.ts`) move them into `types/`
opportunistically under a boy-scout rule — the next time that file is touched for any reason,
its inline types move with it (or get a `// TODO(types)` marker if the diff must stay small).
No big-bang sweep.

Cross-boundary shapes the frontend also consumes come from `@manooch/types` instead; the
module-local `types/` folder is for shapes internal to this backend module or projections of
entities that aren't shared upstream. See `guard-nestjs-module`.
```

---

## Edit 1b — append to the Stack/database bullet about migrations
## (the long paragraph starting "Database: PostgreSQL 16 via TypeORM...")

APPEND the following to the end of that paragraph (after the "Any future entity column change
must ship a migration..." sentence):

```md
Any entity column change must additionally follow "Production migration safety" in
`skill-db-architect`: confirm the target environment's `migrations` table is baselined,
quote the emitted SQL in the PR, run a post-deploy `information_schema` assertion and a
read smoke-test before routing traffic, and add a boot-time column assertion so a missing
column fails the deploy instead of 500ing on first read. This rule exists because of two
incidents — the payment-links `durationDays` drift (no `migrations` table on prod plus a
wrong runbook container/role) and the later "stuck feature" in the same root-cause class —
both of which deployed green and then 500'd on prod.
```

---

## Edit 2 — in the "Modules (`src/modules/`)" intro paragraph
## (the paragraph that starts "41 modules, grouped by concern...")

APPEND this sentence to the end of that intro paragraph (before the "Core commerce" table):

```md
A module may contain more than one `*.service.ts` when the service is large enough to warrant
internal collaborators behind a single public facade (e.g. `orders-query.service.ts` consumed
only by `orders.service.ts`). Don't assume one service file per module — see
`skill-transaction-engine` "Service decomposition" for the triggers and pattern.
```
