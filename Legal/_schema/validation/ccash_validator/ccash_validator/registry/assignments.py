"""
Role assignments registry loader for CCASH validation.

Parses assignments.md to load role assignment data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class RoleAssignment(BaseModel):
    """A single role assignment within an entity."""
    
    assignment_id: str = Field(default="", description="Assignment ID like ASN-001")
    role_type: str = Field(description="Role type from llc_roles.md")
    person_id: str = Field(description="Person ID from persons.md")
    person_name: str = Field(default="", description="Person name for display")
    title: Optional[str] = Field(default=None, description="Override title")
    abbreviation: Optional[str] = Field(default=None, description="Role abbreviation like CEO")
    effective_date: Optional[str] = Field(default=None, description="When role became effective")
    status: str = Field(default="active", description="active or inactive")
    notes: Optional[str] = Field(default=None, description="Assignment notes")
    ownership_percentage: Optional[int] = Field(default=None, description="For member roles")
    reports_to: Optional[str] = Field(default=None, description="Reports to which role")
    
    def get_field(self, field_path: str) -> str:
        """
        Get a field value by path.
        
        Args:
            field_path: Field name like 'ownership_percentage' or 'title'
            
        Returns:
            Field value as string, or empty string if not found
        """
        if hasattr(self, field_path):
            value = getattr(self, field_path)
            if value is not None:
                return str(value)
        return ""


class EntityAssignment(RegistryEntry):
    """Role assignments for an entity (company or series)."""
    
    entity_type: str = Field(default="company", description="company or series")
    entity_name: str = Field(default="", description="Full entity name")
    status: str = Field(default="active", description="active or inactive")
    formed_date: Optional[str] = Field(default=None, description="Formation date")
    roles: dict[str, RoleAssignment] = Field(default_factory=dict, description="Role type -> assignment")
    inherits_from: Optional[str] = Field(default=None, description="Entity to inherit roles from")
    
    model_config = {"frozen": False}
    
    def get_role(self, role_type: str) -> Optional[RoleAssignment]:
        """Get assignment for a specific role."""
        return self.roles.get(role_type)
    
    def get_person_for_role(self, role_type: str) -> Optional[str]:
        """Get person ID for a specific role."""
        assignment = self.roles.get(role_type)
        return assignment.person_id if assignment else None


class AssignmentsRegistry(Registry[EntityAssignment]):
    """Registry of entity role assignments."""
    
    marker_type: MarkerType = Field(default=MarkerType.ROLE)
    
    def get_entity(self, entity_id: str) -> Optional[EntityAssignment]:
        """Get assignments for a specific entity."""
        for entry in self.entries:
            if entry.id == entity_id:
                return entry
        return None
    
    def get_role_assignment(
        self, entity_id: str, role_type: str
    ) -> Optional[RoleAssignment]:
        """Get a specific role assignment."""
        entity = self.get_entity(entity_id)
        if entity:
            return entity.get_role(role_type)
        return None
    
    def get_person_for_role(
        self, entity_id: str, role_type: str
    ) -> Optional[str]:
        """Get the person ID assigned to a role."""
        assignment = self.get_role_assignment(entity_id, role_type)
        return assignment.person_id if assignment else None


def load_assignments_registry(schema_dir: Path) -> AssignmentsRegistry:
    """
    Load assignments registry from assignments.md.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        AssignmentsRegistry with all assignments loaded
    """
    assignments_file = schema_dir / "assignments.md"
    
    if not assignments_file.exists():
        return AssignmentsRegistry(
            marker_type=MarkerType.ROLE,
            source_file=str(assignments_file),
            entries=[],
        )
    
    content = assignments_file.read_text(encoding="utf-8")
    entries = _parse_assignments_md(content)
    
    return AssignmentsRegistry(
        marker_type=MarkerType.ROLE,
        source_file=str(assignments_file),
        entries=entries,
    )


def _parse_assignments_md(content: str) -> list[EntityAssignment]:
    """
    Parse assignments.md content into EntityAssignment objects.
    
    The file structure is:
    - ## Company Assignments / ## Series Assignments sections
    - ### Entity: <name> subsections
    - #### ASN-XXX: <role> sub-subsections with yaml blocks
    """
    entries = []
    
    # Find all YAML code blocks with assignment data
    yaml_pattern = re.compile(r'```yaml\n(.*?)```', re.DOTALL)
    
    # Track current entity context
    entity_assignments: dict[str, EntityAssignment] = {}
    
    # Find all assignment blocks (#### ASN-XXX: Role)
    # Extract entity_id from the YAML inside each block
    all_yaml_blocks = yaml_pattern.findall(content)
    
    for yaml_content in all_yaml_blocks:
        # Check if this is an entity definition block
        entity_id_match = re.search(r'^entity_id:\s*(\S+)', yaml_content, re.MULTILINE)
        entity_type_match = re.search(r'^entity_type:\s*(\S+)', yaml_content, re.MULTILINE)
        entity_name_match = re.search(r'^entity_name:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
        
        # Check if this is an assignment block
        assignment_id_match = re.search(r'^assignment_id:\s*(\S+)', yaml_content, re.MULTILINE)
        role_id_match = re.search(r'^role_id:\s*(\S+)', yaml_content, re.MULTILINE)
        person_id_match = re.search(r'^person_id:\s*(\S+)', yaml_content, re.MULTILINE)
        
        if entity_id_match and entity_type_match and not assignment_id_match:
            # This is an entity definition block
            entity_id = entity_id_match.group(1).lower()
            entity_type = entity_type_match.group(1)
            entity_name = entity_name_match.group(1).strip('"\'') if entity_name_match else ""
            
            formation_date_match = re.search(r'^formation_date:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            formation_date = formation_date_match.group(1).strip('"\'') if formation_date_match else None
            
            inherits_match = re.search(r'^inherits_from:\s*(\S+)', yaml_content, re.MULTILINE)
            inherits_from = inherits_match.group(1) if inherits_match else None
            
            if entity_id not in entity_assignments:
                entity_assignments[entity_id] = EntityAssignment(
                    id=entity_id,
                    entity_type=entity_type,
                    entity_name=entity_name,
                    formed_date=formation_date,
                    inherits_from=inherits_from,
                    roles={},
                    source_line=0,
                )
        
        elif assignment_id_match and role_id_match and person_id_match and entity_id_match:
            # This is an assignment block
            entity_id = entity_id_match.group(1).lower()
            assignment_id = assignment_id_match.group(1)
            role_id = role_id_match.group(1)
            person_id = person_id_match.group(1)
            
            person_name_match = re.search(r'^person_name:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            person_name = person_name_match.group(1).strip('"\'') if person_name_match else ""
            
            role_title_match = re.search(r'^role_title:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            role_title = role_title_match.group(1).strip('"\'') if role_title_match else None
            
            role_abbrev_match = re.search(r'^role_abbreviation:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            role_abbrev = role_abbrev_match.group(1).strip('"\'') if role_abbrev_match else None
            
            effective_match = re.search(r'^effective_date:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            effective_date = effective_match.group(1).strip('"\'') if effective_match else None
            
            status_match = re.search(r'^status:\s*(\S+)', yaml_content, re.MULTILINE)
            status = status_match.group(1) if status_match else "active"
            
            notes_match = re.search(r'^notes:\s*["\']?([^"\'\n]+)', yaml_content, re.MULTILINE)
            notes = notes_match.group(1).strip('"\'') if notes_match else None
            
            ownership_match = re.search(r'^ownership_percentage:\s*(\d+)', yaml_content, re.MULTILINE)
            ownership_pct = int(ownership_match.group(1)) if ownership_match else None
            
            reports_match = re.search(r'^reports_to:\s*(\S+)', yaml_content, re.MULTILINE)
            reports_to = reports_match.group(1) if reports_match else None
            
            # Ensure entity exists
            if entity_id not in entity_assignments:
                entity_assignments[entity_id] = EntityAssignment(
                    id=entity_id,
                    entity_type="company" if entity_id == "company" else "series",
                    roles={},
                    source_line=0,
                )
            
            # Add role assignment
            entity_assignments[entity_id].roles[role_id] = RoleAssignment(
                assignment_id=assignment_id,
                role_type=role_id,
                person_id=person_id,
                person_name=person_name,
                title=role_title,
                abbreviation=role_abbrev,
                effective_date=effective_date,
                status=status,
                notes=notes,
                ownership_percentage=ownership_pct,
                reports_to=reports_to,
            )
    
    return list(entity_assignments.values())
