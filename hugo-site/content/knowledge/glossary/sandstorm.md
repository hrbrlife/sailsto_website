---
title: "Sandstorm - Glossary"
description: "An open-source platform for self-hosting web applications, providing OS-level isolation for each application instance (grain) in the Sails.to runtime."
ogImage: "/og-image.png"
keywords: ["sandstorm", "glossary", "self-hosting", "isolation", "grain", "security", "sandbox", "melusina"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - "bloom"
  - "cap-n-proto"
  - "grain"
  - "melusina"
  - "powerbox"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Sandstorm</h1>
        <p class="term-short">An open-source platform for self-hosting web applications, providing OS-level isolation for each application instance (grain) in the Sails.to runtime.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p><strong>Sandstorm</strong> is an open-source platform for self-hosting web applications, providing OS-level isolation for each application instance (<a href="/knowledge/glossary/grain/">grain</a>). Sails.to extends Sandstorm through <a href="/knowledge/glossary/melusina/">Melusina</a> OS to create the runtime environment where all platform grains execute. Each grain runs in its own security sandbox with its own storage, capabilities, and lifecycle.</p>
            <p>Unlike container orchestration platforms that share kernels and require complex networking policies, Sandstorm enforces isolation at the supervisor level. Each grain gets a private filesystem, a restricted network namespace, and communicates exclusively through <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a> RPC. The <a href="/knowledge/glossary/powerbox/">Powerbox</a> mediates all capability grants between grains, ensuring no ambient authority exists in the system.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>Sandstorm gives Sails.to true application isolation without containers or VMs. Each <a href="/knowledge/glossary/grain/">grain</a> is a security boundary — compromise one, and the rest remain unaffected. This is not a policy enforced by configuration; it is a structural property of the runtime.</p>
            <p>For regulated financial infrastructure, this isolation model is critical. Every investor's data, every offering's state, every compliance workflow runs in its own sandbox. Auditors can verify that access boundaries are enforced by architecture, not by access control lists that can be misconfigured or overridden.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/grain/" class="related-term-link">Grain</a>
                <a href="/knowledge/glossary/melusina/" class="related-term-link">Melusina</a>
                <a href="/knowledge/glossary/bloom/" class="related-term-link">BLOOM</a>
                <a href="/knowledge/glossary/powerbox/" class="related-term-link">Powerbox</a>
                <a href="/knowledge/glossary/cap-n-proto/" class="related-term-link">Cap'n Proto</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Isolation as architecture</h3>
            <p>Every grain sandboxed. Every boundary enforced. Every capability explicit.</p>
            <a href="/signup/?type=issuer" class="btn">Learn More</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
