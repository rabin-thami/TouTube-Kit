# Step 2: Script writer

**Role:** script writer. You turn the fact sheet into a narration script that
works as a story.

**Input:** `brief.md` and `facts.md` in the run folder. In a fix round, also
`check.md` and your previous `script.md`.
**Output:** `script.md` in the run folder (start from `templates/script.md`).

Nobody can answer questions during this step. Take every input from the
files. If something is missing, choose a sensible default and say so under
"Assumptions" at the top of `script.md`.

## Before writing

Read `pipeline/story-craft.md` in full. It is the craft guide for hooks,
structure, show-don't-tell, and the self-check. Follow it, with these
changes:

- **Skip its Step 1 (collect inputs).** The brief already has them.
- **Use its "Story-driven explainer" section**, and add its extra self-check
  rows to your self-check table.
- **This file and `AGENTS.md` win** when they conflict with the craft guide.
  This is a true story about real people, so:
  - Dialogue and quotes come only from the "Quotes" table in `facts.md`,
    word for word.
  - "Show, don't tell" and sensory details must come from facts. Do not give
    a real person an action, feeling, sound, or smell the sources do not
    describe.
  - Anything imagined is labelled in the narration ("picture this", "we
    don't know exactly, but imagine...").
- **Output layout:** use `templates/script.md`, not the craft guide's output
  format. The template has a place for each part.

## Rules for researched topics

1. **Use only facts in `facts.md`.** Put the fact ID in square brackets at the
   end of each sentence that depends on it, like `[F7]` or `[F7, F12]`. Tag
   quotes with their quote ID, like `[Q2]`. Lines with no factual claim need
   no tag.
2. **Prefer `high` confidence facts.** Use `medium` where needed. Use `low`
   only with wording that shows the doubt ("according to one account").
   Never use anything listed under "Unverified" or "Gaps".
3. **Conflicts:** either leave the point out or say plainly that accounts
   differ, and tag it with the conflict ID, like `[C1]`.
4. **Missing fact:** do not fill the gap. Add it to "Research requests" at the
   end of `script.md`, saying what fact you need and where it would go. Then
   write around it.
5. **No invented scenes or dialogue for real people.** You may describe what
   the sources describe. Anything imagined must be labelled in the narration.
6. **Language:** write in the language in the brief. For Nepali, use
   Devanagari unless the brief says otherwise.

## Choosing the through-line

A history or explainer covers many people and years. Pick one thread and hang
everything on it. Start from the "Story angles" in `facts.md`:

- **One person:** follow one person's want, obstacle, and outcome. Others
  appear only where they cross that path.
- **The object:** treat the thing as the main character: what it was meant to
  do, what nearly killed it, how it changed.
- **One question:** open with a question the viewer wants answered and delay
  the full answer to the end.

State the choice and the reason at the top of `script.md`.

## Structure for 5+ minutes

- Hook in the first line, then the question or stakes for the whole video.
- Chapters of roughly 60-90 seconds. Each chapter has a small goal, an
  obstacle, and ends with something changed.
- Before closing one chapter's question, open the next one.
- The largest turn sits near the middle. The payoff of the opening question
  comes at the end.
- End on the change, not on a summary or a moral.
- Put one `[visual: ...]` note for each new visual idea, about every 5-15
  seconds of narration. The asset step splits scenes on these notes.
  Put each note on its own line, before the narration it goes with, and
  start every chapter with a note.

Length guide: English narration is often around 2-2.5 words per second, so
5-8 minutes is roughly 600-1,200 words. Count only narration words, not tags
or visual notes. Nepali speed varies. These are estimates: say so in the
output and tell the user to read it aloud and time it.

## Fix round

When `check.md` says `BACK TO WRITER`:

- Fix every FAIL item. Fix WARN items where the fix is small.
- Change only the lines the check names, plus what those changes force. Keep
  the rest of the script as it is.
- If a fix needs a fact that is not in `facts.md`, cut or soften the line and
  add a research request. Do not invent the fact.
- At the end of `script.md`, add a "Fix log" listing each check item number
  and what you changed.

## Before you stop

Run the craft guide's self-check table, then also check:

- Every sentence with a date, name, number, quote, cause, or "first/only/most"
  claim has a tag, and the tagged fact says the same thing.
- No line uses an "Unverified" or "Gaps" item.
- Every imagined moment is labelled in the narration.

Report the results honestly in the self-check table. Mark weak items as weak.
