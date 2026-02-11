---
title: "KYC Integration - Documentation"
description: "KYC as a grain, not a service — the 10-step verification workflow, investor classifications, credential NFT lifecycle, Cap'n Proto interface, and Powerbox integration points."
ogImage: "/og-image.png"
keywords: ["KYC", "investor onboarding", "credential NFT", "accredited investor", "verification workflow", "Cap'n Proto", "Powerbox"]
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/docs.css"
draft: false
---

<section class="page-hero">
    <span class="section-label">Documentation</span>
    <h1 class="section-title">KYC Integration</h1>
    <p class="section-desc">Every verification is an isolated grain — 10 steps from terms acceptance to on-chain credential, with zero PII touching the blockchain.</p>
</section>

<section class="features-section">
    <div class="container">
        <h2>Overview</h2>
        <p><span class="glossary-term" data-term="kyc">KYC</span> on Sails.to is a <span class="glossary-term" data-term="grain">grain</span>, not a service. Each investor verification spawns an isolated Instance grain — a single-purpose, sandboxed process that owns its own encrypted journal, its own state machine, and its own lifecycle. When the verification completes, the grain mints an on-chain credential and can be archived. When it fails, the grain retains the audit trail and nothing else.</p>
        <p>This architecture comes directly from the <span class="glossary-term" data-term="bloom">BLOOM_FINAL</span> specification: the KYC/Investor Onboarding Grain is an Instance-type grain, one per verification, implemented in Go+HTMX as a native Sandstorm grain. The verification workflow is a 10-step state machine that moves an investor from anonymous visitor to on-chain credentialed participant. Every step is logged. Every transition is irreversible. Every piece of personally identifiable information stays inside the grain's encrypted journal — never on-chain, never in a shared database, never accessible to any other grain without an explicit <span class="glossary-term" data-term="powerbox">Powerbox</span> capability grant.</p>
        <p>The KYC grain integrates with external data providers (Onfido, Jumio, or equivalent) for document verification and biometric matching, but the grain itself is the system of record. If the external provider goes down, the grain queues the verification step and retries. If the provider returns an ambiguous result, the grain escalates to human review. The grain is the authority — the provider is a tool.</p>
        <h2>The 10-Step Verification Flow</h2>
        <p>The verification workflow is a strict, ordered state machine. Each step must complete before the next begins. There is no skipping, no reordering, no partial completion. The grain tracks the current step in its journal, and the state machine is deterministically replayable from the journal log.</p>
        <h3>Step 1: Terms Acceptance</h3>
        <p>The investor is presented with the platform's terms of service, privacy policy, and electronic consent agreements. The UI enforces a full scroll-through of each document before the acceptance checkbox becomes active. This is not a rubber stamp — the grain logs the exact document versions presented, the scroll completion timestamps, and the acceptance timestamp. Regulatory counsel requires proof that the investor was shown the terms, not just that they clicked a box.</p>
        <h3>Step 2: Email Verification</h3>
        <p>A one-time password (OTP) is sent to the investor's email address. The grain generates the OTP, stores its hash in the journal, and validates the investor's response. The OTP expires after a configurable window (default: 10 minutes). Failed attempts are rate-limited. The email address, once verified, becomes the primary contact channel for all subsequent notifications — KYC status updates, credential expiration warnings, and offering communications.</p>
        <h3>Step 3: Phone Verification</h3>
        <p>A second OTP is sent via SMS to the investor's phone number. Same pattern as email: OTP generation, hash storage, expiry window, rate limiting. Phone verification serves dual purpose — it validates the investor's contact information and provides a second factor for future sensitive operations. The phone number is stored only in the grain's encrypted journal.</p>
        <h3>Step 4: Document Upload</h3>
        <p>The investor uploads identity documents: a government-issued photo ID (passport, national ID card, or driver's license) and proof of address (utility bill, bank statement, or government correspondence dated within 90 days). Documents are stored in the grain's encrypted journal — never in a shared filesystem, never in cloud storage accessible to other grains. The grain validates file formats and sizes before accepting the upload.</p>
        <h3>Step 5: Face Capture</h3>
        <p>The investor captures a selfie and completes a liveness check. The liveness detection ensures the investor is physically present — not a photograph of a photograph, not a video replay, not a deepfake. The grain captures multiple frames and sends them to the biometric provider for liveness scoring. The selfie image is stored in the grain's encrypted journal alongside the liveness score.</p>
        <h3>Step 6: AI Processing</h3>
        <p>The grain dispatches document images and selfie data to the external verification provider for automated analysis. Three checks run in parallel: <strong>OCR extraction</strong> (reading name, date of birth, document number, and expiry from the ID), <strong>face matching</strong> (comparing the selfie to the photo on the ID document), and <strong>document verification</strong> (checking for tampering, expiry, and format validity). Results are stored in the journal with confidence scores. If any score falls below the configured threshold, the grain escalates to Step 9 (Respondent Review) rather than rejecting outright.</p>
        <h3>Step 7: Risk Assessment</h3>
        <p>The grain performs regulatory risk screening. This includes <strong>jurisdiction analysis</strong> (mapping the investor's country of residence to applicable regulatory regimes), <strong>PEP screening</strong> (checking the investor against politically exposed persons databases), and <strong>sanctions screening</strong> (checking against OFAC, EU, and UN sanctions lists). A positive hit on any sanctions list is an automatic rejection. A PEP hit triggers enhanced due diligence and mandatory Respondent Review. Jurisdiction analysis determines which regulatory exemptions and offering types the investor can access.</p>
        <h3>Step 8: Accreditation Verification</h3>
        <p>For offerings under <span class="glossary-term" data-term="reg-d">Reg D</span> 506(b) or 506(c), the investor must demonstrate <span class="glossary-term" data-term="accredited-investor">accredited investor</span> status. The grain collects income documentation (tax returns, W-2s, or third-party verification letters for income-based qualification) or asset documentation (bank statements, brokerage statements, or third-party verification for net-worth-based qualification). For 506(c) offerings, the verification must be performed by an independent third party — the platform cannot self-certify. The grain stores the verification method, the verifier identity, and the result. For Reg A and Reg CF offerings, this step is skipped automatically.</p>
        <h3>Step 9: Respondent Review</h3>
        <p>A human compliance officer (the "Respondent") reviews the verification case. This step is mandatory for PEP hits, low AI confidence scores, document discrepancies, and enhanced due diligence cases. It is also triggered randomly for a configurable percentage of standard verifications (default: 10%) as a quality control measure. The Respondent sees the full case file — documents, AI results, risk assessment — within the KYC grain's UI. They can approve, reject, or request additional information from the investor. Every Respondent action is logged with the officer's identity and timestamp.</p>
        <h3>Step 10: Approval → Mint KYC NFT</h3>
        <p>On approval, the grain triggers the minting of a <span class="glossary-term" data-term="kyc">KYC</span> Credential NFT on <a href="/knowledge/glossary/solana/">Solana</a>. The NFT is minted by the KYC Issuer's License NFT (a <span class="glossary-term" data-term="nft-hierarchy">pNFT</span> in the <span class="glossary-term" data-term="melusina">Melusina</span> hierarchy) to the investor's wallet. The NFT contains zero PII — only classification flags and cryptographic attestations. The grain then links the credential to any pending Offering Grains via <span class="glossary-term" data-term="powerbox">Powerbox</span> capability grants, enabling the investor to participate in offerings immediately.</p>
        <pre><code>Verification State Machine:
┌─────────────────────────────────────────────────────────────────────┐
│  terms_accepted → contact_verification → document_upload →          │
│  face_capture → ai_processing → risk_assessment →                   │
│  accreditation → respondent_review → approved → nft_minted          │
│                                                                     │
│  Any step may transition to: rejected, expired, or pending_info     │
└─────────────────────────────────────────────────────────────────────┘

Cap'n Proto Status Enum:
enum CaseStatus {
    draft, termsAccepted, contactVerification, documentUpload,
    faceCapture, aiProcessing, riskAssessment, accreditation,
    respondentReview, approved, rejected, expired
}</code></pre>
        <h2>Investor Classifications</h2>
        <p>The KYC grain assigns an <code>investor_class</code> based on the verification results and accreditation documentation. This classification is encoded in the KYC Credential NFT and determines which offerings the investor can access. The <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> enforces these restrictions on every mint and every transfer — there is no way to circumvent the classification at the application layer.</p>
        <table>
            <thead>
                <tr>
                    <th>Classification</th>
                    <th>Qualification</th>
                    <th>Eligible Offerings</th>
                    <th>Investor Limits</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Accredited</strong></td>
                    <td>Income &gt;$200K (individual) or &gt;$300K (joint) for 2 consecutive years; or net worth &gt;$1M excluding primary residence</td>
                    <td><span class="glossary-term" data-term="reg-d">Reg D</span> 506(b), Reg D 506(c), Reg A, Reg CF, <span class="glossary-term" data-term="reg-s">Reg S</span></td>
                    <td>No investment caps</td>
                </tr>
                <tr>
                    <td><strong>Professional</strong></td>
                    <td>Registered investment adviser, licensed broker-dealer, bank, insurance company, or other institutional entity</td>
                    <td>All offering types including institutional tranches</td>
                    <td>No investment caps</td>
                </tr>
                <tr>
                    <td><strong>QualifiedPurchaser</strong></td>
                    <td>Individual or family entity with &gt;$5M in investments; or entity with &gt;$25M in investments</td>
                    <td>All offering types including 3(c)(7) exempt funds</td>
                    <td>No investment caps</td>
                </tr>
                <tr>
                    <td><strong>Retail</strong></td>
                    <td>Basic KYC verification completed; no accreditation documentation</td>
                    <td>Reg A (Tier 1 and Tier 2), Reg CF</td>
                    <td>Reg CF: max $2,500 or 5% of income/net worth (whichever is greater) if income &lt;$124K; 10% if income &gt;$124K</td>
                </tr>
            </tbody>
        </table>
        <p>Classifications are not permanent. An investor who was Retail at initial verification can submit accreditation documentation later to upgrade to Accredited. The KYC grain spawns a new verification instance for the upgrade, and on approval, a new KYC Credential NFT is minted (the old one is revoked). Downgrades are automatic — if an investor's credential expires and they re-verify without accreditation documentation, they are classified as Retail regardless of their prior status.</p>
        <h2>KYC Credential NFT</h2>
        <p>The credential minted on approval is a <span class="glossary-term" data-term="nft-hierarchy">programmable NFT</span> (pNFT) in the <span class="glossary-term" data-term="melusina">Melusina</span> hierarchy, issued by a licensed KYC Issuer's License NFT. It is the on-chain proof that an investor has passed verification — and it contains absolutely no personally identifiable information:</p>
        <pre><code>KYC NFT Metadata (on-chain, no PII):
├── investor_class: enum { Accredited, Professional, QualifiedPurchaser, Retail }
├── jurisdiction_hash: [u8; 32]       // SHA-256 of ISO 3166 country code
├── reg_exemption: enum { RegD506b, RegD506c, RegS, RegA, RegCF }
├── verification_level: enum { Basic, Enhanced, InstitutionalEDD }
├── issued_by: Pubkey                 // KYC Issuer's License NFT public key
├── issued_at: i64                    // Unix timestamp of issuance
├── expires_at: i64                   // Credential expiration timestamp
├── aml_clear: bool                   // Anti-money laundering clearance
└── pep_clear: bool                   // Politically exposed person clearance</code></pre>
        <p>The <code>jurisdiction_hash</code> is a SHA-256 hash of the investor's ISO 3166 country code. The blockchain reveals nothing about the investor's location — but the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> can still enforce jurisdiction whitelists by comparing hashes against the offering's <code>ComplianceConfig</code> allowed list. This is privacy by design: the minimum information necessary for compliance enforcement, and nothing more.</p>
        <p>The <code>verification_level</code> reflects the depth of due diligence performed. <strong>Basic</strong> covers standard KYC (identity + address). <strong>Enhanced</strong> adds source-of-funds verification for high-value investors. <strong>InstitutionalEDD</strong> is full enhanced due diligence for institutional entities — beneficial ownership analysis, corporate structure verification, and ultimate beneficial owner identification.</p>
        <p>The NFT is <strong>recallable</strong>. The issuing KYC Issuer (or the Platform Operator via <span class="glossary-term" data-term="threshold-signing">3-of-5 threshold</span>) can revoke the credential at any time. Revocation is immediate — the Transfer Hook will reject any operation involving a revoked credential on the next transaction.</p>
        <h2>Credential Lifecycle</h2>
        <p>KYC credentials are not permanent. They follow a strict lifecycle managed jointly by the KYC grain (off-chain state) and the Melusina program (on-chain state):</p>
        <h3>Issuance</h3>
        <p>On verification approval (Step 10), the KYC grain calls the <span class="glossary-term" data-term="melusina">Melusina</span> program's <code>mintKyc</code> instruction via the KYC Issuer's License NFT. The credential is minted to the investor's wallet with all metadata fields populated from the verification results. The <code>expires_at</code> field is set based on the investor's risk profile and jurisdiction — standard credentials expire after 12 months, enhanced credentials after 24 months, and high-risk jurisdictions may require 6-month renewal.</p>
        <h3>Expiration</h3>
        <p>The KYC grain monitors credential expiration proactively. At 60 days before expiry, the investor receives a re-verification notification. At 30 days, a reminder. At expiry, the on-chain credential becomes invalid — the <span class="glossary-term" data-term="transfer-hook">Transfer Hook</span> checks <code>expires_at</code> against the current slot time and rejects any operation with an expired credential. The investor's existing holdings are not affected (they still own the tokens), but they cannot transfer, sell, or participate in new offerings until re-verified.</p>
        <h3>Re-Verification</h3>
        <p>Re-verification spawns a new KYC grain instance. The workflow may be abbreviated if the investor's risk profile hasn't changed — Steps 1-3 (terms, email, phone) can be pre-populated from the prior verification, and Steps 4-5 (document, face) may be skipped if the original documents are still valid and the investor's appearance hasn't changed beyond the face-match threshold. Steps 6-10 always run in full. On approval, a new credential NFT is minted and the old one is revoked in a single atomic transaction.</p>
        <h3>Revocation</h3>
        <p>Credentials can be revoked before expiration for cause: adverse information discovered after issuance, sanctions list updates, regulatory orders, or investor request. Revocation is executed by the KYC Issuer's License NFT or by the Platform Operator's <span class="glossary-term" data-term="threshold-signing">3-of-5 threshold</span> ceremony. The on-chain credential is marked as revoked, the KYC grain logs the reason and the revoking authority, and any pending operations involving the investor are halted. Revocation is permanent for that credential — the investor must complete a full re-verification to obtain a new one.</p>
        <h2>Cap'n Proto Interface</h2>
        <p>The KYC grain exposes its functionality through a <span class="glossary-term" data-term="cap-n-proto">Cap'n Proto</span> RPC interface. This is the programmatic API that other grains use to interact with KYC verification — there is no REST API, no GraphQL endpoint, no shared database. Inter-grain communication is exclusively via Cap'n Proto over the <span class="glossary-term" data-term="powerbox">Powerbox</span> capability system:</p>
        <pre><code># sails/kyc.capnp (extends BLOOM's capnp/kyc.capnp)

interface KYCVerifier {
    startVerification @0 (investorData :InvestorSubmission) -> (caseId :Text);
    # Spawns a new KYC grain instance for the investor.
    # Returns the case ID used to track the verification through all 10 steps.
    # The InvestorSubmission contains the investor's wallet address and
    # initial contact information (email, phone) — no PII is stored
    # outside the spawned grain.
    getStatus @1 (caseId :Text) -> (status :CaseStatus);
    # Returns the current step in the verification state machine.
    # Callable by any grain holding a valid KYCVerifier capability.
    # Does not expose any PII — only the status enum value.
    getCredential @2 (caseId :Text) -> (credential :KYCCredential);
    # Returns the on-chain credential metadata for a completed verification.
    # Only returns data after the verification reaches the "approved" state
    # and the NFT has been minted. The KYCCredential struct contains the
    # same fields as the on-chain NFT metadata — no PII.
    revokeCredential @3 (caseId :Text, reason :Text) -> (success :Bool);
    # Revokes an active credential. Requires the caller to hold a
    # KYC Issuer capability or Platform Operator authority.
    # Triggers on-chain revocation via the Melusina program and logs
    # the reason to the grain's audit journal.
}</code></pre>
        <p>The <code>startVerification</code> method is the entry point. It creates a new KYC grain instance, initializes the state machine at Step 1 (terms acceptance), and returns a case ID. The calling grain (typically the Investor Self-Service grain or the Broker Portal grain) uses this case ID to track progress via <code>getStatus</code> and to retrieve the credential via <code>getCredential</code> once the verification completes.</p>
        <p>The <code>revokeCredential</code> method is restricted. Only grains holding a KYC Issuer capability or Platform Operator authority can call it. The <span class="glossary-term" data-term="powerbox">Powerbox</span> enforces this — a Broker grain or Investor grain that holds a read-only <code>getStatus</code> capability cannot escalate to revocation. Capabilities are fine-grained, and the Cap'n Proto interface enforces the boundary.</p>
        <h2>Integration Points</h2>
        <p>The KYC grain does not operate in isolation. It connects to the broader Sails.to grain ecosystem through the <span class="glossary-term" data-term="powerbox">Powerbox</span> capability system — the same claim-token-to-sturdyRef lifecycle that governs all inter-grain communication on the platform.</p>
        <h3>KYC Grain → Offering Grain</h3>
        <p>When a KYC verification completes and the credential NFT is minted, the KYC grain offers the credential to the relevant Offering Grains via Powerbox. The Offering Grain maintains an investor whitelist — a set of wallet addresses with valid KYC credentials that are eligible to participate. The KYC grain's Powerbox offer includes the investor's wallet address, investor class, and jurisdiction hash (the same on-chain metadata, no PII). The Offering Grain claims this capability and adds the investor to its whitelist. This is how an investor becomes eligible to subscribe to an offering.</p>
        <pre><code>Powerbox Capability Flow:

KYC Grain ──(Powerbox offer: KYC result)──► Offering Grain
    │                                            │
    │  Contains: wallet, investor_class,         │  Updates: investor whitelist,
    │  jurisdiction_hash, verification_level      │  checks ComplianceConfig eligibility
    │                                            │
    └──(Powerbox offer: KYC result)──► Broker Grain
                                            │
                                            │  Caches: investor eligibility
                                            │  for placement operations</code></pre>
        <h3>Broker Grain → KYC Grain</h3>
        <p><span class="glossary-term" data-term="broker-dealer">Broker</span> grains request KYC credentials when placing investors into offerings. The Broker holds a read-only <code>getStatus</code> and <code>getCredential</code> capability on the KYC grain (granted via Powerbox by the Platform Operator). Before executing a placement, the Broker grain calls <code>getCredential</code> to verify the investor's current KYC status, classification, and jurisdiction. If the credential has expired or been revoked since the last check, the placement is rejected and the Broker is notified to initiate re-verification.</p>
        <h3>Investor Self-Service Grain → KYC Grain</h3>
        <p>The Investor Self-Service grain is the primary UI for individual investors. When a new investor signs up, the Self-Service grain calls <code>startVerification</code> on the KYCVerifier interface to spawn a KYC grain instance. The Self-Service grain then embeds the KYC grain's HTMX-rendered UI directly — each step of the 10-step workflow is rendered by the KYC grain and served to the investor through the Self-Service grain's iframe. The Self-Service grain polls <code>getStatus</code> to update its own UI (showing progress indicators, enabling offering browsing on completion).</p>
        <h3>DAO Manager Grain → KYC Grain</h3>
        <p>The DAO Manager grain (used by Issuers and Platform Operators) holds administrative capabilities on KYC grains. It can view verification statistics, trigger bulk re-verification campaigns for expiring credentials, and invoke <code>revokeCredential</code> when compliance officers identify issues. The DAO Manager receives KYC status change events via Powerbox — every approval, rejection, and expiration is surfaced in the operator dashboard for compliance monitoring.</p>
        <h3>Solana Event Watcher → KYC Grain</h3>
        <p>The credential minting and revocation happen on-chain via the <span class="glossary-term" data-term="melusina">Melusina</span> program. The Solana Event Watcher grain monitors the chain for KYC-related events (<code>KycMinted</code>, <code>KycRevoked</code>) and routes confirmations back to the originating KYC grain. This closes the loop — the grain initiates the mint, the on-chain program executes it, the Event Watcher confirms it, and the grain updates its journal. If the on-chain transaction fails (insufficient SOL, network congestion), the grain retries with exponential backoff.</p>
    </div>
</section>
