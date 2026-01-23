# Document Templates & MVP Validation

> **Purpose**: Single source of truth for document templates and validation rules.
> The README.md references this file for all validation logic.

---

## Rule Index (Quick Reference)

### Severity Levels
| Level | Meaning | Blocks Output? |
|-------|---------|----------------|
| ERROR | Document invalid | YES |
| WARNING | Should fix | NO |
| INFO | Suggestion | NO |

### Rule Categories
| Prefix | Category | Applies To |
|--------|----------|------------|
| BASE-* | All documents | * |
| FORM-* | Formation docs | A*, D* |
| GOV-* | Governance docs | B1, B2, B3, B10 |
| COMP-* | Compliance docs | B4-B9 |
| CLIENT-* | Client agreements | F*, B11 |
| ABN-* | ABN documents | C1, C2 |
| SCHED-* | Schedules | E*, N*, C3 |
| FLOW-* | Process flows | flows/*.md |
| MSB-* | MSB model rules | See applies_to |

---

## Global Rules (Apply to Multiple Templates)

```yaml
rules:
  # MSB Model Rules - Critical for regulatory compliance
  - id: MSB-001
    name: no_white_label
    description: Prohibited "white-label" language
    check: content NOT CONTAINS "white-label" AND content NOT CONTAINS "white label"
    applies_to: [00_Business_Model, A2, A3, B1, B11, D1, F1, F2, C1, C2]
    severity: ERROR
    
  - id: MSB-002
    name: no_rent_a_license
    description: Prohibited "rent-a-license" language
    check: content NOT CONTAINS "rent-a-license" AND content NOT CONTAINS "rent a license"
    applies_to: [00_Business_Model, A2, A3, B1, B11, D1, F1, F2]
    severity: ERROR
    
  - id: MSB-003
    name: independent_msb_model
    description: Must state independent MSB model for client docs
    check: content CONTAINS "independent" AND content CONTAINS "MSB"
    applies_to: [00_Business_Model, A2, A3, B11, F1]
    severity: ERROR
    
  - id: MSB-004
    name: client_own_ein
    description: Client docs must mention own EIN
    check: content MATCHES /own EIN|its own.*EIN|Client Series.*EIN/i
    applies_to: [A2, B11, F1, E1, N5]
    severity: ERROR
    
  - id: MSB-005
    name: client_fincen_registration
    description: Client docs must require FinCEN registration
    check: content CONTAINS "FinCEN" AND content CONTAINS "registration"
    applies_to: [A2, B11, F1, E1, N5]
    severity: ERROR

  # FinCEN Rules
  - id: FINCEN-001
    name: biennial_not_annual
    description: FinCEN renewal is biennial, not annual
    check: content NOT MATCHES /FinCEN.*annual|annually.*FinCEN/i
    applies_to: [E1, E2, N5, B5]
    severity: ERROR
    
  - id: FINCEN-002
    name: biennial_stated
    description: Must state biennial/two-year renewal
    check: content MATCHES /biennial|every two years|2.year/i
    applies_to: [E1, E2, N5]
    severity: WARNING
```

---

## Template Philosophy

Like a TypeScript interface, each template defines:
1. **Required Sections** - Must exist (compile error if missing)
2. **Required Properties** - Metadata that must be present
3. **MVP Conditions** - Business logic that must be satisfied
4. **Optional Sections** - May exist, validated if present

---

## Base Template (All Documents)

Every document inherits from this base template:

```yaml
template: BaseDocument
version: 1.0

metadata:
  required:
    - docCode        # Unique identifier (e.g., "B7", "F1")
    - title          # Human-readable title
    - effectiveDate  # When document becomes effective
    - version        # Semantic version (MAJOR.MINOR)
    - category       # FORMATION | GOVERNANCE | COMPLIANCE | CLIENT | CHECKLIST | SCHEDULE
    - status         # DRAFT | REVIEW | APPROVED | SUPERSEDED
  optional:
    - supersedes     # Previous version reference
    - expiresDate    # If document has sunset clause
    - reviewDate     # Next scheduled review

sections:
  required:
    - HEADER         # Title, effective date, version
  optional:
    - VERSION_HISTORY
    - DEFINITIONS
    - REFERENCES

mvp_conditions:
  - id: BASE-001
    name: has_effective_date
    description: Document must have a valid effective date
    check: metadata.effectiveDate IS NOT NULL
    severity: ERROR
    
  - id: BASE-002
    name: has_version
    description: Document must be versioned
    check: metadata.version MATCHES /^\d+\.\d+$/
    severity: ERROR
    
  - id: BASE-003
    name: no_placeholder_brackets
    description: No unfilled [____] placeholders in approved documents
    check: content NOT MATCHES /\[_{2,}\]/
    condition: metadata.status == 'APPROVED'
    severity: ERROR
    
  - id: BASE-004
    name: cross_refs_valid
    description: All document cross-references must resolve
    check: ALL cross_references EXIST IN document_registry
    severity: ERROR
```

---

## Formation Document Template

```yaml
template: FormationDocument
extends: BaseDocument
version: 1.0
applies_to: [A1, A2, A3, D1]

metadata:
  required:
    - filedWith      # Montana SOS
    - filingFee      # Dollar amount
    - filingDate     # When filed (null if not yet filed)

sections:
  required:
    - ENTITY_IDENTIFICATION
    - PURPOSE
    - REGISTERED_AGENT
    - EXECUTION

mvp_conditions:
  - id: FORM-001
    name: valid_entity_name
    description: Entity name must match master record
    check: sections.ENTITY_IDENTIFICATION.legalName == "CCASH MONEY SERVICES (US) SERIES LLC"
    severity: ERROR
    
  - id: FORM-002
    name: montana_jurisdiction
    description: Must specify Montana jurisdiction
    check: sections.ENTITY_IDENTIFICATION.jurisdiction == "Montana"
    severity: ERROR
    
  - id: FORM-003
    name: has_registered_agent
    description: Must have registered agent in Montana
    check: sections.REGISTERED_AGENT IS NOT NULL
    severity: ERROR
    
  - id: FORM-004
    name: proper_execution
    description: Execution section must have signature blocks
    check: sections.EXECUTION HAS signature_block
    severity: ERROR
    
  - id: FORM-005
    name: series_statute_citation
    description: Must cite Montana Series LLC statute
    check: content CONTAINS "MCA § 35-8-304" OR content CONTAINS "35-8-304"
    severity: WARNING
```

---

## Governance Document Template

```yaml
template: GovernanceDocument
extends: BaseDocument
version: 1.0
applies_to: [B1, B2, B3, B10]

metadata:
  required:
    - approvedBy     # Manager | Members | Board
    - approvalDate   # When approved

sections:
  required:
    - PURPOSE
    - SCOPE
    - AUTHORITY      # Who has power to act
    - PROCEDURES     # How to exercise authority
  optional:
    - DELEGATION
    - AMENDMENTS

mvp_conditions:
  - id: GOV-001
    name: clear_authority_chain
    description: Must specify who can approve/act
    check: sections.AUTHORITY IS NOT NULL AND LENGTH > 50
    severity: ERROR
    
  - id: GOV-002
    name: amendment_process
    description: Must specify how document can be amended
    check: sections.AMENDMENTS IS NOT NULL OR content CONTAINS "amend"
    severity: WARNING
    
  - id: GOV-003
    name: consistent_with_master_oa
    description: Must not conflict with B1 Master Operating Agreement
    check: NO_CONFLICTS_WITH document_registry.B1
    severity: ERROR
    manual_review: true
```

---

## Compliance Document Template

```yaml
template: ComplianceDocument
extends: BaseDocument
version: 1.0
applies_to: [B4, B5, B6, B7, B8, B9]

metadata:
  required:
    - regulatoryBasis    # What regulation this implements
    - responsibleOfficer # CCO, CTO, etc.
    - reviewFrequency    # ANNUAL | BIENNIAL | ON_CHANGE

sections:
  required:
    - PURPOSE
    - SCOPE
    - REQUIREMENTS       # What must be done
    - RESPONSIBILITIES   # Who does it
    - MONITORING         # How compliance is verified
    - RECORDKEEPING      # What records to maintain
  optional:
    - TRAINING
    - EXCEPTIONS
    - ESCALATION

mvp_conditions:
  - id: COMP-001
    name: has_regulatory_basis
    description: Must cite regulatory authority
    check: metadata.regulatoryBasis IS NOT NULL
    severity: ERROR
    
  - id: COMP-002
    name: has_responsible_party
    description: Must assign responsibility to specific officer
    check: metadata.responsibleOfficer IN [CCO, CEO, CFO, CTO, GC]
    severity: ERROR
    
  - id: COMP-003
    name: has_monitoring_mechanism
    description: Must specify how compliance is monitored
    check: sections.MONITORING IS NOT NULL AND LENGTH > 100
    severity: ERROR
    
  - id: COMP-004
    name: has_recordkeeping
    description: Must specify record retention
    check: sections.RECORDKEEPING IS NOT NULL
    severity: ERROR
    
  - id: COMP-005
    name: retention_minimum_5_years
    description: BSA requires 5-year retention minimum
    check: sections.RECORDKEEPING CONTAINS "five years" OR "5 years"
    condition: metadata.regulatoryBasis CONTAINS "BSA"
    severity: ERROR
```

---

## Client Agreement Template

```yaml
template: ClientAgreement
extends: BaseDocument
version: 1.0
applies_to: [F1, F2, B11]

metadata:
  required:
    - parties            # Who is bound
    - governingLaw       # Montana
    - disputeResolution  # Arbitration | Litigation

sections:
  required:
    - RECITALS           # Background and intent
    - DEFINITIONS        # Defined terms
    - SERVICES           # What's being provided
    - FEES               # Compensation
    - TERM_TERMINATION   # Duration and exit
    - REPRESENTATIONS    # Warranties
    - LIMITATION_LIABILITY
    - GOVERNING_LAW
    - SIGNATURES
  optional:
    - INDEMNIFICATION
    - CONFIDENTIALITY
    - IP_RIGHTS
    - INSURANCE

mvp_conditions:
  - id: CLIENT-001
    name: msb_model_clarity
    description: Must clearly state independent MSB model
    check: content CONTAINS "independent" AND content CONTAINS "MSB" AND content CONTAINS "own EIN"
    severity: ERROR
    
  - id: CLIENT-002
    name: fincen_requirement
    description: Must require client FinCEN registration
    check: content CONTAINS "FinCEN" AND content CONTAINS "registration"
    severity: ERROR
    
  - id: CLIENT-003
    name: montana_governing_law
    description: Governing law must be Montana
    check: sections.GOVERNING_LAW CONTAINS "Montana"
    severity: ERROR
    
  - id: CLIENT-004
    name: arbitration_clause
    description: Must have arbitration or dispute resolution
    check: sections.GOVERNING_LAW CONTAINS "arbitration" OR content CONTAINS "dispute resolution"
    severity: WARNING
    
  - id: CLIENT-005
    name: liability_cap_present
    description: Must have limitation of liability
    check: sections.LIMITATION_LIABILITY IS NOT NULL
    severity: ERROR
    
  - id: CLIENT-006
    name: liability_cap_reasonable
    description: Liability cap should be at least $1,000
    check: sections.LIMITATION_LIABILITY EXTRACT_AMOUNT >= 1000
    severity: WARNING
    
  - id: CLIENT-007
    name: no_white_label_language
    description: Must not use "white-label" or "rent-a-license" language
    check: content NOT CONTAINS "white-label" AND content NOT CONTAINS "rent-a-license"
    severity: ERROR
```

---

## Schedule/Checklist Template

```yaml
template: ScheduleDocument
extends: BaseDocument
version: 1.0
applies_to: [C3, E1, E2, N3, N5]

metadata:
  required:
    - parentDocument     # What document this is a schedule to
    - updateFrequency    # How often updated

sections:
  required:
    - PURPOSE
    - CONTENT            # The actual schedule data
  optional:
    - INSTRUCTIONS
    - UPDATE_PROCESS

mvp_conditions:
  - id: SCHED-001
    name: has_parent_reference
    description: Must reference parent document
    check: metadata.parentDocument IS NOT NULL
    severity: ERROR
    
  - id: SCHED-002
    name: tables_complete
    description: All table cells must have values (no empty cells)
    check: ALL tables HAVE no_empty_required_cells
    severity: WARNING
    
  - id: SCHED-003
    name: consistent_with_parent
    description: Must not conflict with parent document
    check: NO_CONFLICTS_WITH metadata.parentDocument
    severity: ERROR
    manual_review: true
```

---

## ABN Template

```yaml
template: ABNDocument
extends: FormationDocument
version: 1.0
applies_to: [C1, C2]

sections:
  required:
    - ASSUMED_NAME
    - DESCRIPTION_OF_BUSINESS
    - APPLICANT_INFORMATION
    - EXECUTION

mvp_conditions:
  - id: ABN-001
    name: no_entity_designator
    description: ABN must not include LLC, Inc, etc.
    check: sections.ASSUMED_NAME NOT MATCHES /\b(LLC|Inc|Corp|Ltd)\b/i
    severity: ERROR
    
  - id: ABN-002
    name: independent_msb_language
    description: Must describe independent MSB model, not white-label
    check: sections.DESCRIPTION_OF_BUSINESS NOT CONTAINS "white-label"
    severity: ERROR
    
  - id: ABN-003
    name: client_series_has_ein_mention
    description: Client ABN must mention own EIN/FinCEN
    check: content CONTAINS "EIN" OR content CONTAINS "FinCEN"
    condition: docCode == "C2"
    severity: WARNING
```

---

## Process Flow Template

```yaml
template: ProcessFlow
extends: BaseDocument
version: 1.0
applies_to: [flows/*]

metadata:
  required:
    - flowName           # Unique identifier
    - trigger            # What starts the flow
    - owner              # Responsible officer
    - sla                # Time to complete

sections:
  required:
    - STATES             # All possible states
    - TRANSITIONS        # Valid state changes
    - RESPONSIBILITIES   # Who does what
    - TIMEOUTS           # Max time in each state
  optional:
    - EXCEPTIONS
    - ESCALATION

mvp_conditions:
  - id: FLOW-001
    name: has_start_state
    description: Must have exactly one START state
    check: sections.STATES HAS exactly_one WHERE name == "START"
    severity: ERROR
    
  - id: FLOW-002
    name: has_terminal_states
    description: Must have at least one terminal state
    check: sections.STATES HAS at_least_one WHERE terminal == true
    severity: ERROR
    
  - id: FLOW-003
    name: all_states_reachable
    description: All states must be reachable from START
    check: ALL sections.STATES ARE reachable_from "START"
    severity: ERROR
    
  - id: FLOW-004
    name: no_orphan_states
    description: All non-terminal states must have outbound transitions
    check: ALL sections.STATES WHERE terminal == false HAVE outbound_transition
    severity: ERROR
    
  - id: FLOW-005
    name: responsibilities_assigned
    description: Every transition must have responsible party
    check: ALL sections.TRANSITIONS HAVE responsible_party
    severity: ERROR
```

---

## Validation Severity Levels

| Severity | Meaning | Blocks Approval? |
|----------|---------|------------------|
| `ERROR` | Document is invalid | Yes |
| `WARNING` | Should be fixed, may be acceptable | No |
| `INFO` | Suggestion for improvement | No |

---

## Template Inheritance Diagram

```
                         ┌──────────────────┐
                         │   BaseDocument   │
                         │  (all documents) │
                         └────────┬─────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Formation     │    │   Governance    │    │   Compliance    │
│   Document      │    │   Document      │    │   Document      │
│  (A1,A2,A3,D1)  │    │  (B1,B2,B3,B10) │    │ (B4-B9)         │
└────────┬────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼                        
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ABNDocument   │    │ ClientAgreement │    │ScheduleDocument │
│    (C1, C2)     │    │   (F1,F2,B11)   │    │ (C3,E1,E2,N3,N5)│
└─────────────────┘    └─────────────────┘    └─────────────────┘

                       ┌─────────────────┐
                       │  ProcessFlow    │
                       │   (flows/*)     │
                       └─────────────────┘
```

---

## Example: Validating F1 (Client Services Agreement)

```yaml
# Validation Report for F1_Client_Services_Agreement.md

document: F1
template: ClientAgreement
validated: 2025-12-14T10:30:00Z

results:
  - id: BASE-001
    status: PASS
    
  - id: BASE-002
    status: PASS
    value: "1.1"
    
  - id: BASE-003
    status: PASS
    note: "No unfilled placeholders found"
    
  - id: CLIENT-001
    status: PASS
    evidence: "Line 45: 'independent Montana MSB with its own EIN'"
    
  - id: CLIENT-002
    status: PASS
    evidence: "Line 52: 'Client Series must maintain FinCEN registration'"
    
  - id: CLIENT-007
    status: PASS
    note: "No prohibited language found"

summary:
  errors: 0
  warnings: 0
  passed: 12
  status: VALID
```
