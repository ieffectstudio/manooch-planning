# Survey invitation and reminder messages

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature keys

- `survey.invitation`
- `survey.reminder`

## Launch outcome

Send each eligible customer a secure survey-response link, record one allowed response, grant configured response points once, and remind only non-respondents.

## Prerequisites

Seller survey service, signed token/link service, response store, optional points ledger, audience/consent service, scheduler, verified sender/templates, outbox/reporting.

## Survey invariants

- Survey belongs to seller.
- 2–6 valid options.
- Active/scheduled state allows invitations.
- Audience belongs to seller.
- Reward is configured and available before copy promises it.

## Invitation flow

1. Create a survey run and snapshot question/options/audience/template.
2. Resolve and deduplicate eligible seller recipients.
3. Create one random/signed token scoped to seller, survey, run, and customer.
4. Build response URL and recipient variables.
5. Queue once with `survey-invite:{surveyRunId}:{customerId}`.
6. Render `name`, `title`, `link`, `date`, `store_name`, optional `points`.
7. Unique links require many-to-many.

## Response endpoint

```http
GET  /public/surveys/:token
POST /public/surveys/:token/responses
```

Response transaction:

1. Verify token signature/hash, expiry, seller/survey/run/customer scope.
2. Verify option belongs to snapshotted survey.
3. Enforce one response according to policy.
4. Insert response.
5. If reward configured, insert points ledger entry once.
6. Commit.

Unique reward key: `(survey_id, customer_id, 'response_reward')`.

## Reminder scheduler

At configured due time, lock reminder run and select original invited recipients with no accepted response. Re-check survey active state, opt-out, mobile validity, caps, and business hours. Queue `survey-reminder:{surveyRunId}:{customerId}:{reminderNumber}`.

## Failure behavior

Invitation SMS failure does not create a response/reward. Reward failure rolls back the response transaction only according to defined product policy; preferred design commits response+reward atomically. Reminder provider failure does not reopen survey.

## Acceptance tests

- Tokens cannot cross seller/survey/customer or be guessed from IDs.
- One response and one reward maximum.
- Respondents are excluded from reminders despite audience changes.
- Ended survey blocks new invitations/responses per status policy.
- Unique links remain aligned with destinations.
- Seller report derives invite/delivery/response counts from real rows.

## Done checklist

- [ ] Token expiry/authorization tests pass.
- [ ] Response/reward uniqueness deployed.
- [ ] Non-respondent query uses original run recipients.
- [ ] Invite/reminder/delivery/response funnel visible.
