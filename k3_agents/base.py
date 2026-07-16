"""Shared machinery for K3 pipeline agents.

Every agent is one K3 chat session that must answer with a single strict
json_schema artifact. A shared static system preamble is prepended to every
agent's prompt so the platform's automatic prefix caching turns repeat runs
into cache hits.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

try:
    from ..kimi_client import KimiClient
    from ..schemas import k3_response_format
except ImportError:
    from kimi_client import KimiClient
    from schemas import k3_response_format

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
    """Base class: one structured-output K3 call per invocation."""

    name: str = "k3-agent"
    output_model: Type[BaseModel]

    def __init__(self, client: Optional[KimiClient] = None, model: Optional[str] = None):
        if client is not None:
            self.client = client
        else:
            self.client = KimiClient(model=model) if model else KimiClient()

    def system_prompt(self) -> str:
        raise NotImplementedError

    def call(
        self,
        user_content: Any,
        max_tokens: int = 32768,
    ) -> BaseModel:
        """Run the agent once and return the validated artifact."""
        messages: List[Dict[str, Any]] = [{"role": "user", "content": user_content}]
        response = self.client.chat_completion(
            messages=messages,
            system=PIPELINE_PREAMBLE + "\n" + self.system_prompt(),
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
