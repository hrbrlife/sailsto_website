---
title: "Hybrid Architecture - Documentation"
description: "The CrossConversion Engine — how Sails.to bridges on-chain Solana tokens to bankable ISIN-identified securities via Clearstream."
ogImage: "/og-image.png"
keywords: ["crossconversion", "hybrid securities", "clearstream", "ISIN", "lockbox", "reconciliation"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
heroDesc: "The CrossConversion Engine — bridging on-chain tokens to bankable securities with mathematical certainty."
draft: false
---
<h2>The Hybrid Model</h2>
        <p><span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> are not purely on-chain. They are not purely traditional. They exist in both worlds simultaneously — and the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> Engine is the mechanism that makes this possible.</p>
        <p>The premise is absolute: an investor holding Sails <span class="glossary-term" data-term="security-token">security tokens</span> on <a href="/knowledge/glossary/solana/">Solana</a> can convert them to <span class="glossary-term" data-term="bankable">bankable</span>, <span class="glossary-term" data-term="isin">ISIN</span>-identified securities held at <span class="glossary-term" data-term="clearstream">Clearstream</span> — and back again. At any time. With full regulatory compliance. Without losing a single unit of value.</p>
        <p>Two directions, one invariant:</p>
        <ul>
            <li><strong>Cross to Bankable:</strong> Lock Solana tokens in the on-chain lockbox → Issue ISIN-identified securities via Clearstream.</li>
            <li><strong>Cross to On-Chain:</strong> Cancel the Clearstream position → Unlock Solana tokens from the lockbox.</li>
        </ul>
        <p>The <strong>1:1 invariant</strong> must always hold:</p>
        <pre><code>tokens_locked == isin_outstanding</code></pre>
        <p>This is not a guideline. This is a mathematical constraint enforced by <span class="glossary-term" data-term="smart-contract">smart contract</span> logic, validated by nightly reconciliation, and audited by an appointed <span class="glossary-term" data-term="trustee">Trustee</span>. If it ever breaks, the system halts and alerts fire.</p>
        <h2>CrossConversion Lockbox</h2>
        <p>The lockbox is an on-chain <span class="glossary-term" data-term="pda">PDA</span> (Program Derived Address) that holds tokens in escrow during their bankable life. It is the heart of the hybrid model — the cryptographic proof that on-chain supply and off-chain positions are always in balance.</p>
        <pre><code>Program: sails_crossconversion
├── init_lockbox(offering_id, isin_code, clearstream_account)
│   → Creates the lockbox PDA, links to Clearstream account
├── lock_tokens(offering_id, amount)
│   → Transfers tokens to lockbox PDA
│   → Emits CrossConversionRequested event
│   → Increments locked counter
├── unlock_tokens(offering_id, amount, trustee_signature, clearstream_proof)
│   → Verifies Clearstream cancellation proof
│   → Validates Trustee NFT signature
│   → Releases tokens back to investor wallet
│   → Decrements locked counter
├── get_lockbox_state(offering_id)
│   → Returns { locked, isin_outstanding }
└── reconcile(offering_id, clearstream_snapshot_hash)
    → Trustee-signed reconciliation (periodic, e.g., daily)
    → Compares on-chain state with Clearstream snapshot hash
    → Emits ReconciliationCompleted or ReconciliationFailed event</code></pre>
        <p>Every <code>lock_tokens</code> call requires a valid <span class="glossary-term" data-term="kyc">KYC</span> credential NFT on the requesting wallet. Every <code>unlock_tokens</code> call requires both a Trustee NFT signature and cryptographic proof of Clearstream position cancellation. There are no shortcuts. There are no overrides. The invariant is sacred.</p>
        <h2>Operator Service</h2>
        <p>The CrossConversion Operator Service is a Sandstorm <span class="glossary-term" data-term="grain">grain</span> (Go+HTMX) that orchestrates the off-chain side of every conversion. It is the bridge between the Solana event stream and the <span class="glossary-term" data-term="clearstream">Clearstream</span> API:</p>
        <ol>
            <li><strong>Event Listening:</strong> Subscribes to <code>CrossConversionRequested</code> events from the Solana program via WebSocket RPC.</li>
            <li><strong>KYC Validation:</strong> Verifies the requesting investor's KYC credential NFT is valid, unexpired, and carries the correct accreditation tier and jurisdiction clearance.</li>
            <li><strong>ISIN Issuance:</strong> Initiates the ISIN issuance workflow with Clearstream's API — submitting the security details, investor allocation, and settlement instructions.</li>
            <li><strong>Proof Storage:</strong> Once Clearstream confirms issuance, stores the proof-of-issuance on-chain in the lockbox PDA metadata.</li>
            <li><strong>Reverse Conversion:</strong> For Cross-to-On-Chain requests, verifies the Clearstream position cancellation and triggers <code>unlock_tokens</code> on the smart contract.</li>
            <li><strong>Audit Trail:</strong> Maintains a complete, append-only log of every conversion action, every API call, every Trustee authentication — stored in the grain's journal with 7-year retention.</li>
            <li><strong>Trustee Authentication:</strong> Every conversion — forward or reverse — requires authentication by an appointed Trustee holding a valid <span class="glossary-term" data-term="trustee">Trustee NFT</span>. No exceptions.</li>
        </ol>
        <p>The Operator Service runs as a Station-type grain. It is long-lived, managing all CrossConversion workflows for the platform. Its <span class="glossary-term" data-term="powerbox">Powerbox</span> capabilities connect it to Offering Grains (for token state), KYC Grains (for credential verification), and the Trustee Dashboard (for authentication signing).</p>
        <h2>Reconciliation</h2>
        <p>Trust but verify — every night, automatically, without fail.</p>
        <p>The Reconciliation Engine is a scheduled process that compares two sources of truth:</p>
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
        <p>The nightly reconciliation process:</p>
        <ol>
            <li>Pulls the daily Clearstream position report for all active ISINs.</li>
            <li>Reads the on-chain lockbox state for every offering with CrossConversion enabled.</li>
            <li>Compares totals: <code>tokens_locked</code> must equal <code>isin_outstanding</code> for every offering.</li>
            <li>Generates a reconciliation report — signed by the Trustee and stored on-chain as a hash.</li>
            <li>On match: emits <code>ReconciliationCompleted</code> event with the snapshot hash.</li>
            <li>On mismatch: emits <code>ReconciliationFailed</code> — triggers P0 alert (immediate response required), freezes affected offering's CrossConversion capability until manual resolution.</li>
        </ol>
        <p>A supply mismatch should <em>never</em> happen. The smart contract enforces the invariant on every lock and unlock. But the reconciliation engine exists because defense in depth is not optional when you're holding other people's securities.</p>
        <h2>Message Formats</h2>
        <p>Communication with <span class="glossary-term" data-term="clearstream">Clearstream</span> follows established financial messaging standards. The Sails.to platform generates and consumes these message types as part of the CrossConversion workflow:</p>
        <table>
            <thead>
                <tr>
                    <th>Message Type</th>
                    <th>Standard</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>MT540</strong></td>
                    <td>SWIFT</td>
                    <td>Receive Free — settlement instruction for incoming securities (Cross to Bankable). Instructs Clearstream to credit the investor's account with the ISIN-identified securities.</td>
                </tr>
                <tr>
                    <td><strong>MT542</strong></td>
                    <td>SWIFT</td>
                    <td>Deliver Free — settlement instruction for outgoing securities (Cross to On-Chain). Instructs Clearstream to cancel the position and provide proof of cancellation.</td>
                </tr>
                <tr>
                    <td><strong>ISO 20022</strong></td>
                    <td>ISO</td>
                    <td>Corporate Actions — distribution notifications, voting instructions, and other corporate events that affect ISIN-identified positions.</td>
                </tr>
            </tbody>
        </table>
        <p>The <span class="glossary-term" data-term="tradfi-bridge">TradFi bridge</span> adapter service (Go, running as a grain or sidecar) handles all message generation, submission, and response parsing. It translates between the Sails.to <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> schema and the SWIFT/ISO messaging formats — ensuring that every CrossConversion is expressed in the language that traditional financial infrastructure expects and trusts.</p>
    </div>
