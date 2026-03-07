---
title: "Compliance Extensions - Documentation"
description: "Beyond the Transfer Hook - credential lifecycle, emergency powers, feature flags, jurisdictional adaptability."
ogImage: "/og-image.png"
keywords: ["compliance extensions", "transfer hook", "credential lifecycle", "emergency powers", "feature flags", "jurisdictional adaptability", "regulatory reporting", "Form D", "Blue Sky", "AML", "K-1"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/docs.css"
heroDesc: "The Transfer Hook enforces the rules. Everything on this page extends those rules into credential lifecycle, emergency powers, jurisdictional adaptability, and regulatory reporting."
draft: false
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.5
  changefreq: "monthly"
ogtype: "article"
---
<h2>Overview</h2>
        <p>The SPL-2022 <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> is the enforcement core - five checks, executed by the <a href="/knowledge/glossary/solana/">Solana</a> runtime on every transfer, with no bypass path. But compliance for regulated securities does not end at transfers. Credentials expire. Regulators issue subpoenas. Courts order seizures. Jurisdictions change their rules. Tax authorities demand filings.</p>
        <p>Compliance extensions are the mechanisms that handle everything the Transfer Hook does not: the lifecycle of <span class="glossary-term" data-term="kyc">KYC</span> credentials between transfers, the emergency powers that override normal operations under legal authority, the feature flags that let issuers adapt offering behavior without redeploying contracts, the jurisdictional rules that vary across regulatory regimes, and the reporting grain that turns on-chain state into regulatory filings.</p>
        <p>None of these extensions weaken the Transfer Hook. They extend the compliance surface around it - covering the full regulatory lifecycle from credential issuance through investor exit and tax reporting.</p>
        <h2>Transfer Hook Extensions</h2>
        <p>The SPL-2022 Transfer Hook enforces five compliance checks on every <span class="glossary-term" data-term="security-token">security token</span> transfer. These checks are executed by the Solana runtime itself - not by application logic, not by an API gateway, not by anything that can be bypassed. The five checks, in order:</p>
        <ol>
            <li><strong>KYC Validity</strong> - Both sender and receiver must hold valid, unexpired KYC Credential NFTs with <code>aml_clear: true</code> and <code>pep_clear: true</code>.</li>
            <li><strong>Lock-Up Period</strong> - The sender's <code>InvestorPosition</code> <span class="glossary-term" data-term="pda">PDA</span> must show a <code>locked_until</code> timestamp in the past. <span class="glossary-term" data-term="reg-d">Reg D</span> lock-ups are typically 6–12 months.</li>
            <li><strong>Jurisdiction Whitelist</strong> - The receiver's <code>jurisdiction_hash</code> must appear in the offering's <code>ComplianceConfig</code> <code>allowed_jurisdictions</code> list.</li>
            <li><strong>Accreditation Tier</strong> - The receiver's <code>investor_class</code> must meet or exceed the offering's accreditation requirement.</li>
            <li><strong>Investor Count</strong> - If the receiver is a new investor, the offering's current investor count must be below <code>max_investors</code>.</li>
        </ol>
        <p>If any check fails, the entire transaction reverts. The tokens do not move. A <code>ComplianceViolation</code> event is emitted with the specific failure reason. See the <a href="/knowledge/docs/transfer-rules/">Transfer Rules documentation</a> for the complete enforcement mechanism, including the execution flow and the architectural guarantee that no transfer - from any program, including raw SPL Token calls and DEX interactions - can bypass these checks.</p>
        <p>Everything that follows on this page builds on this foundation. The Transfer Hook is the floor. Compliance extensions are the rest of the building.</p>
        <h2>Credential Lifecycle</h2>
        <p>KYC Credential NFTs are not permanent. They carry an <code>expires_at</code> timestamp, and when that timestamp passes, the credential is treated identically to no credential at all - the Transfer Hook rejects any transfer involving an expired credential. This is by design: regulatory verification decays. An investor verified 18 months ago may have changed jurisdiction, lost accreditation status, or become a politically exposed person.</p>
        <h3>Expiration Tracking</h3>
        <p>The platform does not wait for expiration to cause a failed transfer. The KYC Grain proactively tracks credential expiration windows and initiates re-verification before credentials expire:</p>
        <table>
            <thead>
                <tr>
                    <th>Window</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>90 days before expiry</strong></td>
                    <td>Informational notification sent to the investor. No restrictions applied.</td>
                </tr>
                <tr>
                    <td><strong>30 days before expiry</strong></td>
                    <td>Re-verification workflow triggered. Investor receives instructions and a deadline. Existing credential remains valid.</td>
                </tr>
                <tr>
                    <td><strong>7 days before expiry</strong></td>
                    <td>Escalation to the <span class="glossary-term" data-term="broker-dealer">Broker-Dealer</span> and Platform Operator. Warning displayed on investor dashboard.</td>
                </tr>
                <tr>
                    <td><strong>Expiration (T+0)</strong></td>
                    <td>Credential becomes invalid. Transfer Hook rejects all transfers involving this wallet. Distribution claims are blocked. Minting is blocked.</td>
                </tr>
            </tbody>
        </table>
        <h3>Mid-Holding Expiration</h3>
        <p>When a credential expires while an investor holds tokens, the tokens are not seized, burned, or moved. The investor still owns them - ownership is a legal right that does not evaporate because a KYC check expired. What changes is the investor's ability to <em>act</em> on those tokens:</p>
        <ul>
            <li><strong>Transfers out:</strong> Blocked. The Transfer Hook rejects any outgoing transfer from a wallet with an expired credential.</li>
            <li><strong>Transfers in:</strong> Blocked. The Transfer Hook rejects any incoming transfer to a wallet with an expired credential.</li>
            <li><strong>Distribution claims:</strong> Blocked. Unclaimed distributions accrue and are released once the credential is renewed.</li>
            <li><strong><span class="glossary-term" data-term="crossconversion">CrossConversion</span> requests:</strong> Blocked. No conversion to or from traditional securities until re-verification is complete.</li>
            <li><strong>Voting and governance:</strong> Unaffected. Token-weighted governance rights are tied to ownership, not credential status.</li>
        </ul>
        <p>Once the investor completes re-verification and a fresh KYC Credential NFT is minted to their wallet, all capabilities are restored immediately. There is no grace period in either direction - invalid means invalid, valid means valid.</p>
        <h3>Credential Revocation</h3>
        <p>Separate from expiration, a credential can be actively revoked by a compliance officer. Revocation sets <code>aml_clear</code> or <code>pep_clear</code> to false on the credential, which causes the Transfer Hook to reject transfers even if the credential has not expired. Revocation is logged as a critical-severity audit event and requires a documented reason. Common triggers: updated sanctions list match, law enforcement request, adverse media screening hit.</p>
        <h2>Emergency Powers</h2>
        <p>Emergency powers are compliance safety valves - operations that override normal rules under legal authority. They exist because regulated securities operate within a legal system that can compel action. These are not everyday operations. Every invocation is logged, audited, and requires cryptographic proof of authorization.</p>
        <h3>Account Freezing</h3>
        <p>The <code>freeze_account</code> instruction locks an investor's position entirely - no transfers, no sales, no <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, no distribution claims - until the freeze is lifted.</p>
        <table>
            <thead>
                <tr>
                    <th>Aspect</th>
                    <th>Detail</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Authorization</strong></td>
                    <td>Requires Security Admin NFT from the <span class="glossary-term" data-term="melusina">Melusina</span> Admin NFT system (<code>level=Security</code>).</td>
                </tr>
                <tr>
                    <td><strong>Effect</strong></td>
                    <td>Sets a frozen flag on the <code>InvestorPosition</code> PDA. The Transfer Hook checks this flag and rejects all outgoing transfers.</td>
                </tr>
                <tr>
                    <td><strong>Unfreezing</strong></td>
                    <td>Same authorization level. Both freeze and unfreeze reasons are logged to the audit trail.</td>
                </tr>
                <tr>
                    <td><strong>Emergency Freeze</strong></td>
                    <td>For high-urgency situations where the Security Admin NFT is unavailable, a 2-of-3 <span class="glossary-term" data-term="threshold-signing">threshold signing</span> ceremony can freeze an account.</td>
                </tr>
                <tr>
                    <td><strong>Audit</strong></td>
                    <td>Every freeze/unfreeze is logged with actor wallet, NFT role, timestamp, and reason. 7-year retention.</td>
                </tr>
            </tbody>
        </table>
        <p>Account freezing is a regulatory tool for <span class="glossary-term" data-term="aml">AML</span>/SAR compliance, court orders, and regulatory investigations. Every use requires a documented reason.</p>
        <h3>Forced Transfers</h3>
        <p>The <code>force_transfer</code> instruction moves tokens from one wallet to another without the sender's consent. It is the most restricted operation in the entire program - a power that exists solely for court-ordered transfers and regulatory enforcement actions.</p>
        <table>
            <thead>
                <tr>
                    <th>Requirement</th>
                    <th>Detail</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Keyholder Threshold</strong></td>
                    <td>3-of-5 <span class="glossary-term" data-term="master-nft">Master NFT</span> keyholder <span class="glossary-term" data-term="threshold-signing">threshold signing</span>. Three separate keyholders, using hardware wallets, in three separate locations, must independently sign.</td>
                </tr>
                <tr>
                    <td><strong>Court Order Hash</strong></td>
                    <td>A SHA-256 hash of the court order document must be included in the instruction. This hash is stored on-chain permanently - cryptographic proof that a legal basis existed.</td>
                </tr>
                <tr>
                    <td><strong>Parameters</strong></td>
                    <td><code>from</code>, <code>to</code>, <code>amount</code>, <code>court_order_hash</code> (SHA-256 of the court order document).</td>
                </tr>
                <tr>
                    <td><strong>Compliance Bypass</strong></td>
                    <td>Force transfer bypasses standard Transfer Hook checks (lock-up, jurisdiction, accreditation). The court order supersedes contract-level rules. The destination wallet's KYC status is still recorded.</td>
                </tr>
                <tr>
                    <td><strong>Audit</strong></td>
                    <td>Critical-severity audit event. All signing keyholders recorded. Court order hash stored immutably on-chain. Notification sent to all platform operators and the <span class="glossary-term" data-term="trustee">Trustee</span>.</td>
                </tr>
            </tbody>
        </table>
        <p>Three keyholders must agree. A court order must be on record. The action is visible on-chain permanently. Maximum transparency, maximum auditability, maximum friction - by design.</p>
        <h3>Emergency Pause</h3>
        <p>All programs include a <code>pause</code> instruction gated by the Security Admin NFT. When invoked, the pause halts all transfer, minting, and distribution operations for a specific offering. This is a circuit-breaker for scenarios such as: a discovered vulnerability in a third-party integration, a regulatory halt order, or a disputed cap table state that requires reconciliation before trading resumes.</p>
        <p>Pause is per-offering, not platform-wide. One offering can be paused while all others continue operating normally. Unpausing requires the same Security Admin NFT authorization and is logged identically.</p>
        <h2>Feature Flags</h2>
        <p>The <code>ComplianceConfig</code> PDA includes a <code>features</code> field - a 64-bit bitmask that controls which capabilities are enabled for a given offering. Feature flags allow issuers to enable or disable specific behaviors without redeploying or migrating the <span class="glossary-term" data-term="smart-contract">smart contract</span>.</p>
        <pre><code>ComplianceConfig.features: u64 (bitmask)
├── Bit 0:  PAUSE_TRADING          // Halt all secondary transfers
├── Bit 1:  RESTRICT_CROSSCONV     // Disable CrossConversion for this offering
├── Bit 2:  REQUIRE_ACCREDITATION  // Enforce accredited investor check
├── Bit 3:  ENFORCE_LOCKUP         // Enforce lock-up period on transfers
├── Bit 4:  ENABLE_DISTRIBUTIONS   // Allow distribution claims
├── Bit 5:  ENABLE_VOTING          // Allow token-weighted governance
├── Bit 6:  RESTRICT_FLOWBACK      // Reg S flowback prevention
├── Bit 7:  ENABLE_OTC_MATCHING    // Allow OTC secondary trading
├── ...
└── Bit 63: RESERVED               // Reserved for future use</code></pre>
        <h3>How Feature Flags Are Checked</h3>
        <p>Each instruction that is gated by a feature flag reads the offering's <code>ComplianceConfig</code> PDA and performs a bitwise AND against the relevant flag. If the bit is not set, the instruction returns a <code>FeatureDisabled</code> error. This check happens before any other validation - a disabled feature fails fast, costs minimal compute, and produces a clear error.</p>
        <pre><code>// Pseudocode: feature flag check
let config = ComplianceConfig::load(offering_id)?;
if config.features & PAUSE_TRADING != 0 {
    return Err(ComplianceError::TradingPaused);
}
// Proceed with transfer checks...</code></pre>
        <h3>Modification Rules</h3>
        <p>Feature flags are modifiable by the Issuer with Platform Operator approval. Every modification is logged to the audit trail with the previous value, the new value, and the reason for the change. Certain flags - such as <code>PAUSE_TRADING</code> - can also be set via emergency powers (Security Admin NFT) without Issuer initiation, for regulatory halt scenarios.</p>
        <p>The bitmask design supports up to 64 independent features. New capabilities can be added to the smart contract and gated behind unused bits without modifying existing flag assignments or requiring data migration.</p>
        <h2>Jurisdictional Adaptability</h2>
        <p>Securities regulations vary by jurisdiction - and a platform that only handles US <span class="glossary-term" data-term="reg-d">Reg D</span> and <span class="glossary-term" data-term="reg-s">Reg S</span> will not scale internationally. The compliance extensions are designed for jurisdictional adaptability: each offering carries its own jurisdiction configuration, and the framework supports regulatory regimes beyond US securities law.</p>
        <h3>Per-Offering Jurisdiction Whitelists</h3>
        <p>Every offering's <code>ComplianceConfig</code> PDA contains an <code>allowed_jurisdictions</code> list - SHA-256 hashes of ISO 3166-1 country codes. The Transfer Hook compares the receiver's <code>jurisdiction_hash</code> against this list on every transfer. The hashing preserves investor privacy: the blockchain does not reveal which country an investor is in.</p>
        <table>
            <thead>
                <tr>
                    <th>Regulatory Regime</th>
                    <th>Jurisdiction Configuration</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-d">Reg D</span> 506(b/c)</strong></td>
                    <td>US-only. Only wallets with US jurisdiction hash can receive tokens.</td>
                    <td>Active</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-s">Reg S</span></strong></td>
                    <td>Non-US only. US jurisdiction hash explicitly excluded. Flowback restrictions enforced via the <code>RESTRICT_FLOWBACK</code> feature flag during the distribution compliance period.</td>
                    <td>Active</td>
                </tr>
                <tr>
                    <td><strong>Dual Reg D + Reg S</strong></td>
                    <td>Segregated token mints - separate US (Reg D) and non-US (Reg S) tranches, each with its own <code>ComplianceConfig</code>. Cross-tranche transfers blocked.</td>
                    <td>Active</td>
                </tr>
                <tr>
                    <td><strong>EU MiFID II</strong></td>
                    <td>EU member state hashes whitelisted. <span class="glossary-term" data-term="accredited-investor">Accreditation</span> tier mapped to MiFID II investor classification (Retail, Professional, Eligible Counterparty). Requires additional credential fields for LEI and national ID scheme.</td>
                    <td>Planned</td>
                </tr>
                <tr>
                    <td><strong>UK FCA</strong></td>
                    <td>UK jurisdiction hash whitelisted post-Brexit, separate from EU. FCA investor categorization (Restricted, High Net Worth, Sophisticated, Professional) mapped to <code>investor_class</code> tiers.</td>
                    <td>Planned</td>
                </tr>
                <tr>
                    <td><strong>Singapore MAS</strong></td>
                    <td>SG jurisdiction hash. MAS accredited investor threshold (SGD 2M net assets or SGD 300K annual income) mapped to accreditation tier. Capital Markets Services licence requirements enforced at the Broker NFT level.</td>
                    <td>Planned (APAC)</td>
                </tr>
                <tr>
                    <td><strong>Hong Kong SFC</strong></td>
                    <td>HK jurisdiction hash. SFC professional investor classification (HKD 8M portfolio threshold) mapped to <code>investor_class</code>. Type 1 / Type 9 licence requirements enforced at the platform operator level.</td>
                    <td>Planned (APAC)</td>
                </tr>
                <tr>
                    <td><strong>Restricted Jurisdictions</strong></td>
                    <td>OFAC-sanctioned jurisdiction hashes are never included in any offering's whitelist. KYC Credential NFTs are never issued for sanctioned jurisdictions - double enforcement.</td>
                    <td>Active</td>
                </tr>
            </tbody>
        </table>
        <h3>Future-Proofing</h3>
        <p>The jurisdiction model is deliberately generic: a whitelist of hashes, an accreditation tier enum, and a regulatory exemption enum. Adding a new regulatory regime does not require smart contract changes - it requires:</p>
        <ol>
            <li>Adding the new jurisdiction's country code hash to the relevant offerings' <code>allowed_jurisdictions</code> lists.</li>
            <li>Mapping the regime's investor classification to existing <code>investor_class</code> tiers (or extending the enum if no existing tier fits).</li>
            <li>Configuring the KYC Grain to perform the jurisdiction-specific verification workflow.</li>
            <li>Adding the regime's reporting requirements to the compliance-grain.</li>
        </ol>
        <p>The smart contract enforces the rules. The off-chain grains handle the jurisdiction-specific logic. This separation means the on-chain program does not need to know anything about MiFID II or MAS regulations - it only needs to know whether a hash is in a list and whether a tier meets a threshold.</p>
        <h2>Audit &amp; Reporting Extensions</h2>
        <p>Compliance is not just enforcement - it is reporting. The compliance-grain (a Go service in the <span class="glossary-term" data-term="sandstorm">Sandstorm</span> actor framework) generates the regulatory filings and reports that securities law requires. These reports are derived from on-chain state and grain journal records - not from a separate database that might drift from the source of truth.</p>
        <h3>Regulatory Filings</h3>
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
                    <td>Notice of exempt offering of securities. Generated as XML validated against the SEC EDGAR schema. Must be filed within 15 days of the first sale of securities. Annual amendments filed to update investor counts and amounts raised.</td>
                </tr>
                <tr>
                    <td><strong>Blue Sky Filings</strong></td>
                    <td>State regulators</td>
                    <td>Per state, per offering</td>
                    <td>State-level securities exemption filings. The compliance-grain tracks per-state exemptions, investor counts, and filing deadlines. States vary widely - some accept federal filing, others require separate state-specific forms.</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="aml">AML</span>/SAR</strong></td>
                    <td>FinCEN</td>
                    <td>As needed</td>
                    <td>Suspicious Activity Reports. Automated flagging based on transaction patterns (unusual volume, rapid transfers near lock-up expiry, structuring patterns). Human compliance officer review before filing - the system flags, a person decides.</td>
                </tr>
                <tr>
                    <td><strong>K-1</strong></td>
                    <td>IRS</td>
                    <td>Annual</td>
                    <td>Schedule K-1 (Partner's Share of Income) for LLC pass-through taxation. Generated from on-chain <span class="glossary-term" data-term="distributions">distribution</span> records and <span class="glossary-term" data-term="cap-table">cap table</span> snapshots at tax year end. Each investor receives a K-1 reflecting their proportional share.</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-s">Reg S</span> Compliance</strong></td>
                    <td>SEC</td>
                    <td>Ongoing</td>
                    <td>Non-US investor tracking, flowback restriction enforcement, and distribution compliance period monitoring. Ensures tokens do not flow back to US wallets during the restricted period.</td>
                </tr>
                <tr>
                    <td><strong>Cap Table Snapshots</strong></td>
                    <td>Internal / Auditors</td>
                    <td>On demand</td>
                    <td>Ownership snapshots pulled directly from on-chain state. Immutable, verifiable, and exportable in standard formats for auditor consumption.</td>
                </tr>
            </tbody>
        </table>
        <h3>Audit Trail</h3>
        <p>Every action across every grain and smart contract is logged to an append-only audit trail. This is not optional and cannot be disabled. The audit event structure:</p>
        <pre><code>AuditEvent {
    id,               // Unique event identifier
    timestamp,        // Precise event time
    severity,         // info | warning | critical
    category,         // auth | transfer | compliance | governance
    actor_id,         // Wallet address of the actor
    actor_type,       // NFT role (Operator, Trustee, Broker, etc.)
    action,           // What was done
    resource,         // What it was done to
    resource_type,    // Offering, investor, distribution, etc.
    success,          // Whether the action succeeded
    error_message,    // Failure reason (if applicable)
    grain_id,         // Which grain processed the action
    offering_id,      // Which offering was affected
    series_id,        // Which Series LLC
    metadata          // Additional context (JSON)
}</code></pre>
        <p><strong>Seven-year retention</strong> - required by SEC regulations for broker-dealer and investment adviser records. Every audit event is written to the grain's append-only journal, encrypted at rest with AES-256, and replicated for durability. After the 7-year retention period, automated purge with legal hold override ensures data is retained only as long as legally required.</p>
        <h3>Audit Export</h3>
        <p>The compliance-grain supports full audit trail export in standard formats for external auditors, regulators, and legal counsel. Exports can be filtered by offering, date range, severity, category, and actor. The export includes cryptographic integrity proofs - an auditor can verify that no events have been tampered with or omitted from the export.</p>
        <p>Grain journals support deterministic replay: given the same sequence of audit events, the grain reconstructs identical state. This is the disaster recovery mechanism - restore the journal, replay the events, verify the state. The log is the truth.</p>
    </div>
