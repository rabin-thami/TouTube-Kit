#!/usr/bin/env bash
# Synthesises the newspaper SFX into public/sfx/ with ffmpeg only (original, no downloads).
# Usage: bash <skill>/scripts/make-sfx.sh [out-dir]
set -euo pipefail
# Run from the Remotion project root. Optional arg: output dir (default public/sfx).
OUT="${1:-public/sfx}"
mkdir -p "$OUT"
FF=(ffmpeg -hide_banner -loglevel error -y)
ENC=(-ac 1 -ar 48000 -c:a pcm_s16le)

# Paper rustle: band-passed white noise with fast irregular amplitude (crinkle), long tail.
"${FF[@]}" -f lavfi -i "anoisesrc=d=0.7:c=white:a=0.6:seed=3" \
  -af "bandpass=f=3500:width_type=o:w=2,tremolo=f=22:d=0.85,afade=t=in:d=0.03,afade=t=out:st=0.2:d=0.5:curve=exp" \
  "${ENC[@]}" "$OUT/paper-rustle.wav"

# Dry-brush swish: pink noise, bristle grit (tremolo), accelerating rise, hard stop (matches ease-in swipe).
"${FF[@]}" -f lavfi -i "anoisesrc=d=0.48:c=pink:a=0.9:seed=7" \
  -af "highpass=f=900,lowpass=f=7000,tremolo=f=40:d=0.4,afade=t=in:d=0.42:curve=qua,afade=t=out:st=0.42:d=0.06" \
  "${ENC[@]}" "$OUT/brush-swish.wav"

# Stamp thunk: 90 Hz decaying body + short noise click.
"${FF[@]}" -f lavfi -i "aevalsrc='0.8*sin(2*PI*90*t)*exp(-t*25)+0.35*(2*random(0)-1)*exp(-t*90)':d=0.3:s=48000" \
  -af "lowpass=f=3000" "${ENC[@]}" "$OUT/stamp-thunk.wav"

# Short whoosh for snap zooms: band-passed noise, quick rise, quick cut.
"${FF[@]}" -f lavfi -i "anoisesrc=d=0.25:c=pink:a=0.9:seed=11" \
  -af "bandpass=f=1200:width_type=o:w=1.5,afade=t=in:d=0.17:curve=qua,afade=t=out:st=0.17:d=0.08" \
  "${ENC[@]}" "$OUT/whoosh-snap.wav"

# Camera pan whoosh: darker, longer.
"${FF[@]}" -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.9:seed=13" \
  -af "highpass=f=150,lowpass=f=2200,afade=t=in:d=0.33:curve=qua,afade=t=out:st=0.33:d=0.17:curve=exp" \
  "${ENC[@]}" "$OUT/whoosh-pan.wav"

# Paper slap for each burst cut: low thump + bright paper transient.
"${FF[@]}" -f lavfi -i "aevalsrc='0.9*sin(2*PI*65*t)*exp(-t*30)+0.6*(2*random(0)-1)*exp(-t*55)':d=0.25:s=48000" \
  -af "lowpass=f=5000" "${ENC[@]}" "$OUT/paper-slap.wav"

# Peak-normalise every file to -3 dBFS so relative levels are set only by `volume` in the cue list.
for f in "$OUT"/*.wav; do
  peak=$(ffmpeg -hide_banner -i "$f" -af volumedetect -f null - 2>&1 | grep -oE 'max_volume: [-0-9.]+' | awk '{print $2}')
  gain=$(awk -v p="$peak" 'BEGIN{print -3 - p}')
  "${FF[@]}" -i "$f" -af "volume=${gain}dB" "${ENC[@]}" "$f.tmp.wav" && mv "$f.tmp.wav" "$f"
done

ls -la "$OUT"
