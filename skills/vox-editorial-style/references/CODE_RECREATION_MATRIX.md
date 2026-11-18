# Code Recreation Matrix

**Classes:**
- **CODE**: code only (React, SVG, CSS, Canvas).
- **ASSET**: needs external media.
- **HYBRID**: code motion applied to supplied media.

**Complexity:** L (low), M (medium), H (high).

**Validated** means built in `StyleCalibration` and checked by measurement or by viewing frames.

| # | Technique | Reference timestamp(s) | Visual behaviour | Method | Required assets | Remotion implementation | Cx | Validation |
|---|---|---|---|---|---|---|---|---|
| 1 | On-twos stepping | V3 throughout; V6; V1 | Graphics change every 2nd frame | CODE | — | `stepped(useCurrentFrame())` | L | **Validated**: 100 % single parity |
| 2 | Flat paper ground | V3, V2 | Flat cream, no grain or vignette | CODE | — | `AbsoluteFill` bg `#F6F5EA` | L | **Validated**: exact colour |
| 3 | Textured paper + vignette | V1 f1260, V4 f0 | Warm paper, 8–15 % corner falloff | CODE | optional paper scan | `PaperTexture` + `Vignette` | L | **Validated**: 13.4 % |
| 4 | Film grain at 12 fps | V1, V6 | Mono 1 px noise, new every 2 f | CODE | — | `Grain` (`feTurbulence`, stepped seed) | L | **Validated**: 1.06 levels at 0.2 |
| 5 | Grid-paper patch | V3 f0 | 48 px dashed grid fading from a corner | CODE | — | `GridPatch` (solid lines now) | L | Partial: dashes missing |
| 6 | Word-on title, boxed | V3 0–7 s | Words appear on VO; ruled box | CODE | VO timings | `TitleCard` | L | **Validated** |
| 7 | Punch-in + creep | V3 f72–88; V1 f5456 | ×1.3 in 16 f ease-out between linear creeps | CODE | — | multiplied `scale` factors | L | **Validated** |
| 8 | Highlighter block wipe | V1 f435–446, f858; V3 f3578 | Yellow block grows L→R behind text, multiply | CODE | — | `Highlight` | L | **Validated** |
| 9 | Brush highlighter stroke | V4 f6–14, f75–78; V1 f5426 | Ragged dry-brush stroke, accelerating swipe, hard stop | CODE | — | `BrushStroke` / `BrushHighlight` (`newspaper.tsx`): SVG path + streak-turbulence bristle gaps + displacement wobble; ragged reveal edge; wobble reseeded A-A-B | M | **Validated** (NewspaperDemo) |
| 9b | Newspaper clipping | V4 f65–151; V1 f2275–2361 | Torn newsprint, masthead, rules, columns, date tag, shadow | CODE | — | `NewsClipping` (deterministic torn `clip-path` + fibre + foxing), `Letterpress`, blackletter/Oswald fonts | M | **Validated** |
| 9c | Letterpress ink + ink-in | V4 f1–4, f65–68, f97–102 | Rough edges, ink speckle, text inks in from fragments | CODE | — | `Letterpress reveal` SVG filter (displacement + speckle alpha) | M | **Validated** |
| 9d | Halftone photo | V4 f97–102; V3 photo cards | Dot screen, dot size follows darkness | CODE (HYBRID with real photos) | photo, or SVG placeholder | `Halftone` (tiled radial screen + arithmetic threshold) | M | **Validated** on SVG placeholder |
| 9e | Headline burst | V1 f2275–2361 | 4–12 f hard cuts; brushed keyword fixed at screen centre | CODE | — | `Series` of `BurstClip`; `minmax(0,1fr) auto minmax(0,1fr)` grid locks the keyword at x = 960 | L | **Validated** (keyword centre x 955–970) |
| 10 | Title typed into a growing yellow box | V1 f1221–1243 (×11) | Box grows with typing | CODE | — | `TypeOn` inside an inline-block yellow box | L | Not built (TypeOn validated) |
| 11 | Typewriter label | V3 f2121–2160; V5 | 1 char/f | CODE | — | `TypeOn` | L | **Validated** |
| 12 | Staggered bar chart | V3 f7817–7861; V1 f3939 | Quart-out 30 f, stagger 5–8 f | CODE | data | `ChartCard` pattern | L | **Validated** |
| 13 | Line chart draw | V1 f1487–1565 | L→R draw, 6 fps steps | CODE | data | SVG path dashoffset, `stepped(f,4)` | L | Not built |
| 14 | Number counter | V1 f729–757 | 11 stepped values, in-out | CODE | — | `Math.round(interpolate(...))` on `stepped(f)` | L | Not built |
| 15 | Hand-drawn ellipse / underline | V6 f108, f256; V1 f1051; V3 f186 | Stroke draws on in 6–12 f | CODE | — | `MarkerEllipse`, SVG path | L | **Validated** (no wobble) |
| 16 | Marker hand lettering | V3 notes; V6 tape | Marker caps | CODE | font (Permanent Marker) | text with `marker` font | L | **Validated** |
| 17 | Pop-in (disc, bullet, sticker) | V2 f141–195; V6 f92 | Expo-out 7–18 f, no overshoot | CODE | — | `PopIn` | L | **Validated** |
| 18 | Tape label slide + rotation settle | V5 f114–230 | Expo-out travel and rotation | CODE | — | `translate` / `rotate` interpolate | L | **Validated** |
| 19 | Camera push to detail | V3 f5523–5599; V6 f52–74 | ×1.18–1.8 in-out, others dim | CODE | — | scale and origin on a camera layer | L | **Validated** (×1.18) |
| 20 | Linear creep / pull during holds | V6 f116–216 | 0.2–0.4 %/2 f | CODE | — | `1 - 0.001*f` | L | **Validated** |
| 21 | Zoom-through cut | V6 f436–492 | Ease-in push → cut → ease-out settle | CODE | — | `zoomThrough()` presentation | M | **Validated** |
| 22 | Whip pan | V6 f220–234 | −309 px in 14 f, ease-out | CODE | — | translate a camera layer, `ease.punch` | L | Not built |
| 23 | Lateral pan between charts | V3 f4670–4739 | 1675 px in 68 f, `ease.pan` | CODE | — | `translate` on a wide canvas | L | Not built |
| 24 | Map region zoom | V3 f1680–1752; V1 f346–406 | Log-scale zoom ×5.7–30, in-out | HYBRID | GeoJSON or map tiles | SVG paths (d3-geo) or `remotion-maps` skill; interpolate log-scale | M–H | Not built |
| 25 | Region fill / outline draw | V3 maps; V1 f417 | Grey→colour fill; outline stroke-on | HYBRID | GeoJSON | SVG `fill` interpolate, dashoffset | M | Not built |
| 26 | People / icon stagger | V3 f1744–1790 | 1 per 2 f, reading order | HYBRID | icon set (original) | map with `opacity` by index | L | Not built |
| 27 | Donut / hemicycle build | V3 f2506; f4443 | Radial draw 18 f; arc sweep 28 f | CODE | data | SVG arcs + dashoffset | M | Not built |
| 28 | Magnifier / loupe | V3 f3786–4100; V6 f383 | Lens slides in, shows a magnified layer | HYBRID | lens frame image (or CSS ring) | `clip-path: circle()` over a scaled duplicate | M | Not built |
| 29 | Loupe reveal transition | V3 f1330–1423 | Lens carries the next scene, grows to fill | CODE | — | custom presentation with an animated `clip-path` | M | Not built |
| 30 | Cut-out photos with border and shadow | V1, V5, V6 | White border, drop shadow, slight rotation | HYBRID | **photos / cut-outs (licensed or original)** | `<Img>` + `shadow.cardLarge` | L | Placeholder only |
| 31 | B&W archival grade | V1 archival | Neutral B&W + warm lift | HYBRID | archival media | `filter: grayscale(1) sepia(.08)` or `duotone()` | L | Placeholder only |
| 32 | Halftone / engraving cut-outs | V2, V3 statue, V6 rat | Printed texture people and objects | ASSET | prepared halftone art (or `halftone()` effect on photos) | `<Img>` or `@remotion/effects` `halftone()` | M | Not built |
| 33 | Footage in inset card + caption | V1 f136–341 | Footage scales to a rounded card | HYBRID | footage | `@remotion/media` `<Video>` in a scaled container | L | Not built |
| 34 | Chromatic aberration | V1 captions; V6 tape | 2–3 px RGB fringe | CODE | — | `text-shadow` split; `chromaticAberration()` for images | L | **Validated** on text |
| 35 | Radial zoom-blur / rack focus | V6 f1031–1039; V1 f0 | Streak or defocus in and out | CODE | — | `@remotion/effects` `zoomBlur()` / `blur()` in `HtmlInCanvas` | M | Not built |
| 36 | Short dissolve | V1 f527, f774 | 3–6 f | CODE | — | `fade()` + `linearTiming(4)` | L | Not built |
| 37 | Page curl | V1 f126–136 | Corner peel | ASSET / H | WebGL or a pre-rendered curl | Three.js plane or a video overlay | H | Not built (novelty) |
| 38 | Crumpled-paper wipe | V1 f1662–1684 | Paper sheet rises | ASSET | paper-texture plate | mask + translate | M | Not built |
| 39 | Texture boil (stop-motion) | V4 all | A-A-B loop at 3.3 Hz | CODE | — | alternate texture seeds every 3 f | L | Not built |
| 40 | Lower third | V3 f2109–2160 | Dots, plate wipe, typed name and role | CODE | — | `LowerThird` (spec in M19) | L | Not built |
| 41 | Sticky-note peel / flip | V6 f863–868 | 3D unfold in 6 f | CODE | — | `rotateY` with `perspective`, motion blur optional | M | Not built |
| 42 | Facecam / interview in a frame | V5, V6, V3 | Live video in a photo frame or rounded rect | ASSET | **interview footage** | `<Video>` in a styled container | L | Not built |
| 43 | Desk props (pens, tubes, tape, clips) | V6, V1 outro | Cropped props at frame edges, DOF blur | ASSET | prop photos (original) | `<Img>` + `filter: blur(3px)` | L | Not built |
| 44 | Fade to black | V2 f390–418; V1 f5840 | Linear 29–58 f | CODE | — | black overlay opacity | L | **Validated** |
| 45 | Music bed / VO / mix | all | -18 LUFS; bed 15–23 dB under VO | ASSET | licensed music, VO | `<Audio volume>` | L | Not built (no audio assets) |
| 45b | Designed SFX on visual events | V3 intro and chapter hits; V5 whooshes | paper rustle, stamp, brush swish, whooshes, paper slaps | CODE (synthesised) | none: `scripts/make-sfx.sh` makes `public/sfx/*.wav` with ffmpeg noise and sine synthesis, peak-normalised to -3 dBFS | cue list → `<Sequence from><Audio src={staticFile()} volume playbackRate/>` (`NewspaperDemo.tsx`) | L | **Validated**: rendered-audio onsets match cue frames within 0–2 f |

**Summary:**

- 45 techniques: 31 CODE, 8 HYBRID, 6 ASSET (or asset-heavy).
- 18 are validated in the calibration composition (#15 without stroke wobble); 1 more is partially validated (#5, solid rather than dashed grid).
- Photographs, archival footage, interviews, halftone art, desk props, music and VO cannot be generated by code and must be supplied or licensed.
