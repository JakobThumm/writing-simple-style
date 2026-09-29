---
name: writing-simple-style
description: Review the writing style of a paper, thesis or report section by section and paragraph by paragraph. Identifies the target audience and purpose of each section together with the user, then checks paragraph structure, sentence structure and language against The Elements of Style and the ISO 24495 plain language standards. Produces a markdown report and a formatted PDF. Use when the user asks for style feedback, a readability or plain-language review, or help making a section clearer.
allowed-tools: Read Bash Edit Write AskUserQuestion Glob Grep mcp__iso-obp__corpus_info mcp__iso-obp__lookup_term mcp__iso-obp__lookup_terms mcp__iso-obp__search_terms
license: MIT
metadata:
    skill-author: Jakob Thumm
---

# Writing Simple Style

## Overview

Walk a document one section at a time and one paragraph at a time, and return concrete,
rewrite-first feedback on **paragraph structure**, **sentence structure**, and **language**.

Two things make this different from a generic style pass:

1. **Audience and purpose are established first, per section, with the user.** The target
   reader of an introduction is not the target reader of a methodology. ISO 24495 treats
   reader characterization as the step that everything else depends on, and this skill
   treats it the same way. The declared audience changes what counts as a finding.
2. **Every finding carries a rewrite.** Strunk's method is bad→better with the word count
   attached. A diagnosis without a replacement sentence is hard to act on.

The output is a markdown report, then a formatted PDF generated from it.

## When to use this skill

- The user asks for feedback on writing style, clarity, readability, or flow
- The user asks for a plain-language review, or mentions ISO 24495
- A section reads badly and the user wants to know why
- A draft is finished and needs a language pass before a proofreading pass

Use the `proofreading` skill instead when the user wants mechanical, document-wide
consistency checks: abbreviations, math notation, figure references, tense, citations.
The two are complementary, and this skill deliberately does not duplicate them
(see [Scope and non-goals](#scope-and-non-goals)).

## Arguments

```
/writing-simple-style [path] [--section <name>] [--all] [--check <group>] [--no-pdf]
```

- `path` — a `.tex` or `.md` file. For a multi-file LaTeX project, pass the root file;
  the skill follows `\input` and `\include`. Defaults to the current directory.
- `--section <name>` — review only sections whose title contains this string. Skips the
  scope prompt.
- `--all` — review the whole document. Skips the scope prompt.
- `--check <group>` — run only one check family: `A`, `P`, `S`, or `L`.
- `--no-pdf` — write the markdown report but skip PDF generation.

---

# Core workflow

The skill runs in four phases. Phases 0 and 1 are interactive; phases 2 and 3 are not.

**Do not turn phase 2 into a conversation.** "Go through each paragraph individually" means
the *analysis and the report* are per paragraph, not that the user is asked a question per
paragraph. A 40-paragraph section must not produce 40 prompts. There are exactly two
interaction points: scope, and audience/purpose per section.

---

## Phase 0: Resolve input and agree the scope

### 0.1 Find the document

1. If `path` is a file, use it. If it is a directory or omitted, look for `main.tex`,
   `paper.tex`, `thesis.tex`, or a single `.tex` / `.md` at the top level. If several
   candidates exist, list them and ask which one.
2. Unsupported extension: say so and stop. This skill handles `.tex` and `.md`.

### 0.2 Map the document

Run the splitter to get the section and paragraph inventory:

```bash
python3 ~/.claude/skills/writing-simple-style/scripts/split_paragraphs.py <path> --summary
```

For a LaTeX root file that pulls in section files, add `--follow-inputs`.

This prints one line per section with its paragraph and word counts. Keep the numbers —
they make the scope warning concrete rather than generic.

### 0.3 Agree the scope

**Always tell the user that the skill works best on a single section or chapter**, and give
the reason: audience and purpose are set per section, and a per-paragraph review of a whole
paper produces a report too long to act on in one sitting.

Then ask, with `AskUserQuestion`, offering the real section titles from step 0.2 as options:

> This skill works best on one section or chapter at a time. Audience and purpose are
> established per section, and per-paragraph feedback on a whole document runs long —
> your document has **{N} sections and {M} paragraphs**, which would be roughly {M} blocks
> of feedback.
>
> What should I review?

Options to offer:

- The two or three largest or most likely sections by name, each with its paragraph count
  (e.g. "Section 3: Method — 12 paragraphs")
- "The whole document — {M} paragraphs across {N} sections"

If the user picks the whole document, accept it without arguing further. They have been
told the trade-off; repeating it is not useful. For a whole-document run, still ask for
audience and purpose **per section** in phase 1, batching the questions where sections
plainly share a reader.

`--section` or `--all` skips this prompt entirely.

### 0.4 Extract the paragraphs

```bash
python3 ~/.claude/skills/writing-simple-style/scripts/split_paragraphs.py <path> --section "<title>" --json /tmp/paras.json
```

Read the JSON. Each paragraph carries `id`, `file`, `start_line`, `end_line`, `n_words`,
`n_sentences`, `has_display_math`, and `text`. Use `id` and the line range as the anchor for
every finding — never guess a line number.

Note what the splitter skipped (`skipped` ranges: tables, figures, algorithms, code blocks).
Those are out of scope; say so in the report rather than silently ignoring them.

---

## Phase 1: Establish audience and purpose (per section)

ISO 24495-3 §5.1.2 makes reader characterization the first step of science writing, and
§5.1.4 does the same for purpose. ISO 24495-3 §5.1.3 adds genre.

### 1.1 Read the section first

Read the section before proposing anything. The options must be grounded in what the text
actually does, not in generic categories. A methodology full of proofs implies a different
reader than one full of implementation detail.

### 1.2 Propose three audiences and three purposes

Use **one** `AskUserQuestion` call containing both questions (and genre as a third if it is
genuinely unclear). Each question offers exactly three options. The tool adds "Other"
automatically, so the user can always override.

Split each option across the tool's two fields. `label` takes a short noun phrase of one
to five words, or it will be truncated in the UI. `description` takes the concrete reader
picture and what choosing it implies. So not `label: "Researchers in the wider field who
know the area but not the notation"`, but:

```
label:       "Wider field"
description: "Researchers in adjacent areas who know the problem but not your
              notation. Subfield terms will need a one-clause definition at first use."
```

The tables below give the option *content*; the bold phrase is the `label` and the rest
belongs in `description`.

Three audience options, calibrated to the section you just read:

| Typical option | What it implies for the checks |
| --- | --- |
| **Specialists in the subfield** — reviewers and direct competitors | Technical terms need no definition. Method detail is expected in full (ISO 24495-3 §5.1.5 h). Jargon threshold: high. |
| **Researchers in the wider field** — adjacent areas, program committee members outside the niche | Subfield terms need a brief in-context definition at first use (ISO 24495-3 §5.3.3 b). Method detail expected, but the reason for each step must be visible. |
| **Practitioners or decision makers** — engineers, reviewers of a proposal, industrial readers | Method depth should be cut to what justifies trusting the result (§5.1.5 h). Every specialized term needs a definition or a plainer equivalent. Implications lead (§5.2.3 a). |

Three purpose options, again from ISO 24495-3 §5.1.4:

| Typical option | What it implies |
| --- | --- |
| **Convince the reader that the problem matters and the approach is new** (introduction, motivation) | Claims must be specific and supported. Emphasis position matters most. |
| **Enable the reader to understand and reproduce the method** (method, system description) | Precision and consistent terminology dominate. Attribution must be unambiguous. |
| **Report what was found and what it means** (results, discussion, conclusion) | Status of information must be explicit (§5.3.2 e). Comparisons must name both sides (§5.3.3 f). Hedges must be quantified (§5.3.3 g). |

Adapt the wording to the actual section. For a related-work section, for instance, the
purpose is usually "position this work against existing approaches and expose the gap".

### 1.3 Record the answer and use it

Write the chosen audience, purpose and genre into the report header for that section. Then
apply them. **The selection must change the output**; if the same findings would appear
regardless of the answer, the prompt was theatre. Specifically:

| The user chose | Then |
| --- | --- |
| Specialists | Do not flag established technical terms as jargon (L6 enforces *consistency* only, L9 only contradictions and synonym drift). Do not flag missing definitions of standard terms. |
| Wider field | Flag subfield terms used without a brief definition at first use (L6, L9). |
| Practitioners | Flag undefined specialized terms as `[ERROR]` (L6, L9). Flag method paragraphs whose detail exceeds what the purpose needs (A5). |
| Purpose = convince | Weight S7 (emphasis at end) and L2 (specific language) up. |
| Purpose = enable reproduction | Weight L6 (terminology consistency) and S3 (attribution) up. |
| Purpose = report findings | Weight L7 (incomplete comparison) and L8 (unquantified hedge) up. |

---

## Phase 2: Run the checks

Work through the section once at section level (group A), then paragraph by paragraph
(groups P, S, L). Collect findings; do not report yet.

Load the two reference files before judging anything:

- `~/.claude/skills/writing-simple-style/references/elements-of-style.md` — Strunk's rule text, examples, and the academic
  adaptations that override him
- `~/.claude/skills/writing-simple-style/references/iso-24495-plain-language.md` — paraphrased ISO guidance with clause numbers

For every finding produce: anchor, quoted span, one-line reason citing the rule, and a
**rewrite**. See the finding format in `templates/output_template.md`.

### Group A — Section and audience fit

Run once per section.

#### A1. Heading predicts content
*ISO 24495-1 §5.2.4.* The heading should let a reader predict what the section contains.
- `[WARN]` if the section's content does not match what its heading promises.
- `[INFO]` if the heading is a bare label ("Model", "Results") where a short informative
  heading would tell the reader more.

#### A2. Structure is recoverable from headings alone
*ISO 24495-3 §5.2.4 d).* Test: list the headings and subheadings with no body text. Can a
reader reconstruct the argument?
- `[WARN]` if the heading list alone does not convey the line of reasoning.
- `[WARN]` if sibling headings are not grammatically parallel (ISO 24495-3 §5.3.3 e):
  "Collecting the data" / "Model architecture" / "We evaluate".
- `[INFO]` if one subsection carries most of the section's content, suggesting a split.

#### A3. Key information leads
*ISO 24495-3 §5.2.3 a), §5.2.2.* Essential material — the main conclusion, the implication,
the purpose of the section — should come early.
- `[WARN]` if the section's main point appears only in its final paragraph.
- `[INFO]` if a long section (>8 paragraphs) opens without an orienting sentence saying
  what it covers.

#### A4. Status of information is explicit
*ISO 24495-3 §5.3.2 e).* A reader must always know whether a sentence states an assumption,
a hypothesis, a method, a result, an interpretation, or a limitation.
- `[ERROR]` if an interpretation or extrapolation is written in the same register as a
  measured result, so the two are indistinguishable.
- `[WARN]` if an assumption is used without ever being marked as one.
- `[WARN]` if the section presents results with no statement of their limits (§5.1.5 j),
  where the declared purpose is to report findings.

#### A5. Depth matches the declared audience
*ISO 24495-3 §5.1.5 h).* This is the check that makes phase 1 load-bearing. The standard is
explicit that method depth should be calibrated to the reader.
- `[WARN]` if the audience is **practitioners or decision makers** and a method paragraph
  gives derivation detail that does not help them judge whether to trust the result.
- `[WARN]` if the audience is **specialists** and the method omits detail they would need
  to assess reliability.
- `[ERROR]` if the audience is **wider field** or **practitioners** and a specialized term
  carries no in-context definition at first use (§5.3.3 b).
- `[INFO]` if the density of undefined notation in one paragraph is far above the section
  average, given the declared reader.

### Group P — Paragraph structure

Run for every paragraph.

#### P1. One topic per paragraph
*Strunk Rule 8; ISO 24495-1 §5.3.5 a).*
State the paragraph's topic in a single clause. If the clause needs an "and" joining
unrelated claims, there are two topics.
- `[ERROR]` if the paragraph covers two topics. Name the sentence where the second begins
  and propose the split point.
- `[INFO]` if two consecutive paragraphs share one topic and should be merged.

#### P2. Topic sentence at or near the start
*Strunk Rule 9 a); ISO 24495-1 §5.3.5 b).*
- `[ERROR]` if the paragraph has no topic sentence at all.
- `[WARN]` if the topic sentence appears after sentence 2. Strunk allows a preceding
  transition sentence; he does not allow three sentences of run-up.
- Do not flag a single transition sentence before the topic sentence. That is explicitly
  permitted.

#### P3. The ending conforms to the beginning
*Strunk Rule 9 c).* The last sentence should reinforce the topic or state its consequence.
- `[WARN]` if the paragraph ends on a digression or a minor detail. Strunk singles this out
  as the fault most worth avoiding.
- `[WARN]` if the paragraph ends with filler that adds no content ("This concludes the
  description of the model.").
- `[INFO]` if the last sentence introduces a new idea that belongs in the next paragraph.

#### P4. Single-sentence paragraphs
*Strunk Rule 8.*
- `[WARN]` for a one-sentence paragraph, unless it is a transition between major parts,
  which Strunk permits.

#### P5. Connection to neighbouring paragraphs
*ISO 24495-1 §5.3.5 c); ISO 24495-3 §5.2.3 c).*
- `[WARN]` if the paragraph has no link to the one before and the topic shift is abrupt.
- `[INFO]` if three or more consecutive paragraphs open with the same connective
  ("Furthermore", "Moreover", "In addition"), which signals a list that should be itemized.
- `[INFO]` if the paragraph is unusually long (>200 words or >9 sentences) — report the
  number and ask whether it holds one topic or several.

### Group S — Sentence structure

Run for every paragraph, reporting per sentence.

#### S1. Do not break sentences in two
*Strunk Rule 6.*
- `[ERROR]` for a fragment that reads as a dropped comma ("We evaluate on three tasks.
  Each involving a different robot.").
- `[WARN]` for a fragment that reads as deliberate emphasis. Strunk permits it but warns it
  will be mistaken for a blunder.

#### S2. Dangling participles and modifiers
*Strunk Rule 7.* An opening participial phrase, adjective phrase, or appositive must refer
to the grammatical subject.
- `[ERROR]` for any dangling opener. The academic archetype: "Using a Kalman filter, the
  measurements are fused." → "Using a Kalman filter, we fuse the measurements."

#### S3. Attribution, not passive voice as such
*Strunk Rule 10, adapted; ISO 24495-1 §5.3.3 c).*
**Do not flag the passive voice by itself.** Flag passives that leave it unclear whose
contribution is being described.
- `[WARN]` for an agentless passive where the reader cannot tell whether the authors, prior
  work, or the system is responsible: "A safety filter is applied to the output."
- Do **not** flag a passive whose agent is fixed by context ("In this work, ... is used"),
  or one describing a property of the system ("The torque is limited to 40 N m"), or one
  where the passive puts the right noun in subject position (Strunk's own exception).
- `[WARN]` for the nominalized passive: "A comparison of the two methods was performed" →
  "We compared the two methods."
- `[WARN]` for `there is` / `there are` / `it can be seen that` openings that a direct verb
  would replace.

#### S4. Succession of loose sentences
*Strunk Rule 14.*
- `[WARN]` for three or more consecutive sentences of the form
  `[clause], and/but/so/which [clause]` in one paragraph. Report the run, not each sentence,
  and propose recasting some as simple or semicolon-joined sentences.

#### S5. Parallel form for co-ordinate ideas
*Strunk Rule 15; ISO 24495-3 §5.3.3 e).*
- `[ERROR]` if items in an enumerated or itemized list do not share a grammatical form.
  Highest yield in contribution lists and hypothesis lists.
- `[ERROR]` if correlatives (`both…and`, `not only…but also`, `either…or`) are followed by
  different parts of speech.
- `[WARN]` if a series repeats an article or preposition before some members but not all.

#### S6. Keep related words together
*Strunk Rule 16; ISO 24495-1 §5.3.3 a) 3).*
- `[WARN]` if a phrase or clause separates the subject from its verb and could move to the
  front of the sentence. The common offender is a citation pile-up: "Reinforcement learning
  (applied to manipulation [3], locomotion [7] and navigation [12]) suffers from sample
  inefficiency."
- `[WARN]` if a relative clause is separated from its antecedent so that it could attach to
  the wrong noun.
- `[WARN]` for a misplaced `only`, `also`, or `not`: "All the methods do not converge" →
  "Not all the methods converge."

#### S7. Emphatic words at the end
*Strunk Rule 18.*
- `[WARN]` if a result sentence buries its finding and ends on a citation, a hedge, or a
  setup clause: "Our method reduces collisions by 30 %, as shown in Table 2." → "As shown in
  Table 2, our method reduces collisions by 30 %."
- `[INFO]` if the new information sits at the start and the given information at the end,
  inverting the natural emphasis.

#### S8. One idea per sentence
*ISO 24495-1 §5.3.4 a), c).*
- `[WARN]` if a sentence over ~35 words carries more than one idea. **Length alone is not a
  finding** — a long sentence developing one idea is fine.
- `[INFO]` if a paragraph's sentence lengths are near-uniform. ISO §5.3.4 c) asks for varied
  length; uniformly short sentences read as a list.

#### S9. Given before new
*ISO 24495-1 §5.3.3 a) 4).*
- `[WARN]` if a sentence opens with information the reader has not met yet while the
  already-known material sits at the end, breaking the link to the previous sentence.

### Group L — Language

Run for every paragraph.

#### L1. Statements in positive form
*Strunk Rule 11.*
- `[WARN]` for a negative used as evasion: "does not perform well" → "performs poorly";
  "is not able to" → "cannot"; "did not consider" → "ignored".
- Do not flag a deliberate antithesis ("not charity, but simple justice") or a negation
  that is the actual claim ("the constraint is not satisfied").

#### L2. Definite, specific, concrete language
*Strunk Rule 12.*
- `[ERROR]` for an unquantified comparative claim: "substantially faster", "significantly
  better", "greatly reduces" with no number anywhere in the sentence.
- `[WARN]` for a vague mechanism: "a suitable technique is applied", "appropriate
  parameters were chosen". Name the technique or the parameter.
- `[WARN]` for vague scale: "a large dataset", "many experiments", "high accuracy".

#### L3. Omit needless words
*Strunk Rule 13; ISO 24495-1 §5.3.4 b).* The highest-volume check. **Always give the word
count delta.**
- `[WARN]` for each padded construction. Strunk's list: `the fact that`, `the question as
  to whether`, `there is no doubt but that`, `in a … manner`, `he is a man who`, `this is a
  … which`, `owing to the fact that`, `in spite of the fact that`, `for … purposes`, and
  superfluous `who is` / `which was`.
- `[WARN]` for a chain of short sentences developing one idea step by step that would be
  stronger combined. Give both versions with word counts, as Strunk does (51 → 26).
- `[INFO]` for softeners that add nothing: `it is important to note that`, `it should be
  mentioned that`, `in order to` (→ `to`), `a number of` (→ the number).
- Report conciseness findings **per paragraph with a total**, not one bullet per phrase.
  "Six padded constructions, 47 words removable (312 → 265)" is more useful than six bullets.

#### L4. Words and expressions commonly misused
*Strunk Chapter V.* Use the filtered table in `~/.claude/skills/writing-simple-style/references/elements-of-style.md`. That table
carries the severity for each entry and lists the entries this skill deliberately drops.
- Respect the exceptions recorded there: do **not** flag sentence-initial "However,";
  do **not** flag `feature` in its machine-learning sense or `state` as a system-state noun;
  do **not** apply Strunk's obsolete entries (`shall`/`will`, split infinitive, or his
  "use *he*" advice on singular *they*).
- `[WARN]` for `very`, `quite`, `rather`, `certainly`, `so` as intensifiers.
- Group repeated hits on one word into a single finding with a count.

#### L5. Noun strings
*ISO 24495-3 §5.3.3 h).* Highest-yield precision check for engineering prose.
- `[ERROR]` for a run of four or more nouns used as one compound.
- `[WARN]` for three nouns where the relation between them is ambiguous.
- Rewrite by inserting the verb and preposition that the string omits: "safety shield
  reachability analysis module" → "the module that performs reachability analysis for the
  safety shield".

#### L6. Terminology consistency
*ISO 24495-1 §5.3.2 g); ISO 24495-3 §5.3.3 a), b).*
**Note the deliberate inversion.** ISO 24495-3 §5.3.3 c) suggests everyday alternatives to
technical terms. For a research paper that costs precision, so this skill does **not** ask
authors to simplify established scientific terms. It enforces the other half instead:

- `[ERROR]` for synonym drift — two or more terms used for one concept ("safety shield",
  "safety layer", "protective module"). Pick one and use it throughout. List every variant
  with its anchor.
- `[ERROR]` for one term used for two concepts.
- `[WARN]`, **only if the declared audience is wider-field or practitioner**, for a
  specialized term with no brief in-context definition at first use.
- `[INFO]` if a term is introduced with a definition and then never used again.

L6 needs no external source. L9 adds the check against published terminology.

#### L7. Complete comparisons
*ISO 24495-3 §5.3.3 f).* A comparison must name both sides.
- `[ERROR]` for a comparative with no stated reference: "our method achieves lower error"
  — lower than what?
- `[WARN]` for "improves", "outperforms", "reduces" where the baseline is implied by
  context but not named in the sentence.

#### L8. Hedges tied to evidence
*ISO 24495-3 §5.3.3 g).* Hedging is legitimate and expected; ISO asks that it be deliberate
and, where possible, quantified.
- `[WARN]` for a hedge on a claim the data could quantify: "performance is typically good"
  → "accuracy is 94 % on average across the five tasks".
- `[WARN]` for stacked hedges: "may potentially be able to somewhat improve".
- `[INFO]` if a hedge is absent where the evidence does not support the strength of the
  claim — a single-setting experiment stated as a general result.
- Do not flag a hedge that correctly marks genuine uncertainty. That is the standard's
  intent, not a fault.

#### L9. Technical terms against published ISO terminology
*ISO 24495-1 §5.3.2 a), c), g); ISO 24495-3 §5.3.3 b), d).*

Where L6 checks that the section is internally consistent, L9 checks it against terminology
that has already been standardized. A term with a published ISO definition is the precise
one to use, and using it in a sense the standard does not support is a real defect —
especially in safety and robotics writing, where the definition may carry legal weight.

This check requires the **`iso-obp` MCP server**. Run it **once per section**, not per
paragraph, so the whole section costs one batch call.

**Step 1 — check availability and scope.**

Call `corpus_info` first. It reports which corpora are indexed and how many entries each
holds. Record the source count and total in the report. If the server is unavailable or
returns an error, skip L9 entirely, note it under "Not assessed", and continue with the
rest of the review. **A missing server is not a finding.**

**Step 2 — collect candidate terms.**

From the section, gather multi-word and single-word noun phrases that read as domain
terminology: `collaborative robot`, `protective separation distance`, `machine learning
model`, `safety-rated monitored stop`. Exclude ordinary prose nouns, author-invented method
names, and symbols. Deduplicate and normalize to lower case. Twenty to sixty candidates for
a typical section is normal.

**Step 3 — one batch lookup.**

Call `lookup_terms` with the full candidate list. Do not loop over `lookup_term`.

**Step 4 — read the status field precisely.** This is where the check goes wrong if rushed.
The server returns four statuses and they are not interchangeable:

| Status | Meaning | What to do |
| --- | --- | --- |
| `defined` | A standard in the index defines this term. | Cite the standard and clause. Compare the paper's usage with the definition. |
| `defined_by_your_transcription` | The user transcribed it by hand from a standard they hold. It cites a source, but the wording is not verified against the published text. | Treat as defined; add "transcription not verified against the published text" to the finding. |
| `defined_by_you_only` | The user's own working definition, from their glossary. **No standard defines it.** | `[WARN]` if the section does not introduce it explicitly. It is a private convention, not established terminology. |
| `not_defined` | Absent from the indexed corpora. | **Not a finding on its own.** See step 5. |

**Never report `not_defined` as "ISO does not define this term".** The index covers the
corpora that were ingested locally, not all of ISO. The correct phrasing is "no definition
in the indexed corpora (n sources)".

**Step 5 — use `match_type` to catch non-preferred designations.**

Each definition carries a `match_type`. When it is `synonym`, the paper used an admitted
synonym and the `term` field holds the standard's **preferred** designation. This is the
cheapest, most reliable synonym-drift signal in the check, and it comes back from the same
batch call — no extra lookup.

Example: looking up `neural net` returns `match_type: "synonym"`, `term: "neural network"`,
`standard: "ISO/IEC 22989:2022"`, `clause: "3.4.8"`, with `synonyms: ["NN", "neural net",
"artificial neural network"]`.

- `[WARN]` when `match_type` is `synonym`: the concept is standardized under a different
  preferred designation. Propose the preferred term, cite standard and clause, and note the
  admitted synonyms so the author can judge.
- Other useful fields on a match: `verbatim_from_source` (false means the wording was not
  taken directly from the published text), `notes` (the standard's own notes, often the
  clearest explanation of scope), and `entry_number`.

**Step 5b — only then, for `not_defined`, try the concept.**

Call `search_terms` with the term as keywords, for the terms that came back `not_defined`.
This catches a concept standardized under a wording too different for the synonym index.

- `[WARN]` only if the result is genuinely the same concept under a standardized
  designation. Cite standard and clause.
- If the results are merely adjacent, record the term as unverified and move on. Do **not**
  flag it. Looking up `collaborative robot`, for instance, returns `not_defined` and the
  search yields `collaborative operation`, `collaborative workspace` and `collaborative
  task` — related vocabulary, none of them the same concept. That is a no-finding.
- A term absent from the index is the normal case for novel research.

**Step 6 — findings.**

- `[ERROR]` if the paper uses a term with a published ISO definition in a sense that
  contradicts that definition. Quote both. This is the highest-value finding the check
  produces — a redefined safety term is a substantive error, not a style note.
- `[WARN]` if the paper defines in its own words a term that a standard already defines, and
  the two differ in scope. Propose adopting the standard definition, or state explicitly in
  the text that the paper departs from it and why.
- `[WARN]` for a non-preferred designation where a standardized one exists (step 5 / 5b).
- `[WARN]` for a `defined_by_you_only` term that the section never introduces.
- `[INFO]` for each term confirmed `defined`, listed compactly in one table rather than one
  finding each. Confirmation is useful to the author, but not as forty separate bullets.

**Audience gating**, consistent with phase 1:

- **Specialists** — an ISO-defined term needs no gloss in the text. Only contradictions and
  synonym drift are findings.
- **Wider field** — `[WARN]` if an ISO-defined term is used with no brief in-context
  definition at first use (ISO 24495-3 §5.3.3 b).
- **Practitioners** — as above, at `[ERROR]`.

**Never call `define_term` or `remove_term`.** Those write to the user's glossary file on
disk, and that file is part of what later answers whether a term is defined. Writing a
definition you inferred would corrupt the source of truth. If the user asks you to record a
term, that is a separate, explicit request.

---

## Phase 3: Write the report

### 3.1 Markdown

Follow `templates/output_template.md` as the skeleton and fill every placeholder. Write it
next to the source as `<name>-style-report.md`, or to the path the user asked for.

Requirements:

- The **scope and reader profile** table comes first, with the audience and purpose chosen
  in phase 1. A reader must be able to audit the findings against the assumptions.
- Every paragraph reviewed gets a block, **including clean ones** — write
  `*No issues found.*` rather than omitting them. Omission makes it look like the paragraph
  was missed.
- Findings sort `[ERROR]`, then `[WARN]`, then `[INFO]`, then by line.
- **Top issues** lists recurring patterns, not one-off slips. Eight agentless passives
  outrank one dangling modifier.
- The overall assessment says what the writing does **well**, not only what is wrong.
- Close with the "Not assessed" section from the template, including the ISO 24495-1 §5.4.3
  point that an automated review does not replace testing with real readers.
- **Never put a language tag on a fenced code block** in the report. A tagged fence makes
  pandoc emit syntax-highlighting macros that the report template does not define, and the
  PDF build fails. Plain ``` fences are safe.
- Quote the author's text inside backticks, never as a `>` blockquote inside a list item.
  Markdown does not nest a blockquote there, and backticks also stop the author's own LaTeX
  macros from being executed during the PDF build.

### 3.2 PDF

```bash
python3 ~/.claude/skills/writing-simple-style/scripts/generate_report_pdf.py <report.md>
```

Run this as the final step unless `--no-pdf` was given. If pandoc or LaTeX is missing, print
the error and tell the user the markdown report is complete and readable on its own. Do not
treat a failed PDF build as a failed review.

### 3.3 Close

Report the counts and the path to both files. Offer, without doing it unprompted, to apply
the rewrites to the source — that is an edit to the user's manuscript and needs their word.

---

# Scope and non-goals

**This skill checks** paragraph structure, sentence structure, word choice, terminology
consistency, and the fit between a section and its declared audience.

**It does not check**, because the `proofreading` skill already does and duplicate findings
make both reports noisy:

| Not here | Where |
| --- | --- |
| Abbreviation introduction, articles, plurals | `proofreading` check 6 |
| Math symbol definition and notation consistency | `proofreading` check 2 |
| Figure and table references, captions | `proofreading` check 4 |
| Tense consistency, en/em-dashes, Oxford commas, compound-adjective hyphenation, British vs American spelling | `proofreading` check 5 |
| Abstract and contribution-list structure, section roadmap | `proofreading` check 1 |
| Statistical reporting | `proofreading` check 3 |

**It also does not check** images, data displays, or table design (ISO 24495-3 §5.3.4–5.3.7),
and it cannot perform the reader testing that ISO 24495-1 §5.4.3 calls for.

# Rules that override the sources

Both sources are applied with deliberate exceptions. They are listed in full in the two
reference files; the ones that matter most:

1. **Passive voice is not a fault.** Only ambiguous attribution is (S3).
2. **Sentence-initial "However," is correct.** Strunk forbids it; modern academic contrast
   structure requires it. Not flagged.
3. **Do not simplify established scientific terminology.** ISO 24495-3 §5.3.3 c) suggests
   everyday alternatives; for a research paper that loses precision. Enforce consistency
   and definition instead (L6).
4. **Do not address the reader as "you".** ISO 24495-1 §5.3.3 b) suggests it; scientific
   writing uses first-person plural.
5. **Short is not the goal.** ISO 24495-1 §5.3.4 c) asks for varied sentence length. Flag
   sentences that carry two ideas, not sentences that are long.
6. **Singular *they* is correct.** Strunk's 1918 entry says otherwise; it is dropped.

# Never do

- Never invent a citation, a number, or a technical claim in a rewrite. If a rewrite needs a
  fact not in the source, say what is missing instead.
- Never rewrite in a register the author does not use. Keep their terminology.
- Never quote from the ISO standards. Cite the clause number; the guidance is paraphrased in
  `~/.claude/skills/writing-simple-style/references/iso-24495-plain-language.md` for this reason.
- Never edit the source document without being asked.
- Never ask the user a question per paragraph.
