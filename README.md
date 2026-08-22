# Customer Club → Armaghan SMS implementation package

**Status:** Final launch scope  
**Provider contract:** Attached Armaghan Webservice v2.4.1  
**Product source:** Customer Club PRD and prototype  
**Audience:** Backend engineers, reviewers, QA, DevOps, and coding agents such as Claude

This clean package contains only the SMS features that can be executed using the documented Armaghan free-form send, delivery-state, account-credit, and inbound-message operations. Unsupported product plans were removed.

## Start here

- Coding-agent instructions: [CLAUDE.md](CLAUDE.md)
- Persian Trello cards: [TRELLO_TODO_FA.md](TRELLO_TODO_FA.md)
- Final release verification: [Launch checklist](docs/18-launch-checklist.md)
- Template-ID answer: [Template ID and binding decision](docs/19-template-id-and-binding-decision.md)

## Shared implementation specifications

1. [Architecture and data model](docs/00-architecture-and-data-model.md)
2. [Armaghan v2 adapter](docs/01-armaghan-v2-adapter.md)
3. [Pre-provisioned seller sender configuration](docs/02-seller-sender-configuration.md)
4. [Seller-owned dynamic templates](docs/03-dynamic-template-management.md)
5. [Template ID and binding decision](docs/19-template-id-and-binding-decision.md)

## Executable feature plans

1. [Welcome and walk-in messages](docs/04-welcome-and-walk-in.md)
2. [Manual campaigns](docs/05-manual-campaigns.md)
3. [Bulk SMS](docs/06-bulk-sms.md)
4. [Personal/direct messages](docs/07-personal-messages.md)
5. [Inactivity reminders](docs/08-inactivity-reminders.md)
6. [Birthday and custom occasions](docs/09-birthday-and-occasions.md)
7. [Points-expiry notifications](docs/10-points-expiry.md)
8. [Retargeting notifications](docs/11-retargeting-notifications.md)
9. [Referral messages](docs/12-referral-messages.md)
10. [Wheel invitation and winner messages](docs/13-wheel-messages.md)
11. [Survey invitation and reminder messages](docs/14-survey-messages.md)
12. [Club-redemption confirmations](docs/15-club-redemption.md)
13. [Basic delivery reports](docs/16-delivery-reports.md)
14. [Inbound SMS and opt-out](docs/17-inbound-opt-out.md)

## Final template decision

The 14 features use seller-owned application templates and the seller's already-approved originator:

```text
sender line      → seller_sender_lines.originator
message template → seller_sms_templates.body/version
provider template ID → not required
```

The backend renders the final body and calls:

- `POST /webservice/rest/v2/sendMessageOneToMany` for the same final text;
- `POST /webservice/rest/v2/sendMessageManyToMany` for different text per recipient.

Do not create 14 Armaghan panel templates per seller for this scope.

## Runtime rule

Every send starts with a server-authoritative `sellerId`:

```text
feature event/API
  → seller/customer ownership check
  → recipient eligibility and opt-out check
  → seller's verified originator
  → seller's active template/version
  → final rendering and 320-character validation
  → transactional outbox and app-credit reservation
  → Armaghan v2 adapter
  → string provider references
  → delivery polling and seller-isolated reporting
```

Never trust a browser-supplied sender number, template ID, balance, reward, points amount, prize, customer ownership, or seller ID.

## Documented provider operations in scope

| Requirement | Operation |
|---|---|
| Same final text to many recipients | `POST /webservice/rest/v2/sendMessageOneToMany` |
| Different final text per recipient | `POST /webservice/rest/v2/sendMessageManyToMany` |
| Delivery state | `POST /webservice/rest/v2/getMessageState` |
| Provider-account credit | `POST /webservice/rest/v2/getUserInfo` |
| Incoming messages | `POST /webservice/rest/v2/getReceivedMessages` |

All originators are assumed to be already provisioned and approved in Armaghan before they are configured for a seller.

## Recommended implementation order

1. Architecture, migrations, tenant constraints, and outbox.
2. Armaghan adapter, error mapping, secret handling, and observability.
3. Seller sender-line configuration and test send.
4. Dynamic template rendering/versioning.
5. Welcome, personal message, and club-redemption single-recipient paths.
6. Manual and bulk campaign pipelines.
7. Scheduler-driven reminder, occasion, points-expiry, and retargeting paths.
8. Referral, wheel, and survey event/link flows.
9. Delivery polling/reporting.
10. Inbound polling and seller-scoped opt-out.
11. Full launch checklist and tenant-isolation tests.

## Security

The real credential supplied during planning is intentionally absent. Rotate it before development/staging use, store credentials in a secret manager, use backend-only POST calls, and redact credentials, complete phone numbers, complete message bodies, and security values from logs.
