# Seller-owned dynamic templates

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Scope

Launch-safe features use application-managed text templates rendered before calling Armaghan's documented free-form endpoints. Every active template belongs to one seller and one feature.

## Canonical variables

| Key | Meaning |
|---|---|
| `name` | customer name |
| `points` | points amount |
| `balance` | resulting/current balance |
| `credit` | retargeting credit |
| `date` | localized date |
| `days` | inactivity days |
| `discount_code` | an actually created code |
| `link` | signed short link |
| `title` | campaign/survey/wheel title |
| `prize` | committed wheel prize |
| `item` | redeemed club item |
| `code` | redemption/reference code |
| `occasion` | occasion title |
| `store_name` | seller store name |

Use English canonical keys internally and localize labels only in the UI.

## Template record

```json
{
  "sellerId":"seller_1",
  "featureKey":"member.welcome",
  "name":"خوش‌آمدگویی",
  "body":"{name} عزیز، به باشگاه {store_name} خوش آمدید…",
  "allowedVariables":["name","store_name","points"],
  "requiredVariables":["name","store_name"],
  "version":3,
  "isActive":true
}
```

## APIs

```http
GET  /api/sellers/me/sms/templates?featureKey=...
POST /api/sellers/me/sms/templates
PUT  /api/sellers/me/sms/templates/:id
POST /api/sellers/me/sms/templates/:id/preview
POST /api/sellers/me/sms/templates/:id/test
```

All operations verify seller ownership and the feature-specific variable allowlist.

## Rendering rules

1. Parse only `{canonical_key}` tokens; never evaluate code.
2. Reject unknown tokens.
3. Reject missing required values.
4. Normalize/strip unsafe control characters from values.
5. Render from committed server data, not browser-submitted balance/reward values.
6. Append seller signature.
7. Reject unresolved `{...}` tokens.
8. Enforce 320 characters on the final body.
9. Store template version/body and final-body snapshot/hash with the outbox.

## Template lifecycle

Editing creates a new version. Scheduled/queued messages keep the approved snapshot they were created with. Deactivation blocks new queue creation but does not rewrite history.

## Batch selection

- Equal final bodies: one-to-many.
- Different final bodies because of customer variables/links: many-to-many.
- Filter recipients before building arrays, then build `contents` and `destinations` from the same recipient objects.

## Security and correctness

- Template ID from browser must resolve under current seller.
- Links must be signed and seller-scoped.
- A `discount_code` can be rendered only after the commerce system creates it.
- Financial/points/prize values come from transaction snapshots.
- Preview uses sample values and is clearly marked as preview.

## Acceptance tests

- Cross-seller template access fails.
- Unknown/missing variables block sending.
- Final length includes signature.
- Editing does not alter queued/history messages.
- Personalized content stays aligned with destinations.
