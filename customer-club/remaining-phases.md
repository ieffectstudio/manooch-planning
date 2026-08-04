# Customer Loyalty Club — Delivery Status & Remaining Phases

**Version:** 1.0 — **Date:** 13 Mordad 1405 (2026-08-04) — **Status:** Phase 1 delivered, Phases 2–4 planned

Governing specs, unchanged by this document: [`PRD.md`](./PRD.md) (v1.0, approved) and the
prototype [`customer-club-admin.html`](./customer-club-admin.html). This document records **what has
actually been built**, **what was decided or changed along the way**, and **what each remaining
phase requires**. Where this document and the PRD disagree on scope, the PRD wins; where they
disagree on implementation detail, this document reflects the code as it exists.

---

## 1. Status at a Glance

Phase 1 is complete and under review. It delivered the foundations the other three phases stand on —
the SMS engine, the points ledger, the campaign system, and the entire mobile shell — plus ten of the
twenty-one screens.

| Area | Delivered | Remaining |
|---|---|---|
| **Admin screens** (of 21 in the prototype) | 10 | 11 |
| **Backend modules** (of 13 planned) | 4 built + 2 extended | 9 |
| **Database migrations** | 3 | ~9 (one per new module group) |
| **Shared type domains** | 6 | ~7 |
| **Phases** | Phase 1 | Phases 2, 3, 4 |

**What a store owner can do today:** activate the plugin, configure points rules and automated-SMS
switches, view the dashboard and reports, build message templates, create and run campaigns, send
bulk SMS to customer segments, set up "days since last purchase" reminder rules, browse customers,
and adjust point balances by hand.

**What they cannot do yet:** spend points in the Club shop, spin the wheel, answer surveys, receive
retargeting cashback, get occasion/birthday messages beyond the campaign switch, invite friends
(referral), be segmented by RFM, or be reached by radar/regional SMS.

**Sequencing rationale.** Phase 2 takes the five tools that consume points, because the points ledger
now exists and the loyalty proposition is not credible to a customer until points can be *spent*.
Phase 3 adds acquisition and segmentation, which need a populated customer base to be meaningful.
Phase 4 takes radar and regional SMS last — both are geography-driven, both have unresolved data
dependencies (§8), and neither blocks anything else.

---

## 2. What Phase 1 Delivered

Branches (both named `feature/customer-club-phase1`):

| Repo | Commits | Range |
|---|---|---|
| `manooch-backend` | 8 | `b741c5f` … `a19a2d7` |
| `manooch-fronts` | 14 | `af34487` … `51507f5` |

### 2.1 Backend

Four modules built, two extended. Full suite green at 492 tests.

| Module | Status | What landed |
|---|---|---|
| `sms/` | new | `SmsQuotaService` (owns every PRD §9 send rule in one place), `SmsOutboxService`, `SmsDispatchTask`, an `SmsProvider` interface with `FakeSmsProvider` and `MeliPayamakProvider`, `admin-sms.controller.ts`. Entities: `sms_settings`, `sms_messages`, `sms_batches`, `sms_credit_accounts`. 3 spec files. |
| `loyalty/` | new | `LoyaltyService` (earn/spend/adjust/balance/history), `PointsExpiryTask`, `admin-loyalty.controller.ts`. Entities: `loyalty_member`, `loyalty_policy`, `point_transaction`. 1 spec file. |
| `campaigns/` | new | `CampaignsService`, `MessageTemplatesService`, `CampaignRunnerTask`, two admin controllers, `message-template-seeds.data.ts` (the 9 PRD §7.8 categories). Entities: `campaign`, `message_template`. 2 spec files. |
| `reports/` | extended | `GET /admin/reports/club` plus `types/club-report.types.ts` — KPIs, SMS performance, daily series, tools report, lifecycle funnel. **No spec files** (see §4.3). |
| `customers/` | extended | Loyalty and purchase-history reads, loyalty-segment filter, `pointsBalance` on the admin customer list. |
| `plugins/` | extended | `customer-club` registered in `PLUGIN_CATALOG`: `key: 'customer-club'`, `type: 'core_sales'`, `depends_on: 'customers'`, `order: 15`, `defaultActive: false`. |

Migrations, in order: `1785842560793-AddCustomerClubSms`, `1785852147665-AddLoyalty`,
`1785854381206-AddCampaigns`.

### 2.2 Frontend

- **Shared types** (`packages/types/src/`), 6 domains: `loyalty`, `sms`, `campaigns`,
  `message-templates`, `reports`, `customers`. These are the author-of-record; the backend consumes a
  vendored snapshot via `npm run sync:types`.
- **The club shell** — `layout.tsx` owning the appbar, per-route title block, FAB and the 5-tab bar;
  `ClubAppBar`, `ClubTabBar`, `ClubFab`/`ClubFabContext`, `clubViews.ts`, and the module-scoped
  `--color-club-*` design tokens.
- **12 UI primitives** in `_common/ui/`: `ClubCard`, `ClubChipsRow`, `ClubEmptyState`,
  `ClubFormField`, `ClubSheet`, `ClubStatBox`, `ClubSwitch`, `ClubTabsCtl`, `SmsBubble`,
  `SmsComposer` (320-char counter + `{variable}` tokens), `persianNumber`, plus the barrel.
- **5 API hook modules** in `_common/api/`: `campaigns`, `customers`, `loyalty`, `reports`, `sms`.

**Screens shipped (10 of 21):**

| Route | Prototype view |
|---|---|
| `/plugin/customer-club` | `dashboard` |
| `…/reports` | `reports` |
| `…/campaigns` | `campaigns` (3 panes) |
| `…/campaigns/templates` | `templates` |
| `…/campaigns/bulk` | `smsgroup` |
| `…/tools` | `tools` (hub) |
| `…/tools/reminders` | `reminders` |
| `…/customers` | `members` |
| `…/customers/points` | `points` |
| `…/settings` | `settings` (3 panes) |

---

## 3. Decisions and Deviations Taken During Phase 1

These are settled. They exist so the next engineer does not re-open them.

### 3.1 There is no `reminders/` backend module

The original module map listed `reminders/` with its own `reminder_rule` and `reminder_run` entities.
It was not built, and is not needed: a reminder rule **is** a `DAYS_SINCE_PURCHASE` campaign, run by
the existing `CampaignRunnerTask`.

The consequence is worth knowing before touching that screen. `Campaign` has no raw message field, so
a rule's SMS text lives in a linked `MessageTemplate`. Creating or editing a rule is therefore a
**two-step mutation** — write the template first, then the campaign that references it. The same
shape will apply to any future tool whose "rule" carries a message.

### 3.2 Entity naming is inconsistent — settle it before Phase 2

The SMS tables are plural (`sms_messages`, `sms_batches`), while loyalty and campaigns are singular
(`loyalty_member`, `point_transaction`, `campaign`). Nine more modules are about to be written. Pick
one convention and apply it to the new tables rather than propagating the split; renaming the four
existing SMS tables is optional and can be deferred.

### 3.3 `reports/` has no test coverage

Every other club module has specs; `reports/` has none, despite `GET /admin/reports/club` computing
the KPIs, funnel, and per-tool aggregates the whole dashboard and reports screen depend on. Phase 2
extends this endpoint with per-tool rows for the new tools — add the spec file at that point, not later.

### 3.4 All date logic must route through the Tehran-time util

A timezone bug shipped and was caught in CI (fixed in `a19a2d7`). `SmsQuotaService` decided business
hours with `Date#getHours()`, and the daily-cap and days-since-purchase boundaries with
`Date#setHours()` — both read the **server process's** timezone. That is `Asia/Tehran` on a developer
machine and **UTC** on CI and in the production container, a 3.5-hour discrepancy that silently
mis-gated sends and made tests pass locally while failing in CI.

The fix added `src/common/utils/tehran-time.util.ts` (`getTehranHour`, `getTehranDayRange`), built on
`Intl.DateTimeFormat` with an explicit `Asia/Tehran` zone — safe as a fixed UTC+03:30 offset since
Iran abolished DST in 2022.

> **Standing rule for every remaining phase:** never call `Date#getHours`/`setHours` for business
> logic. Occasion and birthday matching, wheel campaign windows, retargeting deadlines, survey
> reminder timing, and the radar 24-hour floor are all instances of the same bug waiting to recur.
> Route them through the util, and write at least one test that pins the behaviour under `TZ=UTC`.

### 3.5 Prototype UI without a backend concept was surfaced honestly, not faked

Where the prototype shows data the backend has no concept of, the screen shows a toast explaining it
rather than inventing a number. Outstanding items of this kind, each a real work item for a later
phase or a product decision:

- SMS plan/quota display and the "buy credit" action (needs the top-up path — §8.3)
- Per-tool KPIs on the tools hub for tools that do not exist yet (resolves as Phases 2–4 land)
- SMS line/sender selector (needs provider credentials — §8.1)
- VIP-exempt toggle on reminder rules, and segment-level audience filtering on reminder rules
- The dashboard's fabricated store name and plan label were removed outright (`389eec2`)

---

## 4. Verification Debt Carried Forward

Both items below were planned for Phase 1 and **were not run**. They are not optional; they are
deferred, and they apply to every phase's screens, not only Phase 1's.

| Check | Status | What it needs |
|---|---|---|
| **Prototype fidelity comparison** — per view, screenshot the prototype at 390×844 and the implemented route side by side, comparing element order, copy, spacing, colour, Persian numerals, chip/tab state and empty states | Never run | A browser automation tool (Playwright MCP or equivalent) in the development environment |
| **Functional smoke test** — the 7-step end-to-end pass: plugin gating, order-completion point award + cancel reversal + no double-award, bulk send on `FakeSmsProvider` with single credit deduction, out-of-hours rejection with no deduction, daily-cap rejection, club purchase stock/points/code, wheel chance validation | Never run | A running dev server plus a seeded database |

Steps 6 and 7 of the smoke test target Phase 2 features and cannot be run until Phase 2 lands.
Steps 1–5 can be run today and should be, before Phase 2 begins building on unverified foundations.

---

## 5. Phase 2 — Club, Wheel, Surveys, Retargeting, Occasions

**Branch:** `feature/customer-club-phase2` · **Screens:** 7 · **Backend modules:** 5

**Goal.** Make points spendable. Phase 1 built the ledger that issues points; until a customer can
exchange them for something, the loyalty proposition is one-directional. This phase adds the five
tools that consume points and the five backend modules behind them.

### 5.1 Backend

| Module | Entities | Key rules |
|---|---|---|
| `club/` | `club_item`, `club_purchase`, `club_settings` | Item image via the existing `modules/uploads` + `STORAGE_PROVIDER` pattern. A purchase must **decrement stock, spend points, and issue a redemption code inside one `QueryRunner` transaction**. Insufficient points returns a typed i18n error, never a partial write. Settings carry minimum points, daily cap, and the confirmation SMS template with `{item}` and `{code}`. |
| `wheel/` | `wheel`, `wheel_prize`, `wheel_spin` | Multiple wheels per store, each with its own prize rows (name, chance, colour). **Prize chances must sum to 100 — validated server-side**, not only in the editor sheet. Each spin costs/awards per PRD §8 (5 points participation) and writes a `wheel_spin` row. |
| `surveys/` | `survey`, `survey_option`, `survey_response` | Short-link token for the SMS body (`{link}`). 50-point reward on response, awarded once per customer per survey. Reminder send to non-respondents. |
| `retargeting/` | `retargeting_policy`, `cashback_grant` | Return percentage, cap, deadline, minimum cart. The cashback tab records manual grants (customer, amount, reason) — a money-adjacent write, so decimal transformer and transaction discipline apply. |
| `occasions/` | `occasion` | The birthday row is **seeded and non-deletable**. Custom occasions carry title, date, time, customer category, and an SMS with `{occasion}`. Date matching is a §3.4 hazard — use the Tehran-time util. |

Also extend `reports/` with the per-tool rows these five tools produce, and add the spec file
called for in §3.3.

### 5.2 Frontend

| Route | Prototype view | Content |
|---|---|---|
| `…/club` | `club` | 3 panes: items · member purchases · settings |
| `…/club/preview` | `club-customer` | Customer-facing preview: balance card, category chips, shop grid, purchase → redemption code |
| `…/tools/wheel` | `lucky` | 4 panes: wheels · spins & prizes (live wheel + prize rows summing 100%) · winners · settings |
| `…/tools/surveys` | `surveys` | 3 panes: list · settings · history |
| `…/tools/surveys/[id]` | `survey-detail` | Received/responded stats, result bars |
| `…/tools/occasions` | `occasions` | 2 panes: occasions list (birthday undeletable) · history |
| `…/tools/retargeting` | `buyback` | 3 panes: settings (%, cap, deadline, min cart, 2 SMS bubbles) · cashback · history |

Modals to build: club item, wheel edit, wheel detail, occasion, survey edit, redeem code.

**Dependencies.** All five tools write point transactions through `LoyaltyService` and send through
`SmsOutboxService`/`SmsQuotaService` — both shipped in Phase 1. The five "club structure" switches on
the campaigns screen currently toggle against tools that do not exist; wire them as this phase lands.

**Phase risks.** The club purchase and wheel spin are the two places in the product where a partial
write corrupts a customer's balance — both warrant test-first development. Wheel chance validation
must live server-side or a crafted request can define an impossible wheel.

---

## 6. Phase 3 — Referral, Lead Magnet, and Segmentation

**Branch:** `feature/customer-club-phase3` · **Screens:** 2 · **Backend modules:** 1 new + 1 extended

**Goal.** Acquisition and analysis. Referral brings new customers in; RFM segmentation makes the
customer base addressable. Both are more valuable once Phase 2 has given customers a reason to engage.

### 6.1 Backend

| Module | Entities | Key rules |
|---|---|---|
| `referral/` | extend the existing `modules/invites`, add `lead_magnet`, `lead_submission` | Invite code, inviter/invitee rewards (500/250 per PRD §8), **daily reward cap**, invite SMS, history. Lead magnet carries a landing link, conversion funnel, and gift (100 points on form completion, 15% code on lead-to-purchase conversion). The "AI smart campaign" is a **canned `goal → text` constant map**, exactly as the prototype implements it — PRD §12 specifies a mock-up for version 1, not a model call. |
| `customers/` | extended | RFM projection (recency / frequency / monetary) and custom labels — product, payment gateway, acquisition channel. |

### 6.2 Frontend

| Route | Prototype view | Content |
|---|---|---|
| `…/tools/referral` | `acquire` | 3 panes: referral · lead magnet · AI smart campaign (goal chips → canned text) |
| `…/customers/segments` | `segments` | 3 panes: points tiers (Bronze/Silver/Gold/Diamond) · RFM (champions, loyal, at risk, new, dormant) · custom labels |

**Dependencies.** Segmentation reads the `point_transaction` and order history built in Phase 1.
RFM categories become audience filters for bulk SMS, so the bulk-send recipient selector gains options
as this lands.

**Phase risks.** RFM thresholds are deferred to the client by PRD §14.4. Phase 3 must ship defaults,
and those defaults must not harden into the API contract — keep them configurable server-side from
the start rather than compiled into a query.

---

## 7. Phase 4 — Radar and Regional SMS

**Branch:** `feature/customer-club-phase4` · **Screens:** 2 · **Backend modules:** 2

**Goal.** Geography-driven outreach. Sequenced last because both carry unresolved external data
dependencies (§8.4, §8.5) and neither blocks any other feature.

### 7.1 Backend

| Module | Entities | Key rules |
|---|---|---|
| `radar/` | `radar_zone`, `radar_hit` | Zone stored as `{ mode: point \| poly, centerX/Y, radiusMeters, vertices: jsonb }` in the prototype's normalized coordinates. Dedicated SMS per zone, **one SMS per passerby per 24 hours** — a §3.4 date hazard, enforce through `SmsQuotaService`. |
| `regional/` | `region_send` + `regions.data.ts` | The prototype's `PROVINCES → cities → hoods` tree ported as static reference data (same convention as the existing `modules/geo/geo.data.ts` — no table, no migration). Send quota is "random N of M available numbers", non-repeating within the window. |

### 7.2 Frontend

| Route | Prototype view | Content |
|---|---|---|
| `…/tools/radar` | `zones` | 2 panes: zone list · settings. Inline SVG map (`viewBox="0 0 300 150"`), point and polygon modes, click-to-place vertices, radius slider 200–3000m |
| `…/tools/regional` | `regional` | 2 panes: send (province → city → neighborhood multi-select, quota slider, live cost) · history |

**Note on the radar map.** It needs no mapping library and no tiles — the prototype draws a
hand-made SVG and stores normalized coordinates. Port it as-is rather than introducing a map
dependency.

**Phase risks.** See §8.4 — zone definition and manual per-zone send are fully buildable, but the
automatic "customer walked past" trigger has no data source in scope.

---

## 8. Open Risks

Carried forward from planning and **still unresolved**. Items 1–3 affect the product today; 4–7 affect
later phases.

1. **Meli Payamak bulk/pattern credentials are missing.** `MeliPayamakProvider` exists but free-form
   send is deferred in code. Until credentials arrive, everything runs on `FakeSmsProvider` and no
   real SMS is delivered. *Needs the client.*
2. **SMS opt-out has no inbound path.** PRD §14.1 specifies "reply 5 to unsubscribe", which requires
   an inbound-SMS webhook the architecture does not contain. The `optedOut` column ships; the webhook
   is unbuilt. Sending marketing SMS without a working opt-out is a compliance exposure, not just a
   missing feature.
3. **SMS credit has no top-up path.** PRD §4.2 excludes the payment gateway, so unless an admin or
   manual top-up route exists, no store can send anything. The prototype's "buy credit" button only
   toasts. *Needs a product decision before launch.*
4. **Radar's automatic trigger has no data source.** Detecting a passerby requires customer-app
   location, which PRD §4.2 puts out of scope. Build zone definition and manual send; gate the
   automatic trigger behind the customer app.
5. **Neighborhood data is prototype-scale.** Porting the prototype's `PROVINCES` tree yields a
   working picker, not real coverage. A real dataset is required before regional SMS goes live.
6. **Points are an unbounded liability.** Nothing caps issued points, and nothing defines what happens
   to outstanding balances when a store deactivates the plugin. Decide the policy before points reach
   production scale.
7. **RFM thresholds are deferred to the client** (PRD §14.4). See §6.2.

---

## 9. Conventions Inherited by Every Remaining Phase

Non-negotiable, already established in Phase 1 code.

**Backend**
- Soft delete everywhere deletable — `@DeleteDateColumn`, `softDelete`/`softRemove`, never `delete`/`remove`
- `QueryRunner` transaction for every multi-record or multi-table mutation
- Decimal `{to, from}` transformer on every money column
- Errors thrown with a code that exists in `src/i18n/fa/errors.json`; `@SuccessMessage()` for success copy
- `@Index()` on every column used for filter, sort, or foreign key; never query inside a loop
- Module scaffold per `guard-nestjs-module`: controllers split by audience (`admin-`/`public-`/`customer-`), types in `types/*.types.ts`, module registered in `AppModule.imports[]`
- Test-first for anything touching money, credit, or points
- **All date logic through `tehran-time.util.ts`** (§3.4)

**Shared types**
- Authored in `manooch-fronts/packages/types` first, then pulled into the backend with
  `npm run sync:types` — never hand-edited in the vendored copy
- Never import `zod` or a `*Schema` at runtime in the backend; enums (runtime) or `import type` only

**Frontend**
- 150-line hard gate per component; 5-file structure; RTL check before layout classes
- Persian strings in `messages`, never inline
- Server Components by default; bottom sheets as client mutation components
- Prototype fidelity covers everything inside the appbar, title block, screens, FAB, tab bar, toasts
  and modals — but **not** the prototype's desktop phone-frame chrome (`.stage`, `.phone`, `.island`,
  `.statusbar`), and **not** its in-memory demo arrays, which are a response-shape spec rather than
  data to ship

**Delivery**
- One branch and one PR per repo per phase
- Branches created with `git checkout -b` in the existing checkout — no git worktrees
