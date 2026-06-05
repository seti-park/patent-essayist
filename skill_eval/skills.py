"""Load and persist a skill's frontmatter (name + description)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str
    raw: str
    path: str  # path to the SKILL.md file


def _resolve_skill_md(path: str) -> str:
    if os.path.isdir(path):
        candidate = os.path.join(path, "SKILL.md")
        if os.path.isfile(candidate):
            return candidate
        raise FileNotFoundError(f"no SKILL.md found in directory {path!r}")
    return path


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_body, rest). frontmatter_body excludes the --- fences."""
    if not text.startswith("---"):
        raise ValueError("SKILL.md does not start with a '---' frontmatter fence")
    # find the closing fence
    m = re.search(r"\n---[ \t]*(?:\n|$)", text[3:])
    if not m:
        raise ValueError("SKILL.md frontmatter is not closed with '---'")
    fm = text[3 : 3 + m.start()].strip("\n")
    rest = text[3 + m.end() :]
    return fm, rest


def _parse_frontmatter(fm: str) -> dict:
    # Prefer a real YAML parser when available; fall back to a minimal one.
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(fm)
        if isinstance(data, dict):
            return {str(k): v for k, v in data.items()}
    except Exception:
        pass

    data: dict = {}
    for line in fm.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        if line[:1] in " \t":  # skip nested / continuation lines in the fallback
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
            value = value[1:-1]
        data[key] = value
    return data


def load_skill(path: str) -> Skill:
    skill_md = _resolve_skill_md(path)
    with open(skill_md, "r", encoding="utf-8") as fh:
        raw = fh.read()
    fm, _ = _split_frontmatter(raw)
    meta = _parse_frontmatter(fm)
    name = str(meta.get("name", "")).strip()
    description = str(meta.get("description", "")).strip()
    if not description:
        raise ValueError(f"{skill_md}: frontmatter has no 'description'")
    return Skill(name=name, description=description, raw=raw, path=skill_md)


def write_description(skill_md_path: str, new_description: str) -> None:
    """Replace the `description:` field in a SKILL.md, leaving the body intact."""
    with open(skill_md_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    head_len = 3  # opening '---'
    m = re.search(r"\n---[ \t]*(?:\n|$)", text[head_len:])
    if not m:
        raise ValueError("cannot locate frontmatter to rewrite")
    fm = text[head_len : head_len + m.start()]
    tail = text[head_len + m.start() :]

    # JSON double-quoting is a valid YAML flow scalar and safely escapes
    # quotes/newlines/backslashes.
    quoted = json.dumps(" ".join(new_description.split()), ensure_ascii=False)
    new_line = f"description: {quoted}"

    # Replace from `description:` up to the next top-level key or end of frontmatter.
    pattern = re.compile(r"(?ms)^description:.*?(?=^[^\s#][^:\n]*:|\Z)")
    if not pattern.search(fm):
        raise ValueError("no 'description:' field found in frontmatter")
    fm_new = pattern.sub(new_line + "\n", fm, count=1).rstrip("\n") + "\n"

    with open(skill_md_path, "w", encoding="utf-8") as fh:
        fh.write(text[:head_len] + fm_new.rstrip("\n") + tail)
