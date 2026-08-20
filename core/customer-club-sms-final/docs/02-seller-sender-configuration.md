# Pre-provisioned seller sender configuration

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Scope

The attached provider API documents sending from an existing `originator`; it does not document obtaining lines. This plan starts only after a real originator has already been provisioned and authorized in Armaghan.

## Data

`seller_sender_lines` stores:

- internal ID;
- seller ID;
- originator as a string;
- display label;
- provider account ID;
- `verified`, `disabled`, or `pending` status;
- default/active flags;
- verification and audit timestamps.

Never generate originators and never store them as numeric database types.

## Admin configuration flow

1. Authorized operator enters an already-approved originator and its provider-account scope.
2. Backend checks that the same provider line is not assigned contrary to product policy.
3. Operator sends a real test through `sendMessageOneToMany` to an authorized test mobile.
4. `errorCode=0` and a returned reference mark submission verified; `-103` rejects the originator.
5. Delivery polling records final test state.
6. Operator activates the line for the seller.

A successful provider submission proves authorization for sending under those credentials; delivery status proves the test message lifecycle.

## Seller APIs

```http
GET  /api/sellers/me/sms/sender-lines
PUT  /api/sellers/me/sms/default-sender-line
POST /api/sellers/me/sms/sender-lines/:id/test
```

The seller receives internal IDs and masked originators. Selection accepts only an internal ID and verifies ownership server-side.

## Runtime resolution

```text
feature-specific seller line, if intentionally configured
  → seller's verified active default line
  → fail with SELLER_SENDER_NOT_CONFIGURED
```

Do not silently fall back to another seller's line or a global environment originator. An environment originator may seed one seller record during migration, after which runtime routing uses the database.

## Test-send requirements

- Authenticated seller ownership.
- Explicit authorized test destination.
- Real seller template rendering.
- `is_test=true` audit/message rows.
- Same adapter/error handling as production.
- Excluded from campaign KPIs, but included in operational cost/audit.

## Failure handling

- `-103`: disable line and alert operations.
- `-101`, `-110`, `-119`: pause affected provider account.
- `-104`: pause sending until provider credit is restored.
- Delivery failure: keep line configuration but expose the test result for review.

## Acceptance tests

- Seller A cannot list/select/test Seller B's line.
- Browser-supplied free-form originator is rejected.
- Pending/disabled lines cannot become default.
- At most one default line exists per seller.
- Every send snapshot contains the resolved seller originator.
