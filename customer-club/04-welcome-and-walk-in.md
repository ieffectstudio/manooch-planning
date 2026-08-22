# Welcome and walk-in messages

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`member.welcome`

## Launch outcome

Send one seller-branded welcome message after a genuinely new club membership, including a committed welcome-points amount when configured. Online membership and the prototype walk-in keypad use the same backend transaction.

## Prerequisites

- Seller has an active verified sender line and active `member.welcome` template.
- Customer mobile is valid and normalized.
- Welcome-points policy is persisted for the seller.
- Customer and points ledger APIs are available.

## Data and constraints

- Customer uniqueness inside a seller tenant by normalized mobile.
- Unique welcome ledger key `(seller_id, customer_id, 'welcome')`.
- Unique outbox idempotency key `welcome:{sellerId}:{customerId}`.
- Store the awarded points and post-award balance snapshots.

## APIs/events

```http
POST /api/sellers/me/customers/walk-in
```

```json
{"name":"زهرا کریمی","mobile":"09120000000"}
```

Online membership emits the same server event:

```ts
MemberCreated { sellerId, customerId, source, occurredAt }
```

## Atomic creation flow

1. Derive seller from authenticated store context.
2. Normalize and validate mobile.
3. Begin transaction and find-or-create seller customer.
4. If the customer already existed, return it without another welcome award/send.
5. Insert welcome-points ledger entry once.
6. Insert `member.welcome` outbox event with committed `name`, `points`, `balance`, and `store_name` variables.
7. Commit.
8. Worker resolves seller sender/template, renders, and calls `sendMessageOneToMany` with one destination.

Provider payload shape:

```json
{
  "originator":"<seller-originator>",
  "content":"<seller welcome text>",
  "destinations":["09120000000"]
}
```

The adapter injects provider credentials and v2 URL.

## Consent and classification

A plain membership/points confirmation is relationship messaging. If promotional discount content is added, apply marketing-consent policy. Always apply invalid-number and seller SMS kill-switch checks.

## Failure behavior

Provider failure does not undo customer creation or committed points. Keep the outbox/message failed or unknown and expose controlled resend. Resend uses the same customer/points snapshot and cannot grant points again.

## Internal statuses

`customer_created → points_committed → sms_queued → provider_accepted → sent/delivered/not_delivered`.

## Acceptance tests

- New online and walk-in members each receive exactly one welcome intent.
- Existing mobile under the same seller gets no duplicate points/message.
- Same mobile under another seller is isolated and may join independently.
- Provider retry/resend cannot create another points ledger entry.
- Seller A's sender/template is never used for Seller B.
- Failed SMS leaves committed membership/points intact.

## Done checklist

- [ ] Walk-in prototype calls backend instead of mutating in-memory arrays.
- [ ] Unique customer/welcome constraints deployed.
- [ ] Template preview/test send passes.
- [ ] Outbox and delivery history visible in customer report.
