# Armaghan v2 adapter

> **Status:** Final — executable launch scope based on the attached Armaghan Webservice v2.4.1 contract.


## Configuration

```dotenv
ARMAGHAN_BASE_URL=https://panel.hisms.ir
ARMAGHAN_API_PREFIX=/webservice/rest/v2
ARMAGHAN_USERNAME=<secret>
ARMAGHAN_PASSWORD=<secret>
ARMAGHAN_TIMEOUT_MS=5000
```

The base URL must be plain URL text, not Markdown-link syntax. Keep credentials backend-only.

## Same text to many recipients

`POST {base}{prefix}/sendMessageOneToMany`

```json
{
  "username":"<secret>",
  "password":"<secret>",
  "originator":"<seller-originator>",
  "content":"<final-rendered-body>",
  "destinations":["09120000000","09120000001"]
}
```

## Personalized text per recipient

`POST {base}{prefix}/sendMessageManyToMany`

```json
{
  "username":"<secret>",
  "password":"<secret>",
  "originator":"<seller-originator>",
  "contents":["سلام سارا…","سلام علی…"],
  "destinations":["09120000000","09120000001"]
}
```

The arrays must have equal length. Reference IDs returned by v2 are strings and map to destinations in order.

## Delivery state

`POST {base}{prefix}/getMessageState`

```json
{
  "username":"<secret>",
  "password":"<secret>",
  "ids":["987654321123456789"]
}
```

Provider states: `0 scheduled`, `1 sent`, `2 delivered`, `3 not delivered`, `4 unknown`, `5 ready`, `6 canceled`; `-100` means reference not found.

## Provider credit

`POST {base}{prefix}/getUserInfo` with credentials. Treat returned `userInfo.credit` as provider-account credit. It is not a replacement for a per-seller application credit ledger when credentials are shared.

## Incoming messages

`POST {base}{prefix}/getReceivedMessages`. Poll with `afterId`, `page`, and `size`; filter/route by `destination`, which is the originator receiving the reply. In v2, message IDs are strings.

## Error mapping

| Code | Meaning | Classification |
|---:|---|---|
| `0` | success | accepted |
| `-101` | authentication error | operational/block account |
| `-103` | invalid originator | configuration/block line |
| `-104` | low provider credit | operational/pause |
| `-105` | malformed request | permanent request failure |
| `-107` | invalid destination | permanent recipient failure |
| `-110` | invalid/unregistered IP | operational |
| `-119` | service inactive | operational |
| `-201` | internal provider error | transient candidate |

Always inspect `errorModel.errorCode`; HTTP 200 alone is not success.

## Adapter interface

```ts
interface ArmaghanV2 {
  sendOneToMany(input: {originator: string; content: string; destinations: string[]}): Promise<string[]>;
  sendManyToMany(input: {originator: string; contents: string[]; destinations: string[]}): Promise<string[]>;
  getStates(ids: string[]): Promise<Array<{id: string; state: number}>>;
  getCredit(): Promise<bigint>;
  getReceived(input: {afterId?: string; destination?: string; page?: number; size?: number}): Promise<ReceivedPage>;
}
```

## Reliability policy

- Configurable 5-second initial timeout.
- Exponential backoff with jitter for known-safe pre-transmission failures.
- Do not automatically retry ambiguous post-transmission timeouts.
- Do not retry permanent input/configuration errors.
- Configure batch size/rate limits instead of assuming undocumented values.
- Use circuit breaking for account-level authentication, credit, IP, and service errors.

## Observability

Record seller ID, outbox ID, feature, operation, batch count, latency, HTTP status, provider error code, and masked reference count. Never log credentials, full destinations, or full bodies.
