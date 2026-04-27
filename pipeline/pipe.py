"""Compose the stage functions into an end-to-end pipeline.

Style: explicit `Result` plumbing, each step is a small named function.
`returns.pipeline.flow` would let us write this point-free, but spelled out
the data flow is easier to read for new contributors.
"""

from __future__ import annotations

from pathlib import Path

from returns.result import Failure, Result, Success

from .models import Markdown, PatentDoc
from .stages import (
    assemble,
    ocr_fallback,
    parse_claims,
    read_pages,
    render,
    segment,
)


def extract(path: Path) -> Result[PatentDoc, str]:
    """Parse a PDF into a fully assembled `PatentDoc`.

    The pipeline is `read -> ocr_fallback -> _build_doc`. Each step is a
    function on values; `Result.map` threads success through and short-
    circuits on failure."""
    return (
        read_pages(path)
        .map(lambda pages: ocr_fallback(path, pages))
        .map(lambda pages: _build_doc(path, pages))
    )


def _build_doc(path: Path, pages) -> PatentDoc:
    sections = segment(pages)
    claims_body = next((s.body for s in sections if s.name == "claims"), "")
    claims = parse_claims(claims_body)
    return assemble(path, pages, sections, claims)


def to_markdown(path: Path) -> Result[Markdown, str]:
    return extract(path).map(render)
