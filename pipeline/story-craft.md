# Story Craft Guide

## Purpose

Turn a topic, idea, or real experience into narration that works as a story,
not as a disconnected list of facts.

This guide defines the **creative and narrative method**: how to find the
story, shape its structure, write engaging narration, and evaluate the
result. It does not define agent roles, file permissions, research, approval
gates, assets, audio, timelines, or rendering. Those belong to the pipeline
instructions and templates.

## 1. How to use this guide

### Standalone writing

When writing directly from a user's idea or experience:

- Collect the information described in Step 2.
- Use the output format in Step 14 unless the user requests another format.
- Ask for essential missing information when it is possible to ask.
- If the user cannot answer, make only safe, clearly stated assumptions.

### YouTube-Kit pipeline

When this guide is used by `pipeline/2-script-writer.md`:

- Follow the Script Writer's input, output, file, research, fact-tagging,
  fix-round, and approval instructions.
- Skip Step 2: the brief and research files already supply the assignment.
- Use Step 8 when the assignment is a researched history or explainer.
- Use `templates/script.md` for the output layout, not Step 14.
- Follow `2-script-writer.md` for the `[visual: ...]` syntax and placement.
  These notes are production markers used by later steps (Step 11).
- If this guide conflicts with `AGENTS.md`, the pipeline step, or its
  template, follow the pipeline.

## 2. Collect inputs (standalone writing only)

Before writing, identify the following. If essential information is
missing, ask once in a short, focused set of questions.

- **Topic or raw idea:** What is the story about?
- **Truth status:** The user's experience, a documented real event, a
  researched subject, or fiction?
- **Format and length:** Reel/Short, long-form YouTube, voiceover, or
  another format; a target duration when known.
- **Language:** Nepali (Devanagari), English, or mixed. Default to the
  language of the request.
- **Audience:** Who is expected to watch?
- **Tone:** Emotional, funny, inspiring, suspenseful, calm, investigative,
  explanatory, or another fitting tone.
- **Goal:** What should the viewer feel, understand, consider, or do?

Do not ask for details already supplied. Do not delay a task over
information that is not needed to write responsibly.

## 3. Truth, evidence, and imagination

These rules apply to every section of this guide. Later sections do not
repeat them.

### True personal stories and real events

- Use only facts supplied by the user or supported by the approved source
  material for the task.
- Do not invent events, actions, dialogue, quotations, dates, numbers,
  people, motives, feelings, sensory details, or causal links.
- Do not use a plausible detail as though it were a known detail.
- If a needed detail is missing, ask for it when the workflow allows. If
  not, leave it out, write around it, or record it as a research request
  according to the pipeline instructions.
- "Show, don't tell" never permits made-up behavior or sensory detail in a
  true story.
- Attribute a quotation to a real person only when the exact words are in
  the supplied material.

### Researched history and explainers

- The research file and its source-backed claims are the factual boundary
  of the script.
- Do not turn uncertainty, disagreement, or a research gap into certainty
  for a smoother story.
- Distinguish what is documented from what is inferred, debated,
  approximate, or unknown.
- Do not invent a person's private thoughts, feelings, intentions,
  conversations, or undocumented actions.
- A causal sequence must be supported. Do not imply that one event caused
  another because the sequence makes a more satisfying story.
- Follow the pipeline's fact-ID, quote-ID, conflict-ID, confidence, and
  research-request rules. This guide does not replace them.

### Fiction

- Identify the work as fiction when it could otherwise be misunderstood.
- Fiction may invent events, dialogue, characters, and sensory details, as
  long as they are not presented as real events or real quotations.
- Do not disguise a real person's invented words or actions as fact.

### Labelled hypothetical moments

A hypothetical example can help a viewer understand a situation or
mechanism. Make its status clear in the narration: "Picture this",
"Imagine a situation where...".

A labelled hypothetical is not permission to reconstruct undocumented
history. Do not place invented words, feelings, decisions, or actions into
a real person's life. Keep the line between documented fact and
illustration unmistakable.

### Facts that need verification

Do not state uncertain facts as established. In standalone writing, flag
them for verification. In YouTube-Kit, do not use them: follow the research
and fact-check workflow, and never use material marked unverified or as a
gap.

## 4. Choose the story mode before the structure

Do not force every topic into the same dramatic pattern. First decide what
kind of story the material can honestly support:

1. **Personal or character-led story:** A person wants something, meets
   obstacles, makes decisions, and changes.
2. **Historical story:** A real person, object, invention, event, or
   question carries the through-line across time.
3. **Mechanism explainer:** A question leads the viewer through a process,
   system, or object so they understand how it works and why it matters.
4. **Fictional story:** An invented character and situation develop through
   conflict and change.

A topic can combine modes, but choose one primary mode so the script has
one organizing principle.

## 5. Build the story core

Write the story core before drafting the narration. Use the fields that fit
the chosen mode. Do not invent a protagonist, measurable goal, villain,
single turning point, or emotional change just to fill a field.

### Core fields

1. **Protagonist or subject:** The person, group, object, system, process,
   or central question the viewer follows.
2. **Want, purpose, or central question:** What the person is trying to
   achieve; what the object was designed to do; what the system is meant to
   do; or what the viewer wants answered.
3. **Obstacle or difficulty:** What blocks progress, complicates the
   question, or limits the mechanism. Use only obstacles the material
   supports. When the material allows, order them from small to big.
4. **Stakes or significance:** What is at risk, what changes, or why the
   answer matters. Avoid inflated stakes.
5. **Change or answer:** What is different by the end, or what the viewer
   now understands.
6. **Cause or path to change:** The documented event, decision, discovery,
   mechanism, or sequence that explains the change. A gradual build-up of
   causes is valid; one dramatic moment is not required.
7. **Theme or deeper question:** The larger human, social, practical, or
   conceptual question. Phrase it as a question when useful, not as a moral.
8. **Want versus need (optional):** For a character-led story, the external
   goal versus the deeper need, only when the material supports it.

### Mode-specific guidance

- **Personal or character-led:** A clear want, credible obstacles, real
  stakes, and a change supported by the person's actual experience.
- **Historical:** A documented person, object, event, or question as the
  through-line. For an object, describe its intended purpose and historical
  role rather than pretending it literally wanted something.
- **Mechanism explainer:** The central question, the problem or function,
  the parts or stages needed, the causal links between them, and the
  consequence. The mechanism itself can carry the progression; a villain or
  emotional arc is not required.
- **Fiction:** Want, opposition, stakes, choice, and change, with enough
  cause and effect that the ending feels earned.

If the story core is vague, narrow the subject or question. If the evidence
cannot support a dramatic arc, use a clearer explanatory structure.

## 6. Build a story spine

Use a compact spine to test whether the sequence makes sense:

```text
At first...
Usually...
Then...
But...
So...
As a result...
Finally...
```

Each "but" introduces a real complication. Each "so" is a consequence of
what came before. Do not use them as decoration, and do not force a simple
chain where the evidence shows several causes or parallel developments.

For a character-led story, compare the opening state with the ending
state: they should make a real change visible.

For a mechanism explainer, the spine can follow:

```text
The viewer's question...
The problem or purpose...
The first important part or step...
What that causes...
The hidden or surprising connection...
The complete explanation...
Why it matters...
```

## 7. Design the hook

Write **three distinct hook options** with different approaches, then pick
the strongest and say why in one line.

- **Unexpected fact:** A verified detail that changes the viewer's
  expectation.
- **Middle of the action:** A documented moment of tension or consequence.
- **Stakes up front:** What could be lost, changed, or misunderstood.
- **Contradiction:** Two supported facts or expectations in tension.
- **Unanswered question:** The central question the video will answer.
- **Unexpected consequence:** A surprising outcome, then how it happened.
- **Familiar object, unfamiliar story:** Something the viewer knows, and the
  hidden history or mechanism behind it.

In YouTube-Kit, the 21 formulas in `tools/yt-script/hooks.json` and the 6
Kallaway formulas in `tools/hooks-kallaway.json` (shape,
example, and when each one fails) are further starting points. A formula is
a tool, not a mould: use it only when it fits the subject and its
"fails_when" condition does not apply.

### What a hook must do

In roughly the first 15 seconds, a hook does three jobs:

1. **Confirm the promise of the title** in the first sentence.
2. **Open a question** the viewer cannot close yet.
3. **Show that the payoff exists**: what the viewer will get by staying.

A hook that only does the third is a summary. One promise per hook: a hook
carrying two promises keeps neither. Specific beats big: a named thing, a
date, or a number from the facts beats "huge" or "incredible".

### Hook rules

- No greeting or channel introduction before the hook.
- Start as late as the material allows. Skip background the viewer does not
  need yet.
- Create curiosity, tension, or a clear expectation. It need not be a
  literal question.
- Make a promise the rest of the video keeps.
- Keep the hook proportional to the evidence: no exaggerated claim,
  manufactured danger, or mystery the research cannot resolve.
- For researched topics, the hook's factual basis must be in the facts.
- Do not reveal the full answer at once when the video builds toward it. Do
  not delay a simple answer so long that the viewer gets frustrated.

### The opening turn

Right after the hook, say in one sentence what the video will do, and start
doing it. No "before we get started", no channel pitch, no subscribe
request: they are the most common reason viewers leave in the first
minute.

## 8. Story-driven explainers

For researched videos about history, inventions, objects, systems, and how
things work. The goal is to explain a real subject through a coherent
narrative, not to force a fictional drama onto it.

### 8.1 Historical explainer

Choose one primary through-line:

- **One person:** Their documented goal, obstacles, decisions, and outcome.
  Others appear when they affect that path.
- **One object or invention:** Its purpose, development, limits, adoption,
  competition, and impact. Its "want" is a metaphor for its function.
- **One question:** Open with a question the viewer wants answered, reveal
  the answer step by step, and complete it at the end.
- **One event or change:** The documented sequence that explains how a
  consequential change happened.

Do not include every person, date, or side story. Keep only details that
advance the through-line or are needed to understand the subject.

### 8.2 Mechanism explainer

For questions such as "How does a computer mouse work?" or "Why does a
bridge stay up?". Build the explanation around a question and a causal
chain:

1. **The viewer's question:** What the viewer wants to understand.
2. **The purpose or problem:** What the system does or what it solves.
3. **The essential parts:** Only the components needed for the explanation.
4. **The process:** What happens, in what order, and why each stage follows
   from the last.
5. **The key insight:** The connection, principle, or non-obvious detail
   that makes it click.
6. **The consequence:** What the mechanism enables, changes, or limits.

Rules:

- Do not force a protagonist, antagonist, rescue, or turning point onto a
  mechanism that has none.
- Explain parts when the viewer needs them, not as a list of definitions.
- Use an analogy only when it clarifies the real mechanism, and say where it
  stops being accurate. It never replaces the actual explanation.
- Say when an explanation is simplified and important details are left out.
- Keep needed technical terms, and explain them plainly at first use.

### 8.3 Keep explanation inside the story

- Introduce information when the viewer needs it for the next development.
- Aim for one main new idea per chapter or section, and one idea per beat
  inside it.
- Explain the idea plainly, then give the viewer a concrete way to grasp it.
- Use a common misconception as a turn only when it is genuinely common and
  the correction is supported: "Most people think X. But..."
- End each section with a reason to continue: an open consequence, a new
  obstacle, a deeper question, or the next link in the mechanism.
- The narrator may react, wonder, and ask ("This is the part that surprised
  me."). Do not transfer that reaction to a historical person or present it
  as evidence.
- Address the viewer as "you" when it makes the explanation more immediate
  ("the banana in your kitchen"), not in every paragraph.

### 8.4 Scenes the sources do not describe

Section 3 applies: no reconstruction written as if documented. A clearly
labelled conceptual image may explain context, and its visual must not look
like authentic archival material.

## 9. Structure by format and length

Flexible guides, not formulas. The evidence and purpose decide the final
structure.

### 30-60 second short

- **Opening:** Hook immediately.
- **Middle:** One clear attempt, explanation, contrast, or escalation.
- **Turn:** One meaningful reveal or consequence.
- **Ending:** Deliver the promised answer, result, or change.

One central idea, one main question, and only the context needed. Do not
cram a long-form story into a short runtime.

### 2-5 minute story or voiceover

- **Beginning:** Hook, subject, central want or question, needed context.
- **Middle:** A few meaningful obstacles, discoveries, or explanatory steps.
- **Turn:** A significant change in understanding, situation, or direction,
  if the material supports one.
- **End:** Resolve the central question and show the consequence or change.

### 5+ minute long-form

A five-part progression can help:

1. **Home:** The initial situation, familiar assumption, or central question.
2. **Into the unknown:** Attempts, investigation, development, or
   explanation begin.
3. **Deep in the problem:** The largest complication, limit, or insight.
4. **The way through:** How the problem is addressed, or how the evidence
   changes the viewer's understanding.
5. **Return changed:** Resolve the opening question and connect the answer
   to its broader significance.

A mechanism explainer may use a sequence of causal stages instead of a
dramatic "darkest point".

### Chapters in long-form

When the brief calls for chapters, give each one a clear purpose or small
question, what is needed to advance it, a real change in the viewer's
understanding or the situation, and a transition that gives a reason to
continue. Avoid chapters that only divide the runtime.

### Story shape

Optionally describe the shape in one line (Kurt Vonnegut style), for
example "good -> bad -> better". If the shape is flat, add a fall or a rise
that the material supports.

### Timing and word count

Speaking rates are estimates. English narration is often around 2-2.5 words
per second; delivery varies by narrator, subject, sentence complexity,
pauses, and language. Time Nepali by reading the script aloud. Always label
duration estimates as estimates, and follow the pipeline's own length
guidance when it has one.

## 10. Write the narration

Apply these craft principles where they serve clarity, truth (section 3),
and the story.

### Show, don't tell

- Prefer concrete, observable details over vague emotion words when those
  details are known.
- If the evidence gives no vivid detail, use a clear explanation instead.
  Do not invent one to make the writing cinematic.
- Tell directly when a time jump or unimportant stretch should be
  compressed ("Three months went by like this.").

### Be specific

- Prefer meaningful specifics over generic language.
- Use local details when they are accurate, relevant, and understandable to
  the audience. Do not add a place, object, brand, date, or cultural detail
  just to make a scene feel authentic.
- Explain unfamiliar local references through context for an international
  audience.

### Build scenes and explanatory beats

Each scene or beat does at least one job: raise a question, set context,
show an attempt, reveal an obstacle, explain a mechanism, give evidence,
change the viewer's understanding, or deliver a consequence. In a mechanism
explainer, a clear demonstration can be the change. Cut repetition and
anything that does not advance the story or the understanding.

### Manage pacing

- Slow down around an important decision, discovery, reveal, or hard idea.
- Use short sentences selectively for urgency or emphasis.
- Use longer sentences when the viewer needs a connected explanation.
- Move quickly through routine context.
- Do not manufacture suspense by withholding what the viewer needs to
  follow the explanation.

### Sentence rhythm and spoken language

- Write for the ear. Prefer clear, natural sentences that read aloud easily.
- Vary sentence length without making every line sound like a trailer.
- Avoid repeated rhetorical questions, exaggerated claims, filler phrases,
  and generic motivational language.

### Dialogue and quotations

- Keep quotes word for word when the workflow requires it.
- Do not create dialogue to show what a person "must have been thinking".
- **Narration-only videos:** the narrator reads every quote, so say who said
  it and where, before or after it ("he later wrote: ..."). Keep each quote
  short, and let the narrator react to it rather than act it out.
- In fiction, invented dialogue should reveal character, advance the
  situation, or change a relationship.

### Subtext and recurring motifs

A recurring object, phrase, image, or idea can unify the story when the
subject supports it, and its meaning may shift by the end. Do not force a
motif into a factual explainer when it distracts from understanding.

### Narration delivery marks

Use short delivery marks only when they help the narrator, such as
`[pause]` before a line that needs space. Present tense at the climax can
work when it suits the tone. Do not overload the script with acting
directions. In YouTube-Kit, follow the voiceover step's markup rules.

### No preaching

Do not end with a generic lesson ("so we should always...") unless the
format calls for direct advice. Let the evidence, consequence, or actual
change carry the meaning.

### Earned endings

The ending keeps the opening promise. Show the change through supported
action, consequence, or understanding.

## 11. Visual notes

- **Standalone writing:** visual notes are optional suggestions. Say that
  they are suggestions, not evidence or production instructions.
- **YouTube-Kit:** `[visual: ...]` is a production marker that the asset and
  timing steps parse. Its syntax, placement and spacing rules live in
  `2-script-writer.md` only; follow them exactly.
- **Visual truth (both):** Distinguish archival material, real photos,
  diagrams, conceptual illustrations, and labelled recreations. Do not imply
  that a generated image shows a real undocumented moment, or add
  identifying details (logos, uniforms, dates, people) the sources do not
  support.

## 12. Endings

Choose the ending that best keeps the story's promise:

- **Emotional resolution:** A supported human consequence or change.
- **Answer or reveal:** Complete the central question.
- **Loop back:** Return to an image, question, or idea from the opening with
  a changed meaning.
- **Practical consequence:** What the mechanism, discovery, or history means
  in the viewer's world.
- **Viewer question:** Invite the viewer's view when discussion is
  genuinely relevant.

**The payoff.** Whatever the ending type, deliver the hook's promise
explicitly, so the viewer knows they got it. A summary of the chapters is
not a payoff. If the answer is genuinely unknown, say so plainly; that is a
payoff too.

**The closing ask.** At most one, and only if it serves the goal in the
brief (for example, "watch the full video" for a trailer Short). It comes
after the payoff and must not weaken it. Avoid an unrelated moral, a
generic call to subscribe, or a second ending after the story has
concluded.

## 13. Self-check before delivery

Check the script against the rows that apply to its mode. Revise weak areas
before delivery. Do not mark an item as passed only because it was
attempted.

### Core checks

| Check | Result |
|---|---|
| The opening creates curiosity, tension, or a clear expectation without an unnecessary introduction. | Pass / Weak / Fail |
| The central subject, want, purpose, or question is clear early. | Pass / Weak / Fail |
| The stakes or significance are understandable and proportional. | Pass / Weak / Fail |
| The sequence is coherent, and cause-and-effect links are supported. | Pass / Weak / Fail |
| Obstacles, discoveries, or stages advance the story and grow in size where the material allows. | Pass / Weak / Fail |
| The ending keeps the opening promise. | Pass / Weak / Fail |
| Important emotions are shown through supported details, not invented behavior. | Pass / Weak / Fail |
| Specific details are accurate and relevant to the audience. | Pass / Weak / Fail |
| Each scene or beat advances the story or the viewer's understanding. | Pass / Weak / Fail |
| The ending avoids an unearned moral or a repeated summary. | Pass / Weak / Fail |
| The script fits the target length; the duration is labelled as an estimate. | Pass / Weak / Fail |
| The truth status is clear, and no fiction is presented as fact. | Pass / Weak / Fail |

### Personal or character-led stories

| Check | Result |
|---|---|
| The main character's goal and obstacles come from the supplied facts. | Pass / Weak / Fail |
| The change has a credible cause or causal sequence. | Pass / Weak / Fail |
| Dialogue, feelings, actions, and sensory details are supported when the story is presented as true. | Pass / Weak / Fail |

### Historical explainers

| Check | Result |
|---|---|
| One clear through-line organizes the selected facts. | Pass / Weak / Fail |
| People and events are shown only as the evidence supports. | Pass / Weak / Fail |
| The script separates documented facts from uncertainty, disagreement, and illustration. | Pass / Weak / Fail |
| The ending explains the outcome or significance of the development. | Pass / Weak / Fail |

### Mechanism explainers

| Check | Result |
|---|---|
| The central question and the mechanism's purpose are clear. | Pass / Weak / Fail |
| The needed parts or stages are explained in an understandable order. | Pass / Weak / Fail |
| The causal links between parts or stages are accurate. | Pass / Weak / Fail |
| Analogies and examples clarify rather than replace the real explanation. | Pass / Weak / Fail |
| Important simplifications are acknowledged. | Pass / Weak / Fail |

### YouTube-Kit handoff

`2-script-writer.md` ("Before you stop") holds the pipeline's own final
checks; they come first. In addition:

| Check | Result |
|---|---|
| The output follows `templates/script.md`. | Pass / Weak / Fail |
| Visual descriptions do not present imagined scenes as archival evidence. | Pass / Weak / Fail |
| Narration, visual notes, and chapter structure match the brief. | Pass / Weak / Fail |

Report weak or failed checks honestly. A self-check does not replace the
independent fact-check.

## 14. Standalone output format

Use this format when writing independently and no pipeline template
overrides it.

1. **Assumptions:** Only assumptions actually made.
2. **Story mode and through-line:** The chosen mode and why it fits.
3. **Story core:** The fields from Step 5 that apply.
4. **Story spine:** The adapted sequence from Step 6.
5. **Hook options:** Three options, the chosen one, and a brief reason.
6. **Final script:** Timestamps where useful for short videos, and short
   `[pause]` or visual suggestions where they help.
7. **Self-check:** The rows from Step 13 that apply, reported honestly.
8. **Weak points and improvements:** One to three specific remaining
   issues. If none remain, say so instead of inventing problems.
9. **Estimated length:** Narration word count and estimated duration,
   marked as an estimate.

## 15. Language and audience

- **Nepali:** Devanagari unless the brief or user asks for Romanized. Use
  natural spoken Nepali, not formal or bookish phrasing.
- **English for international audiences:** Avoid unexplained Nepal-specific
  references unless they matter to the story; explain needed local context
  naturally.
- **Mixed language:** Follow the audience and the user's mix. Use English
  technical terms only where the audience understands them or they are
  genuinely useful.
- **All languages:** Keep meaning, factual precision, and natural spoken
  rhythm. Do not translate idioms literally when it sounds unnatural.

## 16. Working principles

1. Story structure serves the subject; the subject does not serve a formula.
2. A compelling narrative never comes at the cost of accuracy.
3. Curiosity is stronger when the video truly answers the question it
   raises.
4. A real person's inner life is never invented to make a scene emotional.
5. An explainer leaves the viewer understanding something, not only feeling
   suspense.
6. Every section advances the story, clarifies the mechanism, sets needed
   context, or delivers a consequence.

## 17. Sources and craft influences

Robert McKee, *Story*; John Yorke, *Into the Woods*; Blake Snyder, *Save the
Cat!*; Lisa Cron, *Wired for Story*; Matthew Dicks, *Storyworthy*; The Moth,
*How to Tell a Story*; Emma Coats's widely circulated "22 rules" list (not
an official Pixar rulebook); Kurt Vonnegut's discussions of story shapes.

These are influences, not proof that every rule here comes from them. The
structures and timing ranges are practical heuristics: check them against
the subject, audience, narrator, and the channel's own analytics.
