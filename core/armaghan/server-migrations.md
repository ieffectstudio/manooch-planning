# Migrate the Manooch stack to an Iranian server

## Context

`manooch-server` (`130.185.121.227`) is hosted abroad. Armaghan/HiSMS firewalls
`panel.hisms.ir:443` to Iranian IPs and will not whitelist a foreign address, so the
OTP cutover completed earlier this session left **production OTP login broken** — every
`/auth/request-otp` times out ~5s and returns `SMS_SEND_FAILED`.

A tunnel that gives only the SMS calls an Iranian egress would fix OTP, but the user
confirmed the move is driven by four things at once: Armaghan, going live with Zarinpal
+ Finnotech Shahkar, enamad/legal hosting requirements, and latency for Iranian users.
Enamad/legal alone forces a real move, so the goal is **relocate the whole stack to Iran
without breaking the build/deploy chain** — not to work around the SMS restriction.

Two findings make this far smaller than it first appears:

1. **Nothing is built on the server.** All three prod stacks pull a prebuilt image
   (`manooch-backend/docker-compose.prod.yml:41`, `manooch-fronts/…:11`,
   `manooch-cms/…:19`). `npm ci` / `pnpm install` / `docker build` run on GitHub's
   US runners and are unaffected by where the server lives. The user's concern that
   "npm installs will fail" does not apply.
2. **Every runtime outbound call already targets an Iranian host** —
   `panel.hisms.ir` (`armaghan.client.ts:13`), `console.melipayamak.com`
   (`meli-payamak.provider.ts:38`), `payment.zarinpal.com` (`zarinpal.config.ts:17`),
   `api.finnotech.ir` (`finnotech.config.ts:21`), `trustseal.enamad.ir`. After the move
   the running app needs **no foreign internet at all**.

So the only blocked surface is the *deploy* path: `docker compose pull` from `ghcr.io`
(blocked from Iran regardless of package visibility), base images from Docker Hub
(blocked), and `git fetch origin main` (works from Iran but is intermittently flaky).
All three repos share an identical `scripts/deploy.sh`, so one fix pattern covers them.

**Chosen approach (user decision):** run a private `registry:2` on the Iranian server
behind the existing Caddy. CI pushes to it; the server pulls from `localhost`. Registry
push is layer-aware so only changed layers cross the wire, and the server makes no
outbound request. No permanent foreign VPS, no full-image transfer per deploy.

## Work

### Phase 0 — Unbreak production today (do first, independent of the migration)

The migration is a multi-day job; OTP is broken *now*. On `manooch-server`, revert the
one line in `~/manooch/manooch-backend/.env` and recreate the container:

```
SMS_PROVIDER=melipayamak
docker compose -f docker-compose.prod.yml up -d api
```

This is the documented rollback path — Melipayamak keys are still present and its
provider code is still wired. **Do not remove Melipayamak** until Armaghan is verified
working from the Iranian box; it is the only rollback that exists.

The `fix-otp` branch stays as-is and can merge whenever — the code default is
`armaghan`, and prod's explicit `.env` value overrides it either way (`.env` is not
git-tracked, so `deploy.sh`'s `git reset --hard` never touches it).

### Phase 1 — Provision the Iranian server

Pick a host with a static public IP and enough headroom (the current box is 1 vCPU /
2 GB, per `manooch-cms/docker-compose.prod.yml`'s header — size up, four Next apps +
Strapi + Postgres on 2 GB is already tight).

1. Docker + compose, `docker network create manooch_net`.
2. **Docker Hub mirror** for base images (`caddy:2`, `postgres:16`, `registry:2`) —
   `/etc/docker/daemon.json`: `{"registry-mirrors": ["https://docker.arvancloud.ir"]}`
   (or `focker.ir`), then `systemctl restart docker`. Verify with `docker pull caddy:2`.
3. Stand up the registry: a `registry:2` container on `manooch_net` bound to
   `127.0.0.1:5000`, with an `htpasswd` file and a persistent volume.
4. Verify Let's Encrypt reachability from Iran (`curl -I https://acme-v02.api.letsencrypt.org/directory`)
   **before** cutover — Caddy's on-demand TLS for seller custom domains depends on it.

### Phase 2 — Repo changes (same pattern in all three repos)

`manooch-backend`, `manooch-fronts`, `manooch-cms`:

- **`.github/workflows/deploy.yml`** — add a second `docker/login-action` +
  push target for `registry.manooch.site`, keeping the existing GHCR push (dual-push
  is cheap insurance and keeps a foreign staging box possible). New secrets:
  `REGISTRY_HOST`, `REGISTRY_USER`, `REGISTRY_PASSWORD`. In `manooch-backend` the
  `IMAGE` env at line 13 becomes two tags.
- **`scripts/deploy.sh`** — point the pull at the local registry. Replace
  `git fetch/checkout/reset` with an `scp` of the few files the server actually needs
  (`docker-compose.prod.yml`, and `Caddyfile` for the backend) pushed from the CI job,
  removing the last outbound dependency. Keep the script idempotent.
- **`manooch-backend/docker-compose.prod.yml`** — image refs become
  `localhost:5000/manooch-api:latest` etc. Add the `registry` service.

**`manooch-backend/Caddyfile`** (backend owns the shared edge):

- Add a `registry.manooch.site` site block reverse-proxying `registry:5000`, with a
  large `request_body { max_size 0 }` so layer uploads aren't truncated.
- **Add `registry.manooch.site` to the `@fixed` expression at line 72.** The file's own
  comment (lines 25-58) documents why: any host not in that list falls through to the
  on-demand TLS oracle's catch-all and gets *permanently denied* on its first HTTPS
  request. Missing this is the single easiest way to break the new registry.

### Phase 3 — Data migration and cutover

Volumes in play: `manooch_pg`, `manooch_uploads`, `manooch_cms_uploads`, `caddy_data`.

1. `pg_dump` **both** databases — `manooch-postgres` is shared: the backend's DB and
   Strapi's dedicated `strapi` DB/role (see `manooch-cms/docker-compose.prod.yml:6-11`).
   Recreate the `strapi` role on the new box before restoring.
2. `rsync` the uploads volumes.
3. **Migrate `caddy_data` too** rather than letting Caddy re-issue. It holds every
   already-issued cert, including one per seller custom domain; a cold start would
   re-request them all at once and can hit Let's Encrypt's 50-certs-per-week limit.
4. Copy `.env`, `.env.db`, `.env.website` by hand (not git-tracked). Update
   `PLATFORM_CUSTOM_DOMAIN_A_IPS`.
5. Bring the stack up on the new box and smoke-test against its IP via `/etc/hosts`
   overrides *before* touching public DNS.
6. DNS cutover: `manooch.site`, `www`, `api`, `admin`, `portal`, `cms`, the
   `*.manooch.site` wildcard, `registry`, and `edge.manooch.site`.

### Phase 4 — Post-cutover

- Set `SMS_PROVIDER=armaghan` again and confirm a real OTP arrives. Only then consider
  removing Melipayamak.
- Zarinpal (`ZARINPAL_MODE`) and Shahkar (`SHAHKAR_MODE`) can move off `dummy`/`off`
  now that the origin is Iranian — each is its own follow-up, not part of this move.

## Risks

- **Seller custom domains are the biggest hazard.** Sellers who verified via an **A
  record** point at `130.185.121.227`; after the move `/domains/resolve` fails for them,
  the Caddy oracle denies the cert, and their storefront goes dark. Mitigation: keep
  **both** IPs in `PLATFORM_CUSTOM_DOMAIN_A_IPS` through the transition, keep the old
  box running as a fallback, and re-point `edge.manooch.site` — CNAME-verified sellers
  migrate automatically with no action on their part.
- Let's Encrypt reachability from the Iranian host is a hard prerequisite (Phase 1.4).
  If it fails, on-demand TLS for custom domains cannot work and the plan needs rework.
- Registry auth is a new public attack surface — htpasswd + Caddy TLS is the minimum;
  consider IP-restricting pushes to GitHub's runner ranges.

## Verification

- `docker pull caddy:2` succeeds on the new box (mirror works).
- A push to `main` in each repo completes CI, lands the image in `registry.manooch.site`,
  and the server pulls it with **zero outbound requests to ghcr.io or Docker Hub**
  (confirm with `journalctl -u docker` / a quick `tcpdump` during a deploy).
- `curl -I https://api.manooch.site/health`, plus one storefront slug, one CNAME-verified
  custom domain, and one A-record custom domain all return 200 over valid TLS.
- Row counts match between old and new Postgres for a few key tables; a known uploaded
  image loads from the new box.
- `curl -m 12 https://panel.hisms.ir/` from the new server returns 200 (not a timeout).
- End-to-end: request an OTP on manooch.site and receive the SMS.
