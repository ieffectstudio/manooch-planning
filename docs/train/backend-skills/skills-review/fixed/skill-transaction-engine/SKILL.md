---
name: skill-transaction-engine
description: Use when writing any manooch-backend service-layer method — single-record CRUD, mutations that touch multiple records or tables, QueryRunner transactions, atomic rollback, deduping a shared step across sibling mutations, N+1 elimination, batch COUNT, service decomposition, or mapping QueryFailedError.
---

# Skill: Transaction Engine

You enforce **service-layer** persistence rules — this is the owning skill for `*.service.ts`
regardless of whether a given method is a plain single-record CRUD op or a multi-record transaction.
Dispatched by `guard-nestjs-module`. (Entities live in `skill-db-architect`; controllers/guards/exception
filters in `skill-api-gateway`.)

> **Graphify first:** if `graphify-out/graph.json` exists, run `graphify query "<module>"`
> before grepping/reading source. Pass this instruction to any subagent.

## 0. Baseline single-record CRUD

Most service methods never touch a transaction at all — don't reach for `QueryRunner` until §1
actually applies.

```ts
async findOne(id: number): Promise<Feature> {
  const item = await this.repo.findOne({ where: { id } });
  if (!item) throw new NotFoundException('FEATURE_NOT_FOUND');
  return item;
}

create(dto: CreateFeatureDto): Promise<Feature> {
  return this.repo.save(this.repo.create(dto));
}

async update(id: number, dto: UpdateFeatureDto): Promise<Feature> {
  const item = await this.findOne(id);      // reuse the NotFoundException guard
  Object.assign(item, dto);
  return this.repo.save(item);
}

async remove(id: number): Promise<void> {
  const item = await this.findOne(id);
  await this.repo.softRemove(item);          // never .remove() — soft delete is mandatory, skill-db-architect
}
```

- Every method has an explicit `Promise<T>` return type.
- `findOne` throws `NotFoundException` with an i18n error **code** (e.g. `'FEATURE_NOT_FOUND'`) for a missing record — the controller never checks for `null`. Error codes live in `src/i18n/fa/errors.json` (skill-api-gateway §2); never pass a free-text English sentence.
- `update`/`remove` call `findOne` first and reuse its guard rather than re-querying.
- Composed return types (an entity plus a computed field) go in `types/<feature>.types.ts`, not inline — see `guard-nestjs-module`.

## 1. Transaction Boundaries & ACID Enforcement
- **Multi-Step Mutation Rule:** Any operation that alters multiple database records, spans multiple tables, or executes sequential write loops must be locked inside an explicit TypeORM transaction block.
- **Implementation Pattern:** Use `QueryRunner` to ensure clean atomic rollbacks upon error. Never allow dangling connections or uncommitted transaction states:
  ```ts
  const queryRunner = this.dataSource.createQueryRunner();
  await queryRunner.connect();
  await queryRunner.startTransaction();
  try {
    await queryRunner.manager.save(entityA);
    await queryRunner.manager.save(entityB);
    await queryRunner.commitTransaction();
  } catch (err) {
    await queryRunner.rollbackTransaction();
    // Map known DB errors to a domain exception; rethrow HttpExceptions (e.g.
    // UnprocessableEntityException from validateTransition) unchanged. Never
    // surface err.message to the client — it can contain raw SQL/schema text.
    if (err instanceof HttpException) throw err;
    if (err instanceof QueryFailedError) {
      // switch on err.code (23505 unique_violation, 23503 FK violation, …) → 409/422
      throw new ConflictException('DB_CONSTRAINT_VIOLATION');
    }
    throw new InternalServerErrorException('INTERNAL_ERROR');
  } finally {
    await queryRunner.release();
  }
  ```

`HttpException` comes from `@nestjs/common`; `QueryFailedError` from `typeorm`.

**Dedup repeated transaction blocks across sibling mutations:** when several service methods (e.g.
`create`/`update`/`setDefault` on an "only one default row per owner" entity) each need the same
"unset the previous default" step inside their own `QueryRunner`, extract it as a private helper
taking the already-open `EntityManager` (`private async unsetPreviousDefault(manager: EntityManager,
ownerId: string)`) rather than repeating the `manager.update(...)` call inline in each method — keeps
the transaction boundary in the caller while removing the duplication. See
`src/modules/addresses/addresses.service.ts`. The same pattern applies to a shared write step like
"reverse stock on CANCELLED" that currently appears in both `updateOrderStatus` and
`bulkUpdateOrderStatus` — one helper taking the `EntityManager`, called from both.

## 2. N+1 Query Elimination & Performance
- **Loop Fetching Prohibition:** Executing DB query selection inside any iterative loop (`for`, `forEach`, `map`) is a critical performance violation for **reads**. Writes inside an already-open `QueryRunner` are fine — the transaction boundary is the point, not the loop itself (and `manager.increment`/`manager.update` on a known id is not a fetch).
- **Batching & Aggregation:** Consolidate lookups via explicit TypeORM QueryBuilder using `WHERE IN` constraints or aggregation.
- **Database Index Optimization:** Any column targeted by filter, sort, or FK operations must carry `@Index(...)` with an explicit name in the TypeORM entity file (declare it in `skill-db-architect`).

### Batch COUNT pattern (computed list fields)
When a list response needs an aggregate count per row (e.g., `itemCount` per order), use a single raw SQL query with `ANY($1)` — never N+1. The composed type goes in `types/<feature>.types.ts` (see `guard-nestjs-module`'s boy-scout rule — existing services move their inline types there on next edit), never declared inline in the service:

```typescript
// types/feature.types.ts
export type AdminFeatureListItem = Feature & { itemCount: number };
```
```typescript
// feature.service.ts
import { AdminFeatureListItem } from './types/feature.types';

async listItems(): Promise<AdminFeatureListItem[]> {
  const rows = await this.repo.find({ order: { createdAt: 'DESC' } });
  if (rows.length === 0) return [];
  const ids = rows.map((r) => r.id);
  const counts: { rowId: string; count: number }[] = await this.dataSource.query(
    `SELECT parent_id AS "rowId", COUNT(id)::int AS "count"
     FROM child_table WHERE parent_id = ANY($1) GROUP BY parent_id`,
    [ids],
  );
  const map = new Map(counts.map((c) => [c.rowId, c.count]));
  return rows.map((r) => ({ ...r, itemCount: map.get(r.id) ?? 0 }));
}
```

`type AdminXxxListItem = Xxx & { computedField: number }` needs no new class or entity — just a type
alias in `types/xxx.types.ts`.

**If the same batch-count query appears in more than one method of the same service** (e.g. an admin
list and a customer list both computing `itemCount` per order), extract it as a private helper that
takes the `DataSource`/`EntityManager` and the row ids — do not copy the raw SQL block. The same rule
applies to any shared raw-SQL/QueryBuilder fragment.

## 2.5 Service decomposition — stay deep, don't grow a god-service

`strategy-deep-module` says a module should hide substantial complexity behind a small public
interface. "Small interface" does **not** mean one 1000-line service file — it means one small set
of public methods. The body behind those methods can and should be split when it grows.

**Decomposition triggers** (any one is enough):

- The service file is comfortably past ~400 lines, or its constructor injects more than ~6–8 repositories/services.
- The service mixes clearly different responsibilities — e.g. list/detail *reads*, a state-machine *lifecycle*, and a document-upload flow are three things, not one.
- A private helper is reused by 2+ public methods but has its own dependencies (repos, other services) that the other methods don't need.
- A subset of methods is transaction/write-heavy while another subset is pure read-model assembly — splitting them makes each easier to test in isolation.

**Pattern — one public facade, internal collaborators:**

Keep the module's single public `XxxService` (controllers keep injecting one thing; the module stays
deep). Move coherent chunks of its body into co-located injectable classes that are **not**
controllers and are **not** exported from the module:

```
src/modules/orders/
├── orders.service.ts                 ← public facade: list/get/status-update entry points, injects the collaborators below
├── orders-query.service.ts           ← @Injectable(), not exported; list/detail read-model assembly, batch COUNT, N+1-safe joins
├── orders-lifecycle.service.ts       ← @Injectable(), not exported; VALID_TRANSITIONS state machine, stock reversal, status-log writes
├── orders-documents.service.ts       ← @Injectable(), not exported; receipt / bank-check submission transaction
├── reorder.service.ts                ← optional, only if the read model is large enough to warrant its own class
└── ...
```

Wire all of them in `orders.module.ts` under `providers: [...]`; the internal ones are injected by
the facade, so they're providers too, but they aren't exported and aren't injected by controllers.
There is no rule that a module folder can only hold one `*.service.ts` — name internal ones
`<feature>-<responsibility>.service.ts`.

Rules:
- The public service stays the only entry point controllers use. Don't expose collaborators through the module's `exports`.
- If a split piece has zero state and zero injected deps, it's a util, not a service — see `skill-platform-infra` (`*.util.ts`).
- When splitting, preserve transaction **boundaries**: a `QueryRunner` created in the facade must be passed into the collaborator (see the `unsetPreviousDefault` helper pattern in §1 that takes an `EntityManager`); don't start a nested transaction per method.
- Defer the split until one of the triggers above is actually hit — don't pre-shatter an 80-line CRUD service into four files (that's the shallow-module anti-pattern `strategy-deep-module` warns against).

This rule applies to new code immediately; existing oversized services are moved opportunistically
under the same boy-scout rule as the `types/` convention.

## 2.6 Logging & observability

- Use the Nest `Logger` (`private readonly logger = new Logger(OrdersService.name)`), never
  `console.log`/`console.error`. The platform captures structured Nest logs; `console.*` bypasses
  log levels and request correlation.
- Log at transaction boundaries:
  - `logger.debug`/`verbose` at transaction start with the operation name and the logical
    aggregate id (e.g. `orderId`) — never the full payload or entity.
  - `logger.warn` in the `catch` block before rethrowing, with the aggregate id and the error
    name/code. Rethrowing without logging loses the breadcrumb — the global filter logs the
    response, but the per-transaction context (which order, which step) is only available here.
  - Do **not** log full DTOs, full entities, PII (mobile numbers, national IDs, recipient names),
    or secrets/tokens. Log ids, error codes, and row counts.
- **Post-commit side effects — warn and continue:** when a side effect intentionally runs *after*
  `commitTransaction()` (e.g. `loyaltyService.earnFromOrder` in `bulkUpdateOrderStatus` — a points
  failure must not roll back a status change already committed to the orders table), wrap it in its
  own try/catch and `logger.warn` with the aggregate id and reason; do not let it reject the
  request. Leave a comment at the call site stating *why* it is post-commit so the next reader
  doesn't "helpfully" move it inside the transaction.
- Use the request/correlation id from the request context where it is provided; do not invent a new
  id system inside a feature service.
- Never log the raw `err.message` from a `QueryFailedError` to the client (see §3) — it may contain
  SQL/schema text. Log it server-side at `error` level if needed, but throw a coded exception to the
  client.

## 3. DB error mapping
Catch `TypeORM QueryFailedError` and map it to `409 Conflict` or `422 Unprocessable Entity`; never
expose raw database error messages to the client (and never `throw new InternalServerErrorException(err.message)`).
Rethrow `HttpException` subclasses (`UnprocessableEntityException`, `NotFoundException`, etc.)
unchanged so their i18n error codes propagate. (Global exception-filter wiring is owned by
`skill-api-gateway`.)
