---
name: skill-platform-infra
description: Use when touching manooch-backend infrastructure that isn't module business logic — src/common/ guards, decorators, filters, or interceptors; a *.task.ts cron job; a *.seeder.ts; a *.util.ts helper; a provider/interface pair; src/config/ and env validation; pagination conventions; or anything in src/auth/.
---

# Skill: Platform Infrastructure

You own the cross-cutting backend surface that doesn't fit inside a single feature module. Dispatched
by `guard-nestjs-module`. (Feature modules themselves are scaffolded there; entities in
`skill-db-architect`; controllers/DTOs/guards-on-routes in `skill-api-gateway`; transactions in
`skill-transaction-engine`.)

> **Graphify first:** if `graphify-out/graph.json` exists, run `graphify query "<symbol>"` before
> grepping/reading source.

## `src/common/` — cross-module building blocks

A concern belongs in `src/common/` only when more than one module needs it unchanged; a
module-specific helper stays inside that module's folder.

| Subfolder | Contents today | Convention |
|---|---|---|
| `guards/` | `CustomerAuthGuard`, `OptionalCustomerAuthGuard`, `SuperAdminGuard` | Guard selection on a route is `skill-api-gateway`'s call — this is where the guard classes themselves live and get extended (`SuperAdminGuard extends CustomerAuthGuard`) |
| `decorators/` | `@CustomerId()`, `@JwtPayload()`, `@SuccessMessage(code)` | `createParamDecorator` for reading request fields a guard set (`customerId`, `jwtPayload`); `SetMetadata` for handler metadata an interceptor reads |
| `filters/` | `AllExceptionsFilter`, `I18nHttpExceptionFilter` | Registered globally via `APP_FILTER` in `app.module.ts` — **never** re-register in a feature module |
| `interceptors/` | `ResponseTransformInterceptor` | Registered globally via `APP_INTERCEPTOR`; reads `@SuccessMessage()` metadata off the handler via `Reflector`, wraps every response as `{ statusCode, success, message, data, errors }` |

To add a new success message: add the key under `success.*` in `src/i18n/fa/*.json`, then
`@SuccessMessage('the.key')` on the handler — don't hand-format a response body, the global
interceptor already does it.

## Cron tasks (`*.task.ts`)

Lives inside the module it serves (e.g. `src/modules/payments/payment-timeout.task.ts`), not in
`common/`. `@Injectable()` class, `@Cron(CronExpression...)` from `@nestjs/schedule` on the method,
inject the module's own service and delegate — no business logic in the task class itself. Register
in the module's `providers[]` alongside the service. `ScheduleModule.forRoot()` is already registered
once, globally, in `app.module.ts` — don't add it again in the feature module.

## Seeders (`*.seeder.ts`)

Module-local (`src/modules/plugins/plugins.seeder.ts`, `src/modules/super-admin/seed/super-admin.seeder.ts`)
— one-time/idempotent data population, not a migration. Guard every insert so re-running is safe
(check-then-insert or `ON CONFLICT DO NOTHING`), never assume a seeder runs exactly once.

## Utils (`*.util.ts`)

Module-local pure functions with no DI (`referral-code.util.ts`, `store-membership.util.ts`,
`store-domains.utils.ts`) — plain exported functions, not an `@Injectable()` class. If it needs a
repository or another service injected, it's a service method, not a util.

## Provider / interface pairs

Pattern: an interface describing the capability + one `@Injectable()` implementation, bound via a
DI token — see `src/modules/uploads/storage/`:
```ts
// storage-provider.interface.ts
export const STORAGE_PROVIDER = 'STORAGE_PROVIDER';
export interface StorageProvider {
  save(key: string, buffer: Buffer, mime: string): Promise<string>;
  delete(key: string): Promise<void>;
}
```
```ts
// module: { provide: STORAGE_PROVIDER, useClass: LocalStorageProvider }
```
Use this shape when a capability could later swap implementation (local disk vs. S3) — don't invent
it for a dependency that will only ever have one implementation.

## `src/config/` and environment validation

Plain exported config builders/objects, no `@Injectable()` — `cors.ts` (`buildCorsOptions()`),
`database.config.ts`, `data-source.ts` (TypeORM CLI entry point, used by `migration:*` scripts —
`skill-db-architect` owns migration workflow), `storage.config.ts`.

- **Every read of `process.env` lives in `src/config/`** — never in a feature service, controller,
  or guard. A service receives a fully-resolved config object/value via injection or a static config
  getter, not the raw env.
- **Validate config on boot.** Use a schema (`Joi.object`/`zod`) invoked from `main.ts` or
  `app.module.ts`: required vars present, URLs parse, enums match, ports numeric. If validation
  fails, log which key is wrong and exit non-zero at startup — a missing env var must never become
  a 500 on first request. This is the same fail-loud-at-boot principle as
  `skill-db-architect`'s post-migration column assertion.
- **Dev-only defaults belong in the config builder**, not scattered through the code: e.g.
  `PORT=4000`, `DB_SYNCHRONIZE=true` when `NODE_ENV !== 'production'`. Production-required vars have
  no fallback.
- **Secrets are read from env only in config**; never log them, interpolate them into error
  messages, or return them from any endpoint/DTO.

## Pagination (list endpoints)

- Paginated list endpoints accept `page` (1-based) and `limit` via the query DTO, with
  `@Type(() => Number)` and a hard cap (`limit <= 100`, default 20) so a client cannot request the
  whole table. Compute `skip = (page - 1) * limit`.
- Offset pagination is fine for admin lists up to ~100k rows. Use keyset/cursor pagination (an
  opaque `cursor` based on `(createdAt, id)`) for infinite-scroll storefront lists.
- The response envelope for a paginated list is:
  ```ts
  // types/<feature>.types.ts
  export interface PaginatedResult<T> {
    data: T[];
    total: number;
    page: number;
    limit: number;
  }
  ```
  `total` comes from a single `COUNT(*)` via QueryBuilder, not by loading all rows.
- Sort order is an explicit enum in the query DTO (`OrdersListSort` already does this), resolved
  via a private `resolveOrderBy()` helper — never accept raw column names from the client (SQL
  injection surface + accidental index scans).
- Filters (`status`, `storeId`, date range) are validated enums/ids in the DTO; date range bounds
  are checked (`dateFrom <= dateTo`) before building the query.

## `src/auth/` — the deliberate exception

`src/auth/` does **not** follow the `src/modules/<feature>/entities/` layout — `Customer`,
`CustomerAuthToken`, and `OtpRequest` (note: no `Entity` suffix, unlike most other entity classes)
sit at the folder root next to `auth.controller.ts`/`auth.service.ts`, because auth is the one module
every other module's guards depend on. Don't "fix" this into an `entities/` subfolder or rename the
classes to match other modules — it's intentional, not drift.
