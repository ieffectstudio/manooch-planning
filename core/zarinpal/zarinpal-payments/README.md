# ZarinPal Payments — Node.js reference integration

Full PRD: [`docs/PRD.md`](docs/PRD.md)

Three modes, one code path, switched by a single env var:

| `ZARINPAL_MODE` | Base URL | Real money | Internet |
|---|---|---|---|
| `dummy` (default) | `http://localhost:PORT/__mock/pg` | no | no |
| `sandbox` | `https://sandbox.zarinpal.com/pg` | no | yes |
| `production` | `https://payment.zarinpal.com/pg` | **yes** | yes |

## Run

```bash
npm install
cp .env.example .env
npm run dev        # http://localhost:3000
npm test           # 17 assertions, offline
```

Open `http://localhost:3000`, enter an amount, hit پرداخت. The dummy gateway shows a fake
bank page with **success / fail / cancel** buttons so you can drive every branch by hand.

## Files

| File | Purpose |
|---|---|
| `src/config.js` | Mode resolution + boot-time guardrails (refuses to start misconfigured in production) |
| `src/zarinpal.js` | API client: `createPayment()`, `verifyPayment()`, error codes, retry/timeout |
| `src/mockGateway.js` | Local fake ZarinPal (request / StartPay / verify, incl. -50, -51, -54, 101) |
| `src/db.js` | JSON store; `markPaid()` is the compare-and-set that makes fulfilment idempotent |
| `src/server.js` | Express routes: checkout, callback, status, reconcile |
| `tests/flow.test.js` | T1–T9 from the PRD test plan |

## Endpoints

```
POST /api/orders                  { amount, title }        -> demo order
POST /api/payments/checkout       { orderId, mobile? }     -> { authority, redirectUrl }
GET  /pay/:orderId                                          -> 302 straight to the gateway
GET  /api/payments/callback?Authority=..&Status=OK|NOK      -> verifies, shows receipt
GET  /api/payments/:authority                               -> payment row
POST /api/payments/reconcile                                -> cron: rescue abandoned payments
GET  /health                                                -> effective config
```

## Switching to sandbox

```env
ZARINPAL_MODE=sandbox
ZARINPAL_MERCHANT_ID=<any 36 characters>
```
Nothing else changes — all three URLs (request / StartPay / verify) switch together, which
is the #1 cause of "خطای غیرمنتظره" when people do this by hand. Note ZarinPal does not
issue dedicated test merchant IDs and the sandbox is intermittently down; that's exactly
why `dummy` mode exists and is the default.

## Switching to production

```env
ZARINPAL_MODE=production
ZARINPAL_MERCHANT_ID=c3e83cb7-e3ca-4a18-8836-64e8191bfec9
ZARINPAL_CURRENCY=IRT
APP_URL=https://yourdomain.com
```
Preconditions: verified account (silver+), gateway approved **for that exact domain**,
valid IBAN, HTTPS, server IP registered if IP restriction is on.

Then set a cron: `*/15 * * * * curl -XPOST https://yourdomain.com/api/payments/reconcile`
(protect that route with a shared secret before shipping).

## The five rules this code enforces

1. **Always verify.** Unverified successful transactions are auto-reversed after ~24h — the
   customer is charged, then refunded days later, and blames you.
2. **`Status=OK` proves nothing.** Anyone can craft that query string. Only `verify.json`
   returning 100/101 is proof.
3. **Amount comes from the DB**, never from the request body, and the verify amount must
   equal the request amount or you get `-50`.
4. **Fulfil at most once.** `markPaid()` returns `true` only to the caller that flipped
   `pending → paid`; code `101` means "already verified, don't ship again".
5. **Reconcile.** Users close the tab mid-redirect. A cron sweeps stale `pending` rows.

## Security note

For ZarinPal the `merchant_id` **is** the API credential — anyone holding it can create and
verify payments on your account. Keep it in `.env` (gitignored), never in client-side code.
The value in `.env.example` was shared in plain chat, so **regenerate it in the panel**
before going live.
