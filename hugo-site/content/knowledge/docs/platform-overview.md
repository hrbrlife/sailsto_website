---
title: "Platform Overview - Documentation"
description: "Complete architectural overview of the Sails.to platform — three pillars, seven grain types."
ogImage: "/og-image.png"
keywords: ["platform architecture", "sandstorm grains", "cap'n proto", "tokenized securities", "data sovereignty"]
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
heroDesc: "The three-pillar architecture that brings regulated securities on-chain — without compromise."
draft: false
---
<h2>Architecture Overview</h2>
        <p>Sails.to is not a monolith. It is not a microservices cluster. It is a <strong>capability-secured grain architecture</strong> — every component isolated at the OS level, every interaction mediated by cryptographic authority, every byte of investor data sovereign to its owner. This is what regulated infrastructure demands, and this is what we built.</p>
        <p>The platform rests on three pillars, each independently auditable, each doing exactly one job with absolute fidelity:</p>
        <pre><code>┌─────────────────────────────────────────────────────┐
│  Sandstorm/Melusina OS                               │
│  ┌───────────────┐  ┌───────────────┐                │
│  │ Station Grain  │  │ Instance Grain │               │
│  │ (Orchestrator) │  │ (Worker)       │               │
│  │                │  │                │               │
│  │ Go binary      │  │ Go binary      │               │
│  │ FD3 → Cap'n    │  │ FD3 → Cap'n    │               │
│  │ Proto RPC      │  │ Proto RPC      │               │
│  │                │  │                │               │
│  │ UiView Server  │  │ UiView Server  │               │
│  │ WebSession     │  │ WebSession     │               │
│  │ (HTMX+Templ)   │  │ (HTMX+Templ)   │               │
│  │                │  │                │               │
│  │ Journal Store  │  │ Journal Store  │               │
│  │ Workflow Engine │  │ Process Engine │               │
│  │ WebSocket Hub  │  │ WebSocket Hub  │               │
│  └───────┬───────┘  └───────┬───────┘                │
│          │ Powerbox           │ Powerbox               │
│          └───────────────────┘                         │
│         Cap'n Proto capabilities                       │
└─────────────────────────────────────────────────────┘</code></pre>
        <h2>The Three Pillars</h2>
        <h3>Pillar 1: sailsto_website — The Business Layer</h3>
        <p>The marketing site, legal templates, and product definition. This is the <span class="glossary-term" data-term="wyoming-dao-llc">Wyoming DAO Series LLC</span> structure made real — audience-specific landing pages for issuers, investors, brokers, and institutions. A comprehensive knowledge base. Legal templates in the <code>Legal/Client_Series/</code> directory. The pricing calculator. Every piece of content that makes Sails.to legible to the world lives here.</p>
        <h3>Pillar 2: Melusina — The On-Chain Authority Layer</h3>
        <p>The <span class="glossary-term" data-term="melusina">Melusina</span> program is the on-chain truth. <a href="/knowledge/glossary/solana/">Solana</a> NFT-based licensing, KYC credentialing, hierarchical access control from <span class="glossary-term" data-term="master-nft">Master NFT</span> down through Reseller, License, and Share layers. <span class="glossary-term" data-term="threshold-signing">Threshold crypto operations</span> for critical governance actions. Every role, every permission, every compliance credential — cryptographically attested on-chain.</p>
        <h3>Pillar 3: BLOOM_FINAL — The Application Engine</h3>
        <p>The grain runtime. Sandstorm/Melusina OS <span class="glossary-term" data-term="grain">grains</span>, <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> RPC, Go+HTMX native stack. KYC workflow orchestration. <span class="glossary-term" data-term="powerbox">Powerbox</span>-based capability sharing between grains. No SPA, no JavaScript framework churn — server-rendered HTML fragments over WebSession, every interaction authenticated at the capability level.</p>
        <h2>Grain Types</h2>
        <p>Seven grain types compose the entire application surface. Each grain is an isolated process with its own journal store, its own capability set, its own security boundary:</p>
        <table>
            <thead>
                <tr>
                    <th>Grain</th>
                    <th>Type</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>DAO Manager</strong></td>
                    <td>Station</td>
                    <td>Central governance hub for a <span class="glossary-term" data-term="series-llc">DAO Series LLC</span> — creates Series, appoints trustees, configures governance rules, monitors compliance across all offerings.</td>
                </tr>
                <tr>
                    <td><strong>Offering</strong></td>
                    <td>Instance</td>
                    <td>Lifecycle management for a single securities offering — configure parameters, manage investor whitelist, execute token minting, track <span class="glossary-term" data-term="cap-table">cap table</span>, process <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, execute distributions.</td>
                </tr>
                <tr>
                    <td><strong>KYC/Onboarding</strong></td>
                    <td>Instance</td>
                    <td>Complete <span class="glossary-term" data-term="kyc">KYC</span> verification workflow for a single investor — 10-step process from terms acceptance through document verification to on-chain credential minting.</td>
                </tr>
                <tr>
                    <td><strong>Broker Portal</strong></td>
                    <td>Station</td>
                    <td>Dashboard for <span class="glossary-term" data-term="broker-dealer">broker-dealers</span> — view available offerings, submit investor subscriptions, track commissions, manage <span class="glossary-term" data-term="secondary-trading">secondary trading</span>, generate regulatory reports.</td>
                </tr>
                <tr>
                    <td><strong>Trustee Dashboard</strong></td>
                    <td>Station</td>
                    <td>Authenticated oversight for appointed <span class="glossary-term" data-term="trustee">trustees</span> — authenticate CrossConversions, sign reconciliation reports, execute emergency freezes, maintain audit trail.</td>
                </tr>
                <tr>
                    <td><strong>Investor Self-Service</strong></td>
                    <td>Instance</td>
                    <td>Personal dashboard for each investor — view portfolio, track <span class="glossary-term" data-term="distributions">distributions</span> and yields, request CrossConversions, download tax documents, participate in governance votes.</td>
                </tr>
                <tr>
                    <td><strong>Introducer Tracking</strong></td>
                    <td>Instance</td>
                    <td>Referral pipeline management — generate unique referral links, track introductions through to funded offerings, calculate 25% commission share, generate payout reports.</td>
                </tr>
            </tbody>
        </table>
        <p><strong>Station grains</strong> are orchestrators — long-lived, managing multiple workflows and participants. <strong>Instance grains</strong> are workers — one per entity (one per offering, one per investor, one per KYC verification), isolated and disposable.</p>
        <h2>Data Sovereignty Model</h2>
        <p>Data lives where it belongs. This is not a design preference — it is a regulatory requirement, and we enforce it architecturally:</p>
        <table>
            <thead>
                <tr>
                    <th>Data Layer</th>
                    <th>What Lives Here</th>
                    <th>What Never Lives Here</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><span class="glossary-term" data-term="on-chain">On-Chain</span> (Solana)</strong></td>
                    <td>Token balances, <span class="glossary-term" data-term="nft-hierarchy">NFT authority</span>, compliance flags, distribution records</td>
                    <td>Names, addresses, document images, phone numbers, emails — <em>zero PII, ever</em></td>
                </tr>
                <tr>
                    <td><strong>In-Grain Journal</strong></td>
                    <td>Encrypted PII, KYC documents, audit trails, business logic state</td>
                    <td>Token balances, on-chain state (that belongs to the ledger)</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="clearstream">Clearstream</span></strong></td>
                    <td><span class="glossary-term" data-term="isin">ISIN</span> positions, <span class="glossary-term" data-term="bankable">bankable</span> custody records</td>
                    <td>On-chain token state (the lockbox maintains the bridge)</td>
                </tr>
            </tbody>
        </table>
        <p>Every grain journal is encrypted at rest with AES-256. GDPR right-to-erasure is handled via cryptographic shredding — delete the encryption key, and the data is gone. Append-only journals enable deterministic replay for audit and disaster recovery. Seven-year retention for regulatory compliance, with automated purge after expiration.</p>
        <h2>Authentication Layers</h2>
        <p>Four layers of authentication, each building on the last. No single layer is sufficient — all four must agree before any operation proceeds:</p>
        <ol>
            <li><strong>Solana Wallet Signature</strong> — proves wallet ownership. The cryptographic foundation.</li>
            <li><strong>NFT Verification</strong> — proves role authorization. You don't just have a wallet; you hold the right <span class="glossary-term" data-term="nft-hierarchy">NFT</span> for the action you're requesting.</li>
            <li><strong>Sandstorm Session</strong> — proves grain access. The OS-level isolation ensures you can only reach grains you've been granted access to.</li>
            <li><strong><span class="glossary-term" data-term="powerbox">Powerbox</span> Capability</strong> — proves inter-grain authority. A claim token becomes a sturdyRef, granting persistent, cross-session access to specific capabilities.</li>
        </ol>
        <p>This is defense in depth — not as a buzzword, but as architecture. Compromise one layer and three remain. See the <a href="/knowledge/docs/authentication/">Authentication documentation</a> for the complete model.</p>
        <h2>The Native Stack</h2>
        <p>Every grain runs Go compiled to a native binary. No HTTP bridge — <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> on file descriptor 3 (FD3) directly. The Go binary implements <code>UiView</code> and <code>WebSession</code> natively. HTMX delivers server-rendered HTML fragments — no SPA, no client-side routing, no JavaScript framework. Journal-based storage gives every grain an append-only log with deterministic replay. WebSocket connections flow through Cap'n Proto's <code>WebSession_WebSocketStream</code> for real-time updates.</p>
        <p>This is the stack. It is simple. It is fast. It is correct. And it will outlast every framework that ships between now and when you read this.</p>
    </div>
