---
title: "Melusina - Glossary"
description: "The on-chain authority layer for Sails.to — a Solana-based system implementing NFT hierarchies, KYC credentialing, SPL-2022 compliance tokens."
ogImage: "/og-image.png"
keywords: ["melusina", "glossary", "on-chain", "authority", "solana", "nft", "compliance", "sails"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - slug: "solana"
    label: "Solana"
  - slug: "master-nft"
    label: "Master NFT"
  - slug: "nft-hierarchy"
    label: "NFT Hierarchy"
  - slug: "smart-contract"
    label: "Smart Contract"
  - slug: "transfer-hook"
    label: "Transfer Hook"
shortDesc: "The on-chain authority layer for Sails.to — a Solana-based system implementing NFT hierarchies, KYC credentialing, SPL-2022 compliance tokens, and threshold crypto."
ctaTitle: "Compliance is the architecture"
ctaText: "Not bolted on. Not optional. Built into every instruction, every account, every transaction."
ctaLabel: "Build on Melusina"
ctaLink: "/signup/?type=issuer"
linkLabel: "Melusina"
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.4
  changefreq: "yearly"
---

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
