#!/usr/bin/env python3
"""Split a LaTeX or Markdown document into sections and paragraphs.

Emits JSON so the reviewing agent has stable, deterministic anchors
(``file:line``) and an up-front paragraph count for every section.

Usage:
    split_paragraphs.py paper.tex
    split_paragraphs.py paper.tex --section "Method"
    split_paragraphs.py chapter.md --json out.json
    split_paragraphs.py main.tex --follow-inputs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------- LaTeX rules

SECTION_OPEN = re.compile(
    r"^\s*\\(chapter|section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\s*\{"
)
LEVELS = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}

TITLE_STRIP = re.compile(r"\\(?:label|index|glsresetall)\s*\{[^}]*\}")


def match_section(line: str) -> tuple[str, str] | None:
    """Return (kind, title) for a sectioning command, tracking brace depth.

    A plain regex would swallow a trailing ``\\label{...}`` into the title,
    because the title itself may contain braces (``\\texttt{x}``).
    """
    m = SECTION_OPEN.match(line)
    if not m:
        return None
    depth = 1
    i = m.end()
    title_chars = []
    while i < len(line) and depth:
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            title_chars.append(line[i : i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        title_chars.append(c)
        i += 1
    if depth:
        return None  # title runs past the end of the line; treat as prose
    title = TITLE_STRIP.sub("", "".join(title_chars)).strip()
    return m.group(1), title

INPUT_CMD = re.compile(r"^\s*\\(?:input|include)\s*\{([^}]+)\}")

# Environments whose content is not running prose and is reported separately.
FLOAT_ENVS = {
    "figure", "figure*", "table", "table*", "tabular", "tabularx", "longtable",
    "algorithm", "algorithmic", "algorithm2e", "tikzpicture", "lstlisting",
    "verbatim", "minted", "thebibliography", "abstract",
}

# Display maths does not end a paragraph; it belongs to the surrounding prose.
MATH_ENVS = {
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*", "eqnarray", "eqnarray*", "displaymath",
    "split", "cases", "aligned", "IEEEeqnarray", "IEEEeqnarray*",
}

BEGIN_ENV = re.compile(r"\\begin\s*\{([^}]+)\}")
END_ENV = re.compile(r"\\end\s*\{([^}]+)\}")

# Abbreviations that must not be treated as a sentence end.
ABBREVS = {
    "e.g", "i.e", "cf", "etc", "vs", "et al", "Fig", "Figs", "Eq", "Eqs",
    "Sec", "Secs", "Tab", "Ref", "Refs", "Alg", "Ch", "App", "No", "Dr",
    "Prof", "Mr", "Ms", "St", "approx", "resp", "w.r.t", "s.t",
}


def strip_tex_comments(line: str) -> str:
    """Remove a trailing LaTeX comment, honouring the escaped percent sign."""
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i : i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


# ------------------------------------------------------------------ data model


@dataclass
class Paragraph:
    id: str
    file: str
    start_line: int
    end_line: int
    n_words: int
    n_sentences: int
    has_display_math: bool
    text: str


@dataclass
class Section:
    id: str
    level: int
    title: str
    file: str
    line: int
    paragraphs: list[Paragraph] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)


# ------------------------------------------------------------------- utilities


def count_sentences(text: str) -> int:
    """Approximate sentence count, tolerant of abbreviations and maths."""
    probe = re.sub(r"\$[^$]*\$", " MATH ", text)
    probe = re.sub(r"\\\[.*?\\\]", " MATH ", probe, flags=re.S)
    probe = re.sub(r"\d+\.\d+", " NUM ", probe)
    count = 0
    for m in re.finditer(r"[.!?]+(?=\s|$)", probe):
        head = probe[: m.start()]
        last = re.search(r"([A-Za-z.]+)$", head)
        if last and last.group(1).rstrip(".") in ABBREVS:
            continue
        count += 1
    return max(count, 1 if probe.strip() else 0)


def count_words(text: str) -> int:
    probe = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    probe = re.sub(r"[{}$\\]", " ", probe)
    return len([w for w in probe.split() if re.search(r"[A-Za-z0-9]", w)])


def is_pure_math(text: str) -> bool:
    stripped = re.sub(r"\s+", "", text)
    if not stripped:
        return False
    for env in MATH_ENVS:
        if stripped.startswith(f"\\begin{{{env}}}") or stripped.startswith("\\["):
            return True
    return False


def collapse_skipped(entries: list[dict]) -> list[dict]:
    """Turn per-line skip records into contiguous ``{env, from, to}`` ranges."""
    out: list[dict] = []
    for e in entries:
        if out and out[-1]["env"] == e["env"] and out[-1]["to"] == e["line"] - 1:
            out[-1]["to"] = e["line"]
        else:
            out.append({"env": e["env"], "from": e["line"], "to": e["line"]})
    return out


def continues_previous(text: str) -> bool:
    """True when a chunk reads as the tail of the paragraph before it."""
    head = text.lstrip()
    if not head:
        return False
    if re.match(r"^(where|with|and|or|such that|for all|here,|in which)\b", head, re.I):
        return True
    # A chunk opening in lower case is almost always a continuation.
    return head[0].islower()


# ------------------------------------------------------------------ TeX parser


def parse_tex(path: Path, follow_inputs: bool) -> list[Section]:
    sections: list[Section] = []
    current = Section(id="sec0", level=1, title="(preamble / untitled)",
                      file=str(path), line=1)
    sections.append(current)

    chunk: list[str] = []
    chunk_start = 0
    env_stack: list[str] = []
    in_document = False
    saw_document_env = False
    chunk_has_math = False

    def flush(end_line: int) -> None:
        nonlocal chunk, chunk_start, chunk_has_math
        text = "\n".join(chunk).strip()
        chunk = []
        has_math, chunk_has_math = chunk_has_math, False
        if not text:
            return
        n_words = count_words(text)
        if n_words == 0 and not has_math:
            return
        paras = current.paragraphs
        # Display maths and its "where" clause belong to the paragraph before.
        if paras and (is_pure_math(text) or (paras[-1].has_display_math
                                             and continues_previous(text))):
            prev = paras[-1]
            prev.text = prev.text + "\n\n" + text
            prev.end_line = end_line
            prev.n_words += n_words
            prev.n_sentences = count_sentences(prev.text)
            prev.has_display_math = prev.has_display_math or has_math or is_pure_math(text)
            return
        paras.append(
            Paragraph(
                id=f"{current.id}-p{len(paras) + 1}",
                file=str(path),
                start_line=chunk_start,
                end_line=end_line,
                n_words=n_words,
                n_sentences=count_sentences(text),
                has_display_math=has_math,
                text=text,
            )
        )

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not any("\\begin{document}" in ln for ln in lines):
        in_document = True  # a fragment file, e.g. sections/method.tex
    else:
        saw_document_env = True

    for idx, raw in enumerate(lines, start=1):
        line = strip_tex_comments(raw)

        if saw_document_env and not in_document:
            if "\\begin{document}" in line:
                in_document = True
            continue
        if "\\end{document}" in line:
            flush(idx - 1)
            break

        if follow_inputs:
            m = INPUT_CMD.match(line)
            if m:
                flush(idx - 1)
                child = (path.parent / m.group(1)).with_suffix(".tex")
                if child.exists():
                    for sub in parse_tex(child, follow_inputs):
                        if sub.paragraphs or sub.title != "(preamble / untitled)":
                            sub.id = f"sec{len(sections)}"
                            for n, p in enumerate(sub.paragraphs, start=1):
                                p.id = f"{sub.id}-p{n}"
                            sections.append(sub)
                            current = sub
                else:
                    print(f"warning: \\input target not found: {child}", file=sys.stderr)
                continue

        # Track environments so blank lines inside a float do not split.
        for m in BEGIN_ENV.finditer(line):
            env_stack.append(m.group(1))
            if m.group(1) in MATH_ENVS:
                chunk_has_math = True
        if "\\[" in line:
            chunk_has_math = True

        top_float = next((e for e in env_stack if e in FLOAT_ENVS), None)

        for m in END_ENV.finditer(line):
            name = m.group(1)
            if name in env_stack:
                # Pop back to the matching begin.
                while env_stack and env_stack.pop() != name:
                    pass

        if top_float:
            if not chunk:
                chunk_start = idx
            current.skipped.append({"line": idx, "env": top_float})
            continue

        sec = match_section(line)
        if sec:
            flush(idx - 1)
            kind, title = sec
            current = Section(
                id=f"sec{len(sections)}",
                level=LEVELS[kind],
                title=title,
                file=str(path),
                line=idx,
            )
            sections.append(current)
            continue

        if not line.strip():
            flush(idx - 1)
            continue

        if not chunk:
            chunk_start = idx
        chunk.append(line)

    flush(len(lines))

    # Drop a leading empty preamble placeholder.
    if sections and not sections[0].paragraphs and sections[0].title.startswith("(preamble"):
        sections.pop(0)
    return sections


# ------------------------------------------------------------- Markdown parser


MD_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MD_FENCE = re.compile(r"^\s*(```|~~~)")


def parse_md(path: Path) -> list[Section]:
    sections: list[Section] = []
    current = Section(id="sec0", level=1, title="(untitled)", file=str(path), line=1)
    sections.append(current)

    chunk: list[str] = []
    chunk_start = 0
    in_fence = False
    in_math = False
    chunk_has_math = False

    def flush(end_line: int) -> None:
        nonlocal chunk, chunk_start, chunk_has_math
        text = "\n".join(chunk).strip()
        chunk = []
        has_math, chunk_has_math = chunk_has_math, False
        if not text:
            return
        n_words = count_words(text)
        if n_words == 0:
            return
        paras = current.paragraphs
        paras.append(
            Paragraph(
                id=f"{current.id}-p{len(paras) + 1}",
                file=str(path),
                start_line=chunk_start,
                end_line=end_line,
                n_words=n_words,
                n_sentences=count_sentences(text),
                has_display_math=has_math,
                text=text,
            )
        )

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for idx, line in enumerate(lines, start=1):
        if MD_FENCE.match(line):
            in_fence = not in_fence
            if not in_fence:
                current.skipped.append({"line": idx, "env": "code block"})
            continue
        if in_fence:
            continue

        if line.strip() == "$$":
            in_math = not in_math
            chunk_has_math = True
            if not chunk:
                chunk_start = idx
            chunk.append(line)
            continue
        if in_math:
            chunk.append(line)
            continue

        m = MD_HEADING.match(line)
        if m:
            flush(idx - 1)
            current = Section(
                id=f"sec{len(sections)}",
                level=len(m.group(1)),
                title=m.group(2).strip(),
                file=str(path),
                line=idx,
            )
            sections.append(current)
            continue

        if line.strip().startswith("|"):
            current.skipped.append({"line": idx, "env": "table row"})
            continue

        if not line.strip():
            flush(idx - 1)
            continue

        if not chunk:
            chunk_start = idx
        chunk.append(line)

    flush(len(lines))
    if sections and not sections[0].paragraphs and sections[0].title == "(untitled)":
        sections.pop(0)
    return sections


# -------------------------------------------------------------------- reporting


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="path to a .tex or .md file")
    ap.add_argument("--section", help="keep only sections whose title contains this "
                                      "string (case-insensitive)")
    ap.add_argument("--follow-inputs", action="store_true",
                    help="follow \\input and \\include from a LaTeX root file")
    ap.add_argument("--json", help="write JSON here instead of stdout")
    ap.add_argument("--summary", action="store_true",
                    help="print a human-readable section/paragraph count only")
    args = ap.parse_args()

    path = Path(args.input)
    if not path.exists():
        sys.exit(f"error: file not found: {path}")

    if path.suffix.lower() in {".tex", ".ltx"}:
        sections = parse_tex(path, args.follow_inputs)
    elif path.suffix.lower() in {".md", ".markdown"}:
        sections = parse_md(path)
    else:
        sys.exit(f"error: unsupported extension '{path.suffix}'. Use .tex or .md.")

    if args.section:
        needle = args.section.lower()
        sections = [s for s in sections if needle in s.title.lower()]
        if not sections:
            sys.exit(f"error: no section title contains {args.section!r}")

    if args.summary:
        total = 0
        for s in sections:
            n = len(s.paragraphs)
            total += n
            words = sum(p.n_words for p in s.paragraphs)
            print(f"{s.file}:{s.line}  [{s.id}] {'  ' * s.level}{s.title}"
                  f"  — {n} paragraph(s), {words} words")
        print(f"\nTotal: {len(sections)} section(s), {total} paragraph(s)")
        return

    for s in sections:
        s.skipped = collapse_skipped(s.skipped)

    payload = {
        "source": str(path),
        "format": path.suffix.lstrip("."),
        "n_sections": len(sections),
        "n_paragraphs": sum(len(s.paragraphs) for s in sections),
        "sections": [asdict(s) for s in sections],
    }
    out = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.json:
        Path(args.json).write_text(out, encoding="utf-8")
        print(f"wrote {args.json}: {payload['n_sections']} section(s), "
              f"{payload['n_paragraphs']} paragraph(s)")
    else:
        print(out)


if __name__ == "__main__":
    main()
