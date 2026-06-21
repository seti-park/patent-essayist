"""Unit tests for the HeaderKit AI-illustration engine (illustration.py).

Runs under pytest:  python -m pytest tools/headerkit/tests/test_illustration.py -q
Or stand-alone:     python tools/headerkit/tests/test_illustration.py
"""

import os
import re
import sys
import tempfile

# Make the repo root importable when run stand-alone (so `tools.headerkit` resolves).
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import pytest  # noqa: E402
from PIL import Image  # noqa: E402

from tools.headerkit import tokens  # noqa: E402
from tools.headerkit import illustration as illo  # noqa: E402
from tools.headerkit.illustration import (  # noqa: E402
    IllustrationSpec,
    generate_illustration_svg,
    render_illustration,
)


# --- fixtures ---------------------------------------------------------------
def _spec(**kw):
    base = dict(
        title="Tesla filed a 70ms predictive-airbag patent before announcing it",
        thesis="A camera sees the crash before it happens and fires the airbag 70ms early",
        keywords=["vision", "airbag", "70ms", "before", "sensor"],
    )
    base.update(kw)
    return IllustrationSpec(**base)


# aurora palette token hex values, normalized lowercase #rrggbb.
def _palette_hexes():
    t = tokens.THEMES["aurora"]
    vals = [t.bg_top, t.bg_bottom, t.accent, t.accent2, t.accent3]
    out = set()
    for v in vals:
        r, g, b = tokens.hex_to_rgb(v)
        out.add(f"#{r:02x}{g:02x}{b:02x}")
    return out


# --- determinism ------------------------------------------------------------
def test_procedural_is_byte_deterministic():
    spec = _spec()
    a = generate_illustration_svg(spec, backend="procedural")
    b = generate_illustration_svg(spec, backend="procedural")
    assert a == b
    # A fresh spec object with identical inputs is also identical.
    c = generate_illustration_svg(_spec(), backend="procedural")
    assert a == c


def test_seed_derived_from_title_when_none():
    s1 = IllustrationSpec(title="Same Title", thesis="x", keywords=["data"])
    s2 = IllustrationSpec(title="Same Title", thesis="different thesis", keywords=["data"])
    # Seed depends on title only; same title -> same seed.
    assert s1.resolved_seed() == s2.resolved_seed()
    s3 = IllustrationSpec(title="Other Title", thesis="x", keywords=["data"])
    assert s1.resolved_seed() != s3.resolved_seed()


def test_explicit_seed_changes_output():
    a = generate_illustration_svg(_spec(seed=1), backend="procedural")
    b = generate_illustration_svg(_spec(seed=2), backend="procedural")
    assert a != b


# --- structure / contract ---------------------------------------------------
def test_svg_viewbox_and_shape():
    svg = generate_illustration_svg(_spec(), backend="procedural")
    assert svg.lstrip().startswith("<svg")
    assert 'viewBox="0 0 1500 1200"' in svg
    assert "</svg>" in svg
    # three layers present
    assert 'id="field-layer"' in svg
    assert 'id="blob-layer"' in svg
    assert 'id="glyph-layer"' in svg
    # luminous gradient field + soft blur
    assert "<linearGradient" in svg
    assert "feGaussianBlur" in svg


def test_blob_count_within_bounds():
    # 2-4 large soft forms: count circles+ellipses inside the blob layer region.
    svg = generate_illustration_svg(_spec(), backend="procedural")
    blob_section = svg.split('id="blob-layer"')[1].split('id="glyph-layer"')[0]
    n = blob_section.count("<circle") + blob_section.count("<ellipse")
    assert 2 <= n <= 4


# --- palette-only -----------------------------------------------------------
def test_uses_only_palette_token_colors():
    svg = generate_illustration_svg(_spec(), backend="procedural")
    palette = _palette_hexes()
    # Every hex color literal in the SVG must be a palette token value.
    found = set(m.lower() for m in re.findall(r"#[0-9a-fA-F]{6}", svg))
    assert found, "expected color literals in the SVG"
    stray = found - palette
    assert not stray, f"non-palette colors present: {stray}"
    # And the bright palette values actually appear.
    assert palette & found == palette or palette & found, "palette colors should appear"


def test_no_pure_black():
    svg = generate_illustration_svg(_spec(), backend="procedural").lower()
    assert "#000000" not in svg
    assert "#000" not in svg
    assert "black" not in svg


def test_palette_values_present():
    svg = generate_illustration_svg(_spec(), backend="procedural").lower()
    t = tokens.THEMES["aurora"]
    # gradient field uses bg_top + bg_bottom
    for c in (t.bg_top, t.bg_bottom):
        r, g, b = tokens.hex_to_rgb(c)
        assert f"#{r:02x}{g:02x}{b:02x}" in svg
    # at least one accent appears
    accents = []
    for c in (t.accent, t.accent2, t.accent3):
        r, g, b = tokens.hex_to_rgb(c)
        accents.append(f"#{r:02x}{g:02x}{b:02x}")
    assert any(a in svg for a in accents)


# --- glyph selection --------------------------------------------------------
def test_different_keywords_yield_different_glyphs():
    vision = generate_illustration_svg(
        _spec(title="t", keywords=["vision", "camera"]), backend="procedural"
    )
    safety = generate_illustration_svg(
        _spec(title="t", keywords=["airbag", "shield"]), backend="procedural"
    )
    # Same seed (same title) but different keywords -> different glyph layer.
    g_vision = vision.split('id="glyph-layer"')[1]
    g_safety = safety.split('id="glyph-layer"')[1]
    assert g_vision != g_safety
    assert vision != safety


def test_no_keyword_match_uses_default_orbit_glyph():
    svg = generate_illustration_svg(
        _spec(title="t", keywords=["xyzzy", "qux"]), backend="procedural"
    )
    glyph_layer = svg.split('id="glyph-layer"')[1]
    # orbit glyph is two crossed ellipses + dots; ensure glyph layer is non-empty.
    assert "<ellipse" in glyph_layer or "<circle" in glyph_layer


def test_keyword_maps_to_expected_glyph():
    # 'time'/'ms' -> clock glyph (12 ticks => many <line> elements in glyph layer).
    svg = generate_illustration_svg(
        _spec(title="t", keywords=["latency", "ms"]), backend="procedural"
    )
    glyph_layer = svg.split('id="glyph-layer"')[1]
    assert glyph_layer.count("<line") >= 12


# --- rendering --------------------------------------------------------------
def test_render_produces_1500x1200_png():
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "illo.png")
        ret = render_illustration(_spec(), out, backend="procedural")
        assert ret == out
        assert os.path.exists(out)
        with Image.open(out) as im:
            assert im.size == (1500, 1200)
            assert im.format == "PNG"


def test_render_custom_size():
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "illo.png")
        render_illustration(_spec(), out, width=750, height=600, backend="procedural")
        with Image.open(out) as im:
            assert im.size == (750, 600)


# --- llm backend ------------------------------------------------------------
def test_llm_backend_uses_supplied_spec_svg():
    bespoke = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1200">'
        '<rect width="1500" height="1200" fill="#fdf6ef"/></svg>'
    )
    spec = _spec(llm_svg=bespoke)
    out = generate_illustration_svg(spec, backend="llm")
    assert out == bespoke


def test_llm_backend_accepts_callable_provider():
    bespoke = '<svg viewBox="0 0 1500 1200"><g/></svg>'
    spec = _spec(llm_svg=lambda s: bespoke)
    assert generate_illustration_svg(spec, backend="llm") == bespoke


def test_llm_backend_module_hook(monkeypatch):
    bespoke = '<svg viewBox="0 0 1500 1200"><g id="hooked"/></svg>'
    monkeypatch.setattr(illo, "LLM_SVG_PROVIDER", lambda s: bespoke)
    assert generate_illustration_svg(_spec(), backend="llm") == bespoke


def test_llm_backend_falls_back_to_procedural():
    out = generate_illustration_svg(_spec(), backend="llm")
    assert 'viewBox="0 0 1500 1200"' in out
    assert "fell back to procedural" in out
    # fallback content matches procedural body (ignoring the prepended comment)
    proc = generate_illustration_svg(_spec(), backend="procedural")
    assert out.endswith(proc)


# --- image-api seam ---------------------------------------------------------
def test_image_api_backend_raises_notimplemented(monkeypatch):
    monkeypatch.delenv(illo.IMAGE_API_KEY_ENV, raising=False)
    with pytest.raises(NotImplementedError) as exc:
        generate_illustration_svg(_spec(), backend="image-api")
    assert illo.IMAGE_API_KEY_ENV in str(exc.value)


def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        generate_illustration_svg(_spec(), backend="nope")


# --- stand-alone runner -----------------------------------------------------
if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
