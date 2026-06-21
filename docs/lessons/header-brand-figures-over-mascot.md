# Header right panel carries patent drawings, not the mascot

> **SUPERSEDED (2026-06-21).** The header system was rebuilt from scratch as the
> **HeaderKit design system** (`tools/headerkit/`, see its README + CONTRACT.md).
> The one-off scripts named below (`make_header*.py`) and the figure-first /
> mascot approaches are both retired. Headers are now a single component library:
> a bright/soft 5:2 "aurora" theme whose **AI-generated conceptual illustration**,
> combined with the title, implies the essay's content. The lesson below is kept
> as historical context for the brand reasoning, not as current guidance. The
> Gyeongtae assets remain in `tools/assets/` for optional future video use only.


Brand decision by SETI (2026-06-12), after seeing the mascot-based investor
header: the code-drawn SVG cat fell short aesthetically, while the patent
line art is the highest-quality visual asset the series owns and is fully
reproducible from the run inputs. So headers are figure-first; the brand is
carried by the warm-paper background, the Liberation type, the token palette,
and the blueprint decorations, not by a character. Gyeongtae assets stay in
tools/assets/ for optional secondary/video use. Why it mattered: it redefines
the series default (tools/make_header_investor.py right panel = figures,
auto row/column layout) and saves future sessions from re-pitching mascot
headers as the primary cover.
