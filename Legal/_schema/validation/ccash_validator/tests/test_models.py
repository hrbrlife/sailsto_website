"""
Tests for the models module.
"""

import pytest
from datetime import datetime

from ccash_validator.models.enums import Severity, ValidationStatus, MarkerType
from ccash_validator.models.markers import Marker, MarkerMatch, MarkerConfig
from ccash_validator.models.results import ValidationResult, DocumentValidation, ValidationSummary


class TestSeverity:
    """Tests for Severity enum."""
    
    def test_severity_values(self):
        """Test severity enum values."""
        assert Severity.ERROR.value == "error"
        assert Severity.WARNING.value == "warning"
        assert Severity.INFO.value == "info"
    
    def test_severity_emoji(self):
        """Test severity emoji property."""
        assert Severity.ERROR.emoji == "❌"
        assert Severity.WARNING.emoji == "⚠️"
        assert Severity.INFO.emoji == "ℹ️"
    
    def test_severity_color(self):
        """Test severity color property."""
        assert Severity.ERROR.color == "red"
        assert Severity.WARNING.color == "yellow"
        assert Severity.INFO.color == "blue"


class TestValidationStatus:
    """Tests for ValidationStatus enum."""
    
    def test_status_values(self):
        """Test status enum values."""
        assert ValidationStatus.PASS.value == "pass"
        assert ValidationStatus.FAIL.value == "fail"
        assert ValidationStatus.SKIP.value == "skip"
        assert ValidationStatus.UNCLEAR.value == "unclear"


class TestMarkerType:
    """Tests for MarkerType enum."""
    
    def test_marker_types(self):
        """Test all marker types exist."""
        assert MarkerType.TERM.value == "TERM"
        assert MarkerType.DOC.value == "DOC"
        assert MarkerType.OBL.value == "OBL"
        assert MarkerType.FLOW.value == "FLOW"
        assert MarkerType.DECISION.value == "DECISION"
        assert MarkerType.RIGHT.value == "RIGHT"
    
    def test_registry_file(self):
        """Test registry file property."""
        assert MarkerType.TERM.registry_file == "defined_terms.md"
        assert MarkerType.DOC.registry_file == "document_registry.md"
        assert MarkerType.OBL.registry_file == "obligations.md"


class TestMarker:
    """Tests for Marker model."""
    
    def test_marker_creation(self):
        """Test basic marker creation."""
        marker = Marker(
            type=MarkerType.TERM,
            value="Company",
            line_number=10,
        )
        assert marker.type == MarkerType.TERM
        assert marker.value == "Company"
        assert marker.line_number == 10
    
    def test_marker_full_marker(self):
        """Test full_marker property."""
        marker = Marker(type=MarkerType.DOC, value="B1")
        assert marker.full_marker == "[DOC:B1]"
    
    def test_marker_validation_empty(self):
        """Test that empty value raises error."""
        with pytest.raises(ValueError):
            Marker(type=MarkerType.TERM, value="")
    
    def test_marker_normalize(self):
        """Test marker normalization."""
        marker = Marker(type=MarkerType.DOC, value="B1 §5.2")
        normalized = marker.normalize([
            {"pattern": r"§.*$", "replacement": ""},
            {"pattern": r"\s.*$", "replacement": ""},
        ])
        assert normalized == "B1"


class TestValidationResult:
    """Tests for ValidationResult model."""
    
    def test_result_creation(self):
        """Test basic result creation."""
        result = ValidationResult(
            rule_id="BASE-001",
            rule_name="effective_date",
            status=ValidationStatus.PASS,
            message="Found effective date",
        )
        assert result.rule_id == "BASE-001"
        assert result.is_passed
        assert not result.is_failed
    
    def test_result_fail(self):
        """Test failed result properties."""
        result = ValidationResult(
            rule_id="BASE-001",
            rule_name="effective_date",
            status=ValidationStatus.FAIL,
            severity=Severity.ERROR,
            message="Missing effective date",
        )
        assert result.is_failed
        assert result.is_error
        assert not result.is_warning
    
    def test_result_warning(self):
        """Test warning result properties."""
        result = ValidationResult(
            rule_id="BASE-002",
            rule_name="version",
            status=ValidationStatus.FAIL,
            severity=Severity.WARNING,
            message="Missing version",
        )
        assert result.is_failed
        assert result.is_warning
        assert not result.is_error
    
    def test_result_to_dict(self):
        """Test conversion to dictionary."""
        result = ValidationResult(
            rule_id="BASE-001",
            rule_name="test",
            status=ValidationStatus.PASS,
            message="Test passed",
        )
        data = result.to_dict()
        assert data["rule_id"] == "BASE-001"
        assert data["status"] == "pass"


class TestDocumentValidation:
    """Tests for DocumentValidation model."""
    
    def test_document_validation(self):
        """Test document validation aggregation."""
        results = [
            ValidationResult(
                rule_id="BASE-001",
                rule_name="test",
                status=ValidationStatus.PASS,
                message="Pass",
            ),
            ValidationResult(
                rule_id="BASE-002",
                rule_name="test",
                status=ValidationStatus.FAIL,
                severity=Severity.ERROR,
                message="Fail",
            ),
            ValidationResult(
                rule_id="BASE-003",
                rule_name="test",
                status=ValidationStatus.FAIL,
                severity=Severity.WARNING,
                message="Warning",
            ),
        ]
        
        validation = DocumentValidation(
            document_path="/path/to/doc.md",
            results=results,
        )
        
        assert validation.total_count == 3
        assert validation.passed_count == 1
        assert validation.error_count == 1
        assert validation.warning_count == 1
        assert validation.has_errors
        assert validation.has_warnings
        assert not validation.is_clean
    
    def test_document_name_extraction(self):
        """Test document name extraction from path."""
        validation = DocumentValidation(
            document_path="/path/to/B1_Master_Operating_Agreement.md",
            results=[],
        )
        assert validation.document_name == "B1_Master_Operating_Agreement.md"


class TestValidationSummary:
    """Tests for ValidationSummary model."""
    
    def test_summary_aggregation(self):
        """Test summary aggregation across documents."""
        summary = ValidationSummary()
        
        # Add document with errors
        summary.add_document(DocumentValidation(
            document_path="/doc1.md",
            results=[
                ValidationResult(
                    rule_id="R1",
                    rule_name="test",
                    status=ValidationStatus.FAIL,
                    severity=Severity.ERROR,
                    message="Error",
                ),
            ],
        ))
        
        # Add clean document
        summary.add_document(DocumentValidation(
            document_path="/doc2.md",
            results=[
                ValidationResult(
                    rule_id="R1",
                    rule_name="test",
                    status=ValidationStatus.PASS,
                    message="Pass",
                ),
            ],
        ))
        
        assert summary.document_count == 2
        assert summary.documents_with_errors == 1
        assert summary.documents_clean == 1
        assert summary.total_errors == 1
        assert not summary.is_passing
