# PRD — Iran Locations Module (NestJS)

> **Handoff instructions for Claude:** Implement this PRD in full in the user's NestJS backend.
> Read every section — including the "Upstream API Reference" and "Appendix" — before writing code.
> Follow the folder structure, type names, DTOs, and acceptance criteria exactly.
> Do not skip the fallback/caching requirements in Section 6 — they are mandatory, not nice-to-have.

---

## 1. Document Control

| Field | Value |
|---|---|
| Title | Iran Locations (Provinces & Cities) Integration |
| Doc version | 1.0 |
| Date | 2026-08-09 |
| Status | Approved for implementation |
| Audience | Backend engineers (NestJS), Claude (implementer) |
| Upstream API | https://www.iran-locations-api.ir/ (free, no API key, open source) |
| Upstream source repo | https://github.com/hamidrezaramzani/iran-locations-api |

---

## 2. Overview & Goals

### 2.1 Problem statement
The product needs Iranian province (استان) and city (شهر) data for:
1. **Frontend dropdowns / autocomplete** — select a province, then a city (persian and english).
2. **Persisting a user's location** — each user can store their province + city; the backend must validate that the chosen city actually belongs to the chosen province.
3. **Filtering** — by name, province id, landline prefix, car licence plate.

### 2.2 Goals
- G1: A NestJS module that exposes clean, typed, normalized endpoints for provinces and cities in both `fa` and `en`.
- G2: The backend never breaks if the upstream API is down (it is currently returning HTTP 500 on its data routes as of 2026-08-09 — this is a real, observed condition).
- G3: Users can store a validated province/city location on their profile.
- G4: Responses are fast (< 50 ms p95 after warm-up) and cheap on upstream traffic.

### 2.3 Non-goals (out of scope)
- Geo queries (distance, radius, bounding box).
- District/neighborhood data, postal codes, timezones.
- Admin CRUD for locations.
- Translation of user-entered names.

---

## 3. Upstream API Reference (verified 2026-08-09)

> Source of truth: the open-source repo `hamidrezaramzani/iran-locations-api` (files `lib/state.ts`, `lib/city.ts`, `pages/api/v1/{fa,en}/{states,cities}.ts`). The live API currently returns **500** on these routes (Vercel), which is why fallback is mandatory (Section 6).

### 3.1 Base paths
- Persian: `https://www.iran-locations-api.ir/api/v1/fa`
- English: `https://www.iran-locations-api.ir/api/v1/en`
- Free, **no API key**, CORS enabled, JSON responses only.

### 3.2 Endpoint: `GET /api/v1/{fa|en}/states`

| Query param | Type | Behavior |
|---|---|---|
| *(none)* | — | All 31 provinces (each WITHOUT the `cities` field) |
| `id` | number | Single province object (not wrapped in array). `id` must be numeric, else 400. |
| `state` | string | Case-insensitive substring match on province name; returns array. |
| `landlinePrefix` | string | Exact match; **must start with `0`** (e.g. `041`), else 400. |
| `carLicencePlate` | string/number | Exact match against `carLicencePlates` array; must be numeric, else 400. |

**Province record shape (verified sample, fa):**
```json
{
  "name": "آذربايجان شرقی",
  "center": "تبریز",
  "latitude": "38.50",
  "longitude": "46.180",
  "landlinePrefix": "041",
  "carLicencePlates": ["15", "25", "35"],
  "id": 1
}
```

### 3.3 Endpoint: `GET /api/v1/{fa|en}/cities`

| Query param | Type | Behavior |
|---|---|---|
| *(none)* | — | All ~344 cities flattened (fa) / ~346 (en) |
| `state_id` | number | All cities of that province (id 1–31); must be numeric, else 400. |
| `state` | string | Substring match on province name; response is an array of wrapper objects `{ "cities": [...] }` (one per matched province) |
| `city` | string | Substring match on city name |

**⚠️ Upstream quirks the NestJS layer MUST normalize away:**

| # | Quirk | Detail |
|---|---|---|
| Q1 | City `id` is **not globally unique** | City ids are per-province (verified: only 26 unique ids across 344 cities). `cityId` alone is ambiguous — persistence MUST store `(provinceId, cityId)` as a pair and validate membership. |
| Q2 | City `id` is inconsistently present | Omitted when querying all cities or by `city`/`state` name; present when querying by `state_id`. |
| Q3 | Cities have **no province reference** | A city record is just `{name, latitude, longitude, id?}` — no provinceId/provinceName. The NestJS layer must attach `provinceId`/`provinceName`. |
| Q4 | `state` filter on cities wraps in `{cities:[...]}` | Non-uniform shape vs `state_id` (bare array). Normalize. |
| Q5 | Coordinates are strings | e.g. `"38.50"`, `"46.180"` — keep as strings or parse to numbers consistently; do NOT mix. |
| Q6 | Duplicate city names exist | Verified: `اردكان`, `حاجي آباد`, `قشم`, `دزفول`, `ايرانشهر`, `شادگان` appear in >1 province. Never treat city name as unique. |
| Q7 | `id` filter response is a bare object | States with `?id=` returns `{...}` not `[{...}]`. Do not assume array. |
| Q8 | Invalid params → HTTP 400 | Error body: `{"message": "<error text>"}` (English, even for fa). |

### 3.4 Dataset facts (verified)
- 31 provinces (`id` 1–31), fa dataset has 344 cities, en dataset has 346.
- Raw data files (MIT-ish, open source, in the upstream repo):
  - fa: `public/iran_cities_with_coordinates.json` (~45 KB)
  - en: `public/iran_cities_in_english.json` (~46 KB)
- Download URLs (pinned, for the fallback bundle):
  - `https://raw.githubusercontent.com/hamidrezaramzani/iran-locations-api/main/public/iran_cities_with_coordinates.json`
  - `https://raw.githubusercontent.com/hamidrezaramzani/iran-locations-api/main/public/iran_cities_in_english.json`

### 3.5 Upstream sample response (full states list, fa)
```json
[
  {
    "name": "آذربايجان شرقی",
    "center": "تبریز",
    "latitude": "38.50",
    "longitude": "46.180",
    "landlinePrefix": "041",
    "carLicencePlates": ["15", "25", "35"],
    "id": 1
  }
]
```

---

## 4. Architecture Decision: Hybrid (live proxy + cache + bundled fallback)

```
                        ┌─────────────────────────────────────────────┐
                        │            NestJS backend                    │
                        │                                             │
 Client ──► Controllers ─► LocationsService ──► Upstream HTTP fetch   │
 (frontend)             │       │    │              (axios/fetch)     │
                        │       │    │                  │             │
                        │       │    └──► In-memory cache ◄──┘        │
                        │       │         (per lang dataset, TTL)     │
                        │       │              │ fail                 │
                        │       └──────────────┼──────────────► Bundled│
                        │                      │            JSON files │
                        │                      ▼             (fallback)│
                        │             Normalization + filtering        │
                        │             (single code path)               │
                        └─────────────────────────────────────────────┘
```

**Rules (mandatory):**
1. **Fetch once, serve many.** The whole dataset is ~45 KB per lang. On first request for a lang, fetch the *full* states list (and build the city index from it). All subsequent queries are answered from memory. This mirrors how the upstream itself works (it loads a JSON file into memory).
2. **Filter locally, never forward per-request params.** After warm-up, the upstream API is only contacted for TTL revalidation, so per-request latency and upstream load are ~zero.
3. **Fallback on any upstream failure** (network error, non-2xx, timeout, malformed JSON): load the bundled JSON copy and log a warning. The API keeps serving.
4. **No data is written to the DB except the user's chosen location** (Section 7). Provinces/cities themselves are never persisted to the database in this iteration (kept in memory + bundled files).

---

## 5. Functional Requirements — NestJS Endpoints

Base path for all location endpoints: `/api/v1/locations` (adjust to project convention if the app already version-prefixes).

### 5.1 `GET /api/v1/locations/states`
List provinces.

| Query param | Type | Required | Validation | Behavior |
|---|---|---|---|---|
| `lang` | string | no (default `fa`) | enum `fa` \| `en` (400 if invalid) | Dataset language |
| `id` | int | no | `@IsInt` / transform | Single province (bare object) |
| `q` | string | no | — | Case-insensitive substring on `name` (aliases upstream `state`) |
| `landlinePrefix` | string | no | must start with `0` (400 otherwise) | Exact match |
| `carLicencePlate` | string | no | numeric (400 otherwise) | Exact match on `carLicencePlates` |

**Response 200 — list (normalized, array):**
```json
[
  {
    "id": 1,
    "name": "آذربايجان شرقی",
    "center": "تبریز",
    "latitude": "38.50",
    "longitude": "46.180",
    "landlinePrefix": "041",
    "carLicencePlates": ["15", "25", "35"]
  }
]
```
**Response 200 — `?id=1` (bare object, NOT wrapped in array):** same record shape, no array.

**Errors:** `400 {"statusCode":400,"message":"..."}` for invalid params; `404 {"statusCode":404,"message":"Province with id 99 not found"}` when `id` matches nothing (upstream returns `{}` — we must return a proper 404 instead).

### 5.2 `GET /api/v1/locations/states/:stateId/cities`
Cities of one province (the standard dropdown flow).

| Param/Query | Type | Required | Validation |
|---|---|---|---|
| `stateId` (path) | int | yes | `@IsInt`, 1–31; 404 if unknown province |
| `lang` | query | no (default `fa`) | enum |

**Response 200:**
```json
[
  {
    "id": 3,
    "provinceId": 1,
    "provinceName": "آذربايجان شرقی",
    "name": "تبريز",
    "latitude": "38.50",
    "longitude": "46.180"
  }
]
```
Note: `provinceId`/`provinceName` are attached by our layer (fixes upstream Q3). City `id` normalized to always be present (fixes Q2).

### 5.3 `GET /api/v1/locations/cities`
City search.

| Query param | Type | Required | Validation | Behavior |
|---|---|---|---|---|
| `lang` | string | no (default `fa`) | enum | Dataset language |
| `q` | string | no | — | Substring on city `name` (aliases upstream `city`) |
| `stateId` | int | no | `@IsInt` | Filter to one province |
| `state` | string | no | — | Substring on province name (kept for parity; `stateId` is preferred) |

**Response 200 — always a flat array of city records** (same shape as 5.2, with `provinceId` + `provinceName`). Fixes upstream Q4 (`{cities:[...]}` wrappers are flattened) and Q2.

**Behavior:** `q` and `stateId`/`state` compose with AND. Empty `q` + no state filter returns all cities (fine — it's ~344 records, < 20 KB; client pagination is out of scope, note in docs).

### 5.4 `PATCH /api/v1/users/me/location`
Persist the authenticated user's location (see Section 7).

```json
// Request body
{
  "provinceId": 1,
  "cityId": 3
}
```
**Validations:** both required ints; province must exist; **city must belong to that province** (composite check — see 7.3). 404 if province unknown; 422/400 with a specific message if city is not in the province (e.g. `"City with id 3 does not exist in province 1"`).

**Response 200:**
```json
{
  "provinceId": 1,
  "cityId": 3,
  "provinceName": "آذربايجان شرقی",
  "cityName": "تبريز"
}
```

### 5.5 Conventions for all endpoints
- `lang` enum validation via `class-validator` `@IsIn(['fa','en'])` on a DTO.
- Query params transformed with `@Type(() => Number)` where numeric.
- All responses snake_case or camelCase — **match the existing project convention**; DTOs must explicitly map fields so the shape is intentional.
- Document endpoints in the project's OpenAPI/Swagger setup with `@ApiOperation`/`@ApiQuery`/`@ApiResponse` decorators.

---

## 6. Non-Functional Requirements

| ID | Requirement | Spec |
|---|---|---|
| NFR-1 | Warm-up latency | First request per lang ≤ 2 s (upstream fetch); every request after ≤ 50 ms p95. |
| NFR-2 | Upstream resilience | Any upstream failure (5xx, timeout, network, invalid JSON) → serve bundled fallback data, log warning, never propagate 5xx to client *for data reads*. |
| NFR-3 | Upstream timeouts | HTTP client timeout: 3 s connect, 5 s response (env-configurable). Use `AbortController`/axios `timeout`. |
| NFR-4 | Cache TTL | 24 h default for full datasets, env-configurable. On expiry, refresh in the background; stale data stays available during refresh (see 6.1). |
| NFR-5 | Concurrency | Only one in-flight upstream request per lang (promise deduplication — see 6.2). |
| NFR-6 | Config | All knobs via `ConfigService`: `IRAN_LOCATIONS_API_BASE_URL`, `IRAN_LOCATIONS_CACHE_TTL_SECONDS`, `IRAN_LOCATIONS_HTTP_TIMEOUT_MS`, `IRAN_LOCATIONS_FALLBACK_DIR` (or paths). Provide sensible defaults so the app works with zero env setup. |
| NFR-7 | Observability | Log on: upstream success/failure, fallback activation, cache refresh. Include `lang` and latency. No PII. |
| NFR-8 | Security | No auth required for read endpoints (public data); `PATCH /users/me/location` requires the existing auth guard. Validate everything with DTOs — never trust upstream JSON types (defensive parsing). |
| NFR-9 | Multi-instance | In-memory cache is per-instance (acceptable for this data). If the project already uses Redis, MAY back the cache with `@nestjs/cache-manager` + redis store — but bundled fallback must still work. |

### 6.1 Cache design (exact)
- Structure: one entry per lang → `{ states: [...], citiesIndex: Map<stateId, city[]> , fetchedAt, rawUpstream? }`.
- Read path: if entry exists and TTL not exceeded → serve. If expired → serve stale data **and** trigger background refresh (no blocking).
- Refresh failure → keep serving stale + log.
- No entry (cold start) → fetch upstream with promise dedup; on failure → load bundled JSON into the same structure and log `LOCATIONS_FALLBACK_ACTIVATED`.

### 6.2 Upstream client
- Single `LocationsUpstreamClient` (or service) wrapping `HttpService`/`fetch` with timeout, retry policy (max 2 retries, exponential backoff 200 ms / 400 ms, only on 5xx/network errors), and per-lang in-flight promise deduplication.

---

## 7. Persistence — User Location

### 7.1 Data model
Add to the existing `User` entity (or a dedicated `UserLocation` table — follow project pattern; recommendation below):

```ts
// Recommended: columns on users table (simple, one location per user)
userId: string (PK, existing)
provinceId: number | null      // FK-less (locations are not DB rows) — document this
cityId: number | null
updatedAt: timestamp
```

- If the project prefers normalized tables: `user_locations(user_id PK/FK, province_id int, city_id int, updated_at)`. Either is acceptable; **do not** create `provinces`/`cities` tables in this iteration.
- Migration must be additive and reversible.

### 7.2 Validation rule (critical)
```ts
// Pseudo — must run inside the LocationsService so it uses the same
// cached/normalized data the read endpoints use
async validateLocation(provinceId: number, cityId: number) {
  const province = await this.getStateById(provinceId);        // 404 if missing
  const city = await this.getCity(provinceId, cityId);          // 422 if not in province
  return { province, city };
}
```
Why composite: upstream city ids are **per-province** (Q1). `cityId: 3` is ambiguous on its own — it exists in province 1, 7, 12, … always resolve via `(provinceId, cityId)`.

### 7.3 Response enrichment
`GET /users/me` (or wherever the user profile is returned) must include the resolved names: `provinceName`, `cityName`, resolved through the same LocationsService. If the stored ids no longer exist in the dataset (data drift), return the ids with `provinceName: null` — do not fail the whole profile request.

---

## 8. Technical Design — File Layout & Types

```
src/
├── locations/
│   ├── locations.module.ts
│   ├── locations.controller.ts          # read endpoints 5.1–5.3
│   ├── locations.service.ts             # orchestration: cache → fallback → filter/normalize
│   ├── locations-upstream.client.ts     # HTTP + retry + timeout + dedup (6.2)
│   ├── locations.cache.ts               # in-memory store per lang (6.1)
│   ├── locations.normalizer.ts          # upstream JSON → internal normalized model (fixes Q1–Q8)
│   ├── dto/
│   │   ├── get-states-query.dto.ts
│   │   ├── get-cities-query.dto.ts
│   │   ├── state-response.dto.ts
│   │   └── city-response.dto.ts
│   ├── interfaces/
│   │   ├── state.interface.ts           # internal State
│   │   └── city.interface.ts            # internal City (with provinceId, provinceName)
│   └── fallback/
│       ├── iran_cities_with_coordinates.json   # pinned fa copy
│       └── iran_cities_in_english.json         # pinned en copy
├── users/
│   ├── dto/update-user-location.dto.ts  # 5.4 body
│   ├── users.controller.ts              # + PATCH /users/me/location
│   └── users.service.ts                 # + validateLocation integration (7.2)
└── ...
```

### 8.1 Internal types (exact)
```ts
// locations/interfaces/state.interface.ts
export interface State {
  id: number;
  name: string;
  center: string;
  latitude: string;   // keep upstream string format (Q5) — or number if project convention; be consistent
  longitude: string;
  landlinePrefix: string;
  carLicencePlates: string[];
}

// locations/interfaces/city.interface.ts
export interface City {
  id: number;               // upstream id, but only unique within province — always pair with provinceId
  provinceId: number;       // ADDED by normalizer (Q3)
  provinceName: string;     // ADDED by normalizer (Q3), in the requested lang
  name: string;
  latitude: string;
  longitude: string;
}
```

### 8.2 Normalizer contract (fixes every upstream quirk)
Input: raw upstream JSON (states array with nested `cities`). Output:
- `State[]` (without `cities`)
- `Map<provinceId, City[]>` and/or flat `City[]` with `provinceId`/`provinceName` attached.
Rules: strip wrapper objects (Q4), always include `id` on cities (Q2), attach province refs (Q3), validate numeric `id`s (skip malformed records + log — defensive, NFR-8).

### 8.3 Service logic (pseudocode)
```ts
async getStates(query: GetStatesQuery, lang: Lang): Promise<State | State[]> {
  const dataset = await this.getDataset(lang);       // cache → upstream → fallback
  return filterStates(dataset, query);               // pure function, unit-testable
}

async getCitiesByStateId(stateId: number, lang: Lang): Promise<City[]> {
  const dataset = await this.getDataset(lang);
  if (!dataset.states.some(s => s.id === stateId)) throw new NotFoundException();
  return dataset.citiesByProvince.get(stateId) ?? [];
}

private async getDataset(lang: Lang): Promise<Dataset> {
  // 1. cache hit (fresh) → return
  // 2. cache hit (stale) → return stale, fire background refresh (dedup)
  // 3. miss → dedup'd upstream fetch; on failure → load fallback JSON
}
```
All filter functions live in `locations.normalizer.ts` as **pure functions** so they can be unit-tested without HTTP.

---

## 9. Error Handling & Logging

| Case | HTTP | Body message (English) |
|---|---|---|
| Invalid `lang` | 400 | `lang must be one of: fa, en` |
| `id`/`stateId` non-numeric | 400 | `id must be a number` |
| `landlinePrefix` not starting with `0` | 400 | `landlinePrefix must start with 0` |
| `carLicencePlate` non-numeric | 400 | `carLicencePlate must be a number` |
| Province not found (`?id=` or `:stateId`) | 404 | `Province with id <id> not found` |
| City not in province (PATCH) | 422 | `City with id <cityId> does not exist in province <provinceId>` |
| Upstream down (reads) | 200 | — serve fallback; log `LOCATIONS_FALLBACK_ACTIVATED lang=fa reason=...` |
| Upstream down (PATCH validation) | 503 | `Location data temporarily unavailable` (only if fallback also unavailable — nearly impossible since bundled) |

Use Nest's exception filters; log via the project's logger (`Logger` or pino), never `console.log`.

---

## 10. Testing Requirements

| Layer | Tool | Must cover |
|---|---|---|
| Unit — normalizer/filters | Jest | Q2/Q4 normalization, name substring (case-insensitive), prefix/plate matching, attach province refs, malformed-record skipping |
| Unit — cache | Jest | TTL expiry, stale-while-refresh, promise dedup (single upstream call under concurrency) |
| Unit — upstream client | Jest + mocked HTTP | timeout, 5xx retry + backoff, fallback trigger on failure |
| Unit — validation service | Jest | composite (provinceId, cityId) check; 404/422 paths |
| e2e — controller | Jest e2e + mocked upstream (nock) | All endpoints: happy paths, 400/404/422 cases, `lang` switch, fallback served when upstream mocked to 500 |
| DB migration test | — | Migration up/down applies cleanly on a fresh DB |

**Acceptance criteria for tests:** `npm run test` and `npm run test:e2e` pass; coverage for `locations/` ≥ 80% lines.

---

## 11. Acceptance Criteria (Definition of Done — all must hold)

- [ ] AC-1: `GET /api/v1/locations/states?lang=fa` returns 31 normalized states; `lang=en` returns 31 English states.
- [ ] AC-2: `GET /api/v1/locations/states/:stateId/cities` returns cities with `provinceId`/`provinceName`; unknown `stateId` → 404.
- [ ] AC-3: `GET /api/v1/locations/cities?q=...&stateId=...` returns flat normalized array; filters compose (AND).
- [ ] AC-4: All upstream quirks Q1–Q8 handled: uniform shapes, always-present city ids, attached province refs, bare-object `?id=` response, 404 instead of `{}`.
- [ ] AC-5: With upstream returning 500 (simulated), all read endpoints still work from bundled fallback and a warning is logged.
- [ ] AC-6: After first request, 100 subsequent requests make **zero** upstream calls (cache) and each completes < 50 ms.
- [ ] AC-7: `PATCH /users/me/location` persists `(provinceId, cityId)`; rejects city not in province with 422; profile GET returns resolved `provinceName`/`cityName`.
- [ ] AC-8: Swagger/OpenAPI docs exist for all new endpoints.
- [ ] AC-9: Env config has defaults; app boots with no env vars set.
- [ ] AC-10: Unit + e2e suites pass; `locations/` coverage ≥ 80%.

---

## 12. Implementation Order (suggested task breakdown)

1. Scaffold module + interfaces + bundled fallback JSON files (pinned from upstream repo).
2. Normalizer + pure filter functions + unit tests (Q1–Q8 fixes).
3. Upstream client (timeout, retry, dedup) + cache (TTL, stale-while-refresh) + `getDataset` orchestration + unit tests.
4. Controller + DTOs + Swagger for read endpoints 5.1–5.3 + e2e tests.
5. User entity/migration + `PATCH /users/me/location` + validation service + profile enrichment + tests.
6. Observability pass (logs, latency) + full acceptance criteria verification.

---

## 13. Open Questions (for the product owner — do NOT block implementation)

1. Should the en dataset's 2 extra cities (346 vs 344) be reconciled? (Recommendation: no — ship both datasets as-is; ids/names stay per-lang.)
2. Do we need pagination for the full cities list? (Recommendation: not now; ~344 records ≈ 18 KB.)
3. Should a user be allowed to clear their location (PATCH with nulls)? (Recommendation: yes — allow `{provinceId: null, cityId: null}`.)

---

## 14. Appendix A — Pinned fallback data URLs

- fa: `https://raw.githubusercontent.com/hamidrezaramzani/iran-locations-api/main/public/iran_cities_with_coordinates.json`
- en: `https://raw.githubusercontent.com/hamidrezaramzani/iran-locations-api/main/public/iran_cities_in_english.json`

> Pin exact file contents into the repo at implementation time (they may drift upstream). Record the source commit in a comment or README note.

## 15. Appendix B — Verified dataset samples

```jsonc
// fa state (id 1 of 31)
{ "name": "آذربايجان شرقی", "center": "تبریز", "latitude": "38.50",
  "longitude": "46.180", "landlinePrefix": "041",
  "carLicencePlates": ["15", "25", "35"], "id": 1 }

// fa city inside province 1
{ "name": "تبريز", "latitude": "38.50", "longitude": "46.180", "id": 1 }

// en equivalents
{ "name": "East Azerbaijan", "center": "Tabriz", "latitude": "38.50",
  "longitude": "46.180", "landlinePrefix": "041",
  "carLicencePlates": ["15", "25", "35"], "id": 1 }
{ "name": "Tabriz", "latitude": "38.50", "longitude": "46.180", "id": 1 }

// Verified data quality notes
// - province ids: 1..31, unique
// - city ids: unique ONLY within a province (26 unique ids across 344 cities)
// - duplicate city names exist across provinces: اردكان، حاجي آباد، قشم، دزفول، ايرانشهر، شادگان
```

---

*End of PRD. Hand to Claude with the instruction: "Implement this PRD in the NestJS backend."*
