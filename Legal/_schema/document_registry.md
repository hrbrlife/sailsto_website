# Document Registry

> **Purpose**: Master index of all documents with metadata.
> Used by README.md for document discovery and output mapping.
> 
> **Note**: Source paths depend on layout state (FLAT vs MIGRATED).
> See `structure.md` for path resolution logic.

---

## Source Path Resolution

```yaml
# FLAT layout (pre-migration): all files in root
flat_pattern: "./{DocCode}_*.md"

# MIGRATED layout (post-migration): organized by series/purpose  
migrated_pattern: "./{SeriesType}/{PurposeType}/{DocCode}_*.md"

# Detection: check for Company/ directory
layout: "MIGRATED" if exists("Company/") else "FLAT"
```

---

## Output Directory Mapping

```yaml
output_structure:
  Formation:
    pattern: "A*.md|D*.md"
    documents: [A1, A2, A3, D1]
  Governance:
    pattern: "B*.md"
    documents: [B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12]
  Client:
    pattern: "F*.md|C*.md"
    documents: [F1, F2, C1, C2, C3]
  Checklists:
    pattern: "E*.md"
    documents: [E1, E2]
  Schedules:
    pattern: "N*.md"
    documents: [N1, N3, N4, N5]
  Overview:
    pattern: "00_*.md"
    documents: [00_README, 00_Business_Model]

# Knowledge sources (not audited documents, but used as reference)
knowledge_sources:
  knowledge_base:
    path: "_schema/knowledge_base/"
    weight: 1.0
    description: "Primary regulatory sources - statutes, CFR, official guidance"
  research_outputs:
    path: "_schema/research_outputs/"
    weight: 0.5
    description: "Secondary LLM research - requires cross-reference validation"
    documents: [RO-001, RO-002, RO-003, RO-004, RO-005, RO-006]
```

---

## Document Template Mapping

```yaml
template_assignments:
  BaseDocument: "*"  # All documents
  FormationDocument: [A1, A2, A3, D1, C1, C2]
  GovernanceDocument: [B1, B2, B3, B10]
  ComplianceDocument: [B4, B5, B6, B7, B8, B9, B12]
  ClientAgreement: [F1, F2, B11, N1]
  ScheduleDocument: [C3, E1, E2, N1, N3, N4, N5]
  ABNDocument: [C1, C2]
```

---

## Registry Format

| DocCode | Title | Category | Filed With | Current Version | Last Updated | Dependencies |
|---------|-------|----------|------------|-----------------|--------------|--------------|

---

## Formation Documents (A-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `A1` | Articles of Organization | FORMATION | Montana SOS | 1.0 | 2025-01 | - |
| `A2` | Exhibit A - Series List | FORMATION | Montana SOS | 1.1 | 2025-12 | A1 |
| `A3` | Exhibit B - Series Operating Agreements | FORMATION | Montana SOS | 1.1 | 2025-12 | A1, A2 |

## Governance Documents (B-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `B1` | Master Operating Agreement | GOVERNANCE | Internal | 1.4 | 2025-12 | A1 |
| `B2` | Officer Appointment Resolution | GOVERNANCE | Internal | 1.0 | 2025-01 | B1 |
| `B3` | Officer Rotation Succession Policy | GOVERNANCE | Internal | 1.2 | 2025-12 | B1, B2 |
| `B4` | Record-Keeping Policy | COMPLIANCE | Internal | 1.3 | 2025-12 | B1 |
| `B5` | BSA/AML Program | COMPLIANCE | Internal | 1.1 | 2025-12 | B1 |
| `B6` | IT Security, Incident, BCP/DRP | COMPLIANCE | Internal | 1.4 | 2025-12 | B1 |
| `B7` | Acceptable Client Use Policy | COMPLIANCE | Internal | 1.4 | 2025-12 | B1, N3, N4 |
| `B8` | Privacy Data Protection Policy | COMPLIANCE | Internal | 1.0 | 2025-01 | B1 |
| `B9` | Fit and Proper Screening Policy | COMPLIANCE | Internal | 1.1 | 2025-12 | B1, B2 |
| `B10` | Insurance and Capital Policy | GOVERNANCE | Internal | 1.1 | 2025-12 | B1 |
| `B11` | Client Services and Licensing Framework | CLIENT | Internal | 1.8 | 2025-12 | B1, F1 |
| `B12` | Partner Due Diligence Standard | COMPLIANCE | Internal | 1.1 | 2025-12 | B1, B4, N1 |

## ABN/Registration Documents (C-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `C1` | ABN Registration - CCASH | FORMATION | Montana SOS | 1.1 | 2025-12 | A1 |
| `C2` | ABN Template - Client Series | FORMATION | Montana SOS | 1.1 | 2025-12 | A1, D1 |
| `C3` | Pricing and Routing Schedule | CLIENT | Internal | 1.1 | 2025-12 | F1, N3 |

## Amendment Documents (D-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `D1` | Articles of Amendment - Add Series | FORMATION | Montana SOS | 1.1 | 2025-12 | A1, A2 |

## Checklist Documents (E-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `E1` | Filing Checklist and Instructions | CHECKLIST | Internal | 1.1 | 2025-12 | A1-D1 |
| `E2` | Securities and MTL Checklist | CHECKLIST | Internal | 1.1 | 2025-12 | E1 |

## Client Agreement Documents (F-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `F1` | Client Services Agreement | CLIENT | Client | 1.7 | 2025-12 | B1, B11, C3 |
| `F2` | End Customer Terms Template | CLIENT | Client | 1.8 | 2025-12 | F1 |

## Schedule Documents (N-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `N1` | Partner MSB Agreement | SCHEDULE | Partner | 1.4 | 2025-12 | N3, N4, B4, B5, B8, B12, C3 |
| `N3` | Approved States Schedule | SCHEDULE | Internal | 1.4 | 2025-12 | B7, N4 |
| `N4` | Partner MSB Directory | SCHEDULE | Internal | 1.3 | 2025-12 | N3, N1, B12, C3 |
| `N5` | Client FinCEN Filing Guide | SCHEDULE | Internal | 1.1 | 2025-12 | E1 |

## Overview Documents (00-Series)

| DocCode | Title | Category | Filed With | Version | Updated | Dependencies |
|---------|-------|----------|------------|---------|---------|--------------|
| `00_README` | Package Overview | OVERVIEW | Internal | 1.0 | 2025-01 | - |
| `00_Business_Model` | Business Model Description | OVERVIEW | Internal | 1.1 | 2025-12 | - |

---

## Dependency Graph

```
                    ┌─────────────────────────────────────────────────────┐
                    │                    A1 (Articles)                     │
                    └─────────────────────┬───────────────────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────────┐
              │                           │                               │
              ▼                           ▼                               ▼
        ┌─────────┐                 ┌─────────┐                     ┌─────────┐
        │   A2    │                 │   A3    │                     │   B1    │
        │ Series  │                 │ Series  │                     │ Master  │
        │  List   │                 │  OAs    │                     │   OA    │
        └────┬────┘                 └─────────┘                     └────┬────┘
             │                                                           │
             │                    ┌──────────────────────────────────────┤
             ▼                    │                                      │
        ┌─────────┐          ┌────┴────┐  ┌─────────┐  ┌─────────┐  ┌────┴────┐
        │   D1    │          │   B2    │  │   B3    │  │  B4-B6  │  │   B7    │
        │Amendment│          │Officers │  │Succession│ │Compliance│ │  AUP    │
        └────┬────┘          └─────────┘  └─────────┘  └─────────┘  └────┬────┘
             │                                                           │
             ▼                                                           ▼
        ┌─────────┐                                                 ┌─────────┐
        │   C2    │                                                 │   N3    │
        │Client ABN│                                                │ States  │
        └─────────┘                                                 └─────────┘
                                                                         │
        ┌─────────┐          ┌─────────┐                                 │
        │   B11   │◄─────────│   F1    │◄────────────────────────────────┘
        │Framework│          │  CSA    │
        └─────────┘          └────┬────┘
                                  │
                                  ▼
                             ┌─────────┐          ┌─────────┐
                             │   F2    │          │   C3    │
                             │End Terms│          │ Pricing │
                             └─────────┘          └─────────┘
```

---

## Change Impact Matrix

When a document changes, these documents may need review:

| If Changed | Review These |
|------------|--------------|
| A1 | A2, A3, B1, C1, D1, E1 |
| A2 | A3, D1, E1 |
| B1 | B2-B11, F1 |
| B3 | B2, B5, B9 |
| B7 | N3, F1, F2 |
| B9 | B2, B3 |
| C3 | F1, N3 |
| E1 | E2, N5 |
| F1 | F2, B11, C3 |
| N3 | B7, C3 |

---

## Generated Output Files

Documents generated by validation execution (not source documents):

```yaml
generated_outputs:
  Reports:
    path: "./OUTPUT/"
    files:
      - VALIDATION_REPORT.md    # Main execution report
    
  Registers:
    path: "./OUTPUT/Registers/"
    files:
      - OBLIGATIONS.md          # Extracted from obligations.md
      - PROCESSES.md            # Extracted from flows/*.md
      - DECISIONS.md            # Extracted from decisions_rights.md
      - RIGHTS.md               # Extracted from decisions_rights.md
    
  Matrices:
    path: "./OUTPUT/Matrices/"
    files:
      - DECISION_MATRIX.md      # Role × Decision cross-tab
      - RIGHTS_MATRIX.md        # Entity × Right cross-tab
      - RACI_MATRIX.md          # Process × Role RACI
```

---

## Version History Format

Each document should maintain a version history:

```markdown
## Version History

| Version | Date | Author | Changes | Breaking? |
|---------|------|--------|---------|-----------|
| 1.1 | 2025-12-14 | [Author] | Updated MSB model language | Yes |
| 1.0 | 2025-01-01 | [Author] | Initial version | - |
```

**Breaking Change**: Any change that:
- Modifies a defined term
- Changes an obligation (who/what/when)
- Alters a process flow
- Affects cross-referenced sections
