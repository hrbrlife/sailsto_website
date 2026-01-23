# Flow Registry Index

> **Purpose**: Master index of all process flows used across CCASH documents.
> All `[FLOW:*]` markers must reference a flow defined in this registry.

---

## Statistics

| Category | Count | Status |
|----------|-------|--------|
| Formation Flows | 6 | Defined |
| Onboarding Flows | 10 | Defined |
| Compliance Flows | 18 | Defined |
| Operations Flows | 12 | Defined |
| Financial Flows | 8 | Defined |
| Governance Flows | 8 | Defined |
| IT/Security Flows | 6 | Defined |
| Dispute Flows | 4 | Defined |
| Annual Compliance | 3 | Defined |
| **Total** | **75** | ✓ Complete |

---

## ID Normalization Rules

All flow IDs use **snake_case**:
- ✓ `client_onboarding`
- ✗ `Client_Onboarding` → normalize to `client_onboarding`
- ✗ `clientOnboarding` → normalize to `client_onboarding`

**Aliases**: Some flows have legacy IDs that should be normalized:
| Legacy ID | Canonical ID |
|-----------|--------------|
| `Access_Control` | `access_control` |
| `AI_Compliance` | `ai_compliance` |
| `AI_Data_Processing` | `ai_data_processing` |
| `AI_Operations` | `ai_operations` |
| `AI_Security` | `ai_security` |
| `AML_Risk_Assessment` | `aml_risk_assessment` |
| `Annual_Compliance` | `annual_compliance` |
| `Arbitration` | `arbitration` |
| `BCP_DRP` | `bcp_drp` |
| `Breach_Response` | `breach_response` |
| `BSA_eFiling` | `bsa_efiling` |
| `BSA_Officer_Succession` | `bsa_officer_succession` |
| `Capital_Management` | `capital_management` |
| `Cash_Management` | `cash_management` |
| `CCO_Qualification` | `cco_qualification` |
| `CDD_EDD` | `cdd_edd` |
| `Change_Management` | `change_management` |
| `CIP` | `cip` |
| `Client_Audit` | `client_audit` |
| `Client_Fund_Trust` | `client_fund_trust` |
| `Client_Insolvency` | `client_insolvency` |
| `Client_Offboarding` | `client_offboarding` |
| `Client_Onboarding` | `client_onboarding` |
| `Compliance` | `compliance_review` |
| `Compliance_Controls` | `compliance_controls` |
| `Compliance_Enforcement` | `compliance_enforcement` |
| `Compliance_Records` | `compliance_records` |
| `Compliance_Training` | `compliance_training` |
| `Cross_Border_Transfer` | `cross_border_transfer` |
| `Data_Processing` | `data_processing` |
| `Data_Sharing` | `data_sharing` |
| `Data_Subject_Rights` | `data_subject_rights` |
| `Disclosure` | `disclosure` |
| `Dispute_Resolution` | `dispute_resolution` |
| `EFTA_Disclosure` | `efta_disclosure` |
| `Emergency_Succession` | `emergency_succession` |
| `Ethics_Compliance` | `ethics_compliance` |
| `Fee_Dispute` | `fee_dispute` |
| `Financial_Controls` | `financial_controls` |
| `Fit_Proper_Screening` | `fit_proper_screening` |
| `Formation` | `formation` |
| `Geographic_Compliance` | `geographic_compliance` |
| `Governance_Setup` | `governance_setup` |
| `Incident_Response` | `incident_response` |
| `Insurance_Coverage` | `insurance_coverage` |
| `Involuntary_Departure` | `involuntary_departure` |
| `Key_Management` | `key_management` |
| `Loss_Allocation` | `loss_allocation` |
| `MSB_Registration` | `msb_registration` |
| `MTL_Compliance` | `mtl_compliance` |
| `Officer_Appointment` | `officer_appointment` |
| `Officer_Rotation` | `officer_rotation` |
| `Onboarding` | `client_onboarding` |
| `Partner_MSB_Routing` | `partner_msb_routing` |
| `Performance_Review` | `performance_review` |
| `Pricing` | `pricing` |
| `Prohibited_Use_Screening` | `prohibited_use_screening` |
| `Record_Destruction` | `record_destruction` |
| `Record_Management` | `record_management` |
| `registration_verification` | `fincen_registration` |
| `Regulatory_Reporting` | `regulatory_reporting` |
| `Regulatory_Setup` | `regulatory_setup` |
| `Routing` | `routing` |
| `Sanctions_Screening` | `sanctions_screening` |
| `SAR_Filing` | `sar_filing` |
| `Schedule_Update` | `schedule_update` |
| `Securities_Offering` | `securities_offering` |
| `Series_Dissolution` | `series_dissolution` |
| `Series_Separation` | `series_separation` |
| `Series_Structure` | `series_structure` |
| `Service_Delivery` | `service_delivery` |
| `Succession_Planning` | `succession_planning` |
| `Transaction_Monitoring` | `transaction_monitoring` |
| `Transaction_Pricing` | `transaction_pricing` |
| `Travel_Rule` | `travel_rule` |
| `Voluntary_Departure` | `voluntary_departure` |

---

## Formation Flows

### formation
- **ID**: `formation`
- **Owner**: Manager
- **Documents**: [DOC:A1], [DOC:E1]
- **Description**: Initial LLC formation with Montana SOS
- **Trigger**: Business decision to form entity
- **States**: `DRAFT → FILED → APPROVED → ACTIVE`

### governance_setup
- **ID**: `governance_setup`
- **Owner**: Manager
- **Documents**: [DOC:B1], [DOC:B2], [DOC:E1]
- **Description**: Post-formation governance establishment
- **Trigger**: Formation approved
- **States**: `PENDING → OFFICERS_APPOINTED → POLICIES_ADOPTED → COMPLETE`

### series_structure
- **ID**: `series_structure`
- **Owner**: Manager
- **Documents**: [DOC:A2], [DOC:A3]
- **Description**: Functional series establishment
- **Trigger**: Governance complete
- **States**: `PLANNED → DOCUMENTED → FILED → ACTIVE`

### company_dissolution
- **ID**: `company_dissolution`
- **Owner**: Manager
- **Documents**: [DOC:B1]
- **Description**: LLC dissolution process
- **Trigger**: Manager decision or statutory requirement
- **States**: `INITIATED → WIND_DOWN → FILED → DISSOLVED`

---

## Onboarding Flows

### client_onboarding
- **ID**: `client_onboarding`
- **Owner**: CCO
- **Documents**: [DOC:F1], [DOC:E1], [DOC:N5]
- **Description**: Full client series onboarding process
- **Trigger**: Sales qualified lead
- **SLA**: 30 business days
- **States**: See `flows/client_onboarding.md` for full state diagram
- **Detailed Flow**: [flows/client_onboarding.md](./client_onboarding.md)

### client_termination
- **ID**: `client_termination`
- **Owner**: CCO
- **Documents**: [DOC:F1], [DOC:B11]
- **Description**: Client series offboarding and wind-down
- **Trigger**: Termination notice or breach
- **States**: `NOTICE → WIND_DOWN → FINAL_SETTLEMENT → TERMINATED`

### ein_application
- **ID**: `ein_application`
- **Owner**: Client Series
- **Documents**: [DOC:N5]
- **Description**: IRS EIN application process
- **Trigger**: CSA execution
- **States**: `PENDING → APPLIED → RECEIVED`

### fincen_registration
- **ID**: `fincen_registration`
- **Owner**: Client Series
- **Documents**: [DOC:N5], [DOC:E1]
- **Description**: Initial FinCEN MSB registration
- **Trigger**: EIN received
- **States**: `PENDING → FILED → CONFIRMED → ACTIVE`

### fincen_renewal
- **ID**: `fincen_renewal`
- **Owner**: Client Series
- **Documents**: [DOC:N5]
- **Description**: Biennial FinCEN registration renewal
- **Trigger**: 2-year anniversary (reminders at 90/60/30 days)
- **States**: `DUE → FILED → CONFIRMED`

### fincen_update
- **ID**: `fincen_update`
- **Owner**: Client Series
- **Documents**: [DOC:N5]
- **Description**: FinCEN registration information update
- **Trigger**: Material change to registration info
- **Deadline**: Within 180 days of change
- **States**: `CHANGE_IDENTIFIED → FILED → CONFIRMED`

### client_offboarding
- **ID**: `client_offboarding`
- **Owner**: CCO
- **Documents**: [DOC:F1], [DOC:B11]
- **Description**: Client series wind-down and separation
- **Trigger**: Termination or non-renewal
- **Alias**: `Client_Offboarding`
- **States**: `INITIATED → WIND_DOWN → FINAL_SETTLEMENT → SEPARATED`

### series_dissolution
- **ID**: `series_dissolution`
- **Owner**: Manager
- **Documents**: [DOC:B1], [DOC:B11], [DOC:D1]
- **Description**: Formal dissolution of a Series including state filings and FinCEN notification
- **Trigger**: Completion of client_offboarding or Manager decision
- **Alias**: `Series_Dissolution`
- **States**: `TERMINATION_EVENT → WIND_DOWN → FUND_DISTRIBUTION → FINCEN_NOTICE → STATE_FILING → DISSOLVED`
- **References**: B1 Article 16, B11 §11.10

### client_insolvency
- **ID**: `client_insolvency`
- **Owner**: Manager/CCO
- **Documents**: [DOC:F1], [DOC:B10]
- **Description**: Client series insolvency handling
- **Trigger**: Client bankruptcy or inability to pay
- **States**: `IDENTIFIED → SUSPENDED → WIND_DOWN → RESOLUTION`

### regulatory_setup
- **ID**: `regulatory_setup`
- **Owner**: CCO
- **Documents**: [DOC:E1]
- **Description**: Post-formation regulatory registration setup
- **Trigger**: Governance setup complete
- **States**: `PLANNED → EIN_OBTAINED → FINCEN_FILED → ACTIVE`

### bsa_efiling
- **ID**: `bsa_efiling`
- **Owner**: CCO
- **Documents**: [DOC:B5], [DOC:E1]
- **Description**: BSA E-Filing system submission
- **Trigger**: SAR requirement or FinCEN filing
- **States**: `PREPARED → SUBMITTED → ACKNOWLEDGED → FILED`

---

## Compliance Flows

### aml_risk_assessment
- **ID**: `aml_risk_assessment`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Enterprise AML risk assessment
- **Frequency**: Annual + on material change
- **States**: `SCHEDULED → IN_PROGRESS → DRAFT → APPROVED`

### cip
- **ID**: `cip`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Customer Identification Program execution
- **Trigger**: New customer relationship
- **States**: `INITIATED → DOCUMENTS_RECEIVED → VERIFIED → COMPLETE`

### cdd_edd
- **ID**: `cdd_edd`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Customer Due Diligence / Enhanced Due Diligence
- **Trigger**: CIP complete or risk flag
- **States**: `STANDARD_CDD → RISK_ASSESSED → EDD_IF_REQUIRED → COMPLETE`

### sanctions_screening
- **ID**: `sanctions_screening`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: OFAC and sanctions list screening
- **Trigger**: New customer, transaction, or list update
- **States**: `SCREENING → CLEAR | MATCH → ESCALATION → RESOLUTION`

### transaction_monitoring
- **ID**: `transaction_monitoring`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Ongoing transaction surveillance
- **Trigger**: Continuous
- **States**: `MONITORING → ALERT → REVIEW → CLEAR | SAR_REQUIRED`

### sar_filing
- **ID**: `sar_filing`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Suspicious Activity Report filing
- **Trigger**: SAR determination from monitoring
- **Deadline**: 30 days from determination
- **States**: `IDENTIFIED → DRAFTED → REVIEWED → FILED`

### regulatory_reporting
- **ID**: `regulatory_reporting`
- **Owner**: CCO
- **Documents**: [DOC:B5], [DOC:B4]
- **Description**: General regulatory reporting obligations
- **Frequency**: As required by regulation
- **States**: `DUE → PREPARED → REVIEWED → FILED`

### compliance_training
- **ID**: `compliance_training`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: BSA/AML compliance training program
- **Frequency**: Initial + annual
- **States**: `SCHEDULED → DELIVERED → TESTED → DOCUMENTED`

### compliance_review
- **ID**: `compliance_review`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Independent compliance program review
- **Frequency**: Annual
- **States**: `SCHEDULED → IN_PROGRESS → FINDINGS → REMEDIATION`

### compliance_enforcement
- **ID**: `compliance_enforcement`
- **Owner**: CCO
- **Documents**: [DOC:B5], [DOC:B7]
- **Description**: Enforcement of compliance policies
- **Trigger**: Policy violation detected
- **States**: `VIOLATION → INVESTIGATION → DETERMINATION → ACTION`

### travel_rule
- **ID**: `travel_rule`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Travel Rule compliance for transfers >$3,000
- **Trigger**: Qualifying transfer
- **States**: `TRANSFER_INITIATED → INFO_COLLECTED → INFO_TRANSMITTED → COMPLETE`

### mtl_compliance
- **ID**: `mtl_compliance`
- **Owner**: CCO
- **Documents**: [DOC:E2], [DOC:N3]
- **Description**: State money transmitter license compliance
- **Trigger**: Interstate operations via Partner MSB
- **States**: `MONITORING → COMPLIANT | ISSUE → REMEDIATION`

### geographic_compliance
- **ID**: `geographic_compliance`
- **Owner**: CCO
- **Documents**: [DOC:N3], [DOC:B7]
- **Description**: Geographic operations compliance
- **Trigger**: Transaction with state/territory implications
- **States**: `STATE_CHECK → APPROVED | PROHIBITED | PARTNER_REQUIRED`

### prohibited_use_screening
- **ID**: `prohibited_use_screening`
- **Owner**: CCO
- **Documents**: [DOC:B7]
- **Description**: Prohibited use detection and enforcement
- **Trigger**: Transaction or activity review
- **States**: `SCREENING → CLEAR | FLAG → INVESTIGATION → ACTION`

### fit_proper_screening
- **ID**: `fit_proper_screening`
- **Owner**: CCO
- **Documents**: [DOC:B9]
- **Description**: Fit and proper person screening for officers/control persons
- **Trigger**: New appointment or periodic review
- **States**: `INITIATED → BACKGROUND_CHECK → REVIEWED → CLEARED | FAILED`

### ethics_compliance
- **ID**: `ethics_compliance`
- **Owner**: CCO
- **Documents**: [DOC:B9]
- **Description**: Ethics and conflict of interest compliance
- **Trigger**: Disclosure or concern raised
- **States**: `DISCLOSURE → REVIEW → CLEARED | CONFLICT → MITIGATION`

### msb_registration
- **ID**: `msb_registration`
- **Owner**: CCO
- **Documents**: [DOC:E1], [DOC:N5]
- **Description**: MSB registration maintenance
- **Trigger**: Initial or renewal
- **States**: `PENDING → FILED → ACTIVE → RENEWAL_DUE`

---

## Operations Flows

### service_delivery
- **ID**: `service_delivery`
- **Owner**: CTO
- **Documents**: [DOC:F1], [DOC:B11]
- **Description**: Core platform service delivery
- **Trigger**: Client active
- **States**: `PROVISIONED → OPERATIONAL → MONITORING`

### partner_msb_routing
- **ID**: `partner_msb_routing`
- **Owner**: Operations
- **Documents**: [DOC:N3], [DOC:C3]
- **Description**: Transaction routing through Partner MSB
- **Trigger**: Interstate transaction
- **States**: `RECEIVED → STATE_CHECK → ROUTED → SETTLED`

### cross_border_transfer
- **ID**: `cross_border_transfer`
- **Owner**: Operations
- **Documents**: [DOC:B5]
- **Description**: Cross-border transfer processing
- **Trigger**: International transaction
- **States**: `RECEIVED → SCREENED → PROCESSED → COMPLETE`

### schedule_update
- **ID**: `schedule_update`
- **Owner**: CCO
- **Documents**: [DOC:N3], [DOC:C3]
- **Description**: Schedule document update process
- **Trigger**: Regulatory change or business decision
- **States**: `DRAFTED → REVIEWED → APPROVED → PUBLISHED → NOTIFIED`

### record_management
- **ID**: `record_management`
- **Owner**: CCO
- **Documents**: [DOC:B4]
- **Description**: Record retention and management
- **Trigger**: Record creation
- **States**: `CREATED → CLASSIFIED → STORED → RETENTION_PERIOD → DESTRUCTION_ELIGIBLE`

### record_destruction
- **ID**: `record_destruction`
- **Owner**: CCO
- **Documents**: [DOC:B4]
- **Description**: Secure record destruction
- **Trigger**: Retention period expired
- **States**: `ELIGIBLE → APPROVED → DESTROYED → DOCUMENTED`

### client_audit
- **ID**: `client_audit`
- **Owner**: CCO
- **Documents**: [DOC:F1], [DOC:C3]
- **Description**: Company audit of Client Series
- **Trigger**: Scheduled or for-cause
- **States**: `SCHEDULED → NOTICE → CONDUCTED → FINDINGS → REMEDIATION`

### securities_offering
- **ID**: `securities_offering`
- **Owner**: CFO
- **Documents**: [DOC:E2]
- **Description**: Securities offering process (S-1 Series)
- **Trigger**: Capital raise decision
- **States**: `PLANNING → DOCUMENTATION → FILING → OFFERING → CLOSED`

### pricing
- **ID**: `pricing`
- **Owner**: CFO
- **Documents**: [DOC:C3]
- **Description**: Pricing and fee management
- **Trigger**: Schedule update or client negotiation
- **States**: `PROPOSED → REVIEWED → APPROVED → EFFECTIVE`

### transaction_pricing
- **ID**: `transaction_pricing`
- **Owner**: Operations
- **Documents**: [DOC:C3]
- **Description**: Per-transaction pricing calculation
- **Trigger**: Transaction
- **States**: `CALCULATED → APPLIED → INVOICED`

### routing
- **ID**: `routing`
- **Owner**: Operations
- **Documents**: [DOC:C3], [DOC:N3]
- **Description**: Transaction routing decision
- **Trigger**: Transaction received
- **States**: `RECEIVED → CLASSIFIED → ROUTED → CONFIRMED`

---

## Financial Flows

### cash_management
- **ID**: `cash_management`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Cash and liquidity management
- **Trigger**: Continuous
- **States**: `MONITORING → FORECASTING → ACTION_IF_NEEDED`

### capital_management
- **ID**: `capital_management`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Capital adequacy management
- **Trigger**: Continuous
- **States**: `MONITORING → ASSESSMENT → COMPLIANT | ACTION_REQUIRED`

### insurance_coverage
- **ID**: `insurance_coverage`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Insurance policy management
- **Trigger**: Annual renewal or material change
- **States**: `REVIEW → RENEWAL → BOUND → ACTIVE`

### client_fund_trust
- **ID**: `client_fund_trust`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Client fund segregation and trust
- **Trigger**: Continuous
- **States**: `RECEIVED → SEGREGATED → HELD → DISBURSED`

### loss_allocation
- **ID**: `loss_allocation`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Loss allocation per series
- **Trigger**: Loss event
- **States**: `IDENTIFIED → ALLOCATED → DOCUMENTED → RECOVERED_IF_APPLICABLE`

### series_separation
- **ID**: `series_separation`
- **Owner**: CFO
- **Documents**: [DOC:A1], [DOC:B1]
- **Description**: Series liability separation maintenance
- **Trigger**: Continuous
- **States**: `MONITORING → COMPLIANT | BREACH → REMEDIATION`

### financial_controls
- **ID**: `financial_controls`
- **Owner**: CFO
- **Documents**: [DOC:B10]
- **Description**: Financial control environment
- **Trigger**: Continuous
- **States**: `DESIGNED → IMPLEMENTED → TESTED → OPERATING`

### fee_dispute
- **ID**: `fee_dispute`
- **Owner**: CFO
- **Documents**: [DOC:C3]
- **Description**: Fee dispute resolution
- **Trigger**: Client fee dispute
- **States**: `RECEIVED → REVIEWED → RESOLVED | ESCALATED`

---

## Governance Flows

### officer_appointment
- **ID**: `officer_appointment`
- **Owner**: Manager
- **Documents**: [DOC:B2], [DOC:B9]
- **Description**: Officer appointment process
- **Trigger**: Vacancy or new position
- **States**: `IDENTIFIED → SCREENED → APPOINTED → EFFECTIVE`

### officer_rotation
- **ID**: `officer_rotation`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Planned officer rotation
- **Trigger**: Term expiration or planned transition
- **States**: `SCHEDULED → TRANSITION_PLANNING → HANDOVER → COMPLETE`

### voluntary_departure
- **ID**: `voluntary_departure`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Officer voluntary departure
- **Trigger**: Resignation
- **States**: `NOTICE → TRANSITION → DEPARTURE → DOCUMENTED`

### involuntary_departure
- **ID**: `involuntary_departure`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Officer involuntary departure
- **Trigger**: Termination for cause or incapacity
- **States**: `DETERMINATION → IMMEDIATE_OR_TRANSITION → DEPARTURE → DOCUMENTED`

### emergency_succession
- **ID**: `emergency_succession`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Emergency succession activation
- **Trigger**: Sudden departure of key officer
- **States**: `TRIGGERED → INTERIM_APPOINTED → PERMANENT_SEARCH → RESOLVED`

### bsa_officer_succession
- **ID**: `bsa_officer_succession`
- **Owner**: Manager
- **Documents**: [DOC:B3], [DOC:B5]
- **Description**: BSA Officer (CCO) succession
- **Trigger**: CCO departure
- **States**: `TRIGGERED → BACKUP_ACTIVATED → PERMANENT_APPOINTED → REGULATORS_NOTIFIED`

### succession_planning
- **ID**: `succession_planning`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Ongoing succession planning
- **Trigger**: Annual review
- **States**: `REVIEW → CANDIDATES_IDENTIFIED → DOCUMENTED → UPDATED`

### performance_review
- **ID**: `performance_review`
- **Owner**: Manager
- **Documents**: [DOC:B3]
- **Description**: Officer performance review
- **Trigger**: Annual
- **States**: `SCHEDULED → CONDUCTED → DOCUMENTED → ACTION_IF_NEEDED`

### cco_qualification
- **ID**: `cco_qualification`
- **Owner**: Manager
- **Documents**: [DOC:B3], [DOC:B9]
- **Description**: CCO qualification verification
- **Trigger**: Appointment or periodic review
- **States**: `CREDENTIALS_VERIFIED → EXPERIENCE_VERIFIED → QUALIFIED → DOCUMENTED`

---

## IT and Security Flows

### bcp_drp
- **ID**: `bcp_drp`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: Business Continuity / Disaster Recovery planning
- **Trigger**: Annual test or incident
- **States**: `PLANNED → TESTED → FINDINGS → UPDATED`

### incident_response
- **ID**: `incident_response`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: Security incident response
- **Trigger**: Incident detected
- **States**: `DETECTED → CONTAINED → ERADICATED → RECOVERED → POST_MORTEM`

### breach_response
- **ID**: `breach_response`
- **Owner**: CCO
- **Documents**: [DOC:B6], [DOC:B8]
- **Description**: Data breach response
- **Trigger**: Breach confirmed
- **States**: `CONFIRMED → ASSESSED → NOTIFIED → REMEDIATED → DOCUMENTED`

### change_management
- **ID**: `change_management`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: IT change management
- **Trigger**: System change request
- **States**: `REQUESTED → REVIEWED → APPROVED → IMPLEMENTED → VERIFIED`

### access_control
- **ID**: `access_control`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: Access control management
- **Trigger**: Access request or review
- **States**: `REQUESTED → APPROVED → PROVISIONED → REVIEWED → REVOKED_IF_NEEDED`

### key_management
- **ID**: `key_management`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: Cryptographic key management
- **Trigger**: Key lifecycle event
- **States**: `GENERATED → ACTIVE → ROTATION_DUE → ROTATED → RETIRED`

---

## Data Privacy Flows

### data_processing
- **ID**: `data_processing`
- **Owner**: CCO
- **Documents**: [DOC:B8]
- **Description**: Personal data processing
- **Trigger**: Data collection
- **States**: `COLLECTED → PURPOSE_DEFINED → PROCESSED → RETAINED → DELETED`

### data_sharing
- **ID**: `data_sharing`
- **Owner**: CCO
- **Documents**: [DOC:B8], [DOC:F2]
- **Description**: Data sharing with third parties
- **Trigger**: Sharing request or requirement
- **States**: `REQUESTED → JUSTIFIED → SAFEGUARDS → SHARED → DOCUMENTED`

### data_subject_rights
- **ID**: `data_subject_rights`
- **Owner**: CCO
- **Documents**: [DOC:B8]
- **Description**: Data subject rights request handling
- **Trigger**: Rights request received
- **States**: `RECEIVED → VERIFIED → PROCESSED → RESPONDED`

### ai_data_processing
- **ID**: `ai_data_processing`
- **Owner**: CCO
- **Documents**: [DOC:F2], [DOC:00_Business_Model]
- **Description**: AI-assisted data processing
- **Trigger**: AI system interaction
- **States**: `INPUT → PROCESSED → OUTPUT → DISCLOSED`

### ai_operations
- **ID**: `ai_operations`
- **Owner**: CTO
- **Documents**: [DOC:00_Business_Model]
- **Description**: AI operations management
- **Trigger**: Continuous
- **States**: `MONITORING → OPERATING → HUMAN_REVIEW_IF_FLAGGED`

### ai_compliance
- **ID**: `ai_compliance`
- **Owner**: CCO
- **Documents**: [DOC:F2]
- **Description**: AI system compliance verification
- **Trigger**: Periodic or regulatory change
- **States**: `ASSESSED → COMPLIANT | GAP → REMEDIATION`

### ai_security
- **ID**: `ai_security`
- **Owner**: CTO
- **Documents**: [DOC:B6]
- **Description**: AI system security
- **Trigger**: Continuous
- **States**: `MONITORING → SECURE | THREAT → RESPONSE`

---

## Dispute Flows

### arbitration
- **ID**: `arbitration`
- **Owner**: GC
- **Documents**: [DOC:F1], [DOC:F2]
- **Description**: Binding arbitration process
- **Trigger**: Dispute unresolved through negotiation
- **States**: `DEMAND → SELECTION → HEARING → AWARD → ENFORCEMENT`

### dispute_resolution
- **ID**: `dispute_resolution`
- **Owner**: CCO
- **Documents**: [DOC:F1]
- **Description**: General dispute resolution
- **Trigger**: Dispute raised
- **States**: `RAISED → NEGOTIATION → MEDIATION_IF_NEEDED → ARBITRATION_IF_NEEDED → RESOLVED`

### disclosure
- **ID**: `disclosure`
- **Owner**: CCO
- **Documents**: [DOC:F2]
- **Description**: Required disclosure process
- **Trigger**: Disclosure requirement
- **States**: `IDENTIFIED → DRAFTED → REVIEWED → DELIVERED → DOCUMENTED`

### efta_disclosure
- **ID**: `efta_disclosure`
- **Owner**: CCO
- **Documents**: [DOC:F2]
- **Description**: Electronic Fund Transfer Act (EFTA) disclosure process for end customers
- **Trigger**: Customer onboarding, service terms update
- **States**: `DRAFTED → COMPLIANCE_REVIEW → APPROVED → DELIVERED → ACKNOWLEDGED`

---

## Annual Compliance Flows

### annual_compliance
- **ID**: `annual_compliance`
- **Owner**: CCO
- **Documents**: [DOC:E1]
- **Description**: Annual compliance calendar execution
- **Trigger**: Calendar year
- **States**: `SCHEDULED → IN_PROGRESS → COMPLETE → DOCUMENTED`

### compliance_records
- **ID**: `compliance_records`
- **Owner**: CCO
- **Documents**: [DOC:B4]
- **Description**: Compliance record maintenance
- **Trigger**: Continuous
- **States**: `CREATED → STORED → ACCESSIBLE → RETENTION_REVIEWED`

### compliance_controls
- **ID**: `compliance_controls`
- **Owner**: CCO
- **Documents**: [DOC:B5]
- **Description**: Compliance control environment
- **Trigger**: Continuous
- **States**: `DESIGNED → IMPLEMENTED → TESTED → OPERATING → REVIEWED`

---

## Validation

All `[FLOW:*]` markers in documents must reference a flow ID defined above.

```yaml
rule: FLOW-REGISTRY-001
description: All FLOW markers must reference defined flows
check: "[FLOW:X]" → X exists in flows/index.md
severity: ERROR

rule: FLOW-CASE-001  
description: FLOW IDs should use snake_case
check: "[FLOW:X]" → X matches /^[a-z][a-z0-9_]*$/
severity: WARNING
action: Normalize to snake_case
```
