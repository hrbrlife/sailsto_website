---
title: "Cap'n Proto - Glossary"
description: "A zero-copy serialization protocol used for inter-grain RPC in the Sails.to platform, eliminating encoding/decoding overhead entirely."
ogImage: "/og-image.png"
keywords: ["capnproto", "cap'n proto", "glossary", "zero-copy", "serialization", "rpc", "grains", "sandstorm"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - "grain"
  - "melusina"
  - "powerbox"
  - "smart-contract"
---

<header class="term-page-header">
    <div class="container">
        <a href="/knowledge/glossary/" class="back-link">← Back to Glossary</a>
        <span class="term-category">Technology</span>
        <h1 class="term-title">Cap'n Proto</h1>
        <p class="term-short">A zero-copy serialization protocol used for inter-grain RPC in the Sails.to platform, eliminating encoding/decoding overhead entirely.</p>
    </div>
</header>
<main class="term-content">
    <div class="term-content-inner">
        <section class="term-section">
            <h2>Full Definition</h2>
            <p><strong>Cap'n Proto</strong> is a data serialization and RPC protocol designed for absolute speed. Unlike JSON, Protobuf, or any format that wastes cycles marshalling data between wire format and in-memory representation, Cap'n Proto uses the same layout for both. Zero copies. Zero parsing. The bytes on the wire <em>are</em> the data structure in memory. On the Sails.to platform, Cap'n Proto is the native protocol for all inter-<a href="/knowledge/glossary/grain/">grain</a> communication, operating on file descriptor 3 (FD3) for direct Sandstorm integration.</p>
        </section>
        <section class="term-section">
            <h2>Why It Matters</h2>
            <p>When a DAO Manager grain needs to coordinate with an Offering grain, or a Broker Portal queries KYC status, every microsecond of serialization overhead is wasted time. Cap'n Proto eliminates that overhead completely. The protocol was purpose-built for capability-based systems — it doesn't just move data, it moves <em>capabilities</em>. A Cap'n Proto RPC call can pass live references to objects across grain boundaries, which is exactly how the <a href="/knowledge/glossary/powerbox/">Powerbox</a> mechanism delegates authority.</p>
            <p>This is not a nice-to-have optimization. When you're running regulated financial infrastructure where compliance checks must execute on every transfer, serialization speed is a systemic constraint. Cap'n Proto removes it from the equation entirely.</p>
        </section>
        <section class="term-section">
            <h2>How It Works</h2>
            <ol>
                <li><a href="/knowledge/glossary/grain/">Grains</a> expose Cap'n Proto interfaces defined in .capnp schema files</li>
                <li>When Grain A calls Grain B, the request is written directly to FD3 — no HTTP, no REST, no encoding step</li>
                <li>Grain B reads the request as a native in-memory data structure — zero deserialization</li>
                <li>Capability references (sturdyRefs) can be embedded in messages, enabling the <a href="/knowledge/glossary/powerbox/">Powerbox</a> to pass live object references between grains</li>
                <li>Responses flow back on the same channel with the same zero-copy guarantee</li>
            </ol>
            <p>The result: inter-grain RPC with latency measured in microseconds, not milliseconds.</p>
        </section>
        <section class="term-section">
            <h2>Related Terms</h2>
            <div class="related-terms">
                <a href="/knowledge/glossary/grain/" class="related-term-link">Grain</a>
                <a href="/knowledge/glossary/powerbox/" class="related-term-link">Powerbox</a>
                <a href="/knowledge/glossary/melusina/" class="related-term-link">Melusina</a>
                <a href="/knowledge/glossary/smart-contract/" class="related-term-link">Smart Contract</a>
            </div>
        </section>
        <div class="term-cta">
            <h3>Speed without compromise</h3>
            <p>Zero-copy serialization powering institutional-grade financial infrastructure.</p>
            <a href="/signup/?type=issuer" class="btn">Learn More</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
