---
title: "Knowledge Base"
description: "Learn everything about Sails CrossSecurities, compliance, blockchain infrastructure, and traditional finance integration."
keywords:
  - CrossSecurities guide
  - tokenization education
  - blockchain securities
  - compliance guide
  - CrossConversion
  - knowledge base
ogImage: "/og-knowledge.png"
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/knowledge-index.css"
scripts:
  - "/js/kb-filters.js"
  - "/js/knowledge-index.js"
---


<section class="page-hero">
    <span class="section-label">Learn</span>
    <h1 class="section-title">Knowledge Base</h1>
    <p class="section-desc">Everything you need to understand Sails CrossSecurities infrastructure — from blockchain basics to regulatory compliance.</p>
    <div class="kb-search">
        <input type="text" id="kb-search-input" placeholder="Search articles, guides, and terms..." class="kb-search-input">
        <svg class="kb-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
        </svg>
    </div>
</section>
<section class="kb-tabs-section">
    <div class="kb-container">
        {{< kb-tabs >}}
    </div>
</section>
<section class="kb-featured">
    <div class="kb-container">
        <h2 class="kb-section-title">Featured Resources</h2>
        <div class="kb-featured-grid">
            <a href="/knowledge/docs/getting-started/" class="kb-card kb-card-featured" data-category="docs">
                <div class="kb-card-icon"><svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></div>
                <div class="kb-card-content">
                    <span class="kb-card-category">Getting Started</span>
                    <h3>Quick Start Guide</h3>
                    <p>New to Sails.to? This guide walks you through the platform, from account setup to your first transaction.</p>
                </div>
                <span class="kb-card-arrow">→</span>
            </a>
            <a href="/knowledge/docs/hybrid-architecture/" class="kb-card kb-card-featured" data-category="docs">
                <div class="kb-card-icon"><svg viewBox="0 0 24 24"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg></div>
                <div class="kb-card-content">
                    <span class="kb-card-category">Architecture</span>
                    <h3>Understanding CrossConversion</h3>
                    <p>Deep dive into how CrossSecurities flow between Solana and bankable custody via ISIN conversion.</p>
                </div>
                <span class="kb-card-arrow">→</span>
            </a>
            <a href="/knowledge/faq/" class="kb-card kb-card-featured" data-category="faq">
                <div class="kb-card-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg></div>
                <div class="kb-card-content">
                    <span class="kb-card-category">Support</span>
                    <h3>Frequently Asked Questions</h3>
                    <p>Answers to the most common questions about CrossSecurities, compliance, and using the platform.</p>
                </div>
                <span class="kb-card-arrow">→</span>
            </a>
        </div>
    </div>
</section>
<section class="kb-resources">
    <div class="kb-container">
        <div class="kb-resource-section" data-category="guides">
            <div class="kb-section-header">
                <h2><svg class="section-icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Guides</h2>
                <p>Step-by-step tutorials and conceptual explanations</p>
            </div>
            <div class="kb-grid">
                <a href="/knowledge/guides/tokenization-101/" class="kb-card">
                    <span class="kb-card-category">Beginner</span>
                    <h3>Tokenization 101</h3>
                    <p>What are security tokens? How do they differ from utility tokens? A complete introduction.</p>
                    <span class="kb-card-meta">10 min read</span>
                </a>
                <a href="/knowledge/guides/wyoming-dao-explained/" class="kb-card">
                    <span class="kb-card-category">Legal</span>
                    <h3>Wyoming DAO LLC Explained</h3>
                    <p>Understanding the legal structure that makes compliant blockchain-based securities possible.</p>
                    <span class="kb-card-meta">8 min read</span>
                </a>
                <a href="/knowledge/guides/investor-eligibility/" class="kb-card">
                    <span class="kb-card-category">Compliance</span>
                    <h3>Investor Eligibility Requirements</h3>
                    <p>Accredited vs. professional investors, KYC/AML requirements, and geographic considerations.</p>
                    <span class="kb-card-meta">6 min read</span>
                </a>
                <a href="/knowledge/guides/isin-conversion/" class="kb-card">
                    <span class="kb-card-category">Technical</span>
                    <h3>CrossConversion: Token to ISIN</h3>
                    <p>How CrossConversion converts on-chain CrossSecurities to bankable securities identifiers.</p>
                    <span class="kb-card-meta">12 min read</span>
                </a>
            </div>
        </div>
        <div class="kb-resource-section" data-category="docs">
            <div class="kb-section-header">
                <h2>📖 Documentation</h2>
                <p>Technical references and platform specifications</p>
            </div>
            <div class="kb-grid">
                <a href="/knowledge/docs/platform-overview/" class="kb-card">
                    <span class="kb-card-category">Overview</span>
                    <h3>Platform Architecture</h3>
                    <p>High-level overview of system components, data flows, and integration points.</p>
                    <span class="kb-card-meta">Technical</span>
                </a>
                <a href="/knowledge/docs/token-standard/" class="kb-card">
                    <span class="kb-card-category">Development</span>
                    <h3>Token Standard</h3>
                    <p>SPL token implementation details, metadata structure, and compliance extensions.</p>
                    <span class="kb-card-meta">Technical</span>
                </a>
                <a href="/knowledge/docs/api-reference/" class="kb-card">
                    <span class="kb-card-category">API</span>
                    <h3>API Reference</h3>
                    <p>REST API endpoints for integration, authentication, and data retrieval.</p>
                    <span class="kb-card-meta">Technical</span>
                </a>
                <a href="/knowledge/docs/compliance-framework/" class="kb-card">
                    <span class="kb-card-category">Compliance</span>
                    <h3>Compliance Framework</h3>
                    <p>On-chain compliance rules, transfer restrictions, and regulatory hooks.</p>
                    <span class="kb-card-meta">Technical</span>
                </a>
            </div>
        </div>
        <div class="kb-resource-section" data-category="faq">
            <div class="kb-section-header">
                <h2><svg class="section-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg> FAQ</h2>
                <p>Quick answers to common questions</p>
            </div>
            <div class="kb-grid">
                <a href="/knowledge/faq/#general" class="kb-card">
                    <span class="kb-card-category">General</span>
                    <h3>General Questions</h3>
                    <p>What is Sails.to? How does it work? Is it safe?</p>
                    <span class="kb-card-meta">12 questions</span>
                </a>
                <a href="/knowledge/faq/#issuers" class="kb-card">
                    <span class="kb-card-category">For Issuers</span>
                    <h3>Issuer FAQ</h3>
                    <p>How to launch a token, costs, timeline, and legal requirements.</p>
                    <span class="kb-card-meta">8 questions</span>
                </a>
                <a href="/knowledge/faq/#investors" class="kb-card">
                    <span class="kb-card-category">For Investors</span>
                    <h3>Investor FAQ</h3>
                    <p>How to invest, custody options, tax implications, and returns.</p>
                    <span class="kb-card-meta">10 questions</span>
                </a>
                <a href="/knowledge/faq/#technical" class="kb-card">
                    <span class="kb-card-category">Technical</span>
                    <h3>Technical FAQ</h3>
                    <p>Blockchain details, wallet setup, and troubleshooting.</p>
                    <span class="kb-card-meta">6 questions</span>
                </a>
            </div>
        </div>
        <div class="kb-resource-section" data-category="glossary">
            <div class="kb-section-header">
                <h2><svg class="section-icon" viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> Glossary</h2>
                <p>Definitions of key terms and concepts</p>
                <a href="/knowledge/glossary/" class="kb-section-link">View Full Glossary →</a>
            </div>
            <div class="kb-glossary-preview">
                {{< glossary-preview >}}
            </div>
        </div>
        <div class="kb-resource-section" data-category="roadmap">
            <div class="kb-section-header">
                <h2><svg class="section-icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> Roadmap</h2>
                <p>Track our development progress and upcoming features</p>
                <a href="/knowledge/roadmap/" class="kb-section-link">View Full Roadmap →</a>
            </div>
            {{< roadmap-cards >}}
        </div>
    </div>
</section>
<section class="cta-section">
    <h2>Can't Find What You're Looking For?</h2>
    <p>Our team is here to help with any questions.</p>
    <a href="/company/contact/" class="btn btn-primary">
        Contact Support
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
    </a>
</section>

