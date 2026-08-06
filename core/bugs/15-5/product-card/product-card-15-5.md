# Product Card Redesign + Filter Bottomsheet — Implementation Plan & Prompt

**Project:** manooch-fronts → storefront
**Files in scope**
- `manooch-fronts/apps/storefront/app/[slug]/_common/ProductList/ProductCard/ProductCard.tsx`
- `manooch-fronts/apps/storefront/app/[slug]/_common/FilterBar/FilterBar.tsx`

**Reference designs (local):**
1. `card-unit-attributes-templete.jpg` — layout reference for how **units, pricing, and attributes** appear on the card. This image also contains a counter, but **only the card layout is adopted from it** (not the counter behavior). **Colors are already correct — do not change the palette.**
2. `card-counter-cart-button.jpg` — reference for the **in-cart state**: the add button becomes a counter, and a **big sticky CTA** appears pinned above the footer nav showing the number of items in the cart.
3. `card-without-unit-attributes-pricing.jpg` — reference for the **price-less variant**: same card, but units and attributes are shown **without any prices**.

---

## Part A — The Plan

### 1. Objective

Redesign the storefront product card so that a product's **units** (e.g., sizes/portions/variations), their **prices**, and its **attributes** (e.g., descriptors/tags/options) are displayed directly on the card in the structure shown in the reference template. The card must support three presentation states, a cart stepper state, and a sticky cart CTA pinned above the footer navigation. Separately, the FilterBar's filter-icon button must open the **product filter bottomsheet**.

### 2. Scope

| # | Item | Type |
|---|------|------|
| 1 | Product card layout redesign (units, pricing, attributes) | UI change |
| 2 | Card state: default "Add" button | UI change |
| 3 | Card state: in-cart counter (stepper) | UI + behavior |
| 4 | Card variant: units/attributes without pricing | UI variant |
| 5 | Big sticky cart CTA above footer nav with cart item count | New UI element |
| 6 | FilterBar filter-icon button opens product filter bottomsheet | Behavior fix |

### 3. Product Card — structural breakdown

Think of the redesigned card as stacked zones. The **exact order, spacing, and alignment of these zones must follow `card-unit-attributes-templete.jpg`** (layout only):

1. **Media zone** — product image.
2. **Identity zone** — product name (and short description, if the template includes one).
3. **Attributes zone** — the product's attributes rendered as compact chips/badges. These communicate product traits/options at a glance.
4. **Units zone** — every purchasable unit of the product is listed (e.g., each size/portion/variation). In the default variant, **each unit displays its own price** next to it.
5. **Action zone** — either the **Add** button (not in cart) or the **counter** (in cart).

**Design note from the requester:** the color palette in the current card/template is approved. The redesign is **strictly about layout and information structure** — do not introduce new colors, and reuse the existing tokens for background, text, accent, and borders.

### 4. Card state 1 — Default (not in cart)

- The card presents name, attributes, units with their prices, and a single **Add** action.
- The Add action's placement follows the template (typically anchored to the card's bottom or action zone).
- If a product has **multiple units**, the first tap on Add adds the default/first unit (or the currently selected unit, if the template shows a selectable unit list — confirm against the reference image).

### 5. Card state 2 — In-cart (counter)

Per `card-counter-cart-button.jpg`:

- Once the customer adds the product, the Add button is **replaced in place by a counter control**: **minus (–)**, current **quantity**, **plus (+)**.
- **Plus** increments the quantity (respecting any stock/maximum limit).
- **Minus** decrements; when the quantity returns to **zero**, the counter reverts to the **Add** button.
- If the product has multiple units that can each be in the cart, the counter reflects the quantity of the relevant/selected unit (confirm placement per reference).
- The counter and the Add button should occupy the **same footprint** so the card does not jump or reflow when switching states.

### 6. Sticky cart CTA (pinned above footer nav)

Per `card-counter-cart-button.jpg`:

- A **large, prominent CTA bar** appears as soon as the cart contains **1 or more items**.
- It is **sticky and pinned directly above the footer navigation** (attached to it — no gap, and it never overlaps or floats detached). When the footer nav is visible, the CTA rides on top of it.
- The CTA **displays the number of items currently in the cart** (e.g., "View Cart · 3 items" — final wording/iconography per template).
- Tapping it navigates to the **cart**.
- When the cart is emptied, the CTA **disappears**.
- It should appear/disappear with a smooth transition (slide/fade) rather than abruptly.
- It must remain visible while scrolling the product list and must not cover card content — the list gets bottom padding equal to the CTA height while it is visible.
- Hide it on screens where it doesn't belong (e.g., the cart/checkout page itself).

### 7. Card variant — No pricing on units or attributes

Per `card-without-unit-attributes-pricing.jpg`:

- Identical layout and structure to the standard card, **but prices are omitted** from the units zone and any price is removed from the attributes zone.
- Name, attributes, and unit names still render; only the price figures are hidden.
- The Add/counter behavior stays exactly the same.
- This should be treated as a **display variant driven by configuration/data** (e.g., a store-level flag or missing price data), not a separate hard-coded card.

### 8. Product list integration

- The card is rendered inside the storefront product list at `[slug]`.
- Every card's counter state must **reflect live cart state** (quantity already in cart for that product/unit), and update instantly on add/increment/decrement.
- The sticky CTA's item count reads from the same cart state and is always consistent with the sum shown on the cards.
- The layout must hold for edge cases: long product names (truncate/wrap per template), products with many units, products with no attributes, missing image (placeholder).

### 9. FilterBar fix — open the product filter bottomsheet

In `manooch-fronts/apps/storefront/app/[slug]/_common/FilterBar/FilterBar.tsx`:

- The FilterBar contains a button with a **filter icon**. Currently it does not surface the product filter UI.
- **Expected behavior:** tapping the filter-icon button **opens the product filter bottomsheet** — the panel that slides up from the bottom of the screen and presents the product filtering options.
- The bottomsheet experience:
  - Slides up from the bottom over a dimmed backdrop.
  - Tapping the backdrop or dragging it down dismisses it.
  - Page scroll behind the sheet is locked while open.
  - The sheet shows the product filter options (as defined in the existing filter UI), with the currently applied filters pre-selected.
  - Applying filters updates the product list; clearing resets them.
- If the design calls for it, the filter button should visually indicate when filters are active (e.g., a badge with the active filter count) — confirm against design; otherwise keep the icon as-is.
- This must work anywhere the FilterBar appears within the `[slug]` storefront context.

### 10. UX details & consistency requirements

- **No layout shift** when the Add button swaps to the counter.
- Counter respects stock limits; at max, plus is disabled or gives feedback.
- The sticky CTA, counter, and card all read from one cart source of truth — no count drift.
- Keep the existing color palette; match the reference templates for spacing, radii, and typography hierarchy.
- Respect the storefront's direction (RTL/LTR) in all three states — card content, counter, CTA, and bottomsheet.
- Smooth micro-transitions on button→counter swap, CTA show/hide, bottomsheet open/close.

### 11. Acceptance criteria (checklist)

- [ ] Card displays units, unit prices, and attributes matching the template layout.
- [ ] Price-less variant renders units/attributes with no prices, matching its reference.
- [ ] Colors unchanged from current palette.
- [ ] Add → counter swap works; quantity persists and syncs with cart; zero returns to Add.
- [ ] Sticky CTA appears above footer nav when cart ≥ 1 item, shows correct live item count, navigates to cart, disappears when cart empties.
- [ ] CTA never overlaps content; list bottom padding adjusts.
- [ ] FilterBar filter-icon button opens the product filter bottomsheet; backdrop/drag dismiss works; applying filters updates the list.
- [ ] Long names, many units, no-attribute products, and missing images render cleanly.
- [ ] Works in the storefront's text direction and on mobile viewport widths (it's a bottomsheet/footer-nav experience — mobile-first).

### 12. Out of scope

- Cart page or checkout redesign.
- Backend/API changes (assumes cart state, unit/attribute/pricing data already available).
- Any color/palette changes.
- Changes to the filter options themselves (only wiring the button to open the sheet).

---

## Part B — The ready-to-use prompt (no coding logic)

> Copy everything between the lines into your coding assistant, and attach the three reference images to it.

---

Redesign the storefront product card and fix the filter bar button in the manooch-fronts storefront app.

TARGET FILES
- The product card: `manooch-fronts/apps/storefront/app/[slug]/_common/ProductList/ProductCard/ProductCard.tsx`
- The filter bar: `manooch-fronts/apps/storefront/app/[slug]/_common/FilterBar/FilterBar.tsx`

REFERENCE IMAGES (attached)
1. `card-unit-attributes-templete.jpg` — use this ONLY for the card's layout: how units, their prices, and attributes are arranged on the card. Ignore everything else in this image (it happens to show a counter; the counter treatment comes from image 2). The colors in it are already correct — do not change any colors.
2. `card-counter-cart-button.jpg` — use this for the state after the customer adds the product to the cart: the add button becomes a quantity counter, and a big sticky CTA bar appears pinned directly above the footer navigation, showing how many items are in the cart.
3. `card-without-unit-attributes-pricing.jpg` — use this for the card variant where units and attributes are displayed without any prices.

WHAT THE NEW PRODUCT CARD MUST DO
- Restructure the card to match the layout in image 1: product image, product name, attributes shown as compact chips/badges, and the product's units listed with each unit's price next to it.
- Keep the existing color palette exactly as it is. This task is about layout and information structure only.
- Default state (product not in cart): show a single Add button in the position the template shows.
- In-cart state (as in image 2): replace the Add button in the same spot with a counter control — minus button, current quantity, plus button. Plus increases quantity, minus decreases it, and at zero the counter turns back into the Add button. The counter must stay in sync with the actual cart state for that product and unit, including quantities added from elsewhere. The swap between Add and counter must not cause the card to resize or jump.
- Sticky cart CTA (as in image 2): when the cart has at least one item, show a big, prominent CTA bar that is sticky and pinned directly on top of the footer navigation — attached to it, never overlapping or floating. It displays the live number of items in the cart, tapping it takes the customer to the cart, and it disappears when the cart is emptied. It must stay visible while scrolling, must not cover product cards (add matching bottom space to the list), should animate in and out smoothly, and must not appear on the cart/checkout screens.
- Price-less variant (as in image 3): support a display mode where the same card shows units and attributes with NO prices at all, while keeping the identical layout and the same Add/counter behavior. Treat it as a configurable display variant, not a separate hard-coded design.
- Handle real-world content gracefully: long product names, products with many units, products with no attributes, missing images, and the storefront's text direction. Mobile-first, since this is a footer-nav/bottomsheet experience.

FILTER BAR FIX
- In FilterBar.tsx, the button with the filter icon must open the product filter bottomsheet when tapped: a panel sliding up from the bottom over a dimmed backdrop, showing the product filter options with currently applied filters pre-selected, dismissible via backdrop tap or drag-down, with background scroll locked while open. Applying filters updates the product list; clearing resets them. It must work wherever this FilterBar is rendered in the storefront.

CONSTRAINTS
- Do not change the color palette.
- Do not change cart page, checkout, or backend behavior; use the existing cart state and product data.
- Card, counter, and sticky CTA must all read from the same cart state so counts never disagree.

DONE WHEN
- The card matches image 1's layout for units/pricing/attributes; the price-less variant matches image 3; the add-to-cart counter and sticky CTA match image 2; and the filter-icon button reliably opens the product filter bottomsheet.

---

## Open questions to confirm against the reference images

1. Exact zone order on the card (image position relative to name/attributes/units/action).
2. With multiple units, does the customer pick a unit on the card first, or does Add default to the first unit?
3. Does each unit get its own counter, or is there one counter per card?
4. Does the sticky CTA also show the cart total price, or only the item count?
5. Should the filter button show a badge with the number of active filters?
