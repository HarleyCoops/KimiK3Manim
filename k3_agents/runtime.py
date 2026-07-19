"""Subscription-mode execution via the Kimi Agent SDK.

The default auth mode is a Kimi subscription: the user logs in once with
the Kimi Code CLI (`kimi` -> /login -> Kimi Code OAuth) and the Agent SDK
reuses those credentials automatically - no API key ever touches this
repository.

The SDK exposes an agent runtime rather than raw chat completions, so
structured output is enforced here by instruction plus Pydantic
validation with one retry, instead of the API-level json_schema contract
used in api-key mode.
"""

from __future__ import annotations

import asyncio
import json
import re
import shutil
from typing import Optional, Type

from pydantic import BaseModel


def subscription_available() -> tuple[bool, str]:
    """Check whether subscription-mode execution can work here.

    Returns (ok, reason_if_not).
    """
    try:
        import kimi_agent_sdk  # noqa: F401
    except ImportError:
        return False, (
            "kimi-agent-sdk is not installed (uv add kimi-agent-sdk)"
        )
    if shutil.which("kimi") is None:
        return False, (
            "the Kimi Code CLI is not on PATH; install it with "
            "'curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash' "
            "and log in once with /login (Kimi Code OAuth)"
        )
    return True, ""


def _extract_json(text: str) -> str:
    """Pull the first JSON object out of an agent reply."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        return fenced.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start:end + 1]
    return text


async def _prompt_once(full_prompt: str, model: Optional[str]) -> str:
    from kimi_agent_sdk import prompt  # imported lazily

    kwargs = {"yolo": False}
    chunks: list[str] = []
    async for msg in prompt(full_prompt, **kwargs):
        part = msg.extract_text()
        if part:
            chunks.append(part)
    return "".join(chunks)


def run_structured(
    user_content: str,
    system: str,
    output_model: Type[BaseModel],
    model: Optional[str] = None,
    retries: int = 1,
) -> BaseModel:
    """Run one structured-output agent turn through the subscription runtime."""
    ok, reason = subscription_available()
    if not ok:
        raise RuntimeError(
            f"Subscription mode unavailable: {reason}. Either complete the "
            f"Kimi Code CLI login or set KIMI_AUTH_MODE=api-key with a "
            f"MOONSHOT_API_KEY."
        )

    schema = json.dumps(output_model.model_json_schema(), indent=2)
    full_prompt = (
        f"{system}\n\n{user_content}\n\n"
        "Respond with ONLY a JSON object (no prose, no code fences) that "
        f"validates against this JSON schema:\n{schema}"
    )

    last_error: Optional[Exception] = None
    attempt_prompt = full_prompt
    for _ in range(retries + 1):
        text = asyncio.run(_prompt_once(attempt_prompt, model))
        try:
            return output_model.model_validate(json.loads(_extract_json(text)))
        except Exception as exc:  # json or validation failure -> retry once
            last_error = exc
            attempt_prompt = (
                full_prompt
                + f"\n\nYour previous reply failed validation with: {exc}. "
                "Reply again with ONLY the corrected JSON object."
            )
    raise ValueError(
        f"Subscription runtime returned unparseable output: {last_error}"
    )
