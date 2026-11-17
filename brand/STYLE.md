# STYLE.md — Everyday Origins Brand System

This file is the single source of truth for how Everyday Origins looks.
Every agent and every person making anything for the channel (thumbnails,
videos, animation, banners, social posts, community posts) follows it.

**How it fits the kit.** This file sets the **theme**: colours, fonts, logo,
materials, light and layout. A video style in `pipeline/styles/` (picked by
the `Style:` line in `brief.md`) sets the **look and motion** of that video:
its composition, layers, camera and transitions. Every style draws in this
file's colours and fonts; each style file has a "Brand mapping" section
that says which token plays which role.

**Precedence.**
- On colour, fonts, logo and layout, this file wins over every other file,
  including the style files.
- On motion, composition and camera, the style file wins.
- On facts, scripts and the render pipeline, `facts.md`, `AGENTS.md` and
  `pipeline/*.md` win.

**Do not improvise the brand.** Do not add colours, fonts, logo versions or
effects that are not in this file. If something is not covered here, use the
closest rule that is, and flag the gap so this file can be updated.

---

## 1. Brand in one paragraph

Everyday Origins is a faceless YouTube channel of 8–15 minute micro-
documentaries about the hidden history of everyday things, for a global,
English-speaking, curious audience. The house look is **editorial paper
cut-out**: warm cream paper, charcoal ink, one calm brand blue, and one
topic colour per video. The feel is curious, trustworthy, warm and slightly
playful (from the smiling logo), never loud, never clickbait.

**Tagline (placeholder until confirmed):** The hidden history of ordinary things.

---

## 2. Colour

### 2.1 Palette and roles

Each colour has one job. Use colours only in their role.

| Token | Name | HEX | RGB | Role |
|---|---|---|---|---|
| `paper` | Warm cream | `#F3EBDD` | 243, 235, 221 | Default background for content, thumbnails and paper sheets; text on charcoal |
| `ink` | Charcoal | `#243139` | 36, 49, 57 | All text on paper, outlines, halftone, shadows; background for brand moments |
| `brand` | Dusty blue | `#7C9DA5` | 124, 157, 165 | Logo "o", marker circles, arrows, tape, route dots, progress bars. Shapes only on paper |
| `brand-text` | Deep dusty blue | `#566D73` | 86, 109, 115 | Blue text on paper |
| `cardstock` | Pale cardstock | `#FFF8EB` | 255, 248, 235 | Photo-print borders only, always with a shadow |
| `topic-mustard` | Mustard | `#E8B65C` | 232, 182, 92 | Topic accent: yellow or golden subjects |
| `topic-terracotta` | Terracotta | `#C56B50` | 197, 107, 80 | Topic accent: red, brown, earthy subjects |
| `topic-terracotta-text` | Deep terracotta | `#9D5540` | 157, 85, 64 | Terracotta text on paper |
| `topic-sage` | Sage green | `#8A9B7C` | 138, 155, 124 | Topic accent: green, plant and blue subjects |

Darker or lighter shades are allowed only for paper depth (shading, edges,
layer separation, a desk surface under the paper), never as a new signal
colour.

### 2.2 Allowed text pairs

Ratios are WCAG contrast ratios calculated on flat colour (checked
2026-11-17). On texture or photos the real contrast is lower, so put text on
a solid card or label, never straight on a photo. "Large" means at least
24px bold, which every Archivo size in section 3 already is.

| Text on background | Ratio | Use |
|---|---|---|
| `ink` on `paper` | 11.27:1 | Any text |
| `paper` on `ink` | 11.27:1 | Any text |
| `ink` on `cardstock` | 12.63:1 | Any text |
| `ink` on `topic-mustard` | 7.17:1 | Highlighted words |
| `ink` on `topic-sage` | 4.49:1 | Highlighted words (large sizes only) |
| `ink` on `topic-terracotta` | 3.55:1 | Highlighted words (large sizes only) |
| `brand-text` on `paper` | 4.63:1 | Labels, dates (large sizes only) |
| `topic-terracotta-text` on `paper` | 4.66:1 | Labels (large sizes only) |
| `brand` on `ink` | 4.59:1 | Taglines, labels (large sizes only) |

**Never use as text:** mustard on cream (1.57:1), sage on cream (2.51:1),
dusty blue on cream (2.46:1), terracotta on cream (3.17:1).

### 2.3 Topic accent (the only colour that changes per video)

1. Exactly **one** topic accent per video. The same one is used in that
   video's thumbnail, animation, title cards and community posts.
2. Choose it before production starts and record it in the video's
   `brief.md` as `Topic accent: mustard | terracotta | sage`.
3. Choose from the subject's natural colour:
   yellow or golden → mustard · red, brown or earthy → terracotta ·
   green or plant → sage.
4. White, grey or black subjects (e.g. salt) take the colour of their story
   (rock salt, earth, salt roads → terracotta). Never use white as an accent.
5. Blue or teal subjects never use dusty blue (reserved for the brand). Use sage.
6. Never place the topic accent directly next to dusty blue. Separate them
   with ink or paper. Their lightness is almost the same (1.02–1.56:1), so
   colour-blind viewers may not tell them apart.
7. Never use terracotta and sage together as two signals (1.26:1, a red/green
   pair).

| Subject | `Topic accent` |
|---|---|
| Banana | mustard |
| Salt | terracotta |
| Coffee | terracotta (text in deep terracotta) |
| Tomato | terracotta |
| Mint, tea leaf, blueberry | sage |

---

## 3. Typography

Only two font families, both free on Google Fonts.

| Use | Font | Weight / style | Case | Size at 1920×1080 |
|---|---|---|---|---|
| Headlines, thumbnail text, channel name | Archivo | 900 | UPPERCASE, letter-spacing −0.02em | 72–110px (video), as large as fits (thumbnail) |
| Labels, callouts, data, lower-thirds | Archivo | 800 | Sentence case | 28–40px, never below 24px |
| Numbers and dates in charts | Archivo | 800 | — | 32–64px |
| Taglines, quotes, the "story" voice | Fraunces | Italic 500 | Sentence case | 36–56px |

Rules:
- At most one Fraunces line per composition.
- No outlines or strokes on text. If text needs help, put it on a paper card,
  or use a soft ink shadow on thumbnails.
- No other fonts, including for "special" videos or styles that ask for a
  typewriter or serif face. Decorative, unreadable text (document body
  lines) is drawn as ink line marks, not set in a font.
- For vertical Shorts (1080×1920), use the same sizes; they are measured on
  the 1080px side.

---

## 4. Logo

- **Primary logo (logo 11):** a lowercase cream "e" and a dusty-blue ring "o"
  as two eyes, with a solid cream smile underneath, on a charcoal square.
  YouTube crops it to a circle.
- Use the exported file only: `brand/logo-11.svg` (and
  `brand/logo-11-800.png`). *These files do not exist yet; add them to
  `brand/` and keep these paths.* Until they exist, leave the logo out
  rather than drawing one.
- Never redraw, recolour, stretch, rotate, add effects to or rearrange the logo.
- Minimum size: 24px. Below that, use nothing.
- **Brand motifs** taken from the logo:
  - **Smile curve:** a shallow solid curve, cream on ink or charcoal on paper,
    used as an underline for the channel name or a chapter title. At most
    once per chapter.
  - **Route dots:** round dots, about 4px dots with 16px gaps at 1080p, ink
    on paper or paper on ink. The standard connector for journeys, timelines
    and "from here to there".

---

## 5. Materials and texture (applies to every style)

- **Look:** matte paper with slightly imperfect torn or cut edges. No gloss,
  no gradients, no glow, no 3D.
- **Light:** from the top-left. Every shadow falls down-right.
- **Shadows:** ink `#243139` at 20–30% opacity, soft blur, offset larger for
  higher layers.
- **Paper grain:** one fixed-seed texture, about 10–12% opacity, multiply.
  Same in every video and thumbnail. Never on photos.
- **Halftone dots:** ink on paper or paper on ink, 10–25% opacity, for
  backgrounds and emphasis only.
- **Photos:** printed photos with a cardstock border, a shadow and sometimes
  tape or a slight tilt. The subject's photo stays in full colour. Supporting
  photos may be gently desaturated but must still look real.

---

## 6. Thumbnails (1280×720)

1. **Background:** cream paper with grain, plus an ink frame or a torn ink
   strip along at least one edge, so the thumbnail does not melt into
   YouTube's white light mode (cream vs white is only 1.18:1).
2. **Subject:** one large paper cut-out or photo of the subject in full
   colour. It is the brightest, biggest thing in the frame.
3. **Text:** 2–4 words, Archivo 900 uppercase in ink. One word sits on a
   topic-accent highlighter stroke.
4. **Brand mark:** one dusty-blue shape (tape strip or marker circle) in the
   same corner on every thumbnail (bottom-left).
5. **Colours:** maximum four brand colours (paper, ink, brand, topic accent)
   plus the subject's own colours.
6. Never: arrows pointing at nothing, red circles, shocked faces, emoji,
   outlined text, more than four words.

---

## 7. Video

**Scene backgrounds**
- Content scenes: cream paper (a style may put it on a darker paper-shade
  desk, section 2.1).
- Brand moments: ink (charcoal) background. These are the intro sting,
  chapter title cards and the end screen.

**Title cards:** ink background, chapter title in paper Archivo 900, smile
curve underneath, chapter number in the topic accent.

**Lower-thirds / labels:** a paper card with an ink label (Archivo 800) and
a 4px dusty-blue edge on the left. Source or date in brand-text.

**Maps and timelines:** paper land, ink coastlines, route dots in dusty blue
or ink, the one place or era the story is about in the topic accent. Oceans
are a slightly darker cream, not blue (blue is the brand colour). Draw
national borders only when the story is about them.

**Charts:** ink axes and labels, bars and lines in ink by default, the one
value that matters in the topic accent. No more than one accent per chart.

**Transitions:** paper slides, folds and reveals, as the style file sets
them. Dip to ink only between chapters.

**Animation detail:** follow the style file the brief names
(`pipeline/styles/<style>.md`) for motion, construction and pacing, and
`pipeline/directing.md` for directing. Their colours and fonts must match
this file through the style's "Brand mapping".

---

## 8. Channel art

- **Profile picture:** logo 11 at 800×800.
- **Banner (2560×1440):** ink background, logo 11 plus "EVERYDAY ORIGINS"
  (Archivo 900, paper) plus the smile curve plus the tagline (Fraunces italic,
  dusty blue) inside the centre safe area of 1546×423. Paper-strip collage in
  the topic colours only at the far left and right.
- *Verify YouTube's current banner and profile picture specs before export.*

---

## 9. Tokens

Copy these into each HyperFrames project (`video/`) instead of retyping
colours. Set `--eo-topic` from the brief's `Topic accent`.

### CSS

```css
:root {
  --eo-paper: #F3EBDD;
  --eo-ink: #243139;
  --eo-brand: #7C9DA5;
  --eo-brand-text: #566D73;
  --eo-cardstock: #FFF8EB;
  --eo-topic-mustard: #E8B65C;
  --eo-topic-terracotta: #C56B50;
  --eo-topic-terracotta-text: #9D5540;
  --eo-topic-sage: #8A9B7C;
  --eo-topic: var(--eo-topic-mustard); /* set per video */

  --eo-font-display: "Archivo", sans-serif;   /* 900 headlines, 800 labels */
  --eo-font-story: "Fraunces", serif;         /* italic 500 */

  --eo-shadow: rgba(36, 49, 57, 0.25);
  --eo-grain-opacity: 0.11;
}
```

### JSON

```json
{
  "colors": {
    "paper": "#F3EBDD",
    "ink": "#243139",
    "brand": "#7C9DA5",
    "brandText": "#566D73",
    "cardstock": "#FFF8EB",
    "topic": {
      "mustard": "#E8B65C",
      "terracotta": "#C56B50",
      "terracottaText": "#9D5540",
      "sage": "#8A9B7C"
    }
  },
  "fonts": {
    "display": { "family": "Archivo", "headline": 900, "label": 800 },
    "story": { "family": "Fraunces", "style": "italic", "weight": 500 }
  },
  "light": "top-left",
  "shadow": { "color": "#243139", "opacity": [0.2, 0.3] },
  "grainOpacity": [0.10, 0.12]
}
```

---

## 10. Checklist (run before anything is published)

- [ ] Only colours from section 2.1, each in its role
- [ ] One topic accent, recorded in the brief, same everywhere in this video
- [ ] Topic accent never touches dusty blue; no terracotta + sage pair
- [ ] Every text pair is from section 2.2
- [ ] Only Archivo and Fraunces, at the sizes in section 3
- [ ] Logo used from the file, unchanged (or left out until the file exists)
- [ ] Light from top-left, shadows down-right, the same grain
- [ ] Thumbnail: ink edge, subject biggest, 2–4 words, blue mark bottom-left
- [ ] Video: content on cream, brand moments on ink
- [ ] The style's "Brand mapping" was followed
