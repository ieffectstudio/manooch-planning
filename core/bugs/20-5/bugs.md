# PRD — Manooch Storefront & Checkout Fixes (compact)

You are a senior engineer debugging **Manooch**, a multi-store SaaS e-commerce platform ("Powered by Manooch"). Each shop is a storefront (e.g. `tajmahal.manooch.site`); there is a portal (super-admin) panel, a seller admin panel, and a shared API. Please analyze root cause, correct behavior, and fix for each bug below; give a concrete plan (+ illustrative code) to implement and test end-to-end.

**Reference plan doc (read first):** `manooch-planning/core/bugs/20-5/fix-useredurer-structure.md` — also plan for this.

---

## Bug 1 — Deleted/unavailable products stay in the storefront cart (badge vs cart page)
- **Bug:** In the storefront **order cart**, if I delete a product from the **seller admin**, the product still exists in **localStorage**. When a product (or its variants) is **deleted, disabled, or has no stock**, the cart **badge counter still shows it**, but the item does **not load** on the cart page — so the badge and the page disagree.
- **Expected:** When a product/variant is **deleted, disabled, or out of stock**, that item must be **removed from the cart** entirely, so the cart page and the badge counter stay in sync. This should be handled cleanly at load (filter stale cart items against the live product data).
- **Question:** How should the cart reconcile localStorage against the backend so stale/deleted/disabled/out-of-stock items (and their variants) are dropped and the badge updated?

## Bug 2 — "Submit order" CTA button color from store primary color
- **Bug:** The **submit-order button** on the storefront and the **checkout page** does not use the store's **primary color**.
- **Expected:** The submit-order CTA on the storefront and checkout page should be colored from the **store primary color** setting.

## Bug 3 — 404 behavior depends on whether the store exists
There are **two different 404 cases** that must behave differently:
1. **Store exists, but an internal page is not found:** the store's **internal 404 template is fine and correct**. In this case the 404 should offer a link that redirects to the **storefront dashboard** (home) of that store.
2. **Store does not exist (e.g. it was deleted from the portal):** the 404 page should **not** show the storefront's **bottomNav**. It should show the **404 text** and a way back to the Manooch website (`manooch.site`). I confirmed a **deleted shop currently shows a 404 page that still renders the bottomNav** — this is wrong.
- **Expected:** Case (1) uses the normal internal 404 template linking to the storefront dashboard; case (2) shows a plain 404 with no bottomNav and a link back to `manooch.site`.
- **Question:** How to distinguish these two cases and route them correctly — internal-page-not-found (redirect to storefront dashboard) vs store-not-exists (plain 404 + link to `manooch.site`, no bottomNav)?

## Bug 4 — City & State bottom sheet needs a search field
- **Bug:** The **city and state (province) bottom sheet** has no search.
- **Expected:** Add a **search field** to the city & state bottom sheet so users can filter options.

## Bug 5 — Color bottom sheet: hex input + copy icon (store primary color)
- **Bug:** The **personalize store primary color** bottom sheet is missing a hex code input.
- **Expected:** Add a **color code input in hex format** (like the "add new color value" bottom sheet for attributes). The input should also have a **copy icon** so the user can copy the **hex of the selected color**.
- **Question:** How should the primary-color picker expose the selected color's hex in an editable input with a copy-to-clipboard button?

## Bug 6 — Order cart empty-state styling & icon wrong
- **Bug:** The **empty page** style of the order cart page template and its **icon size** are incorrect.
- **Expected:** Match the **team storefront empty template** — fix the empty-state layout and icon size. The empty-state CTA (**"مشاهده محصولات"** / "View products") color should be set from the **store primary color**.

## Bug 7 — Plugin enable/disable toggle doesn't take effect until refresh (admin)
- **Bug:** In the **admin panel**, when I go to the **plugin manage page** and **toggle a plugin** on/off, then click **back** and return to the **dashboard**, the plugin I enabled/disabled **still works as before** — until I **refresh** the page.
- **Expected:** The plugin enable/disable change should take effect **immediately** after returning to the dashboard, without requiring a page refresh. The toggled state must be reflected in the running app (e.g. state updated in the store/cache and re-fetched when returning).
- **Question:** Why does the plugin toggle not propagate until a refresh (stale state/cache that isn't invalidated on navigation), and how should the app reflect the toggle immediately on return to the dashboard?

---

## Deliverables per bug: root cause • correct behavior • recommended fix • edge cases.
**Also:** read and incorporate the plan doc `fix-useredurer-structure.md` and make sure the fixes are consistent with it.
**Edge cases:** cart badge vs cart page sync when product is deleted/disabled/out-of-stock (incl. variants); primary-color-driven CTAs across storefront/checkout/empty-state; 404 when an internal page of an existing store is not found (link to storefront dashboard) vs when the store itself does not exist (plain 404, no bottomNav, link to `manooch.site`); city/state search filtering; hex input + copy for primary color; empty-cart layout/icon matching the team template; plugin toggle taking effect immediately (no refresh) across admin pages.
