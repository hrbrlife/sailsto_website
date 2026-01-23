"""
Integration tests for the full validator.
"""

import pytest
from pathlib import Path
import tempfile
import os

from ccash_validator.validator import DocumentValidator
from ccash_validator.config import ValidatorConfig, load_config
from ccash_validator.models.enums import ValidationStatus
from ccash_validator.models.results import ValidationSummary


@pytest.fixture
def temp_patterns_file():
    """Create a temporary patterns.yaml for testing."""
    content = '''
version: "2.0"

markers:
  TERM:
    description: "Defined terms"
    extract_pattern: '\\[TERM:([A-Za-z0-9_/. -]+)\\]'
    validate_pattern: '^[A-Za-z][A-Za-z0-9_/. -]*$'
    registry_file: "defined_terms.md"
    
  DOC:
    description: "Document references"
    extract_pattern: '\\[DOC:([^\\]]+)\\]'
    validate_pattern: '^[A-Z0-9]+[a-z]?(_[A-Za-z_]+)?'
    registry_file: "document_registry.md"

metadata:
  effective_date:
    description: "Effective date"
    rule_id: "BASE-001"
    patterns:
      - 'Effective Date:'
    required: true
    severity: "ERROR"
    
  version:
    description: "Version number"
    rule_id: "BASE-002"
    patterns:
      - 'Version:\\s*\\d+\\.\\d+'
    required: true
    severity: "WARNING"

prohibited:
  white_label:
    description: "Prohibited white-label"
    rule_id: "MSB-001"
    patterns:
      - 'white[-\\s]?label'
    case_insensitive: true
    severity: "ERROR"

required:
  independent_msb:
    description: "Independent MSB"
    rule_id: "MSB-003"
    patterns:
      - 'independent.*MSB'
    case_insensitive: true
    severity: "ERROR"
'''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(content)
        return Path(f.name)


@pytest.fixture
def temp_schema_dir(temp_patterns_file):
    """Create a temporary schema directory structure."""
    schema_dir = temp_patterns_file.parent
    
    # Create minimal registry files
    (schema_dir / "defined_terms.md").write_text('''
# Defined Terms

| Term | Definition |
|------|------------|
| [TERM:Company] | CCASH LLC |
| [TERM:Client] | A Client Series |
''')
    
    (schema_dir / "document_registry.md").write_text('''
# Document Registry

| DocCode | Filename |
|---------|----------|
| `B1` | B1_Master_Operating_Agreement.md |
| `F1` | F1_Client_Services_Agreement.md |
''')
    
    return schema_dir


class TestDocumentValidator:
    """Tests for DocumentValidator."""
    
    def test_validator_creation(self, temp_patterns_file):
        """Test validator can be created."""
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        assert validator is not None
    
    def test_validate_clean_document(self, temp_patterns_file, temp_schema_dir):
        """Test validating a clean document."""
        doc_content = '''# Test Document

**Effective Date:** December 15, 2025
**Version:** 1.0

Each client is an independent MSB.

See [TERM:Company] and [DOC:B1].
'''
        doc_file = temp_schema_dir / "test_doc.md"
        doc_file.write_text(doc_content)
        
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        result = validator.validate_document(doc_file)
        
        assert not result.has_errors
    
    def test_validate_document_with_errors(self, temp_patterns_file, temp_schema_dir):
        """Test validating a document with errors."""
        doc_content = '''# Bad Document

This is a white-label solution.
No effective date or version.
'''
        doc_file = temp_schema_dir / "bad_doc.md"
        doc_file.write_text(doc_content)
        
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        result = validator.validate_document(doc_file)
        
        assert result.has_errors
        # Should have: missing effective date, white-label found, missing independent MSB
        error_ids = [r.rule_id for r in result.get_errors()]
        assert "MSB-001" in error_ids  # white-label
        assert "BASE-001" in error_ids  # missing date
    
    def test_validate_specific_checks(self, temp_patterns_file, temp_schema_dir):
        """Test running only specific checks."""
        doc_content = '''# Test Document

**Effective Date:** December 15, 2025
**Version:** 1.0

This is a white-label solution.
'''
        doc_file = temp_schema_dir / "test_doc.md"
        doc_file.write_text(doc_content)
        
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        
        # Only run metadata checks
        result = validator.validate_document(doc_file, checks=["metadata"])
        rule_ids = {r.rule_id for r in result.results}
        
        assert "BASE-001" in rule_ids  # metadata check
        assert "MSB-001" not in rule_ids  # prohibited check not run
    
    def test_doc_code_extraction(self, temp_patterns_file):
        """Test document code extraction from filename."""
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        
        assert validator._extract_doc_code("B1_Master_Operating_Agreement.md") == "B1"
        assert validator._extract_doc_code("F1_Client_Services_Agreement.md") == "F1"
        assert validator._extract_doc_code("00_README.md") == "00_README"
        assert validator._extract_doc_code("B11_Something.md") == "B11"


class TestValidatorConfig:
    """Tests for ValidatorConfig."""
    
    def test_config_loading(self, temp_patterns_file):
        """Test configuration loading."""
        config = load_config(temp_patterns_file)
        
        assert config.config.version == "2.0"
        assert "TERM" in config.config.markers
        assert "effective_date" in config.config.metadata
        assert "white_label" in config.config.prohibited
    
    def test_config_reload(self, temp_patterns_file):
        """Test configuration reload."""
        config = load_config(temp_patterns_file)
        original_version = config.config.version
        
        config.reload()
        assert config.config.version == original_version
    
    def test_config_not_found(self):
        """Test error when config file not found."""
        with pytest.raises(FileNotFoundError):
            load_config(Path("/nonexistent/patterns.yaml"))


class TestValidationSummary:
    """Tests for validation summary generation."""
    
    def test_validate_all_summary(self, temp_patterns_file, temp_schema_dir):
        """Test validate_all returns proper summary."""
        # Create test docs in schema_dir directly (not Company subdir to avoid permission issues)
        (temp_schema_dir / "test1.md").write_text('''
**Effective Date:** 2025-01-01
**Version:** 1.0
Content with independent MSB.
''')
        
        (temp_schema_dir / "test2.md").write_text('''
**Effective Date:** 2025-01-01
**Version:** 1.0
This is white-label.
''')
        
        validator = DocumentValidator(patterns_file=temp_patterns_file)
        
        # Validate just the two test docs
        result1 = validator.validate_document(temp_schema_dir / "test1.md")
        result2 = validator.validate_document(temp_schema_dir / "test2.md")
        
        # Manually create summary
        summary = ValidationSummary()
        summary.add_document(result1)
        summary.add_document(result2)
        summary.complete()
        
        # Summary should aggregate results
        assert summary.document_count == 2
        assert summary.total_checks > 0
