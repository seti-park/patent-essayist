"""Immutable data model for the patent extraction pipeline.

Every type is frozen so that stage functions stay pure: a stage receives a
value, returns a new value, never mutates.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class PdfKind(str, Enum):
    NATIVE = "native"      # has embedded text on every page
    SCANNED = "scanned"    # image-only pages, OCR required
    MIXED = "mixed"        # some pages text, some image


class RawPage(Frozen):
    index: int             # 0-based page index
    text: str              # markdown-ish text from the extractor
    char_count: int
    needs_ocr: bool = False


class Claim(Frozen):
    number: int
    text: str
    depends_on: tuple[int, ...] = Field(default_factory=tuple)


class Section(Frozen):
    name: Literal["title", "abstract", "claims", "description", "drawings"]
    body: str


class PatentDoc(Frozen):
    source_path: str
    kind: PdfKind
    language: str = "en"
    sections: tuple[Section, ...] = Field(default_factory=tuple)
    claims: tuple[Claim, ...] = Field(default_factory=tuple)
    page_count: int = 0
    needs_ocr_pages: tuple[int, ...] = Field(default_factory=tuple)


class Markdown(Frozen):
    source_path: str
    text: str
