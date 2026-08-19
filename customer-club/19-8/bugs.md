# Customer Club — Bug & Change Report (19/08)

**Scope:** Customer Club plugin (admin + dashboard), Storefront dashboard, Seller (admin) dashboard.

**Reference files**
- `manooch-planings/customer-club/customer-club-admin.html`
- `manooch-planings/customer-club/manooch-dashboard.html`
- `manooch-planings/customer-club/19-8/collapse-header.png`
- `manooch-planings/customer-club/19-8/bell-icon.png`
- `manooch-planings/customer-club/19-8/dashboard-card.png`

**Ground rules for this task**
- Match the referenced HTML mockups and screenshots as the source of truth.
- Follow the existing project conventions (icon library, shared components, styling approach) — do not introduce one-off patterns.
- Do not describe or propose implementation logic in your reply; report what changed and where.

---

## 1. Architecture & code style — read this first

This is the root problem, and it is more important than any single UI bug below. Several
items in sections 2–5 are symptoms of it. Fix this first; some of the others may disappear
on their own.

### 1.1 Customer Club does not follow the frontend style guide
**Issue:** The Customer Club module was not built to the frontend coding style guide. It
diverges from the conventions every other module follows.
**Expected:** Bring it into full conformance with the style guide — naming, file and folder
layout, component boundaries, imports, and styling approach.

### 1.2 Module structure must mirror the other modules
**Issue:** Customer Club is structured differently from the rest of the codebase, so it
doesn't behave like a peer module.
**Expected:** Restructure it so its anatomy is indistinguishable from any other module. Pick
an existing, well-formed module as the reference and mirror it: same folder hierarchy, same
file naming, same placement of components / routes / styles / icons, same import patterns.
No Customer-Club-only conventions.

### 1.3 Reuse the shared components — colors are the only allowed difference
**Issue:** Customer Club components look like the shared ones but are separate
implementations, which is why they drift.
**Expected:** Use the existing shared components rather than parallel copies. Customer Club's
visual identity comes **only** from color differences, applied through the project's normal
theming/token mechanism — not by forking or overriding a component. If a shared component
genuinely can't express what a screen needs, flag it to me instead of forking it.

**Before starting:** confirm which module you're using as the structural reference, and list
any place where a shared component can't be reused. Don't guess.

---

## 2. Blocking / functional

### 2.1 ClubTabBar navigation is dead
**Route:** `/plugin/customer-club/settings`
**Issue:** Clicking items in `ClubTabBar` does nothing — no navigation to the target pages.
**Expected:** Every tab navigates to its corresponding page, and the active tab reflects the current route.

---

## 3. Layout & behavior

### 3.1 HeroCard collapse animation missing / page glitches on scroll
**Reference:** `19-8/collapse-header.png`
**Applies to:** Customer Club, Storefront dashboard, Seller (admin) dashboard.
**Issue:**
- The collapsing header card is not implemented.
- The banner is meant to hide on scroll, but instead of hiding it simply stops rendering — which makes the page visibly glitch/jump.

**Expected:**
- The header collapses into the compact card shown in the screenshot.
- The banner hides smoothly on scroll and restores smoothly — no jump, flicker, or layout shift.
- Identical behavior across all three dashboards.

### 3.2 Bell icon should not be in the Customer Club dashboard header
**Reference:** `19-8/bell-icon.png`
**Issue:** The bell icon does not belong in this header.
**Expected:** Remove it.

### 3.3 QuickActionsRow alignment
**Issue:** Items and their labels are not centered.
**Expected:** Each item is centered within its cell, and the label text is center-aligned.

### 3.4 Topbar consistency
**Issue:** Customer Club pages use their own header.
**Expected:** Every Customer Club page **except the dashboard** uses the shared `AdminTopbar`, exactly as the other plugins do.

---

## 4. Icons

### 4.1 No hard-coded inline SVGs
**Issue:** Icons are being pasted inline as raw SVG markup (e.g. the search/magnifier icon).
**Expected:** All icons come from the shared icon library and are imported from there. I already wrote a frontend skill covering this — please follow it.

### 4.2 Chevron instead of arrow
**Expected:**
- All Customer Club cards use `CHEVRON_LEFT`.
- **Exception:** the search/magnifier icon stays as-is.
- On the seller dashboard cards, replace `ARROW_LEFT` with `CHEVRON_LEFT`.

---

## 5. Visual / content

### 5.1 CustomerClubCard
**Reference:** `manooch-dashboard.html`
- Label: `مشاهده باشگاه مشتریان کسب و کار شما` → `مشاهده باشگاه`
- The "گزارشات" report button (title + cup icon) uses the green from the mockup, `#12B76A`.

### 5.2 Seller dashboard cards
**Reference:** `19-8/dashboard-card.png`
**Cards:** `اشتراک باقی‌مانده`, `مشتریان`, `گزارشات`, `باشگاه مشتریان`
**Expected:** Restyle all four to match the screenshot exactly (layout, spacing, colors, icon placement).

### 5.3 Plan renaming
| Current | New |
| --- | --- |
| پلن پیشرفته | Plan Pro — پلن پرو |
| پلن اقتصادی | Plan Standard — پلن استاندارد |

Apply everywhere the plan names appear: UI labels, badges, and any related copy.

---

## Definition of done
- Customer Club's structure and code style are indistinguishable from the reference module.
- No forked copies of shared components remain; Customer Club's differences are color-only.
- All items above are addressed, or explicitly flagged as blocked with a reason.
- No inline SVG icons remain in the touched files.
- Collapse/scroll behavior is smooth on all three dashboards.
- No regressions in other plugins that share `AdminTopbar` or the shared components.
