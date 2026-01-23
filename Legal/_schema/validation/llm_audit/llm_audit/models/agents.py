"""
Agent configuration and role models.

Defines the agent roles and their configurations for the audit system.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """
    Agent roles in the audit system.
    
    Derived from _schema/roles.md and legal document requirements.
    """
    
    # Specialist Auditors (run in parallel)
    LEGAL_AUDITOR = "legal_auditor"
    COMPLIANCE_AUDITOR = "compliance_auditor"
    TECHNICAL_AUDITOR = "technical_auditor"
    FINANCIAL_AUDITOR = "financial_auditor"
    DATA_PRIVACY_AUDITOR = "data_privacy_auditor"
    OPERATIONAL_AUDITOR = "operational_auditor"
    
    # Pipeline Agents (run sequentially after auditors)
    CONSOLIDATOR = "consolidator"
    SKEPTIC = "skeptic"
    REVIEWER = "reviewer"
    
    # Orchestration
    DISPATCHER = "dispatcher"
    
    # Summarization Agents (V2 pipeline)
    MASTER_SUMMARIZER = "master_summarizer"
    SUMMARY_GENERATOR = "summary_generator"
    
    @property
    def is_auditor(self) -> bool:
        """Whether this role is a parallel auditor."""
        return self in {
            AgentRole.LEGAL_AUDITOR,
            AgentRole.COMPLIANCE_AUDITOR,
            AgentRole.TECHNICAL_AUDITOR,
            AgentRole.FINANCIAL_AUDITOR,
            AgentRole.DATA_PRIVACY_AUDITOR,
            AgentRole.OPERATIONAL_AUDITOR,
        }
    
    @property
    def is_summarizer(self) -> bool:
        """Whether this role is a summarizer agent."""
        return self in {
            AgentRole.MASTER_SUMMARIZER,
            AgentRole.SUMMARY_GENERATOR,
        }
    
    @property
    def description(self) -> str:
        """Human-readable description of the role."""
        return {
            AgentRole.LEGAL_AUDITOR: "Reviews contract structure, cross-references, and Montana LLC law compliance",
            AgentRole.COMPLIANCE_AUDITOR: "Checks BSA/AML, FinCEN, MSB, and regulatory requirements",
            AgentRole.TECHNICAL_AUDITOR: "Validates marker syntax, schema conformance, and document structure",
            AgentRole.FINANCIAL_AUDITOR: "Audits capital requirements, insurance, fees, and financial obligations",
            AgentRole.DATA_PRIVACY_AUDITOR: "Reviews GDPR, CCPA, data handling, and consent provisions",
            AgentRole.OPERATIONAL_AUDITOR: "Checks officer duties, series separation, governance, and succession",
            AgentRole.CONSOLIDATOR: "Merges findings from all auditors, resolves conflicts, deduplicates",
            AgentRole.SKEPTIC: "Challenges consolidation, identifies gaps, stress-tests findings",
            AgentRole.REVIEWER: "Makes final approval decision, classifies severities, generates report",
            AgentRole.DISPATCHER: "Routes documents to appropriate auditors based on content",
            AgentRole.MASTER_SUMMARIZER: "Generates corpus-wide master summary from all documents",
            AgentRole.SUMMARY_GENERATOR: "Generates individual document summaries for context",
        }[self]
    
    @property
    def default_model(self) -> str:
        """Suggested default model for this role."""
        # Use Grok 4.1 fast for all agents via OpenRouter
        return "x-ai/grok-4.1-fast"


class AgentConfig(BaseModel):
    """
    Configuration for a single agent.
    
    Can be loaded from YAML config file.
    """
    
    role: AgentRole = Field(description="Agent role")
    
    # Model settings
    model: str = Field(
        default="",
        description="Model identifier (e.g., 'openrouter/anthropic/claude-3.5-sonnet')"
    )
    provider: str = Field(
        default="openrouter",
        description="Provider to use (openrouter, openai, local)"
    )
    temperature: float = Field(
        default=0.1,
        ge=0.0, le=2.0,
        description="Model temperature (lower = more deterministic)"
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum tokens in response"
    )
    
    # Prompts
    system_prompt_file: Optional[str] = Field(
        default=None,
        description="Path to system prompt markdown file"
    )
    system_prompt: str = Field(
        default="",
        description="Inline system prompt (overrides file if set)"
    )
    
    # Behavior
    enabled: bool = Field(
        default=True,
        description="Whether this agent is enabled"
    )
    timeout_seconds: int = Field(
        default=120,
        description="Timeout for agent execution"
    )
    retry_count: int = Field(
        default=2,
        description="Number of retries on failure"
    )
    
    # Output
    output_format: str = Field(
        default="json",
        description="Expected output format (json, markdown)"
    )
    
    model_config = {"extra": "allow"}
    
    def get_effective_model(self) -> str:
        """Get the model to use (configured or default)."""
        if self.model:
            return self.model
        return self.role.default_model
    
    def get_full_model_id(self) -> str:
        """Get full model ID with provider prefix for LiteLLM."""
        model = self.get_effective_model()
        
        # If already has openrouter/ prefix, use as-is
        if model.startswith("openrouter/"):
            return model
        
        # For OpenRouter provider, always add the prefix
        # OpenRouter model IDs look like: openrouter/x-ai/grok-4-fast
        # or openrouter/openai/gpt-4o-mini
        if self.provider == "openrouter":
            return f"openrouter/{model}"
        
        # If already has a known provider prefix for non-OpenRouter, use as-is
        known_prefixes = (
            "openai/",
            "anthropic/",
            "azure/",
            "vertex_ai/",
            "bedrock/",
            "ollama/",
            "huggingface/",
            "sagemaker/",
        )
        if any(model.startswith(prefix) for prefix in known_prefixes):
            return model
        
        # Add provider prefix for direct API calls
        if self.provider == "openai":
            return model  # OpenAI models don't need prefix
        elif self.provider == "local":
            return f"openai/{model}"  # Local vLLM uses OpenAI-compatible API
        
        return model


class AuditContext(BaseModel):
    """
    Context passed to agents during audit.
    
    Contains document content and schema context.
    """
    
    # Document being audited
    document_path: str = Field(description="Path to the document")
    document_name: str = Field(description="Document filename")
    document_code: Optional[str] = Field(default=None, description="Document code (e.g., 'B1')")
    document_content: str = Field(description="Full document content")
    
    # Schema context
    defined_terms: Optional[str] = Field(
        default=None,
        description="Content of defined_terms.md for reference"
    )
    obligations: Optional[str] = Field(
        default=None,
        description="Content of obligations.md for cross-checking"
    )
    decisions: Optional[str] = Field(
        default=None,
        description="Content of decisions_rights.md for cross-checking"
    )
    roles: Optional[str] = Field(
        default=None,
        description="Content of roles.md for role validation"
    )
    
    # Related documents (for cross-reference checking)
    related_docs: dict[str, str] = Field(
        default_factory=dict,
        description="Map of doc_code -> content for cross-references"
    )
    
    # Document metadata
    document_type: Optional[str] = Field(
        default=None,
        description="Type of document (governance, compliance, formation, etc.)"
    )
    
    # Audit scope
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Specific areas to focus on (empty = all)"
    )
    
    model_config = {"extra": "allow"}
    
    def get_context_summary(self) -> str:
        """Get a summary of available context for prompts."""
        available = []
        if self.defined_terms:
            available.append("defined_terms")
        if self.obligations:
            available.append("obligations")
        if self.decisions:
            available.append("decisions_rights")
        if self.roles:
            available.append("roles")
        if self.related_docs:
            available.append(f"related_docs ({len(self.related_docs)})")
        
        return f"Available context: {', '.join(available) if available else 'none'}"


class OrchestratorConfig(BaseModel):
    """
    Configuration for the audit orchestrator.
    """
    
    # Agent configs
    agents: dict[str, AgentConfig] = Field(
        default_factory=dict,
        description="Agent configurations by role name"
    )
    
    # Pipeline settings
    parallel_auditors: bool = Field(
        default=True,
        description="Run auditor agents in parallel"
    )
    max_parallel: int = Field(
        default=5,
        description="Maximum parallel agent executions"
    )
    
    # Consolidation settings
    enable_skeptic: bool = Field(
        default=True,
        description="Enable skeptic agent to challenge findings"
    )
    require_reviewer_approval: bool = Field(
        default=True,
        description="Require reviewer agent for final approval"
    )
    
    # Thresholds
    auto_pass_threshold: int = Field(
        default=0,
        description="Max finding count for auto-pass (0 = require review)"
    )
    critical_finding_blocks: bool = Field(
        default=True,
        description="Any CRITICAL finding blocks passing"
    )
    
    # Provider settings
    default_provider: str = Field(
        default="openrouter",
        description="Default LLM provider"
    )
    default_model: str = Field(
        default="x-ai/grok-4.1-fast",
        description="Default model for LLM calls"
    )
    providers: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Provider configurations (base_url, api_key, etc.)"
    )
    
    model_config = {"extra": "allow"}
    
    def get_agent_config(self, role: AgentRole) -> AgentConfig:
        """Get config for an agent role, with defaults."""
        if role.value in self.agents:
            config = self.agents[role.value]
            # Ensure role is set
            config.role = role
            return config
        
        # Return default config for this role
        return AgentConfig(
            role=role,
            provider=self.default_provider,
        )
    
    def get_enabled_auditors(self) -> list[AgentConfig]:
        """Get all enabled auditor agent configs."""
        configs = []
        for role in AgentRole:
            if role.is_auditor:
                config = self.get_agent_config(role)
                if config.enabled:
                    configs.append(config)
        return configs
