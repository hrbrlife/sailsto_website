# Sails.to Website — Final Audit & Implementation Gameplan
**Date:** January 21, 2026  
**Status:** ✅ IMPLEMENTATION COMPLETE — Ready for beta launch

---

## Fee Structure (CONFIRMED)

### Primary Fees
| Fee Type | Amount | When Charged | Notes |
|----------|--------|--------------|-------|
| Direct placement | 0.5% | **Only after soft cap reached** | Investor risk limited to Clearstream fees if soft cap missed |
| Broker network | 6% | After soft cap reached | 100% goes to introducing broker |
| Secondary trades | 0.5% | On trade execution | Split ⅓ platform, ⅔ brokers |
| Trust & admin | 1%/yr | Annually | For ongoing administration |

### Optional Services
| Service | Cost | Timeline |
|---------|------|----------|
| ISIN/Clearstream conversion | ~$4K | ~1 week |
| ViennaMTF listing | ~$3K | Additional |

### Key Investor Protection
**Soft cap miss = Zero platform fees.** Investors only lose any Clearstream fees they've incurred (if they converted to ISIN). Platform fees (0.5%) only charged once soft cap is reached.

---

## Implementation Status — ALL COMPLETE ✅

### Glossary Term Pages (20/20) ✅
All created in `/knowledge/glossary/`:
- security-token.html, kyc.html, aml.html, isin.html, clearstream.html
- wyoming-dao-llc.html, series-llc.html, spv.html
- accredited-investor.html, professional-investor.html
- reg-s.html, reg-d.html, solana.html, smart-contract.html
- tradfi-bridge.html, tokenization.html, custody.html
- secondary-trading.html, cap-table.html, distributions.html

### Blog Posts (7/7) ✅
All created in `/knowledge/blog/`:
- why-wyoming.html
- security-tokens-explained.html
- sec-guidance-2025.html
- institutional-adoption.html
- real-estate-tokenization.html
- kyc-compliance-guide.html
- tradfi-bridge-explained.html

### Guide Pages (2/2) ✅
Created in `/knowledge/guides/`:
- getting-started.html
- wyoming-dao-explained.html

### Footer Fix ✅
- Changed "Sails.to Foundation" → "Sails.to DAO LLC" on 15 pages

### Legal Dates Fix ✅
- Updated all dates from "January 2025" → "January 2026" in company/legal.html

### OG Meta Tags ✅
Added to:
- issuers.html
- investors.html
- brokers.html
- regulated.html
- company/legal.html
- knowledge/docs/index.html

### Pricing Page ✅
- Created pricing.html with complete fee breakdown

### Content Updates ✅
- Trust fee (1%/yr) already in issuers.html fee table
- Added $150K minimum investment to investors.html hero
- Fee structure with soft cap protection correctly explained in pricing.html

---

## Site Structure (Final)

```
drafts/
├── index.html (home)
├── signup.html
├── pricing.html ← NEW
├── issuers.html
├── investors.html
├── brokers.html
├── regulated.html
├── whatsails.html
├── pitchdeck.html
├── exec_summ.html
├── styles.css
├── company/
│   ├── about.html
│   ├── contact.html
│   └── legal.html
├── knowledge/
│   ├── index.html
│   ├── faq.html
│   ├── blog/
│   │   ├── index.html
│   │   ├── why-wyoming.html
│   │   ├── security-tokens-explained.html
│   │   ├── sec-guidance-2025.html
│   │   ├── institutional-adoption.html
│   │   ├── real-estate-tokenization.html
│   │   ├── kyc-compliance-guide.html
│   │   ├── tradfi-bridge-explained.html
│   │   └── future-of-tokenized-securities.html
│   ├── docs/
│   │   └── index.html
│   ├── glossary/
│   │   ├── index.html
│   │   └── [20 term pages]
│   └── guides/
│       ├── getting-started.html ← NEW
│       └── wyoming-dao-explained.html ← NEW
└── assets/
    ├── css/glossary.css
    ├── js/glossary.js
    └── content/glossary.json
```

---

## Ready for Launch ✅

All identified issues have been resolved. Site is ready for beta launch.

*Last updated: January 21, 2026*
