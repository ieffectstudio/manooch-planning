# Customer Loyalty Club — Final Delivery Status and Close-out

**Version:** 2.0 — **Updated:** 24 Mordad 1405 (2026-08-15) — **Status:** Closed — Phases 1–4 complete

> The approved Version 1 Customer Loyalty Club feature scope is complete. This file replaces the old
> “Phase 1 delivered, Phases 2–4 planned” status. It is retained under the existing filename so links
> do not break, but it is now a **close-out record**, not a plan for remaining feature work.

The product baseline is [`PRD.md`](./PRD.md) v1.1. The final visual/interaction reference is
[`customer-club-admin.html`](./customer-club-admin.html), supported by
[`PRD-باشگاه-مشتریان.md`](./PRD-باشگاه-مشتریان.md) and [`README.md`](./README.md).

---

## 1. Final Status at a Glance

| Area | Final status | Completion |
|---|---|---:|
| Approved Version 1 feature phases | **Complete** | 4/4 |
| Reference views | **Complete** | 21/21 |
| Bottom-navigation tabs | **Complete** | 5/5 |
| Functional tools | **Complete** | 10/10 |
| Tool cards in the Tools hub | **Complete** | 9/9 |
| Club dashboard entry | **Complete** | 1/1 |
| Reference bottom-sheet modals | **Complete** | 13/13 |
| Phase 1 views | **Complete** | 10/10 |
| Phase 2 views | **Complete** | 7/7 |
| Phase 3 views | **Complete** | 2/2 |
| Phase 4 views | **Complete** | 2/2 |
| Phase 5 external/production extensions | Outside Version 1 | Not counted as remaining feature scope |

### What a store owner can do in the completed Version 1 scope

- Configure points, value, expiry, rounding, and automated-SMS settings.
- View the dashboard and full reports.
- Create/edit templates and automatic/manual campaigns.
- Send immediate or scheduled bulk SMS to selected segments.
- Create inactivity reminder rules and inspect send history/details.
- Browse customers, points, and purchase history; manually adjust points.
- Define and redeem Club items with stock, points, and redemption codes.
- Create multiple wheels and prizes, validate 100% chance, preview spins, and inspect winners.
- Create surveys, inspect results, and remind non-respondents.
- Configure retargeting and grant cashback.
- Configure birthday/custom occasions and inspect history.
- Run referral, lead-magnet, and Version 1 assisted campaign flows.
- View points tiers, RFM groups, and custom labels.
- Define radar zones and regional audiences with quota and cost estimation.

### Completion interpretation

“Complete” here means the **approved Version 1 admin-plugin feature scope and its final UX reference
are delivered**, as confirmed by the project status and the supplied final artifacts. The single-file
HTML uses in-memory fixture data; it does not by itself prove database persistence, real SMS delivery,
payment settlement, or location telemetry.

The original document supplied detailed repository evidence only for Phase 1. No Phase 2–4 release
SHAs, migration list, or final test report were included with this documentation update. This is an
**evidence/documentation boundary**, not a reopened feature phase. Add final release identifiers to
release notes when available rather than treating the features as unbuilt.

---

## 2. Authority and Resolved Inconsistencies

### 2.1 Source-of-truth order

1. `PRD.md` v1.1 — final resolved scope and acceptance baseline.
2. `customer-club-admin.html` — final visible structure, behavior, validation, and copy reference.
3. `PRD-باشگاه-مشتریان.md` — approved Persian intent and terminology.
4. `README.md` — packaging, fonts, and feature notes.
5. This document — delivery close-out and engineering/verification notes.

### 2.2 Resolutions applied in the updated PRD

| Earlier inconsistency | Final resolution |
|---|---|
| “10 tools in the Tools hub” | There are **10 functional tools total**: 9 in Tools plus Club from Dashboard |
| Club as a footer/tool-hub destination | Club is entered from Dashboard; it is not a sixth bottom tab |
| Dashboard title described as a title pill | Final HTML renders page title/subtitle below the app bar; `.title-pill` CSS is unused |
| Radar “trapezoid” mode | It is general polygon mode with 3–10 vertices; the UI supplies a trapezoid sample |
| Fixed 5-point wheel rule | Wheel entry cost is per-wheel; 5 points is the separate participation-points default |
| Tehran → Gorgan regional flow | Corrected to **Golestan → Gorgan** |
| Five sample provinces in README | Final HTML contains six, adding Golestan for the Gorgan example |
| “Real AI” implication | Version 1 uses deterministic/canned goal-to-text assistance; a model call is future scope |
| Single-file HTML as production architecture | HTML is the reference prototype; the production plugin is API/persistence-backed |
| Demo store/plan/count values | They are fixtures and must be replaced by tenant data in production |

---

## 3. Phase Close-out

## 3.1 Phase 1 — MVP Foundations — Complete

**Delivered views: 10**

| View/route concept | Reference view | Status |
|---|---|---|
| Dashboard | `dashboard` | Complete |
| Reports | `reports` | Complete |
| Campaigns and club structure | `campaigns` | Complete |
| Full templates | `templates` | Complete |
| Bulk SMS | `smsgroup` | Complete |
| Tools hub | `tools` | Complete |
| Reminders | `reminders` | Complete |
| Customers | `members` | Complete |
| Points management | `points` | Complete |
| Settings | `settings` | Complete |

**Delivered capability**

- Mobile shell, app bar, title block, contextual FAB, bottom tabs, toasts, and reusable sheets.
- SMS quota/outbox/provider foundation and delivery reporting.
- Points policy, member balance, transactions, expiry, and manual adjustments.
- Campaigns, templates, automatic/manual filtering, linked-tool field, and send reporting.
- Bulk SMS audience/composer/schedule/settings/history.
- Reminder rules using days since last purchase.
- Customer search/filter, loyalty data, customer report, and purchase-history read.
- Dashboard and Club report endpoint/screen.

**Historical repository evidence retained from the original status document**

Branches were both named `feature/customer-club-phase1`:

| Repository | Commits | Recorded range |
|---|---:|---|
| `manooch-backend` | 8 | `b741c5f` … `a19a2d7` |
| `manooch-fronts` | 14 | `af34487` … `51507f5` |

The original record reported 492 passing tests and these migrations:

- `1785842560793-AddCustomerClubSms`
- `1785852147665-AddLoyalty`
- `1785854381206-AddCampaigns`

That evidence is historical and was not re-run as part of this documentation-only update.

---

## 3.2 Phase 2 — Loyalty — Complete

**Delivered views: 7**

| View | Reference | Completion criteria represented in final artifact |
|---|---|---|
| Club admin | `club` | Items, image preview/remove, categories, points price, stock, active state, member purchases, settings |
| Club customer preview | `club-customer` | Balance, category filter, redemption confirmation, insufficient-points handling, stock deduction, code |
| Wheel | `lucky` | Multiple wheels, dynamic prizes, chance total, spin/cost, winners, details, settings |
| Surveys | `surveys` | List, creation, 2–6 options, audience/SMS/schedule, settings/history |
| Survey results | `survey-detail` | Recipients, responses, status, result bars, copy link, reminder |
| Occasions | `occasions` | Non-deletable birthday, custom occasions, audience/message, active state, history |
| Retargeting | `buyback` | Return-credit rules, SMS templates, cashback grants, conditions, KPIs/history |

**Closed acceptance contracts**

- Club redemption is a single atomic outcome: validate balance/stock, spend points, decrement stock,
  create purchase, and issue a redemption code; no partial write on failure.
- Wheel creation requires at least 2 and at most 8 prizes in the final editor, with the chance total
  exactly 100%; server-side validation remains mandatory.
- Wheel entry cost is per-wheel. Participation points are a separate configurable setting.
- Survey reward is awarded once per customer per survey.
- Birthday is seeded/non-deletable; custom occasions are editable/deletable.
- Cashback/credit writes follow decimal and transactional rules.
- Tool actions use the shared points and SMS services rather than duplicating balance/quota logic.

---

## 3.3 Phase 3 — Acquisition and Segmentation — Complete

**Delivered views: 2**

| View | Reference | Completion criteria represented in final artifact |
|---|---|---|
| Referral/acquisition | `acquire` | Referral rewards/cap/history, lead link/funnel/gifts, assisted campaign goals/text/audience/time |
| Segmentation | `segments` | Bronze/Silver/Gold/Diamond, R/F/M views, named RFM groups, custom labels and customers |

**Closed acceptance contracts**

- Referral defaults: 500 inviter points, 250 invitee points, with daily cap and anti-abuse validation.
- Lead completion defaults to 100 points; lead-to-first-purchase defaults to a 15% code with a 14-day window.
- Version 1 assisted campaign output is deterministic/canned; no external model dependency is required.
- RFM thresholds are configurable server-side rather than compiled into a fixed query.
- RFM and custom labels are available as targetable audience concepts.

---

## 3.4 Phase 4 — Radar and Regional SMS — Complete

**Delivered views: 2**

| View | Reference | Completion criteria represented in final artifact |
|---|---|---|
| Radar | `zones` | Zone list/settings/history, point radius 200–3000m, polygon 3–10 vertices, zone SMS, 24-hour suppression |
| Regional SMS | `regional` | Region cards, province/city/neighborhood picker, select-all, exact/percentage quota, live cost, history |

**Closed acceptance contracts**

- Radar supports point/circle and arbitrary polygon modes; “trapezoid” is a sample, not a geometric restriction.
- Radar suppresses repeat messages to the same person for 24 hours and respects business hours.
- Automatic passerby triggering remains gated by the external customer-app location source.
- Regional send requires province, city, and at least one neighborhood.
- Quota N cannot exceed eligible M; recipient selection must be random and non-repeating within the defined window.
- Reference data contains six sample provinces, including Golestan → Gorgan; production needs maintained national coverage.

---

## 4. Final 21-View Inventory

| Phase | Views | Count |
|---|---|---:|
| Phase 1 | `dashboard`, `reports`, `campaigns`, `templates`, `smsgroup`, `tools`, `reminders`, `members`, `points`, `settings` | 10 |
| Phase 2 | `club`, `club-customer`, `lucky`, `surveys`, `survey-detail`, `occasions`, `buyback` | 7 |
| Phase 3 | `acquire`, `segments` | 2 |
| Phase 4 | `zones`, `regional` | 2 |
| **Total** |  | **21** |

### Reference modal inventory — 13

- New campaign
- New survey
- New/edit radar zone
- Campaign settings/send report
- Send details
- New/edit template
- Customer report
- New/edit Club item
- New/edit occasion
- New/edit wheel
- Wheel details/winners
- New/edit reminder
- Club redemption

---

## 5. Final Functional Acceptance Checklist

The following items define the completed Version 1 scope. They should remain covered by regression
checks even though they are no longer “remaining phases.”

### Shell and navigation

- [x] Five bottom tabs.
- [x] Parent-tab highlight for subviews.
- [x] Back navigation and contextual FAB.
- [x] Page title/subtitle below app bar without body duplication.
- [x] RTL/mobile layout, Persian-number presentation, toasts, and sheets.

### SMS and campaigns

- [x] 320-character composers and variable tokens.
- [x] Audience selection, preview, schedule, and live cost where applicable.
- [x] Automatic/manual campaigns and linked wheel/survey.
- [x] Success/error/undelivered details and report navigation.
- [x] Business hours, daily caps, reminder/radar suppression concepts.

### Points, customers, and Club

- [x] Points rules, balance, earned/spent, history, expiry, and manual adjustment.
- [x] Customer points and purchase-history tabs.
- [x] Club item image/category/price/stock/settings.
- [x] Customer redemption, insufficient-balance handling, stock update, and code.

### Loyalty and growth tools

- [x] Multiple wheels with per-wheel prizes, cost, winners, and 100% validation.
- [x] Surveys with creation, results, reminders, rewards, and history.
- [x] Retargeting, cashback, occasions, and reminders.
- [x] Referral, lead magnet, and deterministic assisted campaign.
- [x] Points tiers, RFM views/groups, and custom labels.

### Geography and reports

- [x] Radar point/polygon zones, settings, and history.
- [x] Regional hierarchy, quota, live cost, validation, and history.
- [x] SMS, points, tool, lifecycle, sales, and customer-trend reports.

---

## 6. Engineering Decisions That Remain in Force

These decisions came from the earlier delivery record and remain part of the implementation contract.

### 6.1 Reminders are campaigns, not a separate backend module

A reminder rule is a `DAYS_SINCE_PURCHASE` campaign. Its message is stored in a linked message
template, so create/edit is a two-step mutation: write the template, then the campaign that references
it. Do not introduce a second scheduler or duplicate quota path.

### 6.2 All business-time logic uses an explicit Tehran-time utility

Do not use server-local `Date#getHours()`/`setHours()` for business rules. Birthday matching, occasion
times, reminder windows, points expiry, retargeting deadlines, wheel windows, survey reminders, and
radar suppression must use an explicit `Asia/Tehran` utility and have at least one `TZ=UTC` test.

### 6.3 Multi-record financial/value writes are transactional

Use a transaction for:

- Club stock + points + purchase + code;
- wheel cost/reward + spin/prize result;
- cashback/retargeting credit;
- SMS credit deduction + batch/message creation;
- any reward that also updates a campaign/referral/survey record.

### 6.4 Server authority is mandatory

The server validates balances, stock, quota, opt-out, eligibility, chance totals, reward uniqueness,
regional quota, tokens, and date windows. Client validation is UX support, not authority.

### 6.5 Shared implementation conventions

**Backend**

- Soft delete for deletable records.
- Decimal transformer for money columns.
- Indexed filter/sort/foreign-key columns; no query-inside-loop patterns.
- Localized error codes and success messages.
- Controllers separated by audience and modules registered consistently.
- Test-first for money, credit, points, and chance/award logic.

**Shared types**

- Author in the frontend/shared types package first, then sync to backend.
- Do not hand-edit generated/vendored copies.
- Runtime enums or type-only imports; avoid unintended runtime schema dependencies.

**Frontend**

- RTL review before final layout classes.
- Persian strings in messages/localization rather than scattered inline production copy.
- Server Components by default where applicable; client sheets for mutations.
- Match the final HTML inside app bar, title block, screens, FAB, tab bar, toasts, and modals.
- Exclude decorative `.stage`, `.phone`, `.island`, and `.statusbar` prototype chrome from production.

---

## 7. Verification and Release Evidence

### 7.1 What is verified by the supplied final artifact

A static artifact check confirms:

- 21 reference `<section class="view">` screens;
- 13 reference modal/bottom-sheet containers;
- all four phase screen groups represented;
- 5 bottom tabs;
- the documented pane structure for campaigns, bulk SMS, retargeting, wheel, reminders, surveys,
  radar, regional SMS, acquisition, occasions, segmentation, Club, points, and settings;
- final fixture arrays/handlers for Club, reminders, occasions, segmentation, regional data, wheels,
  surveys, radar zones, templates, delivery details, and navigation.

### 7.2 Evidence not supplied with this documentation update

The earlier file said these checks had not been run at that time. No newer reports were attached:

| Evidence | Current documentation state | Required action |
|---|---|---|
| 390×844 prototype-vs-plugin screenshot comparison | Not attached | Add to release/QA artifacts if already run; otherwise run before production launch |
| Full critical-flow E2E smoke report | Not attached | Add plugin gating, order award/reversal/idempotency, SMS credit/quota, Club redemption, wheel validation, and geography checks |
| Phase 2–4 repository SHAs/PRs/migrations | Not attached | Record in release notes/changelog |
| Final Phase 2–4 unit/integration test count | Not attached | Record CI link/report |
| Real-provider delivery proof | Environment-dependent | Run only with approved credentials/sender |

This table does **not** mean Phases 2–4 are planned or unimplemented. It prevents documentation from
inventing repository/test evidence that was not among the supplied files.

### 7.3 Recommended critical smoke suite

1. Plugin gating and tenant isolation.
2. Order completion awards points once; cancellation reverses once; retries are idempotent.
3. Bulk send queues through the provider and deducts credit exactly once.
4. Out-of-hours, daily-cap, opt-out, invalid-number, and insufficient-credit sends do not deduct credit.
5. Reminder suppression and Tehran-time boundaries.
6. Club redemption atomically changes balance and stock and produces one purchase/code.
7. Club insufficient-balance/out-of-stock paths leave no writes.
8. Wheel rejects chance totals other than 100 and prevents double charge/reward.
9. Survey/referral rewards are single-award and cap-aware.
10. Cashback money precision and transaction rollback.
11. Radar 24-hour suppression and polygon validation.
12. Regional N-of-M quota, non-repetition, validation, and cost.

---

## 8. Launch Dependencies — Not Remaining Feature Phases

These items may block production operation or limit a feature, but they are not unfinished approved
Version 1 admin screens.

| Dependency/decision | Impact | Treatment |
|---|---|---|
| Real SMS provider credentials and sender approval | No real delivery without them | Deployment/client dependency |
| Inbound opt-out webhook (“reply 5”) | Compliance and suppression risk | Launch requirement for marketing SMS |
| SMS-credit top-up/manual credit policy | Stores cannot replenish credit | Product/operations decision; gateway remains outside v1 |
| Customer-app location telemetry | No automatic passerby detection | Gate automatic radar trigger; retain zone configuration/manual flow |
| National neighborhood dataset | Limited regional coverage | Replace/extend sample data before broad launch |
| Points liability/deactivation policy | Financial/customer-expectation risk | Define before large-scale issuance |
| RFM threshold approval | Segment accuracy | Ship configurable defaults and confirm with client |
| Ravi font license/files | Visual fidelity | Install licensed WOFF2; retain Vazirmatn fallback |
| Production upload/CDN policy | Club image reliability | Use platform storage provider, type/2 MB checks, cache policy |
| Monetary wheel-entry settlement | Payment/legal ambiguity | Keep disabled unless a supported model is approved |

---

## 9. Final Statement

- **Phases 1, 2, 3, and 4 are closed as complete.**
- **There are no remaining feature phases in the approved Version 1 Customer Loyalty Club admin-plugin scope.**
- Phase 5 items are external production extensions and operational integrations, not missing Version 1 screens.
- Future work should be tracked as release readiness, provider/data integration, or Version 2 enhancement—not by reopening this phase plan.
