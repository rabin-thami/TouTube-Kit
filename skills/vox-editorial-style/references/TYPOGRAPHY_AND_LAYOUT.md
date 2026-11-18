# Typography & Layout

## 1. Font identification status

**No reference font was positively identified.** Vox and its imitators use proprietary or licensed faces. Everything below is a visual category plus a free Google Fonts stand-in, chosen by comparing letterforms in full-resolution crops (`reference-analysis/V1_porsche/work/typesheet.jpg`, `V2_camera/work/title_crop.jpg`, `V3_elections/work/c_*.png`).

| Category observed | Where | Stand-in (installed via `@remotion/google-fonts`) | Alternatives |
|---|---|---|---|
| Heavy transitional news serif, caps, bracketed serifs | V3 title card, V1 map labels, V6 headers | **Source Serif 4** 900 | Merriweather Black, Newsreader ExtraBold |
| Same serif, semibold, sentence case | V3 chart titles, legends | **Source Serif 4** 600 | Newsreader 600 |
| Old-style serif italic with old-style figures | V1 captions, quotes, emphasis words; V5 accent tags | **Source Serif 4 Italic** | Gelasio Italic (Georgia metrics), EB Garamond Italic |
| High-contrast display serif | V4 title, V2 name | Playfair Display 700/900i (not installed) | DM Serif Display |
| Heavy condensed italic serif | V2 "Camera" | Playfair Display Black Italic (not installed) | — |
| Neo-grotesk sans | V3 data labels and big numbers; V2 kicker; V6 "Sexual orientation" | **Inter** 400/500/700 | Public Sans, Archivo |
| Geometric/humanist sans (body) | V2 bio, V5 caption | Poppins / Nunito Sans (not installed) | Mulish |
| Marker hand lettering, caps | V3 pink notes, V6 tape and sticky, V5 notes | **Permanent Marker** | Gochi Hand, Kalam Bold |
| Blackletter masthead | V4 | UnifrakturMaguntia (not installed) | — |

Only the four faces in bold are loaded in `templates/style-system/ (copied into the project as src/style-system/)fonts.ts`. Add others with `loadFont()` from `@remotion/google-fonts/<Name>`.

## 2. Type scale (1080p px)

The references were measured as cap height. Font size is approximately cap height ÷ 0.66 for Source Serif 4 and ÷ 0.73 for Inter.

| Role | Measured cap | Font size to use | Weight / style | Case | Tracking | Line height | Source |
|---|---|---|---|---|---|---|---|
| Title card | 93 px (after punch) | 118 px pre-punch (cap ≈ 80 → ≈ 104 after ×1.3) | Serif 900 | CAPS | −0.01em | 0.95–1.0 | V3 f150 [Measured]; calibration |
| Card title in yellow box | 66 px | 100 px | Serif 600–700 | Title Case | 0 | 1.0 | V1 f1260 [Measured] |
| Section header on paper | x-height 40 | 85–90 px | Serif 700 | Title Case | 0 | 1.1 | V6 f144 [Measured] |
| Chart title | 34–36 px | 52 px | Serif 600 | Sentence | 0 | 1.2 | V3 [Measured] |
| Legend / diagram label | 34 px | 50 px | Serif 600–700, series colour or ink | Sentence | 0 | 1.2 | V3 f4640 |
| Data label / value | ~30 px | 34–36 px | Sans 500 / 700 | Sentence | 0 | 1.2 | V3 [Inferred] |
| Caption under footage | 30–35 px | 46–52 px | Serif italic, `#E4E704` on footage | sentence | 0 | 1.2 | V1 f1980 |
| Lower-third name | 36 px | 54 px | Serif 700 | CAPS | +0.02em | — | V3 f2200 [Measured] |
| Lower-third role | 28 px | 42 px | Serif 700 italic | Sentence | 0 | — | V3 f2200 [Measured] |
| Annotation | 20–34 px | 30–46 px | Marker, `redDeep` / pink | CAPS or lower | +0.02em | — | V3, V6 |
| Axis tick | 10–12 px | 16–18 px | Sans | — | — | — | V3 [Inferred] |
| Body paragraph | x-height 15 | 24 px / 30 px leading, measure about 700 px | Sans 400 + 600 run-ins | Sentence | 0 | 1.25 | V2 [Measured crop] |

**Hierarchy rule.** Have at most three type sizes on screen: title, label and annotation. Make the serif title 1.5–2.5× the label size.

## 3. Text animation

| Behaviour | Spec | Source |
|---|---|---|
| Entrance: typing | 1 char/f labels; about 1.6 f/char titles (@24) | V3 D12, V1 D1 |
| Entrance: word-on | one step per narrated word, no fade | V3 D2 |
| Entrance: word fade | each word grey→ink over about 2 f, sequential | V1 D11 |
| Entrance: rise + fade | 10 px rise, 12 f @60 ≈ 5 f @24 | V2 #6 |
| Entrance: ink-in | eroded letters complete over 4 drawings | V4 |
| Exit | mostly a hard cut. Otherwise the highlight erodes then letters drop out right→left (V4), or a wipe-off R→L in 5 f with its highlight (V1 D4) | |

Text never flies in, bounces or rotates in.

## 4. Layout system

**Canvas:** 1920×1080. For other aspect ratios, see §6.

| Zone | Rule | Source |
|---|---|---|
| Safe margin | 90–140 px from every edge; lower-third left edge x = 139 (7.2 %) | V3 [Measured] |
| Centre axis | titles, charts and title boxes centred on x = 960 | V1 f1260, V3 |
| Chart title band | top at y ≈ 92; subtitle about 70 px below | V3 [Measured] |
| Chart body | starts at y ≈ 300; bars left-anchored at x ≈ 520; labels right-aligned to x ≈ 480 | V3 D8 (x = 522) |
| Title card | ruled box (10 px ink stroke) about 1000×560, centred, one supporting cut-out to the right | V3 f92 |
| Card title | yellow box top at y = 181; object in the lower half (y 560–900) | V1 D1 |
| Footage caption | ▶ at x ≈ 160–215, italic text from x ≈ 230, baseline y ≈ 955 | V1 D18 |
| Lower third | plate top y ≈ 814, bottom ≈ 916 | V3 D12 |
| Quote | text block on one half (x ≈ 1220–1700), cut-out portrait with offset yellow outline on the other half | V1 f1140 |
| Collage | key object centred; header top-centre; tape labels overlapping the object's lower-left edge; props cropped at the frame edges | V6 |
| Grid paper | local patch with 48 px pitch, 1–2 corners, radial fade | V3 c_grid |

**Negative space.** Flat-family frames keep at least 40 % of the canvas as empty paper (V3 sheets [Observed]). Collage frames fill the edges with props but leave a calm centre.

**Layer hierarchy, back to front:**

1. Ground colour
2. Static paper texture
3. Grid patch
4. Ghost / background type at 20 % opacity (V3 DEM/REP, V5 "after this")
5. Cards and cut-outs with shadows
6. Ink type
7. Highlighter (multiply)
8. Hand annotations
9. Magnifier / lens
10. Vignette
11. Grain
12. Pillarbox or watermark (optional)

## 5. Positioning patterns worth reusing

- **Label leader:** a thin line from the object to a yellow-box label (V1 D8, V6 D8). The line draws first, then the label pops at its end.
- **Speech-bubble highlight:** a yellow box with a small pointer, used as a map label (V1 D4).
- **Pillarboxed 4:3 inside 16:9** with `#1F1F1F` bars (V6). Use it for archival or documentary chapters.

## 6. Responsive behaviour across aspect ratios

These are inferred; no 9:16 Vox master was analysed. V5 shows a 9:16 collage inside a 16:9 frame.

| Aspect | Rule |
|---|---|
| 16:9 | the reference layout |
| 9:16 | Stack title above object. Scale type by width (`width/1920` for 16:9 values ×1.6 in 1080×1920). Labels as white-on-black or yellow strips at the top-left of the card (V5) |
| 1:1 | Centre everything. Chart bars become vertical. Lower third moves to y ≈ 78 % |
| 4:3 inside 16:9 | 1440×1080 picture at x = 240, bars `#1F1F1F` |

Drive sizes from `useVideoConfig().width` rather than hard-coded px when you build multi-format components.
