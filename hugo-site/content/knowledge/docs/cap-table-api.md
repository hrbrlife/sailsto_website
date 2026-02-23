---
title: "Cap Table API - Documentation"
description: "The cap table on Sails.to is the live state of InvestorPosition PDAs on Solana — always current, always verifiable, always immutable."
ogImage: "/og-image.png"
keywords: ["cap table", "InvestorPosition", "OfferingState", "PDA", "ownership", "snapshot", "audit", "CrossConversion", "access control"]
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
heroDesc: "The cap table is not a spreadsheet — it's the live state of on-chain PDAs, read and exposed by the Offering Grain."
draft: false
---
<h2>Overview</h2>
        <p>The cap table on Sails.to is not a spreadsheet. It is the live state of the <span class="glossary-term" data-term="pda">InvestorPosition PDAs</span> on <a href="/knowledge/glossary/solana/">Solana</a>. There is no separate database of ownership records, no CSV export that becomes stale the moment it is generated, no reconciliation step between "the cap table" and "the ledger." They are the same thing. The blockchain <em>is</em> the cap table.</p>
        <p>The <span class="glossary-term" data-term="offering">Offering</span> <span class="glossary-term" data-term="grain">Grain</span> reads this <span class="glossary-term" data-term="on-chain">on-chain</span> state and exposes it through the <code>getCapTable</code> method on its <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> OfferingAPI interface. Every query returns the current state of the ledger — not a cached copy, not a periodic sync, but the actual on-chain data at the moment of the request. When a token is minted, transferred, locked in a <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox, or frozen by a compliance action, the cap table reflects that change immediately because the cap table <em>is</em> that change.</p>
        <p>This design eliminates an entire class of operational risk that plagues traditional cap table management: the drift between what the spreadsheet says and what actually happened. On Sails.to, ownership is on-chain, queries are against on-chain state, and every position is independently verifiable by anyone with a <a href="/knowledge/glossary/solana/">Solana</a> RPC endpoint.</p>
        <h2>InvestorPosition PDA</h2>
        <p>Every investor's position in an offering is stored as a <span class="glossary-term" data-term="pda">Program Derived Address</span> — a deterministic on-chain account seeded from the offering ID and the investor's wallet address. The <code>InvestorPosition</code> PDA is the atomic unit of the cap table. One PDA per investor per offering, created when the investor first subscribes and updated with every subsequent event that affects their position.</p>
        <pre><code>InvestorPosition PDA
Seeds: ["investor_position", offering_id, wallet]
├── offering_id: Pubkey        // The offering this position belongs to
├── wallet: Pubkey             // The investor's Solana wallet address
├── balance: u64               // Current token balance (including locked tokens)
├── locked_until: i64          // Lock-up expiration timestamp (0 if unlocked)
├── accreditation_tier: u8     // Investor classification at time of subscription
├── jurisdiction: String       // Two-letter country code (ISO 3166-1)
├── position_index: u32        // Sequential index for distribution bitmap
└── created_at: i64            // Timestamp of initial subscription</code></pre>
        <p>The PDA address is deterministic — given an offering ID and a wallet address, anyone can derive the PDA address and read the investor's position directly from the blockchain without going through the platform API. This is the verifiability guarantee: an investor can independently confirm their ownership using any <a href="/knowledge/glossary/solana/">Solana</a> explorer or RPC client.</p>
        <h3>Key Fields</h3>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>offering_id</code></strong></td>
                    <td><code>Pubkey</code></td>
                    <td>The <span class="glossary-term" data-term="offering">offering</span> this position belongs to. Links the investor to a specific Series within the <span class="glossary-term" data-term="operating-series">DAO Series LLC</span>.</td>
                </tr>
                <tr>
                    <td><strong><code>wallet</code></strong></td>
                    <td><code>Pubkey</code></td>
                    <td>The investor's <a href="/knowledge/glossary/solana/">Solana</a> wallet address. Combined with <code>offering_id</code>, this forms the unique seed pair for the PDA.</td>
                </tr>
                <tr>
                    <td><strong><code>balance</code></strong></td>
                    <td><code>u64</code></td>
                    <td>Current token balance. This includes tokens locked in the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox — locked tokens still count toward ownership, only the custody rail changes.</td>
                </tr>
                <tr>
                    <td><strong><code>locked_until</code></strong></td>
                    <td><code>i64</code></td>
                    <td>Unix timestamp when the lock-up period expires. Transfers are blocked by the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> until this timestamp is reached. Set to <code>0</code> if no lock-up applies.</td>
                </tr>
                <tr>
                    <td><strong><code>accreditation_tier</code></strong></td>
                    <td><code>u8</code></td>
                    <td>The investor's accreditation classification at time of subscription: <code>1</code> = Accredited Investor, <code>2</code> = Qualified Purchaser, <code>3</code> = Institutional. Used by the Transfer Hook to enforce <span class="glossary-term" data-term="reg-d">Reg D</span> transfer restrictions.</td>
                </tr>
                <tr>
                    <td><strong><code>jurisdiction</code></strong></td>
                    <td><code>String</code></td>
                    <td>Two-letter country code recorded from the investor's <span class="glossary-term" data-term="kyc">KYC</span> credential. The Transfer Hook checks this against the offering's allowed jurisdictions whitelist on every transfer.</td>
                </tr>
            </tbody>
        </table>
        <p>The <code>position_index</code> field deserves special attention. It is assigned sequentially when the investor first subscribes and never changes — even if the investor sells all tokens and later reacquires them. This index maps the investor to a specific bit in the <code>claimed_bitmap</code> of <a href="/knowledge/docs/distributions-api/">DistributionRecord</a> PDAs, enabling efficient tracking of which investors have claimed their <span class="glossary-term" data-term="distributions">distributions</span> for each epoch.</p>
        <h2>OfferingState PDA</h2>
        <p>While <code>InvestorPosition</code> PDAs represent individual holdings, the <code>OfferingState</code> PDA provides the aggregate view of an offering — the total picture of supply, ownership, and status. There is exactly one <code>OfferingState</code> PDA per offering, created when the offering is initialized by the <span class="glossary-term" data-term="offering">Issuer</span>.</p>
        <pre><code>OfferingState PDA
Seeds: ["offering_state", series_id]
├── series_id: Text            // The Series identifier within the DAO LLC
├── max_supply: u64            // Maximum token supply authorized for this offering
├── minted: u64                // Total tokens minted to date
├── locked_in_crossconv: u64   // Tokens currently locked in CrossConversion lockbox
├── nominal_value: u64         // Nominal value per token (in cents)
├── status: enum               // Active, Paused, Closed, Redeemed
├── token_mint: Pubkey         // Solana mint address for the security token
├── isin_code: Text            // ISIN code (if CrossConversion enabled)
├── compliance_config: Pubkey  // Reference to ComplianceConfig PDA
└── created_at: i64            // Offering initialization timestamp</code></pre>
        <h3>Key Fields</h3>
        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>series_id</code></strong></td>
                    <td><code>Text</code></td>
                    <td>The Series identifier within the Wyoming DAO Series LLC. Each offering maps 1:1 to a Series — the legal entity wrapper for the asset.</td>
                </tr>
                <tr>
                    <td><strong><code>max_supply</code></strong></td>
                    <td><code>u64</code></td>
                    <td>Maximum number of <span class="glossary-term" data-term="security-token">security tokens</span> that can be minted for this offering. Set at initialization, immutable after first investor subscription.</td>
                </tr>
                <tr>
                    <td><strong><code>minted</code></strong></td>
                    <td><code>u64</code></td>
                    <td>Total tokens minted to date. The difference <code>max_supply - minted</code> represents remaining capacity. Incremented on every <code>mint_security_token</code> instruction.</td>
                </tr>
                <tr>
                    <td><strong><code>locked_in_crossconv</code></strong></td>
                    <td><code>u64</code></td>
                    <td>Tokens currently locked in the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox. These tokens are still part of the total supply and still count toward their holders' ownership — only the custody rail has changed from on-chain to <span class="glossary-term" data-term="bankable">bankable</span> via <span class="glossary-term" data-term="clearstream">Clearstream</span>.</td>
                </tr>
                <tr>
                    <td><strong><code>nominal_value</code></strong></td>
                    <td><code>u64</code></td>
                    <td>Nominal value per token in cents. Used for valuation calculations and K-1 generation. Set at initialization.</td>
                </tr>
                <tr>
                    <td><strong><code>status</code></strong></td>
                    <td><code>enum</code></td>
                    <td><code>Active</code> (accepting subscriptions and transfers), <code>Paused</code> (temporarily halted by <span class="glossary-term" data-term="trustee">Trustee</span>), <code>Closed</code> (no new subscriptions), or <code>Redeemed</code> (final redemption complete, tokens burned).</td>
                </tr>
            </tbody>
        </table>
        <p>The supply invariant <code>minted == sum(all InvestorPosition.balance)</code> is enforced at the program level. Every mint instruction increments <code>minted</code> and creates or updates the corresponding <code>InvestorPosition</code>. Every burn decrements both. There is no way for the aggregate to drift from the sum of individual positions — the smart contract makes it structurally impossible.</p>
        <h2>Cap Table Endpoints</h2>
        <p>The Cap Table API is exposed through the platform's API gateway at <code>api.sails.to</code>. Authentication uses <a href="/knowledge/docs/authentication/">Solana wallet signature + NFT verification</a>. All endpoints return JSON. The data returned is read directly from <span class="glossary-term" data-term="on-chain">on-chain</span> state — there is no intermediate database or cache layer between the API and the blockchain.</p>
        <h3>REST Endpoints</h3>
        <table>
            <thead>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Authorization</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>/v1/offerings/:id/cap-table</code></td>
                    <td><code>GET</code></td>
                    <td>Issuer NFT or <span class="glossary-term" data-term="trustee">Trustee</span> NFT</td>
                    <td>Returns the full cap table for the offering — every <code>InvestorPosition</code> PDA associated with the offering ID. Includes wallet address, balance, lock-up status, accreditation tier, jurisdiction, and CrossConversion status. Supports pagination via <code>?page=</code> and <code>?per_page=</code> query parameters.</td>
                </tr>
                <tr>
                    <td><code>/v1/offerings/:id/cap-table/summary</code></td>
                    <td><code>GET</code></td>
                    <td>Issuer NFT or Trustee NFT</td>
                    <td>Returns aggregate cap table metrics: total investors, total minted supply, tokens on-chain vs. tokens in CrossConversion lockbox, ownership concentration (top 10 holders), and jurisdiction breakdown.</td>
                </tr>
                <tr>
                    <td><code>/v1/offerings/:id/cap-table/position/:wallet</code></td>
                    <td><code>GET</code></td>
                    <td>Issuer NFT, Trustee NFT, or investor wallet signature (own position only)</td>
                    <td>Returns a single investor's position: balance, ownership percentage, lock-up expiration, accreditation tier, jurisdiction, distribution history, and CrossConversion status for that position.</td>
                </tr>
                <tr>
                    <td><code>/v1/offerings/:id/cap-table/snapshot</code></td>
                    <td><code>POST</code></td>
                    <td>Issuer NFT or Trustee NFT</td>
                    <td>Creates an on-demand ownership snapshot. Reads all <code>InvestorPosition</code> PDAs at the current <a href="/knowledge/glossary/solana/">Solana</a> slot and returns a timestamped, immutable record of ownership. See <a href="#cap-table-snapshots">Cap Table Snapshots</a> below.</td>
                </tr>
            </tbody>
        </table>
        <h3>Cap'n Proto Interface</h3>
        <p>The Offering <span class="glossary-term" data-term="grain">Grain</span> also exposes the cap table through its <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> OfferingAPI interface for direct grain-to-grain communication via <span class="glossary-term" data-term="powerbox">Powerbox</span>. This is the method used by Investor Grains, Broker Grains, and the Compliance Grain to read cap table data without going through the REST API gateway.</p>
        <pre><code># From sails/offering.capnp

interface OfferingAPI {
  getCapTable @1 () -> (investors :List(InvestorPosition));
  # Returns the full list of InvestorPosition records for this offering.
  # Each InvestorPosition includes: offering_id, wallet, balance,
  # locked_until, accreditation_tier, jurisdiction, position_index.
  # Data is read directly from on-chain PDAs at the time of the call.
}</code></pre>
        <p>The <code>getCapTable</code> method returns a <code>List(InvestorPosition)</code> — the same data structure as the REST endpoint, but delivered through the Powerbox capability system. The calling grain must hold a valid capability for the Offering Grain: an <code>OfferingAPI</code> capability (for Issuers and Brokers) or a <code>TrusteeView</code> capability (for Trustees). Investor Grains hold <code>InvestorView</code> capabilities, which only expose their own position — not the full cap table.</p>
        <h3>Response Format</h3>
        <pre><code>GET /v1/offerings/:id/cap-table

{
  "offering_id": "series-alpha-2024",
  "series_id": "series-alpha",
  "snapshot_slot": 285431200,
  "total_investors": 247,
  "total_supply": 1000000,
  "locked_in_crossconv": 150000,
  "investors": [
    {
      "wallet": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgHkV",
      "balance": 5000,
      "ownership_percentage": 0.50,
      "locked_until": "2025-06-15T00:00:00Z",
      "accreditation_tier": 1,
      "jurisdiction": "US",
      "crossconversion_status": {
        "on_chain": 3000,
        "bankable": 2000
      },
      "position_index": 0
    },
    {
      "wallet": "9bKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAbC",
      "balance": 12000,
      "ownership_percentage": 1.20,
      "locked_until": "2025-03-01T00:00:00Z",
      "accreditation_tier": 2,
      "jurisdiction": "DE",
      "crossconversion_status": {
        "on_chain": 12000,
        "bankable": 0
      },
      "position_index": 1
    }
  ]
}</code></pre>
        <h2 id="cap-table-snapshots">Cap Table Snapshots</h2>
        <p>A cap table snapshot is a point-in-time record of all ownership positions for an offering, pulled directly from on-chain state. Snapshots are immutable — once created, they cannot be modified, because they reference a specific <a href="/knowledge/glossary/solana/">Solana</a> slot number. Anyone can independently verify a snapshot by reading the same PDAs at the same slot using an archival RPC node.</p>
        <p>Snapshots serve three primary purposes:</p>
        <ul>
            <li><strong>Audit compliance:</strong> Auditors require a frozen view of ownership at specific dates — quarter-end, year-end, or the date of a specific event. Snapshots provide this without requiring the auditor to interact with the live ledger.</li>
            <li><strong>Tax season:</strong> K-1 generation requires ownership percentages at each <span class="glossary-term" data-term="distributions">distribution</span> epoch. The Compliance <span class="glossary-term" data-term="grain">Grain</span> uses cap table snapshots to determine each investor's pro-rata share for tax reporting.</li>
            <li><strong>Regulatory filings:</strong> <span class="glossary-term" data-term="reg-d">Reg D</span> and Reg S filings require accurate investor counts and ownership breakdowns by jurisdiction and accreditation tier. Snapshots provide this data in an exportable, verifiable format.</li>
        </ul>
        <h3>Snapshot Lifecycle</h3>
        <table>
            <thead>
                <tr>
                    <th>Step</th>
                    <th>Action</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>1</strong></td>
                    <td>Request</td>
                    <td>An Issuer or <span class="glossary-term" data-term="trustee">Trustee</span> calls <code>POST /v1/offerings/:id/cap-table/snapshot</code> with an optional <code>label</code> parameter (e.g., "Q4-2024-audit", "year-end-2024").</td>
                </tr>
                <tr>
                    <td><strong>2</strong></td>
                    <td>On-chain read</td>
                    <td>The Offering Grain reads all <code>InvestorPosition</code> PDAs for the offering at the current Solana slot. The slot number is recorded as the snapshot's anchor point.</td>
                </tr>
                <tr>
                    <td><strong>3</strong></td>
                    <td>Hash &amp; store</td>
                    <td>The snapshot data is hashed (SHA-256) and the hash is stored in the Offering Grain's journal. The full snapshot data is stored alongside the hash for retrieval.</td>
                </tr>
                <tr>
                    <td><strong>4</strong></td>
                    <td>Export</td>
                    <td>The snapshot can be exported as JSON or CSV via <code>GET /v1/offerings/:id/cap-table/snapshots/:snapshot_id</code>. The export includes the Solana slot number and the SHA-256 hash for independent verification.</td>
                </tr>
            </tbody>
        </table>
        <h3>Snapshot vs. Live Cap Table</h3>
        <p>The live cap table (via <code>GET /v1/offerings/:id/cap-table</code>) always returns the current state. A snapshot freezes the state at a specific moment. Both read from the same on-chain data — the difference is that a snapshot records the Solana slot number and preserves the data for historical reference. The live cap table is what you query to see who owns what <em>right now</em>. A snapshot is what you hand to an auditor to show who owned what <em>on a specific date</em>.</p>
        <h2>CrossConversion Impact</h2>
        <p>When an investor converts their on-chain tokens to <span class="glossary-term" data-term="bankable">bankable</span> securities via <span class="glossary-term" data-term="crossconversion">CrossConversion</span>, the cap table reflects a change in custody — not a change in ownership. The tokens are locked in the CrossConversion lockbox <span class="glossary-term" data-term="pda">PDA</span>, and the investor receives an equivalent position in <span class="glossary-term" data-term="clearstream">Clearstream</span> identified by the offering's <span class="glossary-term" data-term="isin">ISIN</span> code. But the investor's <code>InvestorPosition</code> PDA still reflects their full balance — locked tokens are included.</p>
        <h3>How the Cap Table Handles CrossConversion</h3>
        <table>
            <thead>
                <tr>
                    <th>Scenario</th>
                    <th>On-Chain Balance</th>
                    <th>Lockbox</th>
                    <th>Bankable</th>
                    <th>Cap Table Balance</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Investor holds 5,000 tokens on-chain</td>
                    <td>5,000</td>
                    <td>0</td>
                    <td>0</td>
                    <td><strong>5,000</strong></td>
                </tr>
                <tr>
                    <td>Investor converts 2,000 to bankable</td>
                    <td>3,000</td>
                    <td>2,000</td>
                    <td>2,000</td>
                    <td><strong>5,000</strong></td>
                </tr>
                <tr>
                    <td>Investor converts remaining 3,000</td>
                    <td>0</td>
                    <td>5,000</td>
                    <td>5,000</td>
                    <td><strong>5,000</strong></td>
                </tr>
                <tr>
                    <td>Investor converts 1,000 back to on-chain</td>
                    <td>1,000</td>
                    <td>4,000</td>
                    <td>4,000</td>
                    <td><strong>5,000</strong></td>
                </tr>
            </tbody>
        </table>
        <p>The cap table provides a unified view regardless of format. An investor who has converted 100% of their tokens to <span class="glossary-term" data-term="bankable">bankable</span> securities still appears on the cap table with their full balance. The <code>crossconversion_status</code> field in the API response breaks down how many tokens are held on-chain versus locked in the <span class="glossary-term" data-term="crossconversion">CrossConversion</span> lockbox, but the total ownership never changes due to a CrossConversion event.</p>
        <p>The supply invariant <code>tokens_locked == isin_outstanding</code> is enforced by the <code>sails_crossconversion</code> program and verified nightly by the reconciliation engine. If the lockbox PDA state and the <span class="glossary-term" data-term="clearstream">Clearstream</span> position report ever disagree, the <span class="glossary-term" data-term="trustee">Trustee</span> is alerted immediately and further CrossConversion operations are suspended until the discrepancy is resolved.</p>
        <h2>Access Control</h2>
        <p>Cap table access is governed by the <span class="glossary-term" data-term="nft-hierarchy">NFT role hierarchy</span>. Different participants see different slices of the cap table based on the role NFT they hold. There is no single "cap table permission" — access is granular and role-specific.</p>
        <table>
            <thead>
                <tr>
                    <th>Role</th>
                    <th>Cap Table Access</th>
                    <th>Authorization</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Issuer</strong></td>
                    <td>Full cap table for their own offering(s). All investor positions, balances, jurisdictions, accreditation tiers, CrossConversion status. Can request snapshots and export data.</td>
                    <td>Issuer NFT linked to the specific offering</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="trustee">Trustee</span></strong></td>
                    <td>Full cap table for all Series under their jurisdiction. Cross-offering view for audit and compliance purposes. Can request snapshots, trigger reconciliation, and export data for regulatory filings.</td>
                    <td>Trustee NFT issued by Platform Operator</td>
                </tr>
                <tr>
                    <td><strong>Broker</strong></td>
                    <td>Positions for investors they placed. A broker sees only the <code>InvestorPosition</code> PDAs for wallets that subscribed through their <span class="glossary-term" data-term="offering">Broker Grain</span>. No visibility into positions placed by other brokers.</td>
                    <td>Broker NFT + placement records in Offering Grain</td>
                </tr>
                <tr>
                    <td><strong>Investor</strong></td>
                    <td>Their own position only. Token balance, ownership percentage, lock-up status, distribution history, and CrossConversion status for each offering they hold. No visibility into other investors' positions.</td>
                    <td>Investor wallet signature + InvestorView <span class="glossary-term" data-term="powerbox">Powerbox</span> capability</td>
                </tr>
                <tr>
                    <td><strong>Auditor</strong></td>
                    <td>Read-only access to full cap table and historical snapshots for specified offerings. Can verify on-chain state, export snapshot data, and cross-reference with distribution records. Cannot modify any state.</td>
                    <td>Auditor NFT (time-limited, issued by Trustee)</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="paying-agent">Paying Agent</span></strong></td>
                    <td>Read-only access to cap table for distribution calculation purposes. Sees balances and position indices needed to execute the <span class="glossary-term" data-term="waterfall">waterfall</span> and track claim status.</td>
                    <td>Paying Agent NFT issued by Trustee</td>
                </tr>
            </tbody>
        </table>
        <h3>Powerbox Capability Scoping</h3>
        <p>Access control is enforced at two layers. First, the REST API gateway verifies the caller's role NFT before routing the request to the Offering Grain. Second, the Offering Grain's <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> interface enforces capability-based scoping — an <code>InvestorView</code> capability physically cannot return other investors' data because the interface definition only exposes the requesting investor's position. This is not a permission check that could be bypassed; it is a structural constraint of the capability system.</p>
        <pre><code>Cap Table Access Flow:

Issuer NFT ──► API Gateway ──► Offering Grain
                                   │
                          getCapTable() → Full List(InvestorPosition)

Investor Wallet ──► API Gateway ──► Investor Grain
                                        │
                               InvestorView capability
                                        │
                                   Offering Grain
                                        │
                              Own InvestorPosition only</code></pre>
        <p>The on-chain data itself is publicly readable — anyone with a <a href="/knowledge/glossary/solana/">Solana</a> RPC endpoint can read any PDA. The access control layer governs what the <em>platform API</em> exposes, not what the blockchain stores. This is intentional: the cap table's verifiability guarantee depends on the data being publicly auditable on-chain, while the API layer provides role-appropriate views for operational use.</p>
    </div>
