# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication Style

- **Never use emojis** in any responses, code, or documentation unless explicitly requested by the user

## Development Commands

### Package Management (UV)

```bash
# Install Python 3.13+ and dependencies
uv python install 3.13
uv sync

# Run Python scripts with uv
uv run python script.py

# Run with specific Python version
uv run --python 3.13 python script.py
```

### Testing

```bash
# Run all tests (requires MOONSHOT_API_KEY)
pytest examples/ -v

# Run specific test file
uv run python examples/test_kimi_integration.py
uv run python examples/test_qft_pipeline.py
```

### Manim Rendering

```bash
# Preview quality (-pql)
manim -pql manim_scenes/harmonic_theorem.py HarmonicDivisionTheorem

# High quality (-pqh)
manim -pqh manim_scenes/epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron

# List all scenes in a file
manim -pql manim_scenes/SlowFastNetwork.py --list_scenes
```

### Environment Setup

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add:
# MOONSHOT_API_KEY=sk-your-key-here
# KIMI_ENABLE_THINKING=heavy
# KIMI_USE_TOOLS=true
```

## High-Level Architecture

### K3 Agent Swarm (current)

The current pipeline is [k3_agents/](k3_agents/): six specialist agents, all
running on `kimi-k3`, exchanging strict
json_schema artifacts defined in [schemas/artifacts.py](schemas/artifacts.py),
orchestrated by a deterministic [supervisor](k3_agents/supervisor.py) that
renders with Manim and drives a coder/critic repair loop.

```bash
uv run python -m k3_agents.supervisor "your concept here"
```

K3 API notes (differ from K2):
- temperature/top_p are fixed server-side on kimi-k3; the client strips them
- thinking is always on; effort via KIMI_REASONING_EFFORT (only "max" today)
- structured output via response_format json_schema strict mode
- responses may include reasoning_content alongside content

### Legacy: 4-Stage Agent Pipeline (K2 era)

KimiK2Manim uses a sequential enrichment pipeline where each agent progressively enhances a `KnowledgeNode` tree:

**Stage 1: Prerequisite Explorer** ([agents/prerequisite_explorer_kimi.py](agents/prerequisite_explorer_kimi.py))

- **Input**: Concept string (e.g., "pythagorean theorem")
- **Output**: Knowledge tree with prerequisite structure
- **Process**: Recursively identifies and structures prerequisite concepts
- **Tool**: Uses Kimi K2's thinking mode to identify prerequisites

**Stage 2: Mathematical Enricher** ([agents/enrichment_chain.py](agents/enrichment_chain.py))

- **Input**: Knowledge tree from Stage 1
- **Output**: Math-enriched tree
- **Process**: Adds LaTeX equations, definitions, examples to each node
- **Tool**: `write_mathematical_content` function call returns structured JSON

**Stage 3: Visual Designer** ([agents/enrichment_chain.py](agents/enrichment_chain.py))

- **Input**: Math-enriched tree from Stage 2
- **Output**: Visual-enriched tree with Manim specifications
- **Process**: Plans colors, animations, transitions, camera movements
- **Tool**: `design_visual_plan` function call returns structured visual specs

**Stage 4: Narrative Composer** ([agents/enrichment_chain.py](agents/enrichment_chain.py))

- **Input**: Fully enriched tree from Stage 3
- **Output**: Complete 2000+ word narrative prompt
- **Process**: Composes single continuous narrative integrating all enrichments
- **Tool**: `compose_narrative` function call returns verbose prompt

### Progressive Enrichment Pattern

The `KnowledgeNode` data structure accumulates fields at each stage:

```python
# Initial tree (Stage 1)
KnowledgeNode(
    concept="pythagorean theorem",
    depth=0,
    prerequisites=[...]
)

# After Stage 2 (Math)
node.equations = ["a²+b²=c²", ...]
node.definitions = {"a": "leg length", ...}

# After Stage 3 (Visual)
node.visual_spec = {
    "color_scheme": "Blue, green, red",
    "animation_description": "Triangle draws itself...",
    "duration": 15
}

# After Stage 4 (Narrative)
node.narrative = "2000+ word prompt..."
```

Each agent processes the tree recursively, ensuring all prerequisite nodes are enriched before the target concept.

### API Client Architecture

**KimiClient** ([kimi_client.py](kimi_client.py))

- Wraps OpenAI Python SDK with Moonshot AI endpoint
- Base URL: `https://api.moonshot.ai/v1`
- Model: `kimi-k3` (configurable via `KIMI_MODEL`)
- Supports OpenAI-compatible tool calling (function calling)
- Handles authentication and error formatting

**ToolAdapter** ([tool_adapter.py](tool_adapter.py))

- Converts OpenAI-style tool definitions to verbose natural language instructions
- Fallback mechanism when API doesn't support function calling
- Enables same agent code to work with or without tool support

### Tool Calling Flow

All enrichment agents use this pattern:

```python
# 1. Define tool schema
TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_mathematical_content",
        "parameters": {...}
    }
}

# 2. Call API with tool definition
response = client.chat_completion(
    messages=[{"role": "user", "content": prompt}],
    tools=[TOOL_SCHEMA],
    tool_choice="auto"
)

# 3. Extract structured data from tool call
payload = response["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
data = json.loads(payload)

# 4. Fallback to text parsing if no tool call
if not tool_calls:
    data = _parse_json_fallback(response_text)
```

## Configuration

All configuration in [config.py](config.py) and `.env`:

**Authentication** (default: subscription, no API key):

- `KIMI_AUTH_MODE`: `subscription` (default) uses the Kimi Code CLI OAuth
  login via the Kimi Agent SDK - install the CLI, run `kimi`, then `/login`
  with Kimi Code OAuth. `api-key` uses `MOONSHOT_API_KEY` against
  api.moonshot.ai directly.
- `MOONSHOT_API_KEY`: Platform API key; required only in api-key mode (also
  used as automatic fallback if the CLI/SDK is unavailable, and for vision
  stages until the SDK accepts image input)

**Optional**:

- `KIMI_MODEL`: Model name (default: `kimi-k3`)
- `KIMI_MODEL_CODE`: Code-gen model for the Manim Coder (default: `kimi-k3`)
- `KIMI_REASONING_EFFORT`: K3 reasoning effort (default: `max`; the only
  accepted value at K3 launch)
- `KIMI_USE_TOOLS`: Enable tool calling (default: `true`)
- `KIMI_ENABLE_THINKING`: Legacy K2-only thinking toggle; ignored by kimi-k3
  (thinking is always on there)

## Important Patterns

### Async/Await Throughout

All agent methods are async and must be called with `await`:

```python
import asyncio

async def main():
    explorer = KimiPrerequisiteExplorer(max_depth=3)
    tree = await explorer.explore_async("concept", verbose=True)

    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)

asyncio.run(main())
```

### Error Handling for API Calls

The KimiClient includes detailed error messages for common issues:

- 401 Unauthorized: Check API key and endpoint
- Tool call failures: Automatic fallback to text parsing
- Rate limiting: Handled by OpenAI SDK retry logic

### Tree Serialization

KnowledgeNode trees can be serialized to/from JSON:

```python
# Save tree
with open("tree.json", "w") as f:
    json.dump(tree.to_dict(), f, indent=2)

# Load tree (requires reconstruction)
with open("tree.json", "r") as f:
    data = json.load(f)
    tree = KnowledgeNode(**data)  # Simplified - see examples
```

### Manim Scene Structure

Generated Manim scenes follow this pattern:

- Inherit from `Scene` class
- Use `construct()` method
- Color schemes use Manim color constants (BLUE, GOLD, RED, etc.)
- Animations use `.animate` syntax
- Camera movements use `self.camera.frame`

## Python Version Requirements

- **Python 3.13+** required (`requires-python = ">=3.13"` in pyproject.toml)
- Use `uv` for version management (recommended)

## Testing Strategy

- **Examples directory** contains test scripts (not pytest tests)
- Most tests require `MOONSHOT_API_KEY` to be set
- Tests use `verbose=True` to show thinking process
- Output saved to `output/` directory
- Rendered videos saved to `media/videos/`

## Common Troubleshooting

### "MOONSHOT_API_KEY environment variable not set"

- Create `.env` file in project root with `MOONSHOT_API_KEY=sk-...`

### Tool calls not working

- Verify `KIMI_USE_TOOLS=true` in `.env`
- Check model supports tool calling (Kimi K2 models do)
- Fallback to text parsing happens automatically

### Unicode errors on Windows

- Tree printing uses ASCII-safe characters on Windows
- No action needed - handled automatically
