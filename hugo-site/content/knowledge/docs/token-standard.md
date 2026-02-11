---
title: "Token Standard - Documentation"
description: "The sails_securities Anchor program — instructions, PDA accounts, events, and SPL-2022 Transfer Hook compliance extensions for regulated security tokens on Solana."
ogImage: "/og-image.png"
keywords: ["security token", "SPL-2022", "anchor program", "solana", "transfer hook", "PDA"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">Token Standard</h1>
    <p class="section-desc">The sails_securities program — security tokens with compliance enforcement at the protocol level.</p>
</section>

<section class="features-section">
    <div class="container">
        <h2>Program Overview</h2>
        <p>The <code>sails_securities</code> program is an <a href="/knowledge/glossary/solana/">Solana</a> Anchor program purpose-built for regulated securities issuance. It extends the <span class="glossary-term" data-term="melusina">Melusina</span> NFT authority pattern with securities-specific logic: offering lifecycle management, compliance-gated minting, <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox integration, distribution waterfall execution, and transfer enforcement via SPL-2022 <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span>.</p>
        <p>This is not a general-purpose token program. Every instruction assumes a regulated context. Every account structure encodes compliance constraints. Every event is designed for audit trail consumption. The program will reject any operation that violates its compliance rules — there is no admin override that bypasses the Transfer Hook, no backdoor for unverified wallets, no way to mint tokens to an investor without a valid <span class="glossary-term" data-term="kyc">KYC</span> credential.</p>
        <h2>Instructions</h2>
        <p>The program exposes eight core instructions. Each instruction enforces its own authorization requirements — the required NFT role, the threshold level, and the compliance checks are non-negotiable:</p>
        <table>
            <thead>
                <tr>
                    <th>Instruction</th>
                    <th>Parameters</th>
                    <th>Authorization</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>init_offering</code></strong></td>
                    <td><code>series_id, token_config, max_supply, nominal_value</code></td>
                    <td>Issuer NFT + Platform Operator approval</td>
                    <td>Creates the <span class="glossary-term" data-term="pda">PDA</span> for a new offering, links it to the <span class="glossary-term" data-term="series-llc">DAO Series LLC</span>, and initializes the <code>ComplianceConfig</code>. Sets the token mint, <span class="glossary-term" data-term="nominal-value">nominal value</span>, and maximum supply.</td>
                </tr>
                <tr>
                    <td><strong><code>mint_security_token</code></strong></td>
                    <td><code>offering_id, investor_wallet, amount</code></td>
                    <td>Issuer NFT or Broker NFT</td>
                    <td>Mints <span class="glossary-term" data-term="security-token">security tokens</span> to an investor. Requires the investor wallet to hold a valid, unexpired KYC Credential NFT with the correct <code>investor_class</code> and <code>jurisdiction_hash</code>. Checks <code>max_investors</code> limit before minting.</td>
                </tr>
                <tr>
                    <td><strong><code>burn_for_crossconversion</code></strong></td>
                    <td><code>offering_id, amount</code></td>
                    <td>Investor wallet + <span class="glossary-term" data-term="trustee">Trustee</span> NFT authentication</td>
                    <td>Locks tokens in the <span class="glossary-term" data-term="crossconversion-series">CrossConversion</span> lockbox PDA. Emits <code>CrossConversionRequested</code> event for <span class="glossary-term" data-term="isin">ISIN</span> issuance workflow. Increments the lockbox counter.</td>
                </tr>
                <tr>
                    <td><strong><code>distribute</code></strong></td>
                    <td><code>offering_id, amount_per_token</code></td>
                    <td><span class="glossary-term" data-term="paying-agent">Paying Agent</span> NFT + Trustee authentication</td>
                    <td>Executes dividend or interest <span class="glossary-term" data-term="distributions">distribution</span> to all token holders. Creates a <code>DistributionRecord</code> with a claimed bitmap for investor pull-based claiming.</td>
                </tr>
                <tr>
                    <td><strong><code>transfer_with_compliance</code></strong></td>
                    <td><code>from, to, amount</code></td>
                    <td>Sender wallet signature</td>
                    <td>Transfers tokens between wallets with full compliance verification. Checks both wallets for valid KYC, enforces lock-up period, validates jurisdiction whitelist, verifies accreditation tier. See <a href="/knowledge/docs/transfer-rules/">Transfer Rules</a>.</td>
                </tr>
                <tr>
                    <td><strong><code>freeze_account</code></strong></td>
                    <td><code>investor_wallet, reason</code></td>
                    <td>Security Admin NFT</td>
                    <td>Regulatory freeze on an investor's position. The investor cannot transfer, sell, or convert tokens until unfrozen. Reason is logged to the audit trail.</td>
                </tr>
                <tr>
                    <td><strong><code>force_transfer</code></strong></td>
                    <td><code>from, to, amount, court_order_hash</code></td>
                    <td>3-of-5 <span class="glossary-term" data-term="threshold-signing">keyholder threshold</span> + court order hash</td>
                    <td>Court-ordered transfer. Requires supermajority keyholder approval and an on-chain hash of the court order document. The most restricted instruction in the program.</td>
                </tr>
                <tr>
                    <td><strong><code>close_offering</code></strong></td>
                    <td><code>offering_id</code></td>
                    <td>Issuer NFT + Platform Operator + Trustee</td>
                    <td>Final redemption. Burns remaining tokens, settles outstanding <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, closes the offering PDA. Irreversible.</td>
                </tr>
            </tbody>
        </table>
        <h2>Account Structure</h2>
        <p>The program uses <span class="glossary-term" data-term="pda">Program Derived Addresses</span> (PDAs) to store all state on-chain. Each PDA is deterministically derived from its seed parameters, ensuring that account addresses are predictable and verifiable:</p>
        <table>
            <thead>
                <tr>
                    <th>PDA Account</th>
                    <th>Seeds</th>
                    <th>Fields</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>OfferingState</code></strong></td>
                    <td><code>["offering", series_id]</code></td>
                    <td><code>series_id</code>, <code>max_supply</code>, <code>minted</code>, <code>locked_in_crossconv</code>, <code>nominal_value</code>, <code>status</code> (active/paused/closed), <code>version</code></td>
                </tr>
                <tr>
                    <td><strong><code>InvestorPosition</code></strong></td>
                    <td><code>["position", offering_id, wallet]</code></td>
                    <td><code>offering_id</code>, <code>wallet</code>, <code>balance</code>, <code>locked_until</code> (lock-up expiry), <code>accreditation_tier</code>, <code>jurisdiction</code> (hash)</td>
                </tr>
                <tr>
                    <td><strong><code>CrossConversionLockbox</code></strong></td>
                    <td><code>["lockbox", offering_id]</code></td>
                    <td><code>offering_id</code>, <code>total_locked</code>, <code>isin_code</code>, <code>clearstream_ref</code></td>
                </tr>
                <tr>
                    <td><strong><code>DistributionRecord</code></strong></td>
                    <td><code>["distribution", offering_id, epoch]</code></td>
                    <td><code>offering_id</code>, <code>epoch</code>, <code>amount_per_token</code>, <code>claimed_bitmap</code> (tracks which investors have claimed)</td>
                </tr>
                <tr>
                    <td><strong><code>ComplianceConfig</code></strong></td>
                    <td><code>["compliance", offering_id]</code></td>
                    <td><code>offering_id</code>, <code>allowed_jurisdictions</code>, <code>min_investment</code>, <code>lock_up_days</code>, <code>max_investors</code>, <code>features</code> (bitmask), <code>version</code></td>
                </tr>
            </tbody>
        </table>
        <p>All PDA accounts include a <code>version</code> field to support data migration when the program is upgraded. The upgrade authority is held by the 3-of-5 <span class="glossary-term" data-term="master-nft">Master NFT</span> keyholder set — no single party can deploy a new program version.</p>
        <h2>Events</h2>
        <p>The program emits structured events for every significant state change. These events are consumed by the Solana Event Watcher grain, which routes them to the appropriate application grains for processing:</p>
        <table>
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Fields</th>
                    <th>Consumed By</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>SecurityMinted</code></strong></td>
                    <td><code>offering</code>, <code>investor</code>, <code>amount</code>, <code>timestamp</code></td>
                    <td>Offering Grain (cap table update), Investor Grain (portfolio notification)</td>
                </tr>
                <tr>
                    <td><strong><code>CrossConversionRequested</code></strong></td>
                    <td><code>offering</code>, <code>amount</code>, <code>direction</code>, <code>isin</code></td>
                    <td>CrossConversion Operator (initiates <span class="glossary-term" data-term="clearstream">Clearstream</span> workflow)</td>
                </tr>
                <tr>
                    <td><strong><code>DistributionPaid</code></strong></td>
                    <td><code>offering</code>, <code>epoch</code>, <code>total_amount</code></td>
                    <td>Investor Grains (claim notification), <span class="glossary-term" data-term="broker-dealer">Broker</span> Grain (settlement confirmation)</td>
                </tr>
                <tr>
                    <td><strong><code>ComplianceViolation</code></strong></td>
                    <td><code>offering</code>, <code>investor</code>, <code>reason</code></td>
                    <td>DAO Manager Grain (alert), Compliance Grain (regulatory log)</td>
                </tr>
                <tr>
                    <td><strong><code>TransferCompleted</code></strong></td>
                    <td><code>offering</code>, <code>from</code>, <code>to</code>, <code>amount</code></td>
                    <td>Offering Grain (cap table update), Broker Grain (trade settlement)</td>
                </tr>
            </tbody>
        </table>
        <p>Every event is also written to the Solana Event Watcher's local event log for replay capability. If a grain misses an event (network partition, grain restart), the watcher replays the missed events in order. No event is ever lost.</p>
        <h2>Compliance Extensions</h2>
        <p>The <code>sails_securities</code> program builds on <strong>SPL-2022</strong> (Token Extensions) — specifically the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> extension. This is the mechanism that makes compliance enforcement inescapable:</p>
        <ul>
            <li><strong>Transfer Hook:</strong> The Solana runtime invokes the Transfer Hook program on <em>every</em> token transfer — not just transfers initiated through the <code>sails_securities</code> program, but any SPL token transfer instruction that touches a Sails security token. This means compliance cannot be bypassed by calling the token program directly.</li>
            <li><strong>Hook Logic:</strong> The Transfer Hook reads both wallets' KYC Credential NFTs, the offering's <code>ComplianceConfig</code> PDA, and the sender's <code>InvestorPosition</code> PDA. If any check fails — expired KYC, jurisdiction mismatch, lock-up period active, accreditation insufficient — the hook returns an error and the entire transfer transaction is reverted.</li>
            <li><strong>Emergency Pause:</strong> The <code>ComplianceConfig</code> includes a <code>features</code> bitmask. Setting the pause bit (gated by Security Admin NFT) causes the Transfer Hook to reject all transfers for that offering — a circuit breaker for regulatory emergencies.</li>
            <li><strong>Upgradeable Programs:</strong> All Anchor programs are deployed with upgrade authority held by the 3-of-5 Master NFT keyholder set. PDA accounts include a <code>version</code> field for data migration. New program versions are deployed alongside old ones, and migration instructions move state from old PDAs to new PDAs. Every upgrade must pass full regression on devnet before mainnet deployment.</li>
        </ul>
        <p>The result: a <span class="glossary-term" data-term="security-token">security token</span> that carries its compliance rules with it. Not in documentation. Not in terms of service. In the program code that the <a href="/knowledge/glossary/solana/">Solana</a> runtime executes on every transfer. This is what "compliance as code" actually means.</p>
    </div>
</section>
