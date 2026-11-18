# V2_camera — "The First Camera Ever Made (Vox-style intro)" — Forensic Breakdown

Source: path in `../sources.tsv` (key V2_camera). 1920x1080, 60 fps CFR, 419 frames, 6.98 s of picture (probe says 7.04 s). Source video not modified.

## A. Inventory

| Item | Path |
|---|---|
| Per-frame diff (all 419 frames) | `framediff.tsv` |
| Cut candidates | `cuts.json` (21,39,57,81,99,117,141,261,390,415) |
| Uniform/cut frames 640x360 | `frames/` (48 files) |
| Contact sheets | `sheets/sheet_00.jpg`, `sheets/sheet_01.jpg` |
| Full-res PNG | `full/f00000…f00360.png` (every 45 f) |
| Work scripts | `work/runs.py` (motion runs), `work/cad.py` (cadence), `work/strip.py` (frame strips), `work/meas.py` (per-frame yellow/red mask bbox + phase-correlation shift), `work/col.py`, `work/maskcol.py` (HEX sampling) |
| Work outputs | `work/meas.txt` (419 rows), `work/s_0_22.jpg`, `work/s_0_141.jpg`, `work/s_129_141.jpg`, `work/s_141_270.jpg`, `work/title_141_200.jpg`, `work/s_255_418.jpg`, `work/s_388_418.jpg`, `work/title_crop.jpg`, `work/body_crop.jpg` |

## B. Inspection record

- Total frames: 419. Numerically measured: all 419 (framediff mad/luma; `meas.py` yellow-mask bbox, red-mask area, global phase-correlation shift for every frame).
- Visually opened (approx. 190 unique frames):
  - 0–22 every frame (23) — `s_0_22.jpg`
  - 0–141 every 3rd (48) — `s_0_141.jpg`
  - 129–141 every frame (13) — `s_129_141.jpg`
  - 141–200 every frame (60, title crop) — `title_141_200.jpg`
  - 141–270 every 3rd (44) — `s_141_270.jpg`
  - 255–418 every 6th (28) — `s_255_418.jpg`
  - 388–418 every 2nd (16) — `s_388_418.jpg`
  - sheet_00 (20 frames 0–285 at 15 f), full-res crops of f180 and f360.
- Not opened individually: odd frames 271–387 that are not multiples of 6 (framediff shows they are mostly exact holds anyway).

## C. Scene table

| # | start t (f) | end t (f) | dur | description | motion | typography | transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.000 (0) | 0.333 (20) | 21 f / 0.35 s | Engraved optics diagram (line art + script) on cream paper | 3 stepped poses at f0/3/9/15 (on 6s, first step on 3); plate drifts up 30→14→10 px (ease-out) | old engraved handwriting only (part of image) | hard cut |
| 2 | 0.350 (21) | 0.633 (38) | 18 f / 0.30 s | "Real candle / pinhole / the image" camera-obscura diagram | stepped drift up 6.7, 5.7 px at f27, f33 | engraved caps in image | hard cut |
| 3 | 0.650 (39) | 0.933 (56) | 18 f / 0.30 s | Room-sized camera obscura engraving | drift up 4.1, 3.6 px (f45, f51) | — | hard cut |
| 4 | 0.950 (57) | 1.333 (80) | 24 f / 0.40 s | Annotated bellows camera on tripod engraving | drift 2.8, 2.4, 2.1 px (f63/69/75) | engraved labels | hard cut |
| 5 | 1.350 (81) | 1.633 (98) | 18 f / 0.30 s | Box camera with mirror (cutaway engraving) | drift ~1.8, 1.9 px (f87/93) diagonal | — | hard cut |
| 6 | 1.650 (99) | 1.933 (116) | 18 f / 0.30 s | Color photo cutout: wooden bellows camera | small 2–3 px steps (f105, f111) | — | hard cut |
| 7 | 1.950 (117) | 2.333 (140) | 24 f / 0.40 s | Color cutout: folding Kodak-type camera; image swaps at f123/129/135/137 (different angle / photo, re-positioned −51 px x at f129) | substitution animation, on 6s, extra swap at 137 | — | hard cut to title |
| 8 | 2.350 (141) | 4.333 (260) | 120 f / 2.0 s | TITLE: "The First / Camera / Ever Made ■" over yellow circle on plain cream | circle scale-in, letter-by-letter reveal, red square pop, all on 6s; slow creep-scale of circle | see F | hard cut |
| 9 | 4.350 (261) | 6.483 (389) | 129 f / 2.15 s | Bio card: halftone portrait of Niépce + two vintage cameras on yellow circle; name, dates, body paragraph right | circle grows (stepped ease-out), name types on, red bullet pops, dates & body fade in; continuous slow creep | see F | fade to black |
| 10 | 6.500 (390) | 6.967 (418) | 29 f / 0.48 s | Same card fading to black | linear luma 188.5→5.1, −6.3/frame, every frame (not stepped) | — | end |

## D. Motion catalog

1. **Global cadence — animated on 6s (10 fps inside 60 fps)** [Measured]. Changing frames are spaced exactly 6 f apart (gap histogram: 43 gaps of 6; framediff spikes at 3,9,15,21,27,33,…; 262/419 frames are exact holds mad<0.05). Only the final fade (390–418) and title-sequence edge frames (145,147–156, 170–175) change at 1–2 f, caused by soft-edge/opacity steps. Evidence: `framediff.tsv`, `work/runs.py` output.
2. **Montage plate drift (shots 1–5)** [Measured, phase correlation on full frames, `work/meas.txt`]: each still moves upward in discrete steps with decaying amplitude per shot — shot 1: −29.9, −13.8, −10.1 px; shot 2: −6.7, −5.7; shot 3: −4.1, −3.6; shot 4: −2.8, −2.4, −2.1; shot 5: −1.6, −1.5 (+ ~−1 px x). Reads as an ease-out settle inside each 18–24 f shot; the montage overall decelerates. [Inferred] stepped jitter adds "hand-placed paper" feel.
3. **Montage cut rhythm** [Measured]: shots 21,18,18,24,18,18,24 frames = 0.30–0.40 s each (≈3–4 animation drawings per image). Total 141 f = 2.35 s for 7 images.
4. **Title circle scale-in** [Measured, yellow mask bbox]: diameter 228 px (f141) → 262 (f147) → 278 (f153) → 286 (f159) → 288 (f165) → 290 (f219) → 302 (f255). Normalised progress 0, .55, .81, .94, .97 per 6 f step: strong ease-out (≈ cubic-bezier(0.16,1,0.3,1) / expo-out) over ~24 f (0.4 s), then a slow linear creep ~+0.5 px per step (continuous push of ~5 % over 2 s). Bbox left edge moves 740→664 while right stays ~950–967: scale anchor is NOT the circle centre [Inferred: anchored right/top, or circle also translates −36 px x].
5. **"Camera" write-on** [Observed, `title_141_200.jpg`]: f141 nothing; f147 "Came"; f153 "Camer"; f159 "Camera" — 4,1,1 letters per 6 f step (reveal by mask wipe left→right rather than strict typewriter; the first step jumps 4 glyphs). "The First" is fully present from f141.
6. **"Ever Made" entrance** [Observed]: appears f159 at ~45 % opacity with "Ever" raised ~10 px above baseline of "Made" (staggered baseline); f165 brighter, still offset; f171 full opacity, baseline aligned. = per-word stagger rise + fade over 12 f (0.2 s), on 6s.
7. **Red square bullet pop** [Measured, red mask area]: 0 (≤f176) → 211 px² (f177) → 440 (f183) → 550 (f189) → 621 (f195) → ~600–630 thereafter; side ≈14.5 → 21 → 23.5 → 25 px. Ease-out scale-in 18 f (0.3 s), no overshoot detected.
8. **Bio card circle (shot 9)** [Measured]: yellow bbox width 545 (f261) → 653 (f267) → 699 (f273) → 723 (f279) → 733 (f286) → 735 (f292) → 753 (f388). Progress .0,.52,.74,.86,.90,.91 — same ease-out family as title circle, ~25 f, then creep +18 px over ~100 f.
9. **Name type-on** [Observed, `s_255_418.jpg`]: "Joseph" visible f267, "Joseph Nic…" f273, full "Joseph Nicephore" f279–285 → ~3 steps / 18 f. Red bullet appears f291–297 (area 358→572 px², f292→f298) to the left of the name, i.e. bullet pops AFTER the text (opposite order to title where square follows "Ever Made").
10. **Dates & body paragraph** [Observed]: dates line appears faint ~f297–303; body paragraph fades in from ~f327 (faint) to full ~f345 (≈18 f, stepped). No positional motion observed.
11. **Final fade to black** [Measured]: mean luma 188.5 (f389) → 5.1 (f418), steps of 6.2–6.6 per frame, i.e. linear opacity ramp over 29 f (0.48 s). The yellow appears to desaturate/darken with the rest (global multiply, not per-layer).

## E. Transitions

- 9 hard cuts (f21, 39, 57, 81, 99, 117, 141, 261) plus image-substitution cuts within shot 7 (f123, 129, 135, 137). [Measured: mad 15–25 at each, single frame].
- No wipes, no cross-dissolves anywhere. Only soft transition: final linear fade to black 390–418. [Measured]
- `cuts.json` candidate f415 is inside the fade (false positive) [Verified, `s_388_418.jpg`].

## F. Typography & layout (1080p px, estimated from 1:1 crops `work/title_crop.jpg`, `work/body_crop.jpg`)

| Element | Face (observed) | Google Font match [Inferred] | Size | Position | Treatment |
|---|---|---|---|---|---|
| "The First" | Neo-grotesque sans, bold, tight tracking, sentence case | Inter Tight Bold / Archivo Bold (orig. likely Helvetica Bold) | cap ≈30 px → ~42 px font | top-left of circle, x≈590, y≈430 | ink-rough edges (print texture), black #161110 |
| "Camera" | Heavy italic old-style serif, condensed | "Playfair Display Black Italic" closest free; orig. resembles ITC Garamond Condensed Bold Italic | cap C ≈95 px, x-height ≈65 px → ~130 px font | overlaps circle centre-left, baseline ≈ y 575 | same rough print edge, slight halftone dots in black |
| "Ever Made" | same sans as "The First" | same | ~40 px | right-aligned under "Camera", x≈1100–1340, y≈610 | followed by red square ■ 25 px (#8B1916) |
| "Joseph Nicephore" | High-contrast serif display, bold | DM Serif Display / Playfair Display Bold | cap ≈40 px → ~56 px | x≈1085, y≈370 | rough ink texture; red 25 px square bullet left of it |
| Dates "(7 March 1765 – 5 July 1833)" | Light italic geometric sans | Poppins Light Italic | ~22 px | under name | grey #5C5446 [Estimated] |
| Body paragraph | Geometric sans, regular with Semibold emphasis for name/keyword | Poppins Regular / SemiBold | x-height ≈15 px → ~24 px, leading ~30 px, 6 lines, measure ~700 px | left edge aligned with name, x≈1070 | grey-brown text, bold run-ins |

Layout: title block centred ~x 960 slightly left; bio card = image left half (x 200–950), text column right (x 1070–1800), vertical centre ~y 400. [Measured from yellow bbox and crops]

## G. Color & texture (HEX measured from `full/` PNGs unless noted)

| Swatch | HEX | Source |
|---|---|---|
| Paper, title/bio scenes | #E6DEC7 (std 0.8) | f180 and f360, regions (100,100,200x200) and (1600,800) [Measured] |
| Paper, montage shot 1 | #EBE5D2 – #F2ECD9 (lighter, vertical gradient, std 2–5) | f0 [Measured] |
| Accent yellow (circle) | #EAB618 / #EAB716 | HSV-mask median f180, f360 [Measured] |
| Accent red (square bullet) | #8B1916 (f360), #821E1B (f180 small sample) | [Measured] |
| Ink black text | #161110 – #191613 | dark-pixel median f180/f360 [Measured] |
| Sepia photo tones (cameras) | #9B7550 / #34281C | f135 [Measured, small sample] |

Texture [Observed]: montage stills have scanned-paper grain, faint horizontal fold/ruled lines and grey mottling; title/bio background is flat warm paper with very fine noise (std <1 → near-flat). Type and portrait have halftone / photocopy texture (dot pattern visible in black). Portrait is a B/W halftone engraving cutout; cameras sepia color cutouts with clean cut edges; NO drop shadows detected on cutouts; no vignette (corner/centre luma identical in f180). Circle has a slightly rough/organic edge (not a perfect vector circle).

## H. Pacing

- Montage: 7 images in 2.35 s (≈3 images/s), each 18–24 f; then title holds 2.0 s (animation complete by f195, ~1.1 s pure hold with creep), bio card 2.15 s (anim done by ~f345, then hold), 0.48 s fade out.
- Ratio: ~33 % fast montage / 30 % title / 37 % card+fade. Motion energy (mad mean per 0.5 s): 1.6–2.0 during montage, 0.03–0.16 in holds.

## I. Uncertainties

- Montage "drift" vectors come from full-frame phase correlation; with large paper texture they may reflect the background plate rather than the drawing (drawing itself also visibly re-positions between steps in `s_0_22.jpg`). Direction/magnitude ±50 %.
- Font identifications are visual estimates; no metadata.
- Circle scale anchor uncertain (bbox shows asymmetric growth).
- Exact opacity values for "Ever Made"/body fades not measured (visual only).
- Odd frames 271–387 not individually viewed.
