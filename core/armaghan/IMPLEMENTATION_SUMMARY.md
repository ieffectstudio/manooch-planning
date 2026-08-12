# Implementation Summary — Melipayamak → Armaghan SMS Migration

**Repo:** `manooch-backend`
**Branch:** `feat-replace-meli-vs-armaghan` (pushed to `origin`, working tree clean)
**PRD:** [`PRD_ARMAGHAN_MIGRATION.md`](./PRD_ARMAGHAN_MIGRATION.md)
**Status:** Armaghan integration built and working against the live account, but **not the active provider in prod yet** — see "Current state" below.

## What shipped

Four commits, in order:

1. **`ae3f082` — Replace Melipayamak SMS with Armaghan SMS WebService (OTP + bulk)**
   - `ArmaghanClient`: shared JSON-POST wrapper handling big-int-safe reference/id parsing and `errorModel` error-code mapping into `ArmaghanApiException`.
   - `normalizeIranianMobile`: standardizes `+98` / `0098` / `98` / bare formats (incl. Persian/Arabic-Indic digit folding) to `09XXXXXXXXX`.
   - `SmsService.sendOtp` rewritten to call Armaghan's `sendParameterizedMessage`. Unlike Melipayamak, Armaghan does not generate the OTP code itself, so `AuthService.requestOtp` now generates the 5-digit code via `crypto.randomInt` before dispatch.
   - `MeliPayamakProvider` replaced by `ArmaghanProvider` (`sendMessageOneToMany` for bulk/marketing sends, `getMessageState` for real delivery-status polling — previously always stubbed as `'pending'`).
   - `MELIPAYAMAK_*` env vars swapped for `ARMAGHAN_*` in both `.env.example` and `.env.production.example`.
   - Frontend OTP request/response contract unchanged — only the backend provider integration moved.

2. **`1460236` — Fix generic type constraint in armaghan.client.spec.ts**
   - `client.post<T>` requires `T extends ArmaghanBaseResponse`; a test's intersection type didn't satisfy that and broke `tsc --noEmit` in the pre-push hook.

3. **`b6293c9` — fix(sms): point Armaghan client at the HiSMS API host**
   - `panel.armaghan.net` refuses connections outright — it was never a reachable API host, so nothing could have sent through it regardless of config.
   - `armaghan.net` and `hisms.ir` are the same platform under two brands, but only `panel.hisms.ir` serves `/webservice/*`. Verified live: `getUserInfo` against `panel.hisms.ir` returns `{"errorCode":0,"userInfo":{"credit":0}}`.
   - Fixed the hardcoded `DEFAULT_BASE_URL` fallback and both env examples. Documented that the host firewalls TCP 443 to IPs whitelisted in the Armaghan panel — an unwhitelisted caller gets a bare timeout, **not** error `-110`, which is easy to misdiagnose as a network fault rather than a whitelisting issue.

4. **`92d7178` — feat(sms): make SMS provider selectable via SMS_PROVIDER, default melipayamak**
   - Reason: Armaghan/HiSMS still had a blank `ARMAGHAN_OTP_TEMPLATE_ID` and prod's outbound IP was still un-whitelisted by HiSMS at merge time. The branch as of commit 1 had deleted Melipayamak entirely, which meant merging would leave prod with **no working SMS provider** — and with `SMS_ENABLED=true` plus a blank template, OTP would have silently fallen back to the mock code (`11111`), echoed straight into the response body.
   - Restored Melipayamak as a full second provider (OTP + bulk), gated both providers behind a new `SMS_PROVIDER` env var (`melipayamak` default, `armaghan`/`hisms` opt-in).
   - Introduced an `OtpSmsProvider` abstraction so `SmsService` delegates to either implementation. The provider's returned code is now authoritative — Armaghan echoes back the code it's given, Melipayamak generates its own — so `AuthService` stores whichever code the active provider actually sent, instead of assuming Melipayamak's generation behavior.
   - Prod's `.env` already had both credential blocks in place; only `SMS_PROVIDER` needed adding (defaults to `melipayamak`), so merging reproduces current prod behavior exactly. Flipping to Armaghan later is a one-line env change once the template ID and IP whitelist are sorted — no rebuild required.

## Key files touched (backend)

- `src/modules/sms/providers/armaghan.client.ts` (+spec) — low-level HTTP wrapper
- `src/modules/sms/providers/armaghan.provider.ts` (+spec) — bulk/marketing provider
- `src/modules/sms/providers/armaghan-otp.provider.ts` (+spec) — OTP provider
- `src/modules/sms/providers/armaghan-api.exception.ts` — errorModel → exception mapping
- `src/modules/sms/providers/melipayamak-otp.provider.ts` (+spec) — restored OTP provider
- `src/modules/sms/providers/meli-payamak.provider.ts` — restored bulk provider
- `src/modules/sms/providers/otp-sms-provider.interface.ts` — new provider abstraction
- `src/modules/sms/providers/sms-provider.selection.ts` (+spec) — `SMS_PROVIDER` selection logic
- `src/modules/sms/utils/normalize-mobile.ts` (+spec) — Iranian mobile normalizer
- `src/modules/sms/sms.service.ts`, `sms.module.ts`, `sms-marketing.module.ts`, `sms-outbox.service.ts`
- `src/auth/auth.service.ts`, `auth.controller.ts` — OTP code generation/storage now provider-agnostic
- `.env.example`, `.env.production.example`

## Current state vs. PRD acceptance criteria

The PRD (Section 6) asked for a **full** decommission of Melipayamak. That was done in commit 1, then deliberately partially reverted in commit 4 as a production-safety measure:

- [x] Armaghan REST API v2 wrapper implemented and verified live (`getUserInfo` succeeds against `panel.hisms.ir`)
- [x] Originator `50002062088` wired as the configured sender
- [x] OTP sent via `sendParameterizedMessage` with `ARMAGHAN_OTP_TEMPLATE_ID`
- [x] Error codes mapped per Section 3.2 (`ArmaghanApiException`)
- [x] `.env.example` updated with `ARMAGHAN_*` params
- [ ] **Melipayamak fully removed** — intentionally *not* done; kept as the default live provider until Armaghan is ready (see below)
- [ ] **Armaghan live in prod** — blocked, not yet flipped on

## Outstanding blockers to actually cutting over

1. `ARMAGHAN_OTP_TEMPLATE_ID` is still blank — needs the pattern code from the Armaghan/HiSMS panel.
2. Prod's outbound IP is still not whitelisted on `panel.hisms.ir` (firewalled at TCP 443; failure mode is a silent timeout, not an `errorCode`).
3. Once both are resolved: flip `SMS_PROVIDER=armaghan` in prod `.env` — no rebuild needed.
4. After Armaghan is confirmed stable in prod, Melipayamak code can be removed to satisfy the PRD's original "full decommission" requirement.

## Note on credentials

`core/armaghan/readme` in this planning repo currently contains a plaintext username/password. Recommend moving those into a secrets manager or the actual `.env` (git-ignored) rather than a planning doc, since this directory is tracked in git.

---
*This file is local to `manooch-planning` and has not been committed or pushed, per instruction.*
