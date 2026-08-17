---
name: guard-nestjs-module
description: Use when creating a new NestJS module or adding any file to an existing one in manooch-backend — folder layout, controller splitting by audience, module wiring, AppModule registration, or deciding which sibling skill owns a given file type.
---

# NestJS Module Scaffold (Manooch)

You own the **module scaffold** for `manooch-backend` — folder tree, `.module.ts` wiring, and
`AppModule` registration — before a single line of business logic is written. Per-layer conventions
live in sibling skills; this skill routes to them so there is one source of truth per file type.

## File-Type Routing

Before writing any file, find its suffix here and read that skill first:

| File | Owning skill |
|---|---|
| `*.entity.ts`, migrations, `.data.ts` reference data, soft delete | `skill-db-architect` |
| `*.controller.ts`, `*.dto.ts`, guards/roles on routes, Swagger, exception shape | `skill-api-gateway` |
| `*.service.ts` — single-record CRUD, multi-record/multi-table mutations, N+1, batch reads, **and when/how to split an oversized service into internal collaborators** | `skill-transaction-engine` (see its "Service decomposition" section) |
| `*.spec.ts`, `src/__mocks__/`, test-first discipline | `skill-tdd-driver` |
| `src/common/` guards/decorators/filters/interceptors, `*.task.ts`, `*.seeder.ts`, `*.util.ts`, provider/interface pairs, `src/config/` | `skill-platform-infra` |
| `types/*.types.ts` — module-local interfaces, type aliases, composed/computed return shapes | this skill (below) |

## Pre-Implementation Check

If `graphify-out/graph.json` exists, run `graphify query "<feature/module you're touching>"` before
grepping/reading source — locate existing patterns to reuse rather than inventing new ones. Check
`src/modules/` for a sibling module solving a similar problem before writing new code.

---

## Module Structure

```
src/modules/<feature-name>/
├── <feature-name>.module.ts          ← TypeOrmModule.forFeature([...]), registers controllers + service
├── <feature-name>.controller.ts      ← single audience (see below)
├── <feature-name>.service.ts         ← business logic (public facade; may delegate to internal *-<responsibility>.service.ts files)
├── <feature-name>.service.spec.ts    ← co-located unit test (skill-tdd-driver)
├── dto/
│   ├── create-<feature>.dto.ts
│   └── update-<feature>.dto.ts       ← PartialType(CreateDto), imported from @nestjs/swagger
├── entities/
│   └── <feature>.entity.ts           ← entities/ for multi-entity modules; module root is fine
│                                         for a single entity (see src/modules/about/).
│                                         Entity classes have NO "Entity" suffix (Product, Order…).
└── types/
    └── <feature>.types.ts            ← module-local interfaces/type aliases, see below
```

Optional members, add only when the module actually needs them:
`<feature>.constants.ts`, `<feature>.data.ts` (static reference data — see `skill-db-architect`),
`<feature>.util.ts`, and internal collaborator services named `<feature>-<responsibility>.service.ts`
(see `skill-transaction-engine` "Service decomposition").

### `types/` — no inline interfaces or type aliases in service/controller files

Any `interface`, `type` alias, or composed return shape (e.g. an entity joined with a computed
field, a list-endpoint result shape, a method return type that isn't just an entity or DTO) lives
in `types/<feature>.types.ts` and is imported from there — never declared inline at the top of a
`.service.ts` or `.controller.ts` file. Export it if a DTO, controller, or another module
references it; keep it unexported if it's purely internal to this module.

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

**Boy-scout rule (no permanent grandfathering):** existing services that still have inline
`export interface` / `export type` at the top of the file (e.g. `orders.service.ts`,
`products.service.ts`, `reviews.service.ts`) are **not** subject to a one-shot sweep, but the next
time you touch that file for any reason — bug fix, new method, refactor — move its inline type
declarations into `types/` in the same change. If you're only changing a single line and moving the
types would balloon the diff, leave a `// TODO(types): move to ./types/<feature>.types on next edit`
marker instead of leaving it silent. Do **not** add new inline types to an existing file that
already has them — new types always go in `types/`.

Why no grandfather clause: the previous wording ("existing files are not being retrofitted") is
why most of `src/modules/` has no `types/` folder today; a boy-scout rule gets us there
module-by-module without a risky big-bang PR.

### Controllers split by audience, not one-per-module

A module serving more than one audience gets one controller file per audience — this is the real
convention (57 controllers across 34 of the 35 module folders in `src/modules/`):

- `admin-<feature>.controller.ts` — `/admin/*`, `CustomerAuthGuard` or `SuperAdminGuard`
- `public-<feature>.controller.ts` — public storefront reads, no guard
- `customer-<feature>.controller.ts` — logged-in shopper routes, `CustomerAuthGuard`

Examples: `src/modules/products/{admin,public}-products.controller.ts`,
`src/modules/orders/{admin,customer}-orders.controller.ts`. A module with a single audience keeps
the plain `<feature>.controller.ts` name (e.g. `src/modules/about/about.controller.ts`).

Guard choice, DTO/validation rules, and Swagger requirements are owned by `skill-api-gateway` —
don't duplicate them here.

---

## Module File

```ts
// products.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AdminProductsController } from './admin-products.controller';
import { PublicProductsController } from './public-products.controller';
import { ProductsService } from './products.service';
import { Product } from './entities/product.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Product])],
  controllers: [AdminProductsController, PublicProductsController],
  providers: [ProductsService],
  // exports: [ProductsService]  ← only if another module needs it
})
export class ProductsModule {}
```

**After creating the module, always register it in `AppModule.imports[]`** (`src/app.module.ts`) —
a module that isn't registered silently doesn't load.

---

## Output Validation Checklist

- [ ] Controllers are split by audience (`admin-`/`public-`/`customer-`) when the module serves more
      than one — confirmed against a sibling module, not assumed.
- [ ] Every route uses the guard its audience actually requires — `CustomerAuthGuard` /
      `SuperAdminGuard` / `OptionalCustomerAuthGuard` / none for public — per `skill-api-gateway`.
      There is no `DevAuthGuard` in this codebase.
- [ ] Entity, DTO, service, and test conventions were read from their owning skill, not reinvented here.
- [ ] No *new* `interface`/`type` declared inline in a `.service.ts` or `.controller.ts` — it belongs
      in `types/`; if you edited a file that still has inline types, they were moved or marked with a
      `TODO(types)` per the boy-scout rule.
- [ ] Module is registered in `AppModule.imports[]`.
- [ ] `npm run build` compiles cleanly; `npm run test` passes if tests exist.

## Common Mistakes

- Inventing a single `<feature>.controller.ts` for a module that actually serves both admin and
  public/customer traffic — split by audience instead.
- Guessing a guard from the route prefix alone — read a sibling controller in the same module tree first.
- Forgetting to add the module to `AppModule.imports` — feature will silently not load.
- Re-deriving entity/DTO/service rules instead of reading the owning skill — leads to drift the
  next time that skill is updated and this one isn't.
- Declaring `export interface`/`export type` at the top of a service or controller, in any module,
  new or existing — put it in `types/<feature>.types.ts`. If you're touching an old file that still
  has them, apply the boy-scout rule (move them, or leave a `TODO(types)` if the diff must stay small).
- Adding an `Entity` suffix to an entity class (e.g. `ProductEntity`) — this codebase's entities are
  `Product`, `Order`, `Customer`, etc., with no suffix (see `skill-platform-infra`'s note on
  `Customer`/`OtpRequest`).
