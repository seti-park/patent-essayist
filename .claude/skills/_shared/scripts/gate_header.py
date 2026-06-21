#!/usr/bin/env python3
"""HeaderKit lint gate for the patent-essay pipeline.

Enforces the frozen HeaderKit contract (tools/headerkit/CONTRACT.md sections 1
and 6): every essay header is composed through the library, the rasterized
output is exactly 5:2, and only the library's own draw modules touch raster
primitives or carry raw color literals.

This gate is the deterministic half of the design-system review (the qualitative
half is the `header-review` skill). It mirrors the run-pattern of the existing
text gates (run_gates.py / gate_emdash.py): stdlib only (Pillow is optional and
only used for the ratio check), every check returns a result dict with a `gate`
name + `findings` list of `check_id` records, and `main()` exits nonzero on any
fail-severity finding.

CHECKS (all hard unless noted):
  HEADER-RATIO-001 (fail) : a PNG under runs/**/header*.png is not exactly 5:2
                            (abs(W/H - 2.5) > EPS). Requires Pillow; if Pillow
                            is unavailable the check downgrades to a warn note.
  HEADER-BYPASS-001 (fail): a header-drawing primitive (`ImageDraw.Draw(`,
                            `Image.new(`) is called in a header context OUTSIDE
                            the allowlisted library draw modules.
  HEADER-TOKENS-001 (fail): a header source file (header.py / a header template)
                            that draws contains a raw `#RRGGBB` hex literal
                            instead of importing palette from `tokens`.
  HEADER-TOKENS-002 (fail): a header source file that draws does not import from
                            `tokens` at all.

TOLERANCE: every check is tolerant of files-not-yet-present. An empty repo (no
header PNGs, no header.py) PASSES with an informational `*-000` note rather than
failing — other agents may not have landed their files yet.
"""

import argparse
import os
import re
import sys

GATE_ID = "header"

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
RATIO_EXPECTED = 5.0 / 2.0       # 2.5 exactly (CONTRACT.md section 1)
RATIO_EPS = 1e-6                 # tiny epsilon; renders are integer 5:2 (e.g. 6000x2400)

# Repo roots scanned for python source (relative to repo root).
SCAN_DIRS = ("tools", os.path.join(".claude", "skills"))

# Files PERMITTED to call raster draw primitives directly. Allowlist by exact
# repo-relative path (CONTRACT.md section 6).
DRAW_ALLOWLIST = frozenset({
    os.path.join("tools", "headerkit", "components.py"),
    os.path.join("tools", "headerkit", "render.py"),
    os.path.join("tools", "headerkit", "illustration.py"),
})

# Files PERMITTED to carry raw hex literals: tokens.py defines the palette, and
# illustration.py legitimately emits token hex into generated SVG strings.
HEX_ALLOWLIST = frozenset({
    os.path.join("tools", "headerkit", "tokens.py"),
    os.path.join("tools", "headerkit", "illustration.py"),
})

# Raster draw primitives that mean "this file draws a header itself".
PRIMITIVE_RE = re.compile(r"\b(?:ImageDraw\.Draw|Image\.new)\s*\(")
# Raw 6-digit hex color literal.
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
# A file "is a header source" if it draws or composes a header.
HEADER_HINT_RE = re.compile(
    r"\b(?:build_header|headerkit|header\.py)\b|from\s+\.?tokens\b|import\s+tokens\b",
)
# Token import (relative or absolute), used by the tokens check.
TOKENS_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+[\w.]*\btokens\b\s+import|import\s+[\w.]*\btokens\b)",
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _repo_root(context):
    """Resolve the repo root: explicit context override, else four levels up
    from this script (_shared/scripts/ -> skills/ -> .claude/ -> repo)."""
    root = (context or {}).get("repo_root")
    if root:
        return os.path.abspath(root)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", "..", ".."))


def _is_test_file(rel):
    """Test files legitimately use raster primitives / hex for fixtures and
    assertions; they are not production header sources, so they are exempt from
    the bypass and token checks."""
    parts = rel.replace("\\", "/").split("/")
    return os.path.basename(rel).startswith("test_") or "tests" in parts


def _iter_py_files(root):
    """Yield (repo_relative_path, absolute_path) for every .py under SCAN_DIRS."""
    for rel_dir in SCAN_DIRS:
        base = os.path.join(root, rel_dir)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for name in files:
                if name.endswith(".py"):
                    ap = os.path.join(dirpath, name)
                    yield os.path.relpath(ap, root), ap


def _iter_header_pngs(root):
    """Yield absolute paths to runs/**/header*.png."""
    runs = os.path.join(root, "runs")
    if not os.path.isdir(runs):
        return
    for dirpath, _dirs, files in os.walk(runs):
        for name in files:
            if name.startswith("header") and name.lower().endswith(".png"):
                yield os.path.join(dirpath, name)


def _strip_fences_and_comments(text):
    """Blank out fenced/triple-quoted code blocks, '#' comments, and string
    literals so a primitive/hex mention inside a docstring or comment is not a
    real violation. Returns a same-line-count scrubbed copy (cheap heuristic)."""
    # Remove triple-quoted blocks (docstrings) first.
    text = re.sub(r'"""[\s\S]*?"""', lambda m: "\n" * m.group(0).count("\n"), text)
    text = re.sub(r"'''[\s\S]*?'''", lambda m: "\n" * m.group(0).count("\n"), text)
    out_lines = []
    for line in text.splitlines():
        # Drop trailing inline comments.
        hash_pos = line.find("#")
        # keep '#RRGGBB' style? no: hex check runs on the ORIGINAL text, this
        # scrub is only for primitive detection, so comments are safe to drop.
        if hash_pos != -1:
            line = line[:hash_pos]
        out_lines.append(line)
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# sub-checks
# ---------------------------------------------------------------------------
def _check_ratio(root):
    findings = []
    pngs = list(_iter_header_pngs(root))
    if not pngs:
        findings.append({
            "check_id": "HEADER-RATIO-000",
            "severity": "note",
            "message": "no runs/**/header*.png present yet; ratio check skipped",
            "location": os.path.join("runs", "**", "header*.png"),
        })
        return findings
    try:
        from PIL import Image  # noqa: WPS433 (optional dependency)
    except Exception:
        findings.append({
            "check_id": "HEADER-RATIO-000",
            "severity": "note",
            "message": "Pillow unavailable; cannot verify 5:2 ratio of %d PNG(s)" % len(pngs),
            "location": "runs/",
        })
        return findings
    for path in sorted(pngs):
        try:
            with Image.open(path) as im:
                w, h = im.size
        except Exception as exc:  # unreadable image -> hard fail, it's a deliverable
            findings.append({
                "check_id": "HEADER-RATIO-001",
                "severity": "fail",
                "message": "header PNG could not be opened: %s" % exc,
                "location": os.path.relpath(path, root),
            })
            continue
        ratio = (w / h) if h else 0.0
        if abs(ratio - RATIO_EXPECTED) > RATIO_EPS:
            findings.append({
                "check_id": "HEADER-RATIO-001",
                "severity": "fail",
                "message": "header is %dx%d (ratio %.4f); must be exactly 5:2 (2.5)" % (w, h, ratio),
                "location": os.path.relpath(path, root),
            })
    return findings


def _check_bypass(root):
    findings = []
    seen_any = False
    for rel, ap in _iter_py_files(root):
        if rel in DRAW_ALLOWLIST or _is_test_file(rel):
            continue
        try:
            with open(ap, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except Exception:
            continue
        scrubbed = _strip_fences_and_comments(raw)
        for lineno, line in enumerate(scrubbed.splitlines(), start=1):
            if PRIMITIVE_RE.search(line):
                seen_any = True
                findings.append({
                    "check_id": "HEADER-BYPASS-001",
                    "severity": "fail",
                    "message": (
                        "raster draw primitive used outside headerkit draw modules; "
                        "route header drawing through tools/headerkit/"
                    ),
                    "location": "%s:%d" % (rel, lineno),
                })
    if not seen_any and not findings:
        findings.append({
            "check_id": "HEADER-BYPASS-000",
            "severity": "note",
            "message": "no out-of-library raster primitives found",
            "location": ", ".join(SCAN_DIRS),
        })
    return findings


def _is_header_source(rel, text):
    """A drawing header source: a header.py / header template that draws OR
    references the headerkit composition surface."""
    name = os.path.basename(rel)
    if name == "header.py" or "header" in name and "review" not in name and "gate" not in name:
        # header.py and header templates.
        if PRIMITIVE_RE.search(text) or HEADER_HINT_RE.search(text) or "build_header" in text:
            return True
    return False


def _check_tokens(root):
    findings = []
    checked_any = False
    for rel, ap in _iter_py_files(root):
        # This gate file and the review/test files are not header sources.
        if rel.endswith(os.path.join("scripts", "gate_header.py")):
            continue
        if _is_test_file(rel):
            continue
        try:
            with open(ap, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except Exception:
            continue
        if not _is_header_source(rel, raw):
            continue
        checked_any = True
        # token import required
        if not TOKENS_IMPORT_RE.search(raw):
            findings.append({
                "check_id": "HEADER-TOKENS-002",
                "severity": "fail",
                "message": "header source draws but does not import palette from `tokens`",
                "location": rel,
            })
        # raw hex literals forbidden (unless on the hex allowlist)
        if rel not in HEX_ALLOWLIST:
            for lineno, line in enumerate(raw.splitlines(), start=1):
                for m in HEX_RE.finditer(line):
                    findings.append({
                        "check_id": "HEADER-TOKENS-001",
                        "severity": "fail",
                        "message": "raw hex color literal %s in header source; use a tokens.Theme value" % m.group(0),
                        "location": "%s:%d" % (rel, lineno + 0),
                    })
    if not checked_any:
        findings.append({
            "check_id": "HEADER-TOKENS-000",
            "severity": "note",
            "message": "no drawing header source (e.g. header.py) present yet; token check skipped",
            "location": os.path.join("tools", "headerkit", "header.py"),
        })
    return findings


# ---------------------------------------------------------------------------
# public entry — same shape as the text gates
# ---------------------------------------------------------------------------
def check(draft_text=None, context=None) -> dict:
    """Run all HeaderKit checks against the repo tree.

    Signature mirrors the text gates' `check(draft_text, context)` so this gate
    can be slotted into the same harness, but the HeaderKit gate inspects the
    filesystem, not a draft string; `draft_text` is ignored. `context` may carry
    `{"repo_root": <path>}` to point the scan at a fixture tree (used by tests).
    """
    context = context or {}
    root = _repo_root(context)
    findings = []
    findings += _check_ratio(root)
    findings += _check_bypass(root)
    findings += _check_tokens(root)
    passed = not any(f["severity"] == "fail" for f in findings)
    return {"gate": GATE_ID, "passed": passed, "findings": findings}


def _report(result: dict) -> None:
    status = "PASS" if result["passed"] else "FAIL"
    print("=" * 64)
    print("HEADERKIT LINT GATE")
    print("=" * 64)
    print("[%s] gate=%s" % (status, result["gate"]))
    n_fail = sum(1 for f in result["findings"] if f["severity"] == "fail")
    n_warn = sum(1 for f in result["findings"] if f["severity"] == "warn")
    n_note = sum(1 for f in result["findings"] if f["severity"] == "note")
    print("  %d fail, %d warn, %d note" % (n_fail, n_warn, n_note))
    print("-" * 64)
    for f in result["findings"]:
        print("  %-5s %-18s %s  (%s)" % (
            f["severity"].upper(), f["check_id"], f["message"], f["location"]))
    if not result["findings"]:
        print("  (no findings)")
    print("=" * 64)
    if status == "PASS" and (n_warn or n_note):
        print("OVERALL: PASS (with notes)")
    else:
        print("OVERALL: %s" % status)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="HeaderKit lint gate (%s)" % GATE_ID)
    p.add_argument("--repo-root", help="repo root to scan (default: inferred from script path)")
    args = p.parse_args(argv)
    ctx = {}
    if args.repo_root:
        ctx["repo_root"] = args.repo_root
    result = check(None, ctx)
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
