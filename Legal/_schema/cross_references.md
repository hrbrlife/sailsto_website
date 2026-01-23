# Cross-Reference Index

> **Purpose**: Machine-readable index of all document-to-document references.
> Enables validation that referenced sections exist and impact analysis when documents change.
>
> **Note**: References use DocCode (e.g., "A1", "B5") not file paths.
> Actual paths resolved via `structure.md` based on layout state (FLAT vs MIGRATED).

---

## Reference Format

```yaml
source:
  doc: DOCUMENT_CODE
  section: SECTION_NUMBER (optional)
target:
  doc: DOCUMENT_CODE  
  section: SECTION_NUMBER (optional)
type: DEFINES | REFERENCES | INCORPORATES | SUPERSEDES | CONFLICTS_WITH
context: "Brief description of the reference"
```

---

## Formation Document References

### A1 → Others
```yaml
- source: {doc: A1, section: "13.1"}
  target: {doc: A2}
  type: INCORPORATES
  context: "A1 incorporates A2 as Exhibit A (Series List)"

- source: {doc: A1, section: "13.2"}
  target: {doc: A3}
  type: INCORPORATES
  context: "A1 incorporates A3 as Exhibit B (Series Operating Agreements)"
```

### A2 → Others
```yaml
- source: {doc: A2, section: "1.6"}
  target: {doc: D1}
  type: REFERENCES
  context: "Client series added via D1 amendment process"

- source: {doc: A2, section: "3.4"}
  target: {doc: E1, section: "6.1.5"}
  type: REFERENCES
  context: "Client FinCEN registration requirement"
```

### A3 → Others
```yaml
- source: {doc: A3, section: "13.3"}
  target: {doc: B1}
  type: REFERENCES
  context: "Company operational infrastructure defined in B1"

- source: {doc: A3, section: "13.9"}
  target: {doc: B7}
  type: REFERENCES
  context: "Client restrictions per AUP"
```

---

## Governance Document References

### B1 → Others
```yaml
- source: {doc: B1, section: "3.1"}
  target: {doc: A1}
  type: REFERENCES
  context: "Company formation documents"

- source: {doc: B1, section: "7.1"}
  target: {doc: B2}
  type: REFERENCES
  context: "Officer appointments per B2"
```

### B3 → Others
```yaml
- source: {doc: B3, section: "6.5"}
  target: {doc: B5}
  type: REFERENCES
  context: "BSA Officer role defined in B5"

- source: {doc: B3, section: "6.6"}
  target: {doc: B9, section: "2.5"}
  type: REFERENCES
  context: "CCO qualifications for BSA Officer"
```

### B5 → Others
```yaml
- source: {doc: B5, section: "2.1"}
  target: {doc: B3, section: "6.5"}
  type: REFERENCES
  context: "BSA Officer succession"

- source: {doc: B5, section: "3.4"}
  target: {doc: B4}
  type: REFERENCES
  context: "SAR record retention per B4"

- source: {doc: B5, section: "CCDD"}
  target: {doc: B6}
  type: REFERENCES
  context: "IT security controls for AML data protection"

- source: {doc: B5, section: "3.5"}
  target: {doc: F2}
  type: REFERENCES
  context: "End-Customer Terms for customer disclosures"
```

### B4 → Others
```yaml
- source: {doc: B4, section: "5.2"}
  target: {doc: B6}
  type: REFERENCES
  context: "IT security for record storage"

- source: {doc: B4, section: "7.1"}
  target: {doc: E2}
  type: REFERENCES
  context: "Securities and MTL record-keeping requirements"
```

### B8 → Others
```yaml
- source: {doc: B8, section: "3.2"}
  target: {doc: B6}
  type: REFERENCES
  context: "IT Security Policy for data protection"

- source: {doc: B8, section: "4.1"}
  target: {doc: F2}
  type: REFERENCES
  context: "End-Customer Terms for privacy disclosures"
```

### B6 → Others
```yaml
- source: {doc: B6, section: "7.1"}
  target: {doc: B10}
  type: REFERENCES
  context: "Insurance and Capital Policy for incident losses"
```

### B7 → Others
```yaml
- source: {doc: B7, section: "9.7"}
  target: {doc: N3}
  type: REFERENCES
  context: "Approved states list"

- source: {doc: B7, section: "9.8"}
  target: {doc: N3, section: "3"}
  type: REFERENCES
  context: "Wyoming crypto exemption"

- source: {doc: B7, section: "9.9"}
  target: {doc: C3, section: "4.7"}
  type: REFERENCES
  context: "Partner MSB fees"

- source: {doc: B7, section: "9.11"}
  target: {doc: N3, section: "6"}
  type: REFERENCES
  context: "State status table"

- source: {doc: B7, section: "3.2"}
  target: {doc: C1}
  type: REFERENCES
  context: "ABN Registration for trade name compliance"
```

### B9 → Others
```yaml
- source: {doc: B9, section: "2.5"}
  target: {doc: B3, section: "6.6"}
  type: REFERENCES
  context: "CCO/BSA qualifications apply to succession"

- source: {doc: B9, section: "2.1"}
  target: {doc: B2}
  type: REFERENCES
  context: "Officer appointments require screening"
```

### B12 → Others
```yaml
- source: {doc: B12, section: "2.1"}
  target: {doc: N1}
  type: REFERENCES
  context: "Partner verification checklist feeds Partner MSB Agreement"

- source: {doc: B12, section: "2.2"}
  target: {doc: N1, section: "4.7-4.9"}
  type: REFERENCES
  context: "Bankability verification (Travel Rule, OFAC, banking cooperation)"

- source: {doc: B12, section: "2.4"}
  target: {doc: B4}
  type: REFERENCES
  context: "Due diligence records retained per B4"

- source: {doc: B12, section: "3.1"}
  target: {doc: N1, section: "Art.4"}
  type: DEFINES
  context: "B12 defines short enforceable terms implemented in N1 Art 4"
```

### B11 → Others
```yaml
- source: {doc: B11, section: "7"}
  target: {doc: E1, section: "6.1"}
  type: REFERENCES
  context: "Client MSB registration process"

- source: {doc: B11, section: "7"}
  target: {doc: N5}
  type: REFERENCES
  context: "Client FinCEN Filing Guide"
```

---

## Client Document References

### F1 → Others
```yaml
- source: {doc: F1, section: "Recital A"}
  target: {doc: B1}
  type: REFERENCES
  context: "Company structure and infrastructure"

- source: {doc: F1, section: "6.2"}
  target: {doc: E1, section: "6.1.5"}
  type: REFERENCES
  context: "Client FinCEN registration requirement"

- source: {doc: F1, section: "Art.8"}
  target: {doc: C3}
  type: INCORPORATES
  context: "Pricing Schedule incorporated by reference"

- source: {doc: F1, section: "Art.10"}
  target: {doc: B7}
  type: INCORPORATES
  context: "AUP incorporated by reference"

- source: {doc: F1, section: "Art.10"}
  target: {doc: N3}
  type: INCORPORATES
  context: "Approved States Schedule incorporated by reference"

- source: {doc: F1, section: "Art.8"}
  target: {doc: F2}
  type: REFERENCES
  context: "End-Customer Terms Template required language"
```

### F2 → Others
```yaml
- source: {doc: F2, section: "1"}
  target: {doc: F1}
  type: REFERENCES
  context: "Client Services Agreement governs relationship"

- source: {doc: F2, section: "4.2"}
  target: {doc: F1}
  type: REFERENCES
  context: "Liability cap per F1 structure"
```

---

## Schedule Document References

### C3 → Others
```yaml
- source: {doc: C3, section: "1.1"}
  target: {doc: F1}
  type: REFERENCES
  context: "Attached to Client Services Agreement"

- source: {doc: C3, section: "4.7"}
  target: {doc: N3, section: "4"}
  type: REFERENCES
  context: "Partner MSB routing states"

- source: {doc: C3, section: "6.2"}
  target: {doc: N3}
  type: REFERENCES
  context: "Routing based on state authorization"
```

### E1 → Others
```yaml
- source: {doc: E1, section: "5.2"}
  target: {doc: N3}
  type: REFERENCES
  context: "Montana-only scope, Partner MSB for interstate"

- source: {doc: E1, section: "6.1.4"}
  target: {doc: N5, section: "2.1"}
  type: REFERENCES
  context: "EIN instructions in FinCEN Guide"

- source: {doc: E1, section: "6.1.5"}
  target: {doc: N5, section: "3"}
  type: REFERENCES
  context: "FinCEN registration process"

- source: {doc: E1, section: "6.1.7"}
  target: {doc: D1}
  type: REFERENCES
  context: "Amendment template for new series"

- source: {doc: E1, section: "6.1.9"}
  target: {doc: C2}
  type: REFERENCES
  context: "ABN template for client"

- source: {doc: E1, section: "6.1.12"}
  target: {doc: B11}
  type: REFERENCES
  context: "Client agreements framework"

- source: {doc: E1, section: "7.2.1"}
  target: {doc: N5, section: "5"}
  type: REFERENCES
  context: "FinCEN biennial renewal process"

- source: {doc: E1, section: "8.1"}
  target: {doc: E2}
  type: REFERENCES
  context: "Securities and MTL checklist for regulatory maintenance"
```

### E2 → Others
```yaml
- source: {doc: E2, section: "2.5"}
  target: {doc: E1, section: "6"}
  type: REFERENCES
  context: "FinCEN registration procedures"

- source: {doc: E2, section: "2.5"}
  target: {doc: E1, section: "7.2"}
  type: REFERENCES
  context: "FinCEN renewal requirements"
```

### N3 → Others
```yaml
- source: {doc: N3, section: "1.2"}
  target: {doc: F1}
  type: REFERENCES
  context: "Incorporated into Client Services Agreement"

- source: {doc: N3, section: "1.2"}
  target: {doc: B7}
  type: REFERENCES
  context: "Incorporated into AUP"

- source: {doc: N3, section: "4.1.3"}
  target: {doc: C3, section: "4.7"}
  type: REFERENCES
  context: "Partner MSB fees"

- source: {doc: N3, section: "4.2.2"}
  target: {doc: N4}
  type: REFERENCES
  context: "Approved Partner MSBs listed in Partner MSB Directory"

- source: {doc: N3, section: "4.3.3"}
  target: {doc: N4}
  type: REFERENCES
  context: "Partner MSB coverage confirmed in Schedule N4"

- source: {doc: N3, section: "6.0"}
  target: {doc: N4}
  type: REFERENCES
  context: "Status table references N4 for Partner MSB availability"

- source: {doc: N3, section: "8.5"}
  target: {doc: N5}
  type: REFERENCES
  context: "Client FinCEN Filing Guide"
```

### N4 → Others
```yaml
- source: {doc: N4, section: "1.1"}
  target: {doc: N3}
  type: REFERENCES
  context: "Partner MSBs support interstate activities per N3"

- source: {doc: N4, section: "2.1"}
  target: {doc: B12}
  type: REFERENCES
  context: "Partner MSB due diligence per Partner Due Diligence Standard"

- source: {doc: N4, section: "2A.1"}
  target: {doc: B12}
  type: REFERENCES
  context: "Due diligence and monitoring process"

- source: {doc: N4, section: "2A.2"}
  target: {doc: N1}
  type: REFERENCES
  context: "Partner obligations defined in Partner MSB Agreement"

- source: {doc: N4, section: "4.2"}
  target: {doc: N3, section: "2"}
  type: REFERENCES
  context: "Montana base operations"

- source: {doc: N4, section: "4.2"}
  target: {doc: N3, section: "3"}
  type: REFERENCES
  context: "Crypto-exempt states"

- source: {doc: N4, section: "4.2"}
  target: {doc: N3, section: "5"}
  type: REFERENCES
  context: "Prohibited states"

- source: {doc: N4, section: "5.2"}
  target: {doc: C3, section: "4.7"}
  type: REFERENCES
  context: "Partner MSB fee pass-through"

- source: {doc: N4, section: "5.3"}
  target: {doc: B8}
  type: REFERENCES
  context: "Privacy policy for data sharing"

- source: {doc: N4, section: "6.3"}
  target: {doc: F1}
  type: REFERENCES
  context: "Notice requirements per Client Services Agreement"
```

### N5 → Others
```yaml
- source: {doc: N5, section: "1.1"}
  target: {doc: E1, section: "6.1.4-6.1.6"}
  type: REFERENCES
  context: "Client registration steps in E1"

- source: {doc: N5, section: "5.3"}
  target: {doc: E1, section: "7.2"}
  type: REFERENCES
  context: "Renewal tracking per E1"
```

### N1 → Others
```yaml
- source: {doc: N1, section: "Recital E"}
  target: {doc: N4}
  type: REFERENCES
  context: "Partner MSB Directory lists approved partners"

- source: {doc: N1, section: "Recital E"}
  target: {doc: N3}
  type: REFERENCES
  context: "Approved States Schedule governs state coverage"

- source: {doc: N1, section: "Art.4"}
  target: {doc: B4}
  type: REFERENCES
  context: "Record-keeping per Record-Keeping Policy"

- source: {doc: N1, section: "Art.4"}
  target: {doc: B5}
  type: REFERENCES
  context: "BSA/AML Program compliance"

- source: {doc: N1, section: "Art.4"}
  target: {doc: B8}
  type: REFERENCES
  context: "Privacy Policy for data sharing"

- source: {doc: N1, section: "Art.4.6"}
  target: {doc: B12}
  type: REFERENCES
  context: "Partner Due Diligence Standard for verification process"

- source: {doc: N1, section: "Art.4.7"}
  target: {doc: B12, section: "2.2"}
  type: REFERENCES
  context: "Travel Rule compliance (bankability requirement)"

- source: {doc: N1, section: "Art.4.8"}
  target: {doc: B12, section: "2.2"}
  type: REFERENCES
  context: "Sanctions screening (bankability requirement)"

- source: {doc: N1, section: "Art.4.9"}
  target: {doc: B12, section: "2.2"}
  type: REFERENCES
  context: "Banking partner cooperation (bankability requirement)"

- source: {doc: N1, section: "Art.5"}
  target: {doc: C3}
  type: REFERENCES
  context: "Pricing and Routing Schedule for fee pass-through"

- source: {doc: N1, section: "Art.9"}
  target: {doc: N5}
  type: REFERENCES
  context: "Client Series FinCEN registration requirement"
```

### Others → N1
```yaml
- source: {doc: N4, section: "2.2"}
  target: {doc: N1}
  type: REFERENCES
  context: "Partner MSB contractual requirements via N1 template"
```

---

## Reference Graph (Adjacency List)

```yaml
# For programmatic graph analysis
graph:
  A1: [A2, A3]
  A2: [D1, E1]
  A3: [B1, B7]
  B1: [A1, B2]
  B2: [B1, B9]
  B3: [B5, B9]
  B4: [B6, E2]
  B5: [B3, B4, B6, F2]
  B6: [B10]
  B7: [N3, C3, C1]
  B8: [B6, F2]
  B9: [B2, B3]
  B11: [E1, N5]
  C3: [F1, N3]
  D1: [A1, A2]
  E1: [D1, C2, B11, N5, N3, E2]
  E2: [E1]
  F1: [B1, C3, B7, N3, B11, F2]
  F2: [F1]
  N1: [N3, N4, B4, B5, B8, B9, C3, N5]
  N3: [B7, C3, F1, N4, N5]
  N4: [N1, N3, B8, B9, C3, F1]
  N5: [E1]
```

---

## Validation Queries

### Find Broken References
```sql
SELECT source.doc, source.section, target.doc, target.section
FROM cross_references
WHERE target.doc NOT IN (SELECT docCode FROM document_registry)
   OR (target.section IS NOT NULL 
       AND target.section NOT IN (SELECT section FROM document_sections WHERE doc = target.doc))
```

### Impact Analysis: What references B7?
```sql
SELECT source.doc, source.section, context
FROM cross_references
WHERE target.doc = 'B7'
ORDER BY source.doc
```

Result:
| Source Doc | Section | Context |
|------------|---------|---------|
| A3 | 13.9 | Client restrictions per AUP |
| F1 | Art.10 | AUP incorporated by reference |
| N3 | 1.2 | Incorporated into AUP |

### Circular Reference Detection
```python
# Detect cycles in reference graph
def find_cycles(graph):
    # DFS-based cycle detection
    ...
```

---

## MVP Validation

```yaml
cross_ref_mvp_conditions:
  - id: XREF-001
    name: all_targets_exist
    description: All referenced documents must exist
    check: ALL target.doc IN document_registry
    severity: ERROR
    
  - id: XREF-002
    name: section_refs_valid
    description: Referenced sections must exist in target doc
    check: ALL target.section EXISTS IN target.doc
    severity: ERROR
    
  - id: XREF-003
    name: no_orphan_documents
    description: Every document should be referenced by at least one other
    check: ALL documents HAVE at_least_one incoming_reference
    condition: doc.category != 'OVERVIEW'
    severity: WARNING
    
  - id: XREF-004
    name: incorporation_bidirectional
    description: INCORPORATES references should be acknowledged in target
    check: FOR_EACH ref WHERE type == 'INCORPORATES'
           target ACKNOWLEDGES incorporation
    severity: WARNING
```
