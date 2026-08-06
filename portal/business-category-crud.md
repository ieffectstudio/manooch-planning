# Business Category CRUD — Full Detailed Explanation

> **Verified against:** `manooch-backend` and `manooch-fronts` (portal + admin apps), 2026-08-06.
> Every claim below is traceable to a file cited inline.
> **Updated 2026-08-06:** the three gaps from §7 v1 (search parity, portal sub-category creation,
> stale `categoryId`) are fixed on branches `fix-taxonomy` in `manooch-backend`/`manooch-fronts`.
> One new gap was found while wiring the `categoryId` fix — see §7 item 4.

## Overview

This document describes the **Business Category CRUD** (Create, Read, Update, Delete) system for
managing **taxonomy-based categories** in a multi-role platform. The system spans two main areas:

1. **Portal (Super Admin / Taxonomy Management)** — Where categories are defined and structured.
   Routes live under `/admin/store-categories/*`, gated by `SuperAdminGuard`
   (`manooch-backend/src/modules/work-fields/admin-store-categories.controller.ts`).
2. **Admin Business Info Tab (Seller / Store Management)** — Where sellers pick a category for
   their store from the same taxonomy.

The taxonomy is **structurally** two-level: a parent table (`WorkGroup`, "category") and a child
table (`WorkField`, "sub-category"), related by a plain foreign key. There is no self-referencing
parent column, so deeper nesting isn't a configuration choice to confirm — it isn't representable
by the schema at all.

---

## 1. Core Concepts

### 1.1 Taxonomy — two entities, not one

- `WorkGroup` — the parent/category. Has `code`, `title`, `nameEn`, `iconAssetId`, `order`, and a
  `fields: WorkField[]` relation.
  (`manooch-backend/src/modules/work-fields/entities/work-group.entity.ts`)
- `WorkField` — the child/sub-category. Has `title`, `nameEn`, `iconAssetId`, `order`, and a
  required `workGroupId` FK (`onDelete: 'CASCADE'` at the DB level, though the service always
  soft-deletes fields explicitly before soft-deleting their group — see §2.4).
  (`manooch-backend/src/modules/work-fields/entities/work-field.entity.ts`)
- A store's category assignment (`Store.category` / `Store.categoryId`) points at a `WorkField`,
  **not** a `WorkGroup` — sellers pick a sub-category, never a top-level group.
  (`manooch-backend/src/modules/stores/store.entity.ts:76-83`)

### 1.2 Code (Taxonomy Code)

- Only `WorkGroup` (parent categories) have a `code`. `WorkField` (sub-categories) have no code
  field at all — confirmed by `CreateStoreSubCategoryDto` / `UpdateStoreSubCategoryDto`, which
  carry no `code` property.
- The code is **hand-typed by the admin**, not auto-generated. The portal form renders it as a
  plain text input whenever the target is a group (`hasCode = kind === 'create-group' ||
  kind === 'edit-group'`), with a hint describing the allowed charset ("فقط حروف بزرگ انگلیسی، عدد
  و _" — uppercase English letters, digits, and underscore only).
  (`manooch-fronts/apps/portal/app/(panel)/taxonomy/_common/TaxonomyFormModal/TaxonomyFormModal.tsx:69-77`,
  `TaxonomyFormModal.consts.ts:4`, `messages/fa.ts:355-356`)
- Server-side format is enforced by `CreateStoreCategoryDto`: `@Matches(/^[A-Z0-9_]+$/)`,
  max length 50. (`manooch-backend/src/modules/work-fields/dto/create-store-category.dto.ts`)
- The code is **editable, both at creation and afterward** — it is not locked once set.
  `UpdateStoreCategoryDto` is `PartialType(CreateStoreCategoryDto)`, and
  `WorkFieldsService.updateCategory` accepts a new `code`, re-checking uniqueness only when it
  actually changes (`work-fields.service.ts:129-151`).
- Uniqueness is enforced among **live** rows only, via a partial unique index —
  `@Index(['code'], { unique: true, where: '"deletedAt" IS NULL' })` — so a soft-deleted group's
  old code can be reused. A collision on create or update throws `409
  STORE_CATEGORY_CODE_TAKEN`.

### 1.3 Nesting (structural two-level relationship)

- A category (`WorkGroup`) can have zero or more sub-categories (`WorkField`); a sub-category
  belongs to exactly one category via its required `workGroupId`.
- There is no parent-selector UI anywhere in the portal — a sub-category's parent is fixed by
  **which route created it**: `POST /admin/store-categories/:id/sub-categories` creates a
  `WorkField` under group `:id` (`admin-store-categories.controller.ts:63-75`,
  `work-fields.service.ts:167-189`). Nothing in `UpdateStoreSubCategoryDto` allows changing
  `workGroupId` afterward — re-parenting is not implemented.
- This gives exactly two levels (group → field) as a schema fact, not a business rule that could
  be relaxed by future configuration — supporting a third level would require a new
  self-referencing column, not a flag change.

---

## 2. Portal — Taxonomy Management

The **Portal** (`manooch-fronts/apps/portal`, route `/taxonomy`,
`app/(panel)/taxonomy/PageClient.tsx`) is the super-admin interface for taxonomy CRUD.

### 2.1 Creating a Taxonomy Entry

| Field | Behavior |
|---|---|
| **Code** (groups only) | Typed by the admin, auto-uppercased on input, validated client-side against `^[A-Z0-9_]+$` before the Save button enables (`TaxonomyFormModal.tsx:24`). |
| **Name / Label (`title`)** | Manually entered, required. |
| **English name (`nameEn`)** | Optional. |
| **Parent** | Not selectable in the UI. A sub-category's parent is fixed by which action created it: a "+" button on each group row (`CategoryGroupRow.tsx`) opens the form with target `{ kind: 'create-field', group }`, which posts to that group's sub-category endpoint. |

Create paths (backend):
- `POST /admin/store-categories` — new group, `CreateStoreCategoryDto` (`code` required).
- `POST /admin/store-categories/:id/sub-categories` — new field under group `:id`,
  `CreateStoreSubCategoryDto` (no `code`). Reachable via the API/Swagger **and** the portal UI's
  per-group "+" action (`TaxonomyFormModal.tsx`).

### 2.2 Reading / Viewing Taxonomy

- `GET /admin/store-categories` returns all groups with their `fields` relation, ordered by
  `order` (`WorkFieldsService.findAll`).
- The portal renders this as a table of groups, each showing name, sub-category count, and status,
  expandable to its fields (`CategoryGroupRow`).
- The code is shown for groups; sub-category rows have no code to display.

### 2.3 Editing a Taxonomy Entry

- **Group**: title, `nameEn`, and **code** are all editable via `PATCH /admin/store-categories/:id`
  (`UpdateStoreCategoryDto`). A code change is validated for uniqueness the same way as on create.
- **Field**: title and `nameEn` are editable via `PATCH
  /admin/store-categories/sub-categories/:subId` (`UpdateStoreSubCategoryDto`). No code field
  exists to edit. No parent (`workGroupId`) field exists to edit.

### 2.4 Deleting a Taxonomy Entry

- Deletion is always a **soft delete** (`deletedAt` set) — the codebase's mandatory convention,
  never a hard `DELETE`.
- Deleting a group drains its fields first (TypeORM soft delete does not cascade), then
  soft-deletes the group itself: `workFieldRepo.softDelete({ workGroupId: id })` followed by
  `workGroupRepo.softDelete({ id })` (`work-fields.service.ts:154-159`).
- **There is no check for stores currently using the category being deleted.** Deletion always
  succeeds. `Store.category` is a `ManyToOne` with `onDelete: 'SET NULL'` specifically so that "a
  taxonomy edit/soft-delete must never touch a seller's store" (comment at
  `store.entity.ts:79-80`) — an affected store's `categoryId` is nulled at the DB level and the
  store keeps functioning with no category assigned. This is a deliberate design choice, not an
  open question.

---

## 3. Admin Business Info Tab — Seller Store Management

The **Admin Business Info Tab** (`manooch-fronts/apps/admin`,
`app/business/_common/InfoTab/InfoTab.tsx`) is where sellers manage their store's data, including
its category.

### 3.1 Seller Capabilities

- Sellers edit their own store's data in this tab, including the category field.
- The seller is restricted to their own store(s) — enforced by the store-scoped admin auth guard,
  not by anything category-specific.

### 3.2 Taxonomy Selection — one shared `Dropdown` component

- Both the registration flow (`app/(auth)/business-info/page.tsx`) and the Info tab
  (`InfoTab.tsx`) use the **same** `Dropdown` component (`@/ui`) — there are not two different
  component types ("bottom sheet" vs. "dropdown button sheet"). The only functional difference is
  which props each call site passes.
- Both list sub-categories (`WorkField`) only, never top-level groups, but their option **values**
  now differ: registration still builds `{ value: f.title, label: f.title }`
  (`business-info/page.tsx:50-52`, unchanged — it only ever writes the free-text `category` field,
  see §7 item 4), while the Info tab builds `{ value: f.id, label: f.title }`
  (`InfoTab.tsx:39-41`) so its selection can drive the `categoryId` FK. A legacy store with only
  `settings.category` (no `categoryId`) has its title resolved back to an id client-side via
  `InfoTab.utils.ts#resolveLegacyCategoryId`, matching on `WorkField.title` (globally unique, see
  §1.2/`WorkFieldsService.createSubCategory`'s `STORE_SUB_CATEGORY_TITLE_TAKEN` check).

### 3.3 Fixed — `searchable` Prop Parity (was missing)

- Registration: `<Dropdown ... searchable searchPlaceholder={fa.auth.businessInfo
  .categorySearchPlaceholder} ... />` (`business-info/page.tsx:159-170`).
- Info tab now passes the same props (`InfoTab.tsx:93-104`) — sellers editing an existing store can
  filter the category list instead of scrolling the full unfiltered set.

### 3.4 Comparison: Registration vs. Admin Business Info

| Feature | Registration Business Info | Admin Business Info Tab |
|---|---|---|
| **Component** | `Dropdown` (`@/ui`) | Same `Dropdown` (`@/ui`) |
| **`searchable` prop** | ✅ passed | ✅ passed (fixed) |
| **User** | New business registering | Existing seller editing their store |
| **Option value** | `WorkField.title` | `WorkField.id` (drives `categoryId` PATCH) |

---

## 4. Summary of Key Rules & Constraints

| Rule | Description |
|---|---|
| **Code is admin-authored** | The `code` field on a `WorkGroup` is typed by the admin, uppercased, and validated against `^[A-Z0-9_]+$` (max 50 chars). |
| **Code is editable** | Editable on both create and update; a change is checked for uniqueness among live rows and 409s on collision. |
| **Sub-categories have no code** | `WorkField` carries no `code` column or DTO field. |
| **Two-table nesting** | `WorkGroup` → `WorkField` via a required `workGroupId` FK. No self-referencing parent column exists, so no deeper nesting is representable. |
| **No re-parenting** | A field's `workGroupId` is fixed at creation (by which route created it) and cannot be changed via the update DTO. |
| **Portal can create sub-categories** (fixed) | Each group row has a "+" action that opens the form targeting that group's `POST .../sub-categories` endpoint. |
| **Soft delete only, no usage guard** | Deleting a group cascades a soft-delete to its fields; any store referencing an affected field has its `categoryId` set to `NULL` automatically — deletion is never blocked. |
| **Seller field matches the FK** (fixed) | The Info tab's category `Dropdown` now selects a `WorkField.id`; on save, `StoresService.update` resolves it, sets `Store.categoryId`, and mirrors the title into `settings.category` in the same write — the two can no longer diverge from this path. |
| **Search prop parity** (fixed) | The Info tab's `Dropdown` now passes `searchable`, matching the registration flow. |
| **Self-serve registration still FK-less** (new, see §7 item 4) | The registration wizard (`working/page.tsx`) posts `category` (free text) only, never `categoryId` — `Store.categoryId` starts `NULL` for every self-serve signup regardless of this fix. |

---

## 5. User Roles & Permissions

| Role | Access |
|---|---|
| **Super Admin (Portal)** | Full CRUD on `WorkGroup`/`WorkField` via `/admin/store-categories/*`, gated by `SuperAdminGuard` (requires `Customer.role === AccountRole.SUPER_ADMIN`). |
| **Seller (Admin Business Info Tab)** | Can change their own store's category selection through the store-settings update path. Cannot create, edit, or delete taxonomy entries — no portal access. |

---

## 6. Data Flow Summary

```
┌───────────────────────────────────────────────────────────────┐
│              PORTAL (Super Admin, SuperAdminGuard)             │
│                                                                 │
│  1. Admin creates a WorkGroup (category)                       │
│     → code typed by hand, validated, unique among live rows    │
│  2. Sub-category (WorkField) creation — API and portal UI       │
│     → POST /admin/store-categories/:id/sub-categories,          │
│       now also reachable via each group row's "+" button        │
│  3. Admin can view/edit (incl. code)/soft-delete groups & fields│
│     → deletion never blocked by stores referencing the field    │
└──────────────────────────┬──────────────────────────────────────┘
                            │  WorkGroup.fields → WorkField
                            ▼
┌───────────────────────────────────────────────────────────────┐
│              ADMIN — Business Info Tab (Seller)                 │
│                                                                 │
│  1. Self-serve registration: submits `category` (free text)     │
│       only — no `categoryId` sent                                │
│     → Store.categoryId starts NULL; settings.category set        │
│     → ⚠ still open, see §7 item 4                                │
│  2. Info tab edit: Dropdown (now `searchable`) selects a          │
│       WorkField.id, PATCHes `categoryId`                         │
│     → StoresService.update resolves it, sets Store.categoryId    │
│       AND mirrors the title into Store.settings.category          │
│     → FK and mirror can no longer diverge from this path (fixed) │
└───────────────────────────────────────────────────────────────┘
```

---

## 7. Open Issues / Action Items

1. ~~Add `searchable` to the Info Tab's category `Dropdown`.~~ **Fixed** (`fix-taxonomy`,
   `manooch-fronts`). `InfoTab.tsx` now passes `searchable` + `searchPlaceholder`, matching
   `app/(auth)/business-info/page.tsx`.

2. ~~Portal has no UI to create sub-categories.~~ **Fixed** (`fix-taxonomy`, `manooch-fronts`).
   Each group row (`CategoryGroupRow.tsx`) now has a "+" action opening `TaxonomyFormModal` with
   target `{ kind: 'create-field', group }`, which posts to
   `POST /admin/store-categories/:id/sub-categories` (no backend change needed — the endpoint
   already worked).

3. ~~Seller-side category edits don't update `Store.categoryId`.~~ **Fixed**
   (`fix-taxonomy`, `manooch-backend` + `manooch-fronts`). `UpdateStoreDto` gained an optional
   `categoryId`; `StoresService.update` resolves it to a `WorkField`, sets `store.categoryId`, and
   mirrors `field.title` into `settings.category` — same pattern as
   `BusinessesService.createOnboarding`. The Info tab's `Dropdown` now selects a `WorkField.id`
   (falling back to resolving a legacy title-only `settings.category` via
   `InfoTab.utils.ts#resolveLegacyCategoryId`) and `Container.tsx`'s `handleSave` sends
   `categoryId` in the store PATCH — including on a category-only change, which previously never
   triggered a store PATCH at all. The settings PATCH (`updateSettings`) no longer sends `category`
   from the client, so it can't race the FK-resolving PATCH and clobber the mirrored title.

4. **New — self-serve registration never sends `categoryId`.** Found while implementing item 3:
   the registration wizard's final step (`manooch-fronts/apps/admin/app/(auth)/working/page.tsx`)
   posts `{ category: data.category }` (free text only) to `POST /admin/onboarding`. In
   `BusinessesService.createOnboarding`, `dto.categoryId` is therefore always `undefined`, so
   `store.categoryId = dto.categoryId ?? null` sets the FK to `NULL` on every self-serve signup —
   only `settings.category` gets populated (via the `dto.category` fallback branch,
   `businesses.service.ts:96-107`). This means a brand-new store already needs the Info tab's
   (now-fixed) `categoryId` PATCH before its FK is populated at all. The admin-driven
   `createStoreForOwner` path (`CreateStoreOnboardingDto`) is unaffected — it has no free-text
   fallback and only accepts `categoryId`. Not fixed here (out of scope for this pass) — would
   need `business-info/page.tsx`'s `categoryOptions` changed to `{ value: f.id, ... }` and
   `working/page.tsx` to send `categoryId` instead of/alongside `category`.
