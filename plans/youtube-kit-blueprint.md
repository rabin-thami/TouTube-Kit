# Blueprint: YouTube History-Video Production Kit

Objective: type one topic ("History of <X>") and get a researched, fact-checked,
user-approved script plus a licensed, downloaded asset list.

Mode: direct (no git repo, no gh). Edit in place. Rollback = delete the files a phase created.

## Invariants (check after every phase)

- `python3 kit.py self-test` passes (from Phase 3 on).
- Python helpers use stdlib only.
- No paid APIs, no copyrighted media, no invented quotes or dates.
- Nothing for voiceover, rendering, thumbnails, upload, web UI or database.

## Layout (target)

```
AGENTS.md            orchestrator: the full stage-by-stage procedure + file contracts
CLAUDE.md            @AGENTS.md import (Claude Code entry point)
README.md            setup + how to run + how to resume
kit.py               stdlib helper: new | status | recheck | approve | fetch-assets | check-assets | self-test
stages/01-research.md ... stages/07-sources.md   one prompt per stage
stages/08-next-production.md                   hook for a later voiceover/render phase (not built)
runs/<YYYY-MM-DD>-<slug>/                      one folder per run
```

## Phase dependency graph

```
P1 scaffold ──┬── P2 stage prompts ──┐
              └── P3 kit.py helper ──┴── P4 end-to-end run ── P5 code review
```

P2 and P3 share no files; both depend on the formats fixed in P1
(AGENTS.md "File contracts").

---

## Phase 1 — Scaffold and file contracts

Context brief: empty folder. Define the run-folder layout and the exact
Markdown table formats every stage reads and writes, so prompts and the
Python helper agree.

Tasks:
- AGENTS.md: trigger phrase, defaults (8-12 min, English, general viewers),
  override syntax, stage order, approval-gate rule, resume rule, file contracts.
- CLAUDE.md: `@AGENTS.md`.
- README.md: setup, how to run, how to resume, how status works.

Verify: AGENTS.md names every stage file and every `kit.py` command.
Exit: file contracts written once, in AGENTS.md only.

## Phase 2 — Stage prompts

Context brief: one Markdown file per stage under `stages/`. Each states
inputs, outputs, rules, and its done-check command.

Tasks: 01-research, 02-claims, 03-script, 04-recheck, 05-approval,
06-assets, 07-sources, 08-next-production (hook only).

Verify: each prompt names its exact output file and the `kit.py` command
that checks it.
Exit: an agent can run any stage reading only AGENTS.md + that stage file.

## Phase 3 — kit.py helper (correctness-critical)

Context brief: single stdlib script, subcommands:
- `new "<topic>" [--minutes 8-12] [--language English] [--audience ...]`
  creates `runs/<date>-<slug>/run.json`.
- `status <run>` prints the first incomplete stage and the prompt to resume from.
- `recheck <run>` fails loudly (exit 1) if any script claim id is missing from
  claims.md, is UNVERIFIED, is a DISPUTED claim not phrased as disputed, a
  VERIFIED claim lacks two sources on different domains, or a narration
  sentence has no claim tag.
- `approve <run>` records sha256 of script.md + claims.md; editing either later
  voids approval.
- `fetch-assets <run>` downloads each asset file URL into `assets/`.
- `check-assets <run>` fails if a license is not allowed, attribution is empty,
  or a file is missing.
- `self-test` runs built-in fixtures (good and broken) for recheck and assets.

Verify: `python3 kit.py self-test` exits 0; broken fixtures are rejected.
Exit: all subcommands work on a temp run.

## Phase 4 — End-to-end: "History of the printing press"

Run stages 1-7 per AGENTS.md. Stop at the approval gate and wait for the
user's "approved". Then assets + sources.
Verify: `kit.py status` reports complete; `recheck` and `check-assets` exit 0.

## Phase 5 — Code review

Run the code-reviewer agent over the kit. Fix critical/high findings,
re-run self-test.

## Review notes (self-review against blueprint checklist)

- Every phase has a verify command and exit criterion.
- Hidden coupling: prompts and kit.py share table formats; fixed once in
  AGENTS.md "File contracts", P2/P3 cite it.
- Approval cannot be faked by file existence: approval hash ties it to content.
- Asset licensing is checked by code, not only by prompt.
