# Defined Terms Registry

> **Purpose**: Single source of truth for all defined terms used across CCASH documents.
> Terms here function like TypeScript interfaces - any usage must conform to these definitions.

---

## Statistics

| Category | Count | Status |
|----------|-------|--------|
| Entity Terms | 32 | Defined |
| Regulatory Terms | 28 | Defined |
| Officer Terms | 7 | Defined |
| Transaction Terms | 18 | Defined |
| Compliance Terms | 22 | Defined |
| Document Terms | 8 | Defined |
| **Total** | **115** | ✓ Complete |

---

## Entity Types

### Company

| Property | Type | Value/Constraint | Authoritative Source |
|----------|------|------------------|---------------------|
| legalName | string | `CCASH MONEY SERVICES (US) SERIES LLC` | A1 §1.1 |
| entityType | enum | `Series LLC` | A1 §1.2 |
| jurisdiction | enum | `Montana` | A1 §1.3 |
| statute | citation | `MCA § 35-8-304` | A1 §1.2 |
| role | enum | `Infrastructure Provider` | 00_Business_Model §1.1 |

**Aliases**: `[TERM:Company]`, `[TERM:CompanyLegalName]`

### ClientSeries

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| seriesCode | string | `/^C-\d{3}$/` | A2 §1.6 |
| legalName | template | `CCASH MONEY SERVICES (US) SERIES LLC – {ClientName} Operations Series` | A2 §1.6 |
| hasEIN | boolean | `REQUIRED = true` | E1 §6.1.4 |
| hasFinCEN | boolean | `REQUIRED = true` | E1 §6.1.5 |
| msbType | enum | `Independent Montana MSB` | 00_Business_Model §2.3.4 |
| parentEntity | ref | `→ Company` | A1 §2.3 |

**Aliases**: `[TERM:ClientSeries]`, `[TERM:Client Series]`

### FunctionalSeries

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| seriesCode | string | `/^[TPBS]-\d+$/` | A2 §1.3-1.5 |
| legalName | template | `CCASH MONEY SERVICES (US) SERIES LLC – {Purpose} Series` | A2 §2.x |
| prefix | enum | `T` (Treasury), `P` (Platform), `B` (Brand), `S` (Securities) | A2 §1.3-1.5 |

**Aliases**: `[TERM:FunctionalSeries]`, `[TERM:Functional Series]`

**Specific Series Terms**:
- `[TERM:Series_T1]` — Treasury Operations Series
- `[TERM:Series_T2]` — Float Management Series
- `[TERM:Series_T3]` — Correspondent Banking Series
- `[TERM:Series_T4]` — Exchange Settlement Series
- `[TERM:Series_P1]` — Core Platform Series
- `[TERM:Series_P2]` — API Platform Series
- `[TERM:Series_P3]` — White Label Platform Series
- `[TERM:Series_B1]` — CCASH Brand Series
- `[TERM:Series_B2]` — Client Brand Series
- `[TERM:Series_S1]` — Securities Series

### Series

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| type | enum | `ClientSeries` \| `FunctionalSeries` | A2; B1 §1.12 |
| legalName | template | `CCASH MONEY SERVICES (US) SERIES LLC – {Name} Series` | A2 |
| separateRecords | boolean | `true` — MCA § 35-8-304(4) | A1 §2.2 |

**Description**: A protected cell within the Montana Series LLC structure, with liability separation per MCA § 35-8-304. The term "Series" includes both Functional Series (T-1 through T-4, B-1, B-2, P-1 through P-3, S-1) and Client Series (C-001 through C-999).

**Aliases**: `[TERM:Series]`

**See Also**: `[TERM:ClientSeries]`, `[TERM:FunctionalSeries]`

**Note**: B1 §1.12-1.14 (v1.2) explicitly defines "Series" broadly to include all series types, and separately defines "Client Series" and "Functional Series" as subtypes.

### SeriesLLC

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| type | enum | `Montana Series LLC` | A1 §1.2 |
| statute | citation | `MCA § 35-8-304` | A1 §1.2 |
| liabilityShield | boolean | `true` — inter-series liability separation | A1 §2.3 |

**Aliases**: `[TERM:SeriesLLC]`, `[TERM:Series LLC]`, `[TERM:MontanaSeriesLLC]`

### EndCustomer

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| relationship | enum | `Customer of ClientSeries` | F2 §1.1 |
| kycRequired | boolean | `true` | B5 §3.2, F2 §3.1 |
| thirdPartyBeneficiary | boolean | `false` (no direct rights vs Company) | F1 §12.5, F2 §5.4 |

**Aliases**: `[TERM:EndCustomer]`, `[TERM:End Customer]`

### Member

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| type | enum | `Manager \| Member` | B1 §2.1 |
| votingRights | boolean | varies by class | B1 §3.2 |

**Aliases**: `[TERM:Member]`

### Manager

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Manager of the LLC` | B1 §3.1 |
| authority | enum | `Manages Company affairs` | B1 §3.4 |
| appointmentAuth | boolean | `Can appoint Officers` | B2 §1.2 |

**Aliases**: `[TERM:Manager]`

### Organizer

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Initial organizer of the LLC` | A1 §4.1 |

**Aliases**: `[TERM:Organizer]`

### RegisteredAgent

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Agent for service of process` | A1 §1.5 |
| jurisdiction | enum | `Montana` | A1 §1.5 |

**Aliases**: `[TERM:RegisteredAgent]`

### PartnerMSB

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Licensed MSB for interstate routing` | N3 §4.1 |
| relationship | enum | `Contracted through Company` | N3 §4.2.3 |
| coverage | ref | `→ StateAuthorization[]` | N3 §4.3 |

**Aliases**: `[TERM:PartnerMSB]`

### PartnerMSBDisruption

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| eventType | enum | `license_loss \| insolvency \| enforcement \| termination \| outage` | N3 §7.2 |
| impact | string | `routing interruption for Covered States` | N3 §7 |
| response | string | `suspend routing and notify clients` | N3 §7.3 |

**Aliases**: `[TERM:PartnerMSBDisruption]`

### AuthorizedDelegate

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| definition | string | `Person authorized to engage in money transmission on behalf of a licensee` | State MTL laws |
| scope | enum | `State-specific designation` | N1 §3.5 |
| filingRequired | boolean | `Varies by state` | N1 §3.5(d) |

**Description**: Under state money transmitter laws, an authorized delegate (also called an agent or authorized agent in some states) is a person or entity authorized to engage in money transmission activities on behalf of a licensed money transmitter. Partner MSBs may qualify as authorized delegates when processing Routed Transactions for the Company or its Client Series.

**Aliases**: `[TERM:AuthorizedDelegate]`

**See Also**: `[TERM:PartnerMSB]`

### TravelRule

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| threshold | currency | `$3,000` | 31 CFR §1010.410(f) |
| originatorInfo | string[] | `name, address, account/identifier` | 31 CFR §1010.410(f) |
| beneficiaryInfo | string[] | `name, account/identifier` | 31 CFR §1010.410(f) |
| requirement | string | `Transmit to next institution in chain` | 31 CFR §1010.410(f) |

**Description**: BSA requirement that financial institutions transmit certain originator and beneficiary information along with funds transfers of $3,000 or more. Partner MSBs must be capable of receiving and transmitting this information for Routed Transactions per N1 §4.7.

**Aliases**: `[TERM:TravelRule]`

**See Also**: `[TERM:BSA/AML]`, `[TERM:PartnerMSB]`

### BankabilityRequirement

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| purpose | string | `Requirements to maintain banking relationships` | B12 §2.2 |
| components | enum[] | `TravelRule \| SanctionsScreening \| BankCooperation` | N1 §4.7-4.9 |
| verification | string | `Confirm partner CAN and WILL comply` | B12 §2.2 |

**Description**: Minimum compliance capabilities that Partner MSBs must demonstrate to support the Company's banking relationships. Unlike prescriptive compliance requirements (which we don't impose), bankability requirements are things our bank actually needs us to verify about partners. Defined in B12 §2.2 and enforced via N1 Art 4.7-4.9.

**Aliases**: `[TERM:BankabilityRequirement]`, `[TERM:Bankability]`

**See Also**: `[TERM:TravelRule]`, `[TERM:PartnerMSB]`, `[TERM:BankingPartner]`

### BankingPartner

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Banking relationship for fiat operations` | B10 §3.2 |
| types | enum[] | `CorrespondentBank \| IntermediaryBank` | B1 §5.3 |

**Aliases**: `[TERM:BankingPartner]`

**Related**: `[TERM:CorrespondentBank]`, `[TERM:IntermediaryBank]`

### PaymentProcessor

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Third-party payment processing` | C3 §4.6 |

**Aliases**: `[TERM:PaymentProcessor]`

### Auditor

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Independent audit function` | B10 §4.1 |
| independence | boolean | `true` | B10 §4.2 |

**Aliases**: `[TERM:Auditor]`

---

## Regulatory Types

### MSBRegistration (MSB)

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| registrant | ref | `→ ClientSeries \| Company` | E1 §5.1.2 |
| registrationNumber | string | FinCEN-issued | E1 §6.1.5 |
| renewalPeriod | duration | `2 years` (biennial) | E1 §7.2.1 |
| reportingThreshold | duration | `180 days` for changes | E1 §7.2.3 |

**Aliases**: `[TERM:MSB]`, `[TERM:MSBRegistration]`

### FinCEN

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Financial Crimes Enforcement Network` | B5 §1.2 |
| authority | string | `Federal MSB registration authority` | N5 §1.2 |

**Aliases**: `[TERM:FinCEN]`

### BSA

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Bank Secrecy Act` | B5 §1.1 |
| regulations | citation | `31 CFR Chapter X` | B5 §1.2 |

**Aliases**: `[TERM:BSA]`, `[TERM:BSA/AML]`, `[TERM:BSA_AML]`, `[TERM:BSA_AML_Program]`, `[TERM:BSA_AML_Officer]`

### OFAC

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Office of Foreign Assets Control` | B5 §4.1 |
| function | string | `Sanctions enforcement` | B5 §4.2 |

**Aliases**: `[TERM:OFAC]`

### MTL

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Money Transmitter License` | E2 §1.1 |
| stateRequired | boolean | `varies by state` | N3 §4-5 |

**Aliases**: `[TERM:MTL]`

### StateAuthorization

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| state | enum | US state/territory code | N3 §6 |
| status | enum | `APPROVED \| PARTNER_MSB \| PROHIBITED \| PENDING` | N3 §6 |
| basis | string | Legal citation or Partner MSB reference | N3 §6 |
| transactionTypes | enum[] | `FIAT \| CRYPTO \| BOTH` | N3 §3-4 |

**State-specific terms**:
- `[TERM:MontanaState]`, `[TERM:Montana]` — Home jurisdiction
- `[TERM:Wyoming]` — Crypto-exempt state (W.S. § 40-22-104)
- `[TERM:ProhibitedState]` — States where operations are prohibited

### MCA

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Montana Code Annotated` | A1 §1.2 |
| seriesStatute | citation | `MCA § 35-8-304` | A1 §1.2 |

**Aliases**: `[TERM:MCA]`, `[TERM:MCA 35-8-304]`

### SecretaryOfState

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | string | `Montana SOS for business filings` | A1 §1.4, E1 §1.1 |

**Aliases**: `[TERM:SecretaryOfState]`

### EIN

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Employer Identification Number` | N5 §2.1 |
| issuer | string | `IRS` | N5 §2.1.2 |
| perSeries | boolean | `true` — each series needs own EIN | N5 §2.1.4 |

**Aliases**: `[TERM:EIN]`

### DBA

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Doing Business As / Assumed Business Name` | C1 §1.1 |
| registration | string | `Montana SOS` | C2 §2.1 |

**Aliases**: `[TERM:DBA]`

### VASP

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Virtual Asset Service Provider` | B5 §1.3 |
| relevance | string | `FATF designation for crypto services` | B5 §1.3 |

**Aliases**: `[TERM:VASP]`

### VirtualCurrency

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| definition | string | `Digital representation of value` | N3 §3.1 |
| exemptions | ref | `Wyoming W.S. § 40-22-104` | N3 §3.1.1 |

**Aliases**: `[TERM:VirtualCurrency]`

### Securities Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:RegulationD]` | SEC Reg D exemption for private placements | E2 §2.1 |
| `[TERM:RegulationA]` | SEC Reg A exemption for smaller offerings | E2 §2.2 |
| `[TERM:RegulationS]` | SEC Reg S exemption for offshore offerings | E2 §2.3 |
| `[TERM:FormD]` | SEC filing for Reg D offerings | E2 §2.1.3 |
| `[TERM:PPM]` | Private Placement Memorandum | E2 §3.1 |
| `[TERM:SubscriptionAgreement]` | Investor subscription document | E2 §3.2 |
| `[TERM:InvestorSuitability]` | Accredited investor verification | E2 §4.1 |

---

## Officer Types

### Officer

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| role | enum | See `OfficerRole` below | B2 §2.1 |
| appointedBy | ref | `→ Manager` | B2 §1.2 |
| term | duration | `1 year` (renewable) | B2 §3.1 |
| screeningRequired | boolean | `true` | B9 §2.1 |

**Aliases**: `[TERM:Officer]`, `[TERM:Officers]`, `[TERM:ControlPerson]`

### OfficerRole (enum)

| Value | BSAOfficer? | Qualifications | Authoritative Source |
|-------|-------------|----------------|---------------------|
| `CEO` | No | B9 §2.2 | B2 §2.1.1 |
| `CCO` | Yes (default) | CAMS + 3yr experience | B9 §2.5, B3 §6.5 |
| `CFO` | No | B9 §2.2 | B2 §2.1.3 |
| `CTO` | No | B9 §2.2 | B2 §2.1.4 |
| `CMO` | No | B9 §2.2 | B2 §2.1.5 |
| `GC` | Backup BSA | B9 §2.2 | B2 §2.1.6 |

**Individual Officer Terms**:
- `[TERM:CEO]` — Chief Executive Officer
- `[TERM:CCO]` — Chief Compliance Officer (also BSA Officer)
- `[TERM:CFO]` — Chief Financial Officer
- `[TERM:CTO]` — Chief Technology Officer
- `[TERM:CMO]` — Chief Marketing Officer

---

## Transaction Types

### Transaction

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| riskLevel | enum | `LOW \| MEDIUM \| HIGH` | C3 §4.3-4.5 |
| routingMethod | enum | `DIRECT \| PARTNER_MSB \| CRYPTO_EXEMPT` | N3 §2-4, B7 §9.8 |
| originState | ref | `→ StateAuthorization` | B7 §9.11 |
| destinationState | ref | `→ StateAuthorization` | B7 §9.11 |

**Risk Level Terms**:
- `[TERM:LowRiskTransaction]` — Standard transaction, minimal review
- `[TERM:MediumRiskTransaction]` — Enhanced review required
- `[TERM:HighRiskTransaction]` — EDD and approval required

### FeeStructure

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| feeType | enum | `ONBOARDING \| TRAINING \| PLATFORM \| TRANSACTION \| IT_LICENSE \| PARTNER_MSB` | C3 §2-5, §4.7 |
| calculationMethod | enum | `FLAT \| PERCENTAGE \| COST_PLUS` | C3 §4.1 |
| volumeTiers | boolean | `true` for transaction fees | C3 §4.2 |

**Fee Type Terms**:
- `[TERM:OnboardingFee]` — Initial setup fee | C3 §2.1
- `[TERM:TrainingFee]` — Compliance training fee | C3 §2.2
- `[TERM:PlatformFee]` — Monthly platform access | C3 §3.1
- `[TERM:TransactionFee]` — Per-transaction fee | C3 §4.1
- `[TERM:ITLicenseFee]` — Software license fee | C3 §3.3
- `[TERM:DirectCosts]` — Pass-through costs | C3 §1.2

### Services

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| definition | string | `Platform and compliance infrastructure` | F1 §1.3 |
| includes | enum[] | `Platform, ComplianceServices, FiatGateway` | F1 §2.1 |

**Service Terms**:
- `[TERM:Services]` — Aggregate services provided
- `[TERM:Platform]` — Technology platform access
- `[TERM:ComplianceServices]` — BSA/AML support services
- `[TERM:FiatGateway]`, `[TERM:Fiat Gateway]` — Fiat on/off ramp services
- `[TERM:DigitalAssetCustody]` — Crypto custody services
- `[TERM:ForeignExchange]` — FX services
- `[TERM:API]` — Application Programming Interface access

### Payment Rail Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:ACH]` | Automated Clearing House | B1 §5.3 |
| `[TERM:SWIFT]` | International wire transfers | B1 §5.3 |
| `[TERM:XRPL]` | XRP Ledger for crypto settlement | B1 §5.3 |

---

## Compliance Types

### Obligation

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| obligor | ref | `→ ClientSeries \| Company \| Officer` | varies |
| obligee | ref | `→ Regulator \| Company \| ClientSeries` | varies |
| frequency | enum | `ONE_TIME \| ANNUAL \| BIENNIAL \| ON_CHANGE \| CONTINUOUS` | varies |
| deadline | duration or date | specific or relative | varies |

### ComplianceEvent

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| eventType | enum | `SAR \| CTR \| REGISTRATION \| RENEWAL \| REPORT` | B5 §3-6 |
| filingDeadline | duration | varies by type | B5 §3.4, §4.2 |
| retentionPeriod | duration | `5 years` minimum | B4 §2.1 |

### KYC/AML Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:KYC]` | Know Your Customer | B5 §3.1 |
| `[TERM:KYB]` | Know Your Business | B5 §3.1 |
| `[TERM:CIP]` | Customer Identification Program | B5 §3.2 |
| `[TERM:CDD]` | Customer Due Diligence | B5 §3.3 |
| `[TERM:EDD]` | Enhanced Due Diligence | B5 §3.4 |
| `[TERM:BeneficialOwnership]` | 25%+ owner identification | B5 §3.5 |
| `[TERM:PEP]` | Politically Exposed Person | B5 §4.3 |

### Reporting Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:SAR]` | Suspicious Activity Report | B5 §5.1 |
| `[TERM:TransactionMonitoring]` | Ongoing transaction surveillance | B5 §5.2 |
| `[TERM:Sanctions]`, `[TERM:SanctionsScreening]` | OFAC sanctions compliance | B5 §4.1 |
| `[TERM:RiskAssessment]` | Enterprise risk evaluation | B5 §2.1 |
| `[TERM:RiskClassification]` | Customer risk tiering | B5 §3.6 |
| `[TERM:RegulatoryReporting]` | Required regulatory filings | B5 §6.1 |
| `[TERM:AnnualReport]` | Annual compliance report | B4 §3.1 |
| `[TERM:CallReport]` | Periodic financial report | B10 §5.1 |

### Training and Policies

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:ComplianceTraining]` | Required BSA/AML training | B5 §7.1 |
| `[TERM:CompliancePolicy]` | Written compliance procedures | B5 §1.4 |
| `[TERM:ComplianceReview]` | Periodic compliance audit | B5 §8.1 |
| `[TERM:ApprovedJurisdictions]` | States where operations permitted | N3 §2-4 |

### IT and Security Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:BCP]` | Business Continuity Plan | B6 §2.1 |
| `[TERM:IncidentResponse]` | Security incident procedures | B6 §3.1 |
| `[TERM:PII]` | Personally Identifiable Information | B8 §1.3 |
| `[TERM:SLA]` | Service Level Agreement | F1 §6.1 |

### Insurance and Capital Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:SuretyBond]` | Required surety bond | B10 §2.1 |

### Client Operational Controls Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:ClientInsurance]` | Client Series insurance requirements | B11 §14A |
| `[TERM:AgentProhibition]` | Prohibition on agent/sub-representative networks | B11 §14B |
| `[TERM:MarketingCompliance]` | Marketing and advertising compliance standards | B11 §14C |

---

## Document Types

### Document

| Property | Type | Constraint | Example |
|----------|------|------------|---------|
| docCode | string | `/^[A-Z]\d+$/` or `/^\d{2}_/` | `B7`, `00_Business_Model` |
| category | enum | `FORMATION \| GOVERNANCE \| COMPLIANCE \| CLIENT \| CHECKLIST \| SCHEDULE` | - |
| filedWith | enum | `SOS \| INTERNAL \| CLIENT \| REGULATOR` | A1→SOS, B1→INTERNAL |
| version | semver | `MAJOR.MINOR` | `1.0` |

### Legal Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:Arbitration]` | Binding arbitration for disputes | F1 §13.1, F2 §8.1 |
| `[TERM:AAA]` | American Arbitration Association | F1 §13.2 |
| `[TERM:ClassActionWaiver]` | Waiver of class action rights | F1 §13.5, F2 §8.3 |
| `[TERM:JuryTrialWaiver]` | Waiver of jury trial | F1 §13.6 |
| `[TERM:ThirdPartyBeneficiary]` | Third party rights (or lack thereof) | F1 §12.5, F2 §5.4 |
| `[TERM:MaterialBreach]` | Breach triggering termination | F1 §11.2 |
| `[TERM:ForceMajeure]` | Force majeure provisions | F1 §12.8 |
| `[TERM:ConfidentialityAgreement]` | NDA/confidentiality terms | F1 §9.1 |
| `[TERM:LiabilitySeparation]` | Series liability shield | A1 §2.3, B1 §2.4 |

### Agreement Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:ClientServicesAgreement]` | F1 document | F1 §1.1 |
| `[TERM:Master_Operating_Agreement]` | B1 document | B1 §1.1 |
| `[TERM:ChangeOfControl]` | Contract-defined change in control of a Client Series | F1 §14.4 |

### AI/Technology Terms

| Term | Definition | Authoritative Source |
|------|------------|---------------------|
| `[TERM:AISystem]` | AI-assisted operations disclosure | F2 §6.1, 00_Business_Model §12 |

---

## Validation Rules

```yaml
# These rules can be checked programmatically

rules:
  - name: client_series_must_have_ein
    type: required_property
    on: ClientSeries
    property: hasEIN
    value: true
    
  - name: fincen_renewal_biennial
    type: duration_match
    on: MSBRegistration.renewalPeriod
    expected: "2 years"
    
  - name: cco_is_bsa_officer
    type: role_assignment
    condition: "OfficerRole == CCO"
    implies: "BSAOfficer == true"
    
  - name: interstate_requires_partner
    type: conditional_routing
    condition: "originState != destinationState AND originState != 'MT'"
    requires: "routingMethod == PARTNER_MSB OR routingMethod == CRYPTO_EXEMPT"
```

---

## Consumer Protection Terms

### ErrorResolution

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| statute | citation | `15 U.S.C. § 1693f` | EFTA |
| regulation | citation | `12 CFR § 1005.11` | Regulation E |
| reportingWindow | duration | `60 days from statement` | F2 §6A.1 |
| investigationPeriod | duration | `10 business days, extendable to 45 days` | F2 §6A.1 |

**Description**: Procedures for investigating and resolving errors in electronic fund transfers as required by the Electronic Fund Transfer Act and Regulation E.

**Aliases**: `[TERM:ErrorResolution]`

### PreauthorizedPayment

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| stopPaymentNotice | duration | `3 business days before scheduled transfer` | F2 §6A.4(a) |
| varyingAmountNotice | duration | `10 days before payment` | F2 §6A.4(b) |
| regulation | citation | `12 CFR § 1005.10` | Regulation E |

**Aliases**: `[TERM:PreauthorizedPayment]`

### DepositInsurance

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fdicCoverage | boolean | `false` for MSB accounts | F2 §6A.6 |
| sipcCoverage | boolean | `false` for MSB accounts | F2 §6A.6 |
| disclosureRequired | boolean | `true` | F2 §6A.6 |

**Description**: Disclosure that customer funds held by MSBs are generally not covered by FDIC or SIPC insurance, though funds may be held at partner banks with pass-through coverage.

**Aliases**: `[TERM:DepositInsurance]`

### UnclaimedProperty

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| dormancyPeriod | duration | `3-5 years (state-dependent)` | F2 §6B.1 |
| escheatmentRequired | boolean | `true` | F2 §6B.2 |
| noticeRequired | boolean | `true before escheatment` | F2 §6B.1 |

**Description**: State unclaimed property laws require reporting and remitting dormant account balances to state authorities after specified dormancy periods.

**Aliases**: `[TERM:UnclaimedProperty]`

### EFTA

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| fullName | string | `Electronic Fund Transfer Act` | 15 U.S.C. § 1693 |
| implementingRegulation | citation | `Regulation E (12 CFR Part 1005)` | F2 §6A |
| applicability | string | `Consumer electronic fund transfers` | F2 §6A |

**Aliases**: `[TERM:EFTA]`, `[TERM:RegulationE]`

### AccountTermination

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| initiator | enum | `EndCustomer \| ClientSeries` | F2 §6C |
| withdrawalTiming | string | `subject to compliance holds` | F2 §6C.3 |
| refundTiming | duration | `within 5 business days where required` | F2 §6C.3 |

**Aliases**: `[TERM:AccountTermination]`

### TransactionReceipt

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| required | boolean | `true` | F2 §6D.1 |
| contents | string | `amount, fees, recipient, date/time, status` | F2 §6D.1 |

**Aliases**: `[TERM:TransactionReceipt]`

### PeriodicStatement

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| frequency | enum | `MONTHLY \| QUARTERLY \| ON_REQUEST` | F2 §6D.2 |
| delivery | enum | `ELECTRONIC \| PAPER` | F2 §6D.2 |

**Aliases**: `[TERM:PeriodicStatement]`

### Eligibility

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| minimumAge | integer | `>= 18` | F2 §6E.1 |

**Aliases**: `[TERM:Eligibility]`

### Residency

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| allowed | string | `U.S. residents only (unless approved)` | F2 §6E.2 |

**Aliases**: `[TERM:Residency]`

### ProhibitedJurisdiction

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| includes | string | `sanctioned jurisdictions and prohibited states` | B7 §9; F2 §6E.3 |

**Aliases**: `[TERM:ProhibitedJurisdiction]`

### UserRepresentations

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| accuracy | boolean | `true and complete information` | F2 §6F |
| lawfulUse | boolean | `must use lawfully` | F2 §6F |

**Aliases**: `[TERM:UserRepresentations]`

### ComplaintEscalation

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| internalProcess | boolean | `required` | F2 §6G |
| escalationRight | boolean | `end-customer may complain to regulators` | F2 §6G.3 |

**Aliases**: `[TERM:ComplaintEscalation]`

### RegulatoryComplaint

| Property | Type | Constraint | Authoritative Source |
|----------|------|------------|---------------------|
| channels | string | `state regulators and CFPB (as applicable)` | F2 §6G.3 |

**Aliases**: `[TERM:RegulatoryComplaint]`

---

## Usage in Documents

When referencing defined terms in documents, use this pattern:

```markdown
The **Client Series** [TERM:ClientSeries] must maintain its own 
**FinCEN registration** [TERM:MSBRegistration] per [DOC:E1§6.1.5].
```

This enables:
1. Automated term consistency checking
2. Hover definitions in tooling
3. Impact analysis when definitions change
