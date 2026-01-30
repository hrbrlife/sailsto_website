/* ═══════════════════════════════════════════════════════════════
   SAILS.TO GLOSSARY TOOLTIPS
   Automatic term detection and tooltip display
   ═══════════════════════════════════════════════════════════════ */

(function() {
    'use strict';
    
    // Glossary data - will be loaded from JSON
    let glossaryData = null;
    
    // Tooltip element
    let tooltipEl = null;
    let hideTimeout = null;
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    async function init() {
        // Create tooltip element
        createTooltip();
        
        // Load glossary data
        await loadGlossaryData();
        
        // Find and enhance glossary terms
        enhanceGlossaryTerms();
        
        // Set up event listeners
        setupEventListeners();
    }
    
    function createTooltip() {
        tooltipEl = document.createElement('div');
        tooltipEl.className = 'glossary-tooltip';
        tooltipEl.innerHTML = `
            <div class="glossary-tooltip-content">
                <div class="glossary-tooltip-header">
                    <span class="glossary-tooltip-term"></span>
                    <span class="glossary-tooltip-category"></span>
                </div>
                <p class="glossary-tooltip-definition"></p>
                <a href="#" class="glossary-tooltip-link">
                    Read full definition
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                </a>
                <div class="glossary-tooltip-arrow"></div>
            </div>
        `;
        document.body.appendChild(tooltipEl);
    }
    
    async function loadGlossaryData() {
        // Try to determine the correct path based on current page location
        const paths = [
            '/assets/content/glossary.json',
            '../assets/content/glossary.json',
            '../../assets/content/glossary.json',
            '../../../assets/content/glossary.json',
            'assets/content/glossary.json'
        ];
        
        for (const path of paths) {
            try {
                const response = await fetch(path);
                if (response.ok) {
                    glossaryData = await response.json();
                    return;
                }
            } catch (e) {
                // Try next path
            }
        }
        
        // Fallback: embedded data for essential terms
        glossaryData = getEmbeddedGlossary();
    }
    
    function getEmbeddedGlossary() {
        // Embedded fallback for all terms used across the site
        return {
            "security-token": {
                "term": "Security Token",
                "shortDefinition": "A digital representation of a traditional security (equity, debt, or fund share) issued on a blockchain with built-in compliance rules.",
                "category": "Finance"
            },
            "kyc": {
                "term": "KYC (Know Your Customer)",
                "shortDefinition": "Regulatory process to verify the identity of clients and assess their suitability for financial services.",
                "category": "Compliance"
            },
            "aml": {
                "term": "AML (Anti-Money Laundering)",
                "shortDefinition": "Laws and procedures designed to prevent criminals from disguising illegally obtained funds as legitimate income.",
                "category": "Compliance"
            },
            "isin": {
                "term": "ISIN",
                "shortDefinition": "International Securities Identification Number - a 12-character code that uniquely identifies a security globally.",
                "category": "Finance"
            },
            "clearstream": {
                "term": "Clearstream",
                "shortDefinition": "A major international securities depository enabling custody and settlement across 110+ markets worldwide.",
                "category": "Finance"
            },
            "wyoming-dao-llc": {
                "term": "Wyoming DAO Series LLC",
                "shortDefinition": "Wyoming's legally-recognized DAO structure with Series LLC capability — each offering gets its own isolated series with separate assets/liabilities.",
                "category": "Legal"
            },
            "series-llc": {
                "term": "Series LLC",
                "shortDefinition": "A corporate structure allowing multiple segregated series under one LLC, each with isolated assets and liabilities.",
                "category": "Legal"
            },
            "spv": {
                "term": "SPV (Special Purpose Vehicle)",
                "shortDefinition": "A subsidiary entity created to isolate financial risk and hold specific assets separate from a parent company.",
                "category": "Legal"
            },
            "accredited-investor": {
                "term": "Accredited Investor",
                "shortDefinition": "An individual or entity meeting SEC financial thresholds ($1M+ net worth or $200K+ income) to invest in unregistered securities.",
                "category": "Compliance"
            },
            "professional-investor": {
                "term": "Professional Investor",
                "shortDefinition": "Under EU MiFID II regulations, an investor with sufficient expertise and experience to make independent investment decisions.",
                "category": "Compliance"
            },
            "reg-s": {
                "term": "Regulation S",
                "shortDefinition": "SEC regulation providing safe harbor for securities offerings made outside the United States to non-US persons.",
                "category": "Compliance"
            },
            "reg-d": {
                "term": "Regulation D",
                "shortDefinition": "SEC regulation providing exemptions from registration for private placements to accredited investors in the US.",
                "category": "Compliance"
            },
            "solana": {
                "term": "Solana",
                "shortDefinition": "High-performance blockchain with 400ms finality and sub-cent transaction fees used for CrossSecurities settlement.",
                "category": "Technology"
            },
            "smart-contract": {
                "term": "Smart Contract",
                "shortDefinition": "Self-executing code on blockchain that automatically enforces agreement terms — handles distributions, transfers, and compliance.",
                "category": "Technology"
            },
            "tradfi-bridge": {
                "term": "TradFi Bridge",
                "shortDefinition": "Infrastructure enabling conversion between blockchain tokens and traditional securities via ISIN/Clearstream.",
                "category": "Finance"
            },
            "tokenization": {
                "term": "Tokenization",
                "shortDefinition": "Creating a digital token on blockchain representing ownership of a real-world asset like securities or real estate.",
                "category": "Finance"
            },
            "custody": {
                "term": "Custody",
                "shortDefinition": "Safekeeping of securities by a regulated custodian — on Sails.to, either on-chain (Solana wallet) or via Clearstream.",
                "category": "Finance"
            },
            "secondary-trading": {
                "term": "Secondary Trading",
                "shortDefinition": "Buying and selling securities between investors after the initial offering, via our multi-broker OTC network.",
                "category": "Finance"
            },
            "cap-table": {
                "term": "Cap Table",
                "shortDefinition": "A record showing ownership stakes, equity dilution, and value of equity — maintained on-chain for transparency.",
                "category": "Finance"
            },
            "distributions": {
                "term": "Distributions",
                "shortDefinition": "Payments to security holders including coupon payments, dividends, or return of capital — automated via smart contract.",
                "category": "Finance"
            },
            "crosssecurities": {
                "term": "CrossSecurities",
                "shortDefinition": "Sails.to's hybrid securities that exist on-chain (Solana) but can CrossConvert to bankable ISIN form via Clearstream.",
                "category": "Finance"
            },
            "crossconversion": {
                "term": "CrossConversion",
                "shortDefinition": "The process of converting CrossSecurities between on-chain (Solana) and bankable (ISIN/Clearstream) forms.",
                "category": "Finance"
            },
            "soft-cap": {
                "term": "Soft Cap",
                "shortDefinition": "Minimum funding target for an offering. If not reached, all investments are automatically refunded.",
                "category": "Finance"
            },
            "hard-cap": {
                "term": "Hard Cap",
                "shortDefinition": "Maximum amount an offering can raise. No investments accepted beyond this limit.",
                "category": "Finance"
            },
            "coupon": {
                "term": "Coupon",
                "shortDefinition": "Periodic interest payment on a bond, expressed as annual percentage of nominal value (e.g., 8% p.a.).",
                "category": "Finance"
            },
            "maturity": {
                "term": "Maturity",
                "shortDefinition": "The date when a bond's principal must be repaid to investors and the security terminates.",
                "category": "Finance"
            },
            "nominal-value": {
                "term": "Nominal Value",
                "shortDefinition": "Face value of a security — the amount used to calculate coupon payments and repaid at maturity ($150,000 minimum on Sails.to).",
                "category": "Finance"
            },
            "escrow": {
                "term": "Escrow",
                "shortDefinition": "Funds held by a neutral third party until conditions are met — used during soft cap phase to protect investors.",
                "category": "Finance"
            },
            "trustee": {
                "term": "Trustee",
                "shortDefinition": "Independent party who oversees issuer compliance, holds security interests, and acts in bondholders' interests.",
                "category": "Legal"
            },
            "otc": {
                "term": "OTC (Over-the-Counter)",
                "shortDefinition": "Trading directly between parties rather than on a public exchange — our broker network facilitates OTC trading of CrossSecurities.",
                "category": "Finance"
            },
            "atomic-settlement": {
                "term": "Atomic Settlement",
                "shortDefinition": "Simultaneous exchange of securities and payment in a single transaction — impossible for one side to fail without the other.",
                "category": "Technology"
            },
            "vienna-mtf": {
                "term": "Vienna MTF",
                "shortDefinition": "Multilateral Trading Facility operated by Vienna Stock Exchange where CrossSecurities in ISIN form can be listed and traded.",
                "category": "Finance"
            },
            "distribution-fee": {
                "term": "Distribution Fee",
                "shortDefinition": "6% fee on capital raised through our broker network (vs 1% for direct referrals). Covers broker commissions and platform costs.",
                "category": "Finance"
            },
            "brokerage-fee": {
                "term": "Brokerage Fee",
                "shortDefinition": "0.5% fee on secondary trades split between platform and brokers. Waived during soft cap phase.",
                "category": "Finance"
            },
            "security-deposit": {
                "term": "Security Deposit",
                "shortDefinition": "$15,000 refundable deposit from issuers, held until end of term or offering cancellation. Ensures commitment.",
                "category": "Finance"
            },
            "operating-series": {
                "term": "Operating Series",
                "shortDefinition": "The DAO LLC series that holds pledged assets, revenue streams, and operational agreements backing the securities.",
                "category": "Legal"
            },
            "treasury-series": {
                "term": "Treasury Series",
                "shortDefinition": "The DAO LLC series managing reserves, distribution pools, and funds awaiting deployment or return to investors.",
                "category": "Legal"
            },
            "crossconversion-series": {
                "term": "CrossConversion Series",
                "shortDefinition": "The DAO LLC series handling the bridge between on-chain tokens and Clearstream-held ISIN securities.",
                "category": "Legal"
            },
            "operational-trust": {
                "term": "Operational Trust",
                "shortDefinition": "Trust structure holding investor funds during offering phase and managing distributions throughout the security's life.",
                "category": "Legal"
            },
            "private-placement": {
                "term": "Private Placement",
                "shortDefinition": "Sale of securities directly to qualified investors without public offering registration — how most CrossSecurities are issued.",
                "category": "Finance"
            },
            "offering-memorandum": {
                "term": "Offering Memorandum",
                "shortDefinition": "Legal document detailing investment terms, risks, use of proceeds, and issuer information — required for all offerings.",
                "category": "Legal"
            },
            "broker-dealer": {
                "term": "Broker-Dealer",
                "shortDefinition": "Licensed securities professional who can execute trades and place investors in offerings through our network.",
                "category": "Finance"
            },
            "liquidity": {
                "term": "Liquidity",
                "shortDefinition": "Ease of buying/selling a security without affecting its price — our OTC network provides liquidity for CrossSecurities.",
                "category": "Finance"
            },
            "minimum-investment": {
                "term": "Minimum Investment",
                "shortDefinition": "$150,000 per CrossSecurity — set to comply with professional/accredited investor regulations globally.",
                "category": "Finance"
            },
            "compliance": {
                "term": "Compliance",
                "shortDefinition": "Adherence to legal/regulatory requirements — automated on-chain via KYC/AML, investor eligibility, and transfer restrictions.",
                "category": "Compliance"
            },
            "on-chain": {
                "term": "On-Chain",
                "shortDefinition": "Recorded directly on blockchain — CrossSecurities exist on Solana with ownership, transfers, and compliance enforced by smart contracts.",
                "category": "Technology"
            },
            "bankable": {
                "term": "Bankable",
                "shortDefinition": "Securities recognized by traditional banking — CrossSecurities can CrossConvert to ISIN form held via Clearstream.",
                "category": "Finance"
            },
            "commission": {
                "term": "Commission",
                "shortDefinition": "Fees paid to brokers/introducers for placing investors — up to 5% primary, 0.5% secondary, 25% of platform fee for introducers.",
                "category": "Finance"
            },
            "investor-verification": {
                "term": "Investor Verification",
                "shortDefinition": "Process confirming identity, financial status, and eligibility to invest — KYC/AML plus accredited/professional status check.",
                "category": "Compliance"
            }
        };
    }
    
    function enhanceGlossaryTerms() {
        if (!glossaryData) return;
        
        // Find all elements with data-term attribute (explicitly marked)
        const explicitTerms = document.querySelectorAll('[data-term]');
        explicitTerms.forEach(el => {
            if (!el.classList.contains('glossary-term')) {
                el.classList.add('glossary-term');
            }
        });
        
        // Also find elements with class glossary-term that might need data-term
        const classTerms = document.querySelectorAll('.glossary-term:not([data-term])');
        classTerms.forEach(el => {
            // Try to match text content to a glossary term
            const text = el.textContent.toLowerCase().trim();
            for (const [key, data] of Object.entries(glossaryData)) {
                if (data.term && data.term.toLowerCase() === text) {
                    el.setAttribute('data-term', key);
                    break;
                }
            }
        });
    }
    
    function setupEventListeners() {
        // Use event delegation for efficiency
        document.addEventListener('mouseenter', handleMouseEnter, true);
        document.addEventListener('mouseleave', handleMouseLeave, true);
        document.addEventListener('click', handleClick, true);
        
        // Hide tooltip on scroll
        window.addEventListener('scroll', () => {
            hideTooltip();
        }, { passive: true });
        
        // Keep tooltip visible when hovering over it
        tooltipEl.addEventListener('mouseenter', () => {
            clearTimeout(hideTimeout);
        });
        
        tooltipEl.addEventListener('mouseleave', () => {
            hideTooltip();
        });
    }
    
    function handleMouseEnter(e) {
        const term = e.target.closest('.glossary-term');
        if (term) {
            clearTimeout(hideTimeout);
            showTooltip(term);
        }
    }
    
    function handleMouseLeave(e) {
        const term = e.target.closest('.glossary-term');
        if (term) {
            hideTimeout = setTimeout(() => {
                hideTooltip();
            }, 150);
        }
    }
    
    function handleClick(e) {
        const term = e.target.closest('.glossary-term');
        if (term && e.target.tagName !== 'A') {
            // On mobile, click toggles tooltip
            if (tooltipEl.style.opacity === '1') {
                hideTooltip();
            } else {
                showTooltip(term);
            }
        }
    }
    
    function showTooltip(termElement) {
        if (!glossaryData) return;
        
        const termKey = termElement.getAttribute('data-term');
        if (!termKey) return;
        
        const data = glossaryData[termKey];
        if (!data) return;
        
        // Populate tooltip content
        const termEl = tooltipEl.querySelector('.glossary-tooltip-term');
        const categoryEl = tooltipEl.querySelector('.glossary-tooltip-category');
        const definitionEl = tooltipEl.querySelector('.glossary-tooltip-definition');
        const linkEl = tooltipEl.querySelector('.glossary-tooltip-link');
        
        termEl.textContent = data.term;
        categoryEl.textContent = data.category;
        categoryEl.className = 'glossary-tooltip-category category-' + data.category.toLowerCase();
        definitionEl.textContent = data.shortDefinition;
        
        // Set link to glossary page
        const basePath = getGlossaryBasePath();
        linkEl.href = basePath + termKey + '.html';
        
        // Position tooltip
        positionTooltip(termElement);
        
        // Show tooltip
        tooltipEl.style.opacity = '1';
    }
    
    function hideTooltip() {
        tooltipEl.style.opacity = '0';
    }
    
    function positionTooltip(termElement) {
        const rect = termElement.getBoundingClientRect();
        const tooltipRect = tooltipEl.getBoundingClientRect();
        
        // Calculate position
        let top = rect.top - tooltipRect.height - 12;
        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
        
        // Check if tooltip would go above viewport
        if (top < 10) {
            // Position below instead
            top = rect.bottom + 12;
            tooltipEl.classList.add('tooltip-below');
        } else {
            tooltipEl.classList.remove('tooltip-below');
        }
        
        // Check horizontal bounds
        if (left < 10) {
            left = 10;
        } else if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        
        tooltipEl.style.top = top + 'px';
        tooltipEl.style.left = left + 'px';
    }
    
    function getGlossaryBasePath() {
        // Determine correct path based on current page
        const path = window.location.pathname;
        
        if (path.includes('/knowledge/glossary/')) {
            return '';
        } else if (path.includes('/knowledge/blog/') || path.includes('/knowledge/docs/') || path.includes('/knowledge/guides/')) {
            return '../glossary/';
        } else if (path.includes('/knowledge/')) {
            return 'glossary/';
        } else if (path.includes('/company/')) {
            return '../knowledge/glossary/';
        } else {
            return 'knowledge/glossary/';
        }
    }
    
})();
