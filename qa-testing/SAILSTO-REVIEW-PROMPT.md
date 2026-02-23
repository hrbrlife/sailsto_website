# Sails.to — Review Context for QA Agents

## What Is Sails.to?

Sails.to is a **compliant sovereign tokenized and classic securities issuance and OTC trading platform**. It provides sovereign infrastructure for issuing, managing, and trading compliant securities on blockchain — with optional bridging to traditional finance venues via CrossConversion.

**This is NOT DeFi.** It is compliant market infrastructure built on blockchain rails. All products are currently in **private testing**.

### Sails.to’s Role: Technology Infrastructure Provider

Sails.to is a **Technology Infrastructure Provider** — not a broker-dealer, not an investment adviser, not a fiduciary, and has no custody of investor funds or securities. It provides templated IT and legal wrapper infrastructure to issuers. The issuer is the self-issuer; Sails.to just provides them with the technology and templated legal structure.

Sails.to works **together with a licensed trust company** to provide compliance oversight and trust services as regulated activities. There is no ability to buy or sell anything on sails.to directly — all investor access is via regulated licensed brokers only.

---

## Core Products

| Product | Status | Description |
|---------|--------|-------------|
| **CrossBonds** | Private Testing | Tokenized bonds — fixed income, profit participation, hybrid structures |
| **CrossShares** | Private Testing | Tokenized equity with DAO governance and voting rights |
| **CrossRWA** | Private Testing | Real-world asset tokenization — real estate, commodities, infrastructure |

---

## Key Mechanisms

### CrossConversion
The signature feature: securities can be held **on-chain** (Solana tokens) OR via **traditional bank custody** (ISIN-numbered instruments via Clearstream XS) — and converted between forms at will. **0.75% conversion fee.**

### Broker-Mediated OTC Network
Sails.to is NOT an exchange. Investors trade WITH their broker. Brokers trade with each other via the OTC network. The broker is always the counterparty of record. This is the compliance mechanism that preserves private placement exemptions (Reg D, Reg S).

Brokers operate their own regulated instance via **sails.broker.tld** white-label platform. Brokers have a **duty of care** — checking suitability of investment products for their clients and verifying whether clients are **QIC’d** (Qualified Investor Certified) for the applicable jurisdiction. US broker for US investors, Mauritius broker for Mauritius investors — jurisdiction-matched.

### The Broker Hop
1. Investor requests quote from their broker
2. Broker sources liquidity (internal, another broker, or issuer treasury)
3. Broker executes as principal
4. Broker allocates to client

### Soulbound Credential System
Hierarchical non-transferable NFTs controlling access:
- Platform License NFT → Broker/Issuer License NFT → KYC Credential Token
- Each role credentialed by the authority above
- No credential = no access

### DAO LLC Services
- **Wyoming Series LLC DAO** — US structure, series segregation, Reg D friendly
- **Marshall Islands DAO LLC** — Offshore, Reg S friendly, tax-neutral
- Near-instant legal entity setup
- The issuing SPV is a Series of a Wyoming DAO LLC **controlled by the issuer**

#### DAO LLC Five-Series Structure
Each issuance creates a DAO LLC with five firewalled Series:

| Series | Purpose | Control |
|---|---|---|
| **Operating Series** | Cashflow, pledges, underlying assets | Issuer operates, Trust authenticates |
| **Revenue Series** | Collected income — investors paid first (waterfall priority) | Issuer initiates, Trust authenticates |
| **Deposit Series** | 3% security deposit — backs orderly wind-down and trustee remedies | Issuer + Trust (both access, trust authenticates use) |
| **Treasury Series** | Token reserves, un-issued tokens, unclaimed distributions | Trust oversight |
| **CrossConversion Series** | On-chain token ↔ bankable ISIN conversion lockbox | Issuer requests, Trust authenticates |

All Series are legally firewalled. The Deposit Series is **under trust** administered by a licensed trust company. All PPMs mandate **arbitration** for dispute resolution. Protection measures ensure no default situation proceeds without settlement attempts first.

---

## Entity Structure

| Entity | Jurisdiction | Role |
|--------|-------------|------|
| **Hrbr.Life Ltd.** | Marshall Islands | IP owner, commercial licensing |
| **Association Melusina-OS.org** | Switzerland | Protocol steward, open-source |
| **Sails.to DAO LLC** | Wyoming, USA | Platform operator |
| **CCA.sh** | Montana, USA | Currency conversion agent / MSB entity |
| **AiTX.pro** | Mauritius (FSC) | Licensed brokerage |
| **InstaTrust** | SVG | Trust company (approval in principle) |

---

## Target Audiences

1. **Issuers** — Companies raising $600K+ via tokenized securities
2. **Professional Investors** — Accredited/qualified investors seeking deal flow
3. **Licensed Brokers** — Broker-dealers adding tokenized securities capability
4. **Business Introducers** — Referral partners earning commissions
5. **Trust Companies** — Fiduciaries administering tokenized assets
6. **Regulated Institutions** — Banks, asset managers wanting white-label infrastructure

---

## Technology Stack

- **Solana** — Blockchain (Solana only)
- **Cap'n Proto** — High-performance RPC framework
- **Clearstream XS** — Global settlement and custody
- **Vienna MTF** — Optional exchange listing (~€3-5k, ~1 week)
- **Hugo** — Static site generator for sails.to website

---

## Brand Voice

- **Confrontational confidence** — "Your license is a PDF in someone's inbox."
- **Problem-first** — Lead with pain, then solution
- **Technically precise** — Securities terms used correctly
- **Institutional but accessible** — Serious for compliance officers, clear for founders

---

## Regulatory Considerations

- All offerings under Reg D 506(c), Reg S, or EU equivalents
- KYC/AML mandatory for all participants
- Professional/accredited investors only — no retail access
- MSB/Money Transmission obligations for conversion activities
- GDPR compliance required for EU visitors
- Securities disclaimers required on pages describing specific offerings

---

## Site Structure (Hugo)

The sails.to website is a Hugo static site with:
- **Audience pages**: /brokers/, /investors/, /issuers/, /introducers/, /trustees/, /regulated/
- **Product pages**: /pricing/, /signup/, /compliance/, /security/, /oversight/, /compare/, /whatsails/, /players/
- **Company**: /company/about/, /company/contact/, /company/legal/
- **Knowledge Hub**: /knowledge/ with sub-sections:
  - /knowledge/docs/ — Technical documentation (15+ pages)
  - /knowledge/guides/ — Getting started guides (5 pages)
  - /knowledge/glossary/ — Financial/technical glossary (50+ terms)
  - /knowledge/faq/ — Frequently asked questions
  - /knowledge/roadmap/ — Product roadmap
  - /knowledge/blog/ — Blog section

---

## What Makes Sails.to Different

1. **CrossConversion** — No other platform lets you seamlessly move between on-chain and traditional custody
2. **Broker-mediated OTC** — Compliant by architecture, not bolt-on compliance
3. **Self-hosted compliance** — Each participant runs their own Melusina OS instance
4. **DAO LLC integration** — Near-instant legal entities mapped to on-chain governance, 5-Series firewalled structure
5. **Soulbound credentials** — Identity infrastructure, not just KYC checkboxes
6. **Solana** — Built on Solana blockchain
7. **Clearstream bridge** — Real global custody, not just crypto custody
8. **Technology infrastructure provider** — Not a dealer or fiduciary; works with licensed trust company
9. **Regulated broker access only** — Duty of care, suitability checks, QIC verification
