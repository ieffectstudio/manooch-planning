# manooch-planings

Planning docs — PRDs, bug reports, and implementation notes — for the Manooch platform. Code lives
in the sibling repos `manooch-backend`, `manooch-fronts`, `manooch-cms`.

This index exists because docs here have gone stale/orphaned before (three PRDs were deleted with
no pointer removed anywhere — `deploy.md`, `enamad.md`, `portal/business-category-crud.md`). When
you delete or supersede a doc, delete its row here too, in the same change.

## `core/` — platform-level features

| Doc | Status |
|---|---|
| [`custom-domain/prd.md`](core/custom-domain/prd.md) | Implemented (code) — DNS/firewall enablement still required before go-live |
| [`stock/PRD-stock-pricing.md`](core/stock/PRD-stock-pricing.md) | Approved spec |
| [`zarinpal/zarinpal-payments/docs/PRD.md`](core/zarinpal/zarinpal-payments/docs/PRD.md) | Draft v1.0 |
| [`zarinpal/prompt.md`](core/zarinpal/prompt.md) | Working notes for the zarinpal prototype above |
| [`fino-teck-verfiy-phone-nId/`](core/fino-teck-verfiy-phone-nId/fino-teck-verfiy-phone-nId.md) | Draft, imported from elsewhere — written against a Python/FastAPI/Redis stack, not this platform's NestJS backend; needs a rewrite before it's actionable here |
| [`14-days-demo/prompt.md`](core/14-days-demo/prompt.md) | Shipped (`feat-2-week-demo`) — 14-day trial, stacking referral gift, plan-expiry gate |
| `bugs/<sprint>/` | Point-in-time bug write-ups (`14-5`, `15-5`, `16-5`, ...) — check the matching front/backend repo's git log for the fix commit before assuming one is still open |
| [`move-server/plan.md`](core/move-server/plan.md) | Reusable server-migration runbook — updated 2026-08-17 with everything proven on the real migration |
| [`move-server/success-deploy-summary.md`](core/move-server/success-deploy-summary.md) | Migration completed 2026-08-16 — post-migration record; secrets rotation still open |
| [`move-server/drop-old-server.md`](core/move-server/drop-old-server.md) | Old server decommission gates — Gates 1-4 passed, Option A (soft stop) done 2026-08-17; Gate 5 (secrets) blocks termination |

## `portal/` — super-admin panel (`apps/portal`)

| Doc | Status |
|---|---|
| [`city-province/prd-api.md`](portal/city-province/prd-api.md) | Approved for implementation — shipped (`manooch-fronts` `af18892`/`2425b4d`, `manooch-backend` `2692ab6`/`b37754d`) |
| [`city-province/fix-module.md`](portal/city-province/fix-module.md) | Execution-plan prompt for the PRD above |
| [`ads-16-5/prompt.md`](portal/ads-16-5/prompt.md) | Ads/banner feature notes for the super-admin dashboard |

## `customer-club/` — loyalty & SMS marketing plugin

| Doc | Status |
|---|---|
| [`PRD.md`](customer-club/PRD.md) | Approved / ready for development — governing spec |
| [`remaining-phases.md`](customer-club/remaining-phases.md) | Phase 1 delivered; Phases 2-4 planned — status-of-record over the PRD for implementation detail |
| [`issues/17-5.md`](customer-club/issues/17-5.md) | Bug report against the shipped Phase 1 UI |

## `visitor/` — visitor order-intake module

| Doc | Status |
|---|---|
| [`PRD.md`](visitor/PRD.md) | In development (working prototype ready) |
| [`issues/16-5.md`](visitor/issues/16-5.md) | Bug reports against the prototype |

## `train/` — Claude Code skill/process proposals

| Doc | Status |
|---|---|
| [`PRD-product-form-state-refactor.md`](train/PRD-product-form-state-refactor.md) | Proposed — ready for engineering review. Shipped as `manooch-fronts` `4fcbbca` + the `react-form-state` skill |

## `cms/` — WordPress → Strapi migration

| Doc | Status |
|---|---|
| [`wp-strapi.md`](cms/wp-strapi.md) | Migration brief — executed; `manooch-cms` is Strapi 5 as of `3b8b191` |
