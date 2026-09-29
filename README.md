# writing-simple-style

A [Claude Code](https://claude.com/claude-code) skill that reviews the writing style of a
paper, thesis or report — section by section, then paragraph by paragraph — and produces a
markdown report and a formatted PDF.

It checks three things for every paragraph:

- **Paragraph structure** — one topic, a topic sentence near the start, an ending that
  conforms to the beginning
- **Sentence structure** — fragments, dangling modifiers, ambiguous attribution,
  parallelism, word order, emphasis
- **Language** — specificity, conciseness, misused words, noun strings, terminology
  consistency, complete comparisons, quantified hedges

## What makes it different

**Audience and purpose are established first, per section.** The target reader of an
introduction is not the target reader of a methodology. ISO 24495 treats reader
characterization as the step everything else depends on, and so does this skill: it proposes
three audiences and three purposes drawn from the section you are actually reviewing, you
pick, and that choice changes what counts as a finding. Choose "specialists" and technical
terms need no definition; choose "practitioners" and an undefined term becomes an error.

**Every finding carries a rewrite.** Strunk's method is bad→better with the word count
attached. A diagnosis without a replacement sentence is hard to act on, so the report gives
one, in your terminology.

## Sources

| Source | Use |
| --- | --- |
| William Strunk Jr., *The Elements of Style* (1918) | Rules 6–18 and the "words commonly misused" list. Public domain, so the rule text and examples are quoted in `references/elements-of-style.md`. |
| ISO 24495-1:2023, *Plain language — Part 1: Governing principles and guidelines* | Sentence and paragraph guidance (§5.3.2–5.3.5). |
| ISO 24495-3, *Plain language — Part 3: Science writing* | Reader characterization, document planning, precise language (§5.3.3). |

**The ISO standards are copyrighted and are not included here.**
`references/iso-24495-plain-language.md` is a paraphrase written for this skill, with clause
numbers so you can look each item up in your own copy. Buy the standards from ISO or a
national member body if you want the source text.

Most of the paragraph- and sentence-level guidance actually lives in **Part 1** §5.3.3–5.3.5;
Part 3 §5.3.1 points back to it. Both parts are cited throughout for that reason.

## Where the skill departs from its sources

Both sources are applied with deliberate exceptions, because plain-language guidance written
for public communication does not transfer unchanged to a research paper:

1. **Passive voice is not flagged as such** — only passives that leave it unclear whose
   contribution is being described.
2. **Sentence-initial "However," is allowed.** Strunk forbids it; it is the standard contrast
   marker in related-work and gap statements.
3. **Established scientific terms are not simplified.** ISO 24495-3 §5.3.3 c) suggests
   everyday alternatives ("kidney disease" for "nephropathy"); in a paper that costs
   precision. The skill enforces the other half of the guidance instead — consistent use and
   definition at first appearance.
4. **The reader is not addressed as "you"** (ISO 24495-1 §5.3.3 b), since papers use
   first-person plural.
5. **Short sentences are not the goal.** Sentences carrying two ideas are flagged; long
   sentences developing one idea are not.
6. **Singular *they* is correct**, contra Strunk's 1918 entry.

Every deviation is documented in the reference files rather than applied silently.

## Install

Clone into your Claude Code skills directory:

```bash
git clone https://github.com/JakobThumm/writing-simple-style.git \
  ~/.claude/skills/writing-simple-style
```

Then invoke it with `/writing-simple-style` or just ask for feedback on your writing style.

## Usage

```
/writing-simple-style [path] [--section <name>] [--all] [--check <group>] [--no-pdf]
```

- `path` — a `.tex` or `.md` file. For a multi-file LaTeX project, pass the root file.
- `--section <name>` — review only sections whose title contains this string.
- `--all` — review the whole document.
- `--check <group>` — one family only: `A` (section fit), `P` (paragraph), `S` (sentence),
  `L` (language).
- `--no-pdf` — markdown report only.

The skill works best on **one section or chapter at a time**, and will tell you so with your
document's actual paragraph count before you choose.

## Requirements

- Python 3.10+ (standard library only)
- `pandoc` and a LaTeX engine, for the PDF step:
  ```bash
  sudo apt install pandoc texlive-latex-recommended texlive-latex-extra
  ```
  Without them the markdown report is still produced and is readable on its own. Check with:
  ```bash
  python3 scripts/generate_report_pdf.py --check-deps report.md
  ```

## Repository layout

```
SKILL.md                                  the skill definition and check catalogue
README.md
LICENSE
references/
  elements-of-style.md                    Strunk's rules, quoted, with academic adaptations
  iso-24495-plain-language.md             paraphrased ISO guidance with clause citations
scripts/
  split_paragraphs.py                     splits .tex/.md into sections and paragraphs
  generate_report_pdf.py                  markdown report -> PDF via pandoc
templates/
  output_template.md                      report skeleton
  report_latex.tex                        pandoc LaTeX template
```

`split_paragraphs.py` is usable on its own. Run it from a clone of this repository, or
give the full path to the installed copy:

```bash
# from a clone
python3 scripts/split_paragraphs.py paper.tex --summary
python3 scripts/split_paragraphs.py paper.tex --section Method --json paras.json

# from anywhere, once installed
python3 ~/.claude/skills/writing-simple-style/scripts/split_paragraphs.py paper.tex --summary
```

For a multi-file LaTeX project, pass the root file and add `--follow-inputs`; anchors then
point at the child file each paragraph actually lives in.

It keeps display maths attached to the paragraph it belongs to, skips floats, tables,
algorithms and code blocks, and reports line ranges so every finding can be anchored.

## Scope

This skill handles paragraph-level rhetorical structure. It deliberately leaves document-wide
mechanical consistency — abbreviations, math notation, figure references, tense, spelling
variant — to a proofreading pass, so the two do not produce duplicate findings.

It also cannot do what ISO 24495-1 §5.4.3 asks for: testing the document with real readers.
The report says so.

## License

MIT. See [LICENSE](LICENSE).

The MIT license covers this skill's own code and prose. It does not extend to ISO 24495,
which is not distributed here.
