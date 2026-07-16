# Kimi K2 Refactor Setup Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install openai python-dotenv
   ```

2. **Get your API key** from https://platform.moonshot.ai/

3. **Add to `.env` file** (in project root):
   ```
   MOONSHOT_API_KEY=sk-your-key-here
   KIMI_ENABLE_THINKING=heavy  # Optional: "heavy" for max reasoning, "medium", "light", or "true"/"false"
   ```

4. **Test the integration**:
   ```bash
   python KimiK2Thinking/examples/test_kimi_integration.py
   ```

## Configuration Options

All configuration is in `KimiK2Thinking/config.py` or via environment variables:

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)
- `KIMI_MODEL`: Kimi model name (default: `"kimi-k3"`)
- `KIMI_MODEL_CODE`: Code-gen model for Manim Coder (default: `"kimi-k2.7-code"`)
- `KIMI_REASONING_EFFORT`: K3 reasoning effort (default: `"max"`)
- `KIMI_USE_TOOLS`: Enable tool calling (default: "true")
- `KIMI_ENABLE_THINKING`: Legacy K2 thinking toggle; ignored by kimi-k3

## How It Works

### 1. API Client (`kimi_client.py`)
- Wraps OpenAI-compatible API calls to Moonshot AI
- Handles authentication and request formatting
- Returns normalized response format

### 2. Tool Adapter (`tool_adapter.py`)
- Converts tool definitions to verbose instructions
- Used when tools aren't available or enabled
- Maintains functionality without function calling

### 3. Agents (`agents/`)
- Refactored versions of existing agents
- Same interface as Claude versions
- Automatically handle tool vs verbose mode

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the project root:
```bash
cd /path/to/Math-To-Manim
python KimiK2Thinking/examples/test_kimi_integration.py
```

### API Key Not Found
Make sure your `.env` file is in the project root and contains:
```
MOONSHOT_API_KEY=your_key_here
```

### Model Not Found
Use current Kimi models (the kimi-k2 series was discontinued 2026-05-25):
- `kimi-k3` (recommended default for the agent swarm)
- `kimi-k2.7-code` (Manim scene generation)

Update in `.env`:
```
KIMI_MODEL=kimi-k3
KIMI_MODEL_CODE=kimi-k2.7-code
KIMI_REASONING_EFFORT=max
```

## Next Steps

1. Test basic API calls with `test_kimi_integration.py`
2. Try the prerequisite explorer with a simple concept
3. Refactor other agents following the same pattern
4. Compare results with Claude version

