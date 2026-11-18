# V5_rabbit — "Spain the Rabbit Island" — Forensic Breakdown

Source: key V5_rabbit in `../sources.tsv`. 1920x1080, 30 fps, 1127 frames, 37.6 s. Source not modified.

**Format note [Observed]:** this is a *portfolio / showcase* frame. A 9:16 vertical short (the actual Vox-style collage piece) plays inside a card on the left (x 258–715, y 134–945 = 458x812 px [Measured f360]); the right side holds a static caption ("A Phoenician sailor mistook rabbits for hyraxes — and that's how Spain got its name.") and a paper tape label "Watch original — 20K+ views on YouTube" that slides in at 3.8–7 s. The outer layout never changes; all scene changes happen inside the card.

## A. Inventory

| Item | Path |
|---|---|
| Per-frame diff | `framediff.tsv` (1127 rows) |
| Cut candidates | `cuts.json` (51,117,204,276,303,378,507,654,765,801,873,1032) |
| Frames / sheets / full-res | `frames/` (63), `sheets/sheet_00.jpg`, `sheet_01.jpg`, `full/f00000…f01080.png` (every 90 f) |
| Work scripts | `work/regions.py` (per-frame diff split: card region / right half / tape region), `work/tape.py` (bg-difference tape bbox), `work/tm.py` (template-match + rotation search for tape), shared `../V2_camera/work/strip.py`, `col.py`, `maskcol.py`, `runs.py`, `cad.py` |
| Work outputs | `work/regions.txt` (all 1126 diffs), `work/tm.txt`, `work/tape.txt`; strips `work/card_0_375.jpg`, `card_376_751.jpg`, `card_752_1126.jpg` (card crop every 6th frame), `work/tape_110_230.jpg` (every 4th), every-frame strips `work/c_50_61.jpg`, `c_114_149.jpg`, `c_200_211.jpg`, `c_300_311.jpg`, `c_410_421.jpg`, `c_578_595.jpg`, `c_1028_1045.jpg`; crops `work/caption_crop.jpg`, `tape_crop.jpg`, `cardedge_crop.jpg` |

## B. Inspection record

- Total frames 1127. Numerically measured: all (framediff; region-split diff for 1126 frame pairs; tape template-match every 2nd frame f118–230; card bbox and shadow profile at f360).
- Visually opened: card crops every 6th frame over the whole video (192 frames: 0,6,…,1124); full-frame tape region every 4th frame f110–230 (31); every frame in f50–61, 114–149, 200–211, 300–311, 410–421, 578–595, 1028–1045 (12+36+12+12+12+18+18 = 120); sheets 00/01 (38 frames). ≈ 330 unique frames opened. Odd frames between the 6-step samples outside the listed ranges were not opened.

## C. Scene table (scenes = shots inside the card; outer frame static throughout)

| # | start t (f) | end t (f) | dur | description (inside card) | motion | typography | transition out |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 (0) | 1.67 (50) | 51 f / 1.7 s | Vignetted portrait (Charles II) on paper; map of Spain cutout with flag, "Spain" script; Infanta portrait enters from right at f24–27; "was named" text | map/flag pop-on at f6, f12 (on 3s/6s); portrait slide-in 2 steps | handwritten script "Spain", bold serif "was named" | hard cut |
| 2 | 1.70 (51) | 3.87 (116) | 66 f / 2.2 s | Dark grey with trapezoid spotlight beam; huge faded "after this" text; rabbit cutout drops in from top (f57) with paper label "mysterious animal?" | rabbit drop 3 f; subtle hover; "after this" fade-in f57–60 | big rounded sans "after this" (tone-on-tone, ~20 % opacity) | white flash cut |
| 3 | 3.90 (117) | 6.77 (203) | 87 f / 2.9 s | White frame → clouds part revealing blue sea map with coastline cutouts; label "it all started with / the ancient Phoenicians"; two boats | "fly-through clouds" reveal f117–150 (white held f117–122, clouds open f123–150); boats drift; label type-on f147–162 | small white sans on black box; italic serif second line | hard cut |
| 4 | 6.80 (204) | 9.17 (275) | 72 f / 2.4 s | Cliff + water footage/collage, striped Phoenician ship enters from right (f204–210); "sailing past" label type-on (f207–222); "the Iberian Peninsula" tape at bottom (f234–) | ship slide-in ~6 f; water loops; label letter-by-letter | white bold sans on black label | hard cut |
| 5 | 9.20 (276) | 10.07 (302) | 27 f / 0.9 s | Classical bust on sea, wood plank foreground, "they noticed" label | label type-on | same label style | hard cut |
| 6 | 10.10 (303) | 12.57 (377) | 75 f / 2.5 s | Black frame with circular spyglass lens (soft vignette) viewing rocky shore; rack-focus blur→sharp f303–309; "some strange" / "animals" (italic) / "on the shore" texts; rabbits | lens pans across scene; focus pull; texts pop | white bold sans + italic serif "animals" | hard cut |
| 7 | 12.60 (378) | 13.87 (416) | 39 f / 1.3 s | Facecam (presenter, rounded rect) on wood planks; "these were" label above, "rabbits" serif-italic label below | live video on 1s; card push down+scale-up f413–416 then gone | label style + italic serif tag | push/whip down |
| 8 | 13.90 (417) | 16.87 (506) | 90 f / 3.0 s | Top-down wood table: "but the sailors mistook them" label, old paper card with rabbit sketch + "wtf?" scribbles (enters f430–436), then pan to "for hyraxes" card, hyrax sketch, pottery shards, coins; red hand-drawn circle "fruit" | slide-ins; continuous pan f465–498 (diff 15–37/frame) | labels + handwritten red marker | hard cut |
| 9 | 16.90 (507) | 19.37 (581) | 75 f / 2.5 s | Bust vs. sea again; "and called this land" label (fades out f550–556); "i-shepan-im" handwritten-italic label writes on (f562–580) | text type/write-on | italic serif tag on paper strip | push-in transition |
| 10 | 19.40 (582) | 21.77 (653) | 72 f / 2.4 s | Antique map (Iberia) slides in over bust from top-left, sea with ship, "or 'hyrax island'" angled caption | map slide/push f582–595 (13 f, 3 steps visible), clouds | italic serif caption rotated ~−25° | hard cut |
| 11 | 21.80 (654) | 25.47 (764) | 111 f / 3.7 s | Roman legion illustration + "later it was / conquered by the Romans" label → pan to landscape (f720–735) → road sign "HISPANIA" + temple, "but the name stuck" | lateral pan, label swap with fade; sign pop-on f730–736 | label style; script "stuck"; condensed sans on sign | hard cut |
| 12 | 25.50 (765) | 26.67 (800) | 36 f / 1.2 s | Red textured bg, gold coin spinning (edge-on f788), "local coins" tag | coin Y-rotation flip ~24 f; zoom to coin face at f800 | small white sans on dark-red box | hard cut |
| 13 | 26.70 (801) | 29.07 (872) | 72 f / 2.4 s | Wrinkled fist on grey cobble bg, "featured" text; hand opens (f831–836) to reveal coin; label "the personified mascot" | hand open substitution; label slide | serif italic "mascot" | hard cut |
| 14 | 29.10 (873) | 34.37 (1031) | 159 f / 5.3 s | Classical painting (woman by sea), pan right reveals man (f891–), "Roman poet Catullus" label, "described Spain as a", "rabbit-ridden land" note; rabbit head collaged onto woman (f1010–1031) with tape note | slow pan/zoom, label swaps, cutout pop | label style; handwritten italic on white tag | hard cut |
| 15 | 34.40 (1032) | 37.53 (1126) | 95 f / 3.2 s | Rusty brown wall, "share this" text; facecam card slides down from top f1036–1050; papers + hand; "with a fellow / Spaniard" label | facecam drop-in ~14 f ease-out; label type-on | label + script "Spaniard" | end (no fade) |

Outer-layer events: f0–1 caption already present (one-frame settle, right-region diff 3.3 at f1); **tape label slides in f114–≈230** (see D2); outer paper otherwise static (right-half mean diff 0.13 outside f110–240) [Measured].

## D. Motion catalog

1. **Layer cadences** [Measured, `regions.txt`]: inner-card changes: 351 gaps of 1 f, 218 gaps of 3 f, 59 gaps of 2 f → illustrated collage sections are animated **on 3s (10 fps)**, facecam / video plates **on 1s**. Outer tape label moves only on even frames → **on 2s (15 fps)**. Shot 3 cloud-reveal in card on 6s at times (card diffs at 126,132,138,144,150… = every 6 f).
2. **Tape label entrance** [Measured, `tm.txt`, `tape_110_230.jpg`]: enters from bottom-right edge at f114, travels up-left with motion blur f122–142 (template match unreliable there), then position offset from rest (dx,dy) = (61,119) f144 → (30,62) f162 → (15,27) f186 → (7,13) f206 → (3,5) f220 → (0,0) f230. Residual halves about every 20 f → **exponential ease-out (expo-out), total ~116 f (3.9 s)**, rotation settles +3° → +1.5° (f146) → 0° (f190) relative to final angle; final tilt ≈ −7° to −8° (minAreaRect, `tape.txt`). Estimated curve: cubic-bezier(0.16, 1, 0.3, 1), 3.9 s, with the first ~1 s covering ~85 % of travel.
3. **Rabbit drop (shot 2)** [Observed `c_50_61.jpg`]: absent f56 → partially in at top f57 → in place f60, label added f60. 3–4 f drop, no visible bounce.
4. **Cloud reveal (shot 3)** [Observed `c_114_149.jpg`]: f117–122 pure white, f123–128 cloud texture fades in from the white, f129–150 clouds thin/part toward bottom-left and top-right revealing sea, label text appears faint f126 and gets a black box f147. ~33 f (1.1 s).
5. **Ship slide-in (shot 4)** [Observed `c_200_211.jpg`]: ship absent f203, enters at right edge f204, mid-frame f207, final ~f210 (≈6 f, two 3-f steps). Label "sa…" f207 → "sailin" f210 → "sailing past" f222: typewriter ≈ 1 char per 2–3 f.
6. **Focus pull (shot 6)** [Observed `c_300_311.jpg`]: cut f303 to blurred lens view, still soft f306, sharp f309 (2 steps of 3 f). Circular lens mask has ~40 px feather + dark vignette.
7. **Facecam push-out (shot 7→8)** [Observed `c_410_421.jpg`]: f413–416 facecam and labels translate down ~25 % card height and scale up ~10 % per frame, f417 gone (wood bg remains) → whip-down exit, 4 f, ease-in.
8. **Map push-in (shot 9→10)** [Observed `c_578_595.jpg`]: f582 map appears top-left over bust, f585 covers top half, f588 covers ~70 %, f591 full, bust slides out right; 3-frame steps, ~13 f (0.43 s), ease-out.
9. **Facecam drop-in (shot 15)** [Observed `c_1028_1045.jpg`]: f1036 top edge visible, f1040 ~40 % down, f1045 ~70 %, settles ~f1050 → ~14 f ease-out slide from top.
10. **Label type-on** [Observed, multiple]: black rectangular labels with white bold sans text reveal L→R (box grows with text), ~1 char / 2–3 f.

## E. Transitions

- 12 hard cuts inside the card (`cuts.json` list verified on strips) [Observed].
- Soft/compound: white flash + cloud reveal (f117–150), push/whip down (f413–417), map push-in (f582–595), lateral pan between illustrations (f465–498, f687–735) [Observed + Measured diff runs].
- Outer frame: no transitions; video ends on a hold, no fade [Measured luma constant].

## F. Typography & layout

| Element | Face [Observed] | Google match [Inferred] | Size | Position | Treatment |
|---|---|---|---|---|---|
| Right caption (4 lines) | Humanist geometric sans, regular (Avenir-like) | Nunito Sans / Mulish Regular | cap ≈43 px → ~58–60 px font; leading ~58 px | x≈925–1600, y≈300–520 | near-black #2A2520-ish [Estimated], slight blur/texture; "hyraxes" on coral marker highlight #CB5F4A (rounded, slightly overshooting box); "Spain" circled with double hand-drawn red ellipse |
| Tape label | same sans | same | cap ≈38 px → ~50 px | centre ≈ (1430,900), tilted ≈ −7° | cream paper strip with soft drop shadow; red hand-drawn underline under "20K+" |
| In-card labels ("sailing past", "they noticed"…) | bold sans, lowercase | Montserrat Bold / Inter Bold | ~22–26 px (in 1080p frame; card is 458 px wide) | top-left of card | white text on black rectangle, tight padding |
| Second-line / accent tags ("the ancient Phoenicians", "rabbits", "animals", "mascot", "i-shepan-im") | italic old-style serif | EB Garamond Italic / Cormorant Italic | ~20–40 px | below labels | on white/cream paper strip or black box |
| Big background text "after this" | rounded heavy sans | Nunito Black | ~110 px in card | centred | tone-on-tone, low opacity |

Layout: card left third (x 258–715), caption and tape occupy right 55 % (x ~900–1880). Card centre y ≈ 540 (vertically centred).

## G. Color & texture (measured on `full/f00360.png`)

| Swatch | HEX | Region |
|---|---|---|
| Outer kraft paper | #B2987D (centre-left), #AD967B (TR), #B59A7F (BL) | [Measured] |
| Card drop-shadow core | #846E5F (below), #97816A (right) | [Measured] |
| Coral highlight / red ink | #CB5F4A | HSV mask median [Measured] |
| Card black bg (shot 6) | #0A090B | [Measured] |
| Kraft ochre accents | #A88454 | [Measured, small sample] |

Texture: outer background is crumpled kraft/parchment with faint dotted-route map lines (treasure-map style dashed paths) [Observed]; luma centre 157 vs corners 155–162 → no vignette [Measured]. **Card drop shadow** [Measured luma profile]: right side drops from 147 (bg) to 78 at card edge and recovers to bg over ~30 px; left/top side only ~12–15 px of darkening → offset ≈ (+8, +8) px, blur ≈ 25 px, opacity ≈ 45–50 %. Card has a ~3–4 px light rim. Tape has its own soft shadow below-right [Observed]. Inner collage: cutouts with white/cream paper borders, rough torn edges on map pieces, halftone/engraving illustrations, wood and rust textures, film grain on facecam.

## H. Pacing

- 15 inner shots in 37.6 s → mean 2.5 s/shot (range 0.9–5.3 s). Fast early (1.7, 2.2, 2.9, 2.4, 0.9 s), slower painting section (5.3 s) near the end.
- Text labels change every ~1–1.5 s inside each shot. Outer frame offers a single slow event (tape entrance, 3.9 s) and is otherwise static.

## I. Uncertainties

- Inner-card motion numbers are from card crops viewed at 100–120 px width; small moves (<5 px at 1080p) not detectable.
- Tape motion f122–142 unmeasured due to motion blur; entry vector inferred visually (from bottom-right).
- Shadow parameters derived from one luma profile; blur/offset ±30 %.
- Shots 11 and 14 may contain additional soft cuts hidden by pans (diff runs 687–735, 891–1026 not viewed frame-by-frame).
- Script content not transcribed beyond on-screen label identification.
