# Writing Style Report — {{document_title}}

<!-- Keep these as a list: consecutive plain lines would merge into one paragraph. -->

- **Date:** {{date}}
- **Source:** {{source_path}}
- **Scope:** {{scope}}  <!-- e.g. "Section 3: Method (sec4, 7 paragraphs)" or "Whole document, 6 sections, 41 paragraphs" -->
- **Basis:** The Elements of Style (Strunk, 1918) and ISO 24495-1 / ISO 24495-3 plain language

---

## Scope and reader profile

One row per reviewed section. Every finding below is judged against the audience and
purpose recorded here, so a reader can audit the review against its own assumptions.

| Section | Audience | Purpose | Genre | Paragraphs | Words |
|---------|----------|---------|-------|------------|-------|
| {{section_title}} | {{audience}} | {{purpose}} | {{genre}} | n | n |

---

## Scorecard

| Group | Check family | Errors | Warnings | Info | Total |
|-------|--------------|--------|----------|------|-------|
| A | Section and audience fit | n | n | n | n |
| P | Paragraph structure      | n | n | n | n |
| S | Sentence structure       | n | n | n | n |
| L | Language                 | n | n | n | n |
|   | **Total**                | **n** | **n** | **n** | **n** |

**Paragraph density:** n findings across n paragraphs (n.n per paragraph).

---

## Overall assessment

{{overall_assessment}}

<!-- 3-5 sentences. Name the two or three habits that drive most findings, rather than
     restating counts. Say what the writing already does well: a report that only lists
     faults gives the author no signal about what to preserve. -->

### Top issues to address

1. **[SEVERITY] Check X.n — {{issue}}** ({{n}} occurrences, e.g. {{anchor}})
2. **[SEVERITY] Check X.n — {{issue}}** ({{n}} occurrences, e.g. {{anchor}})
3. **[SEVERITY] Check X.n — {{issue}}** ({{n}} occurrences, e.g. {{anchor}})

<!-- 3-6 items, ordered by how much the fix improves the section. Recurring patterns
     outrank one-off slips: "eight agentless passives" beats "one dangling modifier". -->

---

## Terminology against published ISO standards (L9)

<!-- Omit this whole section if the iso-obp MCP server was unavailable, and say so
     under "Not assessed" instead. -->

Checked {{n}} candidate terms against {{n_sources}} indexed corpora ({{n_entries}} entries)
via the `iso-obp` server.

| Term | Status | Standard / clause | Note |
|------|--------|-------------------|------|
| {{term}} | defined | ISO 8373:2021 §3.1 | usage matches |
| {{term}} | not in index | — | no definition in the indexed corpora |

**Read `not in index` correctly.** It means the term is absent from the corpora listed
above, not that ISO defines it nowhere. Novel research terms land here as a matter of
course, and that is not a defect.

Findings that arise from this table appear under **Language** with the other L-checks.

---

## A. Section and audience fit

**Summary:** {{section_level_summary}}

### Findings

{{a_findings}}

---

## Section: {{section_title}}

**Audience:** {{audience}} · **Purpose:** {{purpose}} · **Genre:** {{genre}} · **Paragraphs:** n · **Words:** n · **Findings:** n

<!-- Keep that on one physical line. Two adjacent lines merge into one paragraph
     when rendered, which reads as a run-on. Repeat everything below, once per
     reviewed section. -->

### Paragraph {{n}} — `{{file}}:{{start_line}}-{{end_line}}` (`{{para_id}}`)

> {{first sentence of the paragraph, or the whole paragraph if under 40 words}}

**Topic:** {{one clause naming what this paragraph is about}} · **Shape:** n sentences, n words, topic sentence {{at start | at sentence n | absent}}

<!-- If the paragraph is clean, write exactly this and move on: -->
*No issues found.*

#### Paragraph structure

{{p_findings}}

#### Sentence structure

{{s_findings}}

#### Language

{{l_findings}}

---

## Finding format

Each finding is a list item with a nested list. The **rewrite is the point** — a
diagnosis without a concrete alternative is hard to act on.

```
- [SEVERITY] P2 — `file.tex:118` — topic sentence appears only in sentence 4.
  - Text: `Many approaches exist for this problem. Early work used A. Later work used B.`
  - Why: Strunk Rule 9; ISO 24495-1 §5.3.5 b). The reader carries three sentences
    before learning what the paragraph is for.
  - Rewrite: Long-horizon settings break the assumptions of existing approaches.
    Early work used A and later work used B, but both assume a short horizon.
```

Rules for findings:

- **Anchor** every finding to `file:line`, taken from the splitter output.
- **Quote** only the offending span, up to about 80 words, and always inside
  backticks. A `>` blockquote does not work inside a list item, and backticks keep
  the author's own LaTeX macros from being executed when the PDF is built.
- Use a `>` blockquote only at the top level, for the paragraph preview under each
  `### Paragraph n` heading.
- **Why** names the source rule: `Strunk Rule N` and/or `ISO 24495-x §5.y.z item`.
  One line. Do not paste the rule text.
- **Rewrite** gives a concrete replacement in the author's own voice and terminology.
  For conciseness findings, append the word count: `(34 → 21 words)`.
- Never invent a citation key, a number, or a technical claim that is not already in
  the source text. If a rewrite needs a fact you do not have, say what is missing
  instead of inventing it.

Severity:

- `[ERROR]` — a clear rule violation that a reader will notice: sentence fragment,
  dangling modifier, missing topic sentence, broken parallelism in a list.
- `[WARN]` — likely a problem, but it depends on intent: agentless passive, long
  sentence, buried emphasis, hedge without a number.
- `[INFO]` — a preference worth one look: word-choice notes, mild wordiness.

---

## Not assessed

This review covers running prose only. The following parts of ISO 24495 Annex B were
not evaluated, and a clean report above does not imply they are in order:

- Ethical presentation of content (ISO 24495-3 §5.1.6)
- Figures, images and data displays (§5.3.4–5.3.6)
- Table design (§5.3.7)
- Abbreviation introduction, math notation, citation consistency — use the
  `proofreading` skill for these
<!-- Include the next line only when the server was unavailable: -->
- Terminology against published ISO standards (check L9): the `iso-obp` MCP server was
  not reachable, so no term was verified against published terminology.
- **Usability testing with real readers (ISO 24495-1 §5.4.3).** ISO treats an author's
  own review as the §5.4.2 step only. The standard is explicit that the sole way to
  learn how readers react is to involve them. This report does not replace that.
