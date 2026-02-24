---
title: "Metadata - Documentation"
description: "Structured metadata for KYC credential NFTs, role NFTs, offering state PDAs, compliance configs, and program events — what every field means and why it exists."
ogImage: "/og-image.png"
keywords: ["metadata", "NFT metadata", "KYC credential", "role NFT", "PDA", "on-chain", "privacy"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/docs.css"
heroDesc: "Every NFT and on-chain account on Sails.to carries structured metadata — the fields that tell the protocol what a token represents, who holds it, and what rules apply."
draft: false
---
<h2>Overview</h2>
        <p>Metadata is not decoration. On Sails.to, metadata is the mechanism by which <span class="glossary-term" data-term="smart-contract">smart contracts</span> enforce compliance, authorize actions, and maintain audit trails. Every NFT — whether it represents a <span class="glossary-term" data-term="kyc">KYC</span> credential, an operator role, or an offering configuration — carries a structured set of fields that the <a href="/knowledge/glossary/solana/">Solana</a> runtime reads and validates on every instruction.</p>
        <p>There are no optional fields in a "nice to have" sense. Each field exists because a specific compliance check, authorization gate, or audit requirement demands it. Remove a field and a smart contract check breaks. Add a field without purpose and you waste on-chain storage that every validator must replicate. The metadata schemas documented here are the product of that discipline.</p>
        <p>This page covers the six metadata categories on the platform: <strong>KYC Credential NFTs</strong>, <strong>Role NFTs</strong>, <strong>OfferingState PDAs</strong>, <strong>ComplianceConfig PDAs</strong>, <strong>Program Events</strong>, and the <strong>privacy architecture</strong> that binds them together.</p>
        <h2>KYC Credential NFT Metadata</h2>
        <p>Every investor on the platform carries a KYC Credential NFT — an on-chain attestation that a licensed verification provider has confirmed the investor's identity, classification, and regulatory status. This NFT contains <strong>zero personally identifiable information</strong>. What it does contain is everything the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> needs to enforce compliance rules at the protocol level.</p>
        <pre><code>KYC NFT Metadata (on-chain, no PII):
├── investor_class:      enum { Accredited, Professional, QualifiedPurchaser, Retail }
├── jurisdiction_hash:   [u8; 32]   // SHA-256 of ISO country code
├── reg_exemption:       enum { RegD506b, RegD506c, RegS, RegA, RegCF }
├── verification_level:  enum { Basic, Enhanced, InstitutionalEDD }
├── issued_by:           Pubkey     // KYC provider's license NFT
├── issued_at:           i64        // Unix timestamp
├── expires_at:          i64        // Credential expiration
├── aml_clear:           bool       // Anti-money laundering clearance
└── pep_clear:           bool       // Politically exposed person check</code></pre>
        <h3>Field-by-Field Breakdown</h3>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Type</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>investor_class</code></strong></td>
                    <td>Enum</td>
                    <td>Determines which offerings the investor can access. An <span class="glossary-term" data-term="accredited-investor">Accredited Investor</span> can participate in <span class="glossary-term" data-term="reg-d">Reg D 506(b)</span> and 506(c) offerings. A <span class="glossary-term" data-term="professional-investor">Professional Investor</span> can access institutional tranches. A <code>QualifiedPurchaser</code> meets the higher threshold for certain private fund exemptions. <code>Retail</code> investors are limited to Reg A and Reg CF offerings. The smart contract checks this classification on every mint, every transfer, and every distribution claim.</td>
                </tr>
                <tr>
                    <td><strong><code>jurisdiction_hash</code></strong></td>
                    <td><code>[u8; 32]</code></td>
                    <td>A SHA-256 hash of the investor's ISO 3166-1 country code. The blockchain never sees the raw country code — only its hash. But the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> can still enforce jurisdiction whitelists by comparing the investor's hash against the offering's list of allowed jurisdiction hashes. A <span class="glossary-term" data-term="reg-s">Reg S</span> offering restricted to non-US investors will reject any transfer to a wallet whose jurisdiction hash matches the US hash.</td>
                </tr>
                <tr>
                    <td><strong><code>reg_exemption</code></strong></td>
                    <td>Enum</td>
                    <td>Records which regulatory exemption the investor was verified under. This matters because different exemptions carry different rules — <span class="glossary-term" data-term="reg-d">Reg D 506(c)</span> requires verified accreditation, while 506(b) allows up to 35 non-accredited investors. The offering's <code>ComplianceConfig</code> checks that the investor's exemption is compatible with the offering's exemption before allowing any operation.</td>
                </tr>
                <tr>
                    <td><strong><code>verification_level</code></strong></td>
                    <td>Enum</td>
                    <td>Indicates the depth of due diligence performed. <code>Basic</code> covers standard identity verification. <code>Enhanced</code> adds source-of-funds checks and additional document review. <code>InstitutionalEDD</code> is full Enhanced Due Diligence for institutional investors — beneficial ownership, corporate structure analysis, and sanctions screening at every level. Higher-value offerings can require a minimum verification level.</td>
                </tr>
                <tr>
                    <td><strong><code>issued_by</code></strong></td>
                    <td>Pubkey</td>
                    <td>The public key of the licensed KYC provider's license NFT that issued this credential. This creates a verifiable chain of authority: the platform can trace any credential back to the provider who issued it, and if a provider's license is revoked, every credential they issued can be flagged for re-verification.</td>
                </tr>
                <tr>
                    <td><strong><code>issued_at</code></strong></td>
                    <td><code>i64</code></td>
                    <td>Unix timestamp recording when the credential was issued. Used for audit trail purposes and to determine credential age — some compliance policies require re-verification after a certain period regardless of the <code>expires_at</code> date.</td>
                </tr>
                <tr>
                    <td><strong><code>expires_at</code></strong></td>
                    <td><code>i64</code></td>
                    <td>Unix timestamp after which this credential is no longer valid. When <code>expires_at</code> passes, the smart contract rejects any new minting or transfer operations for this investor until a fresh credential is issued. The platform tracks expiration windows proactively and triggers re-verification workflows before credentials expire.</td>
                </tr>
                <tr>
                    <td><strong><code>aml_clear</code></strong></td>
                    <td><code>bool</code></td>
                    <td><span class="glossary-term" data-term="aml">Anti-money laundering</span> clearance. If <code>false</code>, the investor has not passed AML screening and cannot participate in any offering. The Transfer Hook checks this flag on every transaction — a cleared investor whose AML status is later revoked is immediately locked out of all transfers.</td>
                </tr>
                <tr>
                    <td><strong><code>pep_clear</code></strong></td>
                    <td><code>bool</code></td>
                    <td>Politically exposed person clearance. PEP status requires enhanced monitoring under most regulatory frameworks. If <code>false</code>, the investor is flagged as a PEP or has not been screened, and the platform applies additional transaction scrutiny. Both <code>aml_clear</code> and <code>pep_clear</code> must be <code>true</code> for unrestricted participation.</td>
                </tr>
            </tbody>
        </table>
        <p>The critical design constraint: <strong>none of these fields contain PII</strong>. No names, no addresses, no document images, no phone numbers. The investor's actual identity documents are encrypted and stored off-chain in the KYC grain's journal with 7-year retention. The on-chain credential carries only the classification flags and cryptographic proofs that the smart contract needs to make compliance decisions.</p>
        <h2>Role NFT Metadata</h2>
        <p>The platform uses NFT-based authorization for every privileged action. There are no API keys, no admin passwords, no shared secrets. If you want to mint <span class="glossary-term" data-term="security-token">security tokens</span>, you need an Issuer NFT in your wallet. If you want to authenticate a <span class="glossary-term" data-term="crossconversion">CrossConversion</span>, you need a <span class="glossary-term" data-term="trustee">Trustee</span> NFT. The smart contract checks the caller's wallet for the required NFT on every instruction — no NFT, no authorization.</p>
        <p>Each Role NFT is a print edition from the <span class="glossary-term" data-term="master-nft">Sails Master NFT</span>, carrying role-specific metadata and optional expiration. All Role NFTs are recallable — if a participant's authorization is revoked, their NFT is burned and every instruction that checks for it will immediately fail.</p>
        <table>
            <thead>
                <tr>
                    <th>Role NFT</th>
                    <th>Capabilities</th>
                    <th>Issued By</th>
                    <th>Recallable</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Platform Operator</strong></td>
                    <td>Deploy offerings, manage platform configuration, approve issuers and brokers, emergency pause</td>
                    <td>Master NFT (3-of-5 <span class="glossary-term" data-term="threshold-signing">keyholder threshold</span>)</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>White-Label Operator</strong></td>
                    <td>Operate a branded instance, manage own issuers and offerings, configure white-label UI</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>Trustee</strong></td>
                    <td>Authenticate CrossConversions, validate distributions, sign reconciliation reports, emergency freeze</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>KYC Issuer</strong></td>
                    <td>Issue KYC Credential NFTs to verified investors, revoke credentials, update verification status</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="broker-dealer">Broker</span></strong></td>
                    <td>Place investors into offerings, execute secondary trades, manage client portfolios, earn placement commissions</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>Issuer</strong></td>
                    <td>Create offerings within their <span class="glossary-term" data-term="series-llc">Series</span>, mint security tokens, manage investor whitelist, configure compliance parameters</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="paying-agent">Paying Agent</span></strong></td>
                    <td>Execute <span class="glossary-term" data-term="distributions">distributions</span>, manage revenue waterfall, process investor claims, handle tax withholding</td>
                    <td>Trustee</td>
                    <td>Yes</td>
                </tr>
            </tbody>
        </table>
        <p>The hierarchy matters. A Platform Operator is issued by the Master NFT holders — the 3-of-5 keyholder set that controls the root of the authority chain. A Paying Agent is issued by a Trustee, not directly by the Platform Operator, because paying agent authority is scoped to the trust relationship. If a Trustee's NFT is recalled, every Paying Agent they issued is also invalidated. Authority flows downward; revocation propagates upward.</p>
        <h2>Offering State Metadata</h2>
        <p>Every offering on the platform is represented by an <code>OfferingState</code> <span class="glossary-term" data-term="pda">PDA</span> — a Program Derived Address account seeded by <code>["offering", series_id]</code>. This PDA is the canonical source of truth for the offering's current state, and every instruction that touches the offering reads from it.</p>
        <pre><code>OfferingState PDA Fields:
├── series_id:            Pubkey   // Links to the DAO Series LLC
├── max_supply:           u64      // Maximum tokens that can ever be minted
├── minted:               u64      // Tokens minted so far
├── locked_in_crossconv:  u64      // Tokens locked in CrossConversion lockbox
├── nominal_value:        u64      // Face value per token (in cents)
├── status:               enum     // Active, Paused, Closed
└── version:              u8       // PDA version for migration support</code></pre>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>series_id</code></strong></td>
                    <td>Links the offering to its parent <span class="glossary-term" data-term="series-llc">DAO Series LLC</span>. Every offering belongs to exactly one Series, and the Series controls the legal structure — operating agreement, member rights, and regulatory filings. The <code>series_id</code> is how the smart contract traces an offering back to its legal entity.</td>
                </tr>
                <tr>
                    <td><strong><code>max_supply</code></strong></td>
                    <td>The hard cap on token issuance. Once <code>minted</code> reaches <code>max_supply</code>, the <code>mint_security_token</code> instruction rejects all further minting. This is not a soft limit — it is enforced at the protocol level and cannot be changed without a program upgrade approved by the 3-of-5 keyholder set.</td>
                </tr>
                <tr>
                    <td><strong><code>minted</code></strong></td>
                    <td>Running count of tokens minted to date. Incremented by the <code>mint_security_token</code> instruction. Combined with <code>max_supply</code>, this gives real-time visibility into how much of an offering has been subscribed — critical for both compliance reporting and investor transparency.</td>
                </tr>
                <tr>
                    <td><strong><code>locked_in_crossconv</code></strong></td>
                    <td>Tokens currently locked in the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox. The supply invariant <code>locked_in_crossconv == isin_outstanding</code> must hold at all times — if on-chain lockbox state ever diverges from <span class="glossary-term" data-term="clearstream">Clearstream</span> positions, the reconciliation engine flags it immediately. This counter is incremented by <code>burn_for_crossconversion</code> and decremented by <code>redeem_from_crossconversion</code>.</td>
                </tr>
                <tr>
                    <td><strong><code>nominal_value</code></strong></td>
                    <td>The face value of each token in cents. A token with <span class="glossary-term" data-term="nominal-value">nominal value</span> of 10000 represents $100.00. This is used by the distribution waterfall to calculate per-token payouts and by the <span class="glossary-term" data-term="cap-table">cap table</span> to report ownership in dollar terms, not just token counts.</td>
                </tr>
                <tr>
                    <td><strong><code>status</code></strong></td>
                    <td>The offering lifecycle state. <code>Active</code> means minting, transfers, and distributions are permitted. <code>Paused</code> freezes all operations — triggered by the emergency pause bit in <code>ComplianceConfig</code> or by a Security Admin NFT action. <code>Closed</code> is terminal: remaining tokens are burned, outstanding CrossConversions settled, and the PDA is sealed. There is no transition back from <code>Closed</code>.</td>
                </tr>
                <tr>
                    <td><strong><code>version</code></strong></td>
                    <td>PDA schema version for data migration support. When the program is upgraded, migration instructions read the <code>version</code> field to determine which migration path to apply. This ensures backward compatibility without breaking existing on-chain state.</td>
                </tr>
            </tbody>
        </table>
        <h2>ComplianceConfig Metadata</h2>
        <p>Every offering carries a companion <code>ComplianceConfig</code> <span class="glossary-term" data-term="pda">PDA</span>, seeded by <code>["compliance", offering_id]</code>. This is where the regulatory rules live — not in documentation, not in terms of service, but in on-chain data that the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> reads on every single token transfer.</p>
        <pre><code>ComplianceConfig PDA Fields:
├── offering_id:              Pubkey              // The offering this config governs
├── allowed_jurisdictions:    Vec&lt;[u8; 32]&gt;       // SHA-256 hashes of allowed ISO codes
├── min_investment:           u64                 // Minimum investment amount (in cents)
├── lock_up_days:             u32                 // Mandatory holding period
├── max_investors:            u32                 // Maximum investor count
├── accreditation_required:   bool                // Whether accredited status is mandatory
├── reg_exemption:            enum                // Which regulatory exemption applies
├── features:                 u64                 // Bitmask for feature flags
└── version:                  u8                  // PDA version for migration</code></pre>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>offering_id</code></strong></td>
                    <td>Links this compliance configuration to its parent offering. One offering, one <code>ComplianceConfig</code> — the relationship is 1:1 and enforced by the PDA seed derivation.</td>
                </tr>
                <tr>
                    <td><strong><code>allowed_jurisdictions</code></strong></td>
                    <td>A list of SHA-256 hashes of ISO 3166-1 country codes representing the jurisdictions from which investors are permitted. The Transfer Hook compares the investor's <code>jurisdiction_hash</code> from their KYC Credential NFT against this list. If the hash is not present, the transfer is rejected. This is how a <span class="glossary-term" data-term="reg-s">Reg S</span> offering excludes US investors without ever storing a country name on-chain.</td>
                </tr>
                <tr>
                    <td><strong><code>min_investment</code></strong></td>
                    <td>The minimum investment amount in cents. The <code>mint_security_token</code> instruction checks that the minted amount multiplied by the <span class="glossary-term" data-term="nominal-value">nominal value</span> meets or exceeds this threshold. Prevents micro-positions that would create compliance overhead disproportionate to their value.</td>
                </tr>
                <tr>
                    <td><strong><code>lock_up_days</code></strong></td>
                    <td>Mandatory holding period in days before an investor can transfer their tokens. For <span class="glossary-term" data-term="reg-d">Reg D</span> securities, this is typically 6–12 months. The <code>transfer_with_compliance</code> instruction compares the investor's <code>locked_until</code> timestamp against the current slot time — if the lock-up has not elapsed, the transfer is rejected at the protocol level. No exceptions, no overrides.</td>
                </tr>
                <tr>
                    <td><strong><code>max_investors</code></strong></td>
                    <td>The maximum number of investors allowed in the offering. Critical for <span class="glossary-term" data-term="reg-d">Reg D</span> compliance — 506(b) limits non-accredited investors to 35, and total investor counts must remain under SEC thresholds. The smart contract tracks the current investor count in the <code>OfferingState</code> PDA and rejects any mint that would exceed this limit.</td>
                </tr>
                <tr>
                    <td><strong><code>accreditation_required</code></strong></td>
                    <td>When <code>true</code>, only investors whose KYC Credential NFT carries an <code>investor_class</code> of <code>Accredited</code>, <code>Professional</code>, or <code>QualifiedPurchaser</code> can participate. <code>Retail</code> investors are blocked. This flag is the on-chain enforcement of the accreditation requirement for Reg D 506(c) and similar exemptions.</td>
                </tr>
                <tr>
                    <td><strong><code>reg_exemption</code></strong></td>
                    <td>The specific regulatory exemption under which the offering operates. This field is cross-checked against the investor's <code>reg_exemption</code> in their KYC Credential NFT to ensure compatibility. An investor verified under Reg A cannot be minted tokens in a Reg D 506(c) offering.</td>
                </tr>
                <tr>
                    <td><strong><code>features</code></strong></td>
                    <td>A 64-bit bitmask for feature flags. The most critical bit is the <strong>emergency pause</strong> — when set (gated by Security Admin NFT), the Transfer Hook rejects all transfers for the offering. This is the circuit breaker for regulatory emergencies. Other bits control optional features like distribution auto-claiming, secondary trading eligibility, and CrossConversion availability — all toggleable without a program upgrade.</td>
                </tr>
                <tr>
                    <td><strong><code>version</code></strong></td>
                    <td>Schema version for forward-compatible data migration, identical in purpose to the <code>OfferingState</code> version field.</td>
                </tr>
            </tbody>
        </table>
        <p>The <code>ComplianceConfig</code> is set at offering creation by the Issuer with Platform Operator approval. Modifications after creation require the same dual authorization. This is compliance as data — stored on-chain, enforced by the runtime, auditable by anyone.</p>
        <h2>Event Metadata</h2>
        <p>The <code>sails_securities</code> program emits five structured events for every significant state change. These are not optional log messages — they are the mechanism by which the off-chain application layer stays synchronized with on-chain state. The Solana Event Watcher grain subscribes to these events and routes them to the appropriate application grains for processing.</p>
        <table>
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Fields</th>
                    <th>Why It Matters</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>SecurityMinted</code></strong></td>
                    <td><code>offering</code>, <code>investor</code>, <code>amount</code>, <code>timestamp</code></td>
                    <td>Triggers <span class="glossary-term" data-term="cap-table">cap table</span> updates in the Offering Grain and portfolio notifications in the Investor Grain. The <code>timestamp</code> field anchors the lock-up period calculation — <code>locked_until = timestamp + lock_up_days</code>.</td>
                </tr>
                <tr>
                    <td><strong><code>CrossConversionRequested</code></strong></td>
                    <td><code>offering</code>, <code>amount</code>, <code>direction</code>, <code>isin</code></td>
                    <td>Initiates the <span class="glossary-term" data-term="clearstream">Clearstream</span> workflow. The <code>direction</code> field indicates whether tokens are being locked (on-chain → bankable) or unlocked (bankable → on-chain). The <code>isin</code> field carries the <span class="glossary-term" data-term="isin">ISIN</span> code for the bankable security, linking the on-chain event to the traditional settlement system.</td>
                </tr>
                <tr>
                    <td><strong><code>DistributionPaid</code></strong></td>
                    <td><code>offering</code>, <code>epoch</code>, <code>total_amount</code></td>
                    <td>Notifies all investor grains that a distribution is available for claiming. The <code>epoch</code> field identifies the distribution period (e.g., Q1 2025), and <code>total_amount</code> represents the aggregate payout. Individual per-token amounts are calculated from the <code>DistributionRecord</code> PDA.</td>
                </tr>
                <tr>
                    <td><strong><code>ComplianceViolation</code></strong></td>
                    <td><code>offering</code>, <code>investor</code>, <code>reason</code></td>
                    <td>Alerts the DAO Manager Grain and Compliance Grain when a transaction is rejected for compliance reasons. The <code>reason</code> field is a structured enum — not a free-text string — covering cases like <code>ExpiredKYC</code>, <code>JurisdictionMismatch</code>, <code>LockUpActive</code>, <code>AccreditationInsufficient</code>, and <code>InvestorLimitReached</code>. Every violation is written to the regulatory audit log.</td>
                </tr>
                <tr>
                    <td><strong><code>TransferCompleted</code></strong></td>
                    <td><code>offering</code>, <code>from</code>, <code>to</code>, <code>amount</code></td>
                    <td>Updates the cap table in the Offering Grain and confirms trade settlement in the <span class="glossary-term" data-term="broker-dealer">Broker</span> Grain. This event fires only after all compliance checks have passed — if you see a <code>TransferCompleted</code> event, the transfer was fully compliant at the time of execution.</td>
                </tr>
            </tbody>
        </table>
        <p>Every event is also written to the Solana Event Watcher's local event log for replay capability. If a grain misses an event — network partition, grain restart, temporary outage — the watcher replays the missed events in order. No event is ever lost. This is the foundation of the platform's eventual consistency model: on-chain state is the source of truth, events are the synchronization mechanism, and replay is the recovery path.</p>
        <h2>Privacy by Design</h2>
        <p>The metadata architecture is built on a single, non-negotiable principle: <strong>no personally identifiable information ever touches the blockchain</strong>. This is not a policy preference — it is a structural constraint enforced by the schema design itself.</p>
        <ul>
            <li><strong>Jurisdiction is hashed.</strong> The <code>jurisdiction_hash</code> field stores a SHA-256 hash of the ISO country code, not the code itself. An observer reading the blockchain sees a 32-byte hash — they cannot determine the investor's country without brute-forcing 249 possible ISO codes (trivial in theory, but the point is that jurisdiction is not stored in plaintext). The Transfer Hook compares hashes, not strings. The compliance check works without ever revealing the underlying data.</li>
            <li><strong>Verification level is categorical.</strong> The <code>verification_level</code> field is an enum — <code>Basic</code>, <code>Enhanced</code>, or <code>InstitutionalEDD</code>. It tells the smart contract how thoroughly the investor was vetted. It does not reveal what documents were submitted, what the documents contained, or who the investor is. The actual verification artifacts — passport scans, proof-of-address documents, selfie captures — are encrypted with AES-256 and stored in the KYC grain's append-only journal, never on-chain.</li>
            <li><strong>Identity is a public key.</strong> Investors are identified on-chain by their wallet address — a Solana public key. The mapping between public key and real-world identity exists only in the KYC grain's encrypted journal, protected by 7-year retention policies and <span class="glossary-term" data-term="compliance">GDPR</span>-compliant cryptographic shredding (delete the encryption key to permanently erase the data).</li>
            <li><strong>Role NFTs carry authorization, not identity.</strong> A Trustee NFT proves that the holder is authorized to authenticate CrossConversions. It does not encode the trustee's name, their firm, or their license number. The mapping between NFT and real-world entity is maintained off-chain in the platform's grain journals.</li>
            <li><strong>Events carry addresses, not names.</strong> When <code>SecurityMinted</code> fires, the <code>investor</code> field is a wallet public key. When <code>ComplianceViolation</code> fires, the <code>investor</code> field is a wallet public key. At no point does any program event include a name, email, phone number, or any other PII.</li>
        </ul>
        <p>This architecture satisfies both regulatory requirements and privacy expectations. Regulators can audit compliance enforcement through on-chain events and metadata — they can verify that every transfer was compliant, every mint checked KYC credentials, and every distribution followed the waterfall rules. But they access investor identity through the off-chain KYC records, not through the blockchain. The chain proves <em>what happened</em>. The grain journals prove <em>who was involved</em>. Neither system exposes more than it needs to.</p>
    </div>
