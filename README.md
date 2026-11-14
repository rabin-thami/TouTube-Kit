# Video Script Pipeline

Research -> script -> fact-check -> your approval -> assets -> voiceover ->
timing -> animation -> your review. Steps up to assets are plain Markdown, so
they work in any coding agent that can read and write files and search the
web. Voiceover, timing, and animation also need Python 3, Node.js 22+
(HyperFrames), FFmpeg, and an `OPENROUTER_API_KEY` (tests) or `ELEVENLABS_API_KEY` (finals). Copy `.env.example` to `.env` and fill in your keys; `.env` is git-ignored.
`tools/narration.py` does the voiceover and timing work; run
`python3 tools/narration.py selftest` to check it.

## Use it

1. Open this folder in your agent (Claude Code, Codex, OpenCode, or another).
2. Type your request, for example:

   > Make a script for a 5 to 8 minute YouTube video about the history of the
   > computer mouse. Language: English. Audience: general viewers.

3. The agent reads `AGENTS.md`, creates `runs/<date>-<topic>/`, and works
   through the steps. It stops for your approval before finding assets.

To run one step: "Do only the research step for <topic>" or "Fact-check
runs/<folder>/script.md".

## How each tool picks it up

| Tool | What it reads | Subagents |
|---|---|---|
| Claude Code | `CLAUDE.md`, which imports `AGENTS.md` | `.claude/agents/*.md` |
| OpenCode | `AGENTS.md` | `.opencode/agents/*.md` |
| Codex | `AGENTS.md` | none included; it runs the steps in order in one session |
| Others | `AGENTS.md` if supported; otherwise say "read AGENTS.md first" | none |

The subagent files are thin wrappers. The real instructions are in
`pipeline/`. Edit those, not the wrappers.

## What is where

- `AGENTS.md`: the pipeline and the rules. This is the "orchestrator".
- `pipeline/`: one instruction file per step, plus `story-craft.md`.
- `templates/`: the format of each handoff file.
- `runs/`: one folder per video.

## Limits

- Not tested in Codex or OpenCode. The file locations follow each tool's
  documentation as of November 2026. Tools change; check their docs if a
  file is not picked up.
- The agent needs web search. Without it, the research step stops.
- The fact-check is only as good as the fact sheet. Open the source links
  yourself for the claims that matter most.
- Asset licences: the agent records what it finds. The final decision is
  yours. This is not legal advice.
- To keep the fact-check independent in a tool without subagents, run step 3
  in a new session.
