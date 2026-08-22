# Basic delivery reports

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Scope

Use documented Armaghan reference IDs and `getMessageState` polling to replace prototype fixture counts with real submission and delivery states.

## Reference ingestion

For each successful provider batch:

1. Check `errorModel.errorCode == 0`.
2. Verify reference count matches destination count.
3. Store every reference as a string.
4. Map `references[n]` to the exact message/destination at index `n`.
5. Mark provider submission accepted.

A count mismatch is an operational integrity error and must not be silently ignored.

## Poller

```text
select nonterminal message references
  → group by provider account
  → configurable-size ID batches
  → POST /v2/getMessageState
  → match response by string id
  → monotonic state update
  → aggregate reports
```

## State mapping

| Provider | Internal | Terminal? |
|---:|---|---:|
| `0` | scheduled | no |
| `1` | sent | no |
| `2` | delivered | yes |
| `3` | not_delivered | yes |
| `4` | unknown | no/review after SLA |
| `5` | ready | no |
| `6` | canceled | yes |
| `-100` | reference_not_found | review |

Do not regress a terminal state due to an older/out-of-order poll. Define a poll SLA; after it expires, unresolved messages become internally `unknown_final` with audit details.

## Reporting API

```http
GET /api/sellers/me/sms/reports/summary?from=&to=
GET /api/sellers/me/sms/runs/:runId/report
GET /api/sellers/me/sms/messages/:id
```

Every query filters seller ID before date/run filters.

## Report counters

- gross selected;
- excluded by reason;
- queued;
- failed before provider acceptance;
- ambiguous submission;
- provider accepted;
- ready/scheduled/sent;
- delivered;
- not delivered;
- canceled;
- reference missing/unknown.

Expose denominator definitions. Delivery rate should normally be `delivered / terminal delivery outcomes` or another explicitly labeled business definition, never an unexplained fixture.

## Poll schedule

Poll recent accepted messages frequently, then back off as they age. Stop terminal rows. Keep batch size, interval, and maximum age configurable because provider limits/SLA are not included in attachments.

## Failure behavior

Provider polling errors do not overwrite message states. Account authentication/IP/service errors trigger operational alerts and circuit breaking. Store sanitized error code/timestamps.

## Acceptance tests

- Large-looking v2 references preserve exact digits as strings.
- References map correctly to personalized batch recipients.
- Out-of-order responses cannot regress terminal states.
- Unknown/not-found remain visible, not counted as delivered.
- Seller A cannot query Seller B run/message/reference.
- Report totals reconcile with recipient rows.

## Done checklist

- [ ] Reference count/order validation deployed.
- [ ] Poll worker, backoff, terminal policy configured.
- [ ] Dashboard and sheets use report API.
- [ ] Operational alerts for stuck/unknown/reference-missing enabled.
