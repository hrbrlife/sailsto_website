---
title: "CrossConversion - Glossary"
description: "The process of moving Sails CrossSecurities between on-chain (Solana) and bankable (ISIN/Clearstream) forms while maintaining 1:1 backing."
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
        <h1 class="term-title">CrossConversion</h1>
        <p class="term-short">The process of moving Sails CrossSecurities between on-chain and bankable forms while maintaining 1:1 backing.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p><strong>CrossConversion</strong> is Sails.to's mechanism for converting <a href="/knowledge/glossary/crosssecurities/">CrossSecurities</a> between their two forms:</p>
            <ul>
                <li><strong>Cross to Bankable:</strong> Lock on-chain tokens in the CrossConversion Series → receive 1:1 ISIN-bearing securities via Clearstream</li>
                <li><strong>Cross to On-Chain:</strong> Redeem ISIN securities → release locked tokens back to your Solana wallet</li>
            </ul>
            <p>The conversion is always 1:1 — ISIN-identified securities outstanding can never exceed tokens locked. Any eligible holder can request CrossConversion for approximately 1.5% of nominal value.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>CrossConversion is what makes <a href="/knowledge/glossary/crosssecurities/">CrossSecurities</a> truly hybrid. Without it, investors would be locked into whatever format they initially chose.</p>
            <p><strong>Use cases:</strong></p>
            <ul>
                <li>Traditional fund manager with mandate restrictions needs ISIN format → cross from on-chain to bankable</li>
                <li>Crypto-native investor wants self-custody → cross from bankable to on-chain</li>
                <li>Selling to a buyer whose bank only settles via Clearstream → cross format to complete the sale</li>
            </ul>
            <p>The underlying security never changes — same rights, same ownership, same issuer. Only the custody rails differ.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>Holder requests CrossConversion through the platform</li>
                <li><strong>Cross to Bankable:</strong> Tokens are locked in the issuer's CrossConversion Series</li>
                <li>ISIN-identified securities are issued via <a href="/knowledge/glossary/clearstream/">Clearstream</a></li>
                <li>Securities appear in holder's bank/brokerage account</li>
                <li><strong>Cross to On-Chain:</strong> Reverse process — redeem ISIN, release tokens</li>
            </ol>
            <p>Processing typically takes 3-5 business days. Fee: ~1.5% of nominal value (0.10-0.25% for the conversion itself, plus Clearstream fees).</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/crosssecurities/" class="related-term-link">CrossSecurities</a>
                <a href="/knowledge/glossary/isin/" class="related-term-link">ISIN</a>
                <a href="/knowledge/glossary/clearstream/" class="related-term-link">Clearstream</a>
                <a href="/knowledge/glossary/solana/" class="related-term-link">Solana</a>
                <a href="/knowledge/glossary/custody/" class="related-term-link">Custody</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Cross between worlds</h3>
            <p>On-chain today, bank custody tomorrow. Your security adapts to your needs.</p>
            <a href="/signup/?type=investor" class="btn">Start Investing</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
