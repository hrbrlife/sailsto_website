# Command Vocabulary

> **Purpose**: Defines the command interface for framework execution.
> Like a Makefile, different commands invoke different workflows.

---

## Command Syntax

```
COMMAND [ROLE] [TARGET] [OPTIONS]

Examples:
  audit all
  audit model_language B1
  amend B1 "fix MSB language"
  validate --strict
  generate registers
  review changes
```

---

## Commands

### `audit`

**Purpose**: Run independent audit(s) on documents.

```yaml
command: audit
aliases: [check, analyze, inspect]

usage:
  audit all                      # All auditors, all documents
  audit {auditor_id}             # Single auditor, all documents
  audit {auditor_id} {doc_code}  # Single auditor, single document
  audit --parallel               # Run all auditors in parallel

auditor_ids:
  - model_language      # MSB model compliance
  - cross_references    # Document link integrity
  - defined_terms       # Term consistency
  - obligations         # Obligation completeness
  - state_compliance    # State-specific requirements

options:
  --strict              # Fail on any WARNING (default: fail on ERROR only)
  --parallel            # Run auditors in parallel (default: sequential)
  --output {dir}        # Override _temp/ directory
  
workflow:
  1. Dispatcher routes to AUDITOR role(s)
  2. Each AUDITOR writes to _temp/auditor_{id}/
  3. Returns summary of findings per auditor
  
output:
  _temp/auditor_{id}/findings.md
  _temp/auditor_{id}/recommendations.md
```

### `consolidate`

**Purpose**: Combine auditor findings into implementation plan.

```yaml
command: consolidate
aliases: [merge, combine, synthesize]

usage:
  consolidate                    # Consolidate all auditor outputs
  consolidate --approve-all      # Auto-approve all recommendations
  consolidate --interactive      # Prompt for each conflict

options:
  --approve-all         # Approve all non-conflicting changes
  --approve-critical    # Approve only ERROR fixes
  --interactive         # Prompt user for conflict resolution
  
prerequisites:
  - At least one audit must have run
  
workflow:
  1. Dispatcher invokes CONSOLIDATOR role
  2. CONSOLIDATOR reads all _temp/auditor_*/
  3. Produces consolidated findings and change manifest
  
output:
  _temp/consolidated/consolidated_findings.md
  _temp/consolidated/implementation_plan.md
  _temp/consolidated/change_manifest.md
```

### `amend`

**Purpose**: Make specific changes to documents.

```yaml
command: amend
aliases: [edit, change, update, fix]

usage:
  amend {doc_code} "{description}"   # Amend specific document
  amend --from-manifest              # Apply all approved changes
  amend --interactive                # Review each change before applying

options:
  --from-manifest       # Apply changes from change_manifest.md
  --dry-run             # Show what would change without modifying
  --interactive         # Prompt before each change
  
workflow:
  1. Dispatcher invokes DRAFTER role
  2. DRAFTER reads change_manifest.md (or creates ad-hoc change)
  3. DRAFTER modifies SOURCE files
  4. Logs changes to _temp/consolidated/draft_log.md
  
output:
  Modified SOURCE files
  _temp/consolidated/draft_log.md
```

### `validate`

**Purpose**: Run validation without audit findings generation.

```yaml
command: validate
aliases: [check, verify]

usage:
  validate                       # Validate all documents
  validate {doc_code}            # Validate single document
  validate --output              # Validate OUTPUT directory

options:
  --strict              # Fail on WARNING
  --output              # Validate OUTPUT/ instead of SOURCE
  --report              # Generate validation report
  
workflow:
  1. Dispatcher invokes REVIEWER role (validation only)
  2. Runs template matching and rule checking
  3. Reports pass/fail
  
output:
  Console output (pass/fail per document)
  Optional: VALIDATION_REPORT.md
```

### `generate`

**Purpose**: Generate output files and registers.

```yaml
command: generate
aliases: [build, produce, output]

usage:
  generate all                   # Full OUTPUT generation
  generate documents             # Clean documents only
  generate registers             # Registers only
  generate matrices              # Matrices only
  generate report                # Validation report only

targets:
  all:        [documents, registers, matrices, report]
  documents:  Clean copies to OUTPUT/{series}/{purpose}/
  registers:  [OBLIGATIONS, PROCESSES, DECISIONS, RIGHTS]
  matrices:   [DECISION_MATRIX, RIGHTS_MATRIX, RACI_MATRIX]
  report:     VALIDATION_REPORT.md

options:
  --force               # Regenerate even if up-to-date
  --clean               # Remove OUTPUT/ before generating
  
prerequisites:
  - Validation must pass (or --force)
  
workflow:
  1. Dispatcher invokes REVIEWER role
  2. Validates SOURCE (unless --force)
  3. Generates OUTPUT structure
  4. Re-validates OUTPUT
  
output:
  OUTPUT/{series}/{purpose}/*.md
  OUTPUT/Registers/*.md
  OUTPUT/Matrices/*.md
  OUTPUT/VALIDATION_REPORT.md
```

### `review`

**Purpose**: Review changes or current state.

```yaml
command: review
aliases: [diff, compare, status]

usage:
  review changes                 # Review pending changes in manifest
  review audit                   # Review audit findings
  review status                  # Current validation status
  review diff {doc_code}         # Show changes to specific doc

options:
  --verbose             # Detailed output
  --json                # Machine-readable output
  
workflow:
  1. Read relevant _temp/ files
  2. Format and display
  
output:
  Console output (formatted)
```

### `clean`

**Purpose**: Clean temporary and output files.

```yaml
command: clean
aliases: [reset, clear]

usage:
  clean temp                     # Remove _temp/
  clean output                   # Remove OUTPUT/
  clean all                      # Remove both

options:
  --dry-run             # Show what would be removed
  
workflow:
  1. Remove specified directories
  2. Report what was removed
```

### `init`

**Purpose**: Initialize or migrate workspace structure.

```yaml
command: init
aliases: [setup, migrate]

usage:
  init                           # Create _schema directories
  init --migrate                 # Migrate flat structure to organized

options:
  --migrate             # Move existing docs to new structure
  --dry-run             # Show what would change
  
workflow:
  1. Create directory structure per structure.md
  2. If --migrate: move files to new locations
  3. Update cross-references
```

---

## Command Pipelines

Common multi-command workflows:

### Full Audit Pipeline
```bash
# Clean slate
clean all

# Run all auditors in parallel
audit all --parallel

# Consolidate findings
consolidate --interactive

# Apply approved changes
amend --from-manifest

# Generate output
generate all
```

### Quick Validation
```bash
validate --strict
```

### Specific Document Fix
```bash
audit model_language B1
amend B1 "Update MSB independence language"
validate B1
```

### CI/CD Pipeline
```bash
audit all --parallel
consolidate --approve-critical
amend --from-manifest --dry-run
validate --strict
generate all
```

---

## Command → Role Mapping

| Command | Primary Role | May Invoke |
|---------|--------------|------------|
| `audit` | AUDITOR | - |
| `consolidate` | CONSOLIDATOR | - |
| `amend` | DRAFTER | - |
| `validate` | REVIEWER | - |
| `generate` | REVIEWER | DRAFTER (if auto-fix) |
| `review` | (none - read only) | - |
| `clean` | (none - file ops) | - |
| `init` | (none - file ops) | - |

---

## Error Codes

```yaml
exit_codes:
  0: Success
  1: Validation failed (ERRORs found)
  2: Validation warnings (--strict mode)
  3: Missing prerequisites (e.g., no audits for consolidate)
  4: File not found
  5: Permission denied (isolation violation)
  6: Invalid command/syntax
```

---

## Command Invocation via LLM

To invoke a command, use this format in your prompt:

```markdown
Execute: {command} {args}

Example:
Execute: audit model_language
Execute: consolidate --approve-critical
Execute: amend --from-manifest
Execute: generate all
```

The LLM should:
1. Read `_schema/commands.md` (this file)
2. Parse the command
3. Read `_schema/roles.md` for role behavior
4. Execute according to workflow
5. Produce output in specified format

