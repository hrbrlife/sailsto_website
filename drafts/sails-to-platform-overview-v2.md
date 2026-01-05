# Sails.to: Regulated Infrastructure for Tokenized Securities Issuance, Compliance, and Multi-Broker OTC Trading

**A Complete Guide for Newcomers**

---

## Executive Summary

Sails.to is an end-to-end platform for issuing, managing, and trading regulated securities on blockchain. It provides issuers with everything they need to launch compliant tokenized securities, while operating a multi-broker OTC (over-the-counter) network for secondary liquidity—with optional bridging to traditional finance venues like the Vienna MTF.

This is not a DeFi protocol. It is regulated market infrastructure built on blockchain rails.

### What Sails.to Provides

- **Issuance tools**: Create and launch security tokens under exemptions like Reg D, Reg S, and EU equivalents
- **Compliance infrastructure**: Self-hosted KYC/AML tooling, investor classification, transfer restrictions
- **Lifecycle management**: Investor communications, corporate actions (coupons, redemptions), reporting
- **Multi-broker OTC network**: Licensed brokers provide liquidity and execution for secondary trading
- **Optional platform-operated broker**: A Sails.to-operated, licensed broker entity can also execute on the same OTC network (where jurisdictionally compatible)
- **Hybrid liquidity**: Global settlement via Clearstream XS ISIN + optional Vienna MTF listing (~€3-5k, ~1 week)
- **DAO LLC services**: Near-instant legal entity setup via Wyoming Series LLC DAO or Marshall Islands DAO LLC structures

### Multi-Chain Architecture

Sails.to is designed as a **multi-chain platform**:

- **Currently supported**: Solana and TON
- **Architecture**: Chain-agnostic credential and settlement layer
- **Future**: Additional chain support as market demand and regulatory clarity evolve

Issuers and brokers can choose their preferred chain based on their investor base, jurisdiction, and operational preferences. The credential hierarchy, fee model, and OTC network operate consistently across supported chains.

### Operating Environment

The platform runs on **Melusina OS**—a heavily modified, blockchain-integrated version of Sandstorm.io. Melusina provides the self-hosted operating environment where brokers and issuers run their compliance, issuance, and servicing applications. Each participant gets an isolated deployment with access to a shared app store, per-issuance containers ("pearls"), and internal content-addressed storage for documents and backups.

Melusina OS is the operating environment. **Sails.to is the product**.

---

## Part 1: The Market Structure

### 1.1 Why Broker-Mediated OTC

Securities law regulates not just who receives economic benefits (dividends, coupons, voting), but who may **own** and **transfer** the security itself. For private placement exemptions like Reg D (US accredited investors) or Reg S (non-US investors), restrictions apply to ownership and transfer—not merely economic realization.

An open AMM or public DEX is:
- Globally accessible
- Permissionless (anyone can buy)
- Anonymous (no eligibility screening)

That is legally equivalent to "anyone may buy this security"—which breaks most private placement exemptions.

Sails.to solves this with a **broker-mediated OTC network**:

- **Investors trade with their broker**, not directly with pools or each other
- **Brokers trade with each other** via the network
- **Brokers are always the counterparty of record**

This is how bond markets, private credit, and institutional securities already work. The broker intermediation is the compliance mechanism.

### 1.2 The Broker's Role

Brokers on Sails.to:
- Perform KYC/AML and investor suitability checks
- Ensure only eligible investors participate
- Provide execution, custody, and dispute resolution
- Quote prices and provide liquidity
- Handle client onboarding and communications

The platform provides infrastructure; brokers (including any platform-operated broker entity where licensed) provide the regulated intermediation layer.

### 1.4 Sails.to as a Broker (Where Licensed)

In parallel to third-party brokers, Sails.to may also operate its own **licensed broker entity** (e.g., under an El Salvador digital-asset services framework) that participates on the **same OTC network**.

Key principles:
- **Same rules as other brokers**: The platform-operated broker is credentialed and behaves like any other broker (KYC, suitability, recordkeeping, counterparty-of-record).
- **No bypass**: Investors still trade via a broker. This simply adds an additional broker participant to the network.
- **Jurisdiction compatibility**: Sails.to only onboards and serves clients directly where that broker entity is legally permitted to do so; elsewhere, clients route through locally licensed brokers.

### 1.3 The "Broker Hop"

When an investor wants to buy a security:

1. Investor requests a quote from their broker
2. Broker sources liquidity (internal inventory, another broker, or issuer treasury)
3. Broker executes the trade as principal
4. Broker allocates the security to the client's wallet

On-chain, this appears as:
- **Broker A → Broker B** (inter-dealer settlement)
- **Broker B → Client** (client allocation)

The client never transacts directly with the market. This preserves exemption integrity, professional-investor restrictions, and clear audit trails.

---

## Part 2: The Credential System

Sails.to uses a hierarchical system of **non-transferable, revocable, renewable credential tokens** (soulbound NFTs) to control access and permissions.

### 2.1 The Trust Hierarchy

```
Platform Operator (Sails.to)
│
├── Licensed Brokers
│   └── Broker Clients (Investors)
│
└── Licensed Issuers
    └── Issuer-Approved Investors (partners, co-investors)
```

Each role receives a credential from the authority above it. No credential, no access.

**Note**: The Sails.to group may also operate a licensed broker entity. In that case, it appears in the system as **one of the Licensed Brokers** (with its own broker credential), separate from the platform operator role.

### 2.2 Platform License NFT

**Issued by**: Platform Operator  
**Held by**: Broker or Issuer entity wallet

**Represents**: "This entity is authorized to operate on Sails.to"

**Properties**:
- Non-transferable (soulbound)
- Revocable (immediate effect)
- Renewable (annual or biannual)
- Contains: jurisdiction(s), license scope, validity period, regulatory references

**Without this credential**:
- No OTC network participation
- No KYC credential issuance authority
- No access to platform smart contracts

### 2.3 Broker License NFT

**Issued by**: Platform Operator  
**Held by**: Broker entity wallet

**Represents**: "This broker is licensed and in good standing"

**Contains**:
- Jurisdiction(s) of operation
- Permitted activities (execution, custody, KYC issuance)
- Renewal/expiry date
- Regulatory license references

**Gates access to**:
- All broker-side OTC actions
- KYC credential issuance to clients
- Broker pool creation and management

### 2.4 Issuer License NFT

**Issued by**: Platform Operator  
**Held by**: Issuer entity wallet

**Represents**: "This issuer is authorized to issue securities on the platform"

**Contains**:
- Allowed exemptions (Reg D, Reg S, EU exemptions)
- Allowed investor categories
- Corporate action authority
- Jurisdiction constraints

**Gates access to**:
- Security token series creation
- Issuance execution
- Corporate actions (coupons, redemptions)
- KYC credential issuance (for known investors/partners)

### 2.5 KYC Credential Token

**Issued by**: Licensed Broker or Licensed Issuer  
**Held by**: Investor identity wallet

**Represents**: "This identity has passed KYC/AML and is eligible for certain securities"

**Contains**:
- Investor classification (professional, accredited, qualified purchaser, etc.)
- Jurisdiction/residency (anonymized—no PII on-chain)
- Issuing authority (which broker/issuer performed KYC)
- Expiry date
- Optional: risk category flags, specific exemption eligibility

**Critical design points**:

1. **Not a global identity**: KYC credentials are trust assertions produced by licensed entities, not universal IDs. Different brokers may issue different credentials to the same investor.

2. **Third-party recognition**: Brokers and issuers may choose to recognize third-party KYC tokens. If a broker trusts another licensed entity's KYC process, they can accept that credential without re-performing verification. This enables:
   - Investor portability between brokers
   - Reduced friction for multi-broker investors
   - Interoperability with external compliant KYC providers

3. **Issuer-specific acceptance**: Each issuance can specify which KYC credential issuers are acceptable for that series.

### 2.6 Wallet Linking and Cold Storage

Investors often want to use hardware wallets, multiple addresses, or rotate keys. Sails.to separates **identity** from **wallet**:

- Each investor has a verified **identity record**
- Multiple **wallets can be linked** to that identity
- Transfers are permitted to any wallet linked to an eligible identity

This enables:
- Hot wallet for active trading
- Cold storage (Ledger, Trezor) for safekeeping
- Custody wallets (broker or institutional)
- Key rotation without losing access or eligibility

**The rule**: A security may only be held by a wallet linked to an eligible identity (or an authorized custodian). Wallet mobility is unrestricted; ownership eligibility is enforced.

---

## Part 3: Legal Structures and Entity Services

### 3.1 DAO LLC Options

Sails.to offers near-instant legal entity setup through two DAO LLC jurisdictions:

**Wyoming Series LLC DAO**
- US-based structure
- Series segregation (assets/liabilities isolated per issuance)
- DAO-friendly statutory framework
- Clear mapping: one Series = one issuance = one security token
- Suitable for Reg D offerings and US-focused structures

**Marshall Islands DAO LLC**
- Offshore structure
- International investor base
- Favorable for Reg S and non-US focused offerings
- DAO governance recognition
- Tax-neutral jurisdiction

### 3.2 Structure Mechanics

Each DAO LLC operates as:
- One master LLC operator (can operate multiple LLCs for different industries/asset classes)
- Each issuance is a **Series** within the LLC
- Each Series:
  - Raises capital from investors
  - Makes a **loan** to an underlying asset/project/borrower
  - Holds collateral (pledges, security interests)
  - Issues a **debt instrument** (loan note / participation)

### 3.3 Issuer Options

Issuers can:
1. **Use their own corporate structure**: Bring an existing entity and issue through it
2. **Use Sails.to DAO LLC service**: Near-instant Wyoming or Marshall Islands Series setup with standardized legal templates

The DAO LLC service provides:
- Pre-drafted operating agreements
- Standardized loan documentation templates
- Pledge and security agreement frameworks
- Offering document templates (PPM/OM)
- Ongoing compliance support

---

## Part 4: The Issuance Model

### 4.1 The Security Instrument

Each security token represents:
- A fractional participation in the Series' loan receivables
- Rights to interest (coupons) and principal repayment
- As defined in offering documents and operating agreements

**Standard parameters**:
- **Denomination**: Minimum 200,000 units (indivisible)—appropriate economic threshold for professional investors
- **Exemption**: Reg D (US accredited), Reg S (non-US), or other applicable exemptions
- **Investor class**: Professional investors only

### 4.2 Three-Phase Issuance: Phase A → Phase B → Phase C

Every issuance has:
- **Soft cap**: Minimum raise required for the deal to proceed
- **Hard cap**: Maximum raise accepted
- **Issuance duration**: Time window for the offering

The issuance progresses through three distinct phases. The **same security token** exists throughout; only its permissions change (see 4.3).

---

#### Phase A: Subscription (Pre-Soft Cap)

**Status**: Deal may or may not close

**Mechanics**:
- Investor funds go into **escrow** (legally segregated)
- No funds released to issuer/borrower
- No fees charged
- Security tokens may be minted immediately but are **non-transferable** and **refundable** in this phase

**Early Bird Incentive**: Issuers may offer a **discounted subscription price** (e.g., 5% discount) for Phase A subscribers.

**If soft cap is NOT reached by deadline**:
- Escrow refunds 100% to all investors
- Tokens are burned/invalidated
- No fees charged
- Series is canceled or relaunched

---

#### Phase B: Committed (Post-Soft Cap)

**Status**: Deal WILL close—soft cap reached, closure is certain

**Mechanics**:
- Refunds are disabled
- Escrow continues to accept subscriptions
- Funds remain locked until closing
- Tokens remain **non-transferable**

**Critical restriction**: During this phase, **only the issuer and licensed brokers may allocate/sell**. Secondary trading among investors is not permitted until Phase C.

**This phase continues until**:
- Hard cap is reached, OR
- Issuance duration expires

---

#### Phase C: Active (Closing and Activation)

**Status**: Issuance complete, securities become live

**Trigger**: Hard cap reached OR issuance duration ends (whichever comes first, after soft cap was reached)

**Closing checklist**:
1. ☐ All KYC completed for allocations
2. ☐ Offering documents executed
3. ☐ Loan agreement signed
4. ☐ Collateral/pledges perfected
5. ☐ Payment confirmations received

**Upon closing**:
- Escrow releases funds to Series
- Loan originates to underlying borrower
- Tokens become transferable **via broker-mediated OTC**
- Issuance fees are charged and distributed
- Secondary trading enabled on OTC network

---

### 4.3 Token Model: Single Token, Three Permission Phases

Rather than separate "subscription receipt" and "security" tokens, Sails.to uses a **single security token** whose permissions change based on the series phase. The token identity remains constant from subscription through maturity.

| Attribute | Phase A (Subscription) | Phase B (Committed) | Phase C (Active) |
|-----------|------------------------|---------------------|------------------|
| Status | Pre-soft-cap | Post-soft-cap | Closed |
| Refundable | ✅ Yes | ❌ No | ❌ No |
| Transferable | ❌ No | ❌ No | ✅ Yes (via OTC) |
| Who can allocate | Issuer + Brokers | Issuer + Brokers | Anyone (via broker) |
| Price tier | Discounted (optional) | Standard | Market |
| Escrow status | Locked | Locked | Released |

**Phase transitions are one-way and irreversible:**
- **A → B**: Triggered when soft cap is reached
- **B → C**: Triggered when closing conditions are met

**Why single-token is superior:**
- **Stable identity**: Investor sees "I own X units of Series Y" from subscription day
- **No conversion event**: Permissions change, not the token itself
- **Cleaner audit trail**: Same token ID tracked throughout entire lifecycle
- **Simpler contracts**: No burn/mint/swap logic at closing
- **Refund mechanics**: In Phase A, refund burns the token and returns escrowed funds

---

## Part 5: The OTC Network

### 5.1 Network Architecture

The Sails.to OTC network is:
- A **multi-broker dealer network**
- With **on-chain settlement**
- And **shared liquidity signaling**
- Operating across supported chains (Solana, TON)

The network can include both:
- **Third-party licensed brokers**
- A **platform-operated licensed broker entity** (where jurisdictionally compatible)

It is **not**:
- A public DEX
- An anonymous order book
- A permissionless AMM

### 5.2 Broker Pools

Each broker can create **OTC pools** for securities they make markets in.

Sails.to's platform-operated broker entity (when used) can also create pools. These pools are treated identically to any other broker pool: same licensing checks, same RFQ routing, and the same fee split.

A broker pool represents:
- A **dealer quote surface** (bid/ask, size, settlement terms)
- A **liquidity commitment** (inventory or access to inventory)
- A **routing endpoint** for RFQs (request-for-quote)
- **Jurisdictional scope** (which investor types can be served)

Think of it as: "This broker is willing to buy/sell security X at price Y for eligible counterparties meeting criteria Z."

### 5.3 Trading Flow

**Step 1**: Investor contacts their broker requesting a quote (RFQ) (either a third-party broker, or the platform-operated broker where permitted)

**Step 2**: Broker sources liquidity:
- Internal inventory
- Other brokers via network
- Issuer treasury (if applicable)

**Step 3**: Broker returns quote to investor

**Step 4**: If accepted, broker executes:
- Broker-to-broker settlement (if sourcing externally)
- Broker-to-client allocation

**Step 5**: Settlement occurs on-chain with full audit trail

### 5.4 Automation Boundaries

**Safe to automate**:
- Quote publication and updates
- Inventory availability broadcasting
- RFQ routing between brokers
- Broker-to-broker settlement execution
- Best-execution routing across broker pools
- Compliance attestation verification

**Must NOT automate**:
- Client execution without broker approval
- Anonymous matching
- Direct client access to liquidity pools
- Wallet-level routing that bypasses broker intermediation

The broker must remain in the execution path for regulatory compliance.

### 5.5 Issuer Treasury as Liquidity Source

Issuers can post their own securities to the OTC network during Phase C (Active):

- **Treasury Pool**: Issuer creates a visible liquidity pool for their securities
- **Accessible to all brokers**: Any licensed broker can source from issuer treasury
- **Broker intermediation preserved**: Clients never transact directly with issuer
- **Standard OTC routing**: Orders flow through the same infrastructure as inter-broker trades

When Investor X (client of Broker A) clicks "buy" on a security, Broker A can source from:
1. Internal inventory
2. Another broker's inventory  
3. **Issuer's treasury pool**

The issuer is just another liquidity source—no special handling required.

### 5.6 Multi-Broker Fee Split: ⅓ Each

The 0.5% trading fee splits three ways:

| Recipient | Share |
|-----------|-------|
| Platform | ⅓ (~0.167%) |
| Buy-side broker(s) | ⅓ (~0.167%) |
| Sell-side broker(s) | ⅓ (~0.167%) |

*Platform receives any rounding remainder.*

**Single broker (internal match)**:
- Broker handles both sides → keeps ⅔ (buy + sell portions)
- Platform keeps ⅓

**Two brokers**:
- Platform: ⅓
- Buy-side broker: ⅓
- Sell-side broker: ⅓

**Multiple brokers per side**:
- Each side's ⅓ splits proportionally among participating brokers

**Example: Client buys €200,000 via two brokers**

| Party | Amount |
|-------|--------|
| Client pays | €201,000 (0.5% fee) |
| Platform | €333.34 (⅓) |
| Broker A (buy-side) | €333.33 (⅓) |
| Broker B (sell-side) | €333.33 (⅓) |

**Why ⅓ split works:**
- All three parties equally incentivized
- Platform, buyers, and sellers all valued equally
- Simple, fair, predictable
- Encourages network cooperation

### 5.7 Atomic Settlement (DvP)

All OTC trades settle via **atomic Delivery-vs-Payment**—asset delivery and payment occur together or not at all.

**Riskless Principal Model**

Every broker-mediated trade is legally structured as simultaneous principal transactions. The atomic execution collapses all legs into a single instant, eliminating settlement risk.

**Atomic Instruction Set**

```
PRECONDITIONS (all must be true):
  ✓ Buyer payment authorized
  ✓ Seller has tokens available
  ✓ All brokers hold valid licenses
  ✓ Buyer identity has valid KYC for this series
  ✓ Receiving wallet linked to eligible identity

ATOMIC EXECUTION:
  1. Debit buyer's stablecoin account
   2. Credit platform fee (⅓; includes rounding remainder)
   3. Credit buy-side broker(s) (⅓)
   4. Credit sell-side participant(s) (⅓)
  5. Credit seller (net proceeds)
  6. Transfer token: Seller → Buyer wallet
  
ROLLBACK: If any step fails, entire transaction reverts
```

**Jurisdiction Compatibility**

| Requirement | How Satisfied |
|-------------|---------------|
| DvP Settlement | Atomic swap ensures asset moves iff payment moves |
| Settlement Finality | Blockchain consensus provides irrevocable finality |
| Principal Trading | Broker momentarily holds asset (riskless principal) |
| Client Segregation | Client never directly faces market or issuer |
| Audit Trail | On-chain events provide immutable settlement proof |

All settlements emit structured events for reconciliation, audit, and regulatory reporting.

---

## Part 6: Hybrid Finance Layer

### 6.1 Global Settlement via Clearstream + Vienna MTF

Sails.to enables global accessibility for professional investors through a two-layer approach:

1. **Clearstream/Euroclear eligibility** — The foundation for global executability
2. **Vienna MTF listing (QI Segment)** — Optional "listed" status for mandate compliance

**Why this architecture?**

Bonds trade OTC regardless of listing status. As Vienna Stock Exchange notes: "almost all trading in debt securities takes place Over The Counter (OTC)." What makes a security "globally executable" is settlement infrastructure, not the exchange logo.

- **Euroclear**: "Your gateway to counterparties worldwide" — 2,000+ financial institutions in 90+ countries
- **Clearstream ICSD**: Settles Eurobonds for "primary and secondary market activities, both for OTC and trading venues' flows"

An XS ISIN + Clearstream eligibility means any private bank with ICSD connectivity can execute OTC trades and settle. No listing required for trading.

### 6.2 Cost and Timeline (Verified)

| Component | Cost | Timeline | Source |
|-----------|------|----------|--------|
| **XS ISIN allocation** | €100 | 1-2 days | Clearstream fee schedule |
| **ICSD admission (new issuer)** | €2,500 | ~1 week | Clearstream fee schedule |
| **Vienna MTF admission fee** | €700 | — | Wiener Börse fee schedule |
| **Vienna MTF listing fee** | €800-2,000 | 2-5 days | Wiener Börse fee schedule |
| **Vienna MTF annual fee** | €150-200 | — | Wiener Börse fee schedule |

**Total setup**: ~€3,500-5,500  
**Timeline**: ~1-2 weeks (can be as fast as 2 days for Vienna review)

No listing agent required for Vienna MTF. The exchange reviews documentation directly.

### 6.3 Settlement Architecture

**Direction of truth**:
- **Canonical security**: The blockchain token (Solana or TON) is the source of truth
- **Off-chain instrument**: A representation backed by immobilized on-chain tokens, settled via Clearstream

Off-chain investors hold a claim against a depositary/custodian SPV whose sole asset is locked blockchain tokens. They do not hold blockchain tokens directly.

**Global reach via ICSD links**:
- Europe: Direct Clearstream/Euroclear access
- Asia: Clearstream links to Hong Kong CMU, Singapore CDP, Japan JASDEC
- Americas: Clearstream-DTC bridge for eligible instruments
- Middle East/Africa: Via correspondent banks with ICSD accounts

### 6.4 Wrap Flow (Blockchain → Clearstream/Vienna)

1. Investor requests wrap through their broker
2. Investor's tokens transfer to **custody/lockbox wallet**
3. Tokens are **locked** (not burned)
4. Depositary issues Clearstream-eligible instrument (XS ISIN)
5. Instrument admitted to Vienna MTF QI Segment
6. Investor receives instrument in their brokerage account (settles via Clearstream)

**Invariant**: Clearstream outstanding ≤ blockchain tokens locked in custody

### 6.5 Unwrap Flow (Clearstream/Vienna → Blockchain)

1. Investor requests unwrap through their broker
2. Clearstream instrument is delivered to depositary and canceled
3. Depositary releases locked blockchain tokens
4. Tokens transfer to investor's registered wallet

### 6.6 Corporate Actions Synchronization

Because the blockchain token is canonical:
- All corporate actions originate on-chain
- Clearstream/Vienna holders receive pass-through economics via depositary
- **Conversion blackout windows** around record dates prevent double-counting or arbitrage

### 6.7 Vienna MTF QI Segment

Vienna's Qualified Investor (QI) Segment is purpose-built for professional-only securities:
- Trading only permitted "for or on behalf of qualified investors"
- No retail distribution
- No additional cost beyond standard fees
- Same fast timeline (~2 days review, listing within 2 days of final docs)

This aligns perfectly with Sails.to's professional-investor-only model.

### 6.8 Why Not Other Venues?

| Venue | Cost | Access | Notes |
|-------|------|--------|-------|
| **Vienna MTF** | ~€3k | OTC via Clearstream | Cheapest, fastest, no listing agent |
| **TISE (Guernsey)** | ~£8k | OTC via Clearstream | Fast, but requires listing agent |
| **BSX (Bermuda)** | ~$4.5k | Limited | No IB/Saxo access, SEC offshore market status |
| **No listing** | ~€2.6k | OTC via Clearstream | Works, but some mandates require "listed" checkbox |

### 6.9 Use Cases

The hybrid layer enables:
- **Global execution**: Any private bank with Clearstream access can buy/settle
- **Mandate compliance**: "Listed" checkbox satisfied via Vienna MTF
- **Institutional access**: Banks and funds that require ICSD settlement
- **Seamless conversion**: Movement between on-chain and off-chain forms
- **Single source of truth**: Blockchain canonical regardless of holding venue

---

## Part 7: Fee Model

### 7.1 Issuance Fees (Primary Origination)

**Standard Issuance**: 6% total
- Charged once, at closing
- Paid by issuer (deducted from proceeds)
- Applies to broker-distributed offerings

**Strategic Issuance**: 1% total
- Applies when issuing only to:
  - Platform partners
  - Co-investors
  - Pre-identified strategic investors
  - No broker-led distribution

**Integration with soft-cap mechanics**:
- If soft cap not reached: **Issuance fee = 0**
- Fees are contingent—not earned until closing occurs

**Standard split (configurable per deal)**:

| Recipient | Standard (6%) | Strategic (1%) |
|-----------|---------------|----------------|
| Platform | 2.0% | 0.75% |
| Brokers/Placement | 3.0% | — |
| Admin/Legal Reserve | 1.0% | 0.25% |

### 7.2 Trading Fees (Secondary OTC)

**Fee**: 0.5% per trade

**Applies to**:
- Broker-mediated secondary trades on OTC network (Phase C)
- Issuer treasury sales via OTC

**Does NOT apply to**:
- Initial issuance subscriptions (Phase A/B)
- Wrap/unwrap conversions

**Fee base**: Notional value of trade

**Split**: ⅓ each

| Recipient | Share |
|-----------|-------|
| Platform | ⅓ (~0.167%) |
| Buy-side broker(s) | ⅓ (~0.167%) |
| Sell-side broker(s) | ⅓ (~0.167%) |

*Platform receives any rounding remainder.*

| Scenario | Platform | Buy-Side | Sell-Side |
|----------|----------|----------|------------|
| Two brokers | ⅓ | ⅓ | ⅓ |
| Single broker (internal) | ⅓ | ⅔ (both sides) | — |
| Multiple per side | ⅓ | Split ⅓ | Split ⅓ |

**Who pays**: Buyer (single-sided)—matches OTC market convention

**Why ⅓ split works**:
- Platform, buy-side, and sell-side equally valued
- All parties always incentivized to participate
- Simple, fair, predictable
- Encourages deal-sharing across the network

**Variants**:
- **Issuer treasury sales**: Same split; issuer is sell-side, broker is buy-side
- **Issuer-sponsored liquidity programs**: Platform may rebate portion to issuer

### 7.3 Conversion Fees (Blockchain ↔ Off-Chain)

Conversion is **asset servicing**, not trading.

**Structure**:
- 0.10% – 0.25% of notional
- Capped at €25,000 (or equivalent)
- Paid by requesting party

**Split**:

| Recipient | Percentage |
|-----------|------------|
| Platform | 70% |
| Depositary/Custodian | 30% |

**No double-charging**: A single economic action (e.g., buy then convert) pays trade fee once and conversion fee once—never stacked.

### 7.4 License and Platform Fees

**Broker License**:
- Annual or biannual subscription
- €25,000 – €150,000 (depending on jurisdiction and scope)
- Covers: network access, compliance tooling, support, upgrades

**Issuer License**:
- Lower flat fee, OR
- Bundled into issuance fee

**Optional service fees**:
- Enhanced reporting and analytics
- Custodial workflow integration
- Compliance vendor integrations
- White-label deployments
- DAO LLC formation and maintenance

---

## Part 8: Smart Contract Architecture

### 8.1 Platform Governance Contract

**Purpose**: Root authority for the platform

**Functions**:
- Define platform authorities (multisig/DAO)
- Control upgrades and global parameters
- Set fee schedules and credential types
- Emergency pause/unpause all or specific functions

### 8.2 License Registry Contract

**Purpose**: Canonical registry of all licensed entities

**Functions**:
- Map entity IDs to credential token accounts
- Query: "Is broker X licensed?", "Is issuer Y authorized?"
- Track status (active/suspended/revoked/expired)
- Cross-chain status synchronization

This registry treats the platform-operated broker entity (when present) as just another broker entry, with its own entity ID and broker credential.

### 8.3 Broker License NFT Contract

**Purpose**: Issue and manage broker credentials

**Enforces**:
- Non-transferability (soulbound)
- Expiration dates with automatic privilege loss
- Revocation with immediate effect
- Renewal (metadata update, not remint)

This includes credentials for any platform-operated broker entity, which must be segregated from the platform operator role.

### 8.4 Issuer License NFT Contract

**Purpose**: Issue and manage issuer credentials

Same mechanics as broker license, scoped to issuer permissions.

### 8.5 Identity Registry & Wallet-Link Contract

**Purpose**: Map legal identities to wallet addresses

**Functions**:
- Link multiple wallets to one identity
- Add/remove wallets (with proper authorization)
- Support key rotation
- Register custody wallets
- Maintain audit logs of all changes

**Authorization**: Requires investor signature + broker/platform co-sign

### 8.6 KYC Credential Contract

**Purpose**: Issue investor eligibility credentials

**Properties**:
- Minted only by licensed brokers/issuers
- Contains: eligibility claims, expiry, issuing authority
- Non-transferable
- Revocable

**Third-party recognition**: Contracts can be configured to accept credentials from specified external issuers.

### 8.7 Series Factory Contract

**Purpose**: Create new issuance series

**Creates**:
- Series ID and metadata
- Security token mint parameters
- Offering parameters (soft cap, hard cap, duration, early-bird discount rate)
- Approved KYC credential issuers for this series
- Fee configuration

### 8.8 Subscription Escrow Contract

**Purpose**: Hold investor funds through the issuance lifecycle

**Functions**:
- Receive subscription payments (stablecoin or fiat-attestation)
- Track subscription amounts, timing, and applicable pricing tier
- Enforce: no release until closing conditions met
- Execute refund if soft cap fails
- Coordinate Phase A → Phase B → Phase C transitions (via Series Phase Manager)
- Support token minting at subscription time and permission changes at phase transitions

### 8.9 Series Phase Manager Contract

**Purpose**: Manage phase transitions and phase-dependent permissions

**Functions**:
- Track current phase for each series (A → B → C)
- Enforce phase transition rules (soft cap triggers A→B, closing triggers B→C)
- Gate token permissions based on current phase
- Process refund requests (Phase A only)
- Coordinate with Escrow Contract on phase changes

### 8.10 Security Token Contract

**Purpose**: The security instrument with phase-dependent permissions

**Enforces**:
- **Phase-based transfer rules**: Queries Series Phase Manager
  - Phase A/B: Only issuer and licensed brokers can allocate
  - Phase C: Full OTC trading among eligible holders
- Transfer restrictions (only to eligible wallets)
- Wallet must be linked to identity with valid KYC credential
- Denomination rules (e.g., indivisible 200k units)
- Lock flags for custody/wrapping
- Special roles for issuer/broker/custodian operations

**Compliance hooks**: Custom logic executes on every transfer to verify eligibility and phase permissions.

### 8.11 OTC Trading Contracts

**A. Quote/RFQ Registry**
- Brokers post indicative quotes
- Respond to RFQ requests
- Price discovery layer

**B. Trade Execution Contract**
- Execute broker-mediated atomic DvP settlements
- Verify all parties hold valid credentials
- Enforce phase permissions (Phase C required)
- Calculate fees: ⅓ platform, ⅓ buy-side, ⅓ sell-side
- Platform receives rounding remainder
- Support multi-broker chains
- Emit audit events

**C. Broker Pool Registry**
- Track which brokers are active for which series
- Activity metrics and compliance status
- Cross-broker liquidity aggregation

**D. Issuer Treasury Pool Contract**
- Issuers register treasury inventory for OTC sale (Phase C)
- Visible to all licensed brokers
- Issuer acts as sell-side participant (receives sell-side ⅓ when applicable)
- Integrates with Trade Execution Contract for atomic settlement

### 8.12 Fee Splitter Contract

**Purpose**: Deterministic fee distribution

**Functions**:
- Issuance fee distribution at close
- Trade fee splitting (⅓ platform, ⅓ buy-side, ⅓ sell-side; rounding remainder to platform)
- Conversion fee splitting (platform/depositary)
- Transparent, auditable, immutable per series

### 8.13 Conversion Lockbox Contract

**Purpose**: Custody for blockchain → off-chain wrapping

**Functions**:
- Receive and lock security tokens
- Emit conversion receipts for off-chain operators
- Release tokens only on validated redemption
- Reconciliation queries and proofs

### 8.14 Corporate Actions Contract

**Purpose**: Execute lifecycle events

**Functions**:
- Schedule and execute coupon payments
- Process principal repayments
- Handle redemptions and calls
- Manage restructurings (if applicable)

**Integrates with**:
- KYC credential checks (who can receive payments)
- Record-date logic
- Conversion blackout window enforcement

### 8.15 Audit/Event Anchoring Contract

**Purpose**: Immutable proof of off-chain artifacts

**Functions**:
- Anchor document hashes (offering docs, agreements, notices)
- Timestamp proofs ("this document existed at time T")
- Support regulatory and audit queries

---

## Part 9: Operational Procedures

### 9.1 Broker Onboarding

1. Broker applies with regulatory credentials and due diligence materials
2. Platform governance reviews and approves
3. Platform issues **Broker License NFT**
4. Broker deploys Melusina OS instance (or uses hosted option)
5. Broker gains access to:
   - OTC network contracts
   - KYC credential issuance
   - Broker pool creation tools
   - Investor management dashboard

**Platform-operated broker**: When Sails.to operates its own licensed broker entity, it is onboarded using the same controls (entity due diligence, broker credential issuance, operational segregation) and then participates in OTC routing as just another broker.

### 9.2 Issuer Onboarding

1. Issuer applies with:
   - Legal structure documentation (or request for DAO LLC service)
   - Compliance readiness evidence
   - Business/asset information
2. Platform governance reviews and approves
3. Platform issues **Issuer License NFT**
4. Issuer either:
   - Deploys own Melusina OS instance, OR
   - Uses platform DAO LLC service (Wyoming or Marshall Islands)
5. Issuer can now create Series

### 9.3 Investor Onboarding

1. Investor approaches a **licensed broker** (including the platform-operated broker where permitted) (or issuer for partner allocations)
2. Broker performs:
   - KYC/AML verification
   - Investor classification (professional, accredited, etc.)
   - Suitability assessment
3. Broker issues **KYC Credential Token** to investor identity
4. Investor links wallets (hot, cold, custody) to their identity
5. Investor can participate in eligible offerings and secondary trading

**Alternative**: If investor already holds a recognized third-party KYC credential, broker may accept it without re-verification (at broker's discretion per their compliance policy).

### 9.4 Issuance Execution (Full Cycle)

**Setup Phase**
1. Issuer creates Series via Series Factory
2. Defines terms:
   - Soft cap / hard cap
   - Issuance duration
   - Early-bird discount (optional; Phase A only)
   - Coupon schedule
   - Collateral/pledge structure
3. Legal documents finalized and anchored
4. Series deployed on-chain (starts in **Phase A**)

**Phase A: Subscription (Pre-Soft Cap)**
1. Broker network distributes offering to eligible investors
2. Investors subscribe; funds flow to Escrow Contract
3. Tokens may be minted immediately with Phase A permissions (non-transferable, refundable)
4. Monitor progress toward soft cap

**Outcome A: Soft cap NOT reached**
- Escrow refunds all investors
- Tokens burned/invalidated
- No fees charged
- Series canceled or relaunched

**Outcome B: Soft cap reached → Phase B**
- Automatic transition to Phase B
- Refunds disabled; tokens remain non-transferable

**Phase B: Committed (Post-Soft Cap)**
1. Deal closure is now guaranteed
2. New subscriptions continue at standard price
3. Funds remain in escrow
4. Only issuer/brokers may allocate (no investor-to-investor trading)
5. Continue until hard cap OR duration expires

**Phase C: Closing → Active**
1. Closing conditions verified
2. Escrow releases funds to Series
3. Loan originates to underlying borrower
4. Tokens become transferable via OTC (Phase C permissions)
5. Issuance fee charged and distributed

**Active Phase**
- Secondary trading enabled
- Issuer treasury may list inventory for OTC sale
- Conversion to off-chain representation available

**Servicing Phase**
- Coupons paid per schedule via Corporate Actions Contract
- Distributions to eligible holders (KYC-verified)
- Investor communications via issuer portal
- Periodic reporting published and anchored

**Maturity**
- Principal repaid
- Final distribution to holders
- Tokens redeemed/burned or marked settled
- Series enters archive state with full documentation retained

### 9.5 Secondary Trading (Full Cycle)

**Two-Broker Trade**
1. **Investor A** wants to sell → contacts Broker A (sell-side)
2. **Broker A** posts to OTC network
3. **Broker B** (buy-side, representing Investor B) sees opportunity
4. Trade executes via atomic settlement:
   - Investor B pays €201,000 (0.5% on €200k)
   - Platform: €333.34 (⅓)
   - Broker B (buy-side): €333.33 (⅓)
   - Broker A (sell-side): €333.33 (⅓)
   - Investor A receives: €200,000
   - Token transfers: Investor A → Investor B
5. Audit events emitted

**Single-Broker Internal Match**
1. **Broker C** has both a buyer and seller among their clients
2. Broker C executes internal match:
   - Buyer pays 0.5% fee
   - Platform: ⅓
   - Broker C: ⅔ (handles both buy + sell sides)
3. Same atomic settlement, same audit trail

**Issuer Treasury Sale**
1. **Investor D** (client of Broker D) wants to buy
2. **Broker D** sources from issuer's Treasury Pool
3. Atomic settlement:
   - Investor D pays retail price
   - Platform: ⅓
   - Broker D (buy-side): ⅓
   - Issuer (sell-side): ⅓
   - Token transfers: Issuer Treasury → Investor D
4. Broker intermediation preserved throughout

### 9.6 Conversion Flow (Blockchain → Clearstream/Vienna)

1. Investor requests wrap via broker
2. Broker initiates Lockbox Contract deposit
3. Investor's tokens transfer to lockbox
4. Lockbox emits conversion receipt
5. Off-chain depositary process:
   - Validates receipt
   - Issues Clearstream-eligible instrument (XS ISIN)
   - Admits to Vienna MTF QI Segment (if not already)
   - Settles to investor's account via Clearstream
6. Conversion fee charged

### 9.7 Conversion Flow (Clearstream/Vienna → Blockchain)

1. Investor requests unwrap via their broker
2. Clearstream instrument delivered to depositary
3. Depositary cancels/redeems instrument
4. Depositary signals Lockbox Contract
5. Lockbox releases tokens to investor's registered wallet
6. Conversion fee charged

---

## Part 10: Risk Controls and Governance

### 10.1 Platform Governance

- **Multisig control** for all critical operations
- **Separation of duties**: distinct authorities for license management, market operations, and contract upgrades
- **Timelocks** on sensitive parameter changes
- **Emergency pause** capability:
  - All trading
  - Specific series
  - Conversions
  - New issuances

### 10.2 Reconciliation

**Daily reconciliation requirements**:
- Lockbox balance vs. off-chain representation outstanding
- Escrow balances vs. subscription records
- Fee accruals vs. distributions
- Cross-chain state consistency

**Tri-party reconciliation**: Platform ↔ Custodian ↔ External auditors

### 10.3 Credential Lifecycle Management

All credentials support:
- **Expiry**: Automatic privilege loss when validity ends
- **Revocation**: Immediate effect (sanctions, violations, status changes)
- **Public status queries**: Any contract can verify "is this credential valid right now?"
- **Renewal**: Metadata update extends validity without reminting

### 10.4 Audit Trail Requirements

Platform retains:
- Complete KYC records: who verified whom, when, under what policy
- All terms disclosed to each investor
- Full trade and settlement history
- All corporate action distributions
- All investor communications and notices
- Document anchoring proofs

All data exportable for regulatory and broker audits.

---

## Part 11: Business Model Summary

### 11.1 Value Proposition for Issuers

**They receive**:
- Fast, programmable issuance with soft/hard cap mechanics
- Early-bird pricing tools to incentivize subscription
- Compliance-ready investor onboarding via broker network
- Path to secondary liquidity from day one
- Lifecycle management and corporate actions tooling
- Optional bridging to traditional finance venues
- DAO LLC service (Wyoming or Marshall Islands) for instant legal structure

**They pay**:
- Issuance fee (6% standard / 1% strategic)—only on successful close
- Optional platform subscriptions for enhanced services
- DAO LLC formation and maintenance fees (if using platform service)

### 11.2 Value Proposition for Brokers

**They receive**:
- New product inventory (tokenized private credit, structured products)
- Integrated KYC management with third-party credential recognition
- OTC network access with multi-broker liquidity
- Transaction fee revenue (⅓ of the 0.5% trade fee when representing a side; ⅔ when internalizing both sides)
- Placement fees on primary distribution (from issuer fee pool)
- Multi-chain flexibility (Solana, TON)

**They pay**:
- License fees (annual/biannual)
- Operational compliance obligations

### 11.3 Value Proposition for Investors

**They receive**:
- Access to private credit deals typically unavailable to them
- Early-bird discounts for early commitment
- Better settlement efficiency than paper-based alternatives
- Transparent lifecycle data and reporting
- Cold storage and hardware wallet support
- Optional conversion to MTF-held instruments
- Credential portability (third-party KYC recognition)

**They pay**:
- Trading fees (embedded in OTC execution)
- Conversion fees (if wrapping/unwrapping)

### 11.4 Platform Revenue Streams

1. **Issuance fees**: 2% of successful raises (from 6% total)
2. **Trading fees**: ⅓ of 0.5% secondary volume (~0.167%)
3. **Conversion fees**: 70% of conversion fee revenue
4. **License subscriptions**: Annual broker and issuer fees
5. **Service fees**: DAO LLC formation, enhanced tooling, white-label

**Optional (when acting as a broker)**: The Sails.to group may also earn the broker-side portion(s) of the trading fee (⅓ per represented side; ⅔ when internalizing both sides) for order flow it executes via its own licensed broker entity.

### 11.5 Platform Defensibility

The competitive moat is the integrated stack:

- **Network effects**: More brokers → better liquidity → more issuers → more investors
- **Credential infrastructure**: Trusted hierarchy with third-party recognition
- **Multi-chain architecture**: Flexibility for diverse issuer/investor preferences
- **Compliance tooling**: Self-hosted KYC, transfer restrictions, audit trails
- **Hybrid finance rails**: Unique on-chain ↔ off-chain conversion capability
- **Legal structure services**: Instant Wyoming/Marshall Islands DAO LLC
- **Operational environment**: Melusina OS with isolated deployments and shared app store

---

## Part 12: Complete Example

**"Alpine Credit Series 2026-A"** — A Tokenized Loan Participation

### Setup

- Issuer: Alpine Capital Partners
- Structure: Marshall Islands DAO LLC via Sails.to service
- Underlying: Secured loan to Alpine Holdings for equipment financing
- Chain: Solana

### Terms

| Parameter | Value |
|-----------|-------|
| Soft Cap | €5,000,000 |
| Hard Cap | €15,000,000 |
| Denomination | €200,000 minimum |
| Early-Bird Discount | 5% (Phase A only) |
| Coupon | 8.5% annual, paid quarterly |
| Maturity | 36 months |
| Collateral | First-priority security interest in financed equipment |
| Exemption | Reg S + Reg D |

### Phase A: Pre-Soft Cap (Subscription)

- Series deployed, enters **Phase A**
- 3 licensed brokers distribute to eligible professional investors
- Early subscribers pay €190,000 per unit (5% discount)
- Security tokens minted immediately (Phase A: refundable, non-transferable)
- €4.2M subscribed in first 3 weeks
- 1 investor requests refund (€200k)—token burned, funds returned
- Net: €4.0M committed
- Soft cap not yet reached; investors can still withdraw

### Soft Cap Reached (Week 4) → Phase B

- Total subscriptions hit €5.1M
- **Automatic transition: Phase A → Phase B**
- All tokens update to Phase B permissions (no longer refundable)
- Deal closure now guaranteed

### Phase B: Post-Soft Cap (Committed)

- New subscribers pay standard €200,000 per unit
- Additional €2.1M subscribed over next 2 weeks
- Total: €7.2M
- Issuance duration expires; closing triggered

### Phase C: Closing → Active

1. Closing conditions verified
2. Escrow releases €7.2M
3. Loan originates to Alpine Holdings
4. **Phase transition: B → C** (all tokens now fully transferable)
5. 36 units total:
   - 21 units to early-bird subscribers (€190k)
   - 15 units to standard subscribers (€200k)
6. Issuance fee: 6% × €7.2M = €432,000
   - Platform: €144,000
   - Brokers: €216,000
   - Admin reserve: €72,000
7. Alpine creates Treasury Pool with 4 unsold units

### Secondary Trading (Month 6)

**Two-broker trade:**
- Investor A wants to exit position (1 unit)
- Broker A (sell-side) posts to OTC network
- Broker B's client (Investor B) wants to buy
- Trade executes at €205,000 (2.5% premium)
- Fee breakdown (0.5% = €1,025):
  - Platform: €341.67 (⅓)
  - Broker A (sell-side): €341.67 (⅓)
  - Broker B (buy-side): €341.66 (⅓)

**Issuer treasury sale (Month 9):**
- Investor C (Broker C's client) buys from Alpine's Treasury Pool
- Trade executes at €200,000 par
- Fee breakdown (0.5% = €1,000):
  - Platform: €333.34 (⅓)
  - Alpine (sell-side): €333.33 (⅓)
  - Broker C (buy-side): €333.33 (⅓)

### Conversion (Month 8)

- Investor D (mandate-restricted fund) wraps 2 units to Vienna MTF
- Tokens locked in custody
- Vienna representation issued to investor's brokerage account
- Conversion fee: 0.15% × €400,000 = €600

### Servicing (Ongoing)

- Quarterly coupon: 8.5% ÷ 4 = 2.125%
- Q1 distribution: €7.2M × 2.125% = €153,000
- Distributed pro-rata:
  - On-chain holders: direct to wallets
  - Vienna holders: via depositary

### Maturity (Month 36)

- Alpine Holdings repays €7.2M principal
- Final distribution to all token holders
- Tokens burned
- Series archived with full documentation

---

## Conclusion

Sails.to provides complete infrastructure for regulated tokenized securities:

1. **Issuance**: Wyoming or Marshall Islands DAO LLC structures, three-phase soft/hard cap mechanics with early-bird incentives, professional-only distribution under Reg D/S exemptions

2. **Compliance**: Hierarchical credential system with third-party KYC recognition, wallet-identity separation for custody flexibility, anonymized on-chain claims

3. **Secondary Liquidity**: Multi-broker OTC network with inter-dealer routing, on-chain settlement, and transparent fee distribution

4. **Hybrid Finance**: Bidirectional conversion between on-chain securities and traditional venue representations (Vienna MTF)

5. **Multi-Chain**: Solana and TON support today, architecture ready for future chain additions

6. **Economics**: 6%/1% issuance fees (contingent on closing), 0.5% trading fees, conversion fees, license subscriptions—all transparent and deterministic

7. **Operations**: Melusina OS provides isolated, self-hosted environments for compliance, issuance management, and investor servicing

The platform serves issuers seeking efficient capital formation, brokers seeking new product inventory, and professional investors seeking access to private credit opportunities—all within a compliant, auditable framework.

---

*This document is for informational purposes only and does not constitute legal, tax, or investment advice. Implementation requires qualified legal counsel and licensed intermediaries appropriate to each jurisdiction.*
