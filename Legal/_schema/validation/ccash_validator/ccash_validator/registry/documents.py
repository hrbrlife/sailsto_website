"""
Documents registry loader for [DOC:*] markers.

Loads document codes from document_registry.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class DocumentEntry(RegistryEntry):
    """A document registry entry."""
    
    filename: str = Field(default="", description="Document filename")
    title: str = Field(default="", description="Document title")
    category: str = Field(default="", description="Document category")
    status: str = Field(default="", description="Document status")


class DocumentsRegistry(Registry[DocumentEntry]):
    """Registry of document codes."""
    
    marker_type: MarkerType = MarkerType.DOC


class DocumentsLoader(RegistryLoader):
    """
    Loader for document_registry.md.
    
    Extracts document codes from the registry table.
    Expected format: | `DocCode` | Filename | Title | Category | Status |
    """
    
    @property
    def marker_type(self) -> MarkerType:
        return MarkerType.DOC
    
    @property
    def registry_filename(self) -> str:
        return "document_registry.md"
    
    def load(self) -> DocumentsRegistry:
        """
        Load documents from document_registry.md.
        
        The file format is expected to be a markdown table with columns:
        | DocCode | Filename | Title | Category | Status |
        """
        content = self._read_file()
        entries: list[DocumentEntry] = []
        seen: set[str] = set()
        
        # Pattern for table rows: | `DocCode` | ... |
        # DocCode format: A1, B1, B11, F1, N1, 00_README, etc.
        row_pattern = r'^\|\s*`([A-Z0-9]+[a-z]?(_[A-Za-z_]+)?)`\s*\|(.+)$'
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            match = re.match(row_pattern, line)
            if match:
                doc_code = match.group(1)
                rest = match.group(3)
                
                # Skip duplicates
                if doc_code.lower() in seen:
                    continue
                seen.add(doc_code.lower())
                
                # Parse remaining columns
                columns = [c.strip() for c in rest.split("|")]
                
                filename = columns[0] if len(columns) > 0 else ""
                title = columns[1] if len(columns) > 1 else ""
                category = columns[2] if len(columns) > 2 else ""
                status = columns[3] if len(columns) > 3 else ""
                
                # Clean up values
                filename = filename.strip("`").strip()
                title = title.strip()
                category = category.strip()
                status = status.strip()
                
                entries.append(DocumentEntry(
                    id=doc_code,
                    source_line=line_num,
                    filename=filename,
                    title=title,
                    category=category,
                    status=status,
                ))
        
        return DocumentsRegistry(
            marker_type=MarkerType.DOC,
            source_file=str(self.registry_path),
            entries=entries,
        )
    
    def normalize_doc_ref(self, value: str) -> str:
        """
        Normalize a document reference for registry lookup.
        
        Strips section anchors, section references, and trailing text.
        
        Args:
            value: Raw DOC marker value (e.g., "B1 §5.2", "B1#section")
            
        Returns:
            Normalized document code (e.g., "B1")
        """
        result = value
        
        # Strip section anchor (#...)
        result = re.sub(r'#.*$', '', result)
        
        # Strip section reference (§...)
        result = re.sub(r'§.*$', '', result)
        
        # Strip trailing whitespace and text
        result = re.sub(r'\s.*$', '', result)
        
        return result.strip()


def load_documents_registry(schema_dir: Path) -> DocumentsRegistry:
    """
    Convenience function to load documents registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated DocumentsRegistry
    """
    loader = DocumentsLoader(schema_dir)
    return loader.load()
