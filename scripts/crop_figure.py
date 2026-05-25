"""Clean a single patent-figure image: header trim → tight crop → padding.

Usage:
    python scripts/crop_figure.py <in.png> [<out.png>]
If <out.png> is omitted, writes <in.stem>.cropped.png next to the input.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from figure.crop import CropConfig, load, process, save  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2

    src = Path(argv[0])
    dst = Path(argv[1]) if len(argv) > 1 else src.with_suffix(".cropped.png")

    arr = load(src)
    out, report = process(arr, CropConfig())
    save(out, dst)

    print(f"input        : {src}  shape={report.in_shape}")
    print(f"orientation  : {report.orientation.value}")
    print(f"header trim  : side={report.trim.side.value}  "
          f"cut={report.trim.cut_at}px  band={report.trim.band_extent}")
    print(f"output       : {dst}  shape={report.out_shape}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
