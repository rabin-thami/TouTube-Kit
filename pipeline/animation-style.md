# Animation Style Guide: Editorial Paper Cut-Out

The visual and motion guide for Step 8. It comes from the user's paper
cut-out explainer prompt (its creative-quality, visual, and motion sections).
That prompt's technical, export, and "no Remotion/HyperFrames" sections are
replaced by `pipeline/8-animate.md`, because this pipeline renders with
HyperFrames in Claude Code. Where this guide and `8-animate.md` or
`AGENTS.md` disagree, those files win. In particular: real cleared photos
from `assets/` are allowed and preferred, and no fact may appear on screen
unless it is in `facts.md` and the narration.

---

## 1. Creative quality standard

The animation must succeed in three areas:

**Visual design:** It should look professionally composed, distinctive, cohesive, and carefully art-directed.

**Motion design:** It should contain continuous visual progression, expressive transitions, layered movement, and multiple meaningful animated elements.

**Educational value:** It should communicate useful information through visual demonstrations, not simply display a sequence of generic statements.

Do not prioritize one area so heavily that the others become weak.

Avoid producing a collection of pretty graphics that fail to explain the topic.

Equally, avoid presenting useful information in dull, static compositions.

The goal is an explainer that teaches through animation itself.

### Information density

Develop a clear educational narrative that goes beyond a superficial introduction.

Use a concrete scenario, mechanism, comparison, cause-and-effect relationship, or visual demonstration where it improves understanding.

Prioritize specific information over generic labels.

A graphic should ideally demonstrate what is happening, why it happens, or how one step affects another.

Use animated charts, changing diagrams, connected objects, moving indicators, comparisons, highlighted relationships, branching paths, and evolving illustrations where they genuinely help explain the subject.

Do not invent factual statistics or imply that fictional demonstration values are real-world measurements.

### Information hierarchy

Use three levels of communication where useful:

1. A short headline identifying the current idea.
2. A central animated visual showing what happens.
3. Supporting labels, data, or annotations explaining important details.

Do not force all three into every composition.

Use graphics to carry much of the explanation so the animation remains understandable without narration.

Avoid long paragraphs or excessive simultaneous text.

---

## 2. Visual direction: editorial paper cut-out

Create a distinctive handcrafted visual language combining physical paper illustration with sophisticated editorial infographic design.

The animation should look like detailed construction-paper artwork brought to life through professional motion design.

It must be more sophisticated than generic flat vector graphics with a grain overlay.

### Color and materials

Use a restrained palette built around:

- Warm cream: #F3EBDD
- Charcoal: #243139
- Terracotta: #C56B50
- Mustard: #E8B65C
- Sage green: #8A9B7C
- Dusty blue: #7C9DA5
- Pale cardstock: #FFF8EB

Add darker or lighter variations as needed for depth, contrast, and hierarchy.

Use matte paper materials with carefully controlled texture.

Each paper object should have:

- Subtly imperfect cut edges
- A fine, stable fiber texture
- Thin exposed paper edges
- Consistent directional lighting
- Soft shadows indicating depth
- Realistic separation between physical layers

Construct complex illustrations from multiple distinct paper components.

Use overlapping foreground, middle-ground, and background elements.

Aim for convincing shallow physical depth rather than full 3D realism.

Use warm, subtle shadows. Avoid excessive blurring or artificial gloss.

### Real photos inside the paper world

Real photos from `assets/` sit in the paper scene as physical prints: a pale
cardstock border, a soft shadow, sometimes a slight tilt or a paper-tape
corner. Labels and arrows attach to them like paper pieces. Do not apply the
paper texture over the photo itself, and do not recolor it so much that it
stops looking like the real thing.

### Rich illustration design

Create recognizable, detailed illustrations suited to the topic.

Use layered geometry for characters, objects, machines, environments, information panels, and process diagrams.

Illustrations should look deliberately designed, with identifiable parts and thoughtful proportions.

Use more detail where it adds meaning or visual interest.

Avoid overly simplified symbols as the main focus of an entire scene.

Do not fill the screen with unrelated decorative elements.

Each major object should either communicate information, establish the setting, or participate in the visual story.

### Editorial infographic elements

Integrate paper-cut illustrations with sophisticated graphic elements, including:

- Animated information cards
- Callouts and annotations
- Connected process diagrams
- Comparison layouts
- Progress indicators
- Flowing information paths
- Layered charts
- Exploded-view illustrations
- Labels that follow or attach to objects
- Highlighted data and relationships
- Visual transformations representing changing information

Choose elements based on the subject.

Do not add every element to every scene.

Graphics should look integrated into the paper environment rather than pasted over it.

### Typography

Use confident, readable typography as an active part of the composition.

Combine short headlines, carefully positioned labels, and occasional numerical or data-driven elements.

Text can appear on cut-paper banners, physical labels, cards, or directly within the editorial layout.

Use typographic movement to reveal information, emphasize relationships, and guide attention.

Vary typographic scale intentionally.

Avoid tiny explanatory paragraphs and overly complicated text effects.

---

## 3. Motion direction

This is a motion graphics production. Movement is central to the experience.

Do not create static illustrations with entrance animations between them.

Every scene should develop visually and contain several meaningful changes.

### Pacing

Create an energetic, fluid, professionally paced sequence. As a creative
target, aim for a meaningful visual beat every 5-10 seconds; the scenes in
`timeline.json` already mark the main ones.

A visual beat is a noticeable development that advances the explanation:

- New information is revealed.
- An object changes state.
- A diagram expands or transforms.
- A piece of data moves between components.
- A comparison develops.
- A decision changes the path of the story.
- A new paper environment is revealed.

Keep the viewer's attention moving naturally from one piece of information to another.

Avoid long pauses where nothing meaningful changes.

Allow brief holds when viewers need time to read or understand something important.

### Choreography

Use coordinated, overlapping movement rather than animating every object separately in sequence.

When appropriate, multiple elements should animate together.

A headline might reveal as a paper object assembles, with annotations entering shortly afterward and a connecting diagram developing beneath it.

Use staggered timing, anticipation, follow-through, and visual continuity.

Give motion a clear beginning, development, and finish.

Transitions should often grow naturally out of the action already taking place.

Avoid stopping the entire composition before introducing the next scene.

### Paper-specific animation

Use the physical paper medium creatively:

- Cut-out pieces assemble into complex illustrations.
- Layers lift, fold, rotate, slide, and settle.
- Paper objects transform through rearrangement.
- Strips unfold into connected diagrams.
- Paper windows reveal additional details.
- Stacked components separate to expose inner mechanisms.
- Labels appear attached to moving pieces.
- Foreground sheets pass across the composition.
- Paper elements reorganize into a new visual explanation.

Keep material behavior consistent.

Paper can bend or fold when appropriate, but should not behave like liquid or rubber unless the effect is deliberately stylized.

### Smooth motion and stop-motion accents

Use smooth animation for camera movement, typography, diagrams, transitions, and information flow.

Apply subtle stepped stop-motion movement selectively to physical paper pieces when it improves the handcrafted appearance.

Do not force the entire animation to run at 12 unique poses per second.

Use easing functions suited to each action.

Avoid repetitive linear movement, unnecessary bouncing, and identical entrance animations.

### Camera movement

Use a virtual 2D camera where it improves the composition.

Possible movements include:

- Controlled pans
- Short zooms
- Reframing between connected diagrams
- Layered parallax
- Revealing a wider composition
- Following moving information through a process

Camera movement should direct attention and connect ideas.

Do not continuously zoom or move the camera without a reason.

---

## 4. Rendering principles

- Every frame must be drawable from its time alone, without depending on the
  previous frame. This is what lets HyperFrames render frame by frame.
- Generate paper grain with a well-mixed deterministic random function and
  stable seeds. Do not regenerate textures every frame; keep them stable as
  objects move.
- Keep shadows, layering, lighting, and clipping consistent across the
  whole video.
- Draw everything that belongs in the video (text, labels, subtitles when
  burned in) into the rendered composition.
