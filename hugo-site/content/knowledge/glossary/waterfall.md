---
title: "Waterfall - Glossary"
description: "The revenue distribution priority structure for Sails.to offerings, enforcing investor-first payment order on-chain via smart contracts."
ogImage: "/og-image.png"
keywords: ["waterfall", "glossary", "revenue", "distribution", "priority", "investor", "on-chain", "smart contract"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Finance</span>
        <h1 class="term-title">Waterfall</h1>
        <p class="term-short">The revenue distribution priority structure for Sails.to offerings, enforcing investor-first payment order on-chain via smart contracts.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p>The <strong>Waterfall</strong> is the predefined priority structure that governs how revenue flows through a Sails.to offering. When income enters the <a href="/knowledge/glossary/operating-series/">Operating Series</a>, it does not sit in a pool waiting for someone to decide where it goes. It flows — automatically, programmatically, inevitably — through the waterfall in strict priority order:</p>
            <ol>
                <li><strong>Senior Debt Holders:</strong> Any senior obligations are satisfied first</li>
                <li><strong>Investor <a href="/knowledge/glossary/distributions/">Distributions</a>:</strong> Pro-rata payments to all token holders based on their proportional ownership</li>
                <li><strong>Platform Fee:</strong> 1% to the Sails.to platform</li>
                <li><strong>Excess to <a href="/knowledge/glossary/treasury-series/">Treasury Series</a>:</strong> Any remaining revenue flows to the offering's treasury reserve</li>
            </ol>
            <p>This waterfall is encoded in the <code>sails_distributions</code> <a href="/knowledge/glossary/smart-contract/">smart contract</a> and enforced on-chain. The order cannot be altered, resequenced, or overridden after deployment.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>In traditional fund structures, the waterfall exists in a legal document. The fund manager executes it. Investors trust that the manager follows the document. History is littered with examples of that trust being violated — fees taken before investors are paid, reserves raided, priority structures quietly reinterpreted.</p>
            <p>On Sails.to, the waterfall is not a document. It is code. The <a href="/knowledge/glossary/paying-agent/">Paying Agent</a> executes <a href="/knowledge/glossary/distributions/">distributions</a> under <a href="/knowledge/glossary/trustee/">Trustee</a> oversight, but neither can alter the priority order. Investors are paid before the platform takes its fee. The platform takes its fee before excess reaches the treasury. This is not a promise. It is a mathematical certainty enforced by <a href="/knowledge/glossary/solana/">Solana</a>.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>Revenue enters the <a href="/knowledge/glossary/operating-series/">Operating Series</a> from the underlying asset or business</li>
                <li>The <code>sails_distributions</code> program reads the waterfall configuration from the offering's <a href="/knowledge/glossary/pda/">PDA</a> accounts</li>
                <li>Senior obligations are calculated and reserved from the available balance</li>
                <li>Investor distributions are computed pro-rata based on the real-time <a href="/knowledge/glossary/cap-table/">cap table</a></li>
                <li>Platform fee (1%) is deducted from remaining revenue</li>
                <li>Any excess flows to the <a href="/knowledge/glossary/treasury-series/">Treasury Series</a> for reserve accumulation</li>
                <li>All payments execute atomically — every step succeeds or none do</li>
            </ol>
            <p>Every waterfall execution creates an immutable DistributionRecord on-chain. The audit trail is permanent.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/distributions/" class="related-term-link">Distributions</a>
                <a href="/knowledge/glossary/operating-series/" class="related-term-link">Operating Series</a>
                <a href="/knowledge/glossary/treasury-series/" class="related-term-link">Treasury Series</a>
                <a href="/knowledge/glossary/paying-agent/" class="related-term-link">Paying Agent</a>
                <a href="/knowledge/glossary/smart-contract/" class="related-term-link">Smart Contract</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Investor-first. Always.</h3>
            <p>Revenue priority enforced by code, not promises. Your distributions flow first.</p>
            <a href="/signup/?type=investor" class="btn">Start Investing</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
