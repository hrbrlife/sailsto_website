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
        // Embedded fallback for essential terms
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
                "shortDefinition": "A major international securities depository enabling custody and settlement across 110+ markets.",
                "category": "Finance"
            },
            "wyoming-dao-llc": {
                "term": "Wyoming DAO LLC",
                "shortDefinition": "A limited liability company structure recognized by Wyoming law for decentralized autonomous organizations.",
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
                "shortDefinition": "An individual or entity meeting SEC financial thresholds that qualifies to invest in unregistered securities.",
                "category": "Compliance"
            },
            "professional-investor": {
                "term": "Professional Investor",
                "shortDefinition": "Under EU/international regulations, an investor with sufficient expertise to make independent investment decisions.",
                "category": "Compliance"
            },
            "reg-s": {
                "term": "Regulation S",
                "shortDefinition": "SEC regulation providing safe harbor for securities offerings made outside the United States.",
                "category": "Compliance"
            },
            "reg-d": {
                "term": "Regulation D",
                "shortDefinition": "SEC regulation providing exemptions from registration for private placements to accredited investors.",
                "category": "Compliance"
            },
            "solana": {
                "term": "Solana",
                "shortDefinition": "A high-performance blockchain known for fast transactions (400ms finality) and low fees.",
                "category": "Technology"
            },
            "smart-contract": {
                "term": "Smart Contract",
                "shortDefinition": "Self-executing code on a blockchain that automatically enforces agreement terms when conditions are met.",
                "category": "Technology"
            },
            "tradfi-bridge": {
                "term": "TradFi Bridge",
                "shortDefinition": "Infrastructure enabling conversion between blockchain tokens and traditional securities via ISIN/Clearstream.",
                "category": "Finance"
            },
            "tokenization": {
                "term": "Tokenization",
                "shortDefinition": "The process of creating a digital token on a blockchain that represents ownership of a real-world asset.",
                "category": "Finance"
            },
            "custody": {
                "term": "Custody",
                "shortDefinition": "The safekeeping and administration of securities on behalf of investors by a regulated custodian.",
                "category": "Finance"
            },
            "secondary-trading": {
                "term": "Secondary Trading",
                "shortDefinition": "The buying and selling of securities between investors after the initial offering.",
                "category": "Finance"
            },
            "cap-table": {
                "term": "Cap Table",
                "shortDefinition": "A record showing ownership stakes, equity dilution, and value of equity in each round of investment.",
                "category": "Finance"
            },
            "distributions": {
                "term": "Distributions",
                "shortDefinition": "Payments made to security holders, including dividends, interest, or return of capital.",
                "category": "Finance"
            },
            "soft-cap": {
                "term": "Soft Cap",
                "shortDefinition": "The minimum funding threshold an offering must reach for the capital raise to proceed.",
                "category": "Finance"
            },
            "hard-cap": {
                "term": "Hard Cap",
                "shortDefinition": "The maximum amount of capital an issuer will accept in a securities offering.",
                "category": "Finance"
            },
            "coupon": {
                "term": "Coupon",
                "shortDefinition": "The periodic interest payment made to bondholders, typically expressed as an annual percentage of nominal value.",
                "category": "Finance"
            },
            "maturity": {
                "term": "Maturity",
                "shortDefinition": "The date on which a bond's principal amount becomes due and payable to the bondholder.",
                "category": "Finance"
            },
            "nominal-value": {
                "term": "Nominal Value",
                "shortDefinition": "The face value of a security as stated by the issuer, representing the principal amount for bonds.",
                "category": "Finance"
            },
            "escrow": {
                "term": "Escrow",
                "shortDefinition": "A neutral holding arrangement where funds are held by a trusted third party until conditions are met.",
                "category": "Finance"
            },
            "trustee": {
                "term": "Trustee",
                "shortDefinition": "An independent fiduciary entity that represents and protects the interests of bondholders or investors.",
                "category": "Legal"
            },
            "otc": {
                "term": "OTC (Over-the-Counter)",
                "shortDefinition": "Securities trading conducted directly between two parties without a centralized exchange.",
                "category": "Finance"
            },
            "atomic-settlement": {
                "term": "Atomic Settlement",
                "shortDefinition": "A transaction mechanism where all parts of a trade execute simultaneously and completely, or not at all.",
                "category": "Technology"
            },
            "vienna-mtf": {
                "term": "Vienna MTF",
                "shortDefinition": "A regulated Multilateral Trading Facility providing compliant secondary trading for security tokens.",
                "category": "Finance"
            },
            "distribution-fee": {
                "term": "Distribution Fee",
                "shortDefinition": "A fee charged to distribute securities tokens to investors during an offering.",
                "category": "Finance"
            },
            "brokerage-fee": {
                "term": "Brokerage Fee",
                "shortDefinition": "A fee charged by a broker for executing securities transactions on behalf of clients.",
                "category": "Finance"
            },
            "security-deposit": {
                "term": "Security Deposit",
                "shortDefinition": "An upfront payment required from issuers to initiate onboarding and cover structuring costs.",
                "category": "Finance"
            },
            "operating-series": {
                "term": "Operating Series",
                "shortDefinition": "A dedicated series within a Series LLC structure holding an issuer's project assets and liabilities.",
                "category": "Legal"
            },
            "treasury-series": {
                "term": "Treasury Series",
                "shortDefinition": "A dedicated series within a Series LLC structure that holds un-issued or repurchased tokens.",
                "category": "Legal"
            },
            "crossconversion-series": {
                "term": "CrossConversion Series",
                "shortDefinition": "A dedicated series that facilitates conversion between on-chain tokens and bankable ISIN format.",
                "category": "Legal"
            },
            "operational-trust": {
                "term": "Operational Trust",
                "shortDefinition": "A trust structure used to hold and manage operational assets on behalf of investors.",
                "category": "Legal"
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
