# Kimi K3 Rebuild Plan: Math-To-Manim as a K3 Agent Swarm

Status: DRAFT (July 16, 2026 - written on K3 launch day)

This document plans the full rebuild of the Math-To-Manim / KimiK2Manim concept
as a series of Kimi K3 agents, replacing the current K2-era 4-stage enrichment
pipeline. It is grounded in API research performed on launch day; items marked
UNCONFIRMED need verification against the live API before implementation.

## 1. Why now

- Kimi K3 launched July 16, 2026: `kimi-k3` on the OpenAI-compatible API at
  `https://api.moonshot.ai/v1` (platform docs rebranded to platform.kimi.ai).
- This repo's default model `kimi-k2-0905-preview` (config.py) belongs to the
  K2 series that was discontinued on May 25, 2026. The pipeline is running on
  a dead model ID; migration is mandatory regardless of the rebuild.
- K3 is explicitly agent-oriented (long-horizon agentic ability was the stated
  architecture goal), has a 1M-token context, always-on reasoning, and
  schema-constrained structured output - all of which map directly onto the
  weaknesses of the current chain (context loss between stages, JSON parsing
  fallbacks, shallow per-node reasoning).

## 2. K3 API facts the design relies on

Verified via official doc snippets and MoonshotAI GitHub (July 16, 2026):

| Fact | Value | Confidence |
|---|---|---|
| Model ID | `kimi-k3` | High |
| Endpoint | `https://api.moonshot.ai/v1`, existing MOONSHOT_API_KEY | Med (key validity UNCONFIRMED) |
| Context | 1,048,576 tokens, flat pricing | High |
| Max output | default 131,072; settable to 1M via `max_completion_tokens` | Med |
| Reasoning | always on; `reasoning_effort` top-level param, only `"max"` today | Med-High |
| Sampling | fixed: temperature 1.0, top_p 0.95 - do NOT send these params | Med-High |
| Streaming | separate `reasoning_content` and `content` deltas | Med-High |
| Tool calling | OpenAI-compatible; `tool_choice="required"` supported | Med-High |
| Structured output | `response_format` json_schema with `strict` mode | Med-High |
| Caching | automatic prefix caching, $0.30/M cache-hit input | Med-High |
| Pricing | $3.00/M input, $0.30/M cached, $15.00/M output | Med-High |
| Cheap workhorse | `kimi-k2.7-code` ($0.95/$4.00) for code-gen-heavy stages | Med |
| Open weights | claimed, NOT yet on Hugging Face | High (checked live) |

UNCONFIRMED and must be tested first: parallel tool calls, `tool_choice`
named-function mode, old API keys still valid post-rebrand, exact k2.6 pricing.

## 3. Tooling choice: Kimi Agent SDK vs Kosong

Three official options exist as of today:

1. **Kimi Agent SDK** (`pip install kimi-agent-sdk`,
   github.com/MoonshotAI/kimi-agent-sdk): programmatic access to the Kimi Code
   CLI agent runtime - sessions, streaming, tool approval, custom tools, MCP.
   Uses the CLI as the execution engine. This is the analogue of the Claude
   Agent SDK and is the requested target.
2. **Kosong** (already a dependency; now developed inside
   MoonshotAI/kimi-cli `packages/kosong`): lightweight LLM abstraction with
   `kosong.step()` tool orchestration. Good for single-agent loops, no
   multi-agent runtime.
3. **Raw OpenAI SDK** (current `kimi_client.py`): lowest-level, most control.

Decision: build the agent layer on the **Kimi Agent SDK** (per the project
goal), keep **Kosong** for in-process tool-loop stages where a full agent
session is overkill, and retire the bespoke `kimi_client.py` + `tool_adapter.py`
plumbing (K3's native structured output eliminates the fallback parser).

## 4. Target architecture: from pipeline to agent swarm

Current design (K2 era): one process, 4 sequential enrichment passes over a
KnowledgeNode tree, each pass making per-node chat calls with hand-rolled JSON
extraction.

Target design (K3 era): a supervisor agent orchestrating specialist agents,
each a K3 session with its own tools, communicating through typed artifacts
on disk rather than through a mutable in-memory tree.

### Agents

1. **Concept Scout** (kimi-k3, reasoning max)
   - Input: user concept string.
   - Replaces: prerequisite_explorer_kimi.py.
   - With 1M context, explores the FULL prerequisite graph in one session
     instead of depth-limited recursion; emits `knowledge_graph.json` via
     strict json_schema output (no fallback parsing).

2. **Mathematical Enricher** (kimi-k3)
   - Replaces Stage 2 of enrichment_chain.py.
   - Whole-graph enrichment in one context: LaTeX, definitions, examples,
     cross-references between nodes (impossible in the per-node K2 design).
   - Emits `math_enriched.json` (json_schema strict).

3. **Visual Designer** (kimi-k3, vision enabled)
   - Replaces Stage 3. Plans color, animation, camera per node.
   - New capability: consumes rendered still frames (base64) from previous
     runs for style continuity - K3 is natively multimodal.
   - Emits `visual_spec.json`.

4. **Narrative Composer** (kimi-k3)
   - Replaces Stage 4. Composes the long-form narrative prompt.
   - K3's 131K default output budget removes the 2000-word ceiling; target a
     full scene-by-scene screenplay.
   - Emits `narrative.md`.

5. **Manim Coder** (kimi-k2.7-code - cheaper, code-specialized)
   - NEW stage the K2 pipeline never had: turns narrative + visual spec into
     runnable Manim CE scenes.
   - Runs inside a Kimi Agent SDK session with file-write and shell tools so
     it can iterate: write scene, `manim --dry_run` / render low-quality,
     read tracebacks, fix.

6. **Render Critic** (kimi-k3, vision)
   - NEW: watches rendered preview frames, scores them against the visual
     spec, and either accepts or sends targeted fix instructions back to the
     Manim Coder. Loop until pass or budget exhausted.

7. **Supervisor** (thin Python, not a model)
   - Deterministic orchestration: sequencing, artifact validation against
     Pydantic schemas, retries, cost/budget accounting. Model-driven
     supervision is deferred until K3 parallel tool calling is confirmed.

### Key design shifts

- Per-node calls -> whole-graph single-context calls (1M window).
- JSON-in-text parsing + ToolAdapter fallback -> strict json_schema output.
- Fire-and-forget prompt generation -> closed-loop render/critique cycle.
- `temperature` tuning per stage -> removed entirely (fixed at 1.0 on K3);
  determinism must come from schemas and critics, not sampling.
- Prompt-prefix discipline: shared static system preamble across agents to
  exploit automatic caching (10x cheaper input on cache hits).

## 5. Repository refactor plan

Phase 0 - hygiene (DONE in part: repo cleanup commit, LICENSE):
- Untrack render caches and media, curate demo assets, fix packaging dupes.

Phase 1 - K3 client migration (no behavior change):
- config.py: default `KIMI_MODEL=kimi-k3`; add `KIMI_REASONING_EFFORT=max`;
  keep `KIMI_MODEL_CODE=kimi-k2.7-code` for the coder stage.
- kimi_client.py: strip temperature/top_p when the target model is `kimi-k3`;
  pass `reasoning_effort`; surface `reasoning_content` in streaming; delete
  the `KIMI_ENABLE_THINKING` toggle path (thinking cannot be disabled on K3).
- Live smoke test: `GET /v1/models` to confirm `kimi-k3` and key validity
  (resolves the UNCONFIRMED items).

Phase 2 - schema layer:
- New `schemas/` package: Pydantic models for KnowledgeGraph, MathEnrichment,
  VisualSpec, Narrative, SceneBundle; JSON-schema export for
  `response_format`. Retire tool_adapter.py.

Phase 3 - agent layer:
- New `k3_agents/` package: one module per agent above, built on
  kimi-agent-sdk sessions; supervisor.py for orchestration; artifacts/ for
  run outputs. Legacy `agents/` stays until parity is demonstrated.

Phase 4 - closed loop:
- Manim Coder + Render Critic loop with low-quality renders in the e2b
  sandbox (e2b_sandbox/ already exists in-repo for exactly this isolation).

Phase 5 - deprecation:
- Move `agents/`, `tool_adapter.py` to `legacy/`; update CLAUDE.md, README,
  examples to the K3 swarm; add pytest smoke tests gated on MOONSHOT_API_KEY.

## 6. Cost model (rough, per full run)

Assume graph exploration + enrichment ~200K input / 60K output on kimi-k3,
coder loop ~150K/80K on kimi-k2.7-code, critic 3 passes ~60K/10K:
- kimi-k3: 0.26M in x $3 + 0.07M out x $15 = ~$1.85 (much less with caching)
- k2.7-code: 0.15M x $0.95 + 0.08M x $4 = ~$0.46
- Total ~= $2-3 per animation at max reasoning; cacheable prefixes cut the
  input side by up to 10x on iterative runs.

## 7. Open questions blocking implementation start

1. Does the existing MOONSHOT_API_KEY authenticate against `kimi-k3`?
   (One live /v1/models call answers this - needs a key in .env.)
2. Parallel tool calls and named tool_choice on K3.
3. Kimi Agent SDK: does the Python package allow a custom base model per
   session (`kimi-k3` vs the Kimi Code `k3` alias), and does it require a
   Kimi Code subscription vs plain API billing? The SDK drives the Kimi Code
   CLI, whose provider endpoint (`api.kimi.com/coding/v1`) is
   subscription-gated; plain API-key usage needs the `type="kimi"` provider
   config pointed at api.moonshot.ai.
4. Findings from the Math-To-Manim upstream-architecture research (pending)
   may add stages worth porting (for example its reverse-knowledge-tree
   prompting or dual video/text output), to be folded in here.
