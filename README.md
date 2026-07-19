# Kimi3Manim

Math and physics animations imagined end-to-end by a swarm of **Kimi K3**
agents and rendered with [Manim Community Edition](https://www.manim.community/).

Give the pipeline a concept - "gauge invariance in electromagnetism",
"the heat kernel", "why planets orbit in ellipses" - and six specialist
agents map its prerequisite structure, enrich it with rigorous mathematics,
design the visual language, write a screenplay, generate runnable Manim
code, and then *watch their own rendered frames* and iterate until the
result is worth shipping.

[![Euler's Identity — rendered by the K3 agent swarm](assets/euler_identity_hero.png)](assets/EulerIdentityFilm.mp4)

*Hero: **Euler's Identity** — a 3.5-minute film written, staged, rendered, and
self-critiqued by the six-agent K3 swarm from a single verbose LaTeX-rich
prompt. Click the collage for the full mp4
([EulerIdentityFilm.mp4](assets/EulerIdentityFilm.mp4)).*

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=HarleyCoops/KimiK3Manim&type=date&legend=top-left)](https://www.star-history.com/#HarleyCoops/KimiK3Manim&type=date)

</div>

---

## Showcase

**The Harmonic Universe** - the pipeline's demonstration piece
([manim_scenes/k3_harmonic_universe.py](manim_scenes/k3_harmonic_universe.py)),
three acts on a single idea:

1. **Circles hiding inside circles.** Fourier epicycles: five rotating
   circles, chained tip to tip, trace a square wave out of pure rotation.
2. **The string chooses its notes.** Boundary conditions quantize a
   vibrating string into discrete harmonics - the birth of eigenmodes.
3. **Many notes make a particle.** Superposing harmonics localizes a wave
   into a packet: the mathematical seed of quantum mechanics.

```bash
uv run manim -qh manim_scenes/k3_harmonic_universe.py K3HarmonicUniverse
```

## Melting Space — Ricci Flow and the Poincaré Conjecture (new)

[![Melting Space — Ricci flow melts a dumbbell into spheres](assets/melting_space.gif)](assets/MeltingSpace.mp4)

*A ~2 minute, 1080p30, LaTeX-rich 3D film, imagined, scripted, and rendered by
Kimi K3 in a single session — from a verbose per-scene prompt it wrote for
itself ([prompts/RicciFlowFilm.tex](prompts/RicciFlowFilm.tex)); scene source:
[manim_scenes/melting_space.py](manim_scenes/melting_space.py). Click the GIF
for the full mp4 ([MeltingSpace.mp4](assets/MeltingSpace.mp4)).*

What you are seeing on screen, scene by scene:

1. **Shapes & the rubber-band test.** A golden wireframe sphere morphs through
   pear, dumbbell, and blob — to a topologist these are all the same shape. A
   cyan loop lassoed around each one slides free; around a ghost donut, a
   magenta loop is stuck forever. This is the entire content of Poincaré's
   1904 question: `∀γ : S¹ → M, γ ≃ point  ⟹  M ≅ S³ ?`
2. **The curvature fingerprint.** Osculating rings snug against the surface
   show principal curvatures `k_i = 1/r_i`; ~760 dots paint the shape by
   Gaussian curvature `K = k₁k₂` — fire where it's tightly curved, ice where
   it's flat. Gauss' Theorema Egregium: `K` is intrinsic, measurable without
   ever leaving the surface.
3. **Heat & the melt.** The heat equation `∂ₜu = Δu` smooths a plate of
   temperature dots until every point equals its neighbors — then Hamilton's
   masterstroke, `∂g/∂t = −2 Ric(g)`: do the same thing to *shape itself*. The
   curvature-painted dumbbell melts toward a uniform gold sphere. Cliffhanger:
   a surface of revolution whose waist keeps thinning.
4. **The neck pinch.** The waist collapses as the `|Rm|_neck` gauge climbs —
   curvature blows up in finite time: `|Rm| → ∞, t → T < ∞`. The flow
   singularizes; the lobes snap apart; a beat of black silence.
5. **Perelman's surgery.** Cut a neck `S² × (−ε, ε)`, cap both stumps with
   `D³`, keep flowing: `M ≅ M₁ # M₂`. A flash of the W-entropy monotonicity
   formula `W(g, f, τ) ↑` — Perelman's proof that no new singularities sneak
   in — and the two halves melt into twin spheres, then a cascade of spheres.
6. **The theorem.** Every simply connected closed 3-manifold is a sphere:
   Poincaré (1904, the question) → Hamilton (1982, the flow) → Perelman
   (2002–03, the surgery). Fields Medal and Millennium Prize — both declined.
   The cyan rubber band returns, slides off the hero sphere one last time:
   **"If every loop can let go, the shape was always a sphere."**

Render it yourself (six scenes, concatenated with ffmpeg):

```bash
for s in MS1Shapes MS2Curvature MS3HeatFlow MS4NeckPinch MS5Surgery MS6Theorem; do
  uv run python -m manim render -r 1920,1080 --fps 30 \
    manim_scenes/melting_space.py "$s"
done
ffmpeg -f concat -safe 0 -i concat.txt -c copy MeltingSpace.mp4
```

## Reverse Reasoning — a K3 protocol film (new)

[![Reverse Reasoning — a Kimi K3 protocol film](assets/k3_reverse_reasoning.gif)](assets/K3ReverseReasoning.mp4)

*A ~1 minute, 1080p30, LaTeX-rich 3D short, designed and directed by Kimi K3
itself in a single session. Click the GIF for the full mp4
([K3ReverseReasoning.mp4](assets/K3ReverseReasoning.mp4)); scene source:
[manim_scenes/k3_reverse_reasoning.py](manim_scenes/k3_reverse_reasoning.py).*

What you are seeing on screen, act by act:

1. **Genesis — 896 sleep, 16 wake.** A Fibonacci-sphere lattice of dormant
   experts drifts in a void; sixteen ignite in magenta and cyan. This is
   Stable LatentMoE: `y = Σ_{i∈T} g_i(x)E_i(x)` with `|T| = 16` active of
   `N_E = 896` experts.
2. **The Goal.** A golden monolith crystallizes over a wireframe manifold of
   conjectures: Nicomachus' theorem `Σ k³ = (n(n+1)/2)²` — the statement the
   protocol will prove. The protocol begins at the end.
3. **Backward Bloom.** Reverse reasoning made visible: the goal `G`
   decomposes into sufficient subgoals (`G ⇐ g₁ ∧ τ ∧ β`), each of which
   blooms further (`g₁ ⇐ ℓ ∧ g₂ ∧ g₃`, `g₂ ⇐ α₁`, `g₃ ⇐ α₂`) until every
   leaf is an axiom glowing green. Every node is real LaTeX and the proof is
   valid — telescoping differences, the factorization lemma, and the base
   case `1³ = 1²`.
4. **Forward Verification.** Direction flip: pulses of light climb the tree
   from the axioms to the goal, igniting every link as it is checked, while
   the K3 machinery that does the checking floats on screen — Kimi Delta
   Attention (`S_t = S_{t-1}Γ_t + β_t k_t(v_t - S_{t-1}k_t)ᵀ`) and Attention
   Residuals (`h_ℓ = Σ_{i<ℓ} w_i h_i`). The goal blazes and emits shockwave
   rings.
5. **Sigil.** The proof collapses into a burning star; a halo of the film's
   LaTeX artifacts orbits it like a debris ring before the end card:
   **reason backward · verify forward**.

Render it yourself (five acts, concatenated with ffmpeg):

```bash
for s in RRGenesis RRGoal RRBackwardBloom RRVerification RRSigil; do
  uv run python -m manim render -r 1920,1080 --fps 30 \
    manim_scenes/k3_reverse_reasoning.py "$s"
done
```

Earlier renders from this repository:

<div align="center">

![Minimal Surfaces Animation](assets/MinimalSurfaces3D.gif)

*Translucent 3D minimal surfaces (catenoid, helicoid, Costa, Enneper) with zero mean curvature H = 0.*

![Slow-Fast Network Architecture](assets/SlowFastNetwork.gif)

*The 1991 ULTRA unnormalized linear transformer: a slow hypernetwork programming fast weights.*

![Rhombicosidodecahedron Animation](assets/rhombicosidodecahedron_preview.gif)

*Rhombicosidodecahedron: 62 faces, golden-ratio geometry, multi-axis rotation.*

</div>

---

## How it works: the K3 agent swarm

The pipeline was rebuilt on the launch day of `kimi-k3` (July 16, 2026)
around three capabilities the K2 generation did not have:

- **1M-token context** - every agent sees the *whole* knowledge graph at
  once instead of processing nodes one at a time, so cross-references and
  visual continuity are planned globally.
- **Strict structured output** - agents are forced to emit exactly one
  validated JSON artifact per stage (`response_format` with
  `json_schema` + `strict`). There is no text-parsing fallback layer
  anymore; a malformed artifact is a hard error, not a silent guess.
- **Native vision** - the Visual Designer can study frames from earlier
  renders for style continuity, and the Render Critic judges the actual
  rendered video, not a description of it.

### The six agents

| Stage | Agent | Model | Consumes | Produces |
|---|---|---|---|---|
| 1 | Concept Scout | `kimi-k3` | concept string | `KnowledgeGraph` |
| 2 | Mathematical Enricher | `kimi-k3` | graph | `MathEnrichment` |
| 3 | Visual Designer | `kimi-k3` (vision) | graph + math | `VisualSpec` |
| 4 | Narrative Composer | `kimi-k3` | graph + math + visuals | `Narrative` |
| 5 | Manim Coder | `kimi-k3` | screenplay + visuals | `SceneBundle` |
| 6 | Render Critic | `kimi-k3` (vision) | rendered frames + spec | `CritiqueReport` |

Every artifact is a Pydantic model in [schemas/artifacts.py](schemas/artifacts.py);
the same class generates the strict JSON schema the model must satisfy and
re-validates the artifact when the supervisor loads it.

### The closed loop

A deterministic supervisor ([k3_agents/supervisor.py](k3_agents/supervisor.py)) -
plain Python, not a model - sequences the stages, persists artifacts to
`output/k3_runs/<concept>/`, renders the generated scenes with real Manim,
samples frames with ffmpeg, and shows them to the Render Critic:

```
Scout -> Enricher -> Designer -> Composer -> Coder -> render
                                               ^         |
                                               |     frames to Critic
                                               |         |
                                               +-- issues if not passed
```

Render failures send the traceback back to the Coder; critic failures send
concrete visual issues back to the Coder. The loop runs until the critic
passes or the repair budget (default 3 rounds) is exhausted.

### Run it

```bash
uv run python -m k3_agents.supervisor "the wave equation"

# options
uv run python -m k3_agents.supervisor "special relativity" --quality -qh --max-repairs 5
```

The run directory will contain every intermediate artifact
(`01_knowledge_graph.json` through `06_critique_*.json`), the generated
scene files, and the final mp4 under `media/`.

---

## Getting started

### 1. Install

Requires Python 3.13+ (managed by [uv](https://docs.astral.sh/uv/)) and
ffmpeg + a LaTeX distribution for Manim's equation rendering.

```bash
git clone https://github.com/HarleyCoops/KimiK3Manim.git
cd KimiK3Manim

# Install uv if needed:
#   macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
#   Windows:     powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

uv python install 3.13
uv sync
uv pip install manim          # or: uv sync --extra render
```

### 2. Authenticate (subscription by default)

**The default and recommended way to authenticate is a Kimi subscription
through the Kimi Code CLI - no API key handling, no per-token billing
surprises, and the same login powers the Kimi Agent SDK runtime.**

```bash
# Install the Kimi Code CLI (single binary, no Node required)
curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash
# or: brew install kimi-code

# Launch it once and log in
kimi
# then inside the TUI:
#   /login  ->  choose "Kimi Code OAuth" and authorize in the browser
```

That is the entire setup. The OAuth login is stored by the CLI and reused
automatically by everything built on the Kimi Code runtime, including the
[Kimi Agent SDK](https://github.com/MoonshotAI/kimi-agent-sdk)
(`uv add kimi-agent-sdk`) that this pipeline uses for subscription-mode
execution. Subscription tiers gate K3 context length (roughly: mid tiers
get 256K, higher tiers the full 1M window).

**Fallback: raw API key.** If you prefer metered platform billing or run
in an environment where the browser OAuth flow is impossible (CI, headless
containers), create a key at [platform.kimi.ai](https://platform.kimi.ai)
and put it in `.env`:

```bash
# .env
MOONSHOT_API_KEY=sk-...
KIMI_AUTH_MODE=api-key
```

The client then talks to `https://api.moonshot.ai/v1` directly with
per-token pricing (kimi-k3: $3.00/M input, $0.30/M cached input, $15.00/M
output as of launch).

### 3. Render something

```bash
# The showcase scene (no model calls needed - it ships with the repo)
uv run manim -qh manim_scenes/k3_harmonic_universe.py K3HarmonicUniverse

# The full pipeline (needs auth from step 2)
uv run python -m k3_agents.supervisor "fourier series"
```

---

## Configuration reference

All configuration lives in [config.py](config.py) and is overridable via
environment variables or `.env`:

| Variable | Default | Purpose |
|---|---|---|
| `KIMI_AUTH_MODE` | `subscription` | `subscription` = Kimi Code CLI OAuth via the Agent SDK; `api-key` = raw platform API with `MOONSHOT_API_KEY` |
| `MOONSHOT_API_KEY` | unset | Platform API key; required only in `api-key` mode |
| `KIMI_MODEL` | `kimi-k3` | Reasoning model for Scout/Enricher/Designer/Composer/Critic |
| `KIMI_MODEL_CODE` | `kimi-k3` | Model for the Manim Coder |
| `KIMI_REASONING_EFFORT` | `max` | K3 reasoning effort (`max` is the only accepted value at launch) |
| `KIMI_MAX_TOKENS` | `8192` | Default completion budget per call |
| `KIMI_USE_TOOLS` | `true` | Tool calling for legacy K2-era code paths |

K3 API behavior worth knowing (handled automatically by
[kimi_client.py](kimi_client.py)):

- `temperature` and `top_p` are **fixed server-side** on `kimi-k3`
  (1.0 / 0.95); the client strips them from requests.
- Thinking is **always on**; the reasoning trace comes back in a separate
  `reasoning_content` field, which the client surfaces alongside `content`.
- Prompt prefixes are cached automatically by the platform; the agents
  share a byte-stable system preamble to exploit the 10x cheaper
  cache-hit input pricing.

---

## Project structure

```
k3_agents/            The swarm: six agents + deterministic supervisor
schemas/              Pydantic artifacts and strict json_schema export
manim_scenes/         Curated scenes, including the K3 showcase
kimi_client.py        OpenAI-compatible client with K3 parameter handling
config.py             Environment-driven configuration
agents/               Legacy K2 4-stage pipeline (kept for reference)
tool_adapter.py       Legacy prompt-based tool fallback (superseded)
e2b_sandbox/          Optional sandboxed rendering environment
docs/                 Architecture notes and the K3 rebuild plan
output/, media/       Run artifacts and rendered videos (gitignored)
```

## Legacy: the K2 pipeline

The original 4-stage pipeline (Prerequisite Explorer, Mathematical
Enricher, Visual Designer, Narrative Composer over a recursive
`KnowledgeNode` tree with tool-calling and text-parsing fallbacks) lives in
[agents/](agents/) and remains importable, but Moonshot discontinued the
entire `kimi-k2` model series on May 25, 2026, so it no longer runs against
live models without pointing `KIMI_MODEL` at a current one. The rebuild
rationale, launch-day API research, and phase plan are in
[docs/KIMI_K3_REBUILD_PLAN.md](docs/KIMI_K3_REBUILD_PLAN.md).

## License

MIT - see [LICENSE](LICENSE).

## References

- [Kimi K3 quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Kimi Code CLI](https://github.com/MoonshotAI/kimi-code)
- [Kimi Agent SDK](https://github.com/MoonshotAI/kimi-agent-sdk)
- [Manim Community Edition](https://www.manim.community/)

## Support

Open an issue at
[HarleyCoops/KimiK3Manim](https://github.com/HarleyCoops/KimiK3Manim/issues).
