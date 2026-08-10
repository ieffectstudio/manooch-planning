# PRD — Manooch Auth Bugs (compact)

You are a senior engineer debugging **Manooch**, a multi-store SaaS e-commerce platform ("Powered by Manooch"). Architecture: one API (`api.manooch.site`), one admin panel for sellers, one portal (super-admin) panel, and many storefronts (one per shop, e.g. `tajmahal.manooch.site`). Auth = OTP (phone → OTP → token).

**Three fully-independent roles (never conflict):**
1. **Seller** — owns/manages a store (admin panel).
2. **Customer** — shops on any storefront.
3. **Portal / Super Admin** — Manooch platform admin (manages all stores/orders; stored separately).

**Key rule — role independence:** One person may hold any combo of roles with the **same phone number** with no conflict. A seller can be a customer (on any shop, incl. their own, with the same number). A super admin can own a store and/or be a customer anywhere. This already works today for own-store + same-number customers and super admins — so customer registration must never be blocked by store ownership.

Please analyze root cause, correct behavior, and fix for each bug below; give a concrete plan (+ illustrative code) to implement and test end-to-end.

---

## Bug 1 — Seller seen as logged-in on their storefront
- Log in to admin as seller → click **"دیدن فروشگاه"** (View Shop) → opens my storefront → hamburger menu shows **authorized/customer menu**, though I never logged in on the storefront.
- **Bug:** Storefront treats seller as an authenticated customer; appears to reuse the admin/seller session/token (shared cookie/global auth state).
- **Expected:** Opening own shop from admin shows the **public/guest** view (or an explicit "preview as seller" mode). Never show the customer-auth menu unless genuinely logged in as a customer there.
- **Question:** Why does the storefront see a seller as an authenticated customer? Is one shared auth token/cookie reused across admin + storefront? How to keep seller vs customer sessions separate?

## Bug 2 — Logging out of storefront also logs out of admin
- Logged into admin as seller → go to profile on storefront → log out → **admin seller session is also killed**.
- **Bug:** Storefront logout invalidates the admin session too.
- **Expected:** Storefront (customer) logout ends **only** the customer session; must not affect the seller's admin session. Tokens fully isolated.
- **Question:** What causes a storefront logout to kill the admin session? Same token, or same storage key (`localStorage`/cookie) used for both seller and customer auth, so logout clears the shared key? How to store/clear them independently?

## Bug 3 — Can't register as a customer on another shop because I own a store
- I own a store (seller). Try to **register as a customer** on `tajmahal.manooch.site/sign-up`. On OTP request to `api.manooch.site/auth/request-otp`, get:
```json
{"statusCode":400,"success":false,"message":"شما قبلاً یک فروشگاه دارید؛ برای فروشگاه جدید با شماره‌ای دیگر ثبت‌نام کنید","errors":[{"code":"ALREADY_HAS_STORE","message":"شما قبلاً یک فروشگاه دارید؛ برای فروشگاه جدید با شماره‌ای دیگر ثبت‌نام کنید"}]}
```
(Translation: "You already have a shop; to create a new shop register with a different number.")
- **Clarification — the rule is legitimate but misplaced:** "Already has a store" is a real business rule, but it exists **only** to stop one phone number from creating **more than one store**. It must fire **only** in the store-creation flow — never during customer sign-up/login.
- **Bug:** I'm **not** creating a store; I'm registering as a **customer** so I can shop. The system blocks me because I already own a store, preventing a seller from being a customer on any other Manooch shop.
- **Expected:** Customer register/login needs only a valid customer account + phone. Owning a store has **no bearing**. The `ALREADY_HAS_STORE` check only gates store creation (one store per number) and never customer auth. (Proof this works: I can already be a customer on my own store with the same number, and super admins can own a store + be a customer anywhere.)
- **Question:** Why does `request-otp` trigger the single-store-per-number check during a customer flow? Does the OTP endpoint assume every request is a seller/store creation? Where should this check live so it only gates store creation?

---

## Deliverables per bug: root cause • correct behavior • recommended fix • edge cases.
**Root cause (shared thread):** seller/customer/portal auth not separated, and role checks applied in the wrong place (OTP/registration not role-aware).
**Edge cases:** seller visiting own store; seller as customer on another shop; super admin as customer/seller; session expiry; no shared `localStorage` keys or cookies across admin/storefront/portal.
