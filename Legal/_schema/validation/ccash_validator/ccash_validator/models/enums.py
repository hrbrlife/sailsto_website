"""
Enumeration types for CCASH validation.
"""

from enum import Enum


class Severity(str, Enum):
    """Severity level for validation findings."""
    
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def emoji(self) -> str:
        """Return emoji representation."""
        return {
            Severity.ERROR: "❌",
            Severity.WARNING: "⚠️",
            Severity.INFO: "ℹ️",
        }[self]
    
    @property
    def color(self) -> str:
        """Return rich color name."""
        return {
            Severity.ERROR: "red",
            Severity.WARNING: "yellow",
            Severity.INFO: "blue",
        }[self]


class ValidationStatus(str, Enum):
    """Status of a validation check."""
    
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    UNCLEAR = "unclear"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def emoji(self) -> str:
        """Return emoji representation."""
        return {
            ValidationStatus.PASS: "✅",
            ValidationStatus.FAIL: "❌",
            ValidationStatus.SKIP: "⏭️",
            ValidationStatus.UNCLEAR: "❓",
        }[self]


class MarkerType(str, Enum):
    """Types of schema markers."""
    
    TERM = "TERM"
    DOC = "DOC"
    OBL = "OBL"
    FLOW = "FLOW"
    DECISION = "DECISION"
    RIGHT = "RIGHT"
    PERSON = "PERSON"
    ROLE = "ROLE"
    CONFIG = "CONFIG"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def registry_file(self) -> str:
        """Return the registry file for this marker type."""
        return {
            MarkerType.TERM: "defined_terms.md",
            MarkerType.DOC: "document_registry.md",
            MarkerType.OBL: "obligations.md",
            MarkerType.FLOW: "flows/index.md",
            MarkerType.DECISION: "decisions_rights.md",
            MarkerType.RIGHT: "decisions_rights.md",
            MarkerType.PERSON: "persons.md",
            MarkerType.ROLE: "assignments.md",
            MarkerType.CONFIG: "config.yaml",
        }[self]
    
    @property
    def description(self) -> str:
        """Return human-readable description."""
        return {
            MarkerType.TERM: "Defined Term",
            MarkerType.DOC: "Document Reference",
            MarkerType.OBL: "Obligation",
            MarkerType.FLOW: "Process Flow",
            MarkerType.DECISION: "Decision Right",
            MarkerType.RIGHT: "Stakeholder Right",
            MarkerType.PERSON: "Person Reference",
            MarkerType.ROLE: "Role Reference",
            MarkerType.CONFIG: "Configuration Value",
        }[self]
