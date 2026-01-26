---
title: "For Brokers"
description: "Expand your product offering with tokenized securities. 6% placement fee, secondary trading commissions, white-label capabilities."
keywords:
  - broker network
  - securities distribution
  - OTC settlement
  - tokenized securities
  - commission sharing
  - broker-dealer
  - securities trading
ogImage: "/og-brokers.png"
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/brokers.css"
scripts:
  - "/js/brokers.js"
---

<section class="page-hero" style="background: var(--navy);">
    <span class="section-label">For Brokers</span>
    <h1 class="section-title">Plug into a<br>ready-built network</h1>
    <p class="section-desc">Access primary and secondary deal flow from day one. No platform development. No compliance infrastructure to build. Route orders, earn commissions, serve clients who want both digital and traditional custody options.</p>
</section>
<section class="detail-section">
    <div class="detail-container">
        <div class="detail-grid">
            <div class="detail-content">
                <h2>Commission sharing built in</h2>
                <p>Every trade on the platform generates revenue that flows directly to participating brokers. No negotiation, no manual billing. Commissions are calculated and distributed automatically on-chain.</p>
                <p>When you place investors in a primary offering, you earn commission from the <strong>6% distribution fee</strong>: the issuer may offer a placement reward (typically 3%), and Sails.to automatically shares 2% of its 6% fee with you. Secondary trading carries a 0.5% fee split equally: ⅓ platform, ⅓ buy-side broker, ⅓ sell-side broker.</p>
                <p><em style="color:#38a169;"><strong>Note:</strong> During soft cap phase, brokerage fees are waived. Primary placement commissions only apply to distributions after soft cap is reached.</em></p>
            </div>
            <ul class="detail-list">
                <li>
                    <span class="icon">💰</span>
                    <div class="text">
                        <h4>Primary Placement: up to 5%</h4>
                        <p>Up to 3% issuer reward + 2% from Sails.to's 6% fee. <em>(After soft cap)</em></p>
                    </div>
                </li>
                <li>
                    <span class="icon">🔄</span>
                    <div class="text">
                        <h4>Secondary Trades: 0.5%</h4>
                        <p>Split ⅓ platform, ⅓ buy-side broker, ⅓ sell-side broker.</p>
                    </div>
                </li>
                <li>
                    <span class="icon">⚡</span>
                    <div class="text">
                        <h4>Instant Settlement</h4>
                        <p>Commissions distribute on-chain at trade execution. No T+2, no invoice cycles.</p>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</section>
<section class="detail-section alt">
    <div class="detail-container">
        <style>
            .calc-card {
                background: white;
                padding: 40px;
                border: 1px solid rgba(0,0,0,0.08);
                max-width: 900px;
                margin: 0 auto;
            }
            .calc-card h2 {
                font-family: var(--font-display);
                font-size: 1.8rem;
                color: var(--ink);
                margin-bottom: 8px;
            }
            .calc-card .intro {
                color: var(--slate);
                margin-bottom: 32px;
            }
            .calc-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 48px;
            }
            @media (max-width: 768px) {
                .calc-grid { grid-template-columns: 1fr; }
            }
            .calc-inputs {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .input-group {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            .input-group label {
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--ink);
            }
            .input-group input {
                padding: 12px 16px;
                border: 1px solid rgba(0,0,0,0.12);
                font-size: 1rem;
                color: var(--ink);
            }
            .input-group input:focus {
                outline: none;
                border-color: var(--gold);
            }
            .input-hint {
                font-size: 0.8rem;
                color: var(--silver);
            }
            .calc-results {
                background: var(--cream);
                padding: 24px;
            }
            .result-section {
                margin-bottom: 24px;
                padding-bottom: 24px;
                border-bottom: 1px solid rgba(0,0,0,0.08);
            }
            .result-section:last-child {
                margin-bottom: 0;
                padding-bottom: 0;
                border-bottom: none;
            }
            .result-section h4 {
                font-size: 0.7rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--slate);
                margin-bottom: 12px;
            }
            .result-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 0;
                font-size: 0.95rem;
            }
            .result-row .label {
                color: var(--ink);
            }
            .result-row .value {
                font-weight: 600;
                color: var(--ink);
            }
            .result-row.sub {
                padding-left: 16px;
                font-size: 0.85rem;
                color: var(--slate);
            }
            .result-row.sub .value {
                font-weight: 500;
                color: var(--slate);
            }
            .result-total {
                background: var(--ink);
                color: white;
                padding: 16px;
                margin: -24px;
                margin-top: 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .result-total .label {
                font-weight: 600;
            }
            .result-total .value {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--gold);
            }
            .assumptions {
                margin-top: 24px;
                padding: 16px;
                background: rgba(201,162,39,0.08);
                font-size: 0.8rem;
                color: var(--slate);
            }
            .assumptions strong {
                color: var(--ink);
            }
        </style>
        <div class="calc-card">
            <h2>💰 Broker Earnings Calculator</h2>
            <p class="intro">Estimate your annual earnings from primary placements and secondary trading activity.</p>
            <div class="calc-grid">
                <div class="calc-inputs">
                    <div class="input-group">
                        <label for="placementAmount">Placement Amount</label>
                        <input type="text" id="placementAmount" value="20,000,000">
                        <span class="input-hint">Total primary placement you bring</span>
                    </div>
                    <div class="input-group">
                        <label for="issuerReward">Issuer Reward (%)</label>
                        <input type="number" id="issuerReward" value="3" min="0" max="10" step="0.5">
                        <span class="input-hint">Issuer's placement bonus to broker</span>
                    </div>
                    <div class="input-group">
                        <label for="sailsShare">Sails.to Share (%)</label>
                        <input type="number" id="sailsShare" value="2" min="0" max="6" step="0.5">
                        <span class="input-hint">Sails.to shares from its 6% distribution fee</span>
                    </div>
                    <div class="input-group">
                        <label for="annualTurnover">Annual Turnover (%)</label>
                        <input type="number" id="annualTurnover" value="30" min="0" max="100" step="5">
                        <span class="input-hint">% of outstanding securities traded per year</span>
                    </div>
                    <div class="input-group">
                        <label for="brokerParticipation">Your Participation in Secondary (%)</label>
                        <input type="number" id="brokerParticipation" value="10" min="0" max="100" step="1">
                        <span class="input-hint">% of secondary deals you participate in</span>
                    </div>
                    <div class="input-group">
                        <label for="commissionShare">Your Commission Share (%)</label>
                        <input type="number" id="commissionShare" value="60" min="50" max="67" step="1">
                        <span class="input-hint">50-67% of broker commission on your deals</span>
                    </div>
                </div>
                <div class="calc-results" id="brokerResults">
                </div>
            </div>
            <div class="assumptions">
                <strong>Assumptions:</strong> Secondary trading commission is 0.5% total, split ⅓ platform, ⅓ buy-side broker, ⅓ sell-side broker (~0.17% each). Primary placement commissions only apply after soft cap is reached. Your share depends on deal structure and whether you represent one or both sides.
            </div>
        </div>
    </div>
</section>
<section class="detail-section alt">
    <div class="detail-container">
        <div class="detail-grid">
            <div class="detail-content">
                <h2>Multi-broker atomic settlement</h2>
                <p>A single order can fill across multiple brokers in one on-chain transaction. No counterparty risk: either the entire trade settles or none of it does.</p>
                <p>This means better fills for clients, more commission opportunities for brokers, and zero manual reconciliation. The smart contract handles matching, netting, and distribution in a single atomic operation.</p>
            </div>
            <ul class="detail-list">
                <li>
                    <span class="icon">🔗</span>
                    <div class="text">
                        <h4>Atomic Execution</h4>
                        <p>All-or-nothing settlement. No partial fills that leave positions hanging.</p>
                    </div>
                </li>
                <li>
                    <span class="icon">🛡️</span>
                    <div class="text">
                        <h4>Zero Counterparty Risk</h4>
                        <p>Settlement and delivery happen simultaneously. No credit exposure between brokers.</p>
                    </div>
                </li>
                <li>
                    <span class="icon">📊</span>
                    <div class="text">
                        <h4>Automatic Reconciliation</h4>
                        <p>On-chain transactions are the source of truth. No end-of-day matching required.</p>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</section>
<section class="detail-section">
    <div class="detail-container">
        <div class="detail-grid">
            <div class="detail-content">
                <h2>OTC liquidity network</h2>
                <p>Quote and trade within a verified universe of eligible investors. When your client needs broader liquidity, route to the network and access inventory across all participating brokers.</p>
                <p>All trades remain compliant. Investor eligibility is enforced at the protocol level, audit trails are automatic, and settlement is instant.</p>
            </div>
            <ul class="detail-list">
                <li>
                    <span class="icon">🌐</span>
                    <div class="text">
                        <h4>Cross-Broker Routing</h4>
                        <p>Access liquidity from the entire network when your book can't fill an order.</p>
                    </div>
                </li>
                <li>
                    <span class="icon">✓</span>
                    <div class="text">
                        <h4>Pre-Verified Investors</h4>
                        <p>Only eligible investors in the system. KYC and accreditation already complete.</p>
                    </div>
                </li>
                <li>
                    <span class="icon">📋</span>
                    <div class="text">
                        <h4>Automatic Audit Trail</h4>
                        <p>Every quote, order, and settlement recorded on-chain. Compliance reporting built in.</p>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</section>
<section class="features-section">
    <div class="features-container">
        <div class="features-header">
            <span class="section-label">What You Get</span>
            <h2 class="section-title">Infrastructure without the build</h2>
        </div>
        <div class="feature-grid three-col">
            <div class="feature-card">
                <span class="feature-icon">📱</span>
                <h3>Trading Interface</h3>
                <p>Web-based order entry for primary subscriptions and secondary trading. White-label available for your own clients.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">🔐</span>
                <h3>Custody Options</h3>
                <p>Hold client assets on Solana or convert to ISIN for traditional custody via Clearstream. You choose what fits each client.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">📊</span>
                <h3>Position & P&L Reporting</h3>
                <p>Real-time positions, transaction history, and performance reporting. Export for your back office systems.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">📄</span>
                <h3>Deal Flow Access</h3>
                <p>See all active offerings with full disclosure documents. Filter by asset type, geography, minimum investment.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">🤝</span>
                <h3>Investor Onboarding</h3>
                <p>Platform handles KYC/AML verification. Bring your clients, we verify eligibility and maintain the records.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">💼</span>
                <h3>Commission Dashboard</h3>
                <p>Track earned commissions in real-time. See pending distributions and historical payouts.</p>
            </div>
        </div>
    </div>
</section>
<section class="detail-section alt">
    <div class="detail-container">
        <div class="stats-row" style="margin-top: 0; padding-top: 0; border-top: none;">
            <div class="stat-item">
                <div class="stat-value">6%</div>
                <div class="stat-label">Primary commission</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">⅔</div>
                <div class="stat-label">Secondary share</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">T+0</div>
                <div class="stat-label">Settlement</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">$0</div>
                <div class="stat-label">Platform fees</div>
            </div>
        </div>
    </div>
</section>
<section class="cta-section">
    <h2>Ready to join the network?</h2>
    <p>Licensed brokers can onboard in days. No platform development, no compliance build-out.</p>
    <a href="/signup/?type=broker" class="btn btn-primary">
        Apply Now
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
    </a>
</section>
