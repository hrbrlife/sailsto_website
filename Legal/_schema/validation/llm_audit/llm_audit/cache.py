"""
Cache and state management for incremental audits.

Uses content hashes to track document changes and skip re-processing.
Stores all intermediate data for legal audit trail.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class DocumentState(BaseModel):
    """State tracking for a single document."""
    
    doc_code: str = Field(description="Document code (e.g., B1)")
    file_path: str = Field(description="Relative path to document")
    content_hash: str = Field(description="SHA256 of document content")
    last_modified: datetime = Field(description="File modification time")
    
    # Processing state
    summary_hash: Optional[str] = Field(default=None, description="Hash when summary was generated")
    summary_generated_at: Optional[datetime] = Field(default=None)
    
    validation_hash: Optional[str] = Field(default=None, description="Hash when validation ran")
    validation_ran_at: Optional[datetime] = Field(default=None)
    
    audit_hash: Optional[str] = Field(default=None, description="Hash when audit ran")
    audit_ran_at: Optional[datetime] = Field(default=None)
    
    def needs_summary(self) -> bool:
        """Check if document needs re-summarization."""
        return self.summary_hash != self.content_hash
    
    def needs_validation(self) -> bool:
        """Check if document needs re-validation."""
        return self.validation_hash != self.content_hash
    
    def needs_audit(self) -> bool:
        """Check if document needs re-audit."""
        return self.audit_hash != self.content_hash


class AuditCache(BaseModel):
    """
    Central cache for all audit state.
    
    Stored in OUTPUT/.audit_cache.json
    """
    
    version: str = Field(default="1.0")
    last_full_run: Optional[datetime] = Field(default=None)
    
    # Document states keyed by doc_code
    documents: dict[str, DocumentState] = Field(default_factory=dict)
    
    # Cached summaries keyed by doc_code
    summaries: dict[str, str] = Field(default_factory=dict)
    
    # Validation results keyed by doc_code
    validation_results: dict[str, dict[str, Any]] = Field(default_factory=dict)
    
    # Dependency graph
    dependency_graph: dict[str, dict[str, list[str]]] = Field(default_factory=dict)
    # Format: {"B1": {"references": ["F1", "B5"], "referenced_by": ["A3"]}}
    
    def get_document(self, doc_code: str) -> Optional[DocumentState]:
        """Get document state by code."""
        return self.documents.get(doc_code)
    
    def update_document_hash(self, doc_code: str, file_path: str, content: str) -> DocumentState:
        """Update or create document state with new hash."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        if doc_code in self.documents:
            doc = self.documents[doc_code]
            doc.content_hash = content_hash
            doc.last_modified = datetime.utcnow()
        else:
            doc = DocumentState(
                doc_code=doc_code,
                file_path=file_path,
                content_hash=content_hash,
                last_modified=datetime.utcnow(),
            )
            self.documents[doc_code] = doc
        
        return doc
    
    def mark_summary_done(self, doc_code: str, summary: str) -> None:
        """Mark summary as generated for current content hash."""
        if doc_code in self.documents:
            doc = self.documents[doc_code]
            doc.summary_hash = doc.content_hash
            doc.summary_generated_at = datetime.utcnow()
            self.summaries[doc_code] = summary
    
    def mark_validation_done(self, doc_code: str, results: dict[str, Any]) -> None:
        """Mark validation as done for current content hash."""
        if doc_code in self.documents:
            doc = self.documents[doc_code]
            doc.validation_hash = doc.content_hash
            doc.validation_ran_at = datetime.utcnow()
            self.validation_results[doc_code] = results
    
    def mark_audit_done(self, doc_code: str) -> None:
        """Mark audit as done for current content hash."""
        if doc_code in self.documents:
            doc = self.documents[doc_code]
            doc.audit_hash = doc.content_hash
            doc.audit_ran_at = datetime.utcnow()
    
    def get_documents_needing_summary(self) -> list[str]:
        """Get list of doc_codes needing re-summarization."""
        return [code for code, doc in self.documents.items() if doc.needs_summary()]
    
    def get_documents_needing_validation(self) -> list[str]:
        """Get list of doc_codes needing re-validation."""
        return [code for code, doc in self.documents.items() if doc.needs_validation()]
    
    def get_documents_needing_audit(self) -> list[str]:
        """Get list of doc_codes needing re-audit."""
        return [code for code, doc in self.documents.items() if doc.needs_audit()]
    
    def get_related_documents(self, doc_code: str) -> tuple[list[str], list[str]]:
        """
        Get documents related to the given document.
        
        Returns:
            Tuple of (references, referenced_by)
        """
        if doc_code not in self.dependency_graph:
            return [], []
        
        graph = self.dependency_graph[doc_code]
        return graph.get("references", []), graph.get("referenced_by", [])


class CacheManager:
    """
    Manages cache persistence and operations.
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize cache manager.
        
        Args:
            output_dir: Path to OUTPUT directory
        """
        self.output_dir = output_dir
        self.cache_file = output_dir / ".audit_cache.json"
        self._cache: Optional[AuditCache] = None
    
    @property
    def cache(self) -> AuditCache:
        """Get or load cache."""
        if self._cache is None:
            self._cache = self.load()
        return self._cache
    
    def load(self) -> AuditCache:
        """Load cache from disk or create new."""
        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text())
                return AuditCache.model_validate(data)
            except Exception:
                # Corrupted cache, start fresh
                return AuditCache()
        return AuditCache()
    
    def save(self) -> None:
        """Save cache to disk."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            self.cache.model_dump_json(indent=2)
        )
    
    def reset(self) -> None:
        """Clear all cache data."""
        self._cache = AuditCache()
        if self.cache_file.exists():
            self.cache_file.unlink()


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 hash of file content."""
    content = file_path.read_text(encoding="utf-8")
    return hashlib.sha256(content.encode()).hexdigest()
