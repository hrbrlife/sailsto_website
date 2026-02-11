---
title: "Distributions API - Documentation"
description: "The sails_distributions program — waterfall-based revenue distribution, investor claiming, reconciliation with Clearstream, and the API endpoints for managing payouts on Sails.to."
ogImage: "/og-image.png"
keywords: ["distributions", "waterfall", "revenue", "investor payout", "claiming", "reconciliation"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">Distributions API</h1>
    <p class="section-desc">Waterfall-based revenue distribution — from revenue receipt to investor payout, enforced on-chain.</p>
</section>

<section class="features-section">
    <div class="container">
        <h2>Overview</h2>
        <p><span class="glossary-term" data-term="distributions">Distributions</span> on Sails.to are <span class="glossary-term" data-term="waterfall">waterfall</span>-based and enforced <span class="glossary-term" data-term="on-chain">on-chain</span>. The <code>sails_distributions</code> program is a dedicated <a href="/knowledge/glossary/solana/">Solana</a> Anchor program that handles everything from revenue receipt to investor payout. It is separate from the <code>sails_securities</code> token program — distributions are a first-class concern with their own instruction set, account structures, and authorization model.</p>
        <p>The design principle is simple: investors get paid before the platform. Revenue flows through a priority structure defined at offering creation, and every step is recorded on-chain. There are no off-chain side agreements, no manual overrides, no way to redirect funds outside the waterfall without <span class="glossary-term" data-term="trustee">Trustee</span> authentication. The <span class="glossary-term" data-term="paying-agent">Paying Agent</span> executes the waterfall; the Trustee authenticates it; the blockchain enforces it.</p>
        <h2>The Waterfall Model</h2>
        <p>Every offering on Sails.to defines a waterfall — a priority structure that determines the order in which revenue is distributed. The waterfall is configured when the offering is initialized via the <code>init_waterfall</code> instruction and cannot be modified after investors have committed capital.</p>
        <p>The waterfall executes in strict priority order. Each tranche must be fully satisfied before the next tranche receives any funds:</p>
        <table>
            <thead>
                <tr>
                    <th>Priority</th>
                    <th>Tranche</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>1</strong></td>
                    <td>Senior Debt Holders</td>
                    <td>If the offering has a senior debt component, these holders are paid first — fixed interest or coupon payments as defined in the offering terms. This tranche is optional and only present for structured offerings.</td>
                </tr>
                <tr>
                    <td><strong>2</strong></td>
                    <td>Investor Distributions</td>
                    <td>Pro-rata distribution to all <span class="glossary-term" data-term="security-token">security token</span> holders based on their token balance at the epoch snapshot. This is the core payout — every investor receives their proportional share of remaining revenue.</td>
                </tr>
                <tr>
                    <td><strong>3</strong></td>
                    <td>Platform Fee</td>
                    <td>1% <span class="glossary-term" data-term="distribution-fee">distribution fee</span> to the platform. This is taken <em>after</em> investors are paid — the platform never takes its fee before investors receive their distributions.</td>
                </tr>
                <tr>
                    <td><strong>4</strong></td>
                    <td>Excess to <span class="glossary-term" data-term="treasury-series">Treasury Series</span></td>
                    <td>Any remaining revenue after all tranches are satisfied flows to the <span class="glossary-term" data-term="operating-series">Operating Series</span> treasury. This excess can be reinvested, held as reserves, or distributed in future epochs.</td>
                </tr>
            </tbody>
        </table>
        <p>The investor-first design is non-negotiable. The platform fee sits at priority 3 — below investor distributions. If revenue in a given epoch is insufficient to fully satisfy the investor tranche, the platform receives zero fees for that epoch. This alignment of incentives is encoded in the smart contract, not in a terms-of-service document.</p>
        <h2>Program Instructions</h2>
        <p>The <code>sails_distributions</code> program exposes five instructions. Each instruction enforces role-based authorization via the <span class="glossary-term" data-term="nft-hierarchy">NFT</span> hierarchy — you cannot call these instructions without holding the correct role NFT:</p>
        <table>
            <thead>
                <tr>
                    <th>Instruction</th>
                    <th>Parameters</th>
                    <th>Authorization</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>init_waterfall</code></strong></td>
                    <td><code>offering_id, tranches[]</code></td>
                    <td>Issuer NFT + Platform Operator approval</td>
                    <td>Defines the waterfall structure for an offering. Each tranche specifies a priority level, recipient type, and allocation rule (fixed amount, percentage, or pro-rata). Creates the waterfall configuration <span class="glossary-term" data-term="pda">PDA</span>. Must be called before any revenue can be deposited. Immutable after first investor subscription.</td>
                </tr>
                <tr>
                    <td><strong><code>deposit_revenue</code></strong></td>
                    <td><code>offering_id, amount, source</code></td>
                    <td><span class="glossary-term" data-term="paying-agent">Paying Agent</span> NFT</td>
                    <td>Deposits revenue into the offering's distribution escrow from the <span class="glossary-term" data-term="operating-series">Operating Series</span>. The <code>source</code> field records the origin of funds (rental income, interest payment, asset sale, etc.) for audit trail purposes. Revenue accumulates until <code>execute_waterfall</code> is called.</td>
                </tr>
                <tr>
                    <td><strong><code>execute_waterfall</code></strong></td>
                    <td><code>offering_id</code></td>
                    <td>Paying Agent NFT + <span class="glossary-term" data-term="trustee">Trustee</span> authentication</td>
                    <td>Executes the waterfall for the current epoch. Takes a snapshot of all token holder balances, calculates the pro-rata allocation per token, satisfies each tranche in priority order, and creates a <code>DistributionRecord</code> PDA. Emits a <code>DistributionPaid</code> event. Requires dual authorization — the Paying Agent initiates, the Trustee authenticates.</td>
                </tr>
                <tr>
                    <td><strong><code>claim_distribution</code></strong></td>
                    <td><code>offering_id, epoch</code></td>
                    <td>Investor wallet signature</td>
                    <td>Investor pulls their allocation for a specific epoch. Reads the <code>DistributionRecord</code> to determine the <code>amount_per_token</code>, multiplies by the investor's token balance at the epoch snapshot, transfers the funds to the investor's wallet, and sets the investor's bit in the <code>claimed_bitmap</code>. Idempotent — calling twice for the same epoch has no effect.</td>
                </tr>
                <tr>
                    <td><strong><code>reconcile</code></strong></td>
                    <td><code>offering_id, epoch, clearstream_data</code></td>
                    <td>Trustee NFT</td>
                    <td>Cross-checks on-chain distribution records with <span class="glossary-term" data-term="bankable">bankable</span> side data from <span class="glossary-term" data-term="clearstream">Clearstream</span>. The Trustee submits a hash of the Clearstream position report, and the program verifies that the total distributed on-chain matches the total distributed via corporate actions on the bankable side. Any discrepancy is flagged and logged.</td>
                </tr>
            </tbody>
        </table>
        <h3>Authorization Flow</h3>
        <p>The dual-authorization model for <code>execute_waterfall</code> deserves emphasis. This is not a single-signer operation:</p>
        <ol>
            <li><strong>Paying Agent initiates</strong> — The Paying Agent (appointed by the Trustee, holding a Paying Agent role NFT) submits the <code>execute_waterfall</code> instruction with the offering ID.</li>
            <li><strong>Trustee authenticates</strong> — The Trustee (holding a Trustee role NFT) co-signs the transaction. The program verifies both NFTs before executing. For standard distributions, this is a <span class="glossary-term" data-term="threshold-signing">1-of-1 Trustee NFT</span> signature. For large distributions exceeding a configurable threshold, a 2-of-3 keyholder ceremony is required.</li>
            <li><strong>On-chain execution</strong> — The program snapshots token balances, runs the waterfall calculation, creates the <code>DistributionRecord</code>, and emits the <code>DistributionPaid</code> event. Funds are placed in escrow for investor claiming.</li>
        </ol>
        <h2>Distribution Records</h2>
        <p>Every executed waterfall creates a <code>DistributionRecord</code> — a <span class="glossary-term" data-term="pda">Program Derived Address</span> that stores the complete state of a single distribution epoch:</p>
        <pre><code>DistributionRecord PDA
Seeds: ["distribution", offering_id, epoch]
├── offering_id: Pubkey        // The offering this distribution belongs to
├── epoch: u32                 // Sequential distribution number (0, 1, 2, ...)
├── amount_per_token: u64      // Lamports (or smallest unit) per token for this epoch
├── total_distributed: u64     // Total amount allocated across all tranches
├── snapshot_slot: u64         // Solana slot at which token balances were snapped
├── claimed_bitmap: Vec&lt;u8&gt;    // Bit array tracking which investors have claimed
├── created_at: i64            // Timestamp of waterfall execution
├── trustee_signature: Pubkey  // Trustee who authenticated this distribution
└── status: enum { Active, Reconciled, Disputed }</code></pre>
        <h3>The Claimed Bitmap</h3>
        <p>The <code>claimed_bitmap</code> is a compact bit array where each bit corresponds to an investor position index. When an investor calls <code>claim_distribution</code>, the program sets their bit to 1. This design has three advantages:</p>
        <ul>
            <li><strong>Space efficiency:</strong> A single byte tracks 8 investors. An offering with 2,000 investors requires only 250 bytes for the bitmap — far cheaper than creating a separate PDA per investor per epoch.</li>
            <li><strong>Idempotency:</strong> The program checks the bitmap before transferring funds. If the investor's bit is already set, the instruction returns success without transferring anything. Double-claiming is impossible.</li>
            <li><strong>Audit visibility:</strong> Anyone can read the bitmap to see exactly which investors have claimed and which have not. Unclaimed distributions are immediately visible to the Paying Agent and Trustee for follow-up.</li>
        </ul>
        <p>Investor position indices are assigned sequentially when tokens are first minted to a wallet. The mapping from wallet address to position index is stored in the <code>InvestorPosition</code> PDA and does not change — even if the investor transfers all their tokens and later reacquires them, they retain their original index.</p>
        <h2>Claiming Distributions</h2>
        <p>Distributions on Sails.to use a <strong>pull-based</strong> model. The <code>execute_waterfall</code> instruction calculates allocations and records them on-chain, but it does not push funds to investors. Instead, each investor calls <code>claim_distribution</code> to pull their allocation when they are ready.</p>
        <h3>On-Chain Holders</h3>
        <p>For investors holding <span class="glossary-term" data-term="security-token">security tokens</span> directly in their <a href="/knowledge/glossary/solana/">Solana</a> wallet, the claim process is straightforward:</p>
        <ol>
            <li>The investor connects their wallet and calls <code>claim_distribution(offering_id, epoch)</code>.</li>
            <li>The program reads the <code>DistributionRecord</code> for the specified epoch and retrieves the <code>amount_per_token</code> value.</li>
            <li>The program reads the investor's <code>InvestorPosition</code> PDA to determine their token balance at the <code>snapshot_slot</code>.</li>
            <li>The program calculates the payout: <code>amount_per_token × investor_balance</code>.</li>
            <li>The program checks the <code>claimed_bitmap</code> — if the investor's bit is already set, the instruction returns without transferring funds.</li>
            <li>The program transfers the calculated amount from the distribution escrow to the investor's wallet, sets the bitmap bit, and emits a claim event.</li>
        </ol>
        <h3>Bankable / Clearstream Holders</h3>
        <p>Investors who hold their position on the <span class="glossary-term" data-term="bankable">bankable</span> side via <span class="glossary-term" data-term="clearstream">Clearstream</span> (through <span class="glossary-term" data-term="crossconversion">CrossConversion</span>) do not claim distributions on-chain. Instead, distributions to these holders are processed as <strong>corporate actions</strong> through Clearstream's settlement infrastructure:</p>
        <ul>
            <li>When <code>execute_waterfall</code> runs, the program identifies tokens locked in the <span class="glossary-term" data-term="crossconversion-series">CrossConversion</span> lockbox and calculates the distribution amount for those positions.</li>
            <li>The Clearstream adapter service receives the <code>DistributionPaid</code> event and initiates a corporate action (ISO 20022 message) to distribute funds to the corresponding <span class="glossary-term" data-term="isin">ISIN</span> holders.</li>
            <li>Clearstream settles the distribution to each investor's custodial account according to its standard settlement cycle.</li>
            <li>The <code>reconcile</code> instruction is then used to verify that the on-chain and bankable distributions match.</li>
        </ul>
        <p>This dual-track claiming model is what makes <span class="glossary-term" data-term="crosssecurities">CrossSecurities</span> work — the same offering can pay both on-chain and traditional finance investors from a single waterfall execution.</p>
        <h2>Reconciliation</h2>
        <p>Reconciliation is the process of cross-checking on-chain distribution records with the bankable side. This is critical for offerings that have investors on both sides of the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> bridge.</p>
        <h3>The Reconcile Instruction</h3>
        <p>After a distribution epoch has been executed and Clearstream has settled the corresponding corporate action, the <span class="glossary-term" data-term="trustee">Trustee</span> calls the <code>reconcile</code> instruction:</p>
        <ol>
            <li>The Trustee obtains the Clearstream position report for the offering's <span class="glossary-term" data-term="isin">ISIN</span>, showing each investor's distribution receipt.</li>
            <li>The Clearstream adapter generates a SHA-256 hash of the position report and submits it as <code>clearstream_data</code>.</li>
            <li>The program compares the total distributed on-chain (from the <code>DistributionRecord</code>) with the total reported by Clearstream.</li>
            <li>If the amounts match, the <code>DistributionRecord</code> status is updated to <code>Reconciled</code>.</li>
            <li>If a discrepancy is detected, the status is set to <code>Disputed</code>, a <code>ComplianceViolation</code> event is emitted, and the DAO Manager <span class="glossary-term" data-term="grain">Grain</span> is alerted for investigation.</li>
        </ol>
        <h3>Reconciliation Schedule</h3>
        <p>The reconciliation engine runs on a configurable schedule — typically within 48 hours of each distribution execution. For high-frequency distributions (monthly), the nightly reconciliation job compares the on-chain lockbox state with Clearstream holdings and flags any drift. A discrepancy in the supply invariant (<code>tokens_locked == isin_outstanding</code>) triggers an immediate alert to the Trustee and platform operators.</p>
        <table>
            <thead>
                <tr>
                    <th>Reconciliation Type</th>
                    <th>Frequency</th>
                    <th>Trigger</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Post-Distribution</strong></td>
                    <td>Per epoch</td>
                    <td>Trustee-initiated after Clearstream confirms corporate action settlement</td>
                </tr>
                <tr>
                    <td><strong>Supply Invariant</strong></td>
                    <td>Nightly</td>
                    <td>Automated comparison of lockbox PDA state vs. Clearstream position report</td>
                </tr>
                <tr>
                    <td><strong>Full Audit</strong></td>
                    <td>Quarterly</td>
                    <td>Comprehensive reconciliation across all offerings, all epochs, all investors — generates the formal audit report</td>
                </tr>
            </tbody>
        </table>
        <h2>API Endpoints</h2>
        <p>The Distributions API is exposed through the platform's API gateway at <code>api.sails.to</code>. Authentication uses <a href="/knowledge/docs/authentication/">Solana wallet signature + NFT verification</a>. All endpoints return JSON.</p>
        <h3>Investor Endpoints</h3>
        <p>Authenticated with investor wallet signature:</p>
        <table>
            <thead>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>/v1/investor/distributions</code></td>
                    <td><code>GET</code></td>
                    <td>Lists all distributions across all offerings the investor holds. Returns epoch, amount, status (claimable / claimed / pending), and offering details. Supports pagination and filtering by offering ID or status.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/distributions/:epoch/claim</code></td>
                    <td><code>POST</code></td>
                    <td>Claims a specific distribution. Submits the <code>claim_distribution</code> instruction on behalf of the investor. Returns the transaction signature and claimed amount. Idempotent — returns success if already claimed.</td>
                </tr>
            </tbody>
        </table>
        <h3>Issuer Endpoints</h3>
        <p>Authenticated with Issuer NFT:</p>
        <table>
            <thead>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>/v1/offerings/:id/distributions</code></td>
                    <td><code>GET</code></td>
                    <td>Lists all distribution epochs for the offering. Returns epoch number, total distributed, amount per token, claim progress (claimed count / total investors), reconciliation status, and timestamps.</td>
                </tr>
                <tr>
                    <td><code>/v1/offerings/:id/distributions/waterfall</code></td>
                    <td><code>GET</code></td>
                    <td>Returns the waterfall configuration for the offering — tranche priorities, allocation rules, and current escrow balance.</td>
                </tr>
                <tr>
                    <td><code>/v1/offerings/:id/distributions/unclaimed</code></td>
                    <td><code>GET</code></td>
                    <td>Returns a list of investors with unclaimed distributions for the offering, grouped by epoch. Used by issuers and paying agents to follow up with investors who have not yet claimed.</td>
                </tr>
            </tbody>
        </table>
        <h3>Distribution Frequency</h3>
        <p>The distribution frequency is configured per offering in the <code>OfferingConfig</code> via the <code>distributionFrequency</code> field. Supported options:</p>
        <table>
            <thead>
                <tr>
                    <th>Frequency</th>
                    <th>Epoch Cadence</th>
                    <th>Typical Use Case</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Monthly</strong></td>
                    <td>12 epochs per year</td>
                    <td>Real estate rental income, recurring revenue assets</td>
                </tr>
                <tr>
                    <td><strong>Quarterly</strong></td>
                    <td>4 epochs per year</td>
                    <td>Standard fund distributions, most common for <span class="glossary-term" data-term="reg-d">Reg D</span> offerings</td>
                </tr>
                <tr>
                    <td><strong>Semi-annually</strong></td>
                    <td>2 epochs per year</td>
                    <td><span class="glossary-term" data-term="coupon">Coupon</span> payments on debt instruments</td>
                </tr>
                <tr>
                    <td><strong>Annually</strong></td>
                    <td>1 epoch per year</td>
                    <td>Year-end profit distributions, special dividends</td>
                </tr>
                <tr>
                    <td><strong>On-demand</strong></td>
                    <td>As needed</td>
                    <td>Asset sale proceeds, liquidation events, ad-hoc distributions</td>
                </tr>
            </tbody>
        </table>
        <p>The frequency setting determines when the Paying Agent is expected to execute the waterfall, but it does not enforce timing at the program level — the <code>execute_waterfall</code> instruction can be called at any time, subject to the dual-authorization requirement. The frequency is a business-logic convention, not a smart contract constraint.</p>
    </div>
</section>
