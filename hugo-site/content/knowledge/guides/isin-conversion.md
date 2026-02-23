---
title: "ISIN Conversion Guide"
type: "guide"
description: "How CrossConversion bridges on-chain tokens and bankable ISIN securities through Clearstream—step by step, with the 1:1 invariant, reconciliation, fees."
ogImage: "/og-image.png"
keywords: ["ISIN", "CrossConversion", "Clearstream", "bankable securities", "on-chain", "custody", "conversion", "settlement"]
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/guides.css"
guideMeta: "How to move between on-chain tokens and bankable ISIN securities—and why the bridge between these two worlds changes everything"
draft: false
---
<nav class="guide-nav">
            <h4>In This Guide</h4>
            <ul>
                <li><a href="#what-is-isin">What Is an ISIN?</a></li>
                <li><a href="#crossconversion-process">The CrossConversion Process</a></li>
                <li><a href="#cross-to-bankable">Cross to Bankable</a></li>
                <li><a href="#cross-to-onchain">Cross to On-Chain</a></li>
                <li><a href="#one-to-one-invariant">The 1:1 Invariant</a></li>
                <li><a href="#reconciliation-trust">Reconciliation & Trust</a></li>
                <li><a href="#fees-timeline">Fees & Timeline</a></li>
                <li><a href="#when-to-convert">When to Convert</a></li>
            </ul>
        </nav>
        <section id="what-is-isin" class="guide-section">
            <h2>What Is an ISIN?</h2>
            <p>An <span class="glossary-term" data-term="isin">ISIN</span> (International Securities Identification Number) is a 12-character alphanumeric code that uniquely identifies a financial instrument globally. It is the lingua franca of traditional finance—every stock, bond, and fund share traded through conventional infrastructure has one.</p>
            <p>When your bank, your wealth manager, or your pension fund says they "can't hold crypto," what they really mean is: they can only hold securities that have an ISIN and are custodied in a recognized depository. Their systems, their compliance frameworks, their reporting infrastructure—all of it is built around ISINs.</p>
            <p><span class="glossary-term" data-term="crossconversion">CrossConversion</span> gives your Sails.to <span class="glossary-term" data-term="security-token">security tokens</span> an ISIN. It makes them visible to every Bloomberg terminal, every custodian, every settlement system on the planet. The token does not change. The asset does not change. Only its form changes—from on-chain to bankable.</p>
            <div class="highlight-box">
                <p><strong>This is the bridge.</strong> On one side: self-custody, programmable compliance, instant settlement on <span class="glossary-term" data-term="solana">Solana</span>. On the other side: <span class="glossary-term" data-term="clearstream">Clearstream</span>, institutional custody, SWIFT settlement, and an ISIN that every traditional financial system on Earth can recognize. CrossConversion lets you walk across this bridge in either direction, any time you choose.</p>
            </div>
        </section>
        <section id="crossconversion-process" class="guide-section">
            <h2>The CrossConversion Process</h2>
            <p>CrossConversion is the mechanism that makes Sails.to <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> truly hybrid. It is not a sale. It is not a swap. It is a change of form—the same security, moving between two custody models, with absolute supply integrity maintained at every step.</p>
            <p>The process is managed by the <code>sails_crossconversion</code> Solana program (on-chain) and the CrossConversion Operator Service (off-chain), with every conversion authenticated by an appointed Trustee holding a Trustee NFT.</p>
            <h3>Two Directions</h3>
            <ul>
                <li><strong>Cross to Bankable:</strong> Lock your on-chain tokens → receive ISIN-identified securities in your Clearstream account</li>
                <li><strong>Cross to On-Chain:</strong> Cancel your Clearstream position → unlock your tokens back to your Solana wallet</li>
            </ul>
            <p>Both directions follow the same principle: tokens are never created or destroyed during conversion. They are locked or unlocked. The total supply—on-chain circulating plus locked—never changes.</p>
        </section>
        <section id="cross-to-bankable" class="guide-section">
            <h2>Cross to Bankable</h2>
            <p>You hold tokens in your Solana wallet and want institutional custody with an ISIN. Here is exactly what happens:</p>
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Initiate Conversion Request</h4>
                    <p>Through your Investor Self-Service dashboard, you request a Cross to Bankable conversion, specifying the offering and the number of tokens to convert. Your <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT is verified automatically.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Token Lock</h4>
                    <p>The <code>lock_tokens</code> instruction executes on Solana. Your tokens are transferred from your wallet to the CrossConversion Lockbox PDA—a program-controlled account that no individual can access. A <code>CrossConversionRequested</code> event is emitted on-chain.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Trustee Authentication</h4>
                    <p>The appointed Trustee reviews the conversion request and authenticates it by signing with their Trustee NFT. No conversion proceeds without Trustee authentication—this is a regulatory requirement, not an optional feature.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4>ISIN Issuance</h4>
                    <p>The CrossConversion Operator Service initiates the ISIN issuance workflow with Clearstream. If the offering already has an ISIN assigned, securities are credited to your Clearstream account under that existing ISIN. If this is the first conversion for the offering, ISIN registration is completed first.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h4>Clearstream Credit</h4>
                    <p>The corresponding number of ISIN-identified securities are credited to your Clearstream account (or your custodian's account at Clearstream). Settlement is confirmed via SWIFT messaging. Proof of issuance is stored on-chain in the Lockbox state.</p>
                </div>
            </div>
            <div class="info-box">
                <h4>After Conversion</h4>
                <p>Your securities now live in Clearstream. They appear in your custody statement. They have an ISIN. Your wealth manager can see them. Your tax reporting software recognizes them. You receive the same distributions—but through traditional payment channels instead of stablecoin. The underlying asset is identical.</p>
            </div>
        </section>
        <section id="cross-to-onchain" class="guide-section">
            <h2>Cross to On-Chain</h2>
            <p>You hold ISIN securities in Clearstream and want to return to self-custody on Solana. The process runs in reverse:</p>
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Initiate Reverse Conversion</h4>
                    <p>You request a Cross to On-Chain conversion through your dashboard (or through your custodian), specifying the number of securities to convert back to tokens.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Clearstream Cancellation</h4>
                    <p>The CrossConversion Operator Service initiates cancellation of the corresponding securities position in Clearstream. The securities are debited from your Clearstream account.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Trustee Authentication</h4>
                    <p>The Trustee verifies the Clearstream cancellation is confirmed and authentic. They sign the reverse conversion with their Trustee NFT, providing the <code>clearstream_proof</code> required by the smart contract.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4>Token Unlock</h4>
                    <p>The <code>unlock_tokens</code> instruction executes on Solana. Tokens are released from the CrossConversion Lockbox PDA back to your wallet. Your KYC Credential NFT is re-verified at this point—if your credential has expired, you must re-verify before tokens can be unlocked.</p>
                </div>
            </div>
            <p>You are back to self-custody. Instant transfers. Stablecoin distributions. Direct on-chain governance participation. All the benefits of native token ownership, restored with a single conversion.</p>
        </section>
        <section id="one-to-one-invariant" class="guide-section">
            <h2>The 1:1 Invariant</h2>
            <p>This is the most critical property of the CrossConversion system, and it is absolute:</p>
            <div class="highlight-box">
                <p><strong><code>tokens_locked == isin_outstanding</code></strong></p>
                <p>At any point in time, the number of tokens locked in the CrossConversion Lockbox PDA on Solana must exactly equal the number of ISIN-identified securities outstanding in Clearstream. No exceptions. No tolerance. No rounding.</p>
            </div>
            <p>This invariant guarantees that no securities are created out of thin air. Every ISIN security in Clearstream has a corresponding locked token on Solana. Every locked token has a corresponding ISIN security in Clearstream. The total supply of the offering—circulating tokens plus locked tokens—never changes.</p>
            <h3>How the Invariant Is Enforced</h3>
            <ul>
                <li><strong>Smart contract level:</strong> The <code>lock_tokens</code> instruction atomically increments the lockbox counter. The <code>unlock_tokens</code> instruction atomically decrements it. These are on-chain operations—immutable, auditable, instant.</li>
                <li><strong>Operator level:</strong> The CrossConversion Operator Service does not initiate ISIN issuance until lock is confirmed on-chain. It does not trigger token unlock until Clearstream cancellation is confirmed.</li>
                <li><strong>Trustee level:</strong> The Trustee independently verifies both sides before authenticating any conversion.</li>
                <li><strong>Reconciliation level:</strong> Nightly automated comparison catches any discrepancy (which should never exist but is checked anyway).</li>
            </ul>
            <p>If the invariant ever breaks—if there is even a single-token discrepancy between locked tokens and outstanding ISINs—the system generates a P0 critical alert, and conversions are halted until the Trustee investigates and resolves the discrepancy.</p>
        </section>
        <section id="reconciliation-trust" class="guide-section">
            <h2>Reconciliation & Trust</h2>
            <p>Trust in CrossConversion does not come from promises—it comes from continuous, automated, independently verifiable reconciliation.</p>
            <h3>Nightly Reconciliation</h3>
            <p>Every night, the Reconciliation Engine performs a full comparison:</p>
            <ol>
                <li>Pull the on-chain lockbox state for every offering (tokens locked, lockbox PDA balance)</li>
                <li>Pull the Clearstream daily position report (ISIN securities outstanding per offering)</li>
                <li>Compare the two datasets at the individual offering level</li>
                <li>Generate a reconciliation report with match/mismatch status</li>
                <li>Trustee reviews and signs the report with their Trustee NFT</li>
                <li>Signed reconciliation hash is stored on-chain via the <code>reconcile</code> instruction</li>
            </ol>
            <h3>The Trustee Role</h3>
            <p>The Trustee is not a Sails.to employee. The Trustee is an appointed fiduciary—typically a regulated trust company—who holds a Trustee NFT issued by the Platform Operator. Their responsibilities:</p>
            <ul>
                <li>Authenticate every CrossConversion (both directions)</li>
                <li>Review and sign nightly reconciliation reports</li>
                <li>Investigate and resolve any discrepancies</li>
                <li>Authenticate distributions and waterfall executions</li>
                <li>Exercise emergency freeze capability if warranted</li>
            </ul>
            <div class="info-box">
                <h4>Verifiable by Anyone</h4>
                <p>The on-chain lockbox state is publicly readable on Solana. Anyone can query the <code>CrossConversionLockbox</code> PDA for any offering and see exactly how many tokens are locked. The Clearstream side is verified by the Trustee, and reconciliation hashes are stored on-chain. This is not "trust us"—this is "verify it yourself."</p>
            </div>
        </section>
        <section id="fees-timeline" class="guide-section">
            <h2>Fees & Timeline</h2>
            <h3>Conversion Fee</h3>
            <p>CrossConversion carries a fee of approximately <strong>0.75% of nominal value</strong> per conversion. This covers:</p>
            <ul>
                <li>ISIN registration and maintenance (Clearstream fees)</li>
                <li>Trustee authentication services</li>
                <li>Reconciliation engine operations</li>
                <li>Settlement processing and SWIFT messaging</li>
            </ul>
            <p>The fee is charged at the time of conversion and deducted from the converted amount. It applies in both directions—Cross to Bankable and Cross to On-Chain.</p>
            <h3>Processing Timeline</h3>
            <table class="comparison-table">
                <tr>
                    <th>Step</th>
                    <th>Cross to Bankable</th>
                    <th>Cross to On-Chain</th>
                </tr>
                <tr>
                    <td>Token lock / unlock</td>
                    <td>Seconds (on-chain)</td>
                    <td>Seconds (on-chain)</td>
                </tr>
                <tr>
                    <td>Trustee authentication</td>
                    <td>Same business day</td>
                    <td>Same business day</td>
                </tr>
                <tr>
                    <td>Clearstream processing</td>
                    <td>2–4 business days</td>
                    <td>2–4 business days</td>
                </tr>
                <tr>
                    <td><strong>Total end-to-end</strong></td>
                    <td><strong>3–5 business days</strong></td>
                    <td><strong>3–5 business days</strong></td>
                </tr>
            </table>
            <p>The on-chain portion is instant. The timeline is driven entirely by traditional finance infrastructure—Clearstream settlement cycles and Trustee review schedules. As these systems modernize, conversion times will compress.</p>
            <div class="requirement-box">
                <h4>First Conversion for an Offering</h4>
                <ul>
                    <li>If an offering does not yet have an ISIN, the first Cross to Bankable conversion triggers ISIN registration</li>
                    <li>ISIN registration takes approximately 1 week and costs ~$4,000 (one-time)</li>
                    <li>Subsequent conversions for the same offering use the existing ISIN and process in the standard 3–5 business day window</li>
                </ul>
            </div>
        </section>
        <section id="when-to-convert" class="guide-section">
            <h2>When to Convert</h2>
            <p>CrossConversion is optional. Many investors will hold tokens on-chain for the entire life of their investment. Others will convert immediately. The right choice depends on your situation:</p>
            <h3>Convert to Bankable When:</h3>
            <ul>
                <li><strong>Mandate restrictions:</strong> Your fund, family office, or pension plan requires all holdings to be in recognized custodial form with ISINs. Many institutional mandates prohibit direct crypto custody—CrossConversion solves this without changing the underlying asset.</li>
                <li><strong>Reporting requirements:</strong> Your compliance or tax reporting infrastructure expects Clearstream statements and ISIN-based positions. Converting makes the security visible to your existing systems.</li>
                <li><strong>Buyer settlement preference:</strong> You are selling your position to a buyer who prefers or requires traditional settlement (DvP through Clearstream) rather than on-chain transfer.</li>
                <li><strong>Custodian integration:</strong> Your wealth manager or private bank can only hold ISIN-identified securities. Converting lets them manage it alongside your traditional portfolio.</li>
            </ul>
            <h3>Stay On-Chain When:</h3>
            <ul>
                <li><strong>Self-custody preference:</strong> You want direct control of your assets in your own wallet—no intermediary, no custodian, no counterparty risk.</li>
                <li><strong>Instant transferability:</strong> You want the ability to transfer tokens to another verified investor in seconds, not days.</li>
                <li><strong>Stablecoin distributions:</strong> You prefer receiving distributions directly in stablecoin to your wallet rather than through traditional payment channels.</li>
                <li><strong>Governance participation:</strong> On-chain token holders can participate directly in DAO governance votes. Bankable form holders vote through the Trustee.</li>
                <li><strong>Cost:</strong> No conversion fee. No Clearstream custody fees. Just Solana transaction fees (fractions of a cent).</li>
            </ul>
            <div class="highlight-box">
                <p><strong>You are not locked in.</strong> Convert to bankable today, convert back to on-chain next month. The bridge runs in both directions. Your asset, your choice, your timing. CrossConversion exists so that the form of your security never limits what you can do with it.</p>
            </div>
        </section>
        <div class="cta-box">
            <h3>Ready to explore CrossConversion?</h3>
            <p>Create your account and experience the bridge between on-chain and bankable securities.</p>
            <a href="/signup/?type=investor" class="btn">Get Started</a>
        </div>
    </div>
