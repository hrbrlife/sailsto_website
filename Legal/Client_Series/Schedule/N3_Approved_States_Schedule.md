# APPROVED STATES SCHEDULE
## CCASH MONEY SERVICES (US) SERIES LLC

<!-- schema:doc DOC:N3 version:1.4 -->

---

**Effective Date:** December 21, 2025

**Schedule Version:** 1.4

---

## VERSION HISTORY

| Version | Date | Author | Summary of Changes | Breaking Change |
|---------|------|--------|-------------------|-----------------|
| 1.0 | December 2025 | CCO | Initial version | — |
| 1.1 | December 14, 2025 | Audit Remediation | Added Section 6.0 clarification for N4 dependency; added version history | No |
| 1.2 | December 15, 2025 | Audit Remediation | Added Section 7 Partner MSB Business Continuity procedures | No |
| 1.3 | December 15, 2025 | Omissions Closure | Added Section 8 consumer disclosures/state requirements; renumbered updates/references sections | No |
| 1.4 | December 21, 2025 | Compliance Fix | Added qualifying language to Montana MTL exemption (§2.1.1) and Wyoming crypto exemption (§3.1.1) requiring legal counsel verification | No |

---

## SECTION 1: PURPOSE AND SCOPE

<!-- schema:flow FLOW:geographic_operations -->

1.1. This Schedule identifies the states and territories in which Client Series [TERM:ClientSeries] may conduct money services business [TERM:MSB] activities and the regulatory basis for such activities.

1.2. This Schedule is incorporated by reference into the Client Services Agreement [DOC:F1] and the Acceptable Client Use Policy [DOC:B7].

1.3. Client Series must operate only within the geographic scope defined in this Schedule. Activities outside approved jurisdictions are prohibited.

---

## SECTION 2: MONTANA BASE OPERATIONS

### 2.1. Montana MSB Authority

<!-- schema:term TERM:MontanaState -->

2.1.1. Based on current state regulatory guidance, Montana [TERM:MontanaState] does not require a separate money transmitter license for MSBs. Money services businesses in Montana operate under federal FinCEN [TERM:FinCEN] registration plus state business registration. This position should be verified with Montana legal counsel and monitored for regulatory changes.

2.1.2. All Client Series are formed under Montana law (MCA § 35-8-304) [TERM:MCA] and may conduct money transmission activities with Montana residents without additional state licensure.

2.1.3. Montana-only operations include: (a) transactions where both sender and recipient are Montana residents or businesses; (b) transactions originated by Montana residents regardless of destination within Montana; and (c) services provided to Montana-based businesses for their Montana operations.

### 2.2. Montana Regulatory Compliance

2.2.1. Client Series must maintain current Montana business registration through the Secretary of State [TERM:SecretaryOfState].

2.2.2. Client Series must maintain its own FinCEN MSB registration [OBL:FINCEN-REG-001].

2.2.3. Client Series must comply with Montana consumer protection laws and the Montana Unfair Trade Practices and Consumer Protection Act.

---

## SECTION 3: CRYPTO-EXEMPT STATE OPERATIONS

### 3.1. Wyoming Virtual Currency Exemption

<!-- schema:term TERM:VirtualCurrency -->

3.1.1. Wyoming exempts virtual currency [TERM:VirtualCurrency] transactions from money transmitter licensing under W.S. § 40-22-104(a)(vi) (verify current statute for applicability). This exemption should be confirmed with Wyoming legal counsel before relying upon it for operations.

3.1.2. Client Series may conduct virtual currency exchange, custody, and transfer services with Wyoming residents without additional state licensure.

3.1.3. The Wyoming exemption applies only to virtual currency activities. Fiat money transmission [TERM:FiatGateway] to or from Wyoming residents requires either a Wyoming money transmitter license or routing through a Partner MSB [TERM:PartnerMSB].

3.1.4. Client Series utilizing the Wyoming exemption must maintain records demonstrating that Wyoming transactions involve only virtual currency [OBL:RECORD-CRYPTO-001].

### 3.2. Other Crypto-Exempt Jurisdictions

3.2.1. The Company [TERM:Company] monitors state legislation for additional crypto or virtual currency exemptions.

3.2.2. Additional crypto-exempt states will be added to this Schedule upon legal review and approval by the Company's compliance team [TERM:CCO].

3.2.3. As of the Effective Date, approved crypto-exempt states are: **Wyoming**.

3.2.4. The following states have partial exemptions or pending legislation under review: [None currently approved].

---

## SECTION 4: PARTNER MSB ROUTING

### 4.1. Interstate Transmission via Partner MSB

<!-- schema:flow FLOW:partner_msb_routing -->

4.1.1. For money transmission activities involving states other than Montana (except as provided in Section 3), Client Series [TERM:ClientSeries] must route transactions through a Partner MSB [TERM:PartnerMSB] that holds appropriate state licenses.

4.1.2. Partner MSB routing enables Client Series to serve customers nationwide while maintaining regulatory compliance [FLOW:partner_msb_routing].

4.1.3. Partner MSB transactions are subject to additional fees as described in Pricing and Routing Schedule [DOC:C3] Section 4.7.

### 4.2. Approved Partner MSBs

4.2.1. The Company [TERM:Company] maintains agreements with licensed Partner MSBs for interstate routing.

4.2.2. Approved Partner MSBs are listed in Schedule N4 [DOC:N4] (Partner MSB Directory), which is maintained separately and updated as partnerships are established.

4.2.3. Client Series may not independently contract with Partner MSBs for routing. All Partner MSB relationships must be through the Company [OBL:PARTNER-RESTRICT-001].

### 4.3. Partner MSB Coverage States

4.3.1. The current Partner MSB network provides coverage for the following states: [To be populated based on Partner MSB license coverage].

4.3.2. States not covered by the Partner MSB network are listed in Section 5 (Prohibited States).

4.3.3. Partner MSB coverage is live only when a Partner MSB and its state licenses are listed in Schedule N4 (Partner MSB Directory). Until a state appears in Schedule N4, assume no Partner MSB coverage is available for that state.

---

## SECTION 5: PROHIBITED STATES AND TERRITORIES

### 5.1. States Requiring Additional Analysis

<!-- schema:term TERM:ProhibitedState -->

5.1.1. The following states have regulatory requirements that currently preclude Client Series [TERM:ClientSeries] operations, either directly or through Partner MSB [TERM:PartnerMSB] routing:

   (a) **New York:** Requires BitLicense for virtual currency business activities. Client Series may not serve New York residents for any crypto-related services until BitLicense is obtained by the Company [TERM:Company] or a Partner MSB.

   (b) **Hawaii:** Has suspended money transmitter licensing for digital currency companies and requires dollar-for-dollar reserves. Client Series may not serve Hawaii residents until regulatory clarity is achieved.

5.1.2. Additional prohibited states may be added based on regulatory developments, Partner MSB coverage limitations, or compliance risk assessments.

### 5.2. U.S. Territories

5.2.1. Puerto Rico, Guam, U.S. Virgin Islands, American Samoa, and Northern Mariana Islands have separate licensing requirements.

5.2.2. Client Series may not serve residents of U.S. territories unless specifically approved in writing by the Company [OBL:TERRITORY-APPROVAL-001].

### 5.3. International Operations

5.3.1. This Schedule addresses only U.S. state and territory operations.

5.3.2. International operations require separate analysis and are not authorized under this Schedule.

---

## SECTION 6: STATE STATUS TABLE

6.0. **Status Legend:** Entries marked "Partner MSB" denote states that may be served only through an approved Partner MSB listed in Schedule N4. If no Partner MSB is listed for a state in Schedule N4, treat that state as not currently available (i.e., prohibited unless and until coverage is confirmed).

### 6.1. California Consumer Privacy Act (CCPA) Requirements

6.1.1. All services provided to California residents must comply with CCPA (Cal. Civ. Code §1798.100 et seq.) and CPRA amendments.

6.1.2. **Required Notices.** Before serving California End Customers:
   (a) "At Collection" notice per CCPA §1798.100(b) disclosing categories of personal information collected;
   (b) "Do Not Sell or Share My Personal Information" link per CCPA §1798.120;
   (c) Privacy policy meeting CCPA §1798.130(a)(5) requirements, updated at least annually.

6.1.3. **Data Subject Rights.** California consumers have the right to:
   (a) Know what personal information is collected;
   (b) Delete personal information (subject to regulatory record retention exceptions);
   (c) Opt-out of sale/sharing of personal information;
   (d) Non-discrimination for exercising rights.

6.1.4. **Response Timelines.** Respond to verifiable consumer requests within forty-five (45) days per CCPA §1798.130.

6.1.5. **Policy Reference.** See [DOC:B8] Privacy Policy for complete CCPA implementation.

| State | Status | Basis | Notes |
|-------|--------|-------|-------|
| Alabama | Partner MSB | State license required | Via Partner routing |
| Alaska | Partner MSB | State license required | Via Partner routing |
| Arizona | Partner MSB | State license required | Via Partner routing |
| Arkansas | Partner MSB | State license required | Via Partner routing |
| California | Partner MSB | State license required | Via Partner routing; **CCPA Required** (see §6.1) |
| Colorado | Partner MSB | State license required | Via Partner routing |
| Connecticut | Partner MSB | State license required | Via Partner routing |
| Delaware | Partner MSB | State license required | Via Partner routing |
| Florida | Partner MSB | State license required | Via Partner routing |
| Georgia | Partner MSB | State license required | Via Partner routing |
| Hawaii | PROHIBITED | Regulatory uncertainty | No service |
| Idaho | Partner MSB | State license required | Via Partner routing |
| Illinois | Partner MSB | State license required | Via Partner routing |
| Indiana | Partner MSB | State license required | Via Partner routing |
| Iowa | Partner MSB | State license required | Via Partner routing |
| Kansas | Partner MSB | State license required | Via Partner routing |
| Kentucky | Partner MSB | State license required | Via Partner routing |
| Louisiana | Partner MSB | State license required | Via Partner routing |
| Maine | Partner MSB | State license required | Via Partner routing |
| Maryland | Partner MSB | State license required | Via Partner routing |
| Massachusetts | Partner MSB | State license required | Via Partner routing |
| Michigan | Partner MSB | State license required | Via Partner routing |
| Minnesota | Partner MSB | State license required | Via Partner routing |
| Mississippi | Partner MSB | State license required | Via Partner routing |
| Missouri | Partner MSB | State license required | Via Partner routing |
| Montana | APPROVED | No MTL required | Direct service |
| Nebraska | Partner MSB | State license required | Via Partner routing |
| Nevada | Partner MSB | State license required | Via Partner routing |
| New Hampshire | Partner MSB | State license required | Via Partner routing |
| New Jersey | Partner MSB | State license required | Via Partner routing |
| New Mexico | Partner MSB | State license required | Via Partner routing |
| New York | PROHIBITED | BitLicense required | No service |
| North Carolina | Partner MSB | State license required | Via Partner routing |
| North Dakota | Partner MSB | State license required | Via Partner routing |
| Ohio | Partner MSB | State license required | Via Partner routing |
| Oklahoma | Partner MSB | State license required | Via Partner routing |
| Oregon | Partner MSB | State license required | Via Partner routing |
| Pennsylvania | Partner MSB | State license required | Via Partner routing |
| Rhode Island | Partner MSB | State license required | Via Partner routing |
| South Carolina | Partner MSB | State license required | Via Partner routing |
| South Dakota | Partner MSB | State license required | Via Partner routing |
| Tennessee | Partner MSB | State license required | Via Partner routing |
| Texas | Partner MSB | State license required | Via Partner routing |
| Utah | Partner MSB | State license required | Via Partner routing |
| Vermont | Partner MSB | State license required | Via Partner routing |
| Virginia | Partner MSB | State license required | Via Partner routing |
| Washington | Partner MSB | State license required | Via Partner routing |
| West Virginia | Partner MSB | State license required | Via Partner routing |
| Wisconsin | Partner MSB | State license required | Via Partner routing |
| Wyoming | APPROVED (Crypto) | W.S. § 40-22-104(a)(vi) | Crypto only |
| District of Columbia | Partner MSB | License required | Via Partner routing |

---

## SECTION 7: PARTNER MSB BUSINESS CONTINUITY

<!-- schema:flow FLOW:partner_msb_contingency -->

### 7.1. Partner MSB Monitoring

7.1.1. The Company [TERM:Company] shall continuously monitor the regulatory status and operational capacity of each Partner MSB [TERM:PartnerMSB] listed in Schedule N4.

7.1.2. Monitoring includes: (a) verification of license status with state regulators; (b) review of Partner MSB financial condition; (c) assessment of operational performance; and (d) tracking of regulatory actions or enforcement proceedings.

7.1.3. The Company's CCO [TERM:CCO] shall maintain emergency contact information for each Partner MSB and conduct at least quarterly status reviews.

### 7.2. Partner MSB Disruption Events

7.2.1. A "Partner MSB Disruption Event" [TERM:PartnerMSBDisruption] occurs when a Partner MSB: (a) has any state license revoked, suspended, or surrendered; (b) becomes insolvent or files for bankruptcy; (c) is subject to a cease-and-desist order or enforcement action; (d) terminates its agreement with the Company; (e) experiences an operational failure preventing transaction processing; or (f) is otherwise unable to provide routing services.

7.2.2. Upon learning of a potential Partner MSB Disruption Event, the Company shall immediately assess the scope and impact on Client Series operations.

### 7.3. Immediate Response Procedures

7.3.1. **Transaction Suspension.** Upon a Partner MSB Disruption Event affecting one or more states, the Company shall immediately suspend new transaction routing to the affected states through the affected Partner MSB [OBL:PARTNER-SUSPEND-001].

7.3.2. **Client Notification.** The Company shall notify all affected Client Series [TERM:ClientSeries] within twenty-four (24) hours of a confirmed Partner MSB Disruption Event, specifying: (a) the states affected; (b) the nature of the disruption; (c) the expected duration (if known); and (d) interim operating procedures.

7.3.3. **End-Customer Communication.** Client Series shall promptly notify affected End-Customers that services to certain states are temporarily unavailable. The Company may provide template notification language.

7.3.4. **Pending Transactions.** For transactions in progress at the time of a Disruption Event: (a) completed transactions shall be settled through normal procedures; (b) pending transactions not yet submitted to the Partner MSB shall be held or returned to the originator; (c) transactions in transit shall be monitored and resolved case-by-case in coordination with the Partner MSB.

### 7.4. Alternative Routing Procedures

7.4.1. **Backup Partner MSB.** Where the Company maintains agreements with multiple Partner MSBs, the Company shall route affected transactions through an alternative Partner MSB with valid licenses in the affected states, subject to pricing adjustments as necessary.

7.4.2. **Transaction Queue.** Where no alternative Partner MSB is immediately available, the Company may queue transactions for a reasonable period (not to exceed five (5) business days) pending restoration of routing capability or customer decision to cancel.

7.4.3. **Refund Option.** End-Customers with transactions that cannot be completed due to a Partner MSB Disruption Event shall be offered a full refund of any fees paid and return of funds within five (5) business days of request.

### 7.5. Schedule N4 Updates

7.5.1. Within five (5) business days of a Partner MSB Disruption Event, the Company shall update Schedule N4 [DOC:N4] to reflect the changed status.

7.5.2. States affected by a Partner MSB Disruption Event shall be marked as "Temporarily Unavailable" until: (a) the original Partner MSB restores service; (b) an alternative Partner MSB is activated; or (c) the state is reclassified as Prohibited.

7.5.3. The Company shall use commercially reasonable efforts to establish alternative routing arrangements within sixty (60) days of a Partner MSB Disruption Event.

### 7.6. Client Series Obligations During Disruption

7.6.1. Client Series shall not attempt to route transactions through unauthorized channels or directly contract with third-party MSBs during a Partner MSB Disruption Event [OBL:NO-WORKAROUND-001].

7.6.2. Client Series shall update their platforms and customer-facing materials to reflect state availability changes within forty-eight (48) hours of Company notification.

7.6.3. Client Series shall cooperate with the Company in managing customer communications and transaction resolution.

### 7.7. Force Majeure

7.7.1. A Partner MSB Disruption Event may constitute a Force Majeure event under the Client Services Agreement [DOC:F1] Article 10 if caused by circumstances beyond the Company's reasonable control.

7.7.2. The Company shall not be liable for damages arising from Partner MSB Disruption Events, provided it follows the procedures in this Section 7.

---

## SECTION 8: CONSUMER DISCLOSURES AND STATE REQUIREMENTS

8.1. **State-Specific Consumer Disclosures.** Client Series shall ensure that end-customer terms [DOC:F2], receipts, and customer-facing UI include any state-specific disclosures, refund timing requirements, and complaint contact information required by applicable law for each jurisdiction served (including where service is provided via Partner MSB routing). [OBL:STATE-CONSUMER-NOTICE-001]

8.2. **Receipts and Statements.** Client Series shall provide transaction receipts and periodic statements as required by [DOC:F2] Section 6D and applicable state law, including state-required legends and regulator contact information where applicable. [OBL:RECEIPT-CUSTOMER-001]

8.3. **Refunds and Cancellations.** Client Series shall implement refund and cancellation processes as required by [DOC:F2] Section 6H, by applicable state law, and by Partner MSB requirements. [OBL:REFUND-CUSTOMER-001]

8.4. **Remittance Transfers (If Applicable).** If a Client Series offers remittance transfers covered by Regulation E Subpart B, the Client Series shall provide required disclosures, receipts, cancellation rights, and error resolution procedures consistent with [DOC:F2] Section 6A.7. [OBL:REMITTANCE-CUSTOMER-001]

---

## SECTION 9: SCHEDULE UPDATES

<!-- schema:flow FLOW:schedule_update -->

9.1. This Schedule is updated as regulatory landscapes change, Partner MSB [TERM:PartnerMSB] coverage expands, or compliance risk assessments require [FLOW:schedule_update].

9.2. Updates are communicated to Client Series [TERM:ClientSeries] through the methods specified in the Client Services Agreement [DOC:F1].

9.3. Client Series are responsible for monitoring Schedule updates and adjusting their operations accordingly [OBL:MONITOR-SCHEDULE-001].

---

## SECTION 10: DOCUMENT REFERENCES

10.1. Acceptable Client Use Policy [DOC:B7] (Sections 9.7-9.12 Geographic Scope)

10.2. Pricing and Routing Schedule [DOC:C3] (Section 4.7 Partner MSB Fees)

10.3. Client Services Agreement [DOC:F1]

10.4. Partner MSB Directory [DOC:N4] (separate document)

10.5. Client FinCEN Filing Guide [DOC:N5]

10.6. Partner MSB Agreement [DOC:N1]

---

*This Schedule is incorporated by reference into the Client Services Agreement and related governance documents. Updated versions supersede prior versions upon effective date.*
