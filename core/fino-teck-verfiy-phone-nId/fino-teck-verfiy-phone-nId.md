# PRD: Shahkar Mobile Verification Before OTP

## Product Requirements Document

**Document Version:** 1.0
**Date:** 2024
**Author:** Product Team
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Purpose
Implement Shahkar (شاهکار) verification as a pre-OTP validation step to ensure the mobile number belongs to the user's National ID before sending any OTP SMS, reducing costs and preventing fraud.

### 1.2 Problem Statement
Currently, OTP SMS is sent without verifying mobile ownership, leading to:
- Wasted SMS costs on fraudulent/mismatched numbers
- Potential fraud attempts using others' mobile numbers
- Poor user experience when verification fails after OTP entry

### 1.3 Proposed Solution
Integrate Finnotech Shahkar API to verify National ID + Mobile Number ownership **before** sending OTP.

---

## 2. Goals & Success Metrics

### 2.1 Business Goals
| Goal | Description |
|------|-------------|
| Reduce SMS Costs | Eliminate OTP SMS to unverified numbers |
| Prevent Fraud | Block registration with mismatched mobile/NID |
| Compliance | Meet Central Bank KYC requirements |
| Improve UX | Fail fast with clear error messages |

### 2.2 Success Metrics (KPIs)
| Metric | Current | Target |
|--------|---------|--------|
| OTP SMS waste rate | ~15% | <2% |
| Fraud registration attempts | Unknown | Track & reduce 80% |
| User drop-off at verification | ~20% | <10% |
| Average verification time | N/A | <3 seconds |

---

## 3. User Stories

### 3.1 Primary User Stories

```
US-01: As a new user, I want to verify my mobile number belongs to my
       National ID so I can proceed with registration securely.

US-02: As a user, I want clear feedback if my mobile doesn't match
       my National ID so I can correct my information.

US-03: As a system admin, I want to track Shahkar verification
       results for compliance reporting.

US-04: As a product owner, I want to reduce unnecessary OTP costs
       by validating before sending SMS.
```

### 3.2 Edge Case Stories

```
US-05: As a user with a corporate SIM, I want to understand why
       verification failed and what alternatives exist.

US-06: As a user, I want the system to handle Shahkar downtime
       gracefully without blocking my registration completely.
```

---

## 4. Functional Requirements

### 4.1 User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      REGISTRATION FLOW                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────┐
│  User    │    │  Enter NID   │    │ Enter Mobile│    │ Submit  │
│  Start   │───▶│  (10 digits) │───▶│ (09XXXXXXXXX)│───▶│  Form   │
└──────────┘    └──────────────┘    └─────────────┘    └────┬────┘
                                                             │
                                                             ▼
                ┌────────────────────────────────────────────────┐
                │           SHAHKAR VERIFICATION                  │
                │  POST /facility/v2/clients/{clientId}/         │
                │       shahkarVerify?trackId={trackId}          │
                └────────────────────┬───────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌─────────┐      ┌──────────┐     ┌──────────┐
              │ MATCHED │      │ MISMATCHED│    │  ERROR   │
              │ isMatch │      │ isMatch   │    │ (Timeout/│
              │ = true  │      │ = false   │    │  Down)   │
              └────┬────┘      └─────┬─────┘    └────┬─────┘
                   │                 │               │
                   ▼                 ▼               ▼
            ┌───────────┐    ┌────────────┐   ┌────────────┐
            │ SEND OTP  │    │ SHOW ERROR │   │  FALLBACK  │
            │ Continue  │    │ Block Flow │   │  STRATEGY  │
            │ Flow      │    │            │   │            │
            └───────────┘    └────────────┘   └────────────┘
```

### 4.2 API Integration Specification

#### Request Details
```yaml
Endpoint: POST /facility/v2/clients/{clientId}/shahkarVerify
Host: https://apibeta.finnotech.ir (Sandbox)
      https://api.finnotech.ir (Production)

Headers:
  Authorization: Bearer {access_token}
  Content-Type: application/json

Query Parameters:
  trackId: string (unique identifier for tracking)

Request Body:
  {
    "mobile": "09123456789",
    "nationalCode": "0012345678"
  }
```

#### Response Handling
```yaml
Success Response (200):
  {
    "result": {
      "isMatch": true,        # Mobile belongs to NID
      "isMatchSpecified": true
    },
    "status": "DONE",
    "trackId": "unique-track-id"
  }

Mismatch Response (200):
  {
    "result": {
      "isMatch": false,       # Mobile does NOT belong to NID
      "isMatchSpecified": true
    },
    "status": "DONE",
    "trackId": "unique-track-id"
  }

Error Responses:
  400: Bad Request (invalid input)
  401: Unauthorized (invalid token)
  403: Forbidden (insufficient scope)
  429: Rate Limited
  500: Server Error
  503: Shahkar Service Unavailable
```

### 4.3 Detailed Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-01 | Validate NID format (10 digits) before API call | P0 | Client-side |
| FR-02 | Validate mobile format (09XXXXXXXXX) before API call | P0 | Client-side |
| FR-03 | Call Shahkar API with validated inputs | P0 | Server-side |
| FR-04 | If `isMatch=true`, proceed to OTP sending | P0 | - |
| FR-05 | If `isMatch=false`, block flow with error message | P0 | - |
| FR-06 | Log all Shahkar requests/responses | P0 | Compliance |
| FR-07 | Implement retry logic (max 2 retries) | P1 | - |
| FR-08 | Implement fallback on Shahkar downtime | P1 | See 4.4 |
| FR-09 | Rate limit Shahkar calls per user (3/hour) | P1 | Prevent abuse |
| FR-10 | Cache successful verifications (24 hours) | P2 | Cost saving |

### 4.4 Fallback Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   FALLBACK DECISION TREE                     │
└─────────────────────────────────────────────────────────────┘

Shahkar API Error
        │
        ├── Is it rate limit (429)?
        │       │
        │       └── YES ──▶ Wait & Retry (exponential backoff)
        │
        ├── Is it server error (5xx)?
        │       │
        │       └── YES ──▶ Retry up to 2 times
        │                          │
        │                          └── Still failing?
        │                                    │
        │                   ┌────────────────┴────────────────┐
        │                   ▼                                 ▼
        │            [OPTION A]                        [OPTION B]
        │         Allow with flag                    Block & notify
        │         "UNVERIFIED"                       user to retry
        │         (risky transactions                    later
        │          blocked later)
        │
        └── Is it client error (4xx)?
                │
                └── YES ──▶ Show user-friendly error
                            Do NOT retry
```

**Recommended Fallback:** Option B (Block & Retry Later) for financial applications.

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Requirement | Target |
|-------------|--------|
| API Response Time | < 3 seconds (95th percentile) |
| Timeout Setting | 10 seconds |
| Concurrent Requests | Support 100 RPS |

### 5.2 Security

| Requirement | Implementation |
|-------------|----------------|
| Token Storage | Encrypted, server-side only |
| NID/Mobile Logging | Masked in logs (09***456789) |
| HTTPS | Mandatory for all API calls |
| Token Refresh | Auto-refresh before expiry |

### 5.3 Availability

| Requirement | Target |
|-------------|--------|
| Uptime | 99.5% (dependent on Finnotech SLA) |
| Graceful Degradation | Must handle Shahkar downtime |

---

## 6. Technical Architecture

### 6.1 System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Web App     │  │ Mobile App  │  │ Admin Dashboard         │  │
│  │ (React)     │  │ (Flutter)   │  │ (Monitoring)            │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
└─────────┼────────────────┼──────────────────────┼───────────────┘
          │                │                      │
          └────────────────┼──────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY                                │
│              (Rate Limiting, Authentication)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ Auth Service     │    │ KYC Service      │◀── NEW SERVICE    │
│  │                  │    │                  │                   │
│  │ - Login          │    │ - shahkarVerify()│                   │
│  │ - Register       │───▶│ - cacheResult()  │                   │
│  │ - SendOTP        │    │ - logAudit()     │                   │
│  └──────────────────┘    └────────┬─────────┘                   │
│                                   │                              │
└───────────────────────────────────┼─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Finnotech API Client                         │   │
│  │                                                           │   │
│  │  - getAccessToken()                                       │   │
│  │  - refreshToken()                                         │   │
│  │  - shahkarVerify(mobile, nationalCode)                    │   │
│  │  - handleErrors()                                         │   │
│  │  - retryWithBackoff()                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ Finnotech API    │    │ SMS Provider     │                   │
│  │ (Shahkar)        │    │ (OTP Sending)    │                   │
│  └──────────────────┘    └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ PostgreSQL       │    │ Redis            │                   │
│  │ - Users          │    │ - Token Cache    │                   │
│  │ - Audit Logs     │    │ - Shahkar Cache  │                   │
│  │ - Verifications  │    │ - Rate Limits    │                   │
│  └──────────────────┘    └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Database Schema

```sql
-- Shahkar Verification Logs (Audit & Compliance)
CREATE TABLE shahkar_verifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id        VARCHAR(100) UNIQUE NOT NULL,

    -- Input (masked for security)
    mobile_hash     VARCHAR(64) NOT NULL,      -- SHA256 hash
    national_code_hash VARCHAR(64) NOT NULL,   -- SHA256 hash
    mobile_masked   VARCHAR(15),               -- 09***456789

    -- Result
    is_match        BOOLEAN,
    is_match_specified BOOLEAN,
    status          VARCHAR(20),               -- DONE, ERROR, TIMEOUT

    -- Metadata
    response_time_ms INTEGER,
    error_code      VARCHAR(50),
    error_message   TEXT,

    -- Timestamps
    created_at      TIMESTAMP DEFAULT NOW(),

    -- Indexes
    INDEX idx_mobile_hash (mobile_hash),
    INDEX idx_created_at (created_at)
);

-- Cache table for successful verifications
CREATE TABLE shahkar_cache (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mobile_hash     VARCHAR(64) NOT NULL,
    national_code_hash VARCHAR(64) NOT NULL,
    is_match        BOOLEAN NOT NULL,
    verified_at     TIMESTAMP DEFAULT NOW(),
    expires_at      TIMESTAMP NOT NULL,

    UNIQUE(mobile_hash, national_code_hash)
);
```

### 6.3 Sample Code Implementation

#### Finnotech Client (Python)
```python
import httpx
import hashlib
from datetime import datetime, timedelta
from typing import Optional
import redis
import logging

logger = logging.getLogger(__name__)


class FinnotechClient:
    """Finnotech API Client for Shahkar Verification"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://api.finnotech.ir",
        redis_client: redis.Redis = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.redis = redis_client
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    async def get_access_token(self) -> str:
        """Get or refresh access token"""

        # Check cache first
        if self.redis:
            cached_token = self.redis.get("finnotech:access_token")
            if cached_token:
                return cached_token.decode()

        # Check memory cache
        if self._access_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                return self._access_token

        # Request new token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dev/v2/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }
            )
            response.raise_for_status()
            data = response.json()

            self._access_token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            # Cache in Redis
            if self.redis:
                self.redis.setex(
                    "finnotech:access_token",
                    expires_in - 300,  # 5 min buffer
                    self._access_token
                )

            return self._access_token

    async def shahkar_verify(
        self,
        mobile: str,
        national_code: str,
        track_id: str
    ) -> dict:
        """
        Verify mobile number ownership via Shahkar.

        Args:
            mobile: Mobile number (09XXXXXXXXX)
            national_code: National ID (10 digits)
            track_id: Unique tracking ID

        Returns:
            dict: {
                "is_match": bool,
                "track_id": str,
                "status": str
            }
        """

        # Input validation
        if not self._validate_mobile(mobile):
            raise ValueError("Invalid mobile format. Expected: 09XXXXXXXXX")

        if not self._validate_national_code(national_code):
            raise ValueError("Invalid national code. Expected: 10 digits")

        # Check cache first
        cache_key = self._get_cache_key(mobile, national_code)
        if self.redis:
            cached = self.redis.get(cache_key)
            if cached:
                logger.info(f"Shahkar cache hit for track_id={track_id}")
                return {
                    "is_match": cached.decode() == "true",
                    "track_id": track_id,
                    "status": "CACHED"
                }

        # Make API call
        token = await self._get_access_token()

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/facility/v2/clients/{self.client_id}/shahkarVerify",
                    params={"trackId": track_id},
                    json={
                        "mobile": mobile,
                        "nationalCode": national_code
                    },
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )

                response.raise_for_status()
                data = response.json()

                result = {
                    "is_match": data["result"]["isMatch"],
                    "track_id": data["trackId"],
                    "status": data["status"]
                }

                # Cache successful result (24 hours)
                if self.redis and result["status"] == "DONE":
                    self.redis.setex(
                        cache_key,
                        86400,  # 24 hours
                        "true" if result["is_match"] else "false"
                    )

                return result

            except httpx.TimeoutException:
                logger.error(f"Shahkar API timeout for track_id={track_id}")
                raise ShahkarTimeoutError("Shahkar service timeout")

            except httpx.HTTPStatusError as e:
                logger.error(f"Shahkar API error: {e.response.status_code}")
                raise ShahkarAPIError(
                    status_code=e.response.status_code,
                    detail=e.response.text
                )

    def validate_mobile(self, mobile: str) -> bool:
        """Validate Iranian mobile number format"""
        import re
        return bool(re.match(r'^09\d{9}$', mobile))

    def validate_national_code(self, code: str) -> bool:
        """Validate Iranian national code (checksum validation)"""
        if not code.isdigit() or len(code) != 10:
            return False

        # Checksum validation
        check = int(code[-1])
        total = sum(int(code[i]) * (10 - i) for i in range(9))

        remainder = total % 11

        return (remainder < 2 and check == remainder) or \
               (remainder >= 2 and check == 11 - remainder)

    def get_cache_key(self, mobile: str, national_code: str) -> str:
        """Generate cache key from hashed inputs"""
        combined = f"{mobile}:{national_code}"
        return f"shahkar:{hashlib.sha256(combined.encode()).hexdigest()}"


class ShahkarError(Exception):
    """Base Shahkar exception"""
    pass


class ShahkarTimeoutError(ShahkarError):
    """Shahkar timeout exception"""
    pass


class ShahkarAPIError(ShahkarError):
    """Shahkar API error exception"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Shahkar API Error {status_code}: {detail}")
```

#### KYC Service (FastAPI)
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, validator
import uuid

router = APIRouter(prefix="/api/v1/kyc", tags=["KYC"])


class ShahkarVerifyRequest(BaseModel):
    mobile: str
    national_code: str

    @validator('mobile')
    def validate_mobile(cls, v):
        import re
        if not re.match(r'^09\d{9}$', v):
            raise ValueError('Invalid mobile format')
        return v

    @validator('national_code')
    def validate_national_code(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Invalid national code')
        return v


class ShahkarVerifyResponse(BaseModel):
    is_match: bool
    track_id: str
    can_proceed: bool
    message: str


@router.post("/shahkar/verify", response_model=ShahkarVerifyResponse)
async def verify_shahkar(
    request: ShahkarVerifyRequest,
    finnotech: FinnotechClient = Depends(get_finnotech_client),
    db = Depends(get_db)
):
    """
    Verify mobile number ownership before OTP.

    This endpoint must be called BEFORE sending OTP.
    """

    track_id = str(uuid.uuid4())

    try:
        # Call Shahkar API
        result = await finnotech.shahkar_verify(
            mobile=request.mobile,
            national_code=request.national_code,
            track_id=track_id
        )

        # Log to database (for compliance)
        await db.execute(
            """
            INSERT INTO shahkar_verifications
            (track_id, mobile_hash, national_code_hash, mobile_masked,
             is_match, status, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
            """,
            track_id,
            hashlib.sha256(request.mobile.encode()).hexdigest(),
            hashlib.sha256(request.national_code.encode()).hexdigest(),
            f"{request.mobile[:3]}***{request.mobile[-3:]}",
            result["is_match"],
            result["status"]
        )

        if result["is_match"]:
            return ShahkarVerifyResponse(
                is_match=True,
                track_id=track_id,
                can_proceed=True,
                message="Mobile number verified successfully"
            )
        else:
            return ShahkarVerifyResponse(
                is_match=False,
                track_id=track_id,
                can_proceed=False,
                message="Mobile number does not belong to this National ID"
            )

    except ShahkarTimeoutError:
        raise HTTPException(
            status_code=503,
            detail="Verification service temporarily unavailable. Please try again."
        )
    except ShahkarAPIError as e:
        if e.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Too many verification attempts. Please wait."
            )
        raise HTTPException(
            status_code=502,
            detail="Verification service error"
        )
```

#### Frontend Integration (React)
```typescript
// types.ts
interface ShahkarVerifyRequest {
  mobile: string;
  nationalCode: string;
}

interface ShahkarVerifyResponse {
  isMatch: boolean;
  trackId: string;
  canProceed: boolean;
  message: string;
}

// api/kyc.ts
export async function verifyShahkar(
  data: ShahkarVerifyRequest
): Promise<ShahkarVerifyResponse> {
  const response = await fetch('/api/v1/kyc/shahkar/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mobile: data.mobile,
      national_code: data.nationalCode,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Verification failed');
  }

  return response.json();
}

// components/RegistrationForm.tsx
import { useState } from 'react';
import { verifyShahkar } from '../api/kyc';

export function RegistrationForm() {
  const [nationalCode, setNationalCode] = useState('');
  const [mobile, setMobile] = useState('');
  const [step, setStep] = useState<'input' | 'verifying' | 'otp'>('input');
  const [error, setError] = useState<string | null>(null);
  const [trackId, setTrackId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setStep('verifying');

    try {
      // Step 1: Verify Shahkar BEFORE OTP
      const result = await verifyShahkar({
        mobile,
        nationalCode,
      });

      setTrackId(result.trackId);

      if (result.canProceed) {
        // Step 2: Only send OTP if Shahkar verified
        await sendOTP(mobile, result.trackId);
        setStep('otp');
      } else {
        setError(result.message);
        setStep('input');
      }
    } catch (err) {
      setError(err.message || 'Verification failed. Please try again.');
      setStep('input');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
        </div>
      )}

      <div className="form-group">
        <label>National ID (کد ملی)</label>
        <input
          type="text"
          value={nationalCode}
          onChange={(e) => setNationalCode(e.target.value)}
          maxLength={10}
          pattern="\d{10}"
          placeholder="0012345678"
          disabled={step === 'verifying'}
          required
        />
      </div>

      <div className="form-group">
        <label>Mobile Number (شماره موبایل)</label>
        <input
          type="tel"
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
          maxLength={11}
          pattern="09\d{9}"
          placeholder="09123456789"
          disabled={step === 'verifying'}
          required
        />
      </div>

      <button
        type="submit"
        disabled={step === 'verifying'}
      >
        {step === 'verifying' ? 'Verifying...' : 'Continue'}
      </button>

      {step === 'verifying' && (
        <p className="info-text">
          Verifying your mobile number ownership...
        </p>
      )}
    </form>
  );
}
```

---

## 7. Error Handling & Messages

### 7.1 Error Codes & User Messages

| Error Code | Internal Cause | User Message (FA) | User Message (EN) |
|------------|---------------|-------------------|-------------------|
| SHAHKAR_MISMATCH | `isMatch=false` | شماره موبایل به این کد ملی تعلق ندارد | Mobile number does not belong to this National ID |
| SHAHKAR_TIMEOUT | API timeout | سرویس در دسترس نیست، لطفا مجددا تلاش کنید | Service unavailable, please try again |
| SHAHKAR_RATE_LIMIT | HTTP 429 | تعداد درخواست‌ها بیش از حد مجاز است | Too many requests, please wait |
| INVALID_NID | Validation fail | کد ملی نامعتبر است | Invalid National ID |
| INVALID_MOBILE | Validation fail | شماره موبایل نامعتبر است | Invalid mobile number |
| CORPORATE_SIM | Business rule | سیم‌کارت سازمانی قابل استفاده نیست | Corporate SIM cards are not supported |

### 7.2 Retry Strategy

```python
RETRY_CONFIG = {
    "max_retries": 2,
    "backoff_factor": 1.5,
    "retry_on_status": [429, 500, 502, 503, 504],
    "timeout_per_request": 10,
}
```

---

## 8. Testing Requirements

### 8.1 Test Cases

| ID | Test Case | Expected Result |
|----|-----------|-----------------|
| TC-01 | Valid NID + Matching Mobile | `isMatch=true`, proceed to OTP |
| TC-02 | Valid NID + Non-matching Mobile | `isMatch=false`, show error |
| TC-03 | Invalid NID format | Client-side validation error |
| TC-04 | Invalid Mobile format | Client-side validation error |
| TC-05 | Shahkar API timeout | Retry 2x, then show error |
| TC-06 | Rate limit exceeded | Show "please wait" message |
| TC-07 | Cached verification (repeat) | Return cached result, no API call |
| TC-08 | Concurrent requests (same user) | Rate limit, allow only 3/hour |

### 8.2 Sandbox Testing

```yaml
Sandbox URL: https://apibeta.finnotech.ir
Test Credentials:
  - NID: 0079893853 + Mobile: 09120000000 → isMatch: true
  - NID: 0079893853 + Mobile: 09121111111 → isMatch: false

Note: Confirm test data with Finnotech support
```

---

## 9. Monitoring & Alerting

### 9.1 Metrics to Track

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Shahkar API latency (p95) | Prometheus | > 5 seconds |
| Shahkar API error rate | Prometheus | > 5% |
| Mismatch rate | Internal | > 30% (fraud indicator) |
| Cache hit rate | Redis | < 20% (review caching) |
| Daily verification count | Grafana | Dashboard only |

### 9.2 Dashboard Requirements

```
┌─────────────────────────────────────────────────────────────┐
│                  SHAHKAR MONITORING DASHBOARD                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Total Today  │  │ Match Rate   │  │ Avg Latency  │       │
│  │   12,453     │  │    87.3%     │  │   1.2 sec    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  [========== API Response Time (last 24h) ===========]      │
│                                                              │
│  [========== Success vs Error Rate ==================]      │
│                                                              │
│  [========== Cache Hit Rate =========================]      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Compliance & Legal

### 10.1 Data Handling

| Data | Storage | Retention | Access |
|------|---------|-----------|--------|
| National ID | Hashed only | As per regulation | Authorized systems only |
| Mobile Number | Hashed + Masked | As per regulation | Authorized systems only |
| Verification Logs | Full audit trail | 7 years (banking) | Compliance team |
| Track IDs | Plain text | 7 years | All systems |

### 10.2 Required Documentation

- [ ] Data Processing Agreement with Finnotech
- [ ] Privacy Policy update mentioning Shahkar verification
- [ ] User consent for mobile verification
- [ ] Audit logging implementation sign-off

---

## 11. Timeline & Milestones

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Setup | 1 week | Finnotech account, API credentials, sandbox access |
| Phase 2: Development | 2 weeks | Backend service, database, API integration |
| Phase 3: Testing | 1 week | Unit tests, integration tests, sandbox testing |
| Phase 4: Frontend | 1 week | UI implementation, error handling |
| Phase 5: UAT | 1 week | User acceptance testing |
| Phase 6: Production | 3 days | Production deployment, monitoring setup |

**Total Estimated Time:** 6-7 weeks

---

## 12. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Shahkar API downtime | Medium | High | Implement fallback, queue requests |
| High API costs | Medium | Medium | Implement caching, rate limiting |
| False mismatches (corporate SIMs) | Low | Medium | Clear error message, support channel |
| Finnotech contract delays | Medium | High | Start process early, parallel development |

---

## 13. Appendix

### A. Finnotech Scopes Required

```
kyc:shahkar-verify:get
```

### B. Environment Variables

```env
# Finnotech Configuration
FINNOTECH_CLIENT_ID=your_client_id
FINNOTECH_CLIENT_SECRET=your_client_secret
FINNOTECH_BASE_URL=https://api.finnotech.ir
FINNOTECH_SANDBOX_URL=https://apibeta.finnotech.ir

# Feature Flags
SHAHKAR_ENABLED=true
SHAHKAR_CACHE_TTL=86400
SHAHKAR_MAX_RETRIES=2
SHAHKAR_TIMEOUT_SECONDS=10
SHAHKAR_RATE_LIMIT_PER_USER=3
```

### C. API Scope Documentation

Refer to: https://docs.finnotech.ir/v2/#/operations/facilityShahkarVerifyGet

---

**Document Approval:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Manager | | | |
| Tech Lead | | | |
| Security Officer | | | |
| Compliance | | | |
