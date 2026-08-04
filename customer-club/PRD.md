# PRD — Customer Loyalty Club (Store Builder Admin Panel)

**Version:** 1.0 — **Date:** Mordad 1405 — **Status:** Approved / Ready for development

---

## 1. Executive Summary

The "Customer Loyalty Club" is a loyalty and SMS-marketing module for online and physical stores, offered in the **store builder's admin panel**. Its goal is to convert ordinary customers into loyal customers through a **points system, smart automated SMS, customer acquisition and win-back tools, and a store for point-based items (Club)**.

The product is designed in a **mobile format** (store management from mobile), using the **Ravi** font and a fully **right-to-left (RTL)** structure.

### Key Product Values
1. **Sales growth**: acquiring new customers (referral/lead magnet) and win-back of churned customers (retargeting/reminders)
2. **Customer retention**: points, club, wheel of fortune, occasions
3. **Data-driven decisions**: comprehensive reports, RFM segmentation, SMS send details
4. **Full automation**: event-based automated SMS (birthday, X days without purchase, expiry, etc.)

---

## 2. Goals and Success Metrics (KPIs)

| Goal | Metric (KPI) | Target (first 6 months) |
|---|---|---|
| Increase membership | Number of club customers | +30% |
| Customer win-back | Retargeting credit usage rate | ≥ 45% |
| Acquisition via invite | Referral conversion rate | ≥ 40% |
| SMS engagement | Delivery rate | ≥ 96% |
| Participation | Survey participation | ≥ 25% |
| Points usage | Points spent (club/wheel/discount) | ≥ 30% of issued points |
| Churn | Reduction of at-risk customers | −20% |

---

## 3. Audiences and Usage Scenarios

| Role | Primary Need | Key Scenario |
|---|---|---|
| **Store owner/manager** | Sales growth and loyalty | Bulk SMS to the "at risk of churn" segment with a 20% discount |
| **Marketing operator** | Running campaigns | Build Nowruz wheel → link to campaign → monitor winners |
| **Support specialist** | Managing customers | View customer purchase history and points, record cashback |
| **End customer** (customer app) | Using points | Buy an item from the club / spin the wheel with points |

---

## 4. Product Scope

### 4.1 In Scope (Version 1)
- Mobile admin panel with 5 main tabs + subpages
- Points and rules management, segmentation (points/RFM/labels)
- SMS campaigns (automated/manual/smart AI), categorized message templates
- 10 loyalty tools (listed in section 7.3)
- Club: define items with image + points purchase + customer page
- Comprehensive reports and send details (success/error/undelivered)
- Customer purchase history and gift credit (cashback)

### 4.2 Out of Scope (Later Versions)
- Standalone customer app (currently an in-panel preview page)
- Real payment gateway integration for buying SMS credit
- Web scenario (currently mobile-first)
- ML-based automated RFM scoring (version 2)

---

## 5. Design Principles

### 5.1 Typography — Ravi font

| Element | Weight |
|---|---|
| h1 (page/card title) | **SemiBold (600)** |
| h2 (section title/subtitle) | **Medium (500)** |
| Body text | **Regular (400)** |

> Ravi is a commercial font (FontIran); licensed woff2 files go in the `fonts/` folder, and until they are available "Vazirmatn" is shown as a fallback.

### 5.2 Color and Spacing
- **Primary color:** Purple `#6C4DF6` — background `#F4F5FA` — text `#181B26`
- Status colors: success `#12B76A`, error `#F04438`, warning `#F79009`
- Card gap 14px, card padding 16px, section-title spacing 28px

### 5.3 Layout
- **Mobile-first** (390×844) with a phone frame on desktop
- Full RTL + Persian numerals (automatic conversion)

---

## 6. Information Architecture and Navigation

```
Bottom bar (5 tabs)

├── 1) Dashboard
│     ├── Header: "Manage Store" button (light) + subtitle under menu title
│     ├── SMS credit card, stats, send chart
│     ├── Entry cards: Club, Reports
│     └── Tool quick actions
├── 2) Campaigns and Club Structure (3 inner tabs)
│     ├── Campaigns (list + bulk SMS CTA)
│     ├── Club structure (active/configure 5 tools)
│     └── Message templates
├── 3) Tools (hub of 10 tools — each: settings + history)
├── 4) Customers
│     ├── Search/segmentation filter
│     ├── Customer report modal (points + purchase history)
│     └── Entry to advanced segmentation
└── 5) Settings (3 tabs)
      ├── Points and rules
      ├── Automated SMS
      └── General
```

**Subpages** (with back button and parent-tab highlight): referral, occasions, regional SMS, club (+ club customer page), bulk SMS, retargeting, wheel of fortune, survey, radar, reminders, points management, segmentation, message templates, reports.

---

## 7. Functional Modules

### 7.1 Dashboard
- **Header:** "Manage Store" button (light style, this page only) + "Customer Loyalty Club" title below the top menu
- **SMS credit card:** balance, monthly usage, progress bar, buy credit (gateway integration in version 2)
- **Stats:** customers, active, active campaigns, issued points
- **Chart** of last 7 days of sends + **smart segmentation** + **quick actions**
- **Entry cards:** Club and Reports
- **Notifications** (icon in header)

### 7.2 Campaigns and Club Structure

**Campaigns tab:**
- List of automated campaigns (birthday, welcome, points expiry, abandoned cart) and manual ones
- Settings modal per campaign: **"Settings" tab** (event, time, active, business hours, dedicated SMS with preview) + **"Send report" tab** (success/error/undelivered + relative bar + last SMS)
- **Linked tool:** select wheel/survey to link the SMS
- Auto/manual filter + bulk SMS CTA

**Club structure tab:**
- Configuration card for 5 tools: retargeting, wheel of fortune, survey, radar, reminders — with active switch and configure button

**Message templates tab:** 3 quick templates + link to the full templates page

### 7.3 Tools (10 tools)

| Tool | Page Entry | Capabilities |
|---|---|---|
| **Referral (customer acquisition)** | `acquire` | Invite code, inviter/invitee reward, daily cap, invite SMS, history + **lead magnet** (landing link, conversion funnel, gift) + **AI smart campaign** (text generation, audience/time suggestion, open-rate prediction) |
| **Occasions** | `occasions` | Birthday (default, cannot be deleted) + custom occasions (title, date, time, customer category, SMS with `{occasion}`) + history |
| **Bulk SMS** | `smsgroup` | Multi-segment recipient selection, 320-character counter, live cost estimate, preview, quick templates, scheduling, send settings, history |
| **Reminders** | `reminders` | Rule: "if X days since last purchase ← automated SMS" — days 7/30/60/90 or custom, segmentation, `{days}` variable, history with details |
| **Retargeting** | `buyback` | Return credit percentage, cap, deadline, minimum cart, SMSs + **cashback tab**: record gift credit (customer/amount/reason) + history |
| **Wheel of fortune** | `lucky` | **Multiple wheels with different items** (prize name + chance + color, dynamic rows, total 100%) — tabs: wheels / spins and prizes / winners / settings — **details of each wheel including that wheel's winners** + customer preview link |
| **Survey** | `surveys` | Create multiple surveys (title/question/dynamic options), send short link in SMS, percentage results, reminder to non-respondents, points reward |
| **Radar (Zone)** | `zones` | Geographic zones with **two modes: point (radius) and trapezoid (click on map for vertices)** — dedicated SMS per zone, one SMS in 24 hours |
| **Regional SMS** | `regional` | **Hierarchical selection province → city → neighborhood** (multi-select) + **send quota** (from N available numbers, send to M — numeric/slider input) + live cost |
| **Club** | `club` | Point-based items with **image upload**, category (product/discount/service), points price, stock + member purchases + settings + **customer page** (balance, purchase with redemption code) |

### 7.4 Customers
- Search (name/mobile) + segmentation filter (VIP, loyal, newcomer, at risk of churn)
- **Customer report modal:** balance/earned/spent cards + **"Points" tab** (history with reason: purchase, reward, spin, survey, club, expiry, etc.) + **"Purchase history" tab** (item, amount, date, channel) + send SMS
- Entry to **advanced segmentation** (points / RFM / labels)

### 7.5 Club
- **Admin (3 tabs):** Items (image/category/price/stock) • member purchases • settings (minimum points, daily cap, confirmation SMS template with `{item}` `{code}`)
- **Customer (preview page):** balance card, item categorization, purchase with points → stock deduction + redemption code + "insufficient points" error

### 7.6 Reports
- Date-range filter (today/month/3 months/year)
- KPIs: SMS sent, delivery rate, points issued/spent
- **SMS performance** (success/error/undelivered + analysis) • **weekly sends** • **tools report** • **customer lifecycle funnel** (visit → lead → new customer → return → churn) + total sales and average order • customer trend
- Entries: dashboard card, "send report" button, "full report" for points, "view full report" for send details

### 7.7 Settings (3 tabs)
- **Points and rules:** welcome 100, every 10,000 Toman = 1 point, every 100 points = 10,000 Toman, minimum redemption 500, 12-month validity, rounding + points message templates
- **Automated SMS:** 5 switches (welcome, birthday, expiry, abandoned cart, VIP news)
- **General:** default sender, business hours (9–21), SMS signature, admin notifications

### 7.8 Message Templates (separate page)
- 9 categories: birthday, welcome, expiry, festival, retargeting, wheel of fortune, survey, radar, general
- Category filter + "use in campaign" + "edit" (name/category/text) + create with "+"
- Common variables: `{name}` `{points}` `{discount code}` `{date}` `{credit}` `{prize}` `{balance}` `{title}` `{link}` `{days}` `{zone}` `{item}`

### 7.9 Customer Segmentation
- **By points:** Bronze/Silver/Gold/Diamond
- **RFM:** R (last purchase) / F (frequency) / M (monetary) analysis + categories (champions, loyal, at risk, new, dormant) with targeting
- **Custom labels:** product, payment gateway, acquisition channel — create/delete + customers with label

---

## 8. Points Rules (default)

| Event | Points |
|---|---|
| Welcome | 100 |
| Every 10,000 Toman purchase | 1 |
| Each wheel spin | 5 (participation) |
| Survey response | 50 |
| Invite a friend (inviter / invitee) | 500 / 250 |
| Lead magnet form completion | 100 |
| Lead-to-purchase conversion | 15% code |
| Expiry | after 12 months |

---

## 9. SMS Rules and Quotas

- Maximum **320 characters** per SMS • cost **250 Toman/SMS** (deducted from credit)
- Sending only during **business hours 9–21** (configurable)
- **Maximum 2 daily SMS per customer** (bulk SMS)
- Radar: maximum **one SMS in 24 hours** to each passerby
- Reminder: maximum one SMS per 30-day window
- Regional quota: send to N numbers out of the total selected numbers (random selection)
- Stop sending to inactive customers (60 days) — can be disabled

---

## 10. Key User Flows

### Flow A — Win back a churned customer
Dashboard → "at risk of churn" → create reminder rule (60 days) → automated SMS with discount code → track in history/send details

### Flow B — Set up the Club
Club → create item (image, points price, stock) → activate → preview customer page → monitor member purchases

### Flow C — Campaign with wheel
Wheel of fortune → create wheel with custom items → Campaigns → new campaign → select "linked tool: wheel" → run → wheel details (winners)

### Flow D — Targeted regional SMS
Regional SMS → province (Tehran) → city (Gorgan) → neighborhoods → quota (1,000 of 12,000) → send → history

---

## 11. Non-Functional Requirements

| Domain | Requirement |
|---|---|
| **Platform** | Mobile-first (iOS/Android WebView priority) — responsive down to 390px |
| **Performance** | Single-file HTML with no dependencies; load < 2 seconds; font with `font-display:swap` |
| **Accessibility** | RTL, Persian numerals, at least AA contrast, touch size ≥ 40px |
| **Security** | Links/codes with unique tokens; stop sending to invalid numbers; anti-abuse quota limits |
| **Errors** | Toast for all actions; form validation with Persian messages |
| **Local storage** | Current demo holds state in memory; production version: store builder API |

---

## 12. Dependencies and Integrations

- **SMS engine**: SMS panel (deduct from credit, delivery/error/undelivered report)
- **Store builder**: orders, customers, discount codes, gateway (for buying credit)
- **Location service**: customer app (for radar) + postal code/profile (for regional)
- **Link shortener**: survey/referral/landing links
- **AI**: text-generation service + audience/time suggestion (version 1: mock-up)

---

## 13. Roadmap (phases)

| Phase | Content |
|---|---|
| **Phase 1 (MVP)** | Points and rules, bulk SMS, automated campaigns, templates, customers, settings |
| **Phase 2 (loyalty)** | Club, wheel of fortune, retargeting + cashback, survey, occasions |
| **Phase 3 (acquisition and intelligence)** | Referral, lead magnet, AI smart campaign, RFM/label segmentation |
| **Phase 4 (geographic and scale)** | Radar, regional SMS (province/city/neighborhood + quota), sales reports |
| **Phase 5 (production)** | API integration, gateway, real customer app, image upload to server, ML-based RFM |

---

## 14. Risks and Open Points

1. **SMS regulations**: need an opt-out mechanism (reply 5) and a minimum interval between sends
2. **Referral abuse**: daily reward cap + confirmation of the invitee's first purchase
3. **Club image size**: max 2 MB/image + CDN caching
4. **RFM accuracy**: define thresholds with the client (defaults in version 1)
5. **Regional quota accuracy**: random selection must be fair and non-repeating within the window
6. **Ravi font**: license required; Vazirmatn fallback for development

---

## 15. Appendix: Glossary

| Term | Definition |
|---|---|
| **Club** | Store of point-based items that the customer buys with points |
| **Retargeting** | Return credit for a purchase (on the next purchase) + cashback |
| **Radar** | SMS to passersby within defined geographic zones |
| **Send quota** | A specified number out of the total numbers of a selection (regional) |
| **Cashback** | Manual gift credit for a specific customer |
| **Lead magnet** | Attracting a visitor with a form/landing and gift, converting to a customer |
| **RFM** | Analysis based on Recency / Frequency / Monetary |
