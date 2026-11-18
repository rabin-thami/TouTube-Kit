# V4_highlight — "The Highlight by Vox (animation-like)" — Forensic Breakdown

Source: key V4_highlight in `../sources.tsv`. 3840x2160, 10 fps (!), 162 frames, 16.2 s. Analysis done on frames downscaled to 1920x1080 (all px values below are 1080p px). Source not modified.

## A. Inventory

| Item | Path |
|---|---|
| Per-frame diff | `framediff.tsv` (162 rows) |
| Cuts | `cuts.json` (only f152) |
| Frames / sheets / full-res | `frames/` (36), `sheets/sheet_00.jpg`, `sheet_01.jpg`, `full/f00000…f00150.png` |
| Work scripts | `../V2_camera/work/strip.py`, `../V2_camera/work/affine.py` (ORB+RANSAC similarity per frame), `work/hl.py` (yellow/red mask extents, n-2/n-3 diff), `../V2_camera/work/col.py`, `maskcol.py` (shared helper scripts kept in V2 work dir) |
| Work outputs | `work/affine.txt`, `work/hl.txt` (all 162 frames), strips `work/s_0_35.jpg`, `s_36_71.jpg`, `s_72_107.jpg`, `s_108_161.jpg`; crops `work/f020_crop.jpg`, `work/f090_crop.jpg`; 1080p stills `work/f000/f020/f090/f140_1080.png` |

## B. Inspection record

- Total frames 162. Numerically measured: all 162 (framediff; per-frame similarity transform scale/rot/translation; yellow and red mask extents; diff vs n-2 and n-3 to detect loops).
- Visually opened: ALL 162 frames (0–161, every frame, in the four strips) + sheets 00/01 + 2 full-res 1:1 crops (f20, f90).

## C. Scene table

| # | start t (f) | end t (f) | dur | description | motion | typography | transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.0 (0) | 0.0 (0) | 1 f | Blank grey paper | — | — | ink-in |
| 2 | 0.1 (1) | 3.0 (30) | 30 f / 3.0 s | Title "The Highlight / BY Vox" | type ink-in (f1–4), highlighter brush swipe on "Highlight" (f6–14), snap zoom ×1.55 (f7–8), hold with texture boil | Playfair-like display serif | snap zoom-out |
| 3 | 3.1 (31) | 6.4 (64) | 34 f / 3.4 s | Title at original size, then erased | zoom-out ×0.645 (f31–32); hold; highlight dissolves out (f40–53); letters drop out in chunks (f55–62); blank paper f63–64 | — | ink-out to blank paper (no cut) |
| 4 | 6.5 (65) | 9.3 (93) | 29 f / 2.9 s | Newspaper headline card: red date tag, 2-line bold serif headline, rule + blackletter masthead | headline inks in f65–68, tag slides up 28 px (f66→67), rule draws L→R (f68–71), highlight swipe on "189 onboard feard dead" f75–78 | bold news serif, blackletter | upward pan |
| 5 | 9.4 (94) | 15.1 (151) | 58 f / 5.8 s | Same card panned up; body column (left) + B/W crash photo (right) | pan up 208 px f94–97 (ease-in), body & photo ink/fade in f97–102, second highlight "Lion Air Flight 610" f118–121, hold with boil | body serif ~20 px | hard cut to black |
| 6 | 15.2 (152) | 16.1 (161) | 10 f / 1.0 s | Black | — | — | end |

## D. Motion catalog

1. **Frame rate / cadence** [Measured]: 10 fps delivery. Every 3rd frame is an exact repeat (gap pattern 2 changes + 1 hold throughout holds). Diff vs n-3 ≈ 0.02–0.1 during holds (`work/hl.txt`, d3 column) while diff vs n-1 ≈ 2.5–3.0 → a **3-frame looping "boil" (A,A,B pattern)**: two paper/ink texture variants alternate, variant B shown 1 frame in 3 (3.3 Hz flicker). Whole-frame, no positional change (similarity transform = identity, `affine.txt`). Used to keep held frames alive.
2. **Title ink-in** [Observed f1–f5]: f1–f3 "The H ighlight" with missing/eroded letter parts (stencil/ink bleed reveal), f4 complete incl. "BY Vox". 4 frames = 0.4 s, no position/scale change.
3. **Highlighter swipe #1 (title)** [Measured, yellow mask right edge]: x = 822 (f6) → 894 (f7) → [zoom f8] → 982 (f8) → 1099 → 1217 → 1330 → 1451 → 1571 (f13) → 1595 (f14). After zoom: constant +113–121 px/frame (~1180 px/s), i.e. **linear wipe with hard stop**, total 9 frames (0.9 s). Final stroke 883x158 px, left-anchored, dry-brush ragged edges, slight upward slant.
4. **Snap zoom-in** [Measured, ORB similarity]: scale ×1.0466 (f7), ×1.4827 (f8) → cumulative ×1.552 in 2 frames (0.2 s); rotation 0, centre-anchored (centre translation 0). Ease-in (5 % then 48 %); no settle/overshoot. Paper texture scales with it (whole comp = camera zoom).
5. **Snap zoom-out** [Measured]: ×0.9705 (f31), ×0.6649 (f32) → back to ×1.001. Mirror of #4 (ease-in, 2 frames).
6. **Highlight erase (title)** [Measured, yellow area]: 30 957 px (f36) → 30 713 (f40) → 29 435 (f46) → 27 685 (f48) → 16 565 (f50) → 4 170 (f51) → 453 (f53) → 0 (f54). Bbox does not shrink → it is an erosion/dissolve (eaten by texture), not a wipe; accelerating (ease-in) over 14 frames, most loss in f49–51.
7. **Title type-out** [Observed f55–62]: "Highlight" loses letters right→left in chunks ("The Hig…" f55–56, "Hig…" f57–62), "BY Vox" persists until f62; f63–64 blank paper. ~8 frames.
8. **Headline build** [Observed + red mask]: f65 partial words of the headline visible mid-line (ink-in from centre outwards, ragged); f66 more words, tag at y 354–411; f67 tag jumps to y 326–392 (−28 px, 1 frame) and headline complete; f68 masthead appears faint; [Observed] the 1 px rule is visible from x≈1060 at f69 and reaches x≈330 at f70, i.e. it grows leftward from the masthead over 2 frames.
9. **Highlighter swipe #2 (headline)** [Measured]: right edge x = 325 (f75) → 489 (f76) → 762 (f77) → 1144 (f78). Steps +164, +273, +382 px → **accelerating (ease-in)**, 4 frames (0.4 s), 828 px wide, 92 px tall, hard stop.
10. **Camera pan up** [Measured, yellow/red bbox y]: highlight top y 407 (f94) → 378 → 313 → 200 (f97); deltas −29, −65, −113 → ease-in over 3 frames, total −207 px, hard stop at f97. Similarity transform confirms pure translation (dC y −1.1, −29.1, −65.0, −113.1).
11. **Body column + photo reveal** [Observed f97–102]: first 2 body lines at f97, half column f98, full column + faint photo f99, photo full opacity f100–101. ~5 frames, top-to-bottom line ink-in + photo opacity fade.
12. **Highlighter swipe #3 ("Lion Air Flight 610")** [Measured yellow area]: 54 020 (f118) → 58 007 → 63 269 → 78 158 (f121): 3–4 frames, observed L→R ("Lion" f119, "Lion Air" f120, full f121–122).

## E. Transitions

- In-scene "ink" transitions only: title is erased to blank paper (f40–64) and the headline inks in on the same paper; no cut between scenes 3 and 4 [Observed].
- Snap zooms (2 frames) act as emphasis/transition beats [Measured].
- Pan up (3 frames) reveals the next content block [Measured].
- Single hard cut: f152 to pure black (mad 155) [Measured] — end card black for 1 s.
- No dissolves between scenes.

## F. Typography & layout

| Element | Face [Observed] | Google match [Inferred] | Size (1080p) | Position | Treatment |
|---|---|---|---|---|---|
| "The Highlight" | High-contrast transitional display serif, bold, ball terminals | Playfair Display Bold (very close) | cap H ≈140 px when zoomed (≈90 px unzoomed) → ~190 / ~125 px font | centred, y ≈ 450 (zoomed) | dark grey #393834, multiply over paper, rough ink |
| "BY" | small caps sans, bold | Oswald/Roboto Condensed Bold | ~30 px | right-aligned under "Highlight" | same grey |
| "Vox" | heavy italic serif | Playfair Display Black Italic | ~110 px | right of "BY" | — |
| Date tag "Oct 29,2018" | Times-like regular | Tinos / Libre Caslon | ~40 px | top-left x≈190, y≈330 | white text on dark-red box #7D3130, box 295x66 px, slightly transparent/distressed |
| Headline | Bold news serif (Times/Century bold) | Tinos Bold / Libre Baskerville Bold | cap ≈45 px → ~62 px font; 2 lines centred | x 200–1700, y 410–520 | grey-black #3A3835, distressed |
| Masthead | Blackletter | UnifrakturMaguntia | ~28 px | right-aligned under headline, after 1 px rule | rule ~1 px dark grey |
| Body copy | Times-like regular | Tinos | ~20 px, leading ~24 px | left column x 30–300 (in 640 thumb) ≈ x 90–900 | justified-ish ragged |

## G. Color & texture (measured on 1080p downscales)

| Swatch | HEX | Where |
|---|---|---|
| Paper centre | #C4BDB2 | f0 centre 200x200 [Measured] |
| Paper corners | #B3AB9E (TL), #B2AA9D (TR), #ACA496 (BR) | f0 [Measured] |
| Highlighter | #BE933B – #C2973D (median), visibly multiplied over text | f20, f90, f140 mask [Measured] |
| Date tag red | #772F2E – #7D3130 | f90, f140 [Measured] |
| Ink text | #393834 – #3A3835 | dark-pixel median [Measured] |
| Photo (B/W, warm) | mid #817A73 | f140 [Measured] |

Texture [Observed/Measured]: crumpled grey paper with creases and stains; **vignette**: centre luma 189.5 vs corners 164–170 (≈ −12 %) [Measured f0]. Two-frame texture boil (see D1). Text has worn letterpress / dry-ink texture and the highlighter shows paper grain through it (multiply). Highlighter stroke edges are ragged dry-brush with small specks. No drop shadows; no DOF blur; photo is flat-printed into the paper (no border shadow).

## H. Pacing

- Title: 6 s total (build 1.4 s, hold ~1.6 s at zoom, 0.2 s zoom out, 2 s hold, 1 s erase). Headline: build 1.3 s, hold 1.6 s; pan 0.3 s; body hold 5 s; black 1 s.
- Everything happens in 2–9 frame bursts (0.2–0.9 s) separated by 1.5–5 s holds kept alive by the 3.3 Hz boil. The 10 fps delivery itself gives the stop-motion feel.

## I. Uncertainties

- 10 fps source: easing curves are sampled at only 2–4 points per move; shape labels (linear / ease-in) are approximate.
- Rule draw direction (f68–71) read from small thumbnails.
- Whether boil is paper-only or also text displacement not separated.
- Fonts estimated visually.
