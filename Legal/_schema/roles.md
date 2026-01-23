# Execution Roles

> **Purpose**: Defines agent roles for framework execution.
> Inspired by audit methodology: independent auditors → consolidator → final report.

---

## Role Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         COMMAND INPUT                           │
│            (audit | amend | validate | generate | review)       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          DISPATCHER                             │
│                  (routes to appropriate role)                   │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│   AUDITOR_1   │       │   AUDITOR_2   │       │   AUDITOR_N   │
│   (isolated)  │       │   (isolated)  │       │   (isolated)  │
│               │       │               │       │               │
│ Focus: Model  │       │ Focus: Refs   │       │ Focus: Terms  │
│ _temp/aud_1/  │       │ _temp/aud_2/  │       │ _temp/aud_N/  │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CONSOLIDATOR                             │
│        (reads all auditor outputs, resolves conflicts,          │
│         produces balanced recommendations)                      │
│                                                                 │
│                      _temp/consolidated/                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          DRAFTER                                │
│           (implements approved changes to SOURCE)               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          REVIEWER                               │
│              (validates changes, generates OUTPUT)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Role Definitions

### AUDITOR

**Purpose**: Independent analysis of documents against specific criteria.

```yaml
role: AUDITOR
instance: "{auditor_id}"  # e.g., "model_language", "cross_refs", "defined_terms"
isolation: STRICT         # Cannot read other auditor outputs
output_dir: "./_temp/auditor_{auditor_id}/"

behavior:
  - Read: _schema/* (all schema files)
  - Read: Source documents (per structure.md paths)
  - Write: ONLY to own _temp/auditor_{id}/ directory
  - Cannot: Read _temp/auditor_*/ of other auditors
  - Cannot: Modify SOURCE files
  - Cannot: Write to OUTPUT/

output_format:
  findings.md: |
    # Audit Findings: {auditor_id}
    Auditor: {auditor_id}
    Timestamp: {ISO8601}
    Scope: {what was audited}
    
    ## Summary
    | Severity | Count |
    |----------|-------|
    | ERROR    | N     |
    | WARNING  | N     |
    | INFO     | N     |
    
    ## Findings
    ### FINDING-001
    - Severity: ERROR|WARNING|INFO
    - Document: {doc_code}
    - Location: {line or section}
    - Rule: {rule_id from templates.md}
    - Found: "{actual text}"
    - Expected: "{expected pattern}"
    - Recommendation: "{suggested fix}"
    
    ### FINDING-002
    ...
    
  recommendations.md: |
    # Recommendations: {auditor_id}
    
    ## Proposed Changes
    | Priority | Document | Change | Rationale |
    |----------|----------|--------|-----------|
    | HIGH     | B1       | ...    | ...       |
    
    ## Implementation Notes
    {any context for consolidator}
```

### Auditor Specializations

```yaml
auditors:
  model_language:
    focus: "MSB model compliance (MSB-001 to MSB-004)"
    scope: "All documents"
    rules: [MSB-001, MSB-002, MSB-003, MSB-004]
    
  cross_references:
    focus: "Document link integrity"
    scope: "All [DOC:*] references"
    rules: [REF-001, REF-002]
    
  defined_terms:
    focus: "Term consistency and usage"
    scope: "All [TERM:*] usage"
    rules: [TERM-001, TERM-002]
    
  obligations:
    focus: "Obligation completeness and consistency"
    scope: "obligations.md vs document text"
    rules: [OBL-001, OBL-002]
    
  state_compliance:
    focus: "State-specific requirements (N3)"
    scope: "N3, B7, F1"
    rules: [STATE-001, STATE-002]
```

---

### CONSOLIDATOR

**Purpose**: Synthesize auditor findings into balanced recommendations.

```yaml
role: CONSOLIDATOR
isolation: NONE           # Can read all auditor outputs
input_dirs: "./_temp/auditor_*/"
output_dir: "./_temp/consolidated/"

behavior:
  - Read: _schema/* (all schema files)
  - Read: ALL _temp/auditor_*/ directories
  - Read: Source documents
  - Write: ONLY to _temp/consolidated/
  - Cannot: Modify SOURCE files
  - Cannot: Write to OUTPUT/

process:
  1. Collect all auditor findings
  2. Deduplicate (same finding from multiple auditors)
  3. Resolve conflicts (auditors disagree)
  4. Prioritize by severity and impact
  5. Produce balanced implementation plan

output_format:
  consolidated_findings.md: |
    # Consolidated Audit Findings
    Generated: {ISO8601}
    Auditors: [{list of auditor_ids}]
    
    ## Consensus Findings (all auditors agree)
    | ID | Severity | Document | Finding | Auditors |
    
    ## Disputed Findings (auditors disagree)
    | ID | Finding | Auditor A Says | Auditor B Says | Resolution |
    
    ## Unique Findings (single auditor)
    | ID | Severity | Document | Finding | Auditor |
    
  implementation_plan.md: |
    # Implementation Plan
    
    ## Phase 1: Critical (ERRORs)
    | Document | Change | Rationale | Est. Impact |
    
    ## Phase 2: Important (WARNINGs)
    ...
    
    ## Phase 3: Improvements (INFO)
    ...
    
    ## Deferred
    | Finding | Reason for Deferral |
    
  change_manifest.md: |
    # Change Manifest
    
    ## Approved Changes
    - CHANGE-001:
        document: B1
        section: "Section 5.2"
        old_text: "..."
        new_text: "..."
        rationale: "..."
        approved: true
    
    ## Rejected Changes
    - CHANGE-002:
        finding: FINDING-005
        reason: "Out of scope / requires legal review"
```

---

### DRAFTER

**Purpose**: Implement approved changes to source documents.

```yaml
role: DRAFTER
isolation: CONTROLLED
input: "./_temp/consolidated/change_manifest.md"
output: SOURCE files (direct modification)

behavior:
  - Read: _schema/*
  - Read: _temp/consolidated/change_manifest.md
  - Read: Source documents
  - Write: SOURCE files (approved changes only)
  - Cannot: Create new findings
  - Cannot: Modify _temp/
  - Cannot: Write to OUTPUT/

constraints:
  - ONLY implement changes marked approved: true
  - MUST preserve document structure/formatting
  - MUST update version history in each modified doc
  - MUST NOT make changes not in manifest

output_format:
  draft_log.md: |
    # Draft Log
    
    ## Changes Applied
    | Change ID | Document | Status | Notes |
    
    ## Skipped
    | Change ID | Reason |
```

---

### REVIEWER

**Purpose**: Validate changes and generate final output.

```yaml
role: REVIEWER
isolation: NONE
input: Modified SOURCE files
output: OUTPUT/ directory

behavior:
  - Read: All _schema/*
  - Read: All SOURCE files
  - Read: _temp/consolidated/ (for comparison)
  - Write: OUTPUT/ directory
  - Cannot: Modify SOURCE files
  - Cannot: Modify _temp/

process:
  1. Re-run full validation (Phase 3 from README.md)
  2. Compare pre/post change state
  3. Generate clean OUTPUT files
  4. Generate registers and matrices
  5. Produce final validation report

output_format:
  review_report.md: |
    # Review Report
    
    ## Validation Results
    | Metric | Before | After | Delta |
    |--------|--------|-------|-------|
    | ERRORs | N | M | ±X |
    | WARNINGs | N | M | ±X |
    
    ## Changes Verified
    | Change ID | Implemented | Validated |
    
    ## Remaining Issues
    [Any new issues introduced]
```

---

## Execution Isolation Rules

```yaml
isolation_matrix:
  AUDITOR:
    can_read:
      - _schema/*
      - SOURCE/**/*.md
    cannot_read:
      - _temp/auditor_*/ (other auditors)
      - _temp/consolidated/
      - OUTPUT/
    can_write:
      - _temp/auditor_{self}/
      
  CONSOLIDATOR:
    can_read:
      - _schema/*
      - SOURCE/**/*.md
      - _temp/auditor_*/ (all auditors)
    cannot_read:
      - OUTPUT/
    can_write:
      - _temp/consolidated/
      
  DRAFTER:
    can_read:
      - _schema/*
      - SOURCE/**/*.md
      - _temp/consolidated/change_manifest.md
    cannot_read:
      - _temp/auditor_*/
    can_write:
      - SOURCE/**/*.md (approved changes only)
      
  REVIEWER:
    can_read:
      - _schema/*
      - SOURCE/**/*.md
      - _temp/consolidated/
    cannot_read:
      - _temp/auditor_*/
    can_write:
      - OUTPUT/**
```

---

## Temp Directory Structure

```
./_temp/
├── auditor_model_language/
│   ├── findings.md
│   └── recommendations.md
├── auditor_cross_references/
│   ├── findings.md
│   └── recommendations.md
├── auditor_defined_terms/
│   ├── findings.md
│   └── recommendations.md
├── auditor_obligations/
│   ├── findings.md
│   └── recommendations.md
├── auditor_state_compliance/
│   ├── findings.md
│   └── recommendations.md
└── consolidated/
    ├── consolidated_findings.md
    ├── implementation_plan.md
    ├── change_manifest.md
    └── review_report.md
```

---

## Role Invocation

```markdown
## To invoke a role:

### As AUDITOR:
"Execute as AUDITOR:{auditor_id}. Read _schema/roles.md for behavior constraints."

### As CONSOLIDATOR:
"Execute as CONSOLIDATOR. Read _schema/roles.md for behavior constraints.
Auditor outputs are in _temp/auditor_*/"

### As DRAFTER:
"Execute as DRAFTER. Read _schema/roles.md for behavior constraints.
Change manifest is at _temp/consolidated/change_manifest.md"

### As REVIEWER:
"Execute as REVIEWER. Read _schema/roles.md for behavior constraints."
```

