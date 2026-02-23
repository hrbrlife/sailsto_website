---
title: "BLOOM_FINAL / The Application Engine - Glossary"
description: "The application engine layer of Sails.to, built on Sandstorm/Melusina OS, providing the grain runtime for all platform applications."
ogImage: "/og-image.png"
keywords: ["bloom", "application engine", "glossary", "sandstorm", "melusina", "grain", "runtime", "cap'n proto"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - slug: "grain"
    label: "Grain"
  - slug: "sandstorm"
    label: "Sandstorm"
  - slug: "cap-n-proto"
    label: "Cap'n Proto"
  - slug: "powerbox"
    label: "Powerbox"
  - slug: "melusina"
    label: "Melusina"
ctaTitle: "One engine, every surface"
ctaText: "Capability-secured grains powering every interaction on the platform."
ctaLabel: "Learn More"
ctaLink: "/signup/?type=issuer"
linkLabel: "BLOOM"
---

<section class="term-section">
    <h2>Full Definition</h2>
    <p><strong>BLOOM_FINAL</strong> is the application engine layer of Sails.to, built on <a href="/knowledge/glossary/sandstorm/">Sandstorm</a>/<a href="/knowledge/glossary/melusina/">Melusina</a> OS. It provides the <a href="/knowledge/glossary/grain/">grain</a> runtime — <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a> RPC, Go+HTMX native stack, KYC workflow orchestration, and <a href="/knowledge/glossary/powerbox/">powerbox</a>-based capability sharing. BLOOM is the canonical pattern for all Sails.to applications.</p>
    <p>Every user-facing interaction on the platform — dashboards, investor onboarding, compliance workflows, distribution management — runs as a grain inside the BLOOM runtime. The architecture enforces capability-based security at every layer, ensuring that each application instance operates within its explicitly granted authority.</p>
</section>
<section class="term-section">
    <h2>Why It Matters</h2>
    <p>BLOOM is where the user experience lives. Every dashboard, every form, every real-time update runs as a <a href="/knowledge/glossary/grain/">grain</a> in the BLOOM runtime. The Go+HTMX stack delivers server-rendered HTML with minimal client-side complexity, while <a href="/knowledge/glossary/cap-n-proto/">Cap'n Proto</a> RPC handles inter-grain communication with zero-copy efficiency.</p>
    <p>By standardizing on a single application engine, Sails.to achieves consistency across all platform surfaces. New features deploy as new grains — isolated, auditable, and governed by the same capability model that protects every other component.</p>
</section>
