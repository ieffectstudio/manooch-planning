# Manual campaigns

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`campaign.manual`

## Launch outcome

Allow a seller to define a named campaign, select a seller-owned audience, compose/select a template, optionally link an active seller wheel/survey, send now or schedule in store time, and inspect real delivery history.

## Prerequisites

Verified sender, active template, segment/customer query service, consent preferences, seller app-credit ledger, transactional outbox, `Asia/Tehran` timezone utilities, and delivery poller.

## Records

- `sms_campaigns`: seller, name, audience definition, status, schedule/timezone, sender/template snapshot, linked-tool snapshot.
- `sms_campaign_runs`: campaign, run time, counts, cost reservation, status.
- `sms_campaign_recipients`: run, customer/mobile hash, variables, exclusion/submission status.

Unique recipient key: `(run_id, normalized_mobile_hash)`.

## APIs

```http
POST /api/sellers/me/sms/campaigns/preview
POST /api/sellers/me/sms/campaigns
POST /api/sellers/me/sms/campaigns/:id/send
POST /api/sellers/me/sms/campaigns/:id/cancel
GET  /api/sellers/me/sms/campaigns/:id/report
```

Preview returns gross, eligible, excluded-by-reason, estimated units/cost, final sample body, and validation errors. It is not a credit reservation.

## Creation and execution

1. Authenticate seller and validate all audience/tool/template IDs belong to seller.
2. Snapshot template, sender, audience definition, linked tool, and variables.
3. For scheduled send, parse local input in seller timezone and persist both local/timezone and UTC instant.
4. At due time, lock one campaign run.
5. Resolve seller customers; normalize and deduplicate mobiles.
6. Re-check opt-out, invalid number, daily cap, business hours, and linked-tool availability.
7. Persist recipient/exclusion rows.
8. Reserve app credit for eligible messages.
9. Render final bodies from server data.
10. Equal bodies use one-to-many; personalized bodies use many-to-many.
11. Save provider references in recipient order and update run counts.

Idempotency per recipient:

```text
campaign:{campaignId}:run:{runId}:recipient:{customerOrMobileHash}
```

## Scheduling rule

Business hours are checked at actual dispatch. Recommended default: move an out-of-hours send to the next opening and record the adjustment. Canceling before submission releases reserved app credit.

## Failure and reporting

Separate: excluded, failed before provider, ambiguous timeout, provider accepted, sent, delivered, not delivered, and canceled. Never report prototype fixture percentages.

## Acceptance tests

- Cross-seller audience/template/tool IDs fail.
- Schedule conversion is correct around Tehran date boundaries.
- Duplicate workers cannot create a second run/recipient send.
- Opt-outs are checked again immediately before provider submission.
- Template edits after creation do not change the run snapshot.
- Cost reservation and release reconcile with actual eligible/submitted rows.

## Done checklist

- [ ] Preview and execute share the same eligibility service.
- [ ] Run/recipient locks and unique keys deployed.
- [ ] Immediate, scheduled, cancel, and report paths tested.
- [ ] Real delivery-state aggregation replaces fixtures.
