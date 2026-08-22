---
name: skill-api-gateway
description: Use when writing NestJS controllers and DTOs in manooch-backend — validation pipe behavior, @ValidateNested nested DTOs, Swagger docs on every method, CustomerAuthGuard/SuperAdminGuard/OptionalCustomerAuthGuard selection, error-code discipline, response serialization, or global exception-filter/response-shape conventions.
---

# Skill: API Gateway

You specialize in the **HTTP edge**: NestJS controllers, DTOs, validation, guards, and exception
filters. Dispatched by `guard-nestjs-module`. (Entities live in `skill-db-architect`; service
transactions in `skill-transaction-engine`; module scaffold in `guard-nestjs-module`.)

> **Graphify first:** if `graphify-out/graph.json` exists, run `graphify query "<module>"`
> before grepping/reading source. Pass this instruction to any subagent.

## 1. Validation

The global pipe (`src/main.ts`) is `I18nValidationPipe` from `nestjs-i18n`, not plain NestJS
`ValidationPipe` — registered with `{ whitelist: true, transform: true }`. There is no
`forbidNonWhitelisted`: unknown properties are **silently stripped**, not rejected with a 400 — don't
write a DTO expecting a rejection for extra fields. The upshot is that a field missing from a DTO
doesn't fail the request, it just never reaches the entity — a PATCH can 200 while silently not
persisting. When a save "succeeds" but a field doesn't take effect, check the DTO's property list
before anything else.
- Every DTO field: `@ApiProperty()` + at least one `class-validator` decorator.
- Nested payloads: `@ValidateNested({ each: true })` + `@Type(() => ChildDto)` from `class-transformer`.
- Numeric query params: `@Type(() => Number)` for class-transformer coercion (path params use
  `ParseIntPipe` on the controller method instead — see §5).
- Validation error messages auto-translate via `src/i18n/fa/validation.json` — don't hand-write
  messages in the DTO.

## 2. Exception Filters & Response Shape

Three filters are registered globally in `app.module.ts` via `APP_FILTER` (LIFO precedence — most
specific last): `AllExceptionsFilter` (catch-all), `I18nHttpExceptionFilter` (translates thrown
`HttpException`s), `I18nValidationExceptionFilter` (validation failures). `ResponseTransformInterceptor`
is the global `APP_INTERCEPTOR`. **Never register any of these per-module or catch `HttpException`
locally** — throw and let the global filters format the response:
```json
{ "statusCode": 404, "errorCode": "PRODUCT_NOT_FOUND", "message": "محصول یافت نشد" }
```
- `errorCode` is the raw string passed to the exception constructor; `message` is auto-translated
  from `src/i18n/fa/errors.json` — add the code there first, then throw it, never invent an inline string.
- `NotFoundException` → 404, `UnprocessableEntityException` → 422, `ConflictException` → 409,
  `ForbiddenException` → 403.
- Database errors: catch `TypeORM QueryFailedError` in the service, map to 409/422 — never let a raw
  DB error message reach the client.

## 2b. Error-code discipline

- Codes are `UPPER_SNAKE_CASE`, `<DOMAIN>_<REASON>` — `ORDER_NOT_FOUND`, `STORE_ID_REQUIRED`,
  `ORDER_TRANSITION_INVALID`. Grep `src/i18n/fa/errors.json` first; reuse an existing code before
  minting a new one.
- The string passed to the exception constructor **is the code**, never an English sentence:
  ```ts
  throw new NotFoundException('ORDER_NOT_FOUND');        // ✅
  throw new NotFoundException('Order not found');        // ❌ — bypasses i18n
  throw new NotFoundException(`Order ${id} not found`);  // ❌ — dynamic, untranslatable
  ```
- Dynamic context (an id, an offending status) goes in the **log** (Nest `Logger` at warn/error
  level with the operation name), never in the client error. Throw the static code; log the detail.
- Before throwing a new code, add it to `src/i18n/fa/errors.json` in the same change. A code not
  present in `errors.json` renders to the client as the raw code string — the global filter does
  not invent a translation.
- One error condition → one code. Don't reuse a generic `BAD_REQUEST` for five different validation
  failures the client might distinguish (e.g. distinguish `STORE_ID_REQUIRED` from
  `ORDER_DOCUMENTS_REQUIRED`).

## 2c. Serialization — entities never cross the wire

- A controller method never returns a TypeORM entity (or an array of entities) directly. It
  returns a response shape — either a class decorated with `@Exclude()`/`@Expose()` (used with
  `ClassSerializerInterceptor`) or a plain mapped object built in the service, as
  `OrdersService.buildOrderDetail` already does.
- Soft-delete columns (`deletedAt`), internal FK-only fields, and raw JSONB blobs are excluded
  from the response shape by default; add each field to the response type explicitly only when it
  is part of the contract.
- Composed/projection response shapes (e.g. `AdminOrderDetail`, `AdminOrderListItem`) live in the
  module's `types/<feature>.types.ts` (see `guard-nestjs-module`). They are **output** shapes,
  distinct from input DTOs under `dto/`.
- `@ApiResponse({ type: ... })` references the response shape class, not the entity, so Swagger
  stays truthful.
- Never reach for `@Res()` and manual `res.json(...)` to work around serialization — fix the
  shape. The global `ResponseTransformInterceptor` already wraps the return value consistently.

## 3. Caching & rate-limiting — not present, don't assume them

`@nestjs/cache-manager` and `@nestjs/throttler` are **not dependencies of this repo** — there is no
`CacheInterceptor`, no `ThrottlerModule`, no `@Throttle()` anywhere in `src/`. Don't reference them as
an existing convention to follow. If a route genuinely needs caching or rate-limiting, that's a new
piece of infrastructure to propose explicitly (add the dependency, wire it in `AppModule`, after
going through `strategy-grill-me` first), not a pattern to copy from a sibling module.

## 4. Routing & Guard Selection

Guards actually exported by `src/common/guards/`:

| Guard | Use for | Behavior |
|---|---|---|
| `CustomerAuthGuard` | `/admin/*` and any authenticated route | Validates a JWT — `Authorization: Bearer` header takes precedence over the `auth_token` cookie; 401 `AUTH_UNAUTHORIZED` if both absent/invalid |
| `SuperAdminGuard` | Platform-global taxonomy, e.g. `/admin/store-categories/*` | Extends `CustomerAuthGuard`, additionally requires `role === AccountRole.SUPER_ADMIN`; 403 `SUPER_ADMIN_FORBIDDEN` otherwise — the only guard that branches on role |
| `OptionalCustomerAuthGuard` | Routes that behave differently signed-in vs anonymous | Mirrors `CustomerAuthGuard`'s precedence but proceeds unauthenticated instead of rejecting |
| *(none)* | Public storefront reads, e.g. `GET /stores/:slug/storefront-config` | Fully public, no guard |

Use `@CustomerId()` (`src/common/decorators/customer-id.decorator.ts`) to read the id either guard
sets on the request — never read `request.customerId` manually.

> There is no `DevAuthGuard` and no `X-Dev-Customer-Id` header auth scheme in this codebase — that
> header only survives as a stale Swagger API-key definition in `main.ts` and an unused i18n error
> key; no guard reads it. If you see it mentioned elsewhere, it's dead. Confirm which guard a route
> needs by reading an existing sibling controller, not by assuming from the route prefix alone.

## 5. Method shape (Swagger, params, status codes)

- Every controller method: `@ApiOperation({ summary })` + `@ApiResponse()` per status code.
- Every numeric path param: `@Param('id', ParseIntPipe) id: number` — never a raw `string`.
- `UpdateDto extends PartialType(CreateDto)` — import `PartialType` from `@nestjs/swagger`, not
  `@nestjs/mapped-types` (both appear in the repo today; converge on `@nestjs/swagger` going forward
  since it preserves the `@ApiProperty()` metadata Swagger needs).
- Throw i18n-coded exceptions from §2b; don't craft response bodies by hand.
- Return the service's already-mapped response shape (§2c); the global interceptor wraps it as
  `{ statusCode, success, message, data, errors }`.
