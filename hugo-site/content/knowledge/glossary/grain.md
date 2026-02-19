---
title: "Grain - Glossary"
description: "The fundamental isolation unit in Sandstorm/Melusina OS — a sandboxed application instance with its own journal store, capabilities, and lifecycle."
ogImage: "/og-image.png"
keywords: ["grain", "glossary", "sandstorm", "isolation", "sandboxed", "application", "instance", "melusina"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - "cap-n-proto"
  - "melusina"
  - "powerbox"
  - "smart-contract"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Grain</h1>
        <p class="term-short">The fundamental isolation unit in Sandstorm/Melusina OS — a sandboxed application instance with its own journal store, capabilities, and lifecycle.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p>A <strong>Grain</strong> is the atomic unit of computation and isolation in the Sandstorm/Melusina OS architecture. Every grain runs in its own sandbox with its own persistent storage, its own capability set, and its own lifecycle — it can be started, stopped, snapshotted, and migrated independently. There is no ambient authority. A grain can only access what it has been explicitly granted through the <a href="/knowledge/glossary/powerbox/">Powerbox</a>. Sails.to deploys two classes of grains:</p>
            <ul>
                <li><strong>Station Grains (Orchestrators):</strong> DAO Manager, Broker Portal, Trustee Dashboard — these coordinate workflows and hold authority delegations</li>
                <li><strong>Instance Grains (Workers):</strong> Offering, KYC, Investor — these execute specific tasks within a single bounded context</li>
            </ul>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>In traditional platforms, a vulnerability in one module can cascade across the entire system. A compromised user service exposes the payment service. A bug in compliance leaks investor data. The grain model makes this architecturally impossible. Each grain is a fortress — its own filesystem, its own network namespace, its own capability boundary.</p>
            <p>For regulated financial infrastructure, this isn't just good engineering — it's a compliance requirement materialized in architecture. When an auditor asks "can the Broker Portal access KYC data it hasn't been granted?", the answer is a provable, cryptographic <strong>no</strong>. The <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a> capability system enforces it at the protocol level.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>A grain is spawned from a package (SPK) containing its application code and dependencies</li>
                <li>The Sandstorm supervisor creates an isolated container with a private filesystem and journal store</li>
                <li>The grain communicates with other grains exclusively via <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a> RPC on FD3</li>
                <li>Capabilities are acquired through the <a href="/knowledge/glossary/powerbox/">Powerbox</a> — claim tokens become persistent sturdyRefs</li>
                <li>When idle, grains are automatically suspended; when needed, they resume from their journal state</li>
            </ol>
            <p>The result: thousands of grains running simultaneously, each provably isolated, each resumable, each auditable.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/powerbox/" class="related-term-link">Powerbox</a>
                <a href="/knowledge/glossary/cap-n-proto/" class="related-term-link">Cap'n Proto</a>
                <a href="/knowledge/glossary/melusina/" class="related-term-link">Melusina</a>
                <a href="/knowledge/glossary/smart-contract/" class="related-term-link">Smart Contract</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Isolation by design</h3>
            <p>Every component sandboxed. Every capability explicit. Every action auditable.</p>
            <a href="/signup/?type=issuer" class="btn">Learn More</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
