"""
Tests for the validators module.
"""

import pytest
from pathlib import Path

from ccash_validator.models.enums import ValidationStatus, Severity
from ccash_validator.models.config import (
    MetadataPatternConfig,
    ProhibitedPatternConfig,
    RequiredPatternConfig,
    PatternsConfig,
)
from ccash_validator.validators.metadata import MetadataValidator
from ccash_validator.validators.prohibited import ProhibitedValidator
from ccash_validator.validators.required import RequiredValidator


@pytest.fixture
def mock_config():
    """Create a minimal patterns config for testing."""
    return PatternsConfig(
        version="2.0",
        metadata={
            "effective_date": MetadataPatternConfig(
                description="Effective date",
                rule_id="BASE-001",
                patterns=[r'Effective Date:', r'effective_date:'],
                required=True,
                severity="ERROR",
            ),
            "version": MetadataPatternConfig(
                description="Version number",
                rule_id="BASE-002",
                patterns=[r'\*{0,2}Version:\*{0,2}\s*\d+\.\d+'],
                required=True,
                severity="WARNING",
            ),
            "placeholders": MetadataPatternConfig(
                description="Unfilled placeholders",
                rule_id="BASE-003",
                patterns=[r'\[_{2,}\]'],
                required=False,
                severity="WARNING",
                invert=True,
                count=True,
            ),
        },
        prohibited={
            "white_label": ProhibitedPatternConfig(
                description="Prohibited white-label",
                rule_id="MSB-001",
                patterns=[r'white[-\s]?label'],
                case_insensitive=True,
                severity="ERROR",
            ),
            "rent_a_license": ProhibitedPatternConfig(
                description="Prohibited rent-a-license",
                rule_id="MSB-002",
                patterns=[r'rent[-\s]?a[-\s]?license'],
                case_insensitive=True,
                severity="ERROR",
            ),
        },
        required={
            "independent_msb": RequiredPatternConfig(
                description="Independent MSB",
                rule_id="MSB-003",
                patterns=[r'independent.*MSB', r'independently\s+registered'],
                case_insensitive=True,
                severity="ERROR",
            ),
        },
    )


class TestMetadataValidator:
    """Tests for MetadataValidator."""
    
    def test_valid_metadata(self, mock_config, sample_content, tmp_path):
        """Test validation of content with valid metadata."""
        validator = MetadataValidator(mock_config, tmp_path)
        results = validator.validate(sample_content)
        
        # Should find effective date and version
        date_result = next(r for r in results if r.rule_id == "BASE-001")
        version_result = next(r for r in results if r.rule_id == "BASE-002")
        
        assert date_result.status == ValidationStatus.PASS
        assert version_result.status == ValidationStatus.PASS
    
    def test_missing_metadata(self, mock_config, missing_metadata_content, tmp_path):
        """Test validation of content missing metadata."""
        validator = MetadataValidator(mock_config, tmp_path)
        results = validator.validate(missing_metadata_content)
        
        date_result = next(r for r in results if r.rule_id == "BASE-001")
        version_result = next(r for r in results if r.rule_id == "BASE-002")
        
        assert date_result.status == ValidationStatus.FAIL
        assert date_result.severity == Severity.ERROR
        assert version_result.status == ValidationStatus.FAIL
    
    def test_placeholder_detection(self, mock_config, tmp_path):
        """Test detection of unfilled placeholders."""
        content = """
**Effective Date:** [____]
**Version:** 1.0

Client Name: [________________]
"""
        validator = MetadataValidator(mock_config, tmp_path)
        results = validator.validate(content)
        
        placeholder_result = next(r for r in results if r.rule_id == "BASE-003")
        assert placeholder_result.status == ValidationStatus.FAIL
        assert "2" in placeholder_result.message  # Found 2 placeholders


class TestProhibitedValidator:
    """Tests for ProhibitedValidator."""
    
    def test_clean_content(self, mock_config, sample_content, tmp_path):
        """Test validation of clean content."""
        validator = ProhibitedValidator(mock_config, tmp_path)
        results = validator.validate(sample_content)
        
        for result in results:
            assert result.status == ValidationStatus.PASS
    
    def test_prohibited_white_label(self, mock_config, prohibited_content, tmp_path):
        """Test detection of white-label language."""
        validator = ProhibitedValidator(mock_config, tmp_path)
        results = validator.validate(prohibited_content)
        
        white_label_result = next(r for r in results if r.rule_id == "MSB-001")
        assert white_label_result.status == ValidationStatus.FAIL
        assert white_label_result.severity == Severity.ERROR
        assert "white-label" in white_label_result.evidence.lower()
    
    def test_prohibited_rent_a_license(self, mock_config, prohibited_content, tmp_path):
        """Test detection of rent-a-license language."""
        validator = ProhibitedValidator(mock_config, tmp_path)
        results = validator.validate(prohibited_content)
        
        ral_result = next(r for r in results if r.rule_id == "MSB-002")
        assert ral_result.status == ValidationStatus.FAIL
        assert ral_result.evidence is not None
    
    def test_case_insensitive(self, mock_config, tmp_path):
        """Test case-insensitive matching."""
        content = "This is a WHITE-LABEL solution."
        validator = ProhibitedValidator(mock_config, tmp_path)
        results = validator.validate(content)
        
        white_label_result = next(r for r in results if r.rule_id == "MSB-001")
        assert white_label_result.status == ValidationStatus.FAIL


class TestRequiredValidator:
    """Tests for RequiredValidator."""
    
    def test_required_present(self, mock_config, tmp_path):
        """Test validation when required language is present."""
        content = """
Each client is an independently registered MSB.
They maintain their own FinCEN registration.
"""
        validator = RequiredValidator(mock_config, tmp_path)
        results = validator.validate(content)
        
        msb_result = next(r for r in results if r.rule_id == "MSB-003")
        assert msb_result.status == ValidationStatus.PASS
    
    def test_required_missing(self, mock_config, tmp_path):
        """Test validation when required language is missing."""
        content = """
Clients operate under our platform.
We handle all the regulatory requirements.
"""
        validator = RequiredValidator(mock_config, tmp_path)
        results = validator.validate(content)
        
        msb_result = next(r for r in results if r.rule_id == "MSB-003")
        assert msb_result.status == ValidationStatus.FAIL
    
    def test_applies_to_filtering(self, mock_config, tmp_path):
        """Test that applies_to filtering works."""
        # Add a rule that only applies to specific docs
        mock_config.required["test_rule"] = RequiredPatternConfig(
            description="Test",
            rule_id="TEST-001",
            patterns=[r'test pattern'],
            severity="ERROR",
            applies_to=["B1", "F1"],
        )
        
        validator = RequiredValidator(mock_config, tmp_path)
        
        # Should run for B1
        results = validator.validate("Some content", doc_code="B1")
        assert any(r.rule_id == "TEST-001" for r in results)
        
        # Should skip for A1
        results = validator.validate("Some content", doc_code="A1")
        assert not any(r.rule_id == "TEST-001" for r in results)
