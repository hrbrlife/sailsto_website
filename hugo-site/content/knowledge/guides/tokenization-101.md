---
title: "Tokenization 101"
type: "guide"
description: "What tokenization is, why it matters, and how Sails.to's CrossSecurities architecture creates hybrid on-chain + bankable securities that actually work in."
ogImage: "/og-image.png"
keywords: ["tokenization", "security tokens", "CrossSecurities", "SPL-2022", "digital securities", "blockchain", "Solana", "compliance"]
stylesheets:
  - "/css/main.css"
  - "/css/pages/glossary.css"
  - "/css/pages/guides.css"
guideMeta: "The complete guide to tokenized securities—what they are, why they exist, and how they will remake capital markets"
draft: false
---
<nav class="guide-nav">
            <h4>In This Guide</h4>
            <ul>
                <li><a href="#what-is-tokenization">What Is Tokenization?</a></li>
                <li><a href="#why-tokenize">Why Tokenize?</a></li>
                <li><a href="#how-sailsto-tokenizes">How Sails.to Tokenizes</a></li>
                <li><a href="#token-lifecycle">The Token Lifecycle</a></li>
                <li><a href="#asset-types">Asset Types</a></li>
                <li><a href="#getting-started">Getting Started</a></li>
            </ul>
        </nav>
        <section id="what-is-tokenization" class="guide-section">
            <h2>What Is Tokenization?</h2>
            <p>Tokenization is the process of representing ownership of a real-world asset as a digital token on a blockchain. A <span class="glossary-term" data-term="security-token">security token</span> is not a cryptocurrency—it is a regulated financial instrument that happens to live on a distributed ledger instead of in a spreadsheet at a transfer agent's office.</p>
            <p>Think of it this way: a traditional stock certificate proves you own shares. A security token does exactly the same thing—except the certificate is a programmable, instantly transferable, compliance-enforcing piece of code running on <span class="glossary-term" data-term="solana">Solana</span>.</p>
            <p>Every rule that governs the security—who can hold it, when it can transfer, how dividends are paid—is encoded directly into the token. Compliance is not a department. It is a feature of the asset itself.</p>
            <div class="highlight-box">
                <p><strong>The fundamental insight:</strong> Securities have always been information. Tokenization simply moves that information to a better database—one that is programmable, auditable, and operates 24/7 without intermediaries extracting rent at every step.</p>
            </div>
        </section>
        <section id="why-tokenize" class="guide-section">
            <h2>Why Tokenize?</h2>
            <p>Traditional securities issuance is a monument to friction. Every step—from formation to distribution to secondary trading—involves intermediaries, paper, delays, and fees that exist because the infrastructure was designed in the 1970s.</p>
            <h3>The Problems with Traditional Issuance</h3>
            <ul>
                <li><strong>Time:</strong> A traditional private placement takes 3–6 months. Legal, compliance, transfer agent setup, subscription processing—all sequential, all manual.</li>
                <li><strong>Cost:</strong> Legal fees, transfer agent fees, custody fees, distribution processing fees. A small offering can lose 5–10% of proceeds to infrastructure.</li>
                <li><strong>Illiquidity:</strong> Once you buy into a private fund, your capital is locked. No secondary market. No price discovery. No exit except redemption—if it's even offered.</li>
                <li><strong>Geographic barriers:</strong> Serving international investors means separate legal opinions, separate custodians, separate compliance frameworks for every jurisdiction.</li>
                <li><strong>Manual distributions:</strong> Paying dividends means ACH files, wire instructions, tax withholding calculations, and reconciliation—all by hand.</li>
            </ul>
            <h3>What Tokenization Solves</h3>
            <ul>
                <li><strong>Instant settlement:</strong> Token transfers settle in seconds, not T+2 days.</li>
                <li><strong>Automated compliance:</strong> Transfer restrictions enforced by <span class="glossary-term" data-term="smart-contract">smart contracts</span>, not compliance officers reviewing every trade.</li>
                <li><strong>Programmable distributions:</strong> Revenue enters the smart contract; distributions flow automatically to every token holder, pro-rata, in stablecoin.</li>
                <li><strong>Global reach:</strong> One token, one standard, accessible to verified investors worldwide.</li>
                <li><strong>Fractional ownership:</strong> Tokens are divisible. A $50M real estate fund can accept a $150K investor without special accommodation.</li>
                <li><strong>Real-time cap table:</strong> The blockchain <em>is</em> the cap table. Always current. Always auditable. No reconciliation needed.</li>
            </ul>
            <div class="info-box">
                <h4>Not Just Cost Savings</h4>
                <p>Tokenization does not merely reduce fees—it enables entirely new capital structures. Assets that were never economically viable to securitize (revenue streams, intellectual property, infrastructure projects) become possible when the cost of issuance drops by 90%.</p>
            </div>
        </section>
        <section id="how-sailsto-tokenizes" class="guide-section">
            <h2>How Sails.to Tokenizes</h2>
            <p>Most tokenization platforms make you choose: on-chain <em>or</em> traditional. Sails.to refuses that choice. Our <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> architecture delivers both simultaneously—a hybrid instrument that is natively on-chain <em>and</em> bankable through traditional infrastructure.</p>
            <h3>The CrossSecurities Architecture</h3>
            <p>Every Sails.to security token is deployed through our <code>sails_securities</code> program on Solana, built on the SPL Token-2022 standard with compliance hooks. But here is what makes it different:</p>
            <ul>
                <li><strong>On-Chain Form:</strong> Tokens live in your <span class="glossary-term" data-term="solana">Solana</span> wallet. Self-custody. Instant transfers to other verified investors. Programmable distributions in stablecoin.</li>
                <li><strong>Bankable Form:</strong> Through <span class="glossary-term" data-term="crossconversion">CrossConversion</span>, the same tokens can be locked on-chain and represented as <span class="glossary-term" data-term="isin">ISIN</span>-identified securities in <span class="glossary-term" data-term="clearstream">Clearstream</span>—the world's largest international securities depository.</li>
            </ul>
            <p>Investors choose their form. They can switch between forms at any time. The asset is identical. Only the custody model changes.</p>
            <h3>The Legal Wrapper</h3>
            <p>Every offering on Sails.to is issued through a <span class="glossary-term" data-term="wyoming-dao-llc">Wyoming DAO LLC</span> with a <span class="glossary-term" data-term="series-llc">Series LLC</span> structure. Each offering is its own series—legally isolated from every other offering on the platform.</p>
            <ul>
                <li>Series A has legal trouble? Series B is untouched.</li>
                <li>One registered agent. One annual filing. Unlimited series.</li>
                <li>Smart contracts recognized as part of the operating agreement under Wyoming law.</li>
            </ul>
            <h3>SPL Token-2022 with Compliance Hooks</h3>
            <p>Our tokens use Solana's SPL Token-2022 standard, which supports transfer hooks—custom logic that executes on every token transfer. Our hooks enforce:</p>
            <ul>
                <li><strong>KYC verification:</strong> Both sender and receiver must hold a valid <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT.</li>
                <li><strong>Accreditation checks:</strong> Investor classification matches the offering's regulatory exemption.</li>
                <li><strong>Jurisdiction whitelisting:</strong> Only allowed jurisdictions can hold the token.</li>
                <li><strong>Lock-up enforcement:</strong> Tokens cannot transfer during the lock-up period.</li>
                <li><strong>Investor count limits:</strong> <span class="glossary-term" data-term="reg-d">Reg D 506(b)</span> offerings enforce the 35 non-accredited investor limit.</li>
            </ul>
            <div class="highlight-box">
                <p><strong>Compliance is not optional—it is physical.</strong> An unauthorized transfer does not fail a compliance check after the fact. It cannot execute at all. The smart contract rejects it at the instruction level. This is not a policy. It is mathematics.</p>
            </div>
        </section>
        <section id="token-lifecycle" class="guide-section">
            <h2>The Token Lifecycle</h2>
            <p>Every Sails.to security token follows a defined lifecycle, managed by the <code>sails_securities</code> Solana program. Here is the complete journey from offering creation to conversion:</p>
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>init_offering</h4>
                    <p>The issuer initializes the offering on-chain. This creates a Program Derived Address (PDA) linking the token to its Series LLC, sets the maximum supply, nominal value per token, and configures the compliance parameters—allowed jurisdictions, minimum investment, lock-up period, and regulatory exemption type.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>mint_security_token</h4>
                    <p>When an investor subscribes and funds are received, tokens are minted directly to their wallet. This instruction verifies the investor holds a valid KYC Credential NFT, checks their accreditation tier matches the offering requirements, and confirms their jurisdiction is whitelisted. No valid credential, no mint. Period.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>distribute</h4>
                    <p>Revenue enters the distribution smart contract. The waterfall executes automatically: senior debt holders first, then pro-rata investor distributions based on token holdings, then platform fees, then excess to treasury. Every token holder receives their share in stablecoin—no ACH, no wire delays, no reconciliation.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4>transfer_with_compliance</h4>
                    <p>Secondary transfers between investors. The transfer hook checks both wallets for valid KYC, verifies accreditation, confirms jurisdiction eligibility, and enforces lock-up periods. If every check passes, the transfer settles instantly. If any check fails, the transaction is rejected on-chain.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h4>burn_for_crossconversion</h4>
                    <p>When an investor wants to move from on-chain to bankable form, tokens are locked in the CrossConversion lockbox PDA. This emits a <code>CrossConversionRequested</code> event that triggers the off-chain process: ISIN issuance and Clearstream account crediting. The tokens are not destroyed—they are locked, maintaining the 1:1 invariant between locked tokens and outstanding ISINs.</p>
                </div>
            </div>
            <div class="info-box">
                <h4>Additional Lifecycle Instructions</h4>
                <p><strong>freeze_account:</strong> Regulatory freeze (requires Security-level Admin NFT). <strong>force_transfer:</strong> Court-ordered transfer (requires 3-of-5 keyholder threshold signing). <strong>close_offering:</strong> Final redemption, burn remaining tokens, wind down the series.</p>
            </div>
        </section>
        <section id="asset-types" class="guide-section">
            <h2>Asset Types</h2>
            <p>Tokenization is not limited to one asset class. Any asset that can be structured as a security can be tokenized on Sails.to. Here are the primary categories:</p>
            <h3>Equity</h3>
            <p>Ownership stakes in companies, funds, or projects. Tokens represent membership interests in the Series LLC, carrying pro-rata economic and governance rights. Ideal for startups, growth companies, and venture-style investments.</p>
            <h3>Debt</h3>
            <p>Fixed-income instruments—bonds, notes, revenue-sharing agreements. Tokens carry a stated coupon or interest rate with automated distribution payments. The smart contract enforces the payment waterfall: senior tranches first, subordinated after.</p>
            <h3>Fund Shares</h3>
            <p>Interests in investment funds—real estate funds, venture funds, hedge funds. Tokenization solves the historic illiquidity problem of alternative fund shares. NAV calculations can be published on-chain. Distributions flow automatically.</p>
            <h3>Real Estate</h3>
            <p>Direct property ownership or real estate fund interests. Each property or portfolio is its own Series LLC, providing clean legal isolation. Rental income distributions are automated. Fractional ownership makes institutional-quality real estate accessible at $150K minimums.</p>
            <div class="requirement-box">
                <h4>Who Can Tokenize on Sails.to?</h4>
                <ul>
                    <li>Registered legal entity (any jurisdiction)</li>
                    <li>Asset with clear ownership rights and legal title</li>
                    <li>Minimum offering size: $500,000</li>
                    <li>Commitment to regulatory compliance (<span class="glossary-term" data-term="reg-d">Reg D</span> / <span class="glossary-term" data-term="reg-s">Reg S</span> framework)</li>
                    <li>Willingness to operate within the Wyoming DAO LLC structure</li>
                </ul>
            </div>
            <h3>Traditional vs. Tokenized Issuance</h3>
            <table class="comparison-table">
                <tr>
                    <th>Aspect</th>
                    <th>Traditional Securities</th>
                    <th>Sails.to Tokenized Securities</th>
                </tr>
                <tr>
                    <td>Issuance timeline</td>
                    <td>3–6 months</td>
                    <td>Weeks</td>
                </tr>
                <tr>
                    <td>Transfer settlement</td>
                    <td>T+2 days</td>
                    <td>Seconds</td>
                </tr>
                <tr>
                    <td>Cap table management</td>
                    <td>Manual spreadsheets / transfer agent</td>
                    <td>Real-time on-chain</td>
                </tr>
                <tr>
                    <td>Distributions</td>
                    <td>Manual ACH / wire processing</td>
                    <td>Automated stablecoin waterfall</td>
                </tr>
                <tr>
                    <td>Compliance enforcement</td>
                    <td>Manual review per trade</td>
                    <td>Smart contract transfer hooks</td>
                </tr>
                <tr>
                    <td>Custody options</td>
                    <td>Custodian only</td>
                    <td>Self-custody or Clearstream (ISIN)</td>
                </tr>
                <tr>
                    <td>Geographic reach</td>
                    <td>Per-jurisdiction setup</td>
                    <td>Global with single compliance layer</td>
                </tr>
                <tr>
                    <td>Secondary liquidity</td>
                    <td>Rare / non-existent for privates</td>
                    <td>Compliant peer-to-peer OTC</td>
                </tr>
            </table>
        </section>
        <section id="getting-started" class="guide-section">
            <h2>Getting Started</h2>
            <p>Tokenization is not speculative. It is not experimental. It is the inevitable endpoint of a financial system that has been digitizing for fifty years. Sails.to is where the digitization becomes complete.</p>
            <h3>For Issuers</h3>
            <p>If you have an asset worth tokenizing, start here:</p>
            <ol>
                <li>Review our <a href="/knowledge/guides/getting-started/">Getting Started guide</a> for issuer onboarding</li>
                <li>Understand the <a href="/knowledge/guides/wyoming-dao-explained/">Wyoming DAO LLC structure</a> that will house your offering</li>
                <li><a href="/company/contact/">Contact our team</a> to discuss your specific asset and structure</li>
            </ol>
            <h3>For Investors</h3>
            <p>If you want to access tokenized securities:</p>
            <ol>
                <li>Review the <a href="/knowledge/guides/investor-eligibility/">Investor Eligibility Guide</a> to confirm your qualification</li>
                <li>Understand the <a href="/knowledge/guides/isin-conversion/">ISIN Conversion process</a> if you prefer bankable form</li>
                <li><a href="/signup/?type=investor">Create your investor account</a> to begin verification</li>
            </ol>
        </section>
        <div class="cta-box">
            <h3>Ready to tokenize?</h3>
            <p>The infrastructure is built. The legal framework is proven. The only question left is what you will build on it.</p>
            <a href="/signup/" class="btn">Get Started</a>
        </div>
    </div>
