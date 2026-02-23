---
title: "Sandstorm - Glossary"
description: "An open-source platform for self-hosting web applications, providing OS-level isolation for each application instance (grain) in the Sails.to runtime."
ogImage: "/og-image.png"
keywords: ["sandstorm", "glossary", "self-hosting", "isolation", "grain", "security", "sandbox", "melusina"]
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/glossary-term.css"

category: "technology"
tags:
  - "infrastructure"
relatedTerms:
  - slug: "grain"
    label: "Grain"
  - slug: "melusina"
    label: "Melusina"
  - slug: "bloom"
    label: "BLOOM"
  - slug: "powerbox"
    label: "Powerbox"
  - slug: "cap-n-proto"
    label: "Cap'n Proto"
ctaTitle: "Isolation as architecture"
ctaText: "Every grain sandboxed. Every boundary enforced. Every capability explicit."
ctaLabel: "Learn More"
ctaLink: "/signup/?type=issuer"
linkLabel: "Sandstorm"
---

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
