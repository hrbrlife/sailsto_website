---
title: "Master NFT - Glossary"
description: "The root authority token in Sails.to's 4-layer NFT hierarchy on Solana, controlled by 3-of-5 keyholder threshold signing."
ogImage: "/og-image.png"
keywords: ["master nft", "glossary", "root", "authority", "token", "solana", "threshold", "keyholder"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/glossary-term.css"

category: "technology"
tags:
  - "defi"
relatedTerms:
  - slug: "nft-hierarchy"
    label: "NFT Hierarchy"
  - slug: "threshold-signing"
    label: "Threshold Signing"
  - slug: "solana"
    label: "Solana"
  - slug: "melusina"
    label: "Melusina"
  - slug: "smart-contract"
    label: "Smart Contract"
ctaTitle: "Authority you can verify"
ctaText: "Cryptographic root of trust. No single point of failure. No single point of compromise."
ctaLabel: "Learn More"
ctaLink: "/signup/?type=issuer"
linkLabel: "Master NFT"
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.4
  changefreq: "yearly"
---

<section class="term-section">
    <h2>Full Definition</h2>
    <p>The <strong>Master NFT</strong> is the supreme authority token in the Sails.to platform — the root of the cryptographic trust chain from which all other authority flows. It sits at Layer 1 of the <a href="/knowledge/glossary/nft-hierarchy/">NFT Hierarchy</a>: Master NFT → Reseller NFT → License NFT (pNFT) → Share NFT. Every operation that creates, modifies, or revokes lower-tier authority must trace back to the Master NFT.</p>
    <p>Control is distributed across 5 keyholders via <a href="/knowledge/glossary/threshold-signing/">threshold signing</a>, requiring 3-of-5 approval for any action. No single keyholder — no single human — can unilaterally exercise Master NFT authority. This is not a policy. It is a mathematical guarantee enforced by the <a href="/knowledge/glossary/solana/">Solana</a> runtime.</p>
</section>
<section class="term-section">
    <h2>Why It Matters</h2>
    <p>The Master NFT is what prevents a rogue actor from seizing control of the platform. Traditional platforms rely on access control lists, database permissions, HR policies — all of which can be circumvented by someone with sufficient access. The Master NFT replaces all of that with cryptographic certainty.</p>
    <p>It can mint new Reseller NFTs to onboard institutional partners, authorize emergency actions like freezing compromised accounts, and execute platform-wide configuration changes. But it can do none of these things without 3 of 5 keyholders independently signing the transaction. The security model is absolute.</p>
</section>
<section class="term-section">
    <h2>How It Works</h2>
    <ol>
        <li>The Master NFT is minted once during platform genesis on <a href="/knowledge/glossary/solana/">Solana</a></li>
        <li>Authority is bound to 5 keyholder wallets via <a href="/knowledge/glossary/threshold-signing/">threshold signing</a> configuration</li>
        <li>Any privileged action (minting Reseller NFTs, emergency freezes, configuration changes) requires a multi-sig transaction</li>
        <li>3 of 5 keyholders must independently sign the transaction within a time window</li>
        <li>The <a href="/knowledge/glossary/solana/">Solana</a> program validates the threshold before executing</li>
    </ol>
    <p>The Master NFT is non-transferable and non-burnable. It is the permanent, immutable root of the Sails.to authority tree.</p>
</section>
