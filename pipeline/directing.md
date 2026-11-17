# Directing Guide

How to direct a video in Step 8, whatever its look. The style file named
in `brief.md` (`pipeline/styles/<style>.md`) says what the video looks
like; this file says how to make choices: what to aim for, where the peak is, how sound and pace carry the story, and what to
check. `8-animate.md` and `AGENTS.md` win where they disagree with this
file. Adapted from a short-film directing method; its music-grid, character
and map-policy parts are left out because here the voice sets the timing
and real photos carry the story.

A video is judged in this order: **sound, rhythm, camera, staging**.
Good-looking frames are only the start.

## 0. Quality standard (every style)

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

## 1. Benchmark (before the storyboard)

Pick one or two reference works (documentaries, title sequences, explainer
channels, ads) that set the bar for this topic and this style. Choose them
for this video; don't reuse the last video's. Write in `storyboard.md`:

- **Learn:** composition, pacing, camera grammar, colour logic, sound.
- **Don't take:** characters, designs, music, specific shots, logos, fonts.

## 2. One peak, one signature shot

- Find the emotional turn in the script (the reveal, the collapse, the
  twist). That is where the strongest visual goes.
- Plan **one signature shot** people remember: a scale reveal, a long
  unbroken move, or a transition made from the medium itself (for paper: a
  fold, tear or cut that becomes the next scene). Put it at the peak.
- One idea per screen. A gag or image the viewer reads at phone size beats
  three they can't. If a beat needs explaining, remove it.

## 3. Sound is half the video

The voice is the master clock (`8-animate.md`): never move or stretch it.
Everything else is placed around it.

- **Every visible action has a sound** that matches its material (paper,
  wood, metal, glass sound different).
- **Three layers:** a quiet ambience bed per chapter (room, wind, sea,
  market), sound effects tied to actions, and the voice on top. Music only
  if licensed or generated; keep it under the voice.
- **At least two near-silences** before the turn or the peak: drop the bed
  and effects for the `[pause]` before it or the gap between chapters. The
  first sound after the silence should be one of the most important in the
  video.
- **Sound as a transition at least twice:** start the next scene's ambience
  or effect before the cut (J-cut), or let the last scene's sound run over
  it (L-cut).
- Every row of the plan's sound list must be audible in the final mix.

- **Triple alignment in the hook:** in the first seconds, the on-screen
  text, the voice and the picture say the same thing. The hook must read
  with the sound off and make sense with eyes closed. A mismatch makes
  people scroll.

## 4. Rhythm and reading time

- **Vary the pace:** alternate busy and calm scenes, include one clear
  speed-up or slow-down, and give the viewer one breath (a held image).
  A video at one even speed has failed.
- A scene that holds one picture for more than about 15 s needs a new beat
  inside it (a push in, a detail, a label, a second print).
- **Hold text long enough to read:** after on-screen text finishes
  appearing, keep it for at least (letters / 15 + 1.5) s. Title cards stay
  at least 4 s. Subtitles stay at least 1.8 s.
- Make it fast with fewer words per screen, not by cutting before people
  finish reading.

## 5. Camera: every move has a reason

- Use **at least four different camera moves** (push, pull, pan, track,
  parallax, focus change, frame within a frame) and real changes of framing
  (wide, medium, close, insert). List the move and its reason per scene in
  `storyboard.md`.
- **Transitions come from the medium** and follow one consistent grammar.
  No default crossfades or hard cuts unless the style asks for them.
- At key moments the subject fills at least a third of the frame height.

## 6. Not the last video again

The style is reused across videos, so the risk is a copy of the previous
one. Before showing the storyboard, compare it with the last video in the
same style on six points: structure, opening image, signature shot, camera
path, sound shape, ending. **At least four must differ**; rethink the ones
that match.

## 7. Failures we see most

Check every storyboard frame and the final contact frames for these:

- Subject too small, too far away, or pushed against the frame edge.
- Too dark to read, or a colour laid on the same colour (red on red).
- Subtitles or labels covering the subject.
- A reveal or gag too fast to understand.
- Blank or half-empty frames inside transitions.
- A zoom, pin or highlight that no longer lines up with its subject after
  the camera moves.

## 8. Before delivery

- **Loudness about -14 LUFS** (YouTube's playback level), true peak below
  -1 dB. Measure:

  ```bash
  ffmpeg -i video/<name>.mp4 -vn -af loudnorm=print_format=summary -f null - 2>&1 | tail -12
  ```

  If it is off by more than 1 LU, fix the audio only (video untouched):

  ```bash
  ffmpeg -i video/<name>.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k video/<name>-14lufs.mp4
  ```

- **One fix round:** fix everything the checks find in one round, then
  check once more. Anything bigger, tell the user in one line at delivery.
  The user's notes after delivery are new rounds: change only what they ask.
- Export one strong frame as `video/poster.jpg` (thumbnail candidate): the
  signature shot or the peak, subject large, no subtitle on it. The real
  thumbnail follows `brand/STYLE.md`, section 6.

## 9. Rendering principles (every style)

- Every frame must be drawable from its time alone, without depending on the
  previous frame. This is what lets HyperFrames render frame by frame.
- Generate grain and textures with a well-mixed deterministic random function and
  stable seeds. Do not regenerate textures every frame; keep them stable as
  objects move.
- Keep shadows, layering, lighting, and clipping consistent across the
  whole video.
- Draw everything that belongs in the video (text, labels, subtitles when
  burned in) into the rendered composition.
