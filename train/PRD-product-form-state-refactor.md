# PRD: Product Form State Management Refactor and Claude Code Skill

| Field | Value |
|---|---|
| Status | Proposed — ready for engineering review |
| Version | 1.0 |
| Date | 2026-08-09 |
| Feature owner | TBD |
| Engineering owner | TBD |
| Target area | Admin product create/edit form |
| Primary implementation | React + TypeScript, `useReducer` + form-local Context |
| Related skill | `.claude/skills/react-form-state/SKILL.md` |

## 1. Executive summary

The current `useProductForm` hook owns field values, pricing rules, stock calculations, upload lifecycle, dirty tracking, payload mapping, and submission. It returns a large bag of values and setter functions that is passed through nested components. This makes the form difficult to understand, test, and safely modify.

This project will:

1. Commit a reusable Claude Code skill for large React form refactors.
2. Refactor product-form source state into a pure `useReducer`.
3. Add a form-local provider so nested sections can consume state and commands without prop drilling.
4. Extract initialization, derived calculations, dirty snapshots, and payload construction into pure functions.
5. Keep uploads, unsaved-change registration, and submission as explicit side effects outside the reducer.
6. Preserve current user-visible and API behavior unless a behavior change is explicitly approved.
7. Add unit and integration tests before removing the old interface.

This is an internal architecture refactor, not a visual redesign and not a move to global application state.

---

## 2. Background and problem statement

### 2.1 Current responsibilities

The existing `useProductForm` hook currently handles all of the following:

- Create/edit mode detection.
- Defaults from `initialData` and `existingImages`.
- Basic fields: title, code, description, audio, and category.
- Inventory fields: stock quantity and unlimited stock.
- Status state.
- Legacy inquiry-pricing migration.
- Pricing mode and price-inquiry behavior.
- Attribute and unit arrays.
- Discount calculation and validation.
- Product, attribute, and unit stock totals.
- Product-price visibility/read-only rules.
- Image tracking, adding, and removing.
- Unsaved-change detection.
- Submit eligibility.
- Submit payload construction.
- Asset-session commit behavior.

### 2.2 Problems

#### A. Too many independent state setters

Related fields can temporarily enter contradictory combinations because updates are spread across independent setters. Business transitions are not represented as named operations.

#### B. Prop drilling

The hook returns a large object containing most form fields and actions. Parent and intermediate components must forward values and setters even when they do not use them.

#### C. Derived logic is mixed with orchestration

Totals, visibility, read-only state, discount calculation, and validity are mixed into the same hook as uploads and submission.

#### D. Submission mapping is difficult to test

Create/edit differences, pending images, removed images, draft units, pricing mode, and stock totals are assembled inside an event handler instead of a pure function.

#### E. Side-effect sequencing is unclear

The current implementation commits pending assets before calling `onSubmit`. If submission can fail, asset lifecycle and form lifecycle may disagree. The exact async contract must be made explicit and tested.

#### F. Business rules are implicit

The following rules are not obvious from the API:

- Whether inquiry is a separate flag or an exclusive pricing mode.
- Whether unit pricing and attribute-based pricing can coexist.
- Whether attributes with all stock values equal to zero own product stock.
- Whether hidden discount state can invalidate submission.
- Whether disabling a section clears its data or only excludes it from the payload.

#### G. The hook is expensive to change safely

A pricing, inventory, upload, or validation change can affect unrelated code. Pure behavior cannot be tested without rendering the hook and mocking its dependencies.

---

## 3. Product goals

### G1. Make form transitions explicit

Represent state changes as typed reducer actions, especially when one user action may affect multiple fields.

### G2. Remove multi-level form prop drilling

Nested form sections must access form state and actions through a provider and guarded hooks.

### G3. Separate source state from derived data

Store only editable/source values. Calculate totals, visibility, read-only state, discount value, stock binding, submit mode, and validity with pure selectors.

### G4. Make payload behavior independently testable

Generate the complete create/edit submission payload with a pure function.

### G5. Keep side effects explicit

The reducer must not call upload/session APIs, `onSubmit`, navigation APIs, timers, or unsaved-change APIs.

### G6. Preserve behavior safely

Use characterization tests and incremental migration. Do not combine this architecture change with unapproved pricing or inventory behavior changes.

### G7. Give Claude Code repeatable project guidance

Commit a project skill that instructs Claude how to analyze and refactor large forms consistently.

---

## 4. Non-goals

This project will not:

- Redesign the Product Form UI.
- Change backend endpoints or database schemas.
- Introduce Redux, Zustand, or another global store for this form.
- Automatically adopt React Hook Form as part of this refactor.
- Rewrite unrelated admin forms.
- Change pricing, inventory, discount, or image business behavior without approval.
- Optimize all Context renders before profiling shows a problem.
- Eliminate every `useState`; controller-only state such as `isSubmitting` may remain local.

React Hook Form can be evaluated as a separate project. The selected implementation for this PRD is React `useReducer` plus form-local Context.

---

## 5. Users and stakeholders

### Primary user

An admin user creating or editing a product. The refactor must not change the expected form behavior.

### Internal users

- Frontend engineers maintaining product forms.
- Reviewers validating pricing and inventory behavior.
- QA engineers testing create and edit flows.
- Engineers using Claude Code to implement future form changes.

### Stakeholders requiring review

- Product/domain owner for pricing and stock rules.
- Backend owner for payload compatibility.
- Frontend owner for architecture and testing.

---

## 6. Success metrics

The refactor is successful when all of the following are true:

1. The form has one reducer-owned source-state object.
2. The reducer contains no side effects.
3. Existing nested sections no longer receive a giant object of form values/setters through multiple levels.
4. No nested section receives raw setter props solely for forwarding.
5. Initialization, selectors, dirty snapshot, and payload building are pure and unit-tested.
6. Create and edit payloads remain compatible with the existing `onSubmit` contract.
7. All current lint, typecheck, and test commands pass.
8. No known regression exists in create, edit, image, pricing, units, attributes, stock, discount, or unsaved-change flows.
9. Failed asynchronous submission does not commit pending assets.
10. The project skill is committed and can be invoked as `/react-form-state`.

Suggested engineering quality target:

- At least 90% branch coverage for reducer, selectors, and payload modules where the repository collects coverage.
- No meaningful input-latency regression in a production-like build.

---

## 7. Required product decisions

The architecture refactor can begin with characterization tests, but these questions must be answered before deliberately changing the related behavior.

| ID | Question | Current behavior inferred from hook | Recommended handling in this PRD |
|---|---|---|---|
| D1 | Is price inquiry an independent flag or a pricing mode? | Legacy `"inquiry"` is migrated to `pricingMode: "simple"` plus `priceInquiry: true`. | Preserve this model in the refactor. Document it. |
| D2 | Can units and priced/stocked attributes coexist? | State allows both; payload may contain units while submitted pricing mode becomes `attributes`. | Preserve current payload initially; domain owner must confirm before enforcing exclusivity. |
| D3 | Do all-zero attribute stocks own product stock? | No. Attribute stock binds only when at least one attribute stock is greater than zero. | Characterize current behavior. Do not change until the domain owner defines a separate “stock managed by attributes” rule. |
| D4 | Can hidden discount state block submission? | Yes, potentially, because validity depends on `showDiscount`, not section visibility. | Treat as a suspected bug. Fix only with approval; otherwise preserve and add a visible validation path. |
| D5 | Does disabling attributes clear them? | No. Values stay in local state but are omitted from submission. | Preserve. |
| D6 | Does leaving unit mode clear units? | No. Values stay in local state but are omitted from relevant payload fields. | Preserve. |
| D7 | What does removing a newly uploaded image do to its tracked asset? | It removes the image from state; cleanup behavior depends on `useSessionAssets`. | Preserve until the session API is inspected. Add cleanup only if the API has an explicit release/untrack operation. |
| D8 | Is `onSubmit` synchronous or asynchronous? | Current hook does not await it. | Expand type to `void | Promise<void>` if compatible, then test both. |

### Decision gate

No reducer action may introduce new exclusivity or clearing behavior until D1–D8 have been reviewed. Suspected bugs should be separate commits from the structural refactor.

---

## 8. Functional requirements

### FR-1: Initial state

The system must provide a pure lazy initializer:

```ts
createProductFormInitialState(input): ProductFormState
```

It must preserve:

- Empty defaults for create mode.
- Existing values for edit mode.
- Legacy inquiry conversion.
- Existing discount-percent derivation.
- Attribute mapping.
- Unit mapping.
- Existing image mapping with `isNew: false`.

The initializer must be used as the third argument to `useReducer` so it runs only for initial reducer construction.

### FR-2: Source state model

`ProductFormState` must contain editable/source values only:

- `title`
- `code`
- `description`
- `audioUrl`
- `categoryId`
- `stockQuantity`
- `unlimitedStock`
- `inactive`
- `pricingMode`
- `priceInquiry`
- `attributesEnabled`
- `price`
- `discountPercent`
- `showDiscount`
- `attributes`
- `units`
- `images`

The following must not be stored in reducer state:

- Stock totals.
- `hasVariantPricing`.
- `priceReadOnly`.
- Visibility values.
- `isStockBound`.
- `boundStockTotal`.
- Submitted pricing mode.
- Derived discount price.
- `canSubmit`.

### FR-3: Reducer actions

The reducer must support typed, discriminated actions for:

- Simple scalar-field changes.
- Pricing mode changes.
- Price inquiry changes.
- Attribute enable/disable changes.
- Attribute collection replacement or domain-level modification.
- Unit collection replacement or domain-level modification.
- Image addition.
- Image removal.
- Explicit form reset when required.

Recommended action names:

```ts
"field/changed"
"pricing/modeChanged"
"pricing/inquiryChanged"
"attributes/enabledChanged"
"attributes/replaced"
"units/replaced"
"images/added"
"images/removed"
"form/reset"
```

Action handling must be exhaustive. Use an `assertNever` helper or the repository's equivalent if supported by lint conventions.

### FR-4: Reducer purity

The reducer must not:

- Track, commit, or discard assets.
- Submit API data.
- Navigate.
- register an unsaved-change guard.
- Read mutable values outside its arguments.
- Mutate arrays or objects from previous state.

### FR-5: Derived metadata

A pure selector must produce the existing calculated values:

```ts
selectProductFormMeta(state): ProductFormMeta
```

`ProductFormMeta` must include at least:

- `attrStockTotal`
- `unitStockTotal`
- `attributesPriced`
- `attributesHaveStock`
- `hasVariantPricing`
- `priceReadOnly`
- `showProductPrice`
- `showDiscountSection`
- `isStockBound`
- `boundStockTotal`
- `submitPricingMode`
- `priceRequired`
- `derivedDiscountPrice`
- `discountValid`
- `canSubmit`

The first implementation must match existing behavior, including edge cases, unless an approved bug-fix commit changes it.

### FR-6: Numeric parsing

Numeric conversion must be centralized in pure helpers instead of repeating `Number(value) || 0`.

The tests must define behavior for:

- Empty string.
- Whitespace.
- Invalid characters.
- Zero.
- Negative values.
- Decimal values where supported.
- Values greater than expected limits.

The initial structural refactor must preserve existing output where the current backend contract depends on it.

### FR-7: Dirty snapshot

A pure function must create the dirty snapshot:

```ts
buildProductFormDirtySnapshot(state): ProductFormDirtySnapshot
```

Requirements:

- Include source values only.
- Represent images with stable identifiers instead of full asset objects.
- Preserve image order if image order is meaningful.
- Exclude calculated metadata.
- Avoid non-serializable or unstable references where possible.

The provider must pass this snapshot to `useDirtySnapshot` and retain `useUnsavedChangesGuard({ isDirty, onDiscard: session.discard })` behavior.

### FR-8: Payload construction

A pure payload builder must construct the complete submission payload:

```ts
buildProductFormSubmitPayload({
  state,
  meta,
  isEdit,
  existingImages,
}): ProductFormSubmitPayload
```

It must preserve:

- Title, code, description, audio, and category.
- Bound stock total versus manually entered stock.
- Unlimited stock.
- Active/inactive status conversion.
- Submitted pricing mode.
- Price inquiry.
- Price string.
- Empty discount price when discount is disabled.
- Derived discount price when discount is enabled.
- Empty attributes when attributes are disabled.
- Units only when pricing mode is `units`.
- `draftUnits` only for create mode with unit pricing.
- Removal of draft-only unit `id`.
- Conversion of nullable draft unit fields to `undefined` where required.
- Pending image assets.
- IDs of existing images removed from the current form.

Payload construction must not commit assets or call `onSubmit`.

### FR-9: Form provider

A form-local `ProductFormProvider` must:

- Create state through `useReducer` and the lazy initializer.
- Calculate metadata from current state.
- Build and register the dirty snapshot.
- Register the unsaved-changes guard.
- Expose state through a guarded state hook.
- Expose dispatch through a guarded dispatch hook.
- Expose side-effecting commands through a guarded commands hook.
- Expose calculated metadata through a guarded metadata hook or the state hook API.

Recommended hooks:

```ts
useProductFormState()
useProductFormDispatch()
useProductFormMeta()
useProductFormCommands()
```

Every hook must throw a clear development error when called outside the provider.

### FR-10: Context layout

At minimum, state and dispatch must use separate contexts so dispatch-only consumers are not subscribed to the state value.

Recommended contexts:

```ts
ProductFormStateContext
ProductFormDispatchContext
ProductFormMetaContext
ProductFormCommandsContext
```

A single giant `{ state, actions, meta }` context is not accepted as the final architecture unless profiling and implementation simplicity are documented in the pull request.

### FR-11: Section consumption

The final form composition must not pass the complete state/action API through intermediate components.

Expected shape:

```tsx
<ProductFormProvider {...props}>
  <ProductFormContent />
</ProductFormProvider>
```

And within content:

```tsx
<GeneralSection />
<PricingSection />
<InventorySection />
<AttributesSection />
<UnitsSection />
<ImagesSection />
<SubmitBar />
```

Sections may still receive true presentation/configuration props, such as layout class names or data not owned by the product form. They must not receive fields and setters merely to forward them.

### FR-12: Image commands

The commands API must expose:

```ts
addImage(asset: Asset): void
removeImage(id: string): void
```

`addImage` must:

1. Track the asset with the existing session API.
2. Add `{ id: asset.id, image: asset, isNew: true }` to state.

`removeImage` must:

1. Remove the image from reducer state.
2. Use an explicit session cleanup API for removed new assets only if such an API exists and current upload semantics approve it.

### FR-13: Submission command

The commands API must expose an async-safe submit operation:

```ts
submit(): Promise<void>
```

Requirements:

- Do not submit when `meta.canSubmit` is false.
- Prevent accidental duplicate submission while pending.
- Build the payload with the pure payload builder.
- Support an `onSubmit` result of `void | Promise<void>` if the calling API can be updated compatibly.
- Commit only the pending images present in the successful payload.
- Do not commit those images after a rejected submission.
- Preserve or rethrow the submit error according to existing project conventions.
- Expose submission pending/error state if required by the current UI.

The required success sequence is:

```text
validate -> build payload -> await onSubmit -> commit submitted asset IDs
```

If repository navigation behavior makes this sequence unsafe, document the conflict and add an integration test before choosing a different sequence.

### FR-14: Create/edit reset behavior

React state initializers do not automatically update when `initialData` changes. The implementation must choose and document one of these contracts:

1. The provider is keyed by product ID and remounts for another product; or
2. A deliberate `form/reset` action runs when the product identity changes.

Do not add an effect that resets the form on every object-reference change.

Recommended default: key the provider by stable product ID when routing already remounts per product.

### FR-15: Compatibility during migration

During migration, the existing `useProductForm` return interface may remain as a compatibility facade. The facade must delegate to reducer state, metadata, and commands rather than maintaining duplicate state.

After all consumers use context, either:

- Rename `useProductForm` to the main guarded context hook; or
- Remove the old facade and update imports in the same final cleanup phase.

There must never be two independent sources of truth.

---

## 9. Non-functional requirements

### NFR-1: Type safety

- No new `any` types.
- Action payloads must be associated with the correct fields.
- Existing domain types (`Asset`, `AttributeAssignment`, `LocalImage`, `PricingMode`, `UnitDraft`, and submit payload types) must be reused rather than duplicated.
- Context hooks must return non-null types.

### NFR-2: Performance

- The refactor must not create an obvious input-latency regression.
- Dispatch identity must remain stable.
- Expensive metadata calculation may use `useMemo`, but correctness must not depend on memoization.
- Do not claim that wrapping one large Context value in `useMemo` prevents consumer rerenders.
- Split section contexts or adopt context selectors only after profiling demonstrates a need.

### NFR-3: Maintainability

- Pure modules should be short and focused.
- Domain action names should describe user intent.
- Comments should explain business reasons, not restate code.
- Avoid a generic abstraction shared with unrelated forms during this PR.

### NFR-4: Accessibility and UX preservation

- Existing labels, error announcements, disabled states, focus behavior, and keyboard behavior must remain unchanged.
- Any newly surfaced submission error must use the existing accessible error pattern.

### NFR-5: Observability

Use existing error reporting for failed submissions. Do not add logging of product descriptions, audio URLs, or other potentially sensitive form content.

---

## 10. Proposed architecture

### 10.1 Target file structure

Adapt names to repository conventions after inspection:

```text
ProductForm/
├── ProductForm.tsx
├── ProductForm.types.ts
├── useProductForm.ts                 # temporary facade or final context hook
├── state/
│   ├── ProductForm.state.ts
│   ├── ProductForm.initialState.ts
│   ├── ProductForm.actions.ts
│   ├── ProductForm.reducer.ts
│   ├── ProductForm.selectors.ts
│   ├── ProductForm.dirtySnapshot.ts
│   ├── ProductForm.payload.ts
│   └── ProductForm.context.tsx
└── sections/
    ├── GeneralSection.tsx
    ├── PricingSection.tsx
    ├── InventorySection.tsx
    ├── AttributesSection.tsx
    ├── UnitsSection.tsx
    ├── ImagesSection.tsx
    └── SubmitBar.tsx
```

The implementation may combine very small files where repository conventions favor fewer modules. It must retain the conceptual boundaries.

### 10.2 State flow

```text
initialData + existingImages
            |
            v
createProductFormInitialState
            |
            v
     useReducer state <--------- typed UI actions
            |
     +------+-------+
     |              |
     v              v
selectors      dirty snapshot
     |              |
     v              v
form sections  unsaved guard
     |
     v
submit command -> payload builder -> onSubmit -> session.commit on success
```

### 10.3 State model

```ts
export interface ProductFormState {
  title: string;
  code: string;
  description: string;
  audioUrl: string | null;
  categoryId: string;
  stockQuantity: string;
  unlimitedStock: boolean;
  inactive: boolean;
  pricingMode: PricingMode;
  priceInquiry: boolean;
  attributesEnabled: boolean;
  price: string;
  discountPercent: string;
  showDiscount: boolean;
  attributes: AttributeAssignment[];
  units: UnitDraft[];
  images: LocalImage[];
}
```

### 10.4 Action model

Simple scalar changes may use a generic action only if field/value correlation remains type-safe. Business transitions must use dedicated actions.

```ts
type ProductFormAction =
  | ScalarFieldChangedAction
  | { type: "pricing/modeChanged"; mode: PricingMode }
  | { type: "pricing/inquiryChanged"; value: boolean }
  | { type: "attributes/enabledChanged"; value: boolean }
  | { type: "attributes/replaced"; attributes: AttributeAssignment[] }
  | { type: "units/replaced"; units: UnitDraft[] }
  | { type: "images/added"; image: LocalImage }
  | { type: "images/removed"; id: string }
  | { type: "form/reset"; state: ProductFormState };
```

### 10.5 Context API

```ts
interface ProductFormCommands {
  addImage(asset: Asset): void;
  removeImage(id: string): void;
  submit(): Promise<void>;
}

function useProductFormState(): ProductFormState;
function useProductFormDispatch(): Dispatch<ProductFormAction>;
function useProductFormMeta(): ProductFormMeta;
function useProductFormCommands(): ProductFormCommands;
```

Submission-only state may be exposed separately:

```ts
interface ProductFormSubmissionState {
  isSubmitting: boolean;
  error: unknown | null;
}
```

### 10.6 Provider responsibilities

The provider is a controller, not a second reducer. It owns:

- Reducer creation.
- Metadata calculation.
- Dirty snapshot registration.
- Session-backed image commands.
- Submission orchestration.
- Context composition.

It does not duplicate form fields in `useState`.

---

## 11. Claude Code skill requirements

### 11.1 Installation

Commit this file to the project:

```text
.claude/skills/react-form-state/SKILL.md
```

The skill must contain YAML frontmatter with:

```yaml
---
name: react-form-state
description: Refactor large React and TypeScript forms with many useState calls, prop drilling, duplicated derived state, or tangled submit logic. Use for deciding between local state, useReducer plus Context, and React Hook Form, and for implementing a form-local provider without changing behavior.
---
```

### 11.2 Skill behavior

The committed skill must instruct Claude to:

- Inspect state, derived data, side effects, payload behavior, and invariants before editing.
- Avoid replacing every `useState` mechanically.
- Choose `useReducer` only for cohesive or transition-heavy state.
- Use Context only for genuinely shared nested state.
- Keep the reducer pure.
- Extract selectors and payload generation.
- Preserve behavior with characterization tests.
- Commit assets only after successful async submission.
- Avoid global state without a cross-page requirement.
- Profile Context behavior before optimization.

### 11.3 Skill verification

The implementation PR must verify that:

1. The file is tracked by Git.
2. YAML frontmatter is valid.
3. Claude Code lists or recognizes the skill.
4. `/react-form-state` can be invoked from the repository.
5. The skill does not contain project secrets or environment-specific credentials.

Official reference: https://docs.anthropic.com/en/docs/claude-code/slash-commands

### 11.4 Optional repository guidance

If the repository has a root `CLAUDE.md`, add only a short pointer rather than duplicating the complete skill:

```md
For large React form state refactors, use the `/react-form-state` skill. Preserve behavior with characterization tests before replacing state architecture.
```

---

## 12. Migration plan

The work must be split into reviewable phases. Each phase must leave the project type-safe and testable.

### Phase 0: Repository inspection and behavior inventory

Tasks:

1. Locate `useProductForm`, `ProductForm.types`, all direct consumers, and nested prop-forwarding components.
2. Inspect `useSessionAssets`, `useDirtySnapshot`, and `useUnsavedChangesGuard` contracts.
3. Inspect the `onSubmit` type and every caller.
4. Identify existing test framework and commands.
5. Record current create/edit payloads for representative scenarios.
6. Resolve or explicitly defer D1–D8.

Exit criteria:

- A dependency map is attached to the PR description or engineering notes.
- Current behavior is documented.
- No production code has been behaviorally changed.

### Phase 1: Add the Claude Code skill

Tasks:

1. Add `.claude/skills/react-form-state/SKILL.md`.
2. Add the optional root `CLAUDE.md` pointer if the repository uses it.
3. Verify invocation.

Exit criteria:

- Skill is recognized and committed.
- Skill content matches project conventions.

### Phase 2: Add characterization tests

Add tests around current behavior before moving logic.

Required scenarios:

- Empty create defaults.
- Fully populated edit defaults.
- Legacy inquiry conversion.
- Existing discount conversion to a rounded percentage.
- Basic simple pricing.
- Price inquiry.
- Unit pricing.
- Attributes with prices.
- Attributes with positive stock.
- Attributes with all-zero stock.
- Discount boundaries.
- Existing, new, and removed images.
- Create versus edit draft units.

Exit criteria:

- Tests document current output, including any intentionally preserved odd behavior.

### Phase 3: Extract pure functions

Tasks:

1. Add `createProductFormInitialState`.
2. Add numeric parsing helpers.
3. Add `selectProductFormMeta`.
4. Add `buildProductFormDirtySnapshot`.
5. Add `buildProductFormSubmitPayload`.
6. Update the existing hook to call these functions while retaining its return API.

Exit criteria:

- Existing UI behavior and hook interface are unchanged.
- Pure functions have focused unit tests.
- No duplicated calculation remains in the hook.

### Phase 4: Introduce the reducer

Tasks:

1. Define `ProductFormState` and typed actions.
2. Implement the pure reducer.
3. Replace field-level `useState` calls with one `useReducer`.
4. Keep compatibility setter wrappers temporarily where consumers still expect them.
5. Add reducer unit tests.

Exit criteria:

- Reducer is the only source of form field state.
- Existing consumers still work.
- No reducer side effects exist.

### Phase 5: Add provider and guarded hooks

Tasks:

1. Add state, dispatch, metadata, and commands contexts.
2. Add `ProductFormProvider`.
3. Move dirty guard registration and session commands into the provider/controller.
4. Add tests for hooks used outside and inside the provider.

Exit criteria:

- Provider can render the current form without behavior changes.
- Guarded hooks return typed non-null values.

### Phase 6: Remove prop drilling section by section

Recommended migration order:

1. Submit bar.
2. Images section.
3. General fields.
4. Inventory.
5. Pricing and discount.
6. Attributes.
7. Units.

For each section:

- Replace forwarded state/setter props with guarded context hooks.
- Keep true presentation props.
- Run typecheck and relevant tests.
- Do not migrate multiple high-risk pricing sections in one unreviewable change.

Exit criteria:

- Intermediate components no longer forward product-form values/actions.
- Form composition is section-oriented.

### Phase 7: Harden submission and asset lifecycle

Tasks:

1. Make submission async-safe.
2. Prevent duplicate submit.
3. Commit only after successful submission.
4. Confirm navigation does not unmount before required asset operations complete.
5. Confirm failed submit leaves assets recoverable and form dirty.
6. Confirm discard behavior removes uncommitted assets according to session semantics.

Exit criteria:

- Integration tests cover submit success and failure.
- Asset-session calls occur in the approved order.

### Phase 8: Cleanup

Tasks:

1. Remove compatibility setters and the old giant return object.
2. Remove dead imports and duplicate types.
3. Rename hooks/files to final conventions.
4. Run formatter, lint, typecheck, unit tests, and integration tests.
5. Perform manual regression testing.

Exit criteria:

- No duplicate state path exists.
- No stale compatibility API remains unless explicitly documented.
- Definition of Done is satisfied.

---

## 13. Detailed test plan

### 13.1 Initial-state unit tests

| Case | Expected result |
|---|---|
| Create with no initial data | Empty strings/default booleans, stock `"0"`, simple pricing, no arrays |
| Edit active product | `inactive === false` |
| Edit inactive product | `inactive === true` |
| Legacy inquiry mode | State mode is `simple`, inquiry flag is true |
| Attribute pricing mode | Attributes enabled and mode normalized as current behavior requires |
| Existing discount | Percentage is rounded using existing formula |
| Existing units | IDs and nullable/default fields map correctly |
| Existing images | `isNew` is false and asset/image reference is preserved |

### 13.2 Reducer unit tests

- Every scalar field action updates only its target field.
- Pricing mode transition preserves or changes related fields exactly as approved.
- Inquiry transition preserves or changes discount values exactly as approved.
- Attribute and unit replacement does not mutate previous state.
- Image add appends a new image.
- Image removal removes only the matching ID.
- Reset returns the provided state.
- Unknown actions are impossible at compile time or handled exhaustively.

### 13.3 Selector unit tests

| Scenario | Required assertion |
|---|---|
| Blank title | Cannot submit |
| Simple pricing with blank/zero price | Cannot submit when price is required |
| Valid simple price | Can submit when other validation passes |
| Price inquiry | Product price hidden and requirement follows approved behavior |
| Unit mode | Product price hidden |
| Attribute has price | Product price is read-only and submitted mode is attributes |
| Attribute has positive stock | Attribute total and stock binding are correct |
| All attribute stock is zero | Match approved D3 behavior |
| Units exist | Unit stock total and stock binding are correct |
| Discount disabled | Empty/invalid percent does not matter |
| Discount enabled with 0 | Invalid |
| Discount enabled with 1 | Valid |
| Discount enabled with 99 | Valid |
| Discount enabled with 100 | Invalid |
| Hidden discount section | Match approved D4 behavior |
| Price 100, discount 10 | Derived discount price is 90 |
| Rounding case | Matches current `Math.round` result |

### 13.4 Payload unit tests

- Manual product stock is used when stock is not bound.
- Derived stock total is stringified when stock is bound.
- Status maps to `active`/`inactive`.
- Submitted pricing mode matches selector output.
- Discount price is empty when disabled.
- Attributes are empty when disabled.
- Units are empty unless mode is `units`.
- Create/unit mode produces `draftUnits` without draft IDs.
- Edit mode produces no `draftUnits`.
- Existing retained images are not pending.
- New retained images are pending.
- Removed existing image IDs are included.
- Removed new image IDs are not included as existing removals.

### 13.5 Provider integration tests

- A nested field reads state without form props.
- Dispatching an input action updates the rendered field.
- A component outside the provider receives the expected guarded-hook error.
- Adding an image calls `session.track` once and updates state.
- Removing an image updates state.
- Dirty state reaches the unsaved-change guard.
- Discard delegates to `session.discard`.
- Invalid form does not call `onSubmit`.
- Valid synchronous submit calls `onSubmit`, then commits.
- Valid asynchronous submit commits only after resolution.
- Rejected submit does not commit.
- Repeated clicks while pending submit once.

### 13.6 Manual regression matrix

Test create and edit flows for:

- Simple price, no discount.
- Simple price with discount.
- Price inquiry.
- Unit pricing with multiple units.
- Attributes with prices.
- Attributes with inventory.
- Unlimited stock.
- Active/inactive status.
- Adding/removing multiple images.
- Removing an existing image.
- Navigating away with dirty changes.
- Discarding changes.
- Failed and successful submission.

Verify the exact network payload in browser developer tools or mocked integration assertions.

---

## 14. Acceptance criteria

### Architecture

- [ ] `.claude/skills/react-form-state/SKILL.md` is committed and valid.
- [ ] Product form field state is owned by one reducer.
- [ ] Reducer, initializer, selectors, dirty snapshot, and payload builder are separate pure concerns.
- [ ] Reducer contains no side effects.
- [ ] Provider is local to the Product Form subtree.
- [ ] State and dispatch use separate contexts.
- [ ] Guarded context hooks throw clear errors outside the provider.
- [ ] No global store is introduced.

### Prop drilling

- [ ] Nested sections no longer receive a giant collection of form fields and setters.
- [ ] Intermediate components do not forward form state they do not use.
- [ ] Presentation/configuration props remain explicit.

### Behavior

- [ ] Create defaults match existing behavior.
- [ ] Edit initialization matches existing behavior.
- [ ] Legacy inquiry behavior is preserved.
- [ ] Pricing, discount, attributes, units, and stock outputs match approved rules.
- [ ] Pending and removed image payloads are correct.
- [ ] Create/edit `draftUnits` behavior is preserved.
- [ ] Dirty and discard behavior is preserved.

### Submission

- [ ] `canSubmit` is computed by a selector.
- [ ] Invalid forms do not submit.
- [ ] Duplicate submission is prevented.
- [ ] Successful submission commits only submitted pending assets.
- [ ] Failed submission does not commit pending assets.
- [ ] Existing navigation behavior still works.

### Quality

- [ ] Typecheck passes.
- [ ] Lint passes.
- [ ] Formatter passes.
- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] Manual regression matrix is complete.
- [ ] No unapproved backend payload changes exist.

---

## 15. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Hidden behavior changes during extraction | High | Characterization tests first; separate structural and bug-fix commits |
| Context causes broad rerenders on each keystroke | Medium | Separate dispatch context; profile; split by section only if needed |
| `initialData` changes without remounting | High | Key provider by product ID or implement explicit reset contract |
| Asset commit order conflicts with navigation | High | Inspect caller and guard behavior; add success/failure/navigation integration tests |
| All-zero attribute stock semantics are changed accidentally | High | Preserve current selector first; resolve D3 separately |
| Generic field action weakens TypeScript safety | Medium | Use mapped discriminated types or typed action creators; dedicated domain actions for coupled fields |
| Compatibility facade lives permanently | Medium | Add removal task and acceptance criterion |
| Large PR is difficult to review | High | Land phases as small commits/PRs with green tests |
| New provider becomes another monolith | Medium | Keep pure modules separate; expose narrow guarded hooks |
| Stale closure in submit command | Medium | Correct callback dependencies; integration test latest state submission |

---

## 16. Rollout and rollback

### Rollout

- No feature flag is required if behavior remains unchanged.
- Prefer a sequence of small pull requests or clearly separated commits following the migration phases.
- Deploy through the normal admin frontend release process.
- Monitor submission errors and asset-upload cleanup failures after release.

### Rollback

- There is no data migration.
- Roll back the refactor commits if a production regression appears.
- Preserve the old public hook interface until provider migration is complete to make rollback lower risk.

---

## 17. Suggested pull request sequence

### PR 1: Skill and characterization

- Add the Claude Code skill.
- Add behavior inventory and characterization tests.
- No production behavior changes.

### PR 2: Pure extraction

- Add initializer, selectors, dirty snapshot, and payload builder.
- Make the current hook delegate to them.

### PR 3: Reducer migration

- Replace field `useState` calls with `useReducer`.
- Keep compatibility return API.

### PR 4: Provider and prop-drilling removal

- Add contexts and guarded hooks.
- Migrate sections incrementally.

### PR 5: Submission hardening and cleanup

- Make submit async-safe.
- Validate asset sequencing.
- Remove compatibility API and dead code.

If the repository prefers one PR, use the same sequence as separately reviewable commits.

---

## 18. Claude Code execution instructions

### Initial invocation

From the project root:

```text
/react-form-state
```

Then provide Claude this instruction:

```text
Implement the Product Form state refactor described in
`docs/PRD-product-form-state-refactor.md`.

Work incrementally and do not change business behavior unless the PRD marks the
change approved. First inspect the repository and report:
1. all consumers of useProductForm,
2. the ProductFormProps and onSubmit contracts,
3. useSessionAssets behavior,
4. dirty/unsaved guard behavior,
5. available tests and package commands,
6. unresolved decisions D1-D8.

Do not edit production code until the behavior map and characterization-test
plan are complete. After approval, implement one PRD phase at a time. Run the
smallest relevant tests, typecheck, and lint after each phase. Keep the reducer
pure and never create a second source of truth.
```

### Phase-by-phase prompt pattern

```text
Use `/react-form-state` and implement only Phase N from the Product Form PRD.
Show the files you expect to modify and list behavior that must remain
unchanged before editing. After implementation, run relevant tests and report:
- changed files,
- preserved behavior,
- tests run,
- unresolved risks,
- next phase.
```

### Review prompt

```text
Use `/react-form-state` to review this refactor against the PRD. Look for:
- reducer side effects,
- duplicated source state,
- derived values stored in state,
- hidden prop drilling,
- unsafe Context usage,
- incorrect create/edit payload differences,
- stale submit closures,
- asset commit before successful submit,
- reset bugs when initialData changes,
- untested pricing, discount, stock, unit, attribute, and image edge cases.
Do not rewrite code until you first provide findings ordered by severity.
```

---

## 19. Definition of Done

The work is done when:

1. Every acceptance criterion is checked.
2. Required product decisions are resolved or explicitly preserved as current behavior.
3. The form uses reducer state and local Context in production.
4. Nested prop drilling for form state/actions is removed.
5. Pure behavior has adequate automated coverage.
6. Successful and failed submit/asset sequences are verified.
7. Create and edit manual regression checks pass.
8. The old duplicate state path and compatibility API are removed or intentionally documented.
9. The skill is committed and usable by the team.
10. Engineering and product/domain owners approve the pull request.
