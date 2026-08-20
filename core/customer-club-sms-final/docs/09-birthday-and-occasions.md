# Birthday and custom occasions

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature keys

- `occasion.birthday`
- `occasion.custom`

## Launch outcome

Send one birthday greeting per customer/year and execute dated seller occasions with a seller-owned audience, time, template, and real history.

## Prerequisites

Verified sender/templates, customer birthday data with defined calendar semantics, scheduler/timezone utilities, audience/consent service, optional commerce discount service.

## Records

`occasions`: seller, type, title, canonical date/recurrence, local send time, timezone, audience, template version, active flag.

`occasion_runs` and `occasion_recipients`: date snapshot, eligibility, exclusion, outbox/reference state.

## APIs

```http
POST /api/sellers/me/occasions
PUT  /api/sellers/me/occasions/:id
PUT  /api/sellers/me/occasions/:id/status
POST /api/sellers/me/occasions/:id/preview
GET  /api/sellers/me/occasions/:id/history
```

Birthday is a seeded system occasion: disable/edit template is allowed; deletion is not.

## Birthday scheduler

1. For each due seller local day/time, lock birthday run.
2. Select seller customers whose canonical birthday matches local date.
3. Apply configured leap-day/calendar policy.
4. Filter consent/validity/caps.
5. Render seller birthday template.
6. Queue once with:

```text
birthday:{sellerId}:{customerId}:{localYear}
```

## Custom occasion scheduler

Require concrete canonical date and local time before activation. At due time, snapshot and resolve audience, filter, render, and dispatch like a manual campaign. Idempotency: `occasion:{occasionId}:run:{scheduledInstant}:recipient:{customerId}`.

## Variables

`name`, `occasion`, `date`, `store_name`, `link`, and `discount_code` only after commerce creates a valid seller code. Do not send prototype discount percentages without a real redemption path.

Personalized bodies use many-to-many; identical seller announcement bodies use one-to-many.

## Calendar rules

Persist canonical dates, not formatted Persian strings. Define source calendar for customer birthdates, conversion to display calendar, timezone boundary, and leap-day behavior. Add tests before activation.

## Failure/reporting

A run retains selected/excluded/accepted/delivery counts. Provider failure does not recreate discounts or change customer birthdays. Controlled retry skips accepted/unknown recipient attempts.

## Acceptance tests

- Birthday sends once per seller/customer/local year.
- Missing/invalid birthdays are skipped with reason.
- Custom occasion cannot activate without date/time/template/audience.
- Cross-seller audiences/templates fail.
- Business-hour adjustment is deterministic and audited.
- No nonexistent discount code is rendered.

## Done checklist

- [ ] Calendar and leap-day policy approved.
- [ ] Daily scheduler lock deployed.
- [ ] Seeded birthday uniqueness deployed.
- [ ] Preview/history and provider states wired to UI.
