# CCASH Legal Operations Framework

> **LLM INSTRUCTION**: This is the command dispatcher for the legal document framework.
> Parse the command and execute according to the appropriate role.

---

## Implementation Status

<!-- schema:status Last-Updated: 2025-12-21 -->

| Metric | Count | Status |
|--------|-------|--------|
| Documents Annotated | 28 | ✓ Complete |
| TERM Markers | 2,260+ | ✓ Embedded |
| DOC Markers | 460+ | ✓ Embedded |
| OBL Markers | 80+ | ✓ Embedded |
| FLOW Markers | 100+ | ✓ Embedded |
| DECISION Markers | 4 | ✓ Embedded |
| RIGHT Markers | 4 | ✓ Embedded |
| Schema Files | 13 | ✓ Created |

### Document Coverage

**Company Documents** (14 files):

*Formation (1):*
- [x] A1_Articles_of_Organization

*Governance (4):*
- [x] B1_Master_Operating_Agreement (v1.4)
- [x] B2_Officer_Appointment_Resolution
- [x] B3_Officer_Rotation_Succession_Policy (v1.2)
- [x] B10_Insurance_and_Capital_Policy

*Compliance (7):*
- [x] B4_Record_Keeping_Policy (v1.3)
- [x] B5_BSA_AML_Program
- [x] B6_IT_Security_Incident_BCP_DRP (v1.4)
- [x] B7_Acceptable_Client_Use_Policy (v1.4)
- [x] B8_Privacy_Data_Protection_Policy
- [x] B9_Fit_and_Proper_Screening_Policy
- [x] B12_Partner_Due_Diligence_Standard (v1.1) **NEW**

*Overview (2):*
- [x] 00_README
- [x] 00_Business_Model

**Client Series Documents** (10 files):

*Client (3):*
- [x] B11_Client_Services_and_Licensing_Framework (v1.8)
- [x] F1_Client_Services_Agreement (v1.7)
- [x] F2_End_Customer_Terms_Template (v1.8)

*Formation (3):*
- [x] A2_Exhibit_A_Series_List
- [x] A3_Exhibit_B_Series_Operating_Agreements
- [x] D1_Articles_of_Amendment_Add_Series

*Schedule (4):*
- [x] N1_Partner_MSB_Agreement (v1.4)
- [x] N3_Approved_States_Schedule (v1.4)
- [x] N4_Partner_MSB_Directory (v1.3)
- [x] N5_Client_FinCEN_Filing_Guide (v1.1)

**Internal Documents** (5 files):

*Checklist (2):*
- [x] E1_Filing_Checklist_and_Instructions
- [x] E2_Securities_and_MTL_Checklist

*Registration (3):*
- [x] C1_ABN_Registration_CCASH
- [x] C2_ABN_Template_Client_Series
- [x] C3_Pricing_and_Routing_Schedule

---

## Quick Start

```markdown
# To execute a command:
Execute: {command} [args] [options]

# Examples:
Execute: audit all
Execute: consolidate --approve-critical
Execute: amend --from-manifest
Execute: generate all
Execute: validate --strict
```

---

## Framework Files

```yaml
Core Schema:
  _schema/defined_terms.md      # Entity type definitions
  _schema/templates.md          # Document templates + validation rules  
  _schema/document_registry.md  # Document inventory + dependencies
  _schema/cross_references.md   # Document link graph
  _schema/structure.md          # Folder organization rules

Person & Role Management:
  _schema/llc_roles.md          # All LLC role types (Manager, CEO, CCO, etc.)
  _schema/entity_config.md      # Flexible entity role configuration
  _schema/persons.md            # Person registry (names, addresses, etc.)
  _schema/assignments.md        # Role assignments (who holds what where)
  _schema/field_mappings.md     # Document placeholder → registry mappings

Operational:
  _schema/obligations.md        # Who owes what to whom, when
  _schema/decisions_rights.md   # Who decides what, who has what rights
  _schema/flows/*.md            # Process/workflow definitions

Execution:
  _schema/commands.md           # Command syntax and workflows
  _schema/roles.md              # AI/automation role definitions
  _schema/README.md             # This file (dispatcher)

Validation:
  _schema/validation/patterns.yaml        # Validation patterns
  _schema/validation/ccash_validator/     # Python validation package
  _schema/validation/llm_audit/           # LLM-based audit pipeline

Knowledge Sources:
  _schema/knowledge_base/                 # Primary regulatory sources (weight: 1.0)
  _schema/research_outputs/               # Secondary LLM research (weight: 0.5)
```

---

## Command Dispatch

When you receive `Execute: {command}`, follow this dispatch table:

| Command | Action |
|---------|--------|
| `audit` | → Go to [AUDIT WORKFLOW](#audit-workflow) |
| `consolidate` | → Go to [CONSOLIDATE WORKFLOW](#consolidate-workflow) |
| `amend` | → Go to [AMEND WORKFLOW](#amend-workflow) |
| `validate` | → Go to [VALIDATE WORKFLOW](#validate-workflow) |
| `generate` | → Go to [GENERATE WORKFLOW](#generate-workflow) |
| `review` | → Go to [REVIEW WORKFLOW](#review-workflow) |
| `clean` | → Go to [CLEAN WORKFLOW](#clean-workflow) |
| `init` | → Go to [INIT WORKFLOW](#init-workflow) |

---

## AUDIT WORKFLOW

**Role**: AUDITOR (see `roles.md`)

### Step 1: Parse Arguments
```
audit [auditor_id] [doc_code] [--parallel] [--strict]

auditor_id (optional): model_language | cross_references | defined_terms | obligations | state_compliance
doc_code (optional): A1, B1, F1, etc.
--parallel: Run multiple auditors concurrently
--strict: Fail on WARNING (default: fail on ERROR only)
```

### Step 2: Load Schema
Read these files into context:
- `_schema/defined_terms.md`
- `_schema/templates.md`
- `_schema/document_registry.md`
- `_schema/structure.md`

### Step 3: Determine Scope
```python
if auditor_id == "all" or not auditor_id:
    auditors = ["model_language", "cross_references", "defined_terms", "obligations", "state_compliance"]
else:
    auditors = [auditor_id]

if doc_code:
    documents = [doc_code]
else:
    documents = discover_documents()  # Per structure.md
```

### Step 4: Execute Audit(s)
For each auditor:
1. **Enforce isolation**: Can only write to `_temp/auditor_{id}/`
2. Read source documents
3. Apply rules from `templates.md` relevant to this auditor's focus
4. Write findings to `_temp/auditor_{id}/findings.md`
5. Write recommendations to `_temp/auditor_{id}/recommendations.md`

### Step 5: Report
```markdown
## Audit Complete

| Auditor | ERRORs | WARNINGs | INFO |
|---------|--------|----------|------|
| model_language | N | N | N |
| ... | ... | ... | ... |

Outputs written to: _temp/auditor_*/
Next: Execute: consolidate
```

---

## CONSOLIDATE WORKFLOW

**Role**: CONSOLIDATOR (see `roles.md`)

### Step 1: Parse Arguments
```
consolidate [--approve-all] [--approve-critical] [--interactive]

--approve-all: Auto-approve all non-conflicting changes
--approve-critical: Approve only ERROR fixes
--interactive: Prompt for conflict resolution
```

### Step 2: Check Prerequisites
```python
if not exists("_temp/auditor_*/findings.md"):
    error("No audit findings. Run: Execute: audit all")
    exit(3)
```

### Step 3: Load All Auditor Outputs
Read all files in:
- `_temp/auditor_model_language/`
- `_temp/auditor_cross_references/`
- `_temp/auditor_defined_terms/`
- `_temp/auditor_obligations/`
- `_temp/auditor_state_compliance/`

### Step 4: Consolidate Findings
1. **Deduplicate**: Same finding from multiple auditors → single entry
2. **Identify conflicts**: Auditors disagree on same issue
3. **Prioritize**: Sort by severity (ERROR > WARNING > INFO)
4. **Resolve conflicts**: Apply resolution strategy per options

### Step 5: Generate Outputs
Write to `_temp/consolidated/`:
- `consolidated_findings.md` — All findings with attribution
- `implementation_plan.md` — Prioritized change list
- `change_manifest.md` — Specific changes with approval status

### Step 6: Report
```markdown
## Consolidation Complete

| Category | Count |
|----------|-------|
| Consensus findings | N |
| Disputed findings | N |
| Unique findings | N |
| Approved changes | N |
| Deferred changes | N |

Outputs written to: _temp/consolidated/
Next: Execute: amend --from-manifest
```

---

## AMEND WORKFLOW

**Role**: DRAFTER (see `roles.md`)

### Step 1: Parse Arguments
```
amend [doc_code] ["description"] [--from-manifest] [--dry-run] [--interactive]

doc_code: Specific document to amend
"description": What to change (for ad-hoc changes)
--from-manifest: Apply all approved changes from change_manifest.md
--dry-run: Show changes without applying
--interactive: Prompt before each change
```

### Step 2: Determine Change Source
```python
if from_manifest:
    changes = read("_temp/consolidated/change_manifest.md")
    changes = filter(changes, approved=True)
elif doc_code and description:
    changes = create_adhoc_change(doc_code, description)
else:
    error("Specify --from-manifest OR {doc_code} {description}")
```

### Step 3: Apply Changes
For each change:
1. Read target document
2. Locate section/text to modify
3. If `--dry-run`: Display diff, continue
4. If `--interactive`: Display diff, prompt "Apply? [y/n]"
5. Apply change to SOURCE file
6. Update version history in document
7. Log to `_temp/consolidated/draft_log.md`

### Step 4: Report
```markdown
## Amendment Complete

| Document | Change | Status |
|----------|--------|--------|
| B1 | Updated Section 5.2 | ✓ Applied |
| F1 | Fixed cross-reference | ✓ Applied |

Modified: N documents
Log: _temp/consolidated/draft_log.md
Next: Execute: validate
```

---

## VALIDATE WORKFLOW

**Role**: REVIEWER (see `roles.md`)

### Step 1: Parse Arguments
```
validate [doc_code] [--strict] [--output] [--report]

doc_code: Specific document to validate (default: all)
--strict: Fail on WARNING
--output: Validate OUTPUT/ directory instead of SOURCE
--report: Generate VALIDATION_REPORT.md
```

### Step 2: Load Schema
Read into context:
- `_schema/defined_terms.md`
- `_schema/templates.md`
- `_schema/document_registry.md`
- `_schema/cross_references.md`
- `_schema/structure.md`

### Step 3: Discover Documents
```python
if output_flag:
    base_path = "./OUTPUT/"
else:
    base_path = "./"

# Discover supports BOTH flat and migrated layouts
documents = discover_documents(base_path, 
    # Flat layout: *.md in root
    include=["*.md", "**/*.md"],
    exclude=[
        "_schema/**",      # Schema files
        "Audits/**",       # Reference material
        "Inspiration/**",  # Templates/examples
        "_temp/**",        # Working directory
        "OUTPUT/**",       # Generated output
    ]
)

# Detect layout state
if exists("Company/") and exists("Client_Series/"):
    layout = "MIGRATED"  # Per structure.md
else:
    layout = "FLAT"      # Pre-migration
    
# Log: "Discovered N documents in {layout} layout"
```

### Step 4: Validate Each Document
For each document:
1. Match template from `templates.md`
2. Apply MVP conditions (BASE-*, MSB-*, etc.)
3. Check cross-references
4. Record violations with severity

### Step 5: Report Results
```markdown
## Validation Results

| Document | Status | ERRORs | WARNINGs |
|----------|--------|--------|----------|
| A1 | ✓ PASS | 0 | 0 |
| B1 | ⚠ WARN | 0 | 2 |
| F1 | ✗ FAIL | 1 | 0 |

Overall: {PASS|WARN|FAIL}
```

If `--report`: Generate `OUTPUT/VALIDATION_REPORT.md` per format in templates section.

---

## GENERATE WORKFLOW

**Role**: REVIEWER (see `roles.md`)

### Step 1: Parse Arguments
```
generate [target] [--force] [--clean]

target: all | documents | registers | matrices | report
--force: Skip validation, generate anyway
--clean: Remove OUTPUT/ before generating
```

### Step 2: Pre-flight
```python
if clean_flag:
    rm -rf OUTPUT/

if not force_flag:
    result = validate()
    if result.errors > 0:
        error("Validation failed. Use --force to override.")
        exit(1)
```

### Step 3: Create Output Structure
Per `structure.md`:
```
OUTPUT/
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
└── Matrices/
```

### Step 4: Generate Content
Based on target:

**documents**: Copy and clean each source document
- Remove schema markers: `[TERM:*]`, `[DOC:*]`, `[FLOW:*]`, `[OBL:*]`
- Remove schema comments: `<!-- schema:* -->`
- Normalize formatting

**registers**: Generate from schema files
- `OBLIGATIONS.md` ← from `obligations.md`
- `PROCESSES.md` ← from `flows/*.md`
- `DECISIONS.md` ← from `decisions_rights.md`
- `RIGHTS.md` ← from `decisions_rights.md`

**matrices**: Generate cross-tabulated views
- `DECISION_MATRIX.md` — Role × Decision
- `RIGHTS_MATRIX.md` — Entity × Right
- `RACI_MATRIX.md` — Process × Role

**report**: Generate validation report
- `VALIDATION_REPORT.md`

### Step 5: Post-validate
Re-run validation on OUTPUT/ to confirm:
- No schema markers remain
- Cross-references still valid

### Step 6: Report
```markdown
## Generation Complete

| Category | Files | Status |
|----------|-------|--------|
| Documents | N | ✓ |
| Registers | 4 | ✓ |
| Matrices | 3 | ✓ |
| Report | 1 | ✓ |

Output directory: ./OUTPUT/
```

---

## REVIEW WORKFLOW

**Purpose**: Read-only inspection of state

### Step 1: Parse Arguments
```
review [target] [--verbose]

target: changes | audit | status | diff {doc_code}
```

### Step 2: Execute Based on Target

**changes**: Display `_temp/consolidated/change_manifest.md`
**audit**: Display `_temp/auditor_*/findings.md` summaries
**status**: Run quick validation, show pass/fail
**diff {doc_code}**: Show pending changes for specific document

---

## CLEAN WORKFLOW

**Purpose**: Remove temporary and generated files

### Step 1: Parse Arguments
```
clean [target] [--dry-run]

target: temp | output | all
```

### Step 2: Execute
```bash
if target == "temp" or target == "all":
    rm -rf _temp/
    
if target == "output" or target == "all":
    rm -rf OUTPUT/
```

---

## INIT WORKFLOW

**Purpose**: Initialize or migrate workspace

### Step 1: Parse Arguments
```
init [--migrate] [--dry-run]

--migrate: Move existing flat files to organized structure
```

### Step 2: Create Directories
Per `structure.md`:
```bash
mkdir -p Company/{Formation,Governance,Compliance,Overview}
mkdir -p Client_Series/{Formation,Client,Schedule}
mkdir -p Internal/{Registration,Checklist}
mkdir -p _temp
mkdir -p OUTPUT
```

### Step 3: If --migrate
Move files per mapping in `structure.md`.

---

## Schema Markers Reference

Remove these when generating OUTPUT:

| Pattern | Regex | Purpose |
|---------|-------|---------|
| Term reference | `\[TERM:[^\]]+\]` | Link to defined term |
| Document reference | `\[DOC:[^\]]+\]` | Link to document |
| Flow reference | `\[FLOW:[^\]]+\]` | Link to process flow |
| Obligation reference | `\[OBL:[^\]]+\]` | Link to obligation |
| Schema comment | `<!--\s*schema:[^>]*-->` | Inline schema metadata |

---

## META

```yaml
framework_version: "2.0"
last_updated: "2025-12-14"
schema_files:
  core:
    - defined_terms.md
    - templates.md
    - document_registry.md
    - cross_references.md
    - structure.md
  operational:
    - obligations.md
    - decisions_rights.md
    - flows/*.md
  execution:
    - commands.md
    - roles.md
    - README.md
```
