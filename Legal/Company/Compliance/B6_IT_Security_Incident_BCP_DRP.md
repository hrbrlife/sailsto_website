# IT SECURITY, INCIDENT RESPONSE, AND BCP/DR POLICY
## [TERM:Company] CCASH MONEY SERVICES (US) SERIES LLC

<!-- schema:doc DOC:B6 version:1.4 -->
<!-- schema:category Compliance -->
<!-- schema:requires B1,B3,B4,B5,B7,B8,B10,F2 -->

---

**Version:** 1.4
**Effective Date:** December 12, 2025

**Adopted By:** [TERM:Manager] Resolution

---

## VERSION HISTORY

| Version | Date | Author | Summary of Changes | Breaking Change |
|---------|------|--------|-------------------|-----------------|
| 1.0 | December 12, 2025 | Management | Initial version | — |
| 1.1 | December 15, 2025 | Omissions Closure | Added payment card data controls and PCI DSS requirements | No |
| 1.2 | December 15, 2025 | Audit Remediation | Extended log retention to 5 years (§4.3); added series separation (§4.4); added breach notification procedures (§6.8); updated schema requires to include B7 | No |
| 1.3 | December 15, 2025 | Audit Remediation | Added IT designee succession (§6.1); vendor DPA requirements (§8.2A); AI consent/legal basis (§10.4A) | No |
| 1.4 | December 21, 2025 | Privacy Architecture | Reframed breach notification, DPA, and AI legal basis language to jurisdiction-neutral standards; aligned with B8 Part II triggers; updated schema version | No |

---

**Definitions:** Unless otherwise defined herein, capitalized terms have the meanings set forth in the [TERM:Master_Operating_Agreement] [DOC:B1].

---

## SECTION 1: PURPOSE AND SCOPE

1.1. This Policy establishes IT security, incident response, business continuity, and disaster recovery standards for all [TERM:Series], with specific controls for [TERM:Series_T2] custody operations and [TERM:Series_T4] infrastructure.

1.2. This Policy applies to all [TERM:Officers], employees, contractors, and service providers who access [TERM:Company] systems, data, wallets, or production environments.

---

## SECTION 2: ACCESS CONTROL
[FLOW:Access_Control]

2.1. Access to systems and wallets shall follow least privilege and role-based access control.

2.2. Multi-factor authentication is required for all administrative access, production systems, cloud consoles, code repositories, and wallet management tools.

2.3. User access reviews shall occur quarterly and upon role change or termination.

---

## SECTION 3: CHANGE MANAGEMENT
[FLOW:Change_Management]

3.1. All production changes shall be documented, peer-reviewed, tested, and approved before deployment.

3.2. Emergency changes shall be logged, reviewed retrospectively within two business days, and approved by the [TERM:CTO] or designee.

---

## SECTION 4: LOGGING AND ALERTING

4.1. System, authentication, and wallet activity logs shall be collected centrally with time synchronization.

4.2. Alerts shall be configured for privileged access, configuration changes, failed logins, wallet movements, and security control failures.

4.3. **Logs shall be retained for at least five years and protected from alteration.** This retention period aligns with BSA record-keeping requirements under 31 CFR §1010.410 and §1010.430. Logs may be archived to cost-effective storage after twelve months, provided they remain accessible and retrievable within 48 hours for regulatory examination.
[DOC:B4] <!-- Record-Keeping Policy -->
[OBL:OBL-BSA-001] <!-- BSA 5-year retention -->

4.4. **Series Separation in Logs.** To preserve the liability shield under MCA §35-8-304, all logs shall include a [TERM:Series] identifier tag for transactions, activities, and events attributable to a specific series. Centralized log systems shall implement:
   (a) Series-tagged log entries enabling filtering by [TERM:Series] designation;
   (b) Role-based access controls limiting log queries to authorized personnel for each series;
   (c) Partitioned storage or logical separation where required for regulatory or contractual purposes.
[DOC:B4] <!-- Record-Keeping Policy, §7 Series Separation -->

---

## SECTION 5: KEY MANAGEMENT FOR T-2 WALLETS
[FLOW:Key_Management]

5.1. Private keys shall use multi-signature or threshold schemes where supported.

5.2. Cold storage keys shall be stored in tamper-evident, access-controlled environments with dual control for access.

5.3. Hot wallet keys shall be held in hardened HSM or equivalent secure enclave, with transaction limits and alerts.

5.4. Key ceremonies and key rotations shall be documented, with separation of duties between key custodians.

---

## SECTION 6: INCIDENT RESPONSE
[FLOW:Incident_Response]

6.1. The Incident Response Lead is the [TERM:CTO] or designee; the [TERM:CCO] joins for compliance-impacting incidents; the [TERM:CEO] handles external communications.

**IT-Specific Designees.** If the CTO is unavailable, the following succession applies per [DOC:B3] §5-6:
   (a) **Primary Designee:** Senior Engineer or Lead DevOps Engineer, as identified in the Technology Operations runbook maintained by [TERM:Series_T4];
   (b) **Secondary Designee:** CEO or Manager, with authority to engage qualified external incident response consultants;
   (c) **Activation Trigger:** Designee activation occurs automatically if CTO is unreachable for more than two (2) hours during a high-severity incident;
   (d) **Runbook Access:** IT designees shall have pre-provisioned access to incident response runbooks, key ceremony procedures, and emergency contact lists, tested quarterly per §11.2.

6.2. Incidents shall be classified by severity and triaged within one hour of detection for high severity.

6.3. Standard steps include detection, containment, eradication, recovery, and post-incident review with documented lessons learned.

6.4. Evidence shall be preserved for forensic analysis and regulatory inquiries.
[DOC:B4]

6.5. Notification protocols shall follow regulatory requirements and contractual obligations; the [TERM:CCO] determines if SAR or other regulatory filings are triggered.
[DOC:B5] <!-- BSA/AML Program -->

6.6. In the event of a security incident resulting in potential loss of client funds or assets, the [TERM:Company] shall: (a) promptly notify affected clients within seventy-two hours of confirmed loss or as required by applicable law, whichever is sooner; (b) notify regulatory authorities as required; (c) prioritize using available insurance proceeds to compensate losses; and (d) at its discretion, contribute additional [TERM:Company] capital to remediate losses beyond insurance coverage, subject to the loss allocation provisions set forth in the [DOC:B10] Insurance, Capital, and Cash Management Policy; and (e) cooperate in good faith with clients on reimbursement plans and investigation.

6.7. The [TERM:CEO] shall be responsible for crisis communications, including client notifications, press statements, and regulatory correspondence, with input from the [TERM:CCO] and legal counsel.

6.8. **Personal Data Breach Notification (Applicable Law).** In the event of a security incident involving personal data:
   (a) **Risk Assessment**: The [TERM:CCO] shall conduct a risk assessment within twenty-four (24) hours of breach awareness to determine likelihood of risk to individuals' rights and interests;
   (b) **Supervisory Authority Notification**: Where required by applicable data protection law, the [TERM:Company] shall notify the relevant supervisory authority within seventy-two (72) hours of becoming aware of the breach, or within any shorter period required by law. When the International Data Protection Addendum in [DOC:B8] applies, this may include EEA, UK, or Swiss regulators;
   (c) **Individual Notification**: Where required by applicable law and where a breach is likely to result in high risk to individuals, the [TERM:Company] shall notify affected individuals without undue delay;
   (d) **California Consumer Notification**: For breaches affecting California residents involving unencrypted personal information, notification shall occur in the most expedient time possible and without unreasonable delay, per Cal. Civ. Code §1798.82. If more than 500 California residents are affected, the California Attorney General shall be notified;
   (e) **Documentation**: All breach assessments, notifications, and response actions shall be documented and retained per [DOC:B4] for at least five (5) years;
   (f) **Cross-Reference**: See [DOC:B8] Privacy and Data Protection Policy for additional data protection requirements.

---

## SECTION 7: BUSINESS CONTINUITY AND DISASTER RECOVERY
[FLOW:BCP_DRP]

7.1. Critical systems and data shall have daily backups with encryption in transit and at rest, stored in at least two geographic locations.

7.2. Restore tests shall occur at least quarterly and be documented with results and remediation of failures.

7.3. Recovery time objectives and recovery point objectives shall be defined for critical systems and wallets; [TERM:Series_T2] and [TERM:Series_T4] shall maintain runbooks to meet these objectives.

7.4. A continuity communication plan shall identify primary and backup channels for executives, regulators, banking partners, and key vendors.

7.5. Alternate processing procedures shall be documented for payment processing, custody operations, and compliance monitoring during outages.

7.6. Banking partner contingency: The [TERM:Company] shall maintain pre-vetted relationships with at least two banking partners where feasible. In the event of banking partner loss, the Business Continuity Plan shall include procedures to transition client operations to backup banking partners within a reasonable timeframe, not to exceed thirty days for critical functions.

---

## SECTION 8: VENDOR AND THIRD-PARTY SECURITY

8.1. Vendors with access to systems or data shall undergo security due diligence, including review of certifications, penetration test reports, and incident history.

8.2. Contracts shall include security, confidentiality, breach notification timelines, and audit rights appropriate to risk.

**8.2A. Data Processing Agreements (DPAs).** Vendors processing personal data on behalf of the [TERM:Company] shall execute a Data Processing Agreement that includes:
   (a) Subject matter, duration, nature, and purpose of processing;
   (b) Types of personal data and categories of data subjects;
   (c) Obligation to process only on documented instructions from the Company;
   (d) Confidentiality commitments for personnel processing personal data;
   (e) Technical and organizational security measures appropriate to the risk and required by applicable law;
   (f) Conditions for sub-processor engagement and approval;
   (g) Assistance with data subject rights requests;
   (h) Audit rights and cooperation with audits;
   (i) Data return or deletion upon termination;
   (j) Cross-border transfer mechanisms where required, aligned with [DOC:B8] Part II.
[DOC:B8] <!-- Privacy and Data Protection Policy §7 -->

8.3. **Payment Card Data and PCI DSS.** The [TERM:Company] and [TERM:ClientSeries] shall not store, process, or transmit payment card data (PAN, CVV, track data) on Company systems unless expressly approved in writing by the [TERM:CTO] and [TERM:CCO] following a PCI scoping assessment. [OBL:PCI-DSS-001]

8.4. **Tokenization Requirement.** Where card acceptance is supported, card data must be handled exclusively by a PCI DSS–compliant third-party payment processor using tokenization. Company systems may store processor tokens and last-four digits, but not full PAN or sensitive authentication data.

8.5. **PCI Compliance Ownership.** Client remains responsible for its own PCI DSS compliance for any card acceptance in its channels, including merchant onboarding, SAQ scope, and compliance evidence. The [TERM:Company] may require proof of PCI compliance as a condition of enabling any card-related integrations.

8.6. **Prohibited Storage.** No employee, contractor, or Client may store card data in logs, screenshots, customer support tickets, or unapproved systems. Any suspected card data exposure constitutes a Security Incident under Section 6 and must be escalated immediately.

---

## SECTION 9: COMPLIANCE ENFORCEMENT CONTROLS
[FLOW:Compliance_Controls]

9.1. The [TERM:Company] implements technical controls to enforce compliance requirements for [TERM:ClientSeries] and their [TERM:EndCustomer] end-customers. These controls are designed to prevent prohibited activity and support proportionate enforcement.

9.2. Geographic controls include IP-based restrictions to block access from prohibited jurisdictions, identification of VPN and anonymization tool usage, and geographic verification for transactions involving restricted regions.
[DOC:B7] <!-- Acceptable Client Use Policy geographic requirements -->

9.3. Transaction controls include velocity limits to detect structuring or unusual patterns, amount thresholds triggering enhanced review, automated screening against sanctions and watchlists, and real-time transaction blocking for prohibited activity.

9.4. User interface controls include warning messages for high-risk activity, friction elements requiring additional confirmation for unusual transactions, and educational prompts regarding compliance requirements.

9.5. Access controls include suspension of API access for non-compliant [TERM:ClientSeries], graduated restrictions based on enforcement escalation level, and temporary holds pending compliance review.

9.6. The [TERM:CTO] implements and maintains these controls in coordination with the [TERM:CCO]. Control parameters may be adjusted based on risk assessment, regulatory requirements, and operational experience.

9.7. Control effectiveness is monitored through regular testing, audit, and review of enforcement actions. False positive rates and client impact are tracked to balance compliance with user experience.

---

## SECTION 10: AI SYSTEMS SECURITY AND OPERATIONS
[FLOW:AI_Security]

10.1. The [TERM:Company] deploys AI systems for security, operations, and compliance functions as part of its AI-centric operational philosophy. AI systems with access to customer data, compliance functions, or operational controls are subject to the security requirements of this Policy.
[DOC:B5] <!-- AI-enabled compliance in BSA/AML -->

10.2. AI system access controls shall follow least privilege principles. Administrative access to AI models and training data requires multi-factor authentication and logging.

10.3. AI models shall be protected from adversarial attacks, data poisoning, and unauthorized modification. Model integrity verification shall occur on deployment and periodically thereafter.

10.4. AI system logs shall capture inputs, outputs, and decision factors to the extent technically feasible, enabling audit and investigation.

**10.4A. AI Processing Legal Basis and Consent.** Where AI systems process personal data:
   (a) **Lawful Basis:** AI processing relies on contractual necessity for service delivery, legitimate interests for fraud prevention and security, and legal obligation for compliance monitoring. Where required by applicable law, explicit consent shall be obtained;
   (b) **Automated Decision-Making:** Where AI systems make solely automated decisions producing legal or similarly significant effects on individuals, the Company shall ensure: (i) human review is available upon request; (ii) individuals are informed of the logic involved and significance of processing; and (iii) the right to contest decisions is documented in [DOC:B8] and [DOC:F2];
   (c) **Consent for Non-Essential AI Processing:** AI processing for purposes beyond core service delivery (e.g., product improvement, behavioral analytics) requires explicit opt-in consent with clear withdrawal mechanism per [DOC:B8] §3;
   (d) **AI PII Minimization:** AI systems shall process only the minimum personal data necessary for the stated purpose, with anonymization or pseudonymization applied where feasible;
   (e) **Retention:** AI logs containing personal data shall follow retention schedules per [DOC:B4] and §4.3, with purpose-based deletion when no longer required.
[DOC:B8] <!-- Privacy Policy consent and rights -->

10.5. AI systems are included in business continuity and disaster recovery planning. Fallback procedures for critical AI-dependent functions shall be documented and tested.

10.6. The [TERM:Company] uses AI-assisted security tools for penetration testing, vulnerability scanning, threat detection, and incident response. Security AI operates under [TERM:CTO] oversight with [TERM:CCO] involvement for compliance-related security matters.

10.7. Third-party AI service providers are subject to vendor security due diligence and contractual security requirements.

10.8. AI system performance, availability, and security incidents are monitored and reported. Material AI system failures are escalated to the [TERM:CTO] and, where compliance-relevant, to the [TERM:CCO].

10.9. As AI technology matures and demonstrates reliability, the [TERM:Company] may expand AI autonomy in security operations, subject to appropriate oversight, testing, and audit procedures.

10.10. **AI System Incident Classification.** AI system incidents shall be classified and responded to as follows:

   (a) **Critical:** AI system failure affecting compliance-critical functions (sanctions screening, transaction hold authority), causing potential regulatory violations, or resulting in loss of funds or data. Response: Immediate failover, executive notification, and post-incident review within 24 hours;

   (b) **High:** AI system degradation affecting service availability or decision quality, elevated false positive/negative rates, or suspected model compromise. Response: Activate fallback procedures, [TERM:CTO] notification within 2 hours, remediation plan within 24 hours;

   (c) **Medium:** AI system performance outside normal parameters, training data issues, or minor functionality degradation. Response: Document and investigate, remediation within 7 days;

   (d) **Low:** Routine AI system maintenance, minor configuration changes, or informational alerts. Response: Standard change management procedures.

10.11. **AI Model Change Control.** Changes to production AI models shall follow change management procedures (Section 3), with additional requirements:

   (a) Pre-deployment validation in a non-production environment;

   (b) Documented approval by the [TERM:CTO] and, for compliance-related models, the [TERM:CCO];

   (c) Rollback procedures and tested ability to revert to previous model version;

   (d) Post-deployment monitoring with defined metrics for success and automatic rollback triggers.

10.12. **Human-in-the-Loop Requirements.** For high-risk AI decisions, the [TERM:Company] maintains human-in-the-loop requirements:

   (a) SAR filing decisions require [TERM:CCO] or designee approval regardless of AI recommendation;

   (b) Customer termination decisions require human review and approval;

   (c) Transactions exceeding defined thresholds require human authorization;

   (d) Appeals of AI decisions are reviewed by human personnel;

   (e) The [TERM:CTO] and [TERM:CCO] may adjust human-in-the-loop thresholds based on demonstrated AI reliability.

10.13. **AI Liability Allocation.** Consistent with the AI Decision Accountability provisions in the [DOC:B5] BSA/AML Program (B5, Section 15):

   (a) The [TERM:Company] retains responsibility for AI system outcomes; liability cannot be transferred to AI vendors or systems;

   (b) Client indemnification obligations extend to claims arising from their reliance on AI system outputs without appropriate verification;

   (c) The [TERM:Company]'s limitation of liability provisions apply to AI-related losses subject to the carve-outs for gross negligence and willful misconduct.

---

## SECTION 11: POLICY REVIEW AND TESTING

11.1. This Policy shall be reviewed annually by the [TERM:CTO] with input from the [TERM:CCO].

11.2. At least one tabletop exercise per year shall test incident response and continuity procedures, with documented results and remediation tracking.
[OBL:OBL-REG-002] <!-- Annual testing requirements -->

11.3. AI systems shall be included in annual policy review and testing, with specific attention to AI-related risks and controls.

---

## SECTION 12: POLICY ACKNOWLEDGMENT

12.1. All [TERM:Officers] shall acknowledge receipt and understanding of this Policy upon appointment and annually thereafter.
[OBL:OBL-OFF-001]

12.2. Key personnel with access to production systems, code repositories, wallets, or infrastructure shall sign an acknowledgment of this Policy and be bound by its terms.

12.3. Acknowledgment records shall be maintained by the [TERM:CTO].
[DOC:B4]

---

## SECTION 13: ADOPTION

13.1. This IT Security, Incident Response, Business Continuity, and Disaster Recovery Policy is hereby adopted.

**[TERM:Manager] MANAGER:**

Signature: ______________________________

Printed Name: [________________]

Title: Manager

Date: ______________________________
