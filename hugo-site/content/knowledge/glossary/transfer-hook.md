---
title: "Transfer Hook - Glossary"
description: "A Solana SPL-2022 extension that intercepts token transfers and enforces compliance rules before allowing any transfer to proceed."
ogImage: "/og-image.png"
keywords: ["transfer hook", "glossary", "solana", "spl-2022", "compliance", "token", "transfer", "kyc"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "defi"
relatedTerms:
  - "accredited-investor"
  - "compliance"
  - "crosssecurities"
  - "kyc"
  - "melusina"
  - "pda"
  - "solana"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Transfer Hook</h1>
        <p class="term-short">A Solana SPL-2022 extension that intercepts token transfers and enforces compliance rules before allowing any transfer to proceed.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p>A <strong>Transfer Hook</strong> is a <a href="/knowledge/glossary/solana/">Solana</a> SPL-2022 token extension that injects custom program logic into every token transfer. When a transfer instruction is executed, the Solana runtime automatically invokes the hook program <em>before</em> the transfer completes. If the hook rejects the transfer, the entire transaction fails atomically. There is no way to bypass it — the hook is embedded in the token mint itself.</p>
            <p>In Sails.to, the transfer hook is the enforcement arm of the <a href="/knowledge/glossary/compliance/">compliance</a> system. Every transfer of a <a href="/knowledge/glossary/crosssecurities/">CrossSecurity</a> token passes through the hook, which performs a battery of checks before allowing the transfer to proceed.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>Security tokens without enforceable transfer restrictions are just tokens with a label. Anyone can claim their token is "compliant" — but if a non-<a href="/knowledge/glossary/kyc/">KYC</a>'d wallet can receive it, if a sanctioned jurisdiction can hold it, if a lock-up period can be circumvented by a simple peer-to-peer transfer, then compliance is a fiction.</p>
            <p>The transfer hook makes compliance a fact. It is not a middleware that can be routed around. It is not an API that can be skipped. It is baked into the <a href="/knowledge/glossary/solana/">Solana</a> runtime's transfer logic. Every transfer — whether initiated from a dApp, a CLI, a DEX, or a direct RPC call — must pass through the hook. The rules are inescapable.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <p>When a transfer is initiated, the Sails.to transfer hook executes the following checks in sequence:</p>
            <ol>
                <li><strong><a href="/knowledge/glossary/kyc/">KYC</a> Verification:</strong> Both the sender and receiver wallets must hold valid KYC verification NFTs issued by the credentialing system</li>
                <li><strong>Jurisdiction Whitelist:</strong> Both wallets must be associated with jurisdictions permitted by the offering's <a href="/knowledge/glossary/compliance/">compliance</a> configuration</li>
                <li><strong>Lock-Up Period:</strong> The sender's tokens must have cleared any time-based lock-up restrictions defined in the offering terms</li>
                <li><strong>Accreditation Tier:</strong> The receiver must meet the minimum <a href="/knowledge/glossary/accredited-investor/">accreditation</a> requirements for the specific security class</li>
                <li>If all checks pass, the transfer proceeds atomically. If any check fails, the entire transaction reverts</li>
            </ol>
            <p>All compliance parameters are stored in <a href="/knowledge/glossary/pda/">PDA</a>-derived ComplianceConfig accounts, readable and verifiable by anyone.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/kyc/" class="related-term-link">KYC</a>
                <a href="/knowledge/glossary/compliance/" class="related-term-link">Compliance</a>
                <a href="/knowledge/glossary/solana/" class="related-term-link">Solana</a>
                <a href="/knowledge/glossary/melusina/" class="related-term-link">Melusina</a>
                <a href="/knowledge/glossary/pda/" class="related-term-link">PDA</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Compliance you cannot bypass</h3>
            <p>Every transfer checked. Every rule enforced. Every violation blocked at the protocol level.</p>
            <a href="/signup/?type=issuer" class="btn">Learn More</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
