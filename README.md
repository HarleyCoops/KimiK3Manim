# Kimi3Manim

Math and physics animations imagined end-to-end by a swarm of **Kimi K3**
agents and rendered with Manim.

## The K3 Agent Swarm (new)

The pipeline was rebuilt on launch day of `kimi-k3` (July 16, 2026) as six
specialist agents exchanging strictly validated JSON artifacts, ending in a
closed render/critique loop on real rendered frames:

| Stage | Agent | Model | Output artifact |
|---|---|---|---|
| 1 | Concept Scout | kimi-k3 | KnowledgeGraph |
| 2 | Mathematical Enricher | kimi-k3 | MathEnrichment |
| 3 | Visual Designer | kimi-k3 (vision) | VisualSpec |
| 4 | Narrative Composer | kimi-k3 | Narrative |
| 5 | Manim Coder | kimi-k2.7-code | SceneBundle (runnable scenes) |
| 6 | Render Critic | kimi-k3 (vision) | CritiqueReport |

A deterministic supervisor sequences the agents, validates every artifact,
renders with Manim, and loops coder/critic until the critic passes.

```bash
# one command: concept in, mp4 out
uv run python -m k3_agents.supervisor "gauge invariance in electromagnetism"
```

The showcase scene lives at
[manim_scenes/k3_harmonic_universe.py](manim_scenes/k3_harmonic_universe.py):

```bash
uv run manim -qh manim_scenes/k3_harmonic_universe.py K3HarmonicUniverse
```

See [docs/KIMI_K3_REBUILD_PLAN.md](docs/KIMI_K3_REBUILD_PLAN.md) for the
architecture rationale and API research. The original K2 pipeline below is
retained for reference; note that the `kimi-k2` model series (including
`kimi-k2-0905-preview`) was discontinued by Moonshot on May 25, 2026.

---


<div align="center">


[![Star History Chart](https://api.star-history.com/svg?repos=HarleyCoops/KimiK2Manim&type=date&legend=top-left)](https://www.star-history.com/#HarleyCoops/KimiK2Manim&type=date)


## Minimal Surfaces: Mathematical Soap Films in 3D Space

![Minimal Surfaces Animation](assets/MinimalSurfaces3D.gif)

*Translucent 3D minimal surfaces (catenoid, helicoid, Costa, Enneper) visualized as mathematical soap films with zero mean curvature H = 0. Generated using Kimi K2's enhanced "liminal solid" prompt technique.*

### The Liminal Solid Prompt

The **liminal solid prompt** is an enhanced prompting technique that bridges abstract mathematical concepts with concrete 3D visualizations. For minimal surfaces, the prompt emphasizes:

> *"Minimal Surfaces: Mathematical Soap Films in 3D Space. This animation MUST use Manim's ThreeDScene class for full 3D rendering. Focus on visualizing surfaces in three-dimensional space with dynamic camera movements, lighting effects, and artistic presentation. Show surfaces like catenoid, helicoid, Costa surface, and Enneper surface as translucent 3D objects that can be viewed from multiple angles. Emphasize depth, perspective, and immersive 3D experience."*

This prompt technique:
- **Bridges abstraction**: Connects mathematical theory (mean curvature H = 0) to physical intuition (soap films)
- **Specifies constraints**: Explicitly requires ThreeDScene for 3D rendering
- **Guides visualization**: Directs camera movements, lighting, and artistic presentation
- **Enables tool calling**: Structured format allows agents to extract visual specifications via tool calls

### Agent Pipeline with Tool Calling

The KimiK2Manim pipeline uses **4 sequential agents** that progressively enrich a knowledge tree through structured tool calls:

![Agent Pipeline with Tool Calling](docs/pipeline_diagram_with_tools.png)

*Each agent calls specialized tools (identify_prerequisites, write_mathematical_content, design_visual_plan, compose_narrative) that communicate with the Kimi K2 API to extract structured data. The pipeline transforms a simple concept into a complete 2000+ word narrative with LaTeX equations, visual specifications, and timing details ready for Manim code generation.*

---


![Slow-Fast Network Architecture](assets/SlowFastNetwork.gif)

*Unnormalized Linear Transformers via [Jürgen Schmidhuber](https://people.idsia.ch/~juergen/1991-unnormalized-linear-transformer.html) and [@SchmidhuberAI](https://twitter.com/SchmidhuberAI) - The 1991 ULTRA (Unnormalized Linear Transformer) demonstrating how a SLOW hypernetwork programs FAST task-specific network weights through additive outer products of KEY and VALUE vectors.*

![Rhombicosidodecahedron Animation](assets/rhombicosidodecahedron_preview.gif)

*Rhombicosidodecahedron with 62 faces, golden ratio geometry, and dynamic multi-axis rotation*

</div>

A standalone Python package for generating Manim animations using the **Kimi K2 thinking model** from Moonshot AI. This package provides agents that build knowledge trees, enrich them with mathematical content and visual specifications, and compose narrative prompts for Manim animation generation.

## Overview

KimiK2Manim uses the Kimi K2 model (via Moonshot AI's OpenAI-compatible API) to:

1. **Explore Prerequisites** - Build knowledge trees by identifying prerequisite concepts
2. **Enrich Mathematically** - Add LaTeX equations, definitions, and examples to each concept
3. **Design Visuals** - Plan Manim visual specifications (colors, animations, transitions)
4. **Compose Narratives** - Generate long-form animation prompts (2000+ words)

## Features

- **KimiClient**: OpenAI-compatible API wrapper for Moonshot AI
- **ToolAdapter**: Converts tool calls to verbose instructions when tools aren't available
- **KimiPrerequisiteExplorer**: Builds knowledge trees recursively
- **KimiEnrichmentPipeline**: Complete enrichment chain (math → visuals → narrative)
- **Kosong Integration**: Official Moonshot AI agent abstraction layer for unified LLM interactions
- **Standalone Package**: No dependencies on parent projects

## Agent Pipeline Flow

The KimiK2Manim pipeline consists of **4 sequential agents** that progressively enrich a knowledge tree until it contains everything needed to generate Manim animation code.

### Pipeline Stages

```
User Prompt → [Agent 1] → [Agent 2] → [Agent 3] → [Agent 4] → Manim Code
              Tree        Math        Visual      Narrative
```

#### Stage 1: Prerequisite Explorer (`KimiPrerequisiteExplorer`)

**Input**: User concept string (e.g., "pythagorean theorem")  
**Output**: `KnowledgeNode` tree with prerequisite structure

**Process**:
- Recursively explores prerequisite concepts
- Builds a hierarchical knowledge tree
- Each node contains: `concept`, `depth`, `is_foundation`, `prerequisites[]`

**Tool Calls**: Uses Kimi K2 to identify prerequisite concepts through natural language reasoning

#### Stage 2: Mathematical Enricher (`KimiMathematicalEnricher`)

**Input**: `KnowledgeNode` tree from Stage 1  
**Output**: Math-enriched tree with equations and definitions

**Process**:
- Recursively processes each node in the tree
- Adds mathematical content to each concept
- Enriches nodes with: `equations[]`, `definitions{}`, `interpretation`, `examples[]`, `typical_values{}`

**Tool Calls**: Uses `write_mathematical_content` tool to get structured math data:
```python
{
    "equations": ["a²+b²=c²", "c=√(a²+b²)"],
    "definitions": {"a": "length of leg", "b": "length of leg", "c": "hypotenuse"},
    "interpretation": "Geometric relationship in right triangles",
    "examples": ["3-4-5 triangle", "5-12-13 triangle"],
    "typical_values": {"3-4-5": "classic integer triangle"}
}
```

#### Stage 3: Visual Designer (`KimiVisualDesigner`)

**Input**: Math-enriched `KnowledgeNode` tree from Stage 2  
**Output**: Visual-enriched tree with Manim specifications

**Process**:
- Recursively designs visual specifications for each node
- Adds visual planning to `visual_spec` field
- Enriches with: `visual_description`, `color_scheme`, `animation_description`, `transitions`, `camera_movement`, `duration`, `layout`

**Tool Calls**: Uses `design_visual_plan` tool to get structured visual data:
```python
{
    "visual_description": "Right triangle with squares on each side",
    "color_scheme": "Blue, green, red for sides a, b, c",
    "animation_description": "Triangle draws itself, squares build outward",
    "transitions": "Fade in triangle first",
    "camera_movement": "Wide shot then zoom in",
    "duration": 15,
    "layout": "Center triangle with equation below"
}
```

#### Stage 4: Narrative Composer (`KimiNarrativeComposer`)

**Input**: Fully enriched `KnowledgeNode` tree (math + visuals) from Stage 3  
**Output**: Complete verbose narrative prompt (2000+ words)

**Process**:
- Orders nodes topologically (foundations first)
- Composes a single continuous narrative integrating all enrichments
- Creates final `narrative` field with verbose prompt

**Tool Calls**: Uses `compose_narrative` tool to generate the final prompt:
```python
{
    "verbose_prompt": "2000+ word narrative with LaTeX, visuals, timing...",
    "concept_order": ["foundation1", "foundation2", "target_concept"],
    "total_duration": 45,
    "scene_count": 3
}
```

### Tool Call Architecture

Each agent uses **Kimi K2's tool calling** to get structured data:

1. **Tool Definition**: Each agent defines a tool schema (function name, parameters, descriptions)
2. **API Call**: Agent sends tool definition to Kimi K2 with the task prompt
3. **Tool Response**: Kimi K2 returns structured JSON via function call
4. **Data Extraction**: Agent extracts JSON payload from `tool_calls[0].function.arguments`
5. **Fallback**: If tool call fails, falls back to parsing JSON from text response

**Example Tool Call Flow**:
```python
# Agent sends request with tool definition
response = client.chat_completion(
    messages=[{"role": "user", "content": "Enrich pythagorean theorem"}],
    tools=[MATHEMATICAL_CONTENT_TOOL],
    tool_choice="auto"
)

# Extract structured data from tool call
tool_calls = response["choices"][0]["message"]["tool_calls"]
payload = json.loads(tool_calls[0]["function"]["arguments"])
# payload = {"equations": [...], "definitions": {...}, ...}
```

### API Call Implementation Details

KimiK2Manim uses the **OpenAI-compatible API** from Moonshot AI to communicate with the Kimi K2 thinking model:

#### KimiClient Architecture

The [KimiClient](kimi_client.py) class wraps the OpenAI Python SDK:

```python
from openai import OpenAI

class KimiClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.client = OpenAI(
            api_key=api_key or MOONSHOT_API_KEY,
            base_url=base_url or "https://api.moonshot.cn/v1"
        )
        self.model = model or "kimi-k2-0905-preview"
```

#### API Call Features

1. **Tool Calling Support**: The client supports OpenAI-compatible function calling
   - Tools defined in JSON schema format
   - Automatic extraction of structured responses
   - Fallback to text parsing if tool calls fail

2. **Response Formatting**: Converts OpenAI SDK responses to consistent dict format
   - Extracts message content, tool calls, and usage statistics
   - Handles streaming and non-streaming responses

3. **Error Handling**: Provides detailed authentication and API error messages
   - 401 authentication troubleshooting
   - API key validation
   - Endpoint verification

4. **Logging**: Built-in verbose logging for debugging
   - API request details (messages, tokens, tools)
   - Response metadata (token usage, content length)
   - Tool call information (function names, arguments)

#### Tool Definition Structure

Each agent defines tools using OpenAI's function calling schema:

```python
MATHEMATICAL_CONTENT_TOOL = {
    "type": "function",
    "function": {
        "name": "write_mathematical_content",
        "description": "Return key mathematical information...",
        "parameters": {
            "type": "object",
            "properties": {
                "equations": {
                    "type": "array",
                    "description": "2-5 LaTeX strings",
                    "items": {"type": "string"}
                },
                "definitions": {
                    "type": "object",
                    "description": "Symbol to definition mapping",
                    "additionalProperties": {"type": "string"}
                }
                # ... more properties
            },
            "required": ["equations", "definitions"]
        }
    }
}
```

#### ToolAdapter for Non-Tool Mode

The [ToolAdapter](tool_adapter.py) converts tool definitions to natural language instructions when tool calling is unavailable:

```python
from kimik2manim.tool_adapter import ToolAdapter

adapter = ToolAdapter()
instructions = adapter.tools_to_instructions([MATHEMATICAL_CONTENT_TOOL])
# Converts tool schema to verbose prompt instructions
```

This allows the pipeline to work even if the API doesn't support function calling.

#### API Call Example from Enrichment Pipeline

From [enrichment_chain.py:199-207](agents/enrichment_chain.py#L199-L207):

```python
response = self.client.chat_completion(
    messages=[{"role": "user", "content": user_prompt}],
    system=system_prompt,
    tools=[MATHEMATICAL_CONTENT_TOOL],
    tool_choice="auto",
    max_tokens=1200,
    temperature=0.2,
)

payload = _extract_tool_payload(response)
if payload is None:
    payload = _parse_json_fallback(self.client.get_text_content(response))
```

The enrichment agents make API calls with:
- **Structured system prompts** describing the agent's role
- **User prompts** with concept details and enrichment requirements
- **Tool definitions** specifying expected JSON structure
- **Fallback parsing** if structured tool calls aren't returned

### Progressive Enrichment

The `KnowledgeNode` tree gets progressively enriched at each stage:

```
Initial Tree:
  - concept
  - depth
  - prerequisites[]

After Math Enrichment:
  + equations[]
  + definitions{}
  + interpretation
  + examples[]

After Visual Enrichment:
  + visual_spec.visual_description
  + visual_spec.color_scheme
  + visual_spec.animation_description
  + visual_spec.duration
  + ...

After Narrative Composition:
  + narrative (verbose_prompt)
```

### Final Output

The enriched tree contains everything needed for Manim code generation:
- **Equations**: LaTeX strings ready for `MathTex()`
- **Visual Specs**: Complete descriptions of what to animate
- **Narrative**: 2000+ word prompt with timing, transitions, and scene flow
- **Structure**: Prerequisite ordering ensures logical presentation

This enriched data can then be used to generate complete Manim Python code that renders the animation.

## Installation

### Prerequisites

**Python 3.13+ Required**: KimiK2Manim now uses [Kosong](https://github.com/MoonshotAI/kosong), the official LLM abstraction layer from Moonshot AI, which requires Python 3.13+.

### Using UV (Recommended)

We recommend using [uv](https://github.com/astral-sh/uv) for Python version management:

```bash
# Install uv (if not already installed)
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/HarleyCoops/KimiK2Manim.git
cd KimiK2Manim

# Install Python 3.13+ and dependencies
uv python install 3.13
uv sync

# Run scripts with Python 3.13
uv run python your_script.py
```

### From Source (Traditional)

```bash
git clone https://github.com/HarleyCoops/KimiK2Manim.git
cd KimiK2Manim

# Ensure Python 3.13+ is installed
python --version  # Should be 3.13+

# Install dependencies
pip install -r requirements.txt
# Or using pyproject.toml:
pip install -e .
```

### Dependencies

Required packages:
- `kosong>=0.21.0` - Official Moonshot AI agent abstraction layer
- `openai>=1.0.0` - OpenAI-compatible API client
- `python-dotenv>=1.0.0` - Environment variable management

See `pyproject.toml` for complete dependency list.

## Quick Start

### 1. Get API Key

Register at [Moonshot AI Platform](https://platform.moonshot.ai/) and get your API key.

### 2. Set Environment Variable

Create a `.env` file in the project root:

```bash
MOONSHOT_API_KEY=your_api_key_here
KIMI_MODEL=kimi-k2-0905-preview  # Optional: specify model name (Kimi K2 model)
KIMI_USE_TOOLS=true        # Optional: enable/disable tools
KIMI_ENABLE_THINKING=heavy  # Optional: thinking mode - "heavy" (max reasoning), "medium", "light", or "true"/"false"
```

### 3. Basic Usage

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
import asyncio

async def main():
    explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
    tree = await explorer.explore_async("quantum field theory", verbose=True)
    tree.print_tree()
    
    # Save to JSON
    import json
    with open("tree.json", "w") as f:
        json.dump(tree.to_dict(), f, indent=2)

asyncio.run(main())
```

### 4. Run Enrichment Pipeline

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline
from kimik2manim.agents.prerequisite_explorer_kimi import KnowledgeNode
import json
import asyncio

async def main():
    # Load existing tree (or create one)
    with open("tree.json", "r") as f:
        tree_data = json.load(f)
    
    # Convert to KnowledgeNode (simplified - see examples for full implementation)
    tree = KnowledgeNode(**tree_data)  # Adjust based on your structure
    
    # Run enrichment
    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)
    
    # Access enriched data
    print(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    print(f"Total duration: {result.narrative.total_duration}s")

asyncio.run(main())
```

### 5. Command-Line Usage

```bash
# Run enrichment pipeline on a tree JSON file
python examples/run_enrichment_pipeline.py path/to/tree.json
```

## Example Renderings

### Rhombicosidodecahedron Animation

KimiK2Manim has been used to generate stunning 3D visualizations, including this rhombicosidodecahedron animation:

The rhombicosidodecahedron is an Archimedean solid with:
- **62 faces**: 20 triangles, 30 squares, and 12 pentagons
- **60 vertices** positioned using golden ratio-based coordinates
- **120 edges** connecting the vertices

#### Visual Design Features

The animation ([manim_scenes/render_rhombicosidodecahedron.py](manim_scenes/render_rhombicosidodecahedron.py)) showcases:

- **Color-coded face types**:
  - Gold edges for pentagonal faces
  - Blue edges for square faces
  - Red edges for triangular faces
- **Glowing vertices** with multi-layer halos
- **Dynamic rotation** on multiple axes with time-varying rotation vector
- **Gradient background** with deep space aesthetic
- **Smooth camera movements** and zoom effects

#### Enhanced Epic Version

The [manim_scenes/epic_rhombicosidodecahedron.py](manim_scenes/epic_rhombicosidodecahedron.py) includes additional effects:

- **Starfield background** with 100 animated stars
- **Enhanced glow effects** on edges and vertices
- **Dynamic camera orbits** with zoom in/out sequences
- **Multi-layered vertex halos** (outer, middle, core)
- **Smooth fade in/out transitions**
- **Title overlay** with golden text

#### Mathematical Formulation

The vertex coordinates use golden ratio constants from McCooey's data:

```python
C0 = (1 + √5) / 4
C1 = (3 + √5) / 4
C2 = (1 + √5) / 2  # Golden ratio φ
C3 = (5 + √5) / 4
C4 = (2 + √5) / 2
```

Vertices are positioned in 3D space using combinations of these constants, creating the precise geometry of the rhombicosidodecahedron.

#### Rendering the Animation

To render the rhombicosidodecahedron:

```bash
# Basic version
manim -pql manim_scenes/render_rhombicosidodecahedron.py ArtisticRhombicosidodecahedron

# Epic version with enhanced effects
manim -pql manim_scenes/epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron

# High quality render
manim -pqh manim_scenes/epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron
```

### Slow-Fast Network Architecture (1991 ULTRA)

The Slow-Fast Network animation visualizes the foundational architecture behind modern Transformers, based on Jürgen Schmidhuber's 1991 [Unnormalized Linear Transformer (ULTRA)](https://people.idsia.ch/~juergen/1991-unnormalized-linear-transformer.html).

**Mathematical Concept**: A meta-learning system where a **SLOW hypernetwork** learns to program the weights of a **FAST task-specific network** through additive outer products of KEY and VALUE vectors:

```
W = Σ(k_i ⊗ v_i) = Σ(k_i · v_i^T)
```

Where:
- **SLOW Network**: Generates KEY and VALUE vectors contextually
- **FAST Network**: Uses dynamically programmed weights W
- **Outer Product**: `k ⊗ v = k · v^T` creates weight matrices
- **QUERY**: Input processed by the fast weight matrix

#### Historical Significance

The 1991 ULTRA predates Google's 2017 quadratic Transformer by 26 years and scales **linearly** in input size (O(n)) rather than quadratically (O(n²)). This architecture demonstrates:

- **End-to-end differentiable** fast weight programming
- **Self-invented KEY/VALUE patterns** learned through gradient descent
- **Meta-learning** capabilities where networks learn to program other networks
- **Linear attention** mechanism (without softmax normalization)

#### Animation Structure

The animation ([SlowFastNetwork.py](SlowFastNetwork.py)) presents the architecture in multiple sections:

1. **Introduction**: Title and overview of SLOW vs FAST networks
2. **Architecture Overview**: Visual representation of the two-network system
3. **KEY & VALUE Generation**: How SLOW network produces programming vectors
4. **Outer Product Mechanism**: Mathematical formulation of weight programming
5. **Fast Weight Matrix**: Dynamic weight construction through additive outer products
6. **Meta-Learning Perspective**: Learning to learn through differentiable programming
7. **Applications**: Modern relevance to Transformers and linear attention

#### Visual Design Features

- **Color-coded networks**: SLOW (blue) and FAST (green) networks visually distinct
- **Animated outer products**: Matrix multiplication visualized step-by-step
- **LaTeX equations**: Professional mathematical notation throughout
- **Vector animations**: KEY and VALUE vectors shown as flowing data
- **Weight matrix visualization**: Dynamic construction of fast weights
- **Clean typography**: PhD-level presentation suitable for academic audiences

#### Rendering the Animation

```bash
# Preview quality
manim -pql SlowFastNetwork.py SlowFastNetworkPhD

# High quality render
manim -pqh SlowFastNetwork.py SlowFastNetworkPhD

# Convert to GIF
ffmpeg -i media/videos/SlowFastNetwork/480p15/SlowFastNetworkPhD.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 media/videos/SlowFastNetwork/480p15/SlowFastNetworkPhD.gif
```

**Reference**: [The 1991 Unnormalized Linear Transformer (ULTRA)](https://people.idsia.ch/~juergen/1991-unnormalized-linear-transformer.html) by Jürgen Schmidhuber ([@SchmidhuberAI](https://twitter.com/SchmidhuberAI))

### Brownian Motion and Einstein's Heat Equation Animation

A comprehensive 2-minute educational animation demonstrating Brownian motion and its connection to Einstein's diffusion equation and heat equation.

**Mathematical Concepts**:
- Random walk theory and mean squared displacement: `⟨x²(t)⟩ = 2Dt`
- Diffusion equation: `∂P/∂t = D∇²P`
- Einstein's relation: `D = k_B T / (6πηa)`
- Connection to heat equation: `∂u/∂t = α∇²u`

#### Scene Versions

The Brownian Motion project includes three scene implementations demonstrating different approaches:

1. **`brownian_motion_scene.py`** - Original unbounded scene
   - Basic implementation without frame boundary constraints
   - Manual text/equation management
   - Demonstrates the core concepts

2. **`brownian_motion_bounded.py`** - Bounded scene with frame constraints
   - Uses `BoundedScene` base class
   - All content automatically constrained within safe frame boundaries
   - Prevents content from rendering outside visible area
   - See [`manim_utils/README_BOUNDED_SCENE.md`](manim_utils/README_BOUNDED_SCENE.md) for details

3. **`brownian_motion_managed.py`** - Complete managed scene (Recommended)
   - Uses `ManagedBoundedScene` with both boundary constraints and scene management
   - Automatic text/equation lifecycle management
   - Prevents overlaps through zone-based positioning
   - Clean section transitions
   - See [`manim_utils/README_SCENE_MANAGEMENT.md`](manim_utils/README_SCENE_MANAGEMENT.md) for details

#### Animation Structure (120 seconds)

1. **Introduction (0-15s)**: Title and historical context
2. **Microscopic View (15-45s)**: Pollen grains and water molecules with Brownian motion
3. **Random Walk Analysis (45-70s)**: Trajectory visualization and mean squared displacement
4. **Diffusion Equation (70-95s)**: PDE derivation and Gaussian solution
5. **Einstein's Relation (95-115s)**: Stokes-Einstein formula and heat equation connection
6. **Conclusion (115-120s)**: Summary message

#### Visual Design Features

- **200 water molecules** (blue dots) moving randomly
- **5 pollen grains** (golden spheres) with colored trajectory trails
- **Animated random walk** trajectory
- **Mean squared displacement** graph showing linear growth
- **Gaussian probability distributions** spreading over time
- **LaTeX equations** with proper formatting
- **Zone-based text layout** preventing overlaps

#### Rendering the Animation

```bash
# Recommended: Managed scene with automatic constraints
python -m manim -pql BrownianMotion/brownian_motion_managed.py BrownianMotionManaged

# Bounded scene (frame constraints only)
python -m manim -pql BrownianMotion/brownian_motion_bounded.py BrownianMotionBounded

# Original scene (no constraints)
python -m manim -pql BrownianMotion/brownian_motion_scene.py BrownianMotionAndEinsteinHeatEquation

# High quality render
python -m manim -pqh BrownianMotion/brownian_motion_managed.py BrownianMotionManaged
```

#### Pipeline Integration

The Brownian Motion scene was generated using the full KimiK2Manim pipeline:

1. **Prerequisite Exploration**: Built knowledge tree from "Brownian Motion and Einstein's Heat Equation"
2. **Mathematical Enrichment**: Added equations, definitions, and interpretations
3. **Visual Design**: Created visual specifications for each concept
4. **Narrative Composition**: Generated verbose animation prompt

The enriched JSON output (`BrownianMotion/output/Brownian_Motion_and_Einstein's_Heat_Equation_enriched.json`) contains:
- Complete knowledge tree with prerequisites
- LaTeX equations for all concepts
- Visual specifications (colors, animations, timing)
- Narrative prompt (2000+ words)

See [`BrownianMotion/README.md`](BrownianMotion/README.md) for complete documentation.

#### Frame Boundary Solution

The Brownian Motion scenes demonstrate solutions to universal Manim rendering issues:

- **Frame Boundaries**: `BoundedScene` ensures all content stays within safe frame area (12.78 × 7.2 units)
- **Text Overlaps**: `ManagedBoundedScene` automatically manages text/equation lifecycle
- **Zone-Based Layout**: Different content types positioned in separate vertical zones
- **Automatic Cleanup**: Old content fades out when new content is added

See [`manim_utils/README_BOUNDED_SCENE.md`](manim_utils/README_BOUNDED_SCENE.md) and [`manim_utils/README_SCENE_MANAGEMENT.md`](manim_utils/README_SCENE_MANAGEMENT.md) for implementation details.

### Harmonic Division Theorem Animation

<div align="center">

![Harmonic Theorem Animation](assets/harmonic_theorem_preview.gif)

*45-second demonstration of the Harmonic Division Theorem with step-by-step LaTeX equations*

</div>

The Harmonic Division Theorem animation demonstrates a fundamental concept in projective geometry:

**Mathematical Concept**: Points A, C, D, B are in harmonic division if their cross-ratio equals -1:
```
(A,B;C,D) = (AC·BD)/(BC·AD) = -1
```

#### Animation Structure (45 seconds)

The animation ([manim_scenes/harmonic_theorem.py](manim_scenes/harmonic_theorem.py)) presents the theorem in five acts:

1. **Introduction (0-5s)**: Title and geometric setup
2. **Construction (5-15s)**: Four collinear points with harmonic division property
3. **Cross-Ratio (15-28s)**: Step-by-step calculation with color-coded segments
4. **Visual Proof (28-40s)**: Circle construction showing harmonic conjugates
5. **Conclusion (40-45s)**: Final boxed theorem

#### Visual Design Features

- **Color-coded points**: A (BLUE), C (GOLD), D (RED), B (GREEN)
- **Glowing halos** around points for emphasis
- **Sequential LaTeX equations** revealed step-by-step
- **Segment highlighting** showing AC·BD and BC·AD relationships
- **Geometric circle** demonstrating pole-polar duality
- **Dark gradient background** for professional aesthetic

#### Rendering the Animation

```bash
# Preview quality
manim -pql manim_scenes/harmonic_theorem.py HarmonicDivisionTheorem

# High quality render
manim -pqh manim_scenes/harmonic_theorem.py HarmonicDivisionTheorem
```

The animation was generated using the KimiK2Manim enrichment pipeline, which:
1. Explored prerequisites (cross-ratio, collinear points, harmonic conjugates)
2. Enriched with LaTeX equations and definitions
3. Designed visual specifications (colors, animations, timing)
4. Composed a narrative prompt with exact 45-second timing breakdown

See [manim_scenes/README.md](manim_scenes/README.md) for more rendering examples and all available scenes.

This demonstrates how KimiK2Manim can be used to generate complex mathematical visualizations with artistic flair!

## Project Structure

```
KimiK2Manim/
├── README.md                    # This file
├── setup.py                     # Package setup (legacy)
├── pyproject.toml               # UV project configuration (Python 3.13+)
├── requirements.txt             # Dependencies (legacy)
├── .python-version              # Python version pin (3.13)
├── .gitignore                   # Git ignore rules
├── config.py                    # Configuration and constants
├── kimi_client.py               # Kimi K2 API client wrapper
├── tool_adapter.py              # Tool call to verbose instruction converter
│
├── agents/                      # Core AI agents
│   ├── __init__.py
│   ├── prerequisite_explorer_kimi.py  # Knowledge tree builder
│   ├── enrichment_chain.py     # Math, visual, narrative enrichment (legacy)
│   └── enrichment_chain_kosong.py  # Kosong-based enrichment (new)
│
├── manim_scenes/                # Manim animation scripts
│   ├── README.md               # Scene documentation
│   ├── render_rhombicosidodecahedron.py
│   ├── epic_rhombicosidodecahedron.py
│   ├── enhance_rhombicosidodecahedron.py
│   ├── kimi2pythag.py
│   └── Kimik2First.py
│
├── BrownianMotion/             # Brownian Motion example project
│   ├── README.md              # Project documentation
│   ├── run_pipeline.py        # Pipeline execution script
│   ├── brownian_motion_scene.py        # Original unbounded scene
│   ├── brownian_motion_bounded.py      # Bounded scene (frame constraints)
│   ├── brownian_motion_managed.py      # Managed scene (recommended)
│   └── output/                # Generated enriched content
│       ├── Brownian_Motion_and_Einstein's_Heat_Equation_enriched.json
│       ├── Brownian_Motion_and_Einstein's_Heat_Equation_narrative.txt
│       └── Brownian_Motion_and_Einstein's_Heat_Equation_prerequisite_tree.json
│
├── manim_utils/                # Manim utility modules
│   ├── bounded_scene.py       # Frame boundary constraints
│   ├── scene_manager.py       # Scene management system
│   ├── managed_scene.py       # Combined managed scene class
│   ├── frame_config.py        # Frame configuration constants
│   ├── README_BOUNDED_SCENE.md
│   └── README_SCENE_MANAGEMENT.md
│
├── examples/                    # Example usage and test scripts
│   ├── test_kimi_integration.py
│   ├── run_enrichment_pipeline.py
│   ├── test_qft_pipeline.py
│   ├── run_pipeline.py
│   ├── test_pipeline_debug.py
│   └── test_pipeline_simple.py
│
├── output/                      # Generated outputs
│   └── rhombicosidodecahedron_narrative.txt
│
├── media/                       # Manim rendered videos
│   └── videos/
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── KOSONG_REFACTORING.md    # Kosong migration guide
│   └── PYTHON_UPGRADE.md        # Python 3.13 upgrade guide
│
└── dev/                         # Development and experimental files
    ├── KimiChatRhom.py
    └── textprompt.txt
```

## Configuration

All configuration is in `config.py` or via environment variables:

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)
- `KIMI_MODEL`: Kimi K2 model name (default: "kimi-k2-0905-preview")
- `KIMI_USE_TOOLS`: Enable tool calling (default: "true")
- `KIMI_ENABLE_THINKING`: Thinking mode - "heavy" (max reasoning), "medium", "light", or "true"/"false" (default: "true")

**Note**: Python 3.13+ is required for Kosong integration. Use `uv python install 3.13` or upgrade Python manually.

## Key Components

### KimiClient

OpenAI-compatible wrapper for Moonshot AI's API:

```python
from kimik2manim.kimi_client import KimiClient

client = KimiClient()
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
print(client.get_text_content(response))
```

### ToolAdapter

Converts tool definitions to verbose instructions:

```python
from kimik2manim.tool_adapter import ToolAdapter

adapter = ToolAdapter()
tools = [...]  # Your tool definitions
instructions = adapter.tools_to_instructions(tools)
```

### KimiPrerequisiteExplorer

Builds knowledge trees by exploring prerequisites:

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer

explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
tree = await explorer.explore_async("special relativity", verbose=True)
```

### KimiEnrichmentPipeline

Complete enrichment chain:

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline

pipeline = KimiEnrichmentPipeline()
result = await pipeline.run_async(tree)
```

## Examples

See the `examples/` directory for:
- `test_kimi_integration.py` - Basic API and agent tests
- `run_enrichment_pipeline.py` - CLI for running enrichment
- `test_qft_pipeline.py` - Full pipeline test with QFT concepts

## Testing

```bash
# Run tests (requires MOONSHOT_API_KEY)
pytest tests/ -v

# Run without API calls (unit tests only)
pytest tests/ -v -k "not api"
```

## Architecture

The package follows a layered architecture with agent orchestration:

1. **Client Layer**: `KimiClient` handles all API communication with Moonshot AI (legacy) or **Kosong** abstraction layer (new)
2. **Adapter Layer**: `ToolAdapter` converts tool calls to verbose instructions when tools aren't available
3. **Agent Layer**: 4 sequential agents orchestrate knowledge tree building and enrichment
4. **Orchestrator**: `KimiEnrichmentPipeline` coordinates the 3 enrichment agents

### Kosong Integration

KimiK2Manim now supports [Kosong](https://github.com/MoonshotAI/kosong), the official LLM abstraction layer from Moonshot AI. Kosong provides:

- **Unified Message Structures**: `Message` class for consistent LLM interactions
- **Async Tool Orchestration**: Automatic tool calling loops with `kosong.step()`
- **Type-Safe Tools**: Pydantic models for tool parameters with validation
- **Provider Abstraction**: Easy switching between LLM providers
- **Reduced Boilerplate**: Less manual tool call parsing and response handling

#### Using Kosong-Based Agents

Example Kosong-based mathematical enricher:

```python
from agents.enrichment_chain_kosong import KosongMathematicalEnricher
from kosong.chat_provider.kimi import Kimi
from kosong.message import Message
import kosong

# Create Kosong Kimi client
kimi = Kimi(
    base_url="https://api.moonshot.ai/v1",
    api_key=os.getenv("MOONSHOT_API_KEY"),
    model="kimi-k2-turbo-preview",
)

# Use Kosong-based enricher
enricher = KosongMathematicalEnricher(client=kimi)
enriched_tree = await enricher.enrich_tree(tree)
```

#### Migration Path

- **Current**: Custom `KimiClient` wrapper with manual tool parsing
- **New**: Kosong abstraction with automatic tool orchestration
- **Status**: Both implementations available; Kosong version in `agents/enrichment_chain_kosong.py`

See `docs/KOSONG_REFACTORING.md` for detailed migration guide.

### Agent Orchestration

The `KimiEnrichmentPipeline` orchestrator runs agents in sequence:

```python
async def run_async(self, root: KnowledgeNode) -> EnrichmentResult:
    # Stage 2: Math enrichment (recursive)
    await self.math.enrich_tree(root)
    
    # Stage 3: Visual design (recursive)
    await self.visual.design_tree(root)
    
    # Stage 4: Narrative composition
    narrative = await self.narrative.compose_async(root)
    
    return EnrichmentResult(enriched_tree=root, narrative=narrative)
```

Each agent processes the entire tree recursively, ensuring all nodes (including prerequisites) are enriched before moving to the next stage.

See `docs/ARCHITECTURE.md` for detailed architecture documentation.

## E2B Sandbox Environment

### 🎮 Interactive Exploration Sandbox

The `e2b_sandbox/` directory provides a complete, self-contained sandbox environment for exploring KimiK2 thinking capabilities, testing visual reasoning, and generating Manim animations. This is ideal for:

- **Research**: Exploring complex concepts with heavy thinking mode
- **Testing**: Validating visual reasoning capabilities
- **Education**: Generating educational content and animations
- **Development**: Prototyping new Manim scenes

### Quick Start

```bash
# 1. Setup the sandbox
cd e2b_sandbox
bash setup.sh

# 2. Configure your API key
cp .env.template ../.env
# Edit ../.env and add your MOONSHOT_API_KEY

# 3. Run an interactive exploration
python interactive_explorer.py

# 4. Run visual reasoning tests
python visual_reasoning_tests.py

# 5. Try the demo
python demo.py --demo all
```

### Features

#### 🔍 Interactive Explorer
Explore concepts with customizable depth and thinking modes:

```python
from e2b_sandbox import quick_explore

result = await quick_explore(
    concept="quantum entanglement",
    thinking_mode="heavy",
    depth=3,
    enrichment=True
)
```

#### 🧪 Visual Reasoning Tests
Automated test suite for validating visual reasoning capabilities:

- Geometric transformations
- Wave phenomena
- Calculus concepts
- Linear algebra
- Complex analysis
- Topology

```python
from e2b_sandbox import run_visual_tests

results = await run_visual_tests()
print(f"Pass rate: {results['pass_rate']}%")
```

#### 🎬 Manim Renderer
Render Manim scenes with quality presets:

```python
from e2b_sandbox import ManimRenderer, setup_sandbox_environment

config = setup_sandbox_environment()
renderer = ManimRenderer(config)

renderer.render_scene(
    scene_file=Path("manim_scenes/harmonic_theorem.py"),
    scene_class="HarmonicDivisionTheorem",
    quality="h"  # High quality (1080p)
)
```

#### 🛠️ Sandbox Tools
Utilities for managing explorations:

```python
from e2b_sandbox import SandboxTools

tools = SandboxTools()
tools.create_exploration_report()
tools.package_exploration("quantum mechanics")
tools.get_storage_usage()
```

### Sandbox Configuration

The sandbox supports multiple modes and configurations:

```bash
# Environment variables (.env file)
MOONSHOT_API_KEY=sk-your-key-here
KIMI_ENABLE_THINKING=heavy  # heavy, medium, light
KIMI_USE_TOOLS=true
SANDBOX_MODE=exploration    # exploration, rendering, interactive, batch
MAX_DEPTH=3                 # Prerequisite tree depth
MANIM_QUALITY=l            # l, m, h, k (480p, 720p, 1080p, 4k)
```

### Use Cases

#### 1. Educational Content Generation
```python
# Generate comprehensive educational content
result = await explorer.explore_concept(
    "calculus fundamental theorem",
    depth=3,
    enrichment=True
)
# Use the narrative and visual specs for educational materials
```

#### 2. Research Visualization
```python
# Explore complex research topics
result = await explorer.explore_concept(
    "quantum chromodynamics",
    depth=4,
    enrichment=True
)
# Get visual specifications for research diagrams
```

#### 3. Batch Processing
```python
# Process multiple concepts
concepts = ["group theory", "ring theory", "field theory"]
results = await explorer.batch_explore(concepts, enrichment=True)
```

### Docker/E2B Deployment

```bash
# Build the E2B container
docker build -t kimik2-sandbox -f e2b_sandbox/e2b.Dockerfile .

# Run the container
docker run -it \
  -e MOONSHOT_API_KEY=sk-your-key \
  -v $(pwd)/output:/home/user/kimik2/output \
  -v $(pwd)/media:/home/user/kimik2/media \
  kimik2-sandbox
```

For complete documentation, see [`e2b_sandbox/README.md`](e2b_sandbox/README.md).

### Interesting Discoveries

The sandbox is designed to be a playground for discovering how KimiK2's "thinking" mode handles:

- **Complex Mathematical Concepts**: Testing extended reasoning on advanced topics
- **Visual Problem Solving**: How well can KimiK2 translate abstract concepts to visual specifications?
- **Multi-stage Reasoning**: Validating the complete prerequisite → math → visual → narrative pipeline
- **Chinese Language Processing**: Exploring the native Chinese agent pipeline capabilities

Try exploring concepts like:
- "fourier transform" - Wave decomposition and harmonics
- "riemann hypothesis" - Number theory and complex analysis
- "quantum entanglement" - Quantum mechanics visualization
- "general relativity" - Spacetime curvature
- "neural network backpropagation" - ML algorithm visualization

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [Moonshot AI Platform](https://platform.moonshot.ai/)
- [Kimi K2 Documentation](https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model)
- [Kosong - LLM Abstraction Layer](https://github.com/MoonshotAI/kosong) - Official Moonshot AI agent framework
- [Kosong Documentation](https://moonshotai.github.io/kosong/)
- [Manim Documentation](https://docs.manim.community/)

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/HarleyCoops/KimiK2Manim/issues).
