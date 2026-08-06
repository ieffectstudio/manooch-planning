# Business Category CRUD — Full Detailed Explanation

> **Verified against:** `manooch-backend` and `manooch-fronts` (portal + admin apps), 2026-08-06.
> Every claim below is traceable to a file cited inline.

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
| **Parent** | Not selectable in the UI. `PageClient.tsx` only ever opens the form with target `create-group` — there is **no "add sub-category" action wired up in the portal**, even though the backend endpoint for it exists and works (see §7, gap 1). |

Create paths (backend):
- `POST /admin/store-categories` — new group, `CreateStoreCategoryDto` (`code` required).
- `POST /admin/store-categories/:id/sub-categories` — new field under group `:id`,
  `CreateStoreSubCategoryDto` (no `code`). Reachable via the API/Swagger, not via the current
  portal UI.

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
- Both build their options the same way: `workGroups.flatMap(g => g.fields.map(f => ({ value:
  f.title, label: f.title })))` — the picker lists sub-categories (`WorkField.title`) only, never
  top-level groups (`InfoTab.tsx:39-41`, `business-info/page.tsx:50-52`).

### 3.3 Known Issue — Missing `searchable` Prop

> **The Info tab's `Dropdown` omits the `searchable` / `searchPlaceholder` props that registration
> passes.**

- Registration: `<Dropdown ... searchable searchPlaceholder={fa.auth.businessInfo
  .categorySearchPlaceholder} ... />` (`business-info/page.tsx:159-170`).
- Info tab: `<Dropdown ... />` with no `searchable` prop (`InfoTab.tsx:93-102`).
- Net effect matches the original observation — sellers editing an existing store must scroll the
  full unfiltered list — but the fix is a one-line prop addition to an existing shared component,
  not new search functionality to build from scratch.

### 3.4 Comparison: Registration vs. Admin Business Info

| Feature | Registration Business Info | Admin Business Info Tab |
|---|---|---|
| **Component** | `Dropdown` (`@/ui`) | Same `Dropdown` (`@/ui`) |
| **`searchable` prop** | ✅ passed | ❌ not passed |
| **User** | New business registering | Existing seller editing their store |
| **Options source** | `WorkField.title` list (identical query/shape) | Same |

**Recommendation:** Add `searchable` + `searchPlaceholder` to the `Dropdown` call in `InfoTab.tsx`
to match registration — this is the fix, not a larger UX redesign.

---

## 4. Summary of Key Rules & Constraints

| Rule | Description |
|---|---|
| **Code is admin-authored** | The `code` field on a `WorkGroup` is typed by the admin, uppercased, and validated against `^[A-Z0-9_]+$` (max 50 chars). |
| **Code is editable** | Editable on both create and update; a change is checked for uniqueness among live rows and 409s on collision. |
| **Sub-categories have no code** | `WorkField` carries no `code` column or DTO field. |
| **Two-table nesting** | `WorkGroup` → `WorkField` via a required `workGroupId` FK. No self-referencing parent column exists, so no deeper nesting is representable. |
| **No re-parenting** | A field's `workGroupId` is fixed at creation (by which route created it) and cannot be changed via the update DTO. |
| **Portal can't create sub-categories** | The creation UI only supports groups; the working sub-category endpoint has no portal entry point. |
| **Soft delete only, no usage guard** | Deleting a group cascades a soft-delete to its fields; any store referencing an affected field has its `categoryId` set to `NULL` automatically — deletion is never blocked. |
| **Seller field lags the FK** | The Info tab's category `Dropdown` writes `settings.category` only; it never sends `categoryId`, so `Store.categoryId` is not updated when a seller changes category post-registration (see §7, gap 2). |
| **Missing search prop** | The Info tab's `Dropdown` doesn't pass `searchable`, unlike the registration flow's identical component. |

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
│  2. Sub-category (WorkField) creation is API-only               │
│     → POST /admin/store-categories/:id/sub-categories works    │
│       but has no button in the portal UI                       │
│  3. Admin can view/edit (incl. code)/soft-delete groups & fields│
│     → deletion never blocked by stores referencing the field    │
└──────────────────────────┬──────────────────────────────────────┘
                            │  WorkGroup.fields → WorkField
                            ▼
┌───────────────────────────────────────────────────────────────┐
│              ADMIN — Business Info Tab (Seller)                 │
│                                                                 │
│  1. Registration: resolves categoryId → WorkField                │
│     → sets Store.categoryId (FK) AND mirrors title into          │
│       Store.settings.category                                   │
│  2. Info tab edit: Dropdown (no `searchable`) writes ONLY        │
│       Store.settings.category — Store.categoryId is never sent   │
│     → ⚠ FK can go stale after a post-registration category change│
└───────────────────────────────────────────────────────────────┘
```

---

## 7. Open Issues / Action Items

1. **Add `searchable` to the Info Tab's category `Dropdown`.** One-prop fix in
   `manooch-fronts/apps/admin/app/business/_common/InfoTab/InfoTab.tsx` to match
   `app/(auth)/business-info/page.tsx`, restoring search parity for sellers editing an existing
   store.

2. **Portal has no UI to create sub-categories.** The backend endpoint (`POST
   /admin/store-categories/:id/sub-categories`) is fully implemented and tested but unreachable
   from `PageClient.tsx` — decide whether to add the "add sub-category" action to the portal, or
   whether sub-categories are intentionally seed-only (`WORK_FIELDS_DATA`).

3. **Seller-side category edits don't update `Store.categoryId`.** Only `settings.category`
   (a title string) is written by the Info tab; the FK to `WorkField` is left pointing at
   whatever was set during registration (or `NULL` if never set). Decide whether the Info tab's
   save path should resolve the selected title back to a `WorkField.id` and include `categoryId`
   in the PATCH, mirroring what `businesses.service.ts`'s onboarding path already does.
