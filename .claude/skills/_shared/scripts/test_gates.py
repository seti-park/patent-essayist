#!/usr/bin/env python3
"""Stdlib unittest suite for the patent-essay validation gates.

Plants violations inline and asserts detection. Run with:

    python test_gates.py

Exits nonzero if any test fails.
"""

import os
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
import gate_meta
import gate_stub
import gate_cashtag
import gate_dupe
import gate_typography
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

    def test_rejected_figure_in_selected_heading_section_not_flagged(self):
        # handoff-template's own convention: a "## Selected figures" table
        # followed by prose/HTML-comment rationale that legitimately names
        # REJECTED figures by number (e.g. "FIG. 2 was reviewed ... but NOT
        # selected"). Those mentions must not count as selected.
        selection = (
            "# Figure Selection\n\n"
            "## Selected figures\n\n"
            "| Figure | File |\n|---|---|\n"
            "| FIG. 1 | fig-01.png |\n"
            "| FIG. 3 | fig-03.png |\n\n"
            "<!-- FIG. 2 was reviewed as the paired precursor to FIG. 3 but NOT "
            "selected: FIG. 3 alone carries the load-bearing concept. -->\n\n"
            "## Paired-figure relationships (acknowledged)\n\n"
            "| Figure(s) | Treatment |\n|---|---|\n"
            "| FIG. 2 + FIG. 3 | FIG. 3 selected, FIG. 2 dropped |\n"
        )
        draft = "Figure 1 and Figure 3 both appear in the essay.\n"
        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
        self.assertTrue(r["passed"], r["findings"])

    def test_rejected_figure_still_orphans_if_truly_selected(self):
        # Sanity check: scoping to the heading section must not blind the
        # gate to a real orphan that IS in the "## Selected figures" table.
        selection = (
            "## Selected figures\n\n"
            "| Figure | File |\n|---|---|\n"
            "| FIG. 1 | fig-01.png |\n"
            "| FIG. 5 | fig-05.png |\n\n"
            "## Paired-figure relationships (acknowledged)\n\n"
            "| Figure(s) | Treatment |\n|---|---|\n"
        )
        draft = "Only Figure 1 appears in the essay.\n"
        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "FIGUSE-001"))


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


class TestMeta(unittest.TestCase):
    def test_reader_instruction_fails(self):
        r = gate_meta.check("Read it the way an examiner would. The rotor spins.\n", {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "META-001"))

    def test_self_reference_fails(self):
        r = gate_meta.check("Everything below is the proof; the rest of this essay shows it.\n", {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "META-001"))

    def test_scope_disclaimer_passes(self):
        # functional self-reference, NOT posturing -> must not fire
        r = gate_meta.check("This essay does not adjudicate them. It only marks where to look.\n", {})
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "META-001"))

    def test_meta_inside_quote_ignored(self):
        r = gate_meta.check('A critic wrote "watch how the patent handles each" last year.\n', {})
        self.assertTrue(r["passed"], r["findings"])

    def test_soft_reader_address_warns(self):
        r = gate_meta.check("You might think the broad claim is the strong move.\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "META-002"))


class TestStub(unittest.TestCase):
    def _doc(self, gamma_body):
        return ("## Alpha\n" + ("word " * 120) + "\n\n"
                "## Beta\n" + ("word " * 110) + "\n\n"
                "## Gamma\n" + gamma_body + "\n\n"
                "# Sources\n- x\n")

    def test_stub_section_warns(self):
        r = gate_stub.check(self._doc("a tiny stub."), {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "STUB-001"))

    def test_balanced_sections_pass(self):
        r = gate_stub.check(self._doc("word " * 100), {})
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "STUB-001"))

    def test_sources_subgroups_not_counted(self):
        draft = ("## Alpha\n" + ("word " * 80) + "\n\n"
                 "## Beta\n" + ("word " * 80) + "\n\n"
                 "## Gamma\n" + ("word " * 80) + "\n\n"
                 "# Sources\n## Patents\n- a\n## Papers\n- b\n")
        r = gate_stub.check(draft, {})
        self.assertFalse(_has(r, "STUB-001"))


class TestCashtag(unittest.TestCase):
    def test_bare_ticker_warns(self):
        r = gate_cashtag.check("The firm is trading as AGLT starting Monday.\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "CASH-001"))

    def test_exchange_colon_warns(self):
        r = gate_cashtag.check("It lists on NASDAQ: AGLT this quarter.\n", {})
        self.assertTrue(_has(r, "CASH-001"))

    def test_cashtag_form_passes(self):
        r = gate_cashtag.check("The firm is trading as $AGLT starting Monday.\n", {})
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "CASH-001"))

    def test_acronym_not_flagged(self):
        r = gate_cashtag.check("The deal with GXO and USPTO filings, sold as one stack.\n", {})
        self.assertFalse(_has(r, "CASH-001"))


class TestDupe(unittest.TestCase):
    def test_gross_repeat_warns(self):
        draft = ("The defensible engine is filed elsewhere entirely. "
                 "Months later, the defensible engine is filed elsewhere entirely.\n")
        r = gate_dupe.check(draft, {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "DUPE-001"))

    def test_no_repeat_passes(self):
        r = gate_dupe.check("The rotor turns a shaft which then drives a centrifugal pump cleanly.\n", {})
        self.assertTrue(r["passed"], r["findings"])
        self.assertFalse(_has(r, "DUPE-001"))

    def test_quoted_repeat_ignored(self):
        draft = ('It says "a deployment mechanism and deployable autonomous delivery robot" once; '
                 'again "a deployment mechanism and deployable autonomous delivery robot" verbatim.\n')
        r = gate_dupe.check(draft, {})
        self.assertFalse(_has(r, "DUPE-001"))


class TestTypography(unittest.TestCase):
    def test_latin_dotted_fails(self):
        r = gate_typography.check("The rotor spins, e.g. at high rpm.\n", {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "LATIN-001"))

    def test_latin_bare_fails(self):
        r = gate_typography.check("Use a sensor, ie a thermocouple, here.\n", {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "LATIN-001"))

    def test_latin_inside_quote_passes(self):
        r = gate_typography.check('The patent says "the load, e.g. a motor, varies".\n', {})
        self.assertTrue(r["passed"], r["findings"])

    def test_exclamation_fails(self):
        r = gate_typography.check("This is a huge result!\n", {})
        self.assertFalse(r["passed"])
        self.assertTrue(_has(r, "EXCLAIM-001"))

    def test_markdown_image_not_exclamation(self):
        r = gate_typography.check("![figure one](fig-01.png)\n", {})
        self.assertFalse(_has(r, "EXCLAIM-001"))

    def test_emoji_warns(self):
        r = gate_typography.check("The result is wild \U0001F525.\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "EMOJI-001"))

    def test_sanctioned_thinking_emoji_passes(self):
        r = gate_typography.check("So who really owns the moat? \U0001F914\n", {})
        self.assertFalse(_has(r, "EMOJI-001"))

    def test_caps_run_warns(self):
        r = gate_typography.check("This is THE BIG DEAL today.\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "CAPS-001"))

    def test_single_acronyms_not_flagged(self):
        r = gate_typography.check("The USB link to the LLM is fast.\n", {})
        self.assertFalse(_has(r, "CAPS-001"))

    def test_part_number_not_flagged(self):
        r = gate_typography.check("See US1234567B2 for the rotor.\n", {})
        self.assertFalse(_has(r, "CAPS-001"))

    def test_nondescriptive_link_warns(self):
        r = gate_typography.check("Read the spec [here](http://x.example).\n", {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "LINK-001"))

    def test_long_sentence_warns(self):
        draft = "The rotor " + "and the shaft " * 20 + "spin together.\n"
        r = gate_typography.check(draft, {})
        self.assertTrue(r["passed"])  # warn only
        self.assertTrue(_has(r, "LONGSENT-001"))

    def test_code_fence_exempt(self):
        r = gate_typography.check("```\nx = 1  # e.g. this!\n```\n", {})
        self.assertTrue(r["passed"], r["findings"])


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
