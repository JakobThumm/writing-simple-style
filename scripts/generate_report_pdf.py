#!/usr/bin/env python3
"""Render a writing-style report (markdown) to a formatted PDF via pandoc.

The markdown marks issues with guillemet tags -- ‹voice›, ‹cut›,
‹struct›, ‹term›, ‹word› -- which this script turns into
coloured labels before handing the document to pandoc.

Usage:
    generate_report_pdf.py report.md
    generate_report_pdf.py report.md -o style-report.pdf --engine xelatex
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "report_latex.tex"

# The five issue categories. Guillemets are used as delimiters rather than
# square brackets because a report is full of real citations -- [12], [ats] --
# and a bracketed tag would be indistinguishable from one, both to a reader
# and to this substitution.
CATEGORY_MACRO = {
    "struct": r"\structtag{}",
    "voice": r"\voicetag{}",
    "cut": r"\cuttag{}",
    "term": r"\termtag{}",
    "word": r"\wordtag{}",
}
CATEGORY_RE = re.compile("‹(" + "|".join(CATEGORY_MACRO) + ")›")

# Category tags travel through pandoc as inert sentinels and only become LaTeX
# macros afterwards. That lets us run pandoc with raw LaTeX disabled, so a
# quoted snippet containing the author's own macros (\rstar, \ac{...}) is
# rendered as text instead of being executed and breaking the build.
SENTINEL = "ZZTAGZZ{}ZZ"
SENTINEL_RE = re.compile(r"ZZTAGZZ(struct|voice|cut|term|word)ZZ")

# Raw LaTeX, dollar maths and raw attributes are all disabled deliberately.
PANDOC_FROM = (
    "markdown"
    "-raw_tex"
    "-tex_math_dollars"
    "-tex_math_single_backslash"
    "-tex_math_double_backslash"
    "-raw_attribute"
    "+pipe_tables"
)

# Fenced code blocks and inline code must keep their tag text literal.
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def check_deps(engine: str) -> bool:
    ok = True
    if not shutil.which("pandoc"):
        print("ERROR: pandoc not found. Install with:\n"
              "  sudo apt install pandoc   |   brew install pandoc", file=sys.stderr)
        ok = False
    if not shutil.which(engine):
        print(f"ERROR: LaTeX engine '{engine}' not found. Install with:\n"
              "  sudo apt install texlive-latex-recommended texlive-latex-extra",
              file=sys.stderr)
        ok = False
    return ok


def extract_title(md: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else "Writing Style Report"


def preprocess(md: str) -> str:
    """Prepare the report markdown for a pandoc run with raw LaTeX disabled.

    Two transformations:

    * category tags become inert sentinels, restored as coloured macros in
      the generated LaTeX;
    Blockquoted source text needs no special handling: pandoc runs with raw
    LaTeX and dollar maths disabled, so the author's macros are escaped to
    literal text rather than executed.
    """
    out: list[str] = []
    in_fence = False
    dropped_title = False
    for line in md.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        # The H1 is rendered by \maketitle; keeping it would repeat the title
        # as a numbered section and nest every heading one level too deep.
        if not dropped_title and re.match(r"^#\s+\S", line):
            dropped_title = True
            continue

        # Protect existing inline code spans from the tag substitution.
        parts = re.split(r"(`+[^`]*`+)", line)
        for i, part in enumerate(parts):
            if not part.startswith("`"):
                parts[i] = CATEGORY_RE.sub(
                    lambda m: SENTINEL.format(m.group(1)), part
                )
        out.append("".join(parts))
    return "\n".join(out)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def build_pdf(md_path: Path, out_path: Path, engine: str, toc: bool) -> None:
    raw = md_path.read_text(encoding="utf-8")
    title = extract_title(raw)

    with tempfile.TemporaryDirectory() as tmpdir:
        work = Path(tmpdir)
        src = work / "report.md"
        src.write_text(preprocess(raw), encoding="utf-8")

        cmd = [
            "pandoc", str(src),
            "--from", PANDOC_FROM,
            "--to", "latex",
            "--standalone",
            "--template", str(TEMPLATE),
            "--variable", f"title={title}",
            "--output", str(work / "report.tex"),
        ]
        if toc:
            cmd += ["--toc", "--toc-depth=2", "--variable", "toc=true"]

        result = run(cmd)
        if result.returncode != 0:
            fail("pandoc failed", result.stderr, md_path)

        tex = (work / "report.tex").read_text(encoding="utf-8")
        tex = SENTINEL_RE.sub(lambda m: CATEGORY_MACRO[m.group(1)], tex)
        (work / "report.tex").write_text(tex, encoding="utf-8")

        # Twice, so the table of contents and page numbers settle.
        passes = 2 if toc else 1
        for _ in range(passes):
            result = run([engine, "-interaction=nonstopmode",
                          "-halt-on-error", "report.tex"], cwd=work)

        built = work / "report.pdf"
        if result.returncode != 0 or not built.exists():
            log = (work / "report.log")
            detail = ""
            if log.exists():
                errs = [ln for ln in log.read_text(errors="replace").splitlines()
                        if ln.startswith("!")]
                detail = "\n".join(errs[:10])
            fail(f"{engine} failed", detail or result.stdout[-2000:], md_path)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(built, out_path)


def fail(what: str, detail: str, md_path: Path) -> None:
    print(f"{what}:", file=sys.stderr)
    print(detail, file=sys.stderr)
    print(f"\nThe markdown report is complete and readable as-is: {md_path}",
          file=sys.stderr)
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="path to the markdown report")
    ap.add_argument("-o", "--output", help="output PDF (default: input with .pdf)")
    ap.add_argument("--engine", default="pdflatex",
                    choices=["pdflatex", "xelatex", "lualatex"],
                    help="LaTeX engine (default: pdflatex)")
    ap.add_argument("--no-toc", action="store_true", help="omit the table of contents")
    ap.add_argument("--check-deps", action="store_true",
                    help="verify pandoc and LaTeX are available, then exit")
    args = ap.parse_args()

    if args.check_deps:
        sys.exit(0 if check_deps(args.engine) else 1)
    if not check_deps(args.engine):
        sys.exit(1)

    md_path = Path(args.input)
    if not md_path.exists():
        sys.exit(f"ERROR: file not found: {md_path}")

    out_path = Path(args.output) if args.output else md_path.with_suffix(".pdf")
    print(f"Generating {out_path} ...")
    build_pdf(md_path, out_path, args.engine, toc=not args.no_toc)
    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
