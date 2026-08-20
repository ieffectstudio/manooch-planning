# Referral messages

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Feature keys

- `referral.invitation`
- `referral.rewarded`

## Launch outcome

Send seller-branded referral invitations containing a secure seller-scoped link, and notify participants after a validated reward is committed.

## Prerequisites

Referral-code/link service, seller customer data, reward/points ledger, abuse controls, first-purchase validation when configured, verified sender/templates, consent/outbox/reporting.

## Records

`referrals`: seller, inviter, code/token hash, invitee/mobile hash, state, qualification event, timestamps.

`referral_rewards`: referral, beneficiary customer, points/value, ledger reference, unique reward type.

`referral_invites`: referral/inviter/destination/day, outbox/message state.

## Invitation API and flow

```http
POST /api/sellers/me/referrals/invitations
```

1. Authenticate seller/inviter ownership.
2. Normalize destination and reject self-referral.
3. Enforce inviter/destination/IP daily limits and opt-out rules.
4. Create/reuse a seller-scoped referral token and signed expiring URL.
5. Queue invitation using:

```text
referral-invite:{sellerId}:{inviterId}:{mobileHash}:{localDate}
```

6. Render `name`, `link`, `store_name`, and promised `points` only when configured.

## Qualification/reward flow

On registration or validated first completed purchase:

1. Resolve token under seller.
2. Verify identity/mobile uniqueness and anti-self-referral rules.
3. Lock referral and confirm it has not qualified.
4. Atomically insert inviter/invitee ledger rewards once.
5. Mark referral qualified.
6. Insert `referral.rewarded` outbox events.
7. Commit and dispatch after commit.

Idempotency: `(referral_id, beneficiary_id, reward_type)`.

## Provider routing

Single invitation uses one-to-many with one destination. Batches with inviter/invitee-specific names/links use many-to-many. Always use the originating seller's configured line/template.

## Failure behavior

SMS failure does not duplicate/reverse rewards. Controlled resend reuses the same token/reward snapshot. Expired/revoked links fail safely.

## Acceptance tests

- Cross-seller token cannot resolve.
- Self-referral, repeated identity, and daily-cap abuse are blocked.
- One qualification awards each configured party at most once.
- First-purchase reward requires completed/paid seller order.
- Copy does not promise unconfigured points/discount.
- Provider retry does not change referral/reward state.

## Done checklist

- [ ] Signed-link expiry and tenant tests pass.
- [ ] Fraud/rate-limit policy enabled.
- [ ] Reward/outbox transaction is atomic.
- [ ] Invitation and reward history show provider state.
