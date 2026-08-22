# Launch checklist

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


Use this only for the 14 launch-safe feature plans in this folder.

## Provider configuration

- [ ] Base URL is plain `https://panel.hisms.ir`.
- [ ] API prefix is `/webservice/rest/v2`.
- [ ] Shared conversation password has been rotated.
- [ ] Credentials are in a secret manager and backend-only.
- [ ] Outbound server IP is registered; `-110` handling tested.
- [ ] Service/credit/authentication circuit breakers configured.
- [ ] Configurable batch size, timeout, retry, and polling limits set.

## Seller configuration

For every enabled seller:

- [ ] A real, pre-provisioned Armaghan originator exists.
- [ ] The line passed a real provider test and is `verified`.
- [ ] Exactly one verified active default line is configured.
- [ ] An active versioned template exists for every enabled feature key.
- [ ] Business hours, timezone, signature, and daily caps are set.
- [ ] Seller application SMS credit/balance policy is configured.

## Core reliability

- [ ] Transactional outbox and worker deployed.
- [ ] Unique seller/business idempotency keys deployed.
- [ ] Ambiguous timeout does not blindly resend.
- [ ] Provider references stored as strings.
- [ ] Reference/destination order and count validated.
- [ ] Delivery poller and terminal/unknown policies active.
- [ ] Dead-letter/review workflow and alerts active.

## Consent and privacy

- [ ] Mobile normalization/deduplication is shared by all features.
- [ ] Seller-scoped opt-out table and final dispatch check enabled.
- [ ] Inbound poll checkpoint and reply-5 parser enabled before marketing.
- [ ] Feature transactional/marketing classifications approved.
- [ ] Credentials, complete mobiles, and complete bodies are redacted from logs.
- [ ] Raw inbound/body retention and access rules are approved.

## Feature verification

- [ ] Welcome/walk-in: new member and points/outbox commit once.
- [ ] Manual campaign: immediate/scheduled/cancel/report tested.
- [ ] Bulk: overlapping segments deduplicate and arrays align.
- [ ] Personal: customer/manual/segment routes use correct controls.
- [ ] Reminder: completed-order query and 30-day suppression tested.
- [ ] Occasions: calendar, leap-day, yearly idempotency tested.
- [ ] Points expiry: point-lot spend race tested.
- [ ] Retargeting: credit ledger and notifications are atomic.
- [ ] Referral: token scope, abuse controls, reward uniqueness tested.
- [ ] Wheel: server spin and prize/points/outbox transaction tested.
- [ ] Survey: token, one response/reward, non-respondent reminder tested.
- [ ] Club redemption: concurrent stock/points and resend tested.
- [ ] Delivery reports: totals reconcile and no terminal regression.
- [ ] Inbound opt-out: digits/routing/race cancellation tested.

## Tenant isolation

For each API, worker, and report:

- [ ] Seller A cannot read/use Seller B's line.
- [ ] Seller A cannot read/use Seller B's template.
- [ ] Seller A cannot target Seller B's customer/segment/tool/item.
- [ ] Provider reference alone never authorizes report access.
- [ ] Same mobile in two sellers remains independently consented/routed.

## End-to-end smoke test per seller

1. Queue and deliver one welcome message.
2. Run identical-body one-to-many send.
3. Run personalized many-to-many send.
4. Verify exact reference mapping and final delivery state.
5. Trigger a seller business event and confirm exactly one outbox.
6. Reply `5` to that seller line and confirm seller-scoped opt-out.
7. Attempt another marketing send and verify dispatch suppression.
8. Repeat with another seller and verify no cross-tenant effect.

Launch only when all applicable checks are evidenced in staging with provider-approved test destinations.
