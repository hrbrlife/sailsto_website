---
title: "Glossary"
description: "Complete glossary of terms for CrossSecurities, tokenized securities, blockchain, compliance, and traditional finance. Definitions for CrossSecurities, CrossConversion, security tokens, KYC, ISIN, Wyoming DAO, and more."
ogImage: "/og-image.png"
keywords: ["glossary", "complete", "terms", "crosssecurities", "tokenized", "securities", "blockchain", "compliance"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/knowledge-glossary-index.css"
scripts:
  - "/js/knowledge-glossary-index.js"
---


<section class="page-hero">
    <span class="section-label">Reference</span>
    <h1 class="section-title">Glossary</h1>
    <p class="section-desc">Key terms and concepts for understanding Sails CrossSecurities infrastructure.</p>
    <div class="glossary-search">
        <input type="text" id="glossary-search-input" placeholder="Search terms..." class="glossary-search-input">
        <svg class="glossary-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
        </svg>
    </div>
</section>
<section class="glossary-filter-section">
    <div class="glossary-container">
        <div class="glossary-filters">
            <button class="glossary-filter active" data-category="all">All Terms</button>
            <button class="glossary-filter" data-category="finance">💰 Finance</button>
            <button class="glossary-filter" data-category="compliance">⚖️ Compliance</button>
            <button class="glossary-filter" data-category="legal">📜 Legal</button>
            <button class="glossary-filter" data-category="technology">⚙️ Technology</button>
        </div>
    </div>
</section>
<section class="glossary-main">
    <div class="glossary-container">
        <div class="glossary-alphabet">
            <a href="#A" class="alpha-link">A</a>
            <a href="#C" class="alpha-link">C</a>
            <a href="#D" class="alpha-link">D</a>
            <a href="#G" class="alpha-link">G</a>
            <a href="#I" class="alpha-link">I</a>
            <a href="#K" class="alpha-link">K</a>
            <a href="#M" class="alpha-link">M</a>
            <a href="#N" class="alpha-link">N</a>
            <a href="#P" class="alpha-link">P</a>
            <a href="#R" class="alpha-link">R</a>
            <a href="#S" class="alpha-link">S</a>
            <a href="#T" class="alpha-link">T</a>
            <a href="#W" class="alpha-link">W</a>
        </div>
        <div class="glossary-letter-section" id="A">
            <h2 class="glossary-letter">A</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/accredited-investor/" class="glossary-card" data-category="compliance">
                    <span class="glossary-card-category compliance">Compliance</span>
                    <h3>Accredited Investor</h3>
                    <p>A U.S. designation for investors meeting specific wealth or income thresholds, allowing access to unregistered securities offerings.</p>
                </a>
                <a href="/knowledge/glossary/aml/" class="glossary-card" data-category="compliance">
                    <span class="glossary-card-category compliance">Compliance</span>
                    <h3>AML (Anti-Money Laundering)</h3>
                    <p>Regulations and procedures designed to prevent criminals from disguising illegally obtained funds as legitimate income.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="C">
            <h2 class="glossary-letter">C</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/cap-n-proto/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Cap'n Proto</h3>
                    <p>Zero-copy serialization protocol used for inter-grain RPC communication in the Sails.to platform, enabling native Sandstorm integration without HTTP bridges.</p>
                </a>
                <a href="/knowledge/glossary/cap-table/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Cap Table</h3>
                    <p>A spreadsheet or database showing the ownership stakes, equity dilution, and value of equity in each round of investment.</p>
                </a>
                <a href="/knowledge/glossary/clearstream/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Clearstream</h3>
                    <p>A Luxembourg-based international central securities depository providing settlement, custody, and asset servicing for securities.</p>
                </a>
                <a href="/knowledge/glossary/crossconversion/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>CrossConversion</h3>
                    <p>The process of converting Sails CrossSecurities between on-chain form (Solana) and bankable form (ISIN/Clearstream).</p>
                </a>
                <a href="/knowledge/glossary/crosssecurities/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>CrossSecurities</h3>
                    <p>Sails' dual-format securities that can be held on-chain (Solana) or in bankable form (ISIN/Clearstream) and converted between forms at will.</p>
                </a>
                <a href="/knowledge/glossary/custody/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Custody</h3>
                    <p>The safekeeping and management of assets on behalf of investors, either through self-custody (private keys) or institutional custody (banks/depositories).</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="D">
            <h2 class="glossary-letter">D</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/distributions/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Distributions</h3>
                    <p>Payments of profits, dividends, or returns to security holders, typically calculated pro-rata based on ownership percentage.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="G">
            <h2 class="glossary-letter">G</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/grain/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Grain</h3>
                    <p>The fundamental isolation unit in Sandstorm/Melusina OS — a sandboxed application instance with its own journal store, capabilities, and lifecycle.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="I">
            <h2 class="glossary-letter">I</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/isin/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>ISIN</h3>
                    <p>International Securities Identification Number — a 12-character code uniquely identifying a security for trading and settlement globally.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="K">
            <h2 class="glossary-letter">K</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/kyc/" class="glossary-card" data-category="compliance">
                    <span class="glossary-card-category compliance">Compliance</span>
                    <h3>KYC (Know Your Customer)</h3>
                    <p>Identity verification procedures required by financial regulations to confirm the identity of customers and assess potential risks.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="M">
            <h2 class="glossary-letter">M</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/master-nft/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Master NFT</h3>
                    <p>The root authority token in Sails.to's 4-layer NFT hierarchy on Solana, controlled by 3-of-5 keyholder threshold signing.</p>
                </a>
                <a href="/knowledge/glossary/melusina/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Melusina</h3>
                    <p>The on-chain authority layer for Sails.to — a Solana-based system implementing NFT hierarchies, KYC credentialing, and threshold crypto operations.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="N">
            <h2 class="glossary-letter">N</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/nft-hierarchy/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>NFT Hierarchy</h3>
                    <p>Sails.to's 4-layer authority structure on Solana: Master → Reseller → License → Share, ensuring cryptographic chain of trust.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="P">
            <h2 class="glossary-letter">P</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/paying-agent/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Paying Agent</h3>
                    <p>The entity authorized to execute distributions and manage the revenue waterfall for a Sails.to offering, operating under Trustee oversight.</p>
                </a>
                <a href="/knowledge/glossary/pda/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>PDA (Program Derived Address)</h3>
                    <p>A deterministic Solana account address derived from program seeds, enabling trustless programmatic state management for offerings and compliance.</p>
                </a>
                <a href="/knowledge/glossary/powerbox/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Powerbox</h3>
                    <p>The inter-grain capability sharing mechanism in Sandstorm/Melusina OS, enabling secure permission delegation via claim tokens and persistent sturdyRefs.</p>
                </a>
                <a href="/knowledge/glossary/professional-investor/" class="glossary-card" data-category="compliance">
                    <span class="glossary-card-category compliance">Compliance</span>
                    <h3>Professional Investor</h3>
                    <p>European classification for investors with sufficient experience, knowledge, and expertise to make their own investment decisions.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="R">
            <h2 class="glossary-letter">R</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/reg-d/" class="glossary-card" data-category="legal">
                    <span class="glossary-card-category legal">Legal</span>
                    <h3>Regulation D (Reg D)</h3>
                    <p>SEC rules providing exemptions from registration for private securities offerings, primarily to accredited investors.</p>
                </a>
                <a href="/knowledge/glossary/reg-s/" class="glossary-card" data-category="legal">
                    <span class="glossary-card-category legal">Legal</span>
                    <h3>Regulation S (Reg S)</h3>
                    <p>SEC rules allowing offerings outside the United States without SEC registration, for non-U.S. investors.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="S">
            <h2 class="glossary-letter">S</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/secondary-trading/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Secondary Trading</h3>
                    <p>The buying and selling of securities after their initial issuance, between investors rather than from the issuer.</p>
                </a>
                <a href="/knowledge/glossary/security-token/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Security Token</h3>
                    <p>A blockchain-based token representing ownership in a security, subject to securities regulations. See CrossSecurities for Sails' implementation.</p>
                </a>
                <a href="/knowledge/glossary/series-llc/" class="glossary-card" data-category="legal">
                    <span class="glossary-card-category legal">Legal</span>
                    <h3>Series LLC</h3>
                    <p>An LLC structure allowing multiple series with separate assets, liabilities, and members under one umbrella entity.</p>
                </a>
                <a href="/knowledge/glossary/smart-contract/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Smart Contract</h3>
                    <p>Self-executing code on a blockchain that automatically enforces the terms of an agreement when conditions are met.</p>
                </a>
                <a href="/knowledge/glossary/solana/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Solana</h3>
                    <p>A high-performance blockchain platform known for fast transaction speeds and low costs, used for Sails.to security tokens.</p>
                </a>
                <a href="/knowledge/glossary/spv/" class="glossary-card" data-category="legal">
                    <span class="glossary-card-category legal">Legal</span>
                    <h3>SPV (Special Purpose Vehicle)</h3>
                    <p>A legal entity created for a specific, limited purpose — often to isolate financial risk or hold particular assets.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="T">
            <h2 class="glossary-letter">T</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/threshold-signing/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Threshold Signing</h3>
                    <p>M-of-N keyholder cryptographic operations used to protect critical Sails.to platform actions, from Master NFT control to emergency freezes.</p>
                </a>
                <a href="/knowledge/glossary/tokenization/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Tokenization</h3>
                    <p>The process of converting rights to an asset into a digital token on a blockchain, enabling fractional ownership and programmable transfers.</p>
                </a>
                <a href="/knowledge/glossary/tradfi-bridge/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>TradFi Bridge (CrossConversion)</h3>
                    <p>Sails.to's CrossConversion system for converting CrossSecurities between on-chain and bankable form.</p>
                </a>
                <a href="/knowledge/glossary/transfer-hook/" class="glossary-card" data-category="technology">
                    <span class="glossary-card-category technology">Technology</span>
                    <h3>Transfer Hook</h3>
                    <p>A Solana SPL-2022 extension that intercepts token transfers and enforces compliance rules — KYC checks, jurisdiction whitelists, lock-up periods.</p>
                </a>
            </div>
        </div>
        <div class="glossary-letter-section" id="W">
            <h2 class="glossary-letter">W</h2>
            <div class="glossary-grid">
                <a href="/knowledge/glossary/waterfall/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>Waterfall</h3>
                    <p>The revenue distribution priority structure for offerings — senior debt first, then investors pro-rata, then platform fee, then treasury.</p>
                </a>
                <a href="/knowledge/glossary/white-label/" class="glossary-card" data-category="finance">
                    <span class="glossary-card-category finance">Finance</span>
                    <h3>White-Label</h3>
                    <p>Branded platform instances for regulated institutions, trust companies, and broker-dealers with custom theming and compliance controls.</p>
                </a>
                <a href="/knowledge/glossary/wyoming-dao-llc/" class="glossary-card" data-category="legal">
                    <span class="glossary-card-category legal">Legal</span>
                    <h3>Wyoming DAO LLC</h3>
                    <p>A legal structure under Wyoming law that recognizes DAOs as limited liability companies, providing legal certainty for blockchain-based organizations.</p>
                </a>
            </div>
        </div>
        <div class="glossary-no-results" style="display: none;">
            <span class="icon-wrapper"><svg><use href="#icon-scan"></use></svg></span>
            <h3>No matching terms found</h3>
            <p>Try a different search term or <a href="/company/contact/">suggest a term</a> to add to our glossary.</p>
        </div>
    </div>
</section>
<section class="cta-section">
    <h2>Ready to Put Knowledge into Action?</h2>
    <p>Start your journey with Sails CrossSecurities.</p>
    <a href="/signup/" class="btn btn-primary">
        Get Started
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
    </a>
</section>

