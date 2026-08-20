# Inactivity reminders

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature key

`reminder.inactive`

## Launch outcome

Automatically message eligible seller customers after configured days since their last completed purchase, while enforcing the PRD's 30-day reminder suppression and business hours.

## Rule data

`reminder_rules`: seller, name, days (1–365), audience/segment, active flag, template version, send local time, business-hour behavior, suppression days (default 30), timestamps.

`reminder_deliveries`: rule, customer, eligibility window, outbox/message, accepted/delivery timestamps.

## Prerequisites

Completed/paid order data, customer/segment service, scheduler, seller timezone, consent, verified sender/template, outbox, reports.

## APIs

```http
POST /api/sellers/me/reminders
PUT  /api/sellers/me/reminders/:id
POST /api/sellers/me/reminders/:id/preview
PUT  /api/sellers/me/reminders/:id/status
GET  /api/sellers/me/reminders/:id/history
```

## Scheduler flow

1. Select active rules due in each seller's local timezone.
2. Acquire one lock for `(rule_id, local_run_date)`.
3. Query seller customers and last completed/paid order.
4. Apply rule threshold and selected audience.
5. Exclude invalid/opted-out/capped customers.
6. Exclude anyone with a reminder accepted in the prior suppression window.
7. Re-check no qualifying new purchase occurred.
8. Render `name`, `days`, `points`, `date`, `store_name`, and an actually created `discount_code` if configured.
9. Insert recipient outbox rows and dispatch personalized many-to-many batches.
10. Store accepted and final delivery history.

Idempotency:

```text
reminder:{ruleId}:{customerId}:{eligibilityWindowStart}
```

Use accepted-provider time for the 30-day suppression start by default, preventing repeated reminders while delivery status is delayed.

## Time semantics

Compute order ages and due runs in explicit seller timezone (`Asia/Tehran` standard). Do not use process-local date methods. Define whether “30 days” means calendar-day boundary or exact 30×24 hours; use one server-side policy consistently.

## Failure behavior

Provider failure does not alter order/customer data. Permanent recipient errors close that recipient attempt. Account errors pause the run. Unknown batches require review and no blind resend.

## Acceptance tests

- Only completed/paid seller orders affect last purchase.
- A new purchase before dispatch makes the customer ineligible.
- 30-day suppression survives rule edits and worker retries.
- Custom days outside 1–365 are rejected.
- Inactive rule/seller creates no outbox.
- Seller line/template is resolved per run.

## Done checklist

- [ ] Order query and timezone boundary tests pass.
- [ ] Rule lock and recipient idempotency deployed.
- [ ] Suppression reason appears in preview/history.
- [ ] Real send/delivery stats replace fixtures.
