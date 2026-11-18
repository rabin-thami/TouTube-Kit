# Production phase brief (voiceover + render)

Handoff for a fresh session. Read this, then `AGENTS.md`, then
`stages/08-production.md`.

## Resume here (updated 2026-11-18, end of session 2)

The plan was confirmed and phases 0-2 are built:

- Phase 0: HyperFrames 0.9.67 (Apache-2.0) pinned; style kit in
  `skills/vox-editorial-style/`; `.venv-tts/` has Kokoro; Google TTS allowed
  by AGENTS.md, but `GOOGLE_TTS_API_KEY` is not set yet.
- Phase 1: `kit.py export`, `shots`, `review`, `check-render [--final]`,
  `approve-draft`; self-test 132 checks.
- Phase 2: `tools/voice.py`; the sample run has the full Kokoro `am_michael`
  voiceover (9 scenes, 11.8 min), word timings, and `video/captions.srt`.
- Director agent: `.claude/agents/director.md` + the user's handbook
  `references/motion-direction-handbook.md`.

**Next (user said yes):** Phase 3 on `runs/2026-11-18-history-of-the-printing-press`.
1. Call the `director` agent (job A) to write `video/shots.md`; `kit.py shots` must pass.
2. Animatic (stage 8 step 4), then show it to the user.
3. Build the compositions, then Director review (job C), then the draft for the user's approval.

Open items: no pronunciation hints yet (the user has not listened to the audio);
`kit.py delegate` does not protect `video/review.md` or `render-approval.json`.

## Where things stood at the start (2026-11-18)

- Stages 1-7 of the kit are built and verified. `python3 kit.py self-test`
  passes (92 checks).
- Sample run `runs/2026-11-18-history-of-the-printing-press/` is COMPLETE:
  - `script.md` v3, approved: 9 scenes, 1,440 words, ~9.6 min, hook H5.
  - `assets.md` + `assets/`: 12 licensed files (PD / CC0 / CC BY-SA 2.0),
    remapped to the 9 scenes. File names (s01-s11) are download names and do
    not match scene numbers.
  - `sources.md`: bibliography and YouTube description (4,111 characters).
- The final code review of the whole kit is deferred to the very end (user's
  decision). Not yet independently reviewed: the hook lab (`kit.py hooks`),
  the delegate fallback chain, the retention warnings.

## Decisions already made by the user

| Topic | Decision |
|---|---|
| Voiceover | Free, local text-to-speech (candidates: Kokoro, Piper). No paid APIs. |
| Render engine | HyperFrames (HTML + GSAP), recommended over Remotion. |
| Visual style | The user's `vox-editorial-style.zip` (kit root). |
| Approval | A draft render is shown to the user before the final render. |
| Format | 16:9 long-form, 1920x1080. Shorts not requested. |

Reasons for HyperFrames: the style kit's HyperFrames template already passes
`npx hyperframes check` with 0 errors and 0 warnings; scenes are plain HTML,
easy to generate from script.md; Remotion needs a paid company licence above
a small team size and the user produces for a company.

## Open checks (do these first, in the plan)

1. **HyperFrames licence** for company use. Not verified yet.
2. **Toolchain:** `node`, `npx`, `ffmpeg` present? HyperFrames CLI version
   (the style kit was validated with 0.9.58).
3. **TTS:** install route and voice quality for Kokoro vs Piper; ask the user
   before installing anything.
4. **Word timestamps:** the style types titles word by word on the voiceover.
   Get timings from the TTS engine if it provides them; otherwise align with a
   local Whisper model.
5. **Style kit location:** extract the zip into the kit (for example
   `skills/vox-editorial-style/`). It is the user's own file, but read its JS
   (`assets/core/editorial-core.js`, `selfcheck.mjs`, `scripts/make-sfx.sh`)
   before running it. The bundled `.wav` files were not played.

## Inputs the production phase consumes (contract)

| From | Use |
|---|---|
| `script.md` narration lines, tags stripped with `\s*\[(?:C\d+|NF)\]` | Voiceover text, one sentence per line |
| `## Scene <n>: <title>` | Scene boundaries / compositions |
| `> VISUAL [ARCHIVAL/MAP/TIMELINE/DIAGRAM/DETAIL/RECONSTRUCTION/B-ROLL]: ...` | Shot list |
| `> TEXT: ...` | On-screen type-on labels, highlighter beats |
| `> SOUND: ...` | SFX / music cues |
| `assets.md` + `assets/` | Images per scene, with licence and attribution |
| `sources.md` | Description and on-screen credits |
| `approval.json` | Refuse to render if `kit.py status <run>` is not COMPLETE |

Never change approved narration in this phase. A wording change goes back
through stage 5 (approval).

## Style mapping (vox-editorial-style)

- Family **B, analog collage** for `ARCHIVAL` shots: textured paper, B&W
  images with a keyline, held 0.7-2 s, tape, newspaper clippings, grain and
  vignette.
- Family **A, flat editorial** for `MAP`, `TIMELINE`, `DIAGRAM`: flat paper,
  vector map of the spread from Mainz, the hand-mould + press system.
- Rules that matter most: graphics animate on twos (12/s); one yellow
  highlight per beat; text types on, never flies in; hard cut by default;
  no overshoot or bounce.
- **Do not transfer** anything from the reference videos: no Vox name, logo,
  stings, scripts, footage, music or exact shot sequences. Do not market the
  output as Vox.
- `RECONSTRUCTION` visuals must be labelled on screen; never pass them off as
  original.

## Suggested phase shape (to confirm in /plan)

1. `stages/08-production.md` prompt (replaces the 08 hook) plus small
   `kit.py` helpers: export narration text per scene, check the render inputs.
2. Voiceover per scene + word timestamps, saved in the run folder.
3. HyperFrames project per run (for example `runs/<run>/video/`): one
   composition per scene, assets from `assets/`, SFX from the style kit.
4. Draft render, then the user's approval, then the final render.
5. Credits card from `assets.md` attributions (CC BY-SA requires them).

## Working conventions from this session

- `/plan` each phase; wait for the user's confirmation before building.
- Script writing (stage 3) is delegated to `agy` with
  `--model gemini-4-hydrogen-high,claude-opus-5-5-high`; research to OpenCode
  (`opencode-go/minimax-m3.1-flash` for this user). Claude reviews delegated output.
- Wikimedia rate-limits downloads (HTTP 429); `fetch-assets` retries, but
  waits can take minutes.
- Do not write to agent memory for this project (user's instruction).
