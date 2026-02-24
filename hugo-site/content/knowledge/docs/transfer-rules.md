---
title: "Transfer Rules - Documentation"
description: "Transfer compliance checks, the SPL-2022 Transfer Hook mechanism, account freezing, forced transfers."
ogImage: "/og-image.png"
keywords: ["transfer rules", "transfer hook", "compliance", "account freezing", "forced transfer", "jurisdiction"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/docs.css"
heroDesc: "Protocol-level enforcement — non-compliant transfers don't get logged and ignored, they get rejected."
draft: false
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.5
  changefreq: "monthly"
ogtype: "article"
---
<h2>Transfer Compliance Checks</h2>
        <p>The <code>transfer_with_compliance</code> instruction is the gate through which every <span class="glossary-term" data-term="security-token">security token</span> transfer must pass. It performs five checks in sequence. If any check fails, the entire transaction reverts — the tokens do not move, and a <code>ComplianceViolation</code> event is emitted with the specific reason for rejection.</p>
        <h3>Check 1: KYC Validity</h3>
        <p>Both the sender and receiver wallets must hold valid, unexpired <span class="glossary-term" data-term="kyc">KYC</span> Credential NFTs. The instruction reads the <code>expires_at</code> field on each credential and compares it to the current slot time. An expired credential is treated the same as no credential — the transfer is rejected.</p>
        <p>Additionally, both credentials must have <code>aml_clear: true</code> and <code>pep_clear: true</code>. If either flag has been revoked since the credential was issued (via a compliance officer action), the transfer is rejected.</p>
        <h3>Check 2: Lock-Up Period</h3>
        <p>The sender's <code>InvestorPosition</code> <span class="glossary-term" data-term="pda">PDA</span> contains a <code>locked_until</code> timestamp. For <span class="glossary-term" data-term="reg-d">Reg D</span> securities, this is typically set to 6-12 months after the initial purchase. The instruction compares <code>locked_until</code> against the current slot time. If the lock-up period has not elapsed, the transfer is rejected — no exceptions, no overrides (except <code>force_transfer</code> with court order, see below).</p>
        <h3>Check 3: Jurisdiction Whitelist</h3>
        <p>The receiver's KYC Credential NFT contains a <code>jurisdiction_hash</code> — a SHA-256 hash of their ISO country code. The instruction reads the offering's <code>ComplianceConfig</code> PDA and checks whether this hash appears in the <code>allowed_jurisdictions</code> list. A <span class="glossary-term" data-term="reg-s">Reg S</span> offering that excludes US investors will reject any transfer to a wallet whose jurisdiction hash matches the US code hash.</p>
        <h3>Check 4: Accreditation Tier</h3>
        <p>The receiver's KYC Credential NFT contains an <code>investor_class</code> field: <span class="glossary-term" data-term="accredited-investor">Accredited</span>, <span class="glossary-term" data-term="professional-investor">Professional</span>, Qualified Purchaser, or Retail. The instruction checks this against the offering's accreditation requirements. A <span class="glossary-term" data-term="reg-d">Reg D 506(c)</span> offering requires Accredited status or above — a Retail investor cannot receive these tokens, period.</p>
        <h3>Check 5: Investor Count</h3>
        <p>If the receiver does not already hold tokens in this offering (i.e., this transfer would create a new investor position), the instruction checks the offering's current investor count against the <code>max_investors</code> limit in the <code>ComplianceConfig</code>. Reg D offerings have strict investor count limits — the program enforces them at the protocol level.</p>
        <h2>Transfer Hook Mechanism</h2>
        <p>The compliance checks described above are not merely enforced by the <code>sails_securities</code> program — they are enforced by the SPL-2022 <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span>, which operates at a lower level in the <a href="/knowledge/glossary/solana/">Solana</a> runtime.</p>
        <p>Here is what this means in practice: even if someone bypasses the <code>sails_securities</code> program entirely and calls the SPL Token program directly to transfer Sails security tokens, the Transfer Hook is <em>still invoked</em>. The Solana runtime calls the hook on every transfer of a token mint that has the Transfer Hook extension enabled. There is no way to move tokens without passing through the compliance checks.</p>
        <p>The Transfer Hook execution flow:</p>
        <ol>
            <li>A transfer instruction is submitted to the Solana runtime (via any program — <code>sails_securities</code>, raw SPL Token, a DEX, anything).</li>
            <li>The runtime detects that the token mint has a Transfer Hook extension configured.</li>
            <li>The runtime invokes the Transfer Hook program with the transfer details: source wallet, destination wallet, amount, and the mint address.</li>
            <li>The hook program reads the KYC Credential NFTs on both wallets, the <code>ComplianceConfig</code> PDA, and the sender's <code>InvestorPosition</code> PDA.</li>
            <li>If all five compliance checks pass, the hook returns success and the transfer proceeds.</li>
            <li>If any check fails, the hook returns an error. The <strong>entire transaction is reverted</strong>. The tokens do not move. A <code>ComplianceViolation</code> event is emitted.</li>
        </ol>
        <p>This is the critical architectural decision: compliance is not enforced by application logic that can be bypassed. It is enforced by the Solana runtime itself. The Transfer Hook is as inescapable as gravity.</p>
        <h2>Account Freezing</h2>
        <p>The <code>freeze_account</code> instruction locks an investor's position — preventing all transfers, sales, <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, and distribution claims until the freeze is lifted.</p>
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
                    <td>Requires Security Admin NFT (from the <span class="glossary-term" data-term="melusina">Melusina</span> Admin NFT system, level=Security)</td>
                </tr>
                <tr>
                    <td><strong>Parameters</strong></td>
                    <td><code>investor_wallet</code> — the wallet to freeze; <code>reason</code> — logged to audit trail</td>
                </tr>
                <tr>
                    <td><strong>Effect</strong></td>
                    <td>Sets a frozen flag on the <code>InvestorPosition</code> PDA. The Transfer Hook checks this flag and rejects all outgoing transfers. Distribution claims are blocked. CrossConversion requests are blocked.</td>
                </tr>
                <tr>
                    <td><strong>Unfreezing</strong></td>
                    <td>Same authorization level (Security Admin NFT). Reason for unfreeze also logged.</td>
                </tr>
                <tr>
                    <td><strong>Emergency Freeze</strong></td>
                    <td>For high-urgency situations, a 2-of-3 <span class="glossary-term" data-term="threshold-signing">threshold signing</span> ceremony can freeze an account even if the Security Admin NFT is unavailable.</td>
                </tr>
                <tr>
                    <td><strong>Audit Trail</strong></td>
                    <td>Every freeze and unfreeze action is logged with the actor's wallet, NFT role, timestamp, and reason. 7-year retention.</td>
                </tr>
            </tbody>
        </table>
        <p>Account freezing is a regulatory tool. It exists for AML/SAR compliance, court orders, and regulatory investigations. It is not a general-purpose moderation feature — every use is logged, audited, and requires a documented reason.</p>
        <h2>Forced Transfers</h2>
        <p>The <code>force_transfer</code> instruction is the most restricted operation in the entire program. It moves tokens from one wallet to another <em>without the sender's consent</em> — a power that exists solely for court-ordered transfers and regulatory enforcement actions.</p>
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
                    <td>3-of-5 <span class="glossary-term" data-term="master-nft">Master NFT</span> keyholder <span class="glossary-term" data-term="threshold-signing">threshold signing</span>. Three separate keyholders, using hardware wallets, in three separate locations, must independently sign the transaction.</td>
                </tr>
                <tr>
                    <td><strong>Court Order Hash</strong></td>
                    <td>A SHA-256 hash of the court order document must be included in the instruction. This hash is stored on-chain permanently — cryptographic proof that a legal basis existed for the forced transfer.</td>
                </tr>
                <tr>
                    <td><strong>Parameters</strong></td>
                    <td><code>from</code> — source wallet; <code>to</code> — destination wallet; <code>amount</code> — token amount; <code>court_order_hash</code> — SHA-256 of the court order</td>
                </tr>
                <tr>
                    <td><strong>Compliance Bypass</strong></td>
                    <td>Force transfer <em>does</em> bypass the standard Transfer Hook compliance checks (lock-up, jurisdiction, accreditation). The court order supersedes contract-level compliance rules. However, the transfer is still logged and the destination wallet's KYC status is recorded.</td>
                </tr>
                <tr>
                    <td><strong>Audit Trail</strong></td>
                    <td>Critical-severity audit event. All 3+ signing keyholders recorded. Court order hash immutably stored on-chain. Notification sent to all platform operators and the <span class="glossary-term" data-term="trustee">Trustee</span>.</td>
                </tr>
            </tbody>
        </table>
        <p>This instruction exists because regulated securities exist in a legal system. Courts can order transfers. Regulators can mandate seizures. The platform must comply — but it does so with maximum transparency, maximum auditability, and maximum friction. Three keyholders must agree. A court order must be on record. The entire action is visible on-chain forever.</p>
        <h2>Jurisdiction Rules</h2>
        <p>Jurisdiction enforcement is one of the most critical compliance functions — especially for offerings that operate under multiple regulatory regimes simultaneously.</p>
        <h3>How Jurisdiction Matching Works</h3>
        <p>Each investor's <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT contains a <code>jurisdiction_hash</code> — a SHA-256 hash of their ISO 3166-1 country code. The offering's <code>ComplianceConfig</code> PDA contains an <code>allowed_jurisdictions</code> list of these same hashes. The Transfer Hook compares the receiver's hash against the whitelist. Match: transfer proceeds. No match: transfer rejected.</p>
        <p>The hashing serves a privacy function — the blockchain does not reveal which country an investor is in. Only the hash is stored on-chain. The Transfer Hook can verify membership in the whitelist without exposing the underlying country code.</p>
        <h3>Common Jurisdiction Configurations</h3>
        <table>
            <thead>
                <tr>
                    <th>Offering Type</th>
                    <th>Jurisdiction Rule</th>
                    <th>Effect</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-d">Reg D</span> 506(b/c)</strong></td>
                    <td>US-only</td>
                    <td>Only wallets with US jurisdiction hash can receive tokens. International investors are blocked at the Transfer Hook level.</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="reg-s">Reg S</span></strong></td>
                    <td>Non-US only</td>
                    <td>US jurisdiction hash is explicitly excluded. Flowback restrictions prevent tokens from reaching US wallets during the distribution compliance period.</td>
                </tr>
                <tr>
                    <td><strong>Dual Reg D + Reg S</strong></td>
                    <td>Segregated tranches</td>
                    <td>Separate token mints for US (Reg D) and non-US (Reg S) tranches. Each mint has its own <code>ComplianceConfig</code> with the appropriate jurisdiction whitelist. Cross-tranche transfers are blocked.</td>
                </tr>
                <tr>
                    <td><strong>Restricted Jurisdictions</strong></td>
                    <td>Sanctions compliance</td>
                    <td>OFAC-sanctioned jurisdiction hashes are never included in any offering's whitelist. The KYC Credential NFT is never issued for sanctioned jurisdictions in the first place — double enforcement.</td>
                </tr>
            </tbody>
        </table>
        <p>Jurisdiction rules are immutable once set on an offering's <code>ComplianceConfig</code> — they can only be modified by the Issuer with Platform Operator approval, and any change is logged to the audit trail. This ensures that an offering's regulatory status cannot be silently changed after investors have committed capital.</p>
    </div>
