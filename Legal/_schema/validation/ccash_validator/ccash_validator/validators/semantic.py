"""
Semantic validator for LLM-powered analysis.

Uses LLM for complex semantic checks that can't be done with regex.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from ccash_validator.models.enums import Severity, ValidationStatus
from ccash_validator.models.results import ValidationResult
from ccash_validator.validators.base import BaseValidator

if TYPE_CHECKING:
    from ccash_validator.models.config import PatternsConfig


class LLMProvider(Protocol):
    """Protocol for LLM providers."""
    
    def query(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Query the LLM with system and user prompts."""
        ...


class MockLLMProvider:
    """Mock LLM provider for testing."""
    
    def query(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Return a mock response."""
        return {
            "found": False,
            "confidence": 0.5,
            "evidence": None,
            "explanation": "Mock provider - no actual analysis performed",
        }


class AnthropicProvider:
    """Anthropic Claude LLM provider."""
    
    def __init__(self, api_key: str | None = None, model: str = "claude-3-haiku-20240307"):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("Anthropic API key required")
    
    def query(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Query Claude."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            
            # Parse response
            content = response.content[0].text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "found": False,
                    "confidence": 0.5,
                    "evidence": None,
                    "explanation": content,
                }
        except Exception as e:
            return {
                "found": False,
                "confidence": 0.0,
                "evidence": None,
                "explanation": f"Error: {e}",
            }


class OpenAIProvider:
    """OpenAI GPT LLM provider."""
    
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: API key (defaults to OPENAI_API_KEY env var)
            model: Model to use
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key required")
    
    def query(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Query GPT."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1024,
            )
            
            # Parse response
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "found": False,
                    "confidence": 0.5,
                    "evidence": None,
                    "explanation": content,
                }
        except Exception as e:
            return {
                "found": False,
                "confidence": 0.0,
                "evidence": None,
                "explanation": f"Error: {e}",
            }


def create_llm_provider(provider: str, api_key: str | None = None) -> LLMProvider:
    """
    Create an LLM provider instance.
    
    Args:
        provider: Provider name (mock, anthropic, openai)
        api_key: Optional API key
        
    Returns:
        LLM provider instance
    """
    if provider == "mock":
        return MockLLMProvider()
    elif provider == "anthropic":
        return AnthropicProvider(api_key)
    elif provider == "openai":
        return OpenAIProvider(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")


class SemanticValidator(BaseValidator):
    """
    Validator using LLM semantic analysis.
    
    Provides deeper analysis for checks that can't be done with regex alone.
    """
    
    def __init__(
        self, 
        config: PatternsConfig, 
        schema_dir: Path,
        llm_provider: str = "mock",
        api_key: str | None = None,
    ):
        """
        Initialize semantic validator.
        
        Args:
            config: Patterns configuration
            schema_dir: Path to _schema directory
            llm_provider: LLM provider name
            api_key: Optional API key
        """
        super().__init__(config, schema_dir)
        self.llm = create_llm_provider(llm_provider, api_key)
        self.llm_provider_name = llm_provider
    
    @property
    def name(self) -> str:
        return "Semantic Validator"
    
    @property
    def description(self) -> str:
        return f"LLM-powered semantic analysis ({self.llm_provider_name})"
    
    def validate(
        self,
        content: str,
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Run semantic validation checks.
        
        Args:
            content: Document content
            doc_code: Document code for filtering
            doc_path: Document path for context
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        
        # Check prohibited patterns with semantic fallback
        for check_name, config in self.config.prohibited.items():
            applies_to = config.applies_to
            if applies_to and doc_code and doc_code not in applies_to:
                continue
            
            llm_config = config.llm_semantic
            if llm_config and llm_config.enabled:
                result = self._semantic_check(
                    content,
                    check_name,
                    config.rule_id,
                    llm_config.prompt,
                    llm_config.min_confidence,
                    is_prohibited=True,
                )
                results.append(result)
        
        # Check required patterns with semantic fallback
        for check_name, config in self.config.required.items():
            applies_to = config.applies_to
            if applies_to and doc_code and doc_code not in applies_to:
                continue
            
            llm_config = config.llm_semantic
            if llm_config and llm_config.enabled:
                result = self._semantic_check(
                    content,
                    check_name,
                    config.rule_id,
                    llm_config.prompt,
                    llm_config.min_confidence,
                    is_prohibited=False,
                )
                results.append(result)
        
        return results
    
    def _semantic_check(
        self,
        content: str,
        check_name: str,
        rule_id: str,
        prompt: str,
        min_confidence: float,
        is_prohibited: bool,
    ) -> ValidationResult:
        """
        Run a single semantic check.
        
        Args:
            content: Document content
            check_name: Name of the check
            rule_id: Rule identifier
            prompt: LLM prompt
            min_confidence: Minimum confidence threshold
            is_prohibited: Whether this checks for prohibited (True) or required (False) content
            
        Returns:
            ValidationResult
        """
        system_prompt = """You are a legal document compliance analyzer.
Analyze the document and answer the question.
Respond ONLY with valid JSON in this format:
{"found": true/false, "confidence": 0.0-1.0, "evidence": "quote if found", "explanation": "brief reason"}"""
        
        # Truncate content to avoid token limits
        truncated = content[:12000] if len(content) > 12000 else content
        
        user_prompt = f"""Document:
{truncated}

Question:
{prompt}"""
        
        response = self.llm.query(system_prompt, user_prompt)
        
        found = response.get("found", False)
        confidence = response.get("confidence", 0.5)
        evidence = response.get("evidence")
        explanation = response.get("explanation", "")
        
        if is_prohibited:
            # For prohibited content, finding it is bad
            if found and confidence >= min_confidence:
                return ValidationResult(
                    rule_id=f"{rule_id}-LLM",
                    rule_name=f"{check_name}_semantic",
                    status=ValidationStatus.FAIL,
                    severity=Severity.WARNING,  # Downgrade to warning for LLM findings
                    message=f"LLM flagged possible {check_name}",
                    evidence=evidence,
                    confidence=confidence,
                    llm_assisted=True,
                )
            else:
                return ValidationResult(
                    rule_id=f"{rule_id}-LLM",
                    rule_name=f"{check_name}_semantic",
                    status=ValidationStatus.PASS,
                    severity=Severity.INFO,
                    message=f"LLM found no {check_name}",
                    confidence=1.0 - confidence,
                    llm_assisted=True,
                )
        else:
            # For required content, finding it is good
            if found and confidence >= min_confidence:
                return ValidationResult(
                    rule_id=f"{rule_id}-LLM",
                    rule_name=f"{check_name}_semantic",
                    status=ValidationStatus.PASS,
                    severity=Severity.INFO,
                    message=f"LLM verified {check_name}",
                    evidence=evidence,
                    confidence=confidence,
                    llm_assisted=True,
                )
            else:
                return ValidationResult(
                    rule_id=f"{rule_id}-LLM",
                    rule_name=f"{check_name}_semantic",
                    status=ValidationStatus.FAIL,
                    severity=Severity.WARNING,
                    message=f"LLM could not verify {check_name}",
                    confidence=1.0 - confidence,
                    llm_assisted=True,
                )
