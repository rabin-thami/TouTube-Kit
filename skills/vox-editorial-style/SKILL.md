---
name: vox-editorial-style
description: Make original explainer and documentary videos in the "editorial paper" Vox-like style (paper grounds, highlighter yellow, serif titles, on-twos stepped motion, newspaper clippings, dry-brush highlights, halftone photos, paper SFX), in any framework (Remotion, HyperFrames, or any HTML/JS/canvas renderer). Use when asked for a Vox-style, explainer, editorial, newspaper, collage or documentary video, or to reuse this style on a new topic. It holds measured tokens, motion recipes, framework adapters, reusable code, SFX and the reference evidence.
---

# Vox Editorial Style

This is a production system extracted frame by frame from 6 reference videos (22,893 frames measured, 14:55 of footage). Use it to make **new, original** videos that share the references' visual language.

- **Analysis evidence:** `references/evidence/`.
- **Source list:** `references/SOURCES.md`.
- **Never copy** the references' scripts, artwork, logos, footage or music (see "Do not transfer").

## 0. Pick the adapter first

| You are using | Read | Reuse |
|---|---|---|
| **Remotion** (React) | `references/adapters/REMOTION.md` | copy `templates/style-system/` into `src/style-system/` |
| **HyperFrames** (HTML + GSAP) | `references/adapters/HYPERFRAMES.md` | `assets/core/editorial-core.js`, `assets/tokens.json` |
| **Anything else** (Motion Canvas, anime.js, canvas, After Effects, Blender, a future framework) | `references/adapters/ANY_FRAMEWORK.md` | `assets/tokens.json` + the math in `assets/core/editorial-core.js` |

`assets/tokens.json` is the single source of truth for colours, type, easing, durations, texture, shadows, pacing and sound. `assets/core/editorial-core.js` is dependency-free JS for easing, stepped time, seeded randomness, torn edges and the SVG filters. Check it with `node assets/core/selfcheck.mjs`.

If the framework has its own skill (for example `remotion-best-practices` or `hyperframes`), load it too. Its render contract wins on framework mechanics; this skill wins on look and motion.

## 1. Workflow (any framework)

1. **Story first.** Write or receive the script. Get narration word timestamps, or mark planned beats.
2. **Pick a family per chapter** ([STYLE_BIBLE §2](references/STYLE_BIBLE.md)):
   - **A. Flat editorial:** `#F6F5EA` paper, no grain or vignette, vector charts, maps and icons. Use it for data and argument.
   - **B. Analog collage:** textured paper, 8–15 % vignette, 12 fps grain, shadowed photos, tape, newspaper clippings, brush. Use it for history and evidence.
3. **Storyboard one idea per beat:** one move, then a hold. Pick a recipe for each beat (M1–M20) and a transition (T1–T11) from [MOTION_RECIPES](references/MOTION_RECIPES.md). Check assets with [CODE_RECREATION_MATRIX](references/CODE_RECREATION_MATRIX.md).
4. **Build** with the adapter, following the rules below.
5. **Sound:** cue SFX on visible actions ([SOUND_DESIGN](references/SOUND_DESIGN.md)).
6. **Verify:**
   - render stills or a frame sequence;
   - check the on-twos cadence, paper colour, grain and vignette numbers;
   - check that audio onsets land within 2 frames of their events.
7. **Render** the full video only when the person approves or asks.

## 2. Non-negotiable rules

| # | Rule | Numbers |
|---|---|---|
| R1 | **Animate graphics on twos.** They change 12×/s. Footage, and fades to black, run every frame | `stepFrame(f,2)` / `onTwos(ease, dur)` |
| R2 | **Hold still between beats** in family A. In family B, creep linearly instead | creep 0.2–0.4 % per 2 f |
| R3 | **Yellow = read this.** One yellow element per beat: a block highlighter (multiply) or a dry brush | `#F0E136` / `#F6EA00` / brush `#F8E10F` |
| R4 | **Text is ink only**, on paper or yellow. Saturated colours are fills, never text | ink `#201E18`, contrast 6–15:1 |
| R5 | **Ease by role. Never overshoot or bounce.** | arrivals `pop`/`expo`; camera `push`/`tilt`; into a cut `accel`; bars `grow` |
| R6 | **Text types on**: 1 char/f for labels, word by word on VO for titles. It never flies in | — |
| R7 | **Stagger in reading order** | icons 2 f, bars 6–8 f, tags 8–24 f |
| R8 | **Move the camera instead of cutting** while the idea stays on the same sheet | push ×1.2–1.8 over 22–76 f |
| R9 | **Hard cut is the default** | cut 2 f before the next VO phrase |
| R10 | **Draw hand annotations** after a highlight: ellipse, underline, arrow | 6–12 f |
| R11 | **Grain and vignette are screen-locked**, above the camera layer | grain 1–1.6 levels (subtle) or 4–5 (strong) |
| R12 | **Archival images:** neutral B&W, white border or keyline, held 0.7–2 s | grayscale + 5–8 % warm tint |

Full rationale and evidence: [STYLE_BIBLE §11](references/STYLE_BIBLE.md).

## 3. Signature effects (all reproducible in code)

| Effect | Spec | Where |
|---|---|---|
| Title card | Boxed heavy serif caps; words appear on the VO; linear creep +0.13 %/f, then a ×1.3 punch over 16 f (`punch`) | M8, recipes |
| Highlighter block | Wipes L→R in 9–19 f (`pop`), multiply | M3 |
| **Dry-brush highlight** | Ragged yellow stroke, bristle gaps, accelerating swipe in 10 f (`accel`), hard stop; pair it with a ×1.22 snap zoom in 4 f | [NEWSPAPER_AND_BRUSH](references/NEWSPAPER_AND_BRUSH.md) |
| **Newspaper clipping** | Torn newsprint `#E7E0CF`, blackletter masthead, double rule, maroon date tag, justified columns, letterpress ink, halftone photo, drop shadow | [NEWSPAPER_AND_BRUSH](references/NEWSPAPER_AND_BRUSH.md) |
| Headline burst | 8 hard cuts of 4–12 f; the brushed keyword lands at the same screen spot every cut | NEWSPAPER_AND_BRUSH |
| Staggered bars | Quart-out over 30 f (`grow`), stagger 8 f | M6 |
| Zoom-through | Out ×1→1.29 over 24 f (`accel`), hard switch, in ×1.82→1 over 28 f (`punch`) | T2 |
| Whip pan | −309 px in 14 f (`punch`) | T5 |
| Tape / sticky | Slides with `expo` plus a 3° rotation settle, or a slap-scale in 8 f | M4, M5 |
| Fade to black | Linear 29–58 f, not stepped | T9 |

## 4. Tokens (short form; all values in `assets/tokens.json`)

- **Paper:** flat `#F6F5EA` · warm `#E5DDC6` · collage `#F2E8DF→#DED4CE` · aged `#C4BDB2` · newsprint `#E7E0CF`. **Dark:** `#12100D`.
- **Ink:** `#201E18` · soft ink `#393733` · news ink `#3A3835`.
- **Data:** red `#FC3828` · blue `#50B7FE` · green `#62C583` · pink `#FF85C1` · purple `#BA75BB`. **Deep red:** `#8B1C1B`. **Date tag:** `#7D3130`.
- **Type stand-ins:** Source Serif 4 (voice) · Inter (data) · Permanent Marker (annotation) · UnifrakturMaguntia (masthead) · Oswald (tabloid headlines).
- **Sizes @1080p:** title 118 px / 900 · chart title 52 px / 600 at top 92 · labels 34 px sans · lower third at x 139, plate top 814.
- **Canvas:** 1920×1080, 24 fps, safe margin 90–140 px, titles centred on x = 960.
- **Easing (cubic-bezier):**

| Name | Control points |
|---|---|
| `pop` | .16,.7,.7,1 |
| `expo` | .16,1,.3,1 |
| `grow` | .25,1,.5,1 |
| `punch` | .2,.8,.3,1 |
| `push` | .7,0,.4,1 |
| `tilt` | .45,0,.55,1 |
| `pan` | .55,0,.1,1 |
| `accel` | .55,0,1,.45 |
| `wipe` | .37,0,.63,1 |

## 5. Pacing and sound

- **Pacing:**
  - Documentary montage: median shot 1.45 s.
  - Explainer: median 3.3 s, with graphic shots carrying internal beats every 2.5–7.5 s.
  - Collage: a new event every 1–2 s.
  - Interviews or footage work as about 8 s breathers every 60–120 s.
- **Mix:** master at -18 to -19 LUFS. Keep the music bed 15–23 dB under the VO. Use 1–6 designed SFX per minute, plus one per burst cut.
- **SFX:** `assets/sfx/*.wav`, original and synthesised by `scripts/make-sfx.sh`. Files: paper-rustle, stamp-thunk, brush-swish, whoosh-snap, whoosh-pan, paper-slap.

## 6. Do not transfer

Keep these original in every video:

- logos, wordmarks and series stings;
- scripts, narration, interviewees and quotes;
- specific artworks (statue on podium, car cut-outs, hemicycles as drawn, rabbit collage, DNA chalk cards);
- exact shot sequences;
- footage, music and SFX from the references.

Reuse only the abstract rules and the code in this skill. Placeholder copy in the templates (for example "The Daily Placeholder") is fictional.

## 7. File map

```
SKILL.md                     this file
assets/tokens.json           machine-readable tokens (all frameworks)
assets/core/editorial-core.js  easing, on-twos, seeded random, torn edges, SVG filters (brush, letterpress, halftone), grain
assets/core/selfcheck.mjs    node asserts against measured reference values
assets/sfx/*.wav             6 original SFX (48 kHz mono, peak -3 dBFS)
scripts/make-sfx.sh          regenerates the SFX with ffmpeg
templates/style-system/      Remotion reference implementation (tokens, fonts, texture, motion, newspaper, zoomThrough, 2 demo compositions)
references/
  STYLE_BIBLE.md             identity, families, rules R1–R14, do-not-transfer
  MOTION_RECIPES.md          M1–M20 + T1–T11 with frame counts and curves
  TYPOGRAPHY_AND_LAYOUT.md   type roles, scale, grid, layers, aspect ratios
  COLOR_AND_TEXTURE.md       measured palette, contrast, grain, vignette, shadows
  NEWSPAPER_AND_BRUSH.md     newspaper / brush / halftone / letterpress / burst specs (framework-neutral)
  SOUND_DESIGN.md            mix targets, cue rules, SFX recipes
  CODE_RECREATION_MATRIX.md  45+ techniques: code vs asset, complexity, validation status
  VIDEO_BREAKDOWNS.md        scene-by-scene of each reference
  SHOT_AND_MOTION_TIMELINE.md  frame-level index of key moves
  REMOTION_IMPLEMENTATION_GUIDE.md  Remotion architecture + calibration results
  ANALYSIS_LIMITATIONS.md    coverage, uncertainty, assumptions
  SOURCES.md                 the 6 reference videos (titles, IDs, metadata)
  adapters/                  REMOTION.md · HYPERFRAMES.md · ANY_FRAMEWORK.md
  evidence/                  per-video forensic breakdowns, audio sync, colour measurements, palette.png
```
