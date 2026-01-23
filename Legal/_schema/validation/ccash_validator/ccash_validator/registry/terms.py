"""
Terms registry loader for [TERM:*] markers.

Loads defined terms from defined_terms.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class TermEntry(RegistryEntry):
    """A defined term entry."""
    
    definition: str = Field(default="", description="Term definition text")
    source_doc: str | None = Field(default=None, description="Source document for the term")


class TermsRegistry(Registry[TermEntry]):
    """Registry of defined terms."""
    
    marker_type: MarkerType = MarkerType.TERM


class TermsLoader(RegistryLoader):
    """
    Loader for defined_terms.md registry.
    
    Extracts terms from [TERM:TermName] markers in the registry file.
    """
    
    @property
    def marker_type(self) -> MarkerType:
        return MarkerType.TERM
    
    @property
    def registry_filename(self) -> str:
        return "defined_terms.md"
    
    def load(self) -> TermsRegistry:
        """
        Load terms from defined_terms.md.
        
        The file format is expected to contain [TERM:Name] markers,
        typically in a table or definition list format.
        """
        content = self._read_file()
        entries: list[TermEntry] = []
        seen: set[str] = set()
        
        # Primary pattern: [TERM:TermName] anywhere
        term_pattern = r'\[TERM:([A-Za-z0-9_/. -]+)\]'
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            for match in re.finditer(term_pattern, line):
                term_name = match.group(1).strip()
                
                # Skip duplicates (keep first occurrence)
                if term_name.lower() in seen:
                    continue
                seen.add(term_name.lower())
                
                # Try to extract definition (text after the term marker)
                definition = ""
                if "|" in line:
                    # Table format: | [TERM:Name] | Definition |
                    parts = line.split("|")
                    if len(parts) >= 3:
                        definition = parts[2].strip()
                elif ":" in line and match.end() < len(line):
                    # Definition list format: [TERM:Name]: Definition
                    rest = line[match.end():].strip()
                    if rest.startswith(":"):
                        definition = rest[1:].strip()
                
                entries.append(TermEntry(
                    id=term_name,
                    source_line=line_num,
                    definition=definition,
                ))
        
        return TermsRegistry(
            marker_type=MarkerType.TERM,
            source_file=str(self.registry_path),
            entries=entries,
        )


def load_terms_registry(schema_dir: Path) -> TermsRegistry:
    """
    Convenience function to load terms registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated TermsRegistry
    """
    loader = TermsLoader(schema_dir)
    return loader.load()
