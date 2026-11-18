# V1_porsche — Motion-Graphics Forensic Breakdown

"VOX-Style Animated Documentary: The History of Porsche"

Tags: **[Observed]** = seen in frames I opened. **[Measured]** = computed by script from pixels. **[Inferred]** = reasoned from evidence, not directly verified.
Frame numbers are 0-based at 30 fps; t = frame/30.
Montage files are in `work/` (`cut_XX.jpg`, `ov_X.jpg`, `d_*.jpg`). They are built from `work/f/NNNNN.jpg`, which holds all 5899 frames at 320x180.
Scripts are in `work/` too: `seg.py act.py cad.py ybox.py zoom.py bars.py tvbox.py pbox.py col.py stats.py`.

---

## A. Inventory

| Field | Value |
|---|---|
| Source | `/mnt/c/Users/rabin/Downloads/Refernace/YTDown.com_YouTube_Media_FwRtt4nhCDE_VOX-Style-Animated-Documentary-The-History-of-Porsche_001_1080p.mp4` (read-only, not modified) |
| Resolution / fps | 1920x1080, 30 fps (CFR) |
| Frames / duration | 5899 / 196.70 s |
| Audio | AAC stereo 44.1 kHz (not analysed here) |
| Mean frame MAD | 5.87. Static fraction (MAD < 0.5) is 44.4% [Measured, cuts.json] |

## B. Inspection record

- **Numeric (all 5899 frames).** framediff.tsv (MAD, histogram distance, luma) was used for cuts, per-second activity and update cadence [Measured].
- **Extra numeric tracking at full 1080p, every frame:**
  - yellow-box bbox: 1216–1250, 420–482
  - portrait rise: 484–500
  - bar heights: 3930–4035
  - TV scale: 2404–2414
  - card bbox: 134–160
- **ORB-affine zoom/translation (from the 320 px frames):**
  - 2–124 (step 2), 342–520 (step 2)
  - 777–846 (step 3), 1036–1050, 1105–1120
  - 1363–1385, 3300–3334 (step 2), 5376–5398
  - 5450–5544 (step 6), 5546–5720 (step 6)
- **In-TV screen diff:** 2405–2529.
- **Frames opened visually.** Tiles are counted per view, overlaps included, ≈ 2,400 in total:
  - 5 contact sheets: 96 uniform frames every 2 s.
  - 13 cut montages (`cut_00..12`): 102 candidates × 8 frames (c-3…c+4) = 816 tiles.
  - 5 overview montages (`ov_0..4`): every 10th frame across the whole video, 590 tiles.
  - 17 dense montages, 907 tiles:

| Montage | Range | Step |
|---|---|---|
| card356 | 1216–1271 | 1 |
| intro | 0–158 | 2 |
| mapde | 342–520 | 3 |
| year | 729–780 | 1 |
| hybrid | 777–940 | 3 |
| timeline | 940–1110 | 3 |
| quote | 1105–1216 | 2 |
| chart | 1485–1600 | 2 |
| bars | 3927–4040 | 2 |
| money | 5300–5400 | 2 |
| words | 5399–5550 | 3 |
| curl | 124–172 | 1 |
| c911 | 1925–1960 | 1 |
| tv | 2398–2440 | 1 |
| news | 3270–3330 | 2 |
| coll | 3425–3700 | 5 |
| dark | 4030–4262 | 4 |

- **Full-res crops** (`work/full/`, `work/typesheet.jpg`): frames 180, 450, 810, 1140, 1260, 1300, 1720, 3960. Colours were also sampled from 360, 960, 1980, 2160, 4320, 4500, 5460, 5760.
- **Sampling intervals:** 2 s (sheets) and 10 frames (overview) across the whole video. Dense sampling (1–3 frames) is limited to the ranges listed above.
- **Not opened frame-by-frame:**
  - 527–729 (beyond cut windows)
  - 1595–1662, 1684–1760
  - 2178–2246, 2529–3000 (except cut windows)
  - 3099–3278, 3700–3927, 4256–5300
  - These ranges are covered at 10-frame density only.

## C. Scene / shot table

The shot list (108 shots) is in `work/shots.txt`. Boundaries come from cuts.json, verified visually. I removed 241, 1461/1466 (merged), 1662/1666/1684 (merged into one crumple transition) and 5868 (a fade, not a cut). I added soft or in-frame boundaries at 130, 1935, 2270, 2275, 2424, 2455, 2484 and 3445–3655.
"Card" means a cut-out car on paper. "Footage cap" means the lower-third ▶ + yellow italic line.

| # | start t (f) | end t (f) | dur f | description | camera / object motion | typography | transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 (0) | 4.30 (129) | 130 | Political/physical world map. Traffic-footage thumbnails (rounded corners, soft drop shadow) pop on around the globe. | Zoom-out 8.8x, ease-out, frames 2–114. Radial zoom blur in frames 0–8 [Measured/Observed] | none | Page-curl peel from bottom-right corner, 126–136 (~10 f) [Observed] |
| 2 | 4.33 (130) | 6.63 (199) | 70 | Hypercar footage. Full-bleed footage shrinks into a rounded inset card on black. Yellow ▶ + italic word ("passion") | Card shrink ~136–150. ▶ spins between frames [Observed] | serif italic word, centered under the card | hard cut (frame swaps inside card) |
| 3 | 6.67 (200) | 7.43 (223) | 24 | Same card layout, new clip | in-clip motion | italic word | hard cut |
| 4 | 7.47 (224) | 8.27 (248) | 25 | Card, rear-view 911. Word changes at 241 (word-swap anim) | in-clip | italic word re-types | hard cut |
| 5 | 8.30 (249) | 9.13 (274) | 26 | Card, SUV | in-clip | italic word | hard cut |
| 6 | 9.17 (275) | 11.37 (341) | 67 | Card, sedan in street | in-clip; footage motion blur at end | italic word | hard cut (to bright map) |
| 7 | 11.40 (342) | 17.53 (526) | 185 | Europe map, zoom to Stuttgart. Pin dot, yellow city outline, "STUTTGART" label with speech-bubble highlight. Then 2 portraits rise from the bottom while the map dims; "Ferdinand Porsche" label | Zoom-in 30x over 346–406 (log ease-in-out) with directional motion blur. Portrait rise 484–~502 | heavy serif caps label; serif label in yellow box | dissolve with B&W footage, 527–~533 |
| 8 | 17.57 (527) | 18.97 (569) | 43 | B&W archival: man drawing car sketches | slight drift | none | hard cut |
| 9 | 19.00 (570) | 19.77 (593) | 24 | Dark studio, modern Taycan, orange light-line sweeps over the body | light sweep | none | hard cut |
| 10 | 19.80 (594) | 22.87 (686) | 93 | Macro of light bar/badge; Porsche crest dissolves in ~630–650 | slow push | none | dissolve 687–~692 |
| 11 | 22.90 (687) | 24.27 (728) | 42 | Sepia archival, Porsche at drafting board, then man in suit (internal dissolve ~690) | archival motion | none | hard cut to paper |
| 12 | 24.30 (729) | 25.77 (773) | 45 | Paper bg, centre year counter 2024→1900. Yellow highlight grows behind "1900" | counter steps at ~12 fps | serif numerals | dissolve 774–777 (3 f) |
| 13 | 25.80 (774) | 28.27 (848) | 75 | B&W photo of early car + passengers. Label "one of the first *hybrid* vehicles" typed in yellow box | scale settle 777–792, then slow push +2.5% | serif label, italic emphasis word | dissolve 847–852 |
| 14 | 28.30 (849) | 31.30 (939) | 91 | Paper ad "EGGER-LOHNER". Highlighter wipe 858–882. Layout then shrinks/slides into a 3-image collage (~894–909) | layout reflow | engraved ad type (source art) | hard cut to dark |
| 15 | 31.33 (940) | 36.80 (1104) | 165 | Dark map texture, horizontal timeline with dot; years scroll 1900→1948. Photo of two men slides in from the right (1036–1048). Yellow ring drawn around one head (1051–1060). Label typed (1066–1090) | year slides L with fade. Photo slide ~12 f | light serif numerals, white | hard cut (to paper) |
| 16 | 36.83 (1105) | 40.50 (1215) | 111 | Paper; cut-out portrait with offset yellow outline. Quote words fade in sequentially; attribution line follows | zoom-out 1.75x, 1106–1119 | serif italic quote, small caps-ish attribution | hard cut |
| 17 | 40.53 (1216) | 42.33 (1270) | 55 | Car card: Porsche 356 cut-out. Title typed into a growing yellow box; price line fades in | static car | serif title in yellow box + small serif price | hard cut |
| 18 | 42.37 (1271) | 44.50 (1335) | 65 | B&W factory footage + footage cap | archival | ▶ + yellow serif italic caption | hard cut |
| 19 | 44.53 (1336) | 45.40 (1362) | 27 | B&W 356 in front of palace | archival | — | photo slide |
| 20–25 | 45.43 (1363) – 49.47 (1484) | | 20 each (21 for last) | Photo-slide carousel on paper: B&W factory/356 photos in thin yellow-edged frames, each replaced by a horizontal push | slide ~4 f (−739 px in 2 f) every 20 f | none | horizontal push ×5. Last one is a hard cut to dark |
| 26 | 49.50 (1485) | 53.13 (1594) | 110 | Dark blueprint bg; line chart; yellow line draws 1487–~1565; yellow title typed | line draw ~78 f, 6 fps steps | yellow serif title, white serif axis labels | hard cut |
| 27 | 53.17 (1595) | 55.73 (1672) | 78 | B&W 356 on mountain road + footage cap | archival pan | caption | crumpled-paper wipe up 1662–1684 |
| 28 | 55.77 (1673) | 58.67 (1760) | 88 | Crumpled paper texture; dashed-line box; typewriter text "But the true *revolution* came in 1963" with year highlight | static | serif roman + italic emphasis | hard cut |
| 29 | 58.70 (1761) | 60.00 (1800) | 40 | B&W design office | archival | — | hard cut |
| 30 | 60.03 (1801) | 61.90 (1857) | 57 | B&W three men talking | archival | — | hard cut |
| 31 | 61.93 (1858) | 64.47 (1934) | 77 | Car card: red 911, title + price | static | title box | focus-ring dissolve 1930–1950 |
| 32 | 64.50 (1935) | 67.63 (2029) | 95 | Green-tinted 1960s 911 footage + caption | archival | caption | hard cut |
| 33 | 67.67 (2030) | 69.13 (2074) | 45 | Faded colour factory footage; yellow circle spot + "rear-engine design" label | — | yellow-box italic label + leader line | hard cut |
| 34 | 69.17 (2075) | 70.97 (2129) | 55 | Paper; engine technical drawing, yellow filled circle behind; label "powerful six-cylinder engine" | circle scale-in | yellow-box serif italic label + line | hard cut |
| 35 | 71.00 (2130) | 72.57 (2177) | 48 | Paper; 911 blueprint views, yellow circle + "unique design" label | same | same | hard cut |
| 36 | 72.60 (2178) | 74.83 (2245) | 68 | B&W lot of 911s + caption | slight pan | caption | hard cut |
| 37 | 74.87 (2246) | 75.63 (2269) | 24 | Vintage ad collage ("1963 PORSCHE") | moving/pan (MAD 39–52 per frame) | source art | hard cut [Inferred from MAD 77] |
| 38 | 75.67 (2270) | 75.80 (2274) | 5 | Ad close-up | — | — | hard cut |
| 39–48 | 75.83 (2275) – 78.70 (2361) | | 5–15 each | Rapid newspaper-headline montage. The word "Porsche" is highlighted yellow and lands at the same screen spot in each clip | static per clip, vignette | newspaper headline type | hard cuts: 2280, 2285, 2300, 2310, 2315, 2320, 2335, 2340, 2350 |
| 49 | 78.73 (2362) | 80.13 (2404) | 43 | B&W US map with car icons; yellow brush-stroke region with small serif text | — | small serif | hard cut |
| 50 | 80.17 (2405) | 80.77 (2423) | 19 | Cream grid paper; retro TV with crest footage. Boiling doodle shapes (yellow/black triangles, circles, rects) | TV scale-pop 2405–~2416 | none | in-TV channel cut |
| 51 | 80.80 (2424) | 81.80 (2454) | 31 | TV: engine factory footage | doodles jitter | — | in-TV cut |
| 52 | 81.83 (2455) | 82.77 (2483) | 29 | TV: archive assembly footage | doodles | — | in-TV cut |
| 53 | 82.80 (2484) | 84.27 (2528) | 45 | TV: engine close-up | doodles | — | hard cut |
| 54 | 84.30 (2529) | 85.93 (2578) | 50 | Paper with faint blueprint; card "1969" with underline draw | slight float | serif numerals | hard cut |
| 55 | 85.97 (2579) | 87.93 (2638) | 60 | Car card: 914 | static | title + price | hard cut |
| 56 | 87.97 (2639) | 89.00 (2670) | 32 | Framed photo of purple 914 on paper | hold | — | hard cut |
| 57 | 89.03 (2671) | 90.10 (2703) | 33 | Larger framed photo, different angle | — | — | hard cut |
| 58 | 90.13 (2704) | 91.17 (2735) | 32 | Framed photo, 914 with model | — | — | hard cut |
| 59 | 91.20 (2736) | 92.60 (2778) | 43 | Faded 70s 914 driving footage | handheld | — | hard cut |
| 60 | 92.63 (2779) | 94.90 (2847) | 69 | Car card: 924 | static | title + price | hard cut |
| 61 | 94.93 (2848) | 95.57 (2867) | 20 | Framed yellow 924 ad photo | — | — | hard cut |
| 62 | 95.60 (2868) | 96.90 (2907) | 40 | Close-up of the same ad, text line with word highlight | push | italic serif | hard cut |
| 63 | 96.93 (2908) | 98.03 (2941) | 34 | Gold 924 on turntable | — | — | hard cut |
| 64 | 98.07 (2942) | 99.97 (2999) | 58 | Car card: 928 | static | title + price | hard cut |
| 65 | 100.00 (3000) | 103.27 (3098) | 99 | Paper; 3/4 cut-out 928; magnifying glass slides in and over the car | glass translation (12 fps) | — | hard cut |
| 66 | 103.30 (3099) | 106.80 (3204) | 106 | Framed 928 Paris street footage + caption | footage | caption | hard cut |
| 67 | 106.83 (3205) | 109.23 (3277) | 73 | Car card: 944 | static | title + price | hard cut |
| 68 | 109.27 (3278) | 114.30 (3429) | 152 | Magazine page on paper; hold then zoom-in 2.25x (3302–3334) to headline; highlight on text | zoom ease-in-out | magazine serif | hard cut to dark |
| 69–74 | 114.33 (3430) – 123.17 (3695) | | 15–55 | Dark textured layered collage. Group photo, sparks, body shell, engine, yellow line, "1996" in an oval. Long overlapping dissolves (soft boundaries ≈3445, 3485, 3535, 3580, 3620, 3655) | slow drift; blend layers | yellow serif "1996" types in | hard cut to paper |
| 75 | 123.20 (3696) | 125.20 (3756) | 61 | Car card: Boxster | static | title + price | hard cut |
| 76 | 125.23 (3757) | 126.27 (3788) | 32 | Boxster forest-road footage, fast pass | footage | ▶ appears | hard cut |
| 77 | 126.30 (3789) | 128.03 (3841) | 53 | Boxster footage + caption | — | caption | hard cut |
| 78 | 128.07 (3842) | 130.87 (3926) | 85 | Boxster footage + caption | — | caption | hard cut |
| 79 | 130.90 (3927) | 134.50 (4035) | 109 | Paper; bar chart "Porsche Global Sales Numbers". 8 dark bars grow staggered; yellow grid lines; red hand-drawn circle | see D | serif title + small source line | hard cut to dark |
| 80 | 134.53 (4036) | 138.27 (4148) | 113 | Dark bg; white-bordered photos slide across and stack (factory/HQ) | slides with motion blur | — | cut to near-black |
| 81 | 138.30 (4149) | 139.93 (4198) | 50 | Near-black; "SUV" in yellow box typed | — | serif | hard cut |
| 82 | 139.97 (4199) | 141.83 (4255) | 57 | Yellow-edged portrait photos pop in one by one; "2002" types | pop-ins | yellow serif year | hard cut to paper |
| 83 | 141.87 (4256) | 145.17 (4355) | 100 | Car card: Cayenne | static | title + price | hard cut |
| 84 | 145.20 (4356) | 146.17 (4385) | 30 | Framed Cayenne photo on paper | — | — | hard cut |
| 85 | 146.20 (4386) | 147.17 (4415) | 30 | Framed desert aerial | — | — | hard cut |
| 86 | 147.20 (4416) | 148.17 (4445) | 30 | Framed canyon photo | — | — | hard cut |
| 87 | 148.20 (4446) | 149.10 (4473) | 28 | Framed factory footage | — | — | hard cut |
| 88 | 149.13 (4474) | 150.20 (4506) | 33 | Framed factory | — | — | hard cut |
| 89 | 150.23 (4507) | 151.00 (4530) | 24 | Framed factory | — | — | hard cut |
| 90 | 151.03 (4531) | 152.10 (4563) | 33 | Framed gearbox worker | — | — | hard cut |
| 91 | 152.13 (4564) | 154.13 (4624) | 61 | Car card: Panamera | static | title + price | hard cut |
| 92 | 154.17 (4625) | 156.27 (4688) | 64 | Panamera pair footage + caption | footage | caption | hard cut |
| 93 | 156.30 (4689) | 158.10 (4743) | 55 | Car card: Macan | static | title + price | hard cut (1-f flash 4743) |
| 94 | 158.13 (4744) | 160.50 (4815) | 72 | Red Macan on bridge + caption | footage | caption | hard cut |
| 95 | 160.53 (4816) | 161.90 (4857) | 42 | Modern factory | footage | — | hard cut |
| 96 | 161.93 (4858) | 163.77 (4913) | 56 | Worker in orange | footage | — | hard cut |
| 97 | 163.80 (4914) | 165.27 (4958) | 45 | Wheel/brake assembly | footage | — | hard cut |
| 98 | 165.30 (4959) | 166.60 (4998) | 40 | Wheel mounting | footage | — | hard cut |
| 99 | 166.63 (4999) | 168.67 (5060) | 62 | Car card: Taycan | static | title + price | hard cut |
| 100 | 168.70 (5061) | 170.13 (5104) | 44 | Taycan city footage | footage | — | hard cut |
| 101 | 170.17 (5105) | 172.23 (5167) | 63 | Taycan footage + caption | footage | caption | hard cut |
| 102 | 172.27 (5168) | 173.37 (5201) | 34 | Taycan close-up + caption | footage | caption | hard cut |
| 103 | 173.40 (5202) | 174.00 (5220) | 19 | White Taycan + caption | footage | caption | hard cut |
| 104 | 174.03 (5221) | 179.93 (5398) | 178 | Two green Taycans, desaturated concrete. "2023" fades. Number "$43 000 000 000" fades in gray, then yellow wipe | push / pull; ease-in punch at end 5392–5398 | serif numerals | hard cut |
| 105 | 179.97 (5399) | 184.80 (5544) | 146 | CRT-shaped paper "screen" with dark bezel. Slot-machine word list scrolls through a box and lands on "Legacy"; yellow brush stroke | punch-in 1.4x (~5456–5468), creep +5% | serif words | hard cut |
| 106 | 184.83 (5545) | 190.67 (5720) | 176 | Desk collage: polaroid-style photos, yellow tape, pencils, paper clips, tagged labels ("911", "Boxster", "Macan") | push-in 1.38x (5546–5558), drifting pan, pull-back 5708–5720 | serif tag labels | hard cut to white |
| 107 | 190.70 (5721) | 196.63 (5898) | 178 | Grid paper with crop marks; seated founder cut-out with yellow offset outline; quote typed + attribution | static | serif italic quote | fade to black, ~5840–5898 |

## D. Motion catalog

Cadence (applies throughout) [Measured, cad.py]:
- Graphic animation updates on **2/3-frame alternation, i.e. ~12 fps on a 30 fps timeline**:
  - year counter 729–774
  - title box 1221–1243
  - magnifier 3000–3099 (gaps 2:19, 3:20)
  - bar chart
  - collage
- Typewriter and line-chart steps are often 5 f (6 fps).
- Camera moves on map/photo layers (0–130, 345–520) and live footage update every frame (30 fps).
- Static holds are pixel-identical (MAD = 0). No animated grain layer runs during holds.

| # | Pattern | Evidence | Parameters |
|---|---|---|---|
| D1 | **Car-card title reveal** (×11: 356, 911, 914, 924, 928, 944, Boxster, Cayenne, Panamera, Macan, Taycan) | `d_card356.jpg`, `ybox.py 1216–1250` | Car cut-out is already static at the cut [Observed]. Title starts 5 f after the cut (1221) as a 29 px yellow bar. The box left edge is fixed at x≈666–672; the right edge grows as characters type, ending 1243 (**22 f**) [Measured]. Width (px): 29, 56, 90, 141, 279, 457, 503, 536, 560, 579 at f+0, 2, 5, 7, 10, 12, 15, 17, 20, 22 → S-curve, ease-in-out-like, driven by typewriter, ~2 f/char, 12 fps steps [Measured/Inferred]. Final box 579x~135 px (x 671–1250, y 181–316), centred at x=960 [Measured]. Price line fades in after ~1230–1245 [Observed]. Hold to the cut: ~25–60 f |
| D2 | **Map zoom-out with photo pop-ins** (intro) | `d_intro.jpg`, zoom.py 2–124 | Scale 1→0.114 (8.8x) over frames 2–114 (112 f). Fraction of log-zoom done: 0.29 @f10, 0.63 @f30, 0.87 @f60, 0.98 @f90 → **ease-out between cubic and quart**. ESTIMATE cubic-bezier(0.2, 0.8, 0.3, 1) applied in log-scale [Measured/Inferred]. Radial zoom blur in frames 0–8. Thumbnails appear continuously, staggered every ~3–8 f, at the edges [Observed] |
| D3 | **Map zoom-in to city** | `d_mapde.jpg`, zoom.py 342–520 | 30x zoom over 346–406 (**60 f**). Log progress: 7.5% @360, 22% @370, 47% @380, 66% @386, 85% @392, 97% @400 → asymmetric ease-in-out, peak velocity at ~60% of the duration (1.26x per 2 f). ESTIMATE cubic-bezier(0.55, 0, 0.35, 1) in log space. Directional motion blur at peak (378–396) [Measured/Observed] |
| D4 | **Pin → outline → label** | `d_mapde.jpg` | Red pin dot grows 402–414 (~12 f). Yellow outline (#ECE048) draws on 417–~430. Label "STUTTGART" (dark heavy serif) fades on ~423–426. Yellow speech-bubble highlight wipes L→R, right edge 1069→1361 px between 435 and 446 (~11 f, decelerating: +55, +63, +44, +36, +20 … px) → ease-out. Hold ~19 f. Wipe-off R→L 465–471 (6 f, faster), text removed with it [Measured/Observed] |
| D5 | **Photo rise from bottom** | pbox.py 484–500 | Top edge y 931→172 (≈760 px) over ~16–18 f. Per-frame Δ: 21, 28, 36, 44, 55, 68, 78, 82, 79, 68, 54, 44, 36, 27, 22, 17 → **symmetric ease-in-out (sine/cubic), ~18 f**. Two portraits move together; the map dims under them [Measured] |
| D6 | **Year counter** | `d_year.jpg` | 2024→1900 in 11 discrete values over 729–757 (28 f, 12 fps). Steps −6, −11, −13, −14, −15, −14, −15, −13, −12, −8, −3 → ease-in-out on the value. Yellow highlight grows L→R behind the number from 749 to 759 (~10 f), overlapping the counter's last steps. Then a 3 f dissolve to a photo [Measured from frames] |
| D7 | **Highlighter wipe on existing text** | `d_hybrid.jpg`, EGGER-LOHNER 858–882; "$43 000…" 5326–5345 | L→R wipe, flat yellow (#F6EA00-ish) rectangle behind text, 19–24 f. Starts thin (~1 char) and decelerates [Observed]. The money number first fades in as gray text, ~5310–5320, then is highlighted |
| D8 | **Typed label in yellow box** (photo callouts) | 789–807, 1066–1090, 4166–4174 "SUV" | Box grows with characters, as in D1, 15–25 f. Optional leader line (2075–2177) [Observed] |
| D9 | **Ring / circle draw** | 1051–1060 (yellow ring round head); 4005–4011 (dark-red hand-drawn ellipse on chart) | Stroke-on, 6–10 f. Ring stroke ≈ 10 px yellow; ellipse ≈ 4 px #8B1A1A-ish [Observed; colour estimate] |
| D10 | **Filled yellow circle behind object** | 2075–2177 | Circle (#F4E900) scales in behind the engine/blueprint; label follows [Observed]. Duration not measured |
| D11 | **Quote reveal + portrait zoom-out** | `d_quote.jpg`, zoom 1105–1120 | Scale 1→0.57 (1.75x) over 1106–1119 (13 f). Per-frame ratio peaks at 1112 → **ease-in-out, ~14 f** [Measured]. Words fade in one at a time from light gray to dark, ~2 f/word, 1113–~1150. Attribution fades ~1147–1160 [Observed] |
| D12 | **Timeline year scroll** | `d_timeline.jpg` 952–1015 | Years slide R→L along a thin glowing line with a centre dot. Each year fades and slides in from the right and exits left (~6–9 f each). Lands on 1948 [Observed] |
| D13 | **Photo horizontal push carousel** | 1363–1466 | Every 20 f, the next framed photo enters from the right: −739 px in 2 f, then −121 px, settled within ~4 f. Very fast ease-out "whip" push [Measured] |
| D14 | **Line chart draw** | `d_chart.jpg` | Axes present at cut. Yellow line draws L→R 1487–~1565 (~78 f), roughly linear in x, stepped at 5 f (6 fps). Title types 1513–1525 [Observed/Measured cadence] |
| D15 | **Bar-chart stagger** | bars.py | 8 bars (77 px wide, 127 px pitch, x 520–1485). Start frames 3939, 3946, 3949, 3954, 3959, 3964, 3969, 3974 → **stagger ≈ 5 f**. Each bar reaches ~90% in ~12 f and settles ~20 f → ease-out (cubic-like), no overshoot detected. Heights morph again ~3990–4005 (data change) [Measured] |
| D16 | **TV scale-pop** | tvbox.py 2405–2414 | TV width 967→1365 px (start ≈ 71% of final). Δ/frame: 108, 89, 66, 45, 32, 22, 17, 12, 7 → **ease-out expo (≈0.75 decay per frame), ~10–12 f**, no overshoot through 2414. Doodle shapes "boil" (re-drawn every 2–3 f) [Measured/Observed] |
| D17 | **Footage → inset card shrink** | `d_curl.jpg` 136–150 | After the page curl, full-bleed footage scales down to a rounded-corner card ≈ x 240–1745, y 65–865 (ESTIMATE from 6 s sheet) on black. ~12 f, ease-out [Observed; estimate] |
| D18 | **Footage caption (lower third)** | 1300, 1980, 3099–3204, 3789–3926, 4625–4688, 5105–5220 | Black ▶ (or yellow ▶ on dark) at x≈160–215, then yellow italic serif sentence at baseline y≈950–960, left-aligned at x≈230. Text typed L→R; held on screen [Observed] |
| D19 | **Magnifier pass** | 3000–3099 | Magnifying-glass cut-out slides from the left over the car, then holds on the wheel; 12 fps steps [Observed] |
| D20 | **Article zoom** | zoom.py 3300–3334 | 1→2.25x over ~32 f. Per-step ratio peaks at 3316–3322 → ease-in-out [Measured] |
| D21 | **Punch-in + creep** (legacy screen) | zoom.py 5450–5544 | 1.0→1.40 in ~12 f (5456–5468), then creep 1.40→1.47 over ~70 f (~0.1%/f), then acceleration at 5540 into the cut [Measured] |
| D22 | **Ease-in push into hard cut** | 5390–5398 | Scale ratio 1.000, 1.004, 1.009, 1.021, 1.036 per 2 f → accelerating zoom, then hard cut [Measured] |
| D23 | **Slot-machine word list** | `d_words.jpg` 5414–5450 | Rectangle grows from a vertical line (5414–5426). Words scroll vertically through it (Velocity, Mastery, Engineering…) and stop on "Legacy" ~5444. Yellow dry-brush stroke swipes L→R 5426–5450 [Observed] |
| D24 | **Desk-collage camera drift** | zoom.py 5546–5720 | Enter push 1→1.38 (12 f), then continuous pan at ~10–70 px/f with direction changes (content moves +x then +y then −y), pull-back 5708–5720 [Measured, ORB noisy] |
| D25 | **Ken Burns on stills** | 777–846 | Slow push ≈ +2.5% over 54 f (~0.05%/f) [Measured] |
| D26 | **Layered dissolve collage** | 3430–3695 | 2–3 footage layers blended (screen/normal) with long overlapping dissolves of ~15–40 f; dark texture base [Observed] |

## E. Transitions catalog

| Type | Frames | Count | Examples |
|---|---|---|---|
| Hard cut | 0 | ~88 of 107 boundaries | most footage and card boundaries |
| Hard cut on accelerating push (ease-in punch) | push ~6–8 f, then cut | ≥2 measured | 5392–5399; 5540–5545 |
| Cross-dissolve, short | 3–6 f | 4 | 527, 687–692, 774–777, 847–852 |
| Layered long dissolve | 15–40 f | ~6 | 3445–3655 collage |
| Page curl (corner peel) | ~10 f | 1 | 126–136 |
| Crumpled-paper wipe (paper rises from bottom) | ~22 f | 1 | 1662–1684 |
| Horizontal push / photo slide | ~4 f | 5 + slides in 4036–4148 | 1363–1466 |
| Focus-reticle dissolve (concentric white rings over a 8 f dissolve, rings shrink to a point by ~1950) | ~20 f | 1 | 1930–1950 |
| In-frame content swap (TV channel change) | 0 | 3 | 2424, 2455, 2484 |
| Layout reflow (graphic shrinks/slides into collage) | ~15 f | 1 | 894–909 |
| Cut to white/paper | 0 | 1 | 5721 |
| Fade to black (end) | ~58 f | 1 | 5840–5898 (luma 29→25 at 5868) |
| 1-frame flash | 1 | 1 | 4743 (MAD 24 then 147) |

## F. Typography & layout

- **Primary face:** transitional/old-style serif, roman, for titles, prices, chart titles and labels. Lining figures in titles ("356") [Observed, typesheet.jpg]. Font not identified. ESTIMATED free matches: **Source Serif 4**, **Libre Caslon Text**, **Lora**.
- **Italic face:** serif italic with **old-style figures** ("1.1L", "40 hp", "356"). Used for footage captions, quotes, the intro words ("passion") and emphasis words ("*hybrid*", "*revolution*") [Observed]. The look resembles Georgia Italic. Free matches: **Gelasio Italic** (Georgia-metric), **Lora Italic**, **Source Serif 4 Italic**.
- **Map label:** heavy/bold serif caps, "STUTTGART" [Observed]. Match: **Libre Caslon Display / Playfair Display Black / Abril Fatface** (ESTIMATE).
- **Car-card title** [Measured, frame 1260]:
  - Black-brown text on a flat yellow box, 579x135 px, x 671–1250, top y 181, centred.
  - Cap height ≈ 66 px. Box padding ≈ 35–40 px horizontal (ESTIMATE).
  - Price line: cap ≈ 35 px, centred at y≈388, mid-gray-brown.
  - Car cut-out centred, lower half (car spans ~x 440–1500, y ~560–900 in 1260; ESTIMATE from the 640 px frame).
- **Footage caption:** yellow (#E4E704 measured, frame 1980, region x300–1700 y900–1040) italic serif, cap ≈ 30–35 px (ESTIMATE). Left-aligned at x≈230, baseline ≈ y 955. Preceded by a ▶ glyph ≈ 50 px [Observed/Estimate].
- **Quote layout** [Observed]: quote block on the left-centre (x≈1220–1700 at frame 1140), ragged-right, italic, ~5 lines. Cut-out portrait on the right with a yellow offset glow/outline (~15–25 px). Final quote (5760) mirrors this layout with grid paper and corner crop marks.
- **Chart title:** bold serif ~40 px cap, plus a small gray source line (frame 3960) [Observed].
- **Treatments:**
  - Text has chromatic aberration (red/cyan fringe ≈ 2–3 px) on footage and some paper scenes, e.g. "passion" at 180 [Observed].
  - Highlights are flat rectangles (D1/D7), speech-bubble rectangles with a pointer (D4), dry-brush strokes (5426+, 2362 map) and filled circles (D10).

## G. Colour & texture

| Element | HEX | Status / location |
|---|---|---|
| Highlight yellow (title box) | **#F6EA00** | Measured t=42.00 f1260, box x600–1320 y150–350 |
| Highlight yellow (Cayenne title) | #F4E800 | Measured f4320, y<500 |
| Yellow circle | #F4E900 | Measured f2160 |
| Chart grid yellow | #F5E930 | Measured f3960 |
| Map outline yellow | #ECE048 | Measured f450, x700–1300 y500–900 |
| Brush stroke yellow (CRT scene, textured) | #D1C317 | Measured f5460 |
| Caption text yellow | #E4E704 | Measured f1980 |
| ▶ triangle yellow | #FAEF07 | Measured f180 |
| Paper (card) centre-left | #E1D7D1 | Measured f1260, x100–300 y500–700 |
| Paper top-centre (brightest) | #EFE5DC | Measured f1260 |
| Paper corners (vignette) | TL #CFC8C1, BR #C0B9B2 | Measured f1260 |
| Paper (blueprint card) | #DCD3CA | f2160 |
| Paper (chart) | #DCD2CC | f3960 |
| Paper (grid quote) | #ECE3DB | f5760 |
| Paper (CRT screen) | #CDC3B5 | f5460 |
| CRT bezel | #8D8F78 | f5460, left strip |
| Bar fill | #333230 | Measured f3960 |
| Dark timeline bg | #120E0B (centre #1A1411) | Measured f960 |
| Intro card surround | #000000 | Measured f180 |
| Map ocean / land (Europe) | #688EB7 / #9C9C71 | Measured f360 |
| Map land (zoomed) | #B9B389 | Measured f450, full frame median |
| Title text | near-black warm, ≈ #231F1C-ish | ESTIMATE (antialiased; measurement noisy) |
| Chart circle red | ≈ #8B1A1A | ESTIMATE visual |

Texture:
- **Vignette:** on all paper scenes the corners are ~35–45 luma levels darker than the centre (#EFE5DC→#C0B9B2) [Measured f1260]. Footage also gets a dark vignette (newspaper montage, 2280–2362) [Observed].
- **Grain/paper:**
  - Paper has fibre specks and baked grain, but static frames are pixel-identical (MAD = 0), so the grain is **not animated** during holds [Measured].
  - Crumpled-paper texture appears at 1673–1760 [Observed].
  - Halftone/print dot texture is visible on the map [Observed].
- **Colour grading of archival footage:** B&W, sepia, green-tinted (1935–2029) and faded 70s colour [Observed].
- **Photo borders:**
  - Thin yellow-olive keyline (#BB9D24 median at f4500, ESTIMATE ~4–6 px) around framed photos/footage on paper [Measured colour / estimated width].
  - Polaroid-style white borders with yellow tape in the desk collage and the dark photo stack [Observed].
- **Drop shadows:** soft, under map thumbnails and framed photos. ESTIMATE blur 15–25 px, offset ~5–10 px down-right, opacity ~35–50% [Inferred visually].
- **Cut-out treatment:** people get a yellow offset glow/outline of ~15–25 px (1105–1215, 5721–5898) [Observed].
- **Chromatic aberration** on text and edges [Observed].

## H. Pacing

- 108 shots (in-TV swaps and soft collage boundaries included). Mean **1.82 s**, median **1.45 s** (43.5 f). Min 5 f (newspaper/ad flashes). Max 185 f (map zoom scene 7) [Measured, stats.py].
- **Distribution:**

| Shot length | Shots |
|---|---|
| <15 f | 9 |
| 15–29 f | 21 |
| 30–59 f | 42 |
| 60–89 f | 18 |
| 90–149 f | 12 |
| ≥150 f | 6 |

- **By 30 s window (shots / mean length):**

| Window | Shots | Mean length |
|---|---|---|
| 0–30 s | 14 | 2.24 s |
| 30–60 s | 15 | 1.91 s |
| 60–90 s | 28 | **1.07 s** (newspaper burst) |
| 90–120 s | 16 | 1.91 s |
| 120–150 s | 16 | 1.85 s |
| 150–180 s | 17 | 2.04 s |
| 180–197 s | 2 | 5.9 s (slow outro) |

- **Rhythm:** model cards are ~2 s holds, each followed by 2–5 shorter footage/photo shots (~1 s each). Bursts of 5–15 f cuts are used for montage emphasis (75.8–78.7 s).
- **Activity:** per-second mean MAD peaks at 162–164 s (factory footage, 20–26) and in the intro. Graphic scenes have 50–80% static frames [Measured, act.py].

## I. Uncertainties

- **Fonts not identified.** Matches are estimates.
- **Text colour sampling** on antialiased small type is unreliable. Text HEX is an estimate.
- **Shot boundaries inferred, not measured:** 2270/2275 (from MAD only) and the collage dissolves 3445–3655 (approximate centres).
- **Detection limits:** small in-frame changes (typewriter characters, inset-only swaps) fall under the MAD 0.5 threshold. Cadence counts for text animations are therefore approximate.
- **ORB zoom/translation estimates:**
  - Reliable for map, quote and article zooms.
  - Noisy for the desk collage (5546–5720), where elements move independently, and around dissolves (777–792 values may be contaminated by the overlay).
- **D17 card bbox** and the drop-shadow parameters are visual estimates from 640/320 px frames, not pixel-measured.
- **Coverage gaps:** ranges listed in B were inspected at 10-frame density only. Unseen micro-animations (e.g. caption typing speed per shot) may vary from the measured examples.
- **12 fps cadence:** inferred from 2/3-frame gaps in MAD. It may come from a 12/24 fps comp, not a deliberate "on-twos" choice.
