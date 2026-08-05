# Full Architecture & Design Explanation — Custom Domain for Storefront
> Feature: `@manooch-fronts/apps/admin/app/domain`
> Edge: Caddy (`manooch-backend/Caddyfile`) — single reverse proxy in front of all services on `manooch_net`
> Backend module: `manooch-backend/src/modules/store-domains/`
> Storefront resolution: `manooch-fronts/apps/storefront/middleware.ts`
> Status: Implemented (code) — operational enablement (DNS zone) required before go-live
> Base Domain: `manooch.site`

---

## 1. Problem Statement (What the Seller Wants)

A seller has:
- **Custom domain owned by seller:** e.g. `sellerName.ir`, `sellerName.com`, or a subdomain like `shop.sellerName.ir`
- **Storefront subdomain (our platform):** `sellerName.manooch.site`

The seller wants: when anyone opens their custom domain, the site loads the same storefront that lives at `sellerName.manooch.site`.

**Key point:** The seller does NOT want to redirect (`301/302`) the user. They want their domain to **serve** the same storefront content directly (white-label / custom domain experience). This is supported for **any TLD**, both **apex** (`sellerName.ir`) and **subdomain** (`shop.sellerName.ir`) forms.

---

## 2. High-Level Concept

There are three layers involved:

1. **DNS Layer** — the seller delegates their domain's nameservers to the platform.
2. **Edge Layer** — Caddy, acting as reverse proxy + automatic HTTPS via on-demand TLS (Let's Encrypt).
3. **Application / Server Layer** — `manooch-backend` maps the incoming domain to a store, and the storefront app renders it.

> **Note on architecture history:** an earlier draft of this PRD proposed ArvanCloud as the CDN/DNS/SSL provider. That path was **not taken**. The implemented system is self-hosted: our own nameservers + Caddy's on-demand TLS. ArvanCloud (or any CDN) could still be placed in front of this origin later as a pure infrastructure choice, but no such integration exists in code today, and none is required for the feature to work.

---

## 3. DNS Strategy — Nameserver Delegation (not CNAME/ANAME)

Unlike a typical CNAME/ANAME-based setup, this platform uses **full nameserver (NS) delegation**:

- The platform exposes two nameserver hostnames, configured via backend env vars `PLATFORM_NS1` / `PLATFORM_NS2` (defaults: `manoch.321.b12.site`, `manoch.321.b11.site` — override with real production values).
- The seller goes to their domain registrar and changes the **NS records** for their domain to point at `PLATFORM_NS1` / `PLATFORM_NS2`.
- This makes the platform **authoritative** for the seller's domain — not just for a single record, but for the whole zone. This works uniformly for apex and subdomain, for any TLD, with no CNAME-at-apex limitation to work around.

**Why this instead of CNAME/ANAME/TXT-token:** it sidesteps the "no CNAME at the apex" DNS restriction entirely (the classic reason ANAME/ALIAS records exist), and verification becomes a simple, forgeable-proof `NS` lookup — no file upload or TXT record for the seller to manage.

**Trade-off / dependency this creates:** because we become authoritative, **we must serve a DNS zone for every verified custom domain** (see §7, Operational Enablement) — this is the one piece that is infrastructure, not application code.

---

## 4. Step-by-Step Flow (Implemented)

**Step 1 — Seller registers the domain in the admin panel**
`@manooch-fronts/apps/admin/app/domain` → `DomainForm` → `POST /admin/stores/:storeId/domain { domain }` (`admin-store-domains.controller.ts` → `StoreDomainsService.register`). Validates format, rejects platform-reserved hosts (`DOMAIN_RESERVED`) and domains already claimed by another store (`DOMAIN_TAKEN`). Row is created in `store_domains` with `status = PENDING`.

**Step 2 — Seller delegates NS at their registrar**
The admin UI (`NameserverPanel`) shows the two platform nameservers (from `GET /admin/stores/:storeId/domain` → `getConfig`). The seller updates NS records at their `.ir`/`.com`/etc. registrar.

**Step 3 — Seller clicks "verify"**
`POST /admin/stores/:storeId/domain/verify` → `StoreDomainsService.verify`: does a live `NS` DNS lookup (`NsLookupService`, wraps `node:dns/promises.resolveNs`) against the seller's domain, checks both platform nameservers are present, and flips `status` to `VERIFIED` (or `FAILED`). 10-second cooldown between checks (`DOMAIN_VERIFY_TOO_SOON`). Dev/test bypass via `DOMAIN_VERIFY_FAKE=true`.

**Step 4 — DNS resolves to the platform edge**
Once NS delegation has propagated, DNS queries for the seller's domain resolve using our nameservers, which must answer with an `A` record for the domain pointing at the Caddy edge's public IP (see §7 — this is the operational step still required per-domain today).

**Step 5 — Request reaches Caddy**
Caddy receives the HTTPS request for the seller's domain, `Host` header intact.

**Step 6 — On-demand TLS cert issuance, gated**
Caddy has no static site block for an arbitrary seller domain, so it falls back to **on-demand TLS**, asking its internal oracle (`GET http://localhost:9000/check?domain=<host>`, unpublished — reachable only from Caddy itself). The oracle proxies the check to the backend's existing public `GET /domains/resolve?domain=<host>` endpoint, which only returns 200 when the domain's `store_domains` row is `VERIFIED` **and** the store is `ACTIVE`. This prevents a random/unregistered domain from ever triggering a Let's Encrypt request against our rate limit. Once authorized, Caddy obtains and caches a Let's Encrypt cert for that exact host.

**Step 7 — Caddy proxies to the storefront app**
`reverse_proxy storefront:3700`, `Host` header unmodified — the storefront app decides what to render based on `Host`, not based on which Caddy site block matched.

**Step 8 — Storefront middleware resolves Host → store slug**
`manooch-fronts/apps/storefront/middleware.ts`: for a host that isn't a platform host and isn't a `<slug>.manooch.site` subdomain, calls the same `GET /domains/resolve?domain=` endpoint, gets back `{ storeId, slug }`, and does `NextResponse.rewrite('/<slug>' + pathname)`. The browser's address bar is untouched — this is the "serve, don't redirect" requirement. Resolution results are cached in-memory (60s for hits, 10s for misses) and **fail open** on network error (never 500s the request).

---

## 5. Data Model

`manooch-backend/src/modules/store-domains/entities/store-domain.entity.ts` — table `store_domains`:

| Column | Notes |
|---|---|
| `id` | uuid PK |
| `storeId` | FK → `stores.id`, cascade delete |
| `domain` | the seller's domain, normalized (lowercased, punycode, scheme/path stripped) |
| `status` | `pending \| verified \| failed` |
| `ns1Verified` / `ns2Verified` | booleans from the last check |
| `lastCheckedAt` / `verifiedAt` | timestamps |
| soft-delete | standard `deletedAt` convention |

Partial unique indexes (scoped to non-deleted rows) enforce: a domain is claimed by at most one store, and a store has at most one active custom domain.

`Store` itself has no `customDomain` column by design — the platform subdomain (`Store.slug`) and the custom domain are modeled as separate concerns; `store_domains` is the join.

---

## 6. Endpoints

**Admin (owner-scoped, `CustomerAuthGuard` + ownership check)** — `@Controller('admin/stores/:storeId/domain')`:
- `GET /admin/stores/:storeId/domain` — current domain + platform nameservers to display.
- `POST /admin/stores/:storeId/domain` — register (`{ domain }`).
- `POST /admin/stores/:storeId/domain/verify` — trigger NS verification.
- `DELETE /admin/stores/:storeId/domain` — remove (soft delete).

**Public** — `@Controller('domains')`:
- `GET /domains/resolve?domain=` — `{ storeId, slug }` for a `VERIFIED` domain of an `ACTIVE` store, 404 otherwise. Consumed by both the storefront middleware and the Caddy on-demand-TLS oracle.

---

## 7. Operational Enablement (the real "not enabled")

The code path above is complete. What makes the feature "not enabled" in practice is entirely **DNS infrastructure**, not a code flag:

1. **Authoritative DNS zone provisioning.** `PLATFORM_NS1` / `PLATFORM_NS2` must be real, reachable authoritative nameservers. When a seller's domain reaches `VERIFIED`, that domain needs a zone served by our nameservers with (at minimum) an apex `A` record pointing at the Caddy edge's public IP — otherwise the delegated domain resolves to NXDOMAIN and nothing loads, even though our app thinks it's verified.
   - **Today:** manual — ops creates the zone/A-record when a domain reaches `VERIFIED`.
   - **Planned follow-up:** automate zone creation via the DNS provider's API, triggered from `StoreDomainsService.verify()` on success.
2. **Caddy edge reachable** on public `80`/`443` with a stable IP (port 80 required for Let's Encrypt HTTP-01 on-demand challenges).
3. **Production env values set:** `PLATFORM_NS1`/`PLATFORM_NS2` = the real nameserver hostnames shown to sellers; `DOMAIN_VERIFY_FAKE` unset/false in production.

---

## 8. Security & Operational Considerations

- **Domain ownership verification:** enforced via NS delegation (§3) — a seller cannot claim a domain without control over its registrar NS settings.
- **SSL Enforcement:** Caddy's `auto_https` redirects HTTP → HTTPS by default.
- **Cert-issuance abuse protection:** the `:9000` on-demand-TLS oracle only authorizes a cert for a domain that is `VERIFIED` and belongs to an `ACTIVE` store — an attacker pointing a random domain at our IP cannot trigger unlimited Let's Encrypt requests against our account's rate limit.
- **Domain squatting prevention:** `DOMAIN_TAKEN` / `DOMAIN_RESERVED` checks in `register()`; `PLATFORM_BLOCKED_HOSTS` env excludes platform-owned hosts.
- **Rate limiting:** custom domains are served by the same storefront app instance as platform subdomains, so they inherit the same app-level rate limits.
- **DNS propagation:** NS changes can take up to 24-48h depending on the seller's previous registrar TTL. The admin UI should set expectations that verification may not succeed immediately after the seller makes the change.
- **No re-verification cron (known gap):** if a seller later removes our NS delegation, their `store_domains` row stays `VERIFIED` and traffic keeps being served under stale trust until someone notices. A scheduled re-check is a recommended follow-up, not yet implemented.

---

## 9. Summary of Recommendations

| Component | Status |
|---|---|
| **Admin registration/verify/remove UI** | Implemented — `apps/admin/app/domain` |
| **Backend domain mapping + verification** | Implemented — `store-domains` module |
| **Storefront Host→slug resolution (serve, not redirect)** | Implemented — `middleware.ts` |
| **Edge TLS for custom domains (any TLD, apex + subdomain)** | Implemented — Caddy catch-all `https://` block + `:9000` oracle gate |
| **DNS zone hosting for verified domains** | **Manual today** — automate as follow-up |
| **Scheduled re-verification** | Not implemented — follow-up |
| **ArvanCloud integration** | Not implemented, not required — superseded by self-hosted Caddy + NS delegation |

---

## 10. Direct Answers

**Q: How does a custom domain end up loading the same storefront as `sellerName.manooch.site`?**
> The seller registers the domain in admin and delegates their NS to our platform nameservers. Once our live NS lookup confirms the delegation, the domain is `VERIFIED`. Our nameservers then need to answer for that domain with an `A` record pointing at the Caddy edge (operational step). Caddy obtains a cert on demand — gated by checking `VERIFIED` status through the same `/domains/resolve` endpoint the storefront middleware uses — and proxies to the storefront app, which rewrites the request internally to the store's slug-based route without changing the browser URL.

**Q: Does this work for apex domains, subdomains, and any TLD?**
> Yes. NS delegation avoids the "no CNAME at the apex" restriction, so both `sellerName.ir` and `shop.sellerName.ir` work identically, for any TLD, without special-casing.

**Q: Is ArvanCloud used?**
> No. This document previously specified ArvanCloud; the implemented system uses self-hosted nameservers and Caddy's on-demand TLS instead. ArvanCloud is not integrated anywhere in the codebase.

---

*This document reflects the implemented architecture as of the `wire-custom-domain` branch. It replaces an earlier draft that specified ArvanCloud as the DNS/CDN provider.*
