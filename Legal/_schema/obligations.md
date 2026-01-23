# Obligations Ledger

> **Purpose**: hledger-style double-entry tracking of all obligations across documents.
> Every obligation has an obligor (who owes) and obligee (who is owed).

---

## Statistics

| Metric | Value |
|--------|-------|
| Defined OBL IDs (registry) | 88 |
| Used OBL IDs (unique, non-schema docs) | 78 |
| Total OBL marker occurrences (non-schema docs) | 129 |

> Recompute by running `bash _schema/validation/marker_audit.sh --verbose`.

---

## Ledger Format

```
DATE OBLIGATION_ID
    ; frequency: ONE_TIME | ANNUAL | BIENNIAL | ON_CHANGE | CONTINUOUS
    ; source: DOCUMENT §SECTION
    ; deadline: DURATION or DATE
    ; penalty: Description of non-compliance consequence
    OBLIGOR                      obligation:TYPE
    OBLIGEE                      receivable:TYPE
```

---

## Company → Regulator Obligations

```ledger
2025-01-01 OBL-REG-001 Company FinCEN Registration
    ; frequency: BIENNIAL
    ; source: E1 §7.2.1
    ; deadline: 2 years from last registration
    ; penalty: Loss of MSB status, enforcement action
    Company                      obligation:fincen_renewal
    FinCEN                       receivable:registration

2025-01-01 OBL-REG-002 Company FinCEN Change Report
    ; frequency: ON_CHANGE
    ; source: E1 §7.2.3
    ; deadline: 180 days from change
    ; penalty: FinCEN enforcement
    Company                      obligation:fincen_update
    FinCEN                       receivable:change_report

2025-01-01 OBL-REG-003 Montana Annual Report
    ; frequency: ANNUAL
    ; source: E1 §7.1.1
    ; deadline: April 15
    ; penalty: Administrative dissolution
    Company                      obligation:annual_report
    Montana SOS                  receivable:filing

2025-01-01 OBL-REG-004 SAR Filing
    ; frequency: ON_TRIGGER
    ; source: B5 §3.4
    ; deadline: 30 days from detection
    ; penalty: BSA violation, criminal liability
    Company                      obligation:sar_filing
    FinCEN                       receivable:sar

2025-01-01 OBL-REG-005 Annual Independent BSA/AML Program Testing
    ; frequency: ANNUAL
    ; source: B5 §10.1
    ; deadline: Annual, within 12 months of prior test
    ; penalty: BSA compliance violation, examination criticism
    Company                      obligation:independent_testing
    CCO                          responsible:coordination
    Manager                      receivable:test_report

2025-01-01 BSA-SAR-001 SAR Report Obligation
    ; frequency: ON_TRIGGER
    ; source: B5 §5.1
    ; deadline: 30 days from determination
    ; penalty: BSA violation
    ; alias: OBL-REG-004 (same obligation, different ID format)
    Company                      obligation:sar_filing
    FinCEN                       receivable:sar

2025-01-01 SAR-REPORT-001 SAR Reporting
    ; frequency: ON_TRIGGER
    ; source: B5 §5.1
    ; deadline: 30 days
    ; penalty: BSA violation
    ; alias: BSA-SAR-001
    Company                      obligation:sar_filing
    FinCEN                       receivable:sar

2025-01-01 MSB-REG-001 MSB Registration Maintenance
    ; frequency: BIENNIAL
    ; source: E1 §5.1.2
    ; deadline: 2 years from registration
    ; penalty: Loss of MSB status
    Company                      obligation:msb_registration
    FinCEN                       receivable:registration
```

---

## ClientSeries → Regulator Obligations

```ledger
2025-01-01 OBL-CLIENT-REG-001 Client FinCEN Registration
    ; frequency: BIENNIAL
    ; source: E1 §7.2.2, N5 §5.1
    ; deadline: 2 years from registration
    ; penalty: Loss of MSB status, Company may suspend
    ClientSeries                 obligation:fincen_renewal
    FinCEN                       receivable:registration

2025-01-01 FINCEN-REG-001 Client FinCEN Registration
    ; frequency: BIENNIAL
    ; source: N5 §1.1.2
    ; deadline: 2 years from registration
    ; penalty: Loss of MSB status
    ; alias: OBL-CLIENT-REG-001
    ClientSeries                 obligation:fincen_registration
    FinCEN                       receivable:registration

2025-01-01 FINCEN-TIMING-001 Initial FinCEN Filing Deadline
    ; frequency: ONE_TIME
    ; source: N5 §1.2.2
    ; deadline: 180 days from commencing MSB activities
    ; penalty: FinCEN enforcement
    ClientSeries                 obligation:initial_fincen
    FinCEN                       receivable:registration

2025-01-01 FINCEN-RENEWAL-001 Biennial FinCEN Renewal
    ; frequency: BIENNIAL
    ; source: N5 §1.2.3, §5.1
    ; deadline: 2 years from registration
    ; penalty: Loss of MSB status
    ClientSeries                 obligation:fincen_renewal
    FinCEN                       receivable:registration

2025-01-01 FINCEN-UPDATE-001 FinCEN Change Reporting
    ; frequency: ON_CHANGE
    ; source: N5 §1.2.4, §6.1
    ; deadline: 180 days from change
    ; penalty: FinCEN enforcement
    ClientSeries                 obligation:fincen_update
    FinCEN                       receivable:change_report

2025-01-01 OBL-CLIENT-REG-002 Client FinCEN Change Report
    ; frequency: ON_CHANGE
    ; source: N5 §6.1
    ; deadline: 180 days from change
    ; penalty: FinCEN enforcement
    ; alias: FINCEN-UPDATE-001
    ClientSeries                 obligation:fincen_update
    FinCEN                       receivable:change_report

2025-01-01 TAX-FILING-001 Client Series Tax Compliance
    ; frequency: ANNUAL
    ; source: B11 §13.1.1
    ; deadline: Per applicable tax law
    ; penalty: Tax penalties and interest
    ClientSeries                 obligation:tax_reporting
    IRS                          receivable:filings

2025-01-01 TAX-1099-CLIENT-001 Client Series End-Customer Information Returns
    ; frequency: ANNUAL
    ; source: B11 §13.1.4
    ; deadline: Per applicable tax law (e.g., 1099 delivery/filing deadlines)
    ; penalty: Tax penalties and interest
    ClientSeries                 obligation:information_returns
    IRS                          receivable:filings
```

---

## ClientSeries → Company Obligations

```ledger
2025-01-01 OBL-CLIENT-CO-001 Monthly Platform Fee
    ; frequency: MONTHLY
    ; source: C3 §3.1
    ; deadline: 10 days from invoice
    ; penalty: Service suspension
    ClientSeries                 obligation:platform_fee
    Company                      receivable:fee  $2,500

2025-01-01 OBL-CLIENT-CO-002 Onboarding Fee
    ; frequency: ONE_TIME
    ; source: C3 §2.1
    ; deadline: Upon CSA execution
    ; penalty: Onboarding halt
    ClientSeries                 obligation:onboarding_fee
    Company                      receivable:fee  $10,000

2025-01-01 OBL-CLIENT-CO-003 Training Fee
    ; frequency: ONE_TIME
    ; source: C3 §2.2
    ; deadline: Upon training completion
    ; penalty: Cannot proceed to ACTIVE
    ClientSeries                 obligation:training_fee
    Company                      receivable:fee  $10,000

2025-01-01 OBL-CLIENT-CO-004 Provide FinCEN Proof
    ; frequency: ONE_TIME + ON_RENEWAL
    ; source: E1 §6.1.6, F1 Art.6
    ; deadline: Before ACTIVE status
    ; penalty: Cannot operate
    ClientSeries                 obligation:fincen_proof
    Company                      receivable:documentation

2025-01-01 OBL-CLIENT-CO-005 Compliance with AUP
    ; frequency: CONTINUOUS
    ; source: B7 §1.1
    ; deadline: Continuous
    ; penalty: Suspension, termination
    ClientSeries                 obligation:aup_compliance
    Company                      receivable:compliance

2025-01-01 OBL-CLIENT-CO-006 Geographic Restrictions
    ; frequency: CONTINUOUS
    ; source: B7 §9.7-9.12, N3
    ; deadline: Continuous
    ; penalty: Suspension, termination
    ClientSeries                 obligation:geographic_compliance
    Company                      receivable:compliance

2025-01-01 FEE-PLATFORM-001 Monthly Platform Fee
    ; frequency: MONTHLY
    ; source: C3 §3.1
    ; deadline: 10 days from invoice
    ; penalty: Service suspension
    ; alias: OBL-CLIENT-CO-001
    ClientSeries                 obligation:platform_fee
    Company                      receivable:fee

2025-01-01 FEE-ONBOARD-001 Onboarding Fee
    ; frequency: ONE_TIME
    ; source: C3 §2.1
    ; deadline: Upon CSA execution
    ; penalty: Onboarding halt
    ; alias: OBL-CLIENT-CO-002
    ClientSeries                 obligation:onboarding_fee
    Company                      receivable:fee

2025-01-01 FEE-TRAINING-001 Training Fee
    ; frequency: ONE_TIME
    ; source: C3 §2.2
    ; deadline: Upon training completion
    ; penalty: Cannot proceed to ACTIVE
    ; alias: OBL-CLIENT-CO-003
    ClientSeries                 obligation:training_fee
    Company                      receivable:fee

2025-01-01 FEE-TRANSACTION-001 Transaction Fees
    ; frequency: PER_TRANSACTION
    ; source: C3 §4.1
    ; deadline: Per invoice cycle
    ; penalty: Service suspension
    ClientSeries                 obligation:transaction_fee
    Company                      receivable:fee

2025-01-01 FEE-LICENSE-001 IT License Fee
    ; frequency: ANNUAL
    ; source: C3 §3.3
    ; deadline: Annual renewal
    ; penalty: License revocation
    ClientSeries                 obligation:license_fee
    Company                      receivable:fee

2025-01-01 FINCEN-NOTIFY-001 Provide FinCEN Documentation
    ; frequency: ONE_TIME + ON_RENEWAL
    ; source: E1 §6.1.6, N5 §4.1
    ; deadline: Before ACTIVE status
    ; penalty: Cannot operate
    ; alias: OBL-CLIENT-CO-004
    ClientSeries                 obligation:fincen_proof
    Company                      receivable:documentation

2025-01-01 EIN-UNIQUE-001 Unique EIN Per Series
    ; frequency: ONE_TIME
    ; source: N5 §2.1.4
    ; deadline: Before FinCEN registration
    ; penalty: Cannot register with FinCEN
    ClientSeries                 obligation:unique_ein
    IRS                          receivable:ein_application

2025-01-01 RECORD-RETENTION-001 5-Year Record Retention
    ; frequency: CONTINUOUS
    ; source: B4 §2.1, N5 §4.2.2
    ; deadline: 5 years after record creation
    ; penalty: Compliance violation
    ClientSeries                 obligation:record_retention
    Company                      receivable:compliance

2025-01-01 RECORD-SERIES-001 Series Record Maintenance
    ; frequency: CONTINUOUS
    ; source: B4 §2.2
    ; deadline: Continuous
    ; penalty: Compliance violation
    ClientSeries                 obligation:series_records
    Company                      receivable:compliance

2025-01-01 RECORD-CRYPTO-001 Crypto Transaction Records
    ; frequency: CONTINUOUS
    ; source: N3 §3.1.4
    ; deadline: Continuous
    ; penalty: Loss of Wyoming exemption
    ClientSeries                 obligation:crypto_records
    Company                      receivable:compliance

2025-01-01 MONITOR-SCHEDULE-001 Schedule Monitoring
    ; frequency: CONTINUOUS
    ; source: N3 §7.3
    ; deadline: Continuous
    ; penalty: Operating outside scope
    ClientSeries                 obligation:schedule_monitoring
    Company                      receivable:compliance

2025-01-01 PARTNER-RESTRICT-001 Partner MSB Restriction
    ; frequency: CONTINUOUS
    ; source: N3 §4.2.3
    ; deadline: Continuous
    ; penalty: Termination
    ClientSeries                 obligation:partner_restriction
    Company                      receivable:compliance

2025-01-01 TERRITORY-APPROVAL-001 Territory Approval Required
    ; frequency: ON_REQUEST
    ; source: N3 §5.2.2
    ; deadline: Before serving territory residents
    ; penalty: Compliance violation
    ClientSeries                 obligation:territory_approval
    Company                      receivable:approval

2025-01-01 COMPLAINT-REPORT-001 Complaint Reporting
    ; frequency: ON_EVENT
    ; source: F1 §8.3
    ; deadline: Within 5 business days
    ; penalty: Compliance violation
    ClientSeries                 obligation:complaint_report
    Company                      receivable:report

2025-01-01 COMPLIANCE-DELEGATION-001 Client BSA/AML Delegation and Cooperation
    ; frequency: CONTINUOUS
    ; source: B11 §14.1.2
    ; deadline: Continuous
    ; penalty: Suspension/termination, regulatory exposure
    ClientSeries                 obligation:aml_delegation
    Company                      receivable:cooperation

2025-01-01 TRAINING-CLIENT-001 Client Compliance Training Completion
    ; frequency: ANNUAL + ONBOARDING
    ; source: B11 §14.2.3
    ; deadline: Before ACTIVE and annually thereafter
    ; penalty: Suspension/termination
    ClientSeries                 obligation:training
    Company                      receivable:completion

2025-01-01 SCREENING-CLIENT-001 Client Key Personnel Screening
    ; frequency: ONBOARDING + ON_CHANGE
    ; source: B11 §14.2.4
    ; deadline: Before privileged access; within 10 business days of role change
    ; penalty: Suspension/termination
    ClientSeries                 obligation:screening
    Company                      receivable:screening

2025-01-01 CLIENT-INSURANCE-001 Client Insurance Maintenance
    ; frequency: CONTINUOUS
    ; source: B11 §14A.1.1
    ; deadline: Continuous
    ; penalty: Suspension/termination, increased risk
    ClientSeries                 obligation:insurance
    Company                      receivable:coverage

2025-01-01 AGENT-PROHIBITION-001 Prohibit Agent/Sub-Representative Networks
    ; frequency: CONTINUOUS
    ; source: B11 §14B.1.1
    ; deadline: Continuous
    ; penalty: Immediate termination, regulatory exposure
    ClientSeries                 obligation:no_agents
    Company                      receivable:compliance

2025-01-01 MARKETING-COMPLIANCE-001 Client Marketing Compliance
    ; frequency: CONTINUOUS
    ; source: B11 §14C.1.1
    ; deadline: Continuous
    ; penalty: Suspension/termination, regulatory exposure
    ClientSeries                 obligation:marketing_compliance
    Company                      receivable:compliance

2025-01-01 NO-WORKAROUND-001 No Unauthorized Routing Workarounds
    ; frequency: CONTINUOUS
    ; source: N3 §7.6.1
    ; deadline: Continuous during disruption events
    ; penalty: Immediate suspension/termination
    ClientSeries                 obligation:no_workarounds
    Company                      receivable:compliance

2025-01-01 CLIENT-BREACH-NOTIFY-001 Client Security Incident Notification
    ; frequency: ON_EVENT
    ; source: F1 §14.14
    ; deadline: Within 24 hours of discovery/suspicion
    ; penalty: Suspension/termination, regulatory exposure
    ClientSeries                 obligation:breach_notification
    Company                      receivable:notice

2025-01-01 SHORTFALL-GUARANTEE-001 Client Shortfall Guarantee
    ; frequency: ON_TRIGGER
    ; source: F1 §14.13
    ; deadline: On demand after dissolution/termination
    ; penalty: Collection action
    Member                       obligation:guarantee
    Company                      receivable:payment

2025-01-01 CLIENT-FINANCIAL-COV-001 Client Solvency and Liquidity Covenant
    ; frequency: CONTINUOUS
    ; source: F1 §6.8(a)
    ; deadline: Continuous
    ; penalty: Suspension/termination, increased loss risk
    ClientSeries                 obligation:solvency_liquidity
    Company                      receivable:assurance

2025-01-01 CLIENT-CAPITAL-001 Client Minimum Capital and Reserves
    ; frequency: CONTINUOUS
    ; source: F1 §6.8(b); B11 §7.11
    ; deadline: Continuous
    ; penalty: Suspension/termination, increased loss risk
    ClientSeries                 obligation:minimum_capital
    Company                      receivable:assurance

2025-01-01 CLIENT-FINANCIAL-REPORT-001 Client Financial Reporting
    ; frequency: QUARTERLY + ON_REQUEST
    ; source: F1 §6.8(c)
    ; deadline: Within 15 business days of request or quarter end
    ; penalty: Suspension/termination
    ClientSeries                 obligation:financial_reporting
    Company                      receivable:financials

2025-01-01 REGCOST-REIMBURSE-001 Reimburse Extraordinary Compliance Costs
    ; frequency: ON_EVENT
    ; source: F1 §11.1(g)
    ; deadline: Net 30 from invoice
    ; penalty: Suspension/termination, collection
    ClientSeries                 obligation:reimburse_compliance_costs
    Company                      receivable:costs

2025-01-01 EARLY-TERM-FEE-001 Early Termination Fee (Initial Term)
    ; frequency: ON_TRIGGER
    ; source: F1 §12.1.1
    ; deadline: Due upon termination effective date
    ; penalty: Collection, offsets against reserves
    ClientSeries                 obligation:early_termination_fee
    Company                      receivable:fee

2025-01-01 MATERIAL-EXPANSION-APPROVAL-001 Material Expansion Approval
    ; frequency: ON_CHANGE
    ; source: B11 §7.4
    ; deadline: Before launch/enablement
    ; penalty: Suspension/termination
    ClientSeries                 obligation:expansion_approval
    Company                      receivable:approval

2025-01-01 INTL-OPS-001 International Operations Approval and Compliance
    ; frequency: ON_CHANGE + CONTINUOUS
    ; source: B11 §7.7
    ; deadline: Before launch; continuous compliance
    ; penalty: Suspension/termination, sanctions exposure
    ClientSeries                 obligation:international_gating
    Company                      receivable:approval

2025-01-01 FOREIGN-QUAL-001 Foreign Qualification and Business Registration
    ; frequency: ON_CHANGE
    ; source: B11 §7.8
    ; deadline: Before doing business where required
    ; penalty: Compliance breach, enforcement exposure
    ClientSeries                 obligation:foreign_qualification
    Company                      receivable:evidence

2025-01-01 CRYPTO-LICENSING-REVIEW-001 Crypto Regulatory Trigger Review
    ; frequency: ON_CHANGE
    ; source: B11 §7.10
    ; deadline: Before enabling new digital asset features
    ; penalty: Suspension/termination, regulatory exposure
    ClientSeries                 obligation:crypto_legal_review
    Company                      receivable:approval

2025-01-01 SUPPORT-ESCALATION-001 End-Customer Support and Escalation
    ; frequency: CONTINUOUS
    ; source: B11 §9.6-9.7
    ; deadline: Continuous; escalate within 1 business day
    ; penalty: Suspension/termination
    ClientSeries                 obligation:support_and_escalation
    Company                      receivable:cooperation

2025-01-01 OFFBOARDING-SPINOFF-001 Spin-Off and Transition Plan
    ; frequency: ON_EXIT
    ; source: B11 §11.11
    ; deadline: As scheduled in approved plan
    ; penalty: Suspension/termination; delayed transition
    ClientSeries                 obligation:offboarding_plan
    Company                      receivable:orderly_exit

2025-01-01 PCI-DSS-001 PCI DSS and Payment Card Data Controls
    ; frequency: CONTINUOUS
    ; source: B6 §8.3-8.6
    ; deadline: Continuous
    ; penalty: Security incident, service suspension
    ClientSeries                 obligation:pci_compliance
    Company                      receivable:security
```

---

## Company → ClientSeries Obligations

```ledger
2025-01-01 OBL-CO-CLIENT-001 Provide Infrastructure
    ; frequency: CONTINUOUS
    ; source: F1 Recital A, B11 §1
    ; deadline: Per SLA
    ; penalty: SLA credits
    Company                      obligation:infrastructure
    ClientSeries                 receivable:services

2025-01-01 OBL-CO-CLIENT-002 Compliance Support
    ; frequency: CONTINUOUS
    ; source: B11 §4
    ; deadline: Per SLA
    ; penalty: SLA credits
    Company                      obligation:compliance_support
    ClientSeries                 receivable:services

2025-01-01 OBL-CO-CLIENT-003 FinCEN Renewal Reminder
    ; frequency: BIENNIAL (90/60/30 days before)
    ; source: N5 §5.3
    ; deadline: 90, 60, 30 days before expiry
    ; penalty: None (courtesy only)
    Company                      obligation:renewal_reminder
    ClientSeries                 receivable:notice

2025-01-01 OBL-CO-CLIENT-004 Schedule Update Notice
    ; frequency: ON_CHANGE
    ; source: C3 §7.2
    ; deadline: 60 days before fee increase
    ; penalty: Fee change invalid
    Company                      obligation:fee_notice
    ClientSeries                 receivable:notice

2025-01-01 PARTNER-SUSPEND-001 Suspend Routing During Partner MSB Disruption
    ; frequency: ON_EVENT
    ; source: N3 §7.3.1
    ; deadline: Immediately upon confirmed disruption
    ; penalty: Regulatory exposure
    Company                      obligation:routing_suspension
    ClientSeries                 receivable:protection

2025-01-01 LICENSING-ROADMAP-001 Quarterly Coverage and Licensing Review
    ; frequency: QUARTERLY + ON_CHANGE
    ; source: B11 §7.9
    ; deadline: Quarterly
    ; penalty: Increased regulatory/operational risk
    Company                      obligation:licensing_roadmap
    ClientSeries                 receivable:clarity

2025-01-01 OMNIBUS-TRUST-001 Omnibus Account Trust Controls
    ; frequency: CONTINUOUS
    ; source: B10 §4.2.1
    ; deadline: Continuous
    ; penalty: Funds safeguarding failure
    Company                      obligation:omnibus_trust
    ClientSeries                 receivable:funds_safeguarding
```

---

## ClientSeries → EndCustomer Obligations

```ledger
2025-01-01 ELIGIBILITY-AGE-001 End-Customer Minimum Age
    ; frequency: CONTINUOUS
    ; source: F2 §6E.1
    ; deadline: Continuous
    ; penalty: Account termination, regulatory exposure
    ClientSeries                 obligation:age_gate
    EndCustomer                  receivable:eligibility

2025-01-01 TERMINATION-CUSTOMER-001 End-Customer Account Termination Process
    ; frequency: ON_REQUEST + ON_EVENT
    ; source: F2 §6C
    ; deadline: As required by law and disclosed terms
    ; penalty: Complaint/escalation risk
    ClientSeries                 obligation:termination_process
    EndCustomer                  receivable:process

2025-01-01 RECEIPT-CUSTOMER-001 End-Customer Receipts and Statements
    ; frequency: PER_TRANSACTION + PERIODIC
    ; source: F2 §6D
    ; deadline: At transaction time and per statement cadence
    ; penalty: Consumer protection exposure
    ClientSeries                 obligation:receipts
    EndCustomer                  receivable:disclosures

2025-01-01 STATE-CONSUMER-NOTICE-001 State-Specific Consumer Disclosures
    ; frequency: CONTINUOUS
    ; source: B11 §12.6; N3 §8.1; F2 §6D.5
    ; deadline: Continuous
    ; penalty: Consumer protection exposure
    ClientSeries                 obligation:state_disclosures
    EndCustomer                  receivable:disclosures

2025-01-01 REFUND-CUSTOMER-001 Refunds, Cancellations, and Reversals
    ; frequency: ON_REQUEST + ON_EVENT
    ; source: F2 §6H; N3 §8.3
    ; deadline: Per disclosed terms and applicable law
    ; penalty: Complaint/escalation risk
    ClientSeries                 obligation:refunds
    EndCustomer                  receivable:refund

2025-01-01 REMITTANCE-CUSTOMER-001 Remittance Transfer Disclosures and Rights
    ; frequency: ON_TRANSACTION
    ; source: F2 §6A.7; N3 §8.4
    ; deadline: At transaction time; per applicable law
    ; penalty: Consumer protection exposure
    ClientSeries                 obligation:remittance_compliance
    EndCustomer                  receivable:disclosures
```

---

## Officer → Company Obligations

```ledger
2025-01-01 OBL-OFF-001 CCO BSA Program Maintenance
    ; frequency: CONTINUOUS
    ; source: B5 §2.1
    ; deadline: Continuous
    ; penalty: Regulatory liability
    CCO                          obligation:bsa_program
    Company                      receivable:compliance

2025-01-01 OBL-OFF-002 CCO Annual Training
    ; frequency: ANNUAL
    ; source: B5 §7.1
    ; deadline: Annual
    ; penalty: Compliance violation
    CCO                          obligation:bsa_training
    Company                      receivable:compliance

2025-01-01 OBL-OFF-003 BSA Officer Succession
    ; frequency: ON_VACANCY
    ; source: B3 §6.6
    ; deadline: 72 hours interim, 30 days permanent
    ; penalty: Regulatory violation
    Manager                      obligation:bsa_succession
    Company                      receivable:compliance

2025-01-01 OFFICER-NOTIFY-001 Officer Change Notification
    ; frequency: ON_CHANGE
    ; source: B2 §4.1
    ; deadline: Within 10 business days
    ; penalty: Compliance violation
    Manager                      obligation:officer_notification
    Company                      receivable:documentation

2025-01-01 OFFICER-REPLACE-001 Officer Replacement
    ; frequency: ON_VACANCY
    ; source: B1 §6.7, B1 §7.5
    ; deadline: 60 days for permanent replacement
    ; penalty: Governance gap
    Manager                      obligation:officer_replacement
    Company                      receivable:compliance

2025-01-01 SCALE-PLAN-001 Scaling and Capacity Planning
    ; frequency: QUARTERLY
    ; source: B1 §5.5
    ; deadline: Quarterly
    ; penalty: Operational/compliance bottlenecks
    Manager                      obligation:capacity_planning
    Company                      receivable:resilience

2025-01-01 INTERSERIES-CONFLICT-001 Inter-Series Conflict Management
    ; frequency: ON_EVENT
    ; source: B1 §4.8
    ; deadline: Promptly upon identification
    ; penalty: Enterprise risk
    Manager                      obligation:conflict_management
    Company                      receivable:stability

2025-01-01 COMPANY-DISSOLUTION-CONTINUITY-001 Company Dissolution Continuity Plan
    ; frequency: ON_TRIGGER
    ; source: B1 §15.3
    ; deadline: Upon dissolution trigger
    ; penalty: Client/end-customer harm
    Manager                      obligation:continuity_plan
    Company                      receivable:orderly_winddown

2025-01-01 OVERSIGHT-001 Independent Oversight and External Review
    ; frequency: ANNUAL
    ; source: B1 §14.10
    ; deadline: Annual
    ; penalty: Governance weakness
    Manager                      obligation:independent_oversight
    Company                      receivable:assurance

2025-01-01 TRANSFER-PRICING-001 Transfer Pricing Documentation
    ; frequency: ANNUAL
    ; source: B1 §11.6
    ; deadline: Annual
    ; penalty: Tax/accounting risk
    CFO                          obligation:transfer_pricing
    Company                      receivable:documentation

2025-01-01 OMNIBUS-RECON-001 Omnibus Account Reconciliation Evidence
    ; frequency: DAILY
    ; source: B10 §4.4.1
    ; deadline: Daily
    ; penalty: Funds safeguarding failure
    CFO                          obligation:omnibus_reconciliation
    Company                      receivable:proof

2025-01-01 OFFICER-REVIEW-001 Officer Performance Review
    ; frequency: ANNUAL
    ; source: B3 §4.1
    ; deadline: Annual
    ; penalty: Governance violation
    Manager                      obligation:officer_review
    Company                      receivable:compliance

2025-01-01 TRAINING-ETHICS-001 Ethics Training
    ; frequency: ANNUAL
    ; source: B9 §3.1
    ; deadline: Annual
    ; penalty: Compliance violation
    Officers                     obligation:ethics_training
    Company                      receivable:compliance

2025-12-14 CONFLICT-REVIEW-001 Conflict of Interest Annual Review
    ; frequency: ANNUAL
    ; source: B1 §14.9.7
    ; deadline: Annual
    ; penalty: Governance violation
    CCO                          obligation:conflict_review
    Company                      receivable:compliance

2025-01-01 CAPITAL-MIN-001 Minimum Capital Maintenance
    ; frequency: CONTINUOUS
    ; source: B10 §2.1
    ; deadline: Continuous
    ; penalty: Regulatory violation
    Company                      obligation:capital_maintenance
    Regulator                    receivable:compliance

2025-01-01 OBL-INS-001 Insurance Maintenance
    ; frequency: ANNUAL
    ; source: B10 §3.1
    ; deadline: Annual renewal
    ; penalty: Operating without coverage
    Company                      obligation:insurance
    Insurer                      receivable:premium

2025-01-01 OBL-OFF-004 Officer Screening
    ; frequency: ON_APPOINTMENT
    ; source: B9 §2.1
    ; deadline: Before appointment
    ; penalty: Invalid appointment
    Manager                      obligation:officer_screening
    Company                      receivable:compliance

2025-01-01 OBL-OFF-005 CCO Qualifications
    ; frequency: CONTINUOUS
    ; source: B9 §2.5
    ; deadline: At appointment and continuous
    ; penalty: Disqualification
    CCO                          obligation:cams_certification
    Company                      receivable:qualification
```

---

## Obligation Summary by Frequency

### Continuous Obligations
| ID | Obligor | Obligation | Source |
|----|---------|------------|--------|
| OBL-CLIENT-CO-005 | ClientSeries | AUP Compliance | B7 §1.1 |
| OBL-CLIENT-CO-006 | ClientSeries | Geographic Restrictions | B7 §9, N3 |
| OBL-CO-CLIENT-001 | Company | Infrastructure | F1, B11 |
| OBL-OFF-001 | CCO | BSA Program | B5 §2.1 |

### Annual Obligations
| ID | Obligor | Obligation | Deadline | Source |
|----|---------|------------|----------|--------|
| OBL-REG-003 | Company | MT Annual Report | April 15 | E1 §7.1.1 |
| OBL-OFF-002 | CCO | BSA Training | Annual | B5 §7.1 |

### Biennial Obligations
| ID | Obligor | Obligation | Source |
|----|---------|------------|--------|
| OBL-REG-001 | Company | FinCEN Renewal | E1 §7.2.1 |
| OBL-CLIENT-REG-001 | ClientSeries | FinCEN Renewal | E1 §7.2.2 |

### Monthly Obligations
| ID | Obligor | Obligation | Deadline | Amount | Source |
|----|---------|------------|----------|--------|--------|
| OBL-CLIENT-CO-001 | ClientSeries | Platform Fee | 10 days | $2,500 | C3 §3.1 |

### One-Time Obligations
| ID | Obligor | Obligation | Trigger | Amount | Source |
|----|---------|------------|---------|--------|--------|
| OBL-CLIENT-CO-002 | ClientSeries | Onboarding Fee | CSA exec | $10,000 | C3 §2.1 |
| OBL-CLIENT-CO-003 | ClientSeries | Training Fee | Training | $10,000 | C3 §2.2 |
| OBL-CLIENT-CO-004 | ClientSeries | FinCEN Proof | Before ACTIVE | - | E1 §6.1.6 |

---

## Obligation Validation Rules

```yaml
obligation_mvp_conditions:
  - rule_id: RULE-MVP-001
    name: all_obligations_have_source
    description: Every obligation must cite authoritative document
    check: ALL obligations HAVE source IS NOT NULL
    severity: ERROR
    
  - rule_id: RULE-MVP-002
    name: all_obligations_have_deadline
    description: Every obligation must have deadline or frequency
    check: ALL obligations HAVE (deadline IS NOT NULL OR frequency IS NOT NULL)
    severity: ERROR
    
  - rule_id: RULE-MVP-003
    name: reciprocal_obligations_balanced
    description: Obligations between parties should be reciprocal
    check: FOR_EACH obligation WHERE obligor == ClientSeries AND obligee == Company
           THERE_EXISTS obligation WHERE obligor == Company AND obligee == ClientSeries
    severity: WARNING
    
  - rule_id: RULE-MVP-004
    name: no_conflicting_deadlines
    description: Same obligation should not have conflicting deadlines
    check: NO duplicate obligation_id WITH different deadlines
    severity: ERROR
```

---

## Calendar Generation

This ledger can generate compliance calendars:

```bash
# Generate calendar for Company obligations due in Q1 2026
./generate_calendar.sh --obligor Company --period 2026-Q1

# Generate calendar for all ClientSeries FinCEN renewals
./generate_calendar.sh --obligation fincen_renewal --type ClientSeries
```

Output format:
```
2026-01-15  OBL-REG-0XX  Example: Montana Annual Report (90 days warning)
2026-03-01  OBL-REG-0YY  Example: FinCEN Renewal (if due)
2026-04-15  OBL-REG-0XX  Example: Montana Annual Report (DEADLINE)
```
