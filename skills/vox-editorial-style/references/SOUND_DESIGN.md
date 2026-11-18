# Sound Design

These rules are measured in `evidence/AUDIO_SYNC.md`. The SFX files are original and synthesised by `scripts/make-sfx.sh` (ffmpeg only, no downloads or licences).

## Mix targets (measured on V1, V3, V5, V6)

| Item | Target |
|---|---|
| Integrated loudness | -18 to -19 LUFS. For social platforms, -14 to -16 is fine if the framework's sound rules ask for it |
| True peak | -1.5 to -2.5 dBTP |
| Loudness range | 2.5–5 LU (flat). A climax may sit +3–4 LU |
| Voice-over | centred mono |
| Music bed | stereo, **15–23 dB under the voice**, constant, little or no ducking |
| SFX | about 6–10 dB under the voice when narration is present |
| Silence | never true silence mid-video. Chapter breaks: a 0.3–1.3 s near-silent gap → cut → sting → new music cue |

## Timing rules

1. **Cut 2 frames before the next VO phrase starts.** Measured median 57 ms in V1: in narrated pieces, cuts follow the narration, not the music beat.
2. **SFX land on visible actions.** A hit lands on its frame, or 1 frame after (sound never early).
3. **Whooshes and swishes start with their move** and peak at its end, matching ease-in moves.
4. **Density:** 1–6 designed SFX per minute, concentrated at the intro, chapter turns and the outro. Montage bursts get one per cut.
5. **Vary repeated SFX** with deterministic random volume (±0.1) and rate (0.9–1.15) so repeats don't sound identical.

## SFX library (`assets/sfx/`, 48 kHz mono, peak -3 dBFS)

| File | Use | Recipe (see `scripts/make-sfx.sh`) | Suggested volume |
|---|---|---|---|
| `paper-rustle.wav` (0.7 s) | clipping or card lands, page appears | white noise, bandpass 3.5 kHz (2 oct), tremolo 22 Hz, exp tail | 0.5 |
| `stamp-thunk.wav` (0.3 s) | tag, stamp or label snaps into place | 90 Hz sine `exp(-25t)` + noise click | 0.55 |
| `brush-swish.wav` (0.48 s) | dry-brush highlight | pink noise, HP 900 / LP 7 k, tremolo 40 Hz (bristles), quadratic rise 0.42 s, hard stop | 0.9 (main), 0.5 at rate 1.25 (short) |
| `whoosh-snap.wav` (0.25 s) | snap zoom in or out | pink noise, bandpass 1.2 kHz, rise 0.17 s | 0.35–0.45 |
| `whoosh-pan.wav` (0.5 s) | camera pan, whip | pink noise HP 150 / LP 2.2 k, rise 0.33 s | 0.5 |
| `paper-slap.wav` (0.25 s) | each hard cut in a montage burst | 65 Hz `exp(-30t)` + noise `exp(-55t)` | 0.55–0.75 |

## Validated cue sheet (NewspaperDemo @24 fps)

| Frame | SFX | Picture |
|---|---|---|
| 0 | paper-rustle | clipping on screen, headline inks in |
| 20 | stamp-thunk | date tag lands |
| 38 | whoosh-snap | snap zoom in |
| 40 | brush-swish | brush swipe f40–50 |
| 78 | whoosh-snap (rate 0.85) | snap zoom out |
| 86 | whoosh-pan | pan up f86–94 |
| 112 | brush-swish (rate 1.25, vol 0.5) | second, shorter brush |
| 150, 160, 168, 176, 182, 188, 194, 202 | paper-slap | burst cuts |
| 210 | brush-swish | brush on the held headline |

Rendered-audio onsets were measured at frames 20, 39, 79, 88, 114, 150, 160, 168, 176, 182, 188, 194, 202 and 212: within 0–2 f of the cues. Whooshes register late because they swell. These are measured numbers; nobody has listened to the result.

## Music

None is included. Use licensed or generated music: one cue per chapter, a low-pulse ambient bed for explainers, and 85–105 BPM for intros and promos.
