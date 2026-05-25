"""Run the patent pipeline over every sample PDF and write Markdown outputs.

Also prints a one-line per-sample report so the user can eyeball
extractor recall (claim count vs. ground truth, OCR detection, etc.)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.pipe import extract  # noqa: E402
from pipeline.stages import render  # noqa: E402

SAMPLES = ROOT / "data" / "samples"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> int:
    pdfs = sorted(SAMPLES.glob("*.pdf"))
    if not pdfs:
        print(f"no PDFs in {SAMPLES}", file=sys.stderr)
        return 1

    print(f"{'sample':<26} {'kind':<8} {'lang':<4} {'pages':>5} "
          f"{'claims':>6} {'truth':>5} {'ocr?':>5}")
    print("-" * 72)

    for pdf in pdfs:
        truth_path = pdf.with_suffix(".truth.json")
        truth = json.loads(truth_path.read_text()) if truth_path.exists() else {}

        result = extract(pdf)
        if not result:
            err = result.failure() if hasattr(result, "failure") else "?"
            print(f"{pdf.name:<26} FAILED: {err}")
            continue

        doc = result.unwrap()
        md = render(doc)
        (OUT / (pdf.stem + ".md")).write_text(md.text, encoding="utf-8")

        print(f"{pdf.name:<26} {doc.kind.value:<8} {doc.language:<4} "
              f"{doc.page_count:>5} {len(doc.claims):>6} "
              f"{truth.get('claims_count','?'):>5} "
              f"{('Y' if doc.needs_ocr_pages else '-'):>5}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
