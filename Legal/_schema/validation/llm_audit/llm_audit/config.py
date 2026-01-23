"""
Configuration loader for LLM Audit system.

Loads and validates YAML configuration files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from pydantic import ValidationError

from llm_audit.models.agents import (
    AgentConfig,
    AgentRole,
    OrchestratorConfig,
)


class ConfigError(Exception):
    """Configuration loading or validation error."""
    
    def __init__(self, message: str, path: Optional[Path] = None):
        super().__init__(message)
        self.path = path


def load_yaml(path: Path) -> dict[str, Any]:
    """
    Load YAML file.
    
    Args:
        path: Path to YAML file
        
    Returns:
        Parsed YAML as dict
        
    Raises:
        ConfigError: If file cannot be loaded or parsed
    """
    try:
        import yaml
    except ImportError:
        raise ConfigError(
            "PyYAML is required for config loading. Install with: pip install pyyaml"
        )
    
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}", path)
    
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        return data or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {path}: {e}", path)


def load_config(path: Path) -> OrchestratorConfig:
    """
    Load orchestrator configuration from YAML file.
    
    The config file format:
    
    ```yaml
    parallel_auditors: true
    max_parallel: 5
    enable_skeptic: true
    require_reviewer_approval: true
    default_provider: openrouter
    
    providers:
      openrouter:
        api_key: ${OPENROUTER_API_KEY}  # env var expansion
      local:
        base_url: http://localhost:8000/v1
    
    agents:
      legal_auditor:
        enabled: true
        model: anthropic/claude-3.5-sonnet
        temperature: 0.1
      compliance_auditor:
        model: openai/gpt-4o
    ```
    
    Args:
        path: Path to YAML config file
        
    Returns:
        Validated OrchestratorConfig
        
    Raises:
        ConfigError: If config is invalid
    """
    import os
    
    data = load_yaml(path)
    
    # Expand environment variables in provider configs
    if "providers" in data:
        for provider_name, provider_config in data["providers"].items():
            if isinstance(provider_config, dict):
                for key, value in provider_config.items():
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]
                        provider_config[key] = os.environ.get(env_var, "")
    
    # Parse agent configs
    if "agents" in data:
        agents_raw = data["agents"]
        agents_parsed = {}
        
        for role_name, agent_data in agents_raw.items():
            try:
                # Find matching role
                role = AgentRole(role_name)
            except ValueError:
                raise ConfigError(
                    f"Unknown agent role: {role_name}. "
                    f"Valid roles: {[r.value for r in AgentRole]}",
                    path,
                )
            
            # Build agent config
            if isinstance(agent_data, dict):
                agent_data["role"] = role
                agents_parsed[role_name] = AgentConfig.model_validate(agent_data)
        
        data["agents"] = agents_parsed
    
    # Validate full config
    try:
        return OrchestratorConfig.model_validate(data)
    except ValidationError as e:
        raise ConfigError(f"Invalid configuration: {e}", path)


def load_config_or_default(
    path: Optional[Path] = None,
    search_paths: Optional[list[Path]] = None,
) -> OrchestratorConfig:
    """
    Load config from path, search paths, or return default.
    
    Search order:
    1. Explicit path if provided
    2. Search paths in order
    3. Default locations: ./llm_audit_config.yaml, ~/.config/llm_audit/config.yaml
    4. Return default config
    
    Args:
        path: Explicit config path
        search_paths: Additional paths to search
        
    Returns:
        Loaded or default OrchestratorConfig
    """
    # Check explicit path
    if path:
        if path.exists():
            return load_config(path)
        raise ConfigError(f"Config file not found: {path}", path)
    
    # Build search list
    paths_to_check = list(search_paths or [])
    paths_to_check.extend([
        Path("llm_audit_config.yaml"),
        Path("llm_audit.yaml"),
        Path(".llm_audit.yaml"),
        Path.home() / ".config" / "llm_audit" / "config.yaml",
    ])
    
    # Check each path
    for check_path in paths_to_check:
        if check_path.exists():
            return load_config(check_path)
    
    # Return default config
    return OrchestratorConfig()


def get_default_config_template() -> str:
    """
    Get default configuration as YAML string.
    
    Returns:
        YAML configuration template
    """
    template = """# LLM Audit Configuration
# Generated by llm-audit init-config

# Pipeline settings
parallel_auditors: true
max_parallel: 5
enable_skeptic: true
require_reviewer_approval: true
auto_pass_threshold: 0
critical_finding_blocks: true

# Default provider (openrouter, openai, local)
default_provider: openrouter

# Provider configurations
providers:
  openrouter:
    # Set OPENROUTER_API_KEY environment variable or .env
    api_key: ${OPENROUTER_API_KEY}
    
  openai:
    # Set OPENAI_API_KEY environment variable or .env
    api_key: ${OPENAI_API_KEY}
    
  anthropic:
    # Set ANTHROPIC_API_KEY environment variable or .env
    api_key: ${ANTHROPIC_API_KEY}
    
  local:
    # For local vLLM or Ollama instances
    base_url: http://localhost:8000/v1
    api_key: ${LOCAL_LLM_API_KEY}

# Agent configurations
agents:
  # Parallel auditors
  legal_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000
    timeout_seconds: 120
    
  compliance_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000
    
  technical_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.0
    max_tokens: 8000
    
  financial_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000
    
  data_privacy_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000
    
  operational_auditor:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000

  # Pipeline agents
  consolidator:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 12000
    
  skeptic:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.2
    max_tokens: 8000
    
  reviewer:
    enabled: true
    model: x-ai/grok-4.1-fast
    temperature: 0.1
    max_tokens: 8000
"""
    return template


def save_default_config(path: Path) -> None:
    """
    Save default configuration template to file.
    
    Args:
        path: Output path
    """
    template = get_default_config_template()
    path.write_text(template)
