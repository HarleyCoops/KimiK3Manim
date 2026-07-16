# KimiK2Manim E2B Sandbox

A self-contained sandbox environment for exploring KimiK2 thinking capabilities, visual reasoning, and Manim animation generation.

## 🎯 Overview

This E2B sandbox provides a complete, interactive environment for:

- **Concept Exploration**: Use KimiK2's "heavy thinking" mode to explore complex concepts
- **Visual Reasoning**: Test KimiK2's ability to reason through visual mathematical problems
- **Manim Integration**: Automatically generate and render mathematical animations
- **Pipeline Testing**: Validate the complete 4-stage enrichment pipeline
- **Interactive Tools**: CLI utilities for managing explorations and outputs

## 🏗️ Architecture

### The KimiK2 Pipeline

```
User Concept
    ↓
[1] Prerequisite Explorer
    └─→ Builds hierarchical knowledge tree
    └─→ Identifies foundational vs advanced concepts
    ↓
[2] Mathematical Enricher
    └─→ Adds LaTeX equations
    └─→ Adds definitions and examples
    ↓
[3] Visual Designer
    └─→ Plans visual specifications
    └─→ Designs color schemes and animations
    ↓
[4] Narrative Composer
    └─→ Generates 2000+ word animation prompts
    └─→ Integrates all enrichments
    ↓
Narrative + Enriched Tree
```

### Sandbox Components

- **`sandbox_config.py`**: Environment configuration and validation
- **`interactive_explorer.py`**: Main exploration interface
- **`visual_reasoning_tests.py`**: Automated visual reasoning test suite
- **`manim_renderer.py`**: Manim rendering utilities
- **`tools.py`**: File management and utility tools
- **`e2b.Dockerfile`**: Container configuration for E2B
- **`setup.sh`**: Automated setup script

## 🚀 Quick Start

### 1. Setup

```bash
# Run the setup script
cd e2b_sandbox
bash setup.sh

# Configure your API key
cp .env.template ../.env
nano ../.env  # Add your MOONSHOT_API_KEY
```

### 2. Basic Exploration

```python
# Run the interactive explorer
python interactive_explorer.py
```

This will:
- Explore a demo concept ("fourier transform")
- Build a knowledge tree with prerequisites
- Run the full enrichment pipeline
- Generate mathematical content, visual specs, and narrative
- Save all outputs to the `output/` directory

### 3. Visual Reasoning Tests

```python
# Run the visual reasoning test suite
python visual_reasoning_tests.py
```

This tests KimiK2's ability to:
- Reason through geometric transformations
- Visualize wave phenomena
- Understand calculus concepts
- Design linear algebra visualizations
- Handle complex analysis
- Represent topological concepts

### 4. Manim Rendering

```python
# Render existing Manim scenes
python manim_renderer.py
```

Or use the ManimRenderer programmatically:

```python
from e2b_sandbox.manim_renderer import ManimRenderer
from e2b_sandbox.sandbox_config import setup_sandbox_environment

config = setup_sandbox_environment()
renderer = ManimRenderer(config)

# Render a scene
renderer.render_scene(
    scene_file=Path("manim_scenes/harmonic_theorem.py"),
    scene_class="HarmonicDivisionTheorem",
    quality="h"  # High quality
)
```

### 5. Sandbox Tools

```python
# Launch interactive tool menu
python tools.py menu
```

Available tools:
- List all outputs
- View latest exploration
- Generate exploration reports
- Check storage usage
- Package explorations for export
- Clean up old outputs
- Convert videos to GIFs

## 📋 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
MOONSHOT_API_KEY=sk-your-key-here

# Optional
KIMI_MODEL=kimi-k3
KIMI_ENABLE_THINKING=heavy  # heavy, medium, light
KIMI_USE_TOOLS=true
SANDBOX_MODE=exploration    # exploration, rendering, interactive, batch
MAX_DEPTH=3
MANIM_QUALITY=l            # l, m, h, k (480p, 720p, 1080p, 4k)
```

### Programmatic Configuration

```python
from e2b_sandbox.sandbox_config import SandboxConfig, SandboxMode

config = SandboxConfig(
    moonshot_api_key="sk-...",
    thinking_mode="heavy",
    mode=SandboxMode.EXPLORATION,
    max_depth=3,
    manim_quality="l"
)
```

## 🎨 Usage Examples

### Example 1: Explore a Single Concept

```python
from e2b_sandbox.interactive_explorer import InteractiveExplorer
from e2b_sandbox.sandbox_config import setup_sandbox_environment
import asyncio

async def explore():
    config = setup_sandbox_environment()
    explorer = InteractiveExplorer(config)

    result = await explorer.explore_concept(
        concept="quantum entanglement",
        depth=3,
        enrichment=True,
        save_output=True
    )

    print(f"Narrative length: {len(result['narrative'])} chars")
    print(f"Knowledge tree depth: {result['tree']['depth']}")

asyncio.run(explore())
```

### Example 2: Batch Exploration

```python
async def batch_explore():
    config = setup_sandbox_environment()
    explorer = InteractiveExplorer(config)

    concepts = [
        "neural network backpropagation",
        "general relativity",
        "riemann hypothesis"
    ]

    results = await explorer.batch_explore(
        concepts=concepts,
        enrichment=True
    )

    explorer.print_summary()

asyncio.run(batch_explore())
```

### Example 3: Custom Visual Reasoning Test

```python
from e2b_sandbox.visual_reasoning_tests import VisualReasoningTest

test = VisualReasoningTest(
    name="Custom Geometry Test",
    concept="hyperbolic geometry",
    expected_visual_elements=["hyperbolic", "curve", "plane", "parallel"],
    description="Test understanding of non-Euclidean geometry"
)

# Run with your explorer and pipeline
result = await test.run(explorer, pipeline)
```

## 📂 Output Structure

```
output/
├── fourier_transform_20250111_143022.json        # Full exploration result
├── fourier_transform_20250111_143022_narrative.txt  # Generated narrative
├── visual_reasoning_tests_20250111_150000.json   # Test results
└── exploration_report_20250111_160000.txt        # Summary report

media/
└── videos/
    ├── harmonic_theorem/
    │   └── 480p15/
    │       └── HarmonicDivisionTheorem.mp4
    └── rhombicosidodecahedron/
        └── 1080p60/
            └── ArtisticRhombicosidodecahedron.mp4
```

## 🧪 Visual Reasoning Tests

The test suite includes 6 comprehensive tests:

1. **Geometric Transformations**: 3D rotations and transformations
2. **Wave Phenomena**: Fourier series and harmonic decomposition
3. **Calculus Concepts**: Riemann sums and integration
4. **Linear Algebra**: Eigenvalues and eigenvectors
5. **Complex Analysis**: Complex plane mappings
6. **Topology**: Homeomorphisms and continuous deformations

Each test:
- Explores the concept with KimiK2
- Runs the full enrichment pipeline
- Validates visual specifications
- Reports pass/fail based on expected visual elements

## 🔧 Advanced Features

### Custom Thinking Modes

```python
# Maximum reasoning effort
config.thinking_mode = "heavy"

# Balanced reasoning
config.thinking_mode = "medium"

# Fast, lightweight reasoning
config.thinking_mode = "light"
```

### Resource Limits

```python
config.max_render_time = 300      # Max seconds per render
config.max_tree_depth = 5         # Max prerequisite depth
config.max_narrative_words = 3000 # Max narrative length
```

### Batch Rendering

```python
renderer = ManimRenderer(config)

scenes = [
    ("manim_scenes/harmonic_theorem.py", "HarmonicDivisionTheorem"),
    ("manim_scenes/render_rhombicosidodecahedron.py", "ArtisticRhombicosidodecahedron"),
]

results = renderer.batch_render(scenes, quality="h")
```

## 🐳 Docker / E2B Deployment

### Build the E2B Container

```bash
docker build -t kimik2-sandbox -f e2b_sandbox/e2b.Dockerfile .
```

### Run the Container

```bash
docker run -it \
  -e MOONSHOT_API_KEY=sk-your-key \
  -v $(pwd)/output:/home/user/kimik2/output \
  -v $(pwd)/media:/home/user/kimik2/media \
  kimik2-sandbox
```

### E2B Cloud Deployment

1. Create an E2B template from the Dockerfile
2. Configure environment variables in E2B dashboard
3. Launch sandbox instances via E2B API
4. Access outputs through E2B file system API

## 📊 Performance Considerations

### Thinking Mode Impact

| Mode   | Speed  | Quality | Use Case |
|--------|--------|---------|----------|
| heavy  | Slow   | Best    | Complex concepts, research |
| medium | Medium | Good    | Standard explorations |
| light  | Fast   | Basic   | Simple concepts, testing |

### Depth Impact

| Depth | Tree Size | Time | Use Case |
|-------|-----------|------|----------|
| 1-2   | Small     | Fast | Quick exploration |
| 3-4   | Medium    | ~5min | Standard depth |
| 5+    | Large     | 10min+ | Comprehensive research |

## 🎯 Use Cases

### 1. Educational Content Generation

Explore a concept and generate a complete educational narrative with visuals:

```python
result = await explorer.explore_concept(
    "calculus fundamental theorem",
    depth=3,
    enrichment=True
)
# Use the narrative to create educational materials
```

### 2. Research Visualization

Understand complex research topics through visual reasoning:

```python
result = await explorer.explore_concept(
    "quantum chromodynamics",
    depth=4,
    enrichment=True
)
# Get visual specifications for diagram creation
```

### 3. Animation Prototyping

Generate ideas for mathematical animations:

```python
result = await explorer.explore_concept(
    "complex analysis residue theorem",
    enrichment=True
)
# Use visual specs and narrative for Manim coding
```

### 4. Concept Mapping

Build comprehensive knowledge maps:

```python
# Explore and save multiple related concepts
concepts = ["group theory", "ring theory", "field theory"]
results = await explorer.batch_explore(concepts, enrichment=False)
# Analyze prerequisite relationships
```

## 🛠️ Troubleshooting

### API Key Issues

```
Error: MOONSHOT_API_KEY is required
```

Solution: Ensure `.env` file contains valid API key

### Manim Rendering Fails

```
Error: LaTeX not found
```

Solution: Install LaTeX with `apt-get install texlive-full`

### Timeout Errors

```
Error: Timeout after 300s
```

Solution: Increase `MAX_RENDER_TIME` in `.env`

## 📚 Additional Resources

- [KimiK2 Documentation](https://platform.moonshot.ai/docs)
- [Manim Documentation](https://docs.manim.community/)
- [E2B Documentation](https://e2b.dev/docs)
- [Project Repository](https://github.com/HarleyCoops/KimiK2Manim)

## 🤝 Contributing

Contributions welcome! Areas of interest:

- Additional visual reasoning tests
- Improved code generation from narratives
- New Manim scene templates
- Performance optimizations
- Documentation improvements

## 📄 License

See main project LICENSE file.

## 🎉 Happy Exploring!

The sandbox is designed to be a playground for exploring the intersection of AI reasoning, mathematical visualization, and educational content generation. Experiment with different concepts, thinking modes, and visual styles to discover what KimiK2 can create!
