# Upstream: yt-script

These files are copied unchanged from a third-party project. They are not
YouTube-Kit code.

- **Project:** youtube-agent-skill by Jake Schincariol
  (https://github.com/Jakeschincariol/youtube-agent-skill)
- **Folder:** `skills/yt-script/`
- **Commit:** `a2feb2104981a375ffd4f87ee04f4f5344ac43c6` (2026-09-16)
- **Licence:** MIT, copyright (c) 2026 Jake Schincariol. Full text in
  `LICENSE` in this folder.
- **Copied on:** 2026-11-16

| File | Status | SHA-256 |
|---|---|---|
| `hooks.json` | unchanged (21 hook formulas) | `76c47b4ad410a8856c9d27aa489d7c447b3ebe30a9024f03e2d59fefe267f5cb` |
| `hookscore.py` | unchanged (reads `hooks.json` from its own folder) | `8205dca03de1d5d8e25614e7c0d8d40fd756a99b838320462195b342d5eb0545` |
| `LICENSE` | upstream licence text | `857c8d5276809c8196b3cd7cb3300324768bfc562b2b6281b06d6865058e186c` |

## How YouTube-Kit uses them

- Step 2 (`pipeline/2-script-writer.md`, "Hooks") uses the 21 formulas as
  starting points and scores English hooks through `tools/hookcheck.py`,
  which strips fact tags, refuses Devanagari text, and then calls
  `hookscore.py` unchanged.
- Upstream's own warning stands: the score was calibrated on 74 English
  short-form hooks. It separates bad hooks from real ones, and barely
  separates a creator's hits from misses. It never predicts views, CTR or
  retention.

## Kit-owned additions (not upstream)

- `tools/hooks-kallaway.json`: 6 extra formulas and 3 rules after
  Kallaway's hook method (Context + Lean + Snapback, triple alignment,
  loops). Written for YouTube-Kit from the user's notes; not part of
  upstream and not covered by its licence.
- `tools/kallaway_score.py`: a second English panel (clarity, specificity,
  curiosity, context+lean, snapback). It reads both formula files and uses
  the same weakest-link verdict as upstream. It is not calibrated on view
  data.

## Left out on purpose

From upstream `SKILL.md` (not copied):

- Its input contract (a raw idea, a `~/.claude/youtube/voice.md` profile,
  asking for three of the creator's videos): Step 2 reads `brief.md` and
  `facts.md` and asks nobody.
- `[ON SCREEN: ...]` beat markers: YouTube-Kit uses `[visual: ...]`, which
  `tools/narration.py` parses into scenes.
- Handing back two hooks with score panels: `templates/script.md` shows
  three options.
- The 150 words-per-minute runtime and the "ship it, or change it?" ending:
  the kit has its own length guide and approval gates (`AGENTS.md`).

Adapted into `pipeline/story-craft.md` (sections 7 and 12): the three jobs
of a hook, one promise per hook, the opening turn, the explicit payoff, and
one closing ask.

To update: copy the two files from a newer upstream commit, then update the
commit and hashes above and run `python3 tools/hookcheck.py selftest`.
