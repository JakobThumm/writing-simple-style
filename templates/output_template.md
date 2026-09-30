# Writing Style Report — {{document_title}}

<!-- Keep these as a list: consecutive plain lines would merge into one paragraph. -->

- **Date:** {{date}}
- **Source:** {{source_path}}
- **Scope:** {{scope}}  <!-- "Section 3: Method (sec4, 7 paragraphs)" or "Whole document, 6 sections, 41 paragraphs" -->
- **Depth:** {{coarse | medium | full}}
- **Basis:** The Elements of Style (Strunk, 1918) and ISO 24495-1 / ISO 24495-3 plain language

---

# Summary

{{Two or three sentences naming the reader and the purpose of this section, and how they
were established — chosen by the author in medium and full, inferred from the text in
coarse. Then one sentence on what the writing already does well.}}

**Issues to address**

1. {{Recurring issue, with its count}} — e.g. "Eight agentless passives leave it unclear
   whether the authors or the system act (¶2, ¶4, ¶7)."
2. {{…}}
3. {{…}}

<!-- Maximum five items. Recurring patterns only: a count is what makes an item belong
     here. One-off slips stay in the per-paragraph sections below. Order by how much
     fixing the pattern improves the section. -->

---

## Marking scheme

| Tag | Meaning | How the span is marked |
|-----|---------|------------------------|
| ‹struct› | sentence structure — order, splitting, parallelism, emphasis | **bold** |
| ‹voice› | voice and attribution — who is doing what | **bold** |
| ‹cut› | needless words | ~~struck through~~ |
| ‹term› | ill-defined or inconsistent term | `monospace` |
| ‹word› | word used incorrectly | **bold** |

<!-- Use guillemets ‹ › for tags, never square brackets: a report is full of real
     citations like [12] and a bracketed tag is indistinguishable from one. -->

---

## Paragraph {{n}} — `{{file}}:{{start_line}}-{{end_line}}`

> {{The entire paragraph, copied verbatim from the source, unedited.}}

### General paragraph comments

{{Comments on paragraph structure: one topic or several, where the topic sentence sits,
whether the ending conforms to the beginning, how it connects to its neighbours. Omit this
heading entirely when there is nothing to say about the paragraph as a whole.}}

### Per-sentence comments

{{Only sentences that carry an issue. Repeat the sentence with the offending spans marked,
then list the issues beneath it.}}

**A survey of this region was made** ‹voice› in 1900, ~~due to the fact that~~ ‹cut› the
apparatus was available.

- ‹voice› Nominalized passive: the sentence names no agent, so the reader cannot tell
  whether this is your survey or a cited one. → "We surveyed this region in 1900."
- ‹cut› "due to the fact that" → "because" (12 → 6 words).

<!-- If the paragraph has no issues at all, write exactly this line under the paragraph
     text and move on. Never omit a paragraph: omission reads as an oversight. -->

*No issues found.*

---

## Writing the per-sentence comments

- **Mark the span, not the whole sentence**, unless the whole sentence is the problem.
- **One bullet per marked span**, opening with the same tag, so the mark and the
  explanation are unambiguous.
- Each bullet is a short description of the mistake, then the fix after `→`. For ‹cut›,
  give the word count: `(34 → 21 words)`.
- Keep the author's terminology and register in every rewrite.
- Never invent a citation, a number, or a technical claim. If a rewrite needs a fact you do
  not have, say what is missing instead.
- Never put a language tag on a fenced code block: pandoc then emits highlighting macros
  and the PDF build fails. Plain ``` fences are safe.
- Use a `>` blockquote only for the verbatim paragraph text. Inside a list item a
  blockquote does not nest, so quote short spans in backticks there.

---

## Terminology against published ISO standards

<!-- Full depth only, and only when the iso-obp MCP server answered. Omit the whole
     section otherwise, and say so under "Not assessed". -->

Checked {{n}} candidate terms against {{n_sources}} indexed corpora ({{n_entries}} entries).

| Term | Status | Standard / clause | Note |
|------|--------|-------------------|------|
| {{term}} | defined | ISO 8373:2021 §3.1 | usage matches |
| {{term}} | defined, standards differ | ISO 12100 §3.6; ISO/PAS 8800 §3.3.5 | state which sense is meant |
| {{term}} | not in index | — | no definition in the indexed corpora |

**Read `not in index` correctly.** It means the term is absent from the corpora listed
above, not that ISO defines it nowhere. Novel research terms land here as a matter of
course, and that is not a defect.

**Known coverage gap:** ISO 10218-1 is not indexed, because the available copies are
ISO/DIS drafts the extractor cannot parse. A robot-safety term defined there can appear
as `not in index`. Treat a miss on such a term as unverified, not unstandardized.

---

## Not assessed

This review covers running prose only. A clean report does not imply the following are in
order:

- Ethical presentation of content (ISO 24495-3 §5.1.6)
- Figures, images, data displays and table design (§5.3.4–5.3.7)
- Abbreviation introduction, math notation, citation consistency — use the
  `proofreading` skill for these
<!-- Coarse and medium only: -->
- Checks outside the seven priority rules. This was a {{coarse|medium}} review; run it at
  full depth for the complete set.
<!-- Only when the server was unreachable: -->
- Terminology against published ISO standards: the `iso-obp` MCP server was not reachable,
  so no term was verified against published terminology.
- **Usability testing with real readers (ISO 24495-1 §5.4.3).** ISO treats an author's own
  review as the §5.4.2 step only. The standard is explicit that the sole way to learn how
  readers react is to involve them. This report does not replace that.
