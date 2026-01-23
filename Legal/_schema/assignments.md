# Role Assignments Registry

> **Purpose**: Maps entities → roles → persons.
> This is the "who holds what role where" record.

---

## Assignment Summary

### Company Role Distribution

```
CCASH MONEY SERVICES (US) SERIES LLC
├── Manager:          Marcus W. Chen (P001)
├── Member:           Marcus W. Chen (P001) - 100%
├── CEO:              Marcus W. Chen (P001)
├── CTO:              David J. Park (P003)
├── CFO:              Elena M. Rodriguez (P004)
├── CCO:              Sarah A. Okonkwo (P002)
├── BSA Officer:      Sarah A. Okonkwo (P002)
├── Registered Agent: Northwest Registered Agent LLC (RA001)
└── Organizer:        Marcus W. Chen (P001) [Formation complete]
```

### Series Role Distribution

```
All Protected Series (P-1, T-1, T-2, T-4):
├── Manager:          [Inherited from Company → P001]
└── Registered Agent: [Shared with Company → RA001]

Client Series (C-###):
├── Manager:          [Client-provided]
├── BSA Officer:      [Client-provided - REQUIRED]
└── Registered Agent: [May share with Company]
```

---

## Company Assignments

### Entity: CCASH MONEY SERVICES (US) SERIES LLC

```yaml
entity_id: company
entity_name: "CCASH MONEY SERVICES (US) SERIES LLC"
entity_type: company
formation_date: "2025-01-01"
mt_entity_id: "[To be assigned upon filing]"
```

#### ASN-001: Manager

```yaml
assignment_id: ASN-001
entity_id: company
role_id: manager
role_title: "Manager"
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
termination_date: null
status: active
notes: "Initial and sole Manager"
```

#### ASN-002: Member

```yaml
assignment_id: ASN-002
entity_id: company
role_id: member
role_title: "Member"
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
termination_date: null
status: active
ownership_percentage: 100
capital_contribution: "$[________________]"
notes: "Initial and sole Member"
```

#### ASN-003: CEO

```yaml
assignment_id: ASN-003
entity_id: company
role_id: ceo
role_title: "Chief Executive Officer"
role_abbreviation: "CEO"
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
termination_date: null
status: active
reports_to: manager
compensation:
  base_salary: "$[________________]"
  structure: "Per B2 Officer Appointment Resolution"
notes: "Founder serves as CEO; same person as Manager"
```

#### ASN-004: CTO

```yaml
assignment_id: ASN-004
entity_id: company
role_id: cto
role_title: "Chief Technology Officer"
role_abbreviation: "CTO"
person_id: P003
person_name: "David J. Park"
effective_date: "2025-01-01"
termination_date: null
status: active
reports_to: ceo
compensation:
  base_salary: "$[________________]"
  structure: "Per B2 Officer Appointment Resolution"
notes: "Co-founder; leads technology and platform development"
```

#### ASN-005: CFO

```yaml
assignment_id: ASN-005
entity_id: company
role_id: cfo
role_title: "Chief Financial Officer"
role_abbreviation: "CFO"
person_id: P004
person_name: "Elena M. Rodriguez, CPA"
effective_date: "2025-01-01"
termination_date: null
status: active
reports_to: ceo
compensation:
  base_salary: "$[________________]"
  structure: "Per B2 Officer Appointment Resolution"
notes: "Financial management and treasury"
```

#### ASN-006: CCO

```yaml
assignment_id: ASN-006
entity_id: company
role_id: cco
role_title: "Chief Compliance Officer"
role_abbreviation: "CCO"
person_id: P002
person_name: "Sarah A. Okonkwo"
effective_date: "2025-01-01"
termination_date: null
status: active
reports_to: manager  # Direct to Manager for independence
also_serves_as:
  - bsa_officer
compensation:
  base_salary: "$[________________]"
  structure: "Per B2 Officer Appointment Resolution"
independence_confirmed: true
notes: "Independent CCO; also serves as BSA/AML Officer. Reports directly to Manager."
```

#### ASN-007: BSA Officer

```yaml
assignment_id: ASN-007
entity_id: company
role_id: bsa_officer
role_title: "BSA/AML Officer"
person_id: P002
person_name: "Sarah A. Okonkwo"
effective_date: "2025-01-01"
termination_date: null
status: active
fincen_designated: true
linked_to: ASN-006  # Same person as CCO
notes: "FinCEN-designated BSA Officer; also serves as CCO"
```

#### ASN-008: Registered Agent

```yaml
assignment_id: ASN-008
entity_id: company
role_id: registered_agent
role_title: "Registered Agent"
person_id: RA001
person_name: "Northwest Registered Agent LLC"
effective_date: "2025-01-01"
termination_date: null
status: active
agent_type: commercial
montana_address: "1900 Prospect Avenue, Helena, MT 59601"
notes: "Commercial RA; serves Company and all Series"
```

#### ASN-009: CMO

```yaml
assignment_id: ASN-009
entity_id: company
role_id: cmo
role_title: "Chief Marketing Officer"
role_abbreviation: "CMO"
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
termination_date: null
status: active
reports_to: ceo
compensation:
  base_salary: "$[________________]"
  structure: "Per B2 Officer Appointment Resolution"
notes: "Founder handles marketing/BD during early stage; may be delegated later"
```

#### ASN-010: Organizer (Formation Complete)

```yaml
assignment_id: ASN-010
entity_id: company
role_id: organizer
role_title: "Organizer"
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
termination_date: "2025-01-01"
status: completed
lifecycle: formation_only
notes: "Organizer role completed upon filing Articles of Organization"
```

---

## Protected Series Assignments

### Series P-1 (Compliance & Operations)

```yaml
entity_id: P-1
entity_name: "Series P-1"
entity_type: protected_series
subtype: operations
purpose: "Compliance, onboarding, and customer support functions"
```

#### ASN-P1-001: Manager (Inherited)

```yaml
assignment_id: ASN-P1-001
entity_id: P-1
role_id: manager
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
status: active
inherited_from: ASN-001
notes: "Inherits Manager from Company"
```

#### ASN-P1-002: Registered Agent (Shared)

```yaml
assignment_id: ASN-P1-002
entity_id: P-1
role_id: registered_agent
person_id: RA001
person_name: "Northwest Registered Agent LLC"
effective_date: "2025-01-01"
status: active
shared_with: [company, T-1, T-2, T-4]
notes: "Shares Registered Agent with Company"
```

---

### Series T-1 (Payment Rails)

```yaml
entity_id: T-1
entity_name: "Series T-1"
entity_type: protected_series
subtype: infrastructure
purpose: "Payment rails and money transmission infrastructure"
```

#### ASN-T1-001: Manager (Inherited)

```yaml
assignment_id: ASN-T1-001
entity_id: T-1
role_id: manager
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
status: active
inherited_from: ASN-001
```

#### ASN-T1-002: Registered Agent (Shared)

```yaml
assignment_id: ASN-T1-002
entity_id: T-1
role_id: registered_agent
person_id: RA001
person_name: "Northwest Registered Agent LLC"
effective_date: "2025-01-01"
status: active
shared_with: [company, P-1, T-2, T-4]
```

---

### Series T-2 (Custody)

```yaml
entity_id: T-2
entity_name: "Series T-2"
entity_type: protected_series
subtype: infrastructure
purpose: "Custody and asset safekeeping"
```

#### ASN-T2-001: Manager (Inherited)

```yaml
assignment_id: ASN-T2-001
entity_id: T-2
role_id: manager
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
status: active
inherited_from: ASN-001
```

#### ASN-T2-002: Registered Agent (Shared)

```yaml
assignment_id: ASN-T2-002
entity_id: T-2
role_id: registered_agent
person_id: RA001
person_name: "Northwest Registered Agent LLC"
effective_date: "2025-01-01"
status: active
shared_with: [company, P-1, T-1, T-4]
```

---

### Series T-4 (Technology)

```yaml
entity_id: T-4
entity_name: "Series T-4"
entity_type: protected_series
subtype: infrastructure
purpose: "Technology platform and software"
```

#### ASN-T4-001: Manager (Inherited)

```yaml
assignment_id: ASN-T4-001
entity_id: T-4
role_id: manager
person_id: P001
person_name: "Marcus W. Chen"
effective_date: "2025-01-01"
status: active
inherited_from: ASN-001
```

#### ASN-T4-002: Registered Agent (Shared)

```yaml
assignment_id: ASN-T4-002
entity_id: T-4
role_id: registered_agent
person_id: RA001
person_name: "Northwest Registered Agent LLC"
effective_date: "2025-01-01"
status: active
shared_with: [company, P-1, T-1, T-2]
```

---

## Client Series Template

### Series C-001 (Example - To Be Completed Per Client)

```yaml
entity_id: C-001
entity_name: "Series C-001"
entity_type: client_series
client_legal_name: "[________________]"
client_dba: "[________________]"
client_ein: "[________________]"
client_fincen_msb: "[________________]"
```

#### ASN-C001-001: Manager

```yaml
assignment_id: ASN-C001-001
entity_id: C-001
role_id: manager
person_id: CLIENT-C001-001  # Client provides
person_name: "[________________]"
effective_date: "[________________]"
status: pending
source: client
notes: "Client-designated Manager"
```

#### ASN-C001-002: BSA Officer

```yaml
assignment_id: ASN-C001-002
entity_id: C-001
role_id: bsa_officer
person_id: CLIENT-C001-002  # Client provides (may be same as Manager)
person_name: "[________________]"
effective_date: "[________________]"
status: pending
source: client
fincen_designated: true
critical: true
notes: "CRITICAL: Client must designate own BSA Officer for their FinCEN registration"
```

#### ASN-C001-003: Registered Agent (Shared Option)

```yaml
assignment_id: ASN-C001-003
entity_id: C-001
role_id: registered_agent
person_id: RA001  # Can share Company's RA
person_name: "Northwest Registered Agent LLC"
effective_date: "[________________]"
status: pending
shared_with: company
notes: "Using Company's Registered Agent (common arrangement)"
```

---

## Role Assignment Matrix

| Entity | Manager | Member | CEO | CTO | CFO | CCO | BSA | RA |
|--------|---------|--------|-----|-----|-----|-----|-----|-----|
| **Company** | P001 | P001 (100%) | P001 | P003 | P004 | P002 | P002 | RA001 |
| **P-1** | P001↑ | — | — | — | — | — | — | RA001↔ |
| **T-1** | P001↑ | — | — | — | — | — | — | RA001↔ |
| **T-2** | P001↑ | — | — | — | — | — | — | RA001↔ |
| **T-4** | P001↑ | — | — | — | — | — | — | RA001↔ |
| **C-###** | CLIENT | — | — | — | — | — | CLIENT | RA001↔ |

Legend: `↑` = Inherited from Company | `↔` = Shared with Company | `—` = Not applicable

---

## Person Role Summary

| Person | Roles Held |
|--------|-----------|
| **P001** (Marcus Chen) | Manager, Member, CEO, Organizer (completed) |
| **P002** (Sarah Okonkwo) | CCO, BSA Officer |
| **P003** (David Park) | CTO |
| **P004** (Elena Rodriguez) | CFO |
| **RA001** (Northwest RA) | Registered Agent (all entities) |

---

## Compliance Verification

### Independence Check

| Check | Status | Notes |
|-------|--------|-------|
| CCO ≠ CEO | ✓ Pass | P002 ≠ P001 |
| CCO ≠ CFO | ✓ Pass | P002 ≠ P004 |
| BSA Officer ≠ CEO | ✓ Pass | P002 ≠ P001 |
| BSA Officer ≠ CFO | ✓ Pass | P002 ≠ P004 |

### Required Role Check

| Entity | Manager | Member | RA | BSA (if FinCEN) |
|--------|---------|--------|-----|-----------------|
| Company | ✓ P001 | ✓ P001 | ✓ RA001 | ✓ P002 |
| P-1 | ✓ P001 | — | ✓ RA001 | — |
| T-1 | ✓ P001 | — | ✓ RA001 | — |
| T-2 | ✓ P001 | — | ✓ RA001 | — |
| T-4 | ✓ P001 | — | ✓ RA001 | — |

---

## Change History

| Date | Assignment | Change | Author |
|------|------------|--------|--------|
| 2025-01-01 | ASN-001 through ASN-009 | Initial company assignments | Formation |
| 2025-01-01 | ASN-P1-*, ASN-T*-* | Initial series assignments | Formation |
| 2025-12-15 | — | Populated with mock data | Schema System |
