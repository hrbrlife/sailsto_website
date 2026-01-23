"""
CCASH Document Validator

A type-safe validation system for CCASH legal documentation.
"""

__version__ = "3.0.0"
__author__ = "CCASH LLC"

from ccash_validator.models import (
    Severity,
    ValidationStatus,
    ValidationResult,
    DocumentValidation,
    MarkerType,
    Marker,
)
from ccash_validator.config import ValidatorConfig
from ccash_validator.validator import DocumentValidator

__all__ = [
    # Models
    "Severity",
    "ValidationStatus", 
    "ValidationResult",
    "DocumentValidation",
    "MarkerType",
    "Marker",
    # Config
    "ValidatorConfig",
    # Validator
    "DocumentValidator",
]
