---
title: "Security Best Practices"
type: "doc"
slug: "security-best-practices"
category: "general"
difficulty: "intermediate"
readTime: "5 min read"
description: "Security Best Practices"
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
date: "2025-01-01"
sitemap:
  priority: 0.5
  changefreq: "monthly"
---

Protect your Melusina deployment with enterprise-grade security measures. This guide covers encryption, access control, network security, and compliance requirements.

## Infrastructure Security

### 1. **Network Isolation**

Deploy in private subnet:

```yaml
# docker-compose.override.yml
networks:
  melusina_private:
    driver: bridge
    internal: true
  melusina_public:
    driver: bridge

services:
  api:
    networks:
      - melusina_private
      - melusina_public
  
  database:
    networks:
      - melusina_private  # No public access
```

### 2. **Firewall Rules**

```bash
# UFW configuration
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp   # SSH (restrict to bastion IP)
ufw allow 443/tcp  # HTTPS only
ufw enable
```

### 3. **VPC Configuration (AWS)**

```terraform
resource "aws_vpc" "melusina" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.melusina.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_security_group" "melusina_api" {
  vpc_id = aws_vpc.melusina.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Data Encryption

### At Rest

#### Database Encryption

PostgreSQL with encryption:

```yaml
# docker-compose.yml
services:
  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_INITDB_ARGS: "--data-checksums"
    volumes:
      - ./encryption:/encryption:ro
    command: >
      postgres
      -c ssl=on
      -c ssl_cert_file=/encryption/server.crt
      -c ssl_key_file=/encryption/server.key
      -c ssl_ciphers='HIGH:MEDIUM:+3DES:!aNULL'
```

#### S3 Bucket Encryption

```bash
# Enable server-side encryption
aws s3api put-bucket-encryption \
  --bucket melusina-evidence \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

#### Application-Level Encryption

```env
# .env
ENCRYPTION_KEY=<generate-32-byte-key>
ENCRYPTION_ALGORITHM=AES-256-GCM
```

Encrypt sensitive fields:

```python
from cryptography.fernet import Fernet

# Document encryption before storage
def encrypt_document(file_content):
    cipher = Fernet(settings.ENCRYPTION_KEY)
    return cipher.encrypt(file_content)
```

### In Transit

#### TLS 1.3 Only

```nginx
# nginx.conf
ssl_protocols TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_stapling on;
ssl_stapling_verify on;
```

#### Certificate Pinning

Mobile app implementation:

```swift
// iOS
let publicKeyHash = "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
let pinningPolicy = PinningPolicy(
    pins: [
        "kyc.yourdomain.com": [publicKeyHash]
    ]
)
```

## Access Control

### Role-Based Access Control (RBAC)

Configure roles:

```yaml
# roles.yml
roles:
  - name: viewer
    permissions:
      - case:read
      - report:read

  - name: operator
    permissions:
      - case:read
      - case:create
      - case:update
      - document:review

  - name: approver
    permissions:
      - case:*
      - case:approve
      - case:reject

  - name: admin
    permissions:
      - *:*
```

Apply roles:

```bash
docker-compose exec api python manage.py assign_role \
  --user=operator@yourdomain.com \
  --role=operator
```

### Multi-Factor Authentication (MFA)

Enable MFA for admin users:

```env
MFA_ENABLED=true
MFA_ISSUER=Melusina
MFA_REQUIRED_FOR_ROLES=admin,approver
```

Setup:

```python
from pyotp import TOTP

# Generate MFA secret
secret = pyotp.random_base32()
totp = TOTP(secret)

# Verify code
if totp.verify(user_code):
    # Grant access
    pass
```

### IP Whitelisting

```env
ALLOWED_IPS=203.0.113.0/24,198.51.100.42
```

Or in Nginx:

```nginx
location /admin {
    allow 203.0.113.0/24;
    allow 198.51.100.42;
    deny all;
}
```

## Audit Logging

### Enable Comprehensive Logging

```env
AUDIT_LOG_ENABLED=true
AUDIT_LOG_LEVEL=INFO
AUDIT_LOG_RETENTION_DAYS=2555  # 7 years
AUDIT_LOG_STORAGE=s3://melusina-audit-logs
```

### Log All Actions

```python
# Automatic audit trail
{
  "timestamp": "2025-11-13T14:30:00Z",
  "action": "case.approved",
  "user": "admin@yourdomain.com",
  "ip": "203.0.113.42",
  "user_agent": "Mozilla/5.0...",
  "case_id": "case_xyz789",
  "changes": {
    "status": ["pending", "approved"],
    "risk_score": [35, 25]
  },
  "metadata": {
    "session_id": "sess_abc123",
    "request_id": "req_xyz789"
  }
}
```

### Tamper-Proof Logs

Use blockchain or append-only storage:

```bash
# Configure immutable S3 bucket
aws s3api put-object-lock-configuration \
  --bucket melusina-audit-logs \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "COMPLIANCE",
        "Years": 7
      }
    }
  }'
```

## Secrets Management

### Use AWS Secrets Manager

```bash
# Store database password
aws secretsmanager create-secret \
  --name melusina/database/password \
  --secret-string "your-secure-password"

# Retrieve in application
aws secretsmanager get-secret-value \
  --secret-id melusina/database/password \
  --query SecretString \
  --output text
```

### Environment Variables

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use docker secrets
docker secret create db_password ./db_password.txt

# Reference in docker-compose.yml
services:
  api:
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
```

## Vulnerability Management

### 1. **Dependency Scanning**

```bash
# Python dependencies
pip install safety
safety check --json

# Docker images
docker scan melusina/api:latest
```

### 2. **Regular Updates**

```bash
# Update all services
docker-compose pull
docker-compose up -d

# Update system packages
apt update && apt upgrade -y
```

### 3. **Penetration Testing**

Schedule annual pen tests. Use tools:

- **OWASP ZAP** - Automated security testing
- **Burp Suite** - Manual testing
- **Nmap** - Network scanning

## Compliance

### GDPR

```env
GDPR_ENABLED=true
GDPR_DATA_RETENTION_DAYS=730  # 2 years
GDPR_RIGHT_TO_ERASURE=true
```

Implement data erasure:

```bash
curl -X DELETE https://kyc.yourdomain.com/api/v1/cases/{case_id}/gdpr-erase \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "user_request": true,
    "reason": "User requested data deletion",
    "confirmed_by": "dpo@yourdomain.com"
  }'
```

### SOC 2 Type II

Required controls:

- [ ] Access controls (RBAC, MFA)
- [ ] Encryption (at rest, in transit)
- [ ] Audit logging (7-year retention)
- [ ] Incident response plan
- [ ] Disaster recovery (RTO < 4 hours, RPO < 1 hour)
- [ ] Vulnerability management
- [ ] Security awareness training

### ISO 27001

Implement ISMS:

```
policies/
├── information-security-policy.md
├── access-control-policy.md
├── encryption-policy.md
├── incident-response-policy.md
└── business-continuity-policy.md
```

## Incident Response

### 1. **Detection**

Monitor for:
- Failed login attempts (>5 in 5 minutes)
- Unusual API usage (10x normal rate)
- Unauthorized access attempts
- Data exfiltration patterns

```env
SECURITY_ALERTS_EMAIL=security@yourdomain.com
SECURITY_ALERTS_SLACK_WEBHOOK=https://hooks.slack.com/...
```

### 2. **Response Playbook**

**Data Breach:**

1. **Isolate** - Disable compromised accounts
2. **Investigate** - Review audit logs
3. **Contain** - Patch vulnerability
4. **Notify** - Users, regulators (within 72 hours for GDPR)
5. **Recover** - Restore from backups
6. **Review** - Post-incident analysis

### 3. **Backup & Recovery**

```bash
# Automated daily backups
0 2 * * * /opt/melusina/backup.sh

# Test restore monthly
docker-compose exec database pg_restore -d melusina /backups/latest.sql
```

## Security Checklist

### Pre-Production

- [ ] Change all default passwords
- [ ] Enable firewall rules
- [ ] Configure TLS certificates
- [ ] Enable database encryption
- [ ] Configure S3 bucket policies
- [ ] Set up audit logging
- [ ] Enable MFA for admins
- [ ] Implement RBAC
- [ ] Run vulnerability scan
- [ ] Document security procedures

### Ongoing

- [ ] Weekly: Review access logs
- [ ] Monthly: Security patches
- [ ] Quarterly: Access review
- [ ] Annually: Penetration testing
- [ ] Annually: SOC 2 audit

## Support

- **Security Issues:** security@melusina-os.org (PGP key: https://melusina-os.org/pgp)
- **Bug Bounty:** https://melusina-os.org/security/bug-bounty
- **Security Advisories:** https://melusina-os.org/security/advisories

---

**Report a vulnerability?** Email security@melusina-os.org with PGP encryption.
