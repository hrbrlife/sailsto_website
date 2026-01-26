---
title: "Active Issuers"
description: "Browse active securities offerings on Sails.to. Filter by structure and trust indicators."
keywords:
  - active offerings
  - tokenized bonds
  - security tokens
  - investment opportunities
  - verified issuers
  - trust indicators
ogImage: "/og-platform.png"
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/issuers-directory.css"
scripts:
  - "/js/issuers-directory.js"
---


<section class="page-hero">
    <h1>Active Offerings</h1>
    <p>Tokenized bonds from verified issuers. Filter by structure and trust indicators.</p>
</section>
<div class="filter-section">
    <div class="filter-container">
        <div class="filter-row">
            <div class="filter-group">
                <span class="filter-label">Structure</span>
                <div class="filter-pills">
                    <button class="filter-pill active" data-filter="structure" data-value="all">All</button>
                    <button class="filter-pill" data-filter="structure" data-value="coupon">Coupon Only</button>
                    <button class="filter-pill" data-filter="structure" data-value="profit">+ Profit Share</button>
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Trust</span>
                <div class="filter-pills">
                    <button class="filter-pill" data-filter="trust" data-value="audited">Audited</button>
                    <button class="filter-pill" data-filter="trust" data-value="regulated">Regulated</button>
                </div>
            </div>
            <span class="results-count"><span id="count">9</span> offerings</span>
        </div>
    </div>
</div>
<section class="issuers-section">
    <div class="issuers-container">
        <div class="issuers-grid">
            <div class="issuer-card" data-structure="coupon" data-audited="true" data-regulated="true">
                <div class="card-hero">
                    ☀️
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇰🇪 Kenya</div>
                        <h3 class="card-title">Solar Grid Africa</h3>
                    </div>
                    <p class="card-description">Distributed solar networks with long-term power purchase agreements from regional utilities.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">10% Coupon</span>
                        <span class="structure-pill maturity">10 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$5.2M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 76%;"></div>
                            <div class="soft-cap-marker" style="left: 59%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $4.0M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $6.8M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="coupon" data-audited="true" data-regulated="false">
                <div class="card-hero">
                    🏢
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇲🇺 Mauritius</div>
                        <h3 class="card-title">Coastal Development</h3>
                    </div>
                    <p class="card-description">12-hectare mixed-use waterfront development with luxury residential, commercial, and hospitality.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">8.5% Coupon</span>
                        <span class="structure-pill maturity">8 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$1.8M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 43%;"></div>
                            <div class="soft-cap-marker" style="left: 48%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $2.0M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $4.2M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item inactive">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="coupon" data-audited="true" data-regulated="true">
                <div class="card-hero">
                    🔋
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇦🇪 UAE</div>
                        <h3 class="card-title">Solar + Storage Platform</h3>
                    </div>
                    <p class="card-description">Commercial and industrial solar + battery storage with 25-year service contracts across MENA.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">11% Coupon</span>
                        <span class="structure-pill maturity">10 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$6.1M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 85%;"></div>
                            <div class="soft-cap-marker" style="left: 56%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $4.0M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $7.2M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="true" data-regulated="false">
                <div class="card-hero">
                    🌱
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇧🇷 Brazil</div>
                        <h3 class="card-title">Sustainable Agribusiness</h3>
                    </div>
                    <p class="card-description">Certified organic coffee and cacao on 800 hectares with direct premium market access.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">6% Coupon</span>
                        <span class="structure-pill profit">+15% Profit</span>
                        <span class="structure-pill maturity">7 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$1.2M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 48%;"></div>
                            <div class="soft-cap-marker" style="left: 60%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $1.5M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $2.5M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📄</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item inactive">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="true" data-regulated="true">
                <div class="card-hero">
                    🏙️
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇵🇹 Portugal</div>
                        <h3 class="card-title">Lisbon Urban Renewal</h3>
                    </div>
                    <p class="card-description">Historic building conversion in tech quarter with co-working, residential, and retail pre-leasing.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">7% Coupon</span>
                        <span class="structure-pill profit">+10% Profit</span>
                        <span class="structure-pill maturity">6 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$3.4M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 89%;"></div>
                            <div class="soft-cap-marker" style="left: 53%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $2.0M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $3.8M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="true" data-regulated="true">
                <div class="card-hero">
                    💻
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇸🇬 Singapore</div>
                        <h3 class="card-title">FinTech Growth Fund</h3>
                    </div>
                    <p class="card-description">Venture debt fund providing growth capital to Series B/C fintech companies across Southeast Asia.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">9% Coupon</span>
                        <span class="structure-pill profit">+8% Exit</span>
                        <span class="structure-pill maturity">5 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$4.8M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 87%;"></div>
                            <div class="soft-cap-marker" style="left: 64%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $3.5M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $5.5M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📄</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="true" data-regulated="false">
                <div class="card-hero">
                    🏖️
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇲🇽 Mexico</div>
                        <h3 class="card-title">Resort & Residences</h3>
                    </div>
                    <p class="card-description">Beachfront resort and fractional residence community with branded management and buyback guarantee.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">8% Coupon</span>
                        <span class="structure-pill profit">+5% Revenue</span>
                        <span class="structure-pill maturity">8 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$2.1M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 41%;"></div>
                            <div class="soft-cap-marker" style="left: 49%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $2.5M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $5.1M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item inactive">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="true" data-regulated="true">
                <div class="card-hero">
                    📦
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇮🇳 India</div>
                        <h3 class="card-title">Logistics Network Hub</h3>
                    </div>
                    <p class="card-description">Multi-modal logistics platform with warehousing, last-mile delivery, and reverse logistics across 12 metros.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">8% Coupon</span>
                        <span class="structure-pill profit">+12% EBITDA</span>
                        <span class="structure-pill maturity">7 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$7.2M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 85%;"></div>
                            <div class="soft-cap-marker" style="left: 59%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $5.0M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $8.5M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item active">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">�</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
            <div class="issuer-card" data-structure="profit" data-audited="false" data-regulated="false">
                <div class="card-hero">
                    🌾
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <div class="card-location">🇮🇩 Indonesia</div>
                        <h3 class="card-title">Palm & Biodiversity</h3>
                    </div>
                    <p class="card-description">Regenerative agriculture platform consolidating smallholder farms into sustainable export cooperatives.</p>
                    <div class="structure-row">
                        <span class="structure-pill coupon">7% Coupon</span>
                        <span class="structure-pill profit">+18% Profit</span>
                        <span class="structure-pill maturity">6 Years</span>
                    </div>
                    <div class="funding-section">
                        <div class="funding-header">
                            <span class="funding-label">Funding Progress</span>
                            <span class="funding-amount">$0.9M raised</span>
                        </div>
                        <div class="funding-bar-container">
                            <div class="funding-bar" style="width: 28%;"></div>
                            <div class="soft-cap-marker" style="left: 56%;"></div>
                        </div>
                        <div class="funding-caps">
                            <span class="cap-label"><span class="cap-dot soft"></span> Soft $1.8M</span>
                            <span class="cap-label"><span class="cap-dot hard"></span> Hard $3.2M</span>
                        </div>
                    </div>
                    <div class="trust-section">
                        <div class="trust-label">Trust Indicators</div>
                        <div class="trust-grid">
                            <div class="trust-item inactive">
                                <span class="trust-icon">🔍</span>
                                <span class="trust-text">Audited</span>
                            </div>
                            <div class="trust-item inactive">
                                <span class="trust-icon">📋</span>
                                <span class="trust-text">CPA</span>
                            </div>
                            <div class="trust-item active">
                                <span class="trust-icon">📄</span>
                                <span class="trust-text">Prospectus</span>
                            </div>
                            <div class="trust-item inactive">
                                <span class="trust-icon">🏛️</span>
                                <span class="trust-text">Regulated</span>
                            </div>
                        </div>
                    </div>
                    <a href="/investors/" class="card-cta">View Details</a>
                </div>
            </div>
        </div>
    </div>
</section>
