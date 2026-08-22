# PRD — Subscription Plan Structure Update (Plan ↔ Plugin Binding)

**Product:** منوچ (Manooch) — Portal Super Admin / Seller Panel / Storefront
**Document type:** PRD
**Version:** 1.0
**Date:** 2026-08-16
**Status:** Draft for review
**Companion prototype:** `plan-plugins-management.html`

> Follows the plugin PRD (plugin management & feature/plugin refactor). This document defines the
> **plan** layer that sits on top of plugins: which plugins are included in each plan, how each
> plan prices its plugins (inherited from the super-admin base price or overridden), and how a
> seller's live subscription drives the plan widget in the seller dashboard.
>
> Contains **no code** — it describes the *what* and *why*. The prototype demonstrates the
> *functional behavior* (switches + per-plan pricing/discount) using the existing design system.

---

## 1. Summary

There are **three subscription plans**. Today:

- Plans are managed via an **edit modal**.
- **Plugins are not bound to plans** — there is no way to say "this plugin is included in plan A
  but not plan B". This is the biggest gap.
- A plugin has a **price** (set by the super admin), but there is no way to express a **per-plan
  price** that differs from that base price.
- Plans should support a **discount**, just like plugins do.
- The **plan widget** in the seller dashboard shows **static** data instead of the seller's actual
  subscription.

This PRD introduces:

1. A new **Plugin ↔ Plan management page** (a matrix: plans as columns, plugins as rows, a switch
   in each cell).
2. A **pricing model** with three levels: plugin **base price** → **plan price** (inherit or
   override) → **plan discount**.
3. A **live plan widget** driven by the seller's subscription (`GET /subscriptions/me`).

---

## 2. Background & current state

### 2.1 Current assets
- 3 subscription plans exist.
- An **edit modal** exists for plans (see screenshots).
- The seller dashboard contains a **plan widget** that currently shows **hard-coded / static** data.

### 2.2 Problems
1. **No plugin↔plan binding.** Plans cannot include/exclude plugins, so every seller on a plan
   effectively sees the same feature set — pricing tiers cannot gate capabilities.
2. **Single flat plugin price.** The super-admin base price is the only price; plans cannot show or
   charge a different amount.
3. **No plan discount.** Discounts exist at the plugin level only.
4. **Static plan widget.** The seller dashboard widget does not read the user's real subscription,
   so it can show wrong plan/status/features.

---

## 3. Goals

1. Bind **every plugin to every plan** through a single management page (matrix of switches).
2. Let each plan **price each plugin** independently — defaulting to the super-admin base price,
   overridable per plan.
3. Let each plan apply a **discount** per plugin (and/or per plan).
4. Make the seller dashboard **plan widget read live subscription data** from the API.
5. Keep the existing design system and edit modal, extended (not replaced) where needed.

## 4. Non-Goals

- Actual billing / invoicing / payment capture for plans (out of scope; this defines state & pricing
  display only).
- Plan creation/deletion UI beyond the existing edit modal (the 3 plans remain).
- Self-service plan change by sellers (unless already supported).

---

## 5. Terminology

| Term | Meaning |
|------|---------|
| **Plan** | A subscription tier (3 exist). Defines which plugins are included and at what price. |
| **Plugin base price** | The price the super admin sets on a plugin (from the plugin page / prior PRD). |
| **Plan price (override)** | The price of a plugin *within a specific plan*. Defaults to base price; can be overridden. |
| **Plan discount** | A percentage discount applied to a plugin's price within a plan. |
| **Effective / final price** | Plan price after applying the plan discount. |
| **Plan ↔ Plugin matrix** | The management page: columns = plans, rows = plugins, cells = switches + price/discount. |
| **Plan widget** | The card in the seller dashboard showing the seller's plan, status, and included plugins. |
| **Subscription** | The seller's actual record returned by `GET /subscriptions/me`. |

---

## 6. Requirements

### 6.1 Plugin ↔ Plan management page (new)

- A new page in the **portal super admin panel**.
- Layout is a **matrix table**:
  - **Columns** = the 3 plans.
  - **Rows** = all plugins (from the plugin registry defined in the plugin PRD — now the **18-plugin
    live registry**, see §6.1 of the plugin PRD; the prototype `plan-plugins-management.html` uses
    this exact list).
  - **Each cell** contains a **switch** to enable/disable that plugin for that plan.
- The page must also expose, per cell, the **price** and **discount** for that plugin in that plan
  (see §6.2).
- The page supports bulk actions: "enable all" / "disable all" per plan column.
- Search/filter by plugin name.
- A "save changes" affordance (state is committed; in the prototype it is simulated with a toast).
- See `plan-plugins-management.html` for the exact behavior and layout (built on the design system).

### 6.2 Pricing model (three levels)

1. **Plugin base price** — set by super admin on the plugin itself (authoritative default).
2. **Plan price** — per (plan, plugin) cell:
   - By default **inherits** the base price (shown as "مطابق پایه" = "matches base").
   - Can be **overridden** to a custom amount (shown as "اختصاصی" = "custom").
3. **Plan discount** — per (plan, plugin) cell, a percentage discount (optional, like plugin
   discounts).
   - Effective price = plan price × (1 − discount%).

Rules:
- The base price is **read-only** in the matrix (it is edited on the plugin page); it is shown as a
  reference next to each plugin row.
- An override is optional; when cleared, the cell falls back to base price.
- Discount is optional; when empty, no discount is shown.
- A plugin included in a plan **without any override** shows the base price and inherits future base
  price changes.

### 6.3 Plan edit modal (update)

The existing edit modal is extended to also surface (not necessarily edit) the plugin-binding
summary:
- Number of included plugins ("۸ از ۱۲ افزونه").
- Plan discount (if a plan-level discount is supported — see open questions).
- A link/button that opens the plugin↔plan matrix page for that plan.

### 6.4 Live plan widget (seller dashboard)

- Replace the static plan widget data with the seller's real subscription from
  `GET https://api.manooch.site/subscriptions/me` (Bearer token).
- The widget must render:
  - Plan name (localized),
  - Subscription **status** (active / expired / trial / pending),
  - Renewal/expiry date,
  - The list of **included plugins** (from the plan binding) — ideally with each plugin's
    included/excluded state,
  - Pricing summary (plan price, discount, final price) if applicable.
- **Loading / empty / error states**: skeleton while loading, an error state with retry, and an
  "no active subscription" state.
- The widget must update whenever the plan binding changes (next fetch, or reactive update).

---

## 6A. Relationship to the existing `minTier` field

The live plugin registry already contains a `minTier` field (currently `null` on every plugin) and
an `isGloballyActive` flag. The plan matrix **supersedes `minTier`**:

- `minTier` can only express "minimum plan", whereas the matrix expresses arbitrary
  include/exclude per plan — the matrix is the source of truth going forward.
- **Migration rule:** when the matrix ships, `minTier` is either (a) removed, or (b) retained as a
  read-only hint derived from the matrix (the lowest tier where the plugin is enabled). Keeping both
  active would create two conflicting sources of truth — this PRD forbids that.

## 7. Relationship between plugin state and plan binding

The two PRDs compose. A plugin is **effectively active for a seller** when ALL of the following
hold:

1. **Plugin globally enabled** (super admin plugin toggle — plugin PRD §7).
2. **Plugin included in the seller's plan** (this PRD's matrix switch).
3. **Not individually disabled for the seller/store** (plugin PRD §7.2).

Rule: if a plugin is excluded from a plan, sellers on that plan cannot see/use it regardless of the
global plugin toggle. Disabling globally overrides everything (off in all plans).

---

## 8. Data model (conceptual)

### 8.1 Plan
- id, name, description, price (plan-level, if applicable), discount (optional), status.

### 8.2 PlanPluginBinding (the matrix cell)
- planId + pluginId (unique pair).
- enabled: boolean.
- priceOverride: number | null (null = inherit base price).
- discountPercent: number | null.

### 8.3 Subscription (as returned by the API)
- plan reference (id/name), status, start/end dates, and the **resolved list of included plugins**
  (already filtered by the plan binding and global toggles). See §9.

---

## 9. API integration — `/subscriptions/me`

**Endpoint:** `GET https://api.manooch.site/subscriptions/me`
**Auth:** `Authorization: Bearer <token>` (token scope: `admin`).

The plan widget consumes this endpoint. The PRD requires the response to contain (contract —
actual field names to be confirmed against the backend):

| Field | Purpose |
|-------|---------|
| `plan` | Plan id/name/slug the seller is on. |
| `status` | active / expired / trial / pending. |
| `startedAt` / `expiresAt` | Dates for the widget. |
| `planPrice` / `discount` / `finalPrice` | Pricing summary (if the plan has pricing). |
| `plugins` | Resolved list of plugins available to this seller, each with `id`, `name`, `enabled` (true/false) — already reflecting the plan binding and global toggles. |

**Acceptance:** the widget renders exclusively from this payload (no hard-coded plan/feature data).
The response shape must be validated against the live API during implementation; any missing fields
(e.g. `plugins`) must be added to the backend contract.

---

## 10. UI / UX requirements (design system)

Consistent with the existing system (see `plugin-page.html`):

- Purple primary `#4B45E6`, soft-purple chips `#EFEBFE` / text `#6C4DF6`.
- Green `#12B76A` (active), red `#E5484D` (disabled/off).
- Cards: white, radius 16px, border `#ECEEF5`, background `#EFF0F6`.
- Toggle switch: 44×24, purple when on, gray when off.
- Text: `#16161D` primary, `#737377` / `#7B8194` secondary.
- RTL Persian, Vazirmatn font.

Matrix-specific:
- Sticky plan header row and sticky plugin-name column for scrolling.
- Cell states:
  - **on** → full-opacity cell, price/discount editable, final price shown.
  - **off** → dimmed cell (e.g. 45% opacity), plugin excluded.
- Price display: `۹۹٬۰۰۰ تومان`; tag `مطابق پایه` (inherit) vs `اختصاصی` (override); struck-through
  original when a discount is active; `قیمت نهایی: …` computed line.
- Discount display: `۲۰٪ تخفیف` or `بدون تخفیف`.

---

## 11. Acceptance criteria

### 11.1 Matrix page
- [ ] All plugins appear as rows; all 3 plans appear as columns.
- [ ] Each cell has a working switch (enable/disable plugin for that plan).
- [ ] "Enable all / disable all" works per plan column.
- [ ] Search filters plugin rows.
- [ ] Price and discount are editable per cell and reflect the three-level model (§6.2).

### 11.2 Pricing
- [ ] Each cell shows base price as reference and inherits it by default.
- [ ] Overriding a cell's price marks it `اختصاصی` and is independent of other plans.
- [ ] Clearing an override falls back to base price (and inherits future base changes).
- [ ] Setting a discount shows the final price correctly; removing it clears the final-price line.

### 11.3 Plan widget
- [ ] Widget reads from `/subscriptions/me` (no static data).
- [ ] Widget shows plan name, status, dates, included plugins, and pricing.
- [ ] Loading / error / no-subscription states all render correctly.

### 11.4 Integration with plugin PRD
- [ ] Effective plugin availability for a seller follows §7 (global toggle AND plan inclusion AND
      seller-level override).

---

## 12. Open questions

1. **Plan names** — confirm the exact 3 plan names (prototype uses placeholders: پایه / حرفهای /
   سازمانی).
2. **Plan-level discount** — is discount per (plan, plugin) only, or also a whole-plan discount?
3. **Inheritance** — should a plan override persist when the base price later changes, or should
   "inherits base" always track base? (This PRD assumes inherit = always track base.)
4. **Privileges** — can any super admin edit plan↔plugin bindings, or a specific role?
5. **API contract** — confirm exact field names/shape of `/subscriptions/me` (esp. the `plugins`
   list) before implementation.
6. **Widget refresh** — poll, refetch on focus, or push (websocket/SSE) for live subscription state?

---

## 13. Success measures

- Any plugin can be included/excluded per plan from one page, and sellers on that plan reflect it
  immediately in the widget and throughout the product.
- Every (plan, plugin) cell supports its own price and discount, independent of other plans and of
  the base price.
- The seller dashboard plan widget contains zero hard-coded subscription data.
