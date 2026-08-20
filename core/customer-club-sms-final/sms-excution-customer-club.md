# SMS execution plan — Customer Club → Armaghan

Branch: **`feat-customer-club-armaghan`** (all repos). Spec: this folder (`README.md`, `CLAUDE.md`, `docs/`).

---

## Context

The customer-club product already ships end to end: `campaigns`, `club`, `wheel`, `surveys`, `radar`,
and `regional` all queue real sends through `SmsOutboxService.createBatch`, a dispatch cron drains the
outbox, and **Armaghan is already the live default provider** (`sms-provider.selection.ts` — OTP verified
against a real `sendParameterizedMessage`, IP whitelisted, Melipayamak kept only as an explicit opt-in).

What this package demands is therefore **not a rebuild — it's the hardening layer the current
implementation does not have**. Concretely, the gaps found in the code:

| Spec requirement | Today |
|---|---|
| Per-seller verified sender lines (`seller_sender_lines`) | `SENDER_LINE_POOL` — 10 hardcoded fake numbers; runtime uses one global `ARMAGHAN_ORIGINATOR` env |
| `sellerId` never trusted from browser | `/admin/stores/:storeId/sms/*` (and club/campaigns/wheel/surveys/radar) read `storeId` straight off the URL with **no ownership check** — any authenticated seller can read or send for any store |
| Versioned per-`feature_key` templates | `message_template` has a 9-value `category`, no feature key, no version, no active-version rule, no required-variable validation |
| Seller-scoped opt-out | `SmsRejectionReason.OPTED_OUT` exists in the enum and is **never produced** — no preferences table, no inbound handling |
| Idempotency keys on every business event | none on the SMS path (`wheel_spin` has one; SMS does not) |
| `sendMessageManyToMany` | not implemented — `ArmaghanProvider` groups by identical body and issues N × `sendMessageOneToMany` |
| `getUserInfo` / `getReceivedMessages` | not implemented |
| Signature + 320-char final validation | not implemented |
| Ambiguous post-transmission timeout ≠ retry | not implemented — any throw marks the recipient failed |
| Credit reserve/commit/release | credit is deducted at dispatch, never reserved; a batch can be created that can't be paid for |
| Delivery reports | poller exists, but no reference-count validation, no monotonic/terminal-state policy, no backoff, no report API |

Outcome: bring the existing pipeline up to this package's contract **without rewriting working product
logic**, one reviewable stage at a time.

### Decisions taken

- **Step-by-step.** One stage at a time; each stage is finished, verified, committed and pushed before
  the next begins. No big-bang branch.
- **One shared platform sender line for now.** Model `seller_sender_lines` properly and seed every store
  to the single `ARMAGHAN_ORIGINATOR`. Inbound routing by `destination` (`docs/17`) cannot work under a
  shared line — see the Blocker below.
- **Backend + admin UI** for surfaces whose data changes (sender line, templates, reports).
- **Tenant fix** = new `StoreOwnershipGuard` applied to customer-club admin controllers.

### Blocker to record, not to invent around

`docs/17-inbound-opt-out.md` routes an inbound reply to a seller via the `destination` (the line that
received it), and states routing is deterministic *because each seller has a dedicated line*. With one
shared platform originator that premise is false. Stage 6 therefore resolves the replying mobile to its
store membership(s) and, when it maps to more than one store, writes the reply to an **ops review
queue** rather than opting the wrong tenant out. This is a documented degradation, marked in the code
and in the `docs/18-launch-checklist.md` evidence, until dedicated per-seller originators are purchased.
`ARMAGHAN_OTP_TEMPLATE_ID` stays unused by all 14 features (`docs/19`).

---

## Working protocol per stage

1. Implement the stage's backend work; add/extend the spec files alongside (`*.spec.ts`, existing suites
   are the pattern — e.g. `sms-outbox.service.spec.ts`, `campaigns.service.spec.ts`).
2. Any new/changed shared type is authored **upstream first** in `manooch-fronts/packages/types`, then
   pulled into the backend with `npm run sync:types` + `npm run build` (backend `CLAUDE.md` — the
   vendored `manooch-backend/packages/types` is never hand-edited).
3. Every entity column change **ships a migration** in `src/migrations/` (prod runs
   `DB_MIGRATIONS_RUN=true`; dev is `synchronize`-managed and never runs them). Continue the timestamp
   series after `1786801600000`. `@Index(...)` always gets an explicit name as its first argument.
4. Frontend work for that stage in `manooch-fronts/apps/admin`, routes added to `lib/routes.ts`.
5. Gate: `npx tsc --noEmit && npm test && npm run lint` in each touched repo, all green, output shown.
6. Commit, push to `feat-customer-club-armaghan`, report, **stop** — next stage starts on your go.

Branch creation uses `git checkout -b feat-customer-club-armaghan` in each existing checkout (no
worktrees). The standing shutdown-on-push rule applies at the **final** stage, not after each
intermediate push.

---

## Stage 1 — Tenant isolation guard  *(card: FND-01 partial)*

Smallest, highest-value, unblocks the "never trust browser `sellerId`" rule everything else depends on.

- New `src/common/guards/store-ownership.guard.ts` — reads `storeId` from route params, resolves the
  caller via `req.customerId` (as `CustomerAuthGuard` sets it), delegates to the **existing**
  `StoresService.assertOwner(storeId, ownerId)` (`src/modules/stores/stores.service.ts:95`), which
  already throws `STORE_NOT_FOUND` / `STORE_FORBIDDEN` off `businesses.ownerId`.
- Apply with `@UseGuards(CustomerAuthGuard, StoreOwnershipGuard)` on the customer-club admin
  controllers: `sms/admin-sms.controller.ts`, `campaigns/admin-campaigns.controller.ts`,
  `campaigns/admin-message-templates.controller.ts`, `club/admin-club.controller.ts`,
  `wheel/`, `surveys/`, `radar/admin-radar.controller.ts`, `loyalty/admin-loyalty.controller.ts`,
  `customers/`.
- Super-admin/portal sessions must pass through untouched — mirror the carve-out
  `PlanEntitlementGuard` already makes for `tokenScope`.
- Tests: guard spec (owner passes, non-owner 403, missing store 404, super-admin passes) + one
  cross-store integration case per guarded controller family.
- Frontend: none.

## Stage 2 — Real seller sender lines  *(card: FND-03, `docs/02`)*

- New entity `seller_sender_lines`: `id`, `storeId`, `originator` **string** (never numeric),
  `label`, `providerAccountId`, `status` (`pending`/`verified`/`disabled`), `isDefault`, `isActive`,
  `verifiedAt`. Unique `(storeId, originator)`; partial unique index for one default active line per
  store (the `UQ_wheel_spin_store_idempotency` partial-index pattern in
  `1786801000000-AddWheel.ts` is the precedent).
- Migration seeds one row per existing store pointing at the shared `ARMAGHAN_ORIGINATOR`, status
  `verified`, `isDefault`. Migrate `sms_settings.senderLine` onto it.
- Super-admin API to register/verify/disable a line (an operator enters an already-approved
  originator — the app never generates one). Seller API: list (masked originator + internal id),
  set default, test-send. Test sends carry `isTest` and are excluded from campaign KPIs but audited
  and costed.
- **Delete `src/modules/sms/sender-lines.constants.ts`** and the `SENDER_LINE_POOL` endpoint.
- `ArmaghanProvider.sendBatch` stops reading `ARMAGHAN_ORIGINATOR` and takes a resolved originator
  from the caller; resolution order is feature-specific line → store's verified default →
  fail `SELLER_SENDER_NOT_CONFIGURED`. Never silently fall back to another store's line.
- `-103` on a line ⇒ disable it + operator alert; `-101`/`-110`/`-119` ⇒ pause the provider account.
- Frontend: `app/plugin/customer-club/setup/page.tsx` and `settings/` sender-line picker consume the
  real endpoint (routes in `lib/routes.ts:404`); fixture numbers disappear from the UI.

## Stage 3 — Complete the Armaghan v2 adapter  *(card: FND-02, `docs/01`)*

`ArmaghanClient` (`providers/armaghan.client.ts`) already does credential injection, redaction, the
18-digit `quoteLargeIntegers` guard, and `errorModel.errorCode` checking — extend, don't replace.

- Add `sendManyToMany` (equal-length `contents`/`destinations`, arrays derived from **one** array of
  recipient objects so indexes cannot drift), `getUserInfo`, `getReceivedMessages`.
- Extend `SmsProvider` (`providers/sms-provider.interface.ts`) with a per-recipient-body send so the
  outbox can pick one-to-many vs many-to-many instead of the current N-calls-grouped-by-body loop.
- Error classification table from `docs/01`: permanent request (`-105`), permanent recipient (`-107`),
  configuration (`-103`), account/operational (`-101`, `-104`, `-110`, `-119`), transient (`-201`).
  Backoff+jitter only for known-safe pre-transmission failures; **never** auto-retry a post-transmission
  timeout — mark the attempt `unknown`.
- Circuit breaker for account-level errors. Observability per `docs/01`: store, outbox, feature,
  operation, batch count, latency, HTTP status, provider code, masked reference count — no credentials,
  no full destinations, no full bodies.
- Tests extend `armaghan.client.spec.ts` / `armaghan.provider.spec.ts`: payload shape, every mapped
  error code, ambiguous timeout, array alignment across batch boundaries.

## Stage 4 — Versioned per-feature templates  *(cards: FND-04; `docs/03`, `docs/19`)*

- Extend `message_template` with `featureKey` (the 17 `LaunchFeatureKey` values from `docs/00`),
  `version`, `isActive`, `allowedVariables`/`requiredVariables` (jsonb), `createdBy`. Unique
  `(storeId, featureKey, version)`; one active version per `(storeId, featureKey)`. Keep `category` for
  the existing UI grouping.
- Platform default bodies per feature key; on feature enable, copy the default into the store's own
  template (extends the existing `MessageTemplatesService.ensureSeeded` +
  `message-template-seeds.data.ts`). Editing creates a **new version**; queued messages keep their
  snapshot; deactivation blocks new queueing but never rewrites history.
- Harden `MessageTemplatesService.render`: reject unknown tokens (already done at save time — also do
  it at render), reject missing required values, strip unsafe control chars, append the store
  signature, reject any unresolved `{...}`, enforce 320 chars **after** signature. Canonical English
  keys (`docs/03`) reconciled with today's `MESSAGE_TEMPLATE_VARIABLES` (`store_name`, `code`,
  `occasion` are missing; `discountCode` vs `discount_code` needs one spelling).
- Snapshot template id + version + rendered-body hash on the outbox row.
- Frontend: `app/plugin/customer-club/campaigns/templates/page.tsx` — feature-key grouping, version
  badge, preview, test send, live 320-char counter including signature.

## Stage 5 — Shared eligibility, opt-out, idempotency, credit  *(cards: FND-01, FND-05; `docs/00`)*

- New `customer_sms_preferences` (unique `(storeId, normalizedMobile)`, marketing opt-in/out, source,
  timestamp) and `sms_suppressions` (store/customer/feature key, window, reason).
- `sms_batches`/`sms_messages` gain `idempotencyKey` with a partial unique index scoped to non-null
  keys (same shape as `UQ_wheel_spin_store_idempotency`), plus `isTest`, `featureKey`, sender/template
  snapshot columns, and an ambiguous-submission flag.
- `SmsQuotaService.evaluate` (already the single rule authority — every send path calls it) gains the
  opt-out and suppression checks, finally producing the unused `SmsRejectionReason.OPTED_OUT`. It stays
  side-effect-free.
- `SmsOutboxService`: reserve app credit at batch creation and commit/release it at dispatch (today
  credit is only deducted at dispatch, so a batch can be created that cannot be paid); re-run
  `evaluate` immediately before the provider call; select one-to-many vs many-to-many from the
  rendered bodies; record exclusion reason per recipient.
- `normalizeIranianMobile` (`utils/normalize-mobile.ts`) becomes the canonical form used for dedupe,
  preferences, and cap counting — currently the provider normalizes but `SmsQuotaService` matches on
  a raw `^09\d{9}$`, so the two disagree on `+98`/`۰۹` input.
- Tests: opt-out-races-dispatch, replayed idempotency key, overlap dedupe, credit
  reserve/release reconciliation, Tehran-boundary cases (reuse `common/utils/tehran-time.util.ts`).

## Stage 6 — Inbound polling and reply-5 opt-out  *(card: SMS-14, `docs/17`)*

- `sms_inbound` table, unique `(providerAccountId, providerMessageId)`; per-account `afterId`
  checkpoint advanced only after the page's rows are durably inserted.
- Poller task alongside `SmsDispatchTask`, calling the Stage-3 `getReceivedMessages`.
- Parser: normalize Persian/Arabic/Latin digits, Unicode whitespace, punctuation, case; exact match on
  the reviewed command list (`5`, `۵`, `٥`, agreed stop words). **No substring matching.**
- Routing: `destination` → `seller_sender_lines`. Under the shared line (see Blocker) fall back to
  resolving the sending mobile's store membership; ambiguous or unknown ⇒ ops review queue, never a
  guessed opt-out.
- Opt-out transaction: upsert `customer_sms_preferences`, record source inbound id/time/rule, cancel
  that store's not-yet-submitted marketing recipients, commit.
- Raw inbound content access-restricted, mobiles masked in logs/UI, retention policy applied.

## Stage 7 — Real delivery reports  *(card: SMS-13, `docs/16`)*

- Reference ingestion: `errorCode == 0`, reference count == destination count (a mismatch is an
  integrity error, logged and failed — `ArmaghanProvider` already refuses to mis-attribute, keep that),
  every reference stored as a string, index-aligned to the recipient.
- Poller: non-terminal references only, configurable batch size/interval/max age, backoff as messages
  age, **monotonic** state updates so an out-of-order poll can't regress a terminal state, `unknown_final`
  after the poll SLA. Map `0/1/2/3/4/5/6/-100` per `docs/16`.
- Report API: `summary?from=&to=`, per-run report, per-message detail — every query filters store id
  **before** date/run filters. Counters per `docs/16` with an explicit delivery-rate denominator.
- Frontend: `app/plugin/customer-club/reports/page.tsx` replaces fixture percentages with the report API.

## Stages 8+ — Per-feature hardening, one card at a time  *(cards SMS-01 … SMS-12)*

Each is its own stage with its own gate; grouped here only for reading. Every one is "add the spec's
idempotency key, run/recipient records, preview API and acceptance tests to a path that already works":

1. **SMS-01 welcome / walk-in** (`docs/04`) — `welcome:{storeId}:{customerId}`, walk-in registration API,
   one-award guarantee (`CampaignTrigger.WELCOME` path in `campaigns.service.ts`).
2. **SMS-02 manual campaigns** (`docs/05`) — run/recipient tables, preview (gross/eligible/excluded/cost),
   schedule in Tehran local + UTC, cancel releases reservation.
3. **SMS-03 bulk** (`docs/06`) — segment-union query (never sum segment counts),
   estimate/run/cancel/detail/test.
4. **SMS-04 personal/direct** (`docs/07`) — customer / manual-mobile / segment modes,
   `personal:{storeId}:{clientCommandId}`, actor+reason audit on manual destinations.
5. **SMS-05 inactivity reminders** (`docs/08`) — rule table, `(rule, local run date)` lock, 30-day
   suppression, paid/completed orders only (today `resolveDaysSincePurchaseAudience` uses
   `MAX(createdAt)` over **all** orders regardless of status — that's a correctness bug this card fixes).
6. **SMS-06 birthday + custom occasions** (`docs/09`) — `birthday:{storeId}:{customerId}:{localYear}`,
   calendar/leap-day policy written down and tested (today's `resolveBirthdayAudience` matches Gregorian
   month/day on `Profile.birthDate`).
7. **SMS-07 points expiry** (`docs/10`) — point **lots** with remaining amounts (`points-expiry.task.ts` +
   `point-transaction.entity.ts` today work off aggregates), spend-race test, re-check before dispatch.
8. **SMS-08 retargeting** (`docs/11`) — `customer_credits` + `credit_notifications` ledgers, atomic
   grant+outbox.
9. **SMS-09 referral** (`docs/12`) — signed seller-scoped tokens, self-referral/abuse limits, one reward
   per `(referral, beneficiary, type)`.
10. **SMS-10 wheel** (`docs/13`) — signed invitation links, `wheel-winner:{spinId}` (`wheel_spin` already
    has a spin-level idempotency key to build on).
11. **SMS-11 survey** (`docs/14`) — signed tokens, one response + one reward, non-respondent reminder from
    the original run recipients.
12. **SMS-12 club redemption** (`docs/15`) — locked stock+points transaction,
    `(storeId, customerId, clientCommandId)`, resend reuses the original code and never re-redeems.

## Final stage — REL-01 launch evidence

Walk `docs/18-launch-checklist.md` and evidence each applicable box in staging against a
provider-approved test destination, including the 8-step per-seller smoke test. Then the standing
shutdown rule applies.

---

## Verification

Per stage, in every touched repo:

```bash
# manooch-backend
npx tsc --noEmit && npm test && npm run lint
# manooch-fronts
pnpm -w typecheck && pnpm -w test && pnpm -w lint
```

Real-send checks (never with `SMS_ENABLED` unset — that routes to `FakeSmsProvider`, which is the
correct default for dev and for the whole unit suite):

- **Stage 2**: register the shared originator for one test store, run the test-send endpoint to an
  authorized mobile, expect `errorCode: 0` + a string reference; confirm a second store cannot list,
  select, or test that line (403).
- **Stage 3**: one identical-body one-to-many send and one personalized many-to-many send; verify each
  reference maps to the right destination by index.
- **Stage 5**: opt a mobile out, queue a marketing batch, confirm it is rejected with `opted_out` at
  both queue time and immediately before dispatch.
- **Stage 6**: reply `5` (and `۵`, `٥`) to the line, confirm one opt-out, one processed inbound row per
  provider id, and that a second store's consent for the same mobile is untouched.
- **Stage 7**: poll a real send to a terminal state; confirm an out-of-order poll cannot regress it and
  that report totals reconcile with recipient rows.

Migrations are authored for prod and never run against dev (dev is `synchronize`-managed). Before each
push, confirm no credential, full mobile, or full message body appears in any log line added.
