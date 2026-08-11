# PRD — Manooch Ads & Banner / Notifications (compact)

You are a senior engineer on **Manooch**, a multi-store SaaS e-commerce platform ("Powered by Manooch"). This is the **Ads & Banner + Notifications** feature. Analyze the requirements below, propose the structure (mirroring the existing **banner feature** in admin & storefront), and give a concrete implementation plan (+ illustrative code) to build and test end-to-end.

**Reference images (read first):**
- `manooch-planning/portal/ads-16-5/banner-seller.png` — ads/banner as shown in the **seller dashboard**
- `manooch-planning/portal/ads-16-5/ads-humburgermenu.png` — the **ads section** in the hamburger menu

**Key idea:** Reuse/extend the existing **banner feature**'s structure/patterns (admin + storefront) so this stays consistent and reusable.

---

## Requirements

### 1. Super admin — add banner & send notifications by business category
- As **super admin** (portal), I should be able to:
  - **Add a banner** and
  - **send notifications**,
  - targeting **business category** — I can **select multiple categories**, or send to **all** categories.
- So super-admin banners/notifications are delivered to stores based on their business category (multi-select or all).

### 2. Super admin → seller notifications: two targeting methods
The **notification** feature (super admin → seller/admin) can be customized in **two ways**:
- **Method A — by business category:** select one or more business categories (or all), as described above.
- **Method B — select specific stores + schedule:** for notifications only, the super admin can **select specific stores** to notify and set a **schedule** (date/time to send).
- So a notification can be sent either by business category or to chosen specific stores on a schedule.

### 2b. Banner & notification lifecycle after the schedule ends
- **Banners:** a banner can be **scheduled**. When the banner's **show time ends**, the banner should **automatically unpublish** (no longer shown).
- **Notifications:** when a scheduled notification's **show time ends**, it is **NOT deleted or unpublished**. Instead it should just get a **disabled style** and be shown with **lower opacity** compared to the other (active) notifications. So expired notifications remain visible in a visually-disabled, faded state, not removed.

### 3. Seller — own notification & banner on the storefront
- Each **seller** can set their **own notification and banner** on their storefront (per-store, seller-controlled).
- This works independently alongside the super-admin category-based banners/notifications.

### 4. Display
- **Seller dashboard:** show the ads/banner (see `banner-seller.png`).
- **Storefront hamburger menu:** an **ads section** lists/shows the ads (see `ads-humburgermenu.png`).

---

## Deliverables: proposed data model • super-admin banner by category • notification targeting (Method A: category multi/all; Method B: specific stores + schedule) • banner schedule auto-unpublish • notification expiry (disabled style, lower opacity, not deleted) • seller per-store banner/notification • storefront/dashboard + hamburger rendering • how super-admin category banners vs seller-owned banners combine • edge cases.
**Align with:** reuse/extend the existing banner feature's structure/patterns.
**Edge cases:** empty state (no banners/notifications); no category selected vs "all"; specific-store selection + schedule (scheduling, timezone, unscheduled/send-now); banner auto-unpublish when show time ends; notification expiry → disabled style + lower opacity (not deleted), vs active notifications; a seller belonging to multiple categories; precedence/combination when both a category-based banner and the seller's own banner exist; enable/disable & lifecycle; consistent behavior between admin config and storefront/dashboard rendering.
