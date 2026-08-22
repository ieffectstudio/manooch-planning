# Bulk SMS

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`bulk.general`

## Launch outcome

Send a seller message to the union of selected seller segments with correct deduplication, dynamic rendering, limits, cost, schedule, test-send, and history.

## Prerequisites

Seller segments, customers, consent data, verified sender/template, outbox, seller app-credit ledger, scheduler, delivery poller.

## APIs

```http
POST /api/sellers/me/sms/bulk/estimate
POST /api/sellers/me/sms/bulk/runs
POST /api/sellers/me/sms/bulk/runs/:id/cancel
GET  /api/sellers/me/sms/bulk/runs/:id
POST /api/sellers/me/sms/bulk/test
```

Request contains segment IDs, template ID/body selection, and optional schedule—not raw trusted customer records.

## Audience algorithm

1. Verify all segment IDs under authenticated seller.
2. Query the union of members; never sum displayed segment counts because members can overlap.
3. Normalize mobiles.
4. Deduplicate by normalized mobile while preserving a deterministic recipient record.
5. Exclude invalid, opted-out, seller-disabled, daily-cap, and suppression matches.
6. Return gross unique count, eligible count, and exclusions by reason.

## Rendering and provider selection

Apply variables, signature, and 320-character final limit.

- No recipient-specific values and same body → `sendMessageOneToMany`.
- `{name}`, `{points}`, unique links, or other differences → `sendMessageManyToMany`.

Build batches from objects, never separate filtered arrays:

```ts
const batch = eligible.map(r => ({
  destination: r.mobile,
  content: render(template, r.variables)
}));
```

Then derive both arrays from `batch`, preserving indexes.

## Credit and idempotency

Create `bulk_run_id`; unique `(run_id, mobile_hash)` prevents duplicate recipients. Reserve seller app credit after final eligibility and before submission. Provider account credit from `getUserInfo` is only an operational guard.

## Test send

Test uses the seller's real sender/template, one authorized test mobile, sample variables, and `is_test=true`. It does not alter production run statistics but is audited and costed.

## Limits

Enforce default maximum two marketing messages per customer/day where configured, seller business hours, optional inactive-customer suppression, and 320 final characters. Batch size/rate are configuration values until confirmed by provider.

## Failure behavior

- Permanent invalid destination: mark recipient failed.
- Account/configuration errors: pause remaining batches.
- Ambiguous timeout: mark batch unknown and do not blind retry.
- Cancel only recipients not yet submitted; do not claim accepted messages were canceled.

## Acceptance tests

- Overlapping segments send once per mobile.
- Recipient contents and destinations stay aligned across batch boundaries.
- Estimate and execution explain changing eligibility.
- Daily caps and opt-out cannot be bypassed by bulk endpoint.
- Duplicate run worker sends no accepted/unknown recipient again.
- Seller reports are tenant-isolated.

## Done checklist

- [ ] Segment-union query and canonical mobile normalization tested.
- [ ] App-credit reservation/reconciliation deployed.
- [ ] Equal/personalized endpoint selection tested.
- [ ] Test send and real history wired to prototype UI.
