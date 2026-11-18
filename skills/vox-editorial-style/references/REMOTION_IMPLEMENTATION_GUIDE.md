# Remotion Implementation Guide

This guide turns the style system into Remotion code. It targets **Remotion 4.0.544**, with `@remotion/transitions` and `@remotion/google-fonts` 4.0.544 (added for this work) and Bun as the package manager. The working code is in `templates/style-system/ (copied into the project as src/style-system/)`.

Before you write new scenes, load the official skills `remotion-best-practices` and `remotion-markup`. Their rules, summarised:

- Drive all animation from `useCurrentFrame()` with `interpolate()` / `Easing`. Never use CSS transitions.
- Use the `scale`, `translate` and `rotate` style properties rather than `transform` strings.
- Keep `useCurrentFrame()` in the smallest component that needs it.
- Use `staticFile()` for assets in `public/`.

## 1. Architecture

```
templates/style-system/ (copied into the project as src/style-system/)
  tokens.ts          colour, shadow, ease{} library, STEP, stepped(), clamp
  fonts.ts           loadFont(): Source Serif 4 (400/600/700/900 + italic), Inter, Permanent Marker
  texture.tsx        <Grain amount/> <PaperTexture amount/> <Vignette strength/> <GridPatch corner pitch/>
  motion.tsx         <TypeOn/> <Highlight/> <PopIn/> <MarkerEllipse/>
  zoomThrough.tsx    zoomThrough(duration, {split,outScale,inScale}) → TransitionPresentation
  StyleCalibration.tsx  3-scene calibration composition (id "StyleCalibration", 1920×1080, 24 fps, 368 f)
```

Suggested additions as the library grows. Each comes from a recipe in [MOTION_RECIPES](MOTION_RECIPES.md).

| Component | Recipe | Props |
|---|---|---|
| `<Camera>` | M8–M10, M14 | `keys: {frame, scale, x, y, easing}[]`, `origin`; wraps scene content; steps on twos |
| `<CardTitle>` | M1 | `text`, `price`, `start`, `framesPerChar` |
| `<BarChart>` | M6 | `data[]`, `start`, `stagger=8`, `duration=30`, `max`, `orientation` |
| `<HighlightLines>` | M3 | `lines[]`, `starts[]`, `easing=ease.wipe` |
| `<LowerThird>` | M19 | `name`, `role`, `start` |
| `<Magnifier>` | M11, T4 | `children` (magnified layer), `path`, `radius=317`, `zoom` |
| `<Counter>` | M15 | `from`, `to`, `start`, `steps=11` |
| `<FootageCard>` | M13 | `src` (`@remotion/media` `<Video>`), `caption` |
| `<ArchivalPhoto>` | §6 colour | `src`, `border`, `grade` (`grayscale(1) sepia(.08)`), `shadow` |
| `loupeReveal()` | T4 | presentation with `clip-path: circle()` |

**Scene architecture:** one component per scene, sequenced with `<TransitionSeries>`. Use hard cuts (adjacent `TransitionSeries.Sequence`, no transition between them) by default and `TransitionSeries.Transition` only for the signature transitions. Keep timing constants at the top of the file and convert seconds with `fps` from `useVideoConfig()` when a scene is authored in seconds.

## 2. Core patterns

### On-twos animation (R1)

```tsx
const f = stepped(useCurrentFrame()); // floor(frame/2)*2
const w = interpolate(f, [start, start + 30], [0, max], {...clamp, easing: ease.grow});
```

Do **not** step live footage (`<Video>`) or opacity fades to black.

### Word-synced type (R8)

Store narration word times (from a transcript, e.g. `@remotion/captions`) and reveal words by frame:

```tsx
{words.map(([w, at]) => <span key={w} style={{opacity: f >= at ? 1 : 0}}>{w} </span>)}
```

### Punch-in with creep (M8)

```tsx
scale:
  (1 + 0.0013 * Math.min(f, 60)) *
  interpolate(f, [60, 76], [1, 1.3], {...clamp, easing: ease.punch}) *
  (1 + 0.001 * Math.max(0, f - 76)),
```

### Highlighter (M3)

```tsx
<Highlight start={60} duration={12} fill={color.highlightPure}>GUESS</Highlight>
```

The block is absolutely positioned behind the text with width `calc((100% + .24em) * p)` and `mix-blend-mode: multiply`.

### Zoom-through transition (T2)

```tsx
<TransitionSeries.Transition
  presentation={zoomThrough(52)}            // 24 f ease-in ×1.29 → cut → 28 f ease-out ×1.82→1
  timing={linearTiming({durationInFrames: 52})}
/>
```

The transition overlaps both scenes by 52 frames. Start the incoming scene's own animations after about frame 40 so they are visible once it has landed.

### Textured ground (family B)

```tsx
<AbsoluteFill style={{background: color.paperCollage}} />
<PaperTexture />                   {/* static multiply mottling */}
… content …
<Vignette strength={0.12} />       {/* measured 13.4 % corner drop */}
<Grain amount={0.2} />             {/* measured 1.06 levels std, 12 fps */}
```

Put `Vignette` and `Grain` **outside** the camera layer so they don't scale with pushes; the references' grain stays screen-locked.

## 3. Configurable parameters

| Parameter | Default | Range from references |
|---|---|---|
| `STEP` | 2 @24 fps | 2 (12 fps), 3 (8–10 fps), 6 @60 (10 fps) |
| Grain `amount` | 0.2 | 0 (flat) – about 0.9 (V6 strength, extrapolated, untested) |
| Vignette `strength` | 0.12 | 0 – 0.15 |
| Bar duration / stagger | 30 / 8 f | 20–30 / 5–10 f |
| Highlight duration | 12 f | 9–34 f |
| Pop duration | 18 f | 7–24 f |
| Push scale / frames | 1.18 / 22 | 1.18–1.8 / 22–76 |
| Zoom-through split / out / in | 24/52, 1.29, 1.82 | — |

## 4. Performance

- **SVG grain** (`feTurbulence` full-frame) costs the most per frame, but it renders only 12 distinct seeds per second. Measured: 368 frames rendered to PNG in under 2 min locally. Studio plays the composition at about 24.7 fps.
- For long videos, pre-render a 2 s grain loop (24 PNGs) to `public/` and play it with `<Loop>` + `<Img>`. The result is identical to the SVG grain and cheaper.
- `PaperTexture` is static and cheap (one filter). If several scenes share it, render it once to a PNG.
- Keep `mix-blend-mode` layers few: about 3 per frame here.
- The calibration's `Composition` uses default JPEG frames (`remotion.config.ts`), which is fine for grain. Use `--image-format=png` for QA measurement.

## 5. Calibration composition — what was validated

`StyleCalibration` (15.3 s, 1920×1080, 24 fps) uses only placeholder copy and data:

| Scene | Frames | Techniques |
|---|---|---|
| Title card | 0–149 | Flat paper `#F6F5EA` + grid patch; Source Serif 4 900 caps in a 10 px ruled box; words revealed at fixed frames (VO stand-in); `Highlight` box on the key word; slow creep → ×1.3 punch (16 f) → creep |
| Zoom-through | 98–149 (52 f overlap) | T2 transition |
| Chart | 98–247 | Serif title + Inter subtitle typed at 1 char/f; 5 bars quart-out 30 f, stagger 8 f; highlighter on one label; marker ellipse draw-on 12 f; marker annotation |
| Collage | 248–367 | Textured paper, vignette, 12 fps grain; tilt-push ×1.18 over 22 f; linear pull-out; shadowed white-border card; tape label expo-out slide with rotation settle; underline draw-on; chromatic fringe on the header; 29 f linear fade to black |

**Verification:**

- The full 368-frame PNG sequence was rendered and measured with the same frame-difference script used on the references.
- Representative frames were viewed and compared side by side with a V3 title frame.
- Studio was opened at `localhost:3123/StyleCalibration` and the composition played back with no console errors.

### Results

| Check | Reference target | Calibration result | Verdict |
|---|---|---|---|
| On-twos cadence | 100 % single-parity motion (V3 D0) | 46/46, 26/26 and 44/44 moving frames on a single parity in the three scenes [Measured] | **Matches** |
| Flat paper colour | `#F6F5EA` | `#F6F5EA` rendered (246,245,234) | **Matches** |
| Grain amplitude | 1.1–1.6 levels (V1 subtle) | 0.71 at `amount 0.1` → **1.06 at `amount 0.2`** [Measured] | **Matches** low end; use 0.25–0.3 for mid-V1 |
| Vignette | 8–15 % corner drop (V1/V4) | 13.4 % (centre 223 → corners about 193) [Measured] | **Matches** |
| Title layout | V3: boxed caps, cap 93 px after punch | First render orphaned "A" and overflowed after the punch. Fixed: explicit line breaks, box 1000 px border-box, font 118, line height 0.98. Cap after punch ≈ 111 px (19 % larger than V3) | **Adjusted**; reduce font to about 100 px for an exact cap match |
| Bar easing / stagger | quart-out 30 f / 8 f | implemented as specified; visually reads like V3 strips | **Matches** (not curve-fitted back) |
| Zoom-through | ×1.29 EI → cut → ×1.82 EO | implemented; title overshoots the frame edges during the ease-in, as in V6 | **Matches** qualitatively |
| Grid patch | dashed hairlines with "+" ticks, 48 px | solid hairlines, 48 px | **Does not match**: needs a dashed SVG pattern |
| Marker ellipse | rough double loop | double loop drawn at a constant stroke width | **Partial**: add `feTurbulence` displacement for a wobbly edge |
| Archival photo | real B&W photo with halftone or engraving | gradient placeholder | **Needs assets** |

**Values that need adjustment:**

- Grain `amount` per family: V1 0.25, V6 about 0.9 (extrapolated; measure before use).
- Title font about 100 px.

**Still to investigate:**

- Radial zoom-blur (`@remotion/effects` `zoomBlur`).
- Loupe reveal.
- Map zooms with real geodata (`remotion-maps` skill).
- Hand-drawn stroke wobble.

## 5b. Sound effects (NewspaperDemo)

- **Assets:** `bash scripts/make-sfx.sh` synthesises six original SFX into `public/sfx/` and peak-normalises each to -3 dBFS:
  - `paper-rustle`, `stamp-thunk` and `paper-slap`;
  - `brush-swish`, which rises with an accelerating curve and stops hard, like the ease-in brush;
  - `whoosh-snap` and `whoosh-pan`.
- **Cues:** a `CUES` array of `{at, sfx, volume, rate}`, each rendered as `<Sequence from={at} layout="none"><Audio src={staticFile(...)} /></Sequence>`.
  - Whooshes start with their move, because they peak at the end.
  - Repeated slaps vary volume and `playbackRate` through `random()` (deterministic), so repeats don't sound identical.
- **Checked:** the rendered WAV has onsets at the cue frames (±2 f).
  - Integrated loudness is -24.5 LUFS and peak is -6.9 dBFS for SFX only.
  - With VO, keep SFX about 6–10 dB under the voice and master the mix to -18/-19 LUFS (STYLE_BIBLE §10).
- **Audio component:** core `remotion` `Audio` is used, because `@remotion/media` is not a declared dependency. Switch to `@remotion/media` after `bunx remotion add @remotion/media` if you want the newer component.

## 6. Workflow for a new video

1. Write the script and record or synthesise the VO. Get word timestamps.
2. Choose a family (A or B) per chapter ([STYLE_BIBLE §2](STYLE_BIBLE.md)).
3. Storyboard each narration beat as **one idea, one move, then a hold**. Pick a recipe (M#) and a transition (T#) from [MOTION_RECIPES](MOTION_RECIPES.md).
4. Build scenes from `templates/style-system/ (copied into the project as src/style-system/)` components. Place cuts 2 frames before phrase starts (R13).
5. Preview in Studio (`bun run dev`). Spot-check with `bunx remotion still <id> out.png --frame=N`. Run `python3 -P` cadence and colour checks if you change tokens.
6. Mix at -18 to -19 LUFS, with the music bed 15–23 dB under the VO ([STYLE_BIBLE §10](STYLE_BIBLE.md)).
