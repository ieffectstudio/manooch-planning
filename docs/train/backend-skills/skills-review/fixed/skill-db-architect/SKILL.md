---
name: skill-db-architect
description: Use when creating or refining TypeORM entities, migrations, or shared-type enums in manooch-backend — columns, decimal transformers, jsonb settings/selectedAttributes, relations, @Index generation, soft delete, deciding entity-vs-static-.data.ts reference data, or importing an enum from @manooch/types.
---

# Skill: Database Architect

You specialize in TypeORM **entity definitions**, migrations, and data-persistence shape. Dispatched
by `guard-nestjs-module`. (Service-layer transactions and N+1 live in `skill-transaction-engine`;
controllers/DTOs in `skill-api-gateway`.)

> **Graphify first:** if `graphify-out/graph.json` exists, run `graphify query "<module>"`
> before grepping/reading source. Pass this instruction to any subagent.

## Entity Conventions (TypeORM)
- **Relations:** TypeORM relation decorators (`@ManyToOne`, `@OneToMany`, `@JoinColumn`, etc.) are allowed — use them when they make the model clearer.
- **Plain FKs:** Simple `@Column()` primitives for cross-domain foreign keys are also fine when you don't need the relation loaded.
- **Decimal Prices:** Use a custom transformer to preserve float precision:
  ```ts
  @Column({ type: 'decimal', transformer: { to: (v) => v, from: (v) => parseFloat(v) } })
  price: number;
  ```
- **JSONB Fields:** Use `type: 'jsonb'` for settings and selectedAttributes columns.
- **Indexing:** Any column targeted by filter, sort, or foreign-key operations must carry `@Index()` in the entity file — and **every `@Index()` must be given an explicit name as its first argument**, e.g. `@Index('IDX_orders_store_created', ['storeId', 'createdAt'])`. Never write the bare/decorator form. An unnamed index gets a deterministic hash from `synchronize` that no hand-written migration will ever match by coincidence; that mismatch is exactly what caused the 2026-08-07 index-name drift (11 indexes existed on prod only under hashed names while migrations referenced literal names — see migration `RenameDriftedIndexNames1786100000000` and CLAUDE.md "Entity Conventions"). The query-side rationale for *which* columns to index lives in `skill-transaction-engine` §N+1. Composite index column order: equality-filter column first, then the sort/range column.

## Static reference data (no DB table needed)
For fixed reference datasets that don't change at runtime (e.g. truly static lookup lists), skip the
entity/migration entirely — bundle a plain `<domain>.data.ts` array (`{ id, name, ...}[]`), serve it
via a thin `<domain>.service.ts` (`Array.find`/`filter`, `NotFoundException` for unknown ids) behind a
**public, unguarded** controller.

(Pattern reference: this is how the old `geo/` module worked before it was replaced by the DB-backed
`locations` module; use the same thin-service + public-controller shape when a dataset truly never
changes at runtime, but reach for a DB-backed module like `locations` when it needs admin CRUD —
see `src/modules/locations/` for the current implementation, not `geo/`.)

## Migrations

`src/migrations/` is authored for **production only**. Dev runs with `synchronize: true`
(`NODE_ENV !== 'production'`), so the dev DB's migrations table stays empty and
`npm run migration:run` is **not runnable locally** — don't try to "fix" a dev DB by running it.
Workflow: `npm run migration:generate` (uses `src/config/data-source.ts`), review the generated SQL,
commit it alongside the entity change — never hand-write a migration to match an entity you haven't
actually changed.

### Production migration safety

This section exists because two production deploys shipped green and then 500'd:
the **payment-links `durationDays`** column (prod had no `migrations` table at all — schema had
been built by `synchronize` before it was disabled — so the column was never applied; the fix
script's runbook also used a wrong container name `manooch-backend-db-1` and wrong role
`postgres` vs. the real `manooch-postgres` / `manooch`, which is why the incident recurred after
its first "fix"), and a **"stuck feature"** in the same root-cause class — migration reported
success during deploy, but a field change did not actually take effect on the prod schema, and
the first request to touch the entity 500'd. Treat every entity column change as if it can cause
that class of outage, and follow these rules:

1. **Every entity column change ships a migration in the same PR** — add, drop, rename, type
   change, nullability change, default change. No "we'll rely on synchronize on prod" and no
   "it's nullable, ship the entity first". The migration, the entity change, and the baseline
   check are one atomic change.
2. **Do not rely on a migration you cannot prove ran.** Before merging a migration that adds a
   required physical object, confirm the target environment's `migrations` table exists and is
   baselined. For a new/reset environment, run `src/scripts/baseline-prod-migrations.sql` (or
   its env-specific equivalent) first — this is the step that was missing in the payment-links
   incident.
3. **Runbook commands in every migration/fix script header must be the verified one** — real
   container name (`manooch-postgres`, not `manooch-backend-db-1`), real role (`manooch`, not
   `postgres`), real database name. Copy-paste from the last successful run; never transcribe
   from memory.
4. **Post-deploy schema assertion before traffic.** After the migration step runs and before
   routing traffic, check the physical change is there:
   ```sql
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_name = '<table>' AND column_name IN ('<changed columns>');
   ```
   Missing row(s) = failed deploy, roll back. For an index, query `pg_indexes`; for an FK,
   `information_schema.table_constraints`.
5. **Read smoke-test on the changed entity.** After migrations apply, exercise one
   representative read of the changed entity (a `findOne`/list against that table). A missing
   column becomes a visible deploy failure instead of a user-facing 500.
6. **Non-additive changes use expand/contract, never in-place.** A rename, type narrowing, or
   drop ships across two deploys: (1) expand — add the new shape, dual-write, backfill; (2)
   after the deploy is verified, contract — stop writing the old shape and drop it. A single
   in-place narrowing on live data is a crash-loop risk (see `CLAUDE.md` stack section).
7. **Fail loud at boot, not on first read.** When a feature depends on a column added by a
   recent migration, add an idempotent startup check (a `SELECT ... LIMIT 0` against the table
   or an `information_schema` check, optionally behind a feature flag) that throws on boot if
   the column is absent. The container must never go healthy and then 500 on first request —
   this is the structural fix for both incidents.
8. **Quote the emitted SQL in the PR description.** Review the generated migration before commit
   (existing rule), and paste the exact `ALTER TABLE` / `CREATE INDEX` it emits so the reviewer
   sees the physical change without running TypeORM locally. The migration timestamp is the
   audit key; reference it in the PR body.

`DB_MIGRATIONS_RUN=true` must be set in production (it is, as of 2026-08-07) — but the flag alone
does not prove a given migration applied; rules 2, 4, and 5 do.

## Soft delete (mandatory)

Every delete is a soft delete — never hard-remove a row.
- Every deletable entity gets `@DeleteDateColumn() deletedAt: Date | null`.
- Services call `softDelete`/`softRemove` — never `delete`/`remove`.
- TypeORM auto-excludes soft-deleted rows from `find()`, including joined relations — don't add a
  manual `deletedAt IS NULL` filter on top.
- A nullable-but-unique column (e.g. a legacy `code` some rows lack) needs a partial unique index
  scoped to live rows so a soft-deleted row's value doesn't block reuse:
  ```ts
  @Index('IDX_work_groups_code_active', ['code'], { unique: true, where: '"deletedAt" IS NULL' })
  ```
  See `StorePaymentSetting`, `StoreDomain`, or `WorkGroup` for the pattern. (The index name is
  mandatory per the indexing rule above.)
- An `inactive`/status flag is not a delete — it's a separate concern, don't conflate the two.

## Shared enums (`@manooch/types`)

`@manooch/types` is vendored at `packages/types`; `manooch-fronts/packages/types` is the
author-of-record — don't hand-edit the vendored copy's `src/`. When an entity column's type is a
shared enum, import the enum and **re-export it under the original local name** so existing imports
across the module keep working:
```ts
import { OrderStatus } from '@manooch/types/orders';
export { OrderStatus };

@Column({ type: 'enum', enum: OrderStatus, default: OrderStatus.PENDING })
status: OrderStatus;
```
Never import `zod` or a `*Schema` export from `@manooch/types` at runtime — only the enum (runtime)
or `import type` (erased) — that keeps `zod` out of the backend bundle. A new enum or shape is added
upstream in `manooch-fronts` first, then pulled in with `npm run sync:types`.
