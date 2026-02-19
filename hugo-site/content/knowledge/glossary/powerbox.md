---
title: "Powerbox - Glossary"
description: "The inter-grain capability sharing mechanism in Sandstorm/Melusina OS, enabling secure permission delegation via claim tokens and persistent sturdyRefs."
ogImage: "/og-image.png"
keywords: ["powerbox", "glossary", "capability", "sharing", "grains", "sandstorm", "sturdyref", "delegation"]
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
  - "grain"
  - "melusina"
  - "trustee"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Powerbox</h1>
        <p class="term-short">The inter-grain capability sharing mechanism in Sandstorm/Melusina OS, enabling secure permission delegation via claim tokens and persistent sturdyRefs.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p>The <strong>Powerbox</strong> is the capability brokering system at the heart of Sandstorm/Melusina OS. It is the <em>only</em> mechanism through which <a href="/knowledge/glossary/grain/">grains</a> can share access to each other's resources. When a grain needs a capability it doesn't have — access to an Offering, a KYC result, a distribution channel — it requests it through the Powerbox. The request produces a claim token. When the granting grain accepts, the claim token becomes a persistent sturdyRef: a durable, revocable, fine-grained capability reference serialized via <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a>.</p>
            <p>There is no ambient authority. No global permissions. No role-based access control. If a grain doesn't hold a sturdyRef to a resource, that resource does not exist in its universe.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>The Powerbox is what makes Sails.to's security model fundamentally different from every other platform in the industry. In a traditional system, a Broker Portal might have "read access to KYC data" via a database role. That role grants access to <em>all</em> KYC data, for <em>all</em> investors, forever, unless explicitly revoked. One compromised credential and the entire KYC database is exposed.</p>
            <p>With the Powerbox, a Broker Portal <a href="/knowledge/glossary/grain/">grain</a> receives a sturdyRef to exactly one KYC result for exactly one investor. It cannot enumerate other results. It cannot escalate its access. It cannot even discover what other capabilities exist. The DAO Manager grain grants Offering access to Brokers through the Powerbox. KYC results flow to <a href="/knowledge/glossary/trustee/">Trustees</a> through the Powerbox. Every capability is explicit, auditable, and revocable.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li>Grain A (e.g., Broker Portal) requests a capability from the Powerbox — "I need access to Offering X"</li>
                <li>The Powerbox identifies Grain B (e.g., DAO Manager) as the authority for that capability</li>
                <li>Grain B evaluates the request and, if authorized, generates a claim token</li>
                <li>The claim token is delivered to Grain A and resolved into a persistent sturdyRef via <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a></li>
                <li>Grain A can now invoke methods on the capability — but only the methods the sturdyRef exposes</li>
                <li>The granting grain can revoke the sturdyRef at any time, instantly terminating access</li>
            </ol>
            <p>Capability delegation is transitive but attenuating — a grain can share a subset of its own capabilities, never more than it holds.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/grain/" class="related-term-link">Grain</a>
                <a href="/knowledge/glossary/cap-n-proto/" class="related-term-link">Cap'n Proto</a>
                <a href="/knowledge/glossary/melusina/" class="related-term-link">Melusina</a>
                <a href="/knowledge/glossary/trustee/" class="related-term-link">Trustee</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Capabilities, not permissions</h3>
            <p>Every access explicit. Every delegation auditable. Every grant revocable.</p>
            <a href="/signup/?type=issuer" class="btn">Learn More</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
