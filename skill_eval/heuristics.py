"""Description-driven heuristics shared by the offline router and improver.

These are deterministic stand-ins for the LLM. They read trigger terms and
scope ("NOT ...") boundaries straight out of the description, so editing the
description measurably changes their behaviour — which is what lets
improve_description.py show real movement even with no API key.
"""

from __future__ import annotations

import re

# Hangul syllables.
_CJK = r"[가-힣]+"
_TOKEN = re.compile(r"[A-Za-z][A-Za-z\-']*|" + _CJK)

_STOPWORDS = {
    "the", "this", "that", "with", "into", "from", "your", "make", "give",
    "want", "need", "please", "about", "some", "have", "show", "tell", "just",
    "for", "and", "out", "our", "all", "can", "you", "one", "use", "even",
    "without", "word", "draft", "first", "based", "core", "turn", "put",
    "이", "그", "저", "좀", "줘", "해줘", "만들어줘", "하나",
}


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text)


def extract_triggers(description: str) -> set[str]:
    """Trigger phrases the skill should fire on, parsed from the description."""
    trigs: set[str] = set()

    # The enumerated list after "asks for ..." up to the next sentence break.
    m = re.search(
        r"asks?\s+for(?:\s+(?:a|an|the))?(.*?)(?:\.|even without|picks|use when)",
        description,
        re.I | re.S,
    )
    segment = m.group(1) if m else description
    for part in re.split(r",|\bor\b|\band\b", segment):
        phrase = part.strip().strip("\"'").lower()
        phrase = re.sub(r"^(a|an|the)\s+", "", phrase)
        if 2 <= len(phrase) <= 30:
            trigs.add(phrase)

    # Any Hangul run in the description is almost certainly a trigger term.
    for run in re.findall(_CJK, description):
        if len(run) >= 2:
            trigs.add(run.lower())

    if "thread" in description.lower():
        trigs.add("thread")

    # Pick up an explicit "also triggers ... : a, b, c" extension list (added by
    # the offline improver) so multi-round improvement compounds.
    for m2 in re.finditer(
        r"(?:also triggers[^:]*:|triggers when the user asks for[^:]*:)(.*?)(?:\.|$)",
        description,
        re.I | re.S,
    ):
        for part in re.split(r",|\bor\b", m2.group(1)):
            phrase = part.strip().strip("\"'").lower()
            if 2 <= len(phrase) <= 30:
                trigs.add(phrase)

    return {t for t in trigs if t and t not in {"a", "an", "the"}}


def extract_negatives(description: str) -> set[str]:
    """Out-of-scope phrases, parsed from 'NOT ...' / 'does not apply to ...'."""
    negs: set[str] = set()
    for m in re.findall(r"\bNOT\s+(?:a |an )?([A-Za-z][A-Za-z\- ]+?)(?:\s*\(|,|\.|$)", description):
        phrase = m.strip().lower()
        if phrase:
            negs.add(phrase)
    for m in re.finditer(r"does not apply to[^:]*:(.*?)(?:\.|$)", description, re.I | re.S):
        for part in re.split(r",|\bor\b", m.group(1)):
            phrase = part.strip().strip("\"'").lower()
            if phrase:
                negs.add(phrase)
    return negs


def heuristic_predict(triggers: set[str], negatives: set[str], prompt: str) -> tuple[bool, float, str]:
    """Predict whether the skill fires. Scope (NOT) overrides a trigger match."""
    low = prompt.lower()
    matched = sorted(t for t in triggers if t in low)
    neg_matched = sorted(n for n in negatives if n in low)

    if neg_matched:
        return (
            False,
            0.9,
            f"out-of-scope marker {neg_matched!r} present; scope overrides",
        )
    if matched:
        return True, min(0.95, 0.6 + 0.1 * len(matched)), f"matched trigger(s) {matched!r}"
    return False, 0.7, "no trigger term from the description appears in the prompt"
