# Stage 8 — Production (voiceover + render)

Turns a COMPLETE run into `video/final.mp4` (16:9, 1920x1080). Work only in
`<run>/video/`. **Never change approved narration**: a wording change goes back
through stage 5 (approval), then `kit.py export` again.

Style: `skills/vox-editorial-style/SKILL.md` and its
`references/adapters/HYPERFRAMES.md`. Mechanics: the `hyperframes` skill.
HyperFrames CLI pinned to **0.9.67**; prefix every call with
`HYPERFRAMES_NO_TELEMETRY=1` and use `npx -y hyperframes@0.9.67 ...`.

## Steps

1. **Export.** `python3 kit.py export <run>` writes `video/plan.json`: per
   scene, the `beats` in script order (`VISUAL`/`TEXT`/`SOUND`/`NOTE` notes and
   `line` narration with tags stripped), the scene's assets, and all credits.
   It refuses if `kit.py status` is not COMPLETE.

2. **Voiceover.** Per scene, write `video/audio/sNN.wav` and
   `video/audio/sNN.words.json`:
   `{"lines": [narration lines, exactly as in plan.json], "words": [{"w", "s", "e"}]}`
   (`s`/`e` = seconds from the start of that scene's wav).
   Engine: Windows TTS or Kokoro (`am_michael`) while developing; Google Cloud
   TTS (key in `GOOGLE_TTS_API_KEY`, never written to a file) for the draft and
   final. Pronunciation hints may change the TTS *input* only, never `lines`.
   Scene duration = its wav length.
   Command (writes the audio, then `video/captions.srt` once every scene has audio):
   `.venv-tts/bin/python -I tools/voice.py <run> --engine kokoro [--voice am_michael] [--scenes 1,3]`
   (`--engine windows` for Windows TTS; `--self-test` checks the caption maths).
   Setup once: `uv venv --python 3.12 .venv-tts`, then install `torch` (CPU
   index), `kokoro`, `soundfile` and spaCy `en_core_web_sm`; needs `espeak-ng`.

3. **Shot list (Director).** Call the `director` agent
   (`.claude/agents/director.md`; any other agent CLI: give it that file as its
   prompt) for job A. It writes `video/shots.md` from `plan.json`, the word
   timings and the assets, following `references/motion-direction-handbook.md`
   and the style kit. Check: `python3 kit.py shots <run>`.

4. **Animatic.** Build each scene as still frames per shot (no animation yet),
   timed to the voice; the Director reviews them (job B). Show the user the
   animatic render and its snapshot sheet; ask for changes before animating.
   Command: `python3 tools/animatic.py <run>` writes `video/animatic/frames/<shot>.png`
   (one still per shot, with its direction notes), `video/animatic/sheet.png` and
   `video/animatic.mp4`. A shot starts at the first word of its first line.

5. **Compositions (Builder).** One HyperFrames project in `video/` (from
   `skills/vox-editorial-style/templates/hyperframes/`), built from `shots.md`:
   - `video/compositions/sNN.html` per scene, shots timed to the words;
   - `video/compositions/credits.html` with every attribution from
     `plan.json` `credits` (CC BY-SA requires them);
   - images only as `../assets/<file>` from `assets.md`;
   - `ARCHIVAL` → family B (analog collage); `MAP`/`TIMELINE`/`DIAGRAM` →
     family A (flat editorial); `RECONSTRUCTION` must show the word
     "Reconstruction" on screen;
   - `TEXT` notes type on with the voice; `SOUND` notes → style-kit SFX.
   - Never copy from the reference videos: no Vox name, logo, stings, music,
     footage or exact shot sequences.
   Check: `npx hyperframes check --json` (0 errors, 0 warnings).

6. **Director review.** Call the `director` agent for job C on each built
   scene. It records `PASS` or `NOTES` with `kit.py review`; the Builder fixes
   every note and asks again. The Builder never records a review. A PASS is
   tied to the scene's hash, so any later edit needs a new review. Check:
   `python3 kit.py check-render <run>`.

7. **Draft.** Render `video/draft.mp4` with `--quality draft`. Show it to the
   user. **Hard stop**: only when the user replies "approved", run
   `python3 kit.py approve-draft <run> --message "<user's reply>"`. Any other
   reply means fix and render a new draft (a new draft voids the approval).

8. **Final.** `python3 kit.py check-render <run> --final` must pass. Render
   with `--quality delivery`, normalise loudness to about -14 LUFS, save as
   `video/final.mp4`. `kit.py status <run>` then says "final rendered".

`video/captions.srt` (from `tools/voice.py`) is for upload, not burned in.
Thumbnails and upload stay out of scope.
