# Color, Texture & Lighting — Vox-style reference set (V1–V6)

Tags: **MEASURED** = median of real pixels (source = video / frame # / box `x0,y0,x1,y1` in native-res px; V4 is 3840x2160, all others 1920x1080). **ESTIMATE** = derived/fitted/judged value.
Frame # = native frame index (`full/f{frame}.png`; consecutive frames in `color/consec/`).
Reproduce: `python3 -P color/<script>.py` from `reference-analysis/` — `palettes.py`, `samples.py`, `texture.py` + `texture2.py`, `shadow_fit.py`, `luma.py`, `swatch_contrast.py`. Raw numbers: `palettes.json`, `samples.json`, `texture.json`, `luma.json`, `contrast.json`. Swatches: `palette.png`. Luma plot: `luma_timeline.png`.

Video character (seen in contact montages):
- **V1 Porsche** (30 fps, 197 s): warm off-white paper graphics + yellow tape titles, alternating with archival B&W and modern color footage, dark interstitials. Graphics frames ≈ 56%.
- **V2 Camera** (60 fps, 7 s): cream paper, engraving cutouts, golden-yellow disc, black italic display type.
- **V3 Elections** (23.976 fps, 586 s): flat near-white digital "paper", flat chart colors (red/blue/green/purple/pink), grey cutout people, talking-head footage; no grain.
- **V4 Highlight** (10 fps, 4K, 16 s): crumpled aged-paper background, ochre highlighter, maroon date tag, newspaper serif.
- **V5 Rabbit** (30 fps, 38 s): kraft treasure-map paper with a vertical phone card (heavy drop shadow).
- **V6 Epigenetics** (23.976 fps, 51 s): 4:3 desk collage (grey dotted paper, tape, chalkboard cards) pillarboxed in 16:9.

---

## 1. Dominant palettes (k-means in CIELAB, all `full/` frames, 320x180 per frame) — MEASURED

Footage vs graphics split by hand from the montages. V1 footage frames: 180, 540, 720, 1440, 1620, 1800, 1980, 2640, 3600, 3780, 4500, 4680, 4860, 5220. V3 footage frames: 360, 2158, 4172, 7624, 11580, 11796, 12228, 12659, 12875, 13091–13954. V6 footage frame: 575. V2, V4 and V5 are all graphics.
HEX values are cluster centroids. The 8-bit Lab round trip can shift them by about ±3 levels. Use the §2 samples as exact colors.

| Video | Set (frames) | Palette (HEX : coverage %) |
|---|---|---|
| V1 | all (32) | #ECE4DA 22.8 · #CEC6BE 17.4 · #080908 13.9 · #74716B 10.9 · #989EA2 9.9 · #504C49 9.2 · #2D2B2A 8.4 · #B1A36F 4.7 · #CE441D 1.4 · #EAE024 1.4 |
| V1 | graphics (18) | #EDE5DB 32.7 · #D2CBC2 24.5 · #120E0D 10.9 · #AEA67F 9.4 · #8D9AAA 8.4 · #846659 6.2 · #3E3737 5.6 · #EBE126 2.3 |
| V1 | footage (14) | #040807 19.4 · #6F6B65 16.7 · #4E4A48 15.5 · #2C2B2A 13.3 · #BDB4A7 12.3 · #E1D9CF 10.8 · #928D88 9.5 · #CC5A1C 2.5 |
| V2 | all (9) | #E4DDC8 58.1 · #EEEAD6 26.8 · #191815 2.9 · #E7B61B 2.4 · #D1CDC0 2.1 · #5B5347 1.8 · #B4B1A6 1.6 · #3D372F 1.5 · #797366 1.4 · #979487 1.3 |
| V3 | all (64) | #F8FAF7 67.2 · #232124 8.0 · #9B908F 4.6 · #E1D9CB 4.5 · #C5B3AA 4.2 · #483B3D 3.9 · #75635D 2.7 · #64C6B0 2.6 · #E35C43 1.3 · #5CB3F4 1.1 |
| V3 | graphics (50) | #F8FAF7 86.7 · #D1CDCC 4.3 · #909192 2.8 · #424042 2.1 · #EB5F49 1.4 · #5BB4F7 1.3 · #CA7EC3 0.8 · #AFD063 0.6 |
| V3 | footage (14) | #2B2A2F 26.2 · #1C171A 14.3 · #B49E8D 14.2 · #DACCBA 12.1 · #5B423C 10.7 · #8A6C60 9.6 · #67B09E 8.8 · #54E1D2 4.2 |
| V4 | all (11) | #BAB4A7 29.2 · #B3ADA1 27.4 · #C1BBAF 17.4 · #ABA599 14.1 · #797369 3.2 · #908C84 2.6 · #484744 2.3 · #B99443 2.1 · #5F5B53 1.5 · #7E403F 0.3 |
| V5 | all (13) | #B5A087 42.5 · #AD977D 29.4 · #C8B397 7.4 · #A0826A 4.6 · #806B57 4.2 · #DCDCD5 3.1 · #605146 3.1 · #4B6F7F 2.0 · #3F332D 2.0 · #100F10 1.5 |
| V6 | all (18) | #1E1F20 33.2 · #D7D7D7 17.9 · #C8C8C8 16.2 · #38363C 10.0 · #B2AFB0 6.5 · #7D7573 5.5 · #969397 4.4 · #5D5454 3.2 · #DACA3B 2.1 · #8DA346 0.9 |
| V6 | graphics (17) | #1E1F20 33.7 · #D4D5D6 21.5 · #C4C4C4 14.7 · #38363C 10.6 · #807C79 6.9 · #A4A4A8 6.6 · #5C5557 3.3 · #CAC53D 2.8 |

Reading: each video uses **one dominant neutral background, covering 60–87% of graphics pixels**. Accents are rare: yellow is 1.4–2.8% of pixels and red/blue are about 1% each. V6's top cluster, #1E1F20, is mostly the pillarbox bars plus the chalkboard cards.

## 2. Targeted samples (median of masked pixels inside box) — MEASURED

Mask: `all` = the whole box. `dark` = the darkest 3% of the box (glyph cores). `light` = the lightest 3%. Hue masks are HSV ranges, defined in `samples.py`. The box shown is the bounding box of the pixels used.

**Backgrounds**
| Role | HEX | Source |
|---|---|---|
| V1 paper, bright center | #F2E8DF | V1 f1260 (800,30,1100,120) |
| V1 paper, left side | #DED4CE | V1 f1260 (40,300,299,999), sd 6.1 |
| V1 paper (Taycan card) | #DCD2CA | V1 f5040 (40,700,499,999) |
| V2 cream paper | #E5DDC6 | V2 f270 (1300,750,1879,1049), sd 0.8 |
| V2 cream paper (engraving scene) | #DFD8C6 | V2 f135 (40,500,699,899) |
| V3 flat "paper" | #F6F5EA (perfectly flat, sd 0) | V3 f2877 (1700,900,1900,1060); V3 f647 corner = #F6F4EC |
| V4 aged paper | #BFB8AC (center ≈ luma 190, corners 166) | V4 f0 (400,400,3439,1759) |
| V5 kraft map | #AD987F | V5 f0 (1500,800,1899,1059) |
| V6 desk paper (lit area) | #D8D6D8 | V6 f791 (1250,450,1499,649) |
| V1 dark interstitial | #12100D | V1 f1080 (40,100,299,899) |
| V1 dark map texture | #040401 (sd 32, textured) | V1 f4140 (20,20,299,299) |
| V6 chalkboard card | #1E1C1F | V6 f935 (400,100,1499,299) |
| V3 credits panel | #282828 | V3 f13307 (40,0,559,1079) |
| **V6 pillarbox bars** | **#1F1F1F**, rgb(31,31,31), sd 0.0: pure flat, not black. Bars are x 0–239 and 1681–1919; the content area is 1440 px wide (4:3) | V6 f863 (10,20,189,1059) and (1730,20,1909,1059) |

**Highlighter / tape yellows**
| Role | HEX | Source |
|---|---|---|
| V1 title tape (opaque) | #F6EA00 | V1 f1260 (664,182,1253,317) |
| V1 subtitle yellow italic | #E5E605 | V1 f1980 (1000,934,1739,987) |
| V1 card border (yellow-green, glow edge) | #AAB83C (anti-aliased; core ≈ #D4E024, ESTIMATE) | V1 f2640 (1300,704,1585,1015) |
| V2 disc (golden) | #EAB718 | V2 f225 (660,348,953,640) |
| V3 text highlighter | #F0E136 | V3 f3740 (110,532,1815,679) |
| V3 dot | #F6EA22 | V3 f1510 (210,354,429,575) |
| V4 highlighter ochre (over paper) | #BC933C | V4 f105 (612,392,2311,603) |
| V6 paper tape | #E0D238 | V6 f144 (240,119,1661,1079) |

Translucent highlights, as a multiply color (result ÷ background × 255). ESTIMATE, derived from the measured pairs:
- V4 ochre: **multiply #FBCC59** over #BFB8AC.
- V5 red word highlight: result #AD5241 over #AD987F gives **multiply #FF8A83**. CSS ≈ `background: rgba(220,60,40,.45); mix-blend-mode: multiply`.
- V3 highlighter: effectively opaque (multiply #F9EA3B).

**Accent reds / blues / chart colors**
| Role | HEX | Source |
|---|---|---|
| V3 Republican red bar | #FC3828 | V3 f1942 (762,217,1059,437) |
| V3 Democrat blue bar | #50B7FE | V3 f1942 (1060,226,1589,435) |
| V3 "Yes" pink bar | #FF85C1 | V3 f647 (475,283,1151,607) |
| V3 map green | #62C583 | V3 f2446 (926,192,1205,633) |
| V3 map purple | #BA75BB | V3 f2877 (484,384,1315,813) |
| V3 map grey (states) | #99989B | V3 f1726 (661,206,966,705) |
| V3 blue stipple on photos | #9BA5BD | V3 f12012 (560,330,1300,800), 7.2% coverage |
| V3 credits name blue | #B4D1DD | V3 f13307 (334,103,643,124) |
| V3 end-card teal backdrop | #5DA695 | V3 f13307 (1500,100,1899,399) |
| V2 red square bullet | #8B1C1B | V2 f225 (1374,617,1398,641) |
| V4 date tag maroon | #7E4341 | V4 f105 (370,234,969,359) |
| V6 methyl red dot | #A62236 | V6 f935 |
| V6 methyl green dot | #33B02D | V6 f935 |
| V6 tube cap blue | #5990CD | V6 f432 |
| V1 cutout car red (photo) | #D52701 | V1 f2820 (800,800,1575,939) |

**Map tones**
| Role | HEX | Source |
|---|---|---|
| V1 physical map, land | #AE9E6A | V1 f360 (600,300,1499,799) |
| V1 physical map, sea | #6F93BC | V1 f360, full frame, blue mask |
| V5 sea (inside the phone card) | #487487 | V5 f180 (258,134,715,864) |
| V3 political map flats | grey #99989B / green #62C583 / purple #BA75BB (see table above) | |

**Text**
| Role | HEX | Source |
|---|---|---|
| V1 title ink (serif) | #312E24 | V1 f1260 (714,214,1205,281) |
| V2 display ink | #0C0803 | V2 f225 (700,420,1201,599) |
| V2 engraving ink | #38352C | V2 f45 (700,287,1499,831) |
| V3 title ink | #201E18 | V3 f2877 (453,122,1464,179) |
| V4 headline ink | #393733 | V4 f105 (444,434,3163,689) |
| V5 body ink | #120702 | V5 f0 (933,297,1299,449) |
| V6 title ink | #3F3D41 | V6 f791 (760,135,1151,183) |
| V3 credits white (roles) | #E3E3E3: off-white, never #FFF | V3 f13307 (370,69,644,90) |

**Drop-shadow color (V5).** Shadow pixel #6E5B49 next to background #AD9377. The per-channel ratios are 0.64, 0.62 and 0.61, so the shadow is a near-neutral black multiply that slightly warms the paper. Use `rgba(0,0,0,a)`, not a tinted color.
Sources: V5 f0 (722,800,729,899) and (800,800,849,899).

## 3. WCAG contrast (main pairs, from MEASURED values)

| Pair | FG | BG | Ratio | Level |
|---|---|---|---|---|
| V1 title ink on paper | #312E24 | #DED4CE | 9.32 | AAA |
| V1 title ink on yellow tape | #312E24 | #F6EA00 | 10.79 | AAA |
| V1 yellow subtitle on dark bg | #E5E605 | #12100D | 14.16 | AAA |
| V2 title ink on paper | #0C0803 | #E5DDC6 | 14.73 | AAA |
| V2 ink on yellow disc | #0C0803 | #EAB718 | 10.73 | AAA |
| V3 title ink on paper | #201E18 | #F6F5EA | 15.21 | AAA |
| V3 ink on highlighter | #201E18 | #F0E136 | 12.32 | AAA |
| V3 red bar on paper | #FC3828 | #F6F5EA | 3.34 | AA-large (graphic) |
| V3 blue bar on paper | #50B7FE | #F6F5EA | 2.01 | fail (fine for fills; don't use for text) |
| V3 credits white on dark | #E3E3E3 | #282828 | 11.49 | AAA |
| V3 credits light-blue on dark | #B4D1DD | #282828 | 9.20 | AAA |
| V4 headline ink on aged paper | #393733 | #BFB8AC | 6.03 | AA |
| V4 ink on ochre highlight | #393733 | #BC933C | 4.17 | AA-large |
| V5 body ink on kraft map | #120702 | #AD987F | 7.17 | AAA |
| V5 red highlight vs kraft | #AD5241 | #AD987F | 1.87 | fail (it's a fill behind ink, ink stays 7:1) |
| V6 title ink on desk grey | #3F3D41 | #D8D6D8 | 7.43 | AAA |
| V6 yellow tape on chalkboard | #E0D238 | #1E1C1F | 10.83 | AAA |
| V6 ink on yellow tape | #201E18 | #E0D238 | 10.67 | AAA |

Rule observed: **text is near-black warm ink at 6–15:1 on its background**. Saturated colors are used only as fills, bars and highlights, never as text.

---

## 4. Texture (MEASURED unless tagged)

Method:
- Flat 64x64 blocks are picked automatically: the lowest std after a σ=4 blur, background only. V4 was downscaled to 1080p first so all px units are comparable.
- **grain** = std of (L − Gauss σ1.5).
- **mid** = std of (Gauss σ1.5 − Gauss σ8): paper mottling.
- **size** = autocorrelation half-width at the 0.5 level, on L − Gauss σ6.
- **temporal** = correlation of the grain residual between consecutive frames (1 = static texture, 0 = fresh grain each frame), plus std(frameA − frameB)/√2.
- Grain "fps": change cadence read from `framediff.tsv` mad values on static shots.

| Video | grain std (8-bit) | mid/paper std | size (AC half-width px @1080p) | chroma | temporal corr | grain changes | verdict |
|---|---|---|---|---|---|---|---|
| V1 | **1.1–1.6** (bg 1.06, light areas 1.62) | 0.7 | 0.9–1.1 | mono (R/B residual corr 1.0) | **−0.04 – 0.16** (fresh) | mad spikes every 2–3 frames at 30 fps (2:3 cadence), **≈12 fps** | animated fine mono grain, subtle |
| V2 | 0.14 | 0.24 | ~3 (compression) | — | 0.14 | spikes every 6 frames at 60 fps (**10 fps**), but amplitude near 0 | essentially clean, faint 10 fps boil |
| V3 | **0.0** | 0.0 | — | — | — | mad alternates 0.01/0.12 every other frame (12 fps), negligible | clean flat digital |
| V4 | 2.5 | **1.6** (crumple) | 1.15 | mono | **0.92** (mostly static) | 2 of every 3 frames change at 10 fps (≈6.7 changes/s), mad ≈2.4 | static paper scan + slight jitter/boil |
| V5 | 4.5 on kraft (texture, not grain) | 1.6 | 0.65 | mono | **0.99** (static) | card/footage motion every 3 frames (10 fps) | baked-in static paper texture, no grain |
| V6 | **4.9** | 1.5 | 0.6 | mono | **0.20** (fresh) | strict on-twos: mad ≈1–2 every 2nd frame at 23.976 → **12 fps** | strongest animated grain |

**Vignette / light falloff.** Corner vs center luma, from single flat frames plus the median stack of graphics frames.
- **V4: 12.6% radial** (center 190 → corner 166; median-stack 8.3%). Classic smooth vignette.
- **V1: ~10–15%.** Paper is #F2E8DF top-center → ~#DED4CE edges. Corners 188–202 vs top-mid 232.
- **V5: ~5–8%.** Corners ~147, edge mids 154–161.
- **V6: directional light, not radial.** Left side ~107–127 vs right side 181–203 (≈40% left-to-right drop), lit from top-right. The desk also carries large soft object shadows.
- **V2, V3: 0%.** Perfectly flat.

**Paper texture.**
- V4: present and strong. Crumple folds, mid std 1.6 and low-frequency std 0.4, static.
- V5: kraft fibers plus mottling, static.
- V1: faint grid paper (dotted/thin lines, visible in f1440/f5760 crops) plus mild texture.
- V6: dot-grid paper (≈ 30–40 px pitch, ESTIMATE from crop).
- V2: clean cream with faint horizontal streaks.
- V3: none.

**Blur / DOF** (variance of Laplacian):
- V6 f72: out-of-focus props at the frame edges (pen 523, top-right object 551) vs the in-focus title "Genetics" 811. This is mild fake DOF on desk props. ESTIMATE: ~2–4 px Gaussian on edge props.
- V1 f5580: end-collage polaroids are soft (29–57, very blurred) and carry a strong **RGB split / chromatic aberration**. On the bottom border edge the B, G and R edges sit at rows 791, 796 and 799 → **R−B ≈ 8 px vertical, G centered** (V1 f5580, cols 200–400). Also seen on V1 f2460 TV.
- V1 f0: radial zoom-blur map transition (lapvar 211).

**Archival photo grade** (CIELAB midtones L 25–75; C* = chroma; ≤3 = neutral, sepia ≈ b*>8):
| Source | a* | b* | median C* | Read |
|---|---|---|---|---|
| V1 f540 archival footage | 2.6 | 3.8 | 4.9 | very slight warm |
| V1 f720 archival footage | 0.8 | 2.1 | 2.6 | neutral-warm |
| V1 f1080 portrait (box 520,80,1150,1000) | −0.3 | 6.3 | 2.9 | faint yellow cast |
| V1 f1440 B&W photo card | 0.1 | 2.1 | 2.8 | neutral |
| V1 f1620 / f1800 footage | −0.3/0.6 | 0.9/2.3 | 0.0/3.7 | neutral |
| V1 f1980 tinted car | −9.0 | 6.7 | 11.1 | green-cyan duotone tint (hue 143°) |
| V3 f360 archival film | 0.7 | −0.2 | 0.1 | pure neutral |
| V3 f12012 photo card | 1.3 | −4.2 | 3.2 | neutral B&W + blue stipple |
| V4 f105 news photo | 1.1 | 4.5 | 4.8 | slight warm (paper bleeds through) |
| V2 f135 camera cutout | 3.8 | 14.0 | 13.5 | **sepia / warm** (object color, not a grade) |
| V6 f1151 engraving rat | 2.3 | 4.7 | 2.8 | neutral-warm |

→ Archival material is **near-neutral B&W with a faint warm lift (b* +2…+6)**, not sepia. An ESTIMATE grade for code: desaturate fully, then tint toward #F2E8DF at 5–8%.

**Halftone / screen** (FFT on 512 px crops; peak/ring = peak magnitude over the median of its frequency ring):
- **V3 f12012 & f11365**: no regular screen. Instead an **irregular blue stipple overlay**: #9BA5BD dots, median area 24 px² (≈5 px dots), nearest-neighbour spacing 10.9 px, 7.2% coverage. The FFT peaks are only 6.6–7.3x the ring median, i.e. structure, not a screen.
- V1 f1440: peak 4.7x at 28 px, from the grid paper, not halftone.
- V4 f105 photo: peak 13.6x at 31.7 px (4K) ≈ 16 px @1080p, angle 141°. This is consistent with a coarse print texture / scan pattern on the news photo (ESTIMATE; not visually a clear dot screen).
- **No true AM halftone found** in any video.

**Code-ready texture parameters (ESTIMATE, derived from the measurements above)**
```
grain.amplitude   : 0 (V3 clean) | 1.0–1.6 (V1 subtle) | 4–5 (V6 strong)  — std in 8-bit levels, monochrome, additive/overlay
grain.size        : 0.6–1.1 px @1080p (render noise at 1px, optional blur σ≈0.5)
grain.fps         : 12 (change on twos @24, 2:3 cadence @30); V2 10 fps
paper.texture     : static (temporal corr ≥0.92); mid-freq std 0.7–1.6, low-freq 0.4–1.5; optional 6.7–12 fps position jitter (V4)
vignette.strength : 0 (flat digital) | 8–15% radial luma drop center→corner (V1,V4) | 5–8% (V5)
vignette.shape    : radial, falloff starts ~r=0.4 of half-diagonal (V4 ring medians 190,189,188,186,183,179,174,172,169,166)
light.directional : V6 only — ~40% drop right→left (top-right key)
chromatic.aberr   : V1 only, R/B ±4 px (8 px total) on collage cards
archival.grade    : saturation 0, warm lift b* +2…+6 (≈5–8% #F2E8DF tint), contrast normal
stipple.overlay   : V3 photos — #9BA5BD dots ~5px, ~11px spacing, ~7% coverage
```

## 5. Drop shadows (fitted: Gaussian-blurred offset box over the luma profile, `shadow_fit.py`)

| Object | Fit | CSS equivalent |
|---|---|---|
| **V5 f0 phone card on kraft** (joint fit of the right+left and bottom+top edges; profile rows 800–900 / cols 450–650) | α 0.62–0.66, offset x 10 / y 12 px, spread 1–3 px, σ 12.5–14.5 px. Darkening at the edge is 0.53 on the shadow side vs 0.17 on the light side. | MEASURED fit → `box-shadow: 10px 12px 27px 2px rgba(0,0,0,.62)` ESTIMATE |
| **V3 f12012 photo stack** (right edge rows 300–450; joint with left edge) | α 0.58–0.66, offset 3–6 px, spread 2, σ 4–5 px. Darkening 0.48 at the edge, gone after ~18 px. | `box-shadow: 4px 5px 10px 2px rgba(0,0,0,.5)` ESTIMATE |
| **V6 f791 paper card** (right edge rows 450–650) | A dark torn-edge outline ~5 px wide (luma 84 on 215), then a soft tail: d = 0.22 at the edge, decaying to 0 over ~15–20 px | `filter: drop-shadow(3px 4px 8px rgba(0,0,0,.25))` + 2–4 px #3a3a3a rough edge stroke, ESTIMATE |
| V1 photo cards (f1440, f2640) | No measurable drop shadow. The cards use a **rounded yellow-green border/glow** instead (~#D4E024 core, radius ≈ 20 px, ESTIMATE) | `border: 6px solid #D4E024; border-radius: 20px; box-shadow: 0 0 6px rgba(212,224,36,.6)` ESTIMATE |

Shadow color is neutral black multiply. The ratio is near-equal across R, G and B (§2).

## 6. Luma timeline / light–dark alternation (`framediff.tsv` luma, 1 s smoothing; classes L ≥170, M 90–170, D <90; strip = one letter per 2 s)

| Video | mean luma | % L / M / D | class switches (runs ≥1 s) | median run | pattern |
|---|---|---|---|---|---|
| V1 | 129 | 28 / 47 / 26 | **47 in 197 s** | 2.8 s | Constant alternation: paper graphic (L) ↔ archival/modern footage (M) ↔ dark interstitial/cards (D), roughly every 3–6 s. Dark runs at 4–12, 20–22, 32–36, 42–44, 50–56, 60–68, 114–122, 126–130, 134–142, 170–172 s. Strip: `MMDDDDMLMMDMLMLMDDMLLDMMMDDDLMDLMDMLMMMMMMLLMMLLMLLMMLLLMDDDDMLDDMLDDDDLLMMMLMLMMMMLMDMMMMMMLLLLLMD` |
| V2 | 201 | 86 / 11 / 3 | 0 | 6 s | all light cream |
| V3 | 205 | 79 / 18 / 3 | 24 in 586 s | 8.4 s | Long light-paper stretches. Mid-tone breaks are talking-head/news footage (88–96, 172–180, 402–408, 476–484, 492–538 s). Dark only for the archival film (14–20 s), one 2 s beat at 318 s, 484–492 s, and the credits (540–586 s, M with dark panel). Otherwise solid `L` |
| V4 | 158 | 57 / 36 / 7 | 2 | 5.5 s | paper L → M as text and photo fill → black at end |
| V5 | 153 | 0 / 99 / 1 | 0 | 37 s | single steady mid-tone kraft scene |
| V6 | 122 (the 31-luma bars pull it down) | 0 / 88 / 12 | 2 | 7.4 s | Steady desk mid-tone. One dark beat at ~38–44 s, a full-frame chalkboard DNA close-up |

Take-away: **the light graphic base is the default (V2, V3, V4). V1 is the outlier, cutting light↔dark every ~3 s for documentary rhythm. Dark beats are reserved for footage, chalkboard close-ups and credits.** Plot: `luma_timeline.png`.

---

## 7. Consolidated cross-video token proposal

| Token | Value | Tag / source |
|---|---|---|
| `background-paper` | **#E5DDC6** | MEASURED V2 f270 (warm cream) |
| `background-paper-light` | #F6F5EA | MEASURED V3 f2877 (flat digital) |
| `background-paper-warm` | #F2E8DF center → #DED4CE edge | MEASURED V1 f1260 (gradient is the vignette) |
| `background-paper-aged` | #BFB8AC | MEASURED V4 f0 |
| `background-kraft` | #AD987F | MEASURED V5 f0 |
| `background-desk` | #D8D6D8 | MEASURED V6 f791 |
| `background-dark` | **#12100D** | MEASURED V1 f1080 |
| `background-dark-board` | #1E1C1F | MEASURED V6 f935 |
| `pillarbox` | #1F1F1F | MEASURED V6 f863 |
| `ink` | **#201E18** | MEASURED V3 f2877 (V1 #312E24, V2 #0C0803) |
| `ink-soft` | #393733 | MEASURED V4 f105 / V6 #3F3D41 |
| `text-on-dark` | #E3E3E3 | MEASURED V3 f13307 |
| `accent-highlight` | **#F0E136** (highlighter) | MEASURED V3 f3740 |
| `accent-highlight-pure` | #F6EA00 (tape/title box) | MEASURED V1 f1260 |
| `accent-highlight-gold` | #EAB718 | MEASURED V2 f225 |
| `accent-highlight-ochre` | #BC933C (multiply #FBCC59) | MEASURED V4 f105 / ESTIMATE multiply |
| `accent-red` | **#FC3828** | MEASURED V3 f1942 |
| `accent-red-deep` | #8B1C1B (maroon variant #7E4341) | MEASURED V2 f225 / V4 f105 |
| `accent-blue` | **#50B7FE** | MEASURED V3 f1942 |
| `accent-blue-muted` | #5990CD | MEASURED V6 f432 |
| `chart-green` / `chart-purple` / `chart-pink` | #62C583 / #BA75BB / #FF85C1 | MEASURED V3 |
| `grey-map` | #99989B | MEASURED V3 f1726 |
| `grey-mid` | #74716B | MEASURED k-means V1 (10.9%) |
| `grey-light` | #C8C8C8 | MEASURED k-means V6 |
| `shadow-card-large` | `10px 12px 27px 2px rgba(0,0,0,.62)` | ESTIMATE, fit V5 f0 |
| `shadow-card-small` | `4px 5px 10px 2px rgba(0,0,0,.5)` | ESTIMATE, fit V3 f12012 |
| `shadow-paper-soft` | `drop-shadow(3px 4px 8px rgba(0,0,0,.25))` | ESTIMATE, V6 f791 |

Swatches: `color/palette.png` (per-video k-means bars sized by coverage, plus these tokens).

### Caveats
- Every frame is h264-compressed, so measured grain is a **lower bound**. Compression smooths fine grain, and grain size (0.6–1.1 px) is close to the codec limit.
- The footage/graphics split is a manual list over sparse `full/` frames (9–64 per video).
- `color/extra/` holds 16 mislabeled PNGs from a failed extraction loop. They are all V6 frames 863–866 under wrong prefixes. Ignore or delete them; `color/consec/` is the correct set.
