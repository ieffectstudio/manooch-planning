# PRD — Customer Loyalty Club (Store Builder Admin Panel)

**Version:** 1.1 — **Updated:** 24 Mordad 1405 (2026-08-15) — **Status:** Delivered / as-built baseline

> This revision reconciles the approved Persian PRD, `README.md`, and the final
> `customer-club-admin.html` reference implementation. The approved
> Version 1 admin-plugin feature scope is complete. The HTML remains the visual and interaction
> reference; production persistence, providers, and external services are supplied by the
> store-builder implementation rather than by the in-memory demo data in the HTML.

## Source-of-truth order

1. **This document** — final English product scope and resolved requirements.
2. **`customer-club-admin.html`** — final screen structure, visible behavior, validation, copy, and interaction reference.
3. **`PRD-باشگاه-مشتریان.md`** — approved Persian product intent and terminology.
4. **`README.md`** — setup guide, packaging, fonts, and feature overview.
5. **`remaining-phases.md`** — delivery close-out and implementation/verification record; it does not redefine scope.

When older documents conflict, the resolved requirement in this PRD applies. Demo names, counts,
phone numbers, links, dates, plan labels, and report values in the HTML are fixtures and are not
production defaults.

---

## 1. Executive Summary

The **Customer Loyalty Club** is a loyalty and SMS-marketing plugin for online and physical stores,
embedded in the store builder's admin panel. It converts ordinary customers into repeat and loyal
customers through:

- points earning, spending, expiry, and manual adjustment;
- manual, scheduled, event-based, and assisted SMS campaigns;
- acquisition and win-back tools;
- point-based Club items and customer redemption;
- segmentation, delivery details, lifecycle reporting, and sales reporting.

The delivered Version 1 experience is **mobile-first**, fully **right-to-left (RTL)**, and designed
around the **Ravi** typeface with **Vazirmatn** as the development fallback. Its final reference
contains **5 bottom-navigation tabs, 22 views, 19 bottom-sheet modals, and 10 functional tools**.
Nine tools appear in the Tools hub; **Club** is the tenth tool and is entered from the Dashboard. The
22nd view (`setup`) and 6 of the 19 modals were added by the newest prototype revision (see §6.2,
§6.3, and §7.10) after the counts below were first drafted.

### Key product values

1. **Sales growth:** referral/lead acquisition and win-back through reminders and retargeting.
2. **Customer retention:** points, Club redemption, wheel, surveys, and occasions.
3. **Data-driven decisions:** reports, RFM segments, labels, sales funnel, and SMS delivery details.
4. **Automation:** event-based messages for welcome, birthday, expiry, abandoned cart, inactivity, and other configured events.

### Delivery state

| Scope group | Status | Delivered reference |
|---|---|---|
| Phase 1 — MVP foundations | Complete | 10 views |
| Phase 2 — Loyalty | Complete | 7 views |
| Phase 3 — Acquisition and intelligence | Complete | 2 views |
| Phase 4 — Geographic outreach | Complete | 2 views |
| Phase 5 — Setup, billing UI, and prototype-only extras | Complete | 1 view (`setup`) + 6 modals (see §7.10) |
| **Approved Version 1 feature scope** | **Complete** | **22/22 views** |
| Phase 6 — external production extensions | Future / outside Version 1 | Real customer app, payment gateway, production media/CDN, ML RFM |

---

## 2. Goals and Success Metrics (KPIs)

These are post-launch business targets, not fixture values from the prototype.

| Goal | Metric (KPI) | Target in first 6 months |
|---|---|---|
| Increase membership | Number of Club customers | +30% |
| Win back customers | Retargeting-credit usage rate | ≥ 45% |
| Acquire through invitations | Referral conversion rate | ≥ 40% |
| SMS engagement | Delivery rate | ≥ 96% |
| Participation | Survey participation | ≥ 25% |
| Points use | Points spent through Club/wheel/discount | ≥ 30% of issued points |
| Reduce churn | Reduction in at-risk customers | −20% |

---

## 3. Audiences and Usage Scenarios

| Role | Primary need | Key scenario |
|---|---|---|
| **Store owner/manager** | Sales growth and loyalty | Send a 20% offer to the at-risk segment and inspect delivery/reporting |
| **Marketing operator** | Campaign execution | Create a Nowruz wheel, connect it to a campaign, and monitor winners |
| **Support specialist** | Customer management | Review points and purchase history, then grant cashback or adjust points |
| **End customer** | Use earned value | Redeem a Club item or spin an available wheel |

---

## 4. Product Scope

### 4.1 Delivered in Version 1

- Mobile admin shell with 5 primary tabs, 22 views, parent-aware back navigation, contextual FABs, toasts, and bottom sheets.
- Points policy, ledger, expiry, balance/history, manual add/deduct, and points-based customer tiers.
- Automated/manual campaigns, bulk SMS, scheduling, reusable templates, variables, preview, cost estimate, and delivery details.
- Ten functional tools: referral/acquisition, occasions, bulk SMS, reminders, retargeting, wheel, surveys, radar, regional SMS, and Club.
- Club administration and customer redemption preview, including image selection, stock, points deduction, and redemption code.
- Customers, loyalty filters, customer points report, purchase history, RFM analysis, and custom labels.
- Dashboard and reports for SMS, points, tool performance, customer lifecycle, customer trend, total sales, and average order.
- Persian UI copy, RTL layout, Persian-number presentation, responsive mobile behavior, and Ravi/Vazirmatn font setup.

### 4.2 Completion boundary

The feature scope is complete when all listed views and interactions are present in the plugin and
respect the business rules in this PRD. The standalone HTML is a reference prototype: it stores demo
changes in memory and uses fixture data. It is **not** evidence of database persistence, provider
delivery, payment settlement, or location telemetry. Those concerns belong to the API-backed plugin
and its deployment environment.

### 4.3 Outside Version 1 / later extensions

- A standalone customer application; Version 1 includes only customer-facing preview/link flows.
- A real payment gateway for purchasing SMS credit.
- Full desktop-first web redesign; Version 1 remains mobile-first.
- ML-based RFM scoring; Version 1 uses deterministic/configurable thresholds.
- Production-wide geographic coverage beyond the supplied/reference region dataset.
- Automatic radar detection without a customer-app location source.

---

## 5. Design Principles

### 5.1 Typography — Ravi

| Element | Weight |
|---|---|
| h1 / page, card, and bottom-sheet title | **SemiBold (600)** |
| h2 / section title and subtitle | **Medium (500)** |
| Body text | **Regular (400)** |
| Large figures / strong emphasis | **Bold (700), where needed** |

Licensed files use:

```text
fonts/Ravi-Regular.woff2
fonts/Ravi-Medium.woff2
fonts/Ravi-SemiBold.woff2
fonts/Ravi-Bold.woff2
```

Vazirmatn is the fallback until licensed Ravi files are installed. Fonts use `font-display: swap`.

### 5.2 Color and spacing

- Primary: `#6C4DF6`; secondary purple: `#8E6BFF`; background: `#F4F5FA`; text: `#181B26`.
- Status colors: success `#12B76A`, error `#F04438`, warning `#F79009`.
- Standard card gap 14px, card padding 16px, and major section spacing 28px.
- Cards use rounded borders, subtle shadows, and status-specific soft backgrounds.

### 5.3 Layout and responsive behavior

- Mobile-first reference viewport: **390×844**.
- Full RTL with automatic Persian-number presentation.
- Touch targets are at least 40px where practical.
- Desktop reference may show a decorative phone frame and side description; these are prototype chrome, not plugin UI.
- In the final HTML markup, the dashboard app bar contains **Manage Store** and notification controls; the page title/subtitle render immediately below the app bar. The unused `.title-pill` style is not a delivered UI element.
- Page titles are not duplicated inside the body.

---

## 6. Information Architecture and Navigation

### 6.1 Primary navigation

```text
Bottom bar — 5 tabs
├── Dashboard
│   ├── SMS credit, quick actions, KPIs, sends chart, smart segments
│   ├── Club entry
│   └── Reports entry
├── Campaigns
│   ├── Campaigns
│   ├── Club structure
│   └── Message templates
├── Tools
│   └── 9 tool cards with enable/configure/history actions
├── Customers
│   ├── Search and segment filters
│   ├── Customer points/purchase report
│   └── Points and advanced segmentation entries
└── Settings
    ├── Points and rules
    ├── Automated SMS
    └── General
```

**Clarification:** there are 10 functional tools in total, but only 9 are listed in the Tools hub.
Club is intentionally accessed from the Dashboard and is not a sixth footer tab.

### 6.2 Final 22-view inventory

The `?tab=` values below are the HTML reference identifiers. Production route paths may differ while
preserving the same information architecture and parent-tab highlight.

| # | Reference view | Parent/entry | Main content |
|---:|---|---|---|
| 1 | `dashboard` | Dashboard | Credit, quick actions, entries, stats, sends, smart segments, campaigns |
| 2 | `reports` | Dashboard | Date range, SMS/points KPIs, tool reports, sales/lifecycle/customer trend |
| 3 | `campaigns` | Campaigns | Campaigns, club structure, quick templates |
| 4 | `templates` | Campaigns | Full categorized template library |
| 5 | `smsgroup` | Campaigns / Tools | Bulk-SMS settings and history |
| 6 | `tools` | Tools | Nine-tool hub |
| 7 | `reminders` | Tools | Rules, history, settings |
| 8 | `buyback` | Tools | Retargeting, cashback, history |
| 9 | `lucky` | Tools | Wheels, spins/prizes, winners, settings |
| 10 | `surveys` | Tools | Survey list, settings, history |
| 11 | `survey-detail` | Surveys | Results and response statistics |
| 12 | `zones` | Tools | Radar zones, settings, history |
| 13 | `regional` | Tools | Region list, send composer/quota, history |
| 14 | `acquire` | Tools | Referral, lead magnet, assisted campaign |
| 15 | `occasions` | Tools | Occasions and send history |
| 16 | `segments` | Customers | Points tiers, RFM, labels |
| 17 | `club` | Dashboard | Items, member purchases, settings |
| 18 | `club-customer` | Club | Customer balance and redemption shop |
| 19 | `members` | Customers | Search, filters, customer list/report |
| 20 | `points` | Customers | Points history and manual registration |
| 21 | `settings` | Settings | Rules, automated SMS, general settings |
| 22 | `setup` | Plugin activation gate | 4-step activation stepper: profile completeness → plan/pay → sender line → success (see §7.10) |

### 6.3 Bottom-sheet interactions

The reference includes 19 modal/bottom-sheet flows:

1. New campaign
2. New survey
3. New/edit radar zone
4. Campaign settings and send report
5. Send details
6. New/edit message template
7. Customer report
8. New/edit Club item
9. New/edit occasion
10. New/edit wheel
11. Wheel details and winners
12. New/edit reminder rule
13. Club redemption confirmation/result
14. Store-profile completion (`modal-profile`) — name/category checklist, gates activation
15. Plan payment (`modal-pay`) — single-plan card, card-number form, UI-only per §7.10
16. SMS credit purchase (`sms-sheet`) — six packages or a custom amount, ends in a gateway placeholder
17. Personal message (`modal-ps`, inside Bulk SMS) — one member or one segment, saved message library
18. Walk-in registration keypad (`modal-kbd`) — numeric mobile entry, +100 welcome balance
19. Quick club setup (`modal-ai` in the reference; delivered as a non-AI one-tap preset — see §7.10)

---

## 7. Functional Modules

### 7.1 Dashboard

- Dashboard-only **Manage Store** control and global notification control.
- Page title/subtitle beneath the app bar.
- SMS-credit card with balance, monthly use, progress, top-up action, and send-report entry.
- Quick actions for bulk SMS, wheel, survey, radar, and retargeting.
- Dedicated entry cards for Club and Reports.
- Customer, active-customer, active-campaign, and issued-points KPIs.
- Seven-day SMS chart, smart segments, and campaign summary.
- Store name, plan name, balances, and metrics must come from production data; HTML values are fixtures.

### 7.2 Campaigns and Club Structure

**Campaigns pane**

- Automatic campaigns: birthday, welcome, points expiry, and abandoned cart.
- Manual campaigns and automatic/manual filtering.
- New campaign: name, audience, optional linked tool, 320-character SMS, variables, immediate/scheduled send.
- Linked tools are active wheels and non-ended surveys.
- Campaign bottom sheet has **Settings** and **Send report** panes, event/time/active/business-hour settings, preview, success/error/undelivered counts, proportional bar, and last message.
- Bulk-SMS CTA.

**Club structure pane**

- Enable/configure cards for retargeting, wheel, surveys, radar, and reminders.

**Message templates pane**

- Three quick templates plus entry to the full template library.

### 7.3 Ten Functional Tools

| Tool | Entry | Delivered capability |
|---|---|---|
| **Referral / acquisition** | `acquire` | Referral code, inviter/invitee reward, daily cap, invitation SMS/history; lead-magnet link/funnel/gifts; assisted campaign goals, canned v1 text, audience/time suggestion, and predicted open rate |
| **Occasions** | `occasions` | Seeded non-deletable birthday plus custom title/date/time/audience/SMS, active state, edit/delete, and history |
| **Bulk SMS** | `smsgroup` | Multi-segment recipients, 320-character composer, variables, quick templates, preview, cost, immediate/scheduled send, sender/business-hour/daily-cap settings, test send, and history |
| **Reminders** | `reminders` | “X days since last purchase” rules (7/30/60/90/custom up to 365), audience, message, active state, history, send time, 30-day suppression, and business-hour setting |
| **Retargeting** | `buyback` | Return-credit percentage or fixed amount, cap, deadline, minimum basket, expiry reminder, channel/combination rules, two SMS templates, cashback grants, KPIs, and history |
| **Wheel** | `lucky` | Multiple wheels, per-wheel cost, 2–8 dynamic prizes, name/chance/color, total chance exactly 100%, spin preview, daily cap, VIP-free setting, participation points, winners, per-wheel details, and customer-preview link |
| **Surveys** | `surveys` | Multiple surveys, 2–6 options, audience, immediate/scheduled SMS with short link, results, non-respondent reminder, response reward, settings, and history |
| **Radar (Zone)** | `zones` | Multiple zones, point/circle mode with 200–3000m radius, polygon mode with 3–10 vertices and a trapezoid sample, zone-specific SMS, enable state, 24-hour suppression, business hours, and history |
| **Regional SMS** | `regional` | Province → city → neighborhood selection, select-all, available-recipient count, exact/percentage quota, random N-of-M selection, live cost, `{region}`, test/send, region cards, and history |
| **Club** | `club` / `club-customer` | Item image/category/points price/stock/active state, member purchases, settings, customer category filtering, points redemption, stock deduction, redemption code, and insufficient-points handling |

### 7.4 Customers and Points

- Search by name/mobile and filter by all, VIP, loyal, newcomer, and at-risk.
- Customer bottom sheet: current/earned/spent totals; points-history filters; reason for each transaction; purchase history with item, amount, date, and channel; direct SMS action.
- Points page: aggregate cards, transaction history, date/filter controls, manual add/deduct with reason, and report entry.
- Advanced segmentation entry.

### 7.5 Club

**Admin — 3 panes**

- Items: name, image upload/preview/remove, JPG/PNG image validation, maximum 2 MB in the reference, category (product/discount/service), points price, stock, description, and active state.
- Member purchases: customer, item, points spent, time, and fulfillment/use status.
- Settings: minimum points, daily purchase cap, and confirmation SMS with `{item}` and `{code}`.

**Customer preview**

- Customer identity and points balance.
- Category chips and active/in-stock item grid.
- Confirmation before redemption.
- Atomic business outcome: validate balance and stock, spend points, decrement stock, create purchase, issue redemption code, and send/queue confirmation. A failure must not leave a partial write.

### 7.6 Reports

- Date-range filters: today, this month, last 3 months, this year.
- KPIs: SMS sent, delivery rate, points issued, points spent.
- SMS performance: success/error/undelivered, proportional bar, and error analysis.
- Weekly send chart and tool reports for retargeting, wheel, survey, Club, and radar.
- Customer lifecycle funnel: visitor → lead → new customer → returning customer → churn.
- Total sales, average order value, and customer trend (new/returning/at-risk/VIP).
- Entries from Dashboard, send-report buttons, points report, and send-details report.

### 7.7 Settings

**Points and rules**

- Welcome points: 100.
- Every 10,000 Toman purchase: 1 point.
- Every 100 points: 10,000 Toman value.
- Minimum conversion/redemption threshold: 500 points.
- Validity: 12 months.
- Rounding and points-message templates.

**Automated SMS**

- Welcome, birthday, expiry, abandoned cart, and VIP-news switches.

**General**

- Default sender, business hours (default 09:00–21:00), SMS signature, and admin notifications.

### 7.8 Message Templates

- Nine categories: birthday, welcome, expiry, festival/discount, retargeting, wheel, survey, radar, general.
- Category filter, create, edit, use in campaign, name/category/text fields, and 320-character limit.
- Common variables include `{name}`, `{points}`, `{discount code}`, `{date}`, `{credit}`, `{prize}`, `{balance}`, `{title}`, `{link}`, `{days}`, `{region}`, `{item}`, `{code}`, and `{occasion}`.
- The production implementation may localize variable keys, but a template must use one consistent canonical key set internally.

### 7.9 Customer Segmentation

- **Points:** Bronze, Silver, Gold, Diamond with ranges and counts.
- **RFM:** Recency, Frequency, Monetary views and targetable groups (champions, loyal, at risk, new, dormant).
- **Custom labels:** product, payment gateway, acquisition channel, and other configured groups; create/delete labels and view labeled customers.
- RFM thresholds must be configurable server-side; Version 1 may ship with deterministic defaults.

### 7.10 Setup, Billing UI, and Prototype-only Extras

These five items were added by the newest prototype revision (commit `81fee16`, +183/−33 in
`customer-club-admin.html`) after the rest of this document was drafted; §6.2/§6.3's view/modal
counts above already include them.

**Setup wizard (`setup`, view 22).** A 4-step activation gate a store passes through once: (1)
store-profile completeness — name and category, `modal-profile` to complete them, or a
"temporary entry (skip)" path straight to the dashboard; (2) the single **باشگاه مشتریان** plan
card, **۲۹۰,۰۰۰ Toman/month** — the prototype's earlier three-tier رایگان/پایه/حرفه‌ای pricing and
its "unlimited SMS" tier were both removed in the same revision, replaced by one plan plus a
separately-purchased SMS credit basket; `modal-pay` collects a card number and always "succeeds"
(no real charge — see the next paragraph); (3) sender-line selection from the store's available
lines; (4) a success pane. An unactivated store landing on any club route redirects here.

**Billing is deliberately deferred, not simulated as complete.** The club's ۲۹۰,۰۰۰/month plan is a
per-plugin add-on, not a whole-store subscription tier (`subscriptions`'s `PlanTier` models exactly
one active tier per seller and would conflict with it — confirmed during implementation, not just
assumed). Both `modal-pay` and the SMS credit purchase sheet (`sms-sheet`) are **UI-only**: club
activation flips `StorePlugin.isActive` once the wizard completes, with no billing entity and no
real charge; the SMS sheet computes real package math (base 400 Toman/message, six tiers at
350→300 Toman/message with volume badges, and a custom-amount path that floors `amount / 400` and
rejects anything under 400 Toman) but ends in a "connecting to gateway" placeholder identical to the
prototype's own toast, not a real credit top-up. This mirrors the pattern `SmsCreditAccount` already
used for manual balance top-ups. Revisit both once a payment gateway (Zarinpal is the internal
candidate) is wired up — until then, treat §12's "Payment/top-up" dependency as **built UI, deferred
settlement**, not as out-of-scope.

**Quick club setup (`modal-ai` in the reference).** The prototype's picker lets an owner multi-select
7 plugin presets, plays a ~650ms-per-item staggered reveal animation, then calls it done. Verification
found this animation configures nothing: its "finish" handler writes one `localStorage` flag and
jumps to sender-line selection: every reward number shown (20% birthday discount, 15% win-back
discount, ۵۰۰ referral points, one free daily wheel spin) exists only in display copy, never
persisted. **Delivered as an honest, non-AI one-tap preset** instead ("راه‌اندازی سریع باشگاه"):
the same 7 toggles, but each writes to a real endpoint already shipped in Phases 2–4 — the points and
referral rules through the loyalty policy, a real birthday campaign against the seeded system
template, a real days-since-purchase retargeting rule, and a real free-entry wheel with prizes
summing to 100%. Two of the seven have no working automatic-send path today and report that plainly
rather than writing a rule that can never fire: an abandoned-cart reminder (no runner support for
that trigger yet) and a custom-occasion campaign (which requires a specific date the picker never
collects). Both percentage-based rewards (birthday 20%, win-back 15%) drop the percentage from their
applied copy, for the same reason discount codes are absent elsewhere in this document — cart
checkout has no live discount-application path yet.

**Personal message (`modal-ps`).** A third pane inside Bulk SMS for sending to exactly one member
(searchable by name/phone) or one loyalty segment, with a saved-message library supporting
create/edit/delete, riding the existing message-template storage rather than a new entity.

**Walk-in registration keypad (`modal-kbd`).** A numeric keypad for capturing a walk-in customer's
mobile number at the register, creating (or finding) the customer and granting the standard +100
welcome-points balance.

---

## 8. Points and Value Rules

| Event | Default / rule |
|---|---|
| Welcome | +100 points |
| Purchase | +1 point per 10,000 Toman |
| Wheel entry | Per-wheel configurable: free or configured points cost; reference choices include 100 and 200 points |
| Wheel participation | +5 points by default, independently configurable from entry cost |
| Survey response | +50 points, once per customer per survey |
| Referral | +500 inviter / +250 invitee, subject to daily cap and validation |
| Lead form completion | +100 points |
| Lead-to-first-purchase | 15% discount code, default 14-day validity |
| Club redemption | Deduct item points price after balance/stock validation |
| Expiry | 12 months by default |

The HTML also displays a monetary wheel-cost option as a demo choice. Enabling paid wheel entry in
production requires a defined payment/value-settlement path; without it, only free/points costs are
in Version 1 operation.

---

## 9. SMS Rules and Quotas

- Maximum **320 characters** per composed message.
- Reference unit cost: **250 Toman per recipient/message**, deducted from SMS credit.
- Default business hours: **09:00–21:00**; tool-specific settings may narrow the range.
- Bulk SMS: maximum **2 messages per customer per day** by default.
- Radar: maximum **1 message per person in any 24-hour window**.
- Reminder: maximum **1 reminder in a 30-day window**.
- Wheel: configurable daily spin cap; reference default is **3** per customer.
- Regional sends choose a random, non-repeating N recipients from M eligible numbers for the applicable window.
- Optional stop for customers inactive for 60 days.
- Invalid, opted-out, or otherwise ineligible numbers must be excluded before credit deduction.
- All date/window logic uses the store timezone; the current implementation standard is `Asia/Tehran`, not the server process timezone.

---

## 10. Key User Flows

### Flow A — Win back an at-risk customer

Dashboard → at-risk segment → Reminders → create 60-day rule → automated SMS with discount code →
inspect history and send details.

### Flow B — Set up the Club

Dashboard → Club → create item with image, points price, and stock → activate → preview customer page →
redeem with points → inspect member purchases.

### Flow C — Campaign with a wheel

Wheel → create/select a wheel and define prizes totaling 100% → Campaigns → new campaign → select the
active wheel as linked tool → send/schedule → inspect wheel details and winners.

### Flow D — Targeted regional SMS

Regional SMS → **Golestan** province → **Gorgan** city → select neighborhoods → set quota (for example,
1,000 of 12,000) → review live cost → send → inspect history.

### Flow E — Survey and follow-up

Surveys → create question and options → select audience → compose SMS with `{link}` → send/schedule →
open survey details → inspect results → remind non-respondents.

### Flow F — Customer support adjustment

Customers → open customer report → inspect points and purchases → Points → add/deduct with reason or
Retargeting → grant cashback → verify history.

---

## 11. Non-Functional Requirements

| Domain | Requirement |
|---|---|
| **Platform** | Mobile-first WebView/browser experience, responsive at 390px and above |
| **Reference fidelity** | Match the final HTML's order, copy, states, Persian numerals, sheets, toasts, and responsive behavior; exclude decorative desktop phone chrome |
| **Performance** | Reference HTML loads without third-party runtime dependencies; production routes should load core UI within 2 seconds under target conditions |
| **Accessibility** | RTL semantics, AA-oriented contrast, meaningful labels, keyboard-capable controls, and touch targets around 40px or larger |
| **Security** | Unique short-link/redemption tokens, authorization by store/customer, server-side validation, anti-abuse caps, and no client-trusted balances/chances |
| **Atomicity** | Transactions for Club redemption, wheel point effects, cashback, credit deduction, and other multi-record writes |
| **Errors** | Persian validation/error messages and visible feedback for every mutation |
| **Persistence** | HTML demo state is in memory; production state is API/database-backed |
| **Time** | Business logic uses explicit `Asia/Tehran` utilities; no server-local `Date#getHours`/`setHours` assumptions |
| **Images** | Validate type and maximum 2 MB; production upload/storage/CDN policy applies |
| **Testing** | Unit/integration coverage for quota, points, money, chance totals, single-award rules, and timezone boundaries; end-to-end smoke coverage for critical flows |

---

## 12. Dependencies and Integrations

- **SMS provider:** send, credit deduction, batching, delivery/error/undelivered reports, sender configuration.
- **Store builder:** plugin activation, orders, customers, carts, discount codes, channels, and reports.
- **Uploads/storage:** Club images through the platform storage provider.
- **Short-link service:** surveys, referral, lead magnet, and customer-preview links.
- **Location source:** customer app/permission for automatic radar hits; postal code/profile/reference data for regional selection.
- **Payment/top-up:** the plan-payment and SMS-credit purchase UI shipped in Version 1 (§7.10); only the actual gateway settlement — the real charge and the real credit top-up — remains deferred, pending a provider (Zarinpal is the internal candidate).
- **AI:** Version 1 is an assisted mock using deterministic goal-to-text suggestions. A model call is a future enhancement, not a Version 1 requirement.

---

## 13. Roadmap and Final Status

| Phase | Content | Final status |
|---|---|---|
| **Phase 1 — MVP** | Points/rules, bulk SMS, automated campaigns, templates, customers, settings, dashboard/reports, reminders | **Complete** |
| **Phase 2 — Loyalty** | Club, wheel, retargeting/cashback, surveys, occasions | **Complete** |
| **Phase 3 — Acquisition and intelligence** | Referral, lead magnet, assisted campaign, RFM/labels | **Complete** |
| **Phase 4 — Geographic and scale** | Radar, regional SMS, geographic history/quota, completed sales/lifecycle reporting | **Complete** |
| **Phase 5 — Setup, billing UI, and prototype-only extras** | Activation wizard, plan/pay UI, SMS-credit purchase UI, personal message, walk-in keypad, de-AI'd quick-setup preset (see §7.10) | **Complete** |
| **Phase 6 — Production extensions** | Gateway top-up, standalone customer app/location source, production media/CDN, ML RFM, full geographic dataset | **Future / outside Version 1** |

There are **no remaining feature phases inside the approved Version 1 admin-plugin scope**. See
`remaining-phases.md` for close-out, evidence boundaries, and launch dependencies.

---

## 14. Version 1 Acceptance Baseline

Version 1 is accepted at product-scope level when:

- all 22 views in §6.2 are reachable and retain the correct parent-tab state;
- the 19 bottom-sheet flows in §6.3 open, validate, save/cancel, and close correctly;
- all 10 tools in §7.3 expose their documented settings/history/results behavior;
- SMS composers enforce 320 characters and show preview, audience, cost, and delivery details where applicable;
- Club redemption and points/money mutations are atomic and server-authoritative;
- wheel prize chances total exactly 100% on both client and server;
- survey/referral/lead rewards cannot be awarded more than allowed;
- regional selection requires province and city (the neighbourhood tier was dropped — see §7.10-adjacent Stage 5a divergence notes in `remaining-phases.md`), and quota cannot exceed eligibility;
- radar polygon validation requires 3–10 vertices and radar suppression enforces 24 hours;
- customer reports show both points and purchase history;
- Persian/RTL/mobile fidelity is maintained at 390×844;
- fixture data and demo-only labels are replaced by tenant/store data in production.

The final HTML satisfies the visible reference interactions. Repository-level release evidence and
external-provider readiness are tracked separately from feature-scope completion.

---

## 15. Operational Risks and Open Decisions

These do not reopen Phases 1–4, but may block or limit production operation.

1. **SMS opt-out:** “reply 5” requires an inbound-SMS webhook and suppression path.
2. **Provider credentials:** real delivery requires valid provider credentials and approved sender lines.
3. **SMS-credit top-up:** the Version 1 UI may show the action, but a real gateway/manual top-up policy must exist before launch.
4. **Radar telemetry:** automatic passerby detection requires a customer-app location source and permission; zone configuration/manual use can exist without it.
5. **Regional data coverage:** the reference dataset contains six sample provinces (including Golestan); nationwide production coverage needs a maintained dataset.
6. **Points liability:** define caps, expiry communication, deactivation behavior, and treatment of outstanding balances.
7. **RFM thresholds:** ship configurable defaults and confirm thresholds with the client.
8. **Referral abuse:** enforce daily cap, identity/phone uniqueness, and first-purchase validation where rewards depend on purchase.
9. **Images:** enforce 2 MB/type limits and production storage/CDN policy.
10. **Ravi license:** install licensed font files; retain Vazirmatn fallback for development.
11. **Monetary wheel entry:** do not enable without a supported settlement/payment model and legal/product approval.

---

## 16. Glossary

| Term | Definition |
|---|---|
| **Club** | Point-based store where customers redeem items using points |
| **Retargeting** | Credit for a future purchase, plus manual cashback grants |
| **Radar** | Location-zone messaging for eligible nearby/passing customers |
| **Regional SMS** | Profile/postal-region targeting through province, city, and neighborhood |
| **Send quota** | Exact N recipients selected from M eligible regional numbers |
| **Cashback** | Manual gift credit granted to a specific customer |
| **Lead magnet** | Landing/form incentive that captures a lead and encourages first purchase |
| **RFM** | Recency / Frequency / Monetary customer analysis |
| **Linked tool** | Active wheel or survey attached to a campaign message |
| **Reference prototype** | `customer-club-admin.html`; final visual/interaction fixture with in-memory demo state |
