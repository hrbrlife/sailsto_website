"""
Test configuration for CCASH Validator tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def schema_dir() -> Path:
    """Get the schema directory path."""
    # Navigate from tests/ to _schema/
    test_dir = Path(__file__).parent
    return test_dir.parent.parent.parent  # ccash_validator -> validation -> _schema


@pytest.fixture
def patterns_file(schema_dir: Path) -> Path:
    """Get the patterns.yaml file path."""
    return schema_dir / "validation" / "patterns.yaml"


@pytest.fixture
def sample_content() -> str:
    """Sample document content for testing."""
    return '''# Sample Document

**Effective Date:** December 15, 2025
**Version:** 1.0

## Article 1: Definitions

The following [TERM:Company] definitions apply:

- [TERM:Client Series] means an independently registered MSB.
- [TERM:End Customer] means the customer of a Client Series.

## Article 2: References

See [DOC:B1] for the Master Operating Agreement.
See [DOC:F1 §5.2] for fee schedules.

## Article 3: Obligations

Per [OBL:REG-001], each Client must maintain independent MSB status.

## Article 4: Flows

The [FLOW:client_onboarding] process must be followed.
'''


@pytest.fixture
def prohibited_content() -> str:
    """Sample content with prohibited language."""
    return '''# Bad Document

**Effective Date:** December 15, 2025
**Version:** 1.0

This document describes our white-label solution for clients.
Clients can operate under our rent-a-license model.
'''


@pytest.fixture
def missing_metadata_content() -> str:
    """Sample content missing required metadata."""
    return '''# Document Without Metadata

This document is missing effective date and version.

## Section 1

Some content here.
'''
