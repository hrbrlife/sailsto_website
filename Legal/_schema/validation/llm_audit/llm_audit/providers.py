"""
LiteLLM provider abstraction layer.

Provides a unified interface for calling LLMs via LiteLLM,
with support for OpenRouter, OpenAI, and local vLLM instances.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env in the package directory or parent directories
    env_paths = [
        Path(__file__).parent.parent / ".env",  # llm_audit/.env
        Path(__file__).parent.parent.parent / ".env",  # validation/llm_audit/.env
        Path.cwd() / ".env",  # Current working directory
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # dotenv not installed, rely on system env vars

try:
    import litellm
    from litellm import acompletion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False
    litellm = None  # type: ignore
    acompletion = None  # type: ignore

from llm_audit.models.agents import AgentConfig


T = TypeVar("T", bound=BaseModel)


class ProviderError(Exception):
    """Error from LLM provider."""
    
    def __init__(
        self,
        message: str,
        provider: str = "unknown",
        model: str = "unknown",
        original_error: Optional[Exception] = None,
    ):
        super().__init__(message)
        self.provider = provider
        self.model = model
        self.original_error = original_error


class LLMProvider:
    """
    LiteLLM-based provider abstraction.
    
    Handles:
    - Multiple provider backends (OpenRouter, OpenAI, local)
    - Structured output parsing via Pydantic
    - Retry logic and error handling
    - Token tracking and logging
    
    Usage:
        provider = LLMProvider()
        
        # Simple completion
        response = await provider.complete(
            agent_config=config,
            messages=[{"role": "user", "content": "Hello"}],
        )
        
        # Structured output
        result = await provider.complete_structured(
            agent_config=config,
            messages=messages,
            response_model=AuditFinding,
        )
    """
    
    def __init__(
        self,
        provider_configs: Optional[dict[str, dict[str, Any]]] = None,
        verbose: bool = False,
    ):
        """
        Initialize provider.
        
        Args:
            provider_configs: Per-provider settings (base_url, api_key, etc.)
            verbose: Enable verbose logging
        """
        if not HAS_LITELLM:
            raise ImportError(
                "LiteLLM is required. Install with: pip install litellm"
            )
        
        self.provider_configs = provider_configs or {}
        self.verbose = verbose
        
        # Token tracking
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0
        
        # Configure LiteLLM
        self._setup_litellm()
    
    def _setup_litellm(self) -> None:
        """Configure LiteLLM settings."""
        # Suppress verbose output unless requested
        if not self.verbose:
            litellm.set_verbose = False  # type: ignore
        
        # Set API keys from environment or config
        if "openrouter" in self.provider_configs:
            config = self.provider_configs["openrouter"]
            if "api_key" in config:
                os.environ["OPENROUTER_API_KEY"] = config["api_key"]
        
        if "openai" in self.provider_configs:
            config = self.provider_configs["openai"]
            if "api_key" in config:
                os.environ["OPENAI_API_KEY"] = config["api_key"]
        
        if "anthropic" in self.provider_configs:
            config = self.provider_configs["anthropic"]
            if "api_key" in config:
                os.environ["ANTHROPIC_API_KEY"] = config["api_key"]
        
        if "local" in self.provider_configs:
            config = self.provider_configs["local"]
            if "base_url" in config:
                # Will be passed per-request for local provider
                pass
    
    def _get_completion_kwargs(
        self,
        agent_config: AgentConfig,
    ) -> dict[str, Any]:
        """Build kwargs for LiteLLM completion call."""
        model = agent_config.get_full_model_id()
        
        kwargs: dict[str, Any] = {
            "model": model,
            "temperature": agent_config.temperature,
            "max_tokens": agent_config.max_tokens,
            "timeout": agent_config.timeout_seconds,
        }
        
        # Provider-specific settings
        if agent_config.provider == "local":
            local_config = self.provider_configs.get("local", {})
            if "base_url" in local_config:
                kwargs["api_base"] = local_config["base_url"]
            if "api_key" in local_config:
                kwargs["api_key"] = local_config["api_key"]
        
        # OpenRouter-specific headers
        if agent_config.provider == "openrouter":
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://github.com/ccash",
                "X-Title": "CCASH Document Audit",
            }
        
        return kwargs
    
    async def complete(
        self,
        agent_config: AgentConfig,
        messages: list[dict[str, str]],
        system_prompt: Optional[str] = None,
        response_format: Optional[dict[str, str]] = None,
    ) -> str:
        """
        Get completion from LLM.
        
        Args:
            agent_config: Agent configuration
            messages: List of message dicts with role and content
            system_prompt: Optional system prompt (prepended to messages)
            response_format: Optional response format (e.g., {"type": "json_object"})
            
        Returns:
            Model response text
            
        Raises:
            ProviderError: On API or model errors
        """
        # Build message list
        full_messages = []
        
        # Add system prompt if provided
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        elif agent_config.system_prompt:
            full_messages.append({"role": "system", "content": agent_config.system_prompt})
        
        full_messages.extend(messages)
        
        # Get completion kwargs
        kwargs = self._get_completion_kwargs(agent_config)
        kwargs["messages"] = full_messages
        
        # Add response_format if specified (enables JSON mode)
        if response_format:
            kwargs["response_format"] = response_format
        
        # Attempt completion with retries
        last_error: Optional[Exception] = None
        
        for attempt in range(agent_config.retry_count + 1):
            try:
                response = await acompletion(**kwargs)
                
                # Track tokens
                if hasattr(response, "usage") and response.usage:
                    self.total_prompt_tokens += response.usage.prompt_tokens or 0
                    self.total_completion_tokens += response.usage.completion_tokens or 0
                
                # Extract response text
                content = response.choices[0].message.content
                return content or ""
                
            except Exception as e:
                last_error = e
                if attempt < agent_config.retry_count:
                    # Exponential backoff
                    await asyncio.sleep(2 ** attempt)
                    continue
                break
        
        raise ProviderError(
            message=f"LLM completion failed after {agent_config.retry_count + 1} attempts: {last_error}",
            provider=agent_config.provider,
            model=agent_config.get_full_model_id(),
            original_error=last_error,
        )
    
    async def complete_structured(
        self,
        agent_config: AgentConfig,
        messages: list[dict[str, str]],
        response_model: Type[T],
        system_prompt: Optional[str] = None,
    ) -> T:
        """
        Get structured output from LLM.
        
        Instructs the model to return JSON matching the Pydantic schema,
        then parses and validates the response.
        
        Args:
            agent_config: Agent configuration
            messages: List of message dicts
            response_model: Pydantic model class for response
            system_prompt: Optional system prompt
            
        Returns:
            Parsed Pydantic model instance
            
        Raises:
            ProviderError: On API errors or parse failures
        """
        # Build schema instruction
        schema = response_model.model_json_schema()
        schema_str = json.dumps(schema, indent=2)
        
        format_instruction = f"""
Respond with valid JSON matching this schema:
```json
{schema_str}
```

Return ONLY the JSON object, no additional text or markdown.
"""
        
        # Append format instruction to system prompt
        full_system = (system_prompt or agent_config.system_prompt or "")
        full_system = f"{full_system}\n\n{format_instruction}".strip()
        
        # Get completion
        response_text = await self.complete(
            agent_config=agent_config,
            messages=messages,
            system_prompt=full_system,
        )
        
        # Parse response
        try:
            # Handle markdown code blocks
            cleaned = response_text.strip()
            if cleaned.startswith("```"):
                # Remove code block markers
                lines = cleaned.split("\n")
                # Find first and last code block markers
                start_idx = 0
                end_idx = len(lines)
                for i, line in enumerate(lines):
                    if line.startswith("```") and i == 0:
                        start_idx = 1
                    elif line.startswith("```"):
                        end_idx = i
                        break
                cleaned = "\n".join(lines[start_idx:end_idx])
            
            data = json.loads(cleaned)
            return response_model.model_validate(data)
            
        except json.JSONDecodeError as e:
            raise ProviderError(
                message=f"Failed to parse JSON response: {e}",
                provider=agent_config.provider,
                model=agent_config.get_full_model_id(),
                original_error=e,
            )
        except Exception as e:
            raise ProviderError(
                message=f"Failed to validate response against schema: {e}",
                provider=agent_config.provider,
                model=agent_config.get_full_model_id(),
                original_error=e,
            )
    
    async def complete_list(
        self,
        agent_config: AgentConfig,
        messages: list[dict[str, str]],
        item_model: Type[T],
        system_prompt: Optional[str] = None,
    ) -> list[T]:
        """
        Get a list of structured items from LLM.
        
        Args:
            agent_config: Agent configuration
            messages: List of message dicts
            item_model: Pydantic model class for list items
            system_prompt: Optional system prompt
            
        Returns:
            List of parsed Pydantic model instances
        """
        # Build schema instruction for array response
        schema = item_model.model_json_schema()
        schema_str = json.dumps(schema, indent=2)
        
        format_instruction = f"""
Respond with a JSON array where each element matches this schema:
```json
{schema_str}
```

Return ONLY the JSON array, no additional text or markdown.
If there are no items, return an empty array: []
"""
        
        full_system = (system_prompt or agent_config.system_prompt or "")
        full_system = f"{full_system}\n\n{format_instruction}".strip()
        
        # Get completion
        response_text = await self.complete(
            agent_config=agent_config,
            messages=messages,
            system_prompt=full_system,
        )
        
        # Parse response
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                start_idx = 1 if lines[0].startswith("```") else 0
                end_idx = len(lines)
                for i, line in enumerate(lines):
                    if line.startswith("```") and i > 0:
                        end_idx = i
                        break
                cleaned = "\n".join(lines[start_idx:end_idx])
            
            data = json.loads(cleaned)
            
            if not isinstance(data, list):
                data = [data]
            
            return [item_model.model_validate(item) for item in data]
            
        except json.JSONDecodeError as e:
            raise ProviderError(
                message=f"Failed to parse JSON response: {e}",
                provider=agent_config.provider,
                model=agent_config.get_full_model_id(),
                original_error=e,
            )
    
    def get_usage_stats(self) -> dict[str, Any]:
        """Get token usage statistics."""
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "estimated_cost": self.total_cost,
        }
    
    def reset_usage(self) -> None:
        """Reset usage counters."""
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0


def create_provider_from_env() -> LLMProvider:
    """
    Create a provider using environment variables for configuration.
    
    Environment variables:
        OPENROUTER_API_KEY: OpenRouter API key
        OPENAI_API_KEY: OpenAI API key
        LOCAL_LLM_BASE_URL: Base URL for local vLLM instance
        
    Returns:
        Configured LLMProvider instance
    """
    configs: dict[str, dict[str, Any]] = {}
    
    if os.environ.get("OPENROUTER_API_KEY"):
        configs["openrouter"] = {
            "api_key": os.environ["OPENROUTER_API_KEY"],
        }
    
    if os.environ.get("OPENAI_API_KEY"):
        configs["openai"] = {
            "api_key": os.environ["OPENAI_API_KEY"],
        }
    
    if os.environ.get("ANTHROPIC_API_KEY"):
        configs["anthropic"] = {
            "api_key": os.environ["ANTHROPIC_API_KEY"],
        }
    
    if os.environ.get("LOCAL_LLM_BASE_URL"):
        configs["local"] = {
            "base_url": os.environ["LOCAL_LLM_BASE_URL"],
            "api_key": os.environ.get("LOCAL_LLM_API_KEY", "not-needed"),
        }
    
    return LLMProvider(provider_configs=configs)


# Global provider instance for convenience functions
_default_provider: Optional[LLMProvider] = None


def _get_default_provider() -> LLMProvider:
    """Get or create the default provider instance."""
    global _default_provider
    if _default_provider is None:
        _default_provider = create_provider_from_env()
    return _default_provider


async def make_completion(
    config: dict[str, Any],
    messages: list[dict[str, str]],
    response_format: Optional[dict[str, str]] = None,
) -> str:
    """
    Simple completion wrapper for KB relevance mapping.
    
    Args:
        config: Dict with 'model' and optionally 'provider' keys
        messages: List of message dicts with role and content
        response_format: Optional response format (e.g., {"type": "json_object"})
        
    Returns:
        Model response text
    """
    provider = _get_default_provider()
    
    # Build an AgentConfig from the dict
    model = config.get("model", "openai/gpt-4o-mini")
    provider_name = config.get("provider", "openrouter")
    
    # Create minimal agent config
    agent_config = AgentConfig(
        name="kb_relevance",
        model=model,
        provider=provider_name,
        temperature=config.get("temperature", 0.0),
        max_tokens=config.get("max_tokens", 4096),
        retry_count=config.get("retry_count", 2),
    )
    
    # Use the provider's complete method
    return await provider.complete(
        agent_config=agent_config,
        messages=messages,
        system_prompt=config.get("system_prompt"),
        response_format=response_format,
    )
