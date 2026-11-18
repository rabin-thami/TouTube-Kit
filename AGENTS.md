# History Video Kit — Orchestrator

You are producing a researched, fact-checked YouTube script and a licensed
asset list for a history topic. Any coding agent that can read files, run
`python3`, and search/fetch web pages can follow this file.

## Trigger

When the user says something like **"Make a video script about History of <X>"**,
run stages 1-7 below, in order, for that topic.

Optional overrides may follow the topic, e.g.
`Make a video script about History of the bicycle, 5-6 min, Spanish, kids`.

| Setting  | Default          | Flag for `kit.py new` |
|----------|------------------|-----------------------|
| Length   | 8-12 min         | `--minutes 8-12`      |
| Language | English          | `--language English`  |
| Audience | general viewers  | `--audience "general viewers"` |

## Procedure

0. **Start or resume.**
   - Run `python3 kit.py status`. If a run for this topic already exists and is
     not complete, resume it at the stage `status` reports. Do not redo
     finished stages.
   - Otherwise create one:
     `python3 kit.py new "History of <X>" [overrides]`. It prints the run folder,
     `runs/<YYYY-MM-DD>-<topic-slug>/`, and writes `run.json` there.
   - **Optional delegation (saves the main agent's usage).** Run
     `python3 kit.py agents`. If another agent CLI is installed, ask the user:
     "Delegate research (stages 1-2) to <agent>? Which model? (default:
     <its default model>)". If yes, run
     `python3 kit.py delegate <run> --agent <agent> [--model <provider/model>] --stages 1-2`
     and wait for it to exit. Do not work on the run meanwhile. Afterwards run
     `kit.py status <run>` and `kit.py check-urls <run>`, spot-check a few
     claims against their pages, fix gaps yourself, then continue at stage 3.
     If no CLI is installed or the user says no, do every stage yourself.
   - **Script writing (stage 3 only):** if `agy` is installed, delegate it with a
     model fallback chain:
     `python3 kit.py delegate <run> --agent agy --stages 3 --model gemini-4-hydrogen-high,claude-opus-5-5-high`.
     Each model is tried in order; one counts as failed on an error, rate
     limit, timeout, or if it wrote no `outline.md` and `script.md`. If every
     model fails, write stage 3 yourself. Either way, review the result
     (recheck, `[NF]` lines, each line against its claim) before stage 5.
     Stage 5 can never be delegated: it needs the user.
1. For each stage, read its prompt file, do the work, write its output into
   the run folder, then run its check command. Do not move on until the check
   passes.

| # | Stage            | Prompt                     | Output         | Check |
|---|------------------|----------------------------|----------------|-------|
| 1 | Research         | `stages/01-research.md`    | `research.md`  | `kit.py status <run>` |
| 2 | Claims           | `stages/02-claims.md`      | `claims.md`    | `kit.py check-urls <run>`, `kit.py status <run>` |
| 3 | Hooks + outline + script | `stages/03-script.md` | `hooks.md`, `outline.md`, `script.md` | `kit.py hooks <run>`, `kit.py recheck <run>` |
| 4 | Re-check         | `stages/04-recheck.md`     | (none)         | `kit.py recheck <run>` exits 0 |
| 5 | **Approval gate**| `stages/05-approval.md`    | `approval.json`| `kit.py status <run>` |
| 6 | Assets           | `stages/06-assets.md`      | `assets.md`, `assets/` | `kit.py check-assets <run>` |
| 7 | Sources          | `stages/07-sources.md`     | `sources.md`   | `kit.py status <run>` says complete |

`<run>` is the run folder path or just its name. Run `kit.py` from the kit root.

**Production (stage 8)** runs only on a COMPLETE run, when the user asks for
the video: follow `stages/08-production.md` (voiceover, Director shot list,
animatic, HyperFrames compositions, Director review, draft, user approval,
final render). The Director is a separate agent (`.claude/agents/director.md`)
that plans and reviews but never builds; only it records `kit.py review`.
Checks: `kit.py export <run>`, `kit.py shots <run>`, `kit.py check-render <run>`, and
`kit.py check-render <run> --final` after
`kit.py approve-draft <run> --message "<user's reply>"`. The draft approval is
a hard stop like stage 5. No thumbnails or upload.

## Hard rules

- **Never invent** facts, dates, quotes, names, numbers, URLs or licenses.
  If you cannot find a source, the claim is UNVERIFIED and stays out of the script.
- Use only sources you actually opened in this run. Copy URLs exactly.
- Preferred sources: primary sources, archives, museums, libraries,
  peer-reviewed or university-press work, reputable encyclopedias
  (Britannica, national biographies). No unsourced blogs, content farms,
  AI-generated pages, social media, or forums.
- Media: only public domain, CC0, CC BY, CC BY-SA. Never NC, ND, "fair use",
  "all rights reserved", or unknown licenses.
- No paid APIs, except Google Cloud Text-to-Speech for the production
  voiceover (user's decision, 2026-11-18). No web UI, database, thumbnails,
  upload. Voiceover and rendering happen only in the production phase, after
  stage 7 is complete.
- **Stage 5 is a hard stop.** Do not start stage 6 until the user replies
  "approved" in this conversation. Any other reply means revise and ask again.

## File contracts

`kit.py` parses these formats. Keep them exact.

### claims.md

One Markdown table with this header, in this column order:

```
| id | claim | source 1 | source 2 | status |
|----|-------|----------|----------|--------|
| C01 | Gutenberg's 42-line Bible was completed by about 1455. | https://... | https://... | VERIFIED |
```

- `id`: `C` + two or more digits, unique.
- `source 1`, `source 2`: full `https://` URLs, or `-` when missing.
- `status`: `VERIFIED` (2+ independent sources agree; the two URLs must be on
  different domains), `DISPUTED` (credible sources disagree; say how in the
  claim text), or `UNVERIFIED` (fewer than two independent sources).

### hooks.md

Written first in stage 3. A `Title: <working title>` line, then one table:

```
| id | pattern | hook | claims | relevance | specificity | curiosity | credibility | clarity | payoff | fit | honesty | total | chosen |
|----|---------|------|--------|-----------|-------------|-----------|-------------|---------|--------|-----|---------|-------|--------|
| H1 | contradiction | Spoken hook text, no tags. | [C73][C74] | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 15 | yes |
```

- At least 5 rows, each a different pattern (hooks-engineering.md §3.4).
- Scores are 0, 1 or 2; `total` is their sum; exactly one row `chosen = yes`.
- `kit.py hooks` rejects a row on: a claim missing / UNVERIFIED / unhedged
  DISPUTED, no tags, over 40 words, more than one number, clickbait wording,
  any 0 score, or no key word shared with the title.
- Scene 1 of script.md must be the chosen hook's words.

### outline.md

Written before script.md (stage 3, step A). Must contain these headings:
`## Angle`, `## Packaging`, `## Beat sheet`, `## Retention plan`, `## Ending`.
Craft guidance: `skills/storytelling/SKILL.md`.

### script.md

```
# <Video title>

Target: <minutes> min, <language>, <audience>

## Scene 1: Hook
> VISUAL: what is on screen (not narration)
One narration sentence per line, ending with its claim tags. [C01]
A line with no factual content is tagged as non-factual. [NF]

## Scene 2: <title>
...
```

- Scenes start with `## Scene <n>: <title>`, numbered from 1. Scene 1 is the
  hook: title contains "Hook", 40 narration words or fewer (about 15 s).
- Lines starting with `>` are visual/production notes and are not narration:
  `> VISUAL [ARCHIVAL|RECONSTRUCTION|MAP|TIMELINE|DIAGRAM|DETAIL|B-ROLL]: ...`,
  `> TEXT: ...`, `> SOUND: ...`, `> NOTE: ...`.
- Every narration line is one sentence and ends with one or more tags:
  `[C01]`, `[C01][C04]`, or `[NF]` for a line that states no fact.
- A line using a DISPUTED claim must say so in words ("historians debate",
  "disputed", "possibly", "according to tradition", ...).
- Total narration: about 150 words per minute of the target length.

### approval.json

Written only by `python3 kit.py approve <run> --message "<user's reply>"`.
It stores hashes of `script.md` and `claims.md`; editing either afterwards
voids the approval.

### assets.md

One Markdown table with this header, in this column order:

```
| scene | description | type | source page | file url | license | attribution | file |
|-------|-------------|------|-------------|----------|---------|-------------|------|
| 1 | Page of the Gutenberg Bible | image | https://commons.wikimedia.org/wiki/File:... | https://upload.wikimedia.org/... | Public domain | "Title" by Author, Public domain, via Wikimedia Commons | s01-gutenberg-bible.jpg |
```

- `scene`: scene number from script.md. Every scene needs at least one row.
- `type`: `image`, `map`, `footage`, or `doc`.
- `license`: `Public domain`, `CC0`, `CC BY <ver>`, or `CC BY-SA <ver>`.
- `file`: bare file name; `kit.py fetch-assets` saves it to `<run>/assets/`.
- Do not use `|` inside a cell (it breaks the table); write "/" instead.

### sources.md

Sections `## Bibliography` and `## YouTube description`. The description
section contains a ready-to-paste attribution block for every asset.
