# Customer Loyalty Club — Remaining Phases and Delivery Status

**Version:** 3.1 — **Updated:** 27 Mordad 1405 (2026-08-18) — **Status:** In progress on `feat-customer-club`

> This file replaces the prior "Version 2.0 — Closed — Phases 1–4 complete" status. That status was
> incorrect: git history shows only `feature/customer-club-phase1` was ever merged to `main` in
> `manooch-backend` and `manooch-fronts` — 10 of the prototype's 22 views. No code for the remaining
> views existed before `feat-customer-club` was branched. This file tracks real, git-verified
> progress against that branch across all three repos, following the staged plan agreed when the
> branch was scoped.

The product baseline is [`PRD.md`](./PRD.md). Its "Delivered / as-built baseline" status line and
4-of-4-phases table describe the same incorrect state this file used to — they are due for the same
correction in the docs pass that produced this update (see §6). The prototype
[`customer-club-admin.html`](./customer-club-admin.html) outranks the PRD wherever the two disagree —
decided when `feat-customer-club` was scoped, since the prototype is itself ahead of its own PRD (see
§1).

---

## 1. What changed in the prototype since the old status was written

`customer-club-admin.html` gained a view and six modals, and had its pricing model rewritten, in a
commit (`81fee16` in this repo) newer than any of the "closed" documentation above described:

- **Views: 21 → 22** — a `view-setup` activation wizard was added (4-step: profile → plan → sender
  line → activation). Not present in PRD.md, README.md, or the old version of this file.
- **Modals: 13 → 19** — added `modal-profile`, `modal-pay`, `modal-ai` (AI-assisted club setup),
  `sms-sheet` (SMS credit purchase), `modal-ps` (personal message inside bulk SMS), `modal-kbd`
  (walk-in registration keypad).
- **Pricing model rewritten**: the three-tier plan (رایگان/پایه/حرفه‌ای) became a single
  ۲۹۰٬۰۰۰ Toman/month "باشگاه مشتریان" plan. There is no unlimited-SMS tier — SMS is a separately
  purchased credit basket at any plan level.
- **`manooch-dashboard.html`** — a second prototype file, the admin app's main dashboard (Figma node
  `38:1186`), which is the entry point into the club and is therefore in scope for this branch.

---

## 2. Status by stage

| Stage | Scope | Status |
|---|---|---:|
| 0 | Branch setup across all 3 repos, billing-model decision (§3) | Done |
| 1 | Setup wizard (`view-setup`) + SMS credit purchase UI | **Done** |
| 2 | Club shop (items, redemption, purchase history, settings) | **Done** |
| 3a | Loyalty tools: wheel, surveys | **Done** |
| 3b | Loyalty tools: occasions, retargeting | Not started |
| 4 | Acquisition (referral/lead magnet) & segmentation | Not started |
| 5 | Geography: radar, regional SMS | Not started |
| 6 | Personal message, walk-in keypad, dashboard rebuild | Not started |
| 7 | Docs reconciliation (this file, then PRD.md, README.md) | In progress (this update) |

### Phase 1 baseline (pre-existing — merged to `main` before this branch)

Delivered as `feature/customer-club-phase1` in both `manooch-backend` and `manooch-fronts`:
`dashboard`, `reports`, `campaigns`, `templates`, `smsgroup`, `tools`, `reminders`, `members`,
`points`, `settings` — 10 views. This is the only part of the old "4 phases complete" claim that was
actually true; everything below it is new work on `feat-customer-club`.

### Stage 1 — Setup wizard + SMS purchase UI — Done

- **Backend** (`manooch-backend`, commit `d9355d2`): `senderLine` column on `sms_settings` +
  migration, `GET .../sms/sender-lines` endpoint, sender-line constants.
- **Frontend** (`manooch-fronts`, commit `81e4d78`): 4-step setup wizard at
  `plugin/customer-club/setup`, an unactivated-store redirect gate in `plugin/layout.tsx`, and
  `SmsCreditSheet` (6 packages + custom-amount calculator, `floor(amount/400)`, sub-400 Toman
  rejected) wired to the dashboard's `#btn-credit` button.
- Both the plan step and the SMS purchase sheet are **UI-only** — activation flips
  `StorePlugin.isActive`, no real charge. See §3.
- Verified live via Playwright against a real backend+DB; full backend test suite green after an
  incidental fix to a pre-existing `SmsQuotaService.updateSettings` bug (blind `Object.assign` of a
  DTO instance onto a loaded entity silently dropped untouched fields from the API response — the DB
  row itself was never corrupted).

### Stage 2 — Club — Done

- **Backend** (`manooch-backend`, commit `fd3a9f3`): new `club` module — `ClubItem`, `ClubPurchase`,
  `ClubSettings` entities, DTOs, `ClubService`, `AdminClubController`, migration. Redemption is one
  atomic transaction: item/stock check → Tehran-day daily-cap check → point spend → stock decrement
  → purchase insert with a generated unique `CLB-XXXX` code → commit → post-commit SMS confirmation.
  A new `LoyaltyService.spendWithinManager` lets the club's own transaction share the point spend
  instead of `LoyaltyService.spend()` opening a second, un-nestable one.
- **"حداقل امتیاز برای خرید از کلاب" is not a club-specific field** — it reuses the existing
  `LoyaltyPolicy.minimumRedemptionPoints`, which `LoyaltyService.spend()`/`spendWithinManager()`
  already enforce for every non-manual spend. This is a deliberate divergence from the prototype's
  flat data model, made to avoid two competing "minimum points" settings.
- **Frontend** (`manooch-fronts`, commit `f3f658d`): `club/page.tsx` (items/history/settings 3-pane,
  porting `view-club`) and `club/preview/page.tsx` (customer shop preview, porting
  `view-club-customer`, **with a real customer picker** — the prototype hardcodes one demo customer,
  which doesn't work for an admin tool with no logged-in customer session).
  Item images use real upload (`useUploadAsset`) rather than the prototype's base64 blob.
  Confirmation-SMS tokens are the fixed Persian set `{نام}`/`{ایتم}`/`{امتیاز}`/`{کد}`, matching the
  prototype exactly (not the campaigns module's English-token composer).
- Verified live: 3 successful redemptions (balance/stock/stats/history all correct, confirmation SMS
  body verified in the outbox), a 4th correctly rejected on the daily cap with **zero balance/stock
  change** — atomicity confirmed against a real database, not only against mocks. 6 new unit tests;
  full backend suite (868/868) green.
- Incidentally found and fixed the identical `Object.assign` bug from Stage 1, this time in
  `LoyaltyService.updatePolicy`. The same pattern exists, unfixed, in ~17 other backend services
  outside this branch's scope (see the branch's own tracking notes) — a candidate for a dedicated
  cleanup pass, not reopened here.

### Stage 3a — Loyalty tools: wheel + surveys — Done

- **Backend** (`manooch-backend`, uncommitted on `feat-customer-club` at time of writing): new
  `wheel` and `surveys` modules — `Wheel`/`WheelPrize`/`WheelSpin`/`WheelSettings` and
  `Survey`/`SurveyOption`/`SurveyResponse`/`SurveySettings` entities, DTOs, services, admin
  controllers, two migrations (`AddWheel`, `AddSurveys`). A wheel spin and a survey response are
  each one atomic transaction, following the Stage 2 `ClubService.redeem` shape: validation →
  Tehran-day daily-cap / single-response check → point spend or award via the new
  `LoyaltyService.earnWithinManager` (see §4.3) → ledger row → commit → post-commit SMS. Prizes and
  survey options are child tables, not JSONB, so a spin/response can reference exactly which row it
  hit and so winners/results can be read back with a real `COUNT(*)`, fixing two prototype defects
  (spin counts and winner lists that never actually persisted — divergences 3–4 in the design plan).
- `PointReason.WHEEL` is exempt from `LoyaltyPolicy.minimumRedemptionPoints` (the floor is a
  redemption rule for the club shop; a wheel entry is a small recurring cost) — the exemption set
  that already carried `MANUAL_ADJUST` for this reason now also carries `WHEEL`, with a regression
  test proving `CLUB_REDEEM` still hits the floor.
- VIP free spins key off `LoyaltySegment.VIP` (a new public `CustomersService.getCustomerSegment`
  single-customer read), not `LoyaltyTier` — matching the prototype's VIP/وفادار/تازه‌وارد/در خطر ریزش
  audience chips, which are segments everywhere else in the app.
- `SmsOutboxService.createBatch` gained an optional per-recipient `body` override (Step B0) so a
  survey invite to N recipients can render `{نام}` per customer instead of one shared body across a
  batch, without falling back to Stage 2's one-batch-per-recipient workaround.
- **Frontend** (`manooch-fronts`, uncommitted on `feat-customer-club` at time of writing):
  `tools/wheel` (4-pane: wheels/spin/winners/settings, SVG wheel with the prototype's 4s spin easing,
  a local-only "چرخش آزمایشی" preview plus a real `tools/wheel/preview` sub-route that calls the
  transactional spin endpoint) and `tools/surveys` (3-pane: list/settings/history, a real survey
  detail view with result bars, and a `tools/surveys/[id]/preview` sub-route for the transactional
  respond endpoint) — both preview sub-routes are the same admin-side stand-in pattern Stage 2's
  `club/preview` established, since there is still no customer-facing app. Wired into
  `dashboard/_common/QuickActionsRow.tsx` and `tools/page.tsx` (previously both fired a
  "coming soon" toast for these two tools).
- All fourteen prototype divergences called out in the design plan were implemented as scoped
  (persisted prize colors, real spin/response counts, FK-based winner joins instead of name-string
  matching, count-before-sum prize validation, cash "toman" entry modeled but rejected with
  `WHEEL_TOMAN_ENTRY_UNSUPPORTED` since no payment gateway exists yet, etc.) — see the plan document
  for the full table; not reproduced here since none of them changed during implementation.
- **Verified live** via Playwright against a real local backend + Postgres (not mocks), the full
  8-step smoke script from the plan's verification section: chance-sum and prize-count validation
  order, a real spin with correct balance/point movement and a non-zero persisted spin/winner count,
  a daily-cap rejection with zero balance change and zero new rows, a VIP free spin, winner SMS
  presence, a scheduled survey invite with correct per-recipient SMS bodies, and a survey response
  cycle (reward once, percentages recompute, second response from the same customer rejected). This
  live pass is what surfaced the three real bugs below — unit tests, full suite, lint, and build were
  all green throughout and did not catch any of them, matching the pattern already seen in Stages 1–2.
- **Bugs found and fixed during live verification** (all three confirmed via targeted module tests,
  the full backend suite, lint, build, and a live re-test after each fix):
  1. **Wheel/survey create & update returned a bare entity, not the joined response shape.**
     `WheelService.createWheel`/`updateWheel` and `SurveyService.createSurvey`/`updateSurvey`
     returned the raw TypeORM row, missing `prizes`/`spinCount`/`winnerCount` (wheel) or `options`
     (survey) that the frontend's Zod response schemas require — a non-fatal "Response validation
     drift" warning in both cases, and a hard crash on wheel create (`.length` read on `undefined`
     prizes). Fixed by having both wheel methods re-read through the existing `getWheel` after their
     transaction commits, and by adding a `getSurveyWithOptions` helper for survey's update path
     (and returning the transaction's own inserted options directly on create, avoiding an extra
     query). Same root cause both times — a service returning less than its own response schema
     promises — worth checking for on any future admin mutation endpoint.
  2. **`Between()` daily-cap query silently used the wrong timezone off the production container.**
     `node-postgres` serializes a JS `Date` bound to a `timestamp without time zone` column using the
     Node process's *local OS timezone*, not UTC, while Postgres's own `now()` (used by
     `@CreateDateColumn()` defaults, DB session already `TimeZone=UTC`) writes UTC-naive values. On
     any host where the Node process isn't itself pinned to UTC, every `Between(start, end)`-style
     date-range query against such a column — the wheel daily-cap count, and by the same pattern
     `getStats`'s `spinsToday`/`spinsYesterday` — silently shifts by the local UTC offset, undercounting
     or overcounting rows. This only ever "worked" in production by coincidence (the container
     defaults to UTC per `manooch-backend/CLAUDE.md`), never as an enforced invariant, and would
     misbehave identically for anyone developing from a non-UTC machine. Fixed by pinning
     `process.env.TZ = 'UTC'` at the top of `bootstrap()` in `main.ts`, before any DB call runs —
     this is a process-wide fix, not scoped to the wheel module, so it protects every existing and
     future `Between()`-over-timestamp query in the codebase, not only Stage 3a's.
  3. A pre-existing, **out-of-scope** UI defect was observed but deliberately left unfixed: the FAB's
     container (`ClubFab.tsx`) sits at `z-45` while `ClubTabBar`'s nav sits at `z-50`; the FAB
     visually pokes above the nav but the nav's fixed positioning intercepts real pointer events in
     the ~10px overlap, so a real click on the FAB across the whole customer-club section (not just
     the two new tools) lands on the nav underneath instead. Testing worked around this with a direct
     DOM `.click()`. This is shared chrome predating Stage 3a — flagging here for a decision on
     whether to fix it as its own small pass, since it affects every existing view, not filing a fix
     unilaterally.
- Test counts: `wheel.service.spec.ts` (23/23), `surveys` module tests (17/17), full backend suite
  (922/922) green, lint 0 errors (unchanged 56-warning baseline), build clean in both repos.

### Stages 3b–7 — Not started

Per the plan, in order:

- **Stage 3b — loyalty tools**: `occasions` (birthday seeded/non-deletable + custom, built on the
  existing `campaigns` module), `buyback`/retargeting (return-credit rules, transactional cashback
  grants).
- **Stage 4 — acquisition & segmentation**: `acquire` (referral 500/250, lead magnet, 15%
  first-purchase code), `segments` (Bronze/Silver/Gold/Diamond + RFM with server-side configurable
  thresholds).
- **Stage 5 — geography**: `zones`/radar (point/circle 200–3000m + polygon 3–10 vertices, 24-hour
  suppression — automatic triggering stays gated behind the still-absent customer-app location
  source), `regional` (province → city → neighborhood, quota N ≤ M enforced, random non-repeating
  selection).
- **Stage 6 — prototype extras + dashboard**: `modal-ps` (personal message inside bulk SMS),
  `modal-kbd` (walk-in registration keypad), and rebuilding the admin main dashboard to
  `manooch-dashboard.html` (Figma `38:1186`).
- **Stage 7 — docs**: this file (done by this update), then PRD.md (§6.2 view/modal counts, pricing
  model, remove the "credit top-up is outside v1" claim it no longer needs since Stage 1 shipped the
  purchase UI), and README.md (same counts, plus the dangling `readme-en.md` reference noted in §6).

---

## 3. Billing decision carried forward from Stage 0

`subscriptions` (`SellerSubscription`, `PlanTier` = basic/economy/advanced) is a whole-store tier
system where a seller has exactly one effective tier, resolved by BASE+OVERLAY date math. The club's
۲۹۰٬۰۰۰/month plan is a **per-plugin add-on**, not a store tier — adding a 4th `PlanTier` would
compete with the seller's real tier and break the one-active-tier invariant other code relies on.

**Real billing is deferred.** The setup wizard's plan/pay step and the SMS purchase sheet are
UI-only; activation flips `StorePlugin.isActive` directly, no billing entity, no real charge. This
mirrors the existing pattern in `SmsCreditAccount` (manual top-up until a gateway lands). Revisit once
a payment gateway is wired up — Zarinpal is the internal candidate
(`manooch-planning/core/zarinpal/`).

---

## 4. Engineering decisions that remain in force

These apply to all remaining stages, not just what has shipped so far.

### 4.1 Reminders are campaigns, not a separate backend module

A reminder rule is a `DAYS_SINCE_PURCHASE` campaign with a linked message template. Occasions
(Stage 3) follow the same shape. Do not introduce a second scheduler or duplicate quota path.

### 4.2 All business-time logic uses an explicit Tehran-time utility

Never use server-local `Date#getHours()`/`setHours()` for business rules. Birthday matching, occasion
times, reminder windows, points expiry, retargeting deadlines, wheel windows, survey reminders, club
daily-cap boundaries, and radar suppression all use `tehran-time.util.ts`'s `getTehranDayRange`, with
at least one `TZ=UTC` test per rule.

### 4.3 Multi-record financial/value writes are transactional

One `QueryRunner` transaction, no partial writes on failure, for: club stock + points + purchase +
code (shipped, Stage 2); wheel cost/reward + spin/prize result (shipped, Stage 3a); survey reward +
response + option count (shipped, Stage 3a); cashback/retargeting credit (Stage 3b); SMS credit
deduction + batch/message creation (existing); any reward that also updates a campaign/referral
record (Stage 4). `LoyaltyService.spendWithinManager` (added in Stage 2) is the reusable pattern for
"share my transaction with a points spend"; `LoyaltyService.earnWithinManager` (added in Stage 3a)
is its award-side counterpart — same contract (`LOYALTY_INVALID_AMOUNT`, `LOYALTY_MEMBER_NOT_FOUND`,
`referenceId` idempotency looked up inside the same manager before crediting), used by the wheel's
participation-points award and the survey's response reward. Use one of these two rather than opening
a second `QueryRunner`.

### 4.4 Server authority is mandatory

The server validates balances, stock, quota, opt-out, eligibility, chance totals, reward uniqueness,
regional quota, tokens, and date windows. Client validation is UX support, not authority.

### 4.5 Shared implementation conventions

**Backend**
- Soft delete (`@DeleteDateColumn`) for deletable records; append-only ledgers (points, SMS, club
  purchases) deliberately omit it, with a comment explaining why.
- Decimal transformer for money columns; `@Index()` always takes an explicit name.
- Localized error codes in `src/i18n/fa/errors.json` (key = the raw exception message) and success
  messages via `@SuccessMessage`.
- Test-first for money, credit, points, and chance/award logic.
- Before blindly `Object.assign(entity, dto)`-ing a class-validator DTO onto a loaded entity: don't.
  Undeclared fields on the DTO instance materialize as own `undefined` properties (class-transformer
  + `transform: true`), so a blind assign overwrites real values with `undefined` and truncates the
  JSON response even though TypeORM's own SQL builder skips `undefined` columns on the actual UPDATE.
  Iterate `Object.entries(patch)` and only assign keys where `value !== undefined`. Confirmed present
  in `SmsQuotaService`/`LoyaltyService` (fixed) and, unfixed, in ~17 other services — check before
  reusing a pattern you find elsewhere in this codebase.

**Shared types**
- Author in `manooch-fronts/packages/types/src/<module>/` first, then `npm run sync:types` in
  `manooch-backend`. Never hand-edit the vendored backend copy.
- When one endpoint returns a base shape and another returns the same shape plus a batch join (e.g.
  a raw purchase vs. a purchase joined with customer name/mobile), model that as two schemas — a base
  and an `X...WithCustomer` extension — rather than making the joined fields optional on one schema.
  `@manooch/types/loyalty`'s `PointTransactionSchema`/`AdminPointTransactionSchema` split is the
  precedent; `@manooch/types/club`'s `ClubPurchaseSchema`/`ClubPurchaseWithCustomerSchema` follows it.

**Frontend**
- RTL review before final layout classes; 390×844 is the reference viewport.
- Match the final HTML inside app bar, title block, screens, FAB, tab bar, toasts, and modals — the
  nav shell (`_common/clubViews.ts`, `ClubAppBar`, `ClubTabBar`, `ClubFab`) already models all 22
  views; only `page.tsx` files are missing for the unbuilt stages, do not rebuild the shell.
- Exclude decorative `.stage`, `.phone`, `.island`, and `.statusbar` prototype chrome from production.

---

## 5. Verification per stage

- **Backend:** full `npm test` in `manooch-backend`, plus a stage-specific suite for anything touching
  money/points/chance logic.
- **Frontend:** `pnpm turbo run typecheck`/`lint`/`build --filter=@manooch/admin`.
- **Visual:** compare each new view against the prototype at 390×844 — RTL, Persian numerals, card
  order, copy.
- **Live:** Playwright against a real local backend+DB, not just mocks — this caught real bugs in
  every stage that has shipped so far (§Stage 1, §Stage 2, §Stage 3a) that unit tests alone did not:
  response-serialization defects (bare-entity returns missing joined fields) in Stages 1, 2, and 3a,
  and — new in Stage 3a — a systemic date-serialization bug (`pg`'s local-timezone `Date` handling
  vs. UTC-naive `timestamp` columns) that only a real, non-UTC-pinned process could expose.

Critical flows still to smoke once Stages 3–5 land: wheel rejects any chance total ≠ 100 and never
double-charges or double-awards; survey/referral rewards are single-award and cap-aware; radar
24-hour suppression and polygon vertex validation; regional quota N cannot exceed M and selection is
random and non-repeating; out-of-hours/daily-cap/opt-out/invalid-number sends deduct no credit.

---

## 6. Known documentation debt (to close out in Stage 7)

- **PRD.md** — "Status: Delivered / as-built baseline" and its phase-completion table describe the
  same incorrect "already shipped" state this file used to. Needs the same correction: 22 views / 19
  modals (not 21/13), the single ۲۹۰٬۰۰۰ plan (not three tiers), and an accurate stage-status table
  instead of "complete."
- **README.md** — same view/modal counts to fix, and it references a `readme-en.md` file that does
  not exist anywhere in this directory. Either that file was lost at some point, or the reference was
  never resolved. Restore it or remove the reference — don't leave a dangling link in Stage 7's pass.
- **`PRD-باشگاه-مشتریان.md`** — the original approved Persian PRD, still the source for product
  intent/terminology per PRD.md's own source-of-truth order; not touched by this update, review it
  for the same stale-status issue when PRD.md is corrected.
