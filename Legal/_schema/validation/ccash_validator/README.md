# CCASH Document Validator

A type-safe, modern Python validation system for CCASH legal documentation.

## Features

- **Type-Safe Models**: Full Pydantic models with validation
- **Registry Validation**: Validates markers against schema registries
- **Pattern-Based Checks**: Metadata, prohibited language, required language
- **LLM Semantic Analysis**: Optional AI-powered semantic validation
- **Rich CLI**: Modern terminal output with colors and formatting
- **Extensible**: Easy to add new validators and patterns

## Installation

### From Source (Development)

```bash
cd _schema/validation/ccash_validator
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

pip install -e ".[dev]"
```

### With LLM Support

```bash
pip install -e ".[dev,llm]"
export ANTHROPIC_API_KEY="your-key"  # or OPENAI_API_KEY
```

## Usage

### Validate All Documents

```bash
ccash-validate --all
```

### Validate Single Document

```bash
ccash-validate path/to/document.md
```

### With LLM Semantic Analysis

```bash
ccash-validate --all --llm --llm-provider anthropic
```

### Output Formats

```bash
# Rich console output (default)
ccash-validate --all

# JSON output
ccash-validate --all --json

# Verbose with evidence
ccash-validate --all -v
```

### Specific Checks

```bash
# Only marker validation
ccash-validate --all --check markers

# Only prohibited language
ccash-validate --all --check prohibited

# Multiple checks
ccash-validate --all --check markers --check metadata
```

## Architecture

```
ccash_validator/
├── __init__.py          # Package exports
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── markers.py       # Marker type definitions
│   ├── results.py       # Validation result models
│   └── config.py        # Configuration models
├── registry/            # Registry loaders
│   ├── __init__.py
│   ├── base.py          # Abstract registry loader
│   ├── terms.py         # TERM registry
│   ├── documents.py     # DOC registry
│   ├── obligations.py   # OBL registry
│   ├── flows.py         # FLOW registry
│   └── decisions.py     # DECISION/RIGHT registry
├── validators/          # Validation logic
│   ├── __init__.py
│   ├── base.py          # Abstract validator
│   ├── metadata.py      # Metadata checks
│   ├── markers.py       # Marker syntax/registry
│   ├── prohibited.py    # Prohibited language
│   ├── required.py      # Required language
│   └── semantic.py      # LLM semantic checks
├── cli.py               # Typer CLI application
├── config.py            # Configuration loading
└── py.typed             # PEP 561 marker
```

## Configuration

The validator reads patterns from `patterns.yaml`:

```yaml
markers:
  TERM:
    extract_pattern: '\[TERM:([A-Za-z0-9_/. -]+)\]'
    validate_pattern: '^[A-Za-z][A-Za-z0-9_/. -]*$'
    registry_file: "defined_terms.md"
```

## Development

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy ccash_validator
```

### Linting

```bash
ruff check ccash_validator
```

## Migration from Bash Scripts

This package replaces:
- `validate.sh` → `ccash-validate` CLI
- `marker_audit.sh` → Built-in marker validation
- `hybrid_validator.py` → Modular validator classes

The same `patterns.yaml` configuration is used for backward compatibility.

## License

MIT License - CCASH LLC
