# Customer Club — §1 structural conversion, remaining work

This tracks what the `fix-feat-customer-club` branch (manooch-fronts) did **not** convert to
the repo's frontend style guide, per `19-8/bugs.md` §1's staged-scope decision. Everything
listed here still works — it wasn't broken by this branch — it just doesn't yet match the
`stock`/`discounts` module anatomy (5-file component folders, `@/ui` primitives, `fa.ts`
strings, `--color-club-*` tokens instead of raw hex).

Snapshot taken before this branch started; some counts (files converted, icons registered,
`ClubIcons`/`ClubNavIcons`/`QuickSetupIcons` deletion) will have already dropped once
`fix-feat-customer-club` lands — cross-check against the branch diff before re-scoping this
list, don't take these numbers as current.

## What this branch converted

- Module shell: `ClubTabBar`, `ClubFab`, `HeroCard`, `QuickActionsRow`, `WalkInKeypadSheet`,
  `QuickSetupSheet` → 5-file folders.
- `ClubAppBar` deleted; all 23 non-dashboard pages render `AdminTopBar` directly (via a shared
  `ClubPageTopBar` wrapper — confirm this landed as a proper 5-file component, not a bare
  function, when reviewing the branch).
- `ClubIcons.tsx` / `ClubNavIcons.tsx` / `QuickSetupIcons.tsx` deleted; their icons registered
  in `packages/ui`'s shared `ICON` registry (19 new keys, 4 more deduped onto existing keys —
  see the branch's Phase 1/Phase 2 commits for the exact mapping).
- `useScrollCollapse` + `CollapsibleHeader` promoted to `packages/ui`; wired into all three
  dashboards (storefront, seller/admin, customer-club).
- Routes for the 5 tab-bar targets centralized into `apps/admin/lib/routes.ts`.
- `CustomerClubCard` (admin home) and the seller-dashboard stat tiles restyled/tokenized.

## Not converted — by subtree

Counts are from the pre-branch snapshot (19/08). Re-audit with `fallow check` before treating
this as authoritative.

### `campaigns/` (20 files)
`campaigns/page.tsx` (353 lines — over the 150-line gate), `campaigns/bulk/` (10 files,
`PersonalMessagePane.tsx` 218 lines, `PersonalMessageFormSheet.tsx` 177 lines,
`PersonalRecipientCard.tsx` 166 lines all over gate), `campaigns/templates/` (4 files). All flat
`.tsx`, no 5-file folders. ~7 inline `<svg>` in `campaigns/page.tsx` alone.

### `club/` (6 files)
`club/page.tsx` (393 lines, largest page in the module), `club/_common/ClubItemFormSheet.tsx`
(227 lines), `RedeemSheet.tsx`, `ClubConfirmationTemplateCard.tsx`. All flat, ~6 inline `<svg>`
in `club/page.tsx`.

### `customers/` (13 files)
`customers/page.tsx` (250 lines), `MemberReportSheet.tsx` (275 lines), `points/page.tsx`
(221 lines), `segments/` (8 files incl. `ScoreThresholdsCard.tsx` 103 lines,
`TaggedMembersCard.tsx`, `TagsPane.tsx` 124 lines). `MemberRow.tsx` has 13 hardcoded per-item
hex colors for platform/segment badges — candidate for the `.consts.ts` `Record` +
`DEFAULT_*` pattern described in `skill-asset-extraction`.

### `reports/` (4 files)
`reports/page.tsx` (155 lines, just over gate), `LifecycleFunnelCard.tsx` (107 lines),
`SmsPerformanceCard.tsx` (4 hex colors).

### `tools/` (largest subtree — ~95 files across 9 tool pages)
- `tools/radar/_common/ZoneFormSheet.tsx` — **426 lines, worst offender in the module.** Also
  carries 7 hex colors including a literal `#4B45E6` that duplicates `--color-club-primary`.
- `tools/page.tsx` (343 lines, 10 inline `<svg>`), `tools/regional/_common/SendPane.tsx`
  (261 lines), `tools/reminders/page.tsx` (207 lines), `tools/surveys/_common/SurveyFormSheet.tsx`
  (212 lines), `tools/wheel/` (12 files, `WheelFormSheet.tsx` 183 lines,
  `WheelSpinPane.tsx` 181 lines — `WheelSvg.tsx` is legitimate generated-geometry SVG, leave it
  inline), `tools/occasions/`, `tools/referral/`, `tools/retargeting/` (each 6-9 files, all flat).
- Every `tools/*/​_common/labels.ts` file (6 of them) is already the *correct* pattern
  (module-local extracted Persian labels) — just not yet migrated into `fa.admin.customerClub.*`
  the way the rest of the admin app does it. Low-risk, high-volume follow-up.

### `settings/` (4 files)
`RulesPane.tsx` (149 lines, right at the gate), `AutoPane.tsx`, `GeneralPane.tsx`,
`SettingRow.tsx`. All flat, 23 Persian lines inline in `RulesPane.tsx` alone.

### `setup/` (8 files)
`SetupStepper.tsx`, `ProfileStep.tsx`, `ProfileSheet.tsx`, `PlanStep.tsx`, `PaySheet.tsx`,
`LineStep.tsx`, `SuccessStep.tsx`. All flat, none over the line gate individually.

### `_common/` remainder
- `_common/api/*` (13 files, 1,266 lines) — was slated for a `hooks.ts` + `schemas.ts` split
  (the `discounts`/`stock` pattern) but only the shell's own data hooks were migrated as part of
  this branch's touched-file set. The rest of `campaigns.ts`, `categories.ts`, `customers.ts`,
  `loyalty.ts`, `radar.ts`, `regional.ts`, `reports.ts`, `sms.ts`, `surveys.ts`, `wheel.ts` still
  live as one file per domain rather than folded into a module-wide `hooks.ts`/`schemas.ts` pair.
  Recommend doing this split gradually, in the same commit as whichever page/tool subtree gets
  converted next — don't do it as one big mechanical move, since 13 files' worth of query hooks
  in one `hooks.ts` would itself blow the line gate.
- `_common/ui/*` (remaining after this branch): `ClubCard.tsx` (fork of `@/ui`'s `Card`),
  `ClubTabsCtl.tsx` (fork of `TabNav`+`TabItem`), `ClubStatBox.tsx` (fork of `AdminStatBox`),
  `ClubEmptyState.tsx` (fork of the shared `EmptyState`), `ClubBarRows.tsx`, `ClubChipsRow.tsx`,
  `ClubFormField.tsx`, `ClubInfoBox.tsx`, `ClubSheet.tsx`, `ClubSwitch.tsx`, `SmsComposer.tsx`,
  `SmsBubble.tsx` (6 hex colors for message-bubble tinting). These are the highest-leverage
  remaining items — replacing `ClubCard`/`ClubTabsCtl`/`ClubStatBox`/`ClubEmptyState` with their
  shared-package equivalents removes four forked components in one pass across every page that
  imports them.

## Remaining inline `<svg>` (outside this branch's touched files)

~92 sites across the subtrees above (down from 122 pre-branch — this branch's icon-registry
migration covered the shell + touched pages only). Grep to re-count against the current tree:

```
rg '<svg' apps/admin/app/plugin/customer-club --glob '!**/WheelSvg.tsx'
```

## Remaining raw hex in `className` / inline `style`

~90 sites (down from 106). Worst concentrations: `ZoneFormSheet.tsx` (7),
`MemberReportSheet.tsx` (5), `ScoreSegmentsPane.tsx` (5), `SmsPerformanceCard.tsx` (4),
`customers/page.tsx` (4), `MemberRow.tsx` (13, see above).

```
rg '\[#[0-9a-fA-F]{3,8}\]|#[0-9a-fA-F]{6}' apps/admin/app/plugin/customer-club
```

## Remaining inline Persian strings

~1,150 lines (down from 1,209). The 6 `tools/*/labels.ts` files and `_common/clubViews.ts`'s
`CLUB_TITLES` are already the right *shape* (extracted, module-local) — the remaining work is
moving them into `apps/admin/messages/fa.ts` under `fa.admin.customerClub.*`, not re-extracting
from scratch.

## Suggested order for the next pass

1. `_common/ui/*` fork replacements (Card/TabNav/StatBox/EmptyState) — touches every page, so
   doing it first means every subsequent subtree conversion inherits it for free.
2. `settings/` and `setup/` (smallest subtrees, good next validation of the pattern before
   tackling `tools/`).
3. `tools/radar/_common/ZoneFormSheet.tsx` on its own — it's the single largest file in the
   module and will need a real split (form sections + a `state/` reducer layer, per
   `plugin/product/_common/ProductForm/state/`), not just a folder move.
4. `campaigns/`, `club/`, `customers/`, `reports/` — remaining page-level subtrees, each roughly
   the size of `settings/`+`setup/` combined.
5. `_common/api/*` hooks/schemas split, done incrementally alongside whichever subtree above is
   in flight, not as a standalone pass.

## §1.3 — shared components that could not be reused as-is

None found during this branch's work. Every shared component needed (`AdminTopBar`, `Icon`,
`Card`, `TabNav`/`TabItem`, `AdminStatBox`, `CollapsibleHeader` (new), `useScrollCollapse` (new))
either already existed with a sufficient prop surface or was added to `packages/ui` following the
existing component conventions. If the next pass through `_common/ui/*` or `tools/radar/ZoneFormSheet.tsx`
finds a screen a shared component genuinely cannot express, add it here with the specific gap
(prop that doesn't exist, layout the shared component can't produce) rather than forking.
