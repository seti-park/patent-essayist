#!/usr/bin/env python3
"""Batch patent-figure cleaner for the patent-essay pipeline (Layer-1 cleaning).

Ported from seti-park/patent-essay-pipeline `patent-figures-clean` v2.1 and adapted to
this repo's input contract. Per figure:

    rotate (optional, vision-decided)      # NEW vs the source repo: bring a
                                           # sideways-printed figure body upright
    -> edge trim (vision-decided fractions)  # cut the USPTO/WO header strip, side-
                                             # rotated header band, or PCT footer
    -> tight_crop (pixel density bbox)       # deterministic, see crop.py
    -> pad (uniform 10% of the longer side)  # consistent margin ratio across the set
    -> save input/figures/fig-NN.png         # grayscale, 300 DPI, optimized
    -> figure-manifest.md (+ optional figures-index.txt)

The VISION half (is there a header? at which y-fraction does it end? is the body
printed sideways?) is decided by Claude while viewing each raw image and delivered
here as --trim-decisions JSON; this script is fully deterministic and testable
without a model. See ../references/header-detection.md for the decision spec.

trim-decisions.json format — {input_filename: spec}, spec one of:
    null                    no rotation, no trim (pre-cleaned input)
    0.12                    shorthand: {"top": 0.12}
    {"top": 0.10}           trim fractions per side (top/right/bottom/left, 0-1),
    {"rotate": 90,          expressed in the POST-rotation frame; "rotate" is
     "top": 0.08}           clockwise degrees in {90, 180, 270}

Output naming: the trailing number(+letters) before the input extension becomes the
label — numeric part zero-padded to 2 digits, letters uppercased (fig-2.png ->
fig-02.png, fig-03a.jpg -> fig-03A.png, 12636684-7.png -> fig-07.png). Unparseable
names fall back to unknown-NN.png (rename by hand after inspection).

Usage:
  python process_figures.py <input_dir> <output_dir> \
      [--trim-decisions trim-decisions.json] [--dpi 300] [--index figures-index.txt]

Dependencies: Pillow + numpy (`pip install pillow numpy`).
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "figure-prep needs Pillow and numpy: pip install pillow numpy (%s)\n" % exc)
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop import CropConfig, load, pad, tight_crop  # noqa: E402

EXTS = {".png", ".jpg", ".jpeg"}
# Digits followed by optional letters, immediately before the file extension.
LABEL_RE = re.compile(r"(\d+)([A-Za-z]*)\.[^.]+$")
TRIM_SIDES = ("top", "right", "bottom", "left")


def derive_label(name):
    """fig-2.png -> 02 ; fig-03a.jpg -> 03A ; 12636684-7.png -> 07 ; random.png -> None."""
    m = LABEL_RE.search(name)
    if not m:
        return None
    digits, letters = m.group(1), m.group(2).upper()
    return "%02d%s" % (int(digits), letters)


def _iter_inputs(input_dir):
    return sorted(
        p for p in Path(input_dir).iterdir()
        if p.is_file() and p.suffix.lower() in EXTS
    )


def _normalize_trim_spec(value):
    """None -> {} ; bare number -> top trim ; dict -> rotate + per-side fractions."""
    if value is None:
        return {}
    if isinstance(value, (int, float)):
        return {"top": float(value)}
    if isinstance(value, dict):
        spec = {k: float(v) for k, v in value.items() if k in TRIM_SIDES and v}
        rotate = int(value.get("rotate") or 0)
        if rotate:
            if rotate not in (90, 180, 270):
                raise ValueError("rotate must be 90, 180, or 270 (clockwise): %r" % rotate)
            spec["rotate"] = rotate
        return spec
    raise ValueError("unsupported trim spec: %r" % (value,))


def _apply_rotate(arr, spec):
    """Rotate clockwise by spec['rotate'] degrees (before trimming — trim fractions
    are expressed in the upright, post-rotation frame)."""
    rotate = spec.get("rotate", 0)
    if not rotate:
        return arr
    return np.rot90(arr, k=(4 - rotate // 90) % 4)


def _apply_trim(arr, spec):
    h, w = arr.shape
    top = int(h * spec.get("top", 0.0))
    bottom = int(h * spec.get("bottom", 0.0))
    left = int(w * spec.get("left", 0.0))
    right = int(w * spec.get("right", 0.0))
    return arr[top: h - bottom if bottom > 0 else h,
               left: w - right if right > 0 else w]


def _emit_manifest(out_dir, cfg, dpi, entries):
    lines = [
        "# figure-manifest",
        "",
        "## Config",
        "",
        "- ink_threshold: %d" % cfg.ink_threshold,
        "- min_ink_density: %d" % cfg.min_ink_density,
        "- edge_shave_px: %d" % cfg.edge_shave_px,
        "- pad_fraction: %.2f" % cfg.pad_fraction,
        "- dpi: %d" % dpi,
        "- mode: L (grayscale)",
        "",
        "## Summary",
        "",
        "- total: %d" % len(entries),
        "- rotated: %d" % sum(1 for e in entries if e["rotate"]),
        "- trimmed: %d" % sum(1 for e in entries if e["trimmed"]),
        "",
        "## Entries",
        "",
        "| Input | Output | Rotate | Trim | In WxH | Cropped WxH | Pad px | Out WxH |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for e in entries:
        lines.append("| %s | %s | %s | %s | %s | %s | %d | %s |" % (
            e["input"], e["output"],
            ("%d°cw" % e["rotate"]) if e["rotate"] else "—",
            e["trim"] or "—",
            e["in_shape"], e["cropped_shape"], e["pad_px"], e["out_shape"]))
    (Path(out_dir) / "figure-manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description="patent figure Layer-1 cleaner")
    p.add_argument("input_dir", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("--trim-decisions", type=Path, default=None)
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--index", type=Path, default=None,
                   help="also write a figures-index.txt (one figure number per line)")
    args = p.parse_args(argv)

    decisions = {}
    if args.trim_decisions:
        decisions = json.loads(args.trim_decisions.read_text(encoding="utf-8"))

    inputs = _iter_inputs(args.input_dir)
    if not inputs:
        sys.stderr.write("no .png/.jpg/.jpeg inputs in %s\n" % args.input_dir)
        return 1
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cfg = CropConfig()
    entries = []
    numbers = set()
    unknown_seq = 0
    for src in inputs:
        spec = _normalize_trim_spec(decisions.get(src.name))
        arr = load(src)
        in_shape = "%dx%d" % (arr.shape[1], arr.shape[0])
        arr = _apply_rotate(arr, spec)
        arr = _apply_trim(arr, spec)
        cropped = tight_crop(arr, cfg)
        padded = pad(cropped, cfg)

        label = derive_label(src.name)
        if label is None:
            unknown_seq += 1
            out_name = "unknown-%02d.png" % unknown_seq
        else:
            out_name = "fig-%s.png" % label
            numbers.add(int(re.match(r"\d+", label).group(0)))
        out_path = args.output_dir / out_name
        Image.fromarray(padded, "L").save(
            out_path, dpi=(args.dpi, args.dpi), optimize=True)

        entries.append({
            "input": src.name, "output": out_name,
            "rotate": spec.get("rotate", 0),
            "trim": ", ".join("%s %.2f" % (k, spec[k]) for k in TRIM_SIDES if k in spec),
            "trimmed": any(k in spec for k in TRIM_SIDES),
            "in_shape": in_shape,
            "cropped_shape": "%dx%d" % (cropped.shape[1], cropped.shape[0]),
            "pad_px": (padded.shape[0] - cropped.shape[0]) // 2,
            "out_shape": "%dx%d" % (padded.shape[1], padded.shape[0]),
        })
        print("  %s -> %s" % (src.name, out_name))

    _emit_manifest(args.output_dir, cfg, args.dpi, entries)
    if args.index:
        args.index.write_text(
            "".join("%d\n" % n for n in sorted(numbers)), encoding="utf-8")
        print("wrote %s (%d figure numbers)" % (args.index, len(numbers)))
    print("wrote %s (%d figures)" % (args.output_dir / "figure-manifest.md", len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
