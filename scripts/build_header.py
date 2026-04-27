"""End-to-end: Layer 1 cleanup + Layer 2 header assembly.

Usage:
    python scripts/build_header.py <out.png> <fig1> [<fig2> ... <figN>]

Inputs are raw patent figure images (PNG/JPEG) — typically a USPTO sheet
straight out of the PDF. Each input is run through Layer 1 (crop.process)
and then Layer 2 normalises the results by label height, composes them
horizontally, and fits them to the 5:2 canvas.

Always raises if any input's "Fig. N" label fails detection — there is no
silent height fallback (see assemble.py docstring).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from figure.assemble import AssembleConfig, build_header, save  # noqa: E402
from figure.crop import CropConfig, load, process                # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    out_path = Path(argv[0])
    inputs = [Path(p) for p in argv[1:]]
    if not 1 <= len(inputs) <= 4:
        print(f"build_header: expected 1–4 input figures, got {len(inputs)}",
              file=sys.stderr)
        return 2

    crop_cfg = CropConfig()
    asm_cfg = AssembleConfig()

    cleaned: list = []
    for src in inputs:
        arr = load(src)
        out, _ = process(arr, crop_cfg)
        cleaned.append(out)
        print(f"  cleaned  {src.name:40s} -> shape={out.shape}")

    header, report = build_header(
        cleaned, asm_cfg, sources=[p.name for p in inputs])
    save(header, out_path)

    print()
    print(f"label heights      : {list(report.label_heights_px)}")
    print(f"target label height: {report.target_label_height_px}")
    print(f"canvas             : {report.canvas_size_px[0]}x{report.canvas_size_px[1]}")
    print(f"output             : {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
