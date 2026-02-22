# Agentic AI Frameworks Comparison for Multi-Agent Testing Panel

> **Date:** 2026-02-22  
> **Purpose:** Select the best framework for building a "panel of expert agents" that analyze websites from multiple perspectives (legal, UX, SEO, editorial, etc.), hold a council, and produce a unified report — using OpenRouter as the LLM backend and Playwright for crawling.

---

## Framework Comparison Matrix

| Criteria | **CrewAI** | **AG2 (AutoGen)** | **LangGraph** | **OpenAI Agents SDK** | **Pydantic AI** | **Mastra** | **Smolagents** |
|---|---|---|---|---|---|---|---|
| **Language** | Python | Python | Python | Python | Python | TypeScript | Python |
| **GitHub Stars** | 44.4k | 4.2k | 24.9k | 19.1k | 15k | 21.3k | 25.5k |
| **License** | MIT | Apache 2.0 | MIT | MIT | MIT | Apache 2.0 | Apache 2.0 |
| **Latest Version** | 1.9.3 | 0.11.1 | 1.0.9 | 0.9.3 | 1.62.0 | 1.5.0 | 1.24.0 |
| **OpenRouter Support** | ✅ Native | ⚠️ Via config | ⚠️ Via LangChain | ⚠️ Via custom client | ✅ **First-class** | ✅ Native | ⚠️ Via LiteLLM |
| **Multi-Agent** | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good (handoffs) | ✅ Good | ✅ Good | ⚠️ Basic |
| **Tool Calling** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Structured Output** | ✅ Pydantic | ✅ Pydantic | ✅ Yes | ✅ Yes | ✅ **Best-in-class** | ✅ Zod | ✅ Yes |
| **Council/Committee** | ✅ Built-in | ✅ GroupChat | ⚠️ Manual graph | ⚠️ Manual orchestration | ⚠️ Manual | ⚠️ Workflows | ⚠️ ManagedAgent |
| **Maturity** | ✅ High | ✅ High | ✅ High | ⚠️ Medium | ✅ High | ⚠️ Medium | ⚠️ Medium |
| **Setup Complexity** | ✅ Low | ⚠️ Medium | ❌ High | ✅ Low | ✅ Low | ⚠️ Medium | ✅ Low |

---

## Detailed Analysis

### 1. CrewAI

**OpenRouter Integration:** Native support. CrewAI lists "Open Router" as a provider in its LLM configuration docs. Configure via:
```python
from crewai import LLM

llm = LLM(
    model="openrouter/anthropic/claude-sonnet-4-5",
    api_key="your-openrouter-key",
)
```
Or via environment variables: `MODEL=openrouter/anthropic/claude-sonnet-4-5` + `OPENROUTER_API_KEY`.

**Multi-Agent:** Best-in-class for the "panel of experts" pattern. CrewAI's entire metaphor is a "Crew" of role-playing agents with defined goals, backstories, and tasks. Supports `Process.sequential` and `Process.hierarchical` (with auto-assigned manager agent). The **Flows** system adds event-driven orchestration with `@start`, `@listen`, `@router` decorators for conditional branching.

**Tool Calling:** Full support. Custom tools via `@tool` decorator or built-in `crewai_tools` package. Easy to wrap Playwright as a tool.

**Structured Output:** Pydantic model output via `output_pydantic` on tasks and `response_format` on LLM.

**Council Pattern Feasibility:** **Excellent.** You can create a crew of expert agents (Legal Expert, UX Expert, SEO Analyst, etc.), run them sequentially or hierarchically, then feed all outputs into a "Council Lead" agent that synthesizes a unified report. The Flows system enables conditional routing based on confidence scores.

**Weaknesses:** Telemetry is on by default (disable with `OTEL_SDK_DISABLED=true`). CLI-centric project setup adds some overhead if you just want a script. Some users report inconsistent results with non-OpenAI models.

---

### 2. AG2 (formerly AutoGen)

**OpenRouter Integration:** Via OAI_CONFIG_LIST with custom `base_url`:
```json
[{
    "model": "anthropic/claude-sonnet-4-5",
    "api_key": "your-openrouter-key",
    "base_url": "https://openrouter.ai/api/v1"
}]
```

**Multi-Agent:** Very strong. Purpose-built for multi-agent conversations. Features `ConversableAgent`, `GroupChat` with `AutoPattern` for automatic agent selection, `UserProxyAgent` for human-in-the-loop. The `run_group_chat` pattern is close to a council pattern.

**Tool Calling:** Full support via `register_function()` with separate `caller` and `executor` agents.

**Structured Output:** Supported via Pydantic models.

**Council Pattern Feasibility:** **Good.** GroupChat with AutoPattern can orchestrate multiple specialist agents debating and refining. However, the conversation-centric model is better suited for iterative back-and-forth than structured sequential analysis + synthesis.

**Weaknesses:** Evolved from Microsoft's AutoGen — community fork has lower adoption (4.2k stars vs original). API has changed significantly between versions. More complex setup than CrewAI. The conversational paradigm can lead to excessive token usage as agents chat back and forth.

---

### 3. LangGraph

**OpenRouter Integration:** Via LangChain's `ChatOpenAI` with custom `base_url`:
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="anthropic/claude-sonnet-4-5",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key="your-openrouter-key",
)
```
OpenRouter officially lists LangChain integration in its docs.

**Multi-Agent:** Graph-based state machine approach. Very flexible but requires manual definition of nodes, edges, and state transitions. No built-in "crew" or "group chat" abstraction.

**Tool Calling:** Via LangChain tools ecosystem — extensive library available.

**Structured Output:** Supported through LangChain's structured output features.

**Council Pattern Feasibility:** **Possible but verbose.** You'd define each expert agent as a graph node, create a state schema to pass analysis results between nodes, and build a final synthesis node. Works well but requires significantly more boilerplate than CrewAI.

**Weaknesses:** Highest complexity ceiling. Tightly coupled to LangChain ecosystem. Requires understanding graph theory / state machine patterns. Overkill for a sequential expert panel → council synthesis workflow. The 36.1k "Used by" count reflects LangChain's broad adoption, not necessarily satisfaction.

---

### 4. OpenAI Agents SDK (formerly Swarm)

**OpenRouter Integration:** Via custom AsyncOpenAI client:
```python
from openai import AsyncOpenAI
from agents import set_default_openai_client, set_default_openai_api

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key",
)
set_default_openai_client(client)
set_default_openai_api("chat_completions")  # Required — Responses API is OpenAI-only
```
Also supports LiteLLM as an extension for 100+ models.

**Multi-Agent:** Agent-to-agent via **handoffs** (specialized tool calls that transfer control). Good for triage/routing patterns. Less natural for "all experts analyze independently, then synthesize."

**Tool Calling:** Excellent. `@function_tool` decorator with automatic schema generation. Clean, Pythonic API.

**Structured Output:** Via `output_type` on agents — uses OpenAI structured outputs.

**Council Pattern Feasibility:** **Moderate.** You'd need to manually orchestrate: run each expert agent independently, collect results, then pass them to a synthesizer agent. The handoff pattern is designed for sequential delegation, not parallel expert panels.

**Weaknesses:** Designed primarily for OpenAI's API — the Responses API and some features (tracing, sessions) only work with OpenAI. Using OpenRouter requires falling back to Chat Completions API and disabling OpenAI-specific tracing. Still at v0.9.3 — pre-1.0.

---

### 5. Pydantic AI ⭐

**OpenRouter Integration:** **First-class support.** Pydantic AI has a dedicated `OpenRouterProvider` and model class:
```python
from pydantic_ai import Agent

agent = Agent('openrouter:anthropic/claude-sonnet-4-5')
```
Or with explicit configuration:
```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    'anthropic/claude-sonnet-4-5',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key='your-openrouter-key',
    ),
)
agent = Agent(model)
```
OpenRouter is listed in Pydantic AI's official sidebar navigation and has its own docs page.

**Multi-Agent:** Supports multi-agent patterns with agent-to-agent delegation. Has a dedicated "Multi-Agent Patterns" docs page. Agents can call other agents as tools via dependency injection. The `pydantic_graph` module enables complex graph-based workflows.

**Tool Calling:** Superb. `@agent.tool` decorator with full type safety, dependency injection via `RunContext`, automatic Pydantic validation of tool arguments.

**Structured Output:** **Best-in-class.** Built by the Pydantic team. `output_type` parameter enforces Pydantic model responses with automatic validation and retry on validation failure. This is the framework's core strength.

**Council Pattern Feasibility:** **Good.** You'd create each expert as an `Agent` with `output_type` set to a structured analysis model, run them (potentially in parallel with `asyncio.gather`), then feed structured results into a Council agent. The strong typing ensures each expert's output is well-formed.

**Weaknesses:** Multi-agent orchestration is less opinionated than CrewAI — you handle the coordination yourself. No built-in "crew" or "group chat" abstraction. However, this gives you maximum control.

**Unique Strengths:** Type safety, observability via Logfire, built-in evals framework (`pydantic_evals`), MCP support, A2A protocol support, graph support, durable execution. The most "production-ready" foundation.

---

### 6. Mastra

**OpenRouter Integration:** Native. OpenRouter lists Mastra in its official framework integrations. Mastra connects to 40+ providers including OpenRouter through its model routing system.

**Multi-Agent:** Agents + graph-based workflows with `.then()`, `.branch()`, `.parallel()` syntax. Human-in-the-loop with suspend/resume.

**Tool Calling:** Full support with TypeScript tooling.

**Council Pattern Feasibility:** **Good** — but requires TypeScript. The workflow engine with `.parallel()` would work well for running multiple expert agents simultaneously, then synthesizing.

**Weaknesses:** **TypeScript only.** This is a dealbreaker if you want to use Playwright's Python bindings or integrate with Python-based analysis tools. Would require a separate Node.js process. v1.5.0, rapidly evolving API.

---

### 7. Smolagents (HuggingFace)

**OpenRouter Integration:** Via LiteLLM integration or OpenAI-compatible server config:
```python
from smolagents import LiteLLMModel, CodeAgent

model = LiteLLMModel(model_id="openrouter/anthropic/claude-sonnet-4-5")
agent = CodeAgent(tools=[...], model=model)
```
The README explicitly shows OpenRouter as an example provider.

**Multi-Agent:** Basic multi-agent via `ManagedAgent` hierarchy — a parent agent can delegate to child agents. Not as sophisticated as CrewAI or AG2 for committee/council patterns.

**Tool Calling:** Full support. Agents write actions as Python code (CodeAgent) or use standard tool calling (ToolCallingAgent).

**Structured Output:** Supported but not as strongly typed as Pydantic AI.

**Council Pattern Feasibility:** **Limited.** The managed agent pattern is hierarchical (boss → workers), not a peer council. You'd need significant custom orchestration.

**Weaknesses:** Designed for single-agent code generation with tool use. Multi-agent is secondary. The "smol" philosophy means less built-in orchestration infrastructure.

---

## Recommendation

### 🏆 TOP PICK: **Pydantic AI + Custom Orchestration**

For your specific use case — a panel of expert agents analyzing websites from different perspectives, with a council synthesis step, integrated with Playwright — **Pydantic AI** is the best choice. Here's why:

#### Why Pydantic AI wins:

1. **First-class OpenRouter support** — Dedicated `OpenRouterProvider`, documented in both Pydantic AI and OpenRouter docs. No hacks needed.

2. **Best structured output in the ecosystem** — Each expert agent can have a strongly-typed `output_type` (e.g., `LegalAnalysis`, `UXAnalysis`, `SEOAnalysis`). Pydantic validates outputs automatically and retries on validation failure. This is critical for a council pattern where expert outputs need to be reliably structured.

3. **Type safety throughout** — Full IDE autocomplete and static type checking. When building a complex multi-agent system, this prevents entire classes of bugs.

4. **Dependency injection** — Pass your Playwright browser context, screenshots, and page data to agents via `RunContext[Dependencies]`. Clean, testable architecture.

5. **Async-native** — Run all expert agents in parallel with `asyncio.gather()`, then feed results to the council agent. Massive speed improvement over sequential execution.

6. **Production-ready infrastructure** — Built-in evals (`pydantic_evals`), observability (Logfire), MCP support, durable execution. You can evaluate and iterate on agent quality systematically.

7. **Lightweight** — `pip install pydantic-ai` and you're running. No CLI scaffolding, no YAML configs, no project structure requirements.

8. **Graph support** — `pydantic_graph` module available for complex workflows if you need conditional routing between experts.

#### Why not CrewAI (runner-up):

CrewAI is the most natural fit conceptually — "Crew of expert agents" is literally its metaphor. However:
- OpenRouter support exists but is via LiteLLM proxy (less direct than Pydantic AI's native provider)
- Structured output is less robust (Pydantic AI is built *by* the Pydantic team)
- The CLI/YAML project scaffolding adds overhead for a custom integration
- Telemetry defaults and dependency weight are concerns
- Historically weaker with non-OpenAI models

**CrewAI is still a strong #2** and would be the pick if you prioritize minimal orchestration code over type safety and structured output quality.

---

### Recommended Architecture

```
┌─────────────────────────────────────────────────┐
│                ORCHESTRATOR                       │
│  (Python async script using Pydantic AI)          │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. CRAWL PHASE (Playwright)                      │
│     ├── Crawl all pages                           │
│     ├── Take screenshots                          │
│     ├── Extract HTML/meta/structured data          │
│     └── Store in CrawlResult (Pydantic model)     │
│                                                   │
│  2. EXPERT ANALYSIS PHASE (parallel)              │
│     ├── LegalAgent    → LegalAnalysis             │
│     ├── UXAgent       → UXAnalysis                │
│     ├── SEOAgent      → SEOAnalysis               │
│     ├── EditorialAgent→ EditorialAnalysis          │
│     ├── SecurityAgent → SecurityAnalysis           │
│     └── A11yAgent     → AccessibilityAnalysis      │
│     (all via asyncio.gather, each with output_type)│
│                                                   │
│  3. COUNCIL PHASE                                 │
│     ├── All analyses fed to CouncilAgent           │
│     ├── CouncilAgent output_type = UnifiedReport   │
│     └── Cross-references, prioritizes, synthesizes │
│                                                   │
│  4. OUTPUT                                        │
│     └── Markdown/JSON unified report               │
└─────────────────────────────────────────────────┘

All LLM calls via OpenRouter → choice of model per agent
```

### Minimal Code Sketch

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
import asyncio

# --- Structured output types ---
class LegalAnalysis(BaseModel):
    issues: list[str] = Field(description="Legal compliance issues found")
    severity: str = Field(description="Overall severity: low/medium/high/critical")
    recommendations: list[str]

class SEOAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    issues: list[str]
    recommendations: list[str]

class UnifiedReport(BaseModel):
    executive_summary: str
    critical_issues: list[str]
    analyses: dict[str, dict]
    priority_actions: list[str]

# --- Model setup (OpenRouter) ---
model = OpenAIChatModel(
    'anthropic/claude-sonnet-4-5',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key='your-openrouter-key',
    ),
)

# --- Expert agents ---
legal_agent = Agent(model, output_type=LegalAnalysis,
    instructions="You are a legal compliance expert. Analyze the website for GDPR, cookie consent, terms of service, privacy policy issues...")

seo_agent = Agent(model, output_type=SEOAnalysis,
    instructions="You are an SEO expert. Analyze meta tags, headings, content structure, mobile-friendliness...")

council_agent = Agent(model, output_type=UnifiedReport,
    instructions="You are a senior web consultant. Synthesize all expert analyses into a prioritized unified report...")

# --- Orchestration ---
async def analyze_website(crawl_data: str):
    # Run experts in parallel
    legal, seo = await asyncio.gather(
        legal_agent.run(f"Analyze this website:\n{crawl_data}"),
        seo_agent.run(f"Analyze this website:\n{crawl_data}"),
    )

    # Council synthesis
    council_input = f"""
    Legal Analysis: {legal.output.model_dump_json()}
    SEO Analysis: {seo.output.model_dump_json()}
    """
    report = await council_agent.run(council_input)
    return report.output
```

This gives you type-safe, parallel, structured multi-agent analysis with native OpenRouter support in ~50 lines of code.
