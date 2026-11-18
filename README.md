# History Video Kit

Type one topic, get a researched, fact-checked, approved YouTube script plus a
licensed asset list with the files downloaded.

```
Make a video script about History of the printing press
```

Works with any coding agent that can read files, run `python3`, and search
and fetch web pages (Claude Code, Codex, Cursor, OpenCode, ...).

## Setup

- Python 3.9+ (stdlib only, nothing to install).
- An agent with web search/fetch.
- Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`. Other agents read
  `AGENTS.md` directly; if yours does not, tell it: "Read AGENTS.md and follow it."

Check the helper:

```
python3 kit.py self-test
```

## How to run

1. Open your agent in this folder.
2. Say: `Make a video script about History of <X>`.
   Optional overrides: `..., 5-6 min, Spanish, kids`
   (defaults: 8-12 min, English, general viewers).
3. The agent runs stages 1-4 and **stops at the approval gate**, showing you
   `script.md` and `claims.md`.
4. Reply `approved` to continue, or say what to change.
5. The agent finds licensed assets, downloads them, and writes `sources.md`.

Output lands in `runs/<YYYY-MM-DD>-<topic-slug>/`:

| File | What |
|------|------|
| `run.json` | topic and settings |
| `research.md` | timeline, people, turning points, causes/effects, surprising facts; every fact sourced |
| `claims.md` | id / claim / source 1 / source 2 / status (VERIFIED, DISPUTED, UNVERIFIED) |
| `hooks.md` | 5+ hook candidates from different patterns, scored on 8 criteria; `kit.py hooks` gates and ranks them; you see the top 2 at approval |
| `outline.md` | angle, title/premise, beat sheet, retention plan with question ledger, ending (craft: `skills/storytelling/`) |
| `script.md` | scenes, hook, one sentence per line, each tagged with claim ids; `>` lines for VISUAL / TEXT / SOUND / NOTE |
| `approval.json` | your approval, tied to the exact script/claims text |
| `assets.md` + `assets/` | per-scene media: URL, type, license, attribution, file |
| `sources.md` | bibliography + YouTube description attribution block |

## Status and resume

```
python3 kit.py status                 # all runs
python3 kit.py status <run-folder>    # one run: which stage it stopped at
```

To resume, tell the agent `Resume <run-folder>` (or repeat the original
request). It runs `status` and continues from the reported stage.

## Helper commands

| Command | Does |
|---------|------|
| `kit.py new "<topic>" [--minutes --language --audience]` | create the run folder |
| `kit.py status [<run>]` | show the stage reached and the prompt to resume from |
| `kit.py recheck <run>` | fail loudly if script.md uses a missing, UNVERIFIED, or unhedged DISPUTED claim, a VERIFIED claim lacks two independent sources, a line is untagged, the hook is too long, or the length is off |
| `kit.py approve <run> --message "approved"` | record approval (only for "approved") |
| `kit.py fetch-assets <run>` | download asset files |
| `kit.py check-assets <run>` | licenses (PD, CC0, CC BY, CC BY-SA only), attribution, files, every scene covered |
| `kit.py check-urls <run>` | open every claims.md source URL; fail on dead links |
| `kit.py hooks <run>` | gate and rank the hook candidates; print the top 2 |
| `kit.py agents` | list other agent CLIs installed (opencode, codex, gemini, agy) |
| `kit.py delegate <run> --agent opencode [--model M] [--stages 1-2]` | run stages headless in another agent CLI, then print status |
| `kit.py export <run>` | stage 8: write `video/plan.json` (narration without tags, shots, assets, credits) |
| `kit.py shots <run>` | stage 8: check the Director's shot list (every line covered in order, licensed assets, readable text, labelled reconstructions) |
| `kit.py review <run> --scene N --verdict PASS\|NOTES [--notes "..."]` | stage 8: the Director's verdict, tied to the scene's hash |
| `kit.py check-render <run> [--final]` | stage 8: audio matches approved narration, compositions, licensed media only, credits; `--final` also needs draft approval |
| `kit.py approve-draft <run> --message "approved"` | record the user's approval of `video/draft.mp4` |
| `kit.py self-test` | built-in tests |

## Delegating research to a cheaper agent

Research (stages 1-2) uses the most tokens. If another agent CLI is
installed, the main agent asks whether to hand those stages off, and which
model to use. The default for opencode is `opencode-go/deepseek-v4-pro`;
pass `--model` to change it, e.g.
`--model opencode-go/minimax-m3.1-flash`. The main agent waits, then checks
the links with `check-urls`, spot-checks claims, and continues from stage 3.
Output goes to `<run>/delegate-<agent>.log`.

Script writing (stage 3) goes to `agy` with a fallback chain:
`--agent agy --stages 3 --model gemini-4-hydrogen-high,claude-opus-5-5-high`.
`--model` takes a comma list; the next model runs if one errors, hits a
limit, times out (45 min), or writes no outline.md/script.md. If all fail,
the main agent writes stage 3 itself. A delegated stage-3 run may not edit
research.md or claims.md; the kit fails the run if it does.

Caution: the delegated CLI runs with auto-approved permissions
(`opencode run --auto`, `codex exec --full-auto`, `gemini --yolo`,
`agy --dangerously-skip-permissions`), so it can
run shell commands in this folder without asking. Delegate only to agents you trust.

## Layout

```
AGENTS.md       orchestrator + file formats
CLAUDE.md       imports AGENTS.md
kit.py          helper
stages/         one prompt per stage (01-08); 08 is production (voiceover + render)
skills/         storytelling craft skill (also copied to .claude/skills/ for Claude Code);
                references/ holds the hook-engineering and attention/retention manuals
plans/          build blueprint
runs/           one folder per video
```

## Not included (by design)

Thumbnails, YouTube upload, web UI, database, paid APIs (except Google Cloud
Text-to-Speech for the production voiceover). Voiceover and rendering are
stage 8: `stages/08-production.md`.

## Limits

- "Independent sources" is checked as different sites; the agent must still
  avoid sources that copy each other.
- "Stated as disputed" is checked by hedge words ("debate", "possibly", ...).
- `[NF]` (non-factual line) is trusted; review it at the approval gate.
- A `[Cxx]` tag is not compared with the sentence's wording; the approval
  gate is where a human checks that each line says what its claim says.
- The license cell in assets.md is trusted as written; copy it from the
  file page (the Commons API returns it in `extmetadata`).
- `check-urls` proves a page answers, not that it states the claim.
- Approval covers `script.md` and `claims.md` only.
- Delegation guards: inside a delegated agent, `approve` and `delegate`
  refuse (`KIT_DELEGATED=1`), and `delegate` fails if the agent changed
  `kit.py`, `AGENTS.md`, `CLAUDE.md`, `stages/` or `approval.json`.
  These are tripwires, not a sandbox.
