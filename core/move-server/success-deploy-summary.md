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
- `api.manooch.site` (Express API)
- `cms.manooch.site` (Strapi → /admin)
- `admin.manooch.site` (→ /sign-in)
- `portal.manooch.site` (→ /sign-in)
- `edge.manooch.site` + all custom/tenant domains (via `*` wildcard)

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

1. **Keep old server running 24–48h** as rollback, then decommission.
2. **Rotate secrets** — DB password, JWT secrets, SMS/API keys (Melipayamak, Finnotech,
   Armaghan) were exposed during the migration. Update in `.env` files after stable.
3. **Optional cleanup** — delete `.env.bak.*` files and update `.env.production.example`
   (they still reference the old IP `130.185.121.227`; inert but stale).

## Rollback plan (if anything breaks in the next 48h)

- Flip Arvan Cloud A records back to `130.185.121.227` → old server resumes instantly.
- Old server was never stopped or modified, so it's a clean fallback.
