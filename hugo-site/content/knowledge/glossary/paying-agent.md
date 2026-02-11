---
title: "Paying Agent - Glossary"
description: "The entity authorized to execute distributions and manage the revenue waterfall for a Sails.to offering, operating under Trustee oversight."
ogImage: "/og-image.png"
keywords: ["paying agent", "glossary", "distributions", "revenue", "waterfall", "trustee", "oversight", "offering"]
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
        <h1 class="term-title">Paying Agent</h1>
        <p class="term-short">The entity authorized to execute distributions and manage the revenue waterfall for a Sails.to offering, operating under Trustee oversight.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p>The <strong>Paying Agent</strong> is the designated entity responsible for executing all financial <a href="/knowledge/glossary/distributions/">distributions</a> within a Sails.to offering structure. Operating under the authority and oversight of the <a href="/knowledge/glossary/trustee/">Trustee</a>, the Paying Agent manages the revenue <a href="/knowledge/glossary/waterfall/">waterfall</a> — ensuring that every dollar flows to the right recipient in the right order. The Paying Agent does not decide <em>whether</em> to distribute; it executes <em>how</em> distributions occur according to the offering's predefined priority structure.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>Investors need absolute certainty that their distributions arrive correctly, on time, and in the right priority order. The Paying Agent is the mechanism that delivers this certainty. When revenue enters the <a href="/knowledge/glossary/operating-series/">Operating Series</a>, the Paying Agent ensures investors are paid before the platform takes its fee, and the platform takes its fee before excess flows to the <a href="/knowledge/glossary/treasury-series/">Treasury Series</a>.</p>
            <p>On Sails.to, this process is enforced on-chain via <a href="/knowledge/glossary/smart-contract/">smart contracts</a>. The Paying Agent's authority is bounded — it can execute distributions according to the waterfall, but it cannot alter the waterfall itself. That requires <a href="/knowledge/glossary/trustee/">Trustee</a> authorization. Separation of duties is not a policy document. It is code.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>Revenue is deposited into the <a href="/knowledge/glossary/operating-series/">Operating Series</a> account</li>
                <li>The Paying Agent initiates the distribution process under <a href="/knowledge/glossary/trustee/">Trustee</a> oversight</li>
                <li>The <a href="/knowledge/glossary/waterfall/">waterfall</a> executes in strict priority: senior obligations → investor pro-rata distributions → platform fee (1%) → Treasury Series</li>
                <li>On-chain distribution records are created for every payment via <a href="/knowledge/glossary/smart-contract/">smart contracts</a></li>
                <li>Investors holding on-chain tokens receive distributions to their wallets; <a href="/knowledge/glossary/isin/">ISIN</a> holders receive via traditional banking rails</li>
            </ol>
            <p>Every distribution is auditable on-chain. Every cent accounted for. Every priority enforced.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/trustee/" class="related-term-link">Trustee</a>
                <a href="/knowledge/glossary/distributions/" class="related-term-link">Distributions</a>
                <a href="/knowledge/glossary/waterfall/" class="related-term-link">Waterfall</a>
                <a href="/knowledge/glossary/operating-series/" class="related-term-link">Operating Series</a>
                <a href="/knowledge/glossary/treasury-series/" class="related-term-link">Treasury Series</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Distributions you can trust</h3>
            <p>Investor-first priority. On-chain enforcement. Every payment verifiable.</p>
            <a href="/signup/?type=investor" class="btn">Start Investing</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
