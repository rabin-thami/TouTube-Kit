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

Read `pipeline/story-craft.md` in full. It is the craft guide for story
modes, hooks, structure, narration, and the self-check. Follow its
"YouTube-Kit pipeline" list (section 1), with these changes:

- **Skip its Step 2 (collect inputs).** The brief already has them. Its
  section 3 (truth, evidence, and imagination) applies to every script.
  Where it says "ask", add a research request instead (rule 4 below).
- **Pick a story mode (its section 4).** For history and how-things-work
  topics, use its section 8. State the mode next to the through-line at the
  top of `script.md`.
- **Self-check:** use its section 13 core rows, the rows for your mode, and
  the YouTube-Kit handoff rows.
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

## Hooks

Follow the craft guide's section 7, then:

1. **Write five candidates**, each from a different approach: the craft
   guide's hook types, the 21 formulas in `tools/yt-script/hooks.json`, or
   the 6 Kallaway formulas in `tools/hooks-kallaway.json`. Read each
   formula's `fails_when` before using it.
2. **Check each one against the facts.** Every number, date, name,
   comparison, superlative ("first", "only", "biggest") and event in it
   needs a fact ID, at a confidence the wording respects (rule 2). Its
   promise must be one this script can pay off, with visuals the asset step
   can find (a "reveal" needs something to show). Drop or rewrite any that
   fail. A strong-sounding hook without support is never used.
3. **Evaluate them:**
   - **English:** write the surviving candidates to `hooks.txt` in the run
     folder, one per line, and run
     `python3 tools/hookcheck.py runs/<run-folder>/hooks.txt --topic "<2-3 subject words>"`.
     It strips fact tags and prints two panels per hook, each with its
     weakest property: the upstream one (specificity, address, stakes,
     curiosity, brevity) and the Kallaway one (clarity, specificity,
     curiosity, context+lean, snapback). Use the weakest properties to
     improve a hook, then score it again once. Put both verdicts in the
     "Score" column, for example `up 47 / K 52`.
   - **Nepali, or any hook with Devanagari:** do not run the scorer (it
     refuses them) and do not translate a hook to score it. Rate the same
     five properties as Strong / Adequate / Weak in words.
   - The score is a diagnostic heuristic. It never overrides fact support or
     fit, and never predicts views, CTR, or retention: do not say it does.
4. **Keep three** in the "Hook options" table of `script.md`, mark the
   chosen one, and give one line for each dropped candidate and why.

## Structure

Pick the structure by the length in `brief.md`.

### Shorts (under 90 seconds)

- Follow the craft guide's "30-60 second short" (section 9): hook in the first 3
  seconds, one idea, one turn, an ending that pays off the hook.
- Kallaway timing for the opening: the viewer knows the topic in 1 second
  (context), leans in by 3 seconds (proof, pain or stakes), and has an
  expectation flipped by 5 seconds (snapback). The flip must be true and in
  `facts.md`.
- One to three chapters. A chapter here is a beat (hook, middle, ending),
  not 60-90 seconds.
- A `[visual: ...]` note about every 2-5 seconds of narration: Shorts need
  faster picture changes than long videos.
- If the brief names a hook method or a call to action, map each of its
  parts to the narration lines at the top of `script.md`.

Length guide: about 100-140 English words for 45-60 seconds.

### 5+ minutes

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

Run the craft guide's self-check rows (section 13), then also check:

- Every sentence with a date, name, number, quote, cause, or "first/only/most"
  claim has a tag, and the tagged fact says the same thing.
- No line uses an "Unverified" or "Gaps" item.
- Every imagined moment is labelled in the narration.
- The ending pays off the chosen hook's promise explicitly, with at most one
  closing ask (craft guide, section 12).
- Every chapter starts with a `[visual: ...]` note, and no chapter ends with
  one. A note after the last line of a chapter has no narration, so its
  scene lasts 0 seconds.

Report the results honestly in the self-check table. Mark weak items as weak.
