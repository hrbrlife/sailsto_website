---
title: "Screening Providers Configuration"
type: "doc"
slug: "screening-providers"
category: "general"
difficulty: "intermediate"
readTime: "5 min read"
description: "Screening Providers Configuration"
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
date: "2025-01-01"
sitemap:
  priority: 0.5
  changefreq: "monthly"
---

Configure third-party screening providers for sanctions lists (OFAC, EU, UN), PEP (Politically Exposed Persons), and adverse media checks. Melusina supports multiple providers with fallback and redundancy.

## Supported Providers

| Provider | Sanctions | PEP | Adverse Media | Pricing |
|----------|-----------|-----|---------------|---------|
| **Dow Jones Risk & Compliance** | ✅ | ✅ | ✅ | $$$$ |
| **Refinitiv World-Check** | ✅ | ✅ | ✅ | $$$$ |
| **ComplyAdvantage** | ✅ | ✅ | ✅ | $$$ |
| **Sumsub** | ✅ | ✅ | ❌ | $$ |
| **Chainalysis** | ✅ (Crypto) | ❌ | ❌ | $$$ |
| **Elliptic** | ✅ (Crypto) | ❌ | ❌ | $$$ |

## Dow Jones Risk & Compliance

### 1. Get API Credentials

1. Sign up at https://risk.dowjones.com
2. Navigate to **API Access**
3. Generate credentials:
   - **Client ID**
   - **Client Secret**
   - **Username**
   - **Password**

### 2. Configure in Melusina

Add to `.env`:

```env
# Dow Jones
SCREENING_DOWJONES_ENABLED=true
SCREENING_DOWJONES_CLIENT_ID=your_client_id
SCREENING_DOWJONES_CLIENT_SECRET=your_client_secret
SCREENING_DOWJONES_USERNAME=your_username
SCREENING_DOWJONES_PASSWORD=your_password
SCREENING_DOWJONES_ENVIRONMENT=production
```

### 3. Test Connection

```bash
docker-compose exec api python manage.py test_screening --provider=dowjones
```

### 4. Configure Match Threshold

In admin panel → **Settings** → **Screening**:

- **Minimum Match Score:** 80% (recommended)
- **Auto-flag above:** 95%
- **Auto-clear below:** 60%

### 5. Usage

Automatic screening occurs when:
- New case created
- Documents verified
- Scheduled daily re-screen (configurable)

Manual screening:
```bash
curl -X POST https://kyc.yourdomain.com/api/v1/cases/{case_id}/screen \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## ComplyAdvantage

### 1. Setup

Sign up at https://complyadvantage.com

Get API key from dashboard.

### 2. Configure

```env
SCREENING_COMPLYADVANTAGE_ENABLED=true
SCREENING_COMPLYADVANTAGE_API_KEY=your_api_key
SCREENING_COMPLYADVANTAGE_FUZZINESS=0.8
```

### 3. Features

- Real-time screening
- Continuous monitoring
- Historical search
- Custom watchlists

## Chainalysis (Crypto)

### 1. For Cryptocurrency Exchanges

Required for wallet verification and transaction monitoring.

### 2. Configure

```env
SCREENING_CHAINALYSIS_ENABLED=true
SCREENING_CHAINALYSIS_API_KEY=your_api_key
SCREENING_CHAINALYSIS_NETWORKS=bitcoin,ethereum,polygon
```

### 3. Wallet Screening

```python
# Automatic when user provides wallet address
case = kyc.cases.create(
    email='user@example.com',
    crypto_wallets=[
        {
            'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
            'network': 'ethereum'
        }
    ]
)
```

Returns:
- Sanctions exposure
- High-risk counterparties
- Mixing service usage
- Darknet marketplace activity
- Ransomware connections

## Multi-Provider Setup (Recommended)

### Fallback Configuration

```env
# Primary provider
SCREENING_PRIMARY_PROVIDER=dowjones

# Fallback providers (in order)
SCREENING_FALLBACK_PROVIDERS=complyadvantage,refinitiv

# Retry logic
SCREENING_MAX_RETRIES=3
SCREENING_RETRY_DELAY=5
```

### Consensus Screening

Use multiple providers and require 2+ matches:

```env
SCREENING_CONSENSUS_MODE=true
SCREENING_CONSENSUS_PROVIDERS=dowjones,complyadvantage,refinitiv
SCREENING_CONSENSUS_THRESHOLD=2
```

## Custom Watchlists

### 1. Upload Custom List

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/watchlists \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@custom-watchlist.csv" \
  -F "name=Internal Blocklist"
```

CSV format:
```csv
name,date_of_birth,nationality,reason
"John Doe","1980-01-01","US","Internal fraud case #123"
```

### 2. Configure Screening

```env
SCREENING_CUSTOM_WATCHLISTS=true
SCREENING_CUSTOM_PRIORITY=high
```

## Scheduled Re-Screening

Monitor existing cases for new sanctions/PEP status.

### Configure Frequency

```env
# Daily at 2 AM UTC
SCREENING_RESCHEDULE_CRON=0 2 * * *

# Only approved cases
SCREENING_RESCHEDULE_STATUSES=approved

# Alert on new matches
SCREENING_RESCHEDULE_ALERT=true
```

### Manual Trigger

```bash
docker-compose exec api python manage.py rescan_cases --days=30
```

## Webhooks

Receive real-time alerts:

```json
{
  "event": "screening.match_found",
  "timestamp": "2025-11-13T14:30:00Z",
  "data": {
    "case_id": "case_xyz789",
    "match": {
      "provider": "dowjones",
      "type": "sanctions",
      "list": "OFAC SDN",
      "score": 98,
      "person": {
        "name": "John Doe",
        "dob": "1980-01-01",
        "nationality": "US"
      }
    }
  }
}
```

## False Positive Handling

### Whitelist

Mark false positives:

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/cases/{case_id}/whitelist \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "match_id": "match_123",
    "reason": "Different person, common name",
    "approved_by": "compliance@yourdomain.com"
  }'
```

### Auto-Rules

Configure in admin panel:
- **Name exact match required**
- **DOB within ±2 years**
- **Nationality must match**

## Compliance Reports

### Generate Report

```bash
curl https://kyc.yourdomain.com/api/v1/reports/screening?start_date=2025-11-01&end_date=2025-11-30 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o screening-report-nov-2025.pdf
```

Includes:
- Total screenings performed
- Matches found (by type)
- False positive rate
- Average response time
- Provider uptime

## Costs Optimization

### 1. **Cache Results**

```env
SCREENING_CACHE_DURATION=7200  # 2 hours
```

### 2. **Batch Processing**

Process multiple cases together:

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/screening/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "case_ids": ["case_1", "case_2", "case_3"]
  }'
```

### 3. **Tiered Screening**

- **Basic:** Free OFAC SDN list only
- **Standard:** Dow Jones or ComplyAdvantage
- **Enhanced:** Multi-provider consensus

## Troubleshooting

### Provider Timeout

```env
SCREENING_TIMEOUT=30  # seconds
```

### Rate Limits

```env
SCREENING_RATE_LIMIT=10  # per minute
```

### Debug Logging

```bash
docker-compose logs -f screening-worker
```

## Support

- **Dow Jones Support:** https://risk.dowjones.com/support
- **ComplyAdvantage Support:** https://complyadvantage.com/support
- **Chainalysis Support:** https://chainalysis.com/support
- **Melusina Integration Support:** screening@melusina-os.org

---

**Need help configuring?** Schedule a [technical consultation](https://melusina-os.org/company).
