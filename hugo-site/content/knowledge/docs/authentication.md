---
title: "Authentication - Documentation"
description: "The four-layer authentication model — from Solana wallet signatures through NFT role verification, Sandstorm sessions, and Powerbox capabilities."
ogImage: "/og-image.png"
keywords: ["authentication", "NFT roles", "threshold signing", "wallet signature", "powerbox capabilities"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/docs.css"
heroDesc: "Four layers of cryptographic proof — because regulated securities demand nothing less."
draft: false
---
<h2>Authentication Layers</h2>
        <p>Sails.to implements a four-layer authentication model. Each layer builds on the one below it. No single layer is sufficient — all four must agree before any operation proceeds. This is not over-engineering; this is what you build when you're responsible for other people's securities.</p>
        <h3>Layer 1: Solana Wallet Signature</h3>
        <p>The cryptographic foundation. Every request begins with a <a href="/knowledge/glossary/solana/">Solana</a> wallet signature proving ownership of the private key. This is standard Ed25519 — the same signature scheme that secures every transaction on the Solana network. No password, no username — just cryptographic proof of identity.</p>
        <h3>Layer 2: NFT Verification</h3>
        <p>A wallet signature proves you <em>exist</em>. An <span class="glossary-term" data-term="nft-hierarchy">NFT</span> proves you're <em>authorized</em>. The platform inspects the wallet for role-specific NFTs minted by the <span class="glossary-term" data-term="melusina">Melusina</span> authority program. No NFT, no access — regardless of how valid your wallet signature is. The NFT encodes your role, your permissions, your expiration date, and whether the platform can recall your authorization.</p>
        <h3>Layer 3: Sandstorm Session</h3>
        <p>OS-level isolation. Once wallet and NFT are verified, the Sandstorm runtime establishes a session bound to a specific <span class="glossary-term" data-term="grain">grain</span>. You can only interact with grains you've been explicitly granted access to. The session is not a cookie — it is a kernel-enforced security boundary. A compromised application cannot reach another grain's data any more than a Linux process can read another process's memory.</p>
        <h3>Layer 4: Powerbox Capability</h3>
        <p>Inter-grain authority. When one grain needs to interact with another — a Broker Portal placing an investor into an Offering Grain, for example — the <span class="glossary-term" data-term="powerbox">Powerbox</span> mediates. A claim token is issued, converted to a sturdyRef, and that sturdyRef grants persistent, cross-session access to specific capabilities. Not to the whole grain — to <em>specific methods</em> on that grain's <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> interface.</p>
        <pre><code>Layer 1: Solana Wallet Signature   → proves wallet ownership
Layer 2: NFT Verification          → proves role authorization
Layer 3: Sandstorm Session          → proves grain access
Layer 4: Powerbox Capability        → proves inter-grain authority</code></pre>
        <p>Compromise one layer and three remain. Steal a wallet key but lack the NFT — denied. Hold the NFT but lack a Sandstorm session — denied. Have a session but no Powerbox capability for the target grain — denied. This is defense in depth as architecture, not as aspiration.</p>
        <h2>Role NFTs</h2>
        <p>The <span class="glossary-term" data-term="melusina">Melusina</span> program mints role-specific NFTs that encode participant authorization. Each is a print edition from the Sails <span class="glossary-term" data-term="master-nft">Master NFT</span>, carrying role-specific metadata and optional expiration. Every role NFT is recallable — the issuing authority can revoke it at any time.</p>
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
                    <td>Deploy offerings, manage platform configuration</td>
                    <td>Master (3-of-5)</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>White-Label Operator</strong></td>
                    <td>Operate branded instance, manage own issuers</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="trustee">Trustee</span></strong></td>
                    <td>Authenticate transactions, validate <span class="glossary-term" data-term="crossconversion">CrossConversions</span></td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>KYC Issuer</strong></td>
                    <td>Issue <span class="glossary-term" data-term="kyc">KYC</span> credential NFTs to verified investors</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="broker-dealer">Broker</span></strong></td>
                    <td>Place investors, execute <span class="glossary-term" data-term="secondary-trading">secondary trades</span></td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong>Issuer</strong></td>
                    <td>Create offerings within their Series, manage investors</td>
                    <td>Platform Operator</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="paying-agent">Paying Agent</span></strong></td>
                    <td>Execute <span class="glossary-term" data-term="distributions">distributions</span>, manage revenue <span class="glossary-term" data-term="waterfall">waterfall</span></td>
                    <td>Trustee</td>
                    <td>Yes</td>
                </tr>
            </tbody>
        </table>
        <p>The hierarchy is strict. A Platform Operator is minted only by the Master NFT's 3-of-5 <span class="glossary-term" data-term="threshold-signing">threshold signing</span> ceremony. A Trustee is minted only by a Platform Operator. A Paying Agent is minted only by a Trustee. The chain of authority is unbroken and on-chain — every role can be traced back to the Master NFT in a single walk of the mint history.</p>
        <h2>Threshold Operations</h2>
        <p>Critical operations require M-of-N keyholder approval, implemented via <span class="glossary-term" data-term="threshold-signing">threshold cryptography</span> from the Melusina program's Shamir-like signing scheme. The threshold levels are calibrated to the severity of the action:</p>
        <table>
            <thead>
                <tr>
                    <th>Threshold</th>
                    <th>Operations</th>
                    <th>Rationale</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>3-of-5</strong></td>
                    <td>Master NFT operations, force transfers, contract upgrades</td>
                    <td>Highest-impact actions affecting platform-wide security. Requires supermajority of geographically distributed keyholders with hardware wallets.</td>
                </tr>
                <tr>
                    <td><strong>2-of-3</strong></td>
                    <td>Large <span class="glossary-term" data-term="crossconversion">CrossConversions</span> (&gt;$1M), emergency freezes</td>
                    <td>High-value operations requiring additional oversight beyond single-Trustee authentication.</td>
                </tr>
                <tr>
                    <td><strong>1-of-1</strong></td>
                    <td>Standard CrossConversions, distribution authentication</td>
                    <td>Routine operations authenticated by a single appointed <span class="glossary-term" data-term="trustee">Trustee</span> holding a valid Trustee NFT.</td>
                </tr>
            </tbody>
        </table>
        <p>Key compromise mitigation: hardware wallet enforcement for all keyholders, geographic distribution of signers, documented key rotation procedures, and the ability to recall any role NFT instantly if a keyholder is compromised. The 3-of-5 threshold means an attacker must compromise three separate hardware wallets held by three separate people in three separate locations. This is the standard we hold ourselves to.</p>
        <h2>Session Management</h2>
        <p>Sandstorm sessions are not traditional web sessions. They are capability-bound, grain-scoped, and kernel-enforced:</p>
        <ul>
            <li><strong>Session Creation:</strong> After Layer 1 (wallet) and Layer 2 (NFT) verification, the platform provisions a Sandstorm session tied to the user's role-appropriate grain. An Issuer gets a DAO Manager grain session. An Investor gets an Investor Self-Service grain session. A Broker gets a Broker Portal grain session.</li>
            <li><strong>Session Scope:</strong> Each session is bound to a single grain. To access another grain's capabilities, you must go through the Powerbox — there is no session that spans multiple grains.</li>
            <li><strong>Capability Persistence:</strong> Powerbox sturdyRefs persist across sessions. If a Broker was granted an <code>OfferingAPI</code> capability from an Offering Grain, that capability survives session restart — it is stored in the grain's journal and restored on replay.</li>
            <li><strong>Time-Bound Tokens:</strong> Trustee sessions include time-bound authentication tokens. A Trustee must re-authenticate periodically — the session itself may persist, but high-value operations require fresh NFT verification within a configurable window.</li>
            <li><strong>Audit Logging:</strong> Every session creation, capability grant, capability use, and session termination is logged to the grain's append-only journal. Seven-year retention. No exceptions.</li>
        </ul>
        <p>The result: a system where authentication is not a gate you pass through once, but a continuous assertion of identity, role, access, and authority — verified at every layer, for every operation, without exception.</p>
    </div>
