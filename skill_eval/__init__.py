"""Skill-description evaluation toolkit.

Evaluates how well a skill's frontmatter `description` field drives routing:
  - trigger accuracy against a labelled prompt set (precision / recall / F1)
  - a rubric score for the description text itself

Backed by the Anthropic API when ANTHROPIC_API_KEY + the `anthropic` SDK are
available, and a deterministic, description-driven heuristic otherwise so the
scripts run anywhere (CI, sandbox) and stay testable offline.
"""

from .skills import Skill, load_skill, write_description
from .dataset import load_dataset, Example
from .llm import LLMClient
from .evaluate import (
    judge_trigger,
    run_trigger_eval,
    score_rubric,
    TriggerReport,
    RubricReport,
)
from .improve import propose_improved_description

__all__ = [
    "Skill",
    "load_skill",
    "write_description",
    "load_dataset",
    "Example",
    "LLMClient",
    "judge_trigger",
    "run_trigger_eval",
    "score_rubric",
    "TriggerReport",
    "RubricReport",
    "propose_improved_description",
]
