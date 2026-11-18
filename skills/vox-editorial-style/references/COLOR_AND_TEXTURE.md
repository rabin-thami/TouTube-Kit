# Color & Texture

**Primary source:** `evidence/COLOR_TEXTURE.md`, which has the full per-video k-means palettes, sample boxes and scripts, plus the swatches in `evidence/palette.png`.

**Additional samples:** `evidence/<KEY>_BREAKDOWN.md` §G.

**Tags:**
- **M** = measured median of masked pixels at the stated frame.
- **E** = estimate.

All measurements were taken on H.264 4:2:0 decodes, so saturated edges are slightly smeared.

## 1. Token table

| Token | HEX | Tag | Source frame / region |
|---|---|---|---|
| `paper` (flat) | `#F6F5EA` (alt `#F6F6EA`) | M | V3 f0, f150, f2877 |
| `paperWarm` | `#E5DDC6` / `#E6DEC7` | M | V2 f180, f270, f360 |
| collage paper | `#F2E8DF` top-centre → `#DED4CE` edge, corners `#CFC8C1`/`#C0B9B2` | M | V1 f1260 |
| aged paper | `#C4BDB2` centre, `#ACA496` corner | M | V4 f0 |
| kraft | `#AD987F` / `#B2987D` | M | V5 f0, f360 |
| desk grey | `#D8D6D8` lit / `#8D8A89` shadow | M | V6 f144, f791 |
| `dark` | `#12100D` (centre `#1A1411`) | M | V1 f960, f1080 |
| chalkboard | `#1E1C1F` / `#333233` | M | V6 f935 |
| pillarbox | `#1F1F1F` (std 0) | M | V6 |
| `ink` | `#201E18` (V1 `#312E24`, V2 `#0C0803`–`#161110`) | M | V3 f2877 |
| `inkSoft` | `#393733` / `#3F3D41` | M | V4 f105, V6 |
| `highlight` | `#F0E136` / `#EEDF2F` | M | V3 f3740 |
| `highlightPure` | `#F6EA00` / `#F4E800` / `#F4E900` | M | V1 f1260, f4320, f2160 |
| caption yellow (on footage) | `#E4E704` | M | V1 f1980 |
| map outline yellow | `#ECE048` | M | V1 f450 |
| tape / sticky yellow | `#E0D237` / `#DBD032` | M | V6 f144, f863 |
| `gold` | `#EAB718` | M | V2 f225 |
| ochre brush | `#BE933B` (≈ multiply of `#FBCC59`, E) | M | V4 |
| `red` | `#FC3828` / `#FA3727` | M | V3 f1870, f1942 |
| `redDeep` | `#8B1916`–`#8B1C1B` | M | V2 f360 |
| date-tag maroon | `#7D3130` | M | V4 |
| coral | `#E96450` (V3), `#CB5F4A` (V5 marker) | M | V3 f7860, V5 |
| `blue` | `#50B7FE` / `#51B7FD` | M | V3 |
| green | `#5DBC7E` / `#62C583`; methyl green `#2FA62A` | M | V3, V6 |
| pink | `#FB96C0` / `#FF85C1` | M | V3 |
| purple | `#BE71AD` / `#BA75BB` | M | V3 |
| slate blue | `#698ACD` | M | V3 f6545 |
| grid hairline | `#CDCCC2` | M | V3 f0 |
| map grey | `#99989B` | M | V3 f1726 |
| lower-third plate | `#EEE4D8` (may be semi-opaque) | M | V3 f2200 |
| map ocean / land | `#688EB7` / `#9C9C71`, zoomed land `#B9B389` | M | V1 f360, f450 |
| bar fill (dark) | `#333230` | M | V1 f3960 |
| photo keyline | `#BB9D24`, about 4–6 px | M colour / E width | V1 f4500 |

## 2. Contrast relationships

| Pair | Ratio | Use |
|---|---|---|
| ink on flat paper (`#201E18` / `#F6F5EA`) | 15.2 : 1 | all text |
| ink on highlighter (`#201E18` / `#F0E136`) | 12.3 : 1 | highlighted words |
| ink on title yellow (`#312E24` / `#F6EA00`) | 10.8 : 1 | card titles |
| caption yellow on dark (`#E5E605` / `#12100D`) | 14.2 : 1 | footage captions |
| ink on aged paper (`#393733` / `#BFB8AC`) | 6.0 : 1 | collage minimum |
| red on paper | 3.3 : 1 | fills, large numerals only |
| blue on paper | 2.0 : 1 | **fills only, never text** |

**Rule [Measured]:** text sits at 6–15 : 1. Saturated colours appear only as fills, bars and highlights.

## 3. Gradients and overlays

- **Paper vignette:** a radial gradient, not a linear one. V4 ring medians are 190, 189, 188, 186, 183, 179, 174, 172, 169, 166 from centre to corner, so falloff starts at about 40 % of the half-diagonal.
- **Highlighter:** `mix-blend-mode: multiply` lets paper grain and ink show through (V4, V3 scans).
- **Dimming:** non-focus data drops to 15–30 % opacity (V3). It is never blurred.
- **Ghost type:** huge serif or sans letters at about 20 % opacity behind collages (V3 DEM/REP, V5).
- **Stipple overlay on photos:** `#9BA5BD` dots about 5 px, about 11 px spacing, 7 % coverage (V3 photo cards). This is not a true halftone; no AM halftone screen was found in any video.

## 4. Texture parameters (code-ready)

| Parameter | Value | Tag | Code |
|---|---|---|---|
| Grain amplitude | 0 (flat) / 1.1–1.6 (subtle, V1) / 4–5 (strong, V6) std in 8-bit levels | M (lower bound, h264) | `<Grain amount>`: 0.2 ⇒ 1.06 levels measured in calibration |
| Grain size | 0.6–1.1 px @1080p, monochrome | M | `feTurbulence baseFrequency 0.85, numOctaves 1` |
| Grain refresh | 12 fps (on twos @24; 2:3 cadence @30) | M | seed = `stepped(frame)/2` |
| Paper texture | static; mid-frequency std 0.7–1.6 | M | `<PaperTexture amount={0.18}>` (multiply) |
| Vignette | 8–15 % (V1, V4), 5–8 % (V5), 0 (V2, V3) corner luma drop | M | `<Vignette strength>` |
| Directional light | 40 % drop right→left (V6 only) | M | `linear-gradient(90deg, rgba(0,0,0,.35), transparent 60%)` multiply, E |
| Chromatic aberration | 2–3 px on text (V1, V6); R−B 8 px on collage cards (V1 f5580) | M/O | `text-shadow: -2px 0 rgba(220,40,40,.35), 2px 0 rgba(40,160,220,.35)` |
| Texture boil (stop-motion) | A-A-B two-variant loop at 3.3 Hz (V4) | M | alternate two `PaperTexture` seeds by `Math.floor(frame/3)%3===2` |
| DOF on props | about 2–4 px Gaussian on edge props (V6) | E | `filter: blur(3px)` on prop layers |

## 5. Shadows

| Object | CSS | Tag |
|---|---|---|
| Large card / phone on paper | `box-shadow: 10px 12px 27px 2px rgba(0,0,0,.62)` | E (fit, V5 f0) |
| Small photo card | `box-shadow: 4px 5px 10px 2px rgba(0,0,0,.5)` | E (fit, V3 f12012) |
| Paper card with a torn edge | `filter: drop-shadow(3px 4px 8px rgba(0,0,0,.25))` + 2–4 px `#3A3A3A` rough edge | E (V6 f791) |
| Cut-out person (V1) | no shadow; a yellow offset outline of about 15–25 px instead | O |
| V1 framed photos | no measurable shadow; rounded yellow-green keyline (`#D4E024`, radius about 20 px) | E |

Shadow colour is neutral black (equal R, G and B ratios). Light comes from the top-left, so shadows fall down-right in every video.

## 6. Archival and photo treatment

| Source | Measured grade |
|---|---|
| V1 archival | a* 0–2.6, b* 0.9–6.3 → near-neutral B&W with a faint warm lift (not sepia) |
| V1 1960s footage | green-cyan duotone (hue 143°, C* 11) as a period cue |
| V3 archival film | pure neutral (C* 0.1) |

**Code:** `filter: grayscale(1) sepia(0.08)`, or `@remotion/effects` `duotone()` for period tints.

## 7. Colour across scenes

| Video | Light / mid / dark split | Pattern |
|---|---|---|
| V1 | 28 / 47 / 26 % | 47 light↔dark class switches in 197 s (median run 2.8 s): paper graphic ↔ footage ↔ dark cards |
| V3 | 79 % light | dark only for archival film, credits and one recap beat |
| V2, V4, V5, V6 | — | one dominant ground per piece |

**Rule:** choose the ground per chapter. Use dark grounds as punctuation (title interstitials, timelines, chalkboard close-ups) and cut back to paper.
