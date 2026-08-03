# PRD — انبار و قیمت‌گذاری (Inventory & Pricing)

**Feature:** Stock & Pricing Management for the Manooch Seller Admin Panel
**Scope:** Frontend UI behavior & rules (MVP). No backend/ERP/warehouse logic.
**Status:** Approved spec (blindspot + business rules resolved)
**Platform:** Mobile-first PWA, `max-w-md`, strictly RTL (`dir="rtl"`)

> This document defines **conditions and capabilities only**. It intentionally excludes coding logic, data schemas, and implementation details.

---

## 1. Overview & Goals

Give a seller a single, simple screen to:

1. View all products with their current price and stock status.
2. Search/filter products.
3. Edit a product's pricing and stock using one of three pricing methods.
4. Save changes immediately from the edit screen.

**Guiding principles**
- Mobile-first and PWA-capable (works offline once compiled).
- Strictly RTL; no left/right hacks — rely on RTL layout and logical properties.
- Shadcn-like, clean, spacious visual style.
- Every product may have **exactly one** pricing method at a time.
- No over-engineering — this is an MVP.

---

## 2. Pricing Methods (the core rule)

Every product has **exactly one** of these three pricing methods active at any moment:

| Method | Persian label | Meaning | Inputs |
|--------|--------------|---------|--------|
| **Simple** | ساده | One price + one total stock for the whole product | Base price, discount %, total stock |
| **Unit** | واحد | Product is sold in multiple sellable units (bag, can, box…); each unit has its own price + stock | A list of units, each with price + stock |
| **Attribute** | ویژگی | Price varies by **one** attribute group only (e.g., RAM size *or* color, never both); each value has its own price + stock | One selected attribute group + rows per value, each with price + stock |

### 2.1 Mutual exclusivity (critical rule)
- **Unit and Attribute can never be active at the same time.** They are mutually exclusive.
- A product may be *capable* of both, but only **one** may have pricing configured.
- Switching between **Unit ↔ Attribute** is a **destructive transition** and requires explicit seller confirmation before the switch is applied.
- Switching **Simple ↔ Unit/Attribute** is **non-destructive** (see §4 for what is kept/cleared).

---

## 3. Pricing Method Selection — Conditions

### 3.1 Capability rules (when a method is available)
- **Simple:** always available for every product.
- **Unit:** available only if the product has defined sellable units (e.g., a unit-of-sale list). If the product has no units, the Unit mode is **disabled/grayed** with an explanatory tooltip.
- **Attribute:** available only if the product has at least one attribute group. If no attributes exist, the mode is **disabled/grayed** with an explanatory tooltip.

### 3.2 Selection UX
- Selection is a **3-way segmented control**: «ساده» / «واحد» / «ویژگی».
- Exactly one segment is active (highlighted) at all times.
- Disabled methods (per §3.1) are shown grayed and non-selectable.

### 3.3 Confirmation gate
- Attempting to switch **Unit ↔ Attribute** opens a bottom-sheet confirmation:
  - Message: *"هر محصول فقط یکی از روشهای قیمتگذاری را میتواند داشته باشد. با تغییر، قیمتها و موجودی روش فعلی حذف میشود."*
  - Buttons: «انصراف» (cancel, keep current method) and «بله، تغییر بده» (confirm, switch).
  - On **confirm**: current method's configured rows/prices are cleared and the new method's panel is shown.
  - On **cancel**: nothing changes; current method stays.

---

## 4. The "قیمت پایه" (Base Pricing) Section

The **Base Pricing** block (قیمت اصلی، درصد تخفیف، موجودی کل) is **shown only in Simple mode** and is **always editable** there.

| Active method | Base Pricing section | Behavior |
|---------------|---------------------|----------|
| **Simple** | **Visible & editable** | Seller enters base price, discount %, and total stock manually. |
| **Unit** | **Hidden** | The block is **not shown**. Instead, a **price selector** (§4.2) appears. |
| **Attribute** | **Hidden** | The block is **not shown**. Instead, a **price selector** (§4.2) appears. |

### 4.1 Price selector (unit / attribute mode)
When Unit or Attribute pricing is active, the base price is **not manually input** — the seller **selects it from the active unit/attribute items**:
- A dropdown lists the product's unit/attribute items (e.g., «بسته ۵۰۰ گرمی — ۲۵۰٬۰۰۰ تومان», «قوطی ۱ کیلویی — ۴۵۰٬۰۰۰ تومان»).
- Selecting an item displays its price as a **read-only** value («قیمت این گزینه»).
- The selected price **cannot be typed or edited** directly; it is derived purely from the chosen item.
- The list of options is driven by the **active pricing method** (unit items in Unit mode, attribute values in Attribute mode).

### 4.2 Memory / undo-safe rule
- The **last manually-entered Simple values** (base price, discount %, total stock) are **remembered**.
- When the seller switches back from **Unit/Attribute → Simple**, those remembered values are **restored** automatically. They are never lost by switching.
- Remembered values are only overwritten when the seller manually edits them again in Simple mode.

---

## 5. Field Rules & Validation (per method)

### 5.1 Simple mode
- **قیمت اصلی (Base price)** — *required*. Positive number ≥ 0. Numeric keypad on mobile.
- **درصد تخفیف (Discount %)** — *optional percentage*. A number 0–100 representing a percentage off. **Empty = no discount.**
  - Displayed selling price = Base price × (1 − discount%). If discount is empty/0, the base price is shown.
  - If a discount is set, the UI must show the calculated final price so the seller sees the result.
  - **Boundary rule:** discount must stay within 0–100. Out-of-range is rejected.
- **موجودی کل (Total stock)** — integer ≥ 0. Negative and non-integer rejected.

### 5.2 Unit mode
- Each unit row has **three** fields:
  - **قیمت (Price)** — *required per row* once the row exists. Number ≥ 0.
  - **موجودی (Stock)** — integer ≥ 0.
  - **درصد تخفیف (Discount %)** — optional percentage 0–100. Empty = no discount for that unit.
- **A row with price but empty stock** = valid (price only, no stock).
- **A row with stock but empty price** = invalid; price is required once a row exists.
- Discount can be set independently **per unit** (each unit may have its own discount %).
- A product must have **at least one unit row** to save in Unit mode. Empty list = cannot save.

### 5.3 Attribute mode
- Exactly **one** attribute group is selectable at a time (e.g., «سایز»). Other groups shown disabled.
- Each attribute value row has **three** fields:
  - **قیمت (Price)** — *required per row* once the row exists. Number ≥ 0.
  - **موجودی (Stock)** — integer ≥ 0.
  - **درصد تخفیف (Discount %)** — optional percentage 0–100. Empty = no discount for that value.
- Same validation rules as Unit mode (§5.2) apply to each value row, including **per-value discount**.
- A product must have **at least one attribute value row** to save in Attribute mode.

---

## 6. Stock Status Logic (the list badge)

The product list shows a stock status badge per product. Rules:

| Status | Persian label | Color | Condition |
|--------|--------------|-------|-----------|
| **In stock** | موجود | Green | Effective stock **> low-stock threshold** |
| **Low stock** | رو به اتمام | Amber | Effective stock **> 0 and ≤ low-stock threshold** |
| **Out of stock** | ناموجود | Red | Effective stock **= 0** |

### 6.1 Effective stock per pricing method
- **Simple:** Effective stock = the **موجودی کل (total stock)** field.
- **Unit:** Effective stock = **sum of stock across all unit rows**.
- **Attribute:** Effective stock = **sum of stock across all attribute value rows**.

### 6.2 Low-stock threshold
- The threshold is **per-product** (configurable by the seller per product).
- **Default threshold = 5** for every product (a new product starts at 5 unless changed).
- The seller can adjust this per product; the badge logic uses that product's own threshold.

### 6.3 Badge display
- Badge shows the status word **and** the effective quantity, e.g., «موجود (۱۲)», «رو به اتمام (۳)», «ناموجود (۰)».
- Status uses only the **effective quantity** (per §6.1), regardless of method.

---

## 6A. Bulk Update via Excel Import

Sellers can update pricing & stock for **many products at once** — including all three pricing types — by uploading an Excel file.

### 6A.1 Access
- A dedicated entry point on the **List screen** («ورود قیمت و موجودی با اکسل») opens the Import view.
- The Import view is a distinct screen with its own back button.

### 6A.2 Product identification (key column)
- The unique key for each row is the **کد محصول (Product Code / SKU)**.
- **Why not the numeric database ID?** IDs are meaningless to sellers, fragile to reference, and not printed on the product.
- **Why not the product title?** Titles can be duplicated, are editable, and are long/RTL-prone — they break reliable matching.
- The Product Code is **unique, immutable, stable**, and **visible on the product card** so sellers always know what to write in the column.
- Titles/IDs are **not** used to match rows; only the Product Code is authoritative.

### 6A.3 Excel structure (three sheets)
The sample file contains **three sheets**, one per pricing type. Sellers use the sheet(s) that match their products:

**Sheet «ساده» (Simple)**
| کد محصول | قیمت اصلی | درصد تخفیف | موجودی کل |
|---|---|---|---|

**Sheet «واحد» (Unit)** — one row per unit; a product can appear on multiple rows
| کد محصول | نام واحد | قیمت | موجودی | درصد تخفیف |
|---|---|---|---|---|

**Sheet «ویژگی» (Attribute)** — one row per attribute value; a product can appear on multiple rows
| کد محصول | گروه ویژگی | مقدار ویژگی | قیمت | موجودی | درصد تخفیف |
|---|---|---|---|---|---|

### 6A.4 Download sample
- A **«دانلود فایل نمونه»** button generates a ready `.xlsx` with all three sheets, correct column headers, and example rows.
- Sellers edit this file rather than building columns from scratch.

### 6A.5 Upload
- Accepted formats: **`.xlsx` and `.xls`**.
- File size cap: **2 MB** (MVP; adjustable).
- Only the supported sheets/columns are processed; unknown sheets are reported as errors.

### 6A.6 Validation (per row)
Each data row is validated before any update is applied:
- **کد محصول** required; must match an existing product → otherwise error «محصول یافت نشد».
- **Price** required and ≥ 0.
- **Discount %** optional, 0–100. Out of range rejected.
- **Stock** integer ≥ 0. Negative / non-integer rejected.
- **Unit sheet:** «نام واحد» required.
- **Attribute sheet:** «گروه ویژگی» and «مقدار ویژگی» required.
- A row with any validation error is **rejected entirely** (no partial update of that row).

### 6A.7 Import result & error reporting (critical requirement)
After import, the seller sees a clear result:
- **Success summary:** count of rows successfully updated.
- **Error summary:** count of rows rejected.
- **Per-row error list**, each showing:
  - the Product Code,
  - the source sheet,
  - the row number,
  - the specific reason(s) — e.g., «محصول یافت نشد», «قیمت نامعتبر», «درصد تخفیف باید ۰ تا ۱۰۰ باشد».
- Errors are **returned to the seller in the UI** so they can fix and re-upload; nothing is silently skipped.
- A successful import refreshes the product list so badges/prices reflect the new data.

### 6A.8 Non-goals (MVP)
- No creation of new products via import (updates only).
- No template auto-detection of arbitrary seller files (sellers must use the provided sample structure).
- No background/large-file batch processing — synchronous import of the uploaded file.

---

## 6B. Full Catalog Export (Excel)

Sellers can **download all products** (with all their units and attributes) as an Excel file in a single click.

### 6B.1 Access
- A **«خروجی اکسل»** card on the List screen, placed beside the import card.
- One tap downloads the file — no dedicated screen needed.

### 6B.2 Content (three sheets)
The export mirrors the import structure (§6A.3), so a downloaded export can be **edited and re-imported** directly (round-trip compatible):

**Sheet «ساده»** — products priced in Simple mode
| کد محصول | قیمت اصلی | درصد تخفیف | موجودی کل |
|---|---|---|---|

**Sheet «واحد»** — **all unit rows** for all products (a product may span multiple rows)
| کد محصول | نام واحد | قیمت | موجودی | درصد تخفیف |
|---|---|---|---|---|

**Sheet «ویژگی»** — **all attribute-value rows** for all products
| کد محصول | گروه ویژگی | مقدار ویژگی | قیمت | موجودی | درصد تخفیف |
|---|---|---|---|---|---|

### 6B.3 Behavior
- Exports the **current** prices, stocks, and discount percentages from the seller's catalog at the time of download.
- Includes every product and every unit/attribute row — nothing is omitted.
- The downloaded file's structure exactly matches the import template, enabling easy bulk edits and re-upload.

### 6B.4 Non-goals (MVP)
- No filtered/partial export (e.g., by category) — full catalog only.
- No formatting/theme styling of the workbook beyond headers.

---

## 7. List Screen (انبار و قیمت‌گذاری) — Capabilities

1. **Header:** Title «انبار و قیمتگذاری»; optional notification icon.
2. **Search:** sticky, live-filter by product title (case-insensitive substring). No results → empty state «محصولی یافت نشد».
3. **Bulk import & export entry:** two cards beside each other — «ورود با اکسل» opens the Excel Import view (§6A), and «خروجی اکسل» downloads the full catalog (§6B).
4. **Product card** shows:
   - Thumbnail placeholder (or product image).
   - Product title (long names truncated).
   - SKU (secondary).
   - Current price in «تومان» with formatted thousand-separators.
   - Stock status badge (§6).
   - **ویرایش (Edit)** icon button → opens edit screen for that product.
5. **Loading state:** skeleton placeholders while list loads.
6. **Empty state:** shown when there are no products at all (distinct from search-no-results).
7. **Bottom navigation:** fixed 4-item Sarnakh bar (خانه / محصولات / انبار / حساب). «انبار» is the active item.

### 7.1 Current price shown on the card
- **Simple:** the final selling price (after discount %), or base price if no discount.
- **Unit / Attribute:** show the **lowest** effective selling price across rows (each row's price after its own discount %) as the "from" price, e.g., «از ۲۵۰٬۰۰۰ تومان», because multiple prices exist. (This is the natural mobile e-commerce convention.)

---

## 8. Edit Screen (بروزرسانی قیمت و موجودی) — Capabilities

1. **Header:** back button (arrow points right for RTL) + title «بروزرسانی قیمت و موجودی».
2. **Context card:** shows the selected product's name, thumbnail, and current status so the seller confirms what they're editing.
3. **Pricing method selector** (§3).
4. **Base Pricing section** (§4).
5. **Method-specific panel** (§5) shown for the active method; the other panels are hidden.
6. **Save CTA:** large primary button «ثبت تغییرات», fixed at the bottom directly above the bottom nav (no gap).

### 8.1 Save behavior
- Tapping save validates all inputs per §5.
  - If valid → show success toast «تغییرات با موفقیت ذخیره شد», then **return to the list** (reflecting the updated price/status).
  - If invalid → show inline errors on the offending fields; nothing is saved; the screen stays.
- **Unsaved-change guard:** if the seller navigates back with unsaved edits, a confirmation prompt asks whether to discard changes.

### 8.2 Save availability
- The Save button is **disabled** until the minimum required data is present:
  - Simple: base price present.
  - Unit: ≥1 unit row with a price.
  - Attribute: ≥1 attribute value row with a price.

---

## 9. Global UX & RTL / Mobile Rules

- **Direction:** entire document `dir="rtl"`. All directional layout uses logical properties (`ps-`, `pe-`, `ms-`, `me-`). **No** `flex-row-reverse` hacks.
- **Numeric keyboards:** all numeric fields open the mobile number pad (`inputmode="numeric"`).
- **Currency:** prices use «تومان» suffix; formatted with thousand-separators; Persian digits preferred in display, accepted in input.
- **Safe area:** bottom nav and CTA respect the device home-indicator inset (`env(safe-area-inset-bottom)`).
- **Long text:** product titles truncate gracefully; no broken RTL wrapping.
- **Sticky elements:** search bar and header are sticky with opaque backgrounds; CTA + nav are fixed at bottom with correct scroll padding so no content is hidden behind them.

---

## 10. Validation Summary (final conditions)

| Field | Required? | Range/rule |
|-------|-----------|-----------|
| Base price (Simple) | Yes | ≥ 0 |
| Discount % (Simple) | No | 0–100; empty = no discount |
| Total stock (Simple) | Yes | integer ≥ 0 |
| Unit row price | Yes (per row) | ≥ 0 |
| Unit row stock | No | integer ≥ 0 |
| Unit row discount % | No (per row) | 0–100; empty = no discount |
| Attribute value price | Yes (per row) | ≥ 0 |
| Attribute value stock | No | integer ≥ 0 |
| Attribute value discount % | No (per row) | 0–100; empty = no discount |
| At least 1 unit row (Unit mode) | Yes | — |
| At least 1 attribute value row (Attribute mode) | Yes | — |
| Discount ≤ 100 (effective selling price ≥ 0) | Derived | selling price = price × (1 − d%) |

---

## 11. Open Items / Non-Goals (for MVP)

- **Non-goals:** full warehouse management, multi-warehouse stock, purchase orders, stock history/audit log, barcode scanning, ERP integration.
- **Permissions/roles** (who may edit prices) are **out of scope** for this MVP and assumed to be "any logged-in seller."
- **Error/retry state** for list load failures is noted but not fully specced (recommend a lightweight retry prompt).
- Discount as **percentage** is a confirmed decision; amount-based discounts are not supported in this version.
- Product *capability* (which products can use Unit/Attribute) is driven by the product's configured units/attributes — the mechanism for how those are configured is a separate feature (Product Catalog), referenced but not built here.
- **Excel import (§6A)** is updates-only (no product creation). Background batch processing, larger files, and auto-detection of arbitrary seller templates are deferred.
- **Conflict rule (open):** if an imported row sets a pricing method (e.g., writes a «واحد» row) for a product that currently uses a different method (e.g., Attribute), the PRD must state whether the import **overrides** the existing method or **rejects** the row. Recommended default: **reject with a clear error** to avoid accidental destructive switches (consistent with the manual confirm gate in §3.3).
