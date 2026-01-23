# CCASH LLM Audit System

Multi-agent LLM audit system for CCASH legal documentation using Agent Squad patterns + LiteLLM provider abstraction.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                                  │
│  ┌─────────────┐                                                    │
│  │  Dispatcher │ ──────────────────────────────────────┐            │
│  └─────────────┘                                       │            │
│         │                                              │            │
│         ▼                                              ▼            │
│  ┌─────────────────────────────────────────┐   ┌─────────────┐     │
│  │         PARALLEL AUDITORS               │   │   Context   │     │
│  │  ┌────────┐ ┌────────┐ ┌────────┐      │   │   Manager   │     │
│  │  │ Legal  │ │Complnce│ │Techncl │ ...  │   └─────────────┘     │
│  │  │Auditor │ │Auditor │ │Auditor │      │                        │
│  │  └────────┘ └────────┘ └────────┘      │                        │
│  └─────────────────────────────────────────┘                        │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│  │Consolidator │ ──▶ │   Skeptic   │ ──▶ │  Reviewer   │          │
│  │   Agent     │     │   Agent     │     │   Agent     │          │
│  └─────────────┘     └─────────────┘     └─────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   LiteLLM       │
                    │  Provider Layer │
                    └─────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     ┌──────────┐     ┌──────────┐     ┌──────────┐
     │OpenRouter│     │  OpenAI  │     │Local vLLM│
     │(Claude)  │     │ (GPT-4)  │     │ (Llama)  │
     └──────────┘     └──────────┘     └──────────┘
```

## Installation

```bash
# From the llm_audit directory
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Copy the env template and add your keys (OPENROUTER_API_KEY, etc.)
cp .env.example .env

# Or export directly
export OPENROUTER_API_KEY="your-key-here"

# Audit a single document
llm-audit check Company/Governance/B1_Master_Operating_Agreement.md

# Full audit of multiple documents
llm-audit audit Company/Governance/*.md

# Generate a config file
llm-audit init-config

# List available agents
llm-audit agents
```

## Auditor Agents

Six specialist auditors run in parallel on each document:

| Agent | Expertise | Default Model |
|-------|-----------|---------------|
| `LegalAuditor` | Contract structure, cross-refs, Montana LLC law | x-ai/grok-4.1-fast (OpenRouter) |
| `ComplianceAuditor` | BSA/AML, FinCEN, MSB regulations | x-ai/grok-4.1-fast (OpenRouter) |
| `TechnicalAuditor` | Marker syntax, schema conformance | x-ai/grok-4.1-fast (OpenRouter) |
| `FinancialAuditor` | Capital requirements, insurance, fees | x-ai/grok-4.1-fast (OpenRouter) |
| `DataPrivacyAuditor` | GDPR, CCPA, data handling | x-ai/grok-4.1-fast (OpenRouter) |
| `OperationalAuditor` | Governance, succession, procedures | x-ai/grok-4.1-fast (OpenRouter) |

## Pipeline Agents

After auditors complete, findings flow through the pipeline:

| Agent | Role | Default Model |
|-------|------|---------------|
| `ConsolidatorAgent` | Merge findings, deduplicate, resolve conflicts | x-ai/grok-4.1-fast (OpenRouter) |
| `SkepticAgent` | Challenge findings, reduce false positives | x-ai/grok-4.1-fast (OpenRouter) |
| `ReviewerAgent` | Make pass/fail decision, generate report | x-ai/grok-4.1-fast (OpenRouter) |

## Configuration

Create `llm_audit_config.yaml`:

```yaml
# Pipeline settings
parallel_auditors: true
max_parallel: 5
enable_skeptic: true
require_reviewer_approval: true

# Default provider
default_provider: openrouter

# Provider configs
providers:
  openrouter:
    # API key from OPENROUTER_API_KEY env var
  local:
    base_url: http://localhost:8000/v1
    api_key: not-needed

# Agent overrides
agents:
  legal_auditor:
    enabled: true
    model: anthropic/claude-3.5-sonnet
    temperature: 0.1
    
  compliance_auditor:
    model: openai/gpt-4o
    
  # Disable an auditor
  financial_auditor:
    enabled: false
```

## CLI Commands

```bash
# Full audit with output report
llm-audit audit Company/ --output report.json

# Audit with specific focus areas
llm-audit audit *.md --focus "BSA,compliance"

# Quick single-file check
llm-audit check B1_Master_Operating_Agreement.md

# Skip skeptic challenge (faster but more false positives)
llm-audit audit Company/ --no-skeptic

# Auto-evaluate without reviewer (use thresholds)
llm-audit audit Company/ --no-reviewer

# Use custom config
llm-audit audit Company/ --config custom.yaml

# Verbose output with token usage
llm-audit audit Company/ -v
```

## Programmatic Usage

```python
import asyncio
from pathlib import Path
from llm_audit import AuditOrchestrator, OrchestratorConfig

async def main():
    # With default config
    orchestrator = AuditOrchestrator(
        schema_dir=Path("_schema")
    )
    
    # Audit single document
    result = await orchestrator.audit_document(
        Path("Company/Governance/B1_Master_Operating_Agreement.md")
    )
    
    print(f"Passed: {result.passed}")
    print(f"Findings: {len(result.findings)}")
    
    for finding in result.findings:
        print(f"  [{finding.severity.value}] {finding.description}")

asyncio.run(main())
```

## Finding Model

Each finding contains:

```python
AuditFinding(
    document_code="B1",
    section="3.2 Officer Duties",
    marker="[ROLE:ceo]",  # Optional
    severity=FindingSeverity.HIGH,
    category=FindingCategory.GOVERNANCE,
    description="Officer authority not clearly defined",
    evidence="The section states...",
    suggested_fix="Add specific authority limitations",
    reference="MCA 35-8-301",  # Optional
    confidence=0.85,
    requires_human_review=True,
)
```

## Output Report

```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "documents_audited": 5,
  "total_findings": 12,
  "passed": false,
  "statistics": {
    "severity_counts": {
      "critical": 0,
      "high": 3,
      "medium": 7,
      "low": 2
    }
  },
  "audits": [...]
}
```

## Environment Variables

The provider layer loads a `.env` file in this directory automatically (via `python-dotenv`), or you can export the variables directly.

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `LOCAL_LLM_BASE_URL` | Base URL for local vLLM/Ollama |
| `LOCAL_LLM_API_KEY` | API key for local instance (if needed) |

## Project Structure

```
llm_audit/
├── pyproject.toml          # Package configuration
├── README.md               # This file
├── llm_audit_config.yaml   # Default config
└── llm_audit/
    ├── __init__.py         # Package exports
    ├── cli.py              # Typer CLI commands
    ├── config.py           # Config loader
    ├── orchestrator.py     # Pipeline orchestration
    ├── providers.py        # LiteLLM wrapper
    ├── agents/
    │   ├── __init__.py
    │   ├── base.py         # BaseAuditor + 6 auditors
    │   └── pipeline.py     # Consolidator, Skeptic, Reviewer
    └── models/
        ├── __init__.py
        ├── agents.py       # AgentRole, AgentConfig, etc.
        └── findings.py     # AuditFinding, DocumentAudit, etc.
```

## License

Apache-2.0
