# Motion Recipes

Reusable animation recipes with measured parameters. Frame counts are given **at 24 fps**, converted from the source fps. The source evidence is listed with each recipe. Code uses `templates/style-system/ (copied into the project as src/style-system/)` (`ease`, `stepped`, `clamp` from `tokens.ts`).

## Global rules

- **G1 — On twos.** Compute every graphic animation from `const f = stepped(useCurrentFrame())`, so values change every 2 frames (12 drawings/s). Live footage and the final fade to black are not stepped. [V3 D0, V6 D1, V1 cadence]
- **G2 — No overshoot.** No tracked move (bars, pops, TV, circles, tape, whips) overshot its target. Use `Easing.bezier` curves from `ease`. If you use `spring()`, set `damping ≥ 200` (critically damped).
- **G3 — Mixed curves.** Arrivals use ease-out, camera moves use ease-in-out, and moves into a cut use ease-in. Do not apply one easing to everything.
- **G4 — Scale moves in log space.** For zooms of 2× or more, interpolate `Math.log(scale)` so the perceived speed matches the references' log-measured curves (V1 D2/D3). Remotion's `interpolate(..., {output: 'perceptual-scale'})` does the same thing.

## Easing library (ESTIMATE fits)

| Token | cubic-bezier | Fitted from |
|---|---|---|
| `ease.pop` | (0.16, 0.7, 0.7, 1), least-squares refit, RMS 0.005 | V2 disc .55/.80/.95 at ¼/½/¾ of the move; pops, highlight blocks |
| `ease.expo` | (0.16, 1, 0.3, 1) | V5 tape (≈85 % of travel in the first quarter); V1 TV (Δ decays ×0.75/f) |
| `ease.grow` | (0.25, 1, 0.5, 1) | V3 bars: 50 % at 6 f and 90 % at 14 f of 30 |
| `ease.punch` | (0.2, 0.8, 0.3, 1) | V3 title punch: .20/.55/.74/.84 per 2 f; V6 whip; V1 intro zoom |
| `ease.push` | (0.7, 0, 0.4, 1), least-squares refit, RMS 0.019 | V3 node push: .06/.20/.50/.75/.88/.97 at 26/42/53/63/74/89 % |
| `ease.tilt` | (0.45, 0, 0.55, 1) | V6 tilt-push; V1 photo rise (symmetric) |
| `ease.pan` | (0.55, 0, 0.1, 1) | V3 lateral pan: peak velocity at 20 %, long tail |
| `ease.accel` | (0.55, 0, 1, 0.45) | V6 zoom-through first half; V1 push into a cut |
| `ease.wipe` | (0.37, 0, 0.63, 1) | V3 highlighter line (symmetric sine) |

---

## M1 — Title typed into a growing highlight box

- **Source:** V1 D1, used ×11 (f1221–1243 @30).
- **Initial state:** a 29 px yellow sliver, 5 f after the cut.
- **Final state:** a 579×135 px `#F6EA00` box, centred, top at y = 181. Ink title cap is about 66 px.
- **Duration:** 18 f @24 (22 f @30).
- **Typing:** about 1.6 f/char @24. The box's right edge follows the typed text, which gives an S-curve width.
- **Price line:** fades in under the box over about 8 f, starting 8 f after the box completes.
- **Remotion:** combine `TypeOn` with an inline-block yellow background. The box width is the text width, so it grows naturally.

## M2 — Type-on / word-on

- **Labels:** 1 char/frame (V3 lower third: 26 chars in about 24 f).
- **Titles:** 1 word per VO word, a single step with no fade (V3 D2 at f12, 17, 29, 35 …). V1 quote words fade in at about 2 f per word.
- **Remotion:** `<TypeOn text start framesPerChar={1} />`. For words, map `[word, frame]` pairs and set `opacity: f >= at ? 1 : 0`. Take the frames from a narration timestamp file.

## M3 — Highlighter wipe

| Variant | Duration @24 | Curve | Source |
|---|---|---|---|
| Flat block behind a word | 9–19 f | `ease.pop` | V1 D4 (11 f @30), D7 (19–24 f @30) |
| Document line by line | 27–34 f per line, pause between lines on VO | `ease.wipe` (peak 650 px/s) | V3 D7 |
| Brush stroke, stop-motion | 9 f | linear, hard stop | V4 #3 |
| Wipe-off | 5 f, R→L | ease-in | V1 D4 |

- **Colour:** `#F0E136` with `mix-blend-mode: multiply` over paper, or `#F6EA00` opaque for title boxes. Dry-brush strokes use `#F8E10F` so they stay saturated under multiply on newsprint.
- **Dry-brush variant:** `<BrushHighlight start duration={10} easing={ease.accel}>` in `newspaper.tsx` (V4 swipe #2 accelerates +164/+273/+382 px per frame). For the linear V4 #3 swipe, pass `easing={(t) => t}`. Pair it with a ×1.2 snap zoom in 2 drawings as the stroke lands (V4 f7–8).
- **Remotion:** `<Highlight start duration fill>` in `motion.tsx`. For multi-line documents, chain one `Highlight` per line with `start = previous.start + previous.duration + pause`.

## M4 — Label / tape slide-in

- **Source:** V5 D2: offset (61,119)→0 px. The residual halves about every 20 f @30. Rotation settles +3°→0 on a −7° base tilt.
- **@24:** 30–90 f with `ease.expo`. The first quarter covers about 85 % of the travel.
- **Remotion:** `translate: (1-p)*dx, (1-p)*dy` and `rotate: base + (1-p)*3deg`, where `p = interpolate(f,[s,s+d],[0,1],{easing: ease.expo})`.

## M5 — Pop-in (disc, bullet, sticker, icon, TV)

| Item | Frames @24 | From | Source |
|---|---|---|---|
| Disc / circle | 10 | 79 % size | V2 #4: 24 f @60 |
| Bullet square | 7 | 58 % | V2 #7: 18 f @60 |
| Sticky note slap | 8 | 10 %, slight rotation | V6 D4 |
| Zoom bubble | 10 | point | V6 D8 |
| TV frame | 8–10 | 71 % | V1 D16 |

- **Curve:** `ease.pop`, no overshoot.
- **After the pop:** a linear creep of +2–5 % over 2 s (V2) keeps the hold alive.
- **Remotion:** `<PopIn start duration from>`.

## M6 — Staggered bar growth

- **Source:** V3 D8 (903 px in 30 f, stagger 6–10 f); V1 D15 (stagger 5 f @30, settled by 20 f).
- **@24:** 30 f per bar, stagger 6–8 f, `ease.grow`. The value label appears when the bar is about 70 % done.
- **Remotion:** see `ChartCard` in `StyleCalibration.tsx`: `width = interpolate(f,[start,start+30],[0,value*max],{easing: ease.grow})`.

## M7 — Hand-drawn stroke draw-on

| Stroke | Frames @24 | Source |
|---|---|---|
| Underline | 8 | V6 D5 |
| Circle / ellipse | 6–12 | V6 D8, V1 D9 |
| Arc around a hemicycle | 24 on, 24 off | V3 D9 |
| Map outline | 10 | V1 D4 |

- **Curve:** near-linear or `ease.tilt`.
- **Remotion:** SVG `<path pathLength={1} strokeDasharray={1} strokeDashoffset={1-p}>`. Use two slightly offset open loops so the stroke reads as hand-drawn (`MarkerEllipse`).

## M8 — Punch-in and creep

- **Source:** V3 D2: linear creep +0.13 %/f, then ×1.30 in 16 f with `ease.punch`, then creep at 0.1 %/f. V1 D21: ×1.40 in 12 f @30, then 0.1 %/f. V4: ×1.55 in 2 f (snap).
- **Remotion:** multiply three factors inline:
  `(1+0.0013*min(f,a)) * interpolate(f,[a,a+16],[1,1.3],{easing: ease.punch}) * (1+0.001*max(0,f-a-16))`.

## M9 — Camera push to detail

| Push | Frames @24 | Source |
|---|---|---|
| ×1.6 with re-centre | 76 | V3 D11 (`ease.push`) |
| ×1.18 | 22 | V6 D3 (`ease.tilt`) |
| ×1.73 | 42 | V6 D13 |
| ×1.75 zoom-out on a portrait | 11 | V1 D11 |

- Non-focus elements fade to 15–30 % during the push (V3 D9/D11).
- **Remotion:** animate `scale` and `translate` on a camera `AbsoluteFill` wrapping the scene, with `transformOrigin` on the target.

## M10 — Region zoom / lateral pan

- **Map zoom:** ×5.7 over 72 f, `cubic-bezier(0.55,0,0.15,1)` (V3 D3). ×30 over 48 f @24 with motion blur at peak velocity (V1 D3). Interpolate in log space (G4).
- **Lateral pan:** 1675 px in 68 f with `ease.pan`, no motion blur (V3 D10).
- **Stop-motion pan:** 207 px in 3 f, ease-in (V4).

## M11 — Slide-in of a prop or card

| Move | Frames @24 | Curve | Source |
|---|---|---|---|
| Magnifier from off-frame | 32–40 | ease-out, then linear drift 0.7 px/f | V3 D6 |
| Magnifier | 16 | ease-out | V6 D9 |
| Photo from right | ~10 | ease-out | V1 |
| Portraits from bottom | 14, 760 px | symmetric `ease.tilt` | V1 D5 |
| Facecam drop | 11 | ease-out | V5 #9 |

## M12 — Reading-order stagger

| Items | Spacing @24 | Source |
|---|---|---|
| Icons / people | about 2 f | V3 D4 |
| Thumbnails | 3–8 f | V1 D2 |
| Tags | 8–24 f | V6 D15 |
| Photo drops | 20–25 f, accelerating | V3 D13 |

Each item appears at full size or pops in 2 drawings.

## M13 — Footage into an inset card

- **Source:** V1 D17.
- Full-bleed footage scales to a rounded card (about 1505×800 px) on black in about 10 f with ease-out.
- A ▶ glyph and a yellow italic one-word caption sit under it.

## M14 — Living hold (creep / boil)

| Family | Hold behaviour | Source |
|---|---|---|
| Flat | fully static | V3 D1 |
| Collage | linear scale drift 0.2–0.4 % per 2 f; slow pan of about 25 px/s | V6 D6/D17 |
| Ken Burns on stills | +2.5 % over 43 f | V1 D25 |
| Stop-motion | A-A-B texture boil at 3.3 Hz | V4 |

Grain refresh (12 fps) also keeps holds alive (V6).

## M15 — Number counter

- **Source:** V1 D6.
- 11 discrete values over 22 f @24 (12 fps), ease-in-out on the value.
- A highlight grows behind the final number, overlapping the last steps.

## M16 — Line-chart draw

- **Source:** V1 D14.
- The line draws L→R over about 62 f @24 at near-constant x-speed, stepped at 6 fps.
- The title types in during the draw.
- **Remotion:** SVG path dash-offset, `stepped(f, 4)`.

## M17 — Radial zoom-blur in/out

- **Source:** V1 f0–8; V6 D19.
- The outgoing shot streaks over 2–4 f; the incoming shot resolves over 4–6 f, then settles with ×0.88 ease-out over 12 f.
- **Remotion:** `@remotion/effects` `zoomBlur()` on an `HtmlInCanvas` wrapper, or a CSS `filter: blur()` ramp. Not validated in the calibration piece.

## M18 — Accelerate into a cut

- **Source:** V1 D22: scale ratio per 2 f of 1.000, 1.004, 1.009, 1.021, 1.036, then a hard cut.
- **@24:** 6–8 f with `ease.accel`, about +7 % total.

## M19 — Lower third

- **Source:** V3 D12.
- Order of events:
  1. Two colour dots travel in (≈ 10 f).
  2. A cream plate `#EEE4D8` wipes L→R in 3 f.
  3. The name types on in bold serif caps (about 1 char/f).
  4. The bold-italic role types at 1 char/f.
- **Position:** left edge x = 139; plate top y ≈ 814; bottom at about 916.

## M20 — Data morphs (explode, donut, hemicycle)

- **Source:** V3 D5/D9.
- Districts move apart into a grid in 16 f, then fade to 30 % over 12 f.
- Donut rings draw radially in 18 f, all at once.
- Hemicycle dots sweep in by arc in 28 f. Non-focus parties dim to 15–25 % opacity over 20 f.

---

## Transitions

| ID | Transition | Duration @24 | How it behaves | Source | Remotion |
|---|---|---|---|---|---|
| T1 | **Hard cut** (default) | 0 | About 82 % of V1 and nearly all of V3. Cut 2 f before the next VO phrase. Montage bursts every 5–25 f | V1, V3 | `Series` / adjacent `Sequence` |
| T2 | **Zoom-through** | 24 + 28 | Outgoing ×1→1.29 ease-in; hard switch; incoming ×1.82→1 ease-out; no cross-fade | V6 D10 | `zoomThrough(52)` presentation (**validated**) |
| T3 | Short dissolve | 3–6 | Between archival stills and footage | V1 | `fade()` with `linearTiming({durationInFrames: 4})` |
| T4 | Loupe / iris reveal | about 75 | A lens crosses the frame showing the next layer inside, then grows to fill it | V3 f1330–1423 | `clip-path: circle()` animated on the incoming scene inside a custom presentation |
| T5 | Whip / push | 3–14 | A fast ease-out translation of the whole frame (−309 px in 14 f), or a photo carousel push (−739 px in 2 f) | V6 D7, V1 D13, V5 | `slide()` with a custom bezier, or translate a camera layer |
| T6 | Page curl | 8 | Corner peel | V1 f126 | Asset-based or WebGL. Novelty |
| T7 | Crumpled-paper wipe | 18 | Paper texture rises from the bottom | V1 f1662 | Asset (paper texture video) plus a mask |
| T8 | Focus-ring dissolve | 16 | Concentric white rings over a dissolve | V1 f1930 | SVG rings + `fade()` |
| T9 | Fade to black | 29–58 | Linear, not stepped | V2, V1 | Opacity overlay |
| T10 | Radial zoom-blur / rack focus | 4–16 | Defocus or streak out, resolve in | V6, V3 f3548 | `zoomBlur()` / `blur()` effects |
| T11 | Cloud fly-through | 26 | White → cloud texture parts | V5 | Asset-based (cloud plates) |
