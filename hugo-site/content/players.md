---
title: "Platform Players"
description: "Follow a deal from first listing to investor payouts — and see exactly who does what at every step of the CrossSecurities lifecycle."
keywords:
  - platform participants
  - CrossSecurities lifecycle
  - issuers
  - investors
  - brokers
  - trustees
  - introducers
  - institutions
ogImage: "/og-players.png"
headScripts:
  - "/assets/js/mermaid.min.js"
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/players.css"
scripts:
  - "/js/players.js"
---

<section class="page-hero" style="background: var(--ink);">
    <span class="section-label">Understand</span>
    <h1 class="section-title">Life of a Deal</h1>
    <p class="section-subtitle">From first listing to investor payouts — follow a CrossSecurities deal through every stage and see who does what.</p>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- CAST OF CHARACTERS                              -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section" id="cast">
    <div class="content-container">
        <h2>The Cast</h2>
        <div class="players-grid">
            <div class="player-card">
                <div class="player-icon">🏢</div>
                <h3>Company</h3>
                <p>The ultimate issuer — the business raising capital. The legal issuer is a DAO Series LLC created for them</p>
            </div>
            <div class="player-card">
                <div class="player-icon">🔐</div>
                <h3>Trustee</h3>
                <p>Licensed fiduciary — holds escrow, protects investors</p>
            </div>
            <div class="player-card">
                <div class="player-icon">🏦</div>
                <h3>Broker</h3>
                <p>Licensed intermediary — connects investors to deals</p>
            </div>
            <div class="player-card">
                <div class="player-icon">👤</div>
                <h3>Investor</h3>
                <p>Professional / accredited — puts up the capital</p>
            </div>
            <div class="player-card">
                <div class="player-icon">🤝</div>
                <h3>Introducer</h3>
                <p>Refers the company — earns a share, no obligations</p>
            </div>
            <div class="player-card">
                <div class="player-icon">🏛️</div>
                <h3>Institution</h3>
                <p>Sails.to — or a licensed entity running the whole platform as a white-label under their own brand</p>
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 1 — THE LISTING                             -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-1">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">1</span>
            <div class="act-title">
                <h2>A Company Wants to Raise Capital</h2>
                <p>An introducer refers a business, or the company comes direct. The platform structures everything — legal entity, compliance, documents — and a trustee is appointed to protect future investors.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            INT["🤝 Introducer&lt;br/&gt;refers the company"]
            ISS["🏢 Company&lt;br/&gt;wants to raise $10M"]
            PLAT["🏛️ Institution&lt;br/&gt;Sails.to or white-label"]
            DAO["📄 DAO Series LLC&lt;br/&gt;legal issuing entity created"]
            TRU["🔐 Trustee&lt;br/&gt;appointed for oversight"]
            LIVE["✅ Offering&lt;br/&gt;goes live"]
            INT -.->|"introduction"| ISS
            ISS ==>|"submits deal"| PLAT
            PLAT ==>|"structures"| DAO
            DAO ==>|"compliance + docs"| ISS
            PLAT ==>|"trust deed"| TRU
            TRU ==>|"approved"| LIVE
            style INT fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px
            style ISS fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style PLAT fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style DAO fill:#6b46c1,color:#fff,stroke:#553c9a,stroke-width:2px
            style TRU fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style LIVE fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px
        </div>
        <div class="act-details">
            <div class="detail-item">
                <strong>🤝 Introducer</strong> — optional. Refers the business. Earns 25% of the platform's commission if the raise succeeds. Zero cost, no license needed, no further obligations.
            </div>
            <div class="detail-item">
                <strong>🏢 Company</strong> — the ultimate issuer. Provides deal details and receives a turnkey Wyoming DAO Series LLC — the legal issuing entity — plus Reg D / Reg S compliance, subscription agreements, and KYC platform. $0 upfront.
            </div>
            <div class="detail-item">
                <strong>🏛️ Institution</strong> — Sails.to is the default platform operator. Alternatively, a licensed entity (trust company, VC manager, multi-family office) can run the same infrastructure as a white-label under their own brand and regulatory wrapper.
            </div>
            <div class="detail-item">
                <strong>🔐 Trustee</strong> — selected from a pre-approved registry. Executes the trust deed, will hold the 3% security deposit, and monitors compliance throughout the life of the deal.
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 2 — DISTRIBUTION                            -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-2">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">2</span>
            <div class="act-title">
                <h2>Brokers Connect Investors to the Deal</h2>
                <p>The offering is distributed through a global network of licensed brokers. Each broker places their own KYC'd investors. Funds flow into escrow held by the trustee — nothing is released until the soft cap is hit.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            LIVE["✅ Offering Live&lt;br/&gt;$10M target"]
            B1["🏦 Broker A"]
            B2["🏦 Broker B"]
            B3["🏦 Broker C"]
            I1["👤 Investor 1&lt;br/&gt;$500k"]
            I2["👤 Investor 2&lt;br/&gt;$300k"]
            I3["👤 Investor 3&lt;br/&gt;$1M"]
            I4["👤 Investor 4&lt;br/&gt;$200k"]
            I5["👤 Investor 5&lt;br/&gt;$750k"]
            ESC["🔐 Escrow&lt;br/&gt;held by Trustee"]
            CAP["🎯 Soft Cap&lt;br/&gt;reached!"]
            LIVE --> B1
            LIVE --> B2
            LIVE --> B3
            B1 --> I1
            B1 --> I2
            B2 --> I3
            B2 --> I4
            B3 --> I5
            I1 -->|"subscribe"| ESC
            I2 -->|"subscribe"| ESC
            I3 -->|"subscribe"| ESC
            I4 -->|"subscribe"| ESC
            I5 -->|"subscribe"| ESC
            ESC ==>|"threshold met"| CAP
            style LIVE fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style B1 fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style B2 fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style B3 fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style I1 fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style I2 fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style I3 fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style I4 fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style I5 fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style ESC fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style CAP fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px
        </div>
        <div class="act-details">
            <div class="detail-item">
                <strong>🏦 Brokers</strong> — distribute the offering to their investor network. Earn up to 5% commission on primary placements (after soft cap). $0 to join.
            </div>
            <div class="detail-item">
                <strong>👤 Investors</strong> — accredited / professional only. Min $150k per investment. Subscribe through their broker. Securities issued on-chain (Solana) or in bankable form (ISIN via Clearstream).
            </div>
            <div class="detail-item">
                <strong>🔐 Trustee</strong> — holds all subscription funds in escrow. If the soft cap isn't reached, investors get a full refund.
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 3 — PROCEEDS                                -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-3">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">3</span>
            <div class="act-title">
                <h2>The Money Moves</h2>
                <p>Soft cap reached. Fees are deducted automatically and proceeds flow to the company. The trustee retains a 3% security deposit. Brokers get paid. The introducer gets their cut. Everyone earns only when the deal succeeds.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            CAP["🎯 $10M Raised"]
            FEE["💰 Fee Split"]
            ISS["🏢 Company&lt;br/&gt;receives ~$9M"]
            BRK["🏦 Brokers&lt;br/&gt;up to 5%"]
            TRU["🔐 Trustee&lt;br/&gt;⅔ of 1% annual"]
            DEP["🔒 Security Deposit&lt;br/&gt;3% held in trust"]
            PLT["🏛️ Institution&lt;br/&gt;⅓ of 1% + share of 6%"]
            INT["🤝 Introducer&lt;br/&gt;25% of platform's cut"]
            CAP ==> FEE
            FEE ==>|"proceeds"| ISS
            FEE -->|"commission"| BRK
            FEE -->|"trust fee begins"| TRU
            FEE -->|"reserved"| DEP
            FEE -->|"platform fee"| PLT
            PLT -.->|"referral share"| INT
            style CAP fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px
            style FEE fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style ISS fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style BRK fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style TRU fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style DEP fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px
            style PLT fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style INT fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px
        </div>
        <div class="fee-summary">
            <h3>The Numbers</h3>
            <div class="fee-grid">
                <div class="fee-item">
                    <span class="fee-amount">6%</span>
                    <span class="fee-label">distribution fee (broker-placed)</span>
                </div>
                <div class="fee-item">
                    <span class="fee-amount">1%</span>
                    <span class="fee-label">distribution fee (issuer's own referrals)</span>
                </div>
                <div class="fee-item">
                    <span class="fee-amount">1%/yr</span>
                    <span class="fee-label">trust &amp; admin — ⅔ trustee, ⅓ platform</span>
                </div>
                <div class="fee-item">
                    <span class="fee-amount">3%</span>
                    <span class="fee-label">security deposit — returned at term end</span>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 4 — OTC TRADING                             -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-4">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">4</span>
            <div class="act-title">
                <h2>Investors Trade</h2>
                <p>Securities are live. Investors can sell to other investors through the multi-broker OTC network. Trades settle instantly (T+0) on-chain — no clearing house delays, no invoices. Commissions pay out at execution.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            SELL["👤 Seller&lt;br/&gt;wants out"]
            BUY["👤 Buyer&lt;br/&gt;wants in"]
            SB["🏦 Sell Broker"]
            BB["🏦 Buy Broker"]
            OTC["⚡ OTC Network&lt;br/&gt;T+0 settlement"]
            SELL ==>|"list"| SB
            BUY ==>|"bid"| BB
            SB ==>|"sell order"| OTC
            BB ==>|"buy order"| OTC
            OTC ==>|"securities"| BUY
            OTC ==>|"payment"| SELL
            style SELL fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style SB fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style OTC fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px
            style BB fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style BUY fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
        </div>
        <div class="act-details">
            <div class="detail-item">
                <strong>0.5% brokerage fee</strong> — paid by the buyer — split three ways: ⅓ buy-side broker, ⅓ sell-side broker, ⅓ platform. Waived during soft cap phase.
            </div>
            <div class="detail-item">
                <strong>CrossConversion</strong> — investors can switch between on-chain tokens (Solana, 24/7, self-custody) and bankable ISIN form (Clearstream, settles to any bank). 0.75% fee, split between trustee and platform.
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 5 — PAYOUTS                                 -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-5">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">5</span>
            <div class="act-title">
                <h2>Investors Get Paid</h2>
                <p>The company generates returns — interest on a bond, profit share on equity, dividends, or revenue distributions. Payments flow through the trustee and are distributed automatically to every investor's wallet or bank account.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            ISS["🏢 Company&lt;br/&gt;generates revenue"]
            TRU["🔐 Trustee&lt;br/&gt;verifies &amp; authorises"]
            DIST["⚡ Platform&lt;br/&gt;distributes automatically"]
            I1["👤 Investor 1&lt;br/&gt;receives $25k"]
            I2["👤 Investor 2&lt;br/&gt;receives $15k"]
            I3["👤 Investor 3&lt;br/&gt;receives $50k"]
            I4["👤 Investor 4&lt;br/&gt;receives $10k"]
            I5["👤 Investor 5&lt;br/&gt;receives $37.5k"]
            ISS ==>|"payment"| TRU
            TRU ==>|"approved"| DIST
            DIST ==>|"on-chain or bank"| I1
            DIST ==>|"on-chain or bank"| I2
            DIST ==>|"on-chain or bank"| I3
            DIST ==>|"on-chain or bank"| I4
            DIST ==>|"on-chain or bank"| I5
            style ISS fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style TRU fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style DIST fill:#3182ce,color:#fff,stroke:#2c5282,stroke-width:2px
            style I1 fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style I2 fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style I3 fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style I4 fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style I5 fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
        </div>
        <div class="act-details">
            <div class="detail-item">
                <strong>Interest, dividends, profit share, revenue distributions</strong> — whatever the offering terms specify. The smart contract enforces the schedule automatically.
            </div>
            <div class="detail-item">
                <strong>🔐 Trustee</strong> — verifies each distribution against the trust deed before authorising. If the company misses payments, the trustee enforces remedies using the 3% security deposit.
            </div>
            <div class="detail-item">
                <strong>On-chain or bank</strong> — investors holding tokens get paid on-chain instantly. Investors holding ISIN securities receive payments through Clearstream to their bank.
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- ACT 6 — MATURITY                                -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section act-section" id="act-6">
    <div class="content-container">
        <div class="act-header">
            <span class="act-number">6</span>
            <div class="act-title">
                <h2>The Deal Closes</h2>
                <p>At maturity — or whenever the term ends — principal is returned, the security deposit goes back to the company, and the trustee's role concludes. Full lifecycle, start to finish.</p>
            </div>
        </div>
        <div class="mermaid">
        flowchart TD
            MAT["📅 Maturity"]
            ISS["🏢 Company&lt;br/&gt;repays principal"]
            TRU["🔐 Trustee&lt;br/&gt;releases deposit"]
            INV["👤 Investors&lt;br/&gt;principal returned"]
            DONE["✅ Deal&lt;br/&gt;complete"]
            MAT ==> ISS
            ISS ==>|"final payment"| TRU
            TRU ==>|"distributed"| INV
            TRU ==>|"3% deposit returned"| ISS
            INV ==> DONE
            style MAT fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px
            style ISS fill:#805ad5,color:#fff,stroke:#6b46c1,stroke-width:2px
            style TRU fill:#d69e2e,color:#fff,stroke:#b7791f,stroke-width:2px
            style INV fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px
            style DONE fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- WHO EARNS WHAT                                  -->
<!-- ═══════════════════════════════════════════════ -->

<section class="content-section" id="earnings">
    <div class="content-container">
        <h2>Who Earns What</h2>
        <div class="earnings-grid">
            <div class="earnings-card">
                <div class="earnings-icon">🏢</div>
                <h3>Company</h3>
                <p class="earnings-amount">Raises capital</p>
                <p class="earnings-detail">$0 upfront. 6% distribution fee (broker-placed) or 1% (own referrals). 1%/yr trust fee. 3% security deposit (returned). Legal issuer is a DAO Series LLC created for them.</p>
            </div>
            <div class="earnings-card">
                <div class="earnings-icon">👤</div>
                <h3>Investor</h3>
                <p class="earnings-amount">Returns on investment</p>
                <p class="earnings-detail">0.5% brokerage on secondary trades (waived during soft cap). 0.75% CrossConversion fee. No fees at issuance.</p>
            </div>
            <div class="earnings-card">
                <div class="earnings-icon">🏦</div>
                <h3>Broker</h3>
                <p class="earnings-amount">Up to 5% primary + 0.167% per trade</p>
                <p class="earnings-detail">Commission on placements (after soft cap). ⅓ of 0.5% brokerage fee on every secondary trade. $0 to join.</p>
            </div>
            <div class="earnings-card">
                <div class="earnings-icon">🔐</div>
                <h3>Trustee</h3>
                <p class="earnings-amount">⅔ of 1% annual + CrossConversion share</p>
                <p class="earnings-detail">Ongoing trust &amp; admin fee for the life of every deal they oversee. Plus a share of the 0.75% CrossConversion fee. Pre-approval required.</p>
            </div>
            <div class="earnings-card">
                <div class="earnings-icon">🤝</div>
                <h3>Introducer</h3>
                <p class="earnings-amount">25% of platform's commission</p>
                <p class="earnings-detail">One introduction. If the company raises $2M through brokers, the introducer earns ~$30k. No license, no cost, no obligations.</p>
            </div>
            <div class="earnings-card">
                <div class="earnings-icon">🏛️</div>
                <h3>Institution</h3>
                <p class="earnings-amount">Custom — controls own fee structure</p>
                <p class="earnings-detail">Sails.to is the default operator. Licensed entities can run the full platform as a white-label under their own brand. Approves issuers, authorises trustees, controls broker networks.</p>
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════ -->
<!-- CTA                                             -->
<!-- ═══════════════════════════════════════════════ -->

<section class="cta-section">
    <div class="content-container" style="text-align: center;">
        <h2>Which player are you?</h2>
        <p>Every role has a page. Find yours.</p>
        <div class="cta-buttons">
            <a href="/issuers/" class="btn-secondary">Raise Capital</a>
            <a href="/investors/" class="btn-secondary">Invest</a>
            <a href="/brokers/" class="btn-secondary">Broker</a>
            <a href="/trustees/" class="btn-secondary">Trustee</a>
            <a href="/introducers/" class="btn-secondary">Introduce</a>
            <a href="/regulated/" class="btn-secondary">Institution</a>
        </div>
        <div style="margin-top: 24px;">
            <a href="/signup/" class="btn-primary">Get Started</a>
        </div>
    </div>
</section>
