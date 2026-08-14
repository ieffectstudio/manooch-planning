# Stock & Pricing Fixes — Full Issue Description (22 May)

> This document rewrites and clarifies all stock feature fixes. No coding logic, no implementation details — only product behavior, UX expectations and business rules.
> Reference screenshots: `stock-list.png` (list screen), `card-item.png` (current card), `stock-card.html` (desired card), `stock-item.png` (full item screen), `pricing-tabs.png` (tabs to be removed), `dropdown.png` (dropdown to be removed).

---

## 1. Context

The Stock (انبار و قیمت‌گذاری) feature has 2 main screens:

1.  **List screen (`stock-list.png`)**: search + bulk excel actions + product cards.
2.  **Item edit screen (`stock-item.png`)**: editing price, discount, stock, min-order per variant.

Current implementation mixes catalog responsibilities (changing pricing method, adding variants) into stock, has wrong data model for SKU, incomplete excel formats, and incorrect card UX.

The intent of Stock is **only inventory & pricing maintenance**, not catalog management.

---

## 2. Core Conceptual Fix — Product vs Variant

**Current behavior:**
- SKU / کد محصول is shown per product (e.g. `605553`). Attribute / unit variants share the same SKU.
- Excel export & import treats rows as products.
- Seller sees product = one entity, even if it has many price variants.

**Expected behavior / Business Rule:**
- In any real stock system, **each sellable variant is a distinct inventory item**.
  - Example: iPhone Blue 128GB vs iPhone Red 128GB vs Orange 128GB — each has different price/stock and **must have its own unique SKU**.
  - For attribute pricing: each attribute value (e.g. بزرگ, کوچک) = one variant = one unique variant-SKU.
  - For unit pricing: each unit (e.g. 500 گرم, 1 کیلو) = one variant = one unique variant-SKU.
  - For simple / inquiry pricing: product has only one variant => one row = product SKU = variant SKU.

- **SKU rule:** SKU must be generated and displayed **per variant**, not per product instance. Product list aggregation can still show product name, but stock counting, searching, and excel must work on variant level.

- **List aggregation:** If a product has multiple variants, the card in `stock-list.png` currently shows «از ۱۹۰,۰۰۰ تومان» (from price) and total stock count e.g. «موجود (۲۰,۰۰۰)». That aggregation logic stays, but underlying identity is variant-SKU.

---

## 3. List Screen Fixes (`stock-list.png` & `card-item.png`)

### 3.1 Card Design — Must Change Completely

**Current (`card-item.png`):**
- Small thumbnail left, edit icon only (pen), price + badge cramped, code: 605553 shown with small grey icon.
- Not visually consistent with customer-facing product list.

**Expected (must match `stock-card.html` reference):**
- Layout must be identical to the product list card used elsewhere in the app.
- Differences allowed:
  - Instead of «افزودن به سبد», bottom full-width button must be «ویرایش» — black background, white text, labeled explicitly with the word ویرایش (not icon-only).
  - Each variant inside a product? In list preview we keep product-level card. But if product has multiple variants, show them stacked inside the card as in `stock-card.html`:
    - Each variant row shows: discount pill (e.g. %۲۰ pink), size/unit label, stock count (e.g. ۲۴ عدد), price, status badge (موجود / ناموجود).
    - Stock count badge «X عدد» should be hidden when stock >= 10 to reduce noise (as in `stock-card.html` logic: 24 is hidden, 4 is shown).
    - Status badge: موجود (green bg) / ناموجود (red bg) per variant effective stock.
- Product header: title right-aligned bold, description faded, thumbnail 132px on left (in RTL, left side visually, but logical end).
- Separation: variants separated by thin divider line.
- Code/SKU: Should show **variant SKU** if variant list, or product SKU if simple. In aggregated list card, show primary SKU + indicate variant count.

**Acceptance:** Seller can instantly recognize product identity, variant prices, and low-stock variants without opening detail.

### 3.2 Import/Export Entry Cards

**Current:** Two small cards «ورود با اکسل» and «خروجی اکسل» with no clear preview.

**Expected:**
- Export format is not complete / not clear. Needs redesign (see §5).
- Both actions must clearly state they work on **variant list**, not product list.

---

## 4. Item Detail Screen Fixes (`stock-item.png` / `pricing-tabs.png` / `dropdown.png`)

### 4.1 Remove Pricing Method Tabs Entirely

File: `pricing-tabs.png` shows segmented control: ساده / واحد / ویژگی

**Problem:** In Stock feature, seller should **not be allowed to change pricing method**. Pricing method is defined during product creation (catalog). Stock screen must be read-only regarding method type.

**Expected:**
- Completely remove the tabs component.
- Instead, show a non-interactive label indicating current active pricing mode: e.g. «نوع قیمت‌گذاری: ویژگی — گروه: اندازه» or «واحد — ۲ واحد تعریف شده».
- No ability to switch from simple to unit or unit to attribute inside Stock. If product has no units defined, don't show message «این محصول واحد فروش تعریف شده‌ای ندارد» as an error with tabs — just show empty state for that mode is not applicable because mode is locked.

This prevents accidental destructive data loss (deleting prices when switching modes).

### 4.2 Remove Price Option Dropdown Entirely

File: `dropdown.png` — «انتخاب گزینه قیمت» dropdown with «بزرگ» and «قیمت این گزینه: ۹۰,۰۰۰ تومان»

**Problem:** This selector forces seller to pick a base price from variants. It's redundant and confusing. Stock should edit all variants directly, not pick one as representative.

**Expected:**
- Remove this entire dropdown section permanently.
- Base price concept only exists for simple pricing. For unit/attribute, there is no base price — only variant prices.

### 4.3 Infinite Stock Switch — Missing

**Current:** No infinite stock control in item screen.

**Expected:**
- Add «موجودی نامحدود» switch/toggle at top of item edit screen (above variant list), visible for all pricing modes.
- **Behavior:**
  - Off (default): normal stock inputs editable per variant.
  - On: All variant stock fields become disabled / show ∞ icon, and effective stock for badge calculation becomes infinite (always «موجود» regardless of number).
  - When toggled on, existing stock numbers are remembered but ignored in status calculation.
  - When toggled off again, remembered values return.
  - Export: If infinite is on, excel should export stock as «نامحدود» or empty with flag, not 0.

### 4.4 Variant Management Restriction

**Current:** Seller might be able to add/change/delete variant definitions in stock.

**Expected (like catalog rule):**
- Seller **cannot** add new attribute value, unit, color, etc. in Stock screen.
- Seller **cannot** delete or rename variants in Stock screen.
- Stock screen only allows editing of these fields **per existing variant**:
  - قیمت (Price)
  - موجودی (Stock) — unless infinite enabled
  - درصد تخفیف (Discount %)
  - حداقل سفارش (Minimum Order) — newly required field, see Excel section
- Variant structure (how many variants, their names, attribute groups) is read-only and comes from catalog.

If seller needs new variant, they must go to product catalog.

### 4.5 Minimum Order Field

**New required field:** Currently not present. Needs to exist per variant (and per simple product).

- Seller must be able to set minimum order quantity per variant (e.g. min 2 bags).
- Show next to stock, editable numeric input >=1, default 1.

---

## 5. Excel Export — Complete Redesign

**Current problem (`stock-list.png` export flow):**
- Export claims to be product list but should be variant list.
- Format incomplete, columns unclear, not usable for bulk update.
- No distinction between attribute vs unit vs simple.

**Expected: Export is Variant List Export**

One Excel file with all variants. Each row = one sellable variant.

If product pricing mode is ساده or استعلامی (inquiry), it has exactly **one row** in export.

If unit or attribute mode, product appears in **multiple rows**, one per variant.

#### Required Columns — Unified variant export (replaces old 3-sheet model)

Header row (exactly these names, in this order):

1.  **variant sku** — Unique SKU per variant (mandatory, unique). Example: `605553-BIG`, `605553-SMALL` or `IPHONE-BLUE-128`. This is the key for import matching.
2.  **product name** — Read-only reference, e.g. «تست». For human readability.
3.  **attribute name | unit name** — One column that holds either attribute group name (e.g. اندازه) OR unit group label (e.g. واحد) OR empty for simple. Label: «نام ویژگی / نام واحد»
4.  **attribute value | unit value** — Value of variant, e.g. بزرگ / ۵۰۰ گرم / Empty for simple. Label: «مقدار ویژگی / مقدار واحد»
5.  **min order** — حداقل سفارش (integer >=1)
6.  **stock** — موجودی (integer, or word نامحدود if infinite switch on)
7.  **discount %** — درصد تخفیف 0-100, empty = no discount
8.  **price** — قیمت نهایی پایه به تومان (without discount; final price calculated via discount %)

Optional clarity columns (read-only, help seller):
- product code (original product group code) for grouping
- pricing mode (ساده / واحد / ویژگی / استعلامی)

**Formatting:**
- Persian headers, but ASCII sku values.
- Each variant price is independent.
- Final price shown as price + discount, but export only stores raw price + discount %.
- No merged cells.

---

## 6. Excel Import — Complete Redesign

**Current problem:** Import expects product list, cannot add/change each product variant individually, template doesn't match new variant logic.

**Expected: Bulk Renewal via Variant List Import**

Seller downloads variant export file (as defined in §5), edits values in Excel (price, stock, discount %, min order) and re-uploads **single file** to update everything.

**Behaviors:**

1.  **Matching Key:** Use **variant sku** as unique identifier for each row. NOT product code, NOT product name. Product name column is ignored on import (only for human).
2.  **Allowed Changes via import:**
    - قیمت (price) per variant
    - موجودی (stock) per variant
    - درصد تخفیف per variant
    - حداقل سفارش per variant
    - infinite flag (if stock = «نامحدود» or special keyword)
3.  **Not Allowed via import:**
    - Renaming variants, adding new variants, deleting variants, changing pricing method — those must be rejected with error «ویرایش ساختار واریانت از طریق انبار ممکن نیست».
4.  **Single file flow:** One file updates all variants regardless of pricing mode (simple + unit + attribute together). No need for 3 separate sheets.

**Validation & Error Reporting (must be clear):**
- Unknown variant sku => error: «کد واریانت یافت نشد: {sku} - ردیف {n}»
- Negative price / invalid discount (not 0-100) / non-integer stock => error per row.
- If stock column = «نامحدود», set infinite flag for that product/variant.
- After upload, show summary:
  - تعداد واریانت‌های بروز شده موفق: X
  - تعداد ردیف‌های ناموفق: Y
  - Per-row error list: variant sku, product name, row number, reason.

This enables seller to renew all pricing & stock with one excel.

---

## 7. Additional UX / Business Rules

- **Simple / Inquiry mode:** One row only. Inventory badge for list = that single stock.
- **Effective stock for list badge:** sum of variant stocks (unless infinite => always موجود). If any variant infinite, product badge = موجود (∞).
- **Low-stock threshold:** Same as before, per product aggregation.
- **Search:** Search by product name OR variant sku.
- **Edit button:** List card CTA must say «ویرایش» (text), not just icon.
- **RTL & Mobile:** No change.

---

## 8. Acceptance Checklist (What to verify)

- [ ] Stock list cards match layout of `stock-card.html` reference: title, description, thumbnail, variant rows with discount, stock count logic (<10 show), price and status badge, and full-width black «ویرایش» button.
- [ ] Pricing method tabs (`pricing-tabs.png`) completely gone from item screen. Only read-only label showing active mode.
- [ ] Price option dropdown (`dropdown.png`) completely gone.
- [ ] Infinite stock switch exists at top of item screen. When ON, all variant stock inputs disabled and badge = موجود (infinite). Export shows نامحدود.
- [ ] Seller cannot add/delete/rename variants in stock edit; fields are price, stock, discount %, min order only.
- [ ] Variant SKU uniqueness: each variant has its own sku, displayed everywhere (card, detail, excel). No shared product sku for different variants.
- [ ] Export file is variant list, not product list. Simple/Inquiry = 1 row, Unit/Attribute = N rows. Columns exactly: variant sku, product name, attribute name | unit name, attribute value | unit value, min order, stock, discount %, price (+ optional helpers).
- [ ] Export data clear and complete, includes min order, stock, discount, price per variant with thousand separators in display but raw numbers in file.
- [ ] Import uses variant sku as key, updates only price/discount/stock/min order. Can bulk renew all variants with single file. Clear error reporting per row.
- [ ] No catalog structure editing via stock (no new attributes/units).

---

## 9. What This Ticket Is NOT

- No change to how variants are created in catalog.
- No backend schema discussion.
- No implementation of Excel parsing libraries.
- No change to product creation flow — only stock maintenance.

This spec is ready to be used as AI coding prompt for the Stock plugin.
