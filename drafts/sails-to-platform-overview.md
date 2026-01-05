# Sails.to: A Regulated Platform for Tokenized Securities Issuance, Compliance, and Broker-Mediated Secondary Trading

**A Complete Guide for Newcomers**

---

## Executive Summary

Sails.to is an end-to-end platform for issuing, managing, and trading regulated securities on the Solana blockchain. It provides issuers with everything they need to launch compliant tokenized securities, while simultaneously operating a multi-broker OTC (over-the-counter) network for secondary liquidity—with optional bridging to traditional finance venues like the Vienna MTF.

This is not a DeFi protocol. It is a regulated market infrastructure built on blockchain rails.

**What Sails.to provides:**

- **Issuance tools**: Create and launch security tokens under exemptions like Reg D, Reg S, and EU equivalents
- **Compliance infrastructure**: Self-hosted KYC/AML tooling, investor classification, transfer restrictions
- **Lifecycle management**: Investor communications, corporate actions (coupons, redemptions), reporting
- **Multi-broker OTC network**: Licensed brokers provide liquidity and execution for secondary trading
- **Hybrid liquidity**: Optional conversion between on-chain securities and off-chain representations (e.g., Vienna MTF listed instruments)
- **Wyoming Series LLC DAO service**: Near-instant legal entity setup for issuers who need it ///AND ALSO MARSHALL ISLANDS DAO SERIES LLC

The platform runs on **Melusina OS**—a heavily modified, Solana-integrated version of Sandstorm.io—but Melusina is the operating environment, not the product. Sails.to is the product. ///SOLANA AND/OR TON AND SUPPORT FOR OTHERS IN FUTURE

---

## Part 1: Why This Architecture Exists

### 1.1 The Problem with "Just Put It on a DEX"

A common question: *"If I have a security token, why can't I just list it on Raydium or Orca like any other token?"*

The answer is regulatory reality.

**Securities law does not only regulate:**
- Who receives dividends
- Who can vote
- Who the issuer communicates with

**It also regulates:**
- Who may *own* the security
- Who it may be *offered or sold* to
- How *transfers* may occur

For exemptions like Reg D (US accredited investors) or Reg S (non-US investors), the restriction applies to **ownership and transfer**, not merely economic realization.

An open AMM pool is:
- Globally accessible
- Permissionless (anyone can buy)
- Anonymous (no eligibility screening)

That is legally equivalent to saying "anyone may buy this security"—which breaks most private placement exemptions.

**The unavoidable conclusion**: If you want compliant secondary trading for professional-only securities, you need a permissioned market structure where eligibility is enforced.

### 1.2 The OTC Network Model

Sails.to solves this with a **broker-mediated OTC network**.

In this model:
- **End investors never trade directly with a pool or each other**
- **Investors trade with their broker**
- **Brokers trade with each other and with the market**

This is how bond markets, private credit, and most institutional securities already work. The broker is always the counterparty of record.

This single design decision is what makes the platform compliant:
- Brokers perform KYC/AML and suitability checks
- Brokers ensure only eligible investors participate
- Brokers provide execution, custody, and dispute resolution
- The platform provides infrastructure, not direct investor access

### 1.3 The "Broker Hop" Explained

When an investor wants to buy a security:

1. Investor requests a quote from their broker
2. Broker sources liquidity (internal inventory or from another broker)
3. Broker executes the trade as principal
4. Broker allocates the security to the client

On-chain, this appears as:
- **Broker A → Broker B** (inter-dealer)
- **Broker B → Client** (client allocation)

The client never touches the open market directly. This preserves:
- Reg D / Reg S integrity
- Professional-investor restrictions
- Clear liability and audit trails

---

## Part 2: The Credential Hierarchy

Sails.to uses a hierarchical system of **non-transferable, revocable, renewable credential tokens** (implemented as soulbound NFTs) to control who can do what.

### 2.1 The Trust Chain

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

### 2.2 Platform License NFT

**Issued by**: Platform Operator  
**Held by**: Broker or Issuer entity  

**Represents**: "This entity is authorized to operate on Sails.to"

**Properties**:
- Non-transferable (soulbound)
- Revocable (immediate, by platform)
- Renewable (annual or biannual)
- Contains: jurisdiction(s), license scope, validity period, regulatory references

**Without this NFT**:
- No OTC participation
- No KYC credential issuance
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

**Gates**:
- All broker-side OTC actions
- KYC credential issuance to clients
- Access to broker pool creation and management

### 2.4 Issuer License NFT

**Issued by**: Platform Operator  
**Held by**: Issuer entity wallet  

**Represents**: "This issuer is authorized to issue securities on the platform"

**Contains**:
- Allowed exemptions (Reg D, Reg S, EU exemptions)
- Allowed investor categories
- Corporate action authority
- Jurisdiction constraints

**Gates**:
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
- Jurisdiction/residency (MUST be anonymized)
- Issuing authority (which broker/issuer performed KYC)
- Expiry date
- Optional: risk category flags, specific exemption eligibility

**Critical point**: This is not a global identity token. It is a **trust assertion** produced by a licensed entity. Different brokers may issue different KYC credentials to the same investor. Brokers or issuers may chose to recognize any (all) third party KYC tokens.

### 2.6 Wallet Linking (How Cold Storage Works)

A common pain point: investors want to use hardware wallets (Ledger), multiple wallets, or rotate keys—but permissioned systems often lock tokens to a single address.

Sails.to solves this by separating **identity** from **wallet**:

- Each investor has a verified **identity record**
- Multiple **wallets can be linked** to that identity
- Transfers are allowed to any wallet linked to an eligible identity

This enables:
- Hot wallet for trading
- Cold storage for safekeeping
- Custody wallets (broker or institutional)
- Key rotation without losing access

**The rule**: A security may only be held by a wallet linked to an eligible identity (or authorized custodian). Wallet mobility is fine; ownership eligibility is enforced.

---

## Part 3: The Issuance Model

### 3.1 Wyoming Series LLC DAO Structure

All asset raises on Sails.to use a **Wyoming Series LLC DAO** structure:

- One master LLC operator (can have multiple LLCs for different industries)
- Each issuance is a **Series** within the LLC
- Each Series:
  - Raises capital from investors
  - Makes a **loan** to an underlying asset/project
  - Holds collateral (pledges, security interests)
  - Issues a **debt instrument** (loan note / participation)

**Why this structure?**
- Series segregation (assets/liabilities isolated per issuance)
- Repeatable template (standardized legal docs)
- DAO governance compatibility
- Clear mapping: one Series = one issuance = one security token

Issuers can either:
- Use their own corporate structure, or
- Use Sails.to's **DAO LLC service** for near-instant Series setup

### 3.2 The Security: Tokenized Loan Participation

The security token represents:
- A fractional participation in the Series' loan receivables
- Rights to interest (coupons) and principal repayment
- As defined in offering documents and operating agreements

**Key parameters**:
- **Denomination**: Minimum 200,000 units (indivisible)—creates economic friction appropriate for professional investors
- **Exemption**: Reg D (US accredited), Reg S (non-US), or other applicable exemptions
- **Investor class**: Professional investors only

### 3.3 Soft-Cap / Hard-Cap Mechanics

Every issuance has:
- **Soft cap**: Minimum raise required to proceed
- **Hard cap**: Maximum raise accepted

**The golden rule**: No one earns fees until the soft cap is reached and the deal closes.

**Pre-close (subscription phase)**:
- Investor funds go into **escrow** (legally segregated)
- No funds are released to the issuer/borrower
- No fees are charged
- Tokens are either:
  - Not yet minted, or
  - Minted but locked/non-transferable
///ISSUER MAY CONSIDER DISCOUNTED PRICE (FOR EXAMPLE -5%) FOR THOSE WHO ARE IN SOFT CAP.
THOSE WHO ARE BEYOND SOFT CAP - NOBODY CAN SELL BUT THE ISSUER/BROKERS I.E. WE CONTINUE LOCK/ESCROW (NOW 100 SURE WILL BE) UNTIL WE REACH THE HARD CAP OR THE ISSUANCE DURATION CLOSES.

**At closing (soft cap reached + conditions met)**:
- Escrow releases funds
- Loan originates
- Security tokens become transferable
- Issuance fees are charged

**If soft cap fails**:
- Escrow refunds 100% to investors
- No fees are charged to anyone
- Series is canceled or relaunched

### 3.4 Two-Phase Token Lifecycle

**Phase A: Subscription Receipt Token (pre-close)**
- Non-transferable
- Represents: "I subscribed X amount to this offering"
- Converts to either:
  - Security token (at closing), or
  - Refund (if soft cap fails)

**Phase B: Security Token (post-close)**
- Minted/unlocked only at closing
- Transferable among eligible participants
- Represents the actual loan participation

This clean separation avoids messy clawbacks and prevents pre-close trading.

### 3.5 Closing Conditions

A professional-grade issuance models closing as a **checklist**:

1. ☐ Soft cap reached
2. ☐ KYC completed for all allocations
3. ☐ Offering documents executed
4. ☐ Loan agreement signed
5. ☐ Collateral/pledges perfected
6. ☐ Payment confirmations received

Only when **all conditions are satisfied**:
- Escrow releases
- Loan originates
- Tokens mint/unlock
- Fees are charged

---

## Part 4: The OTC Network

### 4.1 What It Is (And What It Isn't)

The Sails.to OTC network is:
- A **multi-broker dealer network**
- With **on-chain settlement**
- And **shared liquidity signaling**

It is **not**:
- A public DEX
- An anonymous order book
- A permissionless AMM

### 4.2 Broker Pools

Each broker can create **OTC pools**, but these are not AMM pools for anonymous users.

A broker pool represents:
- A **dealer quote surface** (bid/ask, size, terms)
- A **liquidity commitment** (inventory or access to inventory)
- A **routing endpoint** for RFQs (request-for-quote)
- **Jurisdictional scope** (which investors can be served)

Think of it as: "This broker is willing to buy/sell X security at Y price for eligible counterparties."

### 4.3 Trading Flow

**Step 1**: Investor requests quote from broker (RFQ)

**Step 2**: Broker sources liquidity:
- Internal inventory
- Other brokers via network
- Issuer treasury (if applicable)

**Step 3**: Broker returns quote to investor

**Step 4**: If accepted, broker executes:
- Broker-to-broker settlement (if external)
- Broker-to-client allocation

**Step 5**: Settlement occurs on-chain with full audit trail

### 4.4 What's Automated vs. What's Not

**Safe to automate**:
- Quote publication
- Inventory availability
- RFQ routing between brokers
- Broker-to-broker settlement
- Best-execution routing across broker pools
- Compliance attestation checks

**Must NOT automate**:
- Client execution without broker approval
- Anonymous matching
- Direct client access to pools
- Wallet-level routing that bypasses brokers

If regulators see "clients press a button and tokens appear" without broker intermediation, the model fails.

### 4.5 Settlement

Settlement can be:
- **DvP (Delivery vs Payment)**: Atomic swap using stablecoins
- **Escrowed settlement**: Timelock with conditions
- **Back-to-back**: Broker fills then allocates

All settlements emit structured events for reconciliation and audit.

---

## Part 5: The Hybrid Layer (Vienna MTF Conversion)

### 5.1 The Direction of Wrapping

Sails.to supports wrapping **from Solana to off-chain venues**, not the reverse.

- **Canonical security**: The Solana token (source of truth)
- **Vienna MTF instrument**: A **representation** backed by immobilized Solana securities

Vienna investors hold a claim against a depositary/custodian SPV whose sole asset is locked Solana tokens. They do not hold Solana tokens directly.

### 5.2 Wrap Flow (Solana → Vienna)

1. Investor requests wrap (through broker workflow)
2. Investor's Solana tokens transfer to **custody/lockbox wallet**
3. Tokens are **locked** (not burned)
4. Depositary issues Vienna MTF instrument
5. Investor receives Vienna instrument in their brokerage account

**Invariant**: Vienna outstanding ≤ Solana tokens locked in custody

### 5.3 Unwrap Flow (Vienna → Solana)

1. Investor requests unwrap through Vienna broker
2. Vienna instrument is delivered to depositary and canceled
3. Depositary releases locked Solana tokens
4. Tokens transfer to investor's registered Solana wallet

### 5.4 Corporate Actions Synchronization

Because Solana is the canonical ledger:
- All corporate actions originate on Solana
- Vienna holders receive pass-through economics via depositary
- **Conversion blackout windows** around record dates prevent double-counting

### 5.5 Why This Matters

This hybrid enables:
- Some investors to trade via traditional MTF infrastructure
- Others to trade via on-chain OTC network
- Seamless conversion between the two
- Single source of truth (no duplicate instruments)

---

## Part 6: The Fee Model

### 6.1 Issuance Fees (Primary Origination)

**Standard Issuance**: 6% total
- Charged once, at closing
- Paid by issuer (deducted from proceeds)

**Strategic Issuance**: 1% total
- Applies when issuing only to:
  - Platform partners
  - Co-investors
  - Pre-identified strategic investors
  - No broker-led public distribution

**Critical integration with soft-cap**:
- If soft cap not reached: **Issuance fee = 0**
- Fees are contingent, not earned until closing

**Suggested split (configurable per deal)**:

| Recipient | Standard (6%) | Strategic (1%) |
|-----------|---------------|----------------|
| Platform | 2.0% | 0.75% |
| Brokers/Placement | 3.0% | — |
| Admin/Legal Reserve | 1.0% | 0.25% |

### 6.2 Trading Fees (Primary Distribution + Secondary OTC)

**Fee**: 0.5% per trade on Solana

**Scope**:
- Broker-mediated primary distributions
- Secondary OTC trades
- **Not charged on**: raw issuance, wrap/unwrap conversions

**Fee base**: Notional value of trade

**Split**:

| Recipient | Percentage |
|-----------|------------|
| Executing Broker | 0.30% |
| Platform | 0.20% |

**Who pays**: Buyer only (single-sided)—matches OTC market convention, simplifies accounting.

**Variants supported**:
- **Internalized trades** (broker matches internally): Broker 0.40%, Platform 0.10%
- **Issuer-sponsored liquidity programs**: Platform rebates to issuer

### 6.3 Conversion Fees (Solana ↔ Vienna)

Conversion is **asset servicing**, not trading. Fees should be:
- Predictable
- Lower than trading fees
- Often capped

**Structure**:
- 0.10% – 0.25% of notional
- Cap at €25,000 (or equivalent)
- Paid by requesting party

**Split**:

| Recipient | Percentage |
|-----------|------------|
| Platform | 70% |
| Depositary/Custodian | 30% |

**No double-charging rule**: If a user trades then immediately converts, they pay trade fee once and conversion fee once—never both for the same economic action.

### 6.4 License and Platform Fees

**Broker License**:
- Annual or biannual subscription
- €25,000 – €150,000 (depending on jurisdiction and scope)
- Covers: access, audits, upgrades, support

**Issuer License**:
- Lower flat fee, or
- Bundled into issuance fee

**Optional service fees**:
- Enhanced reporting
- Custodial workflows
- Compliance vendor integrations
- White-label deployments

This creates stable, recurring revenue independent of transaction volume.

---

## Part 7: Smart Contract Architecture

### 7.1 Platform Governance Contract

**Purpose**: Root authority for the platform

**Functions**:
- Define platform authorities (multisig/DAO)
- Control upgrades and global parameters
- Set fee schedules and credential types
- Emergency pause/unpause

### 7.2 License Registry Contract

**Purpose**: Canonical registry of all licensed entities

**Functions**:
- Map entity IDs to credential token accounts
- Query: "Is broker X licensed?", "Is issuer Y authorized?"
- Track status (active/suspended/revoked/expired)

### 7.3 Broker License NFT Contract

**Purpose**: Issue and manage broker credentials

**Enforces**:
- Non-transferability (soulbound)
- Expiration dates
- Revocation (immediate effect)
- Renewal (metadata update, not remint)

### 7.4 Issuer License NFT Contract

**Purpose**: Same as broker license, for issuers

### 7.5 Identity Registry & Wallet-Link Contract

**Purpose**: Map legal identities to wallet addresses

**Functions**:
- Link multiple wallets to one identity
- Add/remove wallets (with authorization)
- Support key rotation
- Register custody wallets
- Maintain audit logs of all changes

**Authorization model**: Investor + broker co-sign, or platform-approved KYC authority

### 7.6 KYC Credential Contract

**Purpose**: Issue investor eligibility credentials

**Properties**:
- Minted only by licensed brokers/issuers
- Contains eligibility claims, expiry, issuing authority
- Non-transferable
- Revocable

### 7.7 Series Factory Contract

**Purpose**: Create new issuance series

**Creates**:
- Series ID
- Security token mint parameters
- Offering parameters (soft cap, hard cap, dates)
- Approved KYC issuers for this series
- Fee configuration

### 7.8 Subscription Escrow Contract

**Purpose**: Hold investor funds until closing

**Functions**:
- Receive subscription payments
- Track subscription amounts per investor
- Enforce: no release until closing conditions met
- Execute refund if soft cap fails
- Trigger token mint/unlock on successful close

### 7.9 Subscription Receipt Token Contract

**Purpose**: Represent pre-close subscriptions

**Properties**:
- Non-transferable
- Burned/converted at close or refund
- Clean audit trail of who subscribed what

### 7.10 Security Token Contract

**Purpose**: The actual security instrument

**Enforces**:
- Transfer restrictions (only to eligible wallets)
- Wallet must be linked to identity with valid KYC
- Denomination rules (e.g., indivisible 200k units)
- Lock flags for custody/wrapping
- Special roles for issuer/broker/custodian

**Includes**: Compliance hooks that run on every transfer

### 7.11 OTC Trading Contracts

**A. Quote/RFQ Registry**
- Brokers post indicative quotes
- Respond to RFQ requests
- Price discovery layer

**B. Trade Execution Contract**
- Execute broker-mediated settlements
- Verify both parties licensed/eligible
- Calculate and distribute fees
- Emit audit events

**C. Broker Pool Registry**
- Track which brokers are active for which series
- Reputation and activity metrics
- Compliance status checks

### 7.12 Fee Splitter Contract

**Purpose**: Deterministic fee distribution

**Functions**:
- Issuance fee distribution at close
- Trade fee splitting (broker/platform)
- Conversion fee splitting (platform/depositary)
- Transparent, auditable, immutable per series

### 7.13 Conversion Lockbox Contract

**Purpose**: Custody for Solana → Vienna wrapping

**Functions**:
- Receive and lock Solana security tokens
- Emit conversion receipts for off-chain operators
- Release tokens only on validated redemption
- Reconciliation queries

### 7.14 Corporate Actions Contract

**Purpose**: Execute lifecycle events

**Functions**:
- Schedule coupon payments
- Execute principal repayments
- Handle redemptions
- Process restructurings (if applicable)

**Integrates with**:
- KYC credential checks (who can receive payments)
- Record-date logic
- Conversion blackout windows

### 7.15 Audit/Event Anchoring Contract

**Purpose**: Immutable proof of off-chain artifacts

**Functions**:
- Anchor document hashes (offering docs, agreements, notices)
- Timestamp proofs ("this document existed at time T")
- Support regulatory/audit queries

---

## Part 8: Operational Flows and Procedures

### 8.1 Broker Onboarding

1. Broker applies (off-chain due diligence by platform)
2. Platform governance approves
3. Platform issues **Broker License NFT**
4. Broker deploys Melusina OS instance
5. Broker gains access to:
   - OTC network contracts
   - KYC credential issuance
   - Broker pool creation

### 8.2 Issuer Onboarding

1. Issuer applies with:
   - Legal structure documentation
   - Compliance readiness evidence
   - Business/asset information
2. Platform governance approves
3. Platform issues **Issuer License NFT**
4. Issuer either:
   - Deploys own Melusina OS instance, or
   - Uses platform DAO LLC service for instant Series setup
5. Issuer can now create Series

### 8.3 Investor Onboarding

1. Investor approaches a **licensed broker** (or issuer for partner allocations)
2. Broker performs:
   - KYC/AML verification
   - Investor classification (professional, accredited, etc.)
   - Suitability assessment
3. Broker issues **KYC Credential Token** to investor identity
4. Investor links wallets (hot, cold, custody) to their identity
5. Investor can now participate in eligible offerings and secondary trading

### 8.4 Issuance Execution (Full Cycle)

**Phase 1: Setup**
1. Issuer creates Series in platform
2. Defines terms:
   - Soft cap / hard cap
   - Subscription window
   - Coupon schedule
   - Collateral/pledge structure
3. Legal documents finalized
4. Series Factory Contract creates the series

**Phase 2: Subscription**
1. Broker network distributes offering to eligible investors
2. Investors subscribe through their brokers
3. Funds flow to Escrow Contract
4. Subscription Receipt Tokens issued

**Phase 3: Closing (or Refund)**

*If soft cap NOT reached by deadline:*
- Escrow Contract refunds all investors
- Subscription Receipt Tokens burned
- No fees charged
- Series canceled or relaunched

*If soft cap reached AND all conditions met:*
- Escrow releases funds to Series
- Loan originates to underlying asset
- Security Tokens minted/unlocked
- Subscription Receipt Tokens converted
- Issuance fee charged and distributed

**Phase 4: Live**
- Security tokens freely transferable (among eligible holders)
- Secondary trading enabled on OTC network
- Conversion to Vienna representation available

**Phase 5: Servicing**
- Coupons paid per schedule
- Corporate Actions Contract distributes to eligible holders
- Investor communications via issuer portal
- Periodic reporting published

**Phase 6: Maturity**
- Principal repaid
- Final distribution to holders
- Tokens redeemed/burned
- Series enters archive state with full retention

### 8.5 Secondary Trading (Full Cycle)

1. **Investor A** wants to sell → contacts their broker
2. **Broker A** posts to OTC network or accepts RFQ
3. **Broker B** (representing Investor B) sees liquidity
4. Brokers negotiate/match
5. **Trade Execution Contract**:
   - Verifies both brokers licensed
   - Verifies both end-clients have valid KYC
   - Executes settlement
   - Charges 0.5% fee, splits to broker/platform
6. **Broker B** allocates security to Investor B's wallet
7. Audit events emitted for reconciliation

### 8.6 Conversion Flow (Solana → Vienna)

1. Investor requests wrap via broker
2. Broker initiates Lockbox Contract deposit
3. Investor's Solana tokens transfer to lockbox
4. Lockbox emits conversion receipt
5. Off-chain depositary process:
   - Validates receipt
   - Issues Vienna MTF instrument
   - Settles to investor's brokerage account
6. Conversion fee charged

### 8.7 Conversion Flow (Vienna → Solana)

1. Investor requests unwrap via Vienna broker
2. Vienna instrument delivered to depositary
3. Depositary cancels/redeems instrument
4. Depositary signals Lockbox Contract
5. Lockbox releases tokens to investor's registered Solana wallet
6. Conversion fee charged

---

## Part 9: Risk Controls and Governance

### 9.1 Platform Governance

- **Multisig control** for all critical operations
- **Separation of duties**: who can revoke licenses vs. who can pause markets vs. who can upgrade contracts
- **Timelocks** on sensitive operations
- **Emergency pause** capability for:
  - All trading
  - Specific series
  - Conversions

### 9.2 Reconciliation

**Daily reconciliation requirements**:
- Lockbox balance vs. Vienna representation outstanding
- Escrow balances vs. subscription records
- Fee accruals vs. distributions

**Tri-party reconciliation**: Platform ↔ Custodian ↔ External auditors

### 9.3 Credential Lifecycle

All credentials must support:
- **Expiry**: Automatic loss of privileges when validity ends
- **Revocation**: Immediate effect (sanctions, bad activity, status change)
- **Public status queries**: Any contract can check "is this credential valid right now?"

### 9.4 Audit Trails

Platform must retain:
- Who performed KYC, when, under what policy
- What terms were disclosed to each investor
- All trades and settlements
- All corporate action distributions
- All communications and notices

All exportable for regulatory/broker audits.

---

## Part 10: The Complete Business Model

### 10.1 Why Issuers Use Sails.to

**They get**:
- Fast, programmable issuance
- Compliance-ready investor onboarding
- Path to secondary liquidity
- Lifecycle management tools
- Optional off-chain market bridging
- DAO LLC service for instant legal structure

**They pay**:
- Issuance fee (only on successful close)
- Optional platform subscriptions
- Optional service fees for complex needs

### 10.2 Why Brokers Join

**They get**:
- New product inventory (tokenized private credit)
- Integrated KYC and investor management
- OTC network access and liquidity
- Transaction fee revenue (0.30% per trade)
- Placement fees on primary distribution

**They pay**:
- License fees (annual/biannual)
- Operational obligations (KYC/AML, suitability, reporting)

### 10.3 Why Investors Use It

**They get**:
- Access to private credit deals
- Better settlement efficiency than paper-based systems
- Transparent lifecycle data
- Cold storage / hardware wallet support
- Optional conversion to MTF-held instruments

**They pay**:
- Trading fees (embedded in OTC pricing)
- Conversion fees (if converting between forms)

### 10.4 Platform Defensibility

The moat is not "a token on Solana." It's the integrated stack:

- Licensed broker network (network effects)
- Licensed issuer base
- Compliance infrastructure
- Issuance lifecycle tooling
- OTC liquidity aggregation
- Off-chain venue conversion rails
- Standardized, repeatable Wyoming Series LLC DAO templates
- Melusina OS operational environment

---

## Part 11: End-to-End Example

**"Alpine Credit Series 2026-A"** — A Tokenized Loan Participation

### Setup
- Issuer uses Sails.to DAO LLC service
- Creates Wyoming Series LLC DAO, Series 2026-A
- Underlying: Secured loan to Alpine Holdings for equipment financing

### Terms
- Soft cap: €5,000,000
- Hard cap: €15,000,000
- Denomination: €200,000 minimum
- Coupon: 8.5% annual, paid quarterly
- Maturity: 36 months
- Collateral: First-priority security interest in financed equipment
- Exemption: Reg S + Reg D

### Distribution
- 3 licensed brokers onboarded
- Brokers distribute to their eligible professional investors
- Investors subscribe; funds enter escrow
- Subscription Receipt Tokens issued

### Outcome: Soft Cap Reached (€7.2M raised)

1. Closing conditions verified
2. Escrow releases €7.2M
3. Loan originates to Alpine Holdings
4. Security tokens minted: 36 units × €200,000
5. Issuance fee charged: 6% × €7.2M = €432,000
   - Platform: €144,000
   - Brokers: €216,000
   - Admin reserve: €72,000

### Secondary Trading
- Month 6: Investor A wants to exit
- Investor A's broker posts sell interest
- Broker B's client wants exposure
- Trade executes at €205,000 (2.5% premium)
- Trade fee: 0.5% × €205,000 = €1,025
  - Executing broker: €615
  - Platform: €410

### Conversion
- Investor C (mandate-restricted) wraps 2 units to Vienna MTF
- Tokens locked in custody
- Vienna representation issued
- Conversion fee: 0.15% × €400,000 = €600

### Servicing
- Quarterly coupons: 8.5% / 4 = 2.125% per quarter
- Q1 distribution: €7.2M × 2.125% = €153,000
- Distributed pro-rata to all holders (Solana direct + Vienna via depositary)

### Maturity (Month 36)
- Alpine Holdings repays principal
- Final distribution to all holders
- Tokens burned/redeemed
- Series archived with full documentation

---

## Conclusion

Sails.to is a complete regulated securities infrastructure built on Solana:

1. **Issuance**: Wyoming Series LLC DAO structures, soft/hard cap escrow, professional-only distribution under Reg D/S exemptions

2. **Compliance**: Hierarchical credential system (Platform → Brokers/Issuers → Investors), wallet-identity separation for custody flexibility

3. **Secondary liquidity**: Broker-mediated OTC network with inter-dealer routing and on-chain settlement

4. **Hybrid finance**: Bidirectional conversion to traditional venues (Vienna MTF) via custody-backed representations

5. **Economics**: 6%/1% issuance fees (contingent on closing), 0.5% trading fees, conversion fees, license subscriptions

6. **Operations**: Melusina OS provides the self-hosted environment for KYC, compliance, issuance management, and investor servicing

The platform doesn't pretend regulated securities can behave like DeFi tokens. Instead, it builds the infrastructure that makes compliant tokenized securities actually work—for issuers, brokers, and professional investors.

---

