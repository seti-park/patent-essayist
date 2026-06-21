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

    def test_supplied_image_used_as_art_layer(self):
        # A supplied raster cover-fits into the art zone; output stays 5:2.
        from PIL import Image
        art = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        art.close()
        self.addCleanup(lambda: os.path.exists(art.name) and os.remove(art.name))
        Image.new("RGB", (1200, 800), (240, 120, 90)).save(art.name)
        im = self._render(image=art.name, scale=1.0)
        self.assertEqual(im.size, (W, H))
        self.assertAlmostEqual(im.size[0] / im.size[1], 2.5, places=6)
        # the supplied art color should appear in the right (art) half
        px = im.convert("RGB").getpixel((int(W * 0.85), int(H * 0.5)))
        self.assertGreater(px[0], px[2])   # warm (R>B), i.e. the art, not the cool gradient


if __name__ == "__main__":
    unittest.main(verbosity=2)
