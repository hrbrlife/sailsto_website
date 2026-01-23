"""
CCASH LLM Audit System

Multi-agent LLM audit system for CCASH legal documentation.
Uses Agent Squad patterns + LiteLLM for provider abstraction.
"""

__version__ = "2.0.0"

from llm_audit.models.findings import (
    AuditFinding,
    AgentAuditResult,
    AuditReport,
    ConsolidatedReport,
    AuditSeverity,
    AuditCategory,
)
from llm_audit.models.agents import (
    AgentRole,
    AgentConfig,
    AuditContext,
    OrchestratorConfig,
)
from llm_audit.integrated import IntegratedOrchestrator
from llm_audit.providers import LLMProvider, create_provider_from_env, ProviderError
from llm_audit.config import load_config, load_config_or_default, ConfigError

__all__ = [
    "__version__",
    # Findings
    "AuditFinding",
    "AgentAuditResult",
    "AuditReport",
    "ConsolidatedReport",
    "AuditSeverity",
    "AuditCategory",
    # Agents
    "AgentRole",
    "AgentConfig",
    "AuditContext",
    "OrchestratorConfig",
    # Core
    "IntegratedOrchestrator",
    "LLMProvider",
    "create_provider_from_env",
    "ProviderError",
    # Config
    "load_config",
    "load_config_or_default",
    "ConfigError",
]
