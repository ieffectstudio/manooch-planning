# Product Requirements Document (PRD)
## Full Migration from Melipayamak to Armaghan SMS WebService (OTP Scope)

**Document Version:** 1.0  
**Target Execution Agent:** Claude / Lead Backend Engineer  
**Scope:** Complete replacement of Melipayamak with Armaghan SMS WebService for One-Time Password (OTP) dispatch and notification delivery.  
**Assigned Sender Number (Originator):** `50002062088`  
**Reference API Version:** Armaghan REST API v2.4.1 (v2 Endpoints)

---

## 1. Executive Summary & Objectives

### 1.1 Objective
The primary objective of this project is to completely decommission and remove the legacy **Melipayamak SMS integration** and replace it with **Armaghan SMS WebService (REST API v2)**. The scope focuses on high-speed, reliable **One-Time Password (OTP)** delivery, user authentication, and transaction verification messages using Armaghan's pattern/template-based messaging service.

### 1.2 Key Deliverables
1. **Melipayamak Deprecation:** Total removal of all Melipayamak SDKs, HTTP requests, configuration variables, and dead code.
2. **Armaghan Driver Integration:** Clean implementation of Armaghan REST API v2 wrapper adhering to a provider interface.
3. **Pattern-Based OTP Dispatch:** Utilization of Armaghan's `sendParameterizedMessage` service for fast OTP delivery bypassing regular promotional queues.
4. **Sender Configuration:** Hardcoded default / configured sender number set to **`50002062088`**.
5. **OTP Form & API Refactoring:** Fixing front-end/back-end OTP submission workflows, rate-limiting, error handling, and delivery confirmation logging.

---

## 2. System Context & Configuration

### 2.1 Configuration Variables Schema
Remove all `MELIPAYAMAK_*` environment variables and replace them with the following schema:

| Variable Name | Required | Default / Example Value | Description |
| :--- | :--- | :--- | :--- |
| `ARMAGHAN_BASE_URL` | Yes | `https://panel.armaghan.net` (or assigned host) | Base URL for Armaghan REST API |
| `ARMAGHAN_USERNAME` | Yes | `<your_username>` | Account username for API authentication |
| `ARMAGHAN_PASSWORD` | Yes | `<your_password>` | Account password for API authentication |
| `ARMAGHAN_ORIGINATOR` | Yes | `50002062088` | Active SMS sender line number |
| `ARMAGHAN_OTP_TEMPLATE_ID` | Yes | `<template_code_from_panel>` | Pattern code defined in Armaghan panel |
| `ARMAGHAN_TIMEOUT_MS` | No | `5000` | HTTP request timeout in milliseconds |

---

## 3. Armaghan API Specifications & Technical Contracts

All requests to Armaghan REST API v2 must send/receive JSON. Credentials (`username` and `password`) are passed inside the JSON payload for `POST` requests or query parameters for `GET` requests.

### 3.1 Base Output Structure
Every Armaghan API response contains an `errorModel` object:
```json
{
  "errorModel": {
    "errorCode": 0,
    "message": null,
    "timestamp": 1678699445454
  }
}
```

### 3.2 System Error Code Reference Table

| Code | Meaning | System Action / Handling Strategy |
| :---: | :--- | :--- |
| `0` | Success | Proceed with OTP workflow, record `referenceId`. |
| `-101` | Authentication Error | Log critical error, alert admin; credentials invalid. |
| `-103` | Invalid Originator (`50002062088`) | Verify line activation on panel; alert admin. |
| `-104` | Low Credit | Trigger low-balance alert to admin; return retry error to user. |
| `-105` | Malformed Request | Check payload structure (JSON body or Query parameters). |
| `-107` | Invalid Destination Number | Return "Invalid phone number format" error to client form. |
| `-110` | IP Not Registered | Whitelist server outbound IP in Armaghan management panel. |
| `-119` | Web Service Inactive | Activate web service feature in user account panel. |
| `-160` | Pattern/Template Code Error | Verify `ARMAGHAN_OTP_TEMPLATE_ID` matches panel pattern. |
| `-161` | Pattern Parameters Mismatch | Verify parameter order and array length match pattern placeholders. |
| `-201` | Internal Provider Error | Trigger fallback/retry mechanism or return server error. |

---

### 3.3 Core Endpoint Requirements

#### A. Primary Endpoint: Parameterized OTP Send (`sendParameterizedMessage`)
*Used for high-priority pattern-based OTP sending (bypasses blacklist / promotional filters).*

* **HTTP Method:** `POST`
* **v2 API Path:** `/webservice/rest/v2/sendParameterizedMessage` (or `/webservice/rest/sendParameterizedMessage`)
* **Request Schema (POST JSON):**
  ```json
  {
    "username": "{{ARMAGHAN_USERNAME}}",
    "password": "{{ARMAGHAN_PASSWORD}}",
    "template": "{{ARMAGHAN_OTP_TEMPLATE_ID}}",
    "parameters": ["<OTP_CODE>"],
    "destinations": ["09121234567"]
  }
  ```
* **Alternative GET Method Format (Query Params):**
  * Path: `/webservice/rest/v2/sendParameterizedMessage`
  * Query parameters: `username`, `password`, `template`, `destinations` (comma-separated), `parameters` (caret `^` separated).
* **Expected Successful Response:**
  ```json
  {
    "errorModel": {
      "errorCode": 0,
      "message": null,
      "timestamp": 1700000000000
    },
    "references": ["987654321123456789"]
  }
  ```

#### B. Secondary Endpoint: Direct Message Send (`sendMessageOneToMany`)
*Used for general non-pattern system alerts or fallback messages.*

* **HTTP Method:** `POST`
* **v2 API Path:** `/webservice/rest/v2/sendMessageOneToMany`
* **Request Schema:**
  ```json
  {
    "username": "{{ARMAGHAN_USERNAME}}",
    "password": "{{ARMAGHAN_PASSWORD}}",
    "originator": "50002062088",
    "content": "Your verification code is: 123456",
    "destinations": ["09121234567"]
  }
  ```

#### C. Delivery Status Tracking (`getMessageState`)
*Used by background workers or status loggers to verify OTP delivery.*

* **HTTP Method:** `POST`
* **v2 API Path:** `/webservice/rest/v2/getMessageState`
* **Request Schema:**
  ```json
  {
    "username": "{{ARMAGHAN_USERNAME}}",
    "password": "{{ARMAGHAN_PASSWORD}}",
    "ids": ["987654321123456789"]
  }
  ```
* **Response Status Code Mapping:**
  * `0`: Scheduled
  * `1`: Sent to Telecom Operator
  * `2`: Received / Delivered to Device
  * `3`: Not Received / Failed Delivery
  * `4`: Unknown State
  * `5`: Ready to Send
  * `6`: Canceled

#### D. Account Credit Monitor (`getUserInfo`)
*Used for health-check endpoint or automated administrative balance alerts.*

* **HTTP Method:** `POST` or `GET`
* **v2 API Path:** `/webservice/rest/v2/getUserInfo`
* **Response Schema:**
  ```json
  {
    "errorModel": { "errorCode": 0, "message": null, "timestamp": 1700000000000 },
    "userInfo": { "credit": 500000 }
  }
  ```

---

## 4. Instructions for Claude (Engineering Execution Plan)

When executing this migration, Claude / the developer agent must follow this exact step-by-step sequence:

```
+-----------------------------------------------------------------------+
| PHASE 1: Audit & Melipayamak Clean-up                                 |
| - Scan codebase for Melipayamak imports, packages, SDKs, config keys  |
| - Remove legacy dependencies from package files (npm/pip/composer)    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| PHASE 2: Configuration & Environment Setup                            |
| - Define ARMAGHAN_* environment variables                             |
| - Set default Originator number to 50002062088                         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| PHASE 3: Core Armaghan Service Implementation                          |
| - Create ArmaghanSmsService adhering to SmsProviderInterface          |
| - Implement phone number standardizer (Format: 09XXXXXXXXX)            |
| - Implement sendOtp() via sendParameterizedMessage                    |
| - Implement fallback send() via sendMessageOneToMany                  |
| - Implement error mapping based on Armaghan error table               |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| PHASE 4: OTP Form & API Route Refactoring                             |
| - Update OTP send controller / route handler                          |
| - Verify rate limits (e.g., 2-min cooldown, phone validation)         |
| - Update response handlers & user feedback messages                   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| PHASE 5: Testing & Verification                                       |
| - Unit tests for request builder & phone parser                       |
| - Integration mock tests for Armaghan REST endpoints                  |
| - Verification of reference ID persistence and logs                   |
+-----------------------------------------------------------------------+
```

---

### Step 1: Audit & Melipayamak Clean-up
1. Search all source code files for references to:
   * `melipayamak` / `MeliPayamak`
   * Melipayamak API URLs (e.g., `rest.payamak-panel.com`, `api.payamak-panel.com`, SOAP endpoints)
   * Environment keys: `MELIPAYAMAK_USERNAME`, `MELIPAYAMAK_PASSWORD`, `MELIPAYAMAK_NUMBER`, etc.
2. Uninstall/Remove Melipayamak SDK or package dependencies from project manifests (`package.json`, `requirements.txt`, `composer.json`, `go.mod`, etc.).
3. Delete unused Melipayamak helper or driver files.

### Step 2: Environment Variable Refactoring
Update configuration schemas (`.env.example`, environment validators, config files):
* Replace all Melipayamak keys with `ARMAGHAN_*` keys.
* Ensure `ARMAGHAN_ORIGINATOR` defaults to `50002062088`.

### Step 3: Implement Armaghan SMS Service Driver
Create a robust service class (e.g., `ArmaghanSmsService` or `ArmaghanProvider`):
1. **Phone Number Sanitization:**
   * Create a normalizer that converts Iranian phone numbers from formats like `+989123456789`, `00989123456789`, `9123456789` into standard 11-digit string starting with `09` (e.g., `09123456789`).
2. **OTP Generation & Sending Method (`sendOtp`):**
   * Call `POST /webservice/rest/v2/sendParameterizedMessage`.
   * Pass `username`, `password`, `template` (`ARMAGHAN_OTP_TEMPLATE_ID`), `parameters` (`[otp_code]`), and `destinations` (`[normalized_phone]`).
   * Extract `references` array from response and return the reference string for logging.
3. **Error Mapping Logic:**
   * Read `errorModel.errorCode`. If `errorCode !== 0`, raise a domain-specific exception (e.g. `SmsSendFailedException`) containing the specific reason according to Section 3.2.

### Step 4: Refactor OTP Dispatcher & Form Logic
1. Update the OTP controller/service layer to call `ArmaghanSmsService.sendOtp(phone, code)`.
2. Ensure the front-end OTP request form receives appropriate structured responses:
   * **Success:** `{ "success": true, "message": "Verification code sent", "cooldownSeconds": 120 }`
   * **Invalid Phone:** `{ "success": false, "message": "Invalid phone number format" }`
   * **Provider Error:** `{ "success": false, "message": "Unable to send SMS. Please try again later." }`
3. Enforce client-side and server-side rate limits (prevent OTP spamming, 1 request per 120 seconds per IP/Phone).

### Step 5: Logging, Telemetry & Status Verification
1. Log every sent OTP event in application logs or database table:
   * Recipient Phone (masked or hashed if needed for privacy)
   * Provider: `armaghan`
   * Sender Line: `50002062088`
   * Reference ID (`references[0]`)
   * Status: `sent` / `failed`
   * Error Code (if failed)
2. Optional: Implement an asynchronous job or health check calling `getMessageState` to track delivered status.

---

## 5. Non-Functional Requirements & Security

1. **Security & Data Confidentiality:**
   * Passwords and credentials must NEVER be logged or exposed in client-side bundles.
   * OTP codes must be securely generated (cryptographically secure random 4-6 digit string).
2. **Performance & Timeout:**
   * Set HTTP connection timeout to **5 seconds** for API requests to ensure front-end form submission doesn't hang if provider is slow.
3. **Resilience & Fallback:**
   * If `sendParameterizedMessage` fails due to provider template maintenance, log error code `-160`/`-161` specifically so developers can inspect template configurations.

---

## 6. Acceptance Criteria & Definition of Done (DoD)

- [ ] **No Melipayamak References:** Codebase scan yields zero occurrences of Melipayamak SDKs, imports, or API calls.
- [ ] **Armaghan Driver Working:** Armaghan REST API v2 wrapper successfully communicates with Armaghan endpoints.
- [ ] **Originator Verified:** All outgoing messages explicitly use sender number `50002062088`.
- [ ] **OTP Delivered via Pattern:** OTP messages are sent using `sendParameterizedMessage` with `ARMAGHAN_OTP_TEMPLATE_ID`.
- [ ] **Form Submission Fixed:** Front-end OTP form triggers correct backend route, handles success/error states gracefully, and shows resend timer.
- [ ] **Error Handling Tested:** Error codes (`-101`, `-104`, `-107`, `-160`) fail gracefully with proper error messages logged.
- [ ] **Environment Configured:** `.env.example` updated with new `ARMAGHAN_*` parameters.
