# Reference Sources

The six videos were analysed to build this style. **They are not bundled with the skill:** they are third-party works and together about 250 MB. The analysis evidence is in `evidence/`.

The original local copies were at `C:\Users\rabin\Downloads\Refernace\` (WSL: `/mnt/c/Users/rabin/Downloads/Refernace/`). The YouTube IDs come from the downloaded filenames.

| Key | Title (as downloaded) | YouTube ID | Res / fps | Frames | Duration | Origin |
|---|---|---|---|---|---|---|
| V1_porsche | VOX-Style Animated Documentary: The History of Porsche | FwRtt4nhCDE | 1920×1080 / 30 | 5,899 | 196.70 s | fan-made Vox-style |
| V2_camera | The First Camera Ever Made (Vox-style intro) | ObxBMSZFakc | 1920×1080 / 60 | 419 | 7.04 s | fan-made Vox-style |
| V3_elections | Why US elections only give you two choices | bqWwV3xk9Qk | 1920×1080 / 23.976 | 14,061 | 586.51 s | Vox |
| V4_highlight | The Highlight by Vox (animation-like Vox) | mGBejyklJHg | 3840×2160 / 10 | 162 | 16.25 s | fan-made Vox-style |
| V5_rabbit | Spain, the Rabbit Island | w_mB6rze3Zg | 1920×1080 / 30 | 1,127 | 37.62 s | collage short in a portfolio frame |
| V6_epigenetics | vox – epigenetics | — | 1920×1080 / 23.976 | 1,225 | 51.14 s | Vox (excerpt, 4:3 pillarboxed) |

**Weighting:**
- Family A (flat editorial) follows V3 and V2.
- Family B (analog collage) follows V1, V4, V5 and V6.
- Where fan-made and original pieces agree, both count equally.

**Re-analysing or adding references:** use the `reference-style-director` skill, or the pipeline in `ANALYSIS_LIMITATIONS.md`. That pipeline is ffprobe → per-frame frame-difference/histogram/luma table → cut candidates → uniform and cut-frame extraction → contact sheets → dense strips around moves → tracking.
