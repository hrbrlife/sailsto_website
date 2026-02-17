---
title: "Investor Eligibility Guide"
description: "Who can invest on Sails.to—investor classifications, the 10-step KYC verification process, regulatory exemptions, geographic eligibility."
ogImage: "/og-image.png"
keywords: ["investor eligibility", "accredited investor", "KYC", "verification", "Reg D", "Reg S", "qualified purchaser", "compliance"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/guides.css"
draft: false
---

<header class="guide-header">
    <div class="container">
        <a href="/knowledge/" class="back-link">← Back to Knowledge Base</a>
        <span class="guide-badge">Guide</span>
        <h1 class="guide-title">Investor Eligibility Guide</h1>
        <p class="guide-meta">Everything you need to know about who can invest, how verification works, and what the system checks before a single token touches your wallet</p>
    </div>
</header>
<main class="guide-content">
    <div class="guide-container">
        <nav class="guide-nav">
            <h4>In This Guide</h4>
            <ul>
                <li><a href="#who-can-invest">Who Can Invest?</a></li>
                <li><a href="#investor-classifications">Investor Classifications</a></li>
                <li><a href="#verification-process">The Verification Process</a></li>
                <li><a href="#regulatory-exemptions">Regulatory Exemptions</a></li>
                <li><a href="#geographic-eligibility">Geographic Eligibility</a></li>
                <li><a href="#minimum-requirements">Minimum Requirements</a></li>
            </ul>
        </nav>
        <section id="who-can-invest" class="guide-section">
            <h2>Who Can Invest?</h2>
            <p>Sails.to offerings are private placements—regulated securities sold under specific exemptions from public registration. This means not everyone can invest. There are rules, and these rules are not suggestions. They are federal law.</p>
            <p>The <span class="glossary-term" data-term="security-token">security tokens</span> on our platform are offered under <span class="glossary-term" data-term="reg-d">Reg D</span> (US investors) and <span class="glossary-term" data-term="reg-s">Reg S</span> (non-US investors) exemptions. Your eligibility depends on three factors:</p>
            <ul>
                <li><strong>Your investor classification</strong> — Are you accredited, professional, or institutional?</li>
                <li><strong>Your jurisdiction</strong> — Where do you reside and what regulations apply?</li>
                <li><strong>Your verification status</strong> — Have you completed our KYC process and received a credential?</li>
            </ul>
            <p>No credential, no tokens. This is enforced at the smart contract level—the <code>mint_security_token</code> instruction on <span class="glossary-term" data-term="solana">Solana</span> physically cannot execute without a valid <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT in your wallet.</p>
            <div class="highlight-box">
                <p><strong>Why this matters:</strong> Every other platform asks you to check a box saying you're accredited. We verify it, encode it on-chain, and make it impossible for non-verified wallets to hold tokens. Compliance is not a checkbox—it is cryptographic proof.</p>
            </div>
        </section>
        <section id="investor-classifications" class="guide-section">
            <h2>Investor Classifications</h2>
            <p>Our KYC Credential NFT encodes your investor classification directly on-chain. No personally identifiable information—just your verified status, jurisdiction hash, and regulatory eligibility. Here are the classifications:</p>
            <h3>Accredited Investor (US)</h3>
            <p>The primary classification for US-based investors under SEC rules:</p>
            <ul>
                <li><strong>Income test:</strong> Individual income exceeding $200,000 (or $300,000 jointly with spouse) in each of the two most recent years, with reasonable expectation of the same in the current year</li>
                <li><strong>Net worth test:</strong> Individual or joint net worth exceeding $1,000,000, excluding the value of the primary residence</li>
                <li><strong>Professional certification:</strong> Holder of Series 7, Series 65, or Series 82 license in good standing</li>
                <li><strong>Entity:</strong> Trust with assets exceeding $5M, or entity owned entirely by accredited investors</li>
            </ul>
            <h3>Professional Investor (International)</h3>
            <p>For non-US investors, classification follows their home jurisdiction's equivalent standards. Common frameworks include:</p>
            <ul>
                <li><strong>MiFID II Professional Client</strong> (EU/EEA) — Meets at least two of: 10+ transactions per quarter, portfolio >€500K, financial sector experience >1 year</li>
                <li><strong>Qualified Investor</strong> (Switzerland, FINMA)</li>
                <li><strong>Sophisticated Investor</strong> (UK FCA, Australia ASIC)</li>
                <li><strong>Professional Investor</strong> (Hong Kong SFC, Singapore MAS)</li>
            </ul>
            <h3>Qualified Purchaser</h3>
            <p>A higher tier under US law (Investment Company Act Section 2(a)(51)): individuals with $5M+ in investments, or entities with $25M+ in investments. Required for certain offering structures.</p>
            <h3>Institutional Investor</h3>
            <p>Banks, insurance companies, registered investment companies, pension funds, and entities with $100M+ in assets. Subject to Enhanced Due Diligence (EDD) but benefit from streamlined verification.</p>
            <div class="info-box">
                <h4>On-Chain Credential, Not On-Chain Identity</h4>
                <p>Your KYC Credential NFT stores <strong>zero</strong> personal information on the blockchain. It contains: <code>investor_class</code> (enum), <code>jurisdiction_hash</code> (SHA-256 of ISO country code), <code>reg_exemption</code> (which regulatory exemption you qualify under), <code>verification_level</code> (Basic, Enhanced, or Institutional EDD), expiration date, and AML/PEP clearance flags. Your name, address, and documents are encrypted in secure off-chain storage with 7-year regulatory retention.</p>
            </div>
        </section>
        <section id="verification-process" class="guide-section">
            <h2>The Verification Process</h2>
            <p>Our KYC workflow is a 10-step process that takes you from anonymous visitor to verified, on-chain-credentialed investor. Every step is designed, every check is real, and the output is a cryptographic credential that unlocks the entire platform.</p>
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Terms Acceptance</h4>
                    <p>You review and accept the platform terms of service, privacy policy, and investor acknowledgements. This is not a click-through—the system requires you to scroll the full document before the acceptance checkbox activates.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Email Verification</h4>
                    <p>A one-time password (OTP) is sent to your email address. You enter it to confirm ownership. This becomes your primary communication channel for offering updates, distribution notifications, and regulatory notices.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Phone Verification</h4>
                    <p>A second OTP sent via SMS to verify your phone number. Two-factor identity anchoring—email and phone—before we collect any sensitive documents.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4>Document Upload</h4>
                    <p>Government-issued photo ID (passport, national ID, or driver's license) plus proof of address (utility bill or bank statement, less than 3 months old). Documents are encrypted at upload and stored in compliance with data protection regulations.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h4>Face Capture</h4>
                    <p>A selfie and liveness check. The system verifies you are a real person (not a photo of a photo) and that your face matches the ID document you uploaded. Anti-spoofing detection runs in real time.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">6</div>
                <div class="step-content">
                    <h4>AI Processing</h4>
                    <p>Automated verification: OCR extracts document data, facial recognition matches your selfie to your ID, document authenticity algorithms check for tampering, and data is cross-referenced against the information you provided. Most legitimate submissions pass in under 60 seconds.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">7</div>
                <div class="step-content">
                    <h4>Risk Assessment</h4>
                    <p>Your profile is screened against sanctions lists (OFAC, EU, UN), Politically Exposed Persons (PEP) databases, and adverse media. Jurisdiction risk is evaluated. A risk level is assigned: Lowest, Low, Medium, High, or Prohibited. High and Prohibited trigger enhanced review or rejection.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">8</div>
                <div class="step-content">
                    <h4>Accreditation Verification</h4>
                    <p>For US investors under <span class="glossary-term" data-term="reg-d">Reg D 506(c)</span>: income verification via tax returns or CPA/attorney letter, or net worth verification via financial statements. For international investors: documentation of professional/qualified investor status per home jurisdiction requirements.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">9</div>
                <div class="step-content">
                    <h4>Respondent Review</h4>
                    <p>A human compliance officer reviews the complete file. AI handles the heavy lifting, but a trained professional makes the final call on every investor. Edge cases, risk flags, and unusual patterns get expert judgment—not just an algorithm.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">10</div>
                <div class="step-content">
                    <h4>KYC Credential NFT Mint</h4>
                    <p>Upon approval, a KYC Credential NFT is minted to your Solana wallet. This NFT is your passport to every offering on the platform. It contains your investor classification, jurisdiction hash, regulatory exemption eligibility, verification level, AML/PEP clearance flags, issuance date, and expiration date. No personal data. Just proof.</p>
                </div>
            </div>
            <div class="requirement-box">
                <h4>KYC Credential NFT Metadata (On-Chain)</h4>
                <ul>
                    <li><strong>investor_class:</strong> Accredited | Professional | QualifiedPurchaser | Retail</li>
                    <li><strong>jurisdiction_hash:</strong> SHA-256 of ISO country code (anonymized)</li>
                    <li><strong>reg_exemption:</strong> RegD506b | RegD506c | RegS | RegA | RegCF</li>
                    <li><strong>verification_level:</strong> Basic | Enhanced | InstitutionalEDD</li>
                    <li><strong>issued_by:</strong> Public key of the licensed KYC provider</li>
                    <li><strong>aml_clear / pep_clear:</strong> Boolean clearance flags</li>
                    <li><strong>expires_at:</strong> Credential expiration timestamp</li>
                </ul>
            </div>
        </section>
        <section id="regulatory-exemptions" class="guide-section">
            <h2>Regulatory Exemptions</h2>
            <p>Sails.to offerings are structured under specific SEC exemptions from registration. The exemption determines who can invest, how the offering can be marketed, and what verification is required.</p>
            <h3>Reg D 506(b)</h3>
            <ul>
                <li><strong>Investors:</strong> Unlimited <span class="glossary-term" data-term="accredited-investor">accredited investors</span> + up to 35 non-accredited sophisticated investors</li>
                <li><strong>Marketing:</strong> No general solicitation or advertising allowed</li>
                <li><strong>Verification:</strong> Self-certification of accreditation is sufficient (issuer has "reasonable belief")</li>
                <li><strong>Best for:</strong> Offerings with existing investor relationships and networks</li>
            </ul>
            <h3>Reg D 506(c)</h3>
            <ul>
                <li><strong>Investors:</strong> Accredited investors only—no exceptions</li>
                <li><strong>Marketing:</strong> General solicitation and advertising permitted</li>
                <li><strong>Verification:</strong> Issuer must take "reasonable steps" to verify accreditation (income/net worth documentation, CPA letter, attorney letter, or broker-dealer confirmation)</li>
                <li><strong>Best for:</strong> Offerings seeking broad marketing reach; Sails.to's primary exemption</li>
            </ul>
            <h3>Reg S (International)</h3>
            <ul>
                <li><strong>Investors:</strong> Non-US persons only (as defined by SEC)</li>
                <li><strong>Marketing:</strong> Must occur outside the United States</li>
                <li><strong>Restrictions:</strong> No directed selling efforts into the US; distribution compliance period applies</li>
                <li><strong>Best for:</strong> International investor participation alongside a Reg D US tranche</li>
            </ul>
            <div class="info-box">
                <h4>Dual-Exemption Offerings</h4>
                <p>Most Sails.to offerings use a combined <strong>Reg D 506(c) + Reg S</strong> structure. US accredited investors participate under Reg D; international professional investors participate under Reg S. One offering, one token, two regulatory frameworks—handled seamlessly by the compliance hooks in the smart contract.</p>
            </div>
        </section>
        <section id="geographic-eligibility" class="guide-section">
            <h2>Geographic Eligibility</h2>
            <p>Tokenized securities do not eliminate borders—they simply make compliance at those borders programmable. Each offering on Sails.to specifies an allowed jurisdiction whitelist, encoded in the <code>ComplianceConfig</code> PDA on Solana.</p>
            <h3>Generally Eligible Jurisdictions</h3>
            <p>Most offerings accept investors from:</p>
            <ul>
                <li><strong>United States:</strong> Accredited investors under Reg D 506(b) or 506(c)</li>
                <li><strong>European Union / EEA:</strong> Professional investors under MiFID II classification</li>
                <li><strong>United Kingdom:</strong> Sophisticated/professional investors per FCA rules</li>
                <li><strong>Switzerland:</strong> Qualified investors under FINMA framework</li>
                <li><strong>Singapore, Hong Kong, Japan:</strong> Professional/accredited investors per local regulations</li>
                <li><strong>Canada, Australia, New Zealand:</strong> Accredited/sophisticated investors under respective regimes</li>
            </ul>
            <h3>Restricted Jurisdictions</h3>
            <p>Investors from the following jurisdictions are generally excluded from all offerings due to sanctions, regulatory uncertainty, or AML risk:</p>
            <ul>
                <li>OFAC-sanctioned countries (North Korea, Iran, Syria, Cuba, Crimea region)</li>
                <li>FATF high-risk jurisdictions (list updated dynamically)</li>
                <li>Jurisdictions where the issuer has not obtained legal opinion on offering eligibility</li>
            </ul>
            <p>Geographic eligibility is checked at two points: during KYC verification (encoded in the <code>jurisdiction_hash</code> of your Credential NFT) and at token transfer (the transfer hook validates sender and receiver jurisdiction against the offering's whitelist).</p>
        </section>
        <section id="minimum-requirements" class="guide-section">
            <h2>Minimum Requirements</h2>
            <p>Here is the complete checklist for investing on Sails.to:</p>
            <div class="requirement-box">
                <h4>Individual Investor Requirements</h4>
                <ul>
                    <li><strong>Minimum investment:</strong> $150,000 per offering</li>
                    <li><strong>US investors:</strong> Must be an <span class="glossary-term" data-term="accredited-investor">accredited investor</span> (income $200K+ individual / $300K+ joint, or net worth $1M+ excluding primary residence)</li>
                    <li><strong>Non-US investors:</strong> Must qualify as professional or qualified investor under home jurisdiction</li>
                    <li><strong>Valid government-issued photo ID</strong> (passport, national ID, driver's license)</li>
                    <li><strong>Proof of address</strong> (utility bill or bank statement, less than 3 months old)</li>
                    <li><strong>Liveness verification</strong> (selfie matching ID photo)</li>
                    <li><strong>Solana wallet</strong> for on-chain custody (or opt for bankable form via <span class="glossary-term" data-term="crossconversion">CrossConversion</span>)</li>
                    <li><strong>Completed KYC process</strong> with valid Credential NFT in wallet</li>
                </ul>
            </div>
            <div class="requirement-box">
                <h4>Entity Investor Requirements</h4>
                <ul>
                    <li>All individual requirements for authorized representative(s)</li>
                    <li>Entity formation documents</li>
                    <li>Beneficial ownership disclosure (all 25%+ owners)</li>
                    <li>Entity accreditation documentation (assets >$5M for trusts, all owners accredited, or other qualifying criteria)</li>
                    <li>Board resolution or authorized signatory documentation</li>
                </ul>
            </div>
            <p>The $150,000 minimum investment reflects the institutional character of these offerings. Sails.to is not a retail platform—it is infrastructure for serious capital allocation, built for investors who understand that compliance and custody are features, not friction.</p>
        </section>
        <div class="cta-box">
            <h3>Ready to verify?</h3>
            <p>Complete your KYC verification and receive your on-chain investor credential.</p>
            <a href="/signup/?type=investor" class="btn">Begin Verification</a>
        </div>
    </div>
</main>
<script src="/assets/js/glossary.js"></script>
