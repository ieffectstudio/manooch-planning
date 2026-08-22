# Stock & Pricing Fixes — Full Issue Description (22 May) — v2 Updated with Filters & New SKU

> This document rewrites and clarifies all stock feature fixes. No coding logic, no implementation details — only product behavior, UX expectations and business rules.
> Reference screenshots: `stock-list.png` (list screen), `card-item.png` (current card), `stock-card.html` (desired card - latest version: icon-only edit next to title, no description, no bottom button), `stock-item.png` (full item screen), `pricing-tabs.png` (tabs to be removed), `dropdown.png` (dropdown to be removed).

---

## 1. Context

The Stock (انبار و قیمت‌گذاری) feature has 2 main screens:

1.  **List screen (`stock-list.png`)**: search + bulk excel actions + filter + product cards.
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

### 2.1 NEW — SKU Structure Update (Critical)

**Current SKU structure:** Simple numeric like `605553` or `COF-AR-500` shared across variants.

**Expected SKU structure — Composite & Globally Unique:**

Format:
```
{SELLER_SHORT} - {PRODUCT_INSTANCE_SKU} - {VARIANT_SKU}
```

Three parts separated by hyphen `-`:

1.  **Short form of seller username / shop name (4 chars)** — e.g. seller username `manooch_coffee` → `MANO`, seller `reza_shop` → `REZA`. 
    - Always 4 characters, uppercased Latin letters, no spaces.
    - Derived automatically from seller account name (first 4 meaningful letters, stripped of symbols). If less than 4, pad or use available.
    - Purpose: Makes SKU globally unique across all sellers on marketplace and instantly identifies seller in warehouse / picking.

2.  **Product instance SKU** — The base SKU assigned when product is created in catalog (e.g. `605553` or `COF-AR-500`). Represents product family, not variant.

3.  **Variant SKU** — Short code for the specific variant (e.g. `BIG`, `SML`, `500G`, `BLUE`, `BASE` for simple).

**Examples:**
- Simple product: `MANO-605553-BASE` or `MANO-605553-STD` (one row only)
- Unit: `MANO-605553-500G`, `MANO-605553-1KG`
- Attribute colors: `REZA-IPH15-BLUE128`, `REZA-IPH15-RED128`, `REZA-IPH15-ORNG128`
- Size: `MANO-FRIED-1KG`, `MANO-FRIED-500G`

**Behavior rules:**
- Full composite SKU is the **primary key** for stock, search, and Excel import/export. Product instance SKU alone is only for grouping.
- When seller creates new variant in catalog, variant SKU part is auto-suggested but editable; full SKU is auto-assembled.
- Old SKUs must be migrated to new format or displayed with new format alongside legacy for transition.
- In UI cards, show short version? Full SKU in detail tooltip, but list card shows at least variant part and full on tap/copy.
- Search in list must match any part: seller short, product SKU, or variant SKU.
- Excel export column `variant sku` now contains this **full composite SKU**, not just variant code.

---

## 3. List Screen Fixes (`stock-list.png` & `card-item.png` & `stock-card.html`)

### 3.1 Card Design — Must Change Completely (Updated per latest request)

**Current (`card-item.png`):**
- Small thumbnail left, edit icon only (pen), price + badge cramped, code: 605553 shown with small grey icon.
- Not visually consistent with customer-facing product list.

**Expected (must match updated `stock-card.html` reference):**
- Layout must be identical to product list card used elsewhere.
- **Latest changes requested:**
  - **Remove description** under title (e.g. "تکه های مختلف مرغ..." removed).
  - **Remove bottom full-width edit button** (`ویرایش` black button at bottom) completely.
  - **Add edit button as icon-only next to title:** In header, title `مرغ سوخاری نرمال` on right, and a small square/rounded icon button (pencil edit icon) immediately next to title on its left side. No text, only icon.
  - Button style: 36x36px, light gray background `#f8f8f8`, border `1px #ececec`, rounded 9px, icon 18px gray.
- Each variant inside a product stacked:
  - Each variant row shows: discount pill (e.g. %۲۰ pink), size/unit label, stock count (e.g. ۲۴ عدد), price, status badge (موجود / ناموجود).
  - Stock count «X عدد» hidden when stock >= 10 (24 hidden, 4 shown).
  - Status badge: موجود (green) / ناموجود (red) per variant effective stock.
- Thumbnail 132px remains, but header now only title + edit icon, no description.
- Separation: variants separated by thin divider line.
- SKU: Display **full composite SKU** (`MANO-605553-BIG`) or at least variant part, visible for copying. In aggregated card, show full SKUs per variant row or reveal on long-press.

**Acceptance:** Card looks clean, title + edit icon at top, no description clutter, no bottom button occupying space.

### 3.2 Import/Export Entry Cards

**Current:** Two small cards «ورود با اکسل» and «خروجی اکسل» with no clear preview.

**Expected:**
- Export format not complete / not clear. Needs redesign (see §5).
- Both actions must clearly state they work on **variant list**, not product list.

### 3.3 NEW — Filter BottomSheet for stock-list

**Current:** No filtering in list; only search by title.

**Expected — Add Filter button + BottomSheet:**

**Placement:**
- Add a «فیلتر» button next to search bar in sticky header (left side of search input, or as icon filter with badge). In RTL, search input on right, filter button on left with icon `adjustments` or `funnel`.
- When active filters applied, show badge count (e.g. `فیلتر • ۲`) with colored dot.

**BottomSheet UI:**
- Tapping filter opens a bottom sheet (half-screen modal, drag handle on top, rounded top corners, overlay dim behind).
- Sheet content scrollable, respects safe-area.
- Sections inside:

  1.  **وضعیت موجودی (Stock Status)** — multi-select chips: `موجود`, `رو به اتمام`, `ناموجود`, `نامحدود (∞)`. Seller can select multiple.
  2.  **روش قیمت‌گذاری (Pricing Mode)** — chips: `ساده`, `واحد`, `ویژگی`, `استعلامی`
  3.  **تخفیف (Discount)** — chips: `دارای تخفیف`, `بدون تخفیف`
  4.  **مرتب‌سازی (Sort)** — optional radio: `جدیدترین`, `کم‌موجودترین اول`, `ارزان‌ترین اول`, `گران‌ترین اول`
  5.  **گروه یا دسته‌بندی** — optional if categories exist (not mandatory MVP)

**Behavior:**
- Selecting filters does not immediately close sheet; seller taps «اعمال فیلتر» CTA at bottom of sheet to apply.
- «پاک کردن» link resets all filters.
- If no products match filter → same empty state «محصولی یافت نشد» but with subtitle «فیلترها را تغییر دهید».
- Filter state persists until cleared or page reload? At least session persistence.
- Filter must work combined with search (search + filters = intersection).
- Filter logic uses effective stock (sum of variants unless infinite).

**Non-goals:** No price range slider, no advanced date filters in MVP.

---

## 4. Item Detail Screen Fixes (`stock-item.png` / `pricing-tabs.png` / `dropdown.png`)

### 4.1 Remove Pricing Method Tabs Entirely

File: `pricing-tabs.png` shows segmented control: ساده / واحد / ویژگی

**Problem:** Seller should not be allowed to change pricing method in Stock.

**Expected:**
- Completely remove tabs component.
- Instead, show non-interactive label: «نوع قیمت‌گذاری: ویژگی — گروه: اندازه» or «واحد — ۲ واحد تعریف شده».
- No switching inside Stock.

### 4.2 Remove Price Option Dropdown Entirely

File: `dropdown.png` — «انتخاب گزینه قیمت» dropdown

**Problem:** Redundant, confusing.

**Expected:** Remove permanently. Base price only exists for simple mode.

### 4.3 Infinite Stock Switch — Missing

**Expected:**
- Add «موجودی نامحدود» switch/toggle at top of item edit screen, visible for all modes.
- Off (default): normal stock inputs editable.
- On: All variant stock fields disabled / show ∞, effective stock = infinite (always موجود).
- Remember previous stock values when toggling on/off.
- Export shows نامحدود, not 0.

### 4.4 Variant Management Restriction

**Expected:**
- Seller **cannot** add/delete/rename variants in Stock.
- Only editable per existing variant: قیمت, موجودی, درصد تخفیف, حداقل سفارش
- Variant structure read-only from catalog.

### 4.5 Minimum Order Field

New required field per variant: حداقل سفارش, integer >=1, default 1, shown next to stock.

---

## 5. Excel Export — Complete Redesign (Updated with new SKU)

**Current problem:** Export is product list, incomplete, unclear, not usable for bulk update, old SKU.

**Expected: Export is Variant List Export with new composite SKU**

One Excel file, each row = one sellable variant.

Simple/Inquiry = 1 row, Unit/Attribute = N rows.

#### Required Columns — Updated Order

1.  **variant sku (full composite)** — New format `{SELLER_SHORT}-{PRODUCT_SKU}-{VARIANT_SKU}` e.g. `MANO-605553-BIG`. This is the key for import matching.
2.  **product instance sku** — The middle part for grouping: `605553`
3.  **seller short code** — `MANO` (read-only, for reference)
4.  **product name** — Read-only reference e.g. «تست»
5.  **attribute name | unit name** — «نام ویژگی / نام واحد»
6.  **attribute value | unit value** — «مقدار ویژگی / مقدار واحد» e.g. بزرگ / ۵۰۰ گرم
7.  **min order** — حداقل سفارش
8.  **stock** — موجودی or «نامحدود»
9.  **discount %** — درصد تخفیف 0-100
10. **price** — قیمت پایه به تومان

Optional: pricing mode, effective stock aggregated.

**Formatting:** Persian headers, ASCII SKU values, no merged cells.

---

## 6. Excel Import — Complete Redesign (Updated)

**Current problem:** product list, cannot handle per-variant, wrong SKU format.

**Expected: Bulk Renewal via Composite Variant SKU**

Seller downloads variant export, edits price/stock/discount/min order, re-uploads single file.

**Behaviors:**

1.  **Matching Key:** Use **full composite variant sku** (`MANO-605553-BIG`) as unique identifier. NOT product code alone. Product name ignored.
2.  **Allowed Changes:** قیمت, موجودی, درصد تخفیف, حداقل سفارش, infinite flag (if stock = نامحدود)
3.  **Not Allowed:** Renaming variants, adding new variants, deleting, changing pricing method, changing SKU structure itself → error «ویرایش ساختار واریانت/کد از طریق انبار ممکن نیست».
4.  **Single file flow:** One file updates all variants regardless of pricing mode.
5.  **Seller short validation:** If imported SKU's seller short doesn't match current seller's short, reject row → error «کد فروشنده ناهماهنگ».

**Validation & Error Reporting:**
- Unknown full composite SKU => error «کد واریانت یافت نشد: {sku} - ردیف {n}»
- Negative price / invalid discount / non-integer stock => error per row.
- If stock = «نامحدود», set infinite flag.
- Summary after upload: موفق count, ناموفق count, per-row list with variant sku, row number, reason.

---

## 7. Additional UX / Business Rules

- **Simple / Inquiry:** one row only. Badge = that single stock.
- **Effective stock:** sum of variant stocks unless infinite => always موجود.
- **Low-stock threshold:** per product aggregation.
- **Search:** by product name OR full composite SKU OR seller short.
- **Edit button:** icon-only next to title in new card design, not bottom full-width. Tooltip «ویرایش».
- **RTL & Mobile:** No change.
- **Filter:** BottomSheet persists with search; badge shows active count.

---

## 8. Acceptance Checklist (Updated)

- [ ] Stock list cards match NEW `stock-card.html`: title + icon-only edit next to title, no description, no bottom button, thumbnail 132px, variant rows with discount, stock count logic (<10 show), status badge.
- [ ] Full composite SKU displayed: `{SELLER_SHORT}-{PRODUCT_SKU}-{VARIANT_SKU}` e.g. MANO-605553-BIG. Show per variant, not shared.
- [ ] Filter button exists next to search in stock-list. Tapping opens bottom sheet with handle, overlay, sections: Stock Status (موجود/رو به اتمام/ناموجود/نامحدود), Pricing Mode (ساده/واحد/ویژگی/استعلامی), Discount (دارای/بدون), Sort (optional). Apply and Clear actions work. Badge count visible when filters active. Works combined with search.
- [ ] Pricing method tabs (`pricing-tabs.png`) completely gone from item screen. Only read-only label.
- [ ] Price option dropdown (`dropdown.png`) completely gone.
- [ ] Infinite stock switch exists at top of item screen. When ON, stock inputs disabled, badge = موجود (infinite), export shows نامحدود.
- [ ] Seller cannot add/delete/rename variants in stock edit; fields are price, stock, discount %, min order only.
- [ ] Export file is variant list: Simple/Inquiry 1 row, Unit/Attribute N rows. Columns include full composite SKU as first column plus seller short and product instance SKU. Data clear and complete with min order, stock, discount, price.
- [ ] Import uses full composite SKU as key, updates only price/discount/stock/min order. Validates seller short. Bulk renew with single file. Clear error reporting per row.
- [ ] No catalog structure editing via stock.

---

## 9. What This Ticket Is NOT

- No change to how variants are created in catalog (except SKU assembly).
- No backend schema discussion (except SKU format definition).
- No implementation of Excel parsing libraries.
- No change to product creation flow except SKU auto-assembly.

This spec is ready to be used as AI coding prompt for Stock plugin with filter bottomsheet and new SKU structure.
