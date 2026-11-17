# Style: Documentary Collage

`Style: documentary-collage` in `brief.md`. A tactile editorial collage:
physical paper, printed documents, clippings, maps and photo cut-outs on a
textured desk, with crisp journalistic annotation and a camera that walks
the viewer through the evidence. Best for investigations, history, and
"why did this happen" topics.

It comes from a documentary-collage explainer prompt the user supplied (its
visual, motion, storytelling and sound sections). That prompt's in-chat
Artifact, Canvas export, synthesized-music and voiceover sections are
replaced by `pipeline/8-animate.md` (HyperFrames render, ElevenLabs voice as
the clock). The quality standard and rendering principles shared by every
style are in `pipeline/directing.md`. Where this guide and `8-animate.md`
or `AGENTS.md` disagree, those files win. Describe and build the look
itself; do not name or imitate a specific publication's brand.

---

## 1. Explain like a journalist

Build each chapter as an investigation: a question, the evidence, the
mechanism, the answer. Every scene points at something specific (a number
on a document, a place on a map, a line in a chart, a detail in a photo) and
shows why it matters.

Direct attention with annotation: a highlighter sweep over the key words, a
circle around a detail, an arrow between two related items, a label naming
what we are looking at.

Story shape across the video: hook (a surprising fact, question or image),
context, evidence, mechanism, answer. The script already carries the order;
the visuals make each step visible.

## 2. Visual direction

### Brand mapping

Colours, fonts, light, shadow and grain come from `brand/STYLE.md`. The
source prompt's own palette (kraft, newsprint, yellow highlighter, red
marker, teal) is replaced by the brand tokens:

| Role in this style | Brand token |
|---|---|
| Desk surface under the paper | a darker shade of `paper` (paper depth, brand 2.1); never a new colour |
| Newsprint, documents, clippings | `paper` |
| Ink, text, outlines, document body lines | `ink` |
| Photo-print borders | `cardstock` |
| Highlighter sweep | the brief's topic accent, ink text on top (brand 2.2) |
| Marker circles, arrows, brackets, tape | `brand`, or `ink` where they touch the highlighter |
| Editorial accent, map routes | `brand` (shapes) and `brand-text` (words) |
| Muted map and chart details | `ink` at lower opacity |

Keep it restrained: paper and ink carry most of the frame; the topic accent
and dusty blue are for attention only, a few marks per scene. A dusty-blue
mark never touches a topic-accent highlight (brand 2.3, rule 6): circle a
highlighted word in `ink`, or leave a paper gap.

### Collage layers (back to front)

1. **Surface:** kraft paper, cardboard or a desk, with subtle stable grain.
2. **Paper:** torn and cut shapes with irregular edges and soft shadows.
3. **Documents and clippings:** printed sheets whose body text is
   decorative and unreadable, with one or two clear, legible key lines.
4. **Photo cut-outs:** the cleared photos from `assets/`, with a
   `cardstock` cut border and shadow. The subject's photo stays in full
   colour; supporting photos may be gently desaturated (brand, section 5).
   Grain and halftone go on the paper around a photo, never on the photo.
5. **Maps and charts** printed onto paper sheets.
6. **Accents, sparingly:** tape, staples, sticky notes, paper clips.
7. **Labels:** cut-out letters and bold sticker-style tags.
8. **Annotation:** highlighter, marker circles, underlines, brackets,
   arrows, clean callouts.

### Real photos and documents

- Real photos come first (`8-animate.md`). The collage treatment (border,
  grain, crop) must not change what the photo shows. ND-licensed files are
  shown whole, without crop or marks on top (`8-animate.md`).
- **Never fabricate a real document.** No made-up headline, quote,
  letterhead, newspaper name, signature or date. A generated document is
  generic and clearly illustrative: decorative body text, and only its key
  line is legible, and that line must be a fact from `facts.md` and the
  narration (`AGENTS.md`, rule 8).
- A drawn "photo-like" cut-out must not look like a real archival photo
  (`8-animate.md`); keep it visibly illustrated.

### Annotation

- Highlighter sweeps look hand-applied: slightly uneven edges, multiply
  blending, drawn left to right over the exact words.
- Circles, underlines, brackets and arrows in dusty-blue or ink marker,
  drawn stroke by stroke. No red circles (brand, section 6).
- Labels and callouts name places, people, numbers and documents. Their
  text is a fact claim like any on-screen text.

### Typography

Fonts and sizes come from `brand/STYLE.md`, section 3:

- Headlines, labels and tags: Archivo 900 / 800.
- A document's one legible key line: Archivo 800, or the composition's
  single Fraunces italic line. Its body text is ink line marks, not a font.
- Mixed cut-out letters (Archivo in paper and ink pieces) only for
  occasional emphasis: one word, not a sentence.
- Short and legible: one headline or question per section.

## 3. Motion direction

Motion feels like a journalist laying out evidence on a desk and guiding
the viewer through it.

### Signature moves

- Paper slides, drops and settles onto the desk with a slight rotation and
  a shadow that tightens as it lands.
- A document slides in, the camera pushes in to one line, and that line is
  highlighted.
- Photos parallax gently in layers: foreground cut-out, midground,
  background.
- Annotations draw on: circles, arrows and underlines appear stroke by
  stroke.
- Maps zoom from wide to a specific place; pins drop and routes draw on.
- Cut-out labels pop on with a quick scale and settle.

### Camera

Deliberate push-ins to the detail that matters, pans across the desk from
one piece of evidence to the next, and pull-backs that reveal how the pieces
connect. Every move is smooth and motivated (`directing.md`, section 5).
The desk is one continuous space: plan where each piece lies so the camera
can travel between them.

### Transitions

Paper-native, one consistent grammar: a sheet slides across the frame, a
page tears away to reveal the next scene, the camera pans to the next item
on the desk, or a photo zooms until it fills the frame. No default
crossfades.

### Pacing

A visual beat (new evidence, a mark, a zoom, a state change) roughly every
2-4 seconds in a Short and every 5-10 seconds in a long video. Hold a
highlighted line long enough to read it (`directing.md`, section 4).

## 4. Sound palette

Under the voice, following `directing.md` section 3:

- paper slides, drops and rustles;
- page tears on transitions;
- highlighter and marker squeaks on annotations;
- a camera-shutter or snap accent on photos, sparingly;
- soft thuds when evidence lands;
- low whooshes on push-ins;
- music (licensed or generated, `8-animate.md`): an inquisitive documentary
  bed of soft pulsing synths or muted piano, a light steady rhythm and warm
  low bass, with a little tension before key reveals, ducked under the
  voice.

## 5. Code-drawn objects

The element review (`8-animate.md`, Method 2) checks these. Paper pieces
have irregular torn or cleanly cut edges, not perfect rectangles; documents
have believable margins and line spacing; maps are traced from real outline
data with no borders unless the topic needs them; pins, tags and stickers
read at phone size. Natural objects are traced from a reference photo as
smooth curved shapes, never blocky.
