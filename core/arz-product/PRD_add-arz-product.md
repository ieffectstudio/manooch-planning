# PRD — "افزودن کالای ارزی" Plugin (add-arz-product)

**Product:** منوچ (Manooch) — Seller Panel → Add Product flow
**Plugin key:** `add-arz-product` · **label:** افزودن کالای ارزی · **type:** `core_sales`
**Document type:** PRD
**Version:** 1.0
**Date:** 2026-08-16
**Status:** Draft — **implementation NOT in current scope** (design/PRD only for now)
**Reference prototype:** `uploads/add-arz-product.html`

> This plugin lets a seller create **gold** and **currency** products with a **live price**,
> **automatic price calculation**, **AI-assisted description**, and **background removal** on
> images. This PRD describes the *what*; it is intentionally deferred from implementation until
> product decides to build it (see §2).

---

## 1. Summary

The standard "add product" flow only handles regular goods. This plugin adds a second product
creation experience with two tabs:

- **طلا (Gold)** — gold products priced from a **live per-gram gold price** plus **اجرت (labor) %**
  and **سود (profit) %**, auto-calculated.
- **ارز (Currency)** — currency products priced from a **live daily exchange rate** plus a
  **fee %** and an **foreign-cost (هزینه ارزی)** amount, auto-calculated.

Both tabs share the same building blocks as regular products (status, name, description, category,
attributes, inventory, image) but replace the static price field with a **live, auto-calculated**
price section.

---

## 2. Scope status

- **Not in scope for implementation now.** This PRD exists so the product decision is documented and
  so the plugin already occupies its row in the **plugin registry** and the **plan matrix**
  (see `plan-plugins-management.html`).
- The prototype (`add-arz-product.html`) is a **functional design reference**, not a spec of record
  for backend contracts. Field names, rate sources, and pricing formulas must be finalized during
  implementation planning.

---

## 3. Goals

1. Let sellers create **gold products** priced from the live gold rate.
2. Let sellers create **currency products** priced from the live exchange rate.
3. Auto-calculate the final product price from the live rate + markup inputs (no manual price).
4. Reuse existing product capabilities (category, attributes, inventory, image, AI description,
   background removal) inside this flow.
5. Behave like every other plugin: plan-bound, toggleable, and hidden when disabled.

## 4. Non-Goals

- Trading/order execution of gold or currency (this is a **catalog/product** feature only).
- Wallet/balance, exchange settlement, or KYC.
- A storefront price-ticker widget (a separate potential plugin; out of scope here).

---

## 5. User flow

1. Seller opens "Add product" and selects **افزودن کالای ارزی** (a distinct entry, gated by this
   plugin).
2. Seller chooses a tab: **طلا** or **ارز**.
3. Seller fills the basic fields; price is computed live as they type.
4. Seller optionally uses AI to complete the description, uploads an image (with background
   removal), and sets inventory.
5. Seller saves → product is created with the computed price.

---

## 6. Detailed requirements

### 6.1 Common to both tabs

| Area | Requirement |
|------|-------------|
| **Product status** | A switch "کالا در فروشگاه نمایش داده نمی‌شود". When on, a red notice shows the product is temporarily inactive (draft/hidden). |
| **Name** | Text input, e.g. "سکه امامی / نیم‌سکه / طلای آب‌شده" or "دلار آمریکا / یورو". |
| **Description + AI** | Description textarea with a "تکمیل با AI" button that generates/autocompletes the description. Button shows a loading state ("در حال نوشتن…") then success. |
| **Category** | Dropdown populated by the **`categories` plugin**. If `categories` is disabled, this section is hidden (section-wrapper rule). |
| **Features/Attributes** | A "فعال‌سازی ویژگی‌های کالا" switch that reveals a list of attribute groups, each showing its name and item count ("۴ آیتم") with an edit action. Populated by the **`attributes` plugin**; hidden when that plugin is disabled. |
| **Inventory** | A "موجودی نامحدود" switch. When on, a green "بدون محدودیت موجودی" note replaces the numeric input; when off, a numeric inventory input shows (grams for gold, count for currency). |
| **Image** | Upload area (PNG/JPG, max 2 MB). After upload, a **background-remover wand button** appears on the image (see §7). |
| **Save** | Primary button ("افزودن محصول طلا" / "افزودن محصول ارز") with success feedback. |

### 6.2 Gold tab (طلا)

1. **Live gold price** — a "قیمت لحظه‌ای طلا" field (تومان بر گرم) with a pulsing "live" indicator.
   Value is pre-filled and updateable; it feeds the calculation.
2. **Weight (وزن گرم)** — numeric input.
3. **اجرت (labor) %** and **سود (profit) %** — two numeric percentage inputs.
4. **Auto-calculated price** section, computing:
   - `قیمت خام = وزن × قیمت لحظه‌ای`
   - `اجرت = قیمت خام × اجرت%`
   - `سود = قیمت خام × سود%`
   - `قیمت نهایی = خام + اجرت + سود`
   - All three components and the total are shown live; the hint explains that changing weight /
     live price / labor / profit moves the total.

### 6.3 Currency tab (ارز)

1. **Source currency** — dropdown: USD, EUR, AED, GBP.
2. **Live rate** — read-only rate (تومان) auto-set from the selected currency ("نرخ به‌صورت خودکار").
3. **Name / description + AI** — same as §6.1.
4. **کارمزد (fee) %** — numeric percentage.
5. **Cost & inventory** — a "هزینه ارزی" amount in the selected currency, plus the inventory controls
   (unlimited switch / count).
6. **Auto-calculated price** section, computing:
   - `مبلغ پایه = هزینه ارزی × نرخ روز`
   - `کارمزد = مبلغ پایه × کارمزد%`
   - `قیمت نهایی = پایه + کارمزد`

### 6.4 Number handling

- Inputs accept Persian digits (۰–۹) and Persian thousands separator (٬) and normalize them
  internally for calculation.
- All computed values render in Persian locale format.

---

## 7. Cross-cutting capabilities reused inside this plugin

These are separate plugins in the registry; the add-arz-product form **consumes** them and must
respect their state (hidden when disabled — section-wrapper rule):

| Capability | Plugin key | Usage in this form |
|-----------|-----------|--------------------|
| Category | `categories` | The دسته‌بندی dropdown. |
| Attributes | `attributes` | The ویژگی‌ها section (attribute groups + item counts). |
| Units | `units` | The unit semantics (گرم for gold, count for currency). |
| Background remover | `background-remover` | The wand button on uploaded images. |
| Voice in product | `voice-in-product` | *(future)* narration on these products' storefront pages. |
| AI description | *(AI service, not a plugin)* | "تکمیل با AI" button. |

> This means `add-arz-product` has **hard dependencies** on `categories` and `attributes`: if either
> is disabled for the seller/plan, those sections must disappear from this form too.

---

## 8. External data (live rates)

- The gold tab needs a **live gold price per gram** feed (تومان).
- The currency tab needs a **daily exchange rate** feed (تومان per USD/EUR/AED/GBP).
- Requirements:
  - Rates are fetched/refreshed automatically.
  - The source of truth (internal service or third-party) is **TBD** — see open questions.
  - A fallback behavior when the feed is unavailable must be defined (e.g. last-known rate + stale
    indicator, or block saving until a fresh rate is available).

---

## 9. Data model (conceptual)

### 9.1 Product record extensions

A gold/currency product carries the normal product fields plus a **variant-specific payload**:

- `productType`: `gold` | `currency`.
- Gold: `weightGrams`, `laborPercent`, `profitPercent`, `liveGoldPriceAtSave`, `rawPrice`,
  `laborAmount`, `profitAmount`, `finalPrice`.
- Currency: `sourceCurrency` (USD/EUR/AED/GBP), `foreignCost`, `feePercent`, `rateAtSave`,
  `baseAmount`, `feeAmount`, `finalPrice`.

### 9.2 Behavior notes

- The **final price is stored at save time** (snapshot). The live price at save time is recorded so
  the product price is reproducible/auditable even if the live rate later changes.
- Recalculating price after save is **out of scope** for v1 (see open questions).

---

## 10. Acceptance criteria

- [ ] Both tabs render and switch correctly.
- [ ] Gold price auto-calculates from weight × live price + labor% + profit% and updates live.
- [ ] Currency price auto-calculates from foreign cost × rate + fee% and updates live.
- [ ] Selecting a currency auto-populates the rate and the unit labels.
- [ ] AI completes the description with a loading → success state.
- [ ] Image upload works; background-remover wand appears and marks the image as background-removed.
- [ ] Status, features, and unlimited-inventory switches show/hide their targets correctly.
- [ ] Category and attributes sections disappear when their plugins are disabled.
- [ ] Persian digit/number normalization works in all numeric inputs.
- [ ] Save produces a product with the snapshot final price.

---

## 11. Open questions

1. **Rate source** — internal rates service or third-party (and which)? Refresh frequency?
2. **Stale-rate behavior** — what happens when the live feed is down at save time?
3. **Repricing** — should the stored price auto-refresh later, or stay a snapshot until the seller
   edits?
4. **Currency inventory unit** — is currency inventory a unit count or a monetary amount?
5. **Gold inventory** — is it weight-based (grams) as in the prototype? Confirm.
6. **Storefront** — how are live-priced products displayed (does the price re-render live on the
   PDP)? This may justify a companion "price ticker" widget later.
7. **Plan gating** — is this a premium/enterprise-only plugin, and at what base price?
