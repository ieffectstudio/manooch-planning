# Architecture and data model

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Scope

This shared design supports only the launch-safe features listed in the folder README. Armaghan is the transport; recipient selection, business events, scheduling, consent, per-seller credit, idempotency, and reports remain application responsibilities.

## Command contract

```ts
type LaunchFeatureKey =
  | 'member.welcome'
  | 'campaign.manual'
  | 'bulk.general'
  | 'personal.direct'
  | 'reminder.inactive'
  | 'occasion.birthday'
  | 'occasion.custom'
  | 'points.expiring'
  | 'retargeting.credit_granted'
  | 'retargeting.credit_expiring'
  | 'referral.invitation'
  | 'referral.rewarded'
  | 'wheel.invitation'
  | 'wheel.winner'
  | 'survey.invitation'
  | 'survey.reminder'
  | 'club.redeemed';

type SmsRecipient = {
  customerId?: string;
  mobile: string;
  variables: Record<string, string>;
};

type SmsCommand = {
  sellerId: string;                 // derived from auth/event ownership
  featureKey: LaunchFeatureKey;
  recipients: SmsRecipient[];
  templateId?: string;              // must belong to sellerId
  scheduledAt?: string;
  timezone: 'Asia/Tehran' | string;
  idempotencyKey: string;
  aggregate: { type: string; id: string };
};
```

## Required tables

### `seller_sms_profiles`

`seller_id`, `provider_account_id`, `default_sender_line_id`, `timezone`, business-hour start/end, daily customer cap, optional signature, `sms_enabled`, timestamps.

### `seller_sender_lines`

`id`, `seller_id`, string `originator`, label, `provider_status`, `is_default`, `is_active`, `verified_at`. Require unique `(seller_id, originator)` and one default active line per seller.

### `seller_sms_templates`

`id`, `seller_id`, `feature_key`, name, body, allowed/required variables, version, `is_active`, creator, timestamps. Require one active version per `(seller_id, feature_key)`.

### `sms_outbox`

`id`, seller, feature, aggregate, idempotency key, sender/template snapshots, scheduled time, state, attempts, ambiguous-timeout flag, timestamps. Unique `(seller_id, idempotency_key)`.

### `sms_messages`

One row per normalized destination: outbox, seller/customer, masked/encrypted destination, final-body hash or protected snapshot, provider reference **string**, submission/delivery state, error code, charge units, timestamps.

### `customer_sms_preferences`

Unique seller/mobile record with marketing opt-in/out, source, and timestamp. Consent is seller-scoped.

### `sms_suppressions`

Seller/customer/feature suppression key, start/end, reason. Used for reminder and frequency rules.

## Queue pipeline

1. Authorize seller and aggregate ownership.
2. Resolve verified default sender and active seller template.
3. Resolve server-side recipient IDs/segments.
4. Normalize Iranian mobiles into one canonical representation.
5. Deduplicate by normalized mobile.
6. Apply consent, validity, business hours, daily caps, and feature suppression.
7. Render every final body and add seller signature.
8. Enforce the final 320-character product limit.
9. Reserve seller application credit and insert outbox/messages transactionally.
10. Dispatch in configurable batches.
11. Save provider references in destination order.
12. Poll delivery states and update reports.

## Endpoint selection

- All final bodies equal: `sendMessageOneToMany`.
- Final bodies vary by recipient: `sendMessageManyToMany`.
- Keep `contents[n]` and `destinations[n]` aligned after filtering and batching.

## Idempotency and timeouts

The provider docs do not define an idempotency key. Prevent duplicates in the application before calling it. If a timeout happens after request transmission, mark the attempt `unknown`; do not blindly resend because the provider may have accepted it.

## Tenant boundaries

Every line, template, customer, segment, campaign, outbox row, message, and report query includes `seller_id`. Provider references and browser IDs are never authorization mechanisms.

## Completion criteria

- Transactional outbox enabled.
- Unique business idempotency keys defined per feature.
- Seller sender/template snapshots stored on each send.
- Opt-out checked both at queue creation and immediately before dispatch.
- Explicit `Asia/Tehran` scheduling used where applicable.
- Provider references stored as strings.
- Cross-seller integration tests pass for every resource.
