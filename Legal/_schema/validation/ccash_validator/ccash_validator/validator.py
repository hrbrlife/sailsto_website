"""
Main document validator for CCASH.

Orchestrates all validation checks on documents.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

from ccash_validator.config import ValidatorConfig, load_config
from ccash_validator.models.enums import MarkerType
from ccash_validator.models.results import DocumentValidation, ValidationResult, ValidationSummary
from ccash_validator.validators.markers import MarkerValidator
from ccash_validator.validators.metadata import MetadataValidator
from ccash_validator.validators.prohibited import ProhibitedValidator
from ccash_validator.validators.required import RequiredValidator
from ccash_validator.validators.semantic import SemanticValidator


class DocumentValidator:
    """
    Main validator orchestrating all document checks.
    
    Combines:
    - Metadata validation (effective date, version, placeholders)
    - Marker validation (TERM, DOC, OBL, FLOW, DECISION, RIGHT)
    - Prohibited language detection
    - Required language verification
    - Optional LLM semantic analysis
    """
    
    def __init__(
        self,
        config: ValidatorConfig | None = None,
        patterns_file: Path | str | None = None,
        enable_llm: bool = False,
        llm_provider: str = "mock",
        llm_api_key: str | None = None,
    ):
        """
        Initialize the document validator.
        
        Args:
            config: Pre-loaded configuration (takes precedence)
            patterns_file: Path to patterns.yaml (used if config not provided)
            enable_llm: Whether to enable LLM semantic analysis
            llm_provider: LLM provider name (mock, anthropic, openai)
            llm_api_key: API key for LLM provider
        """
        if config:
            self.config = config
        else:
            self.config = load_config(patterns_file)
        
        self.enable_llm = enable_llm
        self.llm_provider = llm_provider
        self.llm_api_key = llm_api_key
        
        # Initialize validators
        self._metadata_validator = MetadataValidator(
            self.config.config, self.config.schema_dir
        )
        self._marker_validator = MarkerValidator(
            self.config.config, self.config.schema_dir
        )
        self._prohibited_validator = ProhibitedValidator(
            self.config.config, self.config.schema_dir
        )
        self._required_validator = RequiredValidator(
            self.config.config, self.config.schema_dir
        )
        
        if enable_llm:
            self._semantic_validator = SemanticValidator(
                self.config.config, 
                self.config.schema_dir,
                llm_provider,
                llm_api_key,
            )
        else:
            self._semantic_validator = None
    
    def validate_document(
        self,
        doc_path: Path | str,
        checks: list[str] | None = None,
    ) -> DocumentValidation:
        """
        Validate a single document.
        
        Args:
            doc_path: Path to the document
            checks: Specific checks to run (metadata, markers, prohibited, required, semantic)
                   If None, runs all enabled checks.
                   
        Returns:
            DocumentValidation with all results
        """
        doc_path = Path(doc_path)
        
        # Read document content
        content = doc_path.read_text(encoding="utf-8")
        
        # Extract document code from filename
        doc_code = self._extract_doc_code(doc_path.name)
        
        # Collect all results
        results: list[ValidationResult] = []
        
        # Determine which checks to run
        if checks is None:
            checks = ["metadata", "markers", "prohibited", "required"]
            if self.enable_llm:
                checks.append("semantic")
        
        # Run validators
        if "metadata" in checks:
            results.extend(self._metadata_validator.validate(content, doc_code, str(doc_path)))
        
        if "markers" in checks:
            results.extend(self._marker_validator.validate(content, doc_code, str(doc_path)))
        
        if "prohibited" in checks:
            results.extend(self._prohibited_validator.validate(content, doc_code, str(doc_path)))
        
        if "required" in checks:
            results.extend(self._required_validator.validate(content, doc_code, str(doc_path)))
        
        if "semantic" in checks and self._semantic_validator:
            results.extend(self._semantic_validator.validate(content, doc_code, str(doc_path)))
        
        return DocumentValidation(
            document_path=str(doc_path),
            document_code=doc_code,
            results=results,
        )
    
    def validate_all(
        self,
        checks: list[str] | None = None,
    ) -> ValidationSummary:
        """
        Validate all documents in the workspace.
        
        Args:
            checks: Specific checks to run (passed to validate_document)
            
        Returns:
            ValidationSummary with all document results
        """
        summary = ValidationSummary(
            llm_enabled=self.enable_llm,
            llm_provider=self.llm_provider if self.enable_llm else None,
        )
        
        for doc_path in self.discover_documents():
            validation = self.validate_document(doc_path, checks)
            summary.add_document(validation)
        
        summary.complete()
        return summary
    
    def discover_documents(self) -> Iterator[Path]:
        """
        Discover all documents to validate.
        
        Yields:
            Paths to markdown documents
        """
        docs_dir = self.config.docs_dir
        
        # Detect layout mode
        if (docs_dir / "Company").exists() and (docs_dir / "Client_Series").exists():
            # Migrated layout
            subdirs = ["Company", "Client_Series", "Internal"]
            for subdir in subdirs:
                dir_path = docs_dir / subdir
                if dir_path.exists():
                    yield from dir_path.rglob("*.md")
        else:
            # Flat layout
            yield from docs_dir.glob("*.md")
    
    def _extract_doc_code(self, filename: str) -> str | None:
        """
        Extract document code from filename.
        
        Examples:
            - "B1_Master_Operating_Agreement.md" -> "B1"
            - "F1_Client_Services_Agreement.md" -> "F1"
            - "00_README.md" -> "00_README"
            
        Args:
            filename: Document filename
            
        Returns:
            Document code or None
        """
        # Remove .md extension
        name = filename.replace(".md", "")
        
        # Pattern for standard doc codes: A1, B1, B11, F1, N1, etc.
        match = re.match(r'^([A-Z][0-9]+[a-z]?)_', name)
        if match:
            return match.group(1)
        
        # Pattern for overview docs: 00_README, 00_Business_Model
        match = re.match(r'^(00_[A-Za-z_]+)', name)
        if match:
            return match.group(1)
        
        # Pattern for special docs: E1, E2, C1, etc.
        match = re.match(r'^([A-Z]+[0-9]+)_', name)
        if match:
            return match.group(1)
        
        # Fallback: use full name without extension
        return name if name else None
    
    def get_marker_registry(self, marker_type: MarkerType):
        """
        Get a marker registry for inspection.
        
        Args:
            marker_type: Type of marker
            
        Returns:
            Registry instance or None
        """
        return self._marker_validator.get_registry(marker_type)
