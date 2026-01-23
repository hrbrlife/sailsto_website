"""
Flows registry loader for [FLOW:*] markers.

Loads process flow IDs from flows/index.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class FlowEntry(RegistryEntry):
    """A process flow registry entry."""
    
    description: str = Field(default="", description="Flow description")
    file_path: str = Field(default="", description="Path to flow file")
    steps_count: int = Field(default=0, description="Number of steps in flow")


class FlowsRegistry(Registry[FlowEntry]):
    """Registry of process flow IDs."""
    
    marker_type: MarkerType = MarkerType.FLOW


class FlowsLoader(RegistryLoader):
    """
    Loader for flows/index.md.
    
    Extracts flow IDs from section headers and alias tables.
    
    Expected formats:
    - Section headers: ### flow_name
    - Alias table: | `Alias` | `canonical_name` |
    - [FLOW:name] markers
    """
    
    @property
    def marker_type(self) -> MarkerType:
        return MarkerType.FLOW
    
    @property
    def registry_filename(self) -> str:
        return "flows/index.md"
    
    def load(self) -> FlowsRegistry:
        """
        Load flows from flows/index.md.
        """
        content = self._read_file()
        entries: list[FlowEntry] = []
        seen_canonical: set[str] = set()
        aliases: dict[str, str] = {}  # alias -> canonical
        
        # Patterns for different formats
        patterns = {
            # Section header: ### flow_name
            "section": r'^###\s+([a-z_]+)\s*$',
            # Alias table row: | `Alias` | `canonical` |
            "alias_table": r'^\|\s*`([A-Za-z_]+)`\s*\|\s*`([a-z_]+)`\s*\|',
            # [FLOW:name] marker
            "marker": r'\[FLOW:([A-Za-z0-9_-]+)\]',
            # List item: - flow_name
            "list_item": r'^\s*[-*]\s+`?([a-z_]+)`?\s*(?:[-:]|$)',
        }
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            # Check section headers (primary canonical names)
            match = re.match(patterns["section"], line)
            if match:
                flow_name = match.group(1)
                if flow_name.lower() not in seen_canonical:
                    seen_canonical.add(flow_name.lower())
                    entries.append(FlowEntry(
                        id=flow_name,
                        source_line=line_num,
                    ))
                continue
            
            # Check alias table
            match = re.match(patterns["alias_table"], line)
            if match:
                alias = match.group(1)
                canonical = match.group(2)
                aliases[alias] = canonical
                
                # Ensure canonical exists
                if canonical.lower() not in seen_canonical:
                    seen_canonical.add(canonical.lower())
                    entries.append(FlowEntry(
                        id=canonical,
                        source_line=line_num,
                    ))
                continue
            
            # Check [FLOW:*] markers
            for match in re.finditer(patterns["marker"], line):
                flow_name = match.group(1)
                normalized = self._normalize_flow_name(flow_name)
                
                if normalized.lower() not in seen_canonical:
                    seen_canonical.add(normalized.lower())
                    entries.append(FlowEntry(
                        id=normalized,
                        source_line=line_num,
                        aliases=[flow_name] if flow_name != normalized else [],
                    ))
        
        # Add aliases to entries
        for alias, canonical in aliases.items():
            for entry in entries:
                if entry.id.lower() == canonical.lower():
                    if alias not in entry.aliases:
                        # Create new entry with updated aliases (entries are frozen)
                        idx = entries.index(entry)
                        entries[idx] = FlowEntry(
                            id=entry.id,
                            aliases=entry.aliases + [alias],
                            source_line=entry.source_line,
                            description=entry.description,
                            file_path=entry.file_path,
                            steps_count=entry.steps_count,
                        )
                    break
        
        return FlowsRegistry(
            marker_type=MarkerType.FLOW,
            source_file=str(self.registry_path),
            entries=entries,
        )
    
    def _normalize_flow_name(self, name: str) -> str:
        """
        Normalize flow name to snake_case canonical form.
        
        Args:
            name: Flow name (could be PascalCase, snake_case, etc.)
            
        Returns:
            Normalized snake_case name
        """
        # Convert PascalCase to snake_case
        result = re.sub(r'([A-Z])', r'_\1', name)
        result = result.lower().strip('_')
        
        # Clean up double underscores
        result = re.sub(r'_+', '_', result)
        
        return result


def load_flows_registry(schema_dir: Path) -> FlowsRegistry:
    """
    Convenience function to load flows registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated FlowsRegistry
    """
    loader = FlowsLoader(schema_dir)
    return loader.load()
