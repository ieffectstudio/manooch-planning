# PRD — Plugin Management System & Feature/Plugin Refactor

**Product:** منوچ (Manooch) store-builder — Admin / Seller Panel / Storefront
**Document type:** Product Requirements Document (PRD)
**Version:** 1.0
**Date:** 2026-08-16
**Status:** Draft for review

> Note: this PRD intentionally contains **no code or implementation logic**. It describes the
> *what* and *why* in full detail so that engineering can later design the *how*. Terms that
> appear in the Persian UI (e.g. پیکربندی = "Configure") are kept in Persian where they map to
> a specific on-screen label, with an English translation alongside.

---

## 1. Summary

Today the admin directory mixes two different kinds of things under one roof:

- **Plugins** — optional, sellable, individually toggleable capabilities (e.g. qr-code, sync, category, banner).
- **Dashboard features** — core, always-on parts of the seller experience (e.g. orders, profile, notifications).

This PRD defines a clean split between the two, introduces a **Plugin Management page** where a
**super admin** (portal) can enable/disable each plugin **per store and per seller**, and makes the
disabled state behave consistently everywhere — in the seller panel, in the admin product/customer
flows, and on the storefront (including URL routes).

It also describes how **Payment Ways** become their own plugin (decoupled from "personilize"), how a
**section wrapper** standardizes the show/hide behavior of every plugin, and the metadata model for
price, discount, and video tutorials shown on the Plugin Management page.

---

## 2. Background & Current State

### 2.1 Current directory reality

- Some features live inside a `plugin` directory.
- Other features are **not** nested in the plugin directory **but are conceptually plugins too**:
  - qr-code
  - sales-report
  - sarnakh
  - sync
  - payment-link
  - payment-enamad

- The rest are **dashboard features**, not plugins:
  - support
  - notification
  - subscription
  - orders
  - profile
  - invite-friends
  - business
  - personilize
  - authentication
  - the dashboard page itself

### 2.2 Problems this PRD solves

1. **No unified on/off switch.** There is no single place where an administrator can disable a
   capability and have that decision respected everywhere.
2. **Leaky disabled state.** When something is off, its pages, widgets, and even URL routes still
   render in the seller panel and storefront.
3. **Category is deeply embedded.** Category appears in the storefront (product listing, filter),
   on the PDP (product detail page) widget and URL slug, and in the admin add-product / customer
   flows. None of these currently respect a disabled state.
4. **Payment ways are tangled into personilize.** Payment methods are a first-class, sellable
   capability and should be their own plugin.
5. **No consistent packaging.** Every plugin should present the same layout, metadata (price,
   discount, optional video tutorial), and a "Configure" entry point.

---

## 3. Goals

1. Introduce a **Plugin Management page** in the **portal super-admin panel** that lists **all**
   plugins.
2. Let a super admin **enable/disable** each plugin:
   - for a **specific store**, and/or
   - for a **specific seller** (from within the seller panel context).
3. Make the disabled state **consistent and total**:
   - The seller does not see the plugin's pages or widgets in the seller panel.
   - The storefront hides all UI and routes tied to the disabled plugin.
   - The admin product/customer flows hide any section tied to the disabled plugin.
4. Extract **Payment Ways** into a dedicated plugin, independent of personilize.
5. Introduce a **section wrapper** concept so every plugin's sections follow one show/hide rule.
6. Define the **plugin metadata model** (price, discount, video tutorial, configure target) shown
   on the management page.
7. Provide a **migration/refactor plan** that reclassifies existing features into plugins vs.
   dashboard features without changing end-user behavior for enabled plugins.

## 4. Non-Goals (out of scope for this phase)

- Payment/billing integration that actually charges a seller for a paid plugin (this PRD defines
  the price/discount *display and state*; actual checkout is a separate initiative).
- Plugin installation from a marketplace by sellers themselves (plugins are centrally controlled by
  the portal for now).
- Any change to the internals of an enabled plugin's business logic.
- Analytics or usage telemetry for plugins.

---

## 5. Terminology

| Term | Meaning |
|------|---------|
| **Portal / Super Admin** | The top-level control panel that manages stores and sellers. |
| **Store** | A single storefront instance owned by a seller (or a tenant). |
| **Seller** | A merchant who owns/operates a store. |
| **Seller Panel** | The merchant-facing admin UI where the seller manages their store. |
| **Plugin** | An optional, toggleable capability with its own page(s), widgets, routes, and metadata. |
| **Dashboard feature** | A core capability that is always available and cannot be disabled. |
| **Enabled / Active** | The plugin is visible and functional for the given scope (store/seller). |
| **Disabled / Inactive** | The plugin is hidden everywhere for the given scope: pages, widgets, sections, and routes. |
| **Configure (پیکربندی)** | Button that navigates to the plugin's own configuration page. |
| **Plugin Management page** | The portal page listing all plugins with enable/disable, price, discount, and video tutorial. |
| **Section Wrapper** | A reusable container that decides, based on plugin state, whether its content renders. |
| **PDP** | Product Detail Page. |

---

## 6. Feature Classification (target state)

This is the canonical inventory the refactor must produce. It will become the source of truth for
the Plugin Management page.

### 6.1 Plugins (toggleable, listed on the management page)

| Plugin | Source / current location | Notes |
|--------|---------------------------|-------|
| qr-code | `plugin` dir | |
| sales-report | `plugin` dir | |
| sarnakh | `plugin` dir | |
| sync | `plugin` dir | |
| payment-link | `plugin` dir | |
| payment-enamad | `plugin` dir | |
| **Category (دسته‌بندی)** | currently not in plugin dir | the flagship example in this PRD (see §9) |
| **Features / Attributes (ویژگی‌ها)** | currently not in plugin dir | |
| **Storefront / Shop (فروشگاه)** | currently not in plugin dir | |
| **Banner (افزونه بنر)** | currently not in plugin dir | |
| **FAQ (سوالات پرتکرار)** | currently not in plugin dir | |
| **Payment Ways (روش‌های پرداخت)** | extracted from personilize | new plugin (see §10) |

> This list is extensible. Any future capability that is optional and sellable becomes a plugin
> and automatically appears here.

### 6.2 Dashboard features (always on, NOT listed as plugins)

- support
- notification
- subscription
- orders
- profile
- invite-friends
- business
- authentication
- the dashboard page itself

> **personilize** stays a dashboard feature. Only its *payment-way* portion moves out into the new
> Payment Ways plugin.

---

## 7. Requirements — Plugin Management Page

### 7.1 Location & access

- Lives in the **portal super-admin panel**.
- Only super admins can see and change plugin state. Sellers can view their own plugins' state but
  cannot change enablement (unless the super admin delegates that permission — see §7.2).

### 7.2 Enablement scope

Disabling must support two granularities:

1. **Per store** — the plugin is off for an entire store. Every seller of that store and the whole
   storefront are affected.
2. **Per seller** — the plugin is off for one specific seller even if the store-level plugin is on.
   Example: super admin disables "Category" for a specific store **or** for the seller themselves
   from inside the seller panel.

> Rule: a plugin is **active for a seller** only if (store-level enabled) AND (seller-level not
> individually disabled).

### 7.3 List content — every plugin shows

- Plugin **name** (e.g. فروشگاه, دسته‌بندی, ویژگی‌ها).
- A short **description**.
- A **status badge**:
  - `فعال` (Active) — green.
  - `در این پلن غیرفعال` (Disabled in this plan) — red/gray.
- A **toggle switch** (on/off).
- When **enabled**: a `پیکربندی` (**Configure**) button that navigates to the plugin's own page.
- When **disabled**: a **price** (e.g. ۹۹٬۰۰۰ تومان) and a `خرید افزونه` (**Buy plugin**) button
  (see §7.5).

### 7.4 Uniform layout

- All plugins use **the same card layout** (icon/title/description, toggle, status badge, action
  row) as shown in the prototype. No plugin gets a bespoke card design.

### 7.5 Price & discount (optional)

- Each plugin **may** carry a **price** and an optional **discount** (e.g. strikethrough original
  price + discounted price).
- Price and discount are **not required** — a plugin can be free.
- Price/discount are set **from the portal** and only affect the display and eventual purchase flow;
  they do not affect enable/disable behavior itself in this phase.

### 7.6 Video tutorial (optional)

- Each plugin **may** carry a **video tutorial** link/embed.
- The tutorial is **set from the portal** and is **not required**.
- If absent, no tutorial UI is shown (the card simply omits it).

### 7.7 "Configure" navigation

- Clicking `پیکربندی` opens the plugin's own configuration page.
- If a plugin has no dedicated configuration screen yet, the button still targets a stub/landing
  page so the behavior is consistent.

---

## 8. Requirements — Disabled behavior (the core contract)

When a plugin is disabled for a seller/store, **all** of the following must hold. This is the
single most important acceptance surface of the PRD.

### 8.1 Seller panel

- The plugin's **menu entries / navigation links** are hidden.
- The plugin's **pages and routes** are inaccessible (guarded — see §11).
- The plugin's **widgets and dashboard cards** are hidden.
- Nothing that *depends on* the disabled plugin is shown.

### 8.2 Admin flows (add product / customer)

- Any **section** in the add-product or customer flows that belongs to the disabled plugin is
  hidden. Example: if **Category** is disabled, the category-picker section disappears from
  add-product and from the customer category selection.

### 8.3 Storefront (the Category example)

If the **Category** plugin is disabled, on the storefront:

1. **Category of products is not visible** — products are no longer grouped/attributed by category.
2. **Category filter is not visible** — the filter control disappears from listing/search.
3. **PDP category widget is not visible** — the category block on the product detail page is hidden.
4. **PDP category route/slug does not exist** — see §9.

The same pattern generalizes to every plugin: *whatever UI, widget, section, or route a plugin
owns is hidden when the plugin is off.*

---

## 9. Detailed Requirement — Category slug / URL behavior

Given a product PDP URL such as:

```
/product/گوشواره/گوشواره-حلقه-ایمیناکاری--afc5463c-16fb-482f-9fd0-599a36ee11ae
```

Here `گوشواره` is the **category** segment in the route.

**When Category is enabled:** the URL works exactly as today.

**When Category is disabled:**

1. The category segment (`گوشواره`) must be **removed** from the route.
2. The product resolves at a **category-less** path, e.g.:
   `/product/گوشواره-حلقه-ایمیناکاری--afc5463c-16fb-482f-9fd0-599a36ee11ae`
3. If products were assigned to a specific category, the disabled state must **move them to the
   parent ("all") category** (or an equivalent uncategorized state) so no product is orphaned or
   lost.
4. Any **old category-based URL** must **not resolve** to a category page — it should behave as
   non-existent (e.g. redirect to the category-less product page or return not-found). The
   requirement is that the category route **does not exist** while disabled.
5. When the plugin is re-enabled, category segments and grouping return.

---

## 10. Requirement — Payment Ways as a new plugin

- **Payment ways** (payment methods: payment-link, payment-enamad, etc.) become their own plugin
  page, fully **separate from personilize**.
- personilize remains a dashboard feature and **loses** its payment-way responsibility.
- The Payment Ways plugin:
  - appears on the Plugin Management page like any other plugin,
  - can be enabled/disabled per store/seller,
  - hides all payment-method UI, selection, and checkout options when disabled,
  - respects the same price/discount/video-tutorial metadata model.
- Existing payment-method configuration is migrated into the new plugin without losing a seller's
  saved settings.

---

## 11. Requirement — Section Wrapper (uniform show/hide)

To guarantee §8 consistently, every plugin's UI must be grouped into identifiable **sections** that
are wrapped by a single mechanism ("section wrapper").

### 11.1 What a section wrapper provides

- A single decision point: **"is this plugin active for the current seller/store?"**
- If active → render the section normally.
- If inactive → render nothing (and, where relevant, guard the route so it is inaccessible).

### 11.2 Where wrappers are applied

- Seller panel: each plugin page and each plugin widget.
- Admin add-product / customer: each plugin-owned input section.
- Storefront: each plugin-owned widget, filter, and route segment.
- PDP: the category widget and the category slug segment.

### 11.3 Scope of wrapping

- The wrapper applies to **plugin-owned sections only**. Dashboard features are never wrapped and
  always render.

---

## 12. Data / Metadata model (conceptual)

The following describes *what must be represented*, not how it is stored.

### 12.1 Plugin registry (one entry per plugin)

- Unique identifier (e.g. `category`, `qr-code`, `payment-ways`).
- Display name (Persian, e.g. `دسته‌بندی`).
- Description.
- Whether it is listed on the management page (always yes for plugins).
- Configure target (which page the `پیکربندی` button opens).
- Optional: price, discount, video tutorial URL.
- Whether it is currently available/visible in the portal.

### 12.2 Enablement state

- Store-level flag per plugin (enabled/disabled).
- Seller-level override per plugin (inherit / force-disable — and if the product later needs it,
  force-enable).
- The effective state for a seller is the combination described in §7.2.

### 12.3 Migration metadata

- A mapping from the **old location** (e.g. folder under `plugin/` or a loose folder) to the
  **new classification** (plugin vs dashboard feature) and its registry entry. This drives the
  refactor in §13.

---

## 13. Migration & Refactor plan (conceptual)

This is a *plan*, not code. Engineering will map each step to concrete implementation.

### 13.1 Phase A — Inventory & classify

1. Enumerate every folder under the admin directory.
2. Tag each as **plugin** or **dashboard feature** using the classification in §6.
3. Confirm the list with product/stakeholders before any code moves.

### 13.2 Phase B — Establish the registry

1. Introduce a single source of truth listing all plugins and their metadata (§12.1).
2. Give every plugin a stable identifier used across panel, storefront, and routes.

### 13.3 Phase C — Introduce the section wrapper

1. Build the wrapper (§11) as the only way to show/hide plugin-owned UI.
2. Wrap existing plugin pages/widgets/sections behind it, starting with **Category** as the pilot.

### 13.4 Phase D — Extract Payment Ways

1. Move payment-method logic out of personilize into the Payment Ways plugin.
2. Migrate saved payment settings so nothing is lost.
3. Verify checkout and payment selection still work when enabled.

### 13.5 Phase E — Portal Plugin Management page

1. Build the management page (§7) from the registry.
2. Wire enable/disable to store-level and seller-level state.

### 13.6 Phase F — Route handling (Category pilot)

1. Implement category-less product routing when Category is disabled (§9).
2. Move products to the parent/"all" category when Category is turned off.

### 13.7 Phase G — Rollout to remaining plugins

1. Apply the wrapper + management-page entry to every remaining plugin (qr-code, sales-report,
   sarnakh, sync, payment-link, payment-enamad, features, storefront, banner, FAQ).
2. Verify disabled behavior per §8 for each.

### 13.8 Phase H — Polish & parity

1. Ensure enabled plugins behave **identically to before** the refactor (no regression).
2. Add the video-tutorial and price/discount fields to the portal.

### 13.9 Non-regression rule

- For any plugin that is **enabled**, end-user behavior must be indistinguishable from today.
- The refactor only *adds* the ability to hide things; it must not change what an enabled plugin
  shows.

---

## 14. UI / UX requirements (from the prototype)

Reference: `plugin-page.html` (mobile seller-panel view) — the portal page follows the same card
language.

- **Top bar**: back button, title `افزونه‌ها` ("Plugins") with a subtitle
  ("افزونه های مورد نیاز خودت رو فعال کن").
- **Card** per plugin with:
  - toggle switch (purple = on, gray = off),
  - name + status badge (`فعال` green / `در این پلن غیرفعال` red),
  - description line.
- **Action row**:
  - enabled → full-width `پیکربندی` button.
  - disabled → price (e.g. `۹۹٬۰۰۰ تومان`) + `خرید افزونه` button.
- **Tab bar** at the bottom with the Plugins tab highlighted.
- The **portal** version additionally shows: store/seller scope selector, price & discount editing,
  and the video-tutorial link (all optional fields).

---

## 15. Acceptance criteria

### 15.1 Management page
- [ ] All plugins from §6.1 appear on the portal Plugin Management page.
- [ ] Each shows name, description, status badge, toggle, and (when relevant) price + buy, or
      configure button.
- [ ] `پیکربندی` navigates to the plugin's own page.
- [ ] Price, discount, and video tutorial are optional; a plugin without them shows no such UI.

### 15.2 Enable/disable
- [ ] Super admin can disable a plugin per store.
- [ ] Super admin can disable a plugin per seller (from within the seller panel).
- [ ] Effective state follows the rule in §7.2.

### 15.3 Disabled consistency (Category pilot)
- [ ] With Category disabled: seller panel hides category pages/widgets.
- [ ] Admin add-product and customer flows hide the category section.
- [ ] Storefront hides category of products and the category filter.
- [ ] PDP hides the category widget.
- [ ] The category route/slug no longer exists; the product resolves at a category-less URL
      (`/product/<product>`), and products are moved to the parent/"all" category.
- [ ] Re-enabling Category restores all of the above.

### 15.4 Payment Ways
- [ ] Payment Ways is its own plugin, listed on the management page, independent of personilize.
- [ ] Disabling it hides payment-method UI and selection.
- [ ] Saved payment settings survive the migration.

### 15.5 Wrapper & parity
- [ ] Every plugin-owned section is behind the wrapper.
- [ ] Dashboard features are never wrapped and always render.
- [ ] Enabled plugins behave identically to before the refactor.

---

## 16. Open questions (to resolve with stakeholders)

1. When Category is disabled, should the old category URLs **redirect** to the category-less product
   page, or return **404**? (This PRD allows either; the product/SEO decision is pending.)
2. Should sellers ever be able to **self-enable** a disabled paid plugin (i.e. trigger the
   `خرید افزونه` flow), or is purchase purely super-admin driven for now?
3. Should there be a **per-seller force-enable** override, or only force-disable?
4. Do price/discount need multi-currency or just تومان for now?
5. For "all category" fallback — should it be a real "Uncategorized" bucket or a virtual parent?

---

## 17. Success measures

- Zero cases where a disabled plugin's page, widget, section, or route is reachable.
- The Category pilot passes all §15.3 criteria end-to-end.
- Payment Ways fully decoupled from personilize with no lost settings.
- Every plugin — current and future — is managed through one page with one consistent layout.
