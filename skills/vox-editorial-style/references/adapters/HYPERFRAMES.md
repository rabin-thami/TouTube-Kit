# Adapter: HyperFrames (HTML + GSAP)

**Validated with:** HyperFrames CLI 0.9.58.

- `templates/hyperframes/` passes `npx hyperframes check --json` with 0 errors and 0 warnings across lint, runtime, layout, motion, contrast, craft and audio.
- Snapshots at 2.6 s and 5.6 s show the torn clipping, letterpress headline, dry brush, snap zoom, pan and second brush.

**Load also:** the `hyperframes` skill. Its contract wins on mechanics: `class="clip"`, `data-start`/`data-duration` in seconds, one paused timeline per scene registered in `window.__timelines`, `fromTo` not `from`, no unseeded random, and fonts.

## Setup

1. Copy `templates/hyperframes/` as a new project, or merge `compositions/front.html` into an existing one. It contains:
   - `index.html`: root, scene host and SFX cue sheet;
   - `compositions/front.html`: the scene;
   - `assets/sfx/`: the six SFX.
2. Run `npx hyperframes check --json`, then `npx hyperframes preview`.

## Translating the system

| Style rule | HyperFrames implementation |
|---|---|
| Tokens | read `assets/tokens.json` values into CSS custom properties or literals |
| On twos (R1) | `ease: onTwos(easeFn, duration)`. GSAP accepts a function ease, so the tween only changes 12×/s. Use it on every graphic tween; never on `<video>` |
| Bezier eases | `cubicBezier(...)` from `assets/core/editorial-core.js` (inlined in the scene script; the template shows the subset). Built-in GSAP approximations if you must: `pop`≈`power2.out`, `expo`≈`expo.out`, `grow`≈`power4.out`, `push`≈`power3.inOut`, `accel`≈`power3.in` |
| Brush | SVG `<filter>` from `brushFilter()` plus a `<clipPath><rect>`; tween `attr: {width: 0→1120}` with `onTwos(accel, 0.42)` |
| Letterpress ink-in | `filter: url(#ink)` on the text; tween the speckle `feColorMatrix` `attr: {values}` alpha offset 0.2→4.4 |
| Torn clipping | at init, `el.style.clipPath = tornClipPath(w, h, seed)`. It is deterministic (seeded) |
| Halftone | SVG `<g filter>` from `halftoneFilter(id, w, h)` around an `<image>` |
| Grain (screen-locked, 12/s) | a 512 px SVG-noise tile as `background-image`; tween `backgroundPosition` over the whole scene with `ease: "steps(D*12)"`. Each step jumps the tile, so the grain looks fresh, with no reseeding and no timers |
| Vignette | static radial-gradient div, multiply |
| Camera moves | one `#camera` wrapper; tween `scale`, `x`, `y` (never `left`/`top`) |
| Transitions | hard cut = scene host boundaries. For a zoom-through, tween the outgoing scene `scale` 1→1.29 (`accel`, 1.0 s) to its end and the incoming 1.82→1 (`punch`, 1.17 s) from its start |
| SFX | `<audio id class="clip" data-start data-duration data-volume src="assets/sfx/…">` in the root; times = frames@24 ÷ 24 (cue sheet in [SOUND_DESIGN](../SOUND_DESIGN.md)) |
| Fonts | bundled stand-ins: **Playfair Display** (headline/masthead), **EB Garamond** (body), **Inter** (data), **Oswald** (tabloid). For the measured look, ship Source Serif 4, Permanent Marker and UnifrakturMaguntia `.woff2` (OFL) in `assets/fonts/` with `@font-face` |

## Things the HyperFrames lint will catch

- **A root without the GSAP script.** Add `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js">` in `<head>`. Without it, the timeline never registers.
- **A clipping taller than the frame.** Mark the scene root `data-layout-allow-overflow`; the camera pans to it on purpose.
- **Small newspaper body type** (22 px) can trigger `text_below_floor`. It is texture, not reading copy. Keep the headline and the brushed phrase large.

## Conflicts with generic HyperFrames motion advice

The `hyperframes` skill suggests motion blur on fast moves and smooth 30 fps tweens. **This style overrides that:**

- graphics step at 12/s;
- no motion blur, except a map zoom over ×10;
- arrivals never overshoot.
