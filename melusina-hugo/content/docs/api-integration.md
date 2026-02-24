---
title: "API Integration Guide"
type: "doc"
slug: "api-integration"
category: "general"
difficulty: "intermediate"
readTime: "5 min read"
description: "API Integration Guide"
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
date: "2025-01-01"
sitemap:
  priority: 0.5
  changefreq: "monthly"
---

Integrate Melusina into your application using our REST or GraphQL APIs. This guide covers authentication, common workflows, webhooks, and best practices.

## Authentication

Melusina uses **API keys** and **JWT tokens** for authentication.

### Generate API Key

1. Log into Melusina admin panel
2. Go to **Settings** → **API Keys**
3. Click **Generate New Key**
4. Name: "Production API Key"
5. Permissions: Select required scopes
6. Click **Create**

**Store securely!** The key is displayed only once.

### Authentication Headers

Include API key in all requests:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://kyc.yourdomain.com/api/v1/cases
```

### JWT Token (Optional)

For user-specific operations:

```bash
# Get JWT token
curl -X POST https://kyc.yourdomain.com/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "your-password"
  }'

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 3600
}
```

## Core API Endpoints

### Create KYC Case

**POST** `/api/v1/cases`

```json
{
  "client_id": "client_abc123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "verification_level": "standard",
  "metadata": {
    "user_id": "usr_456",
    "source": "web_signup"
  }
}
```

**Response:**
```json
{
  "id": "case_xyz789",
  "status": "invited",
  "invitation_url": "https://kyc.yourdomain.com/verify/abc123...",
  "expires_at": "2025-11-20T12:00:00Z"
}
```

### Get Case Status

**GET** `/api/v1/cases/{case_id}`

```json
{
  "id": "case_xyz789",
  "status": "approved",
  "risk_score": 25,
  "risk_level": "low",
  "verified_at": "2025-11-13T14:30:00Z",
  "documents": [
    {
      "type": "passport",
      "verified": true,
      "extracted_data": {
        "full_name": "John Doe",
        "date_of_birth": "1990-05-15",
        "nationality": "US",
        "document_number": "123456789"
      }
    }
  ],
  "screening": {
    "sanctions": "clear",
    "pep": false,
    "adverse_media": false
  }
}
```

### List Cases

**GET** `/api/v1/cases?status=pending&limit=50`

```json
{
  "count": 127,
  "next": "/api/v1/cases?status=pending&limit=50&offset=50",
  "results": [...]
}
```

### Update Case

**PATCH** `/api/v1/cases/{case_id}`

```json
{
  "status": "approved",
  "reviewer_notes": "All documents verified. Low risk profile.",
  "approved_by": "admin@yourdomain.com"
}
```

## Webhooks

Melusina sends real-time webhooks for case status changes.

### Configure Webhook

1. Go to **Settings** → **Webhooks**
2. Add endpoint: `https://yourapp.com/webhooks/kyc`
3. Select events:
   - `case.created`
   - `case.updated`
   - `case.approved`
   - `case.rejected`
4. Save

### Webhook Payload

```json
{
  "event": "case.approved",
  "timestamp": "2025-11-13T14:30:00Z",
  "data": {
    "case_id": "case_xyz789",
    "status": "approved",
    "email": "user@example.com",
    "risk_score": 25,
    "metadata": {
      "user_id": "usr_456"
    }
  },
  "signature": "sha256=abc123..."
}
```

### Verify Webhook Signature

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    received = signature.replace('sha256=', '')
    return hmac.compare_digest(expected, received)

# Usage
if verify_webhook(request.body, request.headers['X-Signature'], WEBHOOK_SECRET):
    # Process webhook
    pass
else:
    # Invalid signature
    return 401
```

## GraphQL API

For complex queries, use GraphQL:

**Endpoint:** `https://kyc.yourdomain.com/graphql`

### Query Example

```graphql
query GetCaseWithDocuments($caseId: ID!) {
  case(id: $caseId) {
    id
    status
    riskScore
    createdAt
    user {
      email
      firstName
      lastName
    }
    documents {
      type
      verified
      extractedData
      uploadedAt
    }
    screening {
      sanctions
      pep
      adverseMedia
      screenedAt
    }
  }
}
```

### Mutation Example

```graphql
mutation ApproveCase($caseId: ID!, $notes: String) {
  approveCase(input: {
    caseId: $caseId
    reviewerNotes: $notes
  }) {
    case {
      id
      status
      approvedAt
    }
    errors
  }
}
```

## SDK Examples

### Python

```python
from melusina import Melusina

# Initialize client
kyc = Melusina(api_key='your_api_key')

# Create case
case = kyc.cases.create(
    client_id='client_abc123',
    email='user@example.com',
    first_name='John',
    last_name='Doe'
)

print(f"Case created: {case.id}")
print(f"Invitation URL: {case.invitation_url}")

# Check status
case = kyc.cases.get('case_xyz789')
if case.status == 'approved':
    print(f"Approved! Risk score: {case.risk_score}")
```

### Node.js

```javascript
const Melusina = require('@melusina/sdk');

const kyc = new Melusina({ apiKey: process.env.MELUSINA_API_KEY });

// Create case
const case = await kyc.cases.create({
  clientId: 'client_abc123',
  email: 'user@example.com',
  firstName: 'John',
  lastName: 'Doe'
});

console.log(`Case created: ${case.id}`);

// Listen for webhooks
app.post('/webhooks/kyc', async (req, res) => {
  const event = kyc.webhooks.verify(req.body, req.headers['x-signature']);
  
  if (event.type === 'case.approved') {
    await updateUserStatus(event.data.metadata.user_id, 'verified');
  }
  
  res.sendStatus(200);
});
```

## Rate Limits

- **Standard tier:** 100 requests/minute
- **Professional tier:** 500 requests/minute
- **Enterprise tier:** Custom limits

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1699887600
```

## Error Handling

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error

### Error Response

```json
{
  "error": "validation_error",
  "message": "Invalid email format",
  "details": {
    "field": "email",
    "value": "invalid-email"
  }
}
```

## Best Practices

### 1. **Use Idempotency Keys**

Prevent duplicate cases:

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/cases \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Idempotency-Key: unique_key_123" \
  -d '...'
```

### 2. **Implement Exponential Backoff**

For failed requests:

```python
import time

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

### 3. **Cache Results**

Cache case status for 5 minutes to reduce API calls.

### 4. **Use Webhooks**

Don't poll for status changes. Use webhooks for real-time updates.

### 5. **Secure API Keys**

- Never commit to version control
- Use environment variables
- Rotate keys every 90 days
- Use different keys for dev/staging/production

## Support

- **API Reference:** https://api-docs.melusina-os.org
- **Status Page:** https://status.melusina-os.org
- **Support:** api-support@melusina-os.org

---

**Ready to integrate?** Check out our [code examples](https://github.com/melusina/examples) on GitHub.
