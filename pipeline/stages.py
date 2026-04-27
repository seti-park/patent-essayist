"""Pure stage functions for the patent extraction pipeline.

Each function is a `Value -> Value` (or `Value -> Result[Value, Failure]`)
transformation. I/O is confined to `read_pages`; everything downstream is
deterministic and testable from in-memory inputs.
"""

from __future__ import annotations

import re
from pathlib import Path

import pymupdf
import pymupdf4llm
from returns.result import Failure, Result, Success

from .models import Claim, Markdown, PatentDoc, PdfKind, RawPage, Section

# Lazy import: only construct the OCR engine when a scanned page demands it.
_OCR_SINGLETON = None


def _ocr_engine():
    global _OCR_SINGLETON
    if _OCR_SINGLETON is None:
        from rapidocr_onnxruntime import RapidOCR
        _OCR_SINGLETON = RapidOCR()
    return _OCR_SINGLETON


# ----------------------------- I/O boundary -----------------------------

# Heuristic: if a page yields fewer than this many extracted characters, it is
# probably image-only and needs OCR.
_OCR_THRESHOLD = 40


def read_pages(path: Path) -> Result[tuple[RawPage, ...], str]:
    """Open a PDF and return one `RawPage` per page. Pure-ish: the only side
    effect is the file read; everything else is in-memory data."""
    try:
        per_page = pymupdf4llm.to_markdown(str(path), page_chunks=True)
    except Exception as e:  # noqa: BLE001  — surface as Failure for the pipeline
        return Failure(f"pymupdf4llm failed: {e}")

    pages: list[RawPage] = []
    for i, chunk in enumerate(per_page):
        text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
        pages.append(RawPage(
            index=i,
            text=text,
            char_count=len(text.strip()),
            needs_ocr=len(text.strip()) < _OCR_THRESHOLD,
        ))
    return Success(tuple(pages))


def ocr_fallback(path: Path,
                 pages: tuple[RawPage, ...]) -> tuple[RawPage, ...]:
    """For every page that `read_pages` flagged as `needs_ocr=True`, run an
    image-based OCR engine and produce a new `RawPage` with the recognised
    text. Pages that already have text pass through unchanged."""
    if not any(p.needs_ocr for p in pages):
        return pages

    doc = pymupdf.open(path)
    try:
        engine = _ocr_engine()
        out: list[RawPage] = []
        for p in pages:
            if not p.needs_ocr:
                out.append(p)
                continue
            pix = doc[p.index].get_pixmap(dpi=200)
            result, _ = engine(pix.tobytes("png"))
            text = "\n".join(line[1] for line in (result or []))
            out.append(RawPage(
                index=p.index,
                text=text,
                char_count=len(text.strip()),
                # Keep needs_ocr as a provenance flag so render() can mark it.
                needs_ocr=True,
            ))
        return tuple(out)
    finally:
        doc.close()


# ----------------------------- pure stages -----------------------------

def classify(pages: tuple[RawPage, ...]) -> PdfKind:
    needs = sum(1 for p in pages if p.needs_ocr)
    if needs == 0:
        return PdfKind.NATIVE
    if needs == len(pages):
        return PdfKind.SCANNED
    return PdfKind.MIXED


def detect_language(pages: tuple[RawPage, ...]) -> str:
    """Cheap language tag: any Hangul present -> 'ko', else 'en'."""
    blob = " ".join(p.text for p in pages)
    return "ko" if re.search(r"[가-힣]", blob) else "en"


# Section-header patterns are matched against the *whole* normalised line, so
# they will not accidentally fire on body lines like "청구항 1." or
# "Claim 3 recites...". Each entry is anchored end-to-end.
_HEADER_TAIL = r"\s*[:：.]?\s*$"
_SECTION_PATTERNS = {
    "abstract":    [r"\(?57\)?\s*Abstract" + _HEADER_TAIL,
                    r"Abstract" + _HEADER_TAIL,
                    r"\(?57\)?\s*요\s*약" + _HEADER_TAIL,
                    r"요\s*약" + _HEADER_TAIL],
    "claims":      [r"Claims?" + _HEADER_TAIL,
                    r"청\s*구\s*항" + _HEADER_TAIL,
                    r"WHAT\s+IS\s+CLAIMED(\s+IS)?" + _HEADER_TAIL],
    "description": [r"Detailed\s+Description" + _HEADER_TAIL,
                    r"Description" + _HEADER_TAIL,
                    r"Specification" + _HEADER_TAIL,
                    r"발명의?\s*상세한?\s*설명" + _HEADER_TAIL,
                    r"명\s*세\s*서" + _HEADER_TAIL],
    "drawings":    [r"Brief\s+Description\s+of\s+(the\s+)?Drawings" + _HEADER_TAIL,
                    r"도\s*면(의?\s*간단한?\s*설명)?" + _HEADER_TAIL],
}

_TITLE_RE = re.compile(r"\(54\)\s*([^\n]{4,200})")
_MD_DECOR = re.compile(r"^[#>\s\*\-_]+|[\*\s]+$")


def _strip_md(line: str) -> str:
    """Remove leading `#`/`*`/whitespace and trailing `*`/whitespace so that
    section-header detection works regardless of how the upstream extractor
    decorated the heading (`## **Claims**`, `**Claims**`, `Claims`, ...)."""
    return _MD_DECOR.sub("", line).strip()


def segment(pages: tuple[RawPage, ...]) -> tuple[Section, ...]:
    """Split the concatenated text into known patent sections.

    Algorithm: walk lines; when a normalised line matches a section pattern,
    change the current section. Lines before any header belong to 'title' if
    (54) is present, else are dropped. Intentionally simple — easy to extend
    one regex at a time as we encounter new patent layouts.
    """
    text = "\n".join(p.text for p in pages)

    title_match = _TITLE_RE.search(text)
    sections: dict[str, list[str]] = {"title": [], "abstract": [], "claims": [],
                                       "description": [], "drawings": []}
    if title_match:
        title = title_match.group(1).strip().rstrip("*").strip()
        sections["title"].append(title)

    current = "description"
    seen_header = False
    for line in text.splitlines():
        normalised = _strip_md(line)
        # Skip the (54) title line entirely — the title was already extracted.
        if title_match and "(54)" in normalised:
            continue
        bumped = False
        for name, patterns in _SECTION_PATTERNS.items():
            if any(re.fullmatch(p, normalised, re.IGNORECASE) for p in patterns):
                current = name
                seen_header = True
                bumped = True
                break
        if bumped:
            continue
        if not seen_header and not title_match:
            continue
        sections[current].append(line)

    return tuple(
        Section(name=name, body="\n".join(lines).strip())
        for name, lines in sections.items() if "".join(lines).strip()
    )


_CLAIM_HEAD = re.compile(
    r"(?:^|\n)\s*(?:\*\*)?(?:청구항\s*)?(\d{1,3})\.\s*(?:\*\*)?\s*",
    re.MULTILINE,
)
_DEP_RE = re.compile(
    r"(?:claim|claims|제\s*)\s*(\d{1,3})(?:\s*(?:to|or|-|–|및|또는|항)\s*(\d{1,3}))?(?:\s*항)?",
    re.IGNORECASE,
)


def parse_claims(claims_section_body: str) -> tuple[Claim, ...]:
    """Split a claims block into numbered claims and extract dependencies."""
    if not claims_section_body:
        return ()

    # Find positions of every claim head and slice between them
    heads = list(_CLAIM_HEAD.finditer(claims_section_body))
    if not heads:
        return ()

    out: list[Claim] = []
    for i, m in enumerate(heads):
        n = int(m.group(1))
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(claims_section_body)
        text = claims_section_body[start:end].strip()
        deps: list[int] = []
        for dm in _DEP_RE.finditer(text):
            a = int(dm.group(1))
            b = int(dm.group(2)) if dm.group(2) else a
            if a == n:           # self-reference is noise
                continue
            deps.extend(range(min(a, b), max(a, b) + 1))
        out.append(Claim(number=n, text=text, depends_on=tuple(sorted(set(deps)))))
    return tuple(out)


def assemble(path: Path,
             pages: tuple[RawPage, ...],
             sections: tuple[Section, ...],
             claims: tuple[Claim, ...]) -> PatentDoc:
    return PatentDoc(
        source_path=str(path),
        kind=classify(pages),
        language=detect_language(pages),
        sections=sections,
        claims=claims,
        page_count=len(pages),
        needs_ocr_pages=tuple(p.index for p in pages if p.needs_ocr),
    )


# ----------------------------- rendering -----------------------------

def render(doc: PatentDoc) -> Markdown:
    src_name = Path(doc.source_path).name
    lines: list[str] = []

    title = next((s.body for s in doc.sections if s.name == "title"), "(untitled)")
    lines.append(f"# {title}\n")
    lines.append(f"<!-- source: {src_name} | kind: {doc.kind.value} | "
                 f"lang: {doc.language} | pages: {doc.page_count} -->\n")

    if doc.kind == PdfKind.SCANNED or doc.needs_ocr_pages:
        lines.append("> **OCR required.** Pages without an extractable text "
                     f"layer: {list(doc.needs_ocr_pages)}. The output below "
                     "reflects only the digital text that was recoverable.\n")

    for name in ("abstract", "description", "drawings"):
        body = next((s.body for s in doc.sections if s.name == name), None)
        if body:
            lines.append(f"## {name.capitalize()}\n\n{body}\n")

    if doc.claims:
        lines.append("## Claims\n")
        for c in doc.claims:
            dep = f"  *(depends on {list(c.depends_on)})*" if c.depends_on else ""
            lines.append(f"**{c.number}.** {c.text}{dep}\n")

    return Markdown(source_path=doc.source_path, text="\n".join(lines).rstrip() + "\n")
