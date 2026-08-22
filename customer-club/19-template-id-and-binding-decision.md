# Template ID and binding decision

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Direct answer

**No—each launch-safe customer-club feature does not need a template created in the Armaghan panel, and it does not need an Armaghan template ID.**

The launch plans in this folder use Armaghan's documented free-form operations:

- `sendMessageOneToMany`
- `sendMessageManyToMany`

These operations receive the seller's `originator` and the final rendered `content`/`contents`. They do not receive a template ID.

## Two different meanings of “template”

### 1. Application template — required for enabled features

This template is stored in the customer-club database:

```text
seller_id + feature_key + body + variables + version + active state
```

Example:

```json
{
  "sellerId": "seller_123",
  "featureKey": "member.welcome",
  "body": "{name} عزیز، به باشگاه {store_name} خوش آمدید. {points} امتیاز هدیه گرفتید.",
  "allowedVariables": ["name", "store_name", "points"],
  "version": 1,
  "isActive": true
}
```

The application renders it before calling Armaghan:

```json
{
  "username": "<secret>",
  "password": "<secret>",
  "originator": "<seller-approved-originator>",
  "content": "سارا عزیز، به باشگاه فروشگاه نمونه خوش آمدید. 100 امتیاز هدیه گرفتید.",
  "destinations": ["09120000000"]
}
```

No Armaghan template ID is used in this request.

### 2. Provider-approved template — optional and not used by the current launch-safe plans

This is a template created/approved in the Armaghan panel and executed with:

```text
POST /webservice/rest/v2/sendParameterizedMessage
```

Example:

```json
{
  "username": "<secret>",
  "password": "<secret>",
  "template": "<armaghan-template-id>",
  "parameters": ["123456"],
  "destinations": ["09120000000"]
}
```

Use this mode only when a provider-approved pattern is required, typically for OTP or another specifically approved transactional route.

## Why provider-template binding is different

The documented `sendParameterizedMessage` request has no `originator` property. Therefore the application cannot choose the seller sender line in that request. The provider template must already be associated with the correct sender/routing configuration in Armaghan.

If provider-template mode is introduced later, the safe assumption is:

- every seller/provider line needs its own approved provider template ID for that feature; or
- Armaghan must confirm in writing that one provider template ID can safely route multiple seller lines and explain how the originator is selected.

Do not share one provider template ID across sellers without that confirmation.

## Decision for the 14 launch-safe features

| Feature | App template | Armaghan template ID |
|---|---:|---:|
| Welcome/walk-in | Required | Not required |
| Manual campaigns | Required/snapshotted | Not required |
| Bulk SMS | Required/snapshotted | Not required |
| Personal messages | Required or composed body | Not required |
| Inactivity reminders | Required | Not required |
| Birthday/custom occasions | Required | Not required |
| Points expiry | Required | Not required |
| Retargeting notifications | Required | Not required |
| Referral messages | Required | Not required |
| Wheel invitation/winner | Required | Not required |
| Survey invitation/reminder | Required | Not required |
| Club-redemption confirmation | Required | Not required |
| Delivery reports | No outgoing template | Not required |
| Inbound opt-out | No outgoing template by default | Not required |

## Do we need to manually create an app template for every seller and feature?

Every **enabled** message feature needs an active seller-scoped application template, but it does not need to be manually typed from zero.

Recommended provisioning:

1. Maintain versioned platform default bodies for each feature key.
2. When a seller enables a feature, copy the current default into `seller_sms_templates` under that seller.
3. Let the seller edit their own copy.
4. Create a new version on every edit.
5. Snapshot the selected version when queueing a campaign/message.
6. Never read another seller's template as fallback.

This gives every seller an independent template without requiring provider-panel approval for each feature.

## Recommended schema

```sql
CREATE TABLE seller_sms_templates (
  id                  uuid PRIMARY KEY,
  seller_id           uuid NOT NULL,
  feature_key         varchar(80) NOT NULL,
  name                varchar(160) NOT NULL,
  body                varchar(320) NOT NULL,
  allowed_variables   jsonb NOT NULL,
  required_variables  jsonb NOT NULL,
  version             integer NOT NULL,
  is_active           boolean NOT NULL DEFAULT true,
  created_at          timestamptz NOT NULL,
  created_by          uuid NOT NULL,
  UNIQUE (seller_id, feature_key, version)
);
```

Enforce one active version per seller/feature with a partial unique index or transactional activation logic.

## Runtime selection

```ts
const seller = await requireSeller(sellerId);
const sender = await requireVerifiedDefaultSender(sellerId);
const template = await requireActiveAppTemplate(sellerId, featureKey);
const content = renderAndValidate(template, variables); // includes signature and 320 limit

await armaghan.sendOneToMany({
  originator: sender.originator,
  content,
  destinations
});
```

For customer-specific rendered bodies:

```ts
await armaghan.sendManyToMany({
  originator: sender.originator,
  contents: recipients.map(r => renderAndValidate(template, r.variables)),
  destinations: recipients.map(r => r.mobile)
});
```

## Configuration rule

For the current launch:

```text
seller sender line      → seller_sender_lines.originator
seller feature template → seller_sms_templates.body/version
provider template ID    → not used
```

The supplied `ARMAGHAN_OTP_TEMPLATE_ID` should not be read by any of these 14 launch-safe features. Keep it unused unless OTP/provider-template mode is deliberately added later.

## When to add a provider template ID later

Add fields such as `send_mode`, `provider_template_id`, `parameter_keys`, and `bound_sender_line_id` only when a feature is intentionally migrated to `sendParameterizedMessage`.

Before enabling it, confirm:

- provider template is approved;
- ordered parameters exactly match the provider panel;
- sender-line binding is known;
- cross-seller isolation is proven;
- errors `-160` and `-161` are handled;
- fallback to free-form mode is an explicit policy, not automatic.

## Final implementation decision

Use **application templates plus each seller's approved originator** for all current launch-safe features. Do not create or bind 14 Armaghan template IDs per seller. This keeps the current implementation fully aligned with `sendMessageOneToMany` and `sendMessageManyToMany` in the attached provider documents.
