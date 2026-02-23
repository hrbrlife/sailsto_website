---
title: "ISIN Conversion - Documentation"
description: "The CrossConversion Engine in detail — how tokens are locked on Solana and issued as ISIN-identified securities via Clearstream."
ogImage: "/og-image.png"
keywords: ["ISIN conversion", "CrossConversion", "lockbox", "Clearstream", "SWIFT", "MT540", "MT542", "reconciliation", "trustee authentication"]
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
heroDesc: "CrossConversion is the bridge — lock Solana tokens, issue bankable ISIN securities via Clearstream, and back again. One invariant. Zero exceptions."
draft: false
---
<h2>Overview</h2>
        <p><span class="glossary-term" data-term="crossconversion">CrossConversion</span> is the mechanism that makes <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> hybrid. It is the bridge between two worlds: <a href="/knowledge/glossary/solana/">Solana</a> tokens that live on-chain and <span class="glossary-term" data-term="isin">ISIN</span>-identified securities held in traditional financial infrastructure at <span class="glossary-term" data-term="clearstream">Clearstream</span>.</p>
        <p>Two directions, one invariant:</p>
        <ul>
            <li><strong>Cross to Bankable:</strong> Lock Solana tokens in the on-chain lockbox → Issue ISIN-identified securities via Clearstream.</li>
            <li><strong>Cross to On-Chain:</strong> Cancel the Clearstream position → Unlock Solana tokens from the lockbox.</li>
        </ul>
        <p>The <strong>1:1 invariant</strong> is the foundation of the entire system:</p>
        <pre><code>tokens_locked == isin_outstanding</code></pre>
        <p>This is not a target. This is not a guideline. This is a mathematical constraint enforced by <span class="glossary-term" data-term="smart-contract">smart contract</span> logic on every lock and unlock operation, validated by nightly reconciliation, and audited by an appointed <span class="glossary-term" data-term="trustee">Trustee</span>. If it ever breaks, the system halts and alerts fire. Always. The total supply of a <span class="glossary-term" data-term="crossconversion-series">CrossConversion Series</span> is constant — tokens are either circulating on Solana or locked in the lockbox with a corresponding ISIN position at Clearstream. Never both. Never neither.</p>
        <p>For the broader architectural context, see the <a href="/knowledge/docs/hybrid-architecture/">Hybrid Architecture</a> documentation. This page covers the lockbox contract, the step-by-step conversion flows, trustee authentication, reconciliation, and SWIFT messaging in full technical detail.</p>
        <h2>The Lockbox Contract</h2>
        <p>The lockbox is an on-chain <span class="glossary-term" data-term="pda">PDA</span> (Program Derived Address) controlled by the <code>sails_crossconversion</code> program. It holds tokens in escrow during their <span class="glossary-term" data-term="bankable">bankable</span> life. No human has custody of the locked tokens — only the program logic can release them, and only when the correct cryptographic proofs are provided.</p>
        <h3>Program Instructions</h3>
        <pre><code>Program: sails_crossconversion
├── init_lockbox(offering_id, isin_code, clearstream_account)
│   → Creates the CrossConversionLockbox PDA for the offering
│   → Links the on-chain lockbox to a specific Clearstream account
│   → Stores the ISIN code in lockbox metadata
│   → Requires Platform Operator NFT authorization
├── lock_tokens(offering_id, amount)
│   → Transfers tokens from investor wallet to lockbox PDA
│   → Increments the locked counter
│   → Emits CrossConversionRequested event
│   → Requires valid KYC Credential NFT on the requesting wallet
├── unlock_tokens(offering_id, amount, trustee_signature, clearstream_proof)
│   → Verifies Clearstream cancellation proof
│   → Validates Trustee NFT signature
│   → Releases tokens from lockbox PDA back to investor wallet
│   → Decrements the locked counter
│   → Emits CrossConversionCompleted event
├── get_lockbox_state(offering_id)
│   → Returns { locked, isin_outstanding, isin_code, clearstream_ref }
│   → Read-only — callable by any authenticated participant
└── reconcile(offering_id, clearstream_snapshot_hash)
    → Trustee-signed reconciliation (periodic, e.g., daily)
    → Compares on-chain state with Clearstream snapshot hash
    → Emits ReconciliationCompleted or ReconciliationFailed event
    → On failure: freezes CrossConversion for the affected offering</code></pre>
        <h3>CrossConversionLockbox PDA Structure</h3>
        <p>Each offering with CrossConversion enabled has a dedicated lockbox PDA. The PDA is derived from the offering ID and the <code>sails_crossconversion</code> program address, making it deterministic and verifiable by anyone:</p>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>offering_id</code></td>
                    <td>Pubkey</td>
                    <td>The offering this lockbox serves</td>
                </tr>
                <tr>
                    <td><code>total_locked</code></td>
                    <td>u64</td>
                    <td>Total tokens currently locked in the PDA</td>
                </tr>
                <tr>
                    <td><code>isin_code</code></td>
                    <td>String</td>
                    <td>The ISIN identifier assigned by Clearstream (e.g., XS1234567890)</td>
                </tr>
                <tr>
                    <td><code>clearstream_ref</code></td>
                    <td>String</td>
                    <td>Clearstream account reference for settlement</td>
                </tr>
                <tr>
                    <td><code>last_reconciliation</code></td>
                    <td>i64</td>
                    <td>Unix timestamp of the last successful reconciliation</td>
                </tr>
                <tr>
                    <td><code>reconciliation_hash</code></td>
                    <td>[u8; 32]</td>
                    <td>SHA-256 hash of the last Clearstream snapshot used in reconciliation</td>
                </tr>
                <tr>
                    <td><code>frozen</code></td>
                    <td>bool</td>
                    <td>If true, all CrossConversion operations are halted pending resolution</td>
                </tr>
            </tbody>
        </table>
        <p>The <code>total_locked</code> field is the on-chain source of truth. It is incremented on every <code>lock_tokens</code> and decremented on every <code>unlock_tokens</code>. The Clearstream side maintains its own <code>isin_outstanding</code> count. The reconciliation engine exists to prove these two numbers are always equal.</p>
        <h2>Cross to Bankable Flow</h2>
        <p>An investor holding <span class="glossary-term" data-term="security-token">security tokens</span> on Solana wants them in their brokerage account as ISIN-identified securities. Here is exactly what happens, step by step:</p>
        <ol>
            <li><strong>Investor requests conversion</strong> — Through their Investor Self-Service <span class="glossary-term" data-term="grain">grain</span>, the investor selects an offering and specifies the number of tokens to convert to bankable format.</li>
            <li><strong>Tokens locked in lockbox PDA</strong> — The <code>lock_tokens</code> instruction transfers the specified tokens from the investor's wallet to the lockbox PDA. The locked counter increments. The tokens are now in escrow — the investor no longer controls them on-chain.</li>
            <li><strong>CrossConversionRequested event emitted</strong> — The Solana program emits an on-chain event containing the offering ID, amount, investor wallet, and conversion direction.</li>
            <li><strong>Operator Service picks up the event</strong> — The CrossConversion Operator Service (a Sandstorm grain subscribed to Solana events via WebSocket RPC) detects the <code>CrossConversionRequested</code> event.</li>
            <li><strong>KYC validation</strong> — The Operator verifies that the investor's <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT is valid, unexpired, and carries the correct <span class="glossary-term" data-term="accredited-investor">accreditation</span> tier and jurisdiction clearance for the offering.</li>
            <li><strong>Trustee authentication</strong> — The Operator routes the conversion request to the appointed <span class="glossary-term" data-term="trustee">Trustee</span> for authentication. The Trustee signs the conversion with their Trustee NFT. For conversions over $1M, 2-of-3 <span class="glossary-term" data-term="threshold-signing">threshold signing</span> is required.</li>
            <li><strong>ISIN issuance initiated with Clearstream</strong> — The Operator submits an MT540 (Receive Free) settlement instruction to <span class="glossary-term" data-term="clearstream">Clearstream</span>, instructing them to credit the investor's account with the ISIN-identified securities.</li>
            <li><strong>Clearstream confirms issuance</strong> — Clearstream processes the instruction, credits the investor's securities account, and returns a confirmation with settlement details.</li>
            <li><strong>Proof stored on-chain</strong> — The Operator stores the Clearstream proof-of-issuance in the lockbox PDA metadata, creating an auditable on-chain record that links the locked tokens to the issued ISIN position.</li>
            <li><strong>Investor sees ISIN in brokerage account</strong> — The ISIN-identified securities appear in the investor's brokerage account at their custodian, visible through standard financial infrastructure just like any other security.</li>
        </ol>
        <p>From the investor's perspective: tokens disappear from their Solana wallet and securities appear in their brokerage account. From the system's perspective: the invariant holds — <code>total_locked</code> increased by exactly the amount of ISIN securities issued.</p>
        <h2>Cross to On-Chain Flow</h2>
        <p>The reverse: an investor holding ISIN-identified securities at Clearstream wants them back as Solana tokens. This flow requires stronger validation because it releases tokens from escrow.</p>
        <ol>
            <li><strong>Investor requests reverse conversion</strong> — Through their Investor Self-Service grain or via their broker, the investor requests conversion of their ISIN position back to on-chain tokens.</li>
            <li><strong>Trustee verifies the request</strong> — The appointed Trustee reviews and authenticates the request. The Trustee confirms that the investor holds the claimed ISIN position and that the conversion is permissible under the offering's <span class="glossary-term" data-term="compliance">compliance</span> rules (lock-up periods, jurisdiction restrictions, transfer limits).</li>
            <li><strong>Clearstream position cancellation</strong> — The Operator submits an MT542 (Deliver Free) settlement instruction to Clearstream, instructing them to cancel the investor's ISIN position for the specified amount.</li>
            <li><strong>Clearstream provides cancellation proof</strong> — Clearstream processes the instruction, debits the investor's securities account, and returns cryptographic proof of cancellation.</li>
            <li><strong>Operator triggers unlock_tokens</strong> — The Operator calls <code>unlock_tokens</code> on the <code>sails_crossconversion</code> program, providing the Trustee's NFT signature and the Clearstream cancellation proof as parameters.</li>
            <li><strong>Smart contract validates proofs</strong> — The program verifies the Trustee NFT signature is valid and the Clearstream proof is authentic before releasing any tokens. Both must pass. No exceptions.</li>
            <li><strong>Tokens released to wallet</strong> — The lockbox PDA transfers the tokens back to the investor's Solana wallet. The locked counter decrements. The <code>CrossConversionCompleted</code> event is emitted.</li>
        </ol>
        <p>The asymmetry is intentional. Locking tokens (Cross to Bankable) requires a valid KYC credential and Trustee authentication. Unlocking tokens (Cross to On-Chain) requires Trustee authentication <em>and</em> cryptographic proof from Clearstream that the ISIN position has been cancelled. You cannot unlock tokens without proving the corresponding bankable position no longer exists.</p>
        <h2>Trustee Authentication</h2>
        <p>Every CrossConversion — forward or reverse — requires authentication by an appointed <span class="glossary-term" data-term="trustee">Trustee</span> holding a valid Trustee NFT minted by the <span class="glossary-term" data-term="melusina">Melusina</span> authority program. The Trustee is the human-in-the-loop that prevents automated systems from moving securities without oversight.</p>
        <h3>Authentication Thresholds</h3>
        <table>
            <thead>
                <tr>
                    <th>Conversion Value</th>
                    <th>Threshold</th>
                    <th>Requirement</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Standard</strong> (≤ $1M)</td>
                    <td>1-of-1</td>
                    <td>Single Trustee NFT signature. The appointed Trustee for the offering reviews and signs the conversion request.</td>
                </tr>
                <tr>
                    <td><strong>Large</strong> (&gt; $1M)</td>
                    <td>2-of-3</td>
                    <td>Two of three designated Trustees must independently review and sign. Implemented via <span class="glossary-term" data-term="threshold-signing">threshold cryptography</span> from the Melusina program's signing scheme.</td>
                </tr>
            </tbody>
        </table>
        <h3>Authentication Flow</h3>
        <ol>
            <li><strong>Request routed to Trustee Dashboard</strong> — The CrossConversion Operator Service sends the conversion request to the Trustee Dashboard grain via <span class="glossary-term" data-term="powerbox">Powerbox</span> capability.</li>
            <li><strong>Trustee reviews details</strong> — The Trustee sees the offering, amount, investor identity (KYC-verified, not PII), conversion direction, and any applicable compliance flags.</li>
            <li><strong>NFT signature</strong> — The Trustee signs the conversion with their Trustee NFT. The signature is verified on-chain by the <code>sails_crossconversion</code> program.</li>
            <li><strong>Threshold collection</strong> — For large conversions, the Operator collects signatures from the required number of Trustees before proceeding. All signatures must be collected within a configurable time window.</li>
            <li><strong>Audit logged</strong> — Every authentication action — approval, rejection, timeout — is logged to the Trustee Dashboard grain's append-only journal. Seven-year retention. No exceptions.</li>
        </ol>
        <p>The Trustee cannot initiate conversions — only authenticate them. The Trustee cannot modify conversion amounts or redirect tokens. The Trustee has exactly one power: approve or reject. This separation of concerns is by design. See the <a href="/knowledge/docs/authentication/">Authentication documentation</a> for the full four-layer model and the role NFT hierarchy.</p>
        <h2>Reconciliation</h2>
        <p>Trust but verify — every night, automatically, without fail. The Reconciliation Engine is the safety net that proves the 1:1 invariant holds across both systems.</p>
        <h3>Two Sources of Truth</h3>
        <table>
            <thead>
                <tr>
                    <th>Source</th>
                    <th>Data</th>
                    <th>Authority</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>On-Chain Lockbox</strong></td>
                    <td>Total tokens locked per offering, per investor position</td>
                    <td>Solana program state (immutable, auditable)</td>
                </tr>
                <tr>
                    <td><strong>Clearstream Holdings</strong></td>
                    <td>ISIN positions, settlement status, corporate actions</td>
                    <td>Clearstream daily position report</td>
                </tr>
            </tbody>
        </table>
        <h3>Nightly Reconciliation Process</h3>
        <ol>
            <li><strong>Pull Clearstream positions</strong> — The Reconciliation Engine requests the daily position report from Clearstream for all active ISINs linked to Sails offerings.</li>
            <li><strong>Read on-chain lockbox state</strong> — For every offering with CrossConversion enabled, the engine calls <code>get_lockbox_state</code> to retrieve the current <code>total_locked</code> value.</li>
            <li><strong>Compare totals</strong> — For each offering: <code>tokens_locked</code> must equal <code>isin_outstanding</code>. No tolerance. No rounding. Exact match.</li>
            <li><strong>Generate reconciliation report</strong> — A detailed report covering every offering, every position, every discrepancy (if any), timestamped and formatted for audit.</li>
            <li><strong>Trustee signs the report</strong> — The appointed Trustee reviews and signs the reconciliation report. The signature and a SHA-256 hash of the Clearstream snapshot are stored on-chain via the <code>reconcile</code> instruction.</li>
            <li><strong>On match</strong> — The program emits a <code>ReconciliationCompleted</code> event with the snapshot hash. The <code>last_reconciliation</code> timestamp updates. Business as usual.</li>
            <li><strong>On mismatch</strong> — The program emits a <code>ReconciliationFailed</code> event. A P0 alert fires (immediate response required). The affected offering's CrossConversion capability is frozen until manual resolution by the Trustee.</li>
        </ol>
        <h3>Discrepancy Handling</h3>
        <p>A supply mismatch should <em>never</em> happen. The smart contract enforces the invariant on every lock and unlock. But the reconciliation engine exists because defense in depth is not optional when you hold other people's securities. If a discrepancy is detected:</p>
        <ul>
            <li><strong>Immediate freeze</strong> — All CrossConversion operations for the affected offering halt. No new locks. No new unlocks.</li>
            <li><strong>P0 alert</strong> — The Platform Operator, Trustee, and compliance team receive immediate notification.</li>
            <li><strong>Root cause investigation</strong> — Manual review of all transactions since the last successful reconciliation.</li>
            <li><strong>Trustee-signed resolution</strong> — The Trustee must sign a resolution report before CrossConversion resumes. The resolution is stored on-chain for audit.</li>
        </ul>
        <h2>SWIFT Messaging</h2>
        <p>Communication with <span class="glossary-term" data-term="clearstream">Clearstream</span> follows established financial messaging standards. The <span class="glossary-term" data-term="tradfi-bridge">TradFi bridge</span> adapter service handles all message generation, submission, and response parsing — translating between the Sails.to <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> schema and the messaging formats that traditional financial infrastructure expects.</p>
        <h3>Settlement Instructions</h3>
        <table>
            <thead>
                <tr>
                    <th>Message Type</th>
                    <th>Standard</th>
                    <th>Direction</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>MT540</strong></td>
                    <td>SWIFT</td>
                    <td>Cross to Bankable</td>
                    <td>Receive Free — instructs Clearstream to credit the investor's account with ISIN-identified securities. Generated by the Operator after tokens are locked and Trustee authentication is complete.</td>
                </tr>
                <tr>
                    <td><strong>MT542</strong></td>
                    <td>SWIFT</td>
                    <td>Cross to On-Chain</td>
                    <td>Deliver Free — instructs Clearstream to cancel the investor's ISIN position. Generated by the Operator after the Trustee authenticates the reverse conversion request.</td>
                </tr>
            </tbody>
        </table>
        <h3>Corporate Actions</h3>
        <table>
            <thead>
                <tr>
                    <th>Message Standard</th>
                    <th>Purpose</th>
                    <th>Examples</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>ISO 20022</strong></td>
                    <td>Corporate action notifications and instructions for ISIN-identified positions</td>
                    <td><span class="glossary-term" data-term="distributions">Distribution</span> notifications, voting instructions, maturity events, coupon payments, and other corporate events that affect bankable positions held at Clearstream</td>
                </tr>
            </tbody>
        </table>
        <p>The TradFi bridge adapter runs as a Go service within the Sandstorm environment (grain or sidecar). It maintains message queues, handles retries on transient failures, validates message schemas before submission, and logs every message sent and received to the grain's append-only journal. Every SWIFT message generated by the platform is traceable to a specific CrossConversion request, a specific Trustee authentication, and a specific on-chain transaction.</p>
        <h2>Next Steps</h2>
        <ul>
            <li><a href="/knowledge/docs/hybrid-architecture/">Hybrid Architecture</a> — The broader architectural context for the CrossConversion Engine</li>
            <li><a href="/knowledge/docs/authentication/">Authentication</a> — The four-layer authentication model and Trustee NFT hierarchy</li>
            <li><a href="/knowledge/docs/token-standard/">Token Standard</a> — How <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> tokens work on Solana</li>
            <li><a href="/knowledge/docs/compliance-framework/">Compliance Framework</a> — KYC credentials and transfer enforcement rules</li>
            <li><a href="/knowledge/docs/transfer-rules/">Transfer Rules</a> — Compliance checks enforced at the protocol level on every transfer</li>
            <li><a href="/knowledge/docs/api-reference/">API Reference</a> — Cap'n Proto schemas for programmatic access to CrossConversion operations</li>
        </ul>
    </div>
