---
title: "Melusina - Glossary"
description: "The on-chain authority layer for Sails.to — a Solana-based system implementing NFT hierarchies, KYC credentialing, SPL-2022 compliance tokens, and threshold crypto."
ogImage: "/og-image.png"
keywords: ["melusina", "glossary", "on-chain", "authority", "solana", "nft", "compliance", "sails"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Melusina</h1>
        <p class="term-short">The on-chain authority layer for Sails.to — a Solana-based system implementing NFT hierarchies, KYC credentialing, SPL-2022 compliance tokens, and threshold crypto.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p><strong>Melusina</strong> is the foundation upon which all Sails.to <a href="/knowledge/glossary/smart-contract/">smart contracts</a> are built. It is not a single contract but an interconnected system of <a href="/knowledge/glossary/solana/">Solana</a> programs that collectively implement the platform's on-chain authority model. Melusina encompasses the entire <a href="/knowledge/glossary/nft-hierarchy/">NFT Hierarchy</a> (Master → Reseller → License → Share), the <a href="/knowledge/glossary/kyc/">KYC</a> credentialing system that issues soulbound verification NFTs, SPL-2022 token extensions for <a href="/knowledge/glossary/compliance/">compliance</a>-enforced transfers, and the <a href="/knowledge/glossary/threshold-signing/">threshold signing</a> infrastructure that protects critical operations.</p>
            <p>Every on-chain action in Sails.to — every token transfer, every distribution, every CrossConversion — ultimately passes through Melusina's authority checks.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>Most tokenization platforms bolt compliance onto their blockchain layer as an afterthought — a modifier here, a whitelist there. Melusina is compliance from the ground up. The authority model, the credentialing system, and the transfer restrictions are not features added to a token contract. They are the architecture itself.</p>
            <p>This means that compliance is not optional, not configurable-away, not bypassable by a privileged admin. When Melusina's <a href="/knowledge/glossary/transfer-hook/">transfer hook</a> checks a transfer, it verifies <a href="/knowledge/glossary/kyc/">KYC</a> status, jurisdiction whitelist, lock-up period, and accreditation tier — all in a single atomic transaction. Either every check passes, or the transfer does not happen. There is no middle ground.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>The <a href="/knowledge/glossary/master-nft/">Master NFT</a> program establishes the root of the authority tree via <a href="/knowledge/glossary/threshold-signing/">threshold signing</a></li>
                <li>The NFT Hierarchy programs manage delegation from Master → Reseller → License → Share</li>
                <li>The KYC Credentialing program issues soulbound verification NFTs to compliant wallets</li>
                <li>SPL-2022 token mints are created with <a href="/knowledge/glossary/transfer-hook/">transfer hooks</a> that enforce compliance at the protocol level</li>
                <li>The Distribution program calculates and executes pro-rata payments to all token holders</li>
                <li><a href="/knowledge/glossary/pda/">PDA</a>-derived accounts store all state deterministically — OfferingState, InvestorPosition, ComplianceConfig</li>
            </ol>
            <p>Melusina is deployed, audited, and immutable. The rules are the rules.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/solana/" class="related-term-link">Solana</a>
                <a href="/knowledge/glossary/master-nft/" class="related-term-link">Master NFT</a>
                <a href="/knowledge/glossary/nft-hierarchy/" class="related-term-link">NFT Hierarchy</a>
                <a href="/knowledge/glossary/smart-contract/" class="related-term-link">Smart Contract</a>
                <a href="/knowledge/glossary/transfer-hook/" class="related-term-link">Transfer Hook</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Compliance is the architecture</h3>
            <p>Not bolted on. Not optional. Built into every instruction, every account, every transaction.</p>
            <a href="/signup/?type=issuer" class="btn">Build on Melusina</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
