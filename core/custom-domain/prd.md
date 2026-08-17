# PRD — Connecting Customer Custom Domains to the Store Builder (v2)

**Version:** 2.0
**Date:** 2026-08-17
**Status:** Ready for implementation
**Primary change from v1:** Removed the dependency on "the customer changes their nameservers" as the main path. The primary path is now **CNAME / A Record**, and **Custom Nameservers** have been deferred to a later phase as an optional capability.

---

## 1. Why v1 Was Rewritten

The previous version assumed the customer would point their domain's NS records at ArvanCloud (or at our own branded nameservers such as `ns1.manooch.site`). A review of ArvanCloud's documentation shows this path is not appropriate for a multi-tenant store builder:

| Limitation | Detail | Source |
|---|---|---|
| Custom NS requires a Professional/Enterprise plan | The "Nameserver personalization" feature in the ArvanCloud CDN panel is unavailable on lower plans | [docs.arvancloud.ir – Custom NS](https://docs.arvancloud.ir/en/cdn/dns-records/custom-ns) |
| Glue IPs must be registered at the registrar | ArvanCloud assigns IPs that must be registered as Glue Records at the registrar (IRNIC or an international registrar) | Same source |
| Account-level activation is manual | Applying custom NS across all domains requires opening a support request with ArvanCloud | Same source |
| CNAME Setup is Enterprise-only | ArvanCloud's SaaS-friendly mode (which also manages the SSL lifecycle) is currently limited to the Enterprise plan | [docs.arvancloud.ir – CNAME Setup](https://docs.arvancloud.ir/en/cdn/domain/cname-setup) |
| NS delegation means handing over the entire zone | Changing NS puts the customer's **entire DNS zone** (email, MX, corporate records, third-party services) under our control — high responsibility and risk | Architectural decision |
| Sales friction | Many customers will not move the nameservers of their primary corporate domain | Architectural decision |

**Conclusion:** NS delegation is not the right tool for "connecting one host to our service"; it is the tool for "handing over complete DNS management." For a store builder, the correct approach is to have the customer create **a single record**.

---

## 2. Product Goal

Every store gets a default subdomain:

```text
reza.manooch.site
```

The customer must be able to connect their own domain:

```text
rezashop.ir
www.rezashop.ir
```

Once the custom domain is live:
- The custom domain becomes the store's **Primary Domain**.
- The old subdomain issues a **301** redirect to the custom domain.
- HTTPS is enabled automatically with zero manual intervention.

### Success Metrics (KPIs)
| Metric | Target |
|---|---|
| Time to connect from the moment the customer creates the record | < 15 minutes in 90% of cases |
| Automatic SSL issuance success rate | > 95% |
| Support tickets per 100 domain connections | < 10 |
| Operator time required per domain on our side | Zero (fully automated) |

---

## 3. Architectural Decision

### Primary path for v1: **Record-based Connection**

The customer keeps their own DNS and nameservers, and only creates the following record:

```text
# Recommended (subdomain)
shop.rezashop.ir.   CNAME   connect.manooch.site.

# Root domain (apex)
rezashop.ir.        A       <ORIGIN_IP>
www.rezashop.ir.    CNAME   connect.manooch.site.
```

`connect.manooch.site` is a stable host we own that points to our Origin/CDN. The advantage: if our server IP ever changes, **no customer has to do anything** — we simply update the `connect` record.

> ⚠️ **DNS constraint:** A CNAME cannot be placed on a root domain (apex). For apex we use an `A` record, or — if the customer's DNS provider supports `ALIAS`/`ANAME`/CNAME flattening (ArvanCloud offers `ANAME`) — that instead.
> For this reason we must reserve **two stable, permanent IPs** for Origin and treat them as part of the product contract.

### Supported Methods (in priority order)

| # | Method | Who controls DNS | SSL | Phase |
|---|---|---|---|---|
| A | CNAME to `connect.manooch.site` | Customer | Automatic (ACME on our server) | **MVP** |
| B | A Record to our IP (for apex) | Customer | Automatic (ACME on our server) | **MVP** |
| C | Full NS delegation to ArvanCloud | Us | ArvanCloud / ACME | Phase 2 (optional, for customers who want it) |
| D | ArvanCloud CNAME Setup (Enterprise) | Customer | ArvanCloud | Phase 3 (depends on plan upgrade) |
| E | Branded Custom Nameservers (`ns1.manooch.site`) | Us | Us | Phase 4 (white-label; requires Enterprise plan + Glue) |

---

## 4. Technical Architecture

```text
Customer Domain (rezashop.ir)
        ↓  A / CNAME  (customer's own DNS)
   [ Our Edge / Origin ]
        ↓
      Nginx  (default_server + dynamic SNI cert)
        ↓  Host header
      Next.js / NestJS
        ↓
   Domain Resolver (cache + DB)
        ↓
      Store (store_id)
```

### 4.1 Nginx Layer

Nginx must accept any unknown Host and dynamically serve the correct certificate.

```nginx
# ---------- HTTP: ACME challenge and redirect only ----------
server {
    listen 80 default_server;
    server_name _;

    # The ACME path must never be redirected
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/acme;
        default_type "text/plain";
        try_files $uri =404;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# ---------- HTTPS: accept all domains ----------
server {
    listen 443 ssl http2 default_server;
    server_name _;

    # Fallback certificate until the per-domain cert is issued
    ssl_certificate     /etc/ssl/manooch/fallback/fullchain.pem;
    ssl_certificate_key /etc/ssl/manooch/fallback/privkey.pem;

    # Dynamic certificate selection based on SNI
    ssl_certificate_by_lua_block { require("cert_resolver").resolve() }  # OpenResty
    # Alternative without Lua: use Caddy, or have a service write per-domain config files

    location / {
        proxy_pass http://127.0.0.1:3000;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;

        proxy_http_version 1.1;
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

> **Strong recommendation:** Instead of Nginx plus custom scripting, use **Caddy** or **Traefik** with `on-demand TLS`. Both automatically obtain and store a certificate for any new domain on its first TLS handshake, gated by an "ask" endpoint that queries our API: "is this domain allowed?" This removes several hundred lines of code and a great deal of operational failure surface.

Sample Caddyfile:

```caddy
{
    on_demand_tls {
        ask http://127.0.0.1:3000/internal/tls/allow
        interval 2m
        burst 5
    }
}

:443 {
    tls {
        on_demand
    }
    reverse_proxy 127.0.0.1:3000 {
        header_up Host {host}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

The `/internal/tls/allow?domain=rezashop.ir` endpoint must return `200` only for domains present in `store_domains` with status `dns_verified` or `active`, and `403` for everything else. **Without this guard, anyone can point their domain at your IP and force you to issue unlimited certificates, burning your ACME rate limits.**

### 4.2 SSL Layer

| Topic | Decision |
|---|---|
| CA | Let's Encrypt (primary) + ZeroSSL (fallback) |
| Validation method | HTTP-01 for customer domains (requires CA access to port 80) |
| Wildcard for our main domain | `*.manooch.site` via DNS-01 using the ArvanCloud API |
| Renewal | Automatic, 30 days before expiry, via a daily job |
| Storage | Certificates in a shared DB/Object Storage, not just local disk (required for horizontal scaling) |

> 🔴 **Critical risk (must be validated in Phase 0):** Due to sanctions, certificate issuance from international CAs against Iranian IPs is intermittently disrupted. Before any development begins, Phase 0 = obtain a real Let's Encrypt certificate on the current server IP. If it fails, fallback options:
> 1. Use ArvanCloud's own SSL capability (certificate issued at the CDN edge rather than at Origin)
> 2. Proxy the ACME flow through a VPS outside Iran for the validation step only
> 3. Purchase a certificate from a domestic CA for the domestic market (caveat: it will not be trusted by international browsers)

### 4.3 Domain Resolver

```ts
// NestJS Middleware — runs on every request
async resolve(host: string): Promise<ResolvedTenant> {
  const normalized = host.toLowerCase().split(':')[0].replace(/^www\./, '');

  // 1. L1 cache (in-memory, TTL 60s)
  // 2. L2 cache (Redis, TTL 5m)
  // 3. Database

  // If it is one of our own subdomains:
  //   - store has an active Primary Domain → 301
  //   - otherwise → render the store
  // If it is a custom domain:
  //   - active → render the store
  //   - inactive/unknown → branded 404: "This domain is not connected to a store"
}
```

Key rules:
- **Cache invalidation** on any domain status change is mandatory (Redis pub/sub).
- An unknown domain must never return a 500; it must return a branded guidance page.
- Internal health checks and `/internal/*` endpoints must bypass the Resolver.

---

## 5. Data Model

### `stores`
```text
id
name
subdomain            -- reza
primary_domain_id    -- FK → store_domains.id (nullable)
```

### `store_domains`
```text
id
store_id
domain               -- rezashop.ir   (lowercase; punycode for IDN domains)
type                 -- custom | subdomain
connection_method    -- cname | a_record | ns_delegation
status               -- pending_dns | dns_verified | issuing_ssl | active | failed | disabled
is_primary           -- boolean
verification_token   -- for TXT-based ownership verification
dns_verified_at
ssl_status           -- none | pending | active | renew_failed | expired
ssl_issued_at
ssl_expires_at
last_check_at
last_error           -- text (user-presentable message)
retry_count
created_at
updated_at
```

**Indexes:** `UNIQUE(domain)` — a domain must never map to two stores; `INDEX(status, last_check_at)` for background jobs.

### `domain_events` (Audit)
```text
id, store_domain_id, event, payload_json, created_at
```
Events: `submitted`, `dns_check_passed`, `dns_check_failed`, `ssl_issued`, `ssl_renewed`, `ssl_failed`, `set_primary`, `removed`

---

## 6. Connection Flow (State Machine)

```text
pending_dns
   │  (correct record observed)
   ▼
dns_verified
   │  (ACME request)
   ▼
issuing_ssl
   │  (certificate issued)
   ▼
active ──► (user sets as primary) ──► primary
   │
   └─► failed (with message and a "Retry" button)
```

### Detailed Steps

**1. Customer submits the domain**
Path: `Settings → Domains → Add Domain`
Server-side validation: domain format, not a `manooch.site` domain, not already in the table, not on the blocklist.

**2. Show the record to the customer** — exactly one record, with a copy button.

**3. DNS check** (automatic every 30s for 15 minutes, then exponential backoff up to 72 hours, plus a "Check now" button)
- Resolve directly against several public resolvers (`8.8.8.8`, `1.1.1.1`, `178.22.122.100`) to avoid cache issues.
- Compare the observed CNAME value or IP against the expected values.

**4. SSL issuance** — job queue (BullMQ) with exponential retry. Max 5 attempts, then `failed`.

**5. Activation** — status becomes `active`. The customer can now click "Set as primary domain."

**6. Subdomain redirect** — enabled only after the domain is `active` and set as primary.

---

## 7. Redirect Rules

| From | To | Code | Condition |
|---|---|---|---|
| `reza.manooch.site/*` | `https://rezashop.ir/*` | 301 | Store has an active Primary Domain |
| `http://rezashop.ir/*` | `https://rezashop.ir/*` | 301 | Always |
| `www.rezashop.ir/*` | `https://rezashop.ir/*` | 301 | Per the customer's canonical choice |
| `rezashop.ir/*` | — | 200 | Render directly |

Hard rules:
- Redirects happen in **exactly one layer** (the application). Nginx handles only `http→https`.
- `/.well-known/acme-challenge/*` is **never** redirected.
- Full path and query string must be preserved.
- Redirect-loop test in CI: every active domain must reach a 200 within at most 1 hop.
- Do **not** enable the redirect until the target domain's SSL is `active` — otherwise all store traffic lands on a certificate error page.

---

## 8. User Experience

### State 1 — Add domain
```text
┌──────────────────────────────────────────────┐
│  Add Custom Domain                           │
│                                              │
│  Your domain:  [ rezashop.ir           ]     │
│                                              │
│  ○ Use the root domain (rezashop.ir)         │
│  ○ Use a subdomain (shop.rezashop.ir)        │
│                                              │
│                       [ Continue ]           │
└──────────────────────────────────────────────┘
```

### State 2 — Show the record
```text
┌──────────────────────────────────────────────┐
│  Create one record in your DNS panel         │
│                                              │
│  Type    Name       Value                    │
│  ─────   ─────────  ───────────────────────  │
│   A       @         185.xx.xx.xx      [copy] │
│   CNAME   www       connect.manooch.site[copy]│
│                                              │
│  ⏳ Waiting for DNS propagation…              │
│     Last checked: 12 seconds ago             │
│                                              │
│  ⓘ You do NOT need to change your domain's   │
│    nameservers. Your email and other domain  │
│    services stay exactly as they are.        │
│                                              │
│              [ Check again ]                 │
└──────────────────────────────────────────────┘
```

### State 3 — Progress
```text
✅ DNS record verified
🔄 Issuing SSL certificate… (usually under 2 minutes)
⬜ Activating domain
```

### State 4 — Success
```text
✅ rezashop.ir is connected
✅ SSL is active — valid until 2026-11-17 (auto-renews)

[ Set as the store's primary domain ]

After this, reza.manooch.site will automatically
redirect to rezashop.ir.
```

### State 5 — Errors (human-readable messages, not technical logs)
| Error | Message shown to customer |
|---|---|
| Record not found | "We don't see a record for this domain yet. If you just created it, please allow up to 30 minutes." |
| Record points elsewhere | "This domain currently points to a different address: 93.x.x.x — please correct the record." |
| CAA blocks issuance | "Your domain's CAA settings prevent certificate issuance. Add the record `0 issue \"letsencrypt.org\"`." |
| Domain already registered | "This domain is connected to another store. Please contact support." |

---

## 9. Internal API

```http
POST   /api/v1/stores/:storeId/domains          # Add a domain
GET    /api/v1/stores/:storeId/domains          # List
GET    /api/v1/domains/:id                      # Detail + live status
POST   /api/v1/domains/:id/verify               # Manual DNS check
POST   /api/v1/domains/:id/retry-ssl            # Retry certificate issuance
POST   /api/v1/domains/:id/set-primary          # Set as primary domain
DELETE /api/v1/domains/:id                      # Remove
GET    /internal/tls/allow?domain=              # For Caddy/Traefik only, bound to localhost
```

Sample `GET /api/v1/domains/:id` response:
```json
{
  "id": 91,
  "domain": "rezashop.ir",
  "status": "issuing_ssl",
  "connection_method": "a_record",
  "is_primary": false,
  "dns": {
    "expected": [{ "type": "A", "name": "@", "value": "185.x.x.x" }],
    "observed": [{ "type": "A", "value": "185.x.x.x" }],
    "matched": true,
    "checked_at": "2026-08-17T09:12:03Z"
  },
  "ssl": { "status": "pending", "expires_at": null },
  "message": "Issuing SSL certificate"
}
```

---

## 10. Background Jobs

| Job | Interval | Responsibility |
|---|---|---|
| `dns-poller` | Every 30s | Checks `pending_dns` domains (with backoff) |
| `ssl-issuer` | Event-driven queue | Issues certificates for `dns_verified` domains |
| `ssl-renewer` | Daily at 03:00 | Renews certificates expiring in < 30 days |
| `domain-healthcheck` | Every 6h | For `active` domains: does it still point to us? If not for 72h → alert the owner |
| `cert-sync` | Every 5 min | Syncs certificates across nodes (once there is more than one server) |

---

## 11. Security

| Risk | Control |
|---|---|
| Domain takeover / connecting someone else's domain | `UNIQUE(domain)` + require a TXT ownership record for sensitive domains |
| On-Demand TLS abuse | The `ask` endpoint approves only registered domains |
| Burning certificate rate limits | Max 5 attempts per domain per day + a global cap on issuances per hour |
| Host header injection | Strict whitelist; invalid Host → 421 or a static page |
| Redirect loops | Automated tests + the single-redirect-layer rule |
| Cookie/session leakage across tenants | Cookies scoped to each tenant's exact `Domain`; never a wildcard `.manooch.site` |
| External access to `/internal/*` | Bind to loopback + block in Nginx/Caddy |

---

## 12. SEO and Migration

- Redirects must be **301**, never 302.
- `<link rel="canonical">` pointing at the Primary Domain.
- `sitemap.xml` and `robots.txt` generated with the Primary Domain.
- The old subdomain must **never be removed** — keep the redirect indefinitely (old links and bookmarks).
- Prompt the customer in the UI, after connection, to register the domain in Google Search Console and submit a Change of Address.

---

## 13. Delivery Roadmap

### Phase 0 — Risk validation (2–3 days) 🔴 before any code
1. Connect a test domain with an A record to the current server.
2. Attempt a real Let's Encrypt issuance against the Iranian server IP.
3. If it fails → decide on the fallback SSL path (section 4.2) **before** development starts.
4. Verify that ArvanCloud allows `/.well-known/acme-challenge/` to pass through.

**Phase 0 deliverable:** a one-page "definitive SSL path" document.

### Phase 1 — MVP (1.5–2 weeks)
1. `store_domains` and `domain_events` tables
2. Domain Resolver + two-layer cache in NestJS
3. Reverse proxy with On-Demand TLS (preferably Caddy)
4. `/internal/tls/allow` endpoint
5. `dns-poller` and `ssl-issuer`
6. Add-domain UI (the 5 states in section 8)
7. Primary Domain logic and 301 redirect
8. Manually connect one real domain as an end-to-end test

### Phase 2 — Stability (1 week)
9. `ssl-renewer` + `domain-healthcheck`
10. Human-readable error messages + retry buttons
11. Admin dashboard: all domains, statuses, manual actions
12. Alerting: renewal failures, lost domains, approaching rate limits

### Phase 3 — ArvanCloud automation (optional, 1 week)
13. Integrate the ArvanCloud API for customers who want to delegate DNS to us entirely (`NS Delegation`)
14. Automatic domain and record creation via `napi.arvancloud.ir/cdn/4.0/domains`

### Phase 4 — White-label / Custom NS (future, conditional)
15. Upgrade the ArvanCloud plan to Professional/Enterprise
16. Define `ns1.manooch.site` / `ns2.manooch.site` in the ArvanCloud panel and register Glue IPs at the registrar
17. Offer as a premium capability for enterprise customers

---

## 14. Out of Scope for v1

- Branded custom nameservers (deferred to Phase 4)
- Multiple simultaneously active domains for one store without redirect (multi-canonical)
- Managing customers' MX/email records
- Persian IDN domains (next phase; requires punycode testing)
- EV/OV certificates

---

## 15. Open Questions for the Team

1. How stable are the Origin IPs? Can we permanently reserve two IPs? (This is a prerequisite for the A-record method.)
2. Should customer-domain traffic also flow through the ArvanCloud CDN, or hit Origin directly? (Affects SSL and caching.)
3. Is there budget to upgrade the ArvanCloud plan to Enterprise? (Only then do CNAME Setup and Custom NS become possible.)
4. What is the expected maximum number of domains in year one? (Affects the certificate storage architecture.)
5. Do the stores have visitors outside Iran? (If yes, a domestic CA is not a viable option.)

---

## Appendix — Method Comparison at a Glance

| Criterion | CNAME/A (recommended) | NS Delegation | Custom NS |
|---|---|---|---|
| Customer effort | 1 record | Change NS at registrar | Change NS at registrar |
| Risk of breaking customer email | None | Yes | Yes |
| Our control over DNS | That host only | Full | Full |
| Cost | Zero | Zero | Professional/Enterprise plan |
| Requires glue records | No | No | Yes |
| Implementation complexity | Low | Medium | High |
| Suitable for multi-tenant SaaS | ✅ Yes | ⚠️ Partially | ⚠️ White-label only |
