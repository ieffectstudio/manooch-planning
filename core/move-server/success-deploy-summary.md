# Success Deploy Summary — Manooch Server Migration

> **Status: ✅ COMPLETE — verified live, no bugs**
> **Date:** 2026-08-16
> **Old server IP:** `130.185.121.227`
> **New server IP:** `95.38.185.156` (`ssh effect@95.38.185.156`)

---

## What was migrated

The full production `manooch` stack (backend + CMS + frontends) was moved from the old
server to the new server with zero data loss and no downtime:

| Component | Details |
|-----------|---------|
| **Project files** | `~/manooch/` (backend, cms, fronts — compose files + all `.env` files) |
| **PostgreSQL** | `pg_dumpall -U manooch` (logical dump) + `manooch_pg` volume (physical) |
| **Volumes (6 total)** | pg data, api uploads, cms uploads, wp db, caddy data (SSL), caddy config |
| **SSL certificates** | Restored via `caddy_data` volume — no cert re-issue needed |
| **Docker images** | Auto-pulled from `ghcr.io/ieffectstudio/*` (no manual transfer) |

---

## Key environment facts (confirmed during migration)

- **Postgres superuser is `manooch`** — NOT `postgres`. All dump/restore commands use
  `-U manooch`. (`POSTGRES_DB=manooch`, defined in `manooch-backend/.env.db`)
- **Images registry:** `ghcr.io/ieffectstudio/manooch-api`, `manooch-cms`,
  `manooch-fronts` (all `:latest`).
- **Frontends use `.env.website`** (there is no `.env` in `manooch-fronts`).
- **CMS is Strapi** (WordPress is legacy — wp-cli container was already exited/retired;
  `manooch_cms_wp_db` volume backed up for safety but not load-bearing).
- **Shared network:** `manooch_net` is declared `external: true` in all three compose
  files — it must be created manually with `docker network create manooch_net`.
- **Caddy** serves SSL/HTTPS on ports 80/443 for all domains.

### Containers (8, all healthy on new server)

```
manooch-postgres     postgres:16                                    (healthy)
manooch-api          ghcr.io/ieffectstudio/manooch-api:latest       (healthy)
manooch-cms          ghcr.io/ieffectstudio/manooch-cms:latest       (healthy)
manooch-caddy        caddy:2                                        (80/443)
manooch-storefront   ghcr.io/ieffectstudio/manooch-fronts:latest
manooch-portal       ghcr.io/ieffectstudio/manooch-fronts:latest
manooch-admin        ghcr.io/ieffectstudio/manooch-fronts:latest
manooch-website      ghcr.io/ieffectstudio/manooch-fronts:latest
```

### Domains served (all verified HTTPS 200/3xx on new IP)

- `manooch.site` (Next.js website)
- `www.manooch.site` (→ 301 to apex)
- `api.manooch.site` (Express API)
- `cms.manooch.site` (Strapi → /admin)
- `admin.manooch.site` (→ /sign-in)
- `portal.manooch.site` (→ /sign-in)
- `<slug>.manooch.site` tenant storefronts (via `*` wildcard, e.g. `tajmahal.manooch.site`)

> **Correction (2026-08-17):** `edge.manooch.site` is **not** served — it fails TLS
> handshake (alert 592, "no information found to solve challenge") on both the new *and*
> old server, so it was never actually working; the "verified HTTPS 200/3xx" claim above
> was wrong. Caddy's on-demand-TLS oracle (`ask http://localhost:9000/check` in
> `manooch-backend/Caddyfile`) denies it because `edge` isn't a registered store slug.
> Not a migration regression — just leave it as-is unless `edge` is meant to be a real host.

---

## Critical config change made

In `~/manooch/manooch-backend/.env`:

```
PLATFORM_CUSTOM_DOMAIN_A_IPS=130.185.121.227   →   PLATFORM_CUSTOM_DOMAIN_A_IPS=95.38.185.156
```

This routes tenant custom domains to the new server IP. Verified in the running
container:

```
$ docker exec manooch-api printenv PLATFORM_CUSTOM_DOMAIN_A_IPS
95.38.185.156
```

DNS A records updated in Arvan Cloud to `95.38.185.156` (root `@`, `*` wildcard, api,
cms, admin, portal). Propagation confirmed via `dig`.

---

## Proven migration steps (for future reference)

```
OLD SERVER (backup)
  mkdir -p ~/backups/$(date +%Y%m%d)
  rsync -a --exclude node_modules --exclude .git ~/manooch/ $BACKUP_DIR/manooch-project/
  docker exec manooch-postgres pg_dumpall -U manooch > $BACKUP_DIR/postgres-full-backup.sql
  (tar all 6 volumes via alpine containers)

  rsync -avz --progress ~/backups/ effect@95.38.185.156:~/backups/

NEW SERVER (restore)
  curl -fsSL https://get.docker.com | sudo sh
  usermod -aG docker $USER ; newgrp docker
  cp -r $BACKUP_DIR/manooch-project/* ~/manooch/
  docker volume create (x6)
  (untar all 6 volumes)
  docker network create manooch_net      ← REQUIRED (external: true)
  cd ~/manooch/manooch-backend && docker compose -f docker-compose.prod.yml up -d
  cd ~/manooch/manooch-cms     && docker compose -f docker-compose.prod.yml up -d
  cd ~/manooch/manooch-fronts  && docker compose -f docker-compose.prod.yml up -d
```

---

## Post-migration TODO (still open)

1. ~~Keep old server running 24–48h as rollback, then decommission.~~ **Done** — see
   "Post-cutover verification" below; containers stopped 2026-08-17 (Option A, soft stop).
2. **Rotate secrets — partially done, 2026-08-17.** Everything fully under our control
   was rotated live on the new server, verified working (containers recreated, DB
   reachable, all domains still 200/3xx, no data loss): Postgres `manooch` role password
   (`DB_PASSWORD`/`POSTGRES_PASSWORD`), Postgres `strapi` role password
   (`DATABASE_PASSWORD`), backend `JWT_SECRET`, and Strapi's `APP_KEYS`,
   `API_TOKEN_SALT`, `ADMIN_JWT_SECRET`, `TRANSFER_TOKEN_SALT`, `JWT_SECRET`,
   `ENCRYPTION_KEY`, `REVALIDATE_SECRET`/`CONSULTATION_SECRET`. Pre-rotation values were
   backed up as `.env.bak.<timestamp>` alongside the existing backup-file convention.
   Effect: every logged-in customer/seller/admin session and both Strapi admin sessions
   were invalidated (users just need to sign back in — no data loss); the 3 existing
   Strapi API tokens ("Read Only", "Full Access", "prod-seed-script") are invalidated too
   — they were unreferenced defaults, not live integrations.

   **Still open — needs you, not something I can self-service:**
   - `MELIPAYAMAK_OTP_KEY`, `FINNOTECH_CLIENT_SECRET`, `ARMAGHAN_PASSWORD` — issued by
     each provider's own dashboard; rotate there, then update `.env` + restart `manooch-api`.
   - `SUPER_ADMIN_PASSWORD` — **editing this env var does nothing.** The seeder
     (`manooch-backend/src/modules/super-admin/seed/super-admin.seeder.ts`) only hashes
     it into the DB once, on first boot, then no-ops forever after — that already
     happened, so the live credential is unaffected by changing the env var. Actually
     rotating it needs either the app's own admin password-change flow, or a direct DB
     update of the bcrypt hash on the `admin_credentials`/`Customer` row for that admin's
     mobile — say which you want and I'll do it.
   - Legacy MySQL/WordPress DB passwords (`.env.db` in `manooch-cms`) — left as-is; no
     running container consumes them (the WordPress/MySQL stack is retired), so they're
     dead credentials, not a live-system risk.

   Stopping/deleting the old server does **not**, by itself, fix secret exposure — but
   now that the live values differ, the plaintext secrets sitting in `~/backups/20260816/`
   on both servers (and on the old server's disk generally) are **stale/inert**, not valid
   against the live system. That significantly lowers the risk of deleting the old VPS —
   see [`drop-old-server.md`](drop-old-server.md) Gate 5.
3. **Optional cleanup** — delete `.env.bak.*` files and update `.env.production.example`
   (they still reference the old IP `130.185.121.227`; inert but stale). Also note
   `.env.production.example` is tracked in `manooch-backend` git, so this needs a commit
   there, not just a server-side edit.

## Rollback plan (if anything breaks in the next 48h)

- Flip Arvan Cloud A records back to `130.185.121.227` → old server resumes instantly.
- Old server's containers were stopped 2026-08-17 (`docker compose down` — disks/volumes
  untouched); rollback is `docker compose up -d` in each of the three project dirs, plus
  the DNS flip. It is no longer "never stopped," but it is still a clean, fast fallback.

## Post-cutover verification (2026-08-17)

Checked ~24h after cutover, before stopping the old server's containers:

- **DNS**: all 7 hosts resolve to `95.38.185.156` via DNS-over-HTTPS (`dns.google/resolve`),
  checked from the old server to avoid local DNS interception on the checking machine.
- **Old server traffic**: `manooch-api` had 0 log lines in the prior 24h (last entry was
  its own 08/15 startup); `manooch-caddy` had 42 lines/24h, all ACME renewal-info and
  `.well-known` scanner probes — no real user requests. Old server was fully idle.
- **New server data parity vs. old server** (measured on both, same moment): DB size
  13 MB, `stores=6`, `products=16`, `orders=1` on both. API uploads volume: 112 files.
  CMS uploads volume: 24 files. Both non-empty.
- **Backups on new server**: `~/backups/20260816/` present with `manooch-project/`,
  `postgres-full-backup.sql` (1.0 MB), and all 6 `vol-*.tar.gz` (159 MB total) — sizes
  match the old server's originals.
- **File parity**: every untracked file that only lived on the old server (`.env`,
  `.env.db`, `.env.bak.*` ×11, `Caddyfile.bak`, `Caddyfile.diag.bak`, `.env.website`,
  `.env.wordpress.bak`, the 94 MB legacy `wp-core/`) is present on the new server too —
  nothing was left behind.
- **No unpushed code**: all three repos (`manooch-backend`, `manooch-cms`,
  `manooch-fronts`) on `main`, clean working tree, zero commits ahead of `origin` on the
  old server.
- **No live tenant custom domains**: `store_domains` table has 4 rows, all
  `pending`/`failed`, 3 soft-deleted — zero verified domains depend on either IP.
- Old server's containers stopped (`docker compose down` ×3) after all the above passed.
  Live site re-checked immediately after and stayed healthy — confirmed nothing was
  still depending on the old server.
