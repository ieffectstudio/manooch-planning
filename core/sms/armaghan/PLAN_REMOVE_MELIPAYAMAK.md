# Verify Armaghan on the Iranian server, then remove Melipayamak

## Context

Melipayamak was supposed to be gone already. PR #49 (`89bfa6c fix(sms): switch OTP provider to
Armaghan with template 4591_002`) shipped Armaghan as the *code* default, but production never
actually flipped: the server was hosted abroad at `130.185.121.227`, and Armaghan/HiSMS firewalls
`panel.hisms.ir:443` to Iranian IPs only. Every Armaghan call timed out at 5s and returned
`SMS_SEND_FAILED`, so `SMS_PROVIDER=melipayamak` was pinned in the production `.env` as an emergency
rollback and Melipayamak was deliberately kept in the tree as the only escape hatch
(`manooch-planings/core/sms/armaghan/server-migrations.md`, Phase 0).

The server has now moved to Iran, which removes that blocker. Recon confirms it:

| Check | Result |
|---|---|
| `manooch-server` host | `95.38.185.156` (Iran) — all 8 containers up, `manooch-api` healthy |
| `curl -I https://panel.hisms.ir/` from the box | **HTTP 200 in 0.9s** (was a hard timeout from abroad) |
| Live `getUserInfo` with prod credentials | `{"errorCode":0,"userInfo":{"credit":12598740}}` — auth OK, IP whitelisted, credit fine |
| Prod `.env` | `SMS_PROVIDER=melipayamak`, `SMS_ENABLED=true`, `ARMAGHAN_OTP_TEMPLATE_ID=4591_002`, both credential blocks present |
| Prod logs (today) | `OTP sent: provider=melipayamak mobile=0992***285 … status=sent` — Melipayamak still carrying live traffic |
| `SHAHKAR_MODE` | `off` — no national-ID gate on `/auth/request-otp` |

The goal: prove a real Armaghan SMS lands on `09928456285`, flip production, then delete Melipayamak
on branch `remove-melipaymak`.

### Access note (blocking, fix first)

`~/.ssh/config` maps `manooch-server` to `IdentityFile ~/.ssh/id_ed25519`, which the server
**rejects**. The key that authenticates is `~/.ssh/manooch_fix`:

```bash
ssh -i ~/.ssh/manooch_fix effect@95.38.185.156
```

Worth correcting the `IdentityFile` line in `~/.ssh/config` so `ssh manooch-server` works again.
Also confirm the GitHub Actions `SSH_HOST` secret points at the new IP — the running `manooch-api`
image is from `2026-08-17T05:02Z`, so a deploy has already succeeded against this box, but verify
rather than assume.

---

## Phase 0 — Send the test SMS (no production impact)

Bypasses NestJS entirely and hits the Armaghan wire API directly, so nothing about live traffic
changes. Run **on the server** (from your laptop the host will time out — the whitelist is per-IP).

```bash
ssh -i ~/.ssh/manooch_fix effect@95.38.185.156
cd ~/manooch/manooch-backend
set -a; . ./.env; set +a
curl -s -X POST "$ARMAGHAN_BASE_URL$ARMAGHAN_API_PREFIX/sendParameterizedMessage" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$ARMAGHAN_USERNAME\",\"password\":\"$ARMAGHAN_PASSWORD\",\"template\":\"$ARMAGHAN_OTP_TEMPLATE_ID\",\"parameters\":[\"55731\"],\"destinations\":[\"09928456285\"]}"
```

**Pass:** `{"errorModel":{"errorCode":0,...},"references":["<18-digit id>"]}` **and** code `55731`
arrives on the handset. Nothing proceeds past this point until the SMS is physically received.

If `errorCode` is non-zero, the mapping in `providers/armaghan-api.exception.ts` names the cause —
most likely `-160` (template `4591_002` wrong/inactive), `-161` (pattern expects a different
parameter count), or `-103` (originator `50002062088` not active on the line).

Optionally confirm delivery status with the reference id via `POST /getMessageState`
(`{"ids":["<ref>"]}`); `2` = delivered to device.

> **Unrelated but flagged:** `manooch-planings/core/sms/armaghan/readme` holds the live Armaghan
> username and password in plaintext, in a git-tracked repo. Worth rotating and moving to the
> server `.env` regardless of anything else in this plan.

## Phase 1 — Flip production to Armaghan

One line, no rebuild. The image already contains both providers.

```bash
cp .env .env.bak.$(date +%Y%m%d%H%M%S)
sed -i 's/^SMS_PROVIDER=melipayamak$/SMS_PROVIDER=armaghan/' .env
grep '^SMS_PROVIDER=' .env
docker compose -f docker-compose.prod.yml up -d api
```

End-to-end verification (`SHAHKAR_MODE=off`, so no national ID needed):

```bash
curl -X POST https://api.manooch.site/auth/request-otp \
  -H 'Content-Type: application/json' -d '{"mobile":"09928456285","mode":"sign-in"}'
docker logs manooch-api --since 5m 2>&1 | grep SmsService
```

**Pass:** the log reads `OTP sent: provider=armaghan mobile=0992***285 reference=<id> status=sent`
(note `reference` is now a real id — Melipayamak always logged `n/a`), the SMS arrives, and the code
completes a real login.

Watch for the silent-failure mode: with `SMS_ENABLED=true` but a provider that reports
`isConfigured() === false`, `SmsService.sendOtp` returns `null` and the response carries the mock
code `11111` with a 200 and no error. If you see `11111`, the env is wrong, not the provider.
`GET /super-admin/otp` (`SuperAdminGuard`) lists the codes actually persisted per phone if you want
to cross-check what was stored against what the handset received.

**Rollback:** set `SMS_PROVIDER=melipayamak`, `up -d api`. Keep this available — do not start Phase 3
until Armaghan has carried real traffic for a soak period you're comfortable with (a day of live
logins is reasonable).

## Phase 2 — Branch

```bash
git -C C:/Sanji/Manooch-Deps/manooch-backend checkout main
git -C C:/Sanji/Manooch-Deps/manooch-backend pull
git -C C:/Sanji/Manooch-Deps/manooch-backend checkout -b remove-melipaymak
```

## Phase 3 — Remove Melipayamak from `manooch-backend`

The whole surface is 16 files, **all in `manooch-backend`** — a repo-wide grep finds zero frontend,
CMS, or shared-types references. No DB column or enum stores a provider name (`SmsMessage` has only
`providerMessageId`), so **no migration and no data backfill are needed.**

Scope per your decision: delete the Melipayamak implementations and the `SMS_PROVIDER` selection,
but keep the `OTP_SMS_PROVIDER` / `BULK_SMS_PROVIDER` tokens and the `OtpSmsProvider` interface. The
bulk token is still genuinely needed — it switches between `FakeSmsProvider` and the real provider on
`SMS_ENABLED` — and the OTP seam is what made this migration reversible.

### Delete

- `src/modules/sms/providers/melipayamak-otp.provider.ts` + `.spec.ts`
- `src/modules/sms/providers/meli-payamak.provider.ts` (no spec exists)
- `src/modules/sms/providers/sms-provider.selection.ts` + `.spec.ts`

No npm dependency to drop — Melipayamak was called over plain `fetch`, not an SDK.

### Rewire

**`src/modules/sms/sms.module.ts`** — drop the `MelipayamakOtpProvider` provider and the
`resolveSmsProvider` factory; the token binding collapses to:

```typescript
{ provide: OTP_SMS_PROVIDER, useExisting: ArmaghanOtpProvider }
```

**`src/modules/sms/sms-marketing.module.ts`** — drop `MeliPayamakProvider` from `providers` and from
the factory's `inject`; the `BULK_SMS_PROVIDER` factory keeps only the `SMS_ENABLED` branch:

```typescript
useFactory: (configService: ConfigService, fake: FakeSmsProvider, armaghan: ArmaghanProvider) =>
  configService.get<string>('SMS_ENABLED') === 'true' ? armaghan : fake,
inject: [ConfigService, FakeSmsProvider, ArmaghanProvider],
```

**`src/modules/sms/sms.service.ts`** — remove the `resolveSmsProvider` import and the
`providerName` local; the two log lines hardcode `provider=armaghan`. Everything else here
(normalization, the `SMS_ENABLED` gate, `maskMobile` logging) is provider-agnostic and stays.

**Guard against the stale env var.** Deleting `resolveSmsProvider` makes `SMS_PROVIDER` dead config,
and prod's `.env` still carries it — a silently-ignored var that reads as if it still works is the
exact footgun that caused this whole episode. Add a short constructor check in `SmsService`: if
`SMS_PROVIDER` is set to anything other than `armaghan`/`hisms`, log an error naming it as ignored.
Cheap, and it makes a bad `.env` loud instead of silent.

### Doc-comment cleanup (each currently names Melipayamak)

- `providers/otp-sms-provider.interface.ts` — the `code` and `reference` field docs both explain
  Melipayamak's divergent behavior. Rewrite for Armaghan-only: `code` is always the code passed in,
  `reference` is always a real message id. **Keep both fields and keep `AuthService` persisting
  `sent.code`** — that indirection costs nothing and is the correct contract.
- `providers/sms-provider.interface.ts:1-3` — the `BULK_SMS_PROVIDER` naming comment cites the
  `SMS_PROVIDER` env var that no longer exists.
- `providers/armaghan.provider.ts`, `providers/armaghan-otp.provider.ts` — comments contrasting with
  Melipayamak.
- `src/auth/auth.service.ts:113-119` — comment block explaining the two providers' differing code
  generation; simplify to Armaghan's behavior.
- `src/auth/auth.controller.ts:35` — the Swagger `summary` string says *"sent via Melipayamak or
  Armaghan (SMS_PROVIDER)"*. This is user-visible in `/api-docs`.
- `src/auth/auth.service.spec.ts:180-205` — two test names and a comment block describe
  "Armaghan-style" vs "Melipayamak-style" code handling. Both assertions stay valid (the contract is
  still "persist what the provider returned"); rename them to describe the contract rather than the
  vendor.

### Env templates

- `.env.example:52,55-57` — remove `SMS_PROVIDER` and the three `MELIPAYAMAK_*` lines.
- `.env.production.example:62,67-69` — same.
- Note in the comment block that Armaghan is the only provider and that `panel.hisms.ir` requires the
  server's outbound IP to be whitelisted in the panel — the failure mode is a bare 5s timeout, not an
  `errorCode`, which is easy to misread as a network fault.

There is **no env validation schema** in this repo (`ConfigModule.forRoot({ isGlobal: true })` at
`src/app.module.ts:107`, no Joi/Zod), so `.env.example` is the de-facto schema. Keeping it accurate
matters more here than in a repo that validates at boot.

## Phase 4 — Verify, push, deploy

```bash
cd C:/Sanji/Manooch-Deps/manooch-backend
npx tsc --noEmit          # pre-push hook runs this; catches any dangling import
npm test                  # 65 spec files; SMS + auth suites are the ones that matter
npm run lint
```

Expect the two deleted spec files to disappear from the run and everything else to stay green.

Push `remove-melipaymak` and open the PR yourself — I won't run `gh pr create`.

**After the PR merges and deploys**, clean the production `.env` in the same session (it is not
git-tracked, so `deploy.sh`'s `git reset --hard` never touches it):

```bash
cp .env .env.bak.$(date +%Y%m%d%H%M%S)
# remove SMS_PROVIDER and MELIPAYAMAK_* lines
docker compose -f docker-compose.prod.yml up -d api
```

Then re-run the Phase 1 end-to-end OTP check as the final confirmation, and revoke the Melipayamak
API key from their console so a stale copy in an old `.env.bak.*` can't be used. Note there are
already two untracked `.env.bak.*` files on the server holding old credentials — worth pruning.

## Verification summary

1. Phase 0 curl returns `errorCode: 0` with a reference id, and code `55731` arrives on `09928456285`.
2. Phase 1 log line reads `provider=armaghan` with a non-`n/a` reference, the OTP arrives, and login
   completes.
3. `npx tsc --noEmit`, `npm test`, `npm run lint` all pass on `remove-melipaymak`.
4. `grep -ri melipayamak src/ .env.example .env.production.example` returns nothing.
5. Post-deploy OTP to `09928456285` still lands, with `SMS_PROVIDER` absent from prod `.env`.

## Out of scope

`manooch-planings/core/sms/armaghan/*` still describes the pre-move state (server abroad, template
blank, IP not whitelisted). Those docs are now stale but live in a different repo; updating them is a
separate commit there, not part of the backend PR.
