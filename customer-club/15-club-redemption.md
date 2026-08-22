# Club-redemption confirmations

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`club.redeemed`

## Launch outcome

After a customer successfully spends points on an active in-stock club item, show and send the same committed redemption code without risking partial points/stock state.

## Prerequisites

Seller club items, points ledger, stock, redemption/purchase records, customer authorization, verified sender/template, outbox, reports.

## API

```http
POST /api/public/sellers/:sellerSlug/club/redemptions
POST /api/sellers/me/club/redemptions/:id/resend-confirmation
GET  /api/sellers/me/club/redemptions
```

Public request uses an authenticated/signed customer context and a client command ID; points price, stock, seller, and customer values are server-loaded.

## Atomic redemption transaction

1. Resolve seller/customer/item and validate ownership.
2. Lock item stock and customer points balance/version.
3. Verify item active, stock positive, balance sufficient, and daily purchase cap.
4. Check unique client command to prevent double-click.
5. Deduct exact item points price in immutable ledger.
6. Decrement stock.
7. Create redemption/purchase record with item/price snapshots.
8. Generate unique secure redemption code.
9. Insert `club.redeemed` outbox using redemption ID.
10. Commit.
11. Return committed redemption/code immediately to UI.

Idempotency: `(seller_id, customer_id, client_command_id)` and `club-redeemed:{redemptionId}`.

## Message

Variables: `name`, `item`, `code`, `points`, `balance`, `date`, `store_name`. Render from committed redemption and post-transaction balance. Send one-to-many with one destination.

## Resend

Resend verifies seller/customer authorization and current message policy, creates a new message attempt linked to original redemption, and reuses the original code/item/points snapshots. It never creates another redemption.

## Failure behavior

Provider failure does not roll back a committed redemption automatically. UI still displays code and history marks confirmation failed/unknown. Business reversal is a separate audited transaction restoring stock/points according to policy.

## Acceptance tests

- Concurrent redemptions cannot oversell/overspend.
- Double-click/replayed request returns one redemption.
- SMS provider failure leaves one valid committed redemption.
- Resend reuses original code and has no points/stock effects.
- Seller/customer cannot redeem another seller's item.
- Message matches committed item/price/balance snapshots.

## Done checklist

- [ ] Transaction/locking and concurrency tests pass.
- [ ] Unique code and command constraints deployed.
- [ ] Prototype in-memory mutation replaced by API.
- [ ] Confirmation and resend status visible in purchase history.
