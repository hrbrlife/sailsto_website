---
title: "Investors API - Documentation"
description: "The Investor Self-Service Grain — portfolio management, distribution tracking, CrossConversion requests, secondary trading, tax documents, DAO governance, and the API endpoints that power the investor experience on Sails.to."
ogImage: "/og-image.png"
keywords: ["investor API", "portfolio", "distributions", "CrossConversion", "secondary trading", "tax documents", "DAO governance", "OTC", "cap table"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">Investors API</h1>
    <p class="section-desc">One grain per investor — portfolio, distributions, trading, tax documents, and governance in a single sandboxed process.</p>
</section>

<section class="features-section">
    <div class="container">

        <h2>Overview</h2>
        <p>The Investor Self-Service <span class="glossary-term" data-term="grain">Grain</span> is an Instance-type grain — one per investor, provisioned automatically when an investor signs up on the platform. It is the investor's personal dashboard, API surface, and data store, implemented in Go+HTMX as a native <span class="glossary-term" data-term="sandstorm">Sandstorm</span> grain. Every piece of investor-specific state — portfolio positions, distribution history, trade listings, wallet connections — lives inside this grain's encrypted journal. No shared database, no centralized user table, no way for one investor's grain to read another investor's data.</p>
        <p>The grain does not hold tokens or execute on-chain transactions directly. It aggregates data from <span class="glossary-term" data-term="offering">Offering Grains</span> via <span class="glossary-term" data-term="powerbox">Powerbox</span> capabilities, surfaces it through an HTMX-rendered UI and a JSON API, and delegates on-chain operations to the appropriate programs. When an investor claims a distribution, the grain submits the <code>claim_distribution</code> instruction to the <code>sails_distributions</code> program. When an investor requests a <span class="glossary-term" data-term="crossconversion">CrossConversion</span>, the grain calls the <code>requestCrossConversion</code> method on the Offering Grain's <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> interface. The grain is the coordinator — the blockchain is the settlement layer.</p>
        <p>The Investors API is exposed through the platform's API gateway at <code>api.sails.to</code>. Authentication uses <a href="/knowledge/docs/authentication/">Solana wallet signature</a> — the investor signs a challenge with their wallet, and the gateway verifies the signature before routing requests to the investor's grain. All endpoints return JSON.</p>

        <h2>Investor Self-Service Grain</h2>
        <p>The grain provides eight core capabilities, each mapping to a section of the investor dashboard and a set of API endpoints:</p>

        <table>
            <thead>
                <tr>
                    <th>Capability</th>
                    <th>Description</th>
                    <th>Data Source</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>View Portfolio</strong></td>
                    <td>All offerings the investor holds <span class="glossary-term" data-term="security-token">security tokens</span> in, with current balances, valuations, and yield metrics.</td>
                    <td>InvestorView capabilities from Offering Grains</td>
                </tr>
                <tr>
                    <td><strong>Track Distributions &amp; Yields</strong></td>
                    <td>Historical and pending distributions, cumulative yield, and per-epoch payout details.</td>
                    <td><span class="glossary-term" data-term="distributions">DistributionRecord</span> PDAs on-chain</td>
                </tr>
                <tr>
                    <td><strong>Request CrossConversion</strong></td>
                    <td>Convert on-chain tokens to <span class="glossary-term" data-term="bankable">bankable</span> <span class="glossary-term" data-term="isin">ISIN</span>-identified securities via <span class="glossary-term" data-term="clearstream">Clearstream</span>, or reverse the conversion.</td>
                    <td>CrossConversion Operator Grain + Trustee authentication</td>
                </tr>
                <tr>
                    <td><strong>Manage Wallet Connections</strong></td>
                    <td>Link and unlink <a href="/knowledge/glossary/solana/">Solana</a> wallets, set a primary wallet for distributions, and view wallet-level token balances.</td>
                    <td>Grain journal (encrypted)</td>
                </tr>
                <tr>
                    <td><strong>Download Tax Documents</strong></td>
                    <td>K-1 forms, distribution statements, and year-end tax summaries generated from on-chain records.</td>
                    <td>Compliance Grain + on-chain distribution records</td>
                </tr>
                <tr>
                    <td><strong>Participate in DAO Governance</strong></td>
                    <td>Vote on proposals, view voting history, and delegate voting weight.</td>
                    <td>GovernanceAPI via Powerbox</td>
                </tr>
                <tr>
                    <td><strong>View Cap Table Position</strong></td>
                    <td>Ownership percentage, token count, and position relative to total outstanding supply for each offering.</td>
                    <td>Offering Grain cap table snapshots</td>
                </tr>
                <tr>
                    <td><strong>List Tokens for OTC Sale</strong></td>
                    <td>Create sell listings for <span class="glossary-term" data-term="otc">OTC</span> secondary trading through the multi-broker network.</td>
                    <td>Broker Grain via Powerbox</td>
                </tr>
            </tbody>
        </table>

        <h2>Portfolio Endpoints</h2>
        <p>The portfolio endpoints provide a unified view of an investor's holdings across all offerings on the platform. Data is aggregated in real time from InvestorView capabilities granted by each Offering Grain the investor participates in.</p>

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
                    <td><code>/v1/investor/portfolio</code></td>
                    <td><code>GET</code></td>
                    <td>Returns all offerings the investor holds tokens in. Each entry includes offering name, series ID, token balance, nominal value per token, current valuation, unrealized yield, and offering status. Supports pagination via <code>?page=</code> and <code>?per_page=</code> query parameters.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/portfolio/:offering_id</code></td>
                    <td><code>GET</code></td>
                    <td>Returns detailed position information for a single offering: token balance, ownership percentage (tokens held ÷ total outstanding), lock-up expiration date, distribution history for this offering, CrossConversion status (how many tokens are on-chain vs. bankable), and the investor's accreditation tier at time of subscription.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/portfolio/summary</code></td>
                    <td><code>GET</code></td>
                    <td>Aggregated portfolio metrics: total valuation across all holdings, total distributions received (lifetime), weighted average yield, number of active offerings, and pending (unclaimed) distribution amount.</td>
                </tr>
            </tbody>
        </table>

        <h3>Position Detail</h3>
        <p>The position detail response for a single offering includes everything an investor needs to understand their holding:</p>

        <pre><code>GET /v1/investor/portfolio/:offering_id

{
  "offering_id": "series-alpha-2024",
  "offering_name": "Alpine Real Estate Fund I",
  "series_id": "series-alpha",
  "token_mint": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgHkV",
  "token_balance": 5000,
  "total_supply": 1000000,
  "ownership_percentage": 0.50,
  "nominal_value_per_token": 100,
  "current_valuation": 500000,
  "lock_up_expires_at": "2025-06-15T00:00:00Z",
  "crossconversion_status": {
    "on_chain": 3000,
    "bankable": 2000,
    "isin_code": "LU0123456789"
  },
  "yield": {
    "cumulative_distributions": 22500,
    "annualized_yield": 4.5,
    "last_distribution_epoch": 7,
    "next_distribution_expected": "2025-04-01T00:00:00Z"
  },
  "distributions": [
    { "epoch": 7, "amount": 3125, "status": "claimed", "claimed_at": "2025-01-15T14:30:00Z" },
    { "epoch": 6, "amount": 3125, "status": "claimed", "claimed_at": "2024-10-12T09:15:00Z" }
  ]
}</code></pre>

        <h3>Ownership Percentage</h3>
        <p>Ownership percentage is calculated as the investor's token balance divided by the total outstanding supply for the offering — not the max supply, but the actual minted and uncancelled supply. This percentage changes when new tokens are minted (dilution) or when tokens are burned (concentration). The grain recalculates this value on every request by querying the Offering Grain's cap table, ensuring it always reflects the current state of the ledger.</p>

        <h3>Yield Tracking</h3>
        <p>Yield is tracked per offering and across the entire portfolio. Per-offering yield is the sum of all distributions claimed, divided by the investor's cost basis (tokens × nominal value at subscription). Portfolio-level yield is the weighted average across all holdings. The grain stores distribution claim receipts in its journal and cross-references them with on-chain <code>DistributionRecord</code> PDAs to ensure consistency. If the grain's journal and the on-chain record disagree, the on-chain record is authoritative.</p>

        <h2>CrossConversion Requests</h2>
        <p><span class="glossary-term" data-term="crossconversion">CrossConversion</span> allows investors to move between <span class="glossary-term" data-term="on-chain">on-chain</span> token ownership and <span class="glossary-term" data-term="bankable">bankable</span> custody via <span class="glossary-term" data-term="clearstream">Clearstream</span>. The Investor Grain exposes this through a simple API — the complexity of lockbox management, <span class="glossary-term" data-term="trustee">Trustee</span> authentication, and Clearstream settlement is handled by the CrossConversion Operator Grain behind the scenes.</p>

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
                    <td><code>/v1/investor/crossconversion</code></td>
                    <td><code>POST</code></td>
                    <td>Submits a new CrossConversion request. Requires <code>offering_id</code>, <code>direction</code> (<code>to_bankable</code> or <code>to_onchain</code>), and <code>amount</code>. Returns a request ID and initial status. The request enters a pending state until Trustee authentication is obtained.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/crossconversion/:request_id</code></td>
                    <td><code>GET</code></td>
                    <td>Returns the current status of a CrossConversion request: <code>pending_trustee</code>, <code>locking</code>, <code>awaiting_clearstream</code>, <code>settled</code>, or <code>failed</code>. Includes timestamps for each state transition and the Trustee's authentication signature once obtained.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/crossconversion</code></td>
                    <td><code>GET</code></td>
                    <td>Lists all CrossConversion requests for the investor, filterable by <code>status</code> and <code>offering_id</code>. Supports pagination.</td>
                </tr>
            </tbody>
        </table>

        <h3>The requestCrossConversion Method</h3>
        <p>Under the hood, the Investor Grain calls the <code>requestCrossConversion</code> method on the Offering Grain's <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> OfferingAPI interface. This is a Powerbox-mediated call — the Investor Grain must hold a valid InvestorView capability for the offering, and the Offering Grain validates the request against the investor's position and the offering's CrossConversion configuration.</p>

        <pre><code># From sails/offering.capnp

interface OfferingAPI {
  requestCrossConversion @2 (direction :ConversionDirection, amount :UInt64)
    -> (request :ConversionRequest);
  # direction: toBankable | toOnChain
  # amount: number of tokens to convert
  # Returns a ConversionRequest with request ID and initial status
}</code></pre>

        <p>The conversion flow proceeds as follows:</p>
        <ol>
            <li><strong>Investor submits request</strong> — The Investor Grain validates that the investor has sufficient unlocked tokens (for <code>to_bankable</code>) or sufficient bankable position (for <code>to_onchain</code>), then calls <code>requestCrossConversion</code> on the Offering Grain.</li>
            <li><strong>Offering Grain queues request</strong> — The Offering Grain records the request and notifies the CrossConversion Operator Grain and the Trustee Dashboard Grain via Powerbox events.</li>
            <li><strong>Trustee authenticates</strong> — The <span class="glossary-term" data-term="trustee">Trustee</span> reviews and signs the conversion request using their Trustee NFT. For conversions under the configurable threshold, this is a 1-of-1 signature. For large conversions exceeding $1M, a 2-of-3 <span class="glossary-term" data-term="threshold-signing">keyholder ceremony</span> is required.</li>
            <li><strong>On-chain execution</strong> — For <code>to_bankable</code>: the <code>sails_crossconversion</code> program locks the investor's tokens in the lockbox <span class="glossary-term" data-term="pda">PDA</span> and emits a <code>CrossConversionRequested</code> event. For <code>to_onchain</code>: the program verifies the Clearstream cancellation proof and unlocks tokens from the lockbox.</li>
            <li><strong>Clearstream settlement</strong> — The CrossConversion Operator Grain initiates the corresponding action with Clearstream: crediting the investor's custodial account (for <code>to_bankable</code>) or cancelling the <span class="glossary-term" data-term="isin">ISIN</span> position (for <code>to_onchain</code>).</li>
            <li><strong>Status update</strong> — The Investor Grain receives a Powerbox notification when the conversion settles and updates the request status to <code>settled</code>.</li>
        </ol>
        <p>The 1:1 supply invariant — <code>tokens_locked == isin_outstanding</code> — is enforced at every step. The lockbox contract will reject any lock or unlock operation that would violate this invariant, and the nightly reconciliation engine verifies it independently by comparing on-chain lockbox state with Clearstream position reports.</p>

        <h2>Secondary Trading</h2>
        <p>Investors can list their <span class="glossary-term" data-term="security-token">security tokens</span> for sale on the <span class="glossary-term" data-term="otc">OTC</span> secondary market. Sails.to operates a multi-broker network — trades are not matched by the platform directly but by licensed <span class="glossary-term" data-term="broker-dealer">broker-dealers</span> who hold Broker role NFTs. The Investor Grain provides the listing interface; the Broker Grain handles matching, compliance checks, and settlement.</p>

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
                    <td><code>/v1/investor/listings</code></td>
                    <td><code>POST</code></td>
                    <td>Creates a new sell listing. Requires <code>offering_id</code>, <code>amount</code> (tokens to sell), and <code>price_per_token</code>. The listing is published to the multi-broker network. Returns a listing ID and status.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/listings</code></td>
                    <td><code>GET</code></td>
                    <td>Lists all active, matched, settled, and cancelled listings for the investor. Supports filtering by <code>status</code> and <code>offering_id</code>.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/listings/:listing_id</code></td>
                    <td><code>GET</code></td>
                    <td>Returns detail for a single listing: current status, matched buyer (if any), settlement progress, and broker information.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/listings/:listing_id</code></td>
                    <td><code>DELETE</code></td>
                    <td>Cancels an active listing. Only possible if the listing has not yet been matched with a buyer. Returns success or an error if the listing is already in settlement.</td>
                </tr>
            </tbody>
        </table>

        <h3>How Trades Match Through the Broker Grain</h3>
        <p>When an investor creates a sell listing, the Investor Grain publishes it to the Broker Grain network via the <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> BrokerAPI interface:</p>

        <pre><code># From sails/broker.capnp

interface BrokerAPI {
  listForSecondaryTrading @1 (offering :Text, amount :UInt64, price :UInt64)
    -> (listing :TradeListing);
  matchTrade @2 (listing :TradeListing, buyer :InvestorCredential)
    -> (settlement :TradeSettlement);
}</code></pre>

        <ol>
            <li><strong>Listing published</strong> — The Investor Grain calls <code>listForSecondaryTrading</code> on the Broker Grain. The listing becomes visible to all brokers in the network who are authorized to trade the offering.</li>
            <li><strong>Buyer identified</strong> — A broker identifies an interested buyer from their client roster. The buyer must hold a valid <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT with the appropriate investor classification and jurisdiction for the offering.</li>
            <li><strong>Compliance check</strong> — The Broker Grain verifies both parties: the seller has sufficient unlocked tokens, the buyer has a valid KYC credential, both wallets pass the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> compliance checks (jurisdiction whitelist, accreditation tier, lock-up period), and the transfer would not violate the offering's <code>ComplianceConfig</code> maximum investor count.</li>
            <li><strong>Trade matched</strong> — The Broker Grain calls <code>matchTrade</code>, which initiates the on-chain <code>transfer_with_compliance</code> instruction on the <code>sails_securities</code> program. The Transfer Hook enforces all compliance rules at the smart contract level.</li>
            <li><strong>Settlement</strong> — On successful transfer, the Broker Grain notifies both the seller's and buyer's Investor Grains via Powerbox. The seller's grain updates the listing status to <code>settled</code> and adjusts the portfolio. The buyer's grain adds the new position.</li>
        </ol>
        <p>The platform does not operate an order book or matching engine. Each trade is a bilateral OTC transaction mediated by a licensed broker. This structure is deliberate — it ensures every secondary trade has a responsible broker-dealer who has performed their own suitability analysis, as required for <span class="glossary-term" data-term="reg-d">Reg D</span> securities.</p>

        <h2>Tax &amp; Statements</h2>
        <p>The Investor Grain provides access to tax documents and distribution statements generated from on-chain records. Data is pulled from <code>DistributionRecord</code> PDAs, cap table snapshots, and the investor's position history — all on-chain, all auditable, all immutable.</p>

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
                    <td><code>/v1/investor/tax/k1/:tax_year</code></td>
                    <td><code>GET</code></td>
                    <td>Downloads the K-1 form for the specified tax year. Each DAO Series LLC is a pass-through entity — income, deductions, and credits flow through to investors proportional to their token holdings. The K-1 is generated by the Compliance Grain from on-chain distribution records and cap table snapshots at each epoch.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/tax/statements</code></td>
                    <td><code>GET</code></td>
                    <td>Lists all available distribution statements. Each statement covers one distribution epoch for one offering and includes the gross distribution amount, any withholding, the net amount paid, and the payment method (on-chain claim or Clearstream corporate action). Supports filtering by <code>tax_year</code> and <code>offering_id</code>.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/tax/statements/:statement_id</code></td>
                    <td><code>GET</code></td>
                    <td>Downloads a specific distribution statement as a PDF. Includes the offering details, epoch number, waterfall tranche breakdown, the investor's pro-rata calculation, and the on-chain transaction signature for verification.</td>
                </tr>
                <tr>
                    <td><code>/v1/investor/tax/summary/:tax_year</code></td>
                    <td><code>GET</code></td>
                    <td>Returns a year-end tax summary aggregating all distributions across all offerings: total ordinary income, total capital gains (if any), total withholding, and the investor's aggregate cost basis. Intended for tax preparation use.</td>
                </tr>
            </tbody>
        </table>

        <h3>K-1 Generation</h3>
        <p>Each offering on Sails.to is structured as a Series within a Wyoming DAO Series LLC. As a pass-through entity, the LLC does not pay federal income tax — instead, each investor receives a Schedule K-1 (Form 1065) reflecting their share of the Series' income, deductions, and credits for the tax year.</p>
        <p>The K-1 is generated by the Compliance Grain using the following data sources:</p>
        <ul>
            <li><strong>Distribution records</strong> — Every <code>DistributionRecord</code> PDA for the offering during the tax year, capturing the <code>amount_per_token</code> and the investor's claimed amount per epoch.</li>
            <li><strong>Cap table snapshots</strong> — The investor's token balance at each epoch's <code>snapshot_slot</code>, determining their pro-rata share. If the investor acquired or disposed of tokens mid-year, the K-1 reflects the weighted average ownership across all epochs.</li>
            <li><strong>Offering classification</strong> — The tax treatment depends on the offering type: rental income for real estate offerings, interest income for debt instruments, dividend income for equity offerings. This classification is stored in the <code>OfferingConfig</code> and does not change after offering initialization.</li>
        </ul>
        <p>K-1s are typically available by March 15 following the tax year, in accordance with IRS partnership return filing deadlines. The Investor Grain sends a notification when the K-1 is ready for download.</p>

        <h3>Distribution Statements</h3>
        <p>Distribution statements are generated per epoch, per offering. Each statement provides a complete audit trail from revenue deposit through waterfall execution to the investor's individual payout. The statement includes the on-chain transaction signature for the <code>execute_waterfall</code> instruction and the investor's <code>claim_distribution</code> instruction — anyone can independently verify the amounts on the <a href="/knowledge/glossary/solana/">Solana</a> blockchain.</p>
        <p>For investors holding positions on the <span class="glossary-term" data-term="bankable">bankable</span> side via <span class="glossary-term" data-term="clearstream">Clearstream</span>, the distribution statement also includes the Clearstream corporate action reference number, allowing the investor to cross-reference with their custodial account statement.</p>

        <h2>Powerbox Integration</h2>
        <p>The Investor Grain does not operate in isolation. It receives capabilities from other grains via the <span class="glossary-term" data-term="powerbox">Powerbox</span> — the same claim-token-to-sturdyRef lifecycle that governs all inter-grain communication on the platform. The grain's functionality is directly determined by which capabilities it holds.</p>

        <h3>InvestorView from Offering Grains</h3>
        <p>When an investor subscribes to an offering, the Offering Grain issues an <code>InvestorView</code> capability to the Investor Grain via Powerbox. This capability provides read access to the investor's position within that offering: token balance, distribution history, cap table position, and CrossConversion status. The Investor Grain claims this capability and stores the resulting sturdyRef in its journal for persistent access across sessions.</p>
        <p>The InvestorView capability is scoped — it only exposes the requesting investor's own position, not the full cap table or other investors' data. An investor who holds tokens in five offerings will hold five separate InvestorView capabilities, one from each Offering Grain. This is how the portfolio view is assembled: the Investor Grain iterates over its InvestorView sturdyRefs and aggregates the responses.</p>

        <pre><code>Powerbox Capability Flow:

Offering Grain A ──(InvestorView)──► Investor Grain
Offering Grain B ──(InvestorView)──►     │
Offering Grain C ──(InvestorView)──►     │
                                         │
                                    Aggregates into
                                    /v1/investor/portfolio</code></pre>

        <h3>KYC Status from KYC Grains</h3>
        <p>The Investor Grain holds a read-only <code>getStatus</code> and <code>getCredential</code> capability on the investor's <span class="glossary-term" data-term="kyc">KYC</span> Grain. This allows the Investor Grain to display the current KYC verification status, credential expiration date, and investor classification directly in the dashboard. When the KYC credential is approaching expiration (60 days or fewer), the Investor Grain surfaces a re-verification prompt.</p>
        <p>The Investor Grain cannot modify the KYC state — it holds read-only capabilities. If the investor needs to re-verify, the Investor Grain calls <code>startVerification</code> on the KYCVerifier interface to spawn a new KYC Grain instance. The KYC Grain's HTMX-rendered UI is embedded directly in the investor dashboard via iframe, so the investor completes the verification flow without leaving their Self-Service Grain.</p>

        <h3>Broker Assistance for Trades</h3>
        <p>When an investor creates a sell listing for secondary trading, the Investor Grain must request assistance from a Broker Grain. The Investor Grain does not hold a BrokerAPI capability by default — it requests one through Powerbox at the time of listing creation. The Platform Operator pre-authorizes a set of Broker Grains for each offering, and the Powerbox routes the request to an eligible broker.</p>

        <pre><code>Powerbox Capability Flow:

Investor Grain ──(Powerbox request: BrokerAPI)──► Powerbox Router
                                                       │
                                              Routes to eligible
                                              Broker Grain(s)
                                                       │
Broker Grain ──(BrokerAPI capability)──► Investor Grain
    │                                         │
    │  Investor calls:                        │
    │  listForSecondaryTrading()              │
    │                                         │
    │  Broker matches buyer, calls:           │
    │  matchTrade() → on-chain settlement     │
    │                                         │
    └──(TradeSettlement notification)──► Investor Grain</code></pre>

        <p>The Broker Grain retains the BrokerAPI capability for the duration of the listing. Once the trade settles or the listing is cancelled, the capability is released. This ensures that brokers only have access to the investor's trading intent for the specific listings they are servicing — no persistent surveillance, no access to the investor's broader portfolio or personal data.</p>

        <h3>Governance Participation</h3>
        <p>For offerings with DAO governance enabled, the Investor Grain receives a <code>GovernanceAPI</code> capability from the DAO Manager Grain. This capability allows the investor to view active proposals, cast votes weighted by their token holdings, and view voting results. The Investor Grain calls <code>vote</code> on the GovernanceAPI interface, which records the vote on-chain and updates the proposal's tally. Voting weight is determined by the investor's token balance at a governance snapshot slot — the same snapshot mechanism used for distribution calculations.</p>

    </div>
</section>
