---
title: "Compliance Framework - Documentation"
description: "KYC credential NFTs, ComplianceConfig PDAs, transfer enforcement, regulatory reporting, and the 7-year audit trail — compliance as code, not as afterthought."
ogImage: "/og-image.png"
keywords: ["compliance", "KYC", "regulatory reporting", "audit trail", "accredited investor", "Reg D"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">Compliance Framework</h1>
    <p class="section-desc">Compliance encoded in smart contracts and enforced at the protocol level — because paper policies don't stop non-compliant transfers.</p>
</section>

<section class="features-section">
    <div class="container">

        <h2>KYC Credential System</h2>
        <p>Every investor on the Sails.to platform carries a <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT — an on-chain attestation of their verified identity, classification, and regulatory status. This NFT contains <strong>zero personally identifiable information</strong>. No names, no addresses, no document images. Only cryptographic proofs and classification flags that the <span class="glossary-term" data-term="smart-contract">smart contract</span> needs to enforce compliance rules.</p>
        <p>The KYC Credential NFT metadata structure:</p>

        <pre><code>KYC NFT Metadata (on-chain, no PII):
├── investor_class: enum { Accredited, Professional, QualifiedPurchaser, Retail }
├── jurisdiction_hash: [u8; 32]   // SHA256 of ISO country code, anonymized
├── reg_exemption: enum { RegD506b, RegD506c, RegS, RegA, RegCF }
├── verification_level: enum { Basic, Enhanced, InstitutionalEDD }
├── issued_by: Pubkey             // Licensed KYC provider's license NFT
├── issued_at: i64                // Unix timestamp
├── expires_at: i64               // Credential expiration
├── aml_clear: bool               // Anti-money laundering clearance
└── pep_clear: bool               // Politically exposed person clearance</code></pre>

        <p>The <code>investor_class</code> determines which offerings an investor can access. An <span class="glossary-term" data-term="accredited-investor">Accredited Investor</span> can participate in <span class="glossary-term" data-term="reg-d">Reg D 506(b)</span> and 506(c) offerings. A <span class="glossary-term" data-term="professional-investor">Professional Investor</span> can access institutional tranches. A Retail investor is limited to <span class="glossary-term" data-term="reg-d">Reg A</span> and Reg CF offerings. The smart contract checks this on every mint, every transfer, every distribution claim.</p>
        <p>The <code>jurisdiction_hash</code> is a SHA-256 hash of the investor's ISO country code — anonymized so that the blockchain reveals nothing about the investor's location, but the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> can still enforce jurisdiction whitelists by comparing hashes.</p>
        <p>Credentials expire. When <code>expires_at</code> passes, the investor's KYC is no longer valid, and the smart contract will reject any new minting or transfer operations until a fresh credential is issued. The platform does not wait for expiration to bite — the KYC Grain tracks expiration windows and triggers re-verification workflows proactively.</p>

        <h2>Compliance Configuration</h2>
        <p>Every offering on the platform carries a <code>ComplianceConfig</code> <span class="glossary-term" data-term="pda">PDA</span> — a Program Derived Address account that encodes the regulatory constraints for that specific offering. This is compliance as data, stored on-chain, immutable once set (modifiable only by the Issuer with Platform Operator approval):</p>

        <pre><code>ComplianceConfig PDA Fields:
├── offering_id: Pubkey            // The offering this config governs
├── allowed_jurisdictions: Vec&lt;[u8; 32]&gt;  // SHA256 hashes of allowed ISO codes
├── min_investment: u64            // Minimum investment amount (in cents)
├── lock_up_days: u32              // Mandatory holding period before transfer
├── max_investors: u32             // Maximum number of investors (e.g., 2000 for Reg D)
├── accreditation_required: bool   // Whether accredited status is mandatory
├── reg_exemption: enum            // Which regulatory exemption applies
├── features: u64                  // Bitmask for feature flags (pause, etc.)
└── version: u8                    // PDA version for migration support</code></pre>

        <p>The <code>max_investors</code> field is critical for <span class="glossary-term" data-term="reg-d">Reg D</span> offerings — 506(b) limits non-accredited investors to 35, while the total investor count must remain under SEC thresholds. The smart contract tracks the current investor count in the <code>OfferingState</code> PDA and rejects any mint that would exceed the limit.</p>
        <p>The <code>lock_up_days</code> field enforces mandatory holding periods. For Reg D securities, this is typically 6-12 months. The <code>transfer_with_compliance</code> instruction checks the investor's <code>locked_until</code> timestamp against the current slot time — if the lock-up hasn't expired, the transfer is rejected at the protocol level.</p>

        <h2>Transfer Enforcement</h2>
        <p>Every token transfer on the platform passes through compliance enforcement. There are no unverified transfers. The <code>transfer_with_compliance</code> instruction performs the following checks before allowing any movement of <span class="glossary-term" data-term="security-token">security tokens</span>:</p>

        <ol>
            <li><strong>KYC Validity:</strong> Both the sender and receiver must hold valid, unexpired KYC Credential NFTs. If either credential has expired or been revoked, the transfer is rejected.</li>
            <li><strong>Lock-Up Period:</strong> The sender's <code>locked_until</code> timestamp must be in the past. If the mandatory holding period hasn't elapsed, the transfer is rejected.</li>
            <li><strong>Jurisdiction Whitelist:</strong> The receiver's <code>jurisdiction_hash</code> must appear in the offering's <code>allowed_jurisdictions</code> list. A <span class="glossary-term" data-term="reg-s">Reg S</span> offering restricted to non-US investors will reject any transfer to a US-jurisdiction wallet.</li>
            <li><strong>Accreditation Tier:</strong> The receiver must meet the offering's accreditation requirements. A <span class="glossary-term" data-term="reg-d">Reg D 506(c)</span> offering requires the receiver to be an <span class="glossary-term" data-term="accredited-investor">Accredited Investor</span> or above.</li>
            <li><strong>Investor Count:</strong> The transfer must not cause the offering to exceed its <code>max_investors</code> limit (relevant when the receiver is a new investor, not an existing holder).</li>
        </ol>

        <p>These checks are enforced by the SPL-2022 <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> — a program extension that the Solana runtime invokes on every token transfer. Non-compliant transfers are not logged and ignored; they are <strong>rejected</strong>. The tokens do not move. See the <a href="/knowledge/docs/transfer-rules/">Transfer Rules documentation</a> for the complete enforcement mechanism.</p>

        <h2>Regulatory Reporting</h2>
        <p>Compliance is not just enforcement — it is reporting. The platform generates the following regulatory filings and reports, automated where possible, human-reviewed where required:</p>

        <table>
            <thead>
                <tr>
                    <th>Report</th>
                    <th>Authority</th>
                    <th>Frequency</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Form D</strong></td>
                    <td>SEC (EDGAR)</td>
                    <td>Per offering + annual amendment</td>
                    <td>Notice of exempt offering. Generated as XML validated against the SEC EDGAR schema. Filed within 15 days of first sale.</td>
                </tr>
                <tr>
                    <td><strong>Blue Sky Filings</strong></td>
                    <td>State regulators</td>
                    <td>Per state, per offering</td>
                    <td>State-level securities exemption filings. The platform tracks per-state exemptions and investor counts to ensure <span class="glossary-term" data-term="compliance">compliance</span> with each state's requirements.</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="aml">AML</span>/SAR</strong></td>
                    <td>FinCEN</td>
                    <td>As needed</td>
                    <td>Suspicious Activity Reports. Automated flagging based on transaction patterns, with human compliance officer review before filing.</td>
                </tr>
                <tr>
                    <td><strong>K-1</strong></td>
                    <td>IRS</td>
                    <td>Annual</td>
                    <td>Partner's share of income for LLC pass-through taxation. Generated from on-chain <span class="glossary-term" data-term="distributions">distribution</span> records and <span class="glossary-term" data-term="cap-table">cap table</span> snapshots at tax year end.</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-s">Reg S</span> Compliance</strong></td>
                    <td>SEC</td>
                    <td>Ongoing</td>
                    <td>Non-US investor tracking, flowback restrictions, and distribution compliance period monitoring.</td>
                </tr>
                <tr>
                    <td><strong>Cap Table Snapshots</strong></td>
                    <td>Internal / Auditors</td>
                    <td>On demand</td>
                    <td>Ownership snapshots pulled directly from on-chain state. Immutable, verifiable, and exportable in standard formats.</td>
                </tr>
            </tbody>
        </table>

        <p>The Regulatory Reporting Grain (a compliance-grain in Go) automates the generation of these reports. Form D XML is validated against the SEC EDGAR schema before submission. Blue Sky filings track per-state investor counts. AML/SAR flagging uses rule-based detection with human review — the system flags, a compliance officer decides.</p>

        <h2>Audit Trail</h2>
        <p>Every action across every grain and smart contract is logged. This is not optional, not configurable, not something that can be turned off for performance reasons. The audit trail is the regulatory backbone of the platform:</p>

        <pre><code>AuditEvent {
    id,                    // Unique event identifier
    timestamp,             // Precise event time
    severity,              // info, warning, critical
    category,              // auth, transfer, compliance, governance
    actor_id,              // Wallet address
    actor_type,            // NFT role (Operator, Trustee, Broker, etc.)
    action,                // What was done
    resource,              // What it was done to
    resource_type,         // Offering, investor, distribution, etc.
    success,               // Whether the action succeeded
    error_message,         // Why it failed (if applicable)
    grain_id,              // Which grain processed the action
    offering_id,           // Which offering was affected
    series_id,             // Which Series LLC
    metadata               // Additional context (JSON)
}</code></pre>

        <p><strong>Seven-year retention</strong> — required by SEC regulations for broker-dealer records and investment adviser records. Every audit event is written to the grain's append-only journal, encrypted at rest with AES-256, and replicated for durability. After the 7-year period, automated purge with legal hold override ensures data is retained only as long as required.</p>
        <p>The audit trail is not just for regulators. It is the system's memory. Grain journals support deterministic replay — given the same sequence of audit events, the grain reconstructs the identical state. This is how disaster recovery works: restore the journal, replay the events, verify the state. No backup snapshots needed. The log <em>is</em> the truth.</p>

    </div>
</section>
