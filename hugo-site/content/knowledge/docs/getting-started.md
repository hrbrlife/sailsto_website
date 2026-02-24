---
title: "Getting Started - Documentation"
description: "Your onboarding guide to the Sails.to platform — choose your role, complete verification, and start working with tokenized securities in minutes."
ogImage: "/og-image.png"
keywords: ["getting started", "onboarding", "KYC", "signup", "investor", "issuer", "broker", "grain provisioning"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/docs.css"
heroDesc: "From signup to your first action on the platform — everything you need to get moving with regulated tokenized securities."
draft: false
---
<h2>Welcome to Sails.to</h2>
        <p>Sails.to is a regulated platform for tokenized securities issuance, compliance, and broker-mediated secondary trading. It is built as a <span class="glossary-term" data-term="wyoming-dao-llc">Wyoming DAO Series LLC</span> — a legal structure purpose-built for on-chain governance of real-world assets. Every offering is a Series. Every participant is cryptographically credentialed. Every action is compliant by default.</p>
        <p>This guide walks you through your first minutes on the platform: choosing your role, completing identity verification, and taking your first action. If you want the full architectural picture first, start with the <a href="/knowledge/docs/platform-overview/">Platform Overview</a>.</p>
        <h3>What You Need</h3>
        <ul>
            <li>A <a href="/knowledge/glossary/solana/">Solana</a>-compatible wallet (Phantom, Solflare, or any Ed25519 wallet)</li>
            <li>A government-issued photo ID (passport, national ID, or driver's license)</li>
            <li>Proof of address (utility bill, bank statement — issued within 90 days)</li>
            <li>For <span class="glossary-term" data-term="accredited-investor">accredited investors</span>: documentation of income or net worth</li>
        </ul>
        <h2>Choose Your Role</h2>
        <p>Every participant on Sails.to holds a role-specific <span class="glossary-term" data-term="nft-hierarchy">NFT</span> that defines what they can do on the platform. Your role determines which <span class="glossary-term" data-term="grain">grain</span> you receive and what capabilities are available to you.</p>
        <table>
            <thead>
                <tr>
                    <th>Role</th>
                    <th>Grain Provisioned</th>
                    <th>Grain Type</th>
                    <th>What You Can Do</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Issuer</strong></td>
                    <td>DAO Manager</td>
                    <td>Station</td>
                    <td>Create Series, launch offerings, manage <span class="glossary-term" data-term="cap-table">cap tables</span>, configure governance, execute <span class="glossary-term" data-term="distributions">distributions</span></td>
                </tr>
                <tr>
                    <td><strong>Investor</strong></td>
                    <td>Investor Self-Service</td>
                    <td>Instance</td>
                    <td>Browse offerings, subscribe, track portfolio, request <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, download tax documents</td>
                </tr>
                <tr>
                    <td><strong>Broker</strong></td>
                    <td>Broker Portal</td>
                    <td>Station</td>
                    <td>View available placements, submit investor subscriptions, manage <span class="glossary-term" data-term="secondary-trading">secondary trading</span>, track commissions</td>
                </tr>
                <tr>
                    <td><strong>Trustee</strong></td>
                    <td>Trustee Dashboard</td>
                    <td>Station</td>
                    <td>Authenticate <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, sign reconciliation reports, execute emergency freezes, maintain audit trail</td>
                </tr>
                <tr>
                    <td><strong>Introducer</strong></td>
                    <td>Introducer Tracking</td>
                    <td>Instance</td>
                    <td>Generate referral links, track introductions, calculate 25% <span class="glossary-term" data-term="commission">commission</span> share, view pipeline</td>
                </tr>
            </tbody>
        </table>
        <p><strong>Station grains</strong> are long-lived orchestrators — they manage multiple workflows and participants. <strong>Instance grains</strong> are per-entity workers — one per investor, one per verification, isolated and sovereign. See the <a href="/knowledge/docs/platform-overview/">Platform Overview</a> for the full grain architecture.</p>
        <h2>Step 1: Sign Up &amp; Verify Your Identity</h2>
        <p>Every participant completes <span class="glossary-term" data-term="kyc">KYC</span> verification before accessing the platform. This is not optional — regulated securities require verified participants. The process spawns a dedicated KYC/Onboarding grain for your verification, ensuring your personal data is isolated at the OS level from the moment it enters the system.</p>
        <p>The verification flow is a 10-step process:</p>
        <ol>
            <li><strong>Terms acceptance</strong> — Review and accept the platform terms of service (scroll + checkbox confirmation)</li>
            <li><strong>Email verification</strong> — Confirm your email address via one-time passcode</li>
            <li><strong>Phone verification</strong> — Confirm your phone number via one-time passcode</li>
            <li><strong>Document upload</strong> — Submit your government-issued photo ID and proof of address</li>
            <li><strong>Face capture</strong> — Selfie with liveness detection to match against your documents</li>
            <li><strong>AI processing</strong> — Automated OCR, face matching, and document verification</li>
            <li><strong>Risk assessment</strong> — Jurisdiction screening, PEP checks, and sanctions list review</li>
            <li><strong>Accreditation verification</strong> — For <span class="glossary-term" data-term="reg-d">Reg D</span> offerings: income or asset documentation</li>
            <li><strong>Compliance review</strong> — A human compliance officer reviews your application</li>
            <li><strong>Approval &amp; credential minting</strong> — Your <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT is minted on <a href="/knowledge/glossary/solana/">Solana</a></li>
        </ol>
        <p>Your KYC Credential NFT contains <strong>zero personally identifiable information</strong>. It encodes only classification flags — investor class, jurisdiction hash, regulatory exemption, verification level, and <span class="glossary-term" data-term="aml">AML</span>/PEP clearance status. Your actual documents and personal data are encrypted in your grain's journal store, sovereign to you. See the <a href="/knowledge/docs/compliance-framework/">Compliance Framework</a> for the full credential specification.</p>
        <h2>Step 2: Your Dashboard</h2>
        <p>Once verified, the platform provisions your role-specific grain. This is your workspace — an isolated, capability-secured environment that only you and explicitly authorized participants can access.</p>
        <h3>Issuer: DAO Manager</h3>
        <p>Your central governance hub. From here you create Series within your <span class="glossary-term" data-term="series-llc">DAO Series LLC</span>, appoint <span class="glossary-term" data-term="trustee">trustees</span> and paying agents, configure governance rules, and monitor compliance across all your offerings. Routes include a dashboard overview, individual Series detail, governance management, compliance logs, and participant directory.</p>
        <h3>Investor: Self-Service Portal</h3>
        <p>Your personal portfolio view. See every offering you hold tokens in, track <span class="glossary-term" data-term="distributions">distributions</span> and yields, request <span class="glossary-term" data-term="crossconversion">CrossConversions</span> between on-chain and <span class="glossary-term" data-term="bankable">bankable</span> formats, download tax documents, and participate in governance votes. One grain per investor — your data never co-mingles with anyone else's.</p>
        <h3>Broker: Broker Portal</h3>
        <p>Your placement and trading dashboard. View offerings you are approved to place, submit investor subscriptions linked to verified KYC credentials, track your 6% placement commissions, and manage <span class="glossary-term" data-term="secondary-trading">secondary OTC trading</span> within compliance rules. <span class="glossary-term" data-term="white-label">White-label</span> configuration is available for branded investor-facing pages.</p>
        <h3>Trustee: Trustee Dashboard</h3>
        <p>Your oversight console. View all Series under your trust jurisdiction, authenticate CrossConversions with your <span class="glossary-term" data-term="trustee">Trustee NFT</span>, sign reconciliation reports, and execute emergency freezes when required. Every action you take is logged to an immutable audit trail.</p>
        <h3>Introducer: Tracking Dashboard</h3>
        <p>Your referral pipeline. Generate unique referral links, track introductions from first contact through to funded offerings, and monitor your 25% <span class="glossary-term" data-term="commission">commission</span> share with automated payout reporting.</p>
        <h2>Step 3: Your First Actions</h2>
        <p>With your grain provisioned and your credentials verified, here is what to do next based on your role:</p>
        <table>
            <thead>
                <tr>
                    <th>Role</th>
                    <th>First Action</th>
                    <th>What Happens</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Issuer</strong></td>
                    <td>Create your first offering</td>
                    <td>An Offering grain is spawned — configure token supply, <span class="glossary-term" data-term="nominal-value">nominal value</span>, pricing, allowed jurisdictions, <span class="glossary-term" data-term="reg-d">Reg D</span>/<span class="glossary-term" data-term="reg-s">Reg S</span> exemption, and lock-up period. The offering's <span class="glossary-term" data-term="cap-table">cap table</span> begins tracking from the first mint.</td>
                </tr>
                <tr>
                    <td><strong>Investor</strong></td>
                    <td>Browse available offerings</td>
                    <td>Your grain receives <span class="glossary-term" data-term="powerbox">Powerbox</span> capabilities from Offering grains you are eligible for — filtered by your jurisdiction, accreditation tier, and the offering's compliance rules.</td>
                </tr>
                <tr>
                    <td><strong>Broker</strong></td>
                    <td>Review your approved placements</td>
                    <td>Your Broker Portal requests OfferingAPI capabilities from active Offering grains. You can begin submitting investor subscriptions once both you and the investor hold valid credentials.</td>
                </tr>
                <tr>
                    <td><strong>Trustee</strong></td>
                    <td>Review Series under your jurisdiction</td>
                    <td>Your dashboard populates with all Series that have appointed you as trustee. You can begin authenticating transactions and signing reconciliation reports immediately.</td>
                </tr>
                <tr>
                    <td><strong>Introducer</strong></td>
                    <td>Generate your first referral link</td>
                    <td>Share with prospective participants. The platform tracks the introduction from signup through to funded offering and calculates your commission automatically.</td>
                </tr>
            </tbody>
        </table>
        <h2>Authentication Model</h2>
        <p>Every action on Sails.to passes through four layers of authentication. No single layer is sufficient — all four must agree before any operation proceeds:</p>
        <ol>
            <li><strong>Solana Wallet Signature</strong> — Proves wallet ownership via Ed25519 cryptographic signature</li>
            <li><strong>NFT Verification</strong> — Proves role authorization. Your wallet must hold the correct <span class="glossary-term" data-term="nft-hierarchy">NFT</span> for the action you are requesting</li>
            <li><strong>Sandstorm Session</strong> — Proves grain access. OS-level isolation ensures you can only reach grains you have been granted access to</li>
            <li><strong><span class="glossary-term" data-term="powerbox">Powerbox</span> Capability</strong> — Proves inter-grain authority. A claim token becomes a sturdyRef, granting persistent cross-session access to specific capabilities</li>
        </ol>
        <p>This is defense in depth — not as a buzzword, but as architecture. Compromise one layer and three remain. See the <a href="/knowledge/docs/authentication/">Authentication documentation</a> for the complete model.</p>
        <h2>Next Steps</h2>
        <p>You are on the platform. Your credentials are minted. Your grain is provisioned. Here is where to go from here:</p>
        <ul>
            <li><a href="/knowledge/docs/platform-overview/">Platform Overview</a> — The three-pillar architecture, seven grain types, and data sovereignty model</li>
            <li><a href="/knowledge/docs/compliance-framework/">Compliance Framework</a> — KYC credentials, transfer enforcement, and regulatory reporting</li>
            <li><a href="/knowledge/docs/token-standard/">Token Standard</a> — How <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> tokens work on Solana</li>
            <li><a href="/knowledge/docs/authentication/">Authentication</a> — The four-layer authentication model in detail</li>
            <li><a href="/knowledge/docs/hybrid-architecture/">Hybrid Architecture</a> — How on-chain tokens bridge to <span class="glossary-term" data-term="bankable">bankable</span> securities via <span class="glossary-term" data-term="clearstream">Clearstream</span></li>
            <li><a href="/knowledge/docs/transfer-rules/">Transfer Rules</a> — Compliance checks enforced at the protocol level on every transfer</li>
            <li><a href="/knowledge/docs/api-reference/">API Reference</a> — <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> schemas and programmatic access</li>
        </ul>
    </div>
