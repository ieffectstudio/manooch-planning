Looking at the skill-create-component skill, I can identify the natural seams where it splits into genuinely independent concerns. Let me map them first:

1. **Audit** — before touching anything (graphify, duplication check, LSP)
2. **Logic extraction** — domain mapping, hook composition pattern
3. **Asset & token extraction** — fa.ts, icons, tokens, cn()
4. **RTL guard** — already referenced as separate skill
5. **5-file scaffold** — the actual file creation
6. **Architecture patterns** — `_common`, Pattern A/B, page-level rules
7. **Validation** — line gate, output matrix

---

```markdown
---
name: skill-audit-before-build
description: Pre-build auditor — runs graphify orientation, design system duplication check, and LSP typings verification before any component is scaffolded. Must be the first skill invoked in every component pipeline.
---

# Audit Before Build

Run this skill FIRST before any component is created or edited.
No file may be written until all three gates below pass.

---

## Gate 1 — Graphify Orientation

If `graphify-out/graph.json` exists:

```bash
graphify query "<feature/module you're touching>"
graphify path "A" "B"
graphify explain "X"
```

- Read raw source ONLY for files graphify surfaces.
- Do not open directories speculatively.
- Pass the same graphify instruction to any subagents you dispatch.

---

## Gate 2 — Design System Duplication Audit

Scan `front/ui/` before writing any layout.
If the core pattern exists → you are **prohibited** from re-implementing it inline.
If a variant is missing → add it as a configurable prop to the existing component.

| Core Need | Target Component |
|-----------|-----------------|
| Clickable actions / triggers | `front/ui/Button/` — `variant: primary\|secondary\|admin\|customer\|link`, `size: sm\|md\|lg`, `fullWidth?` |
| Text / numeric form input | `front/ui/TextInput/` — `size: sm\|md\|lg`, `leadingIcon?`, `icon?`, `inputDir?`, `readOnly?` |
| Multiline textarea | `front/ui/TextArea/` |
| Options picker / select overlay | `front/ui/Dropdown/` — `options: {value,label,icon?}[]`, `size: sm\|md\|lg`, `renderer?` |
| Drawer / bottom sheet / modal | `front/ui/BottomSheet/` — `open`, `onClose`, `title` |
| Vector icons | `front/ui/Icon/` — `type={ICON.*}`, `size?`, `fill?`, `stroke?` |
| OTP blocks | `front/ui/OtpInput/` — `state: default\|error\|success` |
| Phone input | `front/ui/PhoneInput/` — Iran flag prefix, `label?`, `error?`, `hint?` |
| Step progress rail | `front/ui/StepIndicator/` — `total`, `current` |
| Step wizard | `front/ui/StepWizard/` — `steps: readonly string[]`, `current` |
| Checkbox | `front/ui/Checkbox/` — `variant: default\|admin`, `size: sm\|md` |
| Toggle switch | `front/ui/Toggle/` — `size: sm\|md`, `variant: primary\|admin` |
| Radio button | `front/ui/RadioButton/` — `size: sm\|md` |
| Radio card selection | `front/ui/SelectableCard/` — `layout: row\|column` |
| Visual radio indicator | `front/ui/SelectionRadio/` — `checked` only |
| Tab container | `front/ui/TabNav/` — `size: md\|lg` |
| Tab button | `front/ui/TabItem/` — `active`, `onClick`, `size: md\|lg` |
| Color hex picker | `front/ui/ColorPicker/` |
| Image carousel | `front/ui/Carousel/` — `images[]`, `className?` |
| SVG progress ring | `front/ui/CircularProgress/` — `percentage`, `size?`, `strokeWidth?`, `label?` |
| Filterable list | `front/ui/List/` — `items[]`, `isLoading`, `renderItem`, `emptyState` |
| Inline alert | `front/ui/Notification/` — `status: default\|success\|warning\|error`, `fill?`, `showIcon?` |
| Overlay notification | `front/ui/Toast/` — `message`, `status?`, `visible`; exports `useToast()` |
| Video tutorial drawer | `front/ui/TutorialSheet/` — `open`, `onClose`, `title`, `description`, `videoUrl?` |
| Audio record / playback | `front/ui/VoiceRecorder/` — `mode: admin\|pdp`, `value?`, `onChange?` |

**Icon registry pre-check** — before using any `ICON.*` in JSX:

```bash
grep "YOUR_ICON:" front/ui/Icon/Icon.consts.ts
```

If missing: extract SVG paths from the HTML reference and register in `Icon.consts.ts` + `Icon.tsx`.
Never embed a raw `<svg>` block inside a component file.

---

## Gate 3 — LSP Typings Verification

1. Run `LSP references` on `ComponentNameProps` — no identical typing contracts may exist elsewhere.
2. Run `LSP definition` on any component you intend to extend — inherit its exact props contract.
3. After all files are written, run `LSP diagnostics` on every file produced.
   - Every warning or error must be resolved before the task is complete.
   - `// @ts-ignore` and `any` typing are permanently banned.

---

## Pass Criteria

| Gate | Pass condition |
|------|---------------|
| Graphify | Relevant files located; no speculative directory reads |
| Duplication | No existing pattern re-implemented inline; missing variants added to existing component |
| LSP | Zero diagnostics errors across all produced files |

Do not proceed to scaffolding until all three gates show ✓.
```

---

```markdown
---
name: skill-logic-extraction
description: Logic domain auditor — maps every stateful and computational concern in a component to its correct layer (hook, utils, consts) before any JSX is written. Prevents inline business logic, bans the "adjust state during render" anti-pattern, and enforces the orchestrating hook composition model.
---

# Logic Extraction Audit

Run this skill after `skill-audit-before-build` and before writing any JSX.

A component `.tsx` file is a **rendering declaration only**.
The component body must contain nothing except:
1. One orchestrating hook call (or a minimal set of atomic hook calls)
2. One `router` call if navigation is needed
3. Structural JSX referencing hook-returned values

---

## Forbidden Inline Patterns

If any of the following appear directly in a component body, it is a violation:

| Forbidden pattern | Correct destination |
|-------------------|-------------------|
| `useMemo` with business logic | Pure function in `.utils.ts`; called from a hook |
| State initialisation with logic | Pure builder function in `.utils.ts` |
| Multi-line event handlers | Named function inside a domain hook |
| Cart manipulation / quantity math | `useProductCart` hook or equivalent |
| Attribute / variant selection logic | `useAttributeSelection` hook or equivalent |
| Unit toggle + quantity adjustment | `useUnitSelection` hook or equivalent |
| Gallery / image sorting | Pure `sortImages()` in `.utils.ts` |
| `useCallback` wrapping multiple setters | Extract whole handler to the owning hook |
| Inline anonymous multi-statement props | `onClick={() => { doX(); doY(); }}` → named handler from hook |
| "Adjust state during render" pattern | See banned pattern below |

### Banned Pattern — Adjust State During Render

```ts
// ❌ BANNED — causes cascading renders; difficult to trace
const [prev, setPrev] = useState(x);
if (x !== prev) {
  setPrev(x);
  setOther(0);
}
```

**Correct replacement:** use `useEffect` with correct dependencies, or restructure so the derived
reset is owned entirely by the hook that holds that state domain.

```ts
// ✅ Correct — inside the owning hook
useEffect(() => {
  setCartCount(0);
}, [perAddQuantity]);
```

---

## Domain Mapping Checklist

Before writing the component, enumerate every distinct logic domain. Each maps to exactly one destination.

```
□ Navigation / routing         → inline router.back() is fine for single calls;
                                 complex nav sequences → dedicated hook
□ Menu / overlay visibility    → useVisible() always; never useState(false) for toggles
□ Data transformation          → pure functions in .utils.ts; imported by hook or component
□ Attribute / variant selection → useAttributeSelection hook
□ Unit selection + quantity    → useUnitSelection hook
□ Cart line management         → useProductCart hook
□ Gallery preparation          → sortImages() in .utils.ts; called via useMemo in hook
□ Price computation            → computePrice() in .utils.ts; called from hook
□ Out-of-stock derivation      → isOutOfStock() in .utils.ts; called from hook
□ Contact / config assembly    → assembleContact() in .utils.ts; called once in hook
□ Search state                 → useSearch hook
□ Bulk selection               → useSelection hook
□ Form fields                  → useForm hook or React Hook Form; never raw useState per field
```

---

## Layer Definitions

### `.utils.ts` — pure functions only

Zero React imports allowed. If you need `useMemo` or `useCallback`, the code belongs in a hook.

```ts
// ✅ Correct
export const sortImages = (images: ProductImage[]): string[] =>
  [...images]
    .sort((a, b) => a.sortOrder - b.sortOrder)
    .map((img) => img.image?.url ?? img.imageUrl);

export const assembleContact = (
  config: StoreConfig | null,
  store: Store,
): ContactInfo => ({
  phone: config?.supportPhone || store.settings.contactPhone1,
  supportId: config?.supportId ?? undefined,
});
```

### `_common/hooks/use<Domain>.ts` — one concern per file

One logic domain per hook file. Name the hook after its domain.

```ts
// useAttributeSelection.ts — attribute state only
export const useAttributeSelection = (product: Product) => {
  const [selectedAttributes, setSelectedAttributes] = useState<
    Record<string, ProductAttributeValue>
  >(() => buildDefaultAttributeSelection(product));

  const handleSelectAttribute = useCallback(
    (attributeId: string, option: ProductAttributeValue) =>
      setSelectedAttributes((prev) => ({ ...prev, [attributeId]: option })),
    [],
  );

  return { selectedAttributes, handleSelectAttribute };
};
```

```ts
// useUnitSelection.ts — unit toggle + quantity state only
export const useUnitSelection = (product: Product) => {
  const [unitSelections, setUnitSelections] = useState<Record<string, number>>(
    () => buildDefaultUnitSelection(product),
  );

  const handleToggleUnit = useCallback((unit: ProductUnit) => {
    setUnitSelections((prev) => {
      const next = { ...prev };
      if (unit.id in next) delete next[unit.id];
      else next[unit.id] = 1;
      return next;
    });
  }, []);

  const handleUnitQuantityChange = useCallback(
    (unitId: string, quantity: number) =>
      setUnitSelections((prev) => ({
        ...prev,
        [unitId]: Math.max(1, quantity),
      })),
    [],
  );

  return { unitSelections, handleToggleUnit, handleUnitQuantityChange };
};
```

```ts
// useProductCart.ts — cart count + guest cart line mutations only
export const useProductCart = ({
  product,
  selectedAttributes,
  unitSelections,
  isUnitsMode,
}: UseProductCartParams) => {
  const [cartCount, setCartCount] = useState(0);

  const attributeValueIds = useMemo(
    () => Object.values(selectedAttributes).map((a) => a.id).sort(),
    [selectedAttributes],
  );

  const perAddQuantity = useMemo(
    () =>
      isUnitsMode
        ? Object.values(unitSelections).reduce((s, q) => s + q, 0)
        : 1,
    [isUnitsMode, unitSelections],
  );

  useEffect(() => { setCartCount(0); }, [perAddQuantity]);

  const applyCartQuantity = useCallback(
    (multiplier: number) => {
      if (isUnitsMode) {
        for (const [unitId, qty] of Object.entries(unitSelections)) {
          setGuestCartLineQuantity(product.id, [], unitId, qty * multiplier);
        }
      } else {
        setGuestCartLineQuantity(product.id, attributeValueIds, null, multiplier);
      }
    },
    [product.id, isUnitsMode, unitSelections, attributeValueIds],
  );

  const handleAddToCart = useCallback(() => {
    setCartCount(1);
    applyCartQuantity(1);
  }, [applyCartQuantity]);

  const handleIncrement = useCallback(() => {
    setCartCount((prev) => {
      const next = prev + 1;
      applyCartQuantity(next);
      return next;
    });
  }, [applyCartQuantity]);

  const handleDecrement = useCallback(() => {
    setCartCount((prev) => {
      if (prev <= 1) {
        if (isUnitsMode) {
          for (const unitId of Object.keys(unitSelections))
            removeGuestCartLine(product.id, [], unitId);
        } else {
          removeGuestCartLine(product.id, attributeValueIds, null);
        }
        return 0;
      }
      const next = prev - 1;
      applyCartQuantity(next);
      return next;
    });
  }, [isUnitsMode, unitSelections, product.id, attributeValueIds, applyCartQuantity]);

  return { cartCount, handleAddToCart, handleIncrement, handleDecrement };
};
```

### `_common/hooks/use<Feature>.ts` — orchestrating hook

Composes domain hooks. This is the only hook the component calls.

```ts
export const useProductDetail = (
  product: Product,
  config: StoreConfig | null,
  store: Store,
) => {
  const menu = useVisible();
  const { selectedAttributes, handleSelectAttribute } = useAttributeSelection(product);
  const { unitSelections, handleToggleUnit, handleUnitQuantityChange } = useUnitSelection(product);
  const isUnitsMode = product.pricingMode === "units";
  const cart = useProductCart({ product, selectedAttributes, unitSelections, isUnitsMode });

  const images = useMemo(() => sortImages(product.images), [product.images]);
  const price = computeEffectivePrice(product, selectedAttributes, unitSelections);
  const outOfStock = isProductOutOfStock(product, selectedAttributes, unitSelections);
  const contact = assembleContact(config, store);

  return {
    menu,
    images,
    price,
    outOfStock,
    contact,
    isUnitsMode,
    selectedAttributes,
    handleSelectAttribute,
    unitSelections,
    handleToggleUnit,
    handleUnitQuantityChange,
    ...cart,
  };
};
```

---

## State Management Rules

### `useVisible` Mandate

Any boolean toggling visibility (bottomsheets, modals, drawers, menus) **must** use `useVisible()`.

```ts
// ❌ Wrong
const [menuOpen, setMenuOpen] = useState(false);

// ✅ Correct
const menu = useVisible();
// menu.isVisible / menu.visible() / menu.invisible() / menu.toggle()
```

### ≥ 3 useState = extract to hook

If a component or hook body would have 3 or more `useState` calls, extract related state into a
named domain hook. Group by concern — one hook per domain.

---

## Hook Placement Rules

| Hook scope | Location |
|-----------|----------|
| Feature-specific | `front/app/admin/<feature>/_common/hooks/hookName.ts` |
| Used by 2+ unrelated features | `front/lib/hooks/hookName.ts` + re-export from `lib/hooks/index.ts` |
| Global / app-wide | `front/lib/hooks/` |

**Promote, don't cross-import.** When a hook written for one feature is needed by an unrelated
feature, move it to `front/lib/hooks/` — do not import across two features' `_common/` folders.

---

## Pass Criteria

Before proceeding to scaffold:

```
□ Every logic domain listed and assigned to a hook file or utils function
□ No multi-line handler exists in the component body
□ No useState(false) toggle anywhere (useVisible used instead)
□ No "adjust state during render" pattern
□ No React imports in .utils.ts files
□ Orchestrating hook identified and named
□ Component body will contain only: hook call + router + JSX
```
```

---

```markdown
---
name: skill-asset-extraction
description: Asset and token extractor — enforces out-of-file compilation of all Persian strings, SVG icons, design tokens, and bitmap images before any component JSX is written. Bans inline hex codes, raw SVG blocks, and direct class-merge library imports.
---

# Asset & Token Extraction

Run this skill before writing component JSX.
Every string, icon, color, and image must be registered in its correct workspace location first.

---

## Extraction Targets

| Asset type | Workspace target | Rule |
|-----------|-----------------|------|
| Persian text | `front/messages/fa.ts` | Namespace: `fa.<componentName>.<key>`. No inline Persian. Copy design text verbatim — never append English glosses in parentheses. |
| SVG icons | `front/ui/Icon/Icon.consts.ts` + `Icon.tsx` | Raw `<svg>` blocks inside component JSX are banned. |
| Bitmap images | `front/public/images/` | Use Next.js `<Image>` with explicit sizing, `unoptimized`, and `priority` where above the fold. |
| Design tokens | `front/app/globals.css` `@theme` block | Use Tailwind token names. No hex codes in className. |
| Class merging | `@/lib/cn` | `cn()` is the only allowed merge function. Never import `twMerge`, `clsx`, or `classnames` directly. |
| Per-item runtime colors | `.consts.ts` `Record<string,string>` + inline `style` | Tailwind cannot generate arbitrary classes at runtime. Always include a `DEFAULT_*` fallback. |

---

## Design Tokens

**`@theme` has 463 tokens. Always read `front/app/globals.css` before using any color.
Never write a hex code directly into a `className`.**

### Hand-crafted app tokens

| Token | Tailwind class |
|-------|---------------|
| Primary CTA blue | `bg-primary` / `text-primary` |
| Menu accent | `bg-menu-accent` |
| Menu accent light | `bg-menu-accent-light` |
| Success | `bg-success` |
| Danger | `bg-danger` |
| Danger deep | `bg-danger-deep` |
| Text strong | `text-strong` |
| Text moderate | `text-moderate` |
| Text heading | `text-heading` |
| Text weak | `text-weak` |
| BG main | `bg-bg-main` |
| BG base | `bg-bg-base` |
| BG soft | `bg-bg-soft` |
| Border light | `border-border-light` |
| Input border | `border-input-border` |
| Auth dark | `bg-auth-dark` |
| Notification success | `bg-notification-success` |
| Notification warning | `bg-notification-warning` |
| Notification error | `bg-notification-error` |

### Figma auto-generated tokens

| Pattern | Example | Description |
|---------|---------|-------------|
| `--color-{palette}-{shade}` | `bg-primary-500`, `text-gray-300` | Base palette 0–900 |
| `--color-{palette}-t{N}` | `bg-primary-t20` | Transparency variants |
| `--color-{category}-{state}-{role}` | `bg-bg-default-primary` | Semantic state tokens |
| `--radius-{size}` | `rounded-[var(--radius-md)]` | none / 2xs–3xl / full |
| `--spacing-{size}` | `p-[var(--spacing-xl)]` | none–17xl |
| `--size-{size}` | `w-[var(--size-20xl)]` | 2xs–27xl |
| `--font-size-{h}` | `text-[length:var(--font-size-h1)]` | h1–h6, p, text, small |
| `--leading-{h}` | `leading-[var(--leading-h1)]` | h1–h6, p, text, small |

### SVG fill / stroke

Use CSS variable format in SVG attributes — never hex literals:

```tsx
// ✅ Correct
<path fill="var(--color-menu-accent)" />

// ❌ Wrong
<path fill="#4b45e6" />
```

One-off decorative SVGs unique to a single component (non-standard dimensions, not reusable) may
remain inline but must still use CSS variable fills.

---

## Persian Text Rules

1. All Persian strings live in `front/messages/fa.ts` under `fa.<componentName>.<key>`.
2. Copy design-reference text verbatim.
3. Never append English translations in parentheses — `'همگام سازی بازار (Marketplace)'` is a bug.
4. Import and reference: `import { fa } from '@/messages/fa'` → `{fa.componentName.key}`.

---

## Icon Registration Workflow

Before using any `ICON.*` constant:

```bash
grep "YOUR_ICON:" front/ui/Icon/Icon.consts.ts
```

**If it exists** → use it directly.

**If it is missing**:
1. Extract SVG `<path>` data from the HTML design reference.
2. Add to `Icon.consts.ts`:
   ```ts
   export const ICON = {
     // ... existing
     YOUR_ICON: 'YOUR_ICON',
   } as const;
   ```
3. Add render case to `Icon.tsx`.
4. Use `<Icon type={ICON.YOUR_ICON} />` in the component.

---

## Dynamic Runtime Colors

When a color varies per data item at runtime:

```ts
// ComponentName.consts.ts
export const PLATFORM_COLORS: Record<string, string> = {
  instagram: '#E1306C',
  telegram: '#2AABEE',
  // ...
};
export const DEFAULT_PLATFORM_COLOR = '#737377';
```

```tsx
// ComponentName.tsx
const color = PLATFORM_COLORS[item.type] ?? DEFAULT_PLATFORM_COLOR;

<div style={{ backgroundColor: `${color}33`, color }}>
  {/* '33' suffix = 20% alpha */}
</div>
```

---

## RTL Inline Dividers

For visual separators between inline-flex items, use inline SVG — CSS borders do not render
correctly inside RTL flex rows:

```tsx
<svg width="1" height="16" viewBox="0 0 1 16" fill="none">
  <path d="M0.5 0V16" stroke="var(--color-border-light)" />
</svg>
```

---

## Pass Criteria

```
□ All Persian strings registered in fa.ts under correct namespace
□ All icons confirmed in Icon.consts.ts (grep run, missing ones added)
□ No hex codes in className strings
□ No raw <svg> blocks in component JSX (except one-off decorative shapes with CSS var fills)
□ No twMerge / clsx / classnames imports anywhere
□ Runtime color maps in .consts.ts with DEFAULT_* fallback
□ Bitmap images using Next.js <Image> with sizing + unoptimized
```
```

---

```markdown
---
name: skill-scaffold-five-file
description: 5-file component scaffolder — creates the exact folder structure, enforces layer responsibilities, applies correct import ordering, enforces barrel export rules, and handles routing type safety.
---

# 5-File Component Scaffold

Run this skill after logic extraction and asset extraction are complete.

---

## Folder Structure

```
/ComponentName
├── ComponentName.tsx        ← Display only. Arrow function. Named export. Max 150 lines.
├── ComponentName.consts.ts  ← Immutable config, static data, lookup maps.
├── ComponentName.types.ts   ← TypeScript interfaces. Minimal prop contracts.
├── ComponentName.utils.ts   ← Pure stateless functions. Zero React imports.
└── index.ts                 ← Barrel export only.
```

For components with logic domains, add a hooks layer alongside:

```
/ComponentName
├── ComponentName.tsx
├── ComponentName.consts.ts
├── ComponentName.types.ts
├── ComponentName.utils.ts
├── index.ts
└── _common/
    └── hooks/
        ├── use<DomainA>.ts
        ├── use<DomainB>.ts
        └── use<FeatureName>.ts   ← orchestrating hook
```

---

## Layer Responsibilities — Strict Definitions

### `ComponentName.types.ts`
- TypeScript interfaces and type aliases only.
- Prop interfaces contain the minimum primitives required for rendering.
- No default values, no logic, no imports from React.

```ts
export interface ComponentNameProps {
  readonly variant?: 'primary' | 'secondary' | 'admin';
  readonly isDisabled?: boolean;
  readonly ariaLabel: string;
}
```

### `ComponentName.consts.ts`
- Immutable static data only: style maps, lookup records, label arrays.
- No React imports.
- Runtime color maps belong here with a `DEFAULT_*` fallback.

```ts
import { cn } from '@/lib/cn';

export const COMPONENT_STYLES = {
  base: 'flex items-center gap-2 rounded-lg px-4 py-2',
  variants: {
    primary: 'bg-primary text-white',
    secondary: 'bg-bg-soft text-strong',
    admin: 'bg-auth-dark text-white',
  },
} as const;
```

### `ComponentName.utils.ts`
- Pure functions only: transformations, computations, formatters.
- **Zero React imports.** No `useState`, `useMemo`, `useCallback`, or any hook.
- No side effects.

```ts
export const sortImages = (images: ProductImage[]): string[] =>
  [...images]
    .sort((a, b) => a.sortOrder - b.sortOrder)
    .map((img) => img.image?.url ?? img.imageUrl);
```

### `ComponentName.tsx`
- Display declaration only.
- Arrow function, named export.
- One orchestrating hook call maximum in the component body.
- No business logic, no multi-line handlers, no raw `useState` for toggles.

```tsx
import { cn } from '@/lib/cn';
import { fa } from '@/messages/fa';
import { COMPONENT_STYLES } from './ComponentName.consts';
import type { ComponentNameProps } from './ComponentName.types';

export const ComponentName = ({
  variant = 'primary',
  isDisabled = false,
  ariaLabel,
}: ComponentNameProps) => (
  <div
    className={cn(COMPONENT_STYLES.base, COMPONENT_STYLES.variants[variant])}
    role="region"
    aria-label={ariaLabel}
    aria-disabled={isDisabled}
  >
    {fa.componentName.content}
  </div>
);
```

### `index.ts`
- Barrel exports only. No logic.

```ts
export * from './ComponentName';
export * from './ComponentName.types';
```

---

## Empty Files

When a component genuinely has no consts or utils (pure presentational wrapper), keep the file
present as a **0-byte file** — do not invent placeholder comments or `export {}`.
0-byte files pass tsc/lint cleanly.

---

## Import Ordering (mandatory)

```ts
1. React core hooks and contexts
2. Next.js routing, linking, image optimisation
3. Third-party utilities (Zod, TanStack Query)
4. Application internal hooks and API frameworks (@/hooks, @/lib/api)
5. Workspace shared UI elements (@/ui, @/components)
6. Sibling child sub-components (./SubComponent)
7. Local hooks (./_common/hooks/*)
8. Component consts (./ComponentName.consts)
9. Component types (./ComponentName.types)
```

---

## UI Import Rules

All shared UI components import from the `@/ui` barrel. Never import from sub-paths.
Multiple named imports on a single statement.

```ts
// ✅ Correct
import { Button, TextInput, Dropdown } from '@/ui';

// ❌ Wrong — split imports, wrong path
import { Button } from '@/ui/_common';
import { TextInput } from '@/ui/_common';
```

**Circular import exception — inside `front/ui/` only:**
When a UI component depends on another UI component, import from the direct sub-path, not the barrel.

```ts
// Inside front/ui/ColorPicker/ColorPicker.tsx
import { BottomSheet } from '@/ui/BottomSheet';   // ✅ direct path avoids circular ref
import { Button } from '@/ui/Button';
```

---

## Variant Pattern

When adding context-specific color themes to a UI component:

1. Add `ComponentVariant = 'default' | 'admin'` to `.types.ts`.
2. Add `VARIANT_CLASSES: Record<ComponentVariant, string>` to `.consts.ts`.
3. Apply via `VARIANT_CLASSES[variant]` in `.tsx`.

Do not combine `outline` and `outline-1` in Tailwind v4 — they conflict.
Embed the full outline string in the variant constant: `"outline outline-primary"`.

---

## Routing Rules (typedRoutes is active)

`typedRoutes: true` is on. Every `<Link href>` and `router.push()` is compile-checked.

- Import routes from `@/lib/routes.ts` — never hardcode route strings.
- Template literals in `router.push()` need an `as Route` cast:
  ```ts
  import type { Route } from 'next';
  router.push(`/admin/plugin/product/${id}` as Route);
  ```
- External URLs use `<a>`, not `<Link>`.
- `'use client'` must be the first line — `import type { Route }` goes after.

---

## Accessibility Requirements

- Use semantic HTML5 tags (`<button>`, `<nav>`, `<aside>`, `<main>`) over `<div>`.
- Interactive elements expose: `aria-expanded`, `aria-selected`, `aria-controls`, `aria-live="polite"`.
- Overlay mechanisms handle `Escape` key to close and programmatic focus lock inside modals.

---

## HTML Fidelity Rules

- HTML design is the source of truth.
- Never add `shadow-*`, `border-*`, `outline-*`, `ring-*` absent from the HTML export.
- Reproduce spacing (padding, margin, gap, border-radius, font-weight) verbatim.
- Prefer `@theme` token names over arbitrary values:
  - `gap-4` not `gap-[14px]`
  - `text-xs` not `text-[13px]`
  - `rounded-2xl` not `rounded-[16px]`

---

## `_common` Placement Rules

| Component type | Folder |
|---------------|--------|
| App-wide admin shared | `front/app/admin/_common/` |
| Page-specific section | `front/app/admin/<feature>/_common/SectionName/` |
| Nested sub-block | `front/app/admin/<feature>/_common/SectionName/SubName/` |
| Page-specific list-item row | `front/app/admin/<feature>/_common/RowName/` |

---

## Pass Criteria

```
□ All 5 files created (0-byte if empty, not omitted)
□ .utils.ts has zero React imports
□ index.ts contains only export statements
□ Import order matches the 9-step sequence
□ All UI imports from @/ui barrel (except circular-ref exception inside front/ui/)
□ 'use client' is line 1 in any client component
□ No hardcoded route strings
□ Semantic HTML used for interactive elements
□ No decoration classes absent from HTML design
```
```

---

```markdown
---
name: skill-architecture-patterns
description: Page and feature architecture rule set — defines Pattern A (section composition) and Pattern B (list page), tab nav extraction, sticky CTA placement, list-item memo rules, and the promote rule for shared hooks.
---

# Architecture Patterns

Reference this skill when deciding how to structure a page, feature folder, or repeated list item.

---

## `_common` Folder — Two Canonical Patterns

### Pattern A — Section Composition

Use when the page has **multiple distinct visual sections** (e.g. Header, MenuGrid, ReportRows).

```
page.tsx                          ← imports and composes sections; no business logic
  └─ imports { Header, MenuGrid } from "./_common"

_common/
  index.ts                        ← re-exports all sections
  Header/                         ← 5-file structure
    Header.tsx                    ← may be "use client" if it owns state/data fetch
    ProfileRow/                   ← nested subfolder when section has 3+ visual blocks
    StatBoxes/
  MenuGrid/                       ← 5-file structure
  ReportRows/                     ← 5-file structure
  hooks/
    use<Feature>.ts               ← shared state hook if page.tsx needs cross-section state
```

**Rules:**
- `page.tsx` is lean — composition only.
- State lives at the outermost section that needs it; passed as props downward.
- Data-fetching hooks live inside the section that owns the data, not in `page.tsx`.
- A section exceeding 150 lines → extract visual sub-blocks into nested subfolders (same 5-file rule).

---

### Pattern B — List Page

Use when the page is a **scrollable list with repeated row items**.

```
page.tsx                          ← "use client"; owns state + TanStack mutations + effects
  └─ imports { PluginRow } from "./_common"

_common/
  index.ts                        ← selective barrel
  types.ts                        ← Zod schemas for API validation
  consts.ts                       ← mock data + config constants
  hooks/
    use<Feature>.ts               ← page-level state hook
  PluginRow/                      ← 5-file structure; memo()-wrapped; fully controlled
```

**Rules:**
- `page.tsx` owns ALL state and TanStack Query mutations.
- List-item components (`PluginRow`, `OrderRow`) must be `memo()`-wrapped and fully controlled
  — no internal `useState`.
- `_common/types.ts` = Zod schemas; `_common/consts.ts` = mocks; `_common/hooks/` = hooks.

---

### Pattern B Variant — Tab Nav

When a list page has tabs, the tab nav is a **separate component** in `_common/<Feature>TabNav/`,
never inlined in `page.tsx`.

```
_common/
  consts.ts                       ← defines tab keys + labels
  <Feature>TabNav/
    <Feature>TabNav.tsx
    index.ts
```

```tsx
// <Feature>TabNav.tsx
import { TabItem } from '@/ui/TabItem';
import { TabNav as UITabNav } from '@/ui/TabNav';
import { FEATURE_TABS } from '../consts';
import type { FeatureTab } from '../consts';

export const FeatureTabNav: FC<{
  activeTab: FeatureTab;
  setActiveTab: (k: FeatureTab) => void;
}> = ({ activeTab, setActiveTab }) => (
  <div className="my-3 flex h-12 items-center px-4">
    <UITabNav size="md">
      {FEATURE_TABS.map((tab) => (
        <TabItem
          key={tab.key}
          active={activeTab === tab.key}
          onClick={() => setActiveTab(tab.key)}
          size="md"
        >
          {tab.label}
        </TabItem>
      ))}
    </UITabNav>
  </div>
);
```

`page.tsx` places `<FeatureTabNav>` **outside** the main `px-4` content container.

---

## List-Item Component Rules

Any repeated row component (`PluginRow`, `OrderRow`, `ProductRow`) must:

1. **Be `memo()`-wrapped:**
   ```ts
   export const PluginRow = memo(({ ... }: PluginRowProps) => { ... });
   ```
2. **Be fully controlled** — no internal `useState`; all state from props; all actions via callbacks.
3. **Use RTL-native styling** — `justify-end`, `items-start`, `text-right`; no `dir` overrides.
4. **Live in local `_common/`** with full 5-file structure.

---

## Sticky Bottom CTA on Admin Pages

`front/app/admin/layout.tsx` renders `AdminBottomNav` at `fixed bottom-0 z-50` on every
`/admin/*` route. A naive `fixed inset-x-0 bottom-0` CTA renders underneath it — clicks are
intercepted by the nav bar even though tsc/build/lint pass clean.

**Always use the established pattern:**

```tsx
<div className="fixed bottom-16 left-1/2 w-full max-w-mobile-lg -translate-x-1/2 bg-linear-to-t from-bg-main to-transparent px-4 pt-8 pb-4">
  <Button variant="admin" onClick={handleSubmit} className="w-full">
    {fa.feature.submitLabel}
  </Button>
</div>
```

`bottom-16` clears the nav bar height. No `z-50` needed.

---

## Hook Placement and the Promote Rule

| Scope | Location |
|-------|----------|
| Feature-specific | `front/app/admin/<feature>/_common/hooks/hookName.ts` |
| Shared across 2+ unrelated features | `front/lib/hooks/hookName.ts` |
| App-wide | `front/lib/hooks/` |

**Promote, don't cross-import.**
When a hook first written for one feature is needed by an unrelated feature, move it to
`front/lib/hooks/` and re-export from `lib/hooks/index.ts`.
Never import from one feature's `_common/` into another feature's folder.

---

## Refactor Rule

When touching any admin module whose `_common` folder does not follow Pattern A or B,
refactor it to the correct pattern as part of that same task.

---

## Performance Rules

- **CLS prevention:** Interactive structures (modals, buttons, menus) must have explicit dimension
  definitions or aspect ratios to avoid layout shifts during hydration.
- **No inline allocations in loops:** Never declare inline arrow functions or pass un-memoized
  object literals as props inside iteration. Use `useCallback` or precompute in `.utils.ts`.
- **Render isolation:** Heavy animations or high-frequency input streams must be isolated in
  lightweight local hooks — never cause parent re-renders.

---

## Pass Criteria

```
□ Page structure matches Pattern A or Pattern B
□ Tab nav extracted to its own component (not inlined in page.tsx)
□ Repeated row components are memo()-wrapped and fully controlled
□ Sticky CTA uses bottom-16 pattern, not fixed bottom-0
□ No cross-feature _common imports
□ Any touched module that violated patterns has been refactored
```
```

---

```markdown
---
name: skill-line-gate
description: 150-line gatekeeper — counts every line in every produced file, defines the split decision tree per file type, and fires during construction not only at the end.
---

# 150-Line Gatekeeper

Apply this skill continuously during construction — not only at the end.
The 150-line limit applies to **every file without exception**: `.tsx`, `.ts`, hooks, utils, types, consts.

---

## What Counts as a Line

Every line increments the counter:

```
✓ import statements
✓ blank lines
✓ inline type annotations
✓ JSX markup (each tag on its own line = 1)
✓ comment lines
✓ closing braces / parentheses on their own line
✓ export statements
```

---

## Warning Threshold

When **any file approaches 120 lines**, immediately apply the correct split.
Do not wait until 150 — the warning fires at 120.

---

## Split Decision Tree

```
File type              Approaching 120 lines?   Action
──────────────────────────────────────────────────────────────────────
Component .tsx         Yes                      1. Extract a logic domain into a hook first.
                                                2. If still over after extraction, split JSX
                                                   into a named child component in a subfolder.

Hook file              Yes                      Split into two focused hooks by sub-domain.
                                                Compose them in a parent orchestrating hook.

Utils file             Yes                      Split by domain:
                                                  cart.utils.ts / gallery.utils.ts

Types file             Yes                      Split by domain:
                                                  cart.types.ts / gallery.types.ts

Consts file            Yes                      Split by domain:
                                                  cart.consts.ts / display.consts.ts
```

---

## The Gate Fires During Construction

When adding a new visual block (price section, CTA variant, badge, thumbnail, new state) to an
existing component:

1. Check the current line count **before committing the edit**.
2. If the addition pushes any file past 120 lines, extract the new block into a sibling subfolder
   **in the same change** — not in a follow-up task.
3. Move any associated `.utils.ts` / `.consts.ts` with the extracted block.
4. Delete the now-orphaned source files. Git records it as a rename.

---

## Canonical Violation and Fix

```
❌ VIOLATION
ProductDetailClient.tsx — 195 lines containing:
  • 4 useState calls with initialisation logic
  • 6 useMemo calls with business computations
  • 8 handler functions
  • "adjust state during render" anti-pattern
  • Inline cart line manipulation
  • Image sorting pipeline

✅ FIX — extract into:
  _common/hooks/useAttributeSelection.ts
  _common/hooks/useUnitSelection.ts
  _common/hooks/useProductCart.ts
  _common/hooks/useProductDetail.ts   ← orchestrating hook
  ProductDetailClient.utils.ts        ← sortImages, assembleContact

Result: ProductDetailClient.tsx → ~50 lines of pure JSX composition.
```

---

## Child Component Extraction Pattern

When a JSX section is too large to inline but is not a full feature:

```
/ParentComponent
├── ParentComponent.tsx          ← thin; imports and composes children
├── ParentComponent.consts.ts
├── ParentComponent.types.ts
├── ParentComponent.utils.ts
├── index.ts
└── ChildSection/                ← same 5-file rule
    ├── ChildSection.tsx
    ├── ChildSection.consts.ts
    ├── ChildSection.types.ts
    ├── ChildSection.utils.ts
    └── index.ts
```

---

## Output Line Count Report

At the end of every scaffolding task, report the line count for every file produced:

```
ComponentName.tsx              48 lines  ✓
ComponentName.consts.ts        22 lines  ✓
ComponentName.types.ts         14 lines  ✓
ComponentName.utils.ts         31 lines  ✓
index.ts                        2 lines  ✓
_common/hooks/useDomainA.ts    44 lines  ✓
_common/hooks/useDomainB.ts    38 lines  ✓
_common/hooks/useFeature.ts    55 lines  ✓
```

Any file at or above 150 lines is a hard failure — fix before closing the task.

---

## Pass Criteria

```
□ Every produced file counted and reported
□ Zero files at or above 150 lines
□ No file that was approaching 120 lines was left unsplit
□ Extracted child components have their own 5-file structure
□ Orphaned utils/consts deleted after extraction
```
```

---

```markdown
---
name: skill-validate-output
description: Final output validator — runs the complete checklist after all files are written. Covers LSP diagnostics, line counts, RTL compliance, state management hygiene, asset completeness, and architecture pattern conformance.
---

# Output Validation

Run this skill last, after all files are written.
Do not close a task until every item below shows ✓.

---

## 1. LSP Diagnostics

```
□ LSP diagnostics run on every file produced
□ Zero TypeScript errors
□ Zero TypeScript warnings
□ No // @ts-ignore in any file
□ No `any` type in any interface or function signature
```

---

## 2. Line Count Audit

Run a line count on every file. Report the result.

```
□ Every file counted and listed
□ Zero files at or above 150 lines
□ No file approaching 120 lines was left without a documented split decision
```

---

## 3. State Management Hygiene

```
□ No useState(false) used for any toggle or visibility state
□ useVisible() used for every boolean open/close/toggle state
□ No "adjust state during render" pattern (if (x !== prev) { setPrev(x); setOther(0); })
□ No component with 3+ useState calls that wasn't extracted into a hook
□ Every multi-line event handler lives in a named hook, not the component body
```

---

## 4. Logic Separation

```
□ Component .tsx contains only: hook call(s) + router + JSX
□ .utils.ts files have zero React imports
□ No business logic (cart math, price computation, image sorting) in component body
□ Each domain hook addresses exactly one concern
□ Orchestrating hook composes domain hooks and returns a flat API
```

---

## 5. Asset Completeness

```
□ All Persian strings registered in fa.ts under fa.<componentName>.<key>
□ No inline Persian text in any .tsx file
□ All icons confirmed in Icon.consts.ts (grep run)
□ No raw <svg> blocks in component JSX (except decorative one-offs with CSS var fills)
□ No hex codes in className strings
□ No twMerge / clsx / classnames imported directly
□ Runtime color maps in .consts.ts with DEFAULT_* fallback
□ Bitmap images using Next.js <Image> with sizing + unoptimized
```

---

## 6. RTL Compliance

```
□ No flex-row-reverse anywhere
□ No logical CSS properties (ps-, pe-, ms-, me-, start-, end-, border-s-, border-e-, rounded-s-, rounded-e-)
□ Physical Tailwind props used: mr-*, ml-*, pl-*, pr-*, text-right, mr-auto
□ DOM child order is natural reading order (not manually reversed)
□ Fixed/absolute centering uses left-1/2 -translate-x-1/2, not start-* / end-*
□ Directional icons use scale-x-[-1] or rotate-180, not transform hacks
□ Persian text inputs use dir="rtl"; numeric/code inputs use inputDir="ltr" + text-left
```

---

## 7. Architecture Pattern Conformance

```
□ Page follows Pattern A (section composition) or Pattern B (list page)
□ Tab nav extracted to its own component, not inlined in page.tsx
□ Repeated row components are memo()-wrapped and fully controlled
□ Sticky CTA uses bottom-16 pattern, not fixed bottom-0
□ No cross-feature _common imports
□ Any touched module that violated patterns was refactored in this task
```

---

## 8. Import and Routing

```
□ Import order follows the 9-step sequence
□ All UI imports from @/ui barrel (exception: inside front/ui/ itself)
□ Multiple named imports from same module on a single line
□ No hardcoded route strings; all from @/lib/routes.ts
□ router.push() with template literals uses `as Route` cast
□ External URLs use <a>, not <Link>
□ 'use client' is line 1 in every client component
```

---

## 9. Scaffold Completeness

```
□ All 5 files present for every component (0-byte if empty, never omitted)
□ Empty files are 0-byte, not files with export {} or placeholder comments
□ index.ts contains only export statements
□ No orphaned .utils.ts or .consts.ts left after extractions
□ Child component extractions have their own complete 5-file structure
```

---

## Final Report Format

```
## Output Validation Report

### Files produced
ComponentName.tsx              48 lines  ✓
ComponentName.consts.ts        22 lines  ✓
ComponentName.types.ts         14 lines  ✓
ComponentName.utils.ts         31 lines  ✓
index.ts                        2 lines  ✓
_common/hooks/useDomainA.ts    44 lines  ✓
_common/hooks/useFeature.ts    55 lines  ✓

### LSP diagnostics
0 errors · 0 warnings across 7 files ✓

### Logic domains mapped
gallery preparation   → sortImages() in .utils.ts         ✓
attribute selection   → useAttributeSelection hook         ✓
cart management       → useProductCart hook                ✓
orchestration         → useProductDetail hook              ✓

### Assets extracted
fa.productDetail.addToCart     registered in fa.ts         ✓
ICON.CART                      confirmed in Icon.consts.ts ✓

### RTL
No flex-row-reverse · No logical props · Natural DOM order ✓

### All gates
✓ Audit Before Build
✓ Logic Extraction
✓ Asset Extraction
✓ 5-File Scaffold
✓ Architecture Patterns
✓ Line Gate
✓ Output Validation
```
```

---

The seven skills and how they chain:

| Order | Skill | When |
|-------|-------|------|
| 1 | `skill-audit-before-build` | Before touching any file |
| 2 | `skill-logic-extraction` | After audit, before JSX |
| 3 | `skill-asset-extraction` | After logic map, before JSX |
| 4 | `skill-scaffold-five-file` | File creation |
| 5 | `skill-architecture-patterns` | Reference during scaffold |
| 6 | `skill-line-gate` | Continuously during construction |
| 7 | `skill-validate-output` | After all files written |

`skill-guard-rtl` (the existing skill you already have) slots in between steps 3 and 4 — after assets are extracted and before JSX layout is written.