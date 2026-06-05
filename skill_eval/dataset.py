"""Labelled prompt set: each example is a prompt + whether the skill should fire."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass


@dataclass
class Example:
    id: str
    prompt: str
    should_trigger: bool
    note: str = ""


def load_dataset(path: str) -> list[Example]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"dataset not found: {path}")
    examples: list[Example] = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON ({exc})") from exc
            examples.append(
                Example(
                    id=str(obj.get("id", f"ex{lineno}")),
                    prompt=obj["prompt"],
                    should_trigger=bool(obj["should_trigger"]),
                    note=str(obj.get("note", "")),
                )
            )
    if not examples:
        raise ValueError(f"dataset {path} is empty")
    return examples
