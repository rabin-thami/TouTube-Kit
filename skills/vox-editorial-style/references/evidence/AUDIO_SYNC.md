# Audio & Sync Analysis — six Vox-style references

Scope: loudness, pauses, music bed, SFX and cut-to-audio sync. Sources were only read, never modified. No narration or music is transcribed or reproduced.

Tags: **[M]** = measured. **[I]** = inferred from measured features. Confidence: H / M / L.

## Method

| Step | How |
|---|---|
| Loudness | ffmpeg `ebur128=peak=true` (verbose framelog). Gives I, LRA, true peak and the per-100 ms M/S curve (`<KEY>/loudness_curve.tsv`). |
| Silence | `silencedetect` at -35 dB / 0.2 s and at -50 dB / 0.2 s. |
| Narration pauses (VAD) | Mono PCM at 32 kHz, STFT with 1024-sample window and 5 ms hop. The 300–3400 Hz band is smoothed over 50 ms. "Pause" = this band is more than 18 dB below its 95th percentile for at least 150 ms. |
| Bands | 80–250 Hz (bass), 300–3400 Hz (voice), 4–12 kHz (high), saved at 50 ms resolution in `bands_50ms.tsv`. Onsets: log spectral flux with an adaptive median/MAD threshold (z ≥ 4), saved in `onsets.tsv`. |
| Mid/Side split | The VO sits dead centre in every video: Side (L−R) RMS is 11–25 dB below Mid in V1, V3, V5 and V6. So Side ≈ a voice-free **music + SFX stem**. It is used for bed level, ducking, tempo and SFX. Limit: any mono-summed music is invisible in Side. |
| Tempo | Autocorrelation of Side-channel flux over 60–180 BPM, for the whole file and per 20 s window. The AC peak value is a confidence proxy: below 0.1 means no pulse, 0.3 or more means a clear pulse. **ESTIMATE.** |
| SFX | `sfx_salient.tsv` lists bursts where the Side level rises ≥ 8 dB above its 3 s rolling median. Kind comes from attack, length and spectral tilt. Bursts ≥ 12 dB are counted as "strong stings/SFX". Music beats also trigger this detector, so the counts are an upper bound (L). |
| Visual events | Cut times from `cuts.json`. Motion peaks come from `framediff.tsv` mad minus a 1 s median (prominence ≥ max(3, p98)). |
| Sync | For each cut or motion peak, the signed offset to the nearest audio event: global onsets (top 25 % strongest), Side onsets, phrase starts (pause ends) and SFX. **Offsets are compared against a 5000-sample uniform-random baseline.** Onset density is about 3 per second, so ±2 frames already gives a 37–50 % chance hit rate. |

Artifacts are in `audio/<KEY>/`: `audio_stats.json`, `audio_stats2.json`, `sfx_salient.tsv`, `spectrogram.png`, `waveform.png` and `timeline.png`. In `timeline.png`: blue = voice band, orange = Side total, black = Side bass, grey = VAD pause, red = cut, magenta = motion peak, green = SFX candidate. Scripts: `analyze.py`, `analyze2.py`, `salient.py`.

---

## Per-video tables

### Loudness [M]

| Key | Dur s | Integrated LUFS | LRA LU | True peak dBTP | Short-term p10 / p50 / p90 LUFS |
|---|---|---|---|---|---|
| V1_porsche | 196.7 | **-17.2** | 2.7 | -1.5 | -19.1 / -17.7 / -16.6 |
| V2_camera | 7.0 | -22.4 | 3.8 | -3.5 | -25.0 / -22.7 / -21.3 |
| V3_elections | 586.5 | **-19.3** | 5.2 | -2.4 | -22.7 / -19.8 / -17.9 |
| V4_highlight | 16.3 | -31.3 | 4.9 | -15.0 | -34.8 / -31.8 / -30.2 |
| V5_rabbit | 37.6 | -19.5 | 2.6 | -5.1 | -20.9 / -20.0 / -18.5 |
| V6_epigenetics | 51.1 | -18.2 | 5.0 | -1.4 | -20.5 / -18.7 / -15.8 |

- V4 is very quiet: -31 LUFS with a -15 dBTP peak. **[I, M]** This looks like an un-normalized fan re-upload; do not use it as a level reference.
- V6 rises about 4 LU in its second half: short-term level is around -20 LUFS for 0–30 s and around -16 LUFS for 30–40 s. **[M]**
- V3 is flat across ten segments (-19 to -21 LUFS) and drifts about 2 LU quieter at the end. **[M]**

### Pauses and narration pacing [M]

| Key | silencedetect -35 dB / 0.2 s | -50 dB | VAD pauses | Pauses/min | Pause median (IQR) s | Max s | Phrase median / p75 s | % time in pause |
|---|---|---|---|---|---|---|---|---|
| V1 | 8 | 0 | 86 | 26.2 | 0.42 (0.32–0.60) | 1.74 | 1.56 / 2.47 | 22 % |
| V2 | 0 | 0 | 3 | 25.6 | 0.52 | 0.87 | 1.18 / 1.97 | 23 % |
| V3 | 27 | 18 | 318 | 32.5 | 0.23 (0.18–0.37) | 2.46 | 0.71 / 1.70 | 18 % |
| V4 | 10 | 3 | 4 | 14.8 | 0.29 | 1.61 | 2.84 / 5.05 | 15 % |
| V5 | 1 | 0 | 32 | 51.0 | 0.32 (0.23–0.42) | 0.90 | 0.57 / 1.29 | 32 % |
| V6 | 1 | 0 | 18 | 21.1 | 0.22 (0.20–0.25) | 0.33 | 1.04 / 1.52 | 8 % |

- Almost no true digital silence. At -35 dB the detector finds 0–27 gaps, and those are mostly chapter breaks or the end of the file. **[M, H]** A music or room bed fills every narration pause.
- "Phrase" here means voice-active runs between VAD pauses. That is roughly breath groups or clauses, not full sentences. **[I]**

### Music bed, ducking, tempo

All dB values are relative to digital full scale per STFT frame. "Voice-over-bed" = median voice-band level (Mid) during speech minus median Side level during speech. It is a lower bound on how far the VO sits above the bed. "Ducking" = Side level in pauses minus Side level during speech; a positive value would mean the bed rises in the gaps.

| Key | Side − Mid overall dB [M] | Bed coverage [M] | Voice-over-bed dB [M] | Ducking dB [M] | Tempo ESTIMATE (AC strength) | Music presence / character |
|---|---|---|---|---|---|---|
| V1 | -25.0 | 99.9 % | **19.6** | 0.0 | ~142 BPM in 7 of 9 windows (0.12–0.28); 72 BPM in the first window | **[I, M]** Continuous low bed at constant level, not ducked. Weak pulse. Bass swell or sting at about 19 s. Bed drops around 40 s (visible gap in the spectrogram). |
| V2 | +1.5 | 97 % | **-4.7** | n/a | none reliable (0.09) | **[I, M]** Music-forward intro: stereo music is as loud as or louder than the centre. Two hits at 0.05 s and 2.1 s. |
| V3 | -19.2 | 91 % | **15.6** | +2.9 (bed slightly louder in pauses) | Changes by section: 60/120 BPM (0.4–0.5) early; ~95 BPM (0.68) mid; ~63, 68 and 76 BPM later | **[I, M]** Several music cues, one per chapter. Chapters break at ~33.5, 64.5, 185, 209–215, 280, 361–375 and 453–456 s with near-silent gaps (-50 dB) and a sting after them. Tonal pad lines are visible in the spectrogram. |
| V4 | -4.8 | 83 % | 1.2 | +17 (bed mostly drops out when VO pauses) | 86 BPM (0.33) | **[I, L]** Music-heavy short. Ends in a fade to silence (15.1–16.3 s). |
| V5 | -21.5 | 97.5 % | **23.2** | -0.4 | none (0.06–0.07) | **[I, M]** Very low, non-rhythmic ambient bed. Several whoosh/riser events. |
| V6 | -11.6 | 98 % | **5.6** | +10.3 (bed louder in pauses) | **104 BPM (0.34–0.38)**, also visible as bass pulses about 0.57 s apart in the spectrogram | **[I, H]** Prominent rhythmic beat bed. Sustained pads from about 20 s. Bed is loud relative to the VO and partly fills the gaps between phrases. |

Bass band minus voice band during speech (Mid) [M]: V1 +2.6, V2 -5.5, V3 -2.4, V4 -5.7, V5 -6.5, V6 +0.1 dB. V1 and V6 have the heaviest low end. In V1 the low end is mostly in Mid, because Side bass stays around -70 dB.

### SFX candidates [M detection / I classification, confidence L–M]

| Key | Salient Side bursts ≥ 8 dB (per min) | Strong ≥ 12 dB (per min) | Kinds of the ≥ 8 dB bursts (click / hit / swish / whoosh) | Strong-event timestamps (s) |
|---|---|---|---|---|
| V1 | 21 (6.4) | 3 (0.9) | 13 / 6 / 2 / 0 | 0.05 hit, 19.05 hit/sting, 191.4 hit (outro) |
| V2 | 4 (34) | 2 (17) | 0 / 3 / 0 / 1 | 0.05 hit, 2.13 hit |
| V3 | 450 (46) | 116 (11.9) | 171 / 235 / 29 / 15 | 2.57 pop, 3.03 snap (+53 dB), 33.56 whoosh + snap, 35.5 hit, 47.1 riser, 65.0 hit (+27 dB). Full list in `V3_elections/sfx_salient.tsv`. Many 0.5 s-spaced "hits" are music beats at 120 BPM. |
| V4 | 9 (33) | 4 (14.8) | 0 / 7 / 1 / 1 | 6.68 hit, 12.73 hit, 13.42 hit, 14.57 whoosh |
| V5 | 25 (40) | 9 (14.4) | 3 / 14 / 0 / 8 | 0.67 whoosh, 7.86 hit, 15.61 whoosh, 19.3 and 19.6 whoosh, 34.29 whoosh, 36.97 and 37.44 hits (end) |
| V6 | 56 (66) | 14 (16.4) | 25 / 22 / 5 / 4 | 4.74, 5.89, 7.05, 9.35, 10.49, 11.66, 14.24 … (about 1.15 s apart = 2 beats at 104 BPM, so these are **beat accents, not SFX**); 40.49 hit; 48.81 whoosh (outro) |

Interpretation **[I]**:
- Real one-off SFX are sparse: about 1/min in V1, and a few whooshes in V5.
- In V3 and V6 most "events" are music transients.
- A cleaner estimate of designed SFX is **about 1–6 per minute**, clustered at the intro, chapter transitions and the outro.

### Sync statistics [M]

"Hit" = within ±2 video frames. Baseline = the same measure for random times. Lift = hit rate divided by baseline.

| Key | Cuts | Cut→strong onset hit / base | Cut→phrase start hit / base | Median signed offset, phrase start − cut (ms) | Cuts inside a VO pause / % time in pause | Cut within ±250 ms of a pause / random | Cut has SFX burst within ±6 frames |
|---|---|---|---|---|---|---|---|
| V1 | 102 | 17.6 % / 9.5 % (1.9×) | **21.6 % / 6.5 % (3.3×)** | **+57** (VO resumes about 2 frames after the cut) | **45 % / 22 %** | **65 % / 43 %** | 4 % |
| V2 | 10 | 10 % / 4 % | 10 % / 4 % | -29 | 30 % / 23 % | 60 % / 44 % | 0 % |
| V3 | 93 | 12.9 % / 13.7 % (1.0×) | 9.7 % / 9.1 % (1.0×) | +50 | 25 % / 18 % | 39 % / 38 % | 46 % (baseline-level; dense music events) |
| V4 | 1 | n/a (1 cut, 10 fps) | — | — | 0 % | 0 % | 0 % |
| V5 | 12 | 8 % / 11 % | 17 % / 12 % | +81 | **67 % / 32 %** | 83 % / 68 % | 25 % |
| V6 | 19 | 15.8 % / 13.6 % (1.2×) | 0 % / 6 % | -474 (cuts fall mid-phrase) | **0 % / 8 %** | 0 % / 24 % | 53 % (beat accents) |

Motion-energy peaks (V1 n=88, V3 n=174, V5 n=19, V6 n=18) give nearly identical results:
- V1: 21.6 % of motion peaks fall within ±2 frames of a phrase start, against a 5.9 % baseline.
- Motion → Side onsets: 39–53 % hit, against a 39–58 % baseline, i.e. no lift.

Chapter transitions in V3 [M]: the near-silent gaps end at 64.9, 185.1, 280.1 and 362.5 s. A cut lands **0.07–0.45 s after each gap ends**, and a sting or hit sits on or just after the cut (for example 65.0 s, +27 dB).

---

## Cross-video synthesis — reusable rules

### Loudness / mix
1. **Target -18 to -19 LUFS integrated, true peak about -1.5 to -2.5 dBTP, LRA 2.5–5 LU.** [M: V1, V3, V5, V6 span -17.2 to -19.5 LUFS and -1.4 to -5.1 dBTP] Confidence H. This is louder than the -23/-24 broadcast spec, typical of YouTube masters.
2. **Keep it flat.** Short-term p10–p90 spread is only 2.5–5 LU. Avoid big dynamic swings, except a +3–4 LU lift for a climax section (as in V6). [M] H.
3. **Centre the VO in mono; put music and SFX in stereo.** Side sits 11–25 dB below Mid. [M] H.
4. **Music bed level vs voice:**
   - Dialogue-led explainers (V1, V3, V5) keep the stereo bed **about 15–23 dB below the voice band**. [M] H
   - Beat-driven short pieces (V6, V2, V4) keep it only **about 0–6 dB below**. [M] H
   - Practical default for a narrated explainer: bed at about **-16 to -20 dB relative to the VO**, which is roughly -36 to -40 LUFS short-term under a -19 LUFS VO. [I] M
5. **Little or no ducking.** V1 and V5 show 0 dB, V3 +3 dB. Beds are mixed low and constant rather than sidechained. In V6 the bed comes up about 10 dB in the gaps, which reads as the music "answering" the VO. [M/I] M
6. **Never let it go to true silence mid-video.** At -50 dB there are zero gaps in V1, V5 and V6, and V3's only gaps are deliberate chapter-break gaps of 0.2–1.3 s. [M] H

### Narration pacing
7. **About 20–33 pauses per minute** (V5 outlier: 51/min). Typical pause **0.2–0.45 s**; long "beat" pauses of **1.1–2.5 s** only at section turns. [M] H
8. **Speech runs (breath groups) median 0.6–1.6 s, p75 1.3–2.5 s.** Pauses take **8–23 %** of runtime. [M] H
9. **Mark chapter breaks with a near-silent gap of 0.3–1.3 s.** In V3 these gaps reach about -50 dB. Follow the gap with a new music cue at a different tempo, a cut, and a sting. [M: V3] M–H

### Music
10. **Use one cue per section.** V3 changes tempo by chapter (60/120, 95, 63–76 BPM). Short pieces use one cue: 104 BPM in V6, about 86 in V4. [M] M
11. **Pick tempo by role.** Explainer beds are low-pulse or ambient (V1 AC ≤ 0.28, V5 AC 0.07). Promo or intro beds are rhythmic, 85–105 BPM, with clear beats. [M/I] M
12. **Bass stings mark key moments.** Examples: V1 at 19 s, coinciding with two cuts and a motion peak; V3 chapter openers. [M] M

### SFX
13. **Use designed SFX sparingly: about 1–6 per minute** of clear one-off hits, whooshes or pops. Concentrate them at the intro (first 0–3 s), chapter transitions and the outro (last 2–5 s). Rhythmic accents come from the music, not from SFX. [I from M] L–M
14. Whooshes and risers (attack over 150 ms) lead into transitions. V5 has whooshes at 0.67, 15.6, 19.3 and 34.3 s. Short hits land on reveals. [M/I] L

### Cut-to-audio sync
15. **Cuts are not frame-locked to music beats or generic audio onsets.** Across V1, V3, V5 and V6, cut→onset hit rates are at or just above the random baseline (1.0–1.9×). [M] H. Do not snap every cut to the beat.
16. **Cuts follow the narration.** In VO-led pieces (V1, V5), cuts fall in or right next to VO pauses 1.5–2× more often than chance (V1: 45 % vs 22 %; V5: 67 % vs 32 %). The new shot typically appears **about 50–80 ms (1.5–2.5 frames at 30 fps) before the next phrase starts**. In V1, 3.3× more cuts than chance land within ±2 frames of a phrase start. [M] M–H. **Rule: cut at the end of the pause, 2 frames before the VO resumes.**
17. **Exception: in music-driven pieces (V6), cuts land mid-phrase** (0 % in pauses; nearest phrase start about 470 ms away). There, cuts follow the music bar rather than the speech. [M] M
18. **Major transitions follow a fixed order:** VO stops → 0.3–1.3 s low-level gap → cut 0.07–0.45 s after the gap → sting or hit on the cut → new music cue. [M: V3 ×4] M
19. **Motion peaks behave like cuts**, with no extra audio lock. Animate on the phrase, not on the onset. [M] M

## Caveats
- Cut lists come from automatic detection. V3 likely under-counts animated transitions (93 cuts in 586 s), and V4 (10 fps) has 1 cut, so V4's sync numbers are meaningless.
- The Side-channel stem misses mono music and SFX, and catches stereo reverb of the VO. SFX labels come from heuristics (attack, length, tilt) without listening.
- The VAD is level-based. Loud beds (V6, V2, V4) shorten or hide pauses.
- Tempo values are autocorrelation estimates. Half- or double-time ambiguity is possible (for example V1 at 72 vs 142 BPM).
