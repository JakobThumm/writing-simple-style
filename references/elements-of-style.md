# The Elements of Style — rules used by this skill

Source: William Strunk Jr., *The Elements of Style* (1918/1920). This edition is in
the public domain, so rule text and Strunk's own before/after examples are quoted
directly below.

This file covers only the rules this skill checks. Rules on punctuation mechanics
(1–5), form (Chapter IV) and spelling (Chapter VI) are out of scope; see
`SKILL.md` § Scope and non-goals.

Each rule below carries an **Academic adaptation** note where Strunk's 1918 advice
has to bend for a modern scientific paper. Where the adaptation contradicts Strunk,
follow the adaptation — and say so in the finding, so the author sees the reasoning
rather than a bare rule number.

---

## Paragraph structure

### Rule 8 — Make the paragraph the unit of composition: one paragraph to each topic

> "Ordinarily [...] a subject requires subdivision into topics, each of which should
> be made the subject of a paragraph. The object of treating each topic in a paragraph
> by itself is, of course, to aid the reader. The beginning of each paragraph is a
> signal to him that a new step in the development of the subject has been reached."

> "As a rule, single sentences should not be written or printed as paragraphs. An
> exception may be made of sentences of transition, indicating the relation between
> the parts of an exposition or argument."

**How to test it.** Try to state the paragraph's topic in a single clause. If that
clause needs an "and" joining two unrelated claims, the paragraph holds two topics
and should be split at the sentence where the second topic starts.

**Academic adaptation.** In a method section, one topic often means one component,
one equation group, or one algorithmic step. A paragraph that defines a component
*and* evaluates it holds two topics.

### Rule 9 — Begin each paragraph with a topic sentence, end it in conformity with the beginning

> "the most generally useful kind of paragraph, particularly in exposition and
> argument, is that in which
> (a) the topic sentence comes at or near the beginning;
> (b) the succeeding sentences explain or establish or develop the statement made in
> the topic sentence; and
> (c) the final sentence either emphasizes the thought of the topic sentence or states
> some important consequence."

> "Ending with a digression, or with an unimportant detail, is particularly to be avoided."

Strunk allows a transition to precede the topic sentence:

> "Sometimes [...] it is expedient to precede the topic sentence by one or more
> sentences of introduction or transition. If more than one such sentence is required,
> it is generally better to set apart the transitional sentences as a separate paragraph."

**How to test it.** Read sentence 1 and the last sentence alone. If a reader cannot
tell they belong to the same paragraph, one of the two is wrong. Usually the last
sentence has drifted.

---

## Sentence structure

### Rule 6 — Do not break sentences in two

> "In other words, do not use periods for commas."

> "I met them on a Cunard liner several years ago. Coming home from Liverpool to New York."
> "He was an interesting talker. A man who had traveled all over the world and lived in
> half a dozen countries."

> "In both these examples, the first period should be replaced by a comma, and the
> following word begun with a small letter."

Strunk permits the deliberate fragment, with a warning:

> "It is permissible to make an emphatic word or expression serve the purpose of a
> sentence [...] The writer must, however, be certain that the emphasis is warranted,
> and that he will not be suspected of a mere blunder in syntax or in punctuation."

**Academic adaptation.** Deliberate fragments are rare in scientific prose. Flag every
fragment with `‹struct›`, and say which kind it is: a dropped comma, or emphasis that a
reader will mistake for one.

### Rule 7 — A participial phrase at the beginning of a sentence must refer to the grammatical subject

> "Walking slowly down the road, he saw a woman accompanied by two children."

> "The word *walking* refers to the subject of the sentence, not to the woman."

The rule extends beyond participles:

> "Participial phrases preceded by a conjunction or by a preposition, nouns in
> apposition, adjectives, and adjective phrases come under the same rule if they begin
> the sentence."

| Wrong | Right |
| --- | --- |
| On arriving in Chicago, his friends met him at the station. | When he arrived in Chicago, his friends met him at the station. |
| Young and inexperienced, the task seemed easy to me. | Young and inexperienced, I thought the task easy. |
| Being in a dilapidated condition, I was able to buy the house very cheap. | *(recast entirely)* |

**Academic adaptation.** The common scientific form is "Using X, the result is Y" —
the result did not use X. Prefer "Using X, we obtain Y."

### Rule 10 — Use the active voice

> "The active voice is usually more direct and vigorous than the passive."

> "This rule does not, of course, mean that the writer should entirely discard the
> passive voice, which is frequently convenient and sometimes necessary."

Strunk's own criterion is *which noun deserves to be the subject*:

> "The dramatists of the Restoration are little esteemed to-day." /
> "Modern readers have little esteem for the dramatists of the Restoration."
> "The first would be the right form in a paragraph on the dramatists of the
> Restoration; the second, in a paragraph on the tastes of modern readers."

He also flags the nominalized passive:

| Wrong | Right |
| --- | --- |
| A survey of this region was made in 1900. | This region was surveyed in 1900. |
| Mobilization of the army was rapidly effected. | The army was rapidly mobilized. |
| Confirmation of these reports cannot be obtained. | These reports cannot be confirmed. |
| There were a great number of dead leaves lying on the ground. | Dead leaves covered the ground. |

**Academic adaptation — this is the important one.** Do not flag passive voice as such.
Flag passive voice that leaves *attribution* ambiguous: the reader cannot tell whether
the authors did this, prior work did this, or the system does it on its own.

- Ambiguous, flag it: "A Kalman filter is used to fuse the measurements." Did we choose
  it, or is it standard practice?
- Clear, leave it: "In this work, the notation $X$ is always used to refer to $Y$."
  Authorship is fixed by "In this work".
- Clear, leave it: "The joint torque is limited to 40 N m." This is a property of the
  system, not anyone's contribution.

### Rule 14 — Avoid a succession of loose sentences

> "This rule refers especially to loose sentences of a particular type, those consisting
> of two co-ordinate clauses, the second introduced by a conjunction or relative.
> Although single sentences of this type may be unexceptionable [...] a series soon
> becomes monotonous and tedious."

> "An unskilful writer will sometimes construct a whole paragraph of sentences of this
> kind, using as connectives *and*, *but*, *so*, and less frequently, *who*, *which*,
> *when*, *where*, and *while*."

> "he should recast enough of them to remove the monotony, replacing them by simple
> sentences, by sentences of two clauses joined by a semicolon, by periodic sentences
> of two clauses, by sentences, loose or periodic, of three clauses — whichever best
> represent the real relations of the thought."

**How to test it.** Three or more consecutive sentences of the shape
`[clause], and/but/which [clause]` in one paragraph.

### Rule 15 — Express co-ordinate ideas in similar form

> "This principle, that of parallel construction, requires that expressions of similar
> content and function should be outwardly similar. The likeness of form enables the
> reader to recognize more readily the likeness of content and function."

> "an article or a preposition applying to all the members of a series must either be
> used only before the first term or else be repeated before each term."

> "Correlative expressions (*both, and*; *not, but*; *not only, but also*; *either, or*;
> *first, second, third*) should be followed by the same grammatical construction."

| Wrong | Right |
| --- | --- |
| It was both a long ceremony and very tedious. | The ceremony was both long and tedious. |
| A time not for words, but action. | A time not for words, but for action. |
| Either you must grant his request or incur his ill will. | You must either grant his request or incur his ill will. |
| Formerly, science was taught by the textbook method, while now the laboratory method is employed. | Formerly, science was taught by the textbook method; now it is taught by the laboratory method. |

**Academic adaptation.** Highest yield in contribution lists, hypothesis lists (H1/H2/H3),
and itemized algorithm steps. Every item in a list should open with the same part of speech.

### Rule 16 — Keep related words together

> "The position of the words in a sentence is the principal means of showing their
> relationship. The writer must therefore, so far as possible, bring together the words,
> and groups of words, that are related in thought, and keep apart those which are not
> so related."

> "The subject of a sentence and the principal verb should not, as a rule, be separated
> by a phrase or clause that can be transferred to the beginning."

| Wrong | Right |
| --- | --- |
| Wordsworth, in the fifth book of The Excursion, gives a minute description of this church. | In the fifth book of The Excursion, Wordsworth gives a minute description of this church. |
| Cast iron, when treated in a Bessemer converter, is changed into steel. | By treatment in a Bessemer converter, cast iron is changed into steel. |
| All the members were not present. | Not all the members were present. |
| He only found two mistakes. | He found only two mistakes. |

> "The relative pronoun should come, as a rule, immediately after its antecedent."

> "Modifiers should come, if possible, next to the word they modify."

**Academic adaptation.** The frequent offender is a long citation block or parenthetical
splitting subject from verb: "Reinforcement learning (which has been applied to
manipulation [3], locomotion [7] and navigation [12]) suffers from sample inefficiency."

### Rule 18 — Place the emphatic words of a sentence at the end

> "The proper place in the sentence for the word, or group of words, which the writer
> desires to make most prominent is usually the end."

| Weaker | Stronger |
| --- | --- |
| Humanity has hardly advanced in fortitude since that time, though it has advanced in many other ways. | Humanity, since that time, has advanced in many other ways, but it has hardly advanced in fortitude. |
| This steel is principally used for making razors, because of its hardness. | Because of its hardness, this steel is principally used in making razors. |

> "The word or group of words entitled to this position of prominence is usually the
> logical predicate, that is, the new element in the sentence."

> "The principle that the proper place for what is to be made most prominent is the end
> applies equally to the words of a sentence, to the sentences of a paragraph, and to the
> paragraphs of a composition."

**Academic adaptation.** A result sentence that ends in a citation, a hedge, or a setup
detail buries its own finding: "Our method reduces the collision rate by 30 %, as shown
in Table 2." → "As shown in Table 2, our method reduces the collision rate by 30 %."

---

## Language

### Rule 11 — Put statements in positive form

> "Make definite assertions. Avoid tame, colorless, hesitating, non-committal language.
> Use the word *not* as a means of denial or in antithesis, never as a means of evasion."

| Evasive | Definite |
| --- | --- |
| not honest | dishonest |
| not important | trifling |
| did not remember | forgot |
| did not pay any attention to | ignored |
| did not have much confidence in | distrusted |
| He was not very often on time. | He usually came late. |

> "Consciously or unconsciously, the reader is dissatisfied with being told only what is
> not; he wishes to be told what is."

Strunk explicitly allows the deliberate antithesis:

> "The antithesis of negative and positive is strong: Not charity, but simple justice."

### Rule 12 — Use definite, specific, concrete language

> "Prefer the specific to the general, the definite to the vague, the concrete to the abstract."

| Vague | Specific |
| --- | --- |
| A period of unfavorable weather set in. | It rained every day for a week. |
| He showed satisfaction as he took possession of his well-earned reward. | He grinned as he pocketed the coin. |
| There is a general agreement among those who have enjoyed the experience that surf-riding is productive of great exhilaration. | All who have tried surf-riding agree that it is most exhilarating. |

**Academic adaptation.** Vagueness in a paper is usually an unquantified claim
("substantially faster", "a large dataset", "good performance") or an unnamed mechanism
("a suitable technique is applied"). Name the number or name the mechanism.

### Rule 13 — Omit needless words

> "Vigorous writing is concise. A sentence should contain no unnecessary words, a
> paragraph no unnecessary sentences, for the same reason that a drawing should have no
> unnecessary lines and a machine no unnecessary parts. This requires not that the writer
> make all his sentences short, or that he avoid all detail and treat his subjects only
> in outline, but that he make every word tell."

| Wordy | Concise |
| --- | --- |
| the question as to whether | whether |
| there is no doubt but that | no doubt |
| used for fuel purposes | used for fuel |
| he is a man who | he |
| in a hasty manner | hastily |
| this is a subject which | this subject |
| His story is a strange one. | His story is strange. |
| owing to the fact that | since, because |
| in spite of the fact that | though, although |
| I was unaware of the fact that | I did not know that |
| the fact that he had not succeeded | his failure |
| His brother, who is a member of the same firm | His brother, a member of the same firm |

> "In especial the expression *the fact that* should be revised out of every sentence in
> which it occurs."

> "*Who is*, *which was*, and the like are often superfluous."

> "A common violation of conciseness is the presentation of a single complex idea, step
> by step, in a series of sentences or independent clauses which might to advantage be
> combined into one."

Strunk quantifies the gain (51 words → 26 words; 43 words → 21 words). **Report a word
count for every conciseness finding**; it is the most persuasive part of the feedback.

### Chapter V — Words and expressions commonly misused

Strunk's own framing of what this list is for:

> "If the writer will make it his purpose from the beginning to express accurately his
> own individual thought, and will refuse to be satisfied with a ready-made formula that
> saves him the trouble of doing so, this last set of expressions will cause him little
> trouble. But if he finds that in a moment of inadvertence he has used one of them, his
> proper course will probably be not to patch up the sentence by substituting one word
> or set of words for another, but to recast it completely."

Entries below are the subset that still applies to scientific writing. The emphasis column
is the skill's, not Strunk's: **flag** means report it, **note** means mention it only at
full depth, **off** means never report it. Findings from this table carry the `‹word›` tag.

| Entry | Rule | Emphasis |
| --- | --- | --- |
| **as good or better than** | Rearrange: "as good as his, or better". | flag |
| **as to whether** | *Whether* alone suffices (Rule 13). | flag |
| **but** after *doubt* / *help* | "no doubt but that" → "no doubt that"; "could not help see but that" → "could not help seeing that". | flag |
| **can** | Means *am/is/are able*. Not a substitute for *may* (permission or possibility). | note |
| **case** | "In many cases, the rooms were poorly ventilated" → "Many of the rooms were poorly ventilated." Usually deletable. | flag |
| **certainly** | An indiscriminate intensifier, like *very*. | flag |
| **claim** (vb.) | Means *lay claim to*. Not a substitute for *declare*, *maintain*, *argue*, *report*. | flag |
| **compare** | *compare to* = point out resemblance between different orders of thing; *compare with* = point out differences within the same order. Benchmarks are compared **with** baselines. | flag |
| **consider** | No *as* when it means "believe to be": "We consider this approach sound", not "consider it as sound". | note |
| **data** | A plural, like *phenomena* and *strata*: "These data were tabulated." | note |
| **dependable** | A needless substitute for *reliable*, *trustworthy*. | note |
| **different than** | Use *different from*, *other than*, or *unlike*. | flag |
| **divided into** | Not to be misused for *composed of*. A dataset is composed of samples; it is divided into folds. | note |
| **due to** | Correct as a predicate adjective tied to a noun ("losses due to fires"); incorrect as an adverbial ("It failed, due to noise" → "because of noise"). | flag |
| **effect** | Noun = *result*; verb = *to bring about*. Do not confuse with *affect*. Avoid the vague noun use ("a smoothing effect"). | flag |
| **fact** | Only for matters capable of direct verification, not matters of judgement. And see *the fact that* under Rule 13. | flag |
| **factor** | Hackneyed: "His superior training was the great factor in his winning" → "He won by being better trained." | flag |
| **feature** | Hackneyed, adds nothing. **Exception: in machine learning, *feature* is a defined technical term — do not flag that sense.** | note |
| **however** | Strunk: in the sense *nevertheless*, not first in its sentence. **Suppressed by default in this skill** — see the note below. | off |
| **interesting** | "Do not announce that what you are about to tell is interesting; make it so." | flag |
| **kind of** / **sort of** | Not a substitute for *rather* or *something like*. Literal sense only. | flag |
| **less** | *Less* for quantity, *fewer* for number: "fewer samples", not "less samples". | flag |
| **like** | Governs nouns and pronouns; before phrases and clauses use *as*. | flag |
| **most** | Not a substitute for *almost*. | flag |
| **oftentimes** | Archaic. Use *often*. | flag |
| **one of the most** | "Threadbare and forcible-feeble" as an opener. Also: the relative clause takes a plural verb — "one of the ablest men that **have** attacked this problem". | flag |
| **people** | A political term; not interchangeable with *the public*, and in a paper rarely the right word for *participants*, *users*, or *subjects*. | note |
| **phase** | A stage of transition or development. Not a substitute for *aspect* or *topic*. | note |
| **possess** | Not a substitute for *have* or *own*: "He possessed great courage" → "He had great courage". | flag |
| **should / would** | First-person conditional takes *should*, not *would*. Habitual past needs no *would*. | note |
| **so** | Not as an intensifier ("so good", "so efficient"). | flag |
| **state** | Not a substitute for *say* or *remark*; restrict to *express fully or clearly*. **Exception: *state* as the technical noun (system state $x$) is not this entry.** | note |
| **very** | "Use this word sparingly. Where emphasis is necessary, use words strong in themselves." | flag |
| **viewpoint** | Write *point of view*, and do not misuse it for *view* or *opinion*. | note |
| **whom** | Often wrongly used for *who* before "he said": "his brother, who he said would send the money". | note |
| **respective / respectively** | "may usually be omitted with advantage". Keep only where the pairing is genuinely needed. | note |
| **while** | Avoid as a loose substitute for *and* or *but*; best replaced by a semicolon. Acceptable for *although* where no ambiguity arises. Strictly, *during the time that*. | flag |
| **literal / literally** | Not for emphasis of a metaphor. | flag |
| **character / nature** (as in "acts of a hostile character") | Redundant padding: "hostile acts". | flag |
| **system** | "Frequently used without need": "the dormitory system" → "dormitories". | note |
| **worth while** | Vague approval; and never before a noun. | note |

#### Strunk entries this skill deliberately drops

Dropped because they are obsolete, prescriptivist in a way modern venues reject, or in
direct conflict with the conventions of the author's own style guide:

| Entry | Why dropped |
| --- | --- |
| **however** (not sentence-initial) | Sentence-initial "However," is the standard contrast marker in related-work and gap statements, and is explicitly prescribed by many house styles. Keep it available; do not flag it. |
| **they** (Strunk: "Use *he* with all the above words") | 1918 advice that misgenders people. Singular *they* is correct and preferred. |
| **shall / will** | The shall/will distinction is dead in modern scientific English. |
| **split infinitive** | No longer in disfavour. |
| **student body**, **thanking you in advance**, **fix**, **get**, **folk**, **lose out**, **near by**, **don't**, **bid**, **prove**, **clever**, **all right**, **etc.**, **one hundred and one** | Register or idiom notes with no bearing on scientific prose. |
| **line / along these lines** | Rare in scientific writing; low yield. |
