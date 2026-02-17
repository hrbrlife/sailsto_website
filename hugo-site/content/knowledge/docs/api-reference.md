---
title: "API Reference - Documentation"
description: "The Sails.to REST gateway and Cap'n Proto RPC interfaces — endpoint groups, authentication model, response formats, error handling."
ogImage: "/og-image.png"
keywords: ["API", "REST", "Cap'n Proto", "endpoints", "rate limiting", "NFT authentication", "RPC"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">API Reference</h1>
    <p class="section-desc">Everything the platform exposes — REST endpoints for web clients, Cap'n Proto interfaces for grain-native callers, and the authentication model that gates every request.</p>
</section>

<section class="features-section">
    <div class="container">
        <h2>Overview</h2>
        <p>The Sails.to API lives at <code>api.sails.to</code>. Every endpoint is authenticated via <a href="/knowledge/glossary/solana/">Solana</a> wallet signature and <span class="glossary-term" data-term="nft-hierarchy">NFT</span> role verification. There are no API keys, no OAuth tokens, no username/password flows. Your wallet <em>is</em> your identity. Your NFT <em>is</em> your authorization. The API simply verifies both and routes you to the correct <span class="glossary-term" data-term="grain">grain</span> capability.</p>
        <p>Two access paths exist. Web clients hit the REST gateway and receive JSON responses. Grain-native callers — other grains, the operator service, automated pipelines — use <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> RPC directly over <span class="glossary-term" data-term="powerbox">Powerbox</span> capabilities, with zero-copy serialization and no HTTP overhead. Both paths enforce the same authentication and compliance checks.</p>
        <pre><code>┌──────────────┐     REST/JSON      ┌──────────────────┐
│  Web Client  │ ──────────────────►│                  │
└──────────────┘                    │   API Gateway    │
                                    │  api.sails.to    │──► Grain Capabilities
┌──────────────┐  Cap'n Proto RPC   │                  │
│  Grain / Svc │ ──────────────────►│                  │
└──────────────┘     (FD3)          └──────────────────┘</code></pre>
        <h2>Authentication</h2>
        <p>Every request passes through the platform's four-layer authentication model before reaching any grain. The API gateway enforces the first two layers; the Sandstorm runtime enforces the remaining two:</p>
        <ol>
            <li><strong>Wallet Signature</strong> — Ed25519 signature proving private key ownership. Included in the <code>X-Solana-Signature</code> header alongside the <code>X-Solana-Pubkey</code> header and a timestamp-based nonce to prevent replay attacks.</li>
            <li><strong>NFT Verification</strong> — The gateway inspects the wallet for role-specific NFTs minted by the <span class="glossary-term" data-term="melusina">Melusina</span> authority program. The required NFT tier depends on the endpoint group (see table below). No NFT, no access.</li>
            <li><strong>Sandstorm Session</strong> — OS-level grain isolation, enforced by the runtime.</li>
            <li><strong>Powerbox Capability</strong> — Inter-grain authority via sturdyRef tokens.</li>
        </ol>
        <p>For the complete authentication model — threshold operations, session management, capability persistence — see the <a href="/knowledge/docs/authentication/">Authentication documentation</a>.</p>
        <h2>Endpoint Groups</h2>
        <p>The REST gateway organizes endpoints into six groups, each gated by a specific authentication tier. Public endpoints require no wallet signature. All others require wallet signature plus the appropriate <span class="glossary-term" data-term="nft-hierarchy">role NFT</span>:</p>
        <table>
            <thead>
                <tr>
                    <th>Endpoint Group</th>
                    <th>Auth Requirement</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong><code>/v1/offerings</code></strong></td>
                    <td>Public</td>
                    <td>List active offerings, retrieve offering details, view public <span class="glossary-term" data-term="cap-table">cap table</span> summaries. No authentication required — this is the storefront.</td>
                </tr>
                <tr>
                    <td><strong><code>/v1/kyc</code></strong></td>
                    <td>Wallet signature</td>
                    <td>Start a <span class="glossary-term" data-term="kyc">KYC</span> verification workflow, check case status, retrieve issued credentials. Routes to the KYC/Onboarding grain for the requesting wallet.</td>
                </tr>
                <tr>
                    <td><strong><code>/v1/broker</code></strong></td>
                    <td><span class="glossary-term" data-term="broker-dealer">Broker</span> NFT required</td>
                    <td>Place investors into offerings, list positions for <span class="glossary-term" data-term="secondary-trading">secondary trading</span>, match and settle trades, view commission reports.</td>
                </tr>
                <tr>
                    <td><strong><code>/v1/trustee</code></strong></td>
                    <td><span class="glossary-term" data-term="trustee">Trustee</span> NFT required</td>
                    <td>Authenticate <span class="glossary-term" data-term="crossconversion">CrossConversions</span>, sign reconciliation reports, authenticate <span class="glossary-term" data-term="distributions">distributions</span>, execute emergency freezes.</td>
                </tr>
                <tr>
                    <td><strong><code>/v1/investor</code></strong></td>
                    <td>Investor wallet auth</td>
                    <td>View portfolio, track distributions and yields, request CrossConversions, download tax documents, participate in governance votes.</td>
                </tr>
                <tr>
                    <td><strong><code>/v1/admin</code></strong></td>
                    <td><span class="glossary-term" data-term="master-nft">Master NFT</span> required</td>
                    <td>Platform-wide management — deploy offerings, configure compliance rules, manage operator NFTs, view aggregate analytics. Requires <span class="glossary-term" data-term="threshold-signing">3-of-5 threshold</span> for critical operations.</td>
                </tr>
            </tbody>
        </table>
        <p>Every endpoint group maps to one or more grain types behind the gateway. The <code>/v1/broker</code> group routes to the Broker Portal station grain. The <code>/v1/investor</code> group routes to the caller's individual Investor Self-Service instance grain. The gateway performs the routing — your client never addresses grains directly.</p>
        <h2>Cap'n Proto Interfaces</h2>
        <p>Behind the REST gateway, every operation is a <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> RPC call on a grain capability. These are the core interfaces that grains expose through the <span class="glossary-term" data-term="powerbox">Powerbox</span>. Grain-native callers use these directly; web clients use them indirectly through the REST translation layer.</p>
        <pre><code>interface OfferingAPI {
  subscribe @0 (investor :InvestorCredential, amount :UInt64)
    -> (result :SubscriptionResult);
  getCapTable @1 () -> (investors :List(InvestorPosition));
  requestCrossConversion @2 (direction :ConversionDirection, amount :UInt64)
    -> (request :ConversionRequest);
  claimDistribution @3 (epoch :UInt32) -> (amount :UInt64);
  getOfferingInfo @4 () -> (info :OfferingInfo);
}</code></pre>
        <pre><code>interface KYCVerifier {
  startVerification @0 (investorData :InvestorSubmission)
    -> (caseId :Text);
  getStatus @1 (caseId :Text) -> (status :CaseStatus);
  getCredential @2 (caseId :Text) -> (credential :KYCCredential);
  revokeCredential @3 (caseId :Text, reason :Text) -> (success :Bool);
}</code></pre>
        <pre><code>interface TrusteeAPI {
  authenticateConversion @0 (request :ConversionRequest)
    -> (authenticated :Bool);
  authenticateDistribution @1 (offering :Text, epoch :UInt32)
    -> (authenticated :Bool);
  signReconciliation @2 (report :ReconciliationReport)
    -> (signature :Data);
  freeze @3 (investor :Text, reason :Text) -> (success :Bool);
}</code></pre>
        <pre><code>interface BrokerAPI {
  placeInvestor @0 (offering :Text, investor :InvestorCredential,
    amount :UInt64) -> (result :PlacementResult);
  listForSecondaryTrading @1 (offering :Text, amount :UInt64,
    price :UInt64) -> (listing :TradeListing);
  matchTrade @2 (listing :TradeListing, buyer :InvestorCredential)
    -> (settlement :TradeSettlement);
}</code></pre>
        <pre><code>interface GovernanceAPI {
  createProposal @0 (title :Text, description :Text,
    actions :List(GovernanceAction)) -> (proposalId :Text);
  vote @1 (proposalId :Text, vote :VoteChoice, weight :UInt64)
    -> (success :Bool);
  executeProposal @2 (proposalId :Text) -> (result :ExecutionResult);
  getProposals @3 () -> (proposals :List(Proposal));
}</code></pre>
        <p>Each <code>@N</code> annotation is the Cap'n Proto method ordinal — stable across schema evolution, ensuring backward compatibility as interfaces grow. New methods are added with new ordinals; existing ordinals never change. For details on how these interfaces connect through capability grants, see the <a href="/knowledge/docs/platform-overview/">Platform Overview</a>.</p>
        <h2>Response Format</h2>
        <p>The API supports two serialization formats, selected by the caller:</p>
        <ul>
            <li><strong>Cap'n Proto (native)</strong> — Zero-copy deserialization. No parsing overhead. This is what grain-to-grain calls use natively over FD3. Request it from the REST gateway with <code>Accept: application/capnp</code>.</li>
            <li><strong>JSON (web fallback)</strong> — Standard JSON over HTTP for browser clients, cURL, and any tooling that doesn't speak Cap'n Proto. This is the default when no <code>Accept</code> header is specified.</li>
        </ul>
        <p>JSON responses follow a consistent envelope:</p>
        <pre><code>{
  "ok": true,
  "data": { ... },
  "meta": {
    "request_id": "req_7f3a8b2c4d5e",
    "grain_id": "grain_xk9p2m4n7r",
    "timestamp": 1718000000
  }
}</code></pre>
        <p>For list endpoints, the <code>data</code> field contains an array and <code>meta</code> includes pagination cursors. The platform does not use offset-based pagination — all list endpoints use opaque cursor tokens for stable iteration over changing datasets.</p>
        <h2>Error Handling</h2>
        <p>Failed requests return a structured error response with a machine-readable code, a human-readable message, and — for <span class="glossary-term" data-term="compliance">compliance</span> violations — the specific rule that was violated:</p>
        <pre><code>{
  "ok": false,
  "error": {
    "code": "COMPLIANCE_VIOLATION",
    "message": "Transfer rejected: receiver KYC credential expired",
    "details": {
      "rule": "kyc_validity",
      "receiver": "7xK9...",
      "credential_expired_at": 1717200000
    }
  },
  "meta": {
    "request_id": "req_8b2c...",
    "timestamp": 1718000000
  }
}</code></pre>
        <p>Standard error codes:</p>
        <table>
            <thead>
                <tr>
                    <th>Code</th>
                    <th>HTTP Status</th>
                    <th>Meaning</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>AUTH_SIGNATURE_INVALID</code></td>
                    <td>401</td>
                    <td>Wallet signature verification failed or nonce expired.</td>
                </tr>
                <tr>
                    <td><code>AUTH_NFT_MISSING</code></td>
                    <td>403</td>
                    <td>Wallet does not hold the required role NFT for this endpoint.</td>
                </tr>
                <tr>
                    <td><code>AUTH_NFT_EXPIRED</code></td>
                    <td>403</td>
                    <td>Role NFT has expired and must be reissued by the authority.</td>
                </tr>
                <tr>
                    <td><code>COMPLIANCE_VIOLATION</code></td>
                    <td>422</td>
                    <td>Operation rejected by on-chain compliance rules. The <code>details</code> field identifies the specific rule (KYC expiry, jurisdiction mismatch, lock-up period, investor cap).</td>
                </tr>
                <tr>
                    <td><code>RATE_LIMITED</code></td>
                    <td>429</td>
                    <td>Request rate exceeded for your NFT tier. Retry after the interval in the <code>Retry-After</code> header.</td>
                </tr>
                <tr>
                    <td><code>RESOURCE_NOT_FOUND</code></td>
                    <td>404</td>
                    <td>The requested offering, investor, or resource does not exist.</td>
                </tr>
                <tr>
                    <td><code>THRESHOLD_REQUIRED</code></td>
                    <td>403</td>
                    <td>Operation requires <span class="glossary-term" data-term="threshold-signing">multi-signature threshold</span> approval (e.g., 3-of-5 for Master NFT operations).</td>
                </tr>
                <tr>
                    <td><code>INTERNAL_ERROR</code></td>
                    <td>500</td>
                    <td>Unexpected grain or system failure. Logged to the audit trail automatically.</td>
                </tr>
            </tbody>
        </table>
        <p>Every error — including compliance violations and authentication failures — is logged to the grain's append-only audit journal. See the <a href="/knowledge/docs/compliance-framework/">Compliance Framework</a> for details on audit trail retention and regulatory reporting.</p>
        <h2>Rate Limits</h2>
        <p>Rate limits are enforced per wallet, scaled by <span class="glossary-term" data-term="nft-hierarchy">NFT</span> tier. Higher-authority roles get higher limits because their operations are inherently lower-volume and higher-value. Public endpoints have the tightest limits to prevent abuse:</p>
        <table>
            <thead>
                <tr>
                    <th>NFT Tier</th>
                    <th>Requests / Minute</th>
                    <th>Burst</th>
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Public</strong> (no auth)</td>
                    <td>30</td>
                    <td>10</td>
                    <td>Offerings list and detail only. IP-based limiting.</td>
                </tr>
                <tr>
                    <td><strong>Investor</strong></td>
                    <td>60</td>
                    <td>20</td>
                    <td>Portfolio, distributions, tax documents.</td>
                </tr>
                <tr>
                    <td><strong>Broker</strong></td>
                    <td>120</td>
                    <td>40</td>
                    <td>Placement, trading, commission reporting.</td>
                </tr>
                <tr>
                    <td><strong>Trustee</strong></td>
                    <td>120</td>
                    <td>40</td>
                    <td>Authentication, reconciliation, freeze operations.</td>
                </tr>
                <tr>
                    <td><strong>Platform Operator</strong></td>
                    <td>300</td>
                    <td>100</td>
                    <td>Offering deployment, configuration, operator management.</td>
                </tr>
                <tr>
                    <td><strong>Master NFT</strong></td>
                    <td>300</td>
                    <td>100</td>
                    <td>Unrestricted admin access. Still rate-limited to prevent runaway automation.</td>
                </tr>
            </tbody>
        </table>
        <p>When a rate limit is hit, the API returns a <code>429</code> with a <code>Retry-After</code> header indicating the number of seconds to wait. Burst allowance permits short spikes above the per-minute rate — useful for Broker batch placements or Investor portfolio refreshes — but sustained traffic above the limit will be throttled.</p>
        <p>Cap'n Proto RPC calls between grains are <strong>not</strong> subject to these rate limits. Rate limiting applies only to the REST gateway. Grain-to-grain calls are governed by Powerbox capability grants — if you hold the capability, you can call it. The Sandstorm runtime handles backpressure at the OS level.</p>
    </div>
</section>
