# Step 6: Voiceover

**Role:** you turn the approved narration into audio with word timings. You
do not change the words.

**Run only when** `brief.md` says `Status: APPROVED`.
**Input:** `script-final.md` and `brief.md` in the run folder.
**Output:** `voiceover/` in the run folder: `chNN.txt`, `chNN.mp3`,
`chNN.alignment.json` for each chapter, and `chapters.json`.

## Before you start

- Read the provider, voice ID, and model ID from the "Voice" line in
  `brief.md`. If it is empty, stop and ask the user. Do not pick a voice
  yourself.

  | Provider | Use for | Key variable | Word timings |
  |---|---|---|---|
  | `openrouter` | Tests and drafts (cheaper) | `OPENROUTER_API_KEY` | No: scene times are estimated from text position, so visuals can land a second or two off the voice |
  | `elevenlabs` | Final videos | `ELEVENLABS_API_KEY` | Yes: scenes start on the exact word |

- Every call costs money. Before the first call in a run, tell the user the
  provider, how many chapters, and how many characters will be sent, and
  wait for a yes. Nobody else can approve this.
- The API key comes from the environment variable only. Never write a key
  into any file, command log, or message.
- Switching provider later (draft on OpenRouter, final on ElevenLabs): delete
  the old `chNN.mp3` files first, then run Steps 6, 7, and the Step 8 build
  again, because every scene time changes.

## Method

1. Split the narration into chapters:

   ```bash
   python3 tools/narration.py split runs/<run-folder>
   ```

   This removes `[F#]`/`[Q#]`/`[C#]` tags and `[visual: ...]` notes from the
   spoken text, turns `[pause]` into a pause, and records where each visual
   note sits. One chapter is one audio file.
2. Read 2-3 of the `chNN.txt` files. Check they hold only words to be spoken:
   no tags, no notes, no markdown.
3. Generate the audio:

   ```bash
   python3 tools/narration.py tts runs/<run-folder> --provider <openrouter|elevenlabs> --voice <voice-id> --model <model-id>
   ```

   Chapters that already have an MP3 are skipped, so a failed run can be
   restarted without paying twice. If a chapter's text changed after its MP3
   was made (a fix round), `tts` and `timeline` stop and name the chapter:
   delete that `chNN.mp3` and run `tts` again. OpenRouter model IDs must be exact dated
   IDs; list them with `GET https://openrouter.ai/api/v1/models?output_modalities=speech`
   and use a voice from the model's `supported_voices`.
4. Listen check: confirm every `chNN.mp3` exists, is not empty, and its length
   is close to the estimate (about 2-2.5 English words per second). A chapter
   far shorter than expected may have been cut off.

## Rules

- Do not reword, shorten, or "fix" the narration. If a line reads badly
  aloud, report it to the user; changes go back through Step 2 and Step 3.
- If the API returns an error, stop and show the error. Do not retry in a
  loop.
- Another voice service can be added to `tools/narration.py` later. With no
  word timings it works like OpenRouter: scene times are estimated.
