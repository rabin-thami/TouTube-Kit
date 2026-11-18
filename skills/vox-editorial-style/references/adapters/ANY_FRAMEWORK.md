# Adapter: any framework (and future ones)

The style is defined by data and math, not by a library.

## What every framework needs

| Capability | Why | If missing |
|---|---|---|
| Time-driven, deterministic rendering (frame or time → picture) | stepped motion, seeded textures, frame-exact cuts | render via a headless browser or image sequence |
| Custom easing function | fitted bezier curves | port `cubicBezier()` (≈30 lines, pure math) |
| Layer stack with blend modes (multiply, overlay) | highlighter, vignette, grain, halftone ink | pre-composite in code, or bake textures to PNG |
| Clip/mask by shape | torn paper, brush reveal, loupe | use alpha mattes |
| Noise source (SVG `feTurbulence`, shader or noise PNG) | grain, brush bristles, letterpress | ship PNG noise tiles (12 variants for 12 fps grain) |
| Audio placed at frame times | SFX cue sheet | mux afterwards with ffmpeg `adelay` |

## Porting checklist

1. **Load `assets/tokens.json`.** Never hard-code colours or durations twice.
2. **Port `cubicBezier`, `onTwos`/`stepFrame`, `seeded`, `tornClipPath` and `tweenScale`** from `assets/core/editorial-core.js`. Then run the selfcheck values as unit tests (`assets/core/selfcheck.mjs`), for example:
   - `ease.grow(6/30) ≈ 0.5`
   - `ease.pop(0.25) ≈ 0.55`
   - `onTwos` gives 12 distinct values per second
3. **Build the layer order** from `tokens.layerOrder`. Grain and vignette sit above the camera.
4. **Implement effects** from [NEWSPAPER_AND_BRUSH](../NEWSPAPER_AND_BRUSH.md) and [MOTION_RECIPES](../MOTION_RECIPES.md). The specs are in px, frames @24 and curve names.
5. **Place SFX** from [SOUND_DESIGN](../SOUND_DESIGN.md).
6. **Verify by measuring rendered frames**, not by eye alone:
   - frame-difference cadence: graphics move on one frame parity only;
   - paper colour equals the token (±1);
   - grain std 1.1–1.6 levels (subtle) on flat paper;
   - vignette corner drop 8–15 %;
   - audio onsets within 2 f of their events.

   The measurement method is in `ANALYSIS_LIMITATIONS.md` and `evidence/`.

## Framework notes

| Framework | Notes |
|---|---|
| **Remotion** | ready-made: [REMOTION.md](REMOTION.md) |
| **HyperFrames** | ready-made: [HYPERFRAMES.md](HYPERFRAMES.md) |
| **Motion Canvas / Revideo** | generators with `yield* tween(d, v => …)`. Wrap the value with `onTwos(ease)`. Use SVG/canvas filters or noise PNGs; `Rect` clip for the brush |
| **anime.js / plain GSAP in a browser + recorder** | same as HyperFrames; seek the timeline per frame. Never record real-time playback |
| **Canvas 2D / WebGL / shaders** | brush = noise-thresholded alpha mask times a reveal rect; grain = hash noise seeded by `floor(t*12)`; halftone = `step(lum + screen, 1)` in a fragment shader |
| **After Effects** | `posterizeTime(12)` on animated layers. Easing via the keyframe velocity matching the bezier (Flow/Ease Copilot). Turbulent Displace for brush edges. Fractal Noise + Posterize Time for grain. CC Ball Action or Halftone effect for halftone |
| **Blender / 3D** | render graphic layers at 12 fps holds (Stepped Interpolation modifier); composite paper and grain in the compositor |
| **Python (MoviePy, Manim)** | port the math; Manim `rate_func=` takes `cubicBezier`; quantise `t` before evaluating |

## Keep these invariants whatever the framework

- 12 drawings/s for graphics.
- No overshoot.
- Yellow means "read this".
- Text is ink only.
- Hard cut by default, 2 f before VO phrases.
- Screen-locked grain.
- Deterministic randomness.
- Original content only.
