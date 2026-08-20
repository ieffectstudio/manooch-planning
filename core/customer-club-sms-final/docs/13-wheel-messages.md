# Wheel invitation and winner messages

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature keys

- `wheel.invitation`
- `wheel.winner`

## Launch outcome

Invite eligible customers to a seller wheel with a secure link and send a confirmation after a server-committed winning spin.

## Prerequisites

Server-authoritative wheel/spin service, signed-link service, points/prize/redemption ledger, verified sender/templates, customer/consent service, outbox/reports.

## Wheel invariants

- Wheel belongs to seller and is active/in period.
- 2–8 prizes.
- Chances total exactly 100% server-side.
- Daily spin cap enforced.
- Entry cost and participation/reward points are distinct.
- Monetary entry is not enabled in this launch plan.

## Invitation flow

1. Validate seller wheel and audience ownership.
2. Generate signed, expiring, seller/wheel/customer-scoped link.
3. Apply consent/cap/business-hour rules.
4. Queue with `wheel-invite:{wheelId}:{customerId}:{campaignRunId}`.
5. Render `name`, `title`, `link`, `points`, `store_name`.
6. Unique links normally require many-to-many.

## Spin transaction

1. Validate link/customer/wheel and acquire spin idempotency lock.
2. Check active state, daily cap, and entry eligibility.
3. Deduct configured points cost if applicable.
4. Select outcome with secure server randomness from persisted chances.
5. Persist prize snapshot and unique redemption code if required.
6. Apply participation/reward points exactly once.
7. Insert `wheel.winner` outbox using spin ID.
8. Commit.

Idempotency: `wheel-spin:{spinCommandId}` and `wheel-winner:{spinId}`.

## Winner dispatch

Render `name`, `prize`, `code`, `date`, `store_name` from committed spin/prize data. Send one-to-many with one destination. Never send before transaction commit.

## Failure/resend

SMS failure does not reroll, re-award, re-deduct, or issue a new code. A controlled resend references the same spin and code.

## Acceptance tests

- Duplicate spin command creates one outcome/effect/message intent.
- Chance total and prize constraints are server-enforced.
- Disabled/ended wheel blocks invitation/spin.
- Invitation links cannot cross customer/seller/wheel.
- Winner body matches persisted prize snapshot.
- Resend reuses original redemption code.

## Done checklist

- [ ] Browser wheel randomness removed from authoritative flow.
- [ ] Spin/points/prize/outbox atomic transaction tested.
- [ ] Signed invitation links implemented.
- [ ] Invitation/winner reports use provider references.
