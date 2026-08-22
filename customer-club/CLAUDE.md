# Claude implementation instructions

## Mission

Implement the Customer Club SMS integration against Armaghan Webservice v2 using only the executable scope defined in this package. Treat `README.md` and `docs/` as the implementation contract.

## Read order

1. `README.md`
2. `docs/00-architecture-and-data-model.md`
3. `docs/01-armaghan-v2-adapter.md`
4. `docs/02-seller-sender-configuration.md`
5. `docs/03-dynamic-template-management.md`
6. `docs/19-template-id-and-binding-decision.md`
7. The feature file currently being implemented
8. `docs/16-delivery-reports.md`
9. `docs/17-inbound-opt-out.md`
10. `docs/18-launch-checklist.md`

## Hard scope

Implement only these feature plans:

- welcome and walk-in messages;
- manual campaigns;
- bulk SMS;
- personal/direct messages;
- inactivity reminders;
- birthday and custom occasions;
- points-expiry notifications;
- retargeting notifications;
- referral messages;
- wheel invitations and winner confirmations;
- survey invitations and reminders;
- club-redemption confirmations;
- basic delivery reports;
- inbound SMS and seller-scoped opt-out.

Do not add unrelated provider or product capabilities unless the user explicitly supplies another documented contract.

## Template rule

For this scope, templates live in the application database. Do not create a provider-template-ID mapping for every feature.

```text
seller originator → seller_sender_lines
feature body/version → seller_sms_templates
provider template ID → unused in current scope
```

Use:

- `sendMessageOneToMany` when every final body is identical;
- `sendMessageManyToMany` when final bodies differ by recipient.

## Non-negotiable architecture rules

1. Derive `sellerId` from authenticated context or server-owned event/aggregate; never trust it from the browser.
2. Verify tenant ownership for lines, templates, customers, segments, tools, items, runs, and reports.
3. Use a transactional outbox. Business transactions create message intent; provider workers never mutate points, stock, credit, rewards, spins, or responses.
4. Define a unique seller-scoped idempotency key for every business event and recipient/run where documented.
5. Normalize/deduplicate mobile numbers before eligibility, credit reservation, and batching.
6. Check opt-out, validity, daily cap, suppression, and business hours before queueing and immediately before provider submission.
7. Store v2 provider message/reference IDs as strings.
8. Preserve destination/content array alignment in many-to-many requests.
9. Treat an HTTP timeout after request transmission as ambiguous; do not blindly retry.
10. Store sender/template/version/business snapshots for audit and deterministic history.
11. Use explicit seller timezone; product standard is `Asia/Tehran`.
12. Apply seller signature before final 320-character validation.
13. Use POST calls from the backend. Never expose provider credentials to frontend code.

## Provider adapter contract

Build calls from:

```text
ARMAGHAN_BASE_URL=https://panel.hisms.ir
ARMAGHAN_API_PREFIX=/webservice/rest/v2
```

Credentials come from a secret manager/environment and must be redacted.

Required operations:

- `sendMessageOneToMany`
- `sendMessageManyToMany`
- `getMessageState`
- `getUserInfo`
- `getReceivedMessages`

Always inspect `errorModel.errorCode`; HTTP 200 is not sufficient. Implement the error mapping in `docs/01-armaghan-v2-adapter.md`.

## Repository behavior

Before coding:

1. Inspect the existing stack, conventions, tenant/auth model, database/ORM, queue, scheduler, logging, tests, and error format.
2. Reuse existing abstractions where they satisfy the contract.
3. Do not rewrite unrelated architecture.
4. Present a short implementation plan and affected files.
5. Implement in small reviewable phases with migrations and tests.
6. Never put real credentials or customer data into fixtures, tests, examples, or logs.

## Minimum test requirements

For every feature:

- happy path;
- cross-seller authorization failure;
- idempotency/replayed command;
- invalid/opted-out destination;
- provider permanent error;
- provider account-level error;
- ambiguous timeout behavior;
- template variable/final-length validation;
- correct sender/template resolution;
- database transaction rollback where business state is atomic.

For batch features additionally test overlap dedupe, stable recipient selection, array alignment, batch boundaries, credit reservation/reconciliation, and partial/unknown submissions.

For scheduler features additionally test Tehran timezone boundaries, duplicate workers, business hours, changed eligibility, and suppression windows.

## Definition of done

A feature is done only when:

- migrations/constraints are applied;
- backend API/event path is wired;
- outbox dispatch is wired to the real adapter abstraction;
- provider references and delivery states are persisted;
- seller-isolated history/reporting is available;
- consent and quota checks are enforced;
- feature unit/integration tests pass;
- relevant items in `docs/18-launch-checklist.md` are evidenced;
- no prototype fixture number, balance, count, percentage, or in-memory mutation remains authoritative.

## If information is missing

Do not invent provider behavior. Mark the point as an explicit blocker, state what contract/data is missing, and continue only with work that remains correct under the documented API.
