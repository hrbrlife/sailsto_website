---
title: "Wallet Verification Guide"
type: "doc"
slug: "wallet-verification"
category: "general"
difficulty: "intermediate"
readTime: "5 min read"
description: "Wallet Verification Guide"
stylesheets:
  - "/css/main.css"
  - "/fonts/fonts.css"
date: "2025-01-01"
sitemap:
  priority: 0.5
  changefreq: "monthly"
---

Verify cryptocurrency wallet ownership and assess blockchain risk for crypto exchanges, DeFi platforms, and Web3 applications.

## Overview

Wallet verification includes:

1. **Ownership Proof** - User signs message with private key
2. **Address Validation** - Checksum verification
3. **Transaction History** - On-chain analysis
4. **Risk Assessment** - Sanctions, mixing services, fraud
5. **Source of Funds** - Transaction graph analysis

## Supported Networks

| Network | Symbol | Address Format | Explorer |
|---------|--------|----------------|----------|
| Bitcoin | BTC | `1A1zP1eP...` or `bc1q...` | blockchain.com |
| Ethereum | ETH | `0x742d35Cc...` | etherscan.io |
| Polygon | MATIC | `0x742d35Cc...` | polygonscan.com |
| Binance Smart Chain | BSC | `0x742d35Cc...` | bscscan.com |
| Solana | SOL | `7EqQdE...` | solscan.io |
| Cardano | ADA | `addr1...` | cardanoscan.io |

## Ownership Verification

### Message Signing

**User signs message:**

```javascript
// MetaMask example
const message = "Verify ownership for Melusina case #xyz789";
const signature = await ethereum.request({
  method: 'personal_sign',
  params: [message, userAddress]
});

// Submit to Melusina
await fetch('https://kyc.yourdomain.com/api/v1/wallets/verify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    case_id: 'case_xyz789',
    address: userAddress,
    network: 'ethereum',
    message: message,
    signature: signature
  })
});
```

**Melusina verifies:**

```python
from eth_account.messages import encode_defunct
from web3 import Web3

def verify_signature(address, message, signature):
    w3 = Web3()
    message_hash = encode_defunct(text=message)
    recovered_address = w3.eth.account.recover_message(
        message_hash,
        signature=signature
    )
    return recovered_address.lower() == address.lower()
```

### Bitcoin Signature

```bash
# User signs with Bitcoin wallet
bitcoin-cli signmessage "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" \
  "Verify ownership for Melusina case #xyz789"

# Returns signature
"H1234567890abcdef..."
```

## Risk Assessment

### Chainalysis Integration

```env
WALLET_SCREENING_PROVIDER=chainalysis
CHAINALYSIS_API_KEY=your_api_key
CHAINALYSIS_RISK_THRESHOLD=medium
```

**Risk categories:**

- **Severe:** Direct sanctions, terrorism financing
- **High:** Darknet markets, ransomware, child exploitation
- **Medium:** Mixing services, high-risk exchanges
- **Low:** Scam, stolen funds (indirect)

### Check Wallet

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/wallets/screen \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "network": "ethereum"
  }'
```

**Response:**

```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "network": "ethereum",
  "risk_level": "low",
  "risk_score": 15,
  "sanctions": false,
  "exposures": [
    {
      "category": "exchange",
      "name": "Binance",
      "direction": "received",
      "amount_usd": 5000,
      "percentage": 45
    },
    {
      "category": "defi",
      "name": "Uniswap",
      "direction": "sent",
      "amount_usd": 3000,
      "percentage": 27
    }
  ],
  "flags": [],
  "last_activity": "2025-11-10T14:30:00Z",
  "total_received_usd": 11000,
  "total_sent_usd": 10500
}
```

## Transaction Analysis

### Source of Funds

Trace incoming transactions:

```bash
curl https://kyc.yourdomain.com/api/v1/wallets/{address}/source-of-funds \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "address": "0x742d35Cc...",
  "analysis_depth": 3,
  "sources": [
    {
      "source_type": "exchange",
      "name": "Coinbase",
      "amount_usd": 8000,
      "percentage": 72.7,
      "hops": 1,
      "risk": "low"
    },
    {
      "source_type": "mining",
      "amount_usd": 2000,
      "percentage": 18.2,
      "hops": 2,
      "risk": "low"
    },
    {
      "source_type": "unknown",
      "amount_usd": 1000,
      "percentage": 9.1,
      "hops": 3,
      "risk": "medium"
    }
  ],
  "recommendation": "approved"
}
```

### Mixing Services Detection

```json
{
  "mixing_detected": true,
  "mixers": [
    {
      "name": "Tornado Cash",
      "amount_btc": 0.5,
      "amount_usd": 15000,
      "timestamp": "2025-10-15T12:00:00Z"
    }
  ],
  "recommendation": "review_required"
}
```

## On-Chain KYC Providers

### Elliptic

```env
WALLET_SCREENING_ELLIPTIC_ENABLED=true
WALLET_SCREENING_ELLIPTIC_API_KEY=your_api_key
WALLET_SCREENING_ELLIPTIC_SECRET=your_secret
```

Features:
- Sanctions screening
- Typology detection (ransomware, fraud, etc.)
- Cross-chain analysis
- Real-time monitoring

### Coinfirm

```env
WALLET_SCREENING_COINFIRM_ENABLED=true
WALLET_SCREENING_COINFIRM_API_KEY=your_api_key
```

Features:
- AML risk reports
- C-Score (0-100 risk rating)
- Regulatory compliance
- Transaction monitoring

## Monitoring & Alerts

### Continuous Monitoring

```env
WALLET_MONITORING_ENABLED=true
WALLET_MONITORING_INTERVAL=3600  # Check every hour
WALLET_MONITORING_ALERT_THRESHOLD=medium
```

**Alert triggers:**

- New incoming transaction from sanctioned address
- Large transaction (>$10,000)
- Interaction with high-risk contract
- Balance change >50%

### Webhook Notification

```json
{
  "event": "wallet.high_risk_transaction",
  "timestamp": "2025-11-13T14:30:00Z",
  "data": {
    "case_id": "case_xyz789",
    "address": "0x742d35Cc...",
    "transaction": {
      "hash": "0xabc123...",
      "from": "0xsanctioned...",
      "amount_usd": 50000,
      "risk": "severe",
      "reason": "OFAC sanctioned address"
    }
  }
}
```

## Multi-Signature Wallets

### Gnosis Safe Verification

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/wallets/verify-multisig \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "address": "0xmultisig...",
    "network": "ethereum",
    "signers": [
      "0xsigner1...",
      "0xsigner2...",
      "0xsigner3..."
    ]
  }'
```

**Verify ownership:**
- Each signer signs message
- Check threshold (e.g., 2-of-3)
- All signers must pass risk assessment

## DeFi Protocol Analysis

### Smart Contract Interaction

Analyze interactions with DeFi protocols:

```json
{
  "address": "0x742d35Cc...",
  "defi_protocols": [
    {
      "protocol": "Uniswap V3",
      "type": "DEX",
      "interactions": 45,
      "total_volume_usd": 123000,
      "risk": "low"
    },
    {
      "protocol": "Aave",
      "type": "Lending",
      "interactions": 12,
      "supplied_usd": 50000,
      "borrowed_usd": 20000,
      "risk": "low"
    }
  ]
}
```

## NFT Verification

### Check NFT Ownership

```bash
curl https://kyc.yourdomain.com/api/v1/wallets/{address}/nfts \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Use cases:**
- Token-gated access
- NFT-based identity
- Proof of community membership

## Compliance

### Travel Rule

For transactions >$1,000 (FATF guidance):

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/travel-rule \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "originator": {
      "name": "John Doe",
      "address": "0xoriginator...",
      "case_id": "case_xyz789"
    },
    "beneficiary": {
      "address": "0xbeneficiary...",
      "vasp": "Coinbase"
    },
    "amount_usd": 5000,
    "asset": "ETH"
  }'
```

## Best Practices

### 1. **Multiple Addresses**

Allow users to verify multiple addresses:

```bash
curl -X POST https://kyc.yourdomain.com/api/v1/cases/{case_id}/wallets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "wallets": [
      {"address": "1A1zP1eP...", "network": "bitcoin"},
      {"address": "0x742d35Cc...", "network": "ethereum"}
    ]
  }'
```

### 2. **Re-screening**

Re-screen wallets daily for new risks.

### 3. **Thresholds**

Configure risk tolerance:

```env
WALLET_AUTO_APPROVE_RISK=low
WALLET_MANUAL_REVIEW_RISK=medium
WALLET_AUTO_REJECT_RISK=severe
```

## Support

- **Chainalysis Support:** https://chainalysis.com/support
- **Elliptic Support:** https://elliptic.co/support
- **Melusina Wallet Integration:** wallets@melusina-os.org

---

**Integrating wallet verification?** Check our [API examples](https://github.com/melusina/wallet-examples).
