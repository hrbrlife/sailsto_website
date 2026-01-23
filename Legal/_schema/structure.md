# Document Structure

> **Purpose**: Defines folder organization by Series Type → Purpose Type → Document Prefix.
> This file governs both SOURCE and OUTPUT directory layouts.

---

## Layout States

The workspace can be in one of two states:

```yaml
layout_states:
  FLAT:
    description: "All documents in root directory (pre-migration)"
    detection: "NOT exists(Company/) AND NOT exists(Client_Series/)"
    path_pattern: "./{DocCode}_*.md"
    example: "./B1_Master_Operating_Agreement.md"
    
  MIGRATED:
    description: "Documents organized by series/purpose (post-migration)"
    detection: "exists(Company/) AND exists(Client_Series/)"
    path_pattern: "./{SeriesType}/{PurposeType}/{DocCode}_*.md"
    example: "./Company/Governance/B1_Master_Operating_Agreement.md"
```

**Discovery must support both states.** Use `init --migrate` to transition from FLAT → MIGRATED.

---

## Series Types

```yaml
series_types:
  Company:
    code: "CO"
    description: "Master company-level documents (CCASH Holdings LLC itself)"
    owns: [A1, B1-B11, 00_*]
    
  Client_Series:
    code: "CS"
    description: "Documents for/about Client Series LLCs"
    owns: [A2, A3, C2, D1, F1, F2, N1, N3, N4, N5]
    
  Internal:
    code: "IN"
    description: "Internal operations, checklists, guides"
    owns: [E1, E2, C1, C3]
```

---

## Purpose Types

```yaml
purpose_types:
  Formation:
    prefix: "A|D"
    description: "Entity creation, amendments, articles"
    
  Governance:
    prefix: "B[1-3]|B10"
    description: "Operating agreements, officers, succession"
    
  Compliance:
    prefix: "B[4-9]"
    description: "BSA/AML, privacy, security, screening"
    
  Client:
    prefix: "F|B11"
    description: "Client-facing agreements and frameworks"
    
  Registration:
    prefix: "C"
    description: "ABN filings, registrations"
    
  Checklist:
    prefix: "E"
    description: "Filing guides, checklists"
    
  Schedule:
    prefix: "N"
    description: "Schedules, exhibits, reference tables"
    
  Overview:
    prefix: "00_"
    description: "README, business model, summaries"
```

---

## Directory Layout

### SOURCE Layout (Current Workspace)
```
./
├── Company/                          # CO - Master company docs
│   ├── Formation/
│   │   └── A1_Articles_of_Organization.md
│   ├── Governance/
│   │   ├── B1_Master_Operating_Agreement.md
│   │   ├── B2_Officer_Appointment_Resolution.md
│   │   ├── B3_Officer_Rotation_Succession_Policy.md
│   │   └── B10_Insurance_and_Capital_Policy.md
│   ├── Compliance/
│   │   ├── B4_Record_Keeping_Policy.md
│   │   ├── B5_BSA_AML_Program.md
│   │   ├── B6_IT_Security_Incident_BCP_DRP.md
│   │   ├── B7_Acceptable_Client_Use_Policy.md
│   │   ├── B8_Privacy_Data_Protection_Policy.md
│   │   └── B9_Fit_and_Proper_Screening_Policy.md
│   └── Overview/
│       ├── 00_README.md
│       └── 00_Business_Model.md
│
├── Client_Series/                    # CS - Client series docs
│   ├── Formation/
│   │   ├── A2_Exhibit_A_Series_List.md
│   │   ├── A3_Exhibit_B_Series_Operating_Agreements.md
│   │   └── D1_Articles_of_Amendment_Add_Series.md
│   ├── Client/
│   │   ├── B11_Client_Services_and_Licensing_Framework.md
│   │   ├── F1_Client_Services_Agreement.md
│   │   └── F2_End_Customer_Terms_Template.md
│   └── Schedule/
│       ├── N1_Partner_MSB_Agreement.md
│       ├── N3_Approved_States_Schedule.md
│       ├── N4_Partner_MSB_Directory.md
│       └── N5_Client_FinCEN_Filing_Guide.md
│
├── Internal/                         # IN - Internal ops docs
│   ├── Registration/
│   │   ├── C1_ABN_Registration_CCASH.md
│   │   ├── C2_ABN_Template_Client_Series.md
│   │   └── C3_Pricing_and_Routing_Schedule.md
│   └── Checklist/
│       ├── E1_Filing_Checklist_and_Instructions.md
│       └── E2_Securities_and_MTL_Checklist.md
│
├── _schema/                          # Framework (not documents)
│   ├── knowledge_base/               # Primary regulatory sources (weight: 1.0)
│   │   ├── 31_cfr_*.txt              # CFR excerpts
│   │   ├── 31_usc_*.txt              # USC excerpts
│   │   ├── fincen_*.md               # FinCEN guidance
│   │   └── ...
│   ├── research_outputs/             # Secondary LLM research (weight: 0.5)
│   │   ├── README.md                 # Index and validation status
│   │   ├── prompts.md                # Research prompt templates
│   │   ├── 01_mt_msb_licensing_federal_overlay.md
│   │   ├── 02_interstate_operations_analysis.md
│   │   ├── 03_mt_msb_case_law_digest.md
│   │   ├── 04_series_llc_msb_structural_analysis.md
│   │   └── ...
│   └── validation/                   # Validation tools
│       ├── llm_audit/                # LLM audit pipeline
│       └── ccash_validator/          # Python validation package
│
├── _temp/                            # Auditor working directories
│   ├── auditor_1/
│   ├── auditor_2/
│   └── auditor_N/
│
└── OUTPUT/                           # Final consolidated output
    └── ...
```

### OUTPUT Layout (Generated)
```
./OUTPUT/
├── Company/
│   ├── Formation/
│   ├── Governance/
│   ├── Compliance/
│   └── Overview/
├── Client_Series/
│   ├── Formation/
│   ├── Client/
│   └── Schedule/
├── Internal/
│   ├── Registration/
│   └── Checklist/
├── Registers/
│   ├── OBLIGATIONS.md
│   ├── PROCESSES.md
│   ├── DECISIONS.md
│   └── RIGHTS.md
├── Matrices/
│   ├── DECISION_MATRIX.md
│   ├── RIGHTS_MATRIX.md
│   └── RACI_MATRIX.md
└── VALIDATION_REPORT.md
```

---

## Document Path Resolution

Given a document code, resolve its path based on layout state:

```python
def resolve_path(doc_code: str, layout: str = None) -> str:
    """
    Resolve document path for either layout state.
    
    FLAT layout:
      A1 → ./A1_*.md
      B5 → ./B5_*.md
      
    MIGRATED layout:
      A1 → ./Company/Formation/A1_*.md
      B5 → ./Company/Compliance/B5_*.md
      F1 → ./Client_Series/Client/F1_*.md
      E1 → ./Internal/Checklist/E1_*.md
    """
    
    # Detect layout if not provided
    if layout is None:
        layout = "MIGRATED" if exists("Company/") else "FLAT"
    
    if layout == "FLAT":
        return f"./{doc_code}_*.md"
    
    # MIGRATED: resolve series and purpose
    series = lookup_series_owner(doc_code)
    purpose = match_purpose_type(doc_code)
    
    return f"./{series}/{purpose}/{doc_code}_*.md"

def lookup_series_owner(doc_code: str) -> str:
    """Map doc_code to series type."""
    ownership = {
        "Company": ["A1", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "00_README", "00_Business_Model"],
        "Client_Series": ["A2", "A3", "B11", "C2", "D1", "F1", "F2", "N3", "N5"],
        "Internal": ["C1", "C3", "E1", "E2"],
    }
    for series, codes in ownership.items():
        if doc_code in codes or any(doc_code.startswith(c.rstrip("*")) for c in codes if "*" in c):
            return series
    return "Internal"  # default

def match_purpose_type(doc_code: str) -> str:
    """Map doc_code prefix to purpose type."""
    import re
    mappings = [
        (r"^(A1|D)", "Formation"),
        (r"^A[23]", "Formation"),  # Client_Series formation
        (r"^B(1[01]?|2|3)$", "Governance"),
        (r"^B[4-9]$", "Compliance"),
        (r"^B11$", "Client"),
        (r"^F", "Client"),
        (r"^C", "Registration"),
        (r"^E", "Checklist"),
        (r"^N", "Schedule"),
        (r"^00_", "Overview"),
    ]
    for pattern, purpose in mappings:
        if re.match(pattern, doc_code):
            return purpose
    return "Other"
```

---

## Migration

To migrate from flat structure to organized:

```bash
# Phase 1: Create directories
mkdir -p Company/{Formation,Governance,Compliance,Overview}
mkdir -p Client_Series/{Formation,Client,Schedule}
mkdir -p Internal/{Registration,Checklist}

# Phase 2: Move files (by prefix)
mv A1_*.md Company/Formation/
mv B1_*.md B2_*.md B3_*.md B10_*.md Company/Governance/
mv B[4-9]_*.md Company/Compliance/
mv 00_*.md Company/Overview/

mv A2_*.md A3_*.md D1_*.md Client_Series/Formation/
mv B11_*.md F*.md Client_Series/Client/
mv N*.md Client_Series/Schedule/

mv C*.md Internal/Registration/
mv E*.md Internal/Checklist/
```

---

## Cross-Reference Updates

After migration, update document_registry.md paths and cross_references.md links.

| Old Path | New Path |
|----------|----------|
| `./A1_*.md` | `./Company/Formation/A1_*.md` |
| `./B5_*.md` | `./Company/Compliance/B5_*.md` |
| `./F1_*.md` | `./Client_Series/Client/F1_*.md` |
| ... | ... |

