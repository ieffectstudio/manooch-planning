# Drop Old Server — Decommission Plan

> **Context:** The `manooch` stack has been fully migrated to the new server
> (`95.38.185.156`) and is verified live. This plan covers safely decommissioning the
> **OLD server** (`130.185.121.227`).
>
> **Golden rule:** the old server is your only instant rollback. Do not drop it until
> every gate below is confirmed.

---

## Status (2026-08-17)

- Cutover completed 2026-08-16. Checked ~24h later, 2026-08-17.
- **Gate 1 (DNS) ✅ PASS** and **Gate 2 (old server drained) ✅ PASS** — see evidence
  below. **Gate 3 (data) ✅ PASS** and **Gate 4 (backups) ✅ PASS** — verified directly on
  the new server. **Gate 5 (secrets) 🟡 PARTIAL** — DB/JWT/Strapi secrets rotated live
  2026-08-17; SMS/payment provider keys and `SUPER_ADMIN_PASSWORD` still open; see below
  and [`success-deploy-summary.md`](success-deploy-summary.md#post-migration-todo-still-open).
- **Option A (soft stop) executed 2026-08-17.** All `manooch-*` containers on the old
  server were stopped via `docker compose down` in each of the three project dirs. VPS,
  disks, and all 6 volumes are untouched — rollback is `docker compose up -d` ×3 + a DNS
  flip. Live site re-checked immediately after and stayed fully healthy.
- **Do not proceed to Option B (termination) until Gate 5 passes.** The old VPS still
  holds the same DB password / JWT secret / Strapi keys as the new one; deleting it
  doesn't remove that exposure (the plaintext values are also baked into
  `~/backups/20260816/` on both hosts), but rotating first means a leaked old-server
  snapshot can't be used against the live system either.

## 0. Summary / Recommendation

- **Minimum wait:** 24 hours after DNS cutover (48h is safer). Given Gates 1–4 passed
  cleanly with zero real traffic on the old server for the full 24h window, Option A
  (soft stop, still reversible) was reasonable at 24h. Reserve the full 48h+ soak,
  and Gate 5 fixed, before Option B (irreversible termination).
- **Before dropping:** confirm DNS propagation externally + real traffic on the new server.
- **Never drop** the same day as the cutover.
- **Keep the backups** on the new server even after the old server is gone — and keep a
  second copy somewhere that isn't either server, since Option B destroys the old one.

---

## Gate 1 — DNS fully propagated (external check)

⚠️ **Don't use plain `dig @8.8.8.8` if you might be checking from a network with DNS
interception (e.g. inside Iran) — it can silently return the wrong answer with no error.**
Use DNS-over-HTTPS instead, which isn't interceptable the same way:

```bash
for d in manooch.site www.manooch.site api.manooch.site cms.manooch.site admin.manooch.site portal.manooch.site; do
  printf '%s => ' "$d"
  curl -s -H 'accept: application/dns-json' "https://dns.google/resolve?name=$d&type=A" | grep -o '"data":"[0-9.]*"'
done
```

(Skip `edge.manooch.site` — it isn't a served host; see Gate-1 result note below.)

✅ **Pass:** every result returns `95.38.185.156` (no `130.185.121.227`).

> Note: if you check too early, you may still see the old IP in some resolvers. Wait
> until your TTL window has elapsed since the DNS change.

**✅ Result (2026-08-17):** all 6 hosts above resolve to `95.38.185.156` via DoH, checked
from the old server. `edge.manooch.site` was checked too and does not resolve to a working
site on *either* server (TLS handshake failure, alert 592) — Caddy's on-demand-TLS oracle
denies it because `edge` isn't a registered store slug. Not a DNS problem, not a
migration regression — just not a real host. See `success-deploy-summary.md`.

---

## Gate 2 — Real traffic hitting the NEW server

Confirm live user requests (not your own test curls) are arriving, and that the OLD
server has gone quiet:

```bash
docker logs manooch-caddy --tail=100
docker logs manooch-api --tail=100
```

✅ **Pass:** you see requests with real client IPs, timestamps, and URLs — over a full
business day including your peak hours.

> Caddy access logging is off in this deployment, so `docker logs manooch-caddy` mostly
> shows ACME renewal/challenge noise, not per-request access lines. The more reliable
> signal on the **old** server is log *volume* over a time window —
> `docker logs manooch-api --since 24h | wc -l` — rather than reading individual lines.

**✅ Result (2026-08-17):** on the old server, `manooch-api` had **0** log lines in the
prior 24h (last entry was its own 2026-08-15 startup); `manooch-caddy` had 42 lines/24h,
all ACME renewal-info and `.well-known/*` scanner probes, zero real requests. The old
server was fully idle.

---

## Gate 3 — Data integrity verified on NEW server

Spot-check that data is real and complete (not empty). **There is no `users` table in
this schema — don't use it as your spot-check, `SELECT count(*) FROM users` just errors.**
Use `stores` / `products` / `orders` instead:

```bash
# List tables
docker exec manooch-postgres psql -U manooch -d manooch -c "\dt"

# Row counts — compare against the old server's numbers before it's gone
docker exec manooch-postgres psql -U manooch -d manooch -Atc "select 'stores='||count(*) from stores;"
docker exec manooch-postgres psql -U manooch -d manooch -Atc "select 'products='||count(*) from products;"
docker exec manooch-postgres psql -U manooch -d manooch -Atc "select 'orders='||count(*) from orders;"

# Uploads present (replace volume name if needed)
docker run --rm -v manooch-backend_manooch_uploads:/data alpine sh -c "ls /data | wc -l"

# CMS uploads present
docker run --rm -v manooch-cms_manooch_cms_uploads:/data alpine sh -c "ls /data | wc -l"
```

✅ **Pass:** table names/row counts look correct and upload files exist.

**✅ Result (2026-08-17):** new server matched the old server exactly at check time —
DB size 13 MB, `stores=6`, `products=16`, `orders=1` on both. API uploads: 112 files.
CMS uploads: 24 files. Both non-empty.

---

## Gate 4 — Backups confirmed intact on NEW server

You must be able to recover without the old server:

```bash
ls -lh ~/backups/$(date +%Y%m%d)/
# Expect: manooch-project/ + postgres-full-backup.sql + 6 vol-*.tar.gz
```

✅ **Pass:** the full backup set exists on the new server. **Do not delete these.**

> ⚠️ If your migration backup was made on an earlier date, check `ls -lh ~/backups/`
> and use the correct date folder.

**✅ Result (2026-08-17):** `~/backups/20260816/` present with `manooch-project/`,
`postgres-full-backup.sql` (1.0 MB), and all 6 `vol-*.tar.gz` (159 MB total) — sizes
match the old server's originals. Also confirmed file-level parity for everything not in
git (`.env`, `.env.db`, `.env.bak.*` ×11, `Caddyfile.bak`/`.diag.bak`, `.env.website`,
`.env.wordpress.bak`, the legacy `wp-core/`) — nothing was left behind on the old server.

---

## Gate 5 — Secrets rotated (or rotation scheduled)

The following were exposed during the migration and should be rotated:

- [ ] PostgreSQL password (`DB_PASSWORD` / `POSTGRES_PASSWORD`)
- [ ] JWT secrets (`JWT_SECRET`, `ADMIN_JWT_SECRET`)
- [ ] Strapi `APP_KEYS`, `API_TOKEN_SALT`, `ENCRYPTION_KEY`, `TRANSFER_TOKEN_SALT`
- [ ] SMS API keys (Melipayamak `MELIPAYAMAK_OTP_KEY`, Finnotech secrets, Armaghan password)

✅ **Pass:** rotated, OR a scheduled ticket exists to rotate immediately after decommission.

**🟡 Result: partially rotated, 2026-08-17.** Initially found byte-for-byte identical on
old vs. new server. Then rotated live on the new server: `DB_PASSWORD`/`POSTGRES_PASSWORD`
(Postgres `manooch` role), `DATABASE_PASSWORD` (Postgres `strapi` role), backend
`JWT_SECRET`, and all of Strapi's `APP_KEYS`/`API_TOKEN_SALT`/`ADMIN_JWT_SECRET`/
`TRANSFER_TOKEN_SALT`/`JWT_SECRET`/`ENCRYPTION_KEY`/`REVALIDATE_SECRET`/
`CONSULTATION_SECRET` — verified working (all containers recreated healthy, DB
queryable, all domains still serving). **Still not rotated:** the 3 SMS/payment provider
keys (Melipayamak, Finnotech, Armaghan — require action in each provider's own dashboard)
and `SUPER_ADMIN_PASSWORD` (editing the env var doesn't work — see
`success-deploy-summary.md` for why; needs either the app's own password-change flow or
a direct DB update). **Gate 5 now partially clears Option B** — the old server's disk and
both servers' `~/backups/20260816/` hold DB/JWT/Strapi secrets that are now stale/inert
against the live system, but still hold the 3 provider keys and the super-admin password
as live, valid credentials. Full termination should wait on those two.

---

## Decommission procedure

### Option A — Soft stop (recommended, low risk)

Stop the stack but keep the VPS (disk/data retained). You can still start it back up
for rollback, but it stops serving:

```bash
# On OLD server
cd ~/manooch/manooch-backend && docker compose -f docker-compose.prod.yml down
cd ~/manooch/manooch-cms     && docker compose -f docker-compose.prod.yml down
cd ~/manooch/manooch-fronts  && docker compose -f docker-compose.prod.yml down
docker ps -a   # should be empty / all exited
```

Keep the instance for 1–2 weeks, then terminate (Option B).

**✅ Executed 2026-08-17.** All `manooch-*` containers stopped and removed (`docker ps -a`
confirms empty except for a pre-existing, unrelated exited `wp-cli` container). Live site
re-checked from an external network immediately after — all domains still returned their
expected status codes, confirming nothing depended on the old server. Rollback if needed:
`docker compose -f docker-compose.prod.yml up -d` in each of the three project dirs, plus
flipping DNS back — see "Rollback" below.

### Option B — Full termination

Only after Option A has been clean for 1–2 weeks (or when you must stop billing), **and**
Gate 5 (secrets) passes:

1. Confirm the new server has been stable for the full observation window.
2. Confirm Gate 4 backups are intact on the new server.
3. **Confirm Gate 5 — rotate secrets first.** Don't terminate while the old server's disk
   still holds live production credentials identical to the new server's.
4. Confirm with each external provider (Melipayamak, Armaghan, Finnotech, Zarinpal)
   that nothing whitelists or calls back the old IP `130.185.121.227` — this repo can't
   see those provider dashboards, only you can check.
5. Take one final snapshot/backup of the old server if the provider supports it.
6. Terminate the old server in your cloud provider's console.

---

## Rollback (if you discover a problem before dropping)

Flip Arvan Cloud A records back to the old IP:

- `@`, `*`, `api`, `cms`, `admin`, `portal` → `130.185.121.227`

**As of 2026-08-17, the old server's containers are stopped** (Option A) — a DNS flip
alone won't bring the site back. Also run, on the old server:

```bash
cd ~/manooch/manooch-backend && docker compose -f docker-compose.prod.yml up -d
cd ~/manooch/manooch-cms     && docker compose -f docker-compose.prod.yml up -d
cd ~/manooch/manooch-fronts  && docker compose -f docker-compose.prod.yml up -d
```

The VPS itself was never modified/terminated, so this remains a fast, clean fallback —
just no longer a single-step one.

---

## Final checklist

```
[x] Gate 1 — external DNS resolves to 95.38.185.156                    (2026-08-17)
[x] Gate 2 — old server confirmed drained of real traffic              (2026-08-17)
[x] Gate 3 — data integrity spot-checks pass                           (2026-08-17)
[x] Gate 4 — full backup set present on new server                     (2026-08-17)
[~] Gate 5 — secrets rotated: DB/JWT/Strapi done (2026-08-17); SMS/payment provider
    keys + SUPER_ADMIN_PASSWORD still open — see success-deploy-summary.md
[x] Option A — old stack stopped (docker compose down)                 (2026-08-17)
[ ] External providers confirmed not dependent on old IP (you only)
[ ] 1–2 weeks clean + remaining Gate 5 items fixed → Option B — terminate old server
```
