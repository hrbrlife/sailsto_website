---
title: "Getting Started with Melusina"
type: "doc"
slug: "getting-started"
category: "general"
difficulty: "intermediate"
readTime: "5 min read"
description: "Getting Started with Melusina"
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
date: "2025-01-01"
sitemap:
  priority: 0.5
  changefreq: "monthly"
---

Build your first KYC workflow in under an hour with Melusina's self-hosted platform. This guide walks you through installation, configuration, and launching your first identity verification case.

## Prerequisites

Before you begin, ensure you have:

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Linux** server (Ubuntu 22.04 LTS recommended)
- **Minimum** 4GB RAM, 2 CPU cores, 20GB storage
- **Domain name** with DNS configured
- **SSL certificate** (Let's Encrypt recommended)

## Installation

### 1. Download Melusina

```bash
wget https://releases.melusina-os.org/latest/melusina-bundle.tar.gz
tar -xzf melusina-bundle.tar.gz
cd melusina
```

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
nano .env
```

Essential variables to configure:

```env
# Domain Configuration
MELUSINA_DOMAIN=kyc.yourdomain.com
MELUSINA_PROTOCOL=https

# Database
POSTGRES_PASSWORD=<generate-strong-password>
REDIS_PASSWORD=<generate-strong-password>

# Email (SMTP)
SMTP_HOST=smtp.yourdomain.com
SMTP_PORT=587
SMTP_USER=kyc@yourdomain.com
SMTP_PASSWORD=<your-smtp-password>

# Object Storage (S3-compatible)
S3_ENDPOINT=https://s3.amazonaws.com
S3_BUCKET=melusina-evidence
S3_ACCESS_KEY=<your-access-key>
S3_SECRET_KEY=<your-secret-key>
```

### 3. Initialize Database

```bash
docker-compose run --rm api python manage.py migrate
docker-compose run --rm api python manage.py createsuperuser
```

### 4. Start Services

```bash
docker-compose up -d
```

### 5. Verify Installation

Check service health:

```bash
docker-compose ps
curl https://kyc.yourdomain.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.5.0",
  "components": {
    "database": "ok",
    "redis": "ok",
    "storage": "ok"
  }
}
```

## First KYC Case

### 1. Access Admin Panel

Navigate to `https://kyc.yourdomain.com/admin` and log in with your superuser credentials.

### 2. Create a Client

1. Go to **Clients** → **Add New**
2. Fill in:
   - **Company Name**: "ACME Exchange"
   - **Industry**: Cryptocurrency Exchange
   - **Risk Tier**: Standard
3. Click **Create Client**

A unique Pearl (isolated container) is provisioned for this client within 30 seconds.

### 3. Invite a User

1. Select the client "ACME Exchange"
2. Click **New Case** → **Individual KYC**
3. Enter email: `john.doe@example.com`
4. Select verification level: **Standard**
5. Click **Send Invitation**

The user receives a branded email with a secure OTP link.

### 4. User Completes KYC

User receives email → Clicks link → Enters OTP → Uploads documents:
- Government ID (passport/driver's license)
- Proof of address (utility bill, bank statement)
- Selfie for liveness check

AI automatically:
- Extracts text from documents
- Validates document authenticity
- Performs face matching
- Checks sanctions lists (OFAC, EU, UN)
- Calculates risk score

### 5. Review & Approve

1. Go to **Cases** → **Pending Review**
2. Open the case for John Doe
3. Review extracted data, risk score, and AI recommendations
4. Click **Approve** or **Request More Info**

Case status updates in real-time. Evidence bundle is stored in S3.

## Next Steps

- [Configure screening providers](./screening-providers.md) (Dow Jones, Refinitiv, ComplyAdvantage)
- [Set up wallet verification](./wallet-verification.md) for crypto addresses
- [Customize workflows](./custom-workflows.md) for different risk tiers
- [Enable biometric authentication](./biometrics.md) (fingerprint, face ID)
- [Integrate with your application](./api-integration.md) via REST or GraphQL

## Support

- **Documentation**: https://docs.melusina-os.org
- **Community**: https://community.melusina-os.org
- **Enterprise Support**: support@melusina-os.org
- **Telegram**: https://t.me/Melusina_Support

## Troubleshooting

### Services won't start

Check Docker logs:
```bash
docker-compose logs -f api
```

Common issues:
- Database not ready → Wait 30 seconds and retry
- Port conflicts → Change ports in `docker-compose.yml`
- Permission errors → Run with `sudo` or add user to docker group

### Email not sending

Test SMTP connection:
```bash
docker-compose exec api python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
```

### Storage errors

Verify S3 credentials:
```bash
docker-compose exec api python manage.py test_storage
```

---

**Need help?** Join our [community forum](https://community.melusina-os.org) or contact [enterprise support](mailto:support@melusina-os.org).
