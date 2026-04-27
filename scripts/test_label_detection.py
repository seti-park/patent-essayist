"""Regression test for figure.assemble.find_label_bbox.

Reads data/fixtures/labels.json, runs find_label_bbox on each pinned image,
and asserts the bbox falls inside the expected ranges. Also asserts each
consistency group has a relative spread within tolerance.

Exit code 0 on success, 1 on any failure. Designed to run both as a script
and as a pytest module (every fixture becomes its own test case).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from figure.assemble import (  # noqa: E402
    AssembleConfig,
    LabelDetectionError,
    find_label_bbox,
    load_figure,
)

FIXTURE_PATH = ROOT / "data" / "fixtures" / "labels.json"


def _load_fixtures() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text())


def _check_one(entry: dict[str, Any], cfg: AssembleConfig
               ) -> tuple[bool, str, dict]:
    src = ROOT / entry["path"]
    arr = load_figure(src)
    h = arr.shape[0]
    bbox = find_label_bbox(arr, cfg, source=str(src.relative_to(ROOT)))
    y_frac = bbox.y1 / h

    failures: list[str] = []
    vlo, vhi = entry["expected_vspan_range"]
    if not (vlo <= bbox.vspan <= vhi):
        failures.append(f"vspan {bbox.vspan} not in [{vlo},{vhi}]")
    hlo, hhi = entry["expected_hspan_range"]
    if not (hlo <= bbox.hspan <= hhi):
        failures.append(f"hspan {bbox.hspan} not in [{hlo},{hhi}]")
    ylo, yhi = entry["expected_y_start_frac_range"]
    if not (ylo <= y_frac <= yhi):
        failures.append(f"y_start_frac {y_frac:.3f} not in [{ylo},{yhi}]")

    return (
        not failures,
        ", ".join(failures) or "OK",
        {"vspan": bbox.vspan, "hspan": bbox.hspan, "y_start_frac": round(y_frac, 3)},
    )


def _check_consistency(group: dict[str, Any], measurements: dict[str, dict]
                       ) -> tuple[bool, str]:
    vspans = [measurements[fp]["vspan"] for fp in group["fixtures"]
              if fp in measurements]
    if len(vspans) < 2:
        return True, f"skip (only {len(vspans)} measurements)"
    lo, hi = min(vspans), max(vspans)
    spread = (hi - lo) / ((hi + lo) / 2)
    ok = spread <= group["max_relative_spread"]
    return ok, (f"vspans={vspans}  spread={spread:.3%}  "
                f"max={group['max_relative_spread']:.0%}")


def main() -> int:
    spec = _load_fixtures()
    cfg = AssembleConfig()

    print("=== per-fixture ===")
    print(f"{'fixture':45s} {'vspan':>6} {'hspan':>6} {'y_frac':>7}  {'status'}")
    print("-" * 90)

    measurements: dict[str, dict] = {}
    failures = 0
    for entry in spec["fixtures"]:
        try:
            ok, msg, m = _check_one(entry, cfg)
        except LabelDetectionError as e:
            ok = False
            msg = f"detection raised: {str(e).splitlines()[1].strip()}"
            m = {"vspan": "-", "hspan": "-", "y_start_frac": "-"}
        except FileNotFoundError as e:
            print(f"{entry['path']:45s} SKIP (missing): {e.filename}")
            continue
        name = Path(entry["path"]).name
        print(f"{name:45s} {m['vspan']!s:>6} {m['hspan']!s:>6} "
              f"{m['y_start_frac']!s:>7}  {'PASS' if ok else 'FAIL'}: {msg}")
        if not ok:
            failures += 1
        measurements[entry["path"]] = m

    print()
    print("=== consistency groups ===")
    for group in spec.get("consistency_groups", []):
        ok, msg = _check_consistency(group, measurements)
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")
        if not ok:
            failures += 1

    print()
    print(f"{'OK' if failures == 0 else 'FAIL'}  ({failures} failure(s))")
    return 0 if failures == 0 else 1


# ---- pytest integration: each fixture becomes its own test ----------------
def _make_pytest_params():
    spec = _load_fixtures()
    return [(entry,) for entry in spec["fixtures"]]


def test_fixture(entry):  # type: ignore[no-untyped-def]
    """Generated pytest case (one per fixture in labels.json)."""
    cfg = AssembleConfig()
    ok, msg, _ = _check_one(entry, cfg)
    assert ok, f"{entry['path']}: {msg}"


try:  # decorate only when pytest is actually present
    import pytest
    test_fixture = pytest.mark.parametrize("entry", [p[0] for p in _make_pytest_params()])(test_fixture)  # type: ignore[assignment]
except ImportError:
    pass


if __name__ == "__main__":
    sys.exit(main())
