"""
Registry loaders for CCASH validation.

Type-safe loading of schema registries (terms, documents, obligations, etc.).
"""

from ccash_validator.registry.base import Registry, RegistryLoader
from ccash_validator.registry.terms import TermsRegistry
from ccash_validator.registry.documents import DocumentsRegistry
from ccash_validator.registry.obligations import ObligationsRegistry
from ccash_validator.registry.flows import FlowsRegistry
from ccash_validator.registry.decisions import DecisionsRegistry
from ccash_validator.registry.persons import PersonsRegistry, PersonEntry, load_persons_registry
from ccash_validator.registry.assignments import AssignmentsRegistry, EntityAssignment, load_assignments_registry

__all__ = [
    "Registry",
    "RegistryLoader",
    "TermsRegistry",
    "DocumentsRegistry",
    "ObligationsRegistry",
    "FlowsRegistry",
    "DecisionsRegistry",
    "PersonsRegistry",
    "PersonEntry",
    "load_persons_registry",
    "AssignmentsRegistry",
    "EntityAssignment",
    "load_assignments_registry",
]
