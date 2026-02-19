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
        <div class="kb-tabs" id="kb-tabs">
            <button class="kb-tab active" data-category="all">All Resources</button>
            <button class="kb-tab" data-category="guides">Guides</button>
            <button class="kb-tab" data-category="docs">Documentation</button>
            <button class="kb-tab" data-category="faq">FAQ</button>
            <button class="kb-tab" data-category="glossary">Glossary</button>
            <button class="kb-tab" data-category="blog">Blog</button>
            <button class="kb-tab" data-category="roadmap">Roadmap</button>
        </div>
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
                <div class="kb-glossary-categories">
                    <a href="glossary/index.html#finance" class="kb-glossary-cat">
                        <span class="kb-glossary-icon" style="color: var(--gold);">💰</span>
                        <span class="kb-glossary-label">Finance</span>
                        <span class="kb-glossary-count">31 terms</span>
                    </a>
                    <a href="glossary/index.html#compliance" class="kb-glossary-cat">
                        <span class="kb-glossary-icon" style="color: var(--navy);">⚖️</span>
                        <span class="kb-glossary-label">Compliance</span>
                        <span class="kb-glossary-count">8 terms</span>
                    </a>
                    <a href="glossary/index.html#legal" class="kb-glossary-cat">
                        <span class="kb-glossary-icon" style="color: var(--crimson);">📜</span>
                        <span class="kb-glossary-label">Legal</span>
                        <span class="kb-glossary-count">9 terms</span>
                    </a>
                    <a href="glossary/index.html#technology" class="kb-glossary-cat">
                        <span class="kb-glossary-icon" style="color: var(--slate);">⚙️</span>
                        <span class="kb-glossary-label">Technology</span>
                        <span class="kb-glossary-count">13 terms</span>
                    </a>
                </div>
                <div class="kb-glossary-featured">
                    <h4>Popular Terms</h4>
                    <div class="kb-glossary-terms">
                        <a href="/knowledge/glossary/crosssecurities/" class="glossary-term-pill">CrossSecurities</a>
                        <a href="/knowledge/glossary/crossconversion/" class="glossary-term-pill">CrossConversion</a>
                        <a href="/knowledge/glossary/wyoming-dao-llc/" class="glossary-term-pill">Wyoming DAO LLC</a>
                        <a href="/knowledge/glossary/isin/" class="glossary-term-pill">ISIN</a>
                        <a href="/knowledge/glossary/clearstream/" class="glossary-term-pill">Clearstream</a>
                        <a href="/knowledge/glossary/kyc/" class="glossary-term-pill">KYC</a>
                        <a href="/knowledge/glossary/nft-hierarchy/" class="glossary-term-pill">NFT Hierarchy</a>
                        <a href="/knowledge/glossary/grain/" class="glossary-term-pill">Grain</a>
                        <a href="/knowledge/glossary/threshold-signing/" class="glossary-term-pill">Threshold Signing</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="kb-resource-section" data-category="roadmap">
            <div class="kb-section-header">
                <h2><svg class="section-icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> Roadmap</h2>
                <p>Track our development progress and upcoming features</p>
                <a href="/knowledge/roadmap/" class="kb-section-link">View Full Roadmap →</a>
            </div>
            <div class="kb-temporal-filters">
                <button class="kb-temporal-tag active" data-temporal="all">All Phases</button>
                <button class="kb-temporal-tag" data-temporal="completed">✓ Completed</button>
                <button class="kb-temporal-tag" data-temporal="beta">● Beta</button>
                <button class="kb-temporal-tag" data-temporal="public">○ Public Launch</button>
                <button class="kb-temporal-tag" data-temporal="future">◇ Future</button>
            </div>
            <div class="kb-grid kb-roadmap-grid">
                <a href="/knowledge/roadmap/#wyoming-dao" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="completed" data-tags="legal compliance">
                    <span class="kb-roadmap-status completed">✓</span>
                    <span class="kb-card-category">Legal</span>
                    <h3>Wyoming DAO LLC Formation</h3>
                    <p>Legal entity established with full compliance framework for tokenized securities.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Completed</span>
                        <span class="kb-tag category">Compliance</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#core-platform" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="completed" data-tags="technical infrastructure">
                    <span class="kb-roadmap-status completed">✓</span>
                    <span class="kb-card-category">Technical</span>
                    <h3>Core Platform Architecture</h3>
                    <p>Solana smart contracts designed and audited for security token issuance.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Completed</span>
                        <span class="kb-tag category">Infrastructure</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#tradfi-bridge-design" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="completed" data-tags="technical infrastructure">
                    <span class="kb-roadmap-status completed">✓</span>
                    <span class="kb-card-category">Technical</span>
                    <h3>CrossConversion Design</h3>
                    <p>ISIN integration pathway and Clearstream custody protocol finalized.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Completed</span>
                        <span class="kb-tag category">Infrastructure</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#regulatory-framework" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="completed" data-tags="legal compliance">
                    <span class="kb-roadmap-status completed">✓</span>
                    <span class="kb-card-category">Compliance</span>
                    <h3>Regulatory Framework</h3>
                    <p>Reg S/Reg D compliance structure with automated investor verification.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Completed</span>
                        <span class="kb-tag category">Legal</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#platform-beta" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="beta" data-tags="product launch">
                    <span class="kb-roadmap-status current">●</span>
                    <span class="kb-card-category">Product</span>
                    <h3>Platform Beta Live</h3>
                    <p>Public beta launch with full issuer and investor onboarding.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal current">Beta</span>
                        <span class="kb-tag category">Launch</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#broker-network" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="beta" data-tags="product infrastructure">
                    <span class="kb-roadmap-status current">●</span>
                    <span class="kb-card-category">Product</span>
                    <h3>Broker Network Activation</h3>
                    <p>First licensed broker partners onboarded with white-label access.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal current">Beta</span>
                        <span class="kb-tag category">Infrastructure</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#first-offering" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="beta" data-tags="product milestone">
                    <span class="kb-roadmap-status current">●</span>
                    <span class="kb-card-category">Product</span>
                    <h3>First CrossSecurities Launch</h3>
                    <p>Inaugural CrossSecurities offering goes live on the platform.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal current">Beta</span>
                        <span class="kb-tag category">Milestone</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#kyc-integration" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="beta" data-tags="compliance technical">
                    <span class="kb-roadmap-status current">●</span>
                    <span class="kb-card-category">Compliance</span>
                    <h3>KYC/AML Integration</h3>
                    <p>Third-party verification partners integrated for automated compliance.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal current">Beta</span>
                        <span class="kb-tag category">Technical</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#tradfi-bridge-live" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="public" data-tags="technical infrastructure">
                    <span class="kb-roadmap-status upcoming">○</span>
                    <span class="kb-card-category">Technical</span>
                    <h3>CrossConversion Live</h3>
                    <p>Full ISIN conversion and Clearstream custody operational.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Public Launch</span>
                        <span class="kb-tag category">Infrastructure</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#secondary-trading" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="public" data-tags="product trading">
                    <span class="kb-roadmap-status upcoming">○</span>
                    <span class="kb-card-category">Product</span>
                    <h3>Secondary Trading</h3>
                    <p>P2P secondary market for compliant token trading between verified investors.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Public Launch</span>
                        <span class="kb-tag category">Trading</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#institutional-partners" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="public" data-tags="business partnerships">
                    <span class="kb-roadmap-status upcoming">○</span>
                    <span class="kb-card-category">Business</span>
                    <h3>Institutional Partners</h3>
                    <p>First institutional custodians and prime brokers integrated.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Public Launch</span>
                        <span class="kb-tag category">Partnerships</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#mobile-app" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="public" data-tags="product mobile">
                    <span class="kb-roadmap-status upcoming">○</span>
                    <span class="kb-card-category">Product</span>
                    <h3>Mobile Experience</h3>
                    <p>iOS and Android apps for investors with full portfolio management.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Public Launch</span>
                        <span class="kb-tag category">Mobile</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#eu-uk-licensing" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="future" data-tags="legal compliance expansion">
                    <span class="kb-roadmap-status future">◇</span>
                    <span class="kb-card-category">Legal</span>
                    <h3>EU/UK Licensing</h3>
                    <p>MiFID II compliance and FCA registration for European markets.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Future</span>
                        <span class="kb-tag category">Expansion</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#apac-expansion" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="future" data-tags="legal compliance expansion">
                    <span class="kb-roadmap-status future">◇</span>
                    <span class="kb-card-category">Legal</span>
                    <h3>APAC Expansion</h3>
                    <p>Singapore MAS and Hong Kong SFC regulatory pathways.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Future</span>
                        <span class="kb-tag category">Expansion</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#cross-chain" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="future" data-tags="technical infrastructure">
                    <span class="kb-roadmap-status future">◇</span>
                    <span class="kb-card-category">Technical</span>
                    <h3>Cross-Chain Support</h3>
                    <p>Ethereum and additional L1 integration for token portability.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Future</span>
                        <span class="kb-tag category">Infrastructure</span>
                    </div>
                </a>
                <a href="/knowledge/roadmap/#dao-governance" class="kb-card kb-card-roadmap" data-category="roadmap" data-temporal="future" data-tags="product governance">
                    <span class="kb-roadmap-status future">◇</span>
                    <span class="kb-card-category">Product</span>
                    <h3>DAO Governance</h3>
                    <p>Token holder voting and decentralized protocol governance activated.</p>
                    <div class="kb-card-tags">
                        <span class="kb-tag temporal">Future</span>
                        <span class="kb-tag category">Governance</span>
                    </div>
                </a>
            </div>
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

