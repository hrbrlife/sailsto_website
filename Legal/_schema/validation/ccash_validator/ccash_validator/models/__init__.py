"""
CCASH Validator Models

Type-safe data models for validation results, markers, and configuration.
"""

from ccash_validator.models.enums import Severity, ValidationStatus, MarkerType
from ccash_validator.models.markers import Marker, MarkerMatch, MarkerConfig
from ccash_validator.models.results import ValidationResult, DocumentValidation, ValidationSummary
from ccash_validator.models.config import (
    MetadataPatternConfig,
    ProhibitedPatternConfig,
    RequiredPatternConfig,
    LLMSemanticConfig,
    PatternsConfig,
)

__all__ = [
    # Enums
    "Severity",
    "ValidationStatus",
    "MarkerType",
    # Markers
    "Marker",
    "MarkerMatch",
    "MarkerConfig",
    # Results
    "ValidationResult",
    "DocumentValidation",
    "ValidationSummary",
    # Config
    "MetadataPatternConfig",
    "ProhibitedPatternConfig",
    "RequiredPatternConfig",
    "LLMSemanticConfig",
    "PatternsConfig",
]
