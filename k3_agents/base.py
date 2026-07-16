"""Shared machinery for K3 pipeline agents.

Every agent is one K3 turn that must answer with a single strict
json_schema artifact. Two execution paths, selected by KIMI_AUTH_MODE:

- "subscription" (default): the Kimi Agent SDK runtime, reusing the Kimi
  Code CLI OAuth login. No API key involved.
- "api-key": raw chat completions against api.moonshot.ai with
  MOONSHOT_API_KEY and API-level structured output.

A shared static system preamble is prepended to every agent's prompt so
the platform's automatic prefix caching turns repeat runs into cache hits.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

try:
    from ..config import KIMI_AUTH_MODE, MOONSHOT_API_KEY
    from ..kimi_client import KimiClient
    from ..schemas import k3_response_format
except ImportError:
    from config import KIMI_AUTH_MODE, MOONSHOT_API_KEY
    from kimi_client import KimiClient
    from schemas import k3_response_format

from . import runtime

# Keep this preamble byte-stable across agents and runs: it is the shared
# cacheable prefix ($0.30/M on cache hits vs $3.00/M cold).
PIPELINE_PREAMBLE = """\
You are one specialist agent inside a pipeline that turns a mathematical or
physical concept into a fully rendered Manim animation. Agents communicate
only through strictly validated JSON artifacts; your entire response must be
one artifact matching the provided schema. Be mathematically precise, cite
equations in LaTeX, and never invent fields.
"""


class K3Agent:
    """Base class: one structured-output turn per invocation."""

    name: str = "k3-agent"
    output_model: Type[BaseModel]

    def __init__(self, client: Optional[KimiClient] = None, model: Optional[str] = None):
        self._client = client
        self._model = model

    @property
    def client(self) -> KimiClient:
        """Lazily construct the api-key client (only needed in api-key mode)."""
        if self._client is None:
            self._client = (
                KimiClient(model=self._model) if self._model else KimiClient()
            )
        return self._client

    def system_prompt(self) -> str:
        raise NotImplementedError

    def _use_subscription(self) -> bool:
        # Subscription is the default; an explicitly provided client (e.g.
        # in tests) or api-key mode routes to raw chat completions. A set
        # MOONSHOT_API_KEY acts as fallback when the SDK/CLI is absent.
        if self._client is not None:
            return False
        if KIMI_AUTH_MODE != "subscription":
            return False
        ok, _ = runtime.subscription_available()
        if not ok and MOONSHOT_API_KEY:
            return False  # graceful fallback to api-key mode
        return True

    def call(
        self,
        user_content: Any,
        max_tokens: int = 32768,
    ) -> BaseModel:
        """Run the agent once and return the validated artifact."""
        system = PIPELINE_PREAMBLE + "\n" + self.system_prompt()

        if self._use_subscription():
            if not isinstance(user_content, str):
                # Multimodal content (vision stages) needs the raw API path
                # until the SDK exposes image input; fall back if we can.
                if MOONSHOT_API_KEY:
                    return self._call_api(user_content, system, max_tokens)
                raise RuntimeError(
                    f"Agent '{self.name}' needs image input, which the "
                    "subscription runtime does not accept yet. Set "
                    "MOONSHOT_API_KEY to enable the raw-API fallback for "
                    "vision stages."
                )
            return runtime.run_structured(
                user_content, system, self.output_model, model=self._model
            )

        return self._call_api(user_content, system, max_tokens)

    def _call_api(self, user_content: Any, system: str, max_tokens: int) -> BaseModel:
        messages: List[Dict[str, Any]] = [{"role": "user", "content": user_content}]
        response = self.client.chat_completion(
            messages=messages,
            system=system,
            max_tokens=max_tokens,
            response_format=k3_response_format(self.output_model),
        )
        text = self.client.get_text_content(response)
        if not text or not text.strip():
            choice = response.get("choices", [{}])[0]
            raise RuntimeError(
                f"Model returned empty content "
                f"(finish_reason={choice.get('finish_reason')}, "
                f"usage={response.get('usage')}); likely exhausted the token "
                f"budget on reasoning. Lower the reasoning effort or shrink the prompt."
            )
        return self.output_model.model_validate(json.loads(text))
