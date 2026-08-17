---
name: guard-review
description: Senior Backend Quality Auditor for manooch-backend — auto-detects mode (debug / pre-PR / post-review), dispatches Pre-PR and Post-Review verification to a subagent to keep main context lean, runs diff-scoped compile gates and local npm audit. Backend-only — this repo owns no frontend code and does not review it.
type: process
---

# Review Agent (Senior Backend Quality Auditor)

Scope: this repo (`manooch-backend`) is a standalone NestJS 11 API. It never reviews
`manooch-fronts` (the Next.js apps / design-system / types packages) — that repo owns its own
`guard-review` variant.

## Mode Detection

Detect the active mode from context:
- **Debug:** active errors, failing tests, runtime exceptions → run inline (interactive root-cause debugging).
- **Pre-PR:** implementation complete, preparing pull request → dispatch to subagent.
- **Post-Review:** resolving code-review feedback → dispatch to subagent.

---

## Debug Mode (inline — main thread)

### 1. Internet pre-check (before touching code)
```
WebSearch: "<exact-error-message> nestjs site:github.com OR stackoverflow.com"
```
Scan top 3 results for known upstream bugs. Report to user before writing a fix.

### 2. Reproduce → Fix → Verify
1. Reproduce the bug — confirm you can trigger it consistently.
2. Write the fix.
3. Confirm the bug no longer occurs.
4. A regression `*.spec.ts` is encouraged for complex logic but not required.

Use `superpowers:systematic-debugging` to guide root-cause tracing.

---

## Pre-PR Mode & Post-Review Mode (subagent dispatch)

**Do not run these steps inline.** Dispatch a single `general-purpose` subagent via the `Agent` tool with the prompt below. All raw tool I/O stays inside the subagent. The subagent returns ONLY the compact report format defined at the end of this section.

### Subagent Prompt Template

```
You are a senior backend quality auditor running a Pre-PR / Post-Review gate for manooch-backend
(a standalone NestJS API repo). This repo has no frontend code — never check frontend rules.

## Step 0 — Compute diff scope
Run: git diff --name-only main...HEAD
(Fallback if empty: git diff --name-only --staged)
Note DEPS_CHANGED (package.json or package-lock.json changed).

## Step 1 — Architectural compliance
If `graphify-out/graph.json` exists, FIRST run `graphify query "<changed modules>"` (use
`graphify path "A" "B"` / `graphify explain "X"` for relationships) to orient on the touched
modules and existing patterns. The subagent MUST use graphify before any grep/Read of source. Then
read in full only the impacted files, plus any file that needs a line-level rule check below.

### Backend rules
- [ ] Multi-record mutations wrapped in QueryRunner (try/catch/finally, commit/rollback/release); the catch block **rethrows a domain exception** — never `InternalServerErrorException(err.message)` (that leaks raw DB text; see skill-transaction-engine §3)
- [ ] No repository **reads** inside for/map loops — batch with `In([...ids])`, a single `ANY($1)` query, or a QueryBuilder. (Writes *inside* an already-open `QueryRunner` are fine — the transaction boundary is the point, not the loop itself.)
- [ ] DTOs match the global pipe actually registered: `I18nValidationPipe({ whitelist: true, transform: true })`. There is **no `forbidNonWhitelisted`** in this repo — unknown fields are silently stripped, so the check is "does the DTO declare every field that must persist?" (a missing field doesn't 400, it silently no-ops). Do **not** demand `forbidNonWhitelisted: true`.
- [ ] **No `@Throttle()` / `@nestjs/throttler` checks.** That package is not a dependency and `@nestjs/cache-manager` isn't either — see skill-api-gateway §3. If a route genuinely needs rate-limiting, that's new infra to propose, not an existing rule to enforce.
- [ ] `@Index(...)` on every filtered/sorted/FK column **with an explicit name as the first argument**, e.g. `@Index('IDX_orders_store_status', ['storeId', 'orderStatus'])` — unnamed indexes get a synchronize hash no migration will match (2026-08-07 drift incident; see CLAUDE.md "Entity Conventions" and skill-db-architect).
- [ ] Guard matches the audience: `CustomerAuthGuard` on `/admin/*` and authed shopper routes, `SuperAdminGuard` only where the route is platform-global (e.g. `/admin/store-categories/*`), `OptionalCustomerAuthGuard` for signed-in-vs-anonymous routes, and **no guard at all** on public storefront reads. There is no `DevAuthGuard`.
- [ ] Soft delete only — every deletable entity has `@DeleteDateColumn`, services call `softDelete`/`softRemove`, never `delete`/`remove`; partial unique indexes on nullable-unique columns use `WHERE "deletedAt" IS NULL`.
- [ ] Any enum or cross-boundary shape the frontend also needs comes from `@manooch/types`
      (the sibling manooch-fronts repo's packages/types, consumed via file: link) — never
      hand-redeclared here. Entity enum columns re-export the imported enum under the local name.
- [ ] No inline `interface`/`type` declared at the top of a touched service or controller — new types belong in `types/<feature>.types.ts`; if a file was edited that still has old inline types, they were moved or marked `TODO(types)` per guard-nestjs-module's boy-scout rule.
- [ ] If the diff adds/removes/changes an entity column: a migration is in the same PR; the PR description quotes the emitted SQL; the change is either additive-only or follows the expand/contract two-deploy pattern; and the runbook command (if any) uses the verified container/role names (`manooch-postgres` / `manooch`, never `manooch-backend-db-1` / `postgres`).
- [ ] If code now reads unconditionally from a column introduced by a recent migration, there is either a boot-time column assertion or the deploy post-checks include the `information_schema` read + a read smoke-test (skill-db-architect "Production migration safety"). A migration file existing is not sufficient evidence that prod's schema changed.
- [ ] Exception codes thrown by touched code are `UPPER_SNAKE_CASE` `<DOMAIN>_<REASON>`, exist in `src/i18n/fa/errors.json`, and no code throws an inline English/dynamic string (skill-api-gateway §2b).
- [ ] Controllers do not return raw TypeORM entities — the return is a mapped response shape from `types/<feature>.types.ts` (skill-api-gateway §2c).
- [ ] No `console.log`/`console.error` in touched service code — Nest `Logger`; transaction catch blocks log before rethrowing; post-commit side effects use the warn-and-continue pattern (skill-transaction-engine §2.6).
- [ ] Any new `process.env` read is in `src/config/`, validated on boot, with no fallback for production-required vars (skill-platform-infra "Configuration & env validation").

## Step 2 — Compile gate
Run: npm run build
Run: npm run lint
Run: npm test

## Step 3 — Dependency audit (only if DEPS_CHANGED is non-empty)
Run: npm audit --omit=dev
Report any HIGH or CRITICAL advisories.

## RETURN FORMAT (compact — no raw tool output, only this table)
**Mode:** [Pre-PR | Post-Review]
**Verdict:** [PASS | BLOCK]

| Gate | Status | Notes |
|------|--------|-------|
| Build (nest build) | RUN/SKIP | errors if any |
| Lint | RUN/SKIP | errors if any |
| Tests (jest) | RUN/SKIP | failures if any |
| npm audit | RUN/SKIP | HIGH/CRITICAL advisories if any |

**Findings** (only items that need fixing):
| File:Line | Rule violated | Exact fix |

**PR Readiness:** [Clear to proceed | Blocked — fix items above first]
```

After the subagent returns its compact report, relay the report to the user. If verdict is BLOCK, fix the listed items then re-invoke guard-review. If PASS, proceed to PR creation.

---

## 95% Confidence Gate (applies to both modes)

Before reporting any finding:
- [ ] File referenced has been read in full.
- [ ] Rule violation cites exact line number and file path.
- [ ] Every fix includes exact corrected code — no abstract descriptions.
- [ ] `npm run build` and `npm test` output included verbatim in subagent evidence.
- [ ] The rule being enforced matches what the owning skill (skill-api-gateway / skill-db-architect /
      skill-transaction-engine / guard-nestjs-module) actually says today — not what a different
      repo's variant said. If a checklist item contradicts an owning skill, the owning skill wins;
      flag the contradiction instead of blocking the PR on it.

---

## PR-Only Rule

```bash
git push -u origin feature/<branch-name>
gh pr create --title "feat: <feature>" --body "..."
```

Create the PR targeting `main` and stop. Never auto-merge. User merges manually.
