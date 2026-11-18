# Analysis Limitations

## 1. Inspection coverage

| Video | Total frames | Measured numerically | Visually inspected (frames opened) | Dense (every-frame) ranges |
|---|---|---|---|---|
| V1_porsche | 5,899 | all 5,899 | ≈ 2,400 tile views (overlaps included): every 10th frame across the whole video, ±4 frames around all 102 cut candidates, 17 dense ranges | 1216–1271, 729–780, 2398–2440, 124–172, 1925–1960 (step 1); others at step 2–5 |
| V2_camera | 419 | all 419 | ≈ 190 unique | 0–22, 129–200 |
| V3_elections | 14,061 | all 14,061 (+ ≈ 4,250 decoded densely for tracking) | ≈ 750 views | 18 ranges at step 3–12 (see the V3 BREAKDOWN §B) |
| V4_highlight | 162 | all 162 | **all 162** | whole video |
| V5_rabbit | 1,127 | all 1,127 | ≈ 330 unique | 7 ranges, every frame |
| V6_epigenetics | 1,225 | all 1,225 | ≈ 560 unique | 11 ranges, every frame |
| **Total** | **22,893** | **22,893 (100 %)** | **≈ 4,400 views, not unique frames** | |

The orchestrator also viewed contact sheets for V1, V3 and V6 (about 60 frames) and the calibration renders.

**Not every frame was visually inspected.** Every frame was measured by frame difference, histogram distance and luma. Frames inside static holds (frame difference below 0.5, 44–80 % of graphic footage) were mostly seen only through representative samples, and so were the interview takes. Each BREAKDOWN §B lists the ranges that were not opened. On-twos and on-threes animation means many unopened frames are exact duplicates of opened neighbours.

**Sampling:**
- Uniform samples every 0.25 s (V2), 0.5 s (V4), 1 s (V5, V6), 2 s (V1) and 3 s (V3).
- Every automatic cut candidate and the frame before it.

## 2. Scenes identified

Total: 199 scene or shot entries.

| Video | Entries |
|---|---|
| V1 | 108 shots (shown as 107 table rows, some grouped) |
| V2 | 10 |
| V3 | 46 scenes (81 shots) |
| V4 | 6 |
| V5 | 15 inner shots + static outer frame |
| V6 | 15 |

Cut detection is automatic and was verified visually:
- V1: 6 false positives removed and 8 soft boundaries added.
- V3: 13 false positives removed.

V3 transitions without a cut may still be under-counted, because soft transitions only show up in sustained frame-difference runs.

## 3. Uncertain measurements

- **Easing curves.** All bezier values are ESTIMATE fits. They are sampled every 2 frames (on twos), or only 2–4 points per move at V4's 10 fps, with ±1 frame of quantisation. Shape labels (ease-out vs in-out) are reliable; exact control points are not.
- **Tracking precision.**
  - Bounding boxes measured on 640×360 frames are ±3 px at 1080p.
  - ORB similarity transforms track the dominant layer only, so they are noisy on V1's desk collage (f5546–5720) and inside dissolves.
  - Phase correlation confidence at peak pan speed was 0.67–0.72 (V3 f4687).
  - V5 inner-card moves under about 5 px were not detectable.
- **Not tracked numerically:**
  - V3 loupe-wipe scale (f1389–1423)
  - V3 lower-third dot paths
  - V1 footage-card shrink (D17)
  - V5 tape motion f122–142 (motion blur)
- **Colours.** H.264 4:2:0 smears saturated edges, and k-means centres blend anti-aliased pixels. The text HEX values are less reliable than fills.
  - V3 lower-third plate colour may include footage showing through.
  - V6 red methyl HEX is darkened by texture.
- **Grain.** Values are lower bounds, because compression removes fine grain and grain size is near the codec limit. V1's 12 fps cadence may come from a 12/24 fps comp rather than deliberate on-twos.
- **Shadows.** CSS values come from fits to single luma profiles, ±30 %.
- **Font sizes.** Measured as cap height at 1080p from full-res crops (V1, V2, V3, V6). Others were estimated from 640 px thumbnails.

## 4. Font identification limits

No font was positively identified. The references use proprietary or unknown faces, and frames carry no metadata. All font names in [TYPOGRAPHY_AND_LAYOUT](TYPOGRAPHY_AND_LAYOUT.md) are visual category matches with free stand-ins. Hand lettering may be drawn assets rather than a font.

## 5. Audio limits

- No transcription was done: no narration content was verified or reproduced.
- Music and SFX were separated with a mid/side heuristic, since the VO is centred. This hides mono music and catches VO reverb.
- SFX classification is heuristic (attack, length, tilt), not listened to. The SFX counts are an upper bound.
- Tempo values are autocorrelation estimates with possible half- or double-time ambiguity (V1 72 vs 142 BPM).
- V4 is probably not loudness-normalised (-31 LUFS) and has one cut, so its sync statistics are meaningless.

## 6. Effects that can't be reliably rebuilt in code

These need supplied or licensed media:

- photographs
- archival film
- interviews
- halftone or engraving illustrations
- desk props
- textures for the page curl and crumpled paper
- music, SFX and VO

The page curl needs WebGL or a pre-rendered asset. V2's and V4's specific display typefaces have no exact free equivalent.

## 7. Assumptions

- **Reference type.** Some references are fan-made "Vox-style" pieces (V1, V2, V4, V5) and two are Vox originals (V3, V6). They were weighted equally where they agree. Family A follows V3; family B follows V1/V6.
- **Delivery fps.** 24 fps is assumed for new work: it matches V3/V6 and gives clean on-twos at 12 fps. At 30 fps, use a 2:3 cadence or `STEP = 2` (15 fps).
- **Frame counts.** Recipe frame counts were converted to 24 fps by duration (seconds × 24) and rounded.
- **Calibration content.** Placeholder text, data and a gradient "photo". It validates technique, not storytelling.

## 8. Housekeeping

- `reference-analysis/` is about 0.4 GB, mostly PNGs. Add `reference-analysis/**/full/`, `**/frames/`, `**/work/` and `color/extra/` to `.gitignore` before committing. This is not done yet; it is the user's call.
- `reference-analysis/color/extra/` holds 16 mislabelled V6 PNGs from a failed agent extraction run. They are safe to delete; `color/consec/` is the correct set.
- `@remotion/google-fonts` and `@remotion/transitions` 4.0.544 were added to `package.json` and `bun.lock`, with the user's approval.
