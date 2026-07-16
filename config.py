"""Configuration for the Kimi K3 pipeline."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
# Note: The correct endpoint is api.moonshot.ai (not .cn). The docs/console
# site rebranded to platform.kimi.ai in 2026; the API host is unchanged.
MOONSHOT_BASE_URL = "https://api.moonshot.ai/v1"

# Model Configuration
# kimi-k3 (launched 2026-07-16): 1M context, always-on thinking, fixed
# sampling (temperature/top_p must not be sent), reasoning_effort param.
# The kimi-k2 series (including kimi-k2-0905-preview) was discontinued
# 2026-05-25 and no longer resolves.
KIMI_MODEL = os.getenv("KIMI_MODEL", "kimi-k3")
# Code-specialized workhorse for scene generation (cheaper than k3).
KIMI_MODEL_CODE = os.getenv("KIMI_MODEL_CODE", "kimi-k2.7-code")
# Backward-compatible alias; prefer KIMI_MODEL in new code.
KIMI_K2_MODEL = KIMI_MODEL

# Reasoning effort for K3 (thinking cannot be disabled on kimi-k3).
# Only "max" is accepted at launch; more levels are planned.
KIMI_REASONING_EFFORT = os.getenv("KIMI_REASONING_EFFORT", "max")

# Default settings (apply to pre-K3 models only; kimi-k3 has fixed
# temperature=1.0 and top_p=0.95 and rejects overrides)
DEFAULT_MAX_TOKENS = int(os.getenv("KIMI_MAX_TOKENS", "8192"))
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9

# Tool Configuration
USE_TOOLS = os.getenv("KIMI_USE_TOOLS", "true").lower() == "true"
TOOLS_ENABLED = USE_TOOLS  # Can be overridden per agent

# Thinking Mode Configuration (legacy K2 models only).
# kimi-k3 ignores this: thinking is always on and controlled solely by
# KIMI_REASONING_EFFORT.
THINKING_MODE = os.getenv("KIMI_ENABLE_THINKING", "true")
ENABLE_THINKING = THINKING_MODE.lower() not in ("false", "none", "off", "0")

# Fallback to verbose instructions if tools not available
FALLBACK_TO_VERBOSE = True


def is_k3_model(model: str) -> bool:
    """True if the model belongs to the K3 family (fixed sampling params)."""
    return model.startswith("kimi-k3")
