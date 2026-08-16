# Drop Old Server — Decommission Plan

> **Context:** The `manooch` stack has been fully migrated to the new server
> (`95.38.185.156`) and is verified live. This plan covers safely decommissioning the
> **OLD server** (`130.185.121.227`).
>
> **Golden rule:** the old server is your only instant rollback. Do not drop it until
> every gate below is confirmed.

---

## 0. Summary / Recommendation

- **Minimum wait:** 24 hours after DNS cutover (48h is safer).
- **Before dropping:** confirm DNS propagation externally + real traffic on the new server.
- **Never drop** the same day as the cutover.
- **Keep the backups** on the new server even after the old server is gone.

---

## Gate 1 — DNS fully propagated (external check)

Confirm the new IP is served to *real users*, not just from the new server itself:

```bash
dig +short manooch.site @8.8.8.8
dig +short manooch.site @1.1.1.1
dig +short api.manooch.site @8.8.8.8
dig +short cms.manooch.site @8.8.8.8
dig +short edge.manooch.site @8.8.8.8
```

✅ **Pass:** every result returns `95.38.185.156` (no `130.185.121.227`).

> Note: if you check too early, you may still see the old IP in some resolvers. Wait
> until your TTL window has elapsed since the DNS change.

---

## Gate 2 — Real traffic hitting the NEW server

Confirm live user requests (not your own test curls) are arriving:

```bash
docker logs manooch-caddy --tail=100
docker logs manooch-api --tail=100
```

✅ **Pass:** you see requests with real client IPs, timestamps, and URLs — over a full
business day including your peak hours.

---

## Gate 3 — Data integrity verified on NEW server

Spot-check that data is real and complete (not empty):

```bash
# List tables
docker exec manooch-postgres psql -U manooch -d manooch -c "\dt"

# Row counts (replace with your real table names)
docker exec manooch-postgres psql -U manooch -d manooch -c "SELECT count(*) FROM users;"

# Uploads present (replace volume name if needed)
docker run --rm -v manooch-backend_manooch_uploads:/data alpine sh -c "ls -la /data | head"

# CMS uploads present
docker run --rm -v manooch-cms_manooch_cms_uploads:/data alpine sh -c "ls -la /data | head"
```

✅ **Pass:** table names/row counts look correct and upload files exist.

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

---

## Gate 5 — Secrets rotated (or rotation scheduled)

The following were exposed during the migration and should be rotated:

- [ ] PostgreSQL password (`DB_PASSWORD` / `POSTGRES_PASSWORD`)
- [ ] JWT secrets (`JWT_SECRET`, `ADMIN_JWT_SECRET`)
- [ ] Strapi `APP_KEYS`, `API_TOKEN_SALT`, `ENCRYPTION_KEY`, `TRANSFER_TOKEN_SALT`
- [ ] SMS API keys (Melipayamak `MELIPAYAMAK_OTP_KEY`, Finnotech secrets, Armaghan password)

✅ **Pass:** rotated, OR a scheduled ticket exists to rotate immediately after decommission.

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

### Option B — Full termination

Only after Option A has been clean for 1–2 weeks (or when you must stop billing):

1. Confirm the new server has been stable for the full observation window.
2. Confirm Gate 4 backups are intact on the new server.
3. Take one final snapshot/backup of the old server if the provider supports it.
4. Terminate the old server in your cloud provider's console.

---

## Rollback (if you discover a problem before dropping)

Flip Arvan Cloud A records back to the old IP:

- `@`, `*`, `api`, `cms`, `admin`, `portal` → `130.185.121.227`

The old server (if not yet terminated) resumes serving immediately — it was never
modified during the migration.

---

## Final checklist

```
[ ] Gate 1 — external DNS resolves to 95.38.185.156
[ ] Gate 2 — real traffic observed on new server (full day incl. peak)
[ ] Gate 3 — data integrity spot-checks pass
[ ] Gate 4 — full backup set present on new server
[ ] Gate 5 — secrets rotated or scheduled
[ ] Option A — old stack stopped (docker compose down)
[ ] 1–2 weeks clean → Option B — terminate old server
```
