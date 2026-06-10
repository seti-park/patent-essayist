#!/usr/bin/env python3
"""Stdlib unittest suite for the patent-essay validation gates.

Plants violations inline and asserts detection. Run with:

    python test_gates.py

Exits nonzero if any test fails.
"""

import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gate_emdash
import gate_anchors
import gate_sources
import gate_banned
import gate_structure
import gate_figure_use
import run_gates


def _has(result, check_id):
    return any(f["check_id"] == check_id for f in result["findings"])


class TestEmdash(unittest.TestCase):
    def test_emdash_outside_quote_fails(self):
        draft = "The system works well — most of the time.\n"
        r = gate_emdash.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "EMDASH-001"))

    def test_emdash_inside_quote_passes(self):
        draft = 'The patent states "the system works — reliably" in column 3.\n'
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "EMDASH-001"))

    def test_emdash_in_blockquote_passes(self):
        draft = "> a verbatim quote — with a dash\n"
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_emdash_in_code_fence_ignored(self):
        draft = "```\nx — y\n```\n"
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_endash_connector_warns(self):
        draft = "The result was good – we measured it twice.\n"
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"])  # warn only, no fail
        self.assertTrue(_has(r, "EMDASH-002"))


class TestAnchors(unittest.TestCase):
    def test_unknown_anchor_fails(self):
        draft = "As shown in [9999], the rotor spins.\n"
        ctx = {"invention_summary_text": "Summary mentions [0001] and [0002]."}
        r = gate_anchors.check(draft, ctx)
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "ANCHOR-001"))

    def test_present_anchors_pass(self):
        draft = "See [0001] and [0002] for detail.\n"
        ctx = {"invention_summary_text": "Summary mentions [0001] and [0002]."}
        r = gate_anchors.check(draft, ctx)
        self.assertTrue(r["passed"], r["findings"])

    def test_no_summary_warns_and_passes(self):
        draft = "See [0001].\n"
        r = gate_anchors.check(draft, {})
        self.assertTrue(r["passed"])
        self.assertTrue(_has(r, "ANCHOR-000"))

    def test_figref_not_in_index_fails(self):
        draft = "Figure 7 shows the gear.\n"
        ctx = {"invention_summary_text": "", "figures_index": [1, 2, 3]}
        r = gate_anchors.check(draft, ctx)
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "FIGREF-001"))

    def test_figref_in_index_passes(self):
        draft = "Fig. 2 and Figure 3 are referenced.\n"
        ctx = {"invention_summary_text": "", "figures_index": [1, 2, 3]}
        r = gate_anchors.check(draft, ctx)
        self.assertTrue(r["passed"], r["findings"])

    def test_malformed_anchor_fails(self):
        draft = "See [123] and [12345] for detail.\n"
        ctx = {"invention_summary_text": "[0001]"}
        r = gate_anchors.check(draft, ctx)
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "ANCHOR-002"))

    def test_wellformed_anchor_no_format_finding(self):
        draft = "See [0001].\n"
        ctx = {"invention_summary_text": "[0001]"}
        r = gate_anchors.check(draft, ctx)
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "ANCHOR-002"))


class TestSources(unittest.TestCase):
    def test_missing_block_fails(self):
        draft = "# Intro\n\nSome body text with no sources.\n"
        r = gate_sources.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "SOURCES-001"))

    def test_duplicate_block_fails(self):
        draft = "# Sources\n- a\n\n# Sources\n- b\n"
        r = gate_sources.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "SOURCES-001"))

    def test_valid_flat_block_passes(self):
        draft = (
            "# Essay\n\nBody.\n\n"
            "# Sources\n"
            "- US1234567B2, Acme, Rotor, priorited 2019-01-01, published 2021-01-01\n"
            "- Smith, John (2020). Title. J. Mech.\n"
        )
        r = gate_sources.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_valid_subgrouped_block_passes(self):
        draft = (
            "# Sources\n"
            "## Patents\n"
            "- US1234567B2, Acme, Rotor\n"
            "## Technical specs\n"
            "- Bosch ECU spec sheet\n"
        )
        r = gate_sources.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_bad_category_fails(self):
        draft = (
            "# Sources\n"
            "## Industry data\n"
            "- some figure\n"
        )
        r = gate_sources.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "SOURCES-002"))

    def test_partial_subgrouping_fails(self):
        draft = (
            "# Sources\n"
            "- a bare top-level entry\n"
            "## Patents\n"
            "- US1, Acme, Rotor\n"
        )
        r = gate_sources.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "SOURCES-003"))

    def test_large_flat_list_warns(self):
        draft = (
            "# Sources\n"
            "- one\n- two\n- three\n- four\n- five\n"
        )
        r = gate_sources.check(draft, {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "SOURCES-004"))


class TestFigureUse(unittest.TestCase):
    SELECTION = "fig-01 maps to the lead. FIG. 2 anchors the mechanism. Figure 3 closes.\n"

    def test_orphan_selected_figure_fails(self):
        draft = "Figure 1 and Fig. 2 are discussed.\n"  # 3 selected but unused
        r = gate_figure_use.check(draft, {"figure_selection_text": self.SELECTION})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "FIGUSE-001"))

    def test_all_used_passes(self):
        draft = "Figure 1, Fig. 2, and Figure 3 all appear.\n"
        r = gate_figure_use.check(draft, {"figure_selection_text": self.SELECTION})
        self.assertTrue(r["passed"], r["findings"])

    def test_offplan_figure_warns(self):
        draft = "Figure 1, Fig. 2, Figure 3, and Figure 9 appear.\n"
        r = gate_figure_use.check(draft, {"figure_selection_text": self.SELECTION})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "FIGUSE-002"))

    def test_no_selection_skips(self):
        r = gate_figure_use.check("Figure 1.\n", {})
        self.assertTrue(r["passed"])
        self.assertTrue(_has(r, "FIGUSE-000"))


class TestBanned(unittest.TestCase):
    def test_banned_hits_fail(self):
        draft = "We delve into the design; it is not just fast, but cheap.\n"
        r = gate_banned.check(draft, {})
        self.assertFalse(r["passed"])
        hits = [f for f in r["findings"] if f["check_id"] == "BANNED-001"]
        # 'delve' literal + 'not just ..., but' regex == 2 hits.
        self.assertEqual(len(hits), 2, hits)

    def test_clean_passes(self):
        draft = "The mechanism rotates a shaft to drive the pump.\n"
        r = gate_banned.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_banned_inside_quote_ignored(self):
        draft = 'The inventor said "we delve into novel territory" here.\n'
        r = gate_banned.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])


class TestStructure(unittest.TestCase):
    def test_long_paragraph_warns(self):
        para = " ".join("This is sentence %d." % i for i in range(12))
        r = gate_structure.check(para + "\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "STRUCT-001"))

    def test_rule_of_three_warns(self):
        draft = "It was fast, cheap, and simple.\n"
        r = gate_structure.check(draft, {})
        self.assertTrue(_has(r, "STRUCT-004"))

    def test_bullet_overuse_warns(self):
        draft = "Intro line.\n- a\n- b\n- c\n- d\n"
        r = gate_structure.check(draft, {})
        self.assertTrue(_has(r, "STRUCT-003"))


class TestQuoteMaskingEdgeCases(unittest.TestCase):
    """Shared QuoteMasker behavior: curly quotes + paragraph-scoped wrap state."""

    def test_emdash_in_quote_wrapping_lines_passes(self):
        draft = 'He said "the rotor\nspins — fast" today.\n'
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_emdash_after_wrapped_quote_closes_fails(self):
        draft = 'He said "the rotor\nspins fast" today — emphatically.\n'
        r = gate_emdash.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "EMDASH-001"))

    def test_unbalanced_quote_masks_only_its_paragraph(self):
        draft = 'An "unbalanced quote here\n\nNext paragraph — with a dash.\n'
        r = gate_emdash.check(draft, {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "EMDASH-001"))

    def test_curly_quoted_emdash_passes(self):
        draft = "He said “the rotor spins — fast” today.\n"
        r = gate_emdash.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])

    def test_curly_quoted_banned_term_ignored(self):
        draft = "The inventor said “we delve into novel territory” here.\n"
        r = gate_banned.check(draft, {})
        self.assertTrue(r["passed"], r["findings"])


class TestMalformedInputs(unittest.TestCase):
    """Malformed orchestrator-written inputs must produce actionable failures,
    never bare tracebacks."""

    def _write(self, text, suffix):
        fh = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False,
                                         encoding="utf-8")
        fh.write(text)
        fh.close()
        return fh.name

    def test_malformed_figures_file_exits_2(self):
        figs = self._write("fig-01\n2\n", ".txt")
        draft = self._write("# t\n\nBody.\n\n# Sources\n- a\n", ".md")
        try:
            rc = run_gates.main(["--draft", draft, "--figures", figs])
            self.assertEqual(rc, 2)
        finally:
            os.unlink(figs)
            os.unlink(draft)

    def test_malformed_banned_regex_is_fail_finding(self):
        terms = self._write("delve\nre:([unclosed\n", ".txt")
        try:
            r = gate_banned.check("We delve here.\n", {"banned_terms_file": terms})
            self.assertFalse(r["passed"])
            self.assertTrue(_has(r, "BANNED-002"))
            # valid entries before/after the bad line still load and match
            self.assertTrue(_has(r, "BANNED-001"))
        finally:
            os.unlink(terms)


class TestBannedListSync(unittest.TestCase):
    """banned_terms.txt is the mechanical mirror of the anti-ai-writing.md Tier-1
    banned-words list (both files document the sync duty in their headers). This
    test fails when the word lists drift apart, so the mirror can't rot silently.
    Rhetorical patterns (prose bullets vs `re:` lines) are not comparable
    mechanically and stay a judgment-level sync."""

    CANON_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "references", "anti-ai-writing.md")

    def _canon_words(self):
        with open(self.CANON_PATH, "r", encoding="utf-8") as fh:
            canon = fh.read()
        m = re.search(r"### Banned words.*?```\n(.*?)```", canon, re.S)
        self.assertIsNotNone(
            m, "Banned-words code block not found under '### Banned words' "
               "in anti-ai-writing.md")
        return {w.strip() for w in re.split(r"[,\s]+", m.group(1)) if w.strip()}

    def _terms_file_literals(self):
        lits = set()
        with open(gate_banned.BANNED_TERMS_FILE, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith("re:"):
                    continue
                lits.add(line)
        return lits

    def test_canon_words_match_terms_file(self):
        canon = self._canon_words()
        terms = self._terms_file_literals()
        self.assertEqual(
            canon, terms,
            "anti-ai-writing.md Tier-1 words and banned_terms.txt literals have "
            "drifted apart.\n  only in canon: %s\n  only in terms file: %s"
            % (sorted(canon - terms), sorted(terms - canon)))


class TestRunGatesEndToEnd(unittest.TestCase):
    CLEAN = (
        "# Essay\n\n"
        "The rotor turns a shaft. The shaft drives a pump. This is described "
        "plainly. See [0001] for the mechanism and Figure 1 for the layout.\n\n"
        "# Sources\n"
        "- US1234567B2, Acme, Rotor, priorited 2019-01-01, published 2021-01-01\n"
        "- Smith, John (2020). Title. J. Mech.\n"
    )
    DIRTY = (
        "# Essay\n\n"
        "We delve into the rotor — it is fast. See [9999] and Figure 9.\n"
        # no Sources block
    )

    def _write(self, text):
        fh = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        fh.write(text)
        fh.close()
        return fh.name

    def test_clean_passes(self):
        ctx = {"invention_summary_text": "[0001]", "figures_index": [1]}
        overall, results = run_gates.run_all(self.CLEAN, ctx)
        self.assertTrue(overall, [r for r in results if not r["passed"]])

    def test_dirty_fails(self):
        ctx = {"invention_summary_text": "[0001]", "figures_index": [1]}
        overall, results = run_gates.run_all(self.DIRTY, ctx)
        self.assertFalse(overall)

    def test_main_exit_codes(self):
        clean_path = self._write(self.CLEAN)
        dirty_path = self._write(self.DIRTY)
        summary = self._write("[0001]")
        figs = self._write("1")
        try:
            rc_clean = run_gates.main(
                ["--draft", clean_path, "--invention-summary", summary, "--figures", figs])
            rc_dirty = run_gates.main(
                ["--draft", dirty_path, "--invention-summary", summary, "--figures", figs])
            self.assertEqual(rc_clean, 0)
            self.assertEqual(rc_dirty, 1)
        finally:
            for p in (clean_path, dirty_path, summary, figs):
                os.unlink(p)


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
