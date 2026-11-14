# Step 7: Timing

**Role:** you turn the word timings into a scene timeline. This step is a
script run, not writing.

**Input:** `voiceover/` from Step 6, and `assets.md` from Step 5.
**Output:** `timeline.json` in the run folder.

## Method

1. Build the timeline:

   ```bash
   python3 tools/narration.py timeline runs/<run-folder>
   ```

   Each `[visual: ...]` note becomes one scene. A scene starts when the
   narrator says the first word after the note and ends where the next scene
   starts. Chapters play back to back, so times run across the whole video.
2. Check the output:
   - Scene numbers count the visual notes in order across the whole script,
     starting at 1. They are the same numbers `assets.md` uses.
   - A scene with `"scene": null` is narration that has no visual note. List
     these for the animation step; it must plan a visual for them.
   - `"timings": "estimated"` (OpenRouter voice) or a warning that the
     alignment does not match the text means scene times are estimated by
     text position. Report it; that is fine for a test, not for a final.
   - Any scene shorter than about 2 seconds or longer than about 20 seconds:
     list it. The animation step may merge or split it.
3. Compare the scene list with `assets.md`. For each scene, note the cleared
   file, "make it", or "not cleared". Report scenes that are in one file but
   not the other.

## `timeline.json` format

```json
{
  "total_seconds": 512.4,
  "chapters": [{"chapter": 1, "title": "...", "audio": "voiceover/ch01.mp3", "start": 0, "duration": 58.2}],
  "scenes": [{"scene": 1, "chapter": 1, "start": 0, "end": 7.8,
              "visual": "close-up, hands peeling a banana", "narration": "The banana in your kitchen is a copy."}]
}
```

Times are in seconds from the start of the video.
