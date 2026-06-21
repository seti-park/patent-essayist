"""Tests for the HeaderKit composer (header.py): output size, 5:2 invariant, and
that the render scale produces a higher-resolution master without distortion."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from PIL import Image

from tools.headerkit.header import build_header
from tools.headerkit import W, H


class TestComposer(unittest.TestCase):
    def _render(self, **kw):
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.close()
        self.addCleanup(lambda: os.path.exists(tmp.name) and os.remove(tmp.name))
        out = build_header(
            title="Filed Before It Was Announced",
            thesis="A patent on file months before the public reveal",
            badge="US 2026/0125022 A1 . PENDING",
            keywords=["vision", "airbag", "before", "sensor"],
            out=tmp.name, **kw,
        )
        return Image.open(out)

    def test_default_scale_is_high_res(self):
        im = self._render()
        self.assertEqual(im.size, (W * 2, H * 2))   # default scale 2x = 6000x2400

    def test_scale_changes_resolution_keeps_ratio(self):
        for scale in (1.0, 2.0, 3.0):
            im = self._render(scale=scale)
            self.assertEqual(im.size, (int(W * scale), int(H * scale)))
            self.assertAlmostEqual(im.size[0] / im.size[1], 2.5, places=6)

    def test_explicit_size_override(self):
        im = self._render(size=(5000, 2000))
        self.assertEqual(im.size, (5000, 2000))

    def test_non_5x2_size_rejected(self):
        with self.assertRaises(ValueError):
            self._render(size=(4000, 2000))   # 2:1, not 5:2


if __name__ == "__main__":
    unittest.main(verbosity=2)
