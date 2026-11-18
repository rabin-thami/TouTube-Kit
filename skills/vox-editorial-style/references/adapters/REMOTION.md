# Adapter: Remotion

**Validated with:** Remotion 4.0.544, Bun, `@remotion/transitions` and `@remotion/google-fonts` 4.0.544.

**Load also:** `remotion-best-practices` and `remotion-markup`. Their rules on frame-driven animation, inline `interpolate()`, `scale`/`translate` style props and `staticFile()` apply.

## Setup

1. Copy `templates/style-system/` into the project as `src/style-system/`.
2. Install `@remotion/transitions` and `@remotion/google-fonts` at the project's Remotion version, for example `bunx remotion add @remotion/google-fonts @remotion/transitions`. Ask before installing.
3. Copy `assets/sfx/*.wav` to `public/sfx/`, or run `scripts/make-sfx.sh` from the project root; it writes `public/sfx/`.
4. Register the demos in `src/Root.tsx` to check the setup:
   - `StyleCalibration`: title, zoom-through, chart, collage, 15.3 s.
   - `NewspaperDemo`: front page and headline burst, with SFX, 10.3 s.
5. Run `bun run dev` to preview in Studio.

## What each file gives you

| File | Exports |
|---|---|
| `tokens.ts` | `color`, `shadow`, `ease` (pop, expo, grow, punch, push, tilt, pan, accel, wipe), `STEP`, `stepped(frame)`, `clamp` |
| `fonts.ts` | `serif` (Source Serif 4), `sans` (Inter), `marker`, `blackletter`, `condensed` (Oswald) |
| `texture.tsx` | `<Grain amount>`, `<PaperTexture>`, `<Vignette strength>`, `<GridPatch corner>` |
| `motion.tsx` | `<TypeOn>`, `<Highlight>`, `<PopIn>`, `<MarkerEllipse>` |
| `newspaper.tsx` | `<BrushStroke>`, `<BrushHighlight>`, `<Letterpress reveal>`, `<Halftone>`, `<NewsClipping>`, `tornClipPath`, `boilSeed`, `fillerText` |
| `zoomThrough.tsx` | `zoomThrough(52)` presentation for `<TransitionSeries.Transition>` |

## Core patterns

```tsx
const f = stepped(useCurrentFrame());                       // R1 on twos
width: interpolate(f, [s, s + 30], [0, max], {...clamp, easing: ease.grow})   // bars
<BrushHighlight start={40} duration={10}>KEY PHRASE</BrushHighlight>         // dry brush
<Sequence from={40} layout="none"><Audio src={staticFile("sfx/brush-swish.wav")} volume={0.9} /></Sequence>
```

- Put `<Vignette>` and `<Grain>` outside the camera layer.
- Start the incoming scene's animations about 40 f in when using `zoomThrough(52)`.

## Calibration results (measured from rendered frames)

| Check | Result |
|---|---|
| On-twos cadence | 100 % single parity |
| Paper colour | exact |
| Grain | 1.06 levels at `amount 0.2` |
| Vignette | 13.4 % |
| Burst keyword lock | x 955–970 |
| SFX onsets | within 0–2 f of their cues |

Full table: [REMOTION_IMPLEMENTATION_GUIDE](../REMOTION_IMPLEMENTATION_GUIDE.md) §5.

**Audio component:** the templates use core `remotion` `Audio`, so no extra dependency is needed. `@remotion/media`'s `<Audio>` is the newer option, available after `bunx remotion add @remotion/media`.
