# STYLE BIBLE — Editorial Paper Explainer

This is the primary, reusable identity document. Values come from the six references (see [SKILL.md](../SKILL.md)). Every number here is tagged and has its evidence in [COLOR_AND_TEXTURE](COLOR_AND_TEXTURE.md), [MOTION_RECIPES](MOTION_RECIPES.md) and `evidence/<KEY>_BREAKDOWN.md`.

---

## 1. Visual philosophy

The viewer should feel they are looking at a **researcher's desk explained by an editor**:

- printed paper, cut-out photographs, a highlighter, a marker;
- each element arranged so exactly one idea is readable at a time;
- motion that is **stepped and deliberate**, not fluid: graphics animate at 10–12 drawings per second;
- an editor who **holds still** while the narrator talks, then makes one decisive move per idea.

The system has three core ideas:

1. **Paper is the stage.** Every graphic sits on a paper ground: flat digital cream or a textured, vignetted sheet. Dark grounds are punctuation, not the default.
2. **Yellow means "read this".** A single highlighter yellow marks the current word, number or object. Saturated red and blue carry data. Text is always near-black warm ink.
3. **One beat, then rest.** Animation happens in short bursts of 4–30 frames, separated by static holds. 44–80 % of frames in the graphic references do not change at all [Measured].

## 2. Two style families

Pick one per project or per chapter. Do not blend them inside one shot.

| | **A. Flat editorial** (V3, V2) | **B. Analog collage** (V1, V4, V5, V6) |
|---|---|---|
| Ground | flat cream `#F6F5EA` / `#E5DDC6`, no grain, no vignette [Measured] | textured paper `#F2E8DF`→`#DED4CE`, kraft `#AD987F`, desk `#D8D6D8`; 8–15 % radial vignette [Measured] |
| Grain | none (std 0.0) | mono, ~1 px, 1.1–1.6 levels (subtle) to 4–5 levels (strong), refreshed at 12 fps [Measured] |
| Objects | vector maps, bars, donuts, icons; B/W halftone cut-outs | photos with white borders, tape, sticky notes, magnifier, pens; drop shadows |
| Camera | holds static; pushes and pans only to move between ideas | almost never static; slow linear push or pull of 0.3–0.4 %/2 f during holds [Measured V6] |
| Annotation | flat yellow highlighter blocks, pink hand lettering | yellow tape / sticky notes, marker circles, brush strokes |
| Edge effects | none | 2–3 px chromatic fringe, defocused props, radial zoom-blur transitions [Observed V1, V6] |

## 3. Colour system

Full tables are in [COLOR_AND_TEXTURE.md](COLOR_AND_TEXTURE.md). M = measured, E = estimate.

| Role | Token | HEX | Tag |
|---|---|---|---|
| Ground, flat | `paper` | `#F6F5EA` | M V3 |
| Ground, warm | `paperWarm` | `#E5DDC6` | M V2 |
| Ground, collage | `paperCollage` | `#F2E8DF` centre → `#DED4CE` edge | M V1 |
| Ground, dark punctuation | `dark` | `#12100D` | M V1 |
| Ink (all text) | `ink` | `#201E18` | M V3 |
| Soft ink | `inkSoft` | `#393733` | M V4 |
| Highlighter (multiply) | `highlight` | `#F0E136` | M V3 |
| Title box / tape (opaque) | `highlightPure` | `#F6EA00` | M V1 |
| Warm accent disc | `gold` | `#EAB718` | M V2 |
| Data red | `red` | `#FC3828` | M V3 |
| Data blue (fills only) | `blue` | `#50B7FE` | M V3 |
| Bullet / marker red | `redDeep` | `#8B1C1B` | M V2 |
| Extra data | green `#62C583`, purple `#BA75BB`, pink `#FF85C1` | | M V3 |
| Grid hairline | `grid` | `#CDCCC2` | M V3 |

**Rules**

- Text is ink on paper or ink on yellow, at 6–15:1 contrast [Measured, all videos]. Never set text in data red or blue: blue on cream is 2.0:1.
- Only one yellow element is active per beat. Older highlights stay, but they are never added two at a time.
- Dark grounds are for footage interstitials, chalkboard close-ups and credits. V1 alternates light and dark about every 3 s for documentary rhythm. Flat-editorial pieces stay light for 79–86 % of runtime [Measured].

## 4. Typography

Details are in [TYPOGRAPHY_AND_LAYOUT.md](TYPOGRAPHY_AND_LAYOUT.md). The references use proprietary faces; the stand-ins below are free Google fonts.

| Role | Look | Stand-in | Size @1080p |
|---|---|---|---|
| Title card | heavy news serif, caps | Source Serif 4, 900 | cap ≈ 90–93 px [Measured V3] |
| Chart / section title | same serif, semibold, sentence case | Source Serif 4, 600 | cap ≈ 34–36 px (font ≈ 52 px) |
| Emphasis word / quote / caption | old-style serif italic | Source Serif 4 Italic | cap 30–35 px |
| Data label / number | neo-grotesk sans | Inter 400–700 | 30–36 px |
| Annotation | marker caps, slight slant | Permanent Marker | cap ≈ 20–34 px |
| Lower third | bold serif caps name, bold italic role, on a `#EEE4D8` plate | Source Serif 4 700 / 700i | cap 36 / 28 px; left edge x = 139 |

**Rules.** The serif is the voice and the sans is the data. Italic marks one emphasised word. Hand lettering is only ever annotation.

## 5. Composition and layout

- **Canvas:** 1920×1080, 16:9. Safe margins are about 90–140 px (lower-third left edge 139 px, V3) [Measured].
- **Centre axis:** titles and charts are centred on x = 960; chart titles sit at y ≈ 92–145 [Measured V3].
- **One focal object.** It sits centre or centre-low (car cut-outs lower half, V1). Labels are attached to it, never floating free.
- **Graph paper is a local patch** (48 px pitch) fading from one corner, not a full-frame grid [Measured V3].
- **Layer order, back to front:** ground → paper texture → grid patch → shadowed cards and cut-outs → ink and labels → highlighter (multiply) → marker annotations → vignette → grain.

## 6. Texture and lighting

- **Grain:** monochrome, about 1 px, refreshed every 2 frames at 24 fps (12 fps). Never refresh it every frame.
- **Paper texture:** static. It never boils on its own (temporal correlation ≥ 0.92 in V4 and V5).
- **Vignette:** radial, falloff starting at about 40 % of the half-diagonal, 8–15 % corner drop. V6 uses a directional key from the top right (40 % drop to the left) instead.
- **Shadows:** neutral black multiply. Large cards `10px 12px 27px 2px rgba(0,0,0,.62)`, small cards `4px 5px 10px 2px rgba(0,0,0,.5)` [ESTIMATE fits].
- **Archival photos:** fully desaturated with a faint warm lift (b* +2…+6), not sepia [Measured].

## 7. Motion identity

Recipes and code are in [MOTION_RECIPES.md](MOTION_RECIPES.md).

1. **On twos.** Graphics and graphic camera moves step at 12 fps on a 24 fps timeline (34 of 41 V3 graphic shots are 100 % single-parity; V6 is on 2s; V1 runs about 12 fps on 30). Live footage runs on ones.
2. **Ease-out for arrivals, ease-in-out for camera, ease-in only into a cut.** No reference move showed spring overshoot. Do not use bouncy springs.
3. **Typical durations @24 fps:**

| Move | Frames |
|---|---|
| pop / sticker / bullet | 8–18 |
| highlighter per line | 11–36 |
| bar grow | 30, staggered 5–8 |
| camera push | 22–76 |
| punch-in | 16 |
| whip | 14 |
| zoom-through | 24 + 28 |

4. **Holds are earned.** After a beat, either hold completely still (flat family) or creep linearly at 0.1–0.4 % scale per 2 frames (collage family).
5. **Text arrives as typing**, at 1 char/frame (labels) or about 2 frames/char (titles), or word by word synced to narration. It does not fly in.

## 8. Transition philosophy

- **Default is the hard cut:** about 82 % of V1 boundaries and nearly all of V3. Cut 2 frames before the narrator's next phrase starts [Measured V1: median 57 ms].
- **Move the camera instead of transitioning** when the next idea lives on the same paper: push to a node, pan to the next chart, zoom into a region.
- **Signature transitions**, used sparingly:
  - zoom-through (ease-in push → cut → ease-out settle);
  - whip pan;
  - magnifier/loupe reveal;
  - radial zoom-blur;
  - short 3–6 f dissolves between archival stills.
  - The page curl and crumpled-paper wipe appear once each and are novelty only.
- **End:** a linear fade to black over 29–58 f.

## 9. Pacing

| Format | Median shot | Beat cadence |
|---|---|---|
| Documentary montage (V1) | 1.45 s; mean 1.82 s | bursts of 5–15 f cuts for montage emphasis |
| Long-form explainer (V3) | 3.3 s overall; graphic shots median 13 s | internal beats every 4.7 s (IQR 2.5–7.5 s); cold open cuts every 1.04 s |
| Collage short (V5, V6) | 2.5–2.7 s | a new visual event every 1–2 s |

Interviews or footage work as about 8 s breathers every 60–120 s (V3).

## 10. Sound (relationship rules)

- Master at -18 to -19 LUFS integrated, true peak about -1.5 to -2.5 dBTP, LRA 2.5–5 LU.
- Narration is centred mono. The music bed sits 15–23 dB under the voice in narrated explainers, with no ducking.
- Leave a 0.3–1.3 s near-silent gap at chapter breaks, then cut, then a sting, then a new cue at a new tempo.
- Use 1–6 designed SFX per minute, concentrated at the intro, chapter turns and the outro.

Source: `evidence/AUDIO_SYNC.md`.

## 11. Repeatable rules

| # | Do | When | Viewer function | Evidence | Conf. |
|---|---|---|---|---|---|
| R1 | Step all graphic animation to 12 fps (`stepped()`) | every graphic layer | hand-made, printed feel; reads as editorial, not UI | V3 D0, V6 D1, V1 cadence, V2 on 6s | High |
| R2 | Hold the frame static between beats | after each move in flat-family scenes | lets narration land; the eye settles | V3 66 % static frames, V1 44 % | High |
| R3 | Mark the one key word or number with a yellow block that wipes L→R in 11–24 f, ease-out | when the narrator says it | directs reading order | V1 D4/D7, V3 D7, V4 #3 | High |
| R4 | Grow bars with quart-out over 30 f, staggered 5–8 f | data reveal | comparison reads in order | V3 D8, V1 D15 | High |
| R5 | Push the camera to the detail (×1.2–1.8, ease-in-out cubic, 22–76 f) instead of cutting, when it is on the same sheet | moving from overview to detail | keeps spatial continuity | V3 D3/D11, V6 D3/D13, V1 D20 | High |
| R6 | Punch in ×1.3 over 16 f with strong ease-out on the title's key word | title cards | emphasis on the thesis | V3 D2 | Medium |
| R7 | Pop elements with expo-out, no overshoot, 8–24 f | stickers, circles, bullets, icons | arrival without cartoon bounce | V2 #4/#7, V6 D4, V1 D16 | High |
| R8 | Type text: labels 1 char/frame; titles word by word on VO | any new text | text paced to speech | V3 D12, V1 D1, V3 D2 | High |
| R9 | Draw hand annotations (ellipse, underline, arrow) in 6–12 f | the second emphasis after a highlight | "the narrator is pointing" | V6 D5/D8, V1 D9, V3 D14 | High |
| R10 | Accelerate (ease-in) into a hard cut; land the next shot with ease-out | energetic scene changes | momentum across the cut | V6 D10, V1 D22 | Medium |
| R11 | In collage scenes, never fully stop: linear creep 0.3–0.4 %/2 f | holds in the analog family | keeps the desk alive | V6 D6/D17 | Medium |
| R12 | Stagger lists and icons in reading order, 2–8 f apart | groups of similar items | counts the items for the viewer | V3 D4, V1 D15, V6 D15 | High |
| R13 | Cut at the end of a VO pause, about 2 frames before the next phrase | every edit in a narrated piece | the picture "answers" the sentence | AUDIO_SYNC rule 16 (V1 3.3× chance) | Medium–High |
| R14 | Give archival imagery a neutral B&W grade and a white border or keyline, and hold it 0.7–2 s | history beats | readable "evidence" register | V1 shots 8–30, colour §4 | Medium |

## 12. Do not transfer

Keep these original in every new video:

- Vox logos and wordmarks, the "America, explained" sting and any series branding.
- Scripts, wording, narration, interviewees and on-screen quotes.
- Specific artwork: the statue on a podium, the car cut-outs, the Porsche crest, the hemicycle designs as drawn, the rabbit-head collage, the methylated-DNA chalk cards.
- Exact shot sequences, such as V1's car-card → footage pattern or V3's New England district explode → donut → people sequence, with the same compositions.
- Footage, music, sound effects and photographs from the references.

Reuse only the abstract rules above, applied to your own story and assets.
