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

## 1. Blocking / functional

### 1.1 ClubTabBar navigation is dead
**Route:** `/plugin/customer-club/settings`
**Issue:** Clicking items in `ClubTabBar` does nothing — no navigation to the target pages.
**Expected:** Every tab navigates to its corresponding page, and the active tab reflects the current route.

### 1.2 Incomplete profile ("پروفایل ناقص") appears to be missing
**Reference:** `customer-club-admin.html`
**Issue:** I can't find this feature implemented anywhere.
**Expected:** Confirm whether it exists. If it does, tell me where. If it doesn't, implement it as shown in the mockup.

---

## 2. Layout & behavior

### 2.1 HeroCard collapse animation missing / page glitches on scroll
**Reference:** `19-8/collapse-header.png`
**Applies to:** Customer Club, Storefront dashboard, Seller (admin) dashboard.
**Issue:**
- The collapsing header card is not implemented.
- The banner is meant to hide on scroll, but instead of hiding it simply stops rendering — which makes the page visibly glitch/jump.

**Expected:**
- The header collapses into the compact card shown in the screenshot.
- The banner hides smoothly on scroll and restores smoothly — no jump, flicker, or layout shift.
- Identical behavior across all three dashboards.

### 2.2 Bell icon should not be in the Customer Club dashboard header
**Reference:** `19-8/bell-icon.png`
**Issue:** The bell icon does not belong in this header.
**Expected:** Remove it.

### 2.3 QuickActionsRow alignment
**Issue:** Items and their labels are not centered.
**Expected:** Each item is centered within its cell, and the label text is center-aligned.

### 2.4 Topbar consistency
**Issue:** Customer Club pages use their own header.
**Expected:** Every Customer Club page **except the dashboard** uses the shared `AdminTopbar`, exactly as the other plugins do.

---

## 3. Icons

### 3.1 No hard-coded inline SVGs
**Issue:** Icons are being pasted inline as raw SVG markup (e.g. the search/magnifier icon).
**Expected:** All icons come from the shared icon library and are imported from there. I already wrote a frontend skill covering this — please follow it.

### 3.2 Chevron instead of arrow
**Expected:**
- All Customer Club cards use `CHEVRON_LEFT`.
- **Exception:** the search/magnifier icon stays as-is.
- On the seller dashboard cards, replace `ARROW_LEFT` with `CHEVRON_LEFT`.

---

## 4. Visual / content

### 4.1 CustomerClubCard
**Reference:** `manooch-dashboard.html`
- Label: `مشاهده باشگاه مشتریان کسب و کار شما` → `مشاهده باشگاه`
- The "گزارشات" report button (title + cup icon) uses the green from the mockup, `#12B76A`.

### 4.2 Seller dashboard cards
**Reference:** `19-8/dashboard-card.png`
**Cards:** `اشتراک باقی‌مانده`, `مشتریان`, `گزارشات`, `باشگاه مشتریان`
**Expected:** Restyle all four to match the screenshot exactly (layout, spacing, colors, icon placement).

### 4.3 Plan renaming
| Current | New |
| --- | --- |
| پلن پیشرفته | Plan Pro — پلن پرو |
| پلن اقتصادی | Plan Standard — پلن استاندارد |

Apply everywhere the plan names appear: UI labels, badges, and any related copy.

---

## Definition of done
- All items above are addressed, or explicitly flagged as blocked with a reason.
- No inline SVG icons remain in the touched files.
- Collapse/scroll behavior is smooth on all three dashboards.
- No regressions in other plugins that share `AdminTopbar`.
