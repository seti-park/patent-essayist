#!/usr/bin/env python3
"""Stdlib unittest suite for the HeaderKit lint gate (gate_header.py).

Builds throwaway fixture repo trees in a tmpdir and asserts each check's
detection. Mirrors test_gates.py's style. Run with:

    python test_gate_header.py

Exits nonzero if any test fails. The ratio tests need Pillow (the same optional
dependency gate_header uses); they self-skip if Pillow is absent.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gate_header

try:
    from PIL import Image
    _HAVE_PIL = True
except Exception:
    _HAVE_PIL = False


def _has(result, check_id):
    return any(f["check_id"] == check_id for f in result["findings"])


def _write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


class _RepoFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self):
        return gate_header.check(None, {"repo_root": self.root})


class TestBypass(_RepoFixture):
    def test_primitive_outside_library_fails(self):
        _write(self.root, "tools/badheader.py",
               "from PIL import Image, ImageDraw\n"
               "img = Image.new('RGB', (3000, 1200))\n"
               "d = ImageDraw.Draw(img)\n")
        r = self.run_gate()
        self.assertFalse(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-BYPASS-001"))

    def test_primitive_in_allowlisted_components_passes(self):
        _write(self.root, "tools/headerkit/components.py",
               "from PIL import Image, ImageDraw\n"
               "img = Image.new('RGB', (3000, 1200))\n"
               "d = ImageDraw.Draw(img)\n")
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "HEADER-BYPASS-001"))

    def test_primitive_in_docstring_ignored(self):
        _write(self.root, "tools/notes.py",
               '"""Example only:\n'
               "    d = ImageDraw.Draw(img)\n"
               '"""\n'
               "x = 1\n")
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])

    def test_empty_tree_passes_with_note(self):
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-BYPASS-000"))


class TestTokens(_RepoFixture):
    COMPLIANT_HEADER = (
        "from .tokens import THEMES, GRID, build\n"
        "def build_header(**kw):\n"
        "    theme = THEMES['aurora']\n"
        "    return theme\n"
    )

    def test_compliant_header_passes(self):
        _write(self.root, "tools/headerkit/header.py", self.COMPLIANT_HEADER)
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "HEADER-TOKENS-001"))
        self.assertFalse(_has(r, "HEADER-TOKENS-002"))

    def test_raw_hex_in_header_fails(self):
        _write(self.root, "tools/headerkit/header.py",
               "from .tokens import THEMES\n"
               "def build_header(**kw):\n"
               "    bg = '#FDF6EF'\n"
               "    return bg\n")
        r = self.run_gate()
        self.assertFalse(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-TOKENS-001"))

    def test_missing_token_import_fails(self):
        _write(self.root, "tools/headerkit/header.py",
               "def build_header(**kw):\n"
               "    return build_header  # builds a header but no tokens import\n")
        r = self.run_gate()
        self.assertFalse(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-TOKENS-002"))

    def test_hex_in_tokens_py_allowed(self):
        # tokens.py legitimately defines palette hex; not a header source anyway.
        _write(self.root, "tools/headerkit/tokens.py",
               "ink = '#2E3A46'\n")
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])

    def test_no_header_source_passes_with_note(self):
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-TOKENS-000"))


@unittest.skipUnless(_HAVE_PIL, "Pillow not installed")
class TestRatio(_RepoFixture):
    def _png(self, rel, size):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.new("RGB", size, (253, 246, 239)).save(path)
        return path

    def test_5x2_png_passes(self):
        self._png("runs/001-essay/header.png", (3000, 1200))
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "HEADER-RATIO-001"))

    def test_4x1_png_fails(self):
        self._png("runs/002-essay/header.png", (4000, 1000))
        r = self.run_gate()
        self.assertFalse(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-RATIO-001"))

    def test_no_png_passes_with_note(self):
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])
        self.assertTrue(_has(r, "HEADER-RATIO-000"))


class TestEndToEnd(_RepoFixture):
    def test_clean_partial_tree_passes(self):
        # Mirror the real partial tree: library files present, no header.py/PNG.
        _write(self.root, "tools/headerkit/components.py",
               "from PIL import Image, ImageDraw\n"
               "img = Image.new('RGB', (3000, 1200))\n")
        _write(self.root, "tools/headerkit/tokens.py", "ink = '#2E3A46'\n")
        r = self.run_gate()
        self.assertTrue(r["passed"], r["findings"])

    def test_dirty_tree_fails(self):
        _write(self.root, "tools/rogue.py",
               "from PIL import Image\n"
               "img = Image.new('RGB', (1, 1))\n")
        r = self.run_gate()
        self.assertFalse(r["passed"])

    def test_main_exit_codes(self):
        # Clean tree -> 0.
        rc_clean = gate_header.main(["--repo-root", self.root])
        self.assertEqual(rc_clean, 0)
        # Add a bypass -> 1.
        _write(self.root, "tools/rogue.py",
               "from PIL import Image\nimg = Image.new('RGB', (1, 1))\n")
        rc_dirty = gate_header.main(["--repo-root", self.root])
        self.assertEqual(rc_dirty, 1)


def _run():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    total = result.testsRun
    failed = len(result.failures) + len(result.errors)
    print("\n%s" % ("=" * 50))
    print("SUMMARY: %d run, %d passed, %d failed" % (total, total - failed, failed))
    print("%s" % ("=" * 50))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(_run())
