# ISO 24495 plain language — guidance used by this skill

## About this file

ISO 24495 is a copyrighted standard. **This file contains no text from the standard.**
It is a paraphrase, written for this skill, of the guidance the checks implement,
with clause numbers so a reader who holds the standard can look each item up.

Two parts are referenced:

| Reference | Title | Role here |
| --- | --- | --- |
| **ISO 24495-1:2023** | Plain language — Part 1: Governing principles and guidelines | Source of nearly all sentence- and paragraph-level guidance (§5.3.2–5.3.5). |
| **ISO 24495-3** | Plain language — Part 3: Science writing | Source of the reader-characterization, document-planning and precise-language guidance. Its §5.3.1 points back to Part 1 for the sentence and paragraph guidance. |

Clause numbers for Part 3 follow ISO/FDIS 24495-3:2026. The published ISO 24495-3:2026
and DIN ISO 24495-3:2025 differ in wording but the clause structure referenced here
is stable.

**Do not obtain, vendor, or commit copies of either standard into this repository.**
Buy them from ISO or a national member body if you want the source text.

---

## The four governing principles (ISO 24495-1, Clause 4)

1. **Relevant** — readers get what they need.
2. **Findable** — readers can easily find what they need.
3. **Understandable** — readers can easily understand what they find.
4. **Usable** — readers can easily use the information.

This skill works on principles 1–3. Principle 4 is about evaluating a document with
real readers (ISO 24495-1 §5.4), which an automated review cannot substitute for.

---

## Principle 1 — Relevant

### Characterize the readers (24495-3 §5.1.2; 24495-1 §5.1.2)

Part 3 stresses that science writing reaches readers of widely varying background,
and that the text should stay as accessible as possible without giving up accuracy
or precision. Knowing the readers determines terminology, organization, what counts
as critical information, and what evidence to supply.

The standard suggests characterizing readers by asking, among other things: are there
distinct reader groups with different backgrounds and purposes; how familiar are they
with domain-specific terminology; do they need the evidence in order to make a decision;
what level of data literacy can be assumed.

**This skill's use:** these questions generate the three audience options offered per
section. The chosen audience then sets the jargon threshold and the definition
requirement for the language checks.

### Identify the genre (24495-3 §5.1.3)

Follow the conventions of the established genre, recognizing that conventions shift
over time. Part 3 lists genres such as research summaries, fact sheets, product
information, science blogs and plain language summaries.

**This skill's use:** a conference paper section, a thesis chapter and a whitepaper
section carry different conventions. The skill asks which, and does not impose
conference-paper conventions on a thesis chapter.

### Identify the purpose (24495-3 §5.1.4)

Identify the document's purpose and express it in a form suited to the readers and
genre — for example answering the readers' questions, advising on action, or helping
them solve a problem. The purpose should be evident in the title and should normally
be stated at or near the start. Fixing the readers and their purpose makes it easier
to find and remove content that is unnecessary, irrelevant, misleading or confusing.

**This skill's use:** the purpose options offered per section, and check A3.

### Plan the document (24495-3 §5.1.5)

The clause lists planning steps. Four matter for reviewing an existing section:

- Establish the primary purpose and the key messages (item a).
- Determine how content is organized so information flows logically (item d).
- **Calibrate the depth of method description to the readers** (item h). The standard
  is explicit that general readers benefit from a brief treatment of method so they
  understand how the evidence was gathered, that specialist readers want the detail so
  they can judge reliability, and that for some readers method detail is overwhelming.
- State the unknowns, uncertainties and limitations, and how much confidence the
  findings support (item j).

**This skill's use:** item h is the mechanism that makes the audience selection
load-bearing for method sections — see check A5.

---

## Principle 2 — Findable

### Structure for the intended readers (24495-3 §5.2.3; 24495-1 §5.2.2)

- Arrange information hierarchically and lead with the most essential material —
  main conclusions, real-world implications, practical applications (item a).
- Provide clear transitions. Signal a shift in topic with transitional phrases and
  sentences so the narrative holds together. The standard notes that transitions can
  signal logic, time, addition, or attitude (item c).

### Provide an overview (24495-3 §5.2.2)

Orient the reader at the start: an informative summary or list of key points for long
or complex documents, and a statement of scope where it helps, including what the
document does *not* cover.

### Headings (24495-1 §5.2.4; 24495-3 §5.2.4 d)

Headings should let readers predict what follows. In long documents the heading
hierarchy must be genuinely hierarchical and visibly so.

**This skill's use:** check A2 tests whether the section's structure is recoverable
from its headings alone.

### Keep supplementary information separate (24495-1 §5.2.5)

Material most readers treat as secondary — detailed derivations, source lists — belongs
in an appendix or equivalent rather than in the main flow.

---

## Principle 3 — Understandable

This is where most of the paragraph-level checks come from. Note that the detailed
guidance lives in **Part 1** §5.3.2–5.3.5; Part 3 §5.3.1 lists these as the general
guidelines to follow and then adds science-specific material in §5.3.2–5.3.7.

### Choose familiar words (24495-1 §5.3.2)

- Choose words that make the text precise and unambiguous (item a).
- Use specialized terms only when readers understand and prefer them, or when readers
  need to learn them to reach their goal — and in that second case, explain every
  specialized term at first appearance (item c).
- Use abbreviations only when readers know the short form better, or when the full form
  is excessively long (item d); spell them out at first appearance unless they are
  common and well understood (item e).
- **Be consistent: the same word for the same meaning, and different words for
  different meanings** (item g).

**Academic adaptation.** Part 3 §5.3.3 c) suggests considering everyday alternatives to
technical terms (its example: "kidney disease" for "nephropathy"). For a research paper
this inverts. A defined scientific term is the precise one, and swapping in a colloquial
synonym loses precision. So this skill does **not** ask authors to simplify established
technical terms. It enforces the other half of the guidance instead — §5.3.2 g)
consistency and §5.3.3 b) definition in context:

- Use the accepted scientific term.
- Define it briefly at first use if the declared audience needs it.
- Then use that same term everywhere for that concept. Synonym drift ("safety shield",
  "safety layer", "protective module" for one thing) is the failure mode to flag.

**Which term is "the accepted" one is answerable, not a matter of taste.** Check L6b puts
candidate terms to the `iso-obp` MCP server, which indexes published terminology from
ISO committee registers and from standards the user has ingested. Where a standard defines
a term, the skill cites the standard and clause, and flags usage that contradicts the
definition. That matters most for safety and robotics vocabulary, where a definition can
carry legal weight.

Two cautions the server's own instructions insist on, carried into L6b:

- Its `not_defined` status means "absent from the corpora indexed here", never "ISO defines
  this nowhere". Novel research terminology lands there routinely and is not a defect.
- Only the status `defined` means a standard defines the term. `defined_by_your_transcription`
  is a hand-entered copy whose wording is unverified, and `defined_by_you_only` is the user's
  private convention, which needs introducing in the text like any other coinage.

### Write clear sentences (24495-1 §5.3.3)

- Use sentence structures familiar to readers; for English the expected pattern is
  subject–verb–object (item a1).
- Avoid structures open to more than one reading (item a2).
- **Do not interrupt the main thought of a sentence with supplementary information**
  (item a3). This is the ISO counterpart of Strunk's Rule 16.
- **Given before new:** open a sentence with information the reader already has, then
  introduce the new information. This is what makes consecutive sentences cohere (item a4).
- Make clear who is doing what; in English this usually means the active voice unless
  there is a specific reason for the passive (item c).
- Item b) advises addressing readers directly with "you". **This skill drops item b):**
  scientific papers use first-person plural ("we"), and ISO 24495-1 notes in the same
  clause that International Standards themselves keep an impersonal tone.

### Write concise sentences (24495-1 §5.3.4)

- One idea per sentence (item a).
- Remove redundant words, vague modifiers, clichés and other constructions that add
  little meaning but cost the reader time and attention (item b).
- Keep sentences reasonably short, but vary the length so the text has rhythm (item c).

**Note the tension with item c.** "Shorter is better" is not the rule. Uniformly short
sentences read as a list. Flag long sentences that carry more than one idea, and flag
monotonous runs, not length alone.

### Write clear and concise paragraphs (24495-1 §5.3.5)

- One topic per paragraph (item a).
- State the topic near the start of the paragraph (item b).
- Make the connections between paragraphs, and within a paragraph, clear (item c).

These coincide with Strunk's Rules 8 and 9. Findings cite both.

### Ensure the document is cohesive (24495-1 §5.3.8)

Relationships among words, sentences, paragraphs, sections and images must all be clear,
with consistent information design and a consistent tone. Readers can understand every
individual element and still fail to understand the whole.

### Indicate the status of information (24495-3 §5.3.2)

Let readers know what kind of claim each statement is: theoretical assumption, hypothesis,
claim, example, method, result, conclusion, limitation, significance, extrapolation,
forecast, or application (item e). Provide citations appropriate to the genre for
quotations, paraphrase, data and borrowed ideas (item c). Describe variables and units
following established conventions such as SI (item g).

**This skill's use:** check A4 — a reader should never be unsure whether a sentence
reports a result, states an assumption, or speculates.

### Use precise language (24495-3 §5.3.3)

The highest-yield clause in the standard for scientific prose. Its items, paraphrased:

| Item | Guidance | Skill check |
| --- | --- | --- |
| a) | Keep language, terminology, tone and expression consistent through the document. A deliberate shift is acceptable for emphasis, for example for urgent information. | L6 |
| b) | Help readers learn important terms and abbreviations by defining them — in context, in a sidebar, or in a glossary. Brief in-context definitions help most. | A5, L6 |
| c) | Consider alternatives to technical terms and jargon. **Inverted for academic writing — see the adaptation note above.** | (adapted) |
| d) | Handle specialized terms and abbreviations per ISO 24495-1 §5.3.2 c) and d). | L6b |
| e) | **Maintain parallel structure** in sentences, paragraphs and headings: align grammatical elements so that similar ideas take similar grammatical form. | S5 |
| f) | **When writing comparisons, present both terms** — state explicitly what is being compared with what. The standard's example is a claim of "significantly lower risk" that never names the comparison group. | L7 |
| g) | **Choose hedges deliberately and quantify them where possible.** Words such as *typically*, *somewhat*, *to some extent*, *roughly comparable*, *can potentially be* signal that an interpretation may change with new data. Where possible, tie the hedge to an observed number or amount. | L8 |
| h) | **Revise noun strings into explanatory phrases.** The standard notes that noun strings make English particularly hard to read. Its examples turn a four- or five-noun pile-up into a phrase with a verb and a preposition. | L5 |

Item h) deserves emphasis for engineering and robotics writing, where noun stacks
accumulate fast: *"safety shield reachability analysis module"* → *"the module that
performs reachability analysis for the safety shield"*.

### Images, tables and data (24495-3 §5.3.4–5.3.7)

Part 3 gives detailed guidance on matching image type to data structure, informative
captions and alternative text, identifying critical data displays, characterizing data
to aid interpretation, and table design. **Out of scope for this skill**, which works on
running prose. The `proofreading` skill's figures-and-tables check covers this ground.

---

## Principle 4 — Usable (24495-1 §5.4; 24495-3 §5.4)

Evaluate the document as it is drafted, then with real readers, then periodically if it
stays in use. ISO 24495-1 §5.4.3 is blunt that the only way to know how readers react is
to involve them.

**Say this in the report.** An automated style review is the §5.4.2 self-evaluation step.
It does not substitute for §5.4.3. The report's closing note should state that.

---

## Checklist mapping (24495-3 Annex B)

Annex B of Part 3 offers a checklist organized by principle, keyed to clauses in both
parts. The questions this skill answers automatically:

| Annex B question (paraphrased) | Skill check |
| --- | --- |
| Have you characterized the readers? | Phase 1 (interactive) |
| Have you identified the genre? | Phase 1 (interactive) |
| Have you identified the purpose? | Phase 1 (interactive) |
| Have you structured the document for readers? | A1, A2, A3 |
| Are you using headings to help readers predict what comes next? | A2 |
| Have you chosen words familiar to readers? | L4, L6 |
| Have you used precise language? | L2, L5, L6, L7, L8 |
| Have you indicated the status of information? | A4 |
| Are your sentences clear and concise? | S1–S9 |
| Are your paragraphs clear and concise? | P1–P5 |
| Is your document as a whole cohesive? | A3, A4, P5 |

Questions Annex B asks that this skill cannot answer — ethical presentation of content,
effective images, critical data displays, table design, usability testing — are listed
in the report as "not assessed" rather than silently skipped.
