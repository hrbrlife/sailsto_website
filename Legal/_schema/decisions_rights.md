# Decision & Rights Matrix

> **Purpose**: Define who can make what decisions and who has what rights.
> Generated outputs include decision authority table and rights allocation.

---

## Statistics

| Category | Defined | Used (unique) | Marker Uses | Status |
|----------|---------|---------------|-------------|--------|
| Decision IDs | 5 | 4 | 5 | Defined |
| Right IDs | 5 | 4 | 4 | Defined |
| **Total** | **10** | **8** | **9** | ✓ Complete |

> **Note**: Used DECISION IDs: `STRATEGIC-001`, `CLIENT-EXPANSION-001`, `CLIENT-TERMS-001`, `COMPLIANCE-001`
> Used RIGHT IDs: `AUDIT-001`, `FEE-MODIFY-001`, `INSPECT-001`, `TERMINATE-001`

---

## Decision ID Registry

All `[DECISION:*]` markers must reference one of these IDs:

| ID | Description | Authority | Source |
|----|-------------|-----------|--------|
| `STRATEGIC-001` | Major business decisions (markets, services, partnerships) | Manager (SOLE) | B1 §3.4 |
| `COMPLIANCE-001` | SAR filing and client restrictions | CCO (SOLE) | B5 §3.4, B7 §2.6 |
| `COMPLIANCE-002` | Standard client approvals meeting criteria | CCO (SOLE) | F1 Art.3 |
| `CLIENT-TERMS-001` | Client service terms and pricing | CEO + CFO (JOINT) | C3 §7.2, F1 Art.4 |
| `CLIENT-EXPANSION-001` | Client geographic expansion approval | CCO (SOLE) | N3 §4.2, B7 §9 |

---

## Right ID Registry

All `[RIGHT:*]` markers must reference one of these IDs:

| ID | Holder | Right | Conditions | Source |
|----|--------|-------|------------|--------|
| `ACCESS-001` | Company | Access Client transaction/customer data | For compliance purposes | F1 Art.5 |
| `AUDIT-001` | Company | Audit Client Series compliance records | With reasonable notice | F1 Art.5, C3 §5 |
| `INSPECT-001` | Company | Inspect Client operations | With notice | F1 Art.5 |
| `TERMINATE-001` | Company/Client | Terminate relationship | Per F1 Art.12 terms | F1 Art.12 |
| `FEE-MODIFY-001` | Company | Modify fee schedules | 60-day notice required | C3 §7.2 |

---

## Decision Categories

```yaml
decision_categories:
  - STRATEGIC      # Business direction, new markets, major investments
  - OPERATIONAL    # Day-to-day operations, routing, pricing
  - COMPLIANCE     # Regulatory decisions, SAR filing, client restrictions
  - FINANCIAL      # Budgets, fees, capital allocation
  - PERSONNEL      # Hiring, firing, appointments
  - CLIENT         # Onboarding, suspension, termination
  - TECHNICAL      # Systems, security, integrations
  - LEGAL          # Contracts, disputes, litigation
```

### Authority Levels

```yaml
authority_levels:
  SOLE:        "Can decide alone"
  JOINT:       "Requires multiple parties"
  CONSULT:     "Must consult but decides alone"
  RECOMMEND:   "Can recommend, another decides"
  INFORM:      "Must be informed of decision"
  NONE:        "No authority"
```

---

## Decision Matrix by Role

| Decision Type | Manager | CEO | CCO | CFO | CTO | GC | Client |
|---------------|---------|-----|-----|-----|-----|-----|--------|
| **STRATEGIC** |
| Enter new state market | SOLE | RECOMMEND | CONSULT | CONSULT | INFORM | CONSULT | NONE |
| Add new service type | SOLE | RECOMMEND | CONSULT | CONSULT | CONSULT | CONSULT | NONE |
| Partner MSB selection | SOLE | RECOMMEND | JOINT | INFORM | INFORM | CONSULT | NONE |
| **OPERATIONAL** |
| Transaction routing | NONE | INFORM | CONSULT | NONE | SOLE | NONE | NONE |
| Fee adjustments (≤10%) | NONE | SOLE | INFORM | CONSULT | NONE | NONE | INFORM |
| Fee adjustments (>10%) | SOLE | RECOMMEND | INFORM | CONSULT | NONE | CONSULT | INFORM |
| **COMPLIANCE** |
| File SAR | NONE | INFORM | SOLE | NONE | NONE | INFORM | NONE |
| Client restriction | NONE | INFORM | SOLE | NONE | NONE | INFORM | INFORM |
| AML policy change | SOLE | CONSULT | RECOMMEND | NONE | NONE | CONSULT | NONE |
| BSA Officer appointment | SOLE | CONSULT | N/A | NONE | NONE | CONSULT | NONE |
| **FINANCIAL** |
| Operating budget | SOLE | RECOMMEND | INFORM | JOINT | INFORM | NONE | NONE |
| Client credit terms | NONE | JOINT | CONSULT | SOLE | NONE | NONE | NONE |
| Capital call | SOLE | RECOMMEND | NONE | RECOMMEND | NONE | CONSULT | NONE |
| **PERSONNEL** |
| Hire Officer | SOLE | RECOMMEND | INFORM | INFORM | INFORM | CONSULT | NONE |
| Remove Officer | SOLE | RECOMMEND | INFORM | INFORM | INFORM | CONSULT | NONE |
| Interim BSA designation | SOLE | NONE | N/A | NONE | NONE | NONE | NONE |
| **CLIENT** |
| Approve new client | NONE | CONSULT | SOLE | NONE | INFORM | NONE | N/A |
| Suspend client | NONE | INFORM | SOLE | INFORM | INFORM | INFORM | INFORM |
| Terminate client | SOLE | RECOMMEND | RECOMMEND | INFORM | INFORM | CONSULT | INFORM |
| **TECHNICAL** |
| System architecture | NONE | INFORM | INFORM | NONE | SOLE | NONE | NONE |
| Security incident response | NONE | INFORM | CONSULT | NONE | SOLE | INFORM | INFORM |
| API access grant | NONE | NONE | CONSULT | NONE | SOLE | NONE | REQUEST |
| **LEGAL** |
| Execute CSA | SOLE | SOLE | NONE | NONE | NONE | CONSULT | JOINT |
| Litigation decision | SOLE | INFORM | INFORM | INFORM | NONE | RECOMMEND | INFORM |
| Regulatory response | SOLE | INFORM | RECOMMEND | NONE | NONE | JOINT | NONE |

---

## Decision Sources

| Decision | Authoritative Document | Section |
|----------|----------------------|---------|
| SAR filing | B5 | §3.4 |
| Client restriction | B7 | §2.6 |
| BSA Officer appointment | B3 | §6.5, §6.6 |
| Fee adjustments | C3 | §7.2 |
| Client termination | F1 | Art.12 |
| Officer removal | B2 | §4.1 |
| Interim BSA | B3 | §6.6.2 |

---

## Rights Matrix

### Rights Categories

```yaml
rights_categories:
  - ACCESS        # Can access information/systems
  - USE           # Can use assets/services
  - MODIFY        # Can change/update
  - DELEGATE      # Can assign to others
  - TRANSFER      # Can transfer to third party
  - TERMINATE     # Can end/revoke
  - BENEFIT       # Receives economic benefit
```

---

## Rights by Entity

### Company Rights (over Client Series)

| Right | Scope | Conditions | Source |
|-------|-------|------------|--------|
| ACCESS | Client transaction data | For compliance | F1 Art.5 |
| ACCESS | Client customer data | For AML/KYC | F1 Art.5, B5 |
| MODIFY | Client series operating agreement | With notice | A3 §13 |
| TERMINATE | Client relationship | Per F1 terms | F1 Art.12 |
| BENEFIT | Platform fees | Monthly | C3 §3 |
| BENEFIT | Transaction fees | Per transaction | C3 §4 |

### Client Series Rights (over Company)

| Right | Scope | Conditions | Source |
|-------|-------|------------|--------|
| USE | Platform infrastructure | While active | F1 Art.2 |
| USE | Compliance services | While active | B11 §4 |
| USE | Brand (if licensed) | Per B11 | B11 §5 |
| ACCESS | Transaction records | Own data only | F1 Art.5 |
| TERMINATE | Relationship | 30 days notice | F1 Art.12 |
| BENEFIT | SLA credits | On breach | F1 Art.9 |

### Client Series Rights (over End Customers)

| Right | Scope | Conditions | Source |
|-------|-------|------------|--------|
| ACCESS | Customer identity data | For KYC | F2 §5 |
| ACCESS | Transaction data | For services | F2 §2 |
| TERMINATE | Customer relationship | Per F2 terms | F2 §8 |
| MODIFY | Terms of service | With notice | F2 §10 |

### End Customer Rights (over Client Series)

| Right | Scope | Conditions | Source |
|-------|-------|------------|--------|
| ACCESS | Own transaction history | On request | F2 §3 |
| ACCESS | Privacy policy | Published | F2 §5, B8 |
| TERMINATE | Account | On request | F2 §8 |
| BENEFIT | Liability cap protection | Per F2 | F2 §4.2 |
| BENEFIT | Dispute resolution | Per F2 | F2 §3 |

### Officer Rights (over Company)

| Right | Role | Scope | Source |
|-------|------|-------|--------|
| ACCESS | All Officers | Relevant records | B4 §3 |
| DELEGATE | CCO | Compliance tasks | B5 §2.1 |
| DELEGATE | CTO | Technical tasks | B6 §2 |
| BENEFIT | All Officers | Indemnification | B1 Art.8 |

---

## Rights Flow Diagram

```
                    MANAGER
                       │
                       │ DELEGATE (governance)
                       ▼
    ┌──────────────────┴──────────────────┐
    │              OFFICERS               │
    │  CEO  │  CCO  │  CFO  │  CTO  │  GC │
    └──────────────────┬──────────────────┘
                       │
                       │ PROVIDE (services)
                       ▼
              ┌────────────────┐
              │ CLIENT SERIES  │ ◄── Own MSB, own EIN, own FinCEN
              │    (C-XXX)     │
              └────────┬───────┘
                       │
                       │ PROVIDE (financial services)
                       ▼
              ┌────────────────┐
              │ END CUSTOMERS  │
              └────────────────┘
```

---

## Validation Rules for Decisions/Rights

```yaml
decision_rights_rules:
  - id: DR-001
    name: sole_authority_documented
    description: Every SOLE decision must cite source document
    check: ALL decisions WHERE authority == 'SOLE' HAVE source IS NOT NULL
    severity: ERROR
    
  - id: DR-002
    name: no_conflicting_authority
    description: Same decision cannot have two SOLE authorities
    check: ALL decisions HAVE at_most_one role WHERE authority == 'SOLE'
    severity: ERROR
    
  - id: DR-003
    name: rights_have_source
    description: Every right must cite authoritative document
    check: ALL rights HAVE source IS NOT NULL
    severity: ERROR
    
  - id: DR-004
    name: terminate_requires_process
    description: TERMINATE rights must reference a process/flow
    check: ALL rights WHERE type == 'TERMINATE' HAVE process_reference
    severity: WARNING
```

---

## Output Generation

When generating OUTPUT, create:

```
./OUTPUT/
  └── Matrices/
      ├── DECISION_MATRIX.md      ← Who decides what
      ├── RIGHTS_MATRIX.md        ← Who has what rights
      └── RACI_MATRIX.md          ← Combined RACI view
```

### RACI Format

| Decision/Process | Responsible | Accountable | Consulted | Informed |
|------------------|-------------|-------------|-----------|----------|
| Client Onboarding | CCO | Manager | GC, CFO | CEO, CTO |
| SAR Filing | CCO | CCO | GC | CEO |
| Fee Change | CEO | Manager | CFO, CCO | Client |
