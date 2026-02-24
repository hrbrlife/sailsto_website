---
title: "NFT Hierarchy - Glossary"
description: "Sails.to's 4-layer authority structure on Solana: Master NFT → Reseller NFT → License NFT (pNFT) → Share NFT, ensuring cryptographic chain of trust."
ogImage: "/og-image.png"
keywords: ["nft hierarchy", "glossary", "authority", "structure", "solana", "master", "reseller", "license"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/glossary-term.css"

category: "technology"
tags:
  - "defi"
relatedTerms:
  - slug: "master-nft"
    label: "Master NFT"
  - slug: "solana"
    label: "Solana"
  - slug: "melusina"
    label: "Melusina"
  - slug: "threshold-signing"
    label: "Threshold Signing"
  - slug: "crosssecurities"
    label: "CrossSecurities"
ctaTitle: "Authority from root to leaf"
ctaText: "Every token, every permission, every action — cryptographically traceable to the source."
ctaLabel: "Learn More"
ctaLink: "/signup/?type=issuer"
linkLabel: "NFT Hierarchy"
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.4
  changefreq: "yearly"
---

<section class="term-section">
    <h2>Full Definition</h2>
    <p>The <strong>NFT Hierarchy</strong> is Sails.to's 4-layer authority delegation system deployed on <a href="/knowledge/glossary/solana/">Solana</a>. Each layer derives its authority from the one above, creating an unbroken cryptographic chain of trust from the platform root to individual user access:</p>
    <ul>
        <li><strong>Layer 1 — <a href="/knowledge/glossary/master-nft/">Master NFT</a>:</strong> The root authority. Controlled by 3-of-5 <a href="/knowledge/glossary/threshold-signing/">threshold signing</a>. Can mint Reseller NFTs and execute platform-level operations.</li>
        <li><strong>Layer 2 — Reseller NFT:</strong> Issued to institutional partners and <a href="/knowledge/glossary/broker-dealer/">broker-dealers</a>. Grants authority to onboard investors, create offerings, and earn commissions within a defined scope.</li>
        <li><strong>Layer 3 — License NFT (pNFT):</strong> Programmable NFT representing a specific offering license. Defines jurisdiction constraints, investor limits, and compliance parameters.</li>
        <li><strong>Layer 4 — Share NFT:</strong> The investor-facing token representing actual ownership in a <a href="/knowledge/glossary/crosssecurities/">CrossSecurity</a>. Transferable subject to <a href="/knowledge/glossary/compliance/">compliance</a> rules.</li>
    </ul>
</section>
<section class="term-section">
    <h2>Why It Matters</h2>
    <p>Traditional financial platforms manage authority through database roles and access control lists — systems that are fundamentally mutable, auditable only through logs, and vulnerable to insider compromise. The NFT Hierarchy replaces all of this with on-chain, verifiable, immutable authority delegation.</p>
    <p>Every action on the platform can be traced back through the hierarchy to the <a href="/knowledge/glossary/master-nft/">Master NFT</a>. A broker can prove their authority is legitimate. An investor can verify their Share NFT was issued through a valid chain. An auditor can reconstruct the entire authority tree from on-chain state alone. No database queries. No log files. Just <a href="/knowledge/glossary/solana/">Solana</a> accounts and the math that binds them.</p>
</section>
<section class="term-section">
    <h2>How It Works</h2>
    <ol>
        <li>The <a href="/knowledge/glossary/master-nft/">Master NFT</a> is minted at platform genesis with <a href="/knowledge/glossary/threshold-signing/">threshold signing</a> authority</li>
        <li>Master NFT holders mint Reseller NFTs to authorized institutional partners</li>
        <li>Reseller NFT holders create License NFTs (pNFTs) for specific offerings, encoding compliance parameters on-chain</li>
        <li>License NFTs authorize the minting of Share NFTs to verified investors who pass <a href="/knowledge/glossary/kyc/">KYC</a> checks</li>
        <li>Every layer validates its parent's authority before executing — a Share NFT cannot exist without a valid License, which cannot exist without a valid Reseller, which cannot exist without the Master</li>
    </ol>
    <p>The hierarchy is enforced by <a href="/knowledge/glossary/melusina/">Melusina</a> <a href="/knowledge/glossary/smart-contract/">smart contracts</a>. It cannot be bypassed.</p>
</section>
