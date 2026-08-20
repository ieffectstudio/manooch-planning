# Retargeting notifications

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature keys

- `retargeting.credit_granted`
- `retargeting.credit_expiring`

## Launch outcome

Notify a customer after committed return credit/cashback is granted and optionally before unused credit expires. This plan covers notifications; financial calculation and redemption remain server-authoritative application logic.

## Prerequisites

Return-credit ledger, seller rules, customer/order ownership, expiry scheduler, verified sender/templates, outbox, app-credit/reporting.

## Records

`customer_credits`: seller/customer, source order/manual grant, amount, remaining, granted/expiry time, state, idempotency source.

`credit_notifications`: credit ID, type (`granted`/`expiring`), snapshot, outbox/message state, unique business key.

## Grant transaction

1. Verify seller owns customer/order and rule applies.
2. Calculate amount server-side with percentage/fixed rule, cap, minimum basket, and combination policy.
3. Insert immutable credit ledger entry once.
4. Insert `retargeting.credit_granted` outbox using credit ID.
5. Commit.
6. Worker renders/sends after commit.

Idempotency: `retargeting-granted:{creditId}`. Manual grants include actor and reason.

## Expiry scheduler

1. Select active, positive, unused credits entering seller warning window.
2. Re-check state/remaining amount.
3. Filter destination/consent/caps/business hours.
4. Queue `retargeting.credit_expiring` with `retargeting-expiry:{creditId}:{warningDate}`.
5. Render from committed credit snapshot.

## Variables

`name`, `credit`, `balance`, `date`, `store_name`, and `discount_code` only when commerce created one. Personalized batches use many-to-many.

## APIs

```http
POST /api/sellers/me/customers/:customerId/credits
PUT  /api/sellers/me/retargeting/settings
POST /api/sellers/me/retargeting/preview
GET  /api/sellers/me/retargeting/history
```

## Failure/reversal

Provider failure never deletes/recalculates credit. A financial reversal is a new ledger event and may cancel an unsent expiry notice. Do not mutate historical message snapshots.

## Acceptance tests

- Same source order/manual command cannot grant twice.
- Credit cap/minimum/expiry are server-enforced.
- Used/expired/reversed credit is excluded from expiry notices.
- Grant and outbox creation are atomic.
- Resending cannot grant another credit.
- Message amount/date match the ledger snapshot.

## Done checklist

- [ ] Financial rule/idempotency tests pass.
- [ ] Grant and expiry templates configured separately.
- [ ] Expiry scheduler checks current remaining balance.
- [ ] History links credit ledger and provider reference.
