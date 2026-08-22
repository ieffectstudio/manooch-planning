# Points-expiry notifications

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`points.expiring`

## Launch outcome

Warn a customer once before still-available points expire, using committed points-lot data and the seller's configured warning window/template.

## Prerequisites

Immutable points ledger/lots with expiry dates, spend allocation policy, customer service, scheduler/timezone utilities, verified sender/template, consent classification, outbox/reporting.

## Data

Each earned points lot has seller, customer, original amount, remaining amount, earned time, expiry time, and source. Do not calculate expiry from only the current aggregate balance.

`points_expiry_notifications` stores seller/customer, grouped expiry date, points snapshot, included lot IDs, outbox/message state, and unique notification key.

## API/settings

```http
PUT  /api/sellers/me/points/expiry-sms-settings
POST /api/sellers/me/points/expiry-sms-settings/preview
GET  /api/sellers/me/points/expiry-notifications
```

Settings: active, days-before-expiry (prototype default 7), local send time, template, and optional minimum expiring amount.

## Scheduler flow

1. Select seller settings due in local timezone.
2. Query positive remaining lots whose expiry matches warning window.
3. Group seller/customer/expiry date when policy allows.
4. Re-read/lock lots before creating notification so spent/reversed amounts are removed.
5. Compute expiring `points` and current `balance` from server data.
6. Apply mobile/consent/cap/business-hour rules.
7. Queue with:

```text
points-expiry:{sellerId}:{customerId}:{expiryDate}:{policyVersion}
```

8. Render `name`, `points`, `balance`, `date`, `store_name`.
9. Dispatch personalized many-to-many batches and save references.

## Concurrency

Point spending may race with the scheduler. Use a transaction/consistent snapshot when creating the notification. The message amount is the queue-time snapshot; if the remaining amount becomes zero before provider dispatch, re-check and cancel unsent intent.

## Classification

A pure expiry warning is relationship messaging. Promotions added to it require marketing consent. Make classification explicit and reviewed.

## Failure behavior

SMS failure never changes points or expiry. Controlled resend uses current eligibility and either the original snapshot or a clearly versioned refreshed message policy.

## Acceptance tests

- Spent/reversed/expired lots are not warned.
- Multiple lots for same date aggregate once.
- Different expiry dates remain separately idempotent.
- Queue retry creates one notification.
- Final points/balance originate from seller ledger.
- Seller A cannot access Seller B's lots/template/line.

## Done checklist

- [ ] Points-lot expiry/spend model confirmed.
- [ ] Race tests with concurrent spend pass.
- [ ] Warning policy and consent classification approved.
- [ ] History links to included lot IDs and message state.
