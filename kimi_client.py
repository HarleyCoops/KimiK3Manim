"""Kimi API Client - OpenAI-compatible wrapper.

This module provides a client for the Kimi models from Moonshot AI
(kimi-k3 flagship and the kimi-k2.x series). The API is OpenAI-compatible.

K3-specific behavior handled here:
- temperature/top_p are fixed server-side on kimi-k3 and must not be sent
- reasoning_effort is a top-level request field (thinking is always on)
- max_completion_tokens replaces max_tokens
- responses may carry reasoning_content alongside content
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Union

from openai import OpenAI

# Import config - works both as package and standalone
try:
    from .config import (
        DEFAULT_MAX_TOKENS,
        DEFAULT_TEMPERATURE,
        DEFAULT_TOP_P,
        KIMI_MODEL,
        KIMI_REASONING_EFFORT,
        MOONSHOT_API_KEY,
        MOONSHOT_BASE_URL,
        is_k3_model,
    )
    from .logger import get_logger
except ImportError:
    from config import (
        DEFAULT_MAX_TOKENS,
        DEFAULT_TEMPERATURE,
        DEFAULT_TOP_P,
        KIMI_MODEL,
        KIMI_REASONING_EFFORT,
        MOONSHOT_API_KEY,
        MOONSHOT_BASE_URL,
        is_k3_model,
    )
    from logger import get_logger


class KimiClient:
    """
    Client for Kimi models from Moonshot AI.

    Uses OpenAI-compatible API format for easy integration.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        reasoning_effort: Optional[str] = None,
        logger=None,
    ):
        """
        Initialize Kimi client.

        Args:
            api_key: Moonshot API key (defaults to MOONSHOT_API_KEY env var)
            base_url: API base URL (defaults to Moonshot endpoint)
            model: Model name (defaults to KIMI_MODEL, i.e. kimi-k3)
            reasoning_effort: K3 reasoning effort (defaults to KIMI_REASONING_EFFORT)
            logger: Logger instance (defaults to global logger)
        """
        self.api_key = api_key or MOONSHOT_API_KEY
        if not self.api_key:
            raise ValueError(
                "MOONSHOT_API_KEY environment variable not set. "
                "Please set it in your .env file or pass api_key parameter."
            )

        # Ensure API key doesn't have extra whitespace
        self.api_key = self.api_key.strip()

        self.base_url = base_url or MOONSHOT_BASE_URL
        self.model = model or KIMI_MODEL
        self.reasoning_effort = reasoning_effort or KIMI_REASONING_EFFORT
        self.logger = logger or get_logger()

        # Initialize OpenAI client with Moonshot endpoint
        # The OpenAI client automatically adds "Bearer " prefix to the API key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system: System prompt (will be prepended to messages)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (ignored on kimi-k3, fixed at 1.0)
            top_p: Nucleus sampling parameter (ignored on kimi-k3, fixed at 0.95)
            tools: List of tool definitions for function calling
            tool_choice: Tool choice mode ('auto', 'required', 'none', or specific tool)
            response_format: Structured output spec, e.g.
                {"type": "json_schema", "json_schema": {..., "strict": True}}
            stream: Whether to stream the response
            **kwargs: Additional parameters passed to API

        Returns:
            Response dict with 'choices', 'usage', etc.
        """
        # Prepare messages
        api_messages = []
        if system:
            api_messages.append({"role": "system", "content": system})
        api_messages.extend(messages)

        k3 = is_k3_model(self.model)

        params: Dict[str, Any] = {
            "model": self.model,
            "messages": api_messages,
            "stream": stream,
            **kwargs,
        }
        if k3:
            # K3: sampling params are fixed server-side; sending them is an
            # error. Thinking is always on; only effort is tunable.
            params["max_completion_tokens"] = max_tokens
            params["reasoning_effort"] = self.reasoning_effort
        else:
            params["max_tokens"] = max_tokens
            params["temperature"] = temperature
            params["top_p"] = top_p

        # Add tools if provided
        if tools:
            params["tools"] = tools
            if tool_choice:
                params["tool_choice"] = tool_choice
        if response_format:
            params["response_format"] = response_format

        # Prepare logging details
        details = {
            "Messages": f"{len(api_messages)} message(s)",
            "Max tokens": str(max_tokens),
        }
        if k3:
            details["Reasoning effort"] = self.reasoning_effort
        else:
            details["Temperature"] = str(temperature)
        if system:
            details["System prompt"] = f"{system[:100]}..."
        if messages:
            details["User message"] = f"{messages[0]['content'][:150]}..."
        if tools:
            details["Tools"] = f"{len(tools)} tool(s) available"
        if tool_choice:
            details["Tool choice"] = str(tool_choice)

        # Make API call with logging
        call_info = {}
        try:
            with self.logger.api_call(self.model, details=details, show_spinner=True) as call_info:
                response = self.client.chat.completions.create(**params)

                if not stream:
                    formatted = self._format_response(response)
                    usage = formatted.get("usage")
                    if usage:
                        call_info['usage'] = usage
        except Exception as e:
            # Provide more helpful error message for authentication issues
            error_msg = str(e)
            if "401" in error_msg or "Invalid Authentication" in error_msg or "AuthenticationError" in str(type(e)):
                self.logger.error("Authentication failed (401)")
                raise ValueError(
                    f"Authentication failed (401). Please verify:\n"
                    f"1. Your MOONSHOT_API_KEY is valid and active at https://platform.kimi.ai/\n"
                    f"2. The API key is correctly set in your .env file (no extra spaces)\n"
                    f"3. Your Moonshot account has API access enabled\n"
                    f"4. The API endpoint is correct: {self.base_url}\n"
                    f"5. Check if your API key has expired or been revoked\n"
                    f"\nOriginal error: {error_msg}"
                ) from e
            if "model" in error_msg.lower() and ("not found" in error_msg.lower() or "invalid" in error_msg.lower()):
                raise ValueError(
                    f"Model '{self.model}' was rejected by the API. The kimi-k2 "
                    f"series was discontinued 2026-05-25; use kimi-k3 or "
                    f"kimi-k2.6+. Original error: {error_msg}"
                ) from e
            raise

        # Convert response to dict format
        if stream:
            return response  # Return stream object as-is
        else:
            text_content = self.get_text_content(formatted)
            tool_calls = None
            if self.has_tool_calls(formatted):
                tool_calls = self.get_tool_calls(formatted)

            # Add debug info if verbose
            if self.logger.verbose:
                if text_content:
                    self.logger.debug(f"Response length: {len(text_content)} chars, preview: {text_content[:100]}...")
                if tool_calls:
                    for i, tc in enumerate(tool_calls):
                        func_name = tc.get("function", {}).get("name", "unknown")
                        self.logger.debug(f"Tool call {i+1}: {func_name}")

            return formatted

    def _format_response(self, response) -> Dict[str, Any]:
        """Format OpenAI response to consistent dict format."""
        choice = response.choices[0]
        message = choice.message

        result = {
            "id": response.id,
            "model": response.model,
            "choices": [{
                "index": choice.index,
                "message": {
                    "role": message.role,
                    "content": message.content,
                },
                "finish_reason": choice.finish_reason,
            }],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            } if response.usage else None,
        }

        # K3 returns the thinking trace as reasoning_content
        reasoning = getattr(message, "reasoning_content", None)
        if reasoning:
            result["choices"][0]["message"]["reasoning_content"] = reasoning

        # Handle tool calls if present
        if hasattr(message, "tool_calls") and message.tool_calls:
            result["choices"][0]["message"]["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in message.tool_calls
            ]

        return result

    def get_text_content(self, response: Dict[str, Any]) -> str:
        """Extract text content from response."""
        if "choices" in response and len(response["choices"]) > 0:
            message = response["choices"][0].get("message", {})
            return message.get("content", "") or ""
        return ""

    def get_reasoning_content(self, response: Dict[str, Any]) -> str:
        """Extract the K3 thinking trace from a response, if present."""
        if "choices" in response and len(response["choices"]) > 0:
            message = response["choices"][0].get("message", {})
            return message.get("reasoning_content", "") or ""
        return ""

    def has_tool_calls(self, response: Dict[str, Any]) -> bool:
        """Check if response contains tool calls."""
        if "choices" in response and len(response["choices"]) > 0:
            message = response["choices"][0].get("message", {})
            return "tool_calls" in message and len(message.get("tool_calls", [])) > 0
        return False

    def get_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool calls from response."""
        if not self.has_tool_calls(response):
            return []

        message = response["choices"][0]["message"]
        return message.get("tool_calls", [])


# Singleton instance
_kimi_client: Optional[KimiClient] = None


def get_kimi_client() -> KimiClient:
    """Get or create singleton Kimi client instance."""
    global _kimi_client
    if _kimi_client is None:
        _kimi_client = KimiClient()
    return _kimi_client
