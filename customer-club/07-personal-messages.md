# Personal/direct messages

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`personal.direct`

## Launch outcome

Send an audited message to one seller customer or a manually entered authorized mobile. If the UI selects a segment, delegate to the bulk pipeline instead of bypassing bulk controls.

## Recipient modes

### Customer

Browser submits internal customer ID; server loads seller-owned customer/mobile/variables.

### Manual mobile

Server normalizes and validates number, records operator and reason, and limits available variables to seller/store values. Manual entry does not silently create a customer.

### Segment

Create a bulk run with the selected seller segment and all bulk eligibility/deduplication controls.

## APIs

```http
POST /api/sellers/me/sms/personal/preview
POST /api/sellers/me/sms/personal/send
GET  /api/sellers/me/sms/personal/history
```

```json
{
  "recipient":{"type":"customer","customerId":"cus_123"},
  "templateId":"tpl_123",
  "clientCommandId":"uuid"
}
```

## Flow

1. Derive seller and actor from authentication.
2. Verify recipient and template ownership.
3. Load current opt-out, daily cap, and business-hours state.
4. Build variables from server records.
5. Render final body, append signature, validate 320 characters.
6. Insert outbox with `personal:{sellerId}:{clientCommandId}`.
7. Worker calls one-to-many with a one-item destination list.
8. Save provider reference and display delivery status.

Avoid the provider's GET one-to-one method because credentials and message text would be placed in URL query strings.

## Consent and classification

Default direct seller messages to marketing rules unless a reviewed transactional reason/classification is explicitly selected. Support staff must not label promotions as transactional. Opt-out is checked at dispatch again.

## Saved messages

Store reusable personal texts as seller template versions. Create/edit/delete preserves historical snapshots. Customer-required variables cannot be used for manual-mobile mode.

## Failure/resend

A controlled resend creates a new command referencing the original message and requires the same eligibility checks. Ambiguous attempts are not automatically resent.

## Acceptance tests

- Customer ID from another seller is rejected.
- Manual mode rejects unresolved customer variables.
- Segment mode uses bulk dedupe/caps/credit/history.
- Marketing opt-out blocks direct promotional sends.
- Replayed client command ID creates one outbox.
- Complete mobile/message text is absent from logs.

## Done checklist

- [ ] All three UI modes route to correct backend path.
- [ ] Actor/reason audit retained for manual destinations.
- [ ] Saved-message ownership/versioning implemented.
- [ ] Delivery state visible from customer history.
