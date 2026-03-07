---
title: "PDA (Program Derived Address) - Glossary"
description: "A deterministic Solana account address derived from program seeds, used in Sails.to for trustless, programmatic state management."
ogImage: "/og-image.png"
keywords: ["pda", "program derived address", "glossary", "solana", "deterministic", "account", "seeds", "trustless"]
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
  - slug: "smart-contract"
    label: "Smart Contract"
  - slug: "melusina"
    label: "Melusina"
  - slug: "crossconversion"
    label: "CrossConversion"
ctaTitle: "State you can verify"
ctaText: "Deterministic addresses. Program-controlled data. Zero trust required."
ctaLabel: "Learn More"
ctaLink: "/signup/?type=issuer"
linkLabel: "PDA"
date: "2026-02-24"
lastmod: "2026-02-24"
sitemap:
  priority: 0.4
  changefreq: "yearly"
---

<section class="term-section">
    <h2>Full Definition</h2>
    <p>A <strong>Program Derived Address (PDA)</strong> is a <a href="/knowledge/glossary/solana/">Solana</a> account address that is deterministically derived from a combination of seed values and a program ID. Unlike regular Solana accounts, PDAs have no private key - they are controlled exclusively by the program that derived them. This makes them the perfect primitive for trustless state management: no human, no wallet, no external entity can modify a PDA's data except through the program's own logic.</p>
    <p>Sails.to uses PDAs extensively across the <a href="/knowledge/glossary/melusina/">Melusina</a> system for critical state accounts:</p>
    <ul>
        <li><strong>OfferingState:</strong> Derived from <code>[offering_id, "state"]</code> - holds all parameters for an active offering</li>
        <li><strong>InvestorPosition:</strong> Derived from <code>[offering_id, investor_wallet, "position"]</code> - tracks individual holdings</li>
        <li><strong>CrossConversionLockbox:</strong> Derived from <code>[offering_id, "lockbox"]</code> - holds tokens locked during <a href="/knowledge/glossary/crossconversion/">CrossConversion</a></li>
        <li><strong>DistributionRecord:</strong> Derived from <code>[offering_id, epoch, "distribution"]</code> - immutable record of each distribution</li>
        <li><strong>ComplianceConfig:</strong> Derived from <code>[offering_id, "compliance"]</code> - jurisdiction whitelists, lock-up periods, accreditation requirements</li>
    </ul>
</section>
<section class="term-section">
    <h2>Why It Matters</h2>
    <p>PDAs are the reason Sails.to's on-chain state is trustless. When a <a href="/knowledge/glossary/smart-contract/">smart contract</a> stores an investor's position in a PDA, that data can only be modified by the program's own verified logic. No admin key. No multisig override. No database migration. The program is the sole authority, and the program's logic is auditable, deployed, and immutable.</p>
    <p>Because PDAs are deterministic, any party can independently derive the address and verify the data. An auditor doesn't need API access or database credentials - they need a Solana RPC endpoint and the seed schema. The state is public, verifiable, and incorruptible.</p>
</section>
<section class="term-section">
    <h2>How It Works</h2>
    <ol>
        <li>The program defines a seed schema - a combination of identifiers that uniquely describe the account's purpose</li>
        <li><a href="/knowledge/glossary/solana/">Solana</a> computes <code>hash(seeds, program_id)</code> and finds an address that falls off the Ed25519 curve (no valid private key exists)</li>
        <li>The program creates and initializes the account at this address, writing structured data via Borsh serialization</li>
        <li>Only the originating program can sign transactions modifying this account - enforced at the Solana runtime level</li>
        <li>Anyone can derive the same address from the same seeds and read the account's data trustlessly</li>
    </ol>
    <p>The result: every piece of Sails.to platform state is stored at a predictable, verifiable, program-controlled address.</p>
</section>
