# Schema Markers

> **Purpose**: Defines inline markers for document annotation.
> Markers enable validation and cross-referencing but are stripped from OUTPUT.

---

## Implementation Statistics

<!-- schema:status Last-Updated: 2025-12-14 -->

| Marker Type | Count | Coverage |
|-------------|-------|----------|
| `[TERM:*]` | 2,260 | All 27 documents |
| `[DOC:*]` | 456 | Cross-references linked |
| `[OBL:*]` | 78 | Key obligations tagged |
| `[FLOW:*]` | 97 | Process flows identified |
| `[DECISION:*]` | 4 | Decision authorities linked |
| `[RIGHT:*]` | 4 | Rights allocations linked |
| **Total** | **2,899** | ✓ Complete |

### Registry Coverage

| Registry | Defined IDs | Used IDs (unique) | Marker Uses | Coverage |
|----------|-------------|-------------------|-------------|----------|
| `defined_terms.md` | 44 | 120 | 2,260 | Via aliases |
| `flows/index.md` | 78 | 83 | 97 | Via aliases |
| `obligations.md` | 48 | 38 | 78 | 100% |
| `decisions_rights.md` | 10 | 7 | 8 | 100% |

> **Note**: TERM and FLOW markers use aliases extensively. Registry IDs map to multiple
> document variations (e.g., `client_onboarding` ↔ `Client_Onboarding`).

### Validation Commands

```bash
# Count markers by type
grep -roh "\[TERM:" . --include="*.md" | grep -v "_schema" | wc -l
grep -roh "\[DOC:" . --include="*.md" | grep -v "_schema" | wc -l
grep -roh "\[OBL:" . --include="*.md" | grep -v "_schema" | wc -l
grep -roh "\[FLOW:" . --include="*.md" | grep -v "_schema" | wc -l
grep -roh "\[DECISION:" . --include="*.md" | grep -v "_schema" | wc -l
grep -roh "\[RIGHT:" . --include="*.md" | grep -v "_schema" | wc -l

# List unique IDs by type
grep -rho "\[TERM:[^]]*\]" . --include="*.md" | grep -v "_schema" | sort -u
grep -rho "\[OBL:[^]]*\]" . --include="*.md" | grep -v "_schema" | sort -u
grep -rho "\[FLOW:[^]]*\]" . --include="*.md" | grep -v "_schema" | sort -u

# Find documents without markers
find . -name "*.md" -not -path "./_schema/*" -not -path "./Audits/*" | while read f; do
  grep -q "\[TERM:" "$f" || echo "$f"
done
```

---

## Marker Types

| Marker | Pattern | Purpose | Example |
|--------|---------|---------|---------|
| Term | `[TERM:name]` | Reference to defined term | `[TERM:Company]` |
| Document | `[DOC:code]` | Reference to another document | `[DOC:B1]` |
| Section | `[DOC:code#section]` | Reference to specific section | `[DOC:B1#5.2]` |
| Obligation | `[OBL:id]` | Link to obligation in obligations.md | `[OBL:MSB-REG-001]` |
| Flow | `[FLOW:name]` | Link to process flow | `[FLOW:client_onboarding]` |
| Decision | `[DECISION:id]` | Link to decision authority | `[DECISION:STRATEGIC-001]` |
| Right | `[RIGHT:id]` | Link to rights allocation | `[RIGHT:TERMINATE-001]` |

---

## Marker Placement Rules

### Term Markers `[TERM:*]`

Place after **first use** of a defined term in each document section:

```markdown
<!-- WRONG: Every instance -->
The [TERM:Company] shall notify the [TERM:Company] and the [TERM:Company]...

<!-- RIGHT: First use per section -->
The [TERM:Company] shall notify the Company and require that...

<!-- Also acceptable: Inline after the term -->
The Company [TERM:Company] shall notify...
```

**Required terms to mark** (from defined_terms.md):
- Company, Client Series, End Customer
- Manager, CCO, Treasurer, Secretary
- MSB, FinCEN, BSA/AML
- Services, Platform, Fiat Gateway

### Document Markers `[DOC:*]`

Place when referencing another document or incorporating by reference:

```markdown
<!-- Cross-reference -->
...as defined in the Master Operating Agreement [DOC:B1].

<!-- Section reference -->
...pursuant to Section 5.2 of the Client Services Agreement [DOC:F1#5.2].

<!-- Incorporation -->
The Series List [DOC:A2] is incorporated herein as Exhibit A.
```

### Obligation Markers `[OBL:*]`

Place at the **source** of an obligation (where it's defined):

```markdown
<!-- Fee obligation -->
Client shall pay the Monthly Platform Fee [OBL:FEE-PLATFORM-001] within 
thirty (30) days of invoice.

<!-- Filing obligation -->
Company shall file the BSA/AML report [OBL:BSA-SAR-001] within the 
timeframe required by FinCEN.

<!-- Maintenance obligation -->
Each Client Series shall maintain [OBL:CAPITAL-MIN-001] minimum net 
capital as specified in Schedule C3.
```

### Flow Markers `[FLOW:*]`

Place when describing a process that has a defined flow:

```markdown
<!-- Process reference -->
New clients must complete the onboarding process [FLOW:client_onboarding] 
before accessing Platform services.

<!-- Termination process -->
Termination shall follow the exit procedure [FLOW:client_termination].
```

### Decision Markers `[DECISION:*]`

Place where decision authority is exercised:

```markdown
<!-- Strategic decision -->
The Manager shall have sole authority [DECISION:STRATEGIC-001] to approve 
new Series formations.

<!-- Operational decision -->
The CCO may approve [DECISION:COMPLIANCE-002] client applications that 
meet standard criteria.
```

### Right Markers `[RIGHT:*]`

Place where a right is granted or exercised:

```markdown
<!-- Termination right -->
Company reserves the right [RIGHT:TERMINATE-001] to terminate this 
Agreement upon thirty (30) days written notice.

<!-- Audit right -->
Company shall have the right [RIGHT:AUDIT-001] to audit Client's 
compliance records.
```

---

## Block Markers

For larger annotated sections, use HTML comments:

```markdown
<!-- schema:obligation OBL:FEE-PLATFORM-001 -->
**Section 4.1 Platform Fees**

Client shall pay the Monthly Platform Fee of $[AMOUNT] within thirty (30) 
days of each invoice date. Late payments shall accrue interest at 1.5% 
per month.
<!-- /schema:obligation -->
```

### Block Marker Types

```markdown
<!-- schema:obligation OBL:xxx -->...<!-- /schema:obligation -->
<!-- schema:flow FLOW:xxx -->...<!-- /schema:flow -->
<!-- schema:term TERM:xxx -->...<!-- /schema:term -->
<!-- schema:decision DECISION:xxx -->...<!-- /schema:decision -->
```

---

## Validation Rules

### MARKER-001: Term Must Exist
```yaml
rule: MARKER-001
description: All [TERM:*] markers must reference defined terms
check: "[TERM:X]" → X exists in defined_terms.md
severity: ERROR
```

### MARKER-002: Document Must Exist
```yaml
rule: MARKER-002
description: All [DOC:*] markers must reference registered documents
check: "[DOC:X]" → X exists in document_registry.md
severity: ERROR
```

### MARKER-003: Obligation Must Exist
```yaml
rule: MARKER-003
description: All [OBL:*] markers must reference defined obligations
check: "[OBL:X]" → X exists in obligations.md
severity: ERROR
```

### MARKER-004: Flow Must Exist
```yaml
rule: MARKER-004
description: All [FLOW:*] markers must reference defined flows
check: "[FLOW:X]" → X exists in flows/*.md
severity: ERROR
```

### MARKER-005: First-Use Coverage
```yaml
rule: MARKER-005
description: Key terms should be marked on first use
check: First occurrence of TERM in document has [TERM:*] marker
severity: WARNING
terms: [Company, Client Series, Manager, CCO, Services]
```

### MARKER-006: Obligation Source
```yaml
rule: MARKER-006
description: Each obligation in obligations.md should have source marker
check: OBL:X in obligations.md → [OBL:X] exists in source document
severity: WARNING
```

---

## Output Stripping

When generating OUTPUT, remove all markers:

```python
import re

def strip_markers(content: str) -> str:
    """Remove all schema markers from document content."""
    
    # Inline markers
    patterns = [
        r'\[TERM:[^\]]+\]',
        r'\[DOC:[^\]]+\]',
        r'\[OBL:[^\]]+\]',
        r'\[FLOW:[^\]]+\]',
        r'\[DECISION:[^\]]+\]',
        r'\[RIGHT:[^\]]+\]',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content)
    
    # Block markers (HTML comments)
    content = re.sub(
        r'<!--\s*schema:[^>]*-->', 
        '', 
        content
    )
    content = re.sub(
        r'<!--\s*/schema:[^>]*-->', 
        '', 
        content
    )
    
    # Clean up double spaces left by removal
    content = re.sub(r'  +', ' ', content)
    
    return content
```

---

## Quick Reference Card

```
TERMS:      [TERM:Company] [TERM:Client Series] [TERM:Manager] [TERM:CCO]
            [TERM:Services] [TERM:Platform] [TERM:MSB] [TERM:FinCEN]

DOCUMENTS:  [DOC:A1] [DOC:B1] [DOC:F1] [DOC:B1#5.2] [DOC:F1#4.1]

OBLIGATIONS:[OBL:FEE-PLATFORM-001] [OBL:BSA-SAR-001] [OBL:CAPITAL-MIN-001]

FLOWS:      [FLOW:client_onboarding] [FLOW:client_termination] [FLOW:sar_filing]

DECISIONS:  [DECISION:STRATEGIC-001] [DECISION:COMPLIANCE-002]

RIGHTS:     [RIGHT:TERMINATE-001] [RIGHT:AUDIT-001] [RIGHT:ACCESS-001]
```
