"""
Models package for LLM Audit system.

Type-safe Pydantic models for audit findings and agent configuration.
"""

from llm_audit.models.findings import (
    AuditFinding,
    AuditReport,
    AgentAuditResult,
    ConsolidatedReport,
    AuditCategory,
    AuditSeverity,
)
from llm_audit.models.agents import (
    AgentRole,
    AgentConfig,
    AuditContext,
    OrchestratorConfig,
)

__all__ = [
    # Findings
    "AuditSeverity",
    "AuditCategory",
    "AuditFinding",
    "AgentAuditResult",
    "AuditReport",
    "ConsolidatedReport",
    # Agents
    "AgentRole",
    "AgentConfig",
    "AuditContext",
    "OrchestratorConfig",
]
