# Shot & Motion Timeline

A chronological technical index of the important animations and transitions, per video, with source frames. Each row links to a recipe in [MOTION_RECIPES.md](MOTION_RECIPES.md) (Mx). Measurements come from the agents' per-frame tracking (`reference-analysis/<KEY>/work/`).

- **Units:** frames at the native fps. Px at 1080p.
- **Shape codes:**
  - **EO** ease-out
  - **EIO** ease-in-out
  - **EI** ease-in
  - **LIN** linear

## V1_porsche (30 fps)

| t (s) | Frames | Event | Measured behaviour | Recipe |
|---|---|---|---|---|
| 0.00 | 0–8 | Radial zoom-blur on the opening map | Blur decays over 8 f | M17 |
| 0.07 | 2–114 | Map zoom-out 8.8× | Log-scale EO, 29 % done at f10, 87 % at f60; cubic-bezier(0.2,0.8,0.3,1) on log-scale ESTIMATE | M10 |
| 0.1–4.0 | 2–124 | Thumbnails pop on | Staggered every 3–8 f | M12 |
| 4.20 | 126–136 | Page-curl peel (bottom-right) | 10 f | T6 |
| 4.53 | 136–150 | Footage shrinks to an inset card | About 12 f EO | M13 |
| 11.53 | 346–406 | Map zoom-in 30× | Log EIO, peak at about 60 %, motion blur f378–396 | M10 |
| 13.40 | 402–430 | Pin grows (12 f), outline draws (13 f), label fades (3 f) | — | M5, M7 |
| 14.50 | 435–446 | Speech-bubble highlight wipe | 11 f EO (+55,+63,+44,+36,+20 px/f); wipe-off 6 f | M3 |
| 16.13 | 484–500 | Two portraits rise from the bottom | 760 px in 18 f, symmetric EIO | M11 |
| 17.57 | 527–533 | Dissolve to archival | 6 f | T3 |
| 24.30 | 729–757 | Year counter 2024→1900 | 11 values on 12 fps, EIO on value | M15 |
| 24.97 | 749–759 | Highlight behind the year | 10 f EO | M3 |
| 25.80 | 774–777 | Dissolve | 3 f | T3 |
| 25.9–28.2 | 777–846 | Ken Burns on a still | +2.5 % in 54 f, LIN | M14 |
| 28.6 | 858–882 | Highlighter wipe over an ad | 24 f EO | M3 |
| 34.5 | 1036–1048 | Photo slides in from the right | About 12 f | M11 |
| 35.0 | 1051–1060 | Yellow ring draw | 9 f | M7 |
| 36.87 | 1106–1119 | Quote portrait zoom-out 1.75× | 14 f EIO | M9 |
| 37.1–38.3 | 1113–1150 | Quote words fade in | About 2 f per word | M2 |
| 40.70 | 1221–1243 | **Car-card title box + typing** | Box 29→579 px in 22 f, typing about 2 f/char, 12 fps | M1 |
| 45.4–49.4 | 1363–1466 | Photo carousel | −739 px in 2 f, settled in about 4 f, every 20 f | T5 |
| 49.57 | 1487–1565 | Line chart draws | About 78 f, near-LIN, 6 fps steps | M16 |
| 55.4 | 1662–1684 | Crumpled-paper wipe up | 22 f | T7 |
| 64.3 | 1930–1950 | Focus-ring dissolve | About 20 f | T8 |
| 75.8–78.7 | 2275–2361 | Newspaper-headline burst | Cuts every 5–15 f; the highlighted word is matched in screen position | T1 |
| 80.17 | 2405–2416 | TV scale-pop 71 %→100 % | 10–12 f expo-out | M5 |
| 130.9 | 3939–3994 | Bar chart, 8 bars | Stagger 5 f, about 90 % at 12 f, settled by 20 f, no overshoot | M6 |
| 133.5 | 4005–4011 | Red hand ellipse | 6 f | M7 |
| 177.4 | 5326–5345 | Highlight on a money figure | 19 f | M3 |
| 179.7 | 5390–5398 | Accelerating push into a hard cut | Scale ratio 1.000→1.036 per 2 f | M18, T2 |
| 181.9 | 5456–5468 | Punch-in 1.4×, then creep | 12 f, then about 0.1 %/f | M8 |
| 184.9 | 5546–5558 | Desk-collage push 1.38× | 12 f | M9 |
| 194.7 | 5840–5898 | Fade to black | 58 f | T9 |

## V2_camera (60 fps, animated on 6s)

| t (s) | Frames | Event | Behaviour | Recipe |
|---|---|---|---|---|
| 0.00–2.33 | 0–140 | 7-image montage | 18–24 f per image; each drifts up with decaying steps (−30, −14, −10 px …) | T1, M14 |
| 2.35 | 141–165 | Title disc scale-in | 228→288 px, progress .55/.81/.94/.97 per 6 f = expo-out 24 f | M5 |
| 2.35 | 141–159 | Title word reveal | Mask L→R in three 6 f steps | M2 |
| 2.65 | 159–171 | Second line | Rise about 10 px and fade, 12 f | M4 |
| 2.95 | 177–195 | Red square bullet | 14.5→25 px, 18 f EO | M5 |
| 4.35 | 261–292 | Bio disc | Expo-out 25 f, then +18 px creep over 100 f | M5, M8 |
| 6.50 | 390–418 | Fade to black | LIN 29 f | T9 |

## V3_elections (23.976 fps, graphics on 2s)

| t (s) | Frames | Event | Behaviour | Recipe |
|---|---|---|---|---|
| 0.5–3.1 | 12–74 | Title words type on to the VO | One step per word, no fade | M2 |
| 0.0–3.0 | 0–72 | Title slow push | +0.13 %/f, LIN | M8 |
| 3.0 | 72–88 | **Punch-in ×1.30** | Progress .20/.55/.74/.84/.90/.96/.99 per 2 f; cubic-bezier(0.2,0.8,0.3,1) | M8 |
| 7.8 | 186–204 | Hand circle around a ballot word | 18 f | M7 |
| 16.0–22.2 | 383–533 | Montage cuts | Every 25 f | T1 |
| 55.5 | 1330–1423 | **Loupe reveal → fill frame** | Lens crosses with the next layer inside, then scales to fill | T4 |
| 70.1 | 1680–1752 | **Region zoom ×5.7** | 72 f EIO, peak at 60 %, long tail; cubic-bezier(0.55,0,0.15,1) | M10 |
| 72.8 | 1744–1790 | People icons stagger | About 1 per 2 f, reading order | M12 |
| 88.0 | 2109–2160 | **Lower third** | Dots, plate wipe 3 f, name 13 chars in 14 f, role 1 char/f | M19 |
| 102.6 | 2460–2524 | Districts explode → donuts | Grid layout 16 f; fade to 30 % over 12 f; donuts draw 18 f | M20 |
| 148.0 | 3548–3564 | Blur-zoom into a paper | 16 f defocus→focus | T10 |
| 149.3 | 3578–3612 | **Highlighter line wipe** | 612 px in 34 f, EIO sine, peak 27 px/f | M3 |
| 158.0 | 3786–3826 | **Loupe entry** | cx 308→699 px, 40 f EO; then 0.72 px/f LIN drift | M11 |
| 185.3 | 4443–4471 | Hemicycle build | 28 f, arc sweep | M20 |
| 188.6 | 4520–4540 | Dim the other parties | 20 f to 15–25 % opacity | M20 |
| 194.8 | 4670–4739 | **Lateral pan** | 1675 px in 68 f; peak at 20 %; cubic-bezier(0.55,0,0.1,1) | M10 |
| 213.6 | 5118–5150 | Banner wipe | 32 f L→R | M3 |
| 230.4 | 5523–5599 | **Push to node ×1.6** | 76 f; cubic-bezier(0.65,0,0.35,1); others fade over f5559–5583 | M9 |
| 326.0 | 7817–7861 | **STV bars** | Quart-out 30 f; stagger 10/6/8/8 f | M6 |
| 408.0 | 9795–9851 | Arc stroke draw-on and draw-off | 24 f each | M7 |
| 498.6 | 11954–12161 | Photo drops onto a pile | Every 25→20 f, hard swaps, ±3–5° rotation | M12 |

## V4_highlight (10 fps)

| t (s) | Frames | Event | Behaviour | Recipe |
|---|---|---|---|---|
| 0.1 | 1–4 | Title ink-in | 4 f erosion reveal | M2 |
| 0.6 | 6–14 | Brush highlighter | LIN about 1180 px/s, hard stop | M3 |
| 0.7 | 7–8 | **Snap zoom ×1.55** | 2 f, EI | M8 |
| 3.1 | 31–32 | Snap zoom out | 2 f | M8 |
| 4.0 | 40–54 | Highlight erodes | Accelerating, mostly in f49–51 | M3 |
| 7.5 | 75–78 | Accelerating highlighter | +164/+273/+382 px per frame | M3 |
| 9.4 | 94–97 | Camera pan up 207 px | EI, 3 f | M10 |
| all | — | Texture boil | A-A-B loop at 3.3 Hz | M14 |

## V5_rabbit (30 fps)

| t (s) | Frames | Event | Behaviour | Recipe |
|---|---|---|---|---|
| 3.8 | 114–230 | **Tape label slide-in** | Expo-out over 116 f; residual (61,119)→(0,0) px, halving about every 20 f; rotation 3°→0 | M4 |
| 3.9 | 117–150 | Cloud fly-through reveal | White → clouds part, 33 f | T11 |
| 6.8 | 204–222 | Ship slide-in plus label typing | 6 f; about 1 char per 2–3 f | M11, M2 |
| 10.1 | 303–309 | Rack focus in a lens | 2 steps of 3 f | T10 |
| 13.8 | 413–416 | Facecam whip-down exit | 4 f EI | T5 |
| 19.4 | 582–595 | Map push-in over a bust | 13 f EO, 3 f steps | T5 |
| 34.5 | 1036–1050 | Facecam drop-in | 14 f EO | M11 |

## V6_epigenetics (23.976 fps, on 2s)

| t (s) | Frames | Event | Behaviour | Recipe |
|---|---|---|---|---|
| 0.7 | 16–30 | Rack focus pulse | — | T10 |
| 0.9 | 22 | Snap pull-back | ×0.953 in one step | M8 |
| 2.2 | 52–74 | **Tilt-push into the header** | ×1.18, 22 f; cubic-bezier(0.45,0,0.55,1); content moves 134 px | M9 |
| 3.8 | 92–100 | Sticky slap | Scale 10 %→100 % in 8 f, slight rotation | M5 |
| 4.5 | 108–116 | Underline draw | 8 f, about 700 px/s | M7 |
| 4.8–9.0 | 116–216 | **Linear pull-out** | 0.2 %/2 f, ×0.83 total | M14 |
| 9.2 | 220–234 | **Whip pan** | −309 px in 14 f, fast EO; then a 2° rotation settle | T5 |
| 10.7 | 256–268 | Marker circle | 12 f | M7 |
| 12.2 | 292–304 | Zoom bubble grows | 10 f EO | M5 |
| 16.0 | 383–399 | Magnifier slide-in | 16 f EO | M11 |
| 18.2 | 436–492 | **Zoom-through** | ×1.29 EI in 24 f → cut f462 → ×1.82→1 EO in 28 f | T2 |
| 27.3 | 654–696 | Push to paper title | ×1.73, 42 f EIO | M9 |
| 32.4–34.9 | 776–836 | Tag pops | 8–24 f apart | M12 |
| 36.0 | 863–868 | Sticky peel-in | 6 f, 3D rotate | M5 |
| 43.0 | 1031–1039 | **Radial zoom-blur transition** | Out 2–4 f, in resolves over 4–6 f | T10 |
| 46.4 | 1113–1125 | Settle pull-out | ×0.88 over 12 f, EO | M9 |

Transition codes (T1–T11) are defined in [MOTION_RECIPES.md § Transitions](MOTION_RECIPES.md#transitions).
