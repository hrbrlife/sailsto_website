---
title: "Documentation"
description: "Technical documentation for Sails.to platform — architecture overview, API reference, token standards, compliance framework, and integration guides."
stylesheets:
  - "../../assets/fonts/fonts.css"
  - "../../styles.css"
  - "../../assets/css/glossary.css"
---


    <section class="page-hero">
        <span class="section-label">Technical Reference</span>
        <h1 class="section-title">Documentation</h1>
        <p class="section-desc">Everything you need to integrate with and build on the Sails.to platform.</p>
    </section>
    <section class="docs-main">
        <div class="docs-container">
            <aside class="docs-sidebar">
                <nav class="docs-nav">
                    <h4>Getting Started</h4>
                    <a href="getting-started.html" class="docs-link">Quick Start Guide</a>
                    <a href="platform-overview.html" class="docs-link">Platform Overview</a>
                    <a href="hybrid-architecture.html" class="docs-link">Hybrid Architecture</a>
                    <h4>Token Standard</h4>
                    <a href="token-standard.html" class="docs-link">SPL Token Implementation</a>
                    <a href="metadata.html" class="docs-link">Token Metadata</a>
                    <a href="compliance-extensions.html" class="docs-link">Compliance Extensions</a>
                    <h4>API Reference</h4>
                    <a href="api-reference.html" class="docs-link">API Overview</a>
                    <a href="authentication.html" class="docs-link">Authentication</a>
                    <a href="investors-api.html" class="docs-link">Investors API</a>
                    <a href="cap-table-api.html" class="docs-link">Cap Table API</a>
                    <a href="distributions-api.html" class="docs-link">Distributions API</a>
                    <h4>Compliance</h4>
                    <a href="compliance-framework.html" class="docs-link">Compliance Framework</a>
                    <a href="kyc-integration.html" class="docs-link">KYC Integration</a>
                    <a href="transfer-rules.html" class="docs-link">Transfer Rules</a>
                    <h4>TradFi Bridge</h4>
                    <a href="tradfi-bridge.html" class="docs-link">Bridge Overview</a>
                    <a href="isin-conversion.html" class="docs-link">ISIN Conversion</a>
                    <a href="clearstream.html" class="docs-link">Clearstream Integration</a>
                </nav>
            </aside>
            <main class="docs-content">
                <div class="docs-hero-card">
                    <h2>Welcome to Sails.to Docs</h2>
                    <p>This documentation covers everything you need to understand, integrate with, and build on the Sails.to hybrid securities platform.</p>
                    <div class="docs-quick-links">
                        <a href="getting-started.html" class="docs-quick-link">
                            <span class="icon">🚀</span>
                            <span class="text">
                                <strong>Quick Start</strong>
                                <small>Get up and running in minutes</small>
                            </span>
                        </a>
                        <a href="api-reference.html" class="docs-quick-link">
                            <span class="icon">⚡</span>
                            <span class="text">
                                <strong>API Reference</strong>
                                <small>Explore our REST APIs</small>
                            </span>
                        </a>
                    </div>
                </div>
                <section class="docs-section">
                    <h3>Core Concepts</h3>
                    <div class="docs-grid">
                        <a href="platform-overview.html" class="docs-card">
                            <span class="docs-card-icon">🏗️</span>
                            <h4>Platform Overview</h4>
                            <p>High-level architecture, components, and data flows.</p>
                        </a>
                        <a href="hybrid-architecture.html" class="docs-card">
                            <span class="docs-card-icon">🔗</span>
                            <h4>Hybrid Architecture</h4>
                            <p>How blockchain and traditional finance systems interoperate.</p>
                        </a>
                        <a href="token-standard.html" class="docs-card">
                            <span class="docs-card-icon">🪙</span>
                            <h4>Token Standard</h4>
                            <p>SPL token implementation with compliance extensions.</p>
                        </a>
                        <a href="compliance-framework.html" class="docs-card">
                            <span class="docs-card-icon">⚖️</span>
                            <h4>Compliance Framework</h4>
                            <p>On-chain transfer restrictions and regulatory hooks.</p>
                        </a>
                    </div>
                </section>
                <section class="docs-section">
                    <h3>API Reference</h3>
                    <p>Our REST API enables programmatic access to core platform functionality.</p>
                    <div class="docs-api-preview">
                        <div class="docs-api-header">
                            <span class="docs-api-method get">GET</span>
                            <code>/api/v1/investors/{id}</code>
                        </div>
                        <p class="docs-api-desc">Retrieve investor details including KYC status and holdings.</p>
                    </div>
                    <div class="docs-api-preview">
                        <div class="docs-api-header">
                            <span class="docs-api-method get">GET</span>
                            <code>/api/v1/offerings/{id}/cap-table</code>
                        </div>
                        <p class="docs-api-desc">Get current cap table for an offering with ownership percentages.</p>
                    </div>
                    <div class="docs-api-preview">
                        <div class="docs-api-header">
                            <span class="docs-api-method post">POST</span>
                            <code>/api/v1/distributions</code>
                        </div>
                        <p class="docs-api-desc">Create and execute a distribution to token holders.</p>
                    </div>
                    <a href="api-reference.html" class="docs-section-link">View Full API Reference →</a>
                </section>
                <section class="docs-section">
                    <h3>TradFi Bridge</h3>
                    <p>The TradFi Bridge enables seamless conversion between Solana tokens and ISIN-denominated securities at Clearstream.</p>
                    <div class="docs-diagram">
                        <div class="docs-diagram-step">
                            <span class="step-num">1</span>
                            <span class="step-text">Investor initiates bridge request</span>
                        </div>
                        <div class="docs-diagram-arrow">→</div>
                        <div class="docs-diagram-step">
                            <span class="step-num">2</span>
                            <span class="step-text">Tokens burned/locked on Solana</span>
                        </div>
                        <div class="docs-diagram-arrow">→</div>
                        <div class="docs-diagram-step">
                            <span class="step-num">3</span>
                            <span class="step-text">ISIN securities credited at Clearstream</span>
                        </div>
                    </div>
                    <a href="tradfi-bridge.html" class="docs-section-link">Learn More About the Bridge →</a>
                </section>
                <section class="docs-section">
                    <h3>Need Help?</h3>
                    <div class="docs-help-grid">
                        <a href="../faq.html" class="docs-help-link">
                            <span class="icon">❓</span>
                            <span class="text">FAQ</span>
                        </a>
                        <a href="https://github.com/sailsto" class="docs-help-link" target="_blank">
                            <span class="icon">🐙</span>
                            <span class="text">GitHub</span>
                        </a>
                        <a href="../../company/contact.html" class="docs-help-link">
                            <span class="icon">💬</span>
                            <span class="text">Contact</span>
                        </a>
                    </div>
                </section>
            </main>
        </div>
    </section>
    
