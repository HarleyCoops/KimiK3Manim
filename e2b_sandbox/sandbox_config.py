"""
E2B Sandbox Configuration for KimiK2Manim
This module provides utilities for managing the E2B sandbox environment.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class SandboxMode(Enum):
    """Sandbox operation modes."""
    EXPLORATION = "exploration"  # For exploring concepts
    RENDERING = "rendering"  # For rendering animations
    INTERACTIVE = "interactive"  # For interactive sessions
    BATCH = "batch"  # For batch processing


@dataclass
class SandboxConfig:
    """Configuration for E2B sandbox environment."""

    # API Configuration
    moonshot_api_key: str
    moonshot_base_url: str = "https://api.moonshot.ai/v1"
    model: str = "kimi-k3"

    # Thinking Configuration
    thinking_mode: str = "heavy"  # heavy, medium, light
    use_tools: bool = True

    # Sandbox Settings
    mode: SandboxMode = SandboxMode.EXPLORATION
    max_depth: int = 3  # For prerequisite exploration
    max_tokens: int = 8000
    temperature: float = 0.7

    # Output Configuration
    output_dir: str = "/home/user/kimik2/output"
    media_dir: str = "/home/user/kimik2/media"
    log_dir: str = "/home/user/kimik2/logs"

    # Manim Configuration
    manim_quality: str = "l"  # l=low, m=medium, h=high, k=4k
    manim_format: str = "mp4"  # mp4 or gif

    # Resource Limits
    max_render_time: int = 300  # seconds
    max_tree_depth: int = 5
    max_narrative_words: int = 3000

    @classmethod
    def from_env(cls) -> 'SandboxConfig':
        """Create configuration from environment variables."""
        return cls(
            moonshot_api_key=os.getenv("MOONSHOT_API_KEY", ""),
            moonshot_base_url=os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.ai/v1"),
            model=os.getenv("KIMI_MODEL", "kimi-k3"),
            thinking_mode=os.getenv("KIMI_ENABLE_THINKING", "heavy"),
            use_tools=os.getenv("KIMI_USE_TOOLS", "true").lower() == "true",
            mode=SandboxMode(os.getenv("SANDBOX_MODE", "exploration")),
            max_depth=int(os.getenv("MAX_DEPTH", "3")),
            manim_quality=os.getenv("MANIM_QUALITY", "l"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "moonshot_api_key": "***" if self.moonshot_api_key else None,
            "moonshot_base_url": self.moonshot_base_url,
            "model": self.model,
            "thinking_mode": self.thinking_mode,
            "use_tools": self.use_tools,
            "mode": self.mode.value,
            "max_depth": self.max_depth,
            "max_tokens": self.max_tokens,
            "manim_quality": self.manim_quality,
        }


def setup_sandbox_environment(config: Optional[SandboxConfig] = None) -> SandboxConfig:
    """
    Set up the E2B sandbox environment with proper configuration.

    Args:
        config: Optional pre-configured SandboxConfig

    Returns:
        Configured SandboxConfig instance
    """
    if config is None:
        config = SandboxConfig.from_env()

    # Ensure directories exist
    os.makedirs(config.output_dir, exist_ok=True)
    os.makedirs(config.media_dir, exist_ok=True)
    os.makedirs(config.log_dir, exist_ok=True)

    # Set environment variables for the application
    os.environ["MOONSHOT_API_KEY"] = config.moonshot_api_key
    os.environ["MOONSHOT_BASE_URL"] = config.moonshot_base_url
    os.environ["KIMI_MODEL"] = config.model
    os.environ["KIMI_ENABLE_THINKING"] = config.thinking_mode
    os.environ["KIMI_USE_TOOLS"] = "true" if config.use_tools else "false"

    return config


def validate_sandbox_config(config: SandboxConfig) -> bool:
    """
    Validate sandbox configuration.

    Args:
        config: SandboxConfig to validate

    Returns:
        True if valid, raises ValueError otherwise
    """
    if not config.moonshot_api_key:
        raise ValueError("MOONSHOT_API_KEY is required")

    if config.thinking_mode not in ["heavy", "medium", "light", "true", "false"]:
        raise ValueError(f"Invalid thinking_mode: {config.thinking_mode}")

    if config.manim_quality not in ["l", "m", "h", "k"]:
        raise ValueError(f"Invalid manim_quality: {config.manim_quality}")

    if config.max_depth < 1 or config.max_depth > 10:
        raise ValueError(f"max_depth must be between 1 and 10, got {config.max_depth}")

    return True
