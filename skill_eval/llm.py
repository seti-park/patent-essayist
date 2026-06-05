"""Thin Anthropic-API client with a clear online/offline flag.

When the `anthropic` SDK is importable and ANTHROPIC_API_KEY is set, `online` is
True and `complete_json` calls Claude. Otherwise callers fall back to the
deterministic heuristics in evaluate.py / improve.py.
"""

from __future__ import annotations

import json
import os

DEFAULT_MODEL = "claude-opus-4-8"


class LLMClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._client = None
        self.online = False
        self.reason = ""

        try:
            import anthropic  # noqa: F401
        except ImportError:
            self.reason = "anthropic SDK not installed (pip install anthropic)"
            return

        if not os.environ.get("ANTHROPIC_API_KEY"):
            self.reason = "ANTHROPIC_API_KEY not set"
            return

        try:
            self._client = anthropic.Anthropic()
            self.online = True
            self.reason = f"Anthropic API ({model})"
        except Exception as exc:  # pragma: no cover - defensive
            self.reason = f"anthropic init failed: {exc}"

    @property
    def mode(self) -> str:
        return "online" if self.online else "offline"

    def complete_json(
        self,
        system: str,
        prompt: str,
        schema: dict,
        *,
        effort: str = "high",
        thinking: bool = True,
        max_tokens: int = 8000,
    ) -> dict:
        """Single structured-output call. Raises RuntimeError when offline."""
        if not self.online:
            raise RuntimeError("LLMClient is offline")

        output_config = {
            "effort": effort,
            "format": {"type": "json_schema", "schema": schema},
        }
        kwargs: dict = dict(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            output_config=output_config,
        )
        if thinking:
            kwargs["thinking"] = {"type": "adaptive"}

        resp = self._client.messages.create(**kwargs)
        text = next((b.text for b in resp.content if b.type == "text"), "")
        return json.loads(text)
