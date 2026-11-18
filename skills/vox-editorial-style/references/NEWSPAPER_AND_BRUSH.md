# Newspaper, Dry Brush, Letterpress, Halftone

This is the framework-neutral spec. Code exists in two forms:

- **Remotion:** `templates/style-system/newspaper.tsx` and `NewspaperDemo.tsx` (validated by rendered frames).
- **Raw SVG/JS:** `assets/core/editorial-core.js` (`brushFilter`, `letterpressFilter`, `halftoneFilter`, `tornClipPath`, `BRUSH_PATH`).

Evidence:
- V4 "The Highlight": the headline card, f65–151 @10 fps.
- V1: the newspaper headline burst, f2275–2361 @30 fps.

## 1. Dry-brush highlight

| Property | Value | Source |
|---|---|---|
| Colour | `#F8E10F`, multiply over paper (stays saturated on newsprint) | V4 ochre `#BE933B` is the multiplied result |
| Shape | slightly up-slanted body with bulged ends: `BRUSH_PATH` in a 1000×100 viewBox stretched over the phrase (`preserveAspectRatio="none"`); covers about −0.18 em to +0.22 em horizontally | V4 #3 "slight upward slant" |
| Texture | horizontal bristle gaps = fractal noise with `baseFrequency 0.0025 0.16`, alpha = 6·R − 1.75; ragged edges = displacement (scale 30) by noise with `baseFrequency 0.03 0.12` | — |
| Reveal | clip rect width 0→100 % of the stroke. The filter sits **outside** the clip, so the leading edge is ragged too | — |
| Timing | **10 f @24, `accel` (ease-in), hard stop** (V4 swipe #2: +164/+273/+382 px per frame). Linear variant 8–9 f for body text (V4 #3: ~1180 px/s) | V4 |
| Pairing | snap zoom ×1.22 in 4 f (`accel`) as the stroke starts; snap back 1/1.22 in 4 f before the next move | V4 f7–8, f31–32 |
| Life during holds | reseed the edge-wobble noise A-A-B (`boilSeed`) so held strokes shimmer | V4 boil |
| Erase (optional) | erosion: animate the bristle alpha offset down over 14 f (ease-in), not a wipe | V4 f40–54 |

## 2. Newspaper clipping

| Element | Spec |
|---|---|
| Stock | `#E7E0CF` newsprint; fibre noise (`baseFrequency 0.6 0.05`, multiply, 35 %); foxing radial gradient to `rgba(150,110,40,.22)` at the edges |
| Edge | torn `clip-path` polygon: 16 px steps, 0–7 px deterministic jitter (`tornClipPath(w,h,seed)`) |
| Shadow | `drop-shadow(6px 8px 14px rgba(0,0,0,.4))` on the **parent**, because clip-path cuts a box-shadow |
| Placement | rotate −1° to ±2°; on an aged-paper ground `#C4BDB2` with paper texture, 13 % vignette and grain 0.15 |
| Date tag | maroon `#7D3130` box, cream serif 28 px; appears at f14 and snaps up 28 px in 2 drawings (f16–20) |
| Masthead | blackletter (UnifrakturMaguntia) 76 px, centred |
| Rules | 4 px + 1 px double rule; draws from the centre outward (scaleX 0→1 over 8 f, the second 2 f later) |
| Headline | heavy serif caps 92 px, line height 1.02; **letterpress ink-in** over 8 f (reveal 0→1) |
| Byline | serif italic 26 px |
| Body | 3 columns (1 : 1 : 1.15), gap 34, serif 22/1.38, justified; inks in after the camera pan |
| Photo | halftone screen (§4), with an italic 18 px caption |
| Camera | pan up 330 px in 8 f (`accel`, hard stop) to reveal the body (V4: −207 px in 3 drawings) |

## 3. Letterpress ink

| Parameter | Value |
|---|---|
| Edge roughness | displacement scale 2.4 by fine noise (`baseFrequency 0.8`) |
| Speckle holes | noise `baseFrequency 0.22`; alpha = −5·A + (4.4 − (1 − reveal)·4.2) |
| Ink-in | `reveal` 0→1 over 8 f (4 drawings). Fragments grow into full letters (V4 f1–4, f65–68) |
| Boil | noise seed A-A-B per drawing (V4 3.3 Hz) |

Earlier calibration: a hole offset of 3.4 looked like rust on bold type. 4.4 is the validated value.

## 4. Halftone photo

- **Method:** a tiled radial-gradient screen (`cell` = 7 px), arithmetic `L + screen − 0.5`, then a discrete threshold, then colourised to ink with paper transparent, multiplied. Dot size follows darkness.
- **Input:** any image or SVG drawing. In HyperFrames or Remotion, wrap the `<image>` in the filtered `<g>`.
- **Real photos:** use licensed or original ones. The demo uses an SVG skyline placeholder.

## 5. Headline burst (montage)

| Parameter | Value |
|---|---|
| Cuts | 8 hard cuts: 10, 8, 8, 6, 6, 6, 8, then a 44 f hold (@24) (V1: 5–15 f @30) |
| Keyword lock | the keyword sits in a 3-column grid `minmax(0,1fr) auto minmax(0,1fr)` whose middle column is centred on x = 960. **Measured:** keyword centre x 955–970 across cuts |
| Variety | change the face per cut (heavy serif, serif italic, Oswald condensed, Inter bold), size 104–150 px, rotation ±2°, and the filler column offset |
| Brush | already present on quick cuts; on the held last cut the brush swipes in at +8 f |
| Frame | clipping larger than the frame (2200×1400 at −140, −160), vignette 0.3, grain 0.2 |
| Sound | one paper slap per cut (volume 0.55–0.75, rate 0.9–1.15, deterministic random), then a brush swish on the held cut |
| End | linear fade to black over 20 f |

## 6. Placeholder copy

All mastheads, headlines and body text in the templates are invented ("The Daily Placeholder", filler sentences about surveys and maps). Replace them with the new video's own copy. Never paste real newspaper articles verbatim; set a real headline only when it is quoted as evidence and properly attributed.
