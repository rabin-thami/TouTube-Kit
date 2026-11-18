# V3_elections — "Why US elections only give you two choices" (Vox) — Motion-graphics forensic breakdown

Tags: **[Observed]** = seen in an opened frame or strip. **[Measured]** = a number computed from pixels. **[Inferred]** = interpretation or estimate.
Frame numbers are 0-based at 23.976 fps (t = f × 1001/24000). Positions and sizes are in px at 1920×1080. The source video was never modified. All scratch work is in `work/`.

---

## A. Inventory

| Item | Value |
|---|---|
| Source | `/mnt/c/Users/rabin/Downloads/Refernace/YTDown.com_YouTube_Media_bqWwV3xk9Qk_Why-US-elections-only-give-you-two-choices_001_1080p.mp4` (row V3_elections of `sources.tsv`) |
| Video | h264, 1920×1080, 16:9, 24000/1001 fps, 14061 frames, 586.51 s, 1.31 Mb/s [Measured: source-probe.json] |
| Audio | AAC stereo 44.1 kHz (not analysed; another agent covers it) |
| Prepared evidence | framediff.tsv (all 14061 frames), cuts.json (93 candidates), scenes_0.25.txt (70), frames/ (375 JPGs), sheets/ (10), full/ (PNGs) |
| My work files | `work/*.py` (seg, ev, twos, bbox, graybox, hl, ring, bars, shift, redbox, col, pace), `work/s_*.jpg` strips, `work/full/F*.png` full-res extracts, `work/c_*.png` crops |
| Seek check | ffmpeg `-ss` dumps align exactly with framediff.tsv. Correlation of my recomputed MAD vs the tsv = 0.99999 at offset 0 [Measured: work/align.py] |

## B. Inspection record

- **Numeric coverage:** all 14061 frames, using framediff.tsv (mad, hist_bhat, luma). I re-segmented them myself (`seg.py`) and extracted motion events (`ev.py`, 154 events in graphics). I also ran an on-twos parity analysis (`twos.py`).
- **Visually inspected:**
  - All 10 contact sheets: 182 uniform frames, every 3 s, 0–586 s.
  - 20 dense strips: about 557 thumbnails in total.
  - 1 classification montage of 12 cut frames.
  - 7 full-res crops.
  - Total: about 750 frame views.
- **Dense per-frame decode** (every frame decoded at 640×360 and measured; thumbnails shown at the stated step). Total ≈ 4,250 frames:

| Range (frames) | Subject | Strip step |
|---|---|---|
| 0–230 | title card | 3 / 6 |
| 230–580 | montage | 10 |
| 770–1050 | ballots / bar charts | 8 |
| 1325–1560 | loupe transition + series sting | 8 |
| 1600–1810 | map zoom | 8 |
| 2100–2160 | lower third | 3 |
| 2440–2620 | district explode / donuts / people | 6 |
| 3540–3770 | document highlighter | 8 |
| 3766–4120 | loupe | 12 |
| 4430–4750 | hemicycle + pan | 10 |
| 4665–4740 | pan | 3 |
| 5070–5260 | PR banner | 8 |
| 5515–5600 | push-in | 4 |
| 7675–8130 | STV bars | 12 |
| 9040–9110 | recap cards | 3 |
| 9779–10010 | hemicycle 2 | 8 |
| 11940–12230 | photo stack | 10 |
| 13490–13630 | outro inserts | 5 |

- **Not opened:**
  - Frames between sheet samples in long static graphic holds and interview takes. Those are covered numerically only: the median mad inside them is 0.00–0.10.
  - Interview stretches use representative frames only.
- **Cut verification:**
  - 13 of the 93 automatic candidates have cut-frame mad < 3. They are internal graphic beats or fades, not edits: 2917, 2921, 2925, 3094, 3100, 3286, 3292, 3296, 8060, 8092, 8556, 10206, 10216 [Measured].
  - Soft transitions without a cut were found as sustained mad runs: 1330–1423 loupe wipe, 1696–1752 map zoom, 4670–4739 pan, 5523–5599 push-in, 3548–3564 blur zoom [Measured + Observed].

## C. Scene table (whole video)

Abbreviations:
- **Motion:** static % = share of frames with mad < 0.5.
- **Typography:** "Serif" = heavy news serif, "Sans" = grotesk, "Hand" = marker lettering.

| # | start t (f) | end t (f) | dur s | Description | Motion | Typography | Transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 (0) | 7.05 (169) | 7.09 | Title card: thin black frame and a B/W cut-out statue. The title types on word by word. A yellow podium rises under the statue. | Slow zoom of about 0.13 %/frame, then a ×1.30 punch-in at f72–88 [Measured] | Serif caps, centred, distressed edges | Hard cut |
| 2 | 7.09 (170) | 13.80 (331) | 6.71 | Ballot macro montage. Party names carry yellow highlighter. A hand-drawn circle draws around REP/DEM over f186–204. Giant ghost "DEM/REP" letters sit behind. | 8 shots of about 1 s, with 4-frame flash inserts at 212, 260, 310 [Measured] | Ballot type (found footage) | Hard cut |
| 3 | 13.85 (332) | 24.02 (576) | 10.17 | Archival/news montage: film leader, archival handwriting, Capitol at dusk, PBS, "Great Divide", CBS 81 %, Al Jazeera, MSNBC | Cuts every 25 f (1.04 s) from f383 to f533 [Measured] | Broadcast graphics; Vox watermark top-right | Hard cut |
| 4 | 24.07 (577) | 32.28 (774) | 8.26 | Gallup 100 % bar, "Is a third party needed?" (Yes pink, No black). One letter is highlighted. | 97 % static [Measured] | Sans title, small sans legend and axis | Hard cut |
| 5 | 32.32 (775) | 38.54 (924) | 6.26 | Ballot collage on grid paper over ghost DEM/REP serif letters. Third-party names are highlighted. | Slow drift; hard swaps at f851 and f871 [Measured] | Ballot scans | Hard cut |
| 6 | 38.58 (925) | 43.42 (1041) | 4.88 | Stacked 100 % bar, 1994–2022 House vote share (Dem / Rep / Other). A hand-drawn ellipse circles the "Other" sliver from about f960. | Draw-on ellipse | Serif chart title, sans legend | Hard cut |
| 7 | 43.46 (1042) | 59.35 (1423) | 15.93 | Three-bar chart with pink hand-lettered annotations and arrows. A loupe sweeps in (f1330–1374), reveals the title card, then grows to fill the frame (f1389–1423). | Loupe wipe [Observed] | Hand caps (pink) | Loupe/iris wipe into title card, then a mosaic cut |
| 8 | 59.39 (1424) | 64.90 (1556) | 5.51 | "America, explained" series sting: square-tile mosaic collage (red curtains, Supreme Court, Capitol, documents), red and blue dots, a scribbled ellipse, and a Vox logo in a yellow circle | Tile reveal; type-on at 2 f per letter, f1477–1493 [Observed] | Serif with italic "explained" | Hard cut |
| 9 | 64.94 (1557) | 87.88 (2107) | 22.98 | US outline map. New England fills grey with a sans label. Zoom into New England, then people icons pop in over 2 rows, then a "36 %" Rep/Dem bar appears. | Zoom ×5.7, f1680–1752; staggered pop f1744–1790 [Measured] | Sans "New England"; serif title; red-plate "36 %" | Cut to interview |
| 10 | 87.92 (2108) | 95.97 (2301) | 8.09 | Interview (Farbod Faraji, home-office webcam) with lower third | Handheld/webcam (93 % active) | Lower third (see F) | Cut |
| 11 | 96.01 (2302) | 113.78 (2728) | 16.85 | 36 % graphic, then coloured New England districts. The districts explode into a 3×7 grid (f2460–2476), fade, and donut charts draw on (f2506–2524). People with blue heads then pop in by reading order (f2566–2602). | Several beats | Serif title | Hard cut |
| 12 | 113.82 (2729) | 131.26 (3147) | 17.44 | US map, Oklahoma highlighted, OK districts in purple, then a 31 % bar, donuts and red-head people | Several soft beats (false cuts 2917–3100) | Serif titles | Hard cut |
| 13 | 131.30 (3148) | 146.27 (3507) | 14.97 | Massachusetts districts (blue and grey), donuts, 30 % bar | Beats; f3284–3334 | Serif titles | Hard cut |
| 14 | 146.31 (3508) | 157.03 (3765) | 10.72 | Academic paper page, a blur-zoom into the abstract (f3548–3564), then highlighter wipes over 3 lines | Wipes [Measured] | Paper scan (LaTeX) | Hard cut |
| 15 | 157.07 (3766) | 171.50 (4112) | 14.47 | US map. A magnifier enters from the left and drifts right. Donuts show inside the lens and swap to elephant/donkey icons at about f4060. | Entry ease-out plus constant drift [Measured] | None | Cut to interview |
| 16 | 171.55 (4113) | 180.35 (4324) | 8.84 | Interview | Live | None | Cut |
| 17 | 180.39 (4325) | 185.10 (4438) | 4.75 | Loupe map with party icons (hold) | Static | None | Hard cut |
| 18 | 185.14 (4439) | 207.29 (4970) | 22.19 | 2021 German hemicycle builds (f4443–4471). Other parties dim; push to FDP with "92 seats". Lateral pan to "Bundestag constituencies" (f4670–4739). | Build, dim, push, pan [Measured] | Serif titles, sans "92 seats" | Hard cut |
| 19 | 207.33 (4971) | 217.09 (5205) | 9.80 | Constituency results map. Dots fly into a hemicycle (f5100–5110). Black "PROPORTIONAL REPRESENTATION" banner wipes on (f5118–5150). | Beats | Serif caps, white on black banner | Hard cut |
| 20 | 217.13 (5206) | 221.76 (5317) | 4.67 | Proportional bar (red / green / purple) with bracket lines; people drop in | Beat | None | Hard cut |
| 21 | 221.81 (5318) | 254.09 (6092) | 32.32 | Electoral-systems map: STV / Open list / Closed list / MMP on a PERSON----PARTY axis. Push into "Closed list" (f5523–5599). Animal-party icons (bird, frog, rabbit), bars "1 1 3", people circled by hand-drawn ellipses. | Push-in [Measured]; holds 84 % static | Serif labels, sans red "PERSON / PARTY" | Hard cut |
| 22 | 254.13 (6093) | 267.18 (6406) | 13.10 | Diagram, then Open-list zoom, then ballot checkbox columns | Beats | Serif | Hard cut |
| 23 | 267.23 (6407) | 280.03 (6714) | 12.85 | Four-party bar (bird, frog, rabbit, cat) "2 3 1 2" with people | Beats | Sans numerals on bar | Hard cut |
| 24 | 280.07 (6715) | 293.17 (7029) | 13.14 | MMP explainer: person and party ballot, regional map | Beats | Serif | Hard cut |
| 25 | 293.21 (7030) | 307.10 (7363) | 13.93 | Small dot hemicycle recolours; bars appear above it | 93 % static | None | Hard cut |
| 26 | 307.14 (7364) | 317.53 (7613) | 10.43 | Systems diagram, then zoom to STV | Beats | Serif | Cut to news |
| 27 | 317.57 (7614) | 320.32 (7680) | 2.75 | 3 local-news clips (CBS2 NY, NBC News Center Maine, "Election 2020") | Live | Broadcast | Hard cut |
| 28 | 320.36 (7681) | 356.81 (8555) | 36.45 | STV: a 5-rank grid with red numbered circles. Checks pop in. Horizontal bars grow (f7817–7861). Votes redistribute; a dashed threshold line carries a pin. | Bar grow [Measured] | Small sans numerals | Soft (false cut 8556) |
| 29 | 356.86 (8556) | 362.49 (8691) | 5.63 | Winners rise with yellow and grey confetti | Beat | None | Hard cut |
| 30 | 362.53 (8692) | 377.46 (9050) | 14.93 | Systems-diagram recap, then the title card returns | Beats | Serif | Cut |
| 31 | 377.50 (9051) | 379.63 (9102) | 2.13 | Recap: earlier graphics shown as rounded cream cards on a dark textured background (MA map, then hemicycle) | Card cut-swaps | Serif titles | Hard cut |
| 32 | 379.67 (9103) | 402.82 (9658) | 23.15 | Capitol and White House cut-outs; a president figure with a party pin on a stick; dot arcs appear over the Capitol | Many small beats on twos | None | Cut to interview |
| 33 | 402.86 (9659) | 407.82 (9778) | 4.96 | Interview | Live | None | Cut |
| 34 | 407.87 (9779) | 421.30 (10101) | 13.43 | US House hemicycle (2-party). An arc stroke draws round it. Recolours into multi-party segments, then shrinks and duplicates ×3. | Beats | None | Hard cut |
| 35 | 421.34 (10102) | 431.97 (10357) | 10.63 | District shapes with people regroup into multi-member districts | Beats | None | Hard cut |
| 36 | 432.01 (10358) | 456.62 (10948) | 24.61 | Oklahoma: grey, then red with elephant badges, then purple multi-party with mixed icons | Beats; 93 % static | None | Hard cut |
| 37 | 456.67 (10949) | 475.35 (11397) | 18.68 | US Code §2c document pan and highlighter. A halftone Capitol card slides in (f11293–11397). | Pan + wipe | Document scan | Cut to interview |
| 38 | 475.39 (11398) | 483.40 (11590) | 8.01 | Interview | Live | None | Cut |
| 39 | 483.44 (11591) | 495.37 (11877) | 11.93 | 5 press photos / footage of members of Congress, 1.4–3.3 s each | Near-static (0 % active) | None | Hard cuts |
| 40 | 495.41 (11878) | 509.76 (12222) | 14.35 | Halftone blue Capitol photo card, then state-capitol photos drop onto a pile over newspaper clippings | Drops every 20–28 f, drift on twos [Measured] | Clipping type | Cut to interview |
| 41 | 509.80 (12223) | 518.27 (12426) | 8.47 | Interview | Live | None | Cut |
| 42 | 518.31 (12427) | 526.65 (12627) | 8.34 | Title-card reprise (statue on podium) | Slow push | Serif | Cut |
| 43 | 526.69 (12628) | 537.70 (12892) | 11.01 | Interview | Live | None | Cut to black |
| 44 | 537.75 (12893) | 540.08 (12949) | 2.33 | Black; the credits column starts | None | None | Cut |
| 45 | 540.12 (12950) | 584.83 (14022) | 44.71 | Outro: dark credits roll on the left, presenter on a teal background on the right. Inserts: document (559.5 s) and four YouTube "Vox highlighter tutorial" thumbnails, 0.5–0.75 s each (565.6–568.0 s). | Credits scroll | Small serif / sans credits | Cut |
| 46 | 584.88 (14023) | 586.42 (14060) | 1.58 | Black | None | None | End |

## D. Motion catalog (numbers and evidence)

**D0. Graphics are animated on twos (12 fps) [Measured].**
- In animated graphic shots, frame-to-frame mad alternates moving and 0.0 on every other frame.
  - Example f2565–2611: 1.0 / 0.0 / 1.7 / 0.0 …
  - Example f9347–9361: 0.7 / 0.0 / 0.9 / 0.0 …
- 34 of 41 animated graphic shots show 100 % single-parity motion (median purity 1.00).
- The 7 "mixed" shots contain internal re-timed layers.
- The parity phase flips between shots, so each comp is rendered on 2s independently.
- Live footage, the interviews and the end credits move on every frame.
- **Reuse rule:** step every graphic animation to 12 fps and keep the camera and footage at 23.976.

**D1. Holds are truly static [Measured].**
- 66.4 % of all frames have mad < 0.5. The median mad inside long graphic shots is 0.00–0.03.
- No constant "breathing" drift is applied to most graphic holds.
- Exceptions: the title card (D2), the loupe (D6) and the photo stack (D13), which carry slow drift.

**D2. Title-card slow zoom and punch-in.** Measured from the box bounding box, f0–104.
- **Slow push.** Width goes from 684 px (f0) to 750 px (f72): about +0.13 % per frame, linear [Measured].
- **Punch-in.** On "WINS" (f72→f88) width goes from 750 to 972 px (×1.30) in 16 frames [Measured].
  - Progress at +2/+4/+6/+8/+10/+12/+14 frames: 0.20, 0.55, 0.74, 0.84, 0.90, 0.96, 0.99.
  - This is a strong ease-out: about easeOutCubic/Quart. ESTIMATE cubic-bezier(0.2, 0.8, 0.3, 1).
- The slow push then resumes at about 0.1 %/f (978→993 px over f92–104).
- **Word type-on is VO-synced, not on a fixed interval [Observed].** Each word appears in one step, with no fade:

| Word | Frame |
|---|---|
| THE | f12 |
| PERSON | about f17 |
| WHO | about f29 |
| GETS | about f35 |
| THE | about f38 |
| MOST | about f41 |
| VOTES | about f56 |
| WINS + podium | about f74 |

- Text is left-aligned inside the box at first. After the punch the block is re-centred.

**D3. Map zoom into a region.** US map → New England, f1680–1752.
- The grey New England region grows from 120 to about 690 px tall (×5.7) over 72 f (3.0 s) [Measured].
- Velocity peaks around f1721–1727 (about 60 % through), and the remaining 25 % takes about 25 f.
- Shape: ease-in-out with a long slow tail. ESTIMATE cubic-bezier(0.55, 0, 0.15, 1) on scale.
- The other states fade out during f1712–1728. The "New England" label wipes off at about f1696–1704 [Observed].

**D4. People-icon stagger [Observed + Measured].**
- After the zoom, B/W cut-out people pop in left→right over 2 rows, from f1744 to about f1790 (2 → 20 figures).
- Per-pair mad rises 2.1 → 6.8 → 1.0, peaking at f1769–1771.
- This means a pop roughly every 2-frame tick (about 0.08 s per figure). Figures appear at full size (pop, no scale tween visible at 8-frame sampling).
- Same pattern at f2566–2602: 21 figures in reading order, about 1.7 f each.

**D5. Explode → donut sequence (f2460–2524) [Observed].**
- Districts translate apart into a 3×7 grid in about 16 f.
- They fade to about 30 % over f2500–2512.
- Donut rings draw on radially in about 18 f, all at once with no stagger.
- People then replace the donuts as the donuts fade out.

**D6. Magnifier / loupe** (f3776–4112, ring tracked with `ring.py`).
- **Ring:** outer radius about 317 px (≈ 634 px diameter, 33 % of frame width). Dark grey rim with a soft shadow [Measured]. The contents are magnified and blurred at the edge.
- **Entry:** from off-frame left. cx = 308 (f3786) → 414 (f3790) → 492 (f3794) → 571 (f3800) → 626 (f3806) → 661 (f3812) → 683 (f3818) → 699 (f3826) [Measured].
  - Ease-out over about 40 f, peak about 27 px/f at the start.
- **Hold drift:** cx 699 → 896 px over f3826–4100. That is about 0.72 px/f (17 px/s), constant and linear [Measured].
- **Content swap:** donuts → party icons at about f4060, a hard swap inside the lens [Observed].
- **Loupe as transition (f1330–1423):** the loupe crosses the chart showing a different layer (the title card) inside the lens. Then the lens scales up until its interior fills the frame [Observed]. The scale curve was not tracked.

**D7. Document highlighter wipe** (f3540–3700, `hl.py`, yellow H 20–35, S > 120).
- Each line wipes left→right, with ease-in-out per segment and holds between segments (VO-synced).
- **Line 1:** right edge x 1041 (f3540) → 1767 (f3564).
- **Line 2:** x 489 → 1101 over f3578–3612 (612 px in 34 f). Per-2f increments: 12, 18, 30, 42, 42, 48, 48, 54, 54, 48, 48, 42, 30, 30, 15, 3. That is symmetric ease-in-out (sine-like); peak 27 px/f ≈ 650 px/s [Measured].
- **Line 2b:** x 1104 → 1791, f3618–3660 (684 px, 42 f).
- **Line 3:** x 141 → 627, f3660–3696 (486 px, 36 f).
- Whole-page drift during the wipes: line-end x creeps 1767 → 1803 (≈ 0.27 px/f) [Measured].
- **Lead-in:** blur-to-sharp zoom from the full page into the abstract, f3548–3564 (about 16 f) [Observed].

**D8. Bar growth, STV chart** (f7815–7862, `bars.py`).
- Bars grow from x = 522–528 px.
- **Bar 1 (blue)**, right edge per 2 f: 627, 810, 993, 1113, 1191, 1251, 1296, 1329, 1359, 1377, 1395, 1407, 1416, 1422, 1425 [Measured].
  - 903 px in about 30 f; 50 % at about 6 f; 90 % at about 14 f.
  - Shape: easeOutQuart. ESTIMATE cubic-bezier(0.25, 1, 0.5, 1).
- **Stagger:** bar starts at f7817, 7827, 7833, 7841, 7849, i.e. Δ = 10, 6, 8, 8 f (median 8 f ≈ 0.33 s). Overlap is about 75 % [Measured].
- **Earlier step:** checkmarks pop into the grid one at a time at VO beats (f7699–7807) [Observed].

**D9. Hemicycle builds.**
- **German build (f4443–4471):** 28 f (1.17 s). The dots sweep in by arc segments, all parties simultaneously [Observed]. The motion event is f4443–4471 [Measured].
- **Dim others:** non-focus parties drop to about 15–25 % opacity over about 20 f (f4520–4540) [Observed].
- **Push to FDP:** about f4570–4605. Then "92 seats" types on (f4590–4600) [Observed].
- **US House build (f9779–9795):** the 2-party arc completes in about 16 f.
  - A black arc stroke draws on clockwise (f9795–9819) and draws off (f9827–9851), 24 f each [Observed].
  - The segments then recolour in steps: green at about f9859, pink at about f9875, yellow at about f9899 (16–24 f apart) [Observed].
  - The arc then shrinks into the corner and copies stagger in at f9963 and f9987 (24 f apart) [Observed].

**D10. Lateral camera pan** (f4670–4739, phase correlation).
- Total 1675 px to the left in 68 f (2.85 s) [Measured].
- Per-2f displacement: 4, 15, 31, 54, 89, 139, 185, 185, 154, 123, 100, 83, 70, 60, 51, 45, 39, 35, 30, 27, 24 … 0.5.
- Peak velocity is at about 20 % of the duration and 50 % distance is reached at about 19 %. The ease-out is a long exponential tail.
- ESTIMATE cubic-bezier(0.55, 0, 0.1, 1); in After Effects terms, about 30 % in-influence and 85 % out-influence.
- No motion blur is visible [Observed].

**D11. Push-in on one diagram node** ("Closed list", f5523–5599, red bird bbox).
- Centre x moves 1636 → 989 px; bird height 126 → 201 px (×1.6). 76 f = 3.17 s [Measured].
- Progress at 26 / 42 / 53 / 63 / 74 / 89 % of time: 0.06, 0.20, 0.50, 0.75, 0.88, 0.97.
- That is symmetric easeInOutCubic: ESTIMATE cubic-bezier(0.65, 0, 0.35, 1).
- The other nodes fade out across f5559–5583 [Observed].

**D12. Lower-third build** (f2109–2160) [Observed].
1. Two small dots, red then blue, appear at the left edge (f2109) and travel. Their routes are not tracked.
2. The cream plate wipes on left→right (f2118–2121).
3. The name types on in caps: f2121 "F" → f2124 "FARBOD" → f2133 "FARBOD FARAJ" → done about f2135. That is 13 chars in about 14 f.
4. The italic role then types on, f2136 → about f2160: 26 chars in about 24 f, i.e. about 1 char per frame (≈ 24 chars/s).

**D13. Photo-stack drops** (f11954–12222).
- New photos land at f11954, 11979, 12003, 12029, 12053, 12081, 12101, 12121, 12141, 12161 [Measured: mad spikes 13–32].
- Intervals: 25, 24, 26, 24, 28, then 20, 20, 20, 20 f. The pace accelerates in the second half.
- Each drop is a hard swap with a slight random rotation (about ±3–5°) [Observed].
- The whole table drifts continuously on twos: mad about 4–6 on every other frame [Measured].

**D14. Series sting "America, explained"** (f1424–1556) [Observed].
- Square-tile mosaic cut-in of collage photos (f1424–1453).
- Words assemble from the centre: "ca" → "merica".
- The italic "explained" types on at about 2 f per letter (f1477–1493).
- A double hand-drawn ellipse scribbles around the title (about f1509–1517).
- A Vox logo pops inside a yellow circle at f1501–1509.

**D15. Banner wipe** (f5118–5150) [Observed].
- The black label bar extends left→right and the text is revealed as the bar passes: "PROPORTIONAL" by f5126, full text by f5150. About 32 f.

**D16. Pacing of animation beats inside graphic shots [Measured].**
- 77 significant motion events (sum mad ≥ 20) between 24 s and 538 s.
- Gap between beats: median 4.71 s, IQR 2.50–7.52 s.

## E. Transition catalog

| Type | Count / where | Evidence |
|---|---|---|
| Hard cut | 80 verified edits (93 candidates minus 13 false) | cut-frame mad 10–153 [Measured] |
| Hard cut on rhythm (montage) | 11 cuts in scenes 2–3, about 1.04 s (25 f) apart, plus 4-frame flash inserts | f383, 407, 432, 457, 482, 504, 533 [Measured] |
| Loupe/iris wipe (magnifier reveals the next layer, then fills the frame) | 1 (f1330–1423) | strip s_t1424 [Observed] |
| Tile-mosaic reveal | 1 (series sting f1424–1453) | [Observed] |
| Blur-zoom (defocus → refocus while scaling in) | 1 (f3548–3564) | [Observed] |
| In-comp camera move as transition (pan to the next chart) | f4670–4739 | D10 [Measured] |
| Push-in to a node (zoom-to-detail, the rest fades) | f5523–5599 and others (open-list, STV zooms) | D11 [Measured] |
| Region zoom (map → sub-region) | f1680–1752, f2729–2760 | D3 [Measured] |
| Fade / dissolve within a graphic (layers fade to about 20–30 %) | many (f2500, 4520, 5560 …) | [Observed] |
| Recap "cards on dark" (frame-in-frame) | f9051–9102 | [Observed] |
| Cut to/from interview | always a hard cut; no lower-third reuse after the first | [Observed] |
| Outro | hard cut to black (f12893) | [Measured] |

No whip-pans with blur, no glitch or film burns between graphics (the f332 film leader is footage), and no cross-dissolves between live shots were observed.

## F. Typography and layout

All sizes are at 1080p and measured from full-res frames unless marked otherwise.

| Role | Look | Measured / estimated size | Position | Font ID (ESTIMATE) → Google matches |
|---|---|---|---|---|
| Title-card headline | Heavy transitional/news serif, all caps, bracketed serifs. Distressed, ink-bleed edges. Black on cream. | Cap height about 93 px; line pitch 111 px (leading ≈ 1.19 × cap) at f150 after the punch [Measured] | Centred block inside a 10 px black rule box (box 492–1476 × 261–822 at f92) | Vox's proprietary serif (not identifiable) → **Source Serif 4 Black**, **Merriweather Black**, **Newsreader ExtraBold** |
| Chart titles ("Share of total House of Representatives votes, 2022") | Same serif family, semibold, sentence case, dark #24221B | Ascender-to-descender 52 px → cap ≈ 34–36 px [Measured/Inferred] | Centred, cx ≈ 964, top ≈ 92 px | Same as above, Semibold |
| Series legend labels ("Republicans", "Democrats", "Freie Demokratische Partei") | Serif bold, coloured to match the series or dark | Cap ≈ 34 px [Measured f4640: 375–412 incl. ascenders] | Above the bars, left-aligned to their segment | Same |
| Diagram labels ("Closed list", "Single transferable vote") | Serif regular/medium, sentence case, centred under the icon | Cap ≈ 34 px before zoom (≈ 55 px at ×1.6) [Measured f5590] | Under the icon | Source Serif 4 / Newsreader |
| Data labels ("92 seats", "New England", "Is a third party needed?", "Yes / No", axis ticks) | Neo-grotesk sans, regular/medium, dark | "92 seats" ≈ 30 px cap; axis ticks ≈ 10–12 px [Inferred from crops/sheets] | Next to the data | → **Inter**, **Public Sans**, **Work Sans** |
| Big numbers on bars ("36 %", "30 %", "1 1 3") | Sans bold, white on a red or blue plate | Plate height ≈ 75 px [Inferred] | Inside the bar's left segment | Inter Bold |
| Axis words ("PERSON ---- PARTY") | Small sans caps, coral red, dashed rule | ≈ 12 px cap [Inferred] | Mid-diagram | Inter Medium |
| Annotations ("PARTY YOU LEAST AGREE WITH", "A THIRD PARTY") | Hand-lettered marker caps, italic slant, pink #F0508A-ish, with hand-drawn arrows | ≈ 20 px cap [Inferred] | Near their targets | → **Permanent Marker** (lighter weight), **Gochi Hand**, **Kalam Bold** |
| Banner ("PROPORTIONAL REPRESENTATION") | Serif caps, cream on a black bar | Bar ≈ 45 px tall [Inferred] | Centred across the hemicycle | Source Serif 4 Semibold |
| Lower third, name | Bold serif caps, black, on a warm-cream plate #EEE4D8 | Ink rows 822–861 → cap ≈ 36 px [Measured f2200] | x = 139 px left edge (≈ 7.2 % margin); plate top ≈ 814 | Source Serif 4 Bold |
| Lower third, role | Bold-italic serif, black, on a second plate | Ink 879–924 (incl. descenders) → cap ≈ 28 px [Measured] | Directly below; plate bottom ≈ 916 px (164 px above the bottom edge) | Source Serif 4 Bold Italic |
| Series sting | Serif roman "America," plus italic "explained" | ≈ 70 px cap [Inferred] | Centred | Newsreader / Source Serif Italic |
| Watermark | "Vox" logotype, top-right, white at about 30–40 % (≈ 100 % white on footage) | ≈ 40 px tall [Inferred] | About 30 px from the top and right edges | Brand asset |

**Layout and grid**
- Charts and titles are centred on x ≈ 960. Chart titles sit at y ≈ 90–145 [Measured].
- Diagrams use roughly a 3-column arrangement (STV at left, Open/Closed list at upper middle / right, MMP at lower middle) [Observed].
- The background "graph paper" is a local patch, not full-frame [Measured c_grid]:
  - dashed hairlines with "+" ticks at intersections
  - cell pitch ≈ 48–49 px
  - placed in 1–2 corners or edges of each composition and fading out
- Margins: the left lower-third edge is 139 px; the graphics keep about 90–140 px safe margins [Measured/Inferred].

## G. Color and texture

| Swatch | HEX | Source (frame / region) | Status |
|---|---|---|---|
| Paper cream (background) | **#F6F6EA** (alt #F6F6EE) | modal colour, f0, f150, f4470, f10430 / f1870, f6545, f7860 | Measured |
| Grid-line core | **#CDCCC2** (darkest 1 %); AA mean #F1EFE5 | f0 x 1500–1880, y 60–400 | Measured |
| Body / title ink | **#24221B** (dark mean) | f0, f150 | Measured |
| Republican red (data charts) | **#FA3727** / **#FC3215** | f1870 36 % bar; f10430 OK map | Measured |
| Democrat blue | **#51B7FD** / **#4CB4FE** / #45AFFD | f1870, f7860, f3453 | Measured |
| Coral red (explainer bars, bird party, PERSON axis) | **#E96450** / #E96653 | f7860, f6545 | Measured |
| Green (party / Greens / frog) | **#5DBC7E** / #63C482 / #5CB975 | f4470, f6545, f7860 | Measured |
| FDP yellow / podium yellow | **#FAF023**; podium **#FCED1A** | f4470 / f150 | Measured |
| Highlighter on scanned docs | **#EEDF2F** (multiplied over grey paper #F2F2F2) | f3740 | Measured |
| Pink (Other / Yes / pink party) | **#FB96C0** / #FA95BD | f1870, f9910 | Measured |
| Purple (Linke-like / rabbit / OK map) | **#BE71AD** / #C47CC5 | f4470, f6545 | Measured |
| Slate blue (cat party) | **#698ACD** | f6545 | Measured |
| Lower-third plate | **#EEE4D8** | f2200 at (818,150), (866,150), (912,300) | Measured (may be semi-opaque) |
| Recap background | dark charcoal ≈ #2A2A28 with texture | f9051–9102 | Estimated |
| Outro credits background | ≈ #2B2B2B; presenter background teal ≈ #3FD0C0 | sheet 8–9 | Estimated |

**Texture**
- **Paper:** a flat cream fill. A 100×100 px patch at f0 has std 0.0, so there is no animated grain in flat areas [Measured].
- **Vignette:** none. The four corner luma values equal the centre value (244) at f0 [Measured].
- **Printed feel** comes from the assets themselves [Observed]:
  - B/W halftone cut-out people and buildings (Capitol, White House, statue)
  - Halftone blue photo cards with deckled white borders and drop shadows
  - Scanned ballots and documents with grain
  - Distressed type on the title card
- **Drop shadows:** soft and offset down-right on cut-outs and photo cards. About 8–12 px blur, ≈ 20–30 % black [Estimated]. The title statue has an elongated cast shadow to the lower-left [Observed].
- **Interview grade:** warm practical light, slightly lifted shadows, webcam softness; not stylised [Observed]. The mean luma of interview shots is 124–129 against about 235 for graphics [Measured].

## H. Pacing statistics

Shot set = 80 verified cuts → 81 shots [Measured, work/pace.py].

**All 81 shots:** mean 7.24 s, median 3.34 s, min 0.17 s (4-frame flashes), max 42.17 s (credits-heavy outro segment).

**Pre-credits body (71 shots):** mean 7.57 s, median 4.67 s.

| Category | Shots | Screen time | % of runtime | Mean shot | Median shot |
|---|---|---|---|---|---|
| Motion graphics | 31 | 406.3 s | 69.3 % | 13.1 s | 13.1 s |
| Documents / ballots / photos | 15 | 56.9 s | 9.7 % | 3.8 s | 1.0 s |
| Interview (one guest, 6 takes) | 6 | 49.5 s | 8.4 % | 8.3 s | 8.3 s |
| Archival / news | 19 | 25.0 s | 4.3 % | 1.3 s | 1.04 s |
| Credits / outro / black | 10 | 48.7 s | 8.3 % | 4.9 s | 2.0 s |

- **Graphic : interview ratio** ≈ 8.2 : 1 by screen time. Interviews are placed as about 8 s "breathers" every 60–120 s (at 88, 172, 403, 475, 510, 527 s) [Measured].
- **Cut density per minute:** 26, 6, 5, 5, 4, 5, 6, 4, 11, 9. The cold open is a fast montage at about 1 s per shot. The middle is long graphic shots with internal animation beats (median 4.7 s apart, D16). The back third has more interview cutting and the photo stack.
- **Shot length:** 24 shots last ≥ 10 s and 26 shots last ≤ 1.1 s. The distribution is bimodal: rapid montage versus long explainer comps.
- **Static share:** 66.4 % of frames are static (mad < 0.5). Overall mean mad is 1.30 [Measured: cuts.json].

## I. Uncertainties

- **Fonts:** Vox uses proprietary faces. The Google matches are visual approximations only. Annotation-lettering size and colour are estimated from 640 px thumbnails, not full-res.
- **Easing:**
  - Curves are fitted from 2-frame (on-twos) samples, so each value carries ±1 frame of quantisation.
  - The bezier values are ESTIMATES.
  - The map-zoom curve was measured on a bbox that includes label remnants early on (f1680–1696).
  - The loupe-wipe scale (f1389–1423) and the lower-third dot paths were not tracked numerically.
- **Bounding-box tracking** at 640×360 gives ±3 px precision at 1080p. Phase correlation in the pan has a confidence of 0.67–0.72 at peak speed (f4687–4691).
- **Scene classification:** the category of each shot was assigned by range from sheets and strips. Short shots inside montages (f212, 260, 310, 4-frame flashes) were seen only as thumbnails. Their content (flash frame vs. blur transition) is uncertain.
- **Long holds:** frames inside long graphic holds and interview takes were not all opened. Claims about them rest on framediff numbers.
- **Colours:**
  - The colours are from H.264 4:2:0 decodes, so saturated edges blur. K-means centres may blend anti-aliased pixels.
  - The lower-third plate colour may include footage showing through.
  - The outro and recap background colours are estimated, not measured.
- **Shadow parameters** (blur and opacity) are visual estimates.
- **Outro:** the meaning of the YouTube-thumbnail inserts (565–568 s) is outside the motion scope. They were noted only as rapid 0.5 s inserts.
