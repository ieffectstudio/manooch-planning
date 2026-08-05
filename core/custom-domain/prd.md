# Full Architecture & Design Explanation — Custom Domain for Storefront
> Feature: `@manooch-fronts/apps/admin/app/domain`
> Edge: Caddy (`manooch-backend/Caddyfile`) — single reverse proxy in front of all services on `manooch_net`
> Backend module: `manooch-backend/src/modules/store-domains/`
> Storefront resolution: `manooch-fronts/apps/storefront/middleware.ts`
> Status: Implemented (code) — operational enablement (DNS record + firewall) required before go-live
> Base Domain: `manooch.site`

---

## 1. Problem Statement (What the Seller Wants)

A seller has:
- **Custom domain owned by seller:** e.g. `sellerName.ir`, `sellerName.com`, or a subdomain like `shop.sellerName.ir`
- **Storefront subdomain (our platform):** `sellerName.manooch.site`

The seller wants: when anyone opens their custom domain, the site loads the same storefront that lives at `sellerName.manooch.site`.

**Key point:** No HTTP redirect. The domain must **serve** the storefront directly. Supported for **any TLD**, both **apex** (`sellerName.ir`) and **subdomain** (`shop.sellerName.ir`) forms.

---

## 2. High-Level Concept

1. **DNS Layer** — the seller adds **one DNS record** at their own registrar/DNS provider pointing at the platform. They keep control of the rest of their zone (email, other subdomains, etc.) — unlike a full nameserver handoff.
2. **Edge Layer** — the Caddy origin, reached directly (not through ArvanCloud), issues an SSL cert on-demand the first time a verified domain is hit.
3. **Application Layer** — `manooch-backend` maps the incoming domain to a store; the storefront app renders it.

> **Architecture history:** two earlier drafts of this PRD were superseded. The first proposed ArvanCloud as the DNS/CDN/SSL provider — never built. The second proposed full nameserver (NS) delegation to platform nameservers — built, but discovered to be broken in production (see §7, Incident) and abandoned before go-live because it (a) hands us the seller's *entire* DNS zone, silently breaking their email/MX and other records unless we re-host everything, and (b) still required manual per-domain provisioning — not actually automatic. The current, implemented model is **CNAME/A to a fixed platform target + Caddy on-demand TLS**, which is genuinely zero-touch on the ops side and leaves the seller's own DNS otherwise untouched.

---

## 3. DNS Strategy — One Record, Not a Nameserver Handoff

- **Subdomain** (`shop.sellerName.ir`): seller adds `CNAME shop → edge.manooch.site`.
- **Apex** (`sellerName.ir`): seller adds `A @ → <origin IP>` (a CNAME can't be used at the apex per DNS rules — a raw IP is required, or an `ANAME`/`ALIAS` record if their provider supports one, pointed at `edge.manooch.site`).
- `edge.manooch.site` is a **DNS-only** (non-proxied) `A` record pointing at the Caddy origin's public IP — a fixed target sellers CNAME to, so it can be repointed later without every seller re-configuring anything.
- The seller's other DNS records (MX, TXT, other subdomains) are untouched.

---

## 4. Step-by-Step Flow (Implemented)

**Step 1 — Seller registers the domain in the admin panel**
`@manooch-fronts/apps/admin/app/domain` → `DomainForm` → `POST /admin/stores/:storeId/domain { domain }` (`admin-store-domains.controller.ts` → `StoreDomainsService.register`). Validates format, rejects platform-reserved hosts (`DOMAIN_RESERVED`) and domains already claimed by another store (`DOMAIN_TAKEN`). Row created in `store_domains`, `status = PENDING`.

**Step 2 — Seller adds the DNS record**
The admin UI (`NameserverPanel`, showing CNAME + A-record fields) displays the CNAME target and the apex IP from `GET /admin/stores/:storeId/domain` → `getConfig`. The seller adds the appropriate record at their own DNS provider.

**Step 3 — Seller clicks "verify"**
`POST /admin/stores/:storeId/domain/verify` → `StoreDomainsService.verify`: resolves the domain's `A` records (`DnsLookupService.lookupA`, wraps `node:dns/promises.resolve4` — this single lookup transparently follows CNAME chains, so it validates both the subdomain-CNAME and apex-A cases) and checks whether any resolved IP is in the configured origin-IP set. Flips `status` to `VERIFIED` or `FAILED`. 10-second cooldown between checks (`DOMAIN_VERIFY_TOO_SOON`). Dev/test bypass via `DOMAIN_VERIFY_FAKE=true`.

**Step 4 — Request reaches the Caddy origin directly**
Once the record resolves, the browser's HTTPS request for the seller's domain goes straight to the Caddy origin's IP (not through ArvanCloud, since ArvanCloud only proxies `*.manooch.site`).

**Step 5 — On-demand TLS cert issuance, gated**
Caddy has no static site block for an arbitrary seller domain, so it falls back to **on-demand TLS**, asking its internal oracle (`GET http://localhost:9000/check?domain=<host>`, unpublished — reachable only from Caddy itself). The oracle proxies the check to the backend's public `GET /domains/resolve?domain=<host>` endpoint, which only returns 200 when the domain's `store_domains` row is `VERIFIED` **and** the store is `ACTIVE`. This prevents an unregistered domain from ever triggering a Let's Encrypt request against our rate limit. Once authorized, Caddy obtains and caches a Let's Encrypt cert for that exact host — automatically, no manual provisioning step.

**Step 6 — Caddy proxies to the storefront app**
`reverse_proxy storefront:3700`, `Host` header unmodified.

**Step 7 — Storefront middleware resolves Host → store slug**
`manooch-fronts/apps/storefront/middleware.ts`: for a host that isn't a platform host and isn't a `<slug>.manooch.site` subdomain, calls the same `GET /domains/resolve?domain=` endpoint, gets `{ storeId, slug }`, and does `NextResponse.rewrite('/<slug>' + pathname)`. Address bar unchanged — serve, not redirect. Results cached in-memory (60s hits / 10s misses), fails open on network error.

---

## 5. Data Model

`manooch-backend/src/modules/store-domains/entities/store-domain.entity.ts` — table `store_domains`:

| Column | Notes |
|---|---|
| `id` | uuid PK |
| `storeId` | FK → `stores.id`, cascade delete |
| `domain` | normalized (lowercased, punycode, scheme/path stripped) |
| `status` | `pending \| verified \| failed` |
| `ns1Verified` / `ns2Verified` | historical pair from the earlier NS-delegation model; both are now always written together from the single A-record check and collapsed into one `verified` boolean at the API layer — kept as-is to avoid a migration |
| `lastCheckedAt` / `verifiedAt` | timestamps |
| soft-delete | standard `deletedAt` convention |

Partial unique indexes (non-deleted rows) enforce one store per domain, one active domain per store.

---

## 6. Endpoints

**Admin (owner-scoped)** — `@Controller('admin/stores/:storeId/domain')`:
- `GET` — current domain + `{ cnameTarget, apexIp }` to display.
- `POST` — register (`{ domain }`).
- `POST /verify` — trigger verification.
- `DELETE` — remove (soft delete).

**Public** — `@Controller('domains')`:
- `GET /domains/resolve?domain=` — `{ storeId, slug }` for a `VERIFIED` domain of an `ACTIVE` store, 404 otherwise. Consumed by both the storefront middleware and the Caddy on-demand-TLS oracle.

---

## 7. Incident — `tajmahl.ir` (why the NS-delegation model was abandoned)

A seller delegated `tajmahl.ir`'s nameservers exactly as instructed by the admin panel, to `manoch.321.b12.site` / `manoch.321.b11.site`. Live DNS investigation found:
- Those two nameserver hostnames **had no A record anywhere** — they were the backend's hardcoded placeholder defaults (`DEFAULT_PLATFORM_NS1`/`NS2`), never overridden by a real production `PLATFORM_NS1`/`NS2` env value.
- `tajmahl.ir`'s delegation was therefore pointed at nameservers that don't exist — an SOA/any-record query for the domain timed out on both 8.8.8.8 and 1.1.1.1. Not a propagation delay; the domain was permanently unresolvable.
- Even with correct nameservers, nothing in the system **provisioned** a seller's zone once verified — a verified domain still required a human to manually create a DNS zone and SSL cert for it. Not actually automatic.

This is why the model changed to **CNAME/A + Caddy on-demand TLS**: it removes the platform's need to host a DNS zone per seller at all, and cert issuance is genuinely automatic (Caddy does it on first request, gated by the existing `/domains/resolve` check) — no per-domain ops step, no risk of an unresolvable hardcoded placeholder.

---

## 8. Security & Operational Considerations

- **Domain ownership verification:** the seller must control DNS for their domain to add the CNAME/A record we check for — equivalent proof-of-control to any other DNS-based verification scheme.
- **SSL Enforcement:** Caddy's `auto_https` redirects HTTP → HTTPS by default.
- **Cert-issuance abuse protection:** the `:9000` on-demand-TLS oracle only authorizes a cert for a domain that is `VERIFIED` and belongs to an `ACTIVE` store.
- **Domain squatting prevention:** `DOMAIN_TAKEN` / `DOMAIN_RESERVED` checks in `register()`; `PLATFORM_BLOCKED_HOSTS` env excludes platform-owned hosts.
- **DNS propagation:** record changes typically take minutes to a few hours; up to 24h for slower registrars/TLDs. The admin UI should set this expectation.
- **No re-verification cron (known gap):** if a seller later removes the record, their `store_domains` row stays `VERIFIED` until someone notices. A scheduled re-check is a recommended follow-up.
- **No stale hardcoded infra defaults:** `PLATFORM_CUSTOM_DOMAIN_A_IPS` has **no non-empty default** — if ops forgets to set it, verification fails safely (nothing to match against) instead of silently succeeding against a wrong/dead value, which is what caused the `tajmahl.ir` incident.

---

## 9. Operational Enablement Checklist

1. Publish `edge.manooch.site` → Caddy origin public IP, **DNS-only** (not proxied) in the DNS provider hosting `manooch.site`.
2. Confirm the Caddy origin is publicly reachable on `80`/`443` by its own IP — custom-domain traffic bypasses ArvanCloud and hits it directly, so it cannot be firewalled to ArvanCloud IPs only. Port 80 is required for Let's Encrypt HTTP-01 on-demand challenges.
3. Set production env: `PLATFORM_CUSTOM_DOMAIN_CNAME_TARGET=edge.manooch.site`, `PLATFORM_CUSTOM_DOMAIN_A_IPS=<comma-separated origin IPs>`. Unset `DOMAIN_VERIFY_FAKE`.

---

## 10. Summary of Recommendations

| Component | Status |
|---|---|
| **Admin registration/verify/remove UI (CNAME/A copy)** | Implemented — `apps/admin/app/domain` |
| **Backend domain mapping + A-record verification** | Implemented — `store-domains` module |
| **Storefront Host→slug resolution (serve, not redirect)** | Implemented — `middleware.ts` |
| **Edge TLS for custom domains (any TLD, apex + subdomain)** | Implemented — Caddy catch-all `https://` block + `:9000` oracle gate |
| **`edge.manooch.site` DNS record + origin firewall opened** | Ops — one-time setup |
| **Scheduled re-verification** | Not implemented — follow-up |
| **NS-delegation model** | Superseded — abandoned after the `tajmahl.ir` incident |
| **ArvanCloud integration for custom domains** | Not implemented, not required |

---

## 11. Direct Answers

**Q: How does a custom domain end up loading the same storefront as `sellerName.manooch.site`?**
> The seller registers the domain in admin and adds one DNS record (CNAME for a subdomain, A for the apex) pointing at the platform. Once our A-record lookup confirms it resolves to our origin, the domain is `VERIFIED`. The first HTTPS request to that domain reaches the Caddy origin directly, which — gated by a check against the same `VERIFIED` status through `/domains/resolve` — automatically obtains a Let's Encrypt cert and proxies to the storefront app, which rewrites the request internally to the store's slug-based route without changing the browser URL.

**Q: Does this work for apex domains, subdomains, and any TLD?**
> Yes — CNAME for subdomains, A (or ANAME/ALIAS where supported) for apex, for any TLD, with no special-casing.

**Q: Is this automatic end-to-end?**
> Yes, on both sides now. Seller side: register → add one record → verify, all via the admin UI. Platform side: cert issuance is on-demand via Caddy, gated by the existing verified-domain check — no manual zone/cert provisioning step, unlike the abandoned NS-delegation model.

---

*This document reflects the implemented architecture as of the `wire-custom-domain` branch, after the `tajmahl.ir` incident led to abandoning the NS-delegation model in favor of CNAME/A + Caddy on-demand TLS.*
