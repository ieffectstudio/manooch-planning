> **Status: Shipped** on branch `feat-2-week-demo` (all three repos). New `seller_subscriptions`
> table (base + overlay windows, resolved with pure date math) replaces the previous hardcoded
> `/subscriptions/me` stub. 14-day Economy trial fires on `createOnboarding`; the referral gift
> (3 days Pro per completed invite, stacking, pause-and-extend on a `source='purchase'` base only)
> is granted post-commit with a daily reconciliation cron; existing sellers were backfilled a
> 90-day purchase window before the guard went live. Gate enforced server-side via a global
> `PlanEntitlementGuard` (`403 PLAN_REQUIRED`) and client-side via `apps/admin/lib/api/client.ts`
> + the `PlanGate` component. Out of scope for this pass (see the PR description): real payment
> (Zarinpal), per-tier feature gating, storefront blocking, and a storeless referrer's gift days
> burning with nothing to spend them on.
>
> — updated 2026-08-11

# PRD — Manooch Subscription / Plan Logic for New Sellers (compact)

You are a senior engineer on **Manooch**, a multi-store SaaS e-commerce platform ("Powered by Manooch"). I need you to design and implement the **plan/subscription logic** for new seller (admin) signups, including a **referral incentive**. Please analyze the requirements below and give a concrete implementation plan (+ illustrative code) to build and test end-to-end.

**Plans:** there are three plans — **Basic**, **Economy**, and **Pro**. (/subscription in the admin panel is where sellers buy/see plans; /invite-friends is the referral/invite page in admin.)

---

## Requirements

### 1. Default trial for every new seller: 14 days Economy
- When a **new seller registers** (admin), by default a **14-day Economy plan** becomes active, so they can see the features and surf inside Manooch during the trial.
- This 14-day Economy trial applies whether or not the seller registered via a referer.

### 2. Referral incentive: referer gets 3 days Pro per successful invite
- If a new seller **registered with a referer** (via the admin **/invite-friends** referral flow) **and completes registration by creating a store**, the **referer** (the person who sent the invite) gets a **3-day Pro plan** subscription as a reward.
- **The reward is per invite and stacks:** the referer gets 3 days of Pro **for each** friend who registers completely. E.g. if I invite 3 friends and they all register completely, I get **9 days of Pro** (3 + 3 + 3).
- **If the referer already owns/paid another plan before this:** the stacked Pro days run first (active and used), and when they end it should **automatically switch back to the referer's previous active plan**.
- So the 3-day (per-invite) Pro reward is a stack-on-top credit: it is used first, then reverts to the prior plan.

### 3. Trial ends with no other plan → block features & redirect to buy
- When the **14-day Economy trial is done** and the seller **does not have any other plan**, the store should:
  - **Redirect the seller to the buy/promotion page** (/subscription in admin), and
  - **none of the (paid) features work** until they pay/subscribe.

---

## Deliverables: proposed plan model & entitlements • default trial activation • referral reward logic (3-day Pro stacking & auto-revert to prior plan) • expiration/blocking flow (redirect to /subscription, features disabled) • edge cases.
**Edge cases:** new seller with referer (14-day Economy + referer's Pro reward awarded independently); reward only credited when the invitee **completes registration by creating a store** (not just signup); multiple successful invites stack (3 days each, e.g. 3 invites → 9 days of Pro); referer with no plan vs already-paid plan (revert to previous active plan after stacked Pro ends); trial expires with a paid plan present (no blocking); trial expires with no plan (block + redirect to /subscription); what happens after the referer's stacked Pro ends if they never had a prior plan; plan tier behavior on the store (features gated per plan).
