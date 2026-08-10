# PRD — Manooch Product Discounts (compact)

You are a senior engineer debugging **Manooch**, a multi-store SaaS e-commerce platform ("Powered by Manooch"). Context: I already fixed **discount display for simple product cards** (products with no units/attributes and no attribute price binding). Now I need to fix discount handling for products with **complex pricing** (unit or attribute based).

**Terminology:**
- **Simple product card** — no units, no attributes, single price. ✅ Discount already fixed here.
- **Complex pricing** — product priced via **units** (each unit has its own stock + price) or **attributes** (each attribute variant has its own stock + price).

Please analyze root cause, correct behavior, and fix for each bug below; give a concrete plan (+ illustrative code) to implement and test end-to-end. Reference images:
- `manooch-planings/core/bugs/20-5/product-card/attribute-pricing-form.png`
- `manooch-planings/core/bugs/20-5/product-card/unit-pricing-from.png`
- `manooch-planings/core/bugs/20-5/product-card/card-variants-discount.png`

---

## Bug 1 — No per-variant discount in the attribute/unit pricing form
- In the **add-product** feature, the attribute/unit pricing forms let me set **stock and price per variant**, but there is **no field to add a discount per each variant**.
- **Bug:** Each unit/attribute variant can have its own stock and price, but **not its own discount**.
- **Expected:** Add a **discount field per variant** in both the unit pricing form and the attribute pricing form. It should:
  - Accept **discount %** format.
  - Be **optional**, defaulting to **0 / null** (i.e. no discount on that unit/attribute by default).
  - Give **each variant its own discount price** (each variant's discount is independent).

## Bug 2 — Discount view broken on product cards with unit/attribute pricing (storefront)
- I already fixed discount display on **simple product cards** (no pricing on attributes/units).
- Now I need to fix discount display for product cards that **have unit or attribute pricing** (`card-variants-discount.png`).
- **Bug:** On the storefront, complex-pricing product cards don't show their (per-variant) discounts correctly.
- **Expected:** A complex-pricing product card should display the correct discount per variant, matching whatever the seller set in the pricing forms.

## Bug 3 — Discount section must be hidden on complex-pricing cards
- When a product has **complex pricing** (unit or attribute), the **discount section on the product card should be totally invisible**.
- **Bug/requirement:** This seems to be a deliberate UX rule — if a product uses unit/attribute pricing, hide the generic discount section on the card entirely.
- **Expected:** Detect "complex pricing" and render no discount section at all on those product cards.

## Bug 4 — Visitor plugin card discount UI broken for all card types
- The **visitor plugin** card UI discount is broken and needs fixing.
- **Bug:** Discount display in the visitor plugin card is incorrect.
- **Expected:** Fix the visitor plugin card discount UI for **all** card types — both **simple** and **complex pricing** cards.

## Bug 5 — PDP page returns 404 only in local dev mode
- **Bug:** When I run the **backend and frontend locally** (dev mode), the **PDP (Product Detail Page) redirects to a 404**. On **production it works fine**.
- **Expected:** The PDP page must load correctly in local dev mode, exactly as it does in production.
- **Please investigate:** What could cause the PDP route to 404 only locally (e.g. missing dev environment config/seed data, missing/incorrect local product records, route or URL/permalink handling that differs between dev and prod, proxy/server routing, or host/port differences between local backend & frontend). Give the likely cause and the fix so the page works in dev.

---

## Deliverables per bug: root cause • correct behavior • recommended fix • edge cases.
**Shared thread:** discount model/schema for variants (units/attributes) is missing end-to-end (missing in seller pricing forms → missing/broken on storefront card → hidden for complex pricing), plus a parallel fix needed in the visitor plugin card for all card types. Plus a separate dev-only issue: PDP route 404s locally but works in prod.
**Edge cases:** per-variant discount defaulting to 0/null; mixed variants (some discounted, some not); a variant discount vs base price; hiding discount section on complex-pricing cards vs showing per-variant discount; visitor plugin behavior for simple vs complex cards; PDP 404 only in local dev vs prod.
