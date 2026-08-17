# Fix PRD — Backend Skills Consistency, `types/` Convention, and Service Decomposition

**Repo:** `manooch-backend`
**Date:** 2026-08-17
**Scope:** Skills + `CLAUDE.md` only. No production code changes in this PRD (per decision).
**Audience:** Anyone maintaining the 10 skills under `.claude/skills/` (or wherever they live).
**Evidence reviewed:** `CLAUDE.md`, all 10 `SKILL.md` files, and `orders.service.ts` (~700 lines)
provided as the reference "large service".

---

## 0. TL;DR decisions

1. **Adopt the `types/<feature>.types.ts` convention for *all* modules, not just new ones.**
   Replace the grandfather clause in `guard-nestjs-module` with a **boy-scout rule**:
   if you touch a service/controller that has inline `interface`/`type` declarations,
   move them to `types/` in the same change. No one-shot sweep, no permanent exemption.
   This is the direct answer to "my modules don't have a `types/` dir and types are inline".

2. **Fix the review gate so it stops contradicting the other skills.** `guard-review`
   currently demands `forbidNonWhitelisted: true` and `@Throttle()` on public routes —
   both are explicitly *not* used by this repo per `skill-api-gateway` §1 and §3, and
   `@nestjs/throttler` is not even a dependency. As written, a Pre-PR audit would block
   correct code. Remove both checks; they belong to a different repo's variant.

3. **Pin down `@Index()` naming everywhere.** `CLAUDE.md` mandates an explicit index
   name (drift incident 2026-08-07), but neither `skill-db-architect` nor the
   `guard-review` checklist says so. Add the rule + an example to both.

4. **Add a "Service decomposition" rule to `skill-transaction-engine`,** informed by
   `strategy-deep-module`. The current skills are silent on how big a service is
   allowed to get, which is exactly how `orders.service.ts` grew to ~700 lines mixing
   queries, detail assembly, reorder, document submission, and the status state
   machine. The rule: keep one public service class (deep module), but split its body
   into co-located internal collaborators when it crosses a size/responsibility
   threshold. A concrete decomposition for `OrdersService` is in §6 (advisory —
   applied opportunistically, not mandated by this PRD).

5. **Fix the smaller drift:** `PartialType` import source, the misleading
   `ProductEntity` example (this codebase does not use an `Entity` suffix — see
   `skill-platform-infra`'s note on `Customer`/`OtpRequest`), the
   `InternalServerErrorException(err.message)` anti-pattern in the transaction
   template, the stale `src/modules/geo/` reference, and the duplicated
   item-count-query pattern in `orders.service.ts`.

6. **NEW — Stop production migration 500s from recurring.** Two separate features
   (the **payment-links `durationDays`** change documented in `CLAUDE.md`, and a
   **"stuck feature"** of the same root-cause class per the user) shipped with a
   green deploy only to 500 in production because the migration "succeeded" but the
   schema did not actually change on prod. Add a new **§10 "Production migration
   safety"** section to the PRD and a **new "Migrations in production"** section in
   `skill-db-architect` codifying: (a) the prod `migrations` table must be baselined
   before a new column-carrying migration is ever relied on; (b) every entity column
   change ships with a migration AND a post-deploy schema assertion; (c) runbook
   commands must be verified against the actual container/role names; (d) the app
   must fail loudly on startup when a required column is missing rather than 500 on
   first read; (e) the deploy pipeline runs the migration and a read-smoke-test
   before routing traffic.

7. **NEW — Add four micro-skills (folded into existing owning skills per the chosen
   format):**
   - **`skill-db-architect`** gains: "Production migration safety" (the incident rules
     from decision 6).
   - **`skill-api-gateway`** gains: "Error codes & i18n discipline" (every thrown
     exception uses a code that exists in `src/i18n/fa/errors.json`; no inline English
     strings; error-code naming convention) and "Serialization & response boundary"
     (entities never cross the wire — map to a response shape/`ClassSerializerInterceptor`;
     never `return this.repo.find()` raw from a controller).
   - **`skill-transaction-engine`** gains: "Logging & observability" (use the Nest
     `Logger`, never `console.log`; log at transaction boundaries and on rollback with
     correlation context; never log secrets/PII; warn-then-continue pattern for
     post-commit side effects like loyalty points — exactly the case already in
     `bulkUpdateOrderStatus`).
   - **`skill-platform-infra`** gains: "Configuration & env validation" (every
     `process.env` read is centralized in `src/config/` and validated via
     `Joi`/`zod`-style schema on boot; no scattered `process.env.X` in services; fail
     fast at startup rather than 500 at first use) and "Pagination convention"
     (cursor/offset + `take`/`skip` cap, total count, typed list envelope in
     `types/`).

   All four are deliberately "micro" — one concern each, with a do/don't example — and
   live inside the owning skill rather than creating new folders, matching the
   "fold into existing skills" packaging decision.

All fixes below are **exact text replacements** against the current `SKILL.md` /
`CLAUDE.md` content. Nothing here invents a new architectural concept — each change
makes one skill agree with another skill or with already-documented reality.

---

## 1. Findings table

| # | File(s) | Problem | Severity | Fix |
|---|---------|---------|----------|-----|
| F1 | `guard-nestjs-module` | Types convention is "new modules only" with an explicit exemption list — guarantees the `types/` dir never exists for the large existing modules (orders, products, reviews) | **High** (root cause of user's complaint) | §2.1 |
| F2 | `guard-review` | Checklist demands `forbidNonWhitelisted: true`; `skill-api-gateway` §1 says the pipe is `whitelist: true` with silent strip | **High** (false-positive BLOCK) | §3.1 |
| F3 | `guard-review` | Checklist demands `@Throttle()` on public routes; `skill-api-gateway` §3 says throttler is not a dependency and must not be assumed | **High** (false-positive BLOCK) | §3.1 |
| F4 | `guard-review` vs `skill-api-gateway` | Review says "guards on all `/admin/*` and privileged routes" but doesn't mention `OptionalCustomerAuthGuard` or the no-guard public case | Medium | §3.1 |
| F5 | `skill-db-architect`, `guard-review`, `CLAUDE.md` | `@Index()` must have an explicit name (2026-08-07 drift incident). `CLAUDE.md` says so; the other two don't. | **High** (prod-drift risk) | §4.1, §3.1 |
| F6 | `guard-nestjs-module` vs `skill-api-gateway` §5 | Module scaffold example uses `ProductEntity`; `skill-platform-infra` explicitly notes entities in this repo have *no* `Entity` suffix (`Customer`, `OtpRequest`). Every entity imported in `orders.service.ts` confirms this (`Order`, `OrderItem`, `BankCheck`…). | Medium (misleads new code) | §2.2 |
| F7 | `skill-transaction-engine` §1 | Catch block template throws `InternalServerErrorException(err.message)` — leaks raw DB error text to the client, contradicting its own §3 and `skill-api-gateway` §2 ("never let a raw DB error message reach the client") | **High** (security + contradiction) | §5.1 |
| F8 | `skill-transaction-engine` §2 | Batch-COUNT example already says "in a **new** module" types go in `types/` — inherits F1's grandfather problem | Medium | §5.2 |
| F9 | `skill-transaction-engine` | No guidance on service size/decomposition; nothing says "don't let one service grow to 700 lines mixing 5 responsibilities" | **High** (root cause of `orders.service.ts` shape) | §5.3 |
| F10 | `skill-db-architect` | Static-reference-data section points at `src/modules/geo/`; `CLAUDE.md` says geo was replaced by `locations` ("DB-backed provinces/cities + portal CRUD (replaced the old static geo module)") | Low (stale path) | §4.2 |
| F11 | `CLAUDE.md` "Modules" / "Entity Conventions" | Top-level doc never mentions the `types/` folder or the "no inline types in services/controllers" rule, so a reader of `CLAUDE.md` alone never learns the convention | Medium | §7 |
| F12 | `guard-nestjs-module` | Doesn't reference the eventual service-decomposition rule (F9); file-type routing table mentions the service but not the "split when large" rule | Low | §2.3 |
| F13 | `skill-db-architect` (and PRD §10) | No production-migration safety rule. Two incidents (payment-links `durationDays`; a "stuck feature" in the same class) deployed green and then 500'd on prod because the migration "succeeded" while the actual schema did not change — prod had no `migrations` table, the runbook used a wrong container/role, and the app only hit the missing column on first read. **High** — user-reported, repeated twice. | **High** | §10 |
| F14 | `skill-api-gateway` | No rule enforcing that exception codes exist in `src/i18n/fa/errors.json`, and no rule against returning raw TypeORM entities from controllers (entity fields leak across the wire; the global interceptor wraps but doesn't strip). | Medium | §11.2, §11.3 |
| F15 | `skill-transaction-engine` | No logging convention. Codebase uses Nest `Logger` inconsistently; the post-commit loyalty-award loop in `bulkUpdateOrderStatus` explicitly needs a "warn and continue" pattern that isn't documented; `console.*` would slip through review. | Medium | §11.4 |
| F16 | `skill-platform-infra` | `process.env` reads are centralized in `src/config/` per the existing docs, but no skill states the rule or the "validate on boot, fail fast" requirement — so new env vars get read ad-hoc inside services and only fail at first use. No pagination convention either, so list endpoints invent their own `take/skip` shapes. | Medium | §11.5, §11.6 |
| — | `orders.service.ts` (evidence only, not changed here) | The item-count raw-SQL block is duplicated verbatim between `listOrders` and `listCustomerOrders` — a concrete case F9's "extract a private helper" rule would catch; also two `for` loops issue per-product queries during CANCELLED stock reversal (acceptable inside a `QueryRunner`, but worth noting against `skill-transaction-engine` §2's loop-fetch rule — these are writes, not reads, and already batched via `manager.increment` per id; no N+1 *read*, but see §6) | Advisory | §6 |

Findings on the three **strategy** skills and `skill-platform-infra` /
`skill-tdd-driver`: reviewed in full; no contradictions with the rest of the set
requiring changes. `strategy-deep-module`'s "deep, not wide" rule is what motivates
F9's *internal* split rather than a public-API split; it is cited there.

---

## 2. Fixes — `guard-nestjs-module/SKILL.md`

### 2.1 F1 — Replace the grandfather clause with a boy-scout rule

**Find** the entire subsection starting at the `### types/` heading through the
end of its second paragraph/code blocks (currently):

> ### `types/` — no inline interfaces or type aliases in service/controller files
>
> **New modules going forward:** any `interface`, `type` alias, or composed return shape ...
> ...
> This is a scaffold rule for **new modules** — existing services with inline `export interface`/
> `export type` at the top of the file (`orders.service.ts`, `products.service.ts`,
> `reviews.service.ts`, and others) are not being retrofitted as part of adopting this convention;
> don't move them unless you're already touching that file for another reason.

**Replace with:**

```md
### `types/` — no inline interfaces or type aliases in service/controller files

Any `interface`, `type` alias, or composed return shape (e.g. an entity joined with
a computed field, a list-endpoint result shape, a method return type that isn't just
an entity or DTO) lives in `types/<feature>.types.ts` and is imported from there —
never declared inline at the top of a `.service.ts` or `.controller.ts` file. Export
it if a DTO, controller, or another module references it; keep it unexported if it's
purely internal.

```ts
// types/product.types.ts
export interface CategoryWithAssets extends Omit<Category, 'imageId'> {
  image: Asset | null;
}

export type AdminProductListItem = Product & { orderCount: number };
```
```ts
// products.service.ts
import { CategoryWithAssets, AdminProductListItem } from './types/product.types';
```

**Boy-scout rule (no permanent grandfathering):** existing services that still have
inline `export interface` / `export type` at the top of the file (e.g.
`orders.service.ts`, `products.service.ts`, `reviews.service.ts`) are **not** subject
to a one-shot sweep, but the next time you touch that file for any reason — bug fix,
new method, refactor — move its inline type declarations into `types/` in the same
change. If you're only changing a single line and moving the types would balloon the
diff, leave a `// TODO(types): move to ./types/<feature>.types on next edit` marker
instead of leaving it silent. Do **not** add new inline types to an existing file
that already has them — new types always go in `types/`.

Why no grandfather clause: the previous wording ("existing files are not being
retrofitted") is why most of `src/modules/` has no `types/` folder today; a
boy-scout rule gets us there module-by-module without a risky big-bang PR.
```

Also update the validation checklist line:

**Find:**
```
- [ ] No `interface`/`type` declared inline in a `.service.ts` or `.controller.ts` — it's in `types/`.
```
**Replace with:**
```
- [ ] No *new* `interface`/`type` declared inline in a `.service.ts` or `.controller.ts` — it belongs in `types/`; if you edited a file that still has inline types, they were moved or marked with a `TODO(types)` per the boy-scout rule.
```

And in **Common Mistakes**, replace:
```
- Declaring `export interface`/`export type` at the top of a service or controller in a **new**
  module — put it in `types/<feature>.types.ts` instead (existing files with this pattern are not
  being retrofitted).
```
with:
```
- Declaring `export interface`/`export type` at the top of a service or controller, in any module,
  new or existing — put it in `types/<feature>.types.ts`. If you're touching an old file that still
  has them, apply the boy-scout rule (move them, or leave a `TODO(types)` if the diff must stay small).
```

### 2.2 F6 — Drop the `Entity` suffix in the scaffold example

This codebase's entities do **not** use an `Entity` suffix. Confirmed by
`skill-platform-infra` ("note: no `Entity` suffix, unlike most other entity classes")
and by every import in `orders.service.ts` (`Order`, `OrderItem`, `BankCheck`,
`Product`, `ProductImage`, `Category`, `ProductAttributeValue`, `ProductUnit`,
`Customer`, `Address`, `ShippingMethod`, `OrderStatusLog`).

**In the Module File example, find:**
```ts
import { ProductEntity } from './entities/product.entity';

@Module({
  imports: [TypeOrmModule.forFeature([ProductEntity])],
```
**Replace with:**
```ts
import { Product } from './entities/product.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Product])],
```

Also in the earlier `types/product.types.ts` example in §2.1 above, `CategoryEntity`
/ `ProductEntity` are already replaced with `Category` / `Product`.

### 2.3 F12 — Cross-link the service-decomposition rule

**In the file-type routing table, replace the `*.service.ts` row:**
```
| `*.service.ts` — single-record CRUD, multi-record/multi-table mutations, N+1, batch reads | `skill-transaction-engine` |
```
with:
```
| `*.service.ts` — single-record CRUD, multi-record/multi-table mutations, N+1, batch reads, **and when/how to split an oversized service into internal collaborators** | `skill-transaction-engine` (see its "Service decomposition" section) |
```

---

## 3. Fixes — `guard-review/SKILL.md`

### 3.1 F2, F3, F4, F5 — Correct the backend-rules checklist

**Find** the entire `### Backend rules` bullet block in the subagent prompt
(currently eight bullets starting with `- [ ] Multi-record mutations...` and ending
with the `@manooch/types` bullet).

**Replace with:**

```md
### Backend rules
- [ ] Multi-record mutations wrapped in QueryRunner (try/catch/finally, commit/rollback/release); the catch block **rethrows a domain exception** — never `InternalServerErrorException(err.message)` (that leaks raw DB text; see skill-transaction-engine §3)
- [ ] No repository **reads** inside for/map loops — batch with `In([...ids])`, a single `ANY($1)` query, or a QueryBuilder. (Writes *inside* an already-open `QueryRunner` are fine — the transaction boundary is the point, not the loop itself.)
- [ ] DTOs match the global pipe actually registered: `I18nValidationPipe({ whitelist: true, transform: true })`. There is **no `forbidNonWhitelisted`** in this repo — unknown fields are silently stripped, so the check is "does the DTO declare every field that must persist?" (a missing field doesn't 400, it silently no-ops). Do **not** demand `forbidNonWhitelisted: true`.
- [ ] **No `@Throttle()` / `@nestjs/throttler` checks.** That package is not a dependency and `@nestjs/cache-manager` isn't either — see skill-api-gateway §3. If a route genuinely needs rate-limiting, that's new infra to propose, not an existing rule to enforce.
- [ ] `@Index(...)` on every filtered/sorted/FK column **with an explicit name as the first argument**, e.g. `@Index('IDX_orders_store_status', ['storeId', 'orderStatus'])` — unnamed indexes get a synchronize hash no migration will match (2026-08-07 drift incident; see CLAUDE.md "Entity Conventions" and skill-db-architect).
- [ ] Guard matches the audience: `CustomerAuthGuard` on `/admin/*` and authed shopper routes, `SuperAdminGuard` only where the route is platform-global (e.g. `/admin/store-categories/*`), `OptionalCustomerAuthGuard` for signed-in-vs-anonymous routes, and **no guard at all** on public storefront reads. There is no `DevAuthGuard`.
- [ ] Soft delete only — every deletable entity has `@DeleteDateColumn`, services call `softDelete`/`softRemove`, never `delete`/`remove`; partial unique indexes on nullable-unique columns use `WHERE "deletedAt" IS NULL`.
- [ ] Any enum or cross-boundary shape the frontend also needs comes from `@manooch/types` (vendored snapshot at `packages/types/`, author-of-record is the sibling `manooch-fronts` repo) — never hand-redeclared. Entity enum columns re-export the imported enum under the local name.
```

Everything else in the subagent prompt (Step 0 diff scope, Step 2 compile gate,
Step 3 npm audit, the compact return table, the 95% confidence gate, the PR-only
rule) stays as-is.

---

## 4. Fixes — `skill-db-architect/SKILL.md`

### 4.1 F5 — Mandate explicit `@Index` names

**Find** the single bullet:
```
- **Indexing:** Any column targeted by filter, sort, or foreign-key operations must carry `@Index()` in the entity file. (The query-side rationale lives in `skill-transaction-engine` §N+1.)
```

**Replace with:**
```
- **Indexing:** Any column targeted by filter, sort, or foreign-key operations must carry `@Index()` in the entity file — and **every `@Index()` must be given an explicit name as its first argument**, e.g. `@Index('IDX_orders_store_created', ['storeId', 'createdAt'])`. Never write the bare/decorator form. An unnamed index gets a deterministic hash from `synchronize` that no hand-written migration will ever match by coincidence; that mismatch is exactly what caused the 2026-08-07 index-name drift (11 indexes existed on prod only under hashed names while migrations referenced literal names — see migration `RenameDriftedIndexNames1786100000000` and CLAUDE.md "Entity Conventions"). The query-side rationale for *which* columns to index lives in `skill-transaction-engine` §N+1.
- **Composite index column order:** put the equality-filter column first, then the sort/range column (matches how the query uses it).
```

The partial-unique-index example in the soft-delete section already uses a name;
extend it to match:
```ts
@Index('IDX_work_groups_code_active', ['code'], { unique: true, where: '"deletedAt" IS NULL' })
```
(no change needed — it already has a name; just make sure the surrounding text
references the naming rule above).

### 4.2 F10 — Fix the stale `geo/` reference

**Find:**
```
See `src/modules/geo/`.
```
**Replace with:**
```
(Pattern reference: this is how the old `geo/` module worked before it was replaced
by the DB-backed `locations` module; use the same thin-service + public-controller
shape, not the legacy static array — see `src/modules/locations/` for the current
DB-backed implementation and only reach for a `.data.ts` array when the data truly
never changes at runtime.)
```

---

## 5. Fixes — `skill-transaction-engine/SKILL.md`

### 5.1 F7 — Stop leaking `err.message` in the transaction template

**Find the §1 catch block:**
```ts
  } catch (err) {
    await queryRunner.rollbackTransaction();
    throw new InternalServerErrorException(err.message);
  } finally {
```

**Replace with:**
```ts
  } catch (err) {
    await queryRunner.rollbackTransaction();
    // Map known DB errors to a domain exception; rethrow HttpExceptions (e.g.
    // UnprocessableEntityException from validateTransition) unchanged. Never
    // surface err.message to the client — it can contain raw SQL/schema text.
    if (err instanceof HttpException) throw err;
    if (err instanceof QueryFailedError) {
      // map err.code (e.g. 23505 unique_violation, 23503 FK) to 409/422 here
      throw new ConflictException('DB_CONSTRAINT_VIOLATION');
    }
    throw new InternalServerErrorException('INTERNAL_ERROR');
  } finally {
```

Add `HttpException` to the implied NestJS common imports and `QueryFailedError` to
the implied TypeORM imports at the top of any file using this pattern. (Doing the
actual `err.code` switch is method-specific; the template must not encourage
`err.message` passthrough — that is both a security leak and a direct contradiction
of this same skill's §3.)

### 5.2 F8 — Remove "in a new module" from the batch-COUNT example

**Find:**
```
When a list response needs an aggregate count per row (e.g., `itemCount` per order), use a single raw SQL query with `ANY($1)` — never N+1. In a **new** module, the composed type goes in `types/<feature>.types.ts` (see `guard-nestjs-module`), not declared inline in the service:
```
**Replace with:**
```
When a list response needs an aggregate count per row (e.g., `itemCount` per order), use a single raw SQL query with `ANY($1)` — never N+1. The composed type goes in `types/<feature>.types.ts` (see `guard-nestjs-module`'s boy-scout rule — existing services move their inline types there on next edit), never declared inline in the service:
```

Also add a short **dedup** note right after the example, directly motivated by the
duplicated item-count block currently in `orders.service.ts` (evidence F12):

```md
**If the same batch-count query appears in more than one method of the same service**
(e.g. an admin list and a customer list both computing `itemCount` per order),
extract it as a private helper that takes the open `EntityManager`/`DataSource` and
the row ids — do not copy the raw SQL block. See `addresses.service.ts` for the
same pattern applied to a repeated "unset previous default" step.
```

### 5.3 F9 — New "Service decomposition" section

Add the following section **between §2 (N+1) and §3 (DB error mapping)**:

```md
### 5.3 (reference) — Service decomposition text as it lands in skill-transaction-engine — stay deep, don't grow a god-service

`strategy-deep-module` says a module should hide substantial complexity behind a
small public interface. "Small interface" does **not** mean one 1000-line service
file — it means one small set of public methods. The body behind those methods can
and should be split when it grows.

**Decomposition triggers** (any one is enough):

- The service file is comfortably past ~400 lines, or its constructor injects more
  than ~6–8 repositories/services.
- The service mixes clearly different responsibilities — e.g. list/detail *reads*,
  a state-machine *lifecycle*, and a document-upload flow are three things, not one.
- A private helper is reused by 2+ public methods but has its own dependencies
  (repos, other services) that the other methods don't need.
- A subset of methods is transaction/write-heavy while another subset is pure
  read-model assembly — splitting them makes each easier to test in isolation.

**Pattern — one public facade, internal collaborators:**

Keep the module's single public `XxxService` (controllers keep injecting one thing;
the module stays deep). Move coherent chunks of its body into co-located injectable
classes that are **not** controllers and are **not** exported from the module:

```
src/modules/orders/
├── orders.service.ts                 ← public facade: list/get/status-update entry points, injects the collaborators below
├── orders-query.service.ts           ← @Injectable(), not exported; list/detail read-model assembly, batch COUNT, N+1-safe joins
├── orders-lifecycle.service.ts       ← @Injectable(), not exported; VALID_TRANSITIONS state machine, stock reversal, status-log writes
├── orders-documents.service.ts       ← @Injectable(), not exported; receipt / bank-check submission transaction
├── reorder.service.ts                ← optional, only if the read model is large enough to warrant its own class
└── ...
```

Wire all of them in `orders.module.ts` under `providers: [...]`; only `OrdersService`
needs to be listed (the internal ones are injected by it, so they're providers too,
but they aren't exported and aren't injected by controllers). There is no rule that
a module folder can only hold one `*.service.ts` — name internal ones
`<feature>-<responsibility>.service.ts`.

Rules:
- The public service stays the only entry point controllers use. Don't expose
  collaborators through the module's `exports`.
- If a split piece has zero state and zero injected deps, it's a util, not a
  service — see `skill-platform-infra` (`*.util.ts`).
- When splitting, preserve transaction **boundaries**: a QueryRunner created in the
  facade must be passed into the collaborator (see the `unsetPreviousDefault`
  helper pattern in §1 that takes an `EntityManager`); don't start a nested
  transaction per method.
- Defer the split until one of the triggers above is actually hit — don't pre-shatter
  a 80-line CRUD service into four files (that's the shallow-module anti-pattern
  `strategy-deep-module` warns against).

This rule applies to new code immediately; existing oversized services are moved
opportunistically under the same boy-scout rule as the `types/` convention.
```

---

## 6. Advisory decomposition for `orders.service.ts` (evidence for F9)

This is the worked example that motivated §5.3. **Not a code change in this PRD** —
documented so the next person to touch the orders module knows the intended seam.

Current state (from the provided file):

- **~700 lines**, **14 injected repositories/services** (`orderRepo`, `orderItemRepo`,
  `bankCheckRepo`, `logRepo`, `customerRepo`, `productRepo`, `productImageRepo`,
  `categoryRepo`, `productAttrValueRepo`, `productUnitRepo`, `addressRepo`,
  `shippingMethodRepo`, `dataSource`, `storesService`, `loyaltyService`).
- Mixes five responsibilities:
  1. List + item-count (admin) — `listOrders`, `resolveOrderBy`, the raw-SQL COUNT.
  2. List + item-count (customer) — `listCustomerOrders` — **same COUNT block duplicated**.
  3. Detail read-model assembly — `getOrderById`, `findCustomerOrder`, `buildOrderDetail` (attribute-value join, address mapping, bank-check mapping, product mapping).
  4. Reorder read-model — `findReorderProducts` (thumbnails, categories, starting-price fallback) — almost entirely independent of the order lifecycle.
  5. Writes / state machine — `submitCustomerReceipt`, `submitCustomerDocuments`,
     `bulkUpdateOrderStatus`, `updateOrderStatus`, `validateTransition`, plus the
     CANCELLED stock-reversal block (which is itself duplicated between
     `bulkUpdateOrderStatus` and `updateOrderStatus`).

Recommended seam (matches §5.3's pattern):

| File | Public methods | Owns |
|------|----------------|------|
| `orders.service.ts` (facade) | `listOrders`, `getOrderById`, `listCustomerOrders`, `findCustomerOrder`, `bulkUpdateOrderStatus`, `updateOrderStatus` | Owns the `callerId`/`assertOwner` tenancy check and the `VALID_TRANSITIONS` guard; delegates everything below. Stays <150 lines. |
| `orders-query.service.ts` | internal `listWithCount(query, scoping)`, `buildOrderDetail(order)` | Both copies of the COUNT query collapse into one helper; `buildOrderDetail` and its attribute/bankcheck/address maps move here. |
| `orders-lifecycle.service.ts` | internal `transition(order, to, {changedBy, reason})` | `validateTransition`, the CANCELLED stock reversal (one copy, takes the open `EntityManager`), the `OrderStatusLog` write, and the post-commit `loyaltyService.earnFromOrder` hook. |
| `orders-documents.service.ts` | internal `submitReceipt`, `submitDocuments` | The receipt and bank-check/cash-receipt submission transaction; `BankCheck` writes live here. |
| `reorder.service.ts` (optional) | internal `findForCustomer(customerId, limit)` | `findReorderProducts`; injects the product/image/category/attr/unit repos the rest of the facade doesn't need. |

Types that should move to `types/orders.types.ts` today:
`AdminOrderListItem`, `AdminOrderAddress`, `AdminOrderBankCheck`, `AdminOrderDetail`,
plus the inline return type of `findReorderProducts`
(`{ data: (Product & {...})[]; total: number }`) — it currently has no name at all.

The inline row-shape types used inside `buildOrderDetail`
(e.g. `{ id: string; value: string; name: string | null; colorHex: string | null }`
and the `countRows` element type) also belong in `types/orders.types.ts`, not
declared at the point of use.

This is a **recommendation**, not a mandate in this PRD — when a future change
touches the orders service, §5.3's triggers are already met, so that change should
land the split alongside its actual feature work.

---

## 7. Fix — `CLAUDE.md`

### 7.1 F11 — Document the `types/` convention at the top level

**In the "Entity Conventions" section, after the last bullet (the `@Index(...)` naming bullet), add:**

```md
### 7.1 (reference) — Module-local types text as it lands in CLAUDE.md

Every module folder may contain a `types/` subdirectory holding `*.types.ts` files
for module-local interfaces, type aliases, and composed/computed return shapes
(an entity joined with a computed field, a list-item shape, etc.). The rule is
**no inline `interface`/`type` declarations at the top of a `.service.ts` or
`.controller.ts`** — they live in `types/<feature>.types.ts` and are imported.
Cross-boundary shapes the frontend also consumes come from `@manooch/types` instead;
the module-local `types/` folder is for shapes that are internal to this backend
module (or are projections of entities that aren't shared upstream). Existing
services with inline types (e.g. `orders.service.ts`) move them into `types/`
opportunistically under a boy-scout rule — see `guard-nestjs-module`.
```

### 7.2 Optional — cross-link service decomposition

Add a one-line pointer in the "Modules" section's intro paragraph:

```md
A module may contain more than one `*.service.ts` when the service is large enough
to warrant internal collaborators behind a single public facade — see
`skill-transaction-engine` "Service decomposition". Don't assume one service file
per module.
```

---

## 8. Out-of-scope / explicitly not changed

- **No production code changes.** `orders.service.ts` is used as evidence; the
  actual split/type-move happens in a future code PR under the boy-scout rule, not
  here. This is per the scope decision.
- **`skill-api-gateway`, `skill-platform-infra`, `skill-tdd-driver`,
  `strategy-deep-module`, `strategy-grill-me`, `strategy-ubiquitous-language`**
  require no content changes. They are the *source* of rules the other files are
  being brought into agreement with.
- **No new dependencies.** The `@Throttle` removal in §3.1 does not mean throttling
  should be added; it means the review gate must stop demanding something that
  doesn't exist. If rate-limiting is ever actually needed, it goes through
  `strategy-grill-me` → `strategy-deep-module` first, as new infra.
- **No entity/DTO/interface rename** in code. The `Entity` suffix fix in §2.2 is a
  documentation/example correction; there is no `ProductEntity` class to rename.
- **No sweep across all 41 modules.** The boy-scout rule is the migration strategy.

---

## 9. Verification checklist for the skills PR itself

After applying the edits:

- [ ] `grep -rn "forbidNonWhitelisted" .claude/skills/` returns nothing (it is mentioned only as "there is no forbidNonWhitelisted", not as a requirement).
- [ ] `grep -rn "@Throttle" .claude/skills/` returns nothing except the explicit "do not reference" note in `skill-api-gateway` and the "do not check" note in `guard-review`.
- [ ] `grep -rn "err.message" .claude/skills/skill-transaction-engine/` returns nothing in a code example.
- [ ] `grep -rn "ProductEntity\|CategoryEntity" .claude/skills/` returns nothing.
- [ ] `grep -rn "src/modules/geo" .claude/skills/` returns nothing.
- [ ] `grep -rn "@Index" .claude/skills/skill-db-architect/` shows every example with a name as the first argument.
- [ ] Every mention of "new module" as a qualifier on the types convention is gone — the boy-scout rule is stated identically in `guard-nestjs-module`, `skill-transaction-engine`, and `CLAUDE.md`.
- [ ] The phrase "Service decomposition" appears in `skill-transaction-engine` and is cross-linked from `guard-nestjs-module` and `CLAUDE.md`.
- [ ] No skill tells the reviewer to require something another skill says doesn't exist (the original F2/F3 class of contradiction).
- [ ] `skill-db-architect` contains a "Production migration safety" section with all 8 rules from §10.2, and references both the payment-links `durationDays` and "stuck feature" incidents.
- [ ] `guard-review`'s backend-rules list contains the two migration checks from §10.3.
- [ ] `skill-api-gateway` contains the "Error codes & i18n discipline" and "Serialization — entities never cross the wire" sections.
- [ ] `skill-transaction-engine` contains the "Logging & observability" section, including the post-commit warn-and-continue pattern.
- [ ] `skill-platform-infra` contains the "Configuration & env validation" and "Pagination" sections.
- [ ] `CLAUDE.md` carries the migration-safety pointer from §10.4.

For the **future code PR** that applies this to `orders.service.ts` (not part of
this PRD): `npm run build`, `npm run lint`, `npm test`, and the `guard-review`
Pre-PR subagent must all pass with the corrected checklist. For **any future PR
that changes an entity column**, the §10.2 rules are part of that same gate.
## 10. NEW — Production migration safety (F13)

### 10.1 The two incidents

**Incident A — payment-links `durationDays` (documented in `CLAUDE.md`):** the
entity gained a column via migration, but prod had no `migrations` table at all
(schema had been built entirely by `synchronize` before it was disabled), so the
column was never applied and every payment-link read 500'd. The fix script's own
runbook command was itself unrunnable against prod (wrong container name
`manooch-backend-db-1` and wrong role `postgres` vs. the real `manooch-postgres` /
`manooch`), so the incident recurred after an earlier attempted fix. Prod has since
been baselined (`src/scripts/baseline-prod-migrations.sql`) and `DB_MIGRATIONS_RUN`
set, and both scripts' headers now document the verified command.

**Incident B — "stuck feature" (same root-cause class, per the user):** the
migration ran "successfully" as part of a green production deploy, but a field
change in the migration did not actually take effect on the prod schema, and the
first request that touched the entity 500'd. The exact migration and stack are not
in the materials reviewed; the rules below are written to cover both incidents
without depending on feature-specific detail. If the feature owner can paste the
migration + stack later, add a one-paragraph postmortem under §10.1 in the same
shape as incident A.

**Shared root cause:** an entity column change was treated as "shipped" once the
migration file existed and the deploy pipeline exited 0, without verifying (a) that
prod's migration-tracking state actually recorded it, (b) that the physical column
was present in the prod database after deploy, and (c) that a representative read
of the changed entity succeeded before real traffic hit it. The app also had no
startup-time assertion, so the missing column surfaced as a runtime 500 on first
read instead of a loud boot failure.

### 10.2 Rules (codify in `skill-db-architect`)

These apply to **every** PR that adds, drops, renames, narrows, or changes the type
of an entity column. `synchronize: true` is dev-only; prod's schema is owned by
migrations (`DB_MIGRATIONS_RUN=true`), and that contract is enforced by these rules.

1. **Every entity column change ships a migration in the same PR.** No "we'll run
   synchronize on prod", no "the column is nullable so it can wait". The migration
   file, the entity change, and the baseline check are one atomic change.
2. **Never rely on a migration you cannot prove ran.** Before a migration that adds
   a required physical object (column/index/FK) is merged, confirm the target
   environment's `migrations` table exists and is baselined. If a new environment
   is being stood up, run `src/scripts/baseline-prod-migrations.sql` (or its env
   equivalent) first — exactly the step that was missing in incident A.
3. **The runbook command in every migration/fix script header must be the verified
   one:** real container name (`manooch-postgres`, not `manooch-backend-db-1`),
   real role (`manooch`, not `postgres`), real database name. Copy-paste from the
   last successful run; never transcribe from memory. A wrong runbook is how
   incident A recurred after its "first fix".
4. **Post-deploy schema assertion before traffic.** The deploy pipeline (or a
   documented manual step if there is no pipeline hook yet) runs, against prod,
   after the migration step and before routing traffic:
   ```sql
   SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_name = '<table>' AND column_name IN ('<changed columns>');
   ```
   If the expected row(s) are missing, the deploy is treated as failed and rolled
   back — not "green, investigate later". For an index, the equivalent is a check
   against `pg_indexes`.
5. **Read smoke-test on the changed entity.** After migrations apply, hit one
   representative read of the changed entity (a `findOne`/list against the table)
   in the deploy's post-check. A missing column turns into a visible deploy failure
   instead of a user-facing 500.
6. **Non-additive changes are expand/contract, never in-place.** A rename, type
   narrowing, or dropped column ships in two deploys: (1) expand — add the new
   column, dual-write, backfill; (2) after deploy and verification, contract —
   stop writing the old column and drop it. A single in-place narrowing on live
   data is exactly the crash-loop class flagged in `CLAUDE.md`'s stack section.
7. **Fail loud at boot, not on first read.** When a feature depends on a column
   added by a recent migration, add an idempotent startup check (a tiny `SELECT ...
   LIMIT 0` or an `information_schema` check behind a feature flag) that throws on
   boot if the column is absent, so the container never goes healthy and never
   serves a 500. This is the structural fix for both incidents — it converts a
   silent runtime failure into a deploy failure.
8. **The migration filename/timestamp is the audit key.** Review the generated SQL
   before committing (per existing rule), and in the PR description quote the
   exact `ALTER TABLE` / `CREATE INDEX` the migration emits so the reviewer can see
   the physical change without running TypeORM locally.

### 10.3 Review-gate additions (`guard-review`)

Add two checks to the backend-rules list in §3.1 (already edited above — this is
the text to add on top):

```md
- [ ] If the diff adds/removes/changes an entity column: a migration is in the same
      PR; the PR description quotes the emitted SQL; and the change is either
      additive-only or follows the expand/contract two-deploy pattern.
- [ ] If a recent migration introduced a column the code now reads unconditionally,
      there is either a startup assertion for it or the deploy post-checks include
      the information_schema read + a read smoke-test (skill-db-architect "Production
      migration safety").
```

### 10.4 `CLAUDE.md` update

Append a short pointer to the existing stack/migrations paragraph so the rule is
discoverable from the top-level doc too:

```md
Any entity column change must follow "Production migration safety" in
`skill-db-architect` — migration + baselined `migrations` table + post-deploy
schema assertion + read smoke-test, with a boot-time assertion so a missing column
fails the deploy instead of 500ing on first read. See the payment-links
`durationDays` and "stuck feature" postmortems there.
```

---

## 11. NEW — Micro-skills (folded into existing owning skills, per decision 7)

These are deliberately short, do/don't sections. The full text to add to each
skill file is in the matching fixed file under `fixed/`; this section explains the
*why* and the exact placement.

### 11.1 `skill-db-architect` — "Production migration safety"

Full section text is §10.2 above. Insert it as a new top-level section between
"Migrations" and "Soft delete". This is the incident-driven micro-skill.

### 11.2 `skill-api-gateway` — "Error codes & i18n discipline"

Why: `skill-api-gateway` §2 already says "add the code to `errors.json` first,
then throw it, never invent an inline string", but there's no *naming* convention
and no checklist enforcing it, so `orders.service.ts` mixes bare codes
(`'ORDER_NOT_FOUND'`, `'ORDER_ACCESS_DENIED'`, `'STORE_ID_REQUIRED'`,
`'ORDER_DOCUMENTS_REQUIRED'`, `'ORDER_TRANSITION_INVALID'`) with the default
English-string constructor argument in places — exactly the inconsistency a
micro-skill prevents.

Section to add (right after §2 "Exception Filters & Response Shape"):

```md
### 11.2 (reference) — Error-code discipline text as it lands in skill-api-gateway

- Codes are `UPPER_SNAKE_CASE`, `<DOMAIN>_<REASON>` — `ORDER_NOT_FOUND`,
  `STORE_ID_REQUIRED`, `ORDER_TRANSITION_INVALID`. Reuse an existing code before
  minting a new one; grep `errors.json` first.
- The string passed to the exception constructor **is the code**, never an English
  sentence:
  ```ts
  throw new NotFoundException('ORDER_NOT_FOUND');        // ✅
  throw new NotFoundException('Order not found');        // ❌ — bypasses i18n
  throw new NotFoundException(`Order ${id} not found`);  // ❌ — dynamic, untranslatable
  ```
- Dynamic context (an id, an offending status) goes in the **log**, not the
  client error. Throw the code; log the detail at warn/error level with the
  Nest `Logger`.
- Before throwing a "new" code, add it to `src/i18n/fa/errors.json` in the same
  change. A code that isn't in `errors.json` renders as a raw string to the client
  — the global filter does not invent a translation.
- One error condition → one code. Don't reuse `BAD_REQUEST` for five different
  validation failures the client might want to distinguish.
```

### 11.3 `skill-api-gateway` — "Serialization & response boundary"

Why: `strategy-deep-module` says "entities never cross the wire", and
`orders.service.ts` already does the right thing in `buildOrderDetail` (it maps to
an explicit response shape), but no skill states the rule or the mechanical
pattern. New controllers routinely `return this.service.find()` and leak every
entity column (including internal fields like `deletedAt`, soft-delete joins, and
JSONB internals).

Section to add after §2b:

```md
### 11.3 (reference) — Serialization — entities never cross the wire

- A controller method never returns a TypeORM entity (or an array of entities)
  directly. It returns a response shape — either a class decorated with
  `@Exclude()`/`@Expose()` (used with `ClassSerializerInterceptor`) or a plain
  mapped object built in the service, as `OrdersService.buildOrderDetail` does.
- Soft-deleted columns (`deletedAt`), internal FK-only fields, and raw JSONB blobs
  are excluded from the response shape by default; add each field to the response
  type explicitly when it is actually part of the contract.
- Response shapes that are composed/projections of entities (like
  `AdminOrderDetail`, `AdminOrderListItem`) live in the module's
  `types/<feature>.types.ts` — see `guard-nestjs-module`. They are not DTOs (DTOs
  are input; these are output).
- `@ApiResponse({ type: ... })` references the response shape class, not the
  entity, so Swagger stays truthful.
- Never `@Res()` and manually `res.json(...)` to work around serialization — fix
  the shape; the global `ResponseTransformInterceptor` already wraps the return
  value.
```

### 11.4 `skill-transaction-engine` — "Logging & observability"

Why: no skill currently says anything about logging. Two cases in the orders
service *must* be logged and aren't: (a) rollbacks inside the `QueryRunner` catch
blocks (currently the error is just rethrown, with no log breadcrumb), and (b) the
post-commit loyalty-award loop that is deliberately "warn and continue" — the
existing comment explains the intent but there's no rule telling the next author to
actually `Logger.warn` the per-order failure.

Section to add after §2.5 (between service decomposition and §3):

```md
### 11.4 (reference) — Logging & observability

- Use the Nest `Logger` (`private readonly logger = new Logger(OrdersService.name)`),
  never `console.log`/`console.error`. The platform captures structured Nest logs;
  `console.*` bypasses log levels and correlation.
- Log at transaction boundaries:
  - `logger.debug` (or verbose) at transaction start with the operation name and
    the logical aggregate id (e.g. `orderId`) — never the full payload.
  - `logger.warn` on a caught-and-rethrown transaction failure, including the
    aggregate id and the error name/code. Re-throwing without logging loses the
    breadcrumb.
  - Never log full DTOs, full entities, PII (mobile numbers, national IDs), or
    secrets/tokens. Log ids, error codes, and counts.
- **Post-commit side effects (warn-and-continue):** when a side effect runs *after*
  `commitTransaction()` on purpose (e.g. `loyaltyService.earnFromOrder` in
  `bulkUpdateOrderStatus` — a points failure must not roll back an already-committed
  status change), wrap it in try/catch and `logger.warn` with the aggregate id and
  reason; do not let it reject the request. The comment at the call site must state
  *why* it's post-commit, so the next reader doesn't "helpfully" move it inside the
  transaction.
- Use correlation ids where the request-scoped context provides one; do not invent
  a new id system in a feature service.
```

### 11.5 `skill-platform-infra` — "Configuration & env validation"

Why: `src/config/` already exists (`cors.ts`, `database.config.ts`, etc.) and
`CLAUDE.md` references it, but none of the skills state the rule that all
`process.env` access lives there and is validated at boot. Without it, a missing
env var becomes a 500 on first use (the same failure class as the migration
incidents) instead of a boot failure.

Section to add under the existing "`src/config/`" subsection:

```md
- Every read of `process.env` lives in `src/config/` — never in a feature service,
  controller, or guard. A service receives a fully-resolved config object/value
  via injection or a static config getter, not the raw env.
- Config is **validated on boot** (a `Joi`/`zod` schema in `src/config/` invoked
  from `main.ts`/`app.module.ts`): required vars present, URLs parse, enums match.
  If validation fails, the app exits non-zero at startup — a missing env var must
  never become a 500 on first request.
- Dev-only defaults (e.g. `PORT=4000`, `DB_SYNCHRONIZE=true` in non-production) are
  set in the config builder, not scattered through the code; production-required
  vars have no fallback.
- Secrets are read from env only in config; they are never logged, interpolated
  into error messages, or returned from any endpoint.
```

### 11.6 `skill-platform-infra` — "Pagination convention"

Why: list endpoints currently invent their own query shapes; the orders module
has `dateFrom/dateTo`, `storeId`, `status`, `sort` but no `take/skip` or `total`,
and every other list module will re-derive it. A tiny convention prevents drift.

Section to add after "Configuration & env validation":

```md
### 11.6 (reference) — Pagination text as it lands in skill-platform-infra

- Paginated list endpoints accept `page` (1-based) and `limit` via the query DTO,
  with `@Type(() => Number)` and a hard cap (`limit <= 100`, default 20) so a
  client can't request the whole table. Offset (`skip = (page - 1) * limit`) is
  fine for admin lists up to ~100k rows; use keyset/cursor pagination (an opaque
  `cursor` based on `(createdAt, id)`) for infinite-scroll storefront lists.
- The response envelope for a paginated list is:
  ```ts
  { data: T[]; total: number; page: number; limit: number }
  ```
  declared in `types/<feature>.types.ts`. `total` comes from a single
  `COUNT(*)` via QueryBuilder, not by loading all rows.
- Sort order is an explicit enum in the query DTO (`OrdersListSort` already does
  this), resolved via a private `resolveOrderBy()` helper — never accept raw
  column names from the client (SQL-injection surface + accidental index scans).
- Filters (`status`, `storeId`, date range) are validated enums/ids in the DTO;
  date range bounds are checked (`dateFrom <= dateTo`) before building the query.
```

These four additions (11.2–11.6) are the "micro-skills" requested — each is small
enough to read in 30 seconds and concrete enough to be enforced by `guard-review`
once added to its checklist.

---

