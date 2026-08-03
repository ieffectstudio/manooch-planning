# PRD — ZarinPal Payment Integration (Node.js)

**Owner:** —
**Status:** Draft v1.0
**Date:** 2026-08-03
**Stack:** Node.js 18+ / Express (portable to Next.js route handlers)

---

## 1. Summary

Add card payments to the product using **ZarinPal** (درگاه پرداخت زرین‌پال), the Iranian
Shaparak-network PSP. The integration must be developable and testable **without moving
real money**, then flipped to production with a single environment variable.

Three runtime environments, one code path:

| Mode | `ZARINPAL_MODE` | Base URL | Money moves? | Needs internet? |
|---|---|---|---|---|
| Dummy / mock | `dummy` | `http://localhost:PORT/__mock/pg` | No | No |
| ZarinPal Sandbox | `sandbox` | `https://sandbox.zarinpal.com/pg` | No | Yes |
| Production | `production` | `https://payment.zarinpal.com/pg` | **Yes** | Yes |

---

## 2. Goals / Non-goals

### Goals
- G1. User can pay for an order with a bank card and the order is marked `paid` **only** after server-side verification.
- G2. Zero-config local development: `npm run dev` works offline in `dummy` mode.
- G3. No double-charging, no double-fulfilment, no lost payments (money taken, order not marked paid).
- G4. Every payment attempt is auditable: authority, ref_id, card mask, amount, status, timestamps.
- G5. Switching test → production requires **only** env-var changes, no code changes.

### Non-goals (v1)
- Direct debit / پرداخت مستقیم (Payman) subscriptions.
- Split settlement (`wages` / تسهیم).
- Refunds & reversals (`/pg/v4/payment/reverse.json`) — manual via panel in v1.
- Multi-currency. Currency is fixed per deployment (`IRT` or `IRR`).
- Other PSPs (IDPay, Zibal). Adapter interface is designed to allow them later.

---

## 3. Prerequisites (account side, before production)

| Item | Blocking? | Notes |
|---|---|---|
| Verified ZarinPal account (احراز هویت) | Yes | Silver level minimum — error `-16` below silver |
| Approved gateway (درگاه) on a **specific domain** | Yes | `callback_url` domain must match exactly → error `-14` |
| `merchant_id` (36-char UUID) | Yes | Panel → درگاه پرداخت → اطلاعات فنی |
| Valid IBAN (شماره شبا) in own name | Yes | Settlement target |
| HTTPS with a valid certificate | Yes | Production callbacks |
| Server IP registered | Conditional | If IP restriction is enabled → error `-10` |
| eNamad (نماد اعتماد) | Conditional | Needed to upgrade from واسط to درگاه مستقیم |

> **Security:** for ZarinPal the `merchant_id` *is* the API credential. Treat it as a secret:
> `.env` only, never in the client bundle, never in git. If leaked → regenerate in the panel.

---

## 4. Payment flow

```
[1] Client            POST /api/payments/checkout   { orderId }
[2] Server            price = lookup(orderId)          <-- NEVER trust client amount
[3] Server -> PG      POST {base}/v4/payment/request.json
                      { merchant_id, amount, currency, description, callback_url, metadata }
[4] PG   -> Server    { data: { code:100, authority:"A000...", fee, fee_type }, errors: [] }
[5] Server            payments.insert(authority, orderId, amount, status='pending')
[6] Server -> Client  302 -> {base}/StartPay/{authority}
[7] User pays on ZarinPal / bank page
[8] PG   -> Browser   302 -> callback_url?Authority=A000...&Status=OK|NOK
[9] Server            if Status != OK  -> mark 'canceled', show failure page
[10] Server -> PG     POST {base}/v4/payment/verify.json
                      { merchant_id, amount, authority }        <-- SAME amount as step 3
[11] PG  -> Server    { data: { code:100|101, ref_id, card_pan, card_hash, fee }, errors: [] }
[12] Server           code 100 -> mark 'paid', fulfil once (idempotent)
                      code 101 -> already verified, do NOT re-fulfil
                      other    -> mark 'failed', store error code
[13] Server -> Client Receipt page showing ref_id
```

### State machine

```
created ──request ok──> pending ──Status=OK & verify 100──> paid
   │                       │
   │                       ├──Status=NOK────────────────> canceled
   │                       ├──verify -51/-54/other──────> failed
   │                       └──no callback in 30 min─────> expired (reconciliation job)
   └──request error──────> failed
```

`paid` is terminal. Transition into `paid` must be a single atomic DB update guarded by
`WHERE status = 'pending'` so concurrent callbacks cannot fulfil twice.

---

## 5. API contract

### 5.1 ZarinPal endpoints

| Purpose | Method | Path (append to base) |
|---|---|---|
| Create payment | POST | `/v4/payment/request.json` |
| Redirect user | GET | `/StartPay/{authority}` |
| Verify payment | POST | `/v4/payment/verify.json` |
| Inquiry (optional) | POST | `/v4/payment/inquiry.json` |
| Unverified list | POST | `/v4/payment/unVerified.json` |

**request.json body**

| Field | Type | Req | Notes |
|---|---|---|---|
| `merchant_id` | string(36) | ✔ | |
| `amount` | integer | ✔ | ≥ 1000 IRT / 10000 IRR; max 100,000,000 IRT |
| `currency` | `IRR` \| `IRT` | ✖ | **Always send explicitly** |
| `description` | string ≤500 | ✔ | |
| `callback_url` | string | ✔ | Must be on the registered domain |
| `metadata.mobile` | string | ✖ | `09xxxxxxxxx` — enables saved-card UX |
| `metadata.email` | string | ✖ | |
| `metadata.order_id` | string | ✖ | Shows in panel, useful for support |

**verify.json body:** `{ merchant_id, amount, authority }` — `amount` must equal the request amount, else `-50`.

**verify.json success response:** `code`, `message`, `ref_id`, `card_pan` (masked), `card_hash` (SHA256), `fee_type`, `fee`.

### 5.2 Our internal endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/payments/checkout` | Body `{ orderId }` → `{ redirectUrl, authority }` |
| GET | `/api/payments/callback` | ZarinPal return URL; verifies and redirects to receipt |
| GET | `/api/payments/:authority` | Payment status for polling / support |
| POST | `/api/payments/reconcile` | Cron-only: verify stale pendings |

---

## 6. Error handling

| Code | Meaning | User-facing action |
|---|---|---|
| `100` | Success | Show receipt + `ref_id` |
| `101` | Already verified | Show receipt, **do not re-fulfil** |
| `-9` | Validation error | Log; likely bad amount/description/callback |
| `-10` | Bad merchant_id or IP | Alert ops — misconfiguration |
| `-11` | Terminal inactive | Alert ops |
| `-12` | Too many attempts | Rate-limit our side, retry later |
| `-14` | Callback domain mismatch | Alert ops — wrong `APP_URL` |
| `-15` / `-16` / `-17` / `-19` | Terminal suspended / level too low / banned | Alert ops |
| `-41` | Over 100M toman | Block at validation time |
| `-50` | Amount mismatch on verify | **Critical** — investigate manually |
| `-51` | Payment not successful | "پرداخت انجام نشد" |
| `-53` | Authority belongs to another merchant | Critical, possible attack |
| `-54` | Invalid authority | 404 the callback |

All non-success codes are persisted on the payment row (`error_code`, `error_message`).
Codes `-10, -11, -14, -15, -16, -19, -50, -53` fire an ops alert.

---

## 7. Hard requirements (the ones that bite)

- **R1 — Verify always.** An unverified successful transaction is auto-reversed by ZarinPal
  after ~24h. Customer's money is taken, then returned days later, and they scream.
- **R2 — Idempotency.** The callback URL can be opened twice (refresh, back button, bots).
  Fulfilment runs at most once per `authority`.
- **R3 — Server-side pricing.** `amount` is derived from the order in the DB, never from the request body.
- **R4 — `Status=OK` is not proof.** Anyone can hit `?Authority=X&Status=OK`. Only `verify.json` code 100/101 is proof.
- **R5 — Currency consistency.** `IRT` vs `IRR` mismatch = 10× under/over charge. One env var, asserted at boot.
- **R6 — Reconciliation job.** Every 15 min, take `pending` payments older than 20 min and
  call `unVerified.json` / `verify.json`; users close the tab mid-redirect constantly.
- **R7 — Persist before redirect.** Row must exist with `authority` before the user leaves the site.
- **R8 — Timeouts + retry.** 15s timeout on PG calls; verify retried up to 3× with backoff
  (verify is safe to retry — 101 on repeats).

---

## 8. Data model

```sql
CREATE TABLE payments (
  id            TEXT PRIMARY KEY,
  order_id      TEXT NOT NULL,
  authority     TEXT UNIQUE,
  amount        INTEGER NOT NULL,      -- in `currency` units
  currency      TEXT NOT NULL,         -- IRR | IRT
  status        TEXT NOT NULL,         -- created|pending|paid|failed|canceled|expired
  ref_id        TEXT,
  card_pan      TEXT,                  -- masked only
  card_hash     TEXT,
  fee           INTEGER,
  fee_type      TEXT,
  error_code    INTEGER,
  error_message TEXT,
  mode          TEXT NOT NULL,         -- dummy|sandbox|production
  created_at    TEXT NOT NULL,
  verified_at   TEXT
);
CREATE INDEX idx_payments_status_created ON payments(status, created_at);
```
Never store full PAN, CVV2, or expiry — we never see them, and must not.

---

## 9. Configuration

```env
ZARINPAL_MODE=dummy                # dummy | sandbox | production
ZARINPAL_MERCHANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ZARINPAL_CURRENCY=IRT              # IRT (toman) or IRR (rial)
APP_URL=http://localhost:3000      # callback base; must match registered domain in prod
PORT=3000
```

Boot-time assertions:
- `production` ⇒ `merchant_id` matches UUID regex, `APP_URL` starts with `https://`.
- `dummy` ⇒ merchant id may be any 36 chars.
- Unknown `ZARINPAL_MODE` ⇒ crash, do not silently default to production.

---

## 10. Test plan

### 10.1 Dummy mode (default local)
A built-in mock gateway that mimics `request.json`, `StartPay`, `verify.json`, including a
payment page with **Pay success / Fail / Cancel** buttons. Deterministic, offline, instant.

| # | Scenario | Expected |
|---|---|---|
| T1 | Happy path | `paid`, `ref_id` shown |
| T2 | User cancels | `canceled`, no fulfilment |
| T3 | Bank failure | `failed`, code `-51` |
| T4 | Refresh callback twice | second verify returns `101`, fulfilment count stays 1 |
| T5 | Tampered `Authority` | `-54`, 404 |
| T6 | Tampered amount in verify | `-50` |
| T7 | Amount below minimum | rejected before hitting PG |
| T8 | Abandoned payment + cron | moves `pending` → `paid`/`expired` |

### 10.2 Sandbox mode
`https://sandbox.zarinpal.com/pg/...`, any 36-character string as `merchant_id`.
**All three URLs must be switched together** (request, StartPay, verify) or you get
"unexpected error". Sandbox is publicly known to be intermittently down — it is a
*secondary* check, not the primary dev loop.

### 10.3 Production smoke test
One real 1,000 toman payment with a real card, confirm `ref_id` appears in the ZarinPal
panel, then refund manually. Do this before announcing launch.

---

## 11. Rollout

1. Build against `dummy`; T1–T8 green in CI.
2. Deploy to staging with `sandbox`; manual pass of T1–T4.
3. Register production domain + callback in the ZarinPal panel; set env vars.
4. Production smoke test with 1,000 toman.
5. Enable reconciliation cron and ops alerts.
6. Announce.

**Rollback:** set `ZARINPAL_MODE` back / disable the checkout button. Existing `pending`
rows are resolved by the reconciliation job, not by the deploy.

---

## 12. Metrics

- Checkout → paid conversion rate.
- Verify failure rate by error code.
- Count of payments requiring reconciliation (target < 2%).
- p95 latency of `request.json` and `verify.json`.
- **Alert:** any `-50` or `-53`, any `paid` row without `ref_id`, reconciliation backlog > 10.

---

## 13. Open questions

- Currency displayed to users: toman or rial? (affects `ZARINPAL_CURRENCY`)
- Who pays the fee — merchant or customer? (`fee_type` in panel)
- Is eNamad already obtained (direct vs. intermediary gateway)?
- Are refunds needed in v1, or is manual panel refund acceptable?
