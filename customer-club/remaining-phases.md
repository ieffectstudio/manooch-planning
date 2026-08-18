# Customer Loyalty Club — Remaining Phases and Delivery Status

**Version:** 3.4 — **Updated:** 27 Mordad 1405 (2026-08-18) — **Status:** In progress on `feat-customer-club`

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
| 3b | Loyalty tools: occasions, retargeting | **Done** |
| 4a | Segmentation (امتیاز / RFM / برچسب‌ها) | **Done** |
| 4c | Design parity with the prototype (tokens, shell, per-view sweep) | **Done** |
| 4b | Acquisition (referral/lead magnet) | **Done** |
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

### Stage 3b — Loyalty tools: occasions + retargeting — Done

- **The unifying decision**: neither tool got a new backend module. Both are configurations of one
  new campaign capability — *a campaign send can also grant points, with a per-recipient body* —
  riding the existing `campaigns` module and its `/admin/stores/:storeId/campaigns` /
  `/message-templates` endpoints. No new controller, route, settings entity, or cron, honouring
  §4.1's no-second-scheduler rule. Reminders and retargeting are both `DAYS_SINCE_PURCHASE`
  campaigns told apart by `config.linkedToolKey` (`'retargeting'` vs. unset) — see §4.1.
- **Backend** (`manooch-backend`, uncommitted on `feat-customer-club` at time of writing): added
  `OCCASION` to `CampaignTrigger` and `giftPoints`/`occasionAt`/`segment` to `CampaignConfig`
  (`@manooch/types`, synced), a migration widening `campaign_trigger_enum` and
  `point_transaction_reason_enum` (`occasion`, `retarget` — irreversible per Postgres `ALTER TYPE …
  ADD VALUE`, documented in the migration file). `CampaignsService.runDueCampaigns` gained a real
  dispatch over `DAYS_SINCE_PURCHASE` (unchanged), `BIRTHDAY` (new — audience resolved by joining
  `Profile.birthDate` month/day against Tehran-local today, scoped to the store via
  `store_customer_status`), and `OCCASION` (new — fires once when `config.occasionAt` falls in
  today's Tehran day range, audience is the whole store filtered by `config.segment`). Points grant
  through `LoyaltyService.earn` with `referenceId: '{campaignId}:{tehranDayKey}'` before the SMS
  batch is queued, so the message never promises points that failed to land — see §4.3.
- **Frontend** (`manooch-fronts`, uncommitted on `feat-customer-club` at time of writing):
  `tools/occasions` (2-pane: rules/history — birthday row toggled via the pre-seeded BIRTHDAY-category
  template, custom occasions via a create/edit sheet with date/time/segment/gift-points/SMS composer,
  default birthday rule's delete button hidden rather than rejecting) and `tools/retargeting`
  (3-pane: rule/settings/history — one rule per store, quick-activate on first toggle with sane
  defaults since there is no seeded template to reuse). Both mirror `tools/reminders`' campaign-backed
  shape. Wired into `tools/page.tsx` cards, `campaigns/page.tsx`'s «ساختار» pane (also fixing two
  stale Stage 3a rows — گردونه شانس and نظرسنجی — that still toasted "coming soon" instead of
  navigating), and `dashboard/_common/QuickActionsRow.tsx`'s retargeting action.
- **Divergences from the prototype** (all deliberate — full 18-row table in the design plan; the
  headline ones): Toman "cashback" credit replaced with points throughout, since nothing in the
  codebase spends a discount code at checkout (`CartService.checkout` hardcodes `discountAmount: 0`);
  `{کد تخفیف}`/`{discountCode}` tokens dropped for the same reason; the occasion enable/disable
  switch — dead in the prototype (`$$('.switch input')` bound once before `#occ-list` existed) — is
  now a real `PATCH .../campaigns/:id/active` call; editing a disabled occasion preserves `isActive`
  instead of the prototype's hardcoded `active: true` on save; occasion history is real `SmsMessage`
  rows keyed by `campaignId`, not a 1:1 rule mapping that showed ۰ ارسال for a brand-new rule.
- **Incidental fixes surfaced while building the runner dispatch**: `CampaignsService.update` and
  `MessageTemplatesService.update` both carried the same blind-`Object.assign` bug documented in
  §4.5 (fixed, same `Object.entries` + `!== undefined` pattern as Stages 1–2); per-recipient SMS
  bodies now render `{name}` per customer instead of literally, a standing limitation the runner's own
  doc comment had flagged as stale; campaign recipients now pass `customerLastVisitAt` into
  `createBatch`, newly activating `SmsQuotaService`'s inactive-customer rule for campaign sends (it
  was silently disabled before, since the campaign path omitted the field — surveys already passed
  it); a missing `faNum()` Persian-digit wrap on `campaign.config.dayOffset` was found and fixed in
  three places, including one **pre-existing, already-shipped** instance in `tools/reminders/page.tsx`
  (noticed only because the same pattern was copied into the new retargeting code).
- **Verified live** via Playwright against a real local backend + Postgres, the plan's 8-step smoke
  script: an occasion dated today sent, granted exactly `giftPoints` once, and rendered a real
  per-customer `{name}` (an empty-string render for the two dev-seed customers was confirmed as a
  genuine data artifact — no `name` set — not a code bug); a same-day re-run of the scheduler sent
  zero additional batches (both for the occasion and, separately, for the birthday trigger — proving
  `referenceId` idempotency holds per-trigger); an occasion dated tomorrow did not fire today; a
  customer's `Profile.birthDate` set to today's month/day was picked up by the birthday rule, a
  non-matching date was not; toggling an occasion or the retargeting rule off persisted across a
  reload; editing a disabled occasion and saving kept it disabled; the retargeting rule's
  `linkedToolKey` correctly isolated it from `tools/reminders`' own list at the same trigger; and all
  three previously-stale «ساختار» pane rows (retargeting, wheel, survey) now navigate instead of
  toasting. Deleting a custom occasion was exercised as part of cleanup and confirmed working end to
  end (soft-delete, list refresh, confirmation toast).
- **A real, live-only bug found and fixed**: `resolveBirthdayAudience`'s join between
  `store_customer_status.customerId` (bare `@Column()`, defaults to varchar) and `Profile.customerId`
  (`@Column({ type: 'uuid' })`) failed with `operator does not exist: character varying = uuid` —
  Postgres has no implicit varchar=uuid cast. Both columns ultimately reference the same
  `Customer.id`, but this is the first query in the codebase to join them directly in raw SQL rather
  than binding one as a parameter. `campaigns.service.spec.ts` mocks the TypeORM query builder, so the
  full unit suite (939/939) never executed real SQL and could not have caught this — exactly the
  defect class the plan's live-verification step exists for. Fixed with an explicit `::uuid` cast in
  the join condition, with a doc comment explaining why.
- Test counts: `campaigns` module tests 28/28, full backend suite 939/939 green, lint 0 errors
  (unchanged 56-warning baseline), build clean in both repos.

### Stage 4a — Customer segmentation (امتیاز / RFM / برچسب‌ها) — Done

- **The reuse decision**: segmentation shipped as a read-model on the existing `reports` module —
  one new endpoint (`GET .../reports/segmentation`), three new columns on the existing
  `LoyaltyPolicy` row, two pure classifier utils, and three new filters on the existing
  `listCustomers` query. No new module, controller, entity, cron, or settings table, extending
  §4.1's rule. Customer tags reused `Category` rows of `type: CUSTOMER` (already CRUD'd by the
  products module) with `parentId` as the group relation — zero schema change. Tag *assignment*
  reused the existing `PATCH .../customers/:id`, though (see incidental fixes) that endpoint's DTO
  didn't actually accept `categoryIds` yet.
- **Backend** (`manooch-backend`, uncommitted on `feat-customer-club` at time of writing):
  `LoyaltyPolicy` gained `silverFromPoints`/`goldFromPoints`/`diamondFromPoints` (defaults
  500/1500/3000) via an additive migration; `classifyTier(balance, policy)`
  (`loyalty/classify-tier.util.ts`) is the pure, unit-tested authority for tier, mirroring
  `classifySegment`'s shape, with `LoyaltyMember.tier` kept as a cached projection written alongside
  `balance` inside `earnWithinTransaction`/`spendWithinTransaction` — the column had been `BRONZE`
  for every member since it was added, since nothing had ever written to it. `reports/rfm.util.ts`
  (`scoreRfm`/`classifyRfmSegment`) buckets R/F/M from `ReportsService.baseOrderQuery` (PAID orders
  only, lifetime window) into the prototype's own edges and five named segments
  (قهرمانان/وفادار/در خطر ریزش/مشتری جدید/خفته).
  `ReportsService.getSegmentation` composes one order aggregate, one `LoyaltyMember` read, and one
  tag-count join into counts and distributions only — no customer array — landing on
  `AdminReportsController`. `ListCustomersQueryDto` gained `tier`/`categoryId`/`rfmSegment` filters,
  the last guarded behind one extra aggregate query only when present.
- **Frontend** (`manooch-fronts`, uncommitted on `feat-customer-club` at time of writing):
  `customers/segments/page.tsx` (3-pane `ClubTabsCtl`: امتیاز/RFM/برچسب‌ها)
  replacing the members page's `comingSoon` entry card with a real link;
  `ScoreSegmentsPane`+`ScoreThresholdsCard` (real tier counts, editable thresholds); `RfmPane`
  (R/F/M sub-tabs with real distribution bars and the five named segment rows, an honest empty
  state instead of `NaN` on a store with no PAID orders); `TagsPane`+`TagCreateCard`+
  `TaggedMembersCard` (real tag CRUD with confirm-delete, group `<select>` backed by parent
  categories); a URL-driven drill-down on `customers/page.tsx` (`?tier=`/`?categoryId=`/
  `?rfmSegment=`) with a clear-filter banner, wrapped in `Suspense` per Next's `useSearchParams()`
  requirement. `ResultBars.tsx` (Stage 3a) was lifted into a shared `_common/ui/ClubBarRows.tsx` so
  the survey detail view and the RFM pane don't carry two bar implementations.
- **Divergences from the prototype** (11 total, all deliberate — full table in the design plan; the
  headline ones): every number in `view-segments` was a hardcoded literal with no server call
  behind it (score counts, RFM distributions/segment scores, tag list, tag members) — all now real;
  score tiers existed nowhere server-side (`LoyaltyMember.tier` dead since the column was added)
  and are now computed and kept in sync; «مشاهده»/«هدف‌گیری» carried `data-goto="members"` but
  applied no filter — now real filtered navigation; tag delete fired immediately with no confirm
  and no server call — now a confirm dialog plus a real `DELETE`; the group `<select>` was five
  hardcoded options bound to nothing — now real parent categories.
- **Incidental fix**: the plan assumed `PATCH .../customers/:id` already wrote `categoryIds`
  (Stage 3b's `createCustomer` already had initial-tag write); reading the service showed the
  *update* path never gained the field. Added `categoryIds?: string[]` to `UpdateCustomerDto` with
  replace-set semantics (same contract as create) plus the response shaping needed to satisfy the
  same `AdminCustomer` Zod shape the list endpoint returns, since the member sheet's tag toggle
  calls this PATCH directly and validates against that schema.
- **Verified live** via Playwright against a real local backend + Postgres, the plan's 8-step smoke
  script: segments page navigates from the members-page card instead of toasting; the score tab's
  four tier counts sum correctly with real balances; a threshold edit (1500→1200) moved counts and
  ranges live and reverted cleanly; the RFM tab rendered real (zeroed, non-NaN) buckets on a store
  with no PAID orders; tag create persisted across reload; assigning a tag via the member sheet
  PATCHed 200 with the full `AdminCustomer` shape and incremented the tag's chip count; the
  tagged-members card listed exactly that customer; delete showed a confirm dialog, cancel
  preserved the tag, accept removed it with a toast; «مشاهده» navigated to `?tier=silver` with a
  working clear-filter banner. This live pass is what surfaced the bug below — unit tests, full
  suite, lint, and build were all green throughout and did not catch it, extending the pattern from
  every prior stage.
- **A real, live-only bug found and fixed**: `getTagCounts`'s parent-category join cast
  `Category.parentId` to `::text` on the same precedent as the `categoryId` join beside it
  (`customer_categories.categoryId` is a bare varchar with no FK) — but `parentId` is declared with
  a plain `@Column()` *and* a `@ManyToOne`/`@JoinColumn` onto the same property name, and TypeORM
  lets the relation win the physical column type: `parentId` is a real `uuid` column in Postgres.
  The cast produced `operator does not exist: text = uuid` on first live boot of the endpoint.
  `reports.service.spec.ts` mocks the query builder, so the full unit suite (979/979) never executed
  the real SQL and could not have caught this — the same defect class as Stage 3b's varchar/uuid
  join, now on the opposite side of a lookalike column. Fixed by dropping the cast on the parent
  join only, with a doc comment explaining the `@ManyToOne` override so the next raw join near this
  entity doesn't get it backwards.
- **Two more live-only findings, both fixed**: a freshly-created tag disappeared from every chip
  list immediately after creation — both `TagsPane` and `MemberReportSheet` treated *any*
  parentless category row as a non-assignable "group", which is wrong for a brand-new standalone
  tag; fixed with the structural rule "a row is a group only once something is nested under it via
  `parentId`", extracted into a shared `assignableCustomerTags` helper so the two call sites can't
  drift apart again. Separately, the score tab kept showing stale ranges/counts after a threshold
  save until an unrelated refetch; fixed by having `useUpdateLoyaltyPolicy` also invalidate the
  segmentation report's query key.
- **Known follow-up, not fixed here**: `ProductsService.deleteCategory` does a plain
  `categoryRepo.remove` with no cleanup of `customer_categories` assignment rows — deleting a tag
  category leaves orphaned join rows behind (worked around manually in the dev DB during this
  stage's testing). Out of scope for this stage since it's a pre-existing gap in category deletion
  generally, not something Stage 4a introduced; worth a dedicated fix.
- Test counts: 26 new tests across `loyalty`/`reports`/`customers`, full backend suite **979/979**
  green (up from 939), lint 0 errors (unchanged 56-warning baseline), build clean in both repos.

### Stage 4c — Design parity with the prototype — Done

- **Why this stage exists**: `customer-club-admin.html` was re-skinned (Manooch brand indigo, flat —
  no shadows, restructured header) in a commit that landed *after* Stages 1–4a had already shipped
  against the older violet-and-shadow design the prototype originally had. `tokens.css`'s own club
  block comment claimed to be "ported verbatim" from the prototype's `:root`, which was no longer
  true — a correctness bug in already-delivered stages, not a polish task, so it was run before
  Stage 4b rather than after (new screens then get built in the final look with no rework).
- **The token drift** (`customer-club-admin.html:33-53` vs. `packages/ui/src/tokens.css`, before/after):

  | Token | Prototype (authoritative) | Old value |
  |---|---|---|
  | `--color-club-primary` | `#4B45E6` | `#6c4df6` |
  | `--color-club-primary-2` | `#6F6AEB` | `#8e6bff` |
  | `--color-club-primary-soft` | `#ECEBFB` | `#efebfe` |
  | `--color-club-bg` | `#FEFEFE` | `#f4f5fa` |
  | `--color-club-muted` | `#737377` | `#7b8194` |
  | `--color-club-border` | `#F0F1F4` | `#eceef5` |
  | `--shadow-club` | `none` | a two-layer drop shadow |

  `--color-club-bg: #FEFEFE` deliberately removes the page/card contrast the old `#f4f5fa` gave —
  the prototype separates cards from the page by `--border` alone, not by a fill difference.
- **What was re-skinned**: the tokens above; the shared kit (`ClubCard` padding `p-4`→`p-3`,
  `ClubTabsCtl` back to `11.5px`/`400` with no active-state shadow, `ClubFab` to `48px`/`15px`
  radius/no shadow, `ClubTabBar` to the prototype's translucent/backdrop-blur bar); every hardcoded
  violet literal across `customers/page.tsx`, `MemberRow.tsx`, `HeroCard.tsx`, `ClubAppBar.tsx`,
  `ClubFab.tsx`; and the shell structure — the dashboard's dark `#202A37` header block with a glass
  (`backdrop-filter: blur`) SMS-credit hero replacing the old solid-gradient card, and inner pages'
  `52px` `#FEFEFE` header with a bare back arrow and inline title/subtitle (the old standalone
  `<h1>/<p>` title block was deleted — the prototype has no such element in either shell mode). All
  21 views were then walked at 390×844 against the prototype's matching `view-*` section.
- **Deliberately deferred, not done**: the prototype's scroll-collapse hero animation
  (`customer-club-admin.html:787-808`) — recorded here as an explicit scope cut, not an oversight.
- **Verified**: `pnpm typecheck:admin && pnpm lint && pnpm build:admin` clean; Playwright at 390×844
  against a real local backend confirmed the dark dashboard header + glass hero, the inner-page 52px
  header on a deep route, no visible drop shadows anywhere in the club tree, indigo (not violet) on
  chips/tabs/buttons, and RTL intact after every layout edit. `manooch-backend` was untouched by this
  stage — no backend test run beyond confirming that.

### Stage 4b — Acquisition (referral / lead magnet / campaign starter) — Done

- **The reuse decision**: acquisition shipped with **no new backend module** — one settings group
  added to the existing `LoyaltyPolicy` row, one optional DTO field, one read endpoint on the
  existing `reports` module, and one award path added inside `CustomersService.createCustomer`'s
  existing transaction, extending §4.1's rule the same way Stage 4a did. There is no dedicated
  `Referral` entity — the point ledger itself is the record (see below).
- **Backend** (`manooch-backend`, uncommitted on `feat-customer-club` at time of writing):
  `LoyaltyPolicy` gained `referrerPoints`/`inviteePoints`/`referrerDailyCap`/
  `leadConversionWindowDays` (defaults 500/250/5/14) via an additive migration and
  `UpdateLoyaltyPolicyDto`. `customers/referral-award.util.ts` runs inside `createCustomer`'s
  existing `QueryRunner`: resolves the invitee's `referrerCode` to a `Customer`, no-ops silently
  (customer still created) on a missing code, a self-referral, or a referrer with no live
  `StoreCustomerStatus` row for this store; otherwise awards both sides via
  `LoyaltyService.earnWithinManager` with `reason: REFERRAL` and `referenceId` set to the other
  party's customer id, capping the referrer's award (never the invitee's) at
  `referrerDailyCap` per Tehran day (`getTehranDayRange`, §4.2). `reports.service.ts` gained
  `getAcquisition(storeId)`: one `PointTransaction` aggregate split by the two fixed award-note
  strings (`REFERRAL_INVITEE_NOTE`/`REFERRAL_REFERRER_NOTE`, exported constants so the write path and
  the read path can't drift apart) for the referral ledger, and a `StoreCustomerStatus`⋈`Order`
  funnel query (registered in a rolling `leadConversionWindowDays` window vs. converted — has a PAID
  order inside that same window from their own join date) for the lead funnel, landing on
  `AdminReportsController`'s existing `GET .../reports/*` shape.
- **Frontend** (`manooch-fronts`, uncommitted on `feat-customer-club` at time of writing):
  `tools/referral/` — a 3-pane `ClubTabsCtl` (`referral`/`lead`/`campaign`) reusing the whole existing
  club kit (`ClubCard`, `ClubStatBox`, `ClubChipsRow`, `ClubEmptyState`, `SmsComposer`, `faNum`) with
  no new primitives. `ReferralPane` shows real referrer/invitee counts and a real "دعوت‌های اخیر" list
  paired by `referenceId`; `ReferralRewardsCard`/`LeadSettingsCard` PATCH the new `LoyaltyPolicy`
  fields (`LeadSettingsCard` reads/writes the **existing** `welcomePoints`, not a second field — the
  same trap `ClubSettings` already avoided for `minimumRedemptionPoints`); `CampaignStarterPane`
  reshapes the prototype's AI tab into goal chips that seed an `SmsComposer` body and open the
  existing `NewCampaignSheet` pre-targeted at the matching `LoyaltySegment` (no LLM wired anywhere).
  `tools/page.tsx`'s «رفرال» card now navigates instead of toasting; `sarnakh` (the walk-in
  phone-first registration screen — the only registration entry point that exists without a
  storefront) gained an optional referrer-code field; the member report sheet surfaces that
  customer's own `referralCode` with a copy action.
- **Divergences from the prototype** (11 total, all deliberate — full table in the design plan; the
  headline ones): the prototype's store-level hardcoded invite code (`CLB-DIJI-2024`) is replaced by
  the existing per-customer `Customer.referralCode` (there is no store-level code to invent); every
  hardcoded stat (`۱۸۶ دعوت فعال`, `۹۲ ثبت‌نام`, `↑۲۴٪`, `نرخ تبدیل ۴۹٪`) is now a real count; the
  reward inputs and «ذخیره» button, previously bound to nothing, now PATCH real policy columns; the
  three-step funnel's fabricated "بازدید از لینک لندینگ" row is dropped entirely — there is no
  landing page to count, and a fabricated visit number is exactly the defect class every prior stage
  has been removing; the 15%-discount first-purchase gift is dropped for Stage 3b's reason
  (`CartService.checkout` still hardcodes `discountAmount: 0`) and repurposed as the real
  `leadConversionWindowDays` setting; the AI tab's fabricated `۸۷٪ باز شدن`/`پنجشنبه ۱۹:۰۰`/AI badge
  are gone along with any LLM call.
- **Test-first coverage**: `referral-award.util.spec.ts` (8 tests — both sides awarded with correct
  `referenceId`s, self-referral ignored, unknown code ignored, non-member referrer ignored, at-cap
  invitee-still-awarded/referrer-skipped, under-cap boundary, a `TZ=UTC` cap-boundary test per §4.2,
  zero-configured-points skips both, and a structural check that no `Invite` row is ever touched);
  `reports.service.spec.ts` gained 3 tests for `getAcquisition` (empty-store zeros with
  `conversionPercent: 0` never `NaN`, aggregated ledger + paired funnel counts, percent rounds rather
  than truncates).
- **Verified live** via Playwright + direct Postgres access against a real local backend (a JWT
  minted with the backend's own secret plus a matching `customer_auth_tokens` row, to drive real
  `CustomerAuthGuard`-protected calls without a full OTP flow), the plan's full 9-step smoke script:
  the tools-page card navigates instead of toasting; registering a customer with another's
  `referralCode` moves both ledgers by the configured amounts, with the referral tab's live counts and
  recent list agreeing with a hand-run SQL count; the `invite` table is confirmed unchanged
  throughout (decision 2 — a club referral must never touch the seller-invite system); pushing past
  the daily cap still creates and awards the invitee, but stops awarding the referrer at the
  configured cap; a garbage code, a self-code, and a non-member's code each create the customer and
  award nothing; a `referrerPoints` PATCH persists across reload (the DTO-whitelist check, per §4.5)
  and the next referral uses the new value; the lead tab shows real zeros (never `NaN`) on data-empty
  paths; a directly-inserted PAID order inside the window moves the converted count/percentage, an
  unpaid order does not; and picking a campaign-starter goal chip opens `NewCampaignSheet` correctly
  pre-filled, whose submission created a real, visible `Campaign` row. All seeded test customers,
  orders, the campaign/template pair, and the seeded auth token were removed from the dev DB after
  verification.
- **A real, live-only bug found and fixed — the fourth instance of this bug class**: `getAcquisition`'s
  lead-funnel join (`StoreCustomerStatus` ⋈ `Order`) failed with
  `operator does not exist: uuid = character varying`. `Order.customerId` *and* `Order.storeId` each
  carry a `@ManyToOne`+`@JoinColumn` alongside a sibling `@Column()` on the same property name —
  TypeORM's relation-driven type inference silently wins, making both physically `uuid` in Postgres,
  while `StoreCustomerStatus.customerId`/`storeId` are genuinely plain `varchar` columns with no
  relation decorator. This is the same defect class as Stage 3b's *missing* cast and Stage 4a's
  *unnecessary* cast — three different raw joins across three stages, each guessing a lookalike
  column's physical type wrong in a different direction. `reports.service.spec.ts` mocks the query
  builder and could not have caught it; only the live run did. Fixed by casting both varchar sides
  (`scs."customerId"::uuid`, `scs."storeId"::uuid`) — never the uuid side, never both sides of the
  same comparison — with a doc comment cross-referencing the prior two instances so the next raw join
  near either entity doesn't get the direction backwards again.
- Test counts: 11 new tests across `customers`/`reports`, full backend suite **990/990** green (up
  from 979), lint 0 errors (unchanged 56-warning baseline), build clean in both repos.

### Stages 5–7 — Not started

Per the plan, in order:

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

### 4.1 Reminders, occasions, and retargeting are all campaigns, not separate backend modules

A reminder rule is a `DAYS_SINCE_PURCHASE` campaign with a linked message template. Occasions
(Stage 3b — `BIRTHDAY` recurring, `OCCASION` one-shot via `config.occasionAt`) and retargeting
(Stage 3b — also `DAYS_SINCE_PURCHASE`) follow the same shape: no new module, controller, route,
settings entity, or cron. Reminders and retargeting share a trigger, so `config.linkedToolKey`
(`'retargeting'` vs. unset) is the tool-ownership discriminator — filter every list/audience query by
it before adding a fourth tool at any of the three triggers already in use.

Segmentation (Stage 4a) extends the same no-new-module rule in a different shape: it's a
**read-model**, not a write path — one endpoint on the existing `reports` module composing
existing tables (`Order`, `LoyaltyMember`, `Category`/`CustomerCategory`), not a new entity.
Customer tags are `Category` rows of `type: CUSTOMER` with `parentId` as the group relation — not
a dedicated tag table — reusing the products module's existing category CRUD wholesale.

Acquisition (Stage 4b) follows the same rule again, combining both prior shapes: its settings are
four columns added to the existing `LoyaltyPolicy` row (a write path, no new entity), its stats are
a `reports` read-model exactly like Stage 4a's segmentation endpoint, and its only new write
behavior — the referral award — is a helper called from inside `CustomersService.createCustomer`'s
existing transaction, not a new controller/service/module. There is deliberately no `Referral`
entity; the `PointTransaction` ledger, keyed by two fixed award-note strings, is the record.

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
a second `QueryRunner`. Occasion/retargeting point grants (Stage 3b) are the one exception that
doesn't need a shared manager — a campaign send has no sibling write to share a transaction with — so
they call plain `LoyaltyService.earn` directly, with `referenceId: '{campaignId}:{tehranDayKey}'` as
the sanctioned "grant once per campaign per Tehran day" primitive: a same-day re-run of
`runDueCampaigns` is a no-op with no extra idempotency machinery, live-verified in Stage 3b.

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
- Pure, unit-tested classifier functions for anything with named buckets/segments —
  `classifySegment` (customer segment), `classifyTier` (Stage 4a, loyalty tier from balance vs.
  `LoyaltyPolicy` thresholds), `scoreRfm`/`classifyRfmSegment` (Stage 4a, RFM). Where a classifier's
  result is also cached on an entity column for cheap reads (`LoyaltyMember.tier`), the column is a
  **projection kept in sync by the write path**, never the source of truth — derive-on-read stays
  authoritative so a later threshold change doesn't leave stored values stale.
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
- **`customer-club-admin.html`'s `:root` is the source of truth for the club's design tokens**
  (`packages/ui/src/tokens.css`'s club block), established by Stage 4c after the prototype was
  re-skinned *after* Stages 1–4a had already shipped against its older colors/shadows — the token
  block had claimed to be "ported verbatim" while having silently drifted. Re-diff the club token
  block against the prototype's `:root` whenever the prototype file changes, don't assume it's still
  in sync; `typecheck`/`lint`/`build` all pass on a wrong color, only a 390×844 screenshot comparison
  catches drift here.

---

## 5. Verification per stage

- **Backend:** full `npm test` in `manooch-backend`, plus a stage-specific suite for anything touching
  money/points/chance logic.
- **Frontend:** `pnpm turbo run typecheck`/`lint`/`build --filter=@manooch/admin`.
- **Visual:** compare each new view against the prototype at 390×844 — RTL, Persian numerals, card
  order, copy.
- **Live:** Playwright against a real local backend+DB, not just mocks — this caught real bugs in
  every stage that has shipped so far (§Stage 1, §Stage 2, §Stage 3a, §Stage 3b, §Stage 4a, §Stage 4b)
  that unit tests alone did not: response-serialization defects (bare-entity returns missing joined
  fields) in Stages 1, 2, and 3a; a systemic date-serialization bug in Stage 3a (`pg`'s local-timezone
  `Date` handling vs. UTC-naive `timestamp` columns); in Stage 3b, a raw-SQL join between a `uuid` and
  an unconverted `varchar` column that only a real Postgres instance — not a mocked query builder —
  could reject; in Stage 4a, the mirror image of that same defect class — a raw-SQL join that added an
  unnecessary `::text` cast onto a column (`Category.parentId`) that TypeORM's `@ManyToOne` relation
  had silently made a real `uuid` — plus two UX-only bugs (a newly created tag misclassified as
  unassignable, a stale cache after a threshold save) that only a live click-through surfaces; and in
  Stage 4b, a fourth instance of the same uuid/varchar join-cast class — `Order.customerId` *and*
  `Order.storeId` both silently `uuid` via a sibling `@JoinColumn`, joined raw against
  `StoreCustomerStatus`'s genuinely-`varchar` columns of the same names — caught only because the
  smoke script exercised the acquisition endpoint's lead-funnel query against a real database. Four
  stages in a row have now each surfaced a different raw SQL join guessing a lookalike column's
  physical type wrong, in three different directions (missing cast, unnecessary cast, cast on both
  sides needed) — a strong signal that every new raw join adjacent to a `@ManyToOne`/`@JoinColumn`
  pair deserves a live check before being trusted, not just a unit test against a mocked builder.

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
