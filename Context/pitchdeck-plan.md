# Sails.to Investor Pitch Deck — Final Plan

**Raise:** $12.5M for 25% post-money  
**Pre-money:** $37.5M | **Post-money:** $50M  
**Minimum Investment:** $150,000  
**Target:** Institutional investors, family offices, strategic partners

---

## Design Philosophy

**Aesthetic:** 80s glam editorial meets institutional credibility
- **Typography:** Cormorant Garamond (display), DM Sans (body), Playfair Display (accents)
- **Color palette:** Ivory/cream base, ink black, gold accents (#C9A227), crimson highlights
- **Layout:** Magazine-style: punchy headline + 2-column editorial substance
- **Diagrams:** Reuse Mermaid flow diagrams from whatsails.html for authority
- **Navigation:** Smooth scroll between slides, click-through to detailed appendix

**Total Slides:** 12-13 (tight, focused, institutional)

---

## SLIDE 1: Cover / Title

### Visual
- Dark hero background (reuse sunrise aesthetic from index.html)
- Logo prominent (sail_logo_w.png on dark)
- Gold accent line separator

### Content

```
RAISE YOUR SAILS
to go beyond with securities that cross the line.

The infrastructure layer where securities cross the line.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Raising: $12.5M at $37.5M pre-money (25% post-money)
Minimum Investment: $150,000

Alexei Karpov — Founder & CEO
Telegram: @akarpovlux | LinkedIn: linkedin.com/in/akarpovlux
WhatsApp: +352621690358

Confidential — NDA on request
```

---

## SLIDE 2: The Problem — "Capital Markets Are Still Forked"

### Headline
**"Issuers and investors still choose between worlds."**

### Two-Column Layout

| **DeFi World** | **TradFi World** |
|----------------|------------------|
| Fast, global, 24/7 | Slow, regional, T+2 settlement |
| Programmable, atomic | Paper-bound, manual reconciliation |
| Self-custody | Counterparty custody required |
| No institutional comfort | No retail/global reach |
| Regulatory gray zone | Compliance theater, multi-provider costs |
| **Cost:** Low infrastructure | **Cost:** $100K+ per issuance across multiple vendors |
| **Timeline:** Days | **Timeline:** Months |

### Pain Points (bottom section)

**Securities Issuance:**
- Months-long process
- High legal, admin, banking, registry, trustee, placement costs
- Limited distribution channels

**Private Placements:**
- Uncertain outcomes (allocation, timing, investor follow-through)
- No visibility into process

**Cross-border:**
- Expensive, slow, opaque

**Crypto/Traditional Bridge:**
- Regulatory gaps, compliance nightmares

### Punch Line
**"The instrument is the same. The packaging shouldn't force a choice."**

---

## SLIDE 3: The Solution — "One Security, Any Format"

### Headline
**"We built the bridge."**

### Core Visual (large, centered)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐
│ Solana Token │ ←→ │  TON Token   │ ←→ │ ISIN via Clearstream │
└──────────────┘    └──────────────┘    └──────────────────────┘
       ↓                   ↓                        ↓
  Same security. Same cap table. Same economics.
  Format is a choice, not a product.
```

### Key Innovation Points

**What We Built:**
- Issue compliant securities **once**
- Settle on Solana or TON (instant, atomic)
- Optional ISIN bridge to traditional custody (~$4K, 1 week)
- KYC'd professional investors can **convert between formats**
- Broker-mediated OTC network (compliance by design)

**The "A-ha":**
> Your security can sit in a Solana wallet in Singapore AND a Clearstream account in Geneva — same cap table entry, different packaging.

**Key Rules:**
- Only KYC'd Professional Investors ($150K typical minimum)
- Broker-mediated transfers (no permissionless DEX)
- On-chain credentials enforce eligibility
- Atomic settlement (Solana: instant, not T+2)

---

## SLIDE 4: The Stack — "Three Revenue Layers"

### Headline
**"Not just tokens. The full stack."**

### Three-Layer Diagram

```
╔═════════════════════════════════════════════════════════════╗
║  SAILS.TO — Securities Issuance & Distribution Platform     ║
║  ────────────────────────────────────────────────────────   ║
║  Issue, manage, trade regulated digital securities          ║
║  Revenue: 0.5-6% on issuance | 0.5% on trading | 1% annual ║
╠═════════════════════════════════════════════════════════════╣
║  CCA.SH — Money Services Business (MSB)                     ║
║  ────────────────────────────────────────────────────────   ║
║  Remittances, payments, fiat on/off ramps, card issuance   ║
║  Revenue: 0.5-2% on corridor volume                         ║
╠═════════════════════════════════════════════════════════════╣
║  MELUSINA OS — Self-Hosted Operating System                 ║
║  ────────────────────────────────────────────────────────   ║
║  Compliance workflows, per-issuance isolation, app store    ║
║  Revenue: SaaS licensing to white-label operators           ║
╚═════════════════════════════════════════════════════════════╝
```

### Why the Stack Matters (bullet points)

- **Integrated:** MSB enables fiat rails for STO; single onboarding unlocks all services
- **Self-hosted:** Zero third-party vendor dependency
- **Licensable:** Melusina white-label = additional revenue stream
- **Strategic:** Licensed entities (80% profit flows to holding company)

**Brand Portfolio:**
- Hrbr.Life (Holding Company)
- AiTX.pro (Mauritius Brokerage)
- Sails.to (STO Platform)
- trade.sails.to (Secondary Trading)
- Cca.sh (MSB Platform)

---

## SLIDE 5: How It Works — "2 Weeks, Not 6 Months"

### Headline
**"From zero to funded in two weeks."**

### Timeline Visual (clean, left-aligned)

```
━━━ ISSUANCE TIMELINE ━━━

Days 1-2:  Due diligence, KYC on principals, legal docs
Day 3:     DAO LLC Series created (instant)
Day 4:     Tokens minted (hard cap amount)
Day 5+:    Distribution begins via 3 channels:

           ┌─ Channel 1: Direct Sales (your network) — 0.5% fee
           ├─ Channel 2: Broker OTC Network — 6% fee  
           └─ Channel 3: ISIN/Clearstream — ~$4K setup

Closing:   Soft cap reached → funds released
           Hard cap met OR duration expires → offering closes
           Unsold tokens burned (final supply = actual investment)

Live:      Secondary trading opens via OTC broker network
```

### Three-Stage Diagram (reuse from whatsails.html)

```
┌─────────────────────────────────────────────────────────┐
│  Phase A: ESCROW (Pre-Soft Cap)                         │
│  • Funds in trust escrow                                │
│  • Optional early-bird discount                         │
│  • Refundable if soft cap not reached                   │
├─────────────────────────────────────────────────────────┤
│  Phase B: FUNDING (Post-Soft Cap)                       │
│  • Funds released to issuer as received                 │
│  • Full price, distribution continues                   │
│  • Only issuer + brokers may allocate                   │
├─────────────────────────────────────────────────────────┤
│  Phase C: ACTIVE (Closed)                               │
│  • Offering complete, unsold tokens burned              │
│  • Secondary trading enabled (OTC broker network)       │
│  • Conversions open to KYC'd holders                    │
└─────────────────────────────────────────────────────────┘
```

### Protection

**Soft Cap Miss = Full Refund (Automatic)**
- Investor receives invested capital back
- Only minimal fees apply (0.5% brokerage + Clearstream if used)
- Structured as zero-coupon redemption

---

## SLIDE 6: Trading & Conversion — "Broker-Mediated, Compliance by Design"

### Headline
**"How securities actually trade."**

### OTC Broker Network Diagram (reuse from whatsails.html)

```
┌────────────────────────────────────────────────────────────┐
│  THE "BROKER HOP" — Why It's Not a DEX                     │
└────────────────────────────────────────────────────────────┘

    Investor A                                    Investor B
    (wants to sell)                               (wants to buy)
         │                                              │
         ↓                                              ↓
    ┌─────────┐                                   ┌─────────┐
    │Broker A │ ←──────── OTC Network ──────────→ │Broker B │
    └─────────┘          (price quote,            └─────────┘
         │               liquidity,                     │
         │               execution)                     │
         └──────────── Atomic Settlement ──────────────┘
                    (Solana: instant DvP)

    ✓ KYC verified at each step
    ✓ Brokers are counterparty of record
    ✓ No permissionless access
    ✓ 0.5% fee split: ⅓ platform, ⅓ buy-side, ⅓ sell-side
```

### Conversion Mechanics (Solana ↔ Clearstream)

```
┌────────────────┐                  ┌──────────────────────┐
│ Solana Token   │ ←── 1:1 Lock ──→ │ ISIN Lockbox Series  │
└────────────────┘                  └──────────────────────┘
                                              │
                                              ↓
                                    ┌──────────────────────┐
                                    │ ISIN-Identified      │
                                    │ Security via         │
                                    │ Clearstream          │
                                    └──────────────────────┘
```

**Key Rules:**
- Issuer controls conversion (with Trust oversight)
- Always 1:1 backed (ISIN securities ≤ locked tokens)
- KYC'd holders may initiate conversion (when enabled)
- Conversion fee: 0.10-0.25% (capped)

---

## SLIDE 7: Business Model — "We Eat When You Eat"

### Headline
**"Zero upfront fees. Pay on success."**

### Revenue Model Table

| Stream | Fee | Who Pays | When | Notes |
|--------|-----|----------|------|-------|
| **Issuance (direct)** | 0.5% | Issuer | On close | Your network, your referral code |
| **Issuance (broker)** | 6% | Issuer | On close | Our OTC broker network |
| **Secondary trading** | 0.5% | Buyer | Per trade | Split: ⅓ platform, ⅓ buy-broker, ⅓ sell-broker |
| **Trust & Admin** | 1%/year | Issuer | Annual | On nominal value |
| **Security deposit** | 3% | Issuer | At issuance | Reserved under trust for fees, legal, winding down |
| **Conversions** | 0.1-0.25% | Requester | Per conversion | Solana ↔ ISIN |
| **MSB corridors** | 0.5-2% | Sender | Per transaction | Remittance spread |
| **Melusina licensing** | SaaS | Operator | Monthly/annual | White-label deployments |

### Unit Economics Example ($10M Raise via Broker Network)

```
Issuance fee:        $600K    (6% of $10M)
Security deposit:    $300K    (3%, reserved)
Annual trust fee:    $100K/yr (1% of nominal)
Secondary trading:    $10K/yr (est. 20% turnover × 0.5%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Year 1 platform revenue per issuer: ~$700K
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Soft Cap Miss:** Only 0.5% brokerage + Clearstream fees apply (no 6% distribution fee)

---

## SLIDE 8: Traction — "Platform, Not Pitch"

### Headline
**"We're not pitching a deck. We're pitching a platform."**

### Platform Maturity

**What's Already Real:**

| Metric | Value | Context |
|--------|-------|---------|
| **KYC/KYB processed** | $200M | Crypto project clients (existing business) |
| **Users verified** | 70,000 | Advanced KYB at scale |
| **Platform completion** | ~70% | Modules production-deployed |
| **Development timeline** | 7 years | Melusina OS in regulated environments |

### Regulatory Milestones

| Jurisdiction | License/Registration | Status |
|--------------|---------------------|--------|
| **Mauritius** | Full Service Investment Dealer (FSC) | ✅ Licensed (in group control) |
| **St. Vincent & Grenadines** | Financial Trustee License | ✅ Approval in principle |
| **Montana + Canada** | MSB registration | 📋 Documentation under review |
| **New Zealand** | VASP registration | 📋 In preparation |
| **Mauritius (extension)** | AI & Robotic investment advisory | 📋 Prepared, awaiting operational status |

### Strategic Board Addition

**Former CEO, State Bank of Mauritius + Airports of Mauritius**
- Joining as Board Member and Chief Strategy Officer
- Direct access to Mauritius financial regulators
- Banking network relationships
- Sovereign fund connections
- Government-level credibility

**Impact:** Transforms profile from "startup" to "institutional platform with government-level relationships"

---

## SLIDE 9: Competition — "Everyone Built Half of It"

### Headline
**"The full-stack, self-hosted, multi-format edge."**

### Competitive Matrix

| Competitor | What They Do | What They Don't |
|------------|--------------|-----------------|
| **Tokeny** | Tokenization infrastructure | No distribution, no trading, no TradFi bridge |
| **ADDX** | Singapore-focused STO platform | No self-custody, limited geography, platform dependency |
| **Securitize** | US-focused compliance + issuance | No DeFi integration, expensive, multi-vendor costs |
| **Fireblocks** | Custody/infrastructure MPC | No issuance, no compliance layer, no legal structure |
| **Clearstream** | Traditional settlement infrastructure | No blockchain native, slow, expensive |
| **Polymath/Polymesh** | Dedicated security token chain | No proven distribution, limited TradFi bridge |

### Our Moat (5 Pillars)

```
1. FULL STACK
   Issuance + distribution + trading + settlement + fiat rails
   
2. SELF-HOSTED
   Zero vendor dependency, issuer controls their data
   Melusina OS: 7 years of development, proven in production
   
3. MULTI-FORMAT
   Same security on Solana, TON, or ISIN
   Interchangeable for KYC'd professional investors
   
4. BROKER NETWORK
   Compliance built in, not bolted on
   OTC network operational from day one
   
5. AI-NATIVE
   Built with AI from the start (3 devs = 30 traditional)
   Not retrofitting old systems
```

---

## SLIDE 10: Team — "Built the Boring Parts of Finance"

### Headline
**"The people who built the institutions we're now disrupting."**

### Core Team Table

| Name | Role | Background | Brings |
|------|------|------------|--------|
| **Alexei Karpov** | Founder & CEO | GMS+ Luxembourg Family Office, Bendura Private Bank Liechtenstein, Jurstax (Mauritius/DIFC/RAK) | Trust/banking expertise, regulatory navigation, 15+ years financial services |
| **Vladislav Mosokkov** | CTO | Deutsche Bank, Oilspace | Crypto + banking software architecture, distributed systems |
| **Lorinc J. Nyitrai** | Data Scientist | UBS, Allianz, TBS | Quantitative modeling, risk analysis, compliance algorithms |
| **Rudi van der Lugt** | Financial Operations | Nomura, ABN AMRO, tier-1 institutions | Securities back-office, settlement operations, post-trade |
| **3 Full-stack Developers** | Engineering | AI-first development | Extreme productivity: 3 devs = 30 traditional |

### Advisory Bench

| Name | Affiliation | Credentials |
|------|-------------|-------------|
| **Jean-Luc Jourdan** | GMS+ Family Office, Luxembourg | Court-witnessed expert, CPA, FINMA-Authorized Shareholder & Co-Founder CIM Bank Geneva |
| **Daniil Savitskii** | Advokaadibüroo K&S Legal, Estonia | Member of the Bar in Tallinn, EUFA Juridical Committee |
| **Akis Papakyriacou, MCIArb** | Akis Papakyriacou LLC, Cyprus | Top securities and banking lawyer (Legal 500) |

### Development Methodology

**7 years:** Melusina OS foundation (used in regulated environments)  
**20 months:** AI-assisted development (Phase 1)  
**6 months:** AI-first approach (Phase 2)

**Result:** Platform complexity that would require 20-30 traditional developers built by team of 7.

---

## SLIDE 11: Go-to-Market — "Five Doors, One Ecosystem"

### Headline
**"Super-app strategy: capture via one door, open the entire ecosystem."**

### Entry Points (Unilever-style Segmentation)

```
┌────────────────────────────────────────────────────────────┐
│  1. TRUST SERVICES                                         │
│     Investment vehicle setup, DAO LLC formation            │
├────────────────────────────────────────────────────────────┤
│  2. INCORPORATION SERVICES                                 │
│     Fast company formation (minutes to days)               │
├────────────────────────────────────────────────────────────┤
│  3. INVESTMENT SERVICES                                    │
│     Direct investment access to curated opportunities      │
├────────────────────────────────────────────────────────────┤
│  4. DIGITAL ASSET EXCHANGE                                 │
│     VASP-regulated, traditional cryptocurrencies           │
├────────────────────────────────────────────────────────────┤
│  5. REMITTANCE SERVICES                                    │
│     Cross-border payments, MSB-regulated corridors         │
└────────────────────────────────────────────────────────────┘
```

### GTM Phases

| Phase | Focus | Timeline | Key Milestones |
|-------|-------|----------|----------------|
| **Now** | Crypto-native issuers, existing network | Live | 3-5 pilot issuances, broker partnerships |
| **6 months** | SME capital raises ($5M-$50M), MENA expansion | Q3 2026 | 10+ issuers, $50M+ volume |
| **12 months** | Institutional funds, white-label Melusina | Q1 2027 | Break-even, 3+ white-label operators |
| **24 months** | Vienna MTF pipeline, broker network at scale | Q1 2028 | Category leader, $500M+ annual volume |

### Distribution Channels

- **Direct:** Issuer network acquisition (low CAC)
- **Broker partnerships:** Licensed OTC dealers (fee share model)
- **AI agents + Telegram bots:** Investor acquisition at scale
- **Super-app integration:** Single KYC, cross-sell all services

---

## SLIDE 12: Cap Table & The Ask — "Institutional Terms"

### Headline
**"$12.5M for 25% post-money — transparent structure, aligned incentives."**

### The Raise

```
┌─────────────────────────────────────────────────────┐
│  RAISING: $12.5M                                    │
│  PRE-MONEY VALUATION: $37.5M                        │
│  POST-MONEY VALUATION: $50M                         │
│  EQUITY SOLD: 25% (post-money)                      │
│  MINIMUM INVESTMENT: $150,000                       │
└─────────────────────────────────────────────────────┘
```

### Pre-Money Cap Table (Before Investors)

**Other Investors Underfunding Structure:**
- Planned Other Investors: 300K units → 9.9%
- Issued Other Investors so far: 170K units
- Proportional equity now: (170/300) × 9.9% = **5.61%**

**Matching Rule (Aligned Incentives):**
- 1× Other Investors holders: **5.61%**
- 1× Founder + Management match: **5.61%**
- 1× SM introducers match: **5.61%**
- Founder base (remaining): **83.17%**
- **Total: 100%**

**Note:** Matching is pre-money and not topped up. Other Investors/SM allocations are diluted alongside founders by investor entry.

---

### Post-Money Cap Table (After $12.5M Investment)

**All existing holders diluted by 0.75:**

| Holder | Shares | % |
|--------|--------|---|
| **Investors** | 333,333 | 25.00% |
| **Other Investors holders** | 56,100 | 4.21% |
| **Founder + Mgmt (match)** | 56,100 | 4.21% |
| **SM introducers** | 56,100 | 4.21% |
| **Founder base** | 831,700 | 62.38% |
| **Total** | 1,333,333 | 100% |

---

### Seniority Program (Post-Money Dilution)

**Structure:**
- 5 senior team members: Rudi, Vlad, Lorinc, Daniil, Anoop
- Base: 1% each at close
- Growth: +1% per person per year
- Duration: 4 years
- **Total new issuance: 5% per year × 4 years = 25% cumulative**

**Critical Point:** This is **new equity issuance post-close**. All existing holders (including investors) are diluted pro-rata.

**Dilution Table:**

| Year | Investor % | Other Investors % | Seniority Cumulative % |
|------|------------|---------|------------------------|
| **Post-close (Y0)** | 25.00% | 4.21% | 0% |
| **Y1** | 23.81% | 4.01% | 5% |
| **Y2** | 22.68% | 3.82% | 10% |
| **Y3** | 21.60% | 3.64% | 15% |
| **Y4** | 20.57% | 3.47% | 25% |

**Visual:** Simple line graph showing ownership drift over 4 years

---

### Use of Funds

| Allocation | Amount | % | Purpose |
|------------|--------|---|---------|
| **Engineering** | $4.4M | 35% | Platform completion (remaining 30%), multi-chain expansion (TON), smart contract audits |
| **Regulatory** | $2.5M | 20% | License applications (5+ jurisdictions), compliance infrastructure, legal counsel |
| **GTM/Sales** | $2.5M | 20% | Issuer acquisition, broker partnerships, brand building, investor marketing |
| **Operations** | $1.9M | 15% | Team scaling (7 → 15 people), infrastructure, office |
| **Reserve** | $1.3M | 10% | Working capital, opportunities, contingency |

---

### 24-Month Milestones (What This Unlocks)

**✓ Technical:**
- Platform 100% complete
- Multi-chain operational (Solana + TON)
- 5+ white-label Melusina operators

**✓ Regulatory:**
- 5+ jurisdictions operational
- MSB corridors live (Montana, Canada, NZ)
- VASP registration complete

**✓ Commercial:**
- $500M+ annual issuance volume
- 100+ deals closed
- 20+ active brokers on OTC network

**✓ Financial:**
- Break-even at ~$15M revenue (achievable by end of Y2)
- Positioned for Series A at $100M+ valuation

---

### Terms Clarity (Explicit Disclosure)

**✓ Investors are diluted pro-rata by the seniority program**  
**✓ Other Investors/SM matching is pre-money and not topped up**  
**✓ No protected pools, no preferential anti-dilution**  
**✓ Standard board seat + observer rights**  
**✓ Information rights + audit access**

---

### Alternate Structure (Appendix Only)

**Convertible Notes Option:**
- Raise: $10M
- Pre-money: $35M
- Note size: $150K each (67 notes)
- Conversion at Series A with 20% discount or $40M cap

*This option available for investors preferring note structure; same underlying economics.*

---

## SLIDE 13: Close — "Why This, Why Now, Why Us"

### Headline
**"The next decade of capital markets starts here."**

### Three Truths

**1. THE MARKET IS MOVING**

> Tokenized securities went from concept to BlackRock in 5 years.  
> The infrastructure layer is up for grabs.  
> First-mover with full-stack + regulatory approval wins.

**2. WE BUILT THE FULL STACK**

> Not a feature. Not a protocol. Not a wrapper.  
> A complete, self-hosted platform that works today.  
> 70% deployed. $200M KYC processed. 7 years of development.

**3. WE KNOW THE TERRAIN**

> Built by people who've done trust, banking, and compliance at the highest levels.  
> Deutsche Bank. UBS. Nomura. ABN AMRO. FINMA-authorized advisors.  
> Former CEO State Bank Mauritius joining as board member and CSO.

---

### Why Now (Visual Timeline)

```
2020 ──────── Crypto boom, DeFi explosion
2021 ──────── Regulatory crackdown, clarity begins
2022 ──────── Wyoming DAO LLC framework, Marshall Islands
2023 ──────── BlackRock tokenizes, institutional validation
2024 ──────── MiCA passes, US clarity emerging
2025 ──────── Infrastructure window opens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2026 ──────── ★ WE ARE HERE ★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              Build the rails everyone will use.
```

---

### The Ask (Clear, Direct)

```
╔═══════════════════════════════════════════════════════════╗
║  Partner with us to own the infrastructure layer.         ║
║                                                            ║
║  $12.5M for 25% of the platform that bridges two worlds.  ║
╚═══════════════════════════════════════════════════════════╝
```

**Contact:**
- **Alexei Karpov** — Founder & CEO
- Telegram: @akarpovlux
- LinkedIn: linkedin.com/in/akarpovlux
- WhatsApp: +352621690358

**Next Steps:**
1. Sign NDA
2. Full data room access (tech, legal, financial)
3. Platform demo + team meeting
4. Term sheet within 2 weeks

---

## APPENDIX (Click-Through, Not Main Flow)

### A1: Full Smart Contract Architecture
- 16 contracts on Solana
- Governance, identity, issuance, trading, finance layers
- Security audits + formal verification status

### A2: Detailed Legal Structure
- DAO LLC formation mechanics
- Series structure internals
- Trust oversight protocols
- ISIN registration process

### A3: Regulatory Timeline & Strategy
- Jurisdiction-by-jurisdiction expansion plan
- License application status + timelines
- Compliance frameworks per region
- Risk mitigation strategies

### A4: Team Full Bios
- Extended backgrounds for core team
- Advisory board detailed credentials
- Hiring plan for next 24 months

### A5: Financial Model Deep Dive
- Full 5-year P&L projections
- Sensitivity analysis (volume, fees, timing)
- Comparable company analysis
- Exit scenarios + returns modeling

### A6: Melusina OS Technical Deep Dive
- Architecture overview
- App store model
- Pearl isolation mechanics
- Security model + certifications

### A7: Comparable Analysis
- Securitize, ADDX, Tokeny, Polymath detailed comparison
- Market positioning matrix
- Competitive advantages breakdown

### A8: Pipeline & Partnerships
- Current issuer pipeline (confidential)
- Broker partnership status
- White-label operator prospects
- Strategic partnerships in negotiation

---

## Implementation Notes for HTML Build

### Design System
- Reuse CSS from index.html (variables, typography, colors)
- Adapt navbar for deck navigation (slide numbers, progress bar)
- Smooth scroll animations between slides
- Click regions for appendix links
- Print-friendly CSS (each slide = page break)

### Diagrams to Port
- OTC broker hop sequence (from whatsails.html)
- Three-stage issuance flow (from whatsails.html)
- Conversion mechanics (from whatsails.html)
- Stack layer diagram (simplified from exec_summ.html)

### Interactive Elements
- Cap table ownership drift graph (Years 0-4)
- Use of funds pie chart (animated)
- Timeline visualization (market milestones)
- Hover states for competitive matrix

### Mobile Considerations
- Stack slides vertically on mobile
- Simplify diagrams for small screens
- Ensure tables are readable (horizontal scroll if needed)
- Contact info always accessible (sticky footer)

---

## Final Checklist Before Building

- [ ] Confirm $12.5M / $37.5M pre / 25% post math
- [ ] Verify Other Investors 170k/300k = 5.61% calculation
- [ ] Triple-check seniority dilution table (investors 25% → 20.57%)
- [ ] Get approval on "Former CEO State Bank Mauritius" language
- [ ] Confirm which pipeline details are disclosable
- [ ] Finalize use of funds breakdown with CFO
- [ ] Get headshots for team slide
- [ ] Export logo assets (sail_logo.png, sail_logo_w.png)
- [ ] Prepare demo platform screenshots
- [ ] Draft NDA template for "next steps"

---

**Status:** Ready to build HTML implementation  
**Owner:** Alexei Karpov  
**Last Updated:** January 14, 2026  
**Version:** 1.0 (Final)
