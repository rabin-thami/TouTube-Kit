# Stage 3 — Outline and script

Input: `run.json`, `claims.md`, `research.md`.
Output: `<run>/hooks.md`, `<run>/outline.md`, then `<run>/script.md`
(formats: AGENTS.md → File contracts → outline.md, script.md).

Craft rules come from `skills/storytelling/SKILL.md`. Read these sections:
§4 foundations, §5 angle, §6 structure, §7 hooks, §11 suspense/reveals,
§12 pacing, §13 voice, §17 endings, §18 revision, §21 templates.
Hook and retention evidence: `skills/storytelling/references/hooks-engineering.md`
(§3.3 hook checklist, §3.4 hook patterns, §3.6 open loops, §4.4 long-form
structure, §6.1 YouTube first 30 s) and
`skills/storytelling/references/attention-retention-manual.md` (§3.4 curiosity
progression, §4.6 honesty, §9.3 question ledger, §11.4 ending). Read only those
sections. That material covers craft only. Facts still come only from claims.md.

## Step 0 — hooks.md (hook lab, before the outline)

1. Pick the working title first (60 characters or fewer, a statement, not a question).
2. Write at least 5 hook candidates, each from a **different** pattern in
   hooks-engineering.md §3.4. Each is the full Scene 1 narration: 40 words or
   fewer, at most one number, and it must confirm the title's promise.
3. Every hook states facts, so tag its claims (`[C01][C07]`). VERIFIED claims,
   or DISPUTED ones only if the hook says they are disputed.
4. Score each 0, 1 or 2 on: relevance, specificity, curiosity, credibility,
   clarity, payoff, fit, honesty (2 = strong). Be strict: a 2 must be earned.
   Write one line per hook in outline.md `## Packaging` explaining its scores.
5. Mark the best passing hook `chosen = yes`. Run `python3 kit.py hooks <run>`:
   it rejects hooks that fail a gate (wrong or unverified claims, too long,
   more than one number, clickbait, any 0 score, no key word from the title)
   and prints the top 2. Fix or replace until it prints `HOOKS OK`.

## Step A — outline.md (before any script text)

1. **Angle.** List 3 candidate angles (skill §5). Score each 1-5 on
   curiosity, clarity, movement, depth, payoff, and evidence (enough VERIFIED
   claims to carry it). Pick one and say why in one line.
2. **Differentiation.** One line: what this video says that the obvious
   version of this topic does not. Search the web for existing video titles on
   the topic if you can; do not copy them.
3. **Packaging.** Working title (60 characters or fewer) and a one-sentence
   premise. The ending must deliver what the title promises.
4. **Story brief** (skill §21.1) and **logline** (§21.2).
5. **Beat sheet** (skill §21.3). Every beat lists the claim ids it uses.
   A beat with no claim id must be a question, transition or reflection.
6. **Retention plan:**
   - **First 30 seconds (words 1-75) stay on the title's promise.** Context or
     detours that the title does not promise come after (hooks-engineering §6.1).
   - a re-hook by about 45 seconds (around word 110)
   - a midpoint turn (skill §11.4)
   - **Question ledger** (attention-retention-manual §9.3), a table:
     `| question | why it matters | scene that advances it | scene that resolves it |`
     One primary question plus a few supporting ones; every row is resolved or
     explicitly left open for a stated reason.
   - **Scene exits:** at most half the scenes after the hook end on a question;
     the rest end on a consequence, contradiction or reveal (`recheck` warns).
7. **Ending type** (skill §17.1). If the central question has no settled
   answer in claims.md, use "open-ended" and say so honestly. Never fake a reveal.
   Name the **one sentence the viewer should remember** and the final image,
   tied back to the hook (attention-retention-manual §11.4). No subscribe pitch.

## Step B — script.md

1. Write in the language, length and audience from `run.json`, about 150
   narration words per minute. `kit.py recheck` fails outside the target ±10%.
2. **Scene 1: Hook** is exactly the `chosen` hook from hooks.md, one sentence
   per line with its tags (`recheck` fails if the words differ). The script's
   `# ` title is the hooks.md title.
3. One sentence per line. End each line with its tags: `[C03]`, `[C03][C07]`,
   or `[NF]` for a line with no fact (question, transition, reflection).
   Never put a fact behind `[NF]`.
4. **Facts:**
   - Only `VERIFIED` claims, tagged `[Cxx]`.
   - A `DISPUTED` claim only phrased as disputed ("historians still debate",
     "sources disagree", "possibly"). Fold disputes into the story's
     question; at most 2 DISPUTED lines per scene.
   - Never an `UNVERIFIED` claim.
   - **Story detail is fact.** A place, object, quote, number or scene
     detail needs a claim. If a beat needs a fact that is not in claims.md, go
     back to stage 2 and verify it first. Never invent private thoughts,
     dialogue or motives (skill §8.1).
5. **Numbers:** at most one number per line; drop numbers that do not
   change the story.
6. **Visual and production lines** start with `>` and are not narration:
   - `> VISUAL [ARCHIVAL|RECONSTRUCTION|MAP|TIMELINE|DIAGRAM|DETAIL|B-ROLL]: ...`
     (a RECONSTRUCTION must never pass as original)
   - `> TEXT: ...` for short on-screen text
   - `> SOUND: ...` for music, effects or silence, only where useful
   - `> NOTE: ...` for pronunciation or production notes
7. **Revise** with skill §18 (four passes, cut test, read-aloud test). Append
   the skill §21.5 script review, filled in, to the end of `outline.md`.

## Done when

- `python3 kit.py hooks <run>` prints `HOOKS OK`,
- `outline.md` exists with the sections above, and
- `python3 kit.py recheck <run>` exits 0. Read its `WARN` lines and fix them
  where you can. Then go to stage 4.
