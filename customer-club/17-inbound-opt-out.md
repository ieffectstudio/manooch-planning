# Inbound SMS and opt-out

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Scope

Poll documented incoming messages, route replies by the seller's dedicated destination/originator, and implement seller-scoped marketing opt-out including the product's “reply 5” instruction.

## Provider input

`POST {base}{prefix}/getReceivedMessages` with credentials and pagination fields such as:

```json
{
  "username":"<secret>",
  "password":"<secret>",
  "page":0,
  "size":100,
  "afterId":"<checkpoint>"
}
```

In each record:

- `id`: provider inbound ID, string under v2;
- `destination`: sender line that received the reply;
- `originator`: customer mobile that sent it;
- `content`: reply text;
- `insertDate`: provider receive timestamp.

## Polling/checkpoint design

1. Maintain checkpoint per provider account.
2. Fetch pages after checkpoint.
3. Insert inbox row with unique `(provider_account_id, provider_message_id)`.
4. Process idempotently.
5. Advance checkpoint only after durable inserts for the page.
6. Continue until no further records.

## Seller routing

Resolve normalized `destination` against active `seller_sender_lines`. The requirement that each seller has a dedicated line makes routing deterministic. Unknown/ambiguous destination goes to an operations queue and must not opt out the wrong tenant.

## Opt-out parser

Normalize Persian/Arabic/Latin digits, Unicode whitespace, punctuation, and case. Maintain reviewed exact commands including `5`/`۵`/`٥` and agreed Persian/English stop words. Avoid broad substring matching that could classify normal conversations as opt-out.

## Opt-out transaction

1. Resolve seller and normalize customer mobile.
2. Lock/upsert `customer_sms_preferences` for seller/mobile.
3. Set marketing opt-out and record source inbound ID/time/parser rule.
4. Cancel all seller marketing recipients not yet submitted.
5. Commit.
6. Ensure dispatch pipeline re-checks preference immediately before provider call.

Opt-out is seller-scoped: replying to Seller A's line does not opt the customer out of Seller B.

## Classification

Launch features with marketing content obey opt-out. Pure relationship confirmations may use a reviewed classification, but promotions cannot be disguised as transactional. Document feature classification centrally.

## Privacy and retention

Encrypt/restrict raw inbound content, mask mobiles in logs/UI by role, record access, and apply retention policy. Do not use inbound content for unrelated analytics without policy/consent.

## Acceptance tests

- `5`, `۵`, and `٥` normalize to the same command.
- Exact parser avoids false-positive substring matches.
- Same inbound provider ID processes once.
- Destination routes opt-out to correct seller only.
- Unknown destination cannot alter preferences.
- Already queued, not-submitted marketing is canceled.
- Last-moment dispatch preference check blocks racing sends.

## Done checklist

- [ ] Per-account checkpoint and unique inbox constraint deployed.
- [ ] Seller-line routing and operations dead-letter queue active.
- [ ] Reviewed commands/classification policy configured.
- [ ] All marketing dispatch paths perform final opt-out check.
