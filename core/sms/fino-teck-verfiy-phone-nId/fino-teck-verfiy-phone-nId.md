# Shahkar Pre-OTP Verification — PRD (concise v1.1)

## Goal
Verify NID+mobile ownership via Finnotech Shahkar BEFORE sending OTP. Block mismatch, cut SMS cost, KYC compliance.

## Flow
1. User submits `mobile` + `nationalCode` (required for sellers & customers)
2. Server validates: mobile `^09\d{9}$`, NID = 10 digits + checksum (sum i×weight, %11 rule)
3. Cache check (24h, key `shahkar:{sha256(mobile:nationalCode)}`) → hit = return cached, no API call
4. Call Finnotech `shahkarVerify` (timeout 10s)
5. No errorCode + `isMatch=true` → send OTP. Mismatch → block with SHAHKAR_MISMATCH. Error → fallback rules (§Fallback)
6. Log audit row (hashed NID/mobile, masked mobile `09***789`, trackId, result, errorCode, latency)

## API
- Prod: `POST https://api.finnotech.ir/facility/v2/clients/{clientId}/shahkarVerify?trackId={uuid}` — JSON body `{mobile, nationalCode}`, header `Authorization: Bearer {token}`
- Sandbox (free): `https://apibeta.finnotech.ir`
- Token: `POST /dev/v2/oauth2/token` grant `client_credentials`; cache in Redis, refresh 5 min before expiry
- Scope: `kyc:shahkar-verify:get`
- Alt endpoint (fallback only, async, costs SMS too): `/kyc/v2/clients/{clientId}/shahkar/smsSend?trackId=&mobile=&nationalCode=` — sends SMS, poll result by trackId. NID in query string = log-leak risk; prefer POST body variant.

## Response handling (v1.1 — critical)
- Success: HTTP 200 `{status:"DONE", trackId, result:{isMatch, isMatchSpecified}}`
- Business errors come as `errorCode` inside 200/400 body. **ALWAYS check `errorCode` before reading `result`** (v1.0 crashed with KeyError on mismatch).
- Mismatch = `FN-KCFH-200001000005` → return `is_match:false` (business outcome, NOT exception)

| Finnotech errorCode | Meaning | Action |
|---|---|---|
| FN-KCFH-200001000005 | NID+mobile mismatch | Block, SHAHKAR_MISMATCH, no retry |
| FN-KCKZ-40000830030 | daily query quota exhausted | Rate-limit message, no retry, alert ops (NOT HTTP 429) |
| FN-KCFH-40400030038 | request not found (bad/expired trackId) | regenerate trackId, retry once |
| FN-KC*-5xxxx (e.g. FN-KCAA-50000860000, FN-KCHR-50001060000, FN-KCKZ-50000199999) | network/system | retry ≤2, then 502 |
| FN-KCFH-20000400001, FN-KCFH-20000300002, FN-KCFH-40000230042 | NID already submitted/registered | idempotent success ALREADY_VERIFIED (use cache) |
| FN-KCFH-40000130009, 400006300127, 40000230060 | invalid/missing NID | INVALID_NID, no retry |
| FN-KCFH-40000130057, 40000230041 | invalid/missing mobile | INVALID_MOBILE, no retry |
| FN-KCFH-40000130058 | NID or mobile invalid | INVALID_NID_OR_MOBILE |
| FN-KCFH-40000530039 | validation error | generic 422 |
| FN-KCFH-40000430035 | invalid OTP or mobile | OTP_INVALID |
| FN-KCFH-40000430036, 40000230063 | invalid OTP trackId | OTP_TRACK_INVALID |
| FN-KCKZ-40000430037, FN-KCKZ-20000530037 | user on bank blacklist | block registration |
| FN-KCFH-40000830046 | NID of deceased person | block with clear msg |
| FN-KCFH-200004000004, FN-KCKZ-200005000004 | NID is bank customer | block |
- Transport: 401 → refresh token, retry once; 403 → stop + alert; 5xx/timeout → retry.

## Fallback rules
- Retry (max 2, backoff 1.5): timeouts, HTTP 401/5xx, any `FN-KC*-5xxxx`.
- Never retry: 4xx validation, mismatch, quota, blacklist, bank-customer, deceased.
- After retries fail → **Option B: block & notify user to retry later** (financial app).
- Corporate SIM / ambiguous → show unsupported message (US-05).

## Client pattern
```python
data = (await client.post(url, params={"trackId": tid}, json=body,
        headers={"Authorization": f"Bearer {token}"})).json()
if data.get("errorCode"):
    return handle_error(data)   # mismatch→is_match False; 5xx→raise retryable; quota→raise; 404→raise notfound; else→raise 400
return {"is_match": data["result"]["isMatch"], "status": data["status"], "track_id": data["trackId"]}
```
Cache `is_match` in Redis 24h; own rate limit 3/hour/user before calling Finnotech.

## User messages (FA / EN)
- mismatch: شماره موبایل به این کد ملی تعلق ندارد / Mobile number does not belong to this National ID
- timeout/5xx: سرویس در دسترس نیست، لطفا مجددا تلاش کنید / Service unavailable, please try again
- rate limit: سقف استعلام روزانه تکمیل شده / Daily limit reached, try later
- invalid NID / mobile: کد ملی / شماره موبایل نامعتبر است

## DB
- `shahkar_verifications`: track_id (unique), mobile_hash, national_code_hash, mobile_masked, is_match, status, error_code, response_time_ms, created_at
- `shahkar_cache`: mobile_hash+national_code_hash (unique), is_match, expires_at (24h)

## Security & compliance
- HTTPS only; token server-side encrypted; mask/hash PII in logs; audit trail 7y; user consent + privacy policy; DPA with Finnotech; never send NID+mobile to unlicensed third parties.

## Env vars
`FINNOTECH_CLIENT_ID / CLIENT_SECRET / BASE_URL=https://api.finnotech.ir / SANDBOX_URL=https://apibeta.finnotech.ir`, `SHAHKAR_ENABLED=true`, `SHAHKAR_CACHE_TTL=86400`, `SHAHKAR_MAX_RETRIES=2`, `SHAHKAR_TIMEOUT_SECONDS=10`, `SHAHKAR_RATE_LIMIT_PER_USER=3`

## Testing (sandbox)
- NID `0079893853` + `09120000000` → match; + `09121111111` → mismatch (confirm with Finnotech)
- Cases: mismatch→is_match false no 500; quota→"try later"; 404→new trackId; duplicate→success; 5xx→retry then 502; cache hit; 401 refresh; 403 alert.

## Cost notes
- No free government API; official tariff tiered (382/200/100 toman per query — 2019 figures, higher today); aggregators ≈500–1,500+ toman/query; smsSend 2–3× more.
- Cut cost: cache 24h, rate-limit, verify only at registration (not per login), negotiate volume tier. Sandbox is free.

---
*v1.1 — updated 2026-08-11. Key changes vs v1.0: errorCode-first parsing, mismatch is error code not isMatch=false, quota is code not HTTP 429, retry driven by codes, added 404/duplicate/blacklist/deceased/OTP codes.*
