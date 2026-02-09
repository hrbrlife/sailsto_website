---
title: "CrossConversion Explained: Connecting On-Chain to Bankable Securities"
date: 2025-01-25
description: "How Sails.to's CrossConversion enables CrossSecurities to move seamlessly between Solana blockchain and Clearstream institutional custody."
ogImage: "/og-image.png"
keywords: ["crossconversion", "explained", "connecting", "on-chain", "bankable", "securities", "sails", "enables"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/blog-post.css"
---

<header class="blog-header">
    <div class="container">
        <a href="/knowledge/blog/" class="back-link">← Back to Blog</a>
        <span class="blog-category">Technology</span>
        <h1 class="blog-title">CrossConversion Explained: Connecting On-Chain to Bankable Securities</h1>
        <div class="blog-meta">
            <span>By Sails.to Team</span>
            <span>•</span>
            <span>January 25, 2026</span>
            <span>•</span>
            <span>13 min read</span>
        </div>
    </div>
</header>
<main class="blog-content">
    <div class="blog-content-inner">
        <p>One of the most common barriers to institutional adoption of <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> is custody. Banks, family offices, and funds have established custodians they trust. Asking them to self-custody on blockchain is often a non-starter.</p>
        <p>That's why we built <span class="glossary-term" data-term="crossconversion">CrossConversion</span>—enabling CrossSecurities to exist simultaneously in both on-chain and bankable formats.</p>
        <h2>The Problem: Two Worlds, One Security</h2>
        <p>Today's securities infrastructure is bifurcated:</p>
        <div class="layer-card">
            <div class="layer-icon">⛓️</div>
            <div class="layer-content">
                <h4>On-Chain Form</h4>
                <p><span class="glossary-term" data-term="solana">Solana</span> and other chains offer programmable ownership, instant settlement, and self-custody. Crypto-native investors love it. Some institutions can't use it.</p>
            </div>
        </div>
        <div class="layer-card">
            <div class="layer-icon">🏦</div>
            <div class="layer-content">
                <h4>Bankable Form</h4>
                <p><span class="glossary-term" data-term="clearstream">Clearstream</span>, Euroclear, DTC provide institutional custody, <span class="glossary-term" data-term="isin">ISIN</span> identifiers, and established settlement rails. Trusted by trillions in assets. Institutions require it.</p>
            </div>
        </div>
        <p>Most platforms force you to choose. Issue on blockchain and lose institutions. Issue traditionally and lose blockchain benefits.</p>
        <p>CrossConversion eliminates this tradeoff.</p>
        <h2>How CrossConversion Works</h2>
        <h3>The Core Concept: Synchronized Forms</h3>
        <p>The same security can exist in two formats:</p>
        <ul>
            <li><strong>On-Chain Form:</strong> SPL token on Solana with embedded compliance via <span class="glossary-term" data-term="smart-contract">smart contract</span></li>
            <li><strong>Bankable Form:</strong> ISIN-bearing security held in institutional <span class="glossary-term" data-term="custody">custody</span></li>
        </ul>
        <p>These aren't different securities—they're different representations of the same underlying ownership. CrossConverting between them doesn't change your rights; it changes where the record lives.</p>
        <h3>The CrossConversion Mechanism</h3>
        <div class="flow-steps">
            <div class="flow-step">
                <div>
                    <strong>Cross to Bankable</strong><br>
                    <p>Investor holding on-chain tokens requests CrossConversion. Tokens are locked in the CrossConversion Series. Equivalent units credited to investor's Clearstream account via their custodian.</p>
                </div>
            </div>
            <div class="flow-step">
                <div>
                    <strong>Custody Verification</strong><br>
                    <p>Clearstream holdings are verified and reconciled with on-chain locked amounts. Total supply always matches across both forms.</p>
                </div>
            </div>
            <div class="flow-step">
                <div>
                    <strong>Cross to On-Chain</strong><br>
                    <p>Investor requests CrossConversion back to on-chain. Clearstream position debited. Equivalent tokens unlocked to verified wallet address.</p>
                </div>
            </div>
        </div>
        <h3>Why Clearstream?</h3>
        <p><span class="glossary-term" data-term="clearstream">Clearstream</span> is one of the world's largest International Central Securities Depositories (ICSDs). Choosing Clearstream provides:</p>
        <ul>
            <li><strong>Global reach:</strong> Settlement in 110+ markets</li>
            <li><strong>Institutional trust:</strong> €16+ trillion in assets under custody</li>
            <li><strong>ISIN assignment:</strong> International Securities Identification Number recognized globally</li>
            <li><strong>Regulatory compliance:</strong> Compliant with EU securities regulations</li>
            <li><strong>Integration:</strong> Connected to existing institutional workflows</li>
        </ul>
        <h2>Comparing the Two Forms</h2>
        <table class="comparison-table">
            <tr>
                <th>Feature</th>
                <th>On-Chain Form</th>
                <th>Bankable Form</th>
            </tr>
            <tr>
                <td>Custody model</td>
                <td>Self-custody (investor controls keys)</td>
                <td>Institutional custody (via bank/broker)</td>
            </tr>
            <tr>
                <td>Settlement speed</td>
                <td>Seconds (blockchain finality)</td>
                <td>T+2 (standard securities settlement)</td>
            </tr>
            <tr>
                <td>Identifier</td>
                <td>Token contract address</td>
                <td>ISIN number</td>
            </tr>
            <tr>
                <td>24/7 trading</td>
                <td>Yes</td>
                <td>Market hours only</td>
            </tr>
            <tr>
                <td>Ideal for</td>
                <td>Crypto-native investors, on-chain integration</td>
                <td>Banks, funds, family offices</td>
            </tr>
            <tr>
                <td>Distributions</td>
                <td>Direct to wallet (stablecoin)</td>
                <td>Through custodian (cash)</td>
            </tr>
        </table>
        <h2>Use Cases</h2>
        <h3>The Crypto-Native Investor</h3>
        <p>You want maximum control. Self-custody is non-negotiable. DeFi composability is appealing. You stay on Solana, hold tokens in your wallet, and receive stablecoin <span class="glossary-term" data-term="distributions">distributions</span> directly.</p>
        <h3>The Family Office</h3>
        <p>You manage a $50M portfolio through Goldman Sachs custody. Your compliance team requires recognized securities identifiers. You hold via Clearstream—same security, familiar infrastructure, ISIN for reporting.</p>
        <h3>The Flexible Investor</h3>
        <p>You start on-chain for the immediate settlement. Six months later, you're refinancing your portfolio and need securities that appear on traditional statements. CrossConvert to bankable. Later, you want self-custody again. CrossConvert back. Same position, different formats.</p>
        <h3>The Issuer</h3>
        <p>You're raising capital globally. Some investors are crypto funds wanting on-chain tokens. Others are European family offices requiring ISIN custody. With CrossConversion, you accommodate both from a single issuance.</p>
        <h2>Technical Architecture</h2>
        <h3>On-Chain Components (Solana)</h3>
        <ul>
            <li><strong>Token Program:</strong> SPL token with compliance extensions</li>
            <li><strong>Whitelist Contract:</strong> Only <span class="glossary-term" data-term="kyc">KYC</span>-verified addresses can hold</li>
            <li><strong>CrossConversion Contract:</strong> Manages lock/unlock for CrossConverted tokens</li>
            <li><strong>Distribution Contract:</strong> Automates dividend/distribution payments</li>
        </ul>
        <h3>Off-Chain Components</h3>
        <ul>
            <li><strong>CrossConversion Operator:</strong> Coordinates between on-chain and Clearstream</li>
            <li><strong>Reconciliation Engine:</strong> Ensures supply matching across forms</li>
            <li><strong>KYC/AML Provider:</strong> Verifies investor eligibility</li>
            <li><strong>Reporting System:</strong> Generates compliant investor communications</li>
        </ul>
        <h3>Clearstream Integration</h3>
        <ul>
            <li><strong>ISIN Assignment:</strong> Each tokenized security receives a unique ISIN</li>
            <li><strong>Custody Interface:</strong> API connection to Clearstream systems</li>
            <li><strong>Corporate Actions:</strong> Distributions, voting, and other events coordinated</li>
        </ul>
        <h2>Security Considerations</h2>
        <h3>Supply Integrity</h3>
        <p>The most critical requirement: total supply must always match across forms. If 1 million tokens are issued:</p>
        <ul>
            <li>Circulating on Solana + Locked in CrossConversion Series + Held at Clearstream = 1 million</li>
            <li>Any discrepancy triggers automatic halt and audit</li>
        </ul>
        <h3>Custody Security</h3>
        <ul>
            <li><strong>On-chain form:</strong> Investor-controlled keys; platform never holds</li>
            <li><strong>Bankable form:</strong> Institutional custody with segregated accounts</li>
            <li><strong>CrossConversion funds:</strong> Multi-signature control requiring multiple parties</li>
        </ul>
        <h3>KYC Persistence</h3>
        <p>Verification carries across forms. A KYC-verified investor in on-chain form remains verified when CrossConverting to bankable form. Their identity is confirmed; only the custody location changes.</p>
        <h2>Benefits for Issuers</h2>
        <ul>
            <li><strong>Maximum investor reach:</strong> Accommodate all investor preferences from single issuance</li>
            <li><strong>Single cap table:</strong> Despite dual representation, one unified <span class="glossary-term" data-term="cap-table">cap table</span></li>
            <li><strong>Simplified distributions:</strong> Platform handles routing payments to correct layer</li>
            <li><strong>Future flexibility:</strong> As markets evolve, securities can move between systems</li>
        </ul>
        <h2>Benefits for Investors</h2>
        <ul>
            <li><strong>Custody choice:</strong> Self-custody or institutional—your preference</li>
            <li><strong>Flexibility:</strong> Change custody models as needs evolve</li>
            <li><strong>Same rights:</strong> Economic and governance rights identical regardless of layer</li>
            <li><strong>Interoperability:</strong> Access benefits of both systems</li>
        </ul>
        <h2>The CrossSecurities Future</h2>
        <p>CrossConversion represents our thesis: the future isn't blockchain replacing traditional finance—it's both systems working together.</p>
        <p>Institutions won't abandon established infrastructure. Crypto-natives won't accept centralized custody. The winning platforms accommodate both, letting each participant choose their preferred model while accessing the same investment opportunities.</p>
        <p>That's what Sails CrossSecurities delivers: one security, two forms, unlimited flexibility.</p>
        <div class="blog-cta">
            <h3>Invest your way</h3>
            <p>Self-custody or institutional—access the same tokenized securities either way.</p>
            <a href="/signup/?type=investor" class="btn">Start Investing</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>

