# Customer Loyalty Club — Store Builder Admin Panel

**Documentation version:** 1.1 — **Last updated:** 24 Mordad 1405 (2026-08-15) — **Status:** Version 1 feature scope complete

English project guide for the **Customer Loyalty Club**, a loyalty and SMS-marketing plugin for the
store-builder admin panel with a **mobile-first**, **RTL**, Ravi-based interface.

[راهنمای فارسی](./README.md)

---

## Final Status

The approved Version 1 feature scope is complete across four phases:

| Item | Status |
|---|---:|
| Completed phases | 4 of 4 |
| Reference views/screens | 21 of 21 |
| Bottom-navigation tabs | 5 of 5 |
| Functional tools | 10 of 10 |
| Tool cards inside the Tools hub | 9 of 9 |
| Separate Club entry from Dashboard | 1 of 1 |
| Reference modals/bottom sheets | 13 of 13 |

> **Clarification:** there are 10 functional tools, but only 9 appear in the Tools hub. **Club** is the tenth tool and opens from the Dashboard card; it is not a sixth footer tab.

Phase 5 contains extensions outside Version 1: a standalone customer app, real SMS-credit payment,
a location source for automatic radar triggers, a complete region dataset, production CDN/media
handling, and ML-based RFM.

---

## Files and Documentation

| File/folder | Purpose |
|---|---|
| [`customer-club-admin.html`](./customer-club-admin.html) | Final visual/interaction reference; single-file HTML/CSS/JS with in-memory demo data |
| [`PRD.md`](./PRD.md) | Final English PRD and authority for resolved requirements |
| [`PRD-باشگاه-مشتریان.md`](./PRD-باشگاه-مشتریان.md) | Approved Persian PRD and source for product intent/terminology |
| [`remaining-phases.md`](./remaining-phases.md) | Final delivery close-out for Phases 1–4 |
| [`README.md`](./README.md) | Persian project guide |
| [`readme-en.md`](./readme-en.md) | This English guide |
| `fonts/` | Local Ravi and Vazirmatn fonts; may be supplied separately from the current package |

### Source-of-truth order

1. `PRD.md` — final scope, rules, and acceptance criteria.
2. `customer-club-admin.html` — screen structure, visible behavior, validation, and UI copy.
3. `PRD-باشگاه-مشتریان.md` — approved Persian product intent.
4. `README.md` and `readme-en.md` — setup and project overview.
5. `remaining-phases.md` — delivery status and implementation-evidence boundary.

Store names, plan labels, phone numbers, links, dates, counts, and report values in the HTML are
**demo fixtures**, not production defaults.

---

## Run the HTML Reference

The reference needs no build tool or package installation:

1. Keep the files in one folder.
2. If licensed fonts are available, place them in `fonts/`.
3. Open `customer-club-admin.html` in a modern browser.

The default view is Dashboard. Use `?tab=` to open a view directly:

```text
customer-club-admin.html
customer-club-admin.html?tab=reports
customer-club-admin.html?tab=club
customer-club-admin.html?tab=club-customer
customer-club-admin.html?tab=lucky
customer-club-admin.html?tab=surveys
customer-club-admin.html?tab=regional
customer-club-admin.html?tab=segments
customer-club-admin.html?tab=templates
```

### Demo behavior

- Demo state is held in browser memory and resets on reload.
- Creating new records and the available edit flows for items, rules, templates, wheels, occasions, and zones are demonstrative.
- SMS delivery, credit purchase, link copying, AI execution, and some actions are simulated with toasts.
- The core interface has no framework or third-party runtime dependency. Any hosting-provider challenge script appended to the file is not product code and can be removed for standalone distribution.
- Desktop phone-frame elements (`.stage`, `.phone`, `.island`, `.statusbar`) are presentation chrome and do not belong in the production plugin UI.

---

## UI Architecture

### Bottom navigation — 5 tabs

1. **Dashboard** — SMS credit, quick actions, KPIs, charts, smart segments, campaigns, Club, and Reports entries.
2. **Campaigns** — campaigns, Club structure, and message templates.
3. **Tools** — 9 tool cards with enable, settings, and history actions.
4. **Customers** — search, filters, customer reports, points, and segmentation.
5. **Settings** — points/rules, automated SMS, and general settings.

On Dashboard, the Manage Store and notification controls are in the app bar. The page title/subtitle
renders immediately below the app bar. The `.title-pill` CSS class is unused and is not a delivered UI element.

### Final 21-view inventory

| Phase | `?tab=` views | Count |
|---|---|---:|
| Phase 1 | `dashboard`, `reports`, `campaigns`, `templates`, `smsgroup`, `tools`, `reminders`, `members`, `points`, `settings` | 10 |
| Phase 2 | `club`, `club-customer`, `lucky`, `surveys`, `survey-detail`, `occasions`, `buyback` | 7 |
| Phase 3 | `acquire`, `segments` | 2 |
| Phase 4 | `zones`, `regional` | 2 |
| **Total** |  | **21** |

### Modals and bottom sheets — 13

- New campaign
- New survey
- Create/edit radar zone
- Campaign settings and send report
- Send details
- Create/edit message template
- Customer report
- Create/edit Club item
- Create/edit occasion
- Create/edit wheel
- Wheel details and winners
- Create/edit reminder rule
- Club redemption confirmation/result

---

## Main Features

### Dashboard and Reports

- SMS-credit card, monthly usage, and send-report entry.
- Quick actions for bulk SMS, wheel, survey, radar, and retargeting.
- Customer, active-customer, active-campaign, and issued-points KPIs.
- SMS success/error/undelivered performance, weekly sends, and tool reports.
- Visitor → lead → new customer → returning customer → churn funnel.
- Total sales, average order value, and customer trends.

### Campaigns, SMS, and Templates

- Automatic and manual campaigns with filters.
- Campaign linking to an active wheel or non-ended survey.
- 320-character messages, variables, preview, and immediate/scheduled delivery.
- Multi-segment bulk SMS with live cost and history.
- Nine template categories: birthday, welcome, expiry, festival, retargeting, wheel, survey, radar, and general.
- Delivery details with success, error, undelivered, proportional bar, and error explanations.

### Customers, Points, and Segmentation

- Search by name/mobile and filter by VIP, loyal, newcomer, and at-risk.
- Customer report with balance, total earned/spent, point history, and purchase history.
- Manual point addition/deduction with a reason.
- Bronze, Silver, Gold, and Diamond tiers.
- RFM views based on Recency, Frequency, and Monetary, with targetable groups.
- Custom labels for product, gateway, acquisition channel, and other groups.

### Club

- Entered from Dashboard, not the footer.
- Three admin panes: items, member purchases, and settings.
- Item name, image, category, points price, stock, description, and active state.
- JPG/PNG preview/removal with a 2 MB reference limit.
- Customer view with balance, category filtering, point redemption, and insufficient-points error.
- Redemption business outcome: validate points/stock, spend points, decrement stock, create purchase, and issue a redemption code.

### Wheel

- Multiple wheels with independent cost and prizes.
- Minimum 2 and maximum 8 prizes in the final editor.
- Prize name, chance, and color; total chance must equal exactly 100%.
- Test spin, winners, per-wheel details, and customer-preview link.
- Per-wheel entry cost is separate from the default 5 participation points.
- Reference daily cap is 3 spins, with optional free VIP spins.

### Surveys

- Multiple surveys with 2–6 options.
- Audience, link-bearing SMS, and immediate/scheduled delivery.
- Recipient/response stats, percentage bars, and non-respondent reminder.
- Default 50-point reward, once per customer per survey.

### Reminders, Retargeting, and Occasions

- Reminder after 7/30/60/90 or a custom value up to 365 days since last purchase.
- Retargeting with percentage/fixed credit, cap, deadline, minimum basket, and issue/expiry messages.
- Manual cashback/gift credit with customer, amount, and reason.
- Non-deletable default birthday plus custom occasions with date, time, audience, and SMS.

### Customer Acquisition

- Referral code, default 500/250 rewards, and daily cap.
- Lead magnet with landing link, funnel, 100 form-completion points, and 15% first-purchase code.
- Version 1 assisted campaigns use a deterministic goal-to-suggested-text map; a real AI model call is outside Version 1.

### Radar and Regional SMS

- Point/circle radar with a 200–3000m radius.
- Free polygon mode with 3–10 vertices; “trapezoid” is only a sample shape.
- Per-zone message, history, and one-message-per-24-hours limit.
- Province → city → neighborhood regional targeting, multi-select, and select-all.
- Exact or percentage N-of-M quota, random selection, recipient count, and live cost.
- Reference data includes six sample provinces and the corrected **Golestan → Gorgan** path.

---

## Important Default Rules

| Rule | Reference value |
|---|---|
| SMS message limit | 320 characters |
| Displayed SMS cost | 250 Toman per recipient/message |
| Business hours | 09:00–21:00 |
| Bulk-SMS daily cap | 2 messages per customer |
| Radar suppression | 1 message per 24 hours |
| Reminder suppression | 1 message per 30-day window |
| Welcome | 100 points |
| Purchase earning | 1 point per 10,000 Toman |
| Point validity | 12 months |
| Survey response | 50 points |
| Referral | 500 inviter / 250 invitee |
| Lead magnet | 100 points + 15% first-purchase code |

All business date/window logic must use the explicit `Asia/Tehran` timezone, not the server process timezone.

---

## Ravi Font Setup

Ravi is a commercial **FontIran** typeface. Place licensed WOFF2 files in `fonts/` using these names:

```text
fonts/Ravi-Regular.woff2    # 400 — body
fonts/Ravi-Medium.woff2     # 500 — h2
fonts/Ravi-SemiBold.woff2   # 600 — h1
fonts/Ravi-Bold.woff2       # 700 — large numbers/emphasis
```

Development fallback:

```text
fonts/Vazirmatn-Regular.woff2
fonts/Vazirmatn-Medium.woff2
fonts/Vazirmatn-SemiBold.woff2
fonts/Vazirmatn-Bold.woff2
```

| Element | Weight |
|---|---:|
| h1 / page, card, and sheet title | 600 |
| h2 / section title | 500 |
| Body | 400 |
| Large figure/emphasis | 700 where needed |

All font faces use `font-display: swap`.

---

## Design Tokens

| Token | Value |
|---|---|
| Primary | `#6C4DF6` |
| Secondary purple | `#8E6BFF` |
| Background | `#F4F5FA` |
| Text | `#181B26` |
| Success | `#12B76A` |
| Error | `#F04438` |
| Warning | `#F79009` |
| Card gap | `14px` |
| Card padding | `16px` |
| Reference viewport | `390×844` |

---

## Demo vs. Production Boundary

### HTML reference

- Fixture data and in-memory state.
- Changes do not survive reload.
- No real SMS, payment, server upload, short-link, AI, or location integration.
- For visual acceptance, element order, copy, RTL, Persian numbers, tab/chip states, toasts, and sheets are authoritative.

### Production plugin

- Data comes from the store-builder API and database.
- Points balances, chances, quotas, opt-outs, credits, and stock are validated server-side.
- Multi-record operations such as Club redemption, wheel effects, cashback, and SMS-credit deduction are transactional.
- Club images use the platform storage provider.
- Schedules and quotas use `Asia/Tehran`.
- Fixtures such as the “DigiStyle” store name, plan label, and report figures are replaced by tenant data.

---

## Operational Dependencies Outside Feature Completion

These do not reopen Phases 1–4, but may be required for a real launch:

- Approved SMS-provider credentials and sender lines.
- Inbound-SMS webhook for opt-out/“reply 5”.
- Manual top-up or payment flow for SMS credit.
- Customer location source and permission for automatic radar triggers.
- Complete, maintained province/city/neighborhood data.
- Points-liability and plugin-deactivation policy.
- Client-approved RFM thresholds.
- Licensed Ravi files and a production image storage/CDN policy.
- Approved settlement model before enabling monetary wheel entry.

---

## Quick Acceptance Check

- [x] The HTML contains 5 primary tabs, 21 views, and 13 reference sheets.
- [x] `?tab=` navigation and parent highlighting exist.
- [x] All 10 functional tools are represented.
- [x] SMS composers provide a 320-character limit and preview.
- [x] Wheel prize totals are validated at 100%.
- [x] Point/polygon radar and quota-based regional SMS are represented.
- [x] Customer reports contain points and purchase history.
- [x] Club contains admin management and customer redemption flows.
- [x] Reports cover SMS, points, tools, lifecycle, customers, and sales.

For complete acceptance criteria, risks, and backend contracts, see [`PRD.md`](./PRD.md) and
[`remaining-phases.md`](./remaining-phases.md).
