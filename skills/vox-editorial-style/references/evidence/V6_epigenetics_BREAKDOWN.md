# V6_epigenetics — Vox "epigenetics" excerpt — Forensic Breakdown

Source: key V6_epigenetics in `../sources.tsv`. 1920x1080, 23.976 fps, 1225 frames, 51.1 s. Source not modified.

**Frame format [Measured f72]:** 4:3 picture 1440x1080 at x 240–1679, pillarbox bars flat #1F1F1F (31,31,31) left/right; a white "Vox" wordmark sits in the top of the right bar (x≈1700–1900, y≈0–60). All px values below are 1080p frame px; "content" coordinates exclude the bars.

## A. Inventory

| Item | Path |
|---|---|
| Per-frame diff | `framediff.tsv` (1225 rows) |
| Cut candidates | `cuts.json` (2,6,10,218,329,429,462,566,610,614,717,766,851,907,1035,1039,1105,1109,1170) |
| Frames / sheets / full-res | `frames/` (91), `sheets/sheet_00–02.jpg`, `full/` (18 PNGs every 72 f) |
| Work scripts | `work/affine_c.py` (ORB+RANSAC similarity transform on content area, every frame), `work/sumaff.py` (groups moving frames into camera-move runs), shared `../V2_camera/work/strip.py`, `col.py`, `maskcol.py`, `cad.py`, `runs.py` |
| Work outputs | `work/affine.txt` (1224 transforms), `work/affine_runs.txt`, `work/affine_moving.txt`; overview strips every 4th frame `work/u_0_319.jpg`, `u_320_639.jpg`, `u_640_959.jpg`, `u_960_1224.jpg`; every-frame strips `work/d_0_40.jpg`, `d_88_118.jpg`, `d_216_236.jpg`, `d_252_306.jpg`, `d_380_400.jpg`, `d_428_470.jpg`, `d_606_622.jpg`, `d_714_770.jpg`, `d_860_874.jpg`, `d_1028_1046.jpg`, `d_1102_1116.jpg`; crops `work/title_crop.jpg` (f144), `tape_crop.jpg` (f144), `age_crop.jpg` (f863), `logo_crop.jpg` (f72) |

## B. Inspection record

- Total frames 1225. Numerically measured: all (framediff; similarity transform scale/rotation/translation for all 1224 pairs; luma).
- Visually opened: every 4th frame 0–1224 (307 frames); every frame in 0–40, 88–118, 216–236, 252–306, 380–400, 428–470, 606–622, 714–770, 860–874, 1028–1046, 1102–1116 (≈335 frames, ~85 overlapping) → ≈ 560 unique frames; plus sheets (51 frames) and 4 full-res crops. Not opened individually: odd/non-multiple-of-4 frames outside those dense windows (on-2s animation means most of those are duplicates of an opened neighbour).

## C. Scene table

| # | start t (f) | end t (f) | dur | description | motion | typography | transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 (0) | 0.63 (15) | 16 f / 0.67 s | Flash montage: magnifier over methylated DNA (f0–1), blank dotted paper (f2–3), rat engraving (f4–5), blurred rat+petri (f6–9), blurred DNA card (f10–15) | 2–6 f flashes, heavy defocus | — | cuts → focus pull |
| 2 | 0.67 (16) | 9.05 (217) | 202 f / 8.4 s | Desk collage: chalk DNA card on stacked photos, "DNA" yellow tape, test tube, pen; "Genetics" header; "EPI" sticky note; blue methyl dots pop on | focus pulses (sharp f16, soft f24–29, sharp f30), snap pull-back f22, tilt-push f52–74, sticky slap f92–100, underline draw f108–116, slow linear pull-out f116–216 | serif "Genetics", marker "EPI"/"DNA" | hard cut + whip pan |
| 3 | 9.09 (218) | 13.68 (328) | 111 f / 4.6 s | Illumina sequencer photo with tape "SCAN – ILLUMINA", DNA card top-right | whip pan f220–234 (ease-out), rotation settle f242–252, slow zoom-out; hand-drawn circle draws on f256–268; leader line f286–292; zoom-bubble (red/green dots) pops f292–304 | marker tape label | hard cut |
| 4 | 13.72 (329) | 17.85 (428) | 100 f / 4.2 s | Methylated DNA chalk card full frame, "METHYLATED DNA" tape | magnifier slides in from right f383–399; held otherwise | marker tape | hard cut |
| 5 | 17.89 (429) | 19.23 (461) | 33 f / 1.4 s | "Methyl group" callout, METHYLATED DNA tape, hand-drawn arrow to circled "Sexual orientation ?", yellow brush ring, test tube | accelerating push-in ×1.29 f436–460 | bold sans "Sexual orientation", small yellow sans "Methyl group" | zoom-through cut |
| 6 | 19.27 (462) | 23.57 (565) | 104 f / 4.3 s | Polaroid of two men (Horvath brothers) + petri dish; marker label writes on; "SALIVA TEST" black tag | zoom continues and decelerates ×1.82 f464–492; label write-on f496–520 | marker caps "HORVATH BROTHERS", tag "SALIVA TEST" | hard cut |
| 7 | 23.61 (566) | 25.40 (609) | 44 f / 1.8 s | Interview facecam video inside photo frame | handheld jitter ±12 px, rot −1.5° (f577–582) | — | hard cut (glitch double) |
| 8 | 25.44 (610) | 29.86 (716) | 107 f / 4.5 s | Research paper on desk with highlighter; f610–613 extreme close text with doubled/offset ghost; push-in to title, "Predictor of Age" highlighted yellow | settle f614–630; ease-in-out push ×1.73 f654–696 | paper print text | hard cut |
| 9 | 29.90 (717) | 31.91 (765) | 49 f / 2.0 s | Back to "Sexual orientation" collage | ease-in-out zoom ×1.76 + pan (f727–765); X scribble draws over text f742–746 | — | hard cut |
| 10 | 31.95 (766) | 35.45 (850) | 85 f / 3.5 s | "Training Data" note: paper card "Epigenetic Predictor of Age" with gears; dotted-cell circles with yellow "AGE 54/73/22/7/71" tags around | slow linear push ×1.16; tags pop staggered (~f776, 784, 800, 812, 836); gears recolour red→green f800–830 | serif "Training Data", sans card title, marker tags | match-zoom cut (×2.01 at f851) |
| 11 | 35.49 (851) | 37.79 (906) | 56 f / 2.3 s | Crossed-out "Sexual orientation" + "Age?" sticky note | slow linear pan up 2.1 px/2 f; sticky note flips/unfolds in f863–868 | marker "Age?" | hard cut |
| 12 | 37.83 (907) | 43.13 (1034) | 128 f / 5.3 s | Long DNA strand on dark chalk, red/green methyl marks; yellow flag labels "Habits", "Hardships", "Time" | slow push 0.35 %/2 f; flags pop f964–968, f992–996, f1008–1012; out: radial zoom-blur f1031–1034 | bold serif on yellow flags | zoom-blur |
| 13 | 43.17 (1035) | 46.05 (1104) | 70 f / 2.9 s | Petri dish of cells (B/W) with red/green zoom bubble | zoom-blur in f1035–1039, snap pull ×0.943 f1043, slow pull-out | — | radial zoom-blur |
| 14 | 46.09 (1105) | 48.76 (1169) | 65 f / 2.7 s | Engraved rat with methylation bubble, yellow brush ring + strokes, pen, highlighter | zoom-blur in f1105–1110, settle pull-out ×0.88 f1113–1125 (ease-out) | — | hard cut |
| 15 | 48.80 (1170) | 51.05 (1224) | 55 f / 2.3 s | End card: chalk card "lucasmariano.com", "THANK YOU!" tape | gradual darkening luma 116.7 → 103.4 | serif URL, marker tape | end |

## D. Motion catalog

1. **Cadence: animated on 2s (12 fps)** [Measured]: gap histogram 528 gaps of 2, 167 of 1 (the 1-gaps are at cuts/blur transitions and live video). Held shots still change on every 2nd frame with mad ≈ 0.7–1.7 (e.g. f336–380), lag-2/4/6 diffs keep growing (4.0 → 7.1 → 8.0 at f1180–1192) → **non-looping grain + light flicker**, not a texture loop.
2. **Snap pull-back** [Measured f22]: scale ×0.953 in one step (2 f).
3. **Tilt/push into "Genetics"** [Measured f52–74, `affine_runs.txt`]: per-2-frame scale 1.001, 1.003, 1.008, 1.012, 1.020, 1.038 | 1.044, 1.022, 1.012, 1.004, 1.002; dy +1,+4,+6,+11,+18,+36,+30,+15,+7,+4,+1 → **ease-in-out (≈ cubic-bezier(0.45,0,0.55,1))**, 22 f (0.92 s), total ×1.18, content moves down 134 px (camera tilts up to reveal header).
4. **"EPI" sticky slap** [Observed `d_88_118.jpg`]: f92 small yellow fleck near "Genetics", f94–95 half-size, f96 near full, f98–100 settled = scale-up from ~10 % to 100 % over ~8 f (4 drawings) with slight rotation, no overshoot visible.
5. **Hand-drawn underline** [Observed]: marker underline under "Genetics" draws L→R f108–116 (~8 f, ~240 px → ≈ 700 px/s).
6. **Slow pull-out** [Measured f116–216]: scale 0.996–0.998 per 2 f, 51 steps, total ×0.83, drift dy −118 px → **linear** (constant velocity), 100 f / 4.2 s.
7. **Whip pan** [Measured f220–234]: dx per 2 f = −60, −82, −60, −41, −30, −22, −14 → total −309 px, peak at step 2 then decay = **fast ease-out** (≈ cubic-bezier(0.2,0.8,0.3,1)), ~14 f (0.58 s); followed by rotation settle +2.0° and scale 0.968 over f242–252.
8. **Circle draw-on** [Observed `d_252_306.jpg`]: rough double-loop marker circle around a DNA segment appears progressively f256–268 (~12 f / 0.5 s). Vertical leader line draws down f286–292 (6 f). Zoom bubble (red/green dot grid) grows from a point f292 → full ~f300–304 (≈10 f, ease-out), centred at the line end.
9. **Magnifier slide-in** [Observed `d_380_400.jpg`]: enters from right edge f383, half in f387, near final f393, settled f397–399 → ~16 f (0.67 s) ease-out, slight scale; glass shows magnified DNA (lens distortion).
10. **Zoom-through transition** [Measured f436–492]: push-in per 2 f 1.000→1.002→…→1.034→1.048→1.080 (×1.29, accelerating, ease-in, 24 f), cut at f462, then new shot continues 1.456 (one step, cut matched) → 1.071, 1.039, 1.026, 1.020 … 1.003 (×1.82 decelerating, 28 f) → velocity-matched **ease-in → cut → ease-out** "zoom through" (total ≈ ×3.4 apparent).
11. **Marker label write-on** [Observed u-strip f496–520]: "HORVATH BROTHERS" letters appear L→R, ~1 letter / 2 f.
12. **Handheld facecam** [Measured f577–582]: dx −12, −9, +10, +7, +8 px, rot −1.5° → real handheld/shake, not keyed.
13. **Push to paper title** [Measured f654–696]: scale per 2 f 1.003→1.010→1.024→1.073→1.152 (peak f678) →1.072→1.046→…→1.001; dx +114, dy +349 → **ease-in-out**, 42 f (1.75 s), total ×1.73. Highlight "Predictor of Age" present by f684.
14. **Zoom + pan to crossed text** [Measured f727–765]: scale steps 1.002, 1.006, 1.015, 1.029, 1.079, 1.150 (peak f737), 1.046, 1.023, 1.015, 1.010 …; total ×1.76, dx −298, dy −266 → asymmetric ease-in-out (accelerate 10 f, decelerate ~28 f). X scribble: 2 strokes appear f742–746 (~4 f).
15. **Staggered tag pops** [Observed u-strip]: "AGE" tags ≈ f776, 784, 800, 812, 836 (8–24 f apart), each pops within ~2 drawings.
16. **"Age?" sticky flip-in** [Observed `d_860_874.jpg`, `age_crop.jpg`]: f863 folded yellow triangle, f864–866 unfolding (3D peel rotation about left edge, motion blur), f867 flat with "Age?", f868–870 small settle. ~6 f (0.25 s).
17. **Slow linear pan** [Measured f853–905]: dy −2.1 px per 2 f constant (≈25 px/s), scale +0.07 %/2 f.
18. **Flag-label pops** [Observed `u_960_1224.jpg`]: "Habits" (top, f964–968), "Hardships" (top, f992–996), "Time" (bottom, f1008–1012); each = yellow flag scales/slides out from its stem; stagger 28 f then 16 f.
19. **Radial zoom-blur transitions** [Observed `d_1028_1046.jpg`, `d_1102_1116.jpg`]: outgoing shot gets radial streak blur over 2–4 f (f1031–1034; f1105–1108), incoming shot starts heavily defocused/streaked and resolves over ~4–6 f (f1035–1039; f1109–1111); then ease-out pull-out settle: per 2 f 0.932, 0.975, 0.988, 0.992, 0.996 (f1113–1121) → ×0.88 over 12 f.
20. **End darkening** [Measured]: luma −0.26 per frame linear over f1172–1224 (116.7 → 103.4).

## E. Transitions

| f | type | evidence |
|---|---|---|
| 2, 6, 10 | hard flash cuts (2–4 f shots) | `d_0_40.jpg` |
| 16 / 24–30 | rack focus in, defocus pulse, focus | `d_0_40.jpg` |
| 218 | hard cut into whip pan | `d_216_236.jpg`, affine |
| 329, 566, 717, 907, 1170 | hard cuts | u-strips |
| 462 | zoom-through (ease-in push → cut → ease-out push) | affine 436–492 |
| 610–614 | hard cut to extreme close text with offset ghost/double image (glitch) then cut to wider | `d_606_622.jpg` |
| 766, 851 | match-scale cuts (scale jump 0.44 / 2.01 measured across the cut) | affine.txt |
| 1031–1039, 1105–1111 | radial zoom-blur transitions | `d_1028_1046.jpg`, `d_1102_1116.jpg` |

`cuts.json` items 1039 and 1109 are blur-resolve steps inside transitions, 614 is the second half of the glitch cut [Verified].

## F. Typography & layout

| Element | Face [Observed] | Google match [Inferred] | Size (1080p) | Treatment |
|---|---|---|---|---|
| "Genetics", "Training Data" | bold old-style/transitional text serif | Source Serif 4 Bold / Merriweather Bold | x-height ≈40 px → ~85 px font (f144) | dark grey ink printed on paper, slightly soft; hand-drawn double marker underline |
| "EPI", "DNA", "METHYLATED DNA", "HORVATH BROTHERS", "THANK YOU!", "AGE 54", "Age?" | hand-lettered marker caps (single-stroke) | Permanent Marker (EPI) / Gochi Hand or "Rock Salt"-lite for tape labels | EPI ≈ 60 px cap; tape labels ≈ 28–34 px | black/dark-blue marker on yellow sticky note (180x140 px) or yellow tape strips |
| "Sexual orientation" | heavy grotesque sans | Inter Bold / Archivo Bold | x-height ≈55 px at zoom → ~105 px | black, enclosed in loose double-loop pencil ellipse, "??" scribbles |
| "Methyl group" | small sans in yellow | Inter Medium | ~22 px | yellow text with thin yellow leader line |
| Flag labels "Habits/Hardships/Time" | bold serif | Source Serif 4 Bold | ~24 px | dark text on yellow flag, thin black stem |
| End-card URL | serif, low contrast grey on chalk | Source Serif 4 | ~40 px | chalky, semi-transparent |
| "Vox" wordmark in bar | Vox logo (condensed serif italic-ish) | — (brand) | ~55 px | white on #1F1F1F bar, top-right |

Layout: top-down desk collage; key object (card / photo) centred, header text top-centre, tape labels overlapping card's lower-left edge, props (test tube, pen, paperclip, highlighter) cropped at frame edges.

## G. Color & texture

| Swatch | HEX | Source |
|---|---|---|
| Pillarbox bars | #1F1F1F (exact, std 0) | f144 x 60–160 [Measured] |
| Dotted desk paper | #CFCECF (lit), #8D8A89 (shadowed top-right) | f144 [Measured] |
| Chalk card | #333233; dark DNA bg #1F1D1F | f144, f935 [Measured] |
| Tape / sticky yellow | #E0D237 (f144), #DBD032 (f863) | HSV mask median [Measured] |
| DNA rungs yellow | #E5BE4D | f935 [Measured] |
| Methyl marker green | #2FA62A | f935 [Measured] |
| Methyl marker red | #6F2D22 (mask median, darkened by texture; visually brighter ~#C83A2E [Estimated]) | f935 |
| Accent red (small) | #8B3627 / #8A3929 | f144, f863 [Measured] |

Texture [Observed/Measured]:
- **Film grain/noise** refreshed every 2 frames (D1).
- **Chromatic aberration** ≈ 2–3 px RGB fringing at high-contrast edges (blue left/top, red right) [Observed `tape_crop.jpg`].
- **Lighting**: strong soft shadow/light gradient across the desk (corner luma at f791: 107, 122, 176, 203 vs centre 173) — simulated window light/vignette, not symmetric [Measured].
- Dotted grid paper (dot pitch ≈ 52 px at f863 zoom) [Estimated].
- Photos/cards have worn white borders, deckled/torn edges, paperclips, translucent tape with soft shadows; chalk card has halftone dot texture.
- **Depth of field**: frequent defocus (rack focus at open, defocused foreground props); zoom/radial motion blur on transitions.
- Drop shadows under cards: soft, offset down-right ~8–15 px [Estimated visually].

## H. Pacing

- 15 scenes in 51 s, median ≈ 2.7 s (range 0.67–8.4 s); the opening "Genetics → EPIgenetics" beat gets 8.4 s, explanation beats 2–4.5 s.
- New visual event (label, circle, sticky, camera move) every ~1–2 s; the camera is almost never fully static (slow linear push/pull 0.3–0.4 %/2 f fills holds).
- Big moves (whip, zoom-through, push to title) take 14–42 f (0.6–1.75 s); small pops 4–10 f.

## I. Uncertainties

- Similarity-transform numbers measure the dominant (largest-area) layer; foreground cutouts moving separately (e.g. magnifier, tags) are not captured by them.
- Easing labels are from 2-frame-sampled values; bezier params are estimates.
- Fonts are visual matches; marker lettering may be hand-drawn assets rather than a font.
- Red methyl dot HEX affected by mask including dark texture pixels.
- Frames between dense windows not individually opened (on-2s duplicates mostly).
